import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random
import copy

# ==========================================
# 1. INPUT DATA (Hardcoded)
# ==========================================

# Example Truck Dimensions
# REFACTORED: X = Width, Y = Length, Z = Height
TRUCK_W = 500   # Width (X)
TRUCK_L = 1000  # Length (Y)
TRUCK_H = 500   # Height (Z)

# Example Boxes
# Generates a mix of sizes for testing
RAW_BOXES = []
random.seed(42)  # Deterministic generation
for i in range(200):
    RAW_BOXES.append({
        "id": i + 1,
        "L": random.randint(50, 200),
        "W": random.randint(50, 200),
        "H": random.randint(50, 200)
    })

# ==========================================
# DATA STRUCTURES
# ==========================================

class Box:
    def __init__(self, raw_data):
        self.id = raw_data['id']
        dims = sorted([raw_data['L'], raw_data['W'], raw_data['H']])
        
        # 3. ORIENTATION (Mandatory Rule for Stability/Packing)
        # We want to align dimensions to TRUCK axes to maximize fit.
        # Usually:
        # dx aligns with TRUCK_W (X)
        # dy aligns with TRUCK_L (Y)
        # dz aligns with TRUCK_H (Z)
        
        # Simple heuristic: align largest dim with largest truck dim?
        # Or standard orientation constraints.
        # Let's keep the previous logic but adapted:
        # X = Width (500), Y = Length (1000), Z = Height (500)
        
        # Heuristic: Min dim to Z (height) to keep com low? Or Max dim to Y (Length) to minimize strips?
        # Let's try: Max dim along Y (Length), Min dim along X (Width).
        
        # PREVIOUS LOGIC: X=Max, Z=Min, Y=Mid
        # NEW LOGIC Request: "fill out the xaxis first (first base)... truck width"
        
        self.dx = dims[1] # Mid dimension to Width (X)
        self.dy = dims[2] # Max dimension to Length (Y) - packing long boxes along length
        self.dz = dims[0] # Min dimension to Height (Z)
        
        # Note: Ideally, specific box orientation should be flexible during packing,
        # but for this script we fix it per box instant.
        
        self.vol = self.dx * self.dy * self.dz
        
        self.orig_dims = [raw_data['L'], raw_data['W'], raw_data['H']]
        
        # Position (to be set)
        self.x = 0
        self.y = 0
        self.z = 0

    def get_face_area_xz(self):
        # Area in the Wall plane (X-Z)
        return self.dx * self.dz

    def __repr__(self):
        return f"Box(id={self.id}, dx={self.dx}, dy={self.dy}, dz={self.dz})"

class SkylineSegment:
    def __init__(self, start, end, height):
        self.start = start
        self.end = end
        self.height = height
        self.width = end - start

    def __repr__(self):
        return f"[{self.start}-{self.end}, h={self.height}]"

# ==========================================
# 2. SORTING
# ==========================================

def sort_boxes(boxes):
    # Sort descending by Face Area (X*Z) to fill walls efficiently?
    # Or by Height?
    # Let's stick to Face Area descending.
    return sorted(boxes, key=lambda b: b.get_face_area_xz(), reverse=True)

# ==========================================
# 4. SKYLINE MANAGEMENT
# ==========================================

def merge_skyline(skyline):
    """Merges adjacent segments with equal height."""
    if not skyline:
        return []
    
    merged = []
    current = skyline[0]
    
    for i in range(1, len(skyline)):
        next_seg = skyline[i]
        if current.height == next_seg.height and current.end == next_seg.start:
            # Merge
            current = SkylineSegment(current.start, next_seg.end, current.height)
        else:
            merged.append(current)
            current = next_seg
    merged.append(current)
    return merged

def update_skyline(skyline, place_x, place_width, place_height):
    """
    Updates the skyline after placing a box.
    The box covers [place_x, place_x + place_width] at 'place_height'.
    """
    new_skyline = []
    place_end = place_x + place_width
    
    for seg in skyline:
        # Case 1: Segment is completely to the left
        if seg.end <= place_x:
            new_skyline.append(seg)
        # Case 2: Segment is completely to the right
        elif seg.start >= place_end:
            new_skyline.append(seg)
        # Case 3: Overlap
        else:
            # Left part of segment (if any)
            if seg.start < place_x:
                new_skyline.append(SkylineSegment(seg.start, place_x, seg.height))
            
            # Right part of segment (if any)
            if seg.end > place_end:
                new_skyline.append(SkylineSegment(place_end, seg.end, seg.height))
                
    # Insert the new segment for the box
    new_seg = SkylineSegment(place_x, place_end, place_height)
    
    # Insert and resort
    final_skyline = []
    inserted = False
    
    if not new_skyline:
        final_skyline = [new_seg]
    else:
        for seg in new_skyline:
            if not inserted and seg.start > new_seg.start:
                final_skyline.append(new_seg)
                inserted = True
            final_skyline.append(seg)
        if not inserted:
            final_skyline.append(new_seg)
        
    return merge_skyline(final_skyline)

