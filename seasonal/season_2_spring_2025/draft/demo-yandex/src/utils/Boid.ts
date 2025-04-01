import * as THREE from 'three';

export class Boid {
  position: THREE.Vector3;
  velocity: THREE.Vector3;
  acceleration: THREE.Vector3;
  mesh: THREE.Mesh;
  maxSpeed: number;
  maxForce: number;
  
  constructor(
    position: THREE.Vector3, 
    velocity: THREE.Vector3, 
    color: THREE.Color = new THREE.Color(0x1a75ff)
  ) {
    this.position = position;
    this.velocity = velocity;
    this.acceleration = new THREE.Vector3();
    this.maxSpeed = 2;
    this.maxForce = 0.1;
    
    // Create boid mesh
    const geometry = new THREE.ConeGeometry(0.5, 2, 8);
    const material = new THREE.MeshPhongMaterial({ 
      color, 
      emissive: color.clone().multiplyScalar(0.2),
      specular: new THREE.Color(0xffffff),
      shininess: 50
    });
    
    this.mesh = new THREE.Mesh(geometry, material);
    this.mesh.position.copy(this.position);
    
    // Rotate to match direction
    this.mesh.rotation.x = Math.PI / 2;
  }
  
  applyForce(force: THREE.Vector3): void {
    this.acceleration.add(force);
  }
  
  // Seek a target position
  seek(target: THREE.Vector3): THREE.Vector3 {
    const desired = new THREE.Vector3().subVectors(target, this.position);
    desired.normalize();
    desired.multiplyScalar(this.maxSpeed);
    
    const steer = new THREE.Vector3().subVectors(desired, this.velocity);
    steer.clampLength(0, this.maxForce);
    
    return steer;
  }
  
  // Avoid getting too close to other boids
  separate(boids: Boid[], desiredSeparation: number): THREE.Vector3 {
    const steer = new THREE.Vector3();
    let count = 0;
    
    for (const other of boids) {
      if (other === this) continue;
      
      const distance = this.position.distanceTo(other.position);
      
      if (distance > 0 && distance < desiredSeparation) {
        // Calculate vector pointing away from neighbor
        const diff = new THREE.Vector3().subVectors(this.position, other.position);
        diff.normalize();
        diff.divideScalar(distance); // Weight by distance
        steer.add(diff);
        count++;
      }
    }
    
    if (count > 0) {
      steer.divideScalar(count);
    }
    
    if (steer.length() > 0) {
      steer.normalize();
      steer.multiplyScalar(this.maxSpeed);
      steer.sub(this.velocity);
      steer.clampLength(0, this.maxForce);
    }
    
    return steer;
  }
  
  // Align with average heading of local flock
  align(boids: Boid[], neighborDistance: number): THREE.Vector3 {
    const sum = new THREE.Vector3();
    let count = 0;
    
    for (const other of boids) {
      if (other === this) continue;
      
      const distance = this.position.distanceTo(other.position);
      
      if (distance > 0 && distance < neighborDistance) {
        sum.add(other.velocity);
        count++;
      }
    }
    
    if (count > 0) {
      sum.divideScalar(count);
      sum.normalize();
      sum.multiplyScalar(this.maxSpeed);
      
      const steer = new THREE.Vector3().subVectors(sum, this.velocity);
      steer.clampLength(0, this.maxForce);
      return steer;
    }
    
    return new THREE.Vector3();
  }
  
  // Move toward average position of local flock
  cohesion(boids: Boid[], neighborDistance: number): THREE.Vector3 {
    const sum = new THREE.Vector3();
    let count = 0;
    
    for (const other of boids) {
      if (other === this) continue;
      
      const distance = this.position.distanceTo(other.position);
      
      if (distance > 0 && distance < neighborDistance) {
        sum.add(other.position);
        count++;
      }
    }
    
    if (count > 0) {
      sum.divideScalar(count);
      return this.seek(sum);
    }
    
    return new THREE.Vector3();
  }
  
  // Bounds checking - avoid walls
  avoidBounds(bounds: { width: number, height: number, depth: number }, padding: number = 5): THREE.Vector3 {
    const halfWidth = bounds.width / 2;
    const halfHeight = bounds.height / 2;
    const halfDepth = bounds.depth / 2;
    
    const desiredVelocity = new THREE.Vector3();
    let strength = 1.0;
    
    if (this.position.x < -halfWidth + padding) {
      desiredVelocity.x = strength;
    } else if (this.position.x > halfWidth - padding) {
      desiredVelocity.x = -strength;
    }
    
    if (this.position.y < -halfHeight + padding) {
      desiredVelocity.y = strength;
    } else if (this.position.y > halfHeight - padding) {
      desiredVelocity.y = -strength;
    }
    
    if (this.position.z < -halfDepth + padding) {
      desiredVelocity.z = strength;
    } else if (this.position.z > halfDepth - padding) {
      desiredVelocity.z = -strength;
    }
    
    if (desiredVelocity.length() > 0) {
      desiredVelocity.normalize();
      desiredVelocity.multiplyScalar(this.maxSpeed);
      
      const steer = new THREE.Vector3().subVectors(desiredVelocity, this.velocity);
      steer.clampLength(0, this.maxForce * 2); // Stronger force for bounds
      return steer;
    }
    
    return new THREE.Vector3();
  }
  
  update(): void {
    // Update velocity by adding acceleration
    this.velocity.add(this.acceleration);
    
    // Limit speed
    this.velocity.clampLength(0, this.maxSpeed);
    
    // Update position
    this.position.add(this.velocity);
    
    // Reset acceleration
    this.acceleration.set(0, 0, 0);
    
    // Update mesh position
    this.mesh.position.copy(this.position);
    
    // Update mesh rotation to face velocity direction
    if (this.velocity.length() > 0) {
      const lookAt = new THREE.Vector3().addVectors(this.position, this.velocity);
      this.mesh.lookAt(lookAt);
      this.mesh.rotation.x += Math.PI / 2; // Adjust for cone geometry orientation
    }
  }
  
  // For debugging: show velocity vector
  showVelocity(): THREE.ArrowHelper {
    return new THREE.ArrowHelper(
      this.velocity.clone().normalize(),
      this.position,
      3,
      0xff0000
    );
  }
}