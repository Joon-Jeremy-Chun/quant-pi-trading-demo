// Classroom starter, written independently. All workflow activity is synthetic.
const $ = (id) => document.getElementById(id);
let data, selectedId, stepNumber = 0, playback = null;
let focusScene = () => {}, resetView = () => {};

function validateSample(sample) {
  if (sample.demo_only !== true) throw new Error('The sample must declare demo_only: true.');
  if (!Array.isArray(sample.prices) || sample.prices.length < 3 || !sample.prices.every(Number.isFinite)) {
    throw new Error('Use at least three finite numbers in prices.');
  }
  if (!Array.isArray(sample.agents) || !sample.agents.length || !Array.isArray(sample.steps) || !sample.steps.length) {
    throw new Error('Add at least one agent and one workflow step.');
  }
  const ids = new Set();
  for (const agent of sample.agents) {
    if (typeof agent.id !== 'string' || !agent.id || ids.has(agent.id)) throw new Error('Agent IDs must be unique strings.');
    ids.add(agent.id);
    for (const key of ['name', 'role', 'input', 'output', 'task']) {
      if (typeof agent[key] !== 'string') throw new Error(`Agent ${agent.id} needs a text ${key}.`);
    }
    if (!/^#[0-9a-f]{6}$/i.test(agent.color) || !Array.isArray(agent.position) || agent.position.length !== 2 || !agent.position.every(Number.isFinite)) {
      throw new Error(`Agent ${agent.id} needs a hex color and a numeric [x, z] position.`);
    }
  }
  for (const step of sample.steps) {
    if (!ids.has(step.agent) || typeof step.status !== 'string' || typeof step.message !== 'string') {
      throw new Error('Every step needs an existing agent, a status and a message.');
    }
  }
  return sample;
}

function currentStep() {
  return stepNumber ? data.steps[(stepNumber - 1) % data.steps.length] : null;
}

function selectAgent(id) {
  const agent = data.agents.find((item) => item.id === id);
  if (!agent) return;
  selectedId = id;
  $('agent-name').textContent = agent.name;
  $('agent-role').textContent = agent.role;
  $('agent-task').textContent = agent.task;
  $('agent-input').textContent = agent.input;
  $('agent-output').textContent = agent.output;
  const active = currentStep();
  $('agent-status').textContent = active?.agent === id ? active.status : 'waiting';
  for (const button of document.querySelectorAll('[data-agent]')) {
    button.setAttribute('aria-pressed', String(button.dataset.agent === id));
  }
  focusScene(id);
}

function addLog(message) {
  const item = document.createElement('li');
  const time = document.createElement('time');
  time.textContent = `Step ${stepNumber}`;
  item.append(time, document.createTextNode(message));
  $('activity-log').prepend(item);
  while ($('activity-log').children.length > 5) $('activity-log').lastElementChild.remove();
}

function advance() {
  stepNumber += 1;
  const step = currentStep();
  $('step-label').textContent = `Step ${stepNumber}`;
  addLog(step.message);
  selectAgent(step.agent);
}

function stopPlayback() {
  clearInterval(playback);
  playback = null;
  $('play').textContent = 'Play';
  $('play').setAttribute('aria-pressed', 'false');
}

function reset() {
  stopPlayback();
  stepNumber = 0;
  $('step-label').textContent = 'Step 0';
  $('activity-log').replaceChildren();
  addLog('Meet the four example teammates. Choose Next step to walk through their pretend workflow.');
  selectAgent(data.agents[0].id);
  resetView();
}

function makeAgentButton(agent, className) {
  const button = document.createElement('button');
  button.type = 'button';
  button.className = className;
  button.dataset.agent = agent.id;
  button.style.setProperty('--agent-color', agent.color);
  button.textContent = `${agent.name} · ${agent.role.split(' ')[0]}`;
  button.addEventListener('click', () => selectAgent(agent.id));
  return button;
}

