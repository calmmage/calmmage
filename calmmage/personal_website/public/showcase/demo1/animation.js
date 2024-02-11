// Create the Three.js scene
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 5;
const renderer = new THREE.WebGLRenderer( { alpha: true } );
renderer.setClearColor( 0x000000, 0 );
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Create the cubes and trails
const cubes = [];
const targets = [];
const trails = [];
const trailTargets = [];
const numCubes = 100;
const numTrails = 20;
const R = 2;
const SCALE = 0.1;
let POSITION_SCALE = 0.5;

// const POSITION_SCALE = 0.0077;
// WIDTH_SCALE = 1;
const H = 900;
const W = 1100;
let WIDTH_SCALE = Math.min(window.innerWidth / W, 1);
POSITION_SCALE = WIDTH_SCALE * 0.5;

// Add resize listener
window.addEventListener('resize', () => {
    WIDTH_SCALE = Math.min(window.innerWidth / W, 1);
    POSITION_SCALE = WIDTH_SCALE * 0.5;
    // Reset camera aspect ratio and renderer size
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

for (let i = 0; i < numCubes; i++) {
    cube = new THREE.Mesh(
        new THREE.BoxGeometry(SCALE, SCALE, SCALE),
        new THREE.MeshBasicMaterial({color: 0xffffff})
    );
    const angle = (i / numCubes) * Math.PI * 2;
    cube.position.x = Math.sin(angle) * R * WIDTH_SCALE;
    cube.position.y = Math.cos(angle) * R * WIDTH_SCALE;
    cubes.push(cube);
    scene.add(cube);

    targetCube = new THREE.Mesh(
        new THREE.BoxGeometry(SCALE, SCALE, SCALE),
        new THREE.MeshBasicMaterial({color: 0xffffff, transparent: true, opacity: 0})
    );
    targetCube.position.x = Math.sin(angle) * R * WIDTH_SCALE;
    targetCube.position.y = Math.cos(angle) * R * WIDTH_SCALE;
    targetCube.range = R;
    targetCube.offset = angle;
    targets.push(targetCube);
    scene.add(targetCube);


    trailTargets.push(cube);
    for (let j = 0; j < numTrails; j++) {
        trail = new THREE.Mesh(
            new THREE.PlaneGeometry(SCALE, SCALE, SCALE),
            new THREE.MeshBasicMaterial({color: 0xffffff, transparent: true, opacity: 1.0 - (j / numTrails)})
        );
        trail.position.x = cube.position.x;
        trail.position.y = cube.position.y;
        trail.position.z = cube.position.z - 0.1;
        trails.push(trail);
        scene.add(trail);
        if (j > 0) {
            trailTargets.push(trails[trails.length - 2]);
        }
    }
}

// Add interactivity
document.addEventListener('mousemove', (event) => {
    mouseX = (event.clientX / window.innerWidth) * 2 - 1; // 1245
    mouseY = -(event.clientY / window.innerHeight) * 2 + 1;  // 1014
    // mouseX *= POSITION_SCALE;
    // mouseY *= POSITION_SCALE;
    cubes.forEach(cube => {
        distance = Math.sqrt((cube.position.x - mouseX) ** 2 + (cube.position.y - mouseY) ** 2);
        if (distance < 2) {
            cube.position.x +=  (cube.position.x - mouseX) / distance
            cube.position.y +=  (cube.position.y - mouseY) / distance
        }
    })
});

let time = 0;

function updateCubes() {
  time += 0.002;
  targets.forEach(cube => {
    cube.position.x = Math.sin(time + cube.offset) * cube.range * WIDTH_SCALE;
    cube.position.y = Math.cos(time + cube.offset) * cube.range * WIDTH_SCALE;
  });
  // all the rest of the cubes just follow their target
    cubes.forEach((cube, i) => {
        distance = Math.sqrt((cube.position.x - targets[i].position.x) ** 2 + (cube.position.y - targets[i].position.y) ** 2);
        cube.position.x += (targets[i].position.x - cube.position.x) * 0.01 * distance;
        cube.position.y += (targets[i].position.y - cube.position.y) * 0.01 * distance;
    });
    trails.forEach((trail, i) => {
        distance = Math.sqrt((trail.position.x - trailTargets[i].position.x) ** 2 + (trail.position.y - trailTargets[i].position.y) ** 2);
        trail.position.x += (trailTargets[i].position.x - trail.position.x) * 0.01 * distance;
        trail.position.y += (trailTargets[i].position.y - trail.position.y) * 0.01 * distance;
    });

}

// Animate the scene
const animate = function () {
    updateCubes();
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
};

animate();
