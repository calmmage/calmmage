import * as THREE from 'three';
import Stats from 'stats.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { Boid } from './utils/Boid';
import { BoidSimulation } from './utils/BoidSimulation';

// Setup Three.js scene
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x111122);

// Setup camera
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 30, 80);

// Setup renderer
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
document.body.appendChild(renderer.domElement);

// Add orbit controls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;

// Add ambient light
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);

// Add directional light
const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(1, 1, 1);
scene.add(directionalLight);

// Add grid helper
const gridHelper = new THREE.GridHelper(200, 20, 0x444444, 0x222222);
scene.add(gridHelper);

// Setup stats
const stats = new Stats();
stats.showPanel(0);
document.body.appendChild(stats.dom);

// Create simulation bounds
const bounds = {
  width: 100,
  height: 60,
  depth: 100
};

// Visual representation of bounds
const boundingBox = new THREE.Box3(
  new THREE.Vector3(-bounds.width/2, -bounds.height/2, -bounds.depth/2),
  new THREE.Vector3(bounds.width/2, bounds.height/2, bounds.depth/2)
);
const boundingBoxHelper = new THREE.Box3Helper(boundingBox, 0x00ff00);
scene.add(boundingBoxHelper);

// Create boid simulation
const simulation = new BoidSimulation(scene, bounds);

// Initialize boids
const numBoids = 200;
simulation.createBoids(numBoids);

// Handle window resize
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

// Connect UI controls
const separationSlider = document.getElementById('separation') as HTMLInputElement;
const alignmentSlider = document.getElementById('alignment') as HTMLInputElement;
const cohesionSlider = document.getElementById('cohesion') as HTMLInputElement;
const speedSlider = document.getElementById('speed') as HTMLInputElement;
const resetButton = document.getElementById('reset') as HTMLButtonElement;

// Value displays
const separationValue = document.getElementById('separation-value')!;
const alignmentValue = document.getElementById('alignment-value')!;
const cohesionValue = document.getElementById('cohesion-value')!;
const speedValue = document.getElementById('speed-value')!;

// Set initial values
simulation.separationWeight = parseFloat(separationSlider.value);
simulation.alignmentWeight = parseFloat(alignmentSlider.value);
simulation.cohesionWeight = parseFloat(cohesionSlider.value);
simulation.speedFactor = parseFloat(speedSlider.value);

// Update values when sliders change
separationSlider.addEventListener('input', () => {
  const value = parseFloat(separationSlider.value);
  simulation.separationWeight = value;
  separationValue.textContent = value.toFixed(1);
});

alignmentSlider.addEventListener('input', () => {
  const value = parseFloat(alignmentSlider.value);
  simulation.alignmentWeight = value;
  alignmentValue.textContent = value.toFixed(1);
});

cohesionSlider.addEventListener('input', () => {
  const value = parseFloat(cohesionSlider.value);
  simulation.cohesionWeight = value;
  cohesionValue.textContent = value.toFixed(1);
});

speedSlider.addEventListener('input', () => {
  const value = parseFloat(speedSlider.value);
  simulation.speedFactor = value;
  speedValue.textContent = value.toFixed(1);
});

// Reset button
resetButton.addEventListener('click', () => {
  simulation.reset(numBoids);
});

// Animation loop
function animate() {
  requestAnimationFrame(animate);
  stats.begin();
  
  controls.update();
  simulation.update();
  
  renderer.render(scene, camera);
  stats.end();
}

animate();
