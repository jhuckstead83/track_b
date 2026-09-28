// Exact-in-x search for the first failing rung of the DH twin.
// For each k: coarse log-grid in x around each off-line |q| (+-0.12), then golden-section
// refinement of every local minimum of the scaled sum. First k with a negative refined min = k*.
// Usage: node rungs2.cjs dh_zeros.json kmin kmax
const fs = require('fs');
const Z = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const KMIN = +process.argv[3] || 219, KMAX = +process.argv[4] || 20000;
const cmul = (a, b) => [a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]];
const ALL = Z.online.map(g => [[0.25 + g * g, 0], 1]).concat(Z.offline.map(([s, t]) => [cmul([s, t], [1 - s, -t]), 2]));
function term(x, q) {
  const d = [x + q[0], q[1]], d2 = cmul(d, d), den = d2[0] * d2[0] + d2[1] * d2[1];
  const num = cmul([4 * x * q[0], 4 * x * q[1]], [d2[0], -d2[1]]);
  return [Math.log(Math.hypot(num[0], num[1]) / den), Math.atan2(num[1], num[0])];
}
// scaled G_k at x using the given orbit list; scaling by exp(k*lmax) keeps the sign
function Gs(x, k, list) {
  let lmax = -Infinity; const tm = list.map(([q, w]) => { const t = term(x, q); if (t[0] > lmax) lmax = t[0]; return [t[0], t[1], w]; });
  let s = 0; for (const [l, p, w] of tm) { const e = k * (l - lmax); if (e > -700) s += w * Math.exp(e) * Math.cos(k * p); }
  return s;
}
function golden(fn, a, b) {
  const g = (Math.sqrt(5) - 1) / 2; let c = b - g * (b - a), d = a + g * (b - a), fc = fn(c), fd = fn(d);
  for (let i = 0; i < 80 && b - a > 1e-12 * Math.abs(a); i++) {
    if (fc < fd) { b = d; d = c; fd = fc; c = b - g * (b - a); fc = fn(c); } else { a = c; c = d; fc = fd; d = a + g * (b - a); fd = fn(d); }
  }
  return fc < fd ? [c, fc] : [d, fd];
}
const results = [];
for (let i = 0; i < Z.offline.length; i++) {
  const [s, t] = Z.offline[i], q0 = cmul([s, t], [1 - s, -t]), r = Math.hypot(q0[0], q0[1]);
  const local = ALL.filter(([q]) => Math.abs(Math.log(Math.hypot(q[0], q[1]) / r)) < 0.6);
  const H = 2e-4, NV = 600, xs = []; for (let j = -NV; j <= NV; j++) xs.push(r * Math.exp(j * H));
  const pre = xs.map(x => local.map(([q, w]) => { const t = term(x, q); return [t[0], t[1], w]; }));
  let first = null;
  for (let k = KMIN; k <= KMAX && !first; k++) {
    const vals = pre.map(tm => { let lmax = -Infinity; for (const u of tm) if (u[0] > lmax) lmax = u[0];
      let v = 0; for (const [l, p, w] of tm) { const e = k * (l - lmax); if (e > -700) v += w * Math.exp(e) * Math.cos(k * p); } return v; });
    for (let j = 1; j < xs.length - 1; j++) {
      if (vals[j] <= vals[j - 1] && vals[j] <= vals[j + 1]) {
        if (vals[j] < 0) { first = { k, x: xs[j], G: vals[j] }; break; }
        const [xm, gm] = golden(x => Gs(x, k, local), xs[j - 1], xs[j + 1]);
        if (gm < 0) { first = { k, x: xm, G: gm }; break; }
      }
    }
  }
  if (first) {
    const full = Gs(first.x, first.k, ALL);
    // previous rung: refined min over the whole window must be >= 0
    let prevMin = Infinity;
    for (let j = 1; j < xs.length - 1; j++) { const [, gm] = golden(x => Gs(x, first.k - 1, local), xs[j - 1], xs[j + 1]); prevMin = Math.min(prevMin, gm); }
    results.push({ zero: i, rho: [s, t], absq: r, argq: Math.atan2(q0[1], q0[0]), kFirst: first.k, x: first.x, Gscaled_local: first.G, Gscaled_full: full, prevRungMinScaled: prevMin });
  } else results.push({ zero: i, rho: [s, t], absq: r, kFirst: null, searchedTo: KMAX });
  console.log(JSON.stringify(results[results.length - 1]));
}
fs.writeFileSync(`dh_first_failure_${KMIN}_${KMAX}.json`, JSON.stringify(results, null, 1));
