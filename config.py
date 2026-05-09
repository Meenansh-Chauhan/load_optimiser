import random

# ==========================================
# INPUT DATA (Hardcoded)
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
