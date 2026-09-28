// Global sign scan of the DH rung W_k(x) over all x in [xlo, xhi] (full orbit sum, every
// local minimum refined by golden section). Supports "positive for all x" below the first failure.
// Usage: node global_check.cjs dh_zeros.json k1,k2,...
const fs = require('fs');
const Z = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const KS = (process.argv[3] || '219,1000,5000,10000,16588,16589').split(',').map(Number);
const cmul = (a, b) => [a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]];
const ALL = Z.online.map(g => [[0.25 + g * g, 0], 1]).concat(Z.offline.map(([s, t]) => [cmul([s, t], [1 - s, -t]), 2]));
const qs = ALL.map(([q]) => Math.hypot(q[0], q[1])).sort((a, b) => a - b);
function term(x, q) {
  const d = [x + q[0], q[1]], d2 = cmul(d, d), den = d2[0] * d2[0] + d2[1] * d2[1];
  const num = cmul([4 * x * q[0], 4 * x * q[1]], [d2[0], -d2[1]]);
  return [Math.log(Math.hypot(num[0], num[1]) / den), Math.atan2(num[1], num[0])];
}
function Gs(x, k) {
  let lmax = -Infinity; const tm = ALL.map(([q, w]) => { const t = term(x, q); if (t[0] > lmax) lmax = t[0]; return [t[0], t[1], w]; });
  let s = 0; for (const [l, p, w] of tm) { const e = k * (l - lmax); if (e > -700) s += w * Math.exp(e) * Math.cos(k * p); }
  return s;
}
function golden(fn, a, b) {
  const g = (Math.sqrt(5) - 1) / 2; let c = b - g * (b - a), d = a + g * (b - a), fc = fn(c), fd = fn(d);
  for (let i = 0; i < 90 && b - a > 1e-13 * a; i++) { if (fc < fd) { b = d; d = c; fd = fc; c = b - g * (b - a); fc = fn(c); } else { a = c; c = d; fc = fd; d = a + g * (b - a); fd = fn(d); } }
  return fc < fd ? [c, fc] : [d, fd];
}
// x range: from well below the first node to the top of the complete list (zeros beyond T
// are unlisted, so only x up to (0.8 T)^2 is claimed)
const xlo = qs[0] / 50, xhi = Math.pow(0.8 * Z.T, 2);
for (const k of KS) {
  const H = Math.min(2e-3, 0.25 / Math.sqrt(k)); const n = Math.ceil(Math.log(xhi / xlo) / H);
  let prev2 = Gs(xlo, k), prev1 = Gs(xlo * Math.exp(H), k), worst = [Infinity, 0], negs = 0;
  for (let j = 2; j <= n; j++) {
    const x = xlo * Math.exp(j * H), v = Gs(x, k);
    if (prev1 <= prev2 && prev1 <= v) { const [xm, gm] = golden(y => Gs(y, k), xlo * Math.exp((j - 2) * H), x); if (gm < worst[0]) worst = [gm, xm]; if (gm < 0) negs++; }
    prev2 = prev1; prev1 = v;
  }
  console.log(`k=${k}: x in [${xlo.toFixed(3)}, ${xhi.toFixed(0)}], ${n} grid pts, min refined scaled G = ${worst[0].toExponential(4)} at x=${worst[1].toFixed(6)}, negative minima: ${negs}`);
}
