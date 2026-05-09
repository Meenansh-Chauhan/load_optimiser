from models import SkylineSegment

# ==========================================
# SKYLINE MANAGEMENT
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
