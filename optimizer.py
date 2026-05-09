from models import Box, SkylineSegment
from skyline import update_skyline

# ==========================================
# SORTING
# ==========================================

def sort_boxes(boxes):
    # Sort descending by Face Area (X*Z) to fill walls efficiently?
    # Or by Height?
    # Let's stick to Face Area descending.
    return sorted(boxes, key=lambda b: b.get_face_area_xz(), reverse=True)

# ==========================================
# CORE ALGORITHM & WALL BUILDING
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
