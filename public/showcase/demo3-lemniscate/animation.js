// Animation: Lemniscate of Bernoulli

// Create the Three.js scene
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 4;
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
const R = 4;
const SCALE = 0.05;
const REACTION_STRENGTH = 0.02;
const REACT_USE_DISTANCE = true;


// funniest to play with
const REACTION_DISTANCE = 1.3;
const FOLLOW_SPEED = 0.015;
let FOLLOW_USE_DISTANCE = true;
const TRAIL_FOLLOW_SPEED = 0.03;
const TRAIL_FOLLOW_USE_DISTANCE = true;
const TIME_SPEED = 0.0005;

// const POSITION_SCALE = 0.0077;
// WIDTH_SCALE = 1;
const H = 900;
const W = 1100;
WIDTH_SCALE = Math.min(window.innerWidth / W, 1);
let POSITION_MULT = 0.006;
POSITION_SCALE = WIDTH_SCALE * POSITION_MULT;

// Add resize listener
window.addEventListener('resize', () => {
    WIDTH_SCALE = Math.min(window.innerWidth / W, 1);
    POSITION_SCALE = WIDTH_SCALE * POSITION_MULT;
    // Reset camera aspect ratio and renderer size
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// init
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
    targetCube.position.x = Math.sin(angle) * R* WIDTH_SCALE;
    targetCube.position.y = Math.cos(angle) * R* WIDTH_SCALE;
    targetCube.range = R;
    targetCube.offset = angle;
    targets.push(targetCube);
    scene.add(targetCube);


    trailTargets.push(cube);
    for (let j = 0; j < numTrails; j++) {
        trail = new THREE.Mesh(
            new THREE.PlaneGeometry(SCALE, SCALE, SCALE),
            new THREE.MeshBasicMaterial({color: 0xffffff, transparent: true, opacity: 0.8 * (1.0 - (j / numTrails))})
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

// Add interactivity
document.addEventListener('mousemove', (event) => {
    mouseX = event.clientX - window.innerWidth / 2; // 1245
    mouseY = window.innerHeight / 2 - event.clientY;  // 1014
    mouseX *= POSITION_SCALE;
    mouseY *= POSITION_SCALE;
    scatterCubes(cubes, mouseX, mouseY, REACTION_STRENGTH, REACTION_DISTANCE, REACT_USE_DISTANCE);
});

const CLICK_REACTION_STRENGTH = 1;
const SCATTER_DURATION = 50;

document.addEventListener('click', (event) => {
    mouseX = event.clientX - window.innerWidth / 2; // 1245
    mouseY = window.innerHeight / 2 - event.clientY;  // 1014
    mouseX *= POSITION_SCALE;
    mouseY *= POSITION_SCALE;
    FOLLOW_USE_DISTANCE = false;
    for (let i = 0; i < SCATTER_DURATION; i++) {
        setTimeout(() => {
            scatterCubes(cubes, mouseX, mouseY, CLICK_REACTION_STRENGTH, 5, true);
        }, i*10);
    }
    setTimeout(() => {
        FOLLOW_USE_DISTANCE = true;
    }, SCATTER_DURATION*10 * 2);

});

let time = 0;

function updateCubes() {
    time += TIME_SPEED;
    targets.forEach(cube => {
        let theta = time * 2 * Math.PI + cube.offset;
        let radius = cube.range;
        cube.position.x = WIDTH_SCALE * radius * Math.cos(theta);
        cube.position.y = WIDTH_SCALE * radius * Math.sin(2 * theta) / 2;
    });
    // all the rest of the cubes just follow their target
    cubes.forEach((cube, i) => {
        distance = Math.sqrt((cube.position.x - targets[i].position.x) ** 2 + (cube.position.y - targets[i].position.y) ** 2);
        x = (targets[i].position.x - cube.position.x) * FOLLOW_SPEED;
        y = (targets[i].position.y - cube.position.y) * FOLLOW_SPEED;
        if (FOLLOW_USE_DISTANCE) {
            x *= distance;
            y *= distance;
        } else {
            x /= distance;
            y /= distance;
        }
        cube.position.x += x ;
        cube.position.y += y ;
    });
    trails.forEach((trail, i) => {
        distance = Math.sqrt((trail.position.x - trailTargets[i].position.x) ** 2 + (trail.position.y - trailTargets[i].position.y) ** 2);
        x = (trailTargets[i].position.x - trail.position.x) * TRAIL_FOLLOW_SPEED;
        y = (trailTargets[i].position.y - trail.position.y) * TRAIL_FOLLOW_SPEED;
        if (TRAIL_FOLLOW_USE_DISTANCE) {
            x *= distance;
            y *= distance;
        } else {
            x /= distance;
            y /= distance;
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