function drawSparkline(prices) {
  const svgNS = 'http://www.w3.org/2000/svg';
  const low = Math.min(...prices), high = Math.max(...prices);
  const points = prices.map((value, index) => [8 + index / (prices.length - 1) * 244, 60 - (value - low) / (high - low || 1) * 48]);
  const line = document.createElementNS(svgNS, 'polyline');
  line.setAttribute('points', points.map((point) => point.join(',')).join(' '));
  line.setAttribute('fill', 'none');
  line.setAttribute('stroke', '#4d916e');
  line.setAttribute('stroke-width', '2');
  line.setAttribute('stroke-linejoin', 'round');
  $('sparkline').append(line);
  const shortAverage = prices.slice(-3).reduce((sum, value) => sum + value, 0) / 3;
  const fullAverage = prices.reduce((sum, value) => sum + value, 0) / prices.length;
  $('sparkline').setAttribute('aria-label', `Invented prices. Last-three average ${shortAverage.toFixed(2)}, full average ${fullAverage.toFixed(2)}.`);
}

function showFallback(message) {
  $('stage').dataset.mode = '2d';
  $('scene-message').textContent = message;
  $('scene-message').classList.add('error');
  $('scene-message').hidden = false;
  $('fallback-map').hidden = false;
  $('reset-view').disabled = true;
  $('stage').querySelector('canvas')?.remove();
  document.querySelector('.scene-caption').textContent = 'Choose a teammate below or on this map';
}

