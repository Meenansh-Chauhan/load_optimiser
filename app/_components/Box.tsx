type BoxProps = {
    position: [number, number, number];
    args: [number, number, number];
    color: string;
};

export function Box({ position, args, color }: BoxProps) {
    return (
        <mesh position={position}>
            <boxGeometry args={args} />
            <meshLambertMaterial attach="material" color={color} />
        </mesh>
    )
}