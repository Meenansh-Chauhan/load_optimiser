from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def main(container, boxes):
    """
    Runs the packing algorithm and returns the results.
    """
    orientations = [
        ("L", "W", "H"),
        ("L", "H", "W"),
        ("W", "L", "H"),
        ("W", "H", "L"),
        ("H", "L", "W"),
        ("H", "W", "L"),
    ]

    freeSpaces = [
        {
            "x": 0,
            "y": 0,
            "z": 0,
            "L": container["L"],
            "W": container["W"],
            "H": container["H"],
        }
    ]

    def volume(L, W, H):
        return L * W * H

    def score(box):
        L, W, H = box["L"], box["W"], box["H"]
        vol = volume(L, W, H)
        max_dim = max(L, W, H)
        surface_area = 2 * (L * W + W * H + H * L)
        return vol * 0.7 + max_dim * 0.2 + surface_area * 0.1

    def best_fit_score(fs, l, w, h):
        unused_volume = fs["L"] * fs["W"] * fs["H"] - (l * w * h)
        side_fit_penalty = (fs["L"] - l) + (fs["W"] - w) + (fs["H"] - h)
        return unused_volume + 0.5 * side_fit_penalty

    def split_space(fs, x, y, z, l, w, h):
        new_spaces = []
        # 1. Right space
        if fs["L"] - l > 0:
            new_spaces.append(
                {
                    "x": x + l,
                    "y": y,
                    "z": z,
                    "L": fs["L"] - l,
                    "W": fs["W"],
                    "H": fs["H"],
                }
            )
        # 2. Front space
        if fs["W"] - w > 0:
            new_spaces.append(
                {
                    "x": x,
                    "y": y + w,
                    "z": z,
                    "L": fs["L"],
                    "W": fs["W"] - w,
                    "H": fs["H"],
                }
            )
        # 3. Above space
        if fs["H"] - h > 0:
            new_spaces.append(
                {
                    "x": x,
                    "y": y,
                    "z": z + h,
                    "L": fs["L"],
                    "W": fs["W"],
                    "H": fs["H"] - h,
                }
            )
        return new_spaces

    sorted_boxes = sorted(boxes, key=score, reverse=True)
    placements = []
    unplaced = []

    for box in sorted_boxes:
        best_score = float("inf")
        best_choice = None
        best_fs_index = -1

        for i, fs in enumerate(freeSpaces):
            for a, b, c in orientations:
                l, w, h = box[a], box[b], box[c]
                if l <= fs["L"] and w <= fs["W"] and h <= fs["H"]:
                    score_value = best_fit_score(fs, l, w, h)
                    if score_value < best_score:
                        best_score = score_value
                        best_choice = (fs, l, w, h, a, b, c)
                        best_fs_index = i

        if best_choice is None:
            unplaced.append(box)
            continue

        fs, l, w, h, a, b, c = best_choice
        x, y, z = fs["x"], fs["y"], fs["z"]

        placements.append(
            {
                "id": box["id"],
                "x": x,
                "y": y,
                "z": z,
                "L": l,
                "W": w,
                "H": h,
                "rotation": (a, b, c),
            }
        )

        # Remove used fs and add new ones
        used_fs = freeSpaces.pop(best_fs_index)
        new_spaces = split_space(used_fs, x, y, z, l, w, h)
        freeSpaces.extend(new_spaces)

    return {"placements": placements, "unplaced": unplaced, "container": container}

@app.route('/pack', methods=['POST'])
def pack():
    data = request.get_json()
    if not data or 'container' not in data or 'boxes' not in data:
        return jsonify({"error": "Missing container or boxes data"}), 400
    
    container = data['container']
    boxes = data['boxes']
    
    result = main(container, boxes)
    
    return jsonify(result)

if __name__ == "__main__":
    app.run(port=5328, debug=True)
