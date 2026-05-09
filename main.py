from config import TRUCK_W, TRUCK_L, TRUCK_H, RAW_BOXES
from optimizer import optimize_load
from visualizer import visualize_load

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
