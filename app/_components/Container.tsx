"use client";
import { Edges } from '@react-three/drei';

type Container = {
    position: [number, number, number];
    args: [number, number, number];
};


export function Container({ position, args }: Container) {
    return (
        <mesh position={position}>
            <boxGeometry args={args} />
            <Edges>
                <lineBasicMaterial color="black" />
            </Edges>
            <meshStandardMaterial transparent opacity={0.05} color="white" />
        </mesh>
    );
}