async function buildScene() {
  // The imports are inside a try/catch so the rest of the dashboard survives
  // a blocked CDN or unavailable WebGL. ?view=2d deliberately skips the imports.
  const THREE = await import('three');
  const { OrbitControls } = await import('three/addons/controls/OrbitControls.js');
  const stage = $('stage');
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.setClearColor(0x000000, 0);
  stage.append(renderer.domElement);
  renderer.domElement.setAttribute('aria-label', 'Four example teammates in a small 3D lab');
  const scene = new THREE.Scene();
  const camera = new THREE.OrthographicCamera(-15, 15, 11, -11, 0.1, 100);
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.enablePan = false;
  controls.minZoom = 0.6;
  controls.maxZoom = 2;
  controls.minPolarAngle = Math.PI / 6;
  controls.maxPolarAngle = Math.PI / 2.4;
  resetView = () => {
    camera.position.set(20, 21, 24);
    camera.zoom = 1;
    camera.updateProjectionMatrix();
    controls.target.set(0, 0, 0);
    controls.update();
  };
  resetView();
  scene.add(new THREE.HemisphereLight(0xffffff, 0x8eaa95, 2.5));
  const sun = new THREE.DirectionalLight(0xffffff, 3);
  sun.position.set(-12, 24, 10);
  sun.castShadow = true;
  sun.shadow.mapSize.set(1024, 1024);
  Object.assign(sun.shadow.camera, { left: -18, right: 18, top: 16, bottom: -16 });
  sun.shadow.normalBias = 0.04;
  scene.add(sun);

  // Begin editing here: all buildings, furniture and people are basic shapes.
  function mesh(geometry, color, x, y, z, parent = scene) {
    const object = new THREE.Mesh(geometry, new THREE.MeshStandardMaterial({ color, roughness: 0.8 }));
    object.position.set(x, y, z);
    object.castShadow = object.receiveShadow = true;
    parent.add(object);
    return object;
  }
  const box = (w, h, d, color, x, y, z, parent) => mesh(new THREE.BoxGeometry(w, h, d), color, x, y, z, parent);
  const sphere = (r, color, x, y, z, parent) => mesh(new THREE.SphereGeometry(r, 16, 12), color, x, y, z, parent);
  box(25, 0.4, 18, '#b7cbbb', 0, -0.28, 0);
  box(24, 0.08, 17, '#d3e2cf', 0, -0.02, 0);
  box(3, 0.04, 17, '#e6dcca', 0, 0.04, 0);
  box(24, 0.04, 1.8, '#e6dcca', 0, 0.05, 0);
  mesh(new THREE.CylinderGeometry(2, 2.2, 0.15, 32), '#c2d6b4', 0, 0.13, 0);
  box(0.3, 1.6, 0.3, '#ac8e68', 0, 0.85, 0);
  sphere(1.1, '#90b484', 0, 2.2, 0);
  sphere(0.8, '#a5c396', 0.7, 2.45, 0.1);
  for (const [x, z] of [[-11, -7], [11, -7], [-11, 7], [11, 7]]) {
    box(0.2, 0.8, 0.2, '#ac8e68', x, 0.4, z);
    sphere(0.65, '#86a77b', x, 1.1, z);
  }

  const actors = new Map(), clickTargets = [];
  const selectionRing = mesh(new THREE.TorusGeometry(0.65, 0.05, 8, 32), '#427c59', 0, 0.2, 0);
  selectionRing.rotation.x = Math.PI / 2;
  for (const agent of data.agents) {
    const [x, z] = agent.position;
    const building = new THREE.Group();
    building.position.set(x, 0, z);
    building.userData.agentId = agent.id;
    scene.add(building);
    box(5.6, 0.18, 4.2, '#f2efe5', 0, 0.17, 0, building);
    box(5.6, 1.4, 0.15, '#f8faf5', 0, 0.9, -2, building);
    box(0.15, 1.4, 4.2, '#eef3ec', -2.7, 0.9, 0, building);
    box(5.6, 0.14, 0.2, agent.color, 0, 1.65, -2, building);
    box(3, 0.12, 1, '#bc9b74', 0, 1.0, -0.8, building);
    for (const lx of [-1.25, 1.25]) box(0.1, 0.75, 0.1, '#9e896d', lx, 0.58, -0.8, building);
    box(1, 0.65, 0.08, '#2f4552', 0, 1.4, -1, building);
    box(0.82, 0.46, 0.03, agent.color, 0, 1.42, -0.945, building);
    box(0.65, 0.04, 0.23, '#e6e9e1', 0, 1.09, -0.42, building);
    const labelCanvas = document.createElement('canvas');
    labelCanvas.width = 512; labelCanvas.height = 128;
    const context = labelCanvas.getContext('2d');
    context.fillStyle = '#fffffff2'; context.fillRect(0, 0, 512, 128);
    context.textAlign = 'center'; context.fillStyle = '#2e4754';
    context.font = 'bold 36px Arial'; context.fillText(agent.name, 256, 50);
    context.font = '25px Arial'; context.fillText(agent.role, 256, 91);
    const texture = new THREE.CanvasTexture(labelCanvas);
    texture.colorSpace = THREE.SRGBColorSpace;
    const label = new THREE.Sprite(new THREE.SpriteMaterial({ map: texture, depthTest: false }));
    label.position.set(0, 3.25, -1.9); label.scale.set(3.8, 0.95, 1);
    building.add(label);

    const person = new THREE.Group();
    person.userData.agentId = agent.id;
    person.position.set(x, 0.27, z + 0.7);
    scene.add(person);
    mesh(new THREE.CapsuleGeometry(0.3, 0.55, 4, 12), agent.color, 0, 0.65, 0, person);
    sphere(0.28, '#f4d8ba', 0, 1.33, 0, person);
    sphere(0.025, '#374955', -0.09, 1.36, 0.265, person);
    sphere(0.025, '#374955', 0.09, 1.36, 0.265, person);
    for (const lx of [-0.17, 0.17]) box(0.15, 0.3, 0.18, '#435364', lx, 0.15, 0, person);
    actors.set(agent.id, { person, home: new THREE.Vector3(x, 0.27, z + 0.7) });
    clickTargets.push(building, person);
  }
  focusScene = (id) => { selectionRing.userData.agentId = id; };
  focusScene(selectedId);
  function resize() {
    const width = stage.clientWidth, height = stage.clientHeight;
    const aspect = width / height;
    const halfHeight = Math.max(10.5, 13.6 / aspect);
    Object.assign(camera, { left: -halfHeight * aspect, right: halfHeight * aspect, top: halfHeight, bottom: -halfHeight });
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
  }
  new ResizeObserver(resize).observe(stage);
  resize();
  const raycaster = new THREE.Raycaster(), pointer = new THREE.Vector2();
  let pointerDown = null;
  renderer.domElement.addEventListener('pointerdown', (event) => { pointerDown = [event.clientX, event.clientY]; });
  renderer.domElement.addEventListener('pointerup', (event) => {
    if (!pointerDown || Math.hypot(event.clientX - pointerDown[0], event.clientY - pointerDown[1]) > 6) return;
    const bounds = renderer.domElement.getBoundingClientRect();
    pointer.set((event.clientX - bounds.left) / bounds.width * 2 - 1, -(event.clientY - bounds.top) / bounds.height * 2 + 1);
    raycaster.setFromCamera(pointer, camera);
    const hit = raycaster.intersectObjects(clickTargets, true)[0];
    let object = hit?.object;
    while (object && !object.userData.agentId) object = object.parent;
    if (object) selectAgent(object.userData.agentId);
  });
  renderer.domElement.addEventListener('webglcontextlost', (event) => {
    event.preventDefault();
    showFallback('The 3D graphics context was lost. The 2D map and workflow controls are still available. Reload to retry 3D.');
  });
  const clock = new THREE.Clock();
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let elapsed = 0;
  function animate() {
    if (stage.dataset.mode !== '3d') return;
    const dt = Math.min(clock.getDelta(), 0.05);
    elapsed += dt;
    const active = currentStep();
    for (const [id, actor] of actors) {
      const destination = actor.home.clone();
      if (active?.agent === id) destination.z += 0.8;
      actor.person.position.lerp(destination, reducedMotion ? 1 : Math.min(1, dt * 3));
      actor.person.rotation.y = active?.agent === id && !reducedMotion ? Math.sin(elapsed * 2) * 0.08 : 0;
    }
    const selected = actors.get(selectionRing.userData.agentId);
    if (selected) selectionRing.position.set(selected.person.position.x, 0.3, selected.person.position.z);
    controls.update();
    renderer.render(scene, camera);
    requestAnimationFrame(animate);
  }
  stage.dataset.mode = '3d';
  $('scene-message').hidden = true;
  animate();
}

