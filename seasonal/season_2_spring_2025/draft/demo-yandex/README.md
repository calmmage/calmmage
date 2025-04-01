# 3D Boid Simulation

A 3D boid simulation implemented with TypeScript and Three.js. Boids algorithm demonstrates emergent behavior through simple rules of separation, alignment, and cohesion.

## Features

- 3D visualization of boid flocking behavior
- Interactive controls for simulation parameters
- Performance monitoring with stats.js
- Responsive design

## Getting Started

1. Install dependencies:
```
npm install
```

2. Start the development server:
```
npm run dev
```

3. Open your browser to the displayed URL (usually http://localhost:5173)

## Controls

- **Separation**: Controls how strongly boids avoid each other
- **Alignment**: Controls how strongly boids align with their neighbors' direction
- **Cohesion**: Controls how strongly boids are attracted to the center of their local group
- **Speed**: Controls the overall movement speed of the boids
- **Reset**: Resets the simulation with new random positions

## Tech Stack

- TypeScript
- Three.js for 3D rendering
- Vite for development and building