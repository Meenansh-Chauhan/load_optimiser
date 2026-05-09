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
