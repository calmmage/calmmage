import * as THREE from 'three';
import {Boid} from './Boid';

export class BoidSimulation {
  scene: THREE.Scene;
  boids: Boid[] = [];
  bounds: { width: number, height: number, depth: number };
  
  // Simulation parameters
  neighborDistance: number = 10;
  desiredSeparation: number = 5;
  separationWeight: number = 1.5;
  alignmentWeight: number = 1.0;
  cohesionWeight: number = 1.0;
  boundsWeight: number = 1.5;
  speedFactor: number = 1.0;
  
  constructor(scene: THREE.Scene, bounds: { width: number, height: number, depth: number }) {
    this.scene = scene;
    this.bounds = bounds;
  }
  
  createBoids(count: number): void {
    // Clear existing boids
    for (const boid of this.boids) {
      this.scene.remove(boid.mesh);
    }
    this.boids = [];
    
    // Create new boids
    for (let i = 0; i < count; i++) {
      const halfWidth = this.bounds.width / 2;
      const halfHeight = this.bounds.height / 2;
      const halfDepth = this.bounds.depth / 2;
      
      // Random position within bounds
      const position = new THREE.Vector3(
        THREE.MathUtils.randFloat(-halfWidth, halfWidth),
        THREE.MathUtils.randFloat(-halfHeight, halfHeight),
        THREE.MathUtils.randFloat(-halfDepth, halfDepth)
      );
      
      // Random initial velocity
      const velocity = new THREE.Vector3(
        THREE.MathUtils.randFloat(-1, 1),
        THREE.MathUtils.randFloat(-1, 1),
        THREE.MathUtils.randFloat(-1, 1)
      ).normalize().multiplyScalar(THREE.MathUtils.randFloat(0.5, 1.5));
      
      // Different color for each boid (blue to cyan to white gradient)
      const hue = 0.6 + THREE.MathUtils.randFloat(0, 0.1);
      const saturation = THREE.MathUtils.randFloat(0.7, 1.0);
      const lightness = THREE.MathUtils.randFloat(0.5, 0.7);
      const color = new THREE.Color().setHSL(hue, saturation, lightness);
      
      const boid = new Boid(position, velocity, color);
      this.boids.push(boid);
      this.scene.add(boid.mesh);
    }
  }
  
  update(): void {
    for (const boid of this.boids) {
      // Calculate steering forces
      const separation = boid.separate(this.boids, this.desiredSeparation)
        .multiplyScalar(this.separationWeight);
      
      const alignment = boid.align(this.boids, this.neighborDistance)
        .multiplyScalar(this.alignmentWeight);
      
      const cohesion = boid.cohesion(this.boids, this.neighborDistance)
        .multiplyScalar(this.cohesionWeight);
      
      const avoidBounds = boid.avoidBounds(this.bounds)
        .multiplyScalar(this.boundsWeight);
      
      // Apply forces
      boid.applyForce(separation);
      boid.applyForce(alignment);
      boid.applyForce(cohesion);
      boid.applyForce(avoidBounds);
      
      // Adjust speed based on slider
      boid.maxSpeed = 2 * this.speedFactor;
      
      // Update boid position and rotation
      boid.update();
      
      // Ensure boids stay within bounds
      this.enforceBounds(boid);
    }
  }
  
  enforceBounds(boid: Boid): void {
    const halfWidth = this.bounds.width / 2;
    const halfHeight = this.bounds.height / 2;
    const halfDepth = this.bounds.depth / 2;
    
    // Wrap around edges (teleport to opposite side)
    if (boid.position.x < -halfWidth) boid.position.x = halfWidth;
    if (boid.position.x > halfWidth) boid.position.x = -halfWidth;
    
    if (boid.position.y < -halfHeight) boid.position.y = halfHeight;
    if (boid.position.y > halfHeight) boid.position.y = -halfHeight;
    
    if (boid.position.z < -halfDepth) boid.position.z = halfDepth;
    if (boid.position.z > halfDepth) boid.position.z = -halfDepth;
  }
  
  reset(count: number): void {
    this.createBoids(count);
  }
}