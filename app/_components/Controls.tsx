"use client";

import { useState } from 'react';

export function Controls({ onVisualize, loading }) {
  const [container, setContainer] = useState({ L: 300, W: 200, H: 180 });
  const [boxes, setBoxes] = useState([
    { id: 1, L: 60, W: 40, H: 30 },
    { id: 2, L: 50, W: 50, H: 40 },
    { id: 3, L: 70, W: 60, H: 20 },
    { id: 4, L: 30, W: 30, H: 30 },
    { id: 5, L: 90, W: 40, H: 50 },
    { id: 6, L: 40, W: 40, H: 40 },
    { id: 7, L: 100, W: 60, H: 30 },
    { id: 8, L: 20, W: 20, H: 20 },
    { id: 9, L: 80, W: 50, H: 25 },
    { id: 10, L: 45, W: 35, H: 30 },
  ]);

  const handleContainerChange = (e) => {
    setContainer({ ...container, [e.target.name]: Number(e.target.value) });
  };

  const handleBoxChange = (index, e) => {
    const newBoxes = [...boxes];
    newBoxes[index] = { ...newBoxes[index], [e.target.name]: Number(e.target.value) };
    setBoxes(newBoxes);
  };

  const addBox = () => {
    const newId = boxes.length > 0 ? Math.max(...boxes.map(b => b.id)) + 1 : 1;
    setBoxes([...boxes, { id: newId, L: 10, W: 10, H: 10 }]);
  };

  const removeBox = (index) => {
    setBoxes(boxes.filter((_, i) => i !== index));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onVisualize({ container, boxes });
  };

  return (
    <div className="absolute top-4 left-4 bg-white/80 backdrop-blur-sm p-4 rounded-lg shadow-lg text-black z-10 max-w-sm">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <h2 className="text-lg font-bold">Container</h2>
          <div className="grid grid-cols-3 gap-2">
            <label>L: <input className="w-full p-1 border rounded" type="number" name="L" value={container.L} onChange={handleContainerChange} /></label>
            <label>W: <input className="w-full p-1 border rounded" type="number" name="W" value={container.W} onChange={handleContainerChange} /></label>
            <label>H: <input className="w-full p-1 border rounded" type="number" name="H" value={container.H} onChange={handleContainerChange} /></label>
          </div>
        </div>

        <div>
          <h2 className="text-lg font-bold">Boxes</h2>
          <div className="max-h-60 overflow-y-auto space-y-2 p-1">
            {boxes.map((box, index) => (
              <div key={index} className="flex items-center gap-2">
                <span className="font-semibold">#{box.id}</span>
                <label>L: <input className="w-14 p-1 border rounded" type="number" name="L" value={box.L} onChange={(e) => handleBoxChange(index, e)} /></label>
                <label>W: <input className="w-14 p-1 border rounded" type="number" name="W" value={box.W} onChange={(e) => handleBoxChange(index, e)} /></label>
                <label>H: <input className="w-14 p-1 border rounded" type="number" name="H" value={box.H} onChange={(e) => handleBoxChange(index, e)} /></label>
                <button type="button" onClick={() => removeBox(index)} className="text-red-500 hover:text-red-700 font-bold text-lg">&times;</button>
              </div>
            ))}
          </div>
          <button type="button" onClick={addBox} className="mt-2 w-full bg-gray-200 hover:bg-gray-300 text-gray-800 py-1 rounded">Add Box</button>
        </div>
        
        <button type="submit" disabled={loading} className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded disabled:bg-blue-300">
          {loading ? 'Loading...' : 'Visualize'}
        </button>
      </form>
    </div>
  );
}
