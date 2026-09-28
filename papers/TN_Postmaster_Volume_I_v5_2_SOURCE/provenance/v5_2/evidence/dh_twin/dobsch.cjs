// Twin test of the principal route via the Dobsch-Donoghue local criterion.
// N-node Löwner PSD for h = x S(x)  <=>  at every x0, Q(p) = sum_rho W_rho p(z_rho)^2 >= 0 for real p, deg p < N,
// with z = 1/(x0+q), W = q z^2 (on-line: real > 0; off-line pair: 2 Re[W0 p(z0)^2]).
// Basis: Lagrange polynomials at N Chebyshev points on [0, Zmax] (well conditioned).
// Tail zeros (t > T) enter as a density (1/2pi) log(5t/2pi), assumed on-line.
// Usage: node dobsch.cjs dh_zeros.json Nmax [offlineIndex] [mode]
const fs = require('fs');
const Zd = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const NMAX = +process.argv[3] || 60, OFF = +(process.argv[4] || 0), MODE = process.argv[5] || 'twin';
const C = {
  add: (a, b) => [a[0] + b[0], a[1] + b[1]], sub: (a, b) => [a[0] - b[0], a[1] - b[1]],
  mul: (a, b) => [a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]],
  div: (a, b) => { const d = b[0] * b[0] + b[1] * b[1]; return [(a[0] * b[0] + a[1] * b[1]) / d, (a[1] * b[0] - a[0] * b[1]) / d]; },
};
const onQ = Zd.online.map(g => 0.25 + g * g);
const offQ = Zd.offline.map(([s, t]) => C.mul([s, t], [1 - s, -t]));
if (MODE === 'control') { // replace every off-line node by a real node of the same modulus: must stay PSD
  offQ.forEach(q => onQ.push(Math.hypot(q[0], q[1]), Math.hypot(q[0], q[1]))); offQ.length = 0;
}
// Gauss-Legendre nodes on [0,1]
function gauss(n) {
  const x = [], w = [];
  for (let i = 1; i <= n; i++) {
    let z = Math.cos(Math.PI * (i - 0.25) / (n + 0.5)), pp;
    for (let it = 0; it < 100; it++) {
      let p1 = 1, p2 = 0; for (let j = 1; j <= n; j++) { const p3 = p2; p2 = p1; p1 = ((2 * j - 1) * z * p2 - (j - 1) * p3) / j; }
      pp = n * (z * p1 - p2) / (z * z - 1); const dz = p1 / pp; z -= dz; if (Math.abs(dz) < 1e-15) break;
    }
    x.push((1 - z) / 2); w.push(1 / ((1 - z * z) * pp * pp));
  }
  return [x, w];
}
const [GX, GW] = gauss(80);
function matrixAt(x0, N) {
  const qmin = Math.min(...onQ, ...offQ.map(q => Math.hypot(q[0], q[1])));
  const Zmax = 1 / (x0 + qmin) * 1.0000001;
  const nodes = [], bw = [];
  for (let k = 0; k < N; k++) { nodes.push(Zmax * (1 - Math.cos(Math.PI * (k + 0.5) / N)) / 2); bw.push((k % 2 ? -1 : 1) * Math.sin(Math.PI * (k + 0.5) / N)); }
  const lag = z => { // barycentric Lagrange values at real z
    for (let k = 0; k < N; k++) if (z === nodes[k]) return nodes.map((_, j) => (j === k ? 1 : 0));
    const t = nodes.map((n, k) => bw[k] / (z - n)); const s = t.reduce((a, b) => a + b, 0); return t.map(v => v / s);
  };
  const lagC = z => { // complex z
    const t = nodes.map((n, k) => C.div([bw[k], 0], C.sub(z, [n, 0]))); const s = t.reduce((a, b) => C.add(a, b), [0, 0]);
    return t.map(v => C.div(v, s));
  };
  const M = Array.from({ length: N }, () => new Float64Array(N));
  const addReal = (W, l) => { for (let i = 0; i < N; i++) { const a = W * l[i]; if (a === 0) continue; for (let j = 0; j < N; j++) M[i][j] += a * l[j]; } };
  for (const q of onQ) { const z = 1 / (x0 + q); addReal(q * z * z, lag(z)); }
  const T = Zd.T;           // tail: t = T/u, u in (0,1]
  for (let g = 0; g < GX.length; g++) {
    const u = GX[g], t = T / u, dt = T / (u * u), q = 0.25 + t * t, z = 1 / (x0 + q);
    addReal(q * z * z * Math.log(5 * t / (2 * Math.PI)) / (2 * Math.PI) * dt * GW[g], lag(z));
  }
  for (const q of offQ) {   // conjugate pair: 2 Re[W0 l_i l_j]
    const z = C.div([1, 0], C.add([x0, 0], q)), W = C.mul(q, C.mul(z, z)), l = lagC(z);
    for (let i = 0; i < N; i++) { const a = C.mul(W, l[i]); for (let j = 0; j < N; j++) M[i][j] += 2 * C.mul(a, l[j])[0]; }
  }
  return M;
}
function minEig(M) { // cyclic Jacobi on the diagonally normalized matrix
  const n = M.length, d = []; for (let i = 0; i < n; i++) d.push(Math.sqrt(Math.abs(M[i][i])) || 1);
  const a = M.map((r, i) => Array.from(r, (v, j) => v / (d[i] * d[j])));
  for (let sweep = 0; sweep < 60; sweep++) {
    let off = 0; for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) off += a[i][j] * a[i][j];
    if (off < 1e-32) break;
    for (let p = 0; p < n; p++) for (let q = p + 1; q < n; q++) {
      if (Math.abs(a[p][q]) < 1e-300) continue;
      const th = (a[q][q] - a[p][p]) / (2 * a[p][q]), t = Math.sign(th || 1) / (Math.abs(th) + Math.sqrt(th * th + 1));
      const c = 1 / Math.sqrt(t * t + 1), s = t * c;
      for (let k = 0; k < n; k++) { const kp = a[k][p], kq = a[k][q]; a[k][p] = c * kp - s * kq; a[k][q] = s * kp + c * kq; }
      for (let k = 0; k < n; k++) { const pk = a[p][k], qk = a[q][k]; a[p][k] = c * pk - s * qk; a[q][k] = s * pk + c * qk; }
    }
  }
  let m = Infinity; for (let i = 0; i < n; i++) m = Math.min(m, a[i][i]); return m;
}
const q0 = MODE === 'control' ? null : offQ[OFF];
const r0 = q0 ? Math.hypot(q0[0], q0[1]) : Math.hypot(...Zd.offline[OFF].length ? [0.25 + Zd.offline[OFF][1] ** 2, 0] : [1, 0]);
const results = [];
let firstN = null;
for (let N = 2; N <= NMAX; N++) {
  let best = [Infinity, 0];
  for (let v = -0.15; v <= 0.15 + 1e-12; v += 0.003) { const x0 = r0 * Math.exp(v); const m = minEig(matrixAt(x0, N)); if (m < best[0]) best = [m, x0]; }
  results.push({ N, minEigNormalized: best[0], x0: best[1] });
  console.log(`N=${N}  min normalized eigenvalue ${best[0].toExponential(4)}  at x0=${best[1].toFixed(3)}`);
  if (firstN === null && best[0] < -1e-8) firstN = N;
}
console.log(MODE, 'first N with min eigenvalue < -1e-8:', firstN);
fs.writeFileSync(`dobsch_${MODE}_${OFF}.json`, JSON.stringify({ mode: MODE, offIndex: OFF, firstN, results }, null, 1));