# ==========================================
# 5. CORE ALGORITHM & WALL BUILDING
# ==========================================

def optimize_load(truck_w, truck_l, truck_h, raw_boxes):
    # TRUCK_W is X-axis limit
    # TRUCK_H is Z-axis limit
    # TRUCK_L is Y-axis limit
    
    all_boxes = [Box(b) for b in raw_boxes]
    sorted_boxes = sort_boxes(all_boxes)
    
    placed_boxes = []
    
    current_y = 0
    
    # Wall Building Loop: Move along Y axis
    while sorted_boxes and current_y < truck_l:
        
        # Initial Skyline for the WALL (along X-axis)
        skyline = [SkylineSegment(0, truck_w, 0)]
        wall_max_y_thickness = 0
        boxes_placed_in_wall = False
        
        # Fill this wall (X-Z plane)
        # Keep trying to place boxes until no box fits in this wall
        while True:
            best_placement = None
            best_box_idx = -1
            
            # IMPROVEMENT: Check ALL skyline segments, not just lowest
            # Sort segments by height to prioritize lower spots, but consider all
            skyline_indices = sorted(range(len(skyline)), key=lambda i: skyline[i].height)
            
            found_fit = False
            
            for idx in skyline_indices:
                if found_fit: break
                
                seg = skyline[idx]
                
                # Check neighbors for smoothing (creating a flat platform)
                # Look for contiguous segment sequence with same or lower height?
                # For simplicity, we strictly place ON TOP of 'seg' or merged plain.
                # Let's stick to the current segment 'seg' as the base.
                # Width available is seg.width (plus potentially neighbors if we implemented rigorous merging lookahead).
                # Current simple logic: specific segment.
                
                # RE-ADD "Progressive Support Smoothing" logic from original code?
                # Original code logic: merge with adjacent "next lowest".
                # Let's simplify: Just try to place on 'seg'.
                # If 'seg' is too small, maybe we can bridge?
                # Bridging is risky without full support.
                # Let's Stick to: Box must fit within the width of the segment (or we merge segments if they are same height).
                
                # Actually, the original code had "merge with neighbors". Let's reinstate a simple version.
                # Try to form a support platform starting at 'idx'.
                
                platform_start = seg.start
                platform_end = seg.end
                platform_h = seg.height
                
                # Try to extend right
                for right_i in range(idx + 1, len(skyline)):
                    if skyline[right_i].height == platform_h:
                        platform_end = skyline[right_i].end
                    else:
                        break
                # Try to extend left
                for left_i in range(idx - 1, -1, -1):
                    if skyline[left_i].height == platform_h:
                        platform_start = skyline[left_i].start
                    else:
                        break
                        
                platform_width = platform_end - platform_start
                
                # Iterate all boxes to find best fit
                for b_i, box in enumerate(sorted_boxes):
                    
                    # 1. Fits in Width (X)
                    if box.dx > platform_width:
                        continue
                    
                    # 2. Fits in Height (Z)
                    if platform_h + box.dz > truck_h:
                        continue
                    
                    # 3. Fits in Length (Y) - truck boundary
                    if current_y + box.dy > truck_l:
                        continue
                    
                    # FOUND A PLACEMENT
                    best_box_idx = b_i
                    best_placement = {
                        'x': platform_start,
                        'y': current_y,
                        'z': platform_h,
                        'box': box
                    }
                    found_fit = True
                    break
            
            if found_fit and best_placement:
                # Place the box
                box = sorted_boxes.pop(best_box_idx)
                
                box.x = best_placement['x']
                box.y = best_placement['y']
                box.z = best_placement['z']
                
                placed_boxes.append(box)
                
                # Update Skyline
                new_h = box.z + box.dz
                skyline = update_skyline(skyline, box.x, box.dx, new_h)
                
                # Update wall thickness (Y consumption)
                wall_max_y_thickness = max(wall_max_y_thickness, box.dy)
                boxes_placed_in_wall = True
                
            else:
                # No box fits in any segment of this wall
                break
        
        # End of Wall filling
        
        if not boxes_placed_in_wall:
            # Could not place ANY box in a fresh wall starting at current_y
            # Means all remaining boxes don't fit in remaining Length OR are too wide/tall for empty truck?
            break
            
        # Move Y forward
        # Ideally: we should have a "Frontier" in Y, but here we move by slices (Stripy)
        # To "Smoothen" Y: we effectively just stack these walls.
        # Improvement: minimize gap?
        # Current logic: `current_y += wall_max_y_thickness`
        # This implies the NEXT wall starts at the furthest point of THIS wall.
        # This leaves gaps if some boxes in this wall were short in Y.
        # But for "Rigid Wall" approach, this is standard.
        
        current_y += wall_max_y_thickness
    
    return placed_boxes, sorted_boxes

