// First failing rung near each off-line zero, for large k.
// Coarse k steps (relative 5e-4) with golden refinement of every low local minimum in x,
// then an exact k-by-k scan inside the final bracket.
// Usage: node rungs3.cjs out.json KMAX zeros1.json [zeros2.json ...]
const fs = require('fs');
const OUT = process.argv[2], KMAX = +process.argv[3];
const lists = process.argv.slice(4).map(p => JSON.parse(fs.readFileSync(p, 'utf8')));
const TOP = Math.max(...lists.map(z => z.T));
const cmul = (a, b) => [a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]];
const online = [...new Set(lists.flatMap(z => z.online).map(g => +g.toFixed(9)))].sort((a, b) => a - b);
const offline = lists.flatMap(z => z.offline).sort((a, b) => a[1] - b[1]);
const ALL = online.map(g => [[0.25 + g * g, 0], 1]).concat(offline.map(([s, t]) => [cmul([s, t], [1 - s, -t]), 2]));
function term(x, q) {
  const d = [x + q[0], q[1]], d2 = cmul(d, d), den = d2[0] * d2[0] + d2[1] * d2[1];
  const num = cmul([4 * x * q[0], 4 * x * q[1]], [d2[0], -d2[1]]);
  return [Math.log(Math.hypot(num[0], num[1]) / den), Math.atan2(num[1], num[0])];
}
function Gs(x, k, list) {
  let lmax = -Infinity; const tm = list.map(([q, w]) => { const t = term(x, q); if (t[0] > lmax) lmax = t[0]; return [t[0], t[1], w]; });
  let s = 0; for (const [l, p, w] of tm) { const e = k * (l - lmax); if (e > -700) s += w * Math.exp(e) * Math.cos(k * p); }
  return s;
}
function golden(fn, a, b) {
  const g = (Math.sqrt(5) - 1) / 2; let c = b - g * (b - a), d = a + g * (b - a), fc = fn(c), fd = fn(d);
  for (let i = 0; i < 80 && b - a > 1e-13 * a; i++) { if (fc < fd) { b = d; d = c; fd = fc; c = b - g * (b - a); fc = fn(c); } else { a = c; c = d; fc = fd; d = a + g * (b - a); fd = fn(d); } }
  return fc < fd ? [c, fc] : [d, fd];
}
const argq = q => Math.atan2(q[1], q[0]);
const thList = Math.max(...offline.map(([s, t]) => Math.abs(argq(cmul([s, t], [1 - s, -t])))));
const SIG0 = 1.3951361582351098, thTail = Math.atan(TOP * (2 * SIG0 - 1) / (TOP * TOP - SIG0 * (SIG0 - 1)));
const Ksector = Math.floor(Math.PI / (2 * Math.max(thList, thTail)));
console.log(`merged list to T=${TOP}: ${online.length} on-line, ${offline.length} off-line pairs; sector-safe k <= ${Ksector}`);
const results = [];
for (let i = 0; i < offline.length; i++) {
  const [s, t] = offline[i], q0 = cmul([s, t], [1 - s, -t]), r = Math.hypot(q0[0], q0[1]), th = Math.abs(argq(q0));
  const complete = r * Math.exp(0.12) <= TOP * TOP;             // local list complete over the search window
  const local = ALL.filter(([q]) => Math.abs(Math.log(Math.hypot(q[0], q[1]) / r)) < 0.35);
  const H = 1e-4, NV = 500, xs = []; for (let j = -NV; j <= NV; j++) xs.push(r * Math.exp(j * H));
  const pre = xs.map(x => local.map(([q, w]) => { const u = term(x, q); return [u[0], u[1], w]; }));
  const minAt = k => {                                          // refined minimum over the window at rung k
    const vals = pre.map(tm => { let lm = -Infinity; for (const u of tm) if (u[0] > lm) lm = u[0];
      let v = 0; for (const [l, p, w] of tm) { const e = k * (l - lm); if (e > -700) v += w * Math.exp(e) * Math.cos(k * p); } return v; });
    let best = [Infinity, 0];
    for (let j = 1; j < xs.length - 1; j++) if (vals[j] <= vals[j - 1] && vals[j] <= vals[j + 1] && vals[j] < 0.05) {
      const [xm, gm] = vals[j] < 0 ? [xs[j], vals[j]] : golden(x => Gs(x, k, local), xs[j - 1], xs[j + 1]);
      if (gm < best[0]) best = [gm, xm];
    }
    return best;
  };
  let k = Ksector + 1, prev = k, hit = null;
  while (k <= KMAX) {
    const [g, x] = minAt(k);
    if (g < 0) { hit = k; break; }
    prev = k; k += Math.max(1, Math.round(k * 5e-4));
  }
  let first = null;
  if (hit) for (let kk = prev + 1; kk <= hit; kk++) { const [g, x] = minAt(kk); if (g < 0) { first = { k: kk, x, G: g, Gfull: Gs(x, kk, ALL) }; break; } }
  const row = { zero: i, rho: [s, t], absq: r, theta: th, localComplete: complete, kFirst: first && first.k, x: first && first.x,
    Gscaled: first && first.G, kTheta2: first ? first.k * th * th : null, searchedTo: first ? null : KMAX };
  results.push(row); console.log(JSON.stringify(row));
}
fs.writeFileSync(OUT, JSON.stringify({ Ksector, results }, null, 1));
