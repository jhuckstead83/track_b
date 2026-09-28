// Twin vs control at fixed centres: does the off-line pair change the Dobsch spectrum at double precision?
// control = the same zero list with the off-line pair moved onto the line (real q of the same modulus).
const { execFileSync } = require('child_process');
const fs = require('fs');
const src = fs.readFileSync('dobsch.cjs', 'utf8');
// reuse matrixAt/minEig by evaluating the module body with a stub argv and no main loop
const body = src.slice(0, src.indexOf('const q0 = MODE'));
function load(mode) {
  const argv = ['node', 'x', 'dh_zeros.json', '2', '0', mode];
  const f = new Function('require', 'process', body + '; return { matrixAt, minEig, offQ, onQ };');
  return f(require, { argv });
}
const twin = load('twin'), ctrl = load('control');
const q0 = twin.offQ[0], r0 = Math.hypot(q0[0], q0[1]);
for (const x0 of [r0 * 0.97, r0, r0 * 1.03]) {
  console.log(`x0 = ${x0.toFixed(2)}  (|q0| = ${r0.toFixed(2)})`);
  for (const N of [10, 20, 30, 40, 45, 50, 55, 60, 64]) {
    const a = twin.minEig(twin.matrixAt(x0, N)), b = ctrl.minEig(ctrl.matrixAt(x0, N));
    console.log(`  N=${String(N).padStart(2)}  twin ${a.toExponential(4)}  control ${b.toExponential(4)}  relative gap ${((a - b) / Math.abs(b)).toExponential(2)}`);
  }
}
