"use client"

import {useRef, useMemo} from "react"
import {Canvas, useFrame} from "@react-three/fiber"
import {Points, PointMaterial} from "@react-three/drei"
import * as random from "maath/random/dist/maath-random.esm"

function Particles(props: any) {
  const ref = useRef<any>()
  const [sphere] = useMemo(() => [random.inSphere(new Float32Array(5000), {radius: 1.5})], [])

  useFrame((state, delta) => {
    if (ref.current) {
      ref.current.rotation.x -= delta / 10
      ref.current.rotation.y -= delta / 15
    }
  })

  return (
    <group rotation={[0, 0, Math.PI / 4]}>
      <Points ref={ref} positions={sphere} stride={3} frustumCulled={false} {...props}>
        <PointMaterial transparent color="#60a5fa" size={0.005} sizeAttenuation={true} depthWrite={false}/>
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
