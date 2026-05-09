import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random

# ==========================================
# VISUALIZATION
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
