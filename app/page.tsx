"use client";
import { OrbitControls, Sky } from '@react-three/drei';
import { Canvas } from '@react-three/fiber';
import { useState, useEffect } from 'react';

import { Box } from './_components/Box';
import { Container } from './_components/Container';
import { Controls } from './_components/Controls';

// Function to generate random colors
const getRandomColor = () => {
  const letters = '0123456789ABCDEF';
  let color = '#';
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
};

export default function Home() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [initialData, setInitialData] = useState(null);

  // Prepare initial data on the client
  useEffect(() => {
    setInitialData({
      container: { L: 300, W: 200, H: 180 },
      boxes: [
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
      ],
    });
  }, []);

  const handleVisualize = async (data) => {
    setLoading(true);
    try {
      const response = await fetch('/api/pack', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.details || 'Failed to get packing result');
      }
      const resultData = await response.json();
      
      const placementsWithColors = resultData.placements.map(p => ({...p, color: getRandomColor()}));
      setResult({...resultData, placements: placementsWithColors});

    } catch (error) {
      console.error(error);
      alert(error.message);
    } finally {
      setLoading(false);
    }
  };
  
  // Automatically run visualization on initial load
  useEffect(() => {
    if(initialData) {
      handleVisualize(initialData);
    }
  }, [initialData]);

  const container = result?.container;
  const placements = result?.placements;

  const containerCenter = container ? [0, container.H / 2, 0] : [0, 0, 0];

  return (
    <div className="w-screen h-screen">
      <Controls onVisualize={handleVisualize} loading={loading} />
      <Canvas camera={{ position: [400, 400, 400], fov: 50 }}>
        <OrbitControls target={containerCenter} />
        <ambientLight intensity={0.8} />
        <pointLight position={[container?.L || 0, container?.H * 2 || 0, container?.W * 2 || 0]} intensity={0.8} />
        <Sky sunPosition={[100, 100, 20]} />

        {container && (
          <Container
            position={[
              -container.L / 2,
              container.H / 2,
              container.W / 2
            ]}
            args={[container.L, container.H, container.W]}
          />
        )}

        {placements && placements.map((p) => (
          <Box
            key={p.id}
            position={[
              p.x - container.L / 2 + p.L / 2,
              p.z + p.H / 2,
              p.y + p.W / 2,
            ]}
            args={[p.L, p.H, p.W]}
            color={p.color}
          />
        ))}
      </Canvas>
    </div>
  );
}
