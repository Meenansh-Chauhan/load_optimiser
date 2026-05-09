# Load Optimiser 🚚📦

![Next.js](https://img.shields.io/badge/Next.js-16.0-black?style=for-the-badge&logo=next.js)
![React](https://img.shields.io/badge/React-19.2-blue?style=for-the-badge&logo=react)
![Three.js](https://img.shields.io/badge/Three.js-3D-white?style=for-the-badge&logo=three.js)
![Python](https://img.shields.io/badge/Python-3.10+-yellow?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-API-black?style=for-the-badge&logo=flask)

A full-stack algorithmic web application designed to solve the 3D Bin Packing Problem. **Load Optimiser** allows logistics users to intelligently pack an assortment of boxes into a given container space, optimizing for maximum volume utilization and stability using a custom Wall-Building packing strategy.

## 🌟 Key Features
- **Algorithmic Efficiency:** Custom Python-based load optimization algorithm using a Skyline Wall-Building heuristic.
- **Interactive 3D Visualization:** Seamless, interactive 3D rendering of the loaded truck/container in the browser using React Three Fiber.
- **Full-Stack Architecture:** Next.js frontend seamlessly communicating with a robust Flask (Python) REST API.
- **Dynamic Configuration:** Real-time optimization response capable of handling hundreds of varied boxes with multiple orientation capabilities.

## 🛠️ Technology Stack
- **Frontend:** Next.js (App Router), React, Tailwind CSS
- **3D Graphics:** Three.js, React Three Fiber, Drei
- **Backend:** Python, Flask
- **Algorithm Visualization (Standalone):** Matplotlib (Python 3D Plotting)

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Meenansh-Chauhan/Load-Optimiser.git
cd Load-Optimiser
```

### 2. Start the Python Backend (Flask API)
The optimization algorithm runs on a Flask server.
```bash
# Navigate to the scripts directory
cd scripts

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (Flask)
pip install Flask

# Run the backend server
python main.py
```
The API will run locally at `http://127.0.0.1:5328/pack`.

### 3. Start the Next.js Frontend
Open a new terminal window at the root of the project.
```bash
# Install Node dependencies
npm install

# Start the Next.js development server
npm run dev
```
Navigate to `http://localhost:3000` in your browser to interact with the application.

## 🧠 How The Algorithm Works
The core logic implements a greedy Skyline Wall-Building Strategy:
1. **Sorting:** Boxes are prioritized by surface area and volume to form strong foundational layers.
2. **Skyline Management:** The algorithm keeps track of the "skyline" height of placed boxes to support progressive stacking.
3. **Wall Building:** Boxes are placed systematically along the length of the container, filling the width and height (X-Z plane) progressively slice by slice.
4. **Orientation:** Each box is dynamically evaluated across up to 6 orientations to find the most space-efficient fit.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

---
*Created by [Meenansh Chauhan](https://github.com/Meenansh-Chauhan)*
