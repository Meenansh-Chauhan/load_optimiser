# Load Optimiser 🚚📦

![Python](https://img.shields.io/badge/Python-3.10+-yellow?style=for-the-badge&logo=python)
![NumPy](https://img.shields.io/badge/NumPy-blue?style=for-the-badge&logo=numpy)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-orange?style=for-the-badge)

An algorithmic Python script designed to solve the 3D Bin Packing Problem. **Load Optimiser** intelligently calculates how to pack an assortment of boxes into a given container space, optimizing for maximum volume utilization using a custom Wall-Building packing strategy, and visually renders the result in 3D.

## 🌟 Key Features
- **Algorithmic Efficiency:** Custom Python-based load optimization algorithm using a Skyline Wall-Building heuristic.
- **Data Visualization:** Built-in 3D rendering of the loaded truck/container using `matplotlib`.
- **Standalone Simplicity:** No complex web servers or frontend frameworks. Just pure, mathematical Python code.

## 🛠️ Technology Stack
- **Language:** Python
- **Algorithm & Math:** NumPy
- **Algorithm Visualization:** Matplotlib (Python 3D Plotting)

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Meenansh-Chauhan/load_optimiser.git
cd load_optimiser
```

### 2. Setup your Environment
```bash
# Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate

# Install dependencies
pip install matplotlib numpy
```

### 3. Run the Optimization
```bash
python main.py
```
This will run the algorithm using the hardcoded test boxes and container dimensions. Once finished, a Matplotlib window will open showing a 3D visualization of the optimal packing layout!

## 📁 Project Structure
```
Load-Optimiser/
├── main.py          # Entry point — run this to execute the optimizer
├── config.py        # Truck dimensions & box generation (input data)
├── models.py        # Data structures (Box, SkylineSegment)
├── skyline.py       # Skyline merge & update logic
├── optimizer.py     # Core wall-building packing algorithm
├── visualizer.py    # 3D Matplotlib rendering
├── .gitignore
└── README.md
```

## 🧠 How The Algorithm Works
The core logic implements a greedy Skyline Wall-Building Strategy:
1. **Sorting:** Boxes are prioritized by surface area and volume to form strong foundational layers.
2. **Skyline Management:** The algorithm keeps track of the "skyline" height of placed boxes to support progressive stacking.
3. **Wall Building:** Boxes are placed systematically along the length of the container, filling the width and height (X-Z plane) progressively slice by slice.
4. **Orientation:** Each box is dynamically evaluated across orientations to find the most space-efficient fit.

---
*Created by [Meenansh Chauhan](https://github.com/Meenansh-Chauhan)*
