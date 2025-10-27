"use client"

import {useRef, useMemo} from "react"
import {Canvas, useFrame} from "@react-three/fiber"
import {Points, PointMaterial} from "@react-three/drei"

function getSpherePositions(count: number, radius: number) {
  const positions = new Float32Array(count * 3)

  for (let i = 0; i < count; i += 1) {
    let x = 0
    let y = 0
    let z = 0
    let mag = 0

    // ensure the point sits inside the unit sphere
    do {
      x = Math.random() * 2 - 1
      y = Math.random() * 2 - 1
      z = Math.random() * 2 - 1
      mag = x * x + y * y + z * z
    } while (mag > 1 || mag === 0)

    const scale = radius / Math.cbrt(mag)
    const idx = i * 3
    positions[idx] = x * scale
    positions[idx + 1] = y * scale
    positions[idx + 2] = z * scale
  }

  return positions
}

function Particles(props: any) {
  const ref = useRef<any>()
  const sphere = useMemo(() => getSpherePositions(5000, 1.5), [])

  useFrame((state, delta) => {
    if (ref.current) {
      ref.current.rotation.x -= delta / 10
      ref.current.rotation.y -= delta / 15
    }
  })

  return (
    <group rotation={[0, 0, Math.PI / 4]}>
      <Points ref={ref} positions={sphere} stride={3} frustumCulled={false} {...props}>
        <PointMaterial transparent color="#60a5fa" size={0.005} sizeAttenuation depthWrite={false}/>
      </Points>
    </group>
  )
}

export function ParticleAnimation() {
  return (
    <div className="absolute inset-0 w-full h-full">
      <Canvas camera={{position: [0, 0, 1]}}>
        <Particles/>
      </Canvas>
    </div>
  )
}
