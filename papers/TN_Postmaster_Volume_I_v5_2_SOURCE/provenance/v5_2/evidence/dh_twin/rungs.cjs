// Rung ladder W_k(x) = (2k-1)! * sum_[rho] m u_x(q)^k, u_x(q) = q/(x+q)^2, for the DH twin.
// Sign is that of G_k(x) = sum_[rho] (4x u_x(q))^k  (on-line orbits give 4xu in (0,1]).
// Usage: node rungs.cjs dh_zeros.json [kmax]
const fs = require('fs');
const Z = JSON.parse(fs.readFileSync(process.argv[2] || 'dh_zeros.json', 'utf8'));
const KMAX = +process.argv[3] || 200000;
const T = Z.T, SIG0 = 1.3951361582351098;

// orbits: on-line q = 1/4 + g^2 (real); off-line rho=(s,t), s>1/2: q = rho(1-rho) and its conjugate
const cmul = (a, b) => [a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]];
const on = Z.online.map(g => 0.25 + g * g);
const off = Z.offline.map(([s, t]) => cmul([s, t], [1 - s, -t]));   // q, conj added in the sum

// 1) sector bound: theta_max over listed zeros and the unlisted tail t > T
const argq = q => Math.atan2(q[1], q[0]);
const thList = Math.max(0, ...off.map(q => Math.abs(argq(q))));
const thTail = Math.atan(T * (2 * SIG0 - 1) / (T * T - SIG0 * (SIG0 - 1)));
const thMax = Math.max(thList, thTail);
const Ksector = Math.floor(Math.PI / (2 * thMax));
console.log(`listed zeros: ${on.length} on-line, ${off.length} off-line pairs (sigma>1/2); T=${T}`);
console.log(`theta_max listed ${thList.toExponential(6)}, tail bound ${thTail.toExponential(6)} -> sector-safe rungs k <= ${Ksector}`);
off.forEach((q, i) => console.log(`  off-line ${i}: rho=${Z.offline[i][0].toFixed(9)}+${Z.offline[i][1].toFixed(9)}i  |q|=${Math.hypot(...q).toFixed(4)}  arg q=${argq(q).toExponential(5)}`));

// log-magnitude and phase of 4x u_x(q)
function term(x, q) {
  const d = [x + q[0], q[1]], d2 = cmul(d, d);
  const den = d2[0] * d2[0] + d2[1] * d2[1];
  const num = cmul([4 * x * q[0], 4 * x * q[1]], [d2[0], -d2[1]]);
  return [Math.log(Math.hypot(num[0], num[1]) / den), Math.atan2(num[1], num[0])];
}
// G_k(x) scaled: returns value / exp(k * lmax) to avoid underflow; sign is what matters
function G(x, k) {
  const terms = [];
  for (const q of on) { const [l] = term(x, [q, 0]); terms.push([l, 0, 1]); }
  for (const q of off) { const [l, p] = term(x, q); terms.push([l, p, 2]); }  // q and conj(q): 2 Re
  const lmax = Math.max(...terms.map(t => t[0]));
  let s = 0;
  for (const [l, p, w] of terms) { const e = k * (l - lmax); if (e > -745) s += w * Math.exp(e) * Math.cos(k * p); }
  return s;
}

// 2) first failing rung: scan x on log grids around each off-line |q| (+-6%), k upward
let best = null;
for (let i = 0; i < off.length; i++) {
  const r = Math.hypot(...off[i]);
  const xs = []; for (let j = -600; j <= 600; j++) xs.push(r * Math.exp(j * 1e-4));
  // local terms only (others are < e^{-k*1e-3} relative for k>=1e4; kept exact anyway via G for checks)
  const loc = [];
  for (const q of on) if (Math.abs(Math.log(q / r)) < 0.2) loc.push([[q, 0], 1]);
  for (const q of off) if (Math.abs(Math.log(Math.hypot(...q) / r)) < 0.2) loc.push([q, 2]);
  const pre = xs.map(x => loc.map(([q, w]) => { const [l, p] = term(x, q); return [l, p, w]; }));
  let firstK = null, atX = null;
  for (let k = Ksector + 1; k <= KMAX && firstK === null; k++) {
    for (let a = 0; a < xs.length; a++) {
      const tm = pre[a]; let lmax = -Infinity; for (const t of tm) if (t[0] > lmax) lmax = t[0];
      let s = 0; for (const [l, p, w] of tm) { const e = k * (l - lmax); if (e > -745) s += w * Math.exp(e) * Math.cos(k * p); }
      if (s < 0) { firstK = k; atX = xs[a]; break; }
    }
  }
  console.log(`  near off-line ${i} (|q|=${r.toFixed(3)}): first negative local sum at k=${firstK} x=${atX && atX.toFixed(6)}`);
  if (firstK !== null && (best === null || firstK < best.k)) best = { k: firstK, x: atX, zero: i };
}
if (best) {
  // confirm with the full (all-orbit) sum, and refine x at that k
  let xm = best.x, gm = G(xm, best.k);
  for (let d = -2000; d <= 2000; d++) { const x = best.x * Math.exp(d * 1e-7); const g = G(x, best.k); if (g < gm) { gm = g; xm = x; } }
  console.log(`FIRST FAILURE: W_${best.k}(x) < 0 at x = ${xm.toFixed(6)} (full-sum scaled G = ${gm.toExponential(4)}); driven by off-line zero ${best.zero}`);
  // check the previous rung is positive at that x and nearby (full sum)
  let minPrev = Infinity; for (let d = -3000; d <= 3000; d++) { const x = best.x * Math.exp(d * 2e-6); minPrev = Math.min(minPrev, G(x, best.k - 1)); }
  console.log(`  W_${best.k - 1} min over the same window (scaled) = ${minPrev.toExponential(4)}`);
  fs.writeFileSync('dh_rungs.json', JSON.stringify({ Ksector, thMax, thList, thTail, firstFailure: { k: best.k, x: xm, G: gm }, offline: Z.offline }, null, 1));
}