# ==========================================
# 8. VISUALIZATION
# ==========================================

def visualize_load(placed_boxes, truck_w, truck_l, truck_h, unplaced_count):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Draw Truck Wireframe (X=Width, Y=Length, Z=Height)
    # 0 to TRUCK_W, 0 to TRUCK_L, 0 to TRUCK_H
    
    # Vertices for box (0,0,0) to (W, L, H)
    
    # Plot edges
    # X axis lines
    ax.plot([0, truck_w], [0, 0], [0, 0], 'k-') # Bottom-Front
    ax.plot([0, truck_w], [truck_l, truck_l], [0, 0], 'k-') # Bottom-Back
    ax.plot([0, truck_w], [0, 0], [truck_h, truck_h], 'k-') # Top-Front
    ax.plot([0, truck_w], [truck_l, truck_l], [truck_h, truck_h], 'k-') # Top-Back
    
    # Y axis lines
    ax.plot([0, 0], [0, truck_l], [0, 0], 'k-')
    ax.plot([truck_w, truck_w], [0, truck_l], [0, 0], 'k-')
    ax.plot([0, 0], [0, truck_l], [truck_h, truck_h], 'k-')
    ax.plot([truck_w, truck_w], [0, truck_l], [truck_h, truck_h], 'k-')
    
    # Z axis lines
    ax.plot([0, 0], [0, 0], [0, truck_h], 'k-')
    ax.plot([truck_w, truck_w], [0, 0], [0, truck_h], 'k-')
    ax.plot([0, 0], [truck_l, truck_l], [0, truck_h], 'k-')
    ax.plot([truck_w, truck_w], [truck_l, truck_l], [0, truck_h], 'k-')

    # Draw Boxes
    colors = plt.cm.jet(np.linspace(0, 1, len(placed_boxes)))
    random.shuffle(colors)
    
    for i, box in enumerate(placed_boxes):
        # ax.bar3d(x, y, z, dx, dy, dz)
        ax.bar3d(box.x, box.y, box.z, box.dx, box.dy, box.dz, 
                 color=colors[i], edgecolor='black', alpha=0.8, linewidth=0.5)
        
    ax.set_xlabel('Width (X)')
    ax.set_ylabel('Length (Y)')
    ax.set_zlabel('Height (Z)')
    ax.set_title(f"3D Truck Load Optimization (Wall Strategy)\nPlaced: {len(placed_boxes)} | Unplaced: {unplaced_count}")
    
    ax.set_xlim(0, truck_w)
    ax.set_ylim(0, truck_l)
    ax.set_zlim(0, truck_h)
    
    # Calculate Utilization
    total_vol = truck_w * truck_l * truck_h
    used_vol = sum(b.vol for b in placed_boxes)
    util_pct = (used_vol / total_vol) * 100
    
    ax.text2D(0.05, 0.95, f"Volume Util: {util_pct:.2f}%", transform=ax.transAxes)
    
    plt.show()

# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":
    print("Starting Optimization (Wall-Building Strategy)...")
    placed, unplaced = optimize_load(TRUCK_W, TRUCK_L, TRUCK_H, RAW_BOXES)
    
    print("\nOptimization Complete.")
    print("----------------------")
    print(f"Total Boxes: {len(RAW_BOXES)}")
    print(f"Placed: {len(placed)}")
    print(f"Unplaced: {len(unplaced)}")
    
    total_vol = TRUCK_W * TRUCK_L * TRUCK_H
    used_vol = sum(b.vol for b in placed)
    print(f"Volume Utilization: {(used_vol/total_vol)*100:.2f}%")
    
    if placed:
        print("\nDisplaying Visualization...")
        visualize_load(placed, TRUCK_W, TRUCK_L, TRUCK_H, len(unplaced))