async function main() {
  try {
    const response = await fetch('./sample_state.json');
    if (!response.ok) throw new Error(`Sample file returned HTTP ${response.status}.`);
    data = validateSample(await response.json());
    $('agent-buttons').replaceChildren(...data.agents.map((agent) => makeAgentButton(agent, 'agent-button')));
    $('fallback-map').replaceChildren(...data.agents.map((agent) => makeAgentButton(agent, 'fallback-node')));
    drawSparkline(data.prices);
    $('next-step').addEventListener('click', advance);
    $('reset').addEventListener('click', reset);
    $('reset-view').addEventListener('click', () => resetView());
    $('play').addEventListener('click', () => {
      if (playback) { stopPlayback(); return; }
      advance();
      playback = setInterval(advance, 2500);
      $('play').textContent = 'Pause';
      $('play').setAttribute('aria-pressed', 'true');
    });
    for (const id of ['next-step', 'reset', 'play']) $(id).disabled = false;
    reset();
    document.documentElement.dataset.ready = 'true';
    if (new URLSearchParams(location.search).get('view') === '2d') {
      showFallback('2D learning view selected. The same sample workflow and teammate controls work here.');
      return;
    }
    try { await buildScene(); }
    catch (error) {
      console.info('3D view unavailable:', error.message);
      showFallback('3D could not load. Check internet access to jsDelivr and browser WebGL support, then reload. You can still use this 2D map.');
    }
  } catch (error) {
    $('scene-message').textContent = `Cannot load the classroom sample: ${error.message} Run python src/demo_dashboard.py and open its localhost URL; check sample_state.json if you edited it.`;
    $('scene-message').classList.add('error');
    $('agent-name').textContent = 'Sample unavailable';
    $('activity-log').textContent = 'No sample workflow was loaded. Check the message above.';
  }
}
main();
