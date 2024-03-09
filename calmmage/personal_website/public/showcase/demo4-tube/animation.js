// Create the Three.js scene
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 5;
const renderer = new THREE.WebGLRenderer({alpha: true});
renderer.setClearColor(0x000000, 0);
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
const POSITION_SCALE = 0.0077;
const REACTION_DISTANCE = 0.5;
const REACTION_STRENGTH = 0.01;
const REACT_USE_DISTANCE = true;

const FOLLOW_SPEED = 0.01;
let FOLLOW_DISTANCE = false;
const TRAIL_FOLLOW_SPEED = 0.01;
const TRAIL_FOLLOW_DISTANCE = true;


// funniest to play with

for (let i = 0; i < numCubes; i++) {
    cube = new THREE.Mesh(
        new THREE.BoxGeometry(SCALE, SCALE, SCALE),
        new THREE.MeshBasicMaterial({color: 0xffffff})
    );
    const angle = (i / numCubes) * Math.PI * 2;
    cube.position.x = Math.sin(angle) * R;
    cube.position.y = Math.cos(angle) * R;
    cubes.push(cube);
    scene.add(cube);

    targetCube = new THREE.Mesh(
        new THREE.BoxGeometry(SCALE, SCALE, SCALE),
        new THREE.MeshBasicMaterial({color: 0xffffff, transparent: true, opacity: 0})
    );
    targetCube.position.x = Math.sin(angle) * R;
    targetCube.position.y = Math.cos(angle) * R;
    targetCube.range = R;
    targetCube.offset = angle;
    targets.push(targetCube);
    scene.add(targetCube);


    trailTargets.push(cube);
    for (let j = 0; j < numTrails; j++) {
        const size = SCALE * (1.0 - 0.5 * (j / numTrails));
        const opacity = 1.0 - (j / numTrails);
        trail = new THREE.Mesh(
            new THREE.PlaneGeometry(size, size, size),
            new THREE.MeshBasicMaterial({
                color: 0xffffff,
                transparent: true,
                opacity: opacity
            })
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
function scatterCubes(cubes, sourceX, sourceY, reaction_strength, reaction_distance, reaction_use_distance = false) {
    cubes.forEach(cube => {
        let distance = Math.sqrt((cube.position.x - sourceX) ** 2 + (cube.position.y - sourceY) ** 2);
        if ((reaction_distance === 0) || distance < reaction_distance) {
            x = (sourceX - cube.position.x) * reaction_strength;
            y = (sourceY - cube.position.y) * reaction_strength;
            if (reaction_use_distance) {
                x /= distance;
                y /= distance;
            }
            cube.position.x -= x;
            cube.position.y -= y;
        }
    })
}

function getMousePosition(event) {
    return {
        x: (event.clientX - window.innerWidth / 2) * POSITION_SCALE,
        y: (window.innerHeight / 2 - event.clientY) * POSITION_SCALE
    }
}

document.addEventListener('mousemove', (event) => {
    position = getMousePosition(event);
    scatterCubes(cubes, position.x, position.y, REACTION_STRENGTH, REACTION_DISTANCE, REACT_USE_DISTANCE);

});

const CLICK_REACTION_STRENGTH = 0.1;
const CLICK_REACTION_DISTANCE = 2;
const SCATTER_DURATION = 20;

document.addEventListener('click', (event) => {
    position = getMousePosition(event);
    FOLLOW_DISTANCE = true;
    for (let i = 0; i < SCATTER_DURATION; i++) {
        setTimeout(() => {
            scatterCubes(cubes, position.x, position.y, CLICK_REACTION_STRENGTH, CLICK_REACTION_DISTANCE, REACT_USE_DISTANCE);
        }, i * 10);
    }
    setTimeout(() => {
        FOLLOW_DISTANCE = false;
    }, SCATTER_DURATION * 10 * 2);

});

let time = 0;

function updateCubes() {
    time += 0.002;
    targets.forEach(cube => {
        cube.position.x = Math.sin(time + cube.offset) * cube.range;
        cube.position.y = Math.cos(time + cube.offset) * cube.range;
    });
    // all the rest of the cubes just follow their target
    cubes.forEach((cube, i) => {
        distance = Math.sqrt((cube.position.x - targets[i].position.x) ** 2 + (cube.position.y - targets[i].position.y) ** 2);
        x = (targets[i].position.x - cube.position.x) * FOLLOW_SPEED;
        y = (targets[i].position.y - cube.position.y) * FOLLOW_SPEED;
        if (FOLLOW_DISTANCE) {
            x *= distance;
            y *= distance;
        }
        cube.position.x += x;
        cube.position.y += y;
    });
    trails.forEach((trail, i) => {
        distance = Math.sqrt((trail.position.x - trailTargets[i].position.x) ** 2 + (trail.position.y - trailTargets[i].position.y) ** 2);
        x = (trailTargets[i].position.x - trail.position.x) * TRAIL_FOLLOW_SPEED;
        y = (trailTargets[i].position.y - trail.position.y) * TRAIL_FOLLOW_SPEED;
        if (TRAIL_FOLLOW_DISTANCE) {
            x *= distance;
            y *= distance;
        }
        trail.position.x += x;
        trail.position.y += y;

    });

}


// Animate the scene
const animate = function () {
    updateCubes();
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
};

animate();
