// Node's built-in assert/vm only. No package installation, browser or network.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'examples/dashboard_3d/app.js'), 'utf8');
const begin = source.indexOf('function validateSample(');
const end = source.indexOf('function currentStep(');
const context = vm.createContext({});
vm.runInContext(source.slice(begin, end), context);
const sample = JSON.parse(fs.readFileSync(path.join(root, 'examples/dashboard_3d/sample_state.json'), 'utf8'));
context.validateSample(sample);
let checks = 1;
for (const mutate of [
  s => s.demo_only = false,
  s => s.prices = [1, 2],
  s => s.prices[0] = Infinity,
  s => s.agents[1].id = s.agents[0].id,
  s => s.agents[0].color = 'invalid',
  s => s.agents[0].position = [1],
  s => s.steps[0].agent = 'unknown',
  s => s.steps = [],
]) {
  const changed = structuredClone(sample);
  mutate(changed);
  assert.throws(() => context.validateSample(changed));
  checks += 1;
}
console.log(JSON.stringify({ dashboard_state_checks: checks, passed: true }));
