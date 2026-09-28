// 51 Twins v1 — build index.html (static SVG plates) from twins-data-v1.js.
// Usage: node build-twins-page-v1.cjs          (check that index.html is current)
//        node build-twins-page-v1.cjs --write  (rewrite index.html)
'use strict';
const path = require('path'), fs = require('fs'), vm = require('vm');
const here = (...p) => path.join(__dirname, ...p);
vm.runInThisContext(fs.readFileSync(here('twins-data-v1.js'), 'utf8'));
const D = globalThis.TWINS51;

// ---------- palette (3Blue1Brown / manim constants) ----------
const BG = '#000000', TXT = '#ECECEC', MUTED = '#9B9B9B', DIM = '#4A4A4A', GRID = '#2A2A2A';
const ZETA = '#58C4DD', TWIN = '#F0AC5F', RED = '#FC6255', GREEN = '#83C167', TEAL = '#5CD0B3', PURPLE = '#9A72AC';
const LANE = { '00': ZETA, '01': TEAL, '10': TWIN, '11': PURPLE };

// ---------- svg helpers ----------
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const r1 = n => +(+n).toFixed(1);
const fmt = n => Number(n).toLocaleString('en-US');
// "W_{16589}" style subscripts become tspans; everything else is escaped.
function rich(s, size) {
  const d = r1(size * 0.3), re = /_\{([^}]*)\}/g; let out = '', last = 0, down = false, m;
  while ((m = re.exec(s))) {
    const pre = s.slice(last, m.index);
    if (pre) { out += down ? `<tspan dy="${-d}">${esc(pre)}</tspan>` : esc(pre); down = false; }
    out += `<tspan dy="${down ? 0 : d}" font-size="${r1(size * 0.7)}">${esc(m[1])}</tspan>`; down = true; last = re.lastIndex;
  }
  const rest = s.slice(last);
  if (rest) out += down ? `<tspan dy="${-d}">${esc(rest)}</tspan>` : esc(rest);
  return out;
}
function T(x, y, s, o = {}) {
  const size = o.size || 17, a = [`x="${r1(x)}"`, `y="${r1(y)}"`, `font-size="${size}"`, `fill="${o.fill || TXT}"`];
  if (o.anchor) a.push(`text-anchor="${o.anchor}"`);
  if (o.weight) a.push(`font-weight="${o.weight}"`);
  if (o.italic) a.push('font-style="italic"');
  if (o.cls) a.push(`class="${o.cls}"`);
  if (o.data) a.push(o.data);
  return `<text ${a.join(' ')}>${rich(s, size)}</text>`;
}
const line = (x1, y1, x2, y2, stroke, w = 3, extra = '') => `<line x1="${r1(x1)}" y1="${r1(y1)}" x2="${r1(x2)}" y2="${r1(y2)}" stroke="${stroke}" stroke-width="${w}" stroke-linecap="round" ${extra}/>`;
const circ = (x, y, r, fill, extra = '') => `<circle cx="${r1(x)}" cy="${r1(y)}" r="${r1(r)}" fill="${fill}" ${extra}/>`;
const ring = (x, y, r, stroke, w = 2, extra = '') => `<circle cx="${r1(x)}" cy="${r1(y)}" r="${r1(r)}" fill="none" stroke="${stroke}" stroke-width="${w}" ${extra}/>`;
const pathD = (d, stroke, w = 3, extra = '') => `<path d="${d}" fill="none" stroke="${stroke}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round" ${extra}/>`;
const cross = (x, y, s, stroke, w = 4, extra = '') => `<g ${extra}>${line(x - s, y - s, x + s, y + s, stroke, w)}${line(x - s, y + s, x + s, y - s, stroke, w)}</g>`;
const check = (x, y, s, stroke, w = 4, extra = '') => pathD(`M${r1(x - s)} ${r1(y)} L${r1(x - s * 0.3)} ${r1(y + s * 0.7)} L${r1(x + s)} ${r1(y - s * 0.8)}`, stroke, w, extra);
function svg(id, w, h, title, desc, body, cls) {
  return `<svg class="tw-svg ${cls}" viewBox="0 0 ${w} ${h}" role="img" aria-labelledby="${id}-t ${id}-d" preserveAspectRatio="xMidYMid meet">` +
    `<title id="${id}-t">${esc(title)}</title><desc id="${id}-d">${esc(desc)}</desc>` +
    `<rect width="${w}" height="${h}" fill="${BG}"/>${body}</svg>`;
}
// The Volume I trapped tip used as a drawing device: a 45° cone and its tangent chain (ratio 3 − 2√2).
function trappedTip(ax, ay, dir, z1, stroke) {
  // dir = [dx, dy] unit vector from the apex into the cone mouth
  const [ux, uy] = dir, lam = 3 - 2 * Math.SQRT2, s45 = Math.SQRT1_2;
  const mouth = z1 * 1.55, px = -uy, py = ux;
  let out = pathD(`M${r1(ax + ux * mouth + px * mouth)} ${r1(ay + uy * mouth + py * mouth)} L${r1(ax)} ${r1(ay)} L${r1(ax + ux * mouth - px * mouth)} ${r1(ay + uy * mouth - py * mouth)}`, DIM, 2);
  let z = z1;
  for (let n = 0; n < 6; n++) { const r = z * s45; if (r < 0.35) break; out += ring(ax + ux * z, ay + uy * z, r, stroke, n ? 1.6 : 2.4); z *= lam; }
  return out;
}

// =====================================================================================
// Plate I — the pair: ζ and its Davenport–Heilbronn twin on the Widder rung ladder
// =====================================================================================
function plate1(orient) {
  const Z = D.zeta, land = orient === 'land';
  const W = land ? 1000 : 520, H = land ? 500 : 1060;
  let b = '';
  // --- inset: zeros in the critical strip below height 100
  const inset = (x0, y0, w, h, zeros, off, color, label) => {
    let g = `<rect x="${x0}" y="${y0}" width="${w}" height="${h}" fill="none" stroke="${GRID}" stroke-width="1.5"/>`;
    const X = s => x0 + s * w, Y = t => y0 + h - t / 100 * h;
    g += line(X(0.5), y0, X(0.5), y0 + h, DIM, 1.5, 'stroke-dasharray="4 5"');
    zeros.forEach(t => { g += circ(X(0.5), Y(t), 3.1, color); });
    off.forEach(([s, t]) => { g += circ(X(s), Y(t), 5.2, RED) + ring(X(1 - s), Y(t), 5.2, RED, 1.8); });
    g += T(X(0.5), y0 - 12, label, { size: land ? 17 : 19, anchor: 'middle', fill: color, italic: true });
    g += T(X(0.5), y0 + h + 20, 'σ = ½', { size: 14, anchor: 'middle', fill: MUTED });
    return g;
  };
  if (land) {
    b += inset(34, 70, 64, 320, D.zeros.zeta, [], ZETA, 'ζ');
    b += inset(128, 70, 64, 320, D.zeros.twinOnLine, D.zeros.twinOffLine, TWIN, 'twin');
    b += T(113, 440, 'zeros up to height 100', { size: 14, anchor: 'middle', fill: MUTED });
    b += T(196, 120, '0.8085 + 85.699i', { size: 13, fill: RED }) + T(196, 136, 'off the line', { size: 12, fill: MUTED });
  } else {
    b += inset(120, 60, 90, 200, D.zeros.zeta, [], ZETA, 'ζ');
    b += inset(310, 60, 90, 200, D.zeros.twinOnLine, D.zeros.twinOffLine, TWIN, 'twin');
    b += T(260, 312, 'zeros up to height 100 · off-line pair in red', { size: 15, anchor: 'middle', fill: MUTED });
  }
  // --- the ladder: position along the track by log10 k
  const L10 = Math.log10(Z.KH);
  const along = k => Math.log10(k) / L10;
  let P, Q; // P(u, lane) → [x, y]; lane 0 = ζ, 1 = twin; u in [0, 1] = log10 k / log10 K_H
  if (land) { const x0 = 420, x1 = 815, yz = 175, yt = 300; P = (u, l) => [x0 + u * (x1 - x0), l ? yt : yz]; Q = { x0, x1, yz, yt }; }
  else { const y0 = 400, y1 = 870, xz = 175, xt = 345; P = (u, l) => [l ? xt : xz, y0 + u * (y1 - y0)]; Q = { y0, y1, xz, xt }; }
  const [zs0, zs1] = [P(0, 0), P(1, 0)], [ts0] = [P(0, 1)], tf = P(along(Z.firstFail), 1), zf = P(along(Z.firstFail), 0);
  // sector-safe band 1 ≤ k ≤ 218 (both tracks)
  const s0 = P(0, 0), s1 = P(along(Z.sectorSafe), 1);
  b += land
    ? `<rect x="${r1(s0[0])}" y="${r1(Q.yz - 34)}" width="${r1(s1[0] - s0[0])}" height="${r1(Q.yt - Q.yz + 68)}" fill="#83C16714" stroke="#83C16744"/>`
    : `<rect x="${r1(Q.xz - 40)}" y="${r1(s0[1])}" width="${r1(Q.xt - Q.xz + 80)}" height="${r1(s1[1] - s0[1])}" fill="#83C16714" stroke="#83C16744"/>`;
  // shared entry gate: the functional equation
  if (land) {
    b += pathD(`M${Q.x0 - 30} ${Q.yz} L${Q.x0 - 30} ${Q.yt}`, TXT, 2.5) + line(Q.x0 - 30, Q.yz, Q.x0, Q.yz, TXT, 2.5) + line(Q.x0 - 30, Q.yt, Q.x0, Q.yt, TXT, 2.5);
    b += T(Q.x0 - 42, (Q.yz + Q.yt) / 2 - 2, 'F(s) = F(1 − s)', { size: 16, anchor: 'end', fill: TXT });
    b += T(Q.x0 - 42, (Q.yz + Q.yt) / 2 + 18, 'same reflection · other Γ factor', { size: 13, anchor: 'end', fill: MUTED });
  } else {
    b += line(Q.xz, Q.y0 - 30, Q.xt, Q.y0 - 30, TXT, 2.5) + line(Q.xz, Q.y0 - 30, Q.xz, Q.y0, TXT, 2.5) + line(Q.xt, Q.y0 - 30, Q.xt, Q.y0, TXT, 2.5);
    b += T((Q.xz + Q.xt) / 2, Q.y0 - 42, 'F(s) = F(1 − s) · same reflection, other Γ factor', { size: 16, anchor: 'middle' });
  }
  // tracks
  b += line(...zs0, ...zs1, ZETA, 5);
  b += line(...ts0, ...tf, TWIN, 5);
  // K_H onward: dashed into the trapped tip (ζ only)
  const tipStart = land ? [880, zs1[1]] : [zs1[0], zs1[1] + 60];
  b += line(...zs1, ...tipStart, ZETA, 4, 'stroke-dasharray="3 8"');
  b += land ? trappedTip(975, Q.yz, [-1, 0], 52, ZETA) : trappedTip(Q.xz, 1040, [0, -1], 62, ZETA);
  // rung ticks at 10^0, 10^3, ..., 10^12
  for (let e = 0; e <= 12; e += 3) {
    const u = e / L10, [xz, yz] = P(u, 0), [xt, yt] = P(u, 1);
    const lbl = e === 0 ? 'k = 1' : '10' + String.fromCharCode(...[...String(e)].map(c => ({ 0: 8304, 1: 185, 2: 178, 3: 179, 4: 8308, 5: 8309, 6: 8310, 7: 8311, 8: 8312, 9: 8313 })[c]));
    if (land) { b += line(xz, Q.yt + 58, xz, Q.yt + 66, MUTED, 1.5) + T(xz, Q.yt + 86, lbl, { size: 14, anchor: 'middle', fill: MUTED }); }
  }
  b += land ? line(Q.x0, Q.yt + 62, Q.x1, Q.yt + 62, DIM, 1.5) + T((Q.x0 + Q.x1) / 2, Q.yt + 110, 'rung index k (log scale)', { size: 14, anchor: 'middle', fill: MUTED })
            : T(Q.xz - 16, Q.y0 + 90, 'rung k ↓', { size: 14, fill: MUTED, anchor: 'end' }) + T(Q.xz - 16, Q.y0 + 106, 'log scale', { size: 13, fill: MUTED, anchor: 'end' });
  // labels on the tracks
  if (land) {
    b += T(Q.x0 - 42, Q.yz + 6, 'ζ(s)', { size: 26, fill: ZETA, italic: true, anchor: 'end' }) + T(Q.x0 - 42, Q.yz + 26, 'Euler product', { size: 13, fill: MUTED, anchor: 'end' });
    b += T(Q.x0 - 42, Q.yt + 6, 'twin f(s)', { size: 22, fill: TWIN, italic: true, anchor: 'end' }) + T(Q.x0 - 42, Q.yt + 26, 'no Euler product', { size: 13, fill: MUTED, anchor: 'end' });
  } else {
    b += T(Q.xz - 16, Q.y0 + 250, 'ζ(s)', { size: 24, fill: ZETA, italic: true, anchor: 'end' }) + T(Q.xz - 16, Q.y0 + 270, 'Euler', { size: 14, fill: MUTED, anchor: 'end' }) + T(Q.xz - 16, Q.y0 + 286, 'product', { size: 14, fill: MUTED, anchor: 'end' });
    b += T(Q.xt + 16, Q.y0 + 24, 'twin f', { size: 20, fill: TWIN, italic: true }) + T(Q.xt + 16, Q.y0 + 44, 'no Euler', { size: 14, fill: MUTED }) + T(Q.xt + 16, Q.y0 + 60, 'product', { size: 14, fill: MUTED });
  }
  // sector-safe label
  b += land ? T((s0[0] + s1[0]) / 2, Q.yz - 14, 'k ≤ 218', { size: 13, anchor: 'middle', fill: GREEN })
            : T(Q.xz + 12, (s0[1] + s1[1]) / 2 + 5, 'k ≤ 218 · both safe', { size: 14, fill: GREEN });
  // W7 frontier marker on ζ
  const w7 = P(along(7), 0);
  b += land ? line(w7[0], Q.yz - 10, w7[0], Q.yz + 10, TXT, 2) + T(w7[0], Q.yz + 30, 'W_{7}', { size: 14, anchor: 'middle', fill: MUTED })
            : line(Q.xz - 10, w7[1], Q.xz + 10, w7[1], TXT, 2) + T(Q.xz - 16, w7[1] + 5, 'W_{7}', { size: 15, anchor: 'end', fill: MUTED });
  // the gate W_16589
  if (land) {
    b += line(zf[0], Q.yz - 26, zf[0], Q.yt + 26, '#FFFFFF55', 2, 'stroke-dasharray="2 6"');
    b += check(zf[0] + 1, Q.yz - 34, 9, GREEN, 3.5);
    b += cross(tf[0], tf[1], 11, RED, 5);
    b += T(zf[0], Q.yz - 58, 'gate W_{16589}', { size: 16, anchor: 'middle', fill: TXT });
    b += T(tf[0] + 18, Q.yt - 30, 'W_{16589}(7140.07) < 0', { size: 16, fill: RED });
    b += T(tf[0] + 18, Q.yt - 10, 'earlier sampled tests: positive', { size: 13, fill: MUTED });
  } else {
    b += line(Q.xz - 30, zf[1], Q.xt + 30, zf[1], '#FFFFFF55', 2, 'stroke-dasharray="2 6"');
    b += check(Q.xz - 32, zf[1] - 2, 8, GREEN, 3.5) + cross(tf[0], tf[1], 11, RED, 5);
    b += T(Q.xt - 14, zf[1] - 16, 'gate W_{16589}', { size: 16, anchor: 'end' });
    b += T(Q.xt + 22, tf[1] - 2, 'W_{16589} < 0', { size: 16, fill: RED }) + T(Q.xt + 22, tf[1] + 17, 'at x = 7140.07', { size: 13, fill: MUTED });
  }
  // K_H and beyond
  if (land) {
    b += line(zs1[0], Q.yz - 12, zs1[0], Q.yz + 12, TXT, 2.5);
    b += T(zs1[0], Q.yz + 34, 'K_{H} ≈ 4.7 × 10¹²', { size: 15, anchor: 'middle' });
    b += T(zs1[0], Q.yz + 52, 'guaranteed by verified zeros', { size: 13, anchor: 'middle', fill: MUTED });
    b += T(925, Q.yz - 108, 'every k', { size: 16, anchor: 'middle', fill: ZETA });
    b += T(925, Q.yz - 88, '⇔ RH · OPEN', { size: 16, anchor: 'middle', fill: ZETA });
    b += T(925, Q.yz + 104, 'trapped tip: a drawing', { size: 12, anchor: 'middle', fill: MUTED });
    b += T(925, Q.yz + 119, 'device, not an identity', { size: 12, anchor: 'middle', fill: MUTED });
  } else {
    b += line(Q.xz - 12, zs1[1], Q.xz + 12, zs1[1], TXT, 2.5);
    b += T(Q.xz + 22, zs1[1] + 5, 'K_{H} ≈ 4.7 × 10¹² · verified zeros', { size: 15 });
    b += T(Q.xz + 56, 1000, 'every k ⇔ RH · OPEN', { size: 17, fill: ZETA });
    b += T(Q.xz + 56, 1022, 'trapped tip: drawing device only', { size: 13, fill: MUTED });
  }
  const desc = `Two tracks enter through the same reflection F(s) = F(1 − s); the twin's Gamma factor is Γ((s+1)/2), zeta's is Γ(s/2). The finite-census computation, on a finite list of the twin's zeros, reports its first detected negative at W${Z.firstFail}; earlier sampled tests are positive. The twin has an off-line zero near 0.8085 + 85.699i; zeta continues through the verified-height bound K_H ≈ 4.7 × 10^12 into an open tip.`;
  return svg('p1' + orient, W, H, 'The pair: zeta and its Davenport–Heilbronn twin', desc, b, orient);
}

// =====================================================================================
// Plate II — at the table: four legal pasts of the turn-85 present, run backward and forward
// =====================================================================================
function plate2(orient, S, opts) {
  const land = orient === 'land', lanes = S.lanes, T0 = S.turn;
  const W = land ? 1000 : 520, H = land ? (opts.compact ? 380 : 520) : (opts.compact ? 1000 : 1180);
  let b = '';
  const order = opts.order || ['00', '01', '10', '11'];
  // time → along-axis coordinate
  let A, laneOff, presentPt, fwdEnd, loopC, loopR;
  if (land) {
    const x0 = 60, xT = 540; A = t => x0 + t / (T0 - 1) * (xT - x0);
    const ys = opts.compact ? [70, 130, 190, 250] : [95, 175, 255, 335];
    laneOff = bits => ys[order.indexOf(bits)];
    presentPt = [xT + 80, (ys[0] + ys[3]) / 2]; fwdEnd = [800, presentPt[1]]; loopR = opts.compact ? 56 : 66; loopC = [fwdEnd[0] + loopR + 18, presentPt[1]];
  } else {
    const y0 = opts.compact ? 120 : 150, yT = opts.compact ? 640 : 720; A = t => y0 + t / (T0 - 1) * (yT - y0);
    const xs = [95, 205, 315, 425];
    laneOff = bits => xs[order.indexOf(bits)];
    presentPt = [(xs[0] + xs[3]) / 2, yT + 60]; fwdEnd = [presentPt[0], presentPt[1] + (opts.compact ? 120 : 150)]; loopR = 62; loopC = [presentPt[0], fwdEnd[1] + loopR + 18];
  }
  const pt = (t, bits) => land ? [A(t), laneOff(bits)] : [laneOff(bits), A(t)];
  // time axis
  if (land) {
    const y = (opts.compact ? 300 : 415);
    b += line(A(0), y, A(T0 - 1), y, DIM, 1.5);
    for (const t of opts.ticks) { b += line(A(t), y - 4, A(t), y + 4, MUTED, 1.5) + T(A(t), y + 22, String(t), { size: 13, anchor: 'middle', fill: MUTED }); }
    b += T(A(0), y + 44, 'turn (backward from the present)', { size: 13, fill: MUTED });
  } else {
    const x = 30;
    b += line(x, A(0), x, A(T0 - 1), DIM, 1.5);
    for (const t of opts.ticks) { b += line(x - 4, A(t), x + 4, A(t), MUTED, 1.5) + T(x + 8, A(t) + 5, String(t), { size: 14, fill: MUTED }); }
  }
  // lanes
  for (const L of lanes) {
    const col = LANE[L.bits], path = L.path || [];
    const first = L.verdict === 'REACHABLE' ? 0 : (L.stopTurn ?? T0 - 1);
    const turns = path.length ? path.map((_, i) => first + i) : [T0 - 1];
    // connector to the present (the one played turn)
    const [lx, ly] = pt(T0 - 1, L.bits);
    b += pathD(land ? `M${r1(lx)} ${r1(ly)} C${r1(lx + 30)} ${r1(ly)} ${r1(presentPt[0] - 30)} ${r1(presentPt[1])} ${r1(presentPt[0])} ${r1(presentPt[1])}`
                    : `M${r1(lx)} ${r1(ly)} C${r1(lx)} ${r1(ly + 30)} ${r1(presentPt[0])} ${r1(presentPt[1] - 30)} ${r1(presentPt[0])} ${r1(presentPt[1])}`,
      col, 2.5, `class="tw-step" data-t="${T0 - 1}" opacity="0.9"`);
    if (turns.length > 1) {
      const [ax, ay] = pt(turns[0], L.bits);
      b += line(ax, ay, lx, ly, col, 2.5, `class="tw-lane" data-from="${turns[0]}" opacity="0.55"`);
    }
    turns.forEach(t => { const [x, y] = pt(t, L.bits); b += circ(x, y, land ? 2.6 : 2.4, col, `class="tw-step" data-t="${t}"`); });
    const [sx, sy] = pt(turns[0], L.bits);
    if (L.verdict === 'REACHABLE') {
      b += ring(sx, sy, 11, col, 2.5, `class="tw-step" data-t="0"`) + check(sx, sy, 5.5, GREEN, 3, `class="tw-step" data-t="0"`);
    } else {
      const cap = land ? line(sx - 9, sy - 13, sx - 9, sy + 13, RED, 4.5) : line(sx - 13, sy - 9, sx + 13, sy - 9, RED, 4.5);
      b += `<g class="tw-step tw-cap" data-t="${turns[0]}">${cap}</g>`;
    }
    // labels
    const lab = opts.label(L);
    if (land) {
      const lx0 = L.verdict === 'REACHABLE' ? sx + 18 : sx - 20, anchor = L.verdict === 'REACHABLE' ? 'start' : 'end';
      const yy = L.verdict === 'REACHABLE' ? sy - 32 : sy - 4;
      b += T(lx0, yy, lab[0], { size: 15, fill: col, anchor, weight: 600 });
      if (lab[1]) b += T(lx0, yy + 19, lab[1], { size: 13, fill: MUTED, anchor });
    } else {
      b += T(sx, sy - 22, L.bits, { size: 16, fill: col, anchor: 'middle', weight: 700 });
    }
  }
  // the present
  b += circ(...presentPt, 13, '#FFFFFF') + ring(...presentPt, 19, '#FFFFFF66', 1.5);
  if (land) { b += T(presentPt[0] + 16, presentPt[1] - 34, opts.presentLabel[0], { size: 15, weight: 600 }) + T(presentPt[0] + 16, presentPt[1] - 16, opts.presentLabel[1], { size: 13, fill: MUTED }); }
  else { b += T(presentPt[0] + 30, presentPt[1] + 5, opts.presentLabel[0], { size: 16, weight: 600 }) + T(presentPt[0] + 30, presentPt[1] + 24, opts.presentLabel[1], { size: 14, fill: MUTED }); }
  // forward: the object keeps going, then the periodic remnant
  b += line(...presentPt, ...fwdEnd, '#FFFFFF', 3, 'class="tw-fwd"');
  b += ring(...loopC, loopR, '#FFFFFF', 3, 'class="tw-fwd"');
  const arrowA = land ? [loopC[0], loopC[1] - loopR] : [loopC[0] + loopR, loopC[1]];
  b += pathD(land ? `M${r1(arrowA[0] - 9)} ${r1(arrowA[1] - 7)} L${r1(arrowA[0] + 3)} ${r1(arrowA[1])} L${r1(arrowA[0] - 9)} ${r1(arrowA[1] + 7)}`
                  : `M${r1(arrowA[0] - 7)} ${r1(arrowA[1] - 9)} L${r1(arrowA[0])} ${r1(arrowA[1] + 3)} L${r1(arrowA[0] + 7)} ${r1(arrowA[1] - 9)}`, '#FFFFFF', 3, 'class="tw-fwd"');
  b += circ(loopC[0] - loopR, loopC[1], 6, GREEN, 'class="tw-orbit"');
  b += T(loopC[0], loopC[1] - 4, opts.loopLabel[0], { size: land ? 15 : 16, anchor: 'middle', weight: 600 });
  b += T(loopC[0], loopC[1] + 16, opts.loopLabel[1], { size: 13, anchor: 'middle', fill: MUTED });
  if (opts.loopLabel[2]) b += land ? T(loopC[0], loopC[1] + loopR + 24, opts.loopLabel[2], { size: 13, anchor: 'middle', fill: GREEN })
                                   : T(loopC[0] + loopR + 12, loopC[1] + 5, opts.loopLabel[2], { size: 14, fill: GREEN });
  if (land) { b += T((presentPt[0] + fwdEnd[0]) / 2 + 6, presentPt[1] + 26, opts.fwdLabel, { size: 13, anchor: 'middle', fill: MUTED }); }
  else { b += T(presentPt[0] + 14, (presentPt[1] + fwdEnd[1]) / 2 + 5, opts.fwdLabel, { size: 14, fill: MUTED }); }
  let Hout = H;
  if (!land) { // portrait lane legend, below the loop
    let y = loopC[1] + loopR + 64;
    for (const L of lanes) {
      const lab = opts.label(L);
      b += circ(40, y - 5, 6, LANE[L.bits]) + T(56, y, lab[0], { size: 16, fill: LANE[L.bits], weight: 600 });
      if (lab[1]) { b += T(56, y + 20, lab[1], { size: 14, fill: MUTED }); y += 50; } else y += 30;
    }
    Hout = y + 6;
  }
  return svg(opts.id + orient, W, Hout, opts.title, opts.desc, b, orient);
}

// =====================================================================================
// Plate IV — the periodic remnant: every observed cycle length is a multiple of 52
// =====================================================================================
function plate4(orient) {
  const land = orient === 'land', R = D.remnant, W = land ? 1000 : 520, H = land ? 330 : 820;
  const maxM = 80, maxN = Math.max(...R.periods.map(p => p[1]));
  let b = '';
  if (land) {
    const x0 = 60, x1 = 950, y = 205, X = m => x0 + m / maxM * (x1 - x0);
    b += line(x0, y, x1, y, DIM, 2);
    for (let m = 0; m <= maxM; m++) b += line(X(m), y - (m % 10 ? 4 : 9), X(m), y + (m % 10 ? 4 : 9), m % 10 ? GRID : MUTED, 1.5);
    for (let m = 0; m <= maxM; m += 10) b += T(X(m), y + 58, m ? '52 × ' + m : '0', { size: 13, anchor: 'middle', fill: MUTED });
    for (const [p, n] of R.periods) { const m = p / 52, r = 5 + 26 * Math.sqrt(n / maxN); b += circ(X(m), y, r, '#58C4DD33') + ring(X(m), y, r, ZETA, 2) + circ(X(m), y, 3, ZETA); b += T(X(m), y - r - 10, fmt(p), { size: 12, anchor: 'middle', fill: TXT }); }
    b += T(x0, 52, 'Cycle lengths of the ' + fmt(R.cycles) + ' deals (of ' + fmt(R.deals) + ') that never end', { size: 18 });
    b += T(x0, 78, 'Only ' + R.periods.length + ' lengths occur: the values of 2·lcm(a, 26, 25 − a), each a multiple of 52 = 51 + 1.', { size: 15, fill: MUTED });
    b += T(x1, 300, 'disc area ∝ number of deals · the turn-85 present cycles at 3,744 = 52 × 72', { size: 13, anchor: 'end', fill: MUTED });
  } else {
    const y0 = 150, y1 = 760, x = 150, Y = m => y0 + m / maxM * (y1 - y0);
    b += line(x, y0, x, y1, DIM, 2);
    for (let m = 0; m <= maxM; m++) b += line(x - (m % 10 ? 4 : 9), Y(m), x + (m % 10 ? 4 : 9), Y(m), m % 10 ? GRID : MUTED, 1.5);
    for (let m = 0; m <= maxM; m += 10) b += T(x - 16, Y(m) + 5, m ? '52 × ' + m : '0', { size: 14, anchor: 'end', fill: MUTED });
    for (const [p, n] of R.periods) { const m = p / 52, r = 5 + 24 * Math.sqrt(n / maxN); b += circ(x, Y(m), r, '#58C4DD33') + ring(x, Y(m), r, ZETA, 2) + circ(x, Y(m), 3, ZETA) + T(x + r + 10, Y(m) + 5, fmt(p) + '  (' + n + ' deals)', { size: 14 }); }
    b += T(24, 50, fmt(R.cycles) + ' of ' + fmt(R.deals) + ' deals never end.', { size: 19 });
    b += T(24, 78, 'Every cycle length is a multiple of 52.', { size: 16, fill: MUTED });
    b += T(24, 102, 'Disc area ∝ number of deals.', { size: 14, fill: MUTED });
  }
  return svg('p4' + orient, W, H, 'The periodic remnant', `Of ${R.deals} seeded 17–17–17 deals, ${R.cycles} never end. Their cycle lengths take ${R.periods.length} values, all multiples of 52.`, b, orient);
}

// =====================================================================================
// Plate V — order twins in Prospect 51: poker forgets order, the archive lock keeps it
// =====================================================================================
function plate5(orient) {
  const land = orient === 'land', P = D.prospect, W = land ? 1000 : 520, H = land ? 360 : 900;
  const suit = { S: '♠', H: '♥', D: '♦', C: '♣' }, red = c => /[HD]$/.test(c);
  const card = (x, y, c, hi) => {
    const rank = c.slice(0, -1), s = c.slice(-1), col = red(c) ? '#E0584F' : '#1B2A24';
    return `<g><rect x="${r1(x)}" y="${r1(y)}" width="62" height="88" rx="7" fill="#F6F1E4" stroke="${hi ? TWIN : '#CFC7B2'}" stroke-width="${hi ? 3.5 : 1.5}"/>` +
      T(x + 8, y + 22, rank, { size: 17, fill: col, weight: 700 }) + T(x + 31, y + 60, suit[s], { size: 30, fill: col, anchor: 'middle' }) + '</g>';
  };
  const row = (x, y, hand, swapIdx, dx) => hand.map((c, i) => card(x + i * dx, y, c, swapIdx.includes(i))).join('');
  let b = '';
  if (land) {
    const x0 = 70, dx = 74;
    b += T(x0, 60, 'the archive key', { size: 16, fill: MUTED }) + row(x0, 74, P.key, [1, 2], dx);
    b += T(x0, 218, 'its order twin', { size: 16, fill: MUTED }) + row(x0, 232, P.twin, [1, 2], dx);
    // swap arrows between the two red jacks
    b += pathD(`M${x0 + dx + 31} 166 C${x0 + dx + 31} 196 ${x0 + 2 * dx + 31} 196 ${x0 + 2 * dx + 31} 226`, TWIN, 2.5) + pathD(`M${x0 + 2 * dx + 31} 166 C${x0 + 2 * dx + 31} 196 ${x0 + dx + 31} 196 ${x0 + dx + 31} 226`, TWIN, 2.5);
    // the two readings
    const cx1 = 560, cx2 = 800;
    b += T(cx1, 52, 'poker', { size: 18, anchor: 'middle' }) + T(cx1, 70, 'order-blind', { size: 13, anchor: 'middle', fill: MUTED });
    b += T(cx2, 52, 'archive lock', { size: 18, anchor: 'middle' }) + T(cx2, 70, 'reads the order', { size: 13, anchor: 'middle', fill: MUTED });
    b += T(cx1, 124, P.category + ' · ' + P.grossPoints, { size: 17, anchor: 'middle', fill: ZETA }) + T(cx1, 282, P.category + ' · ' + P.grossPoints, { size: 17, anchor: 'middle', fill: ZETA });
    b += T(cx1, 206, '=', { size: 30, anchor: 'middle', fill: ZETA });
    b += check(cx2 - 50, 118, 10, GREEN, 4) + T(cx2 - 30, 124, 'opens', { size: 17, fill: GREEN });
    b += cross(cx2 - 50, 276, 9, RED, 4) + T(cx2 - 30, 282, 'stays shut', { size: 17, fill: RED });
    b += line(470, 40, 470, 330, GRID, 1.5) + line(690, 40, 690, 330, GRID, 1.5);
  } else {
    const x0 = 60, dx = 82;
    b += T(x0, 50, 'the archive key', { size: 17, fill: MUTED }) + row(x0, 64, P.key, [1, 2], dx);
    b += T(x0, 218, 'its order twin', { size: 17, fill: MUTED }) + row(x0, 232, P.twin, [1, 2], dx);
    b += pathD(`M${x0 + dx + 31} 156 C${x0 + dx + 31} 190 ${x0 + 2 * dx + 31} 190 ${x0 + 2 * dx + 31} 226`, TWIN, 2.5) + pathD(`M${x0 + 2 * dx + 31} 156 C${x0 + 2 * dx + 31} 190 ${x0 + dx + 31} 190 ${x0 + dx + 31} 226`, TWIN, 2.5);
    b += T(40, 400, 'poker · order-blind', { size: 19 });
    b += T(40, 434, 'key: ' + P.category + ' · ' + P.grossPoints, { size: 17, fill: ZETA }) + T(40, 462, 'twin: ' + P.category + ' · ' + P.grossPoints, { size: 17, fill: ZETA }) + T(40, 494, 'the same reading', { size: 15, fill: MUTED });
    b += T(40, 580, 'archive lock · reads the order', { size: 19 });
    b += check(52, 612, 9, GREEN, 4) + T(72, 618, 'key: opens', { size: 17, fill: GREEN });
    b += cross(52, 648, 8, RED, 4) + T(72, 654, 'twin: stays shut', { size: 17, fill: RED });
  }
  return svg('p5' + orient, W, H, 'Order twins in Prospect 51', `${P.key.join(' ')} and ${P.twin.join(' ')} are both ${P.category}. Only the first order opens the archive lock.`, b, orient);
}

// ---------- plate II configurations ----------
const lab85 = L => ({
  '00': ['00 · the recorded past', 'runs back to the 17–17–17 deal'],
  '01': ['01 · stops at once', 'lengths 36·14·1; the clock needs ≡ 2 (mod 3)'],
  '10': ['10 · stops at turn 66', `all ${L.statesExpanded} backward states die`],
  '11': ['11 · stops at once', 'lengths 33·17·1; the clock needs ≡ 2 (mod 3)']
})[L.bits];
const S85 = D.sedaps85, S32 = D.sedaps32;
const opt85 = orient => ({
  id: 'p2', ticks: [0, 17, 34, 51, 66, 84], label: lab85, presentLabel: ['the present · turn 85', S85.endpointSizes.join(' · ') + ' cards'],
  fwdLabel: 'turns 85 → 356', loopLabel: ['period ' + fmt(S85.forward.period), '= 52 × ' + S85.forward.periodOver52, 'never ends'],
  title: 'Twins at the table: four legal pasts of one SEDAPS present',
  desc: 'Four legal pasts reach the turn-85 present. Run backward, 01 and 11 stop at once (mod-3 clock), 10 stops at turn 66, and only 00 reaches the 17–17–17 deal. Run forward, the present enters a cycle at turn 356 of period 3,744 and never ends.'
});
const opt32 = orient => ({
  id: 'p3', compact: true, ticks: [0, 17, 31], label: L => [L.bits + ' · its own deal', ''], presentLabel: ['the present · turn 32', S32.endpointSizes.join(' · ') + ' cards'],
  fwdLabel: 'turns 32 → ' + fmt(S32.forward.enters), loopLabel: ['period ' + fmt(S32.forward.period), '= 52 × ' + S32.forward.periodOver52],
  title: 'Four for four: a present whose four pasts all come from deals',
  desc: 'At a certified turn-32 present, all four legal pasts are reached from four different 17–17–17 deals. The present then cycles with period 780 = 52 × 15.'
});

// ---------- page ----------
const plates = [
  { id: 'plate-1', num: 'I', h: 'The pair.', lead: 'ζ and a function with the same completed reflection symmetry s ↔ 1 − s, but a different Gamma factor and no Euler product, climb the same ladder of positivity tests. The twin’s finite-census scans detect a negative at rung 16,589 near x = 7140.07. Earlier sampled tests are positive; this is numerical evidence, not a certificate over every x. The ζ track shows the inherited verified-height bound.',
    svgs: [plate1('land'), plate1('port')], chips: [['PROVED', 'the twin must fail some rung'], ['EVID', 'detected negative at k = 16,589 on the finite zero list (rechecked at 40, 60 and 100 digits)'], ['CERT', 'ζ passes every k ≤ K_H (verified-height channel)'], ['OPEN', 'ζ passes every k ⇔ RH']],
    note: 'Source: TN Postmaster Volume I v5.2, Technical Dossier §§69A–69B. The twin is completed as (5/π)<sup>s/2</sup>Γ((s+1)/2)f(s): it shares the reflection of ξ, not its Gamma factor. (The textbook odd-character form has (5/π)<sup>(s+1)/2</sup>. The two differ by the constant (5/π)<sup>1/2</sup>, which cancels in the reflection and in the logarithmic derivative that every rung uses. The choice is deliberate.) The rungs are evaluated from its zeros below height 260, so the detected negative is a computation on that list, not a certificate over all zeros. The shrinking circles are the trapped-tip cascade of <a href="/papers/Volume_I_Exact_Geometry_and_Symbolic_Foundations.pdf">Volume I</a>, used only to draw “infinitely many rungs” in finite width.' },
  { id: 'plate-2', num: 'II', h: 'At the table.', lead: 'In 51 SEDAPS one present can have four legal pasts. They are twins: each one steps to the same present under the same rule. Here the equal 17–17–17 start and elapsed turn count 85 are known, so only a past that traces back to a fair deal in exactly 84 turns is real. Run the tape backward and watch which twins stop.',
    svgs: [plate2('land', S85, opt85('land')), plate2('port', S85, opt85('port'))], run: true,
    chips: [['PROVED', '01 and 11 fail the mod-3 clock'], ['COMPUTED', '10 at turn 84: every backward history dies by turn 66'], ['CERT', '10 does come from fair deals, at turns 24, 27, 30 and 33'], ['CERT', '00: the recorded deal replays'], ['CERT', 'forward cycle: turn 356, period 3,744']],
    note: 'The mod-3 clock: while three queues are live, each loses one card a turn and the winner gains three, so every length is ≡ 17 − t (mod 3). At turn 84 that is 2, and the lengths of 01 and 11 fall in three different classes, so no turn works for them. The turn count matters for 10: fair deals reach it at turns 24, 27, 30 and 33, never at 84. Without the turn count, two twins survive and one bit tells them apart. Details and scripts: <a href="/area-51/sedaps-51/RESEARCH_UPDATE_v0_4_1.md">SEDAPS research update v0.4.1</a>.' },
  { id: 'plate-3', num: 'III', h: 'Four for four.', lead: 'The gate does not always pick one. At this certified present, four different fair deals lead to its four different pasts. Every twin is real.',
    svgs: [plate2('land', S32, opt32('land')), plate2('port', S32, opt32('port'))],
    chips: [['CERT', 'four deals replayed with the shipped rule'], ['CERT', 'forward cycle: period 780 = 52 × 15']],
    note: 'Five such presents are certified (turns 32, 35, 41, 50 and 53). So four pasts is the true maximum even among states reached from fair deals.' },
  { id: 'plate-4', num: 'IV', h: 'The periodic remnant.', lead: 'A SEDAPS game has finitely many states, so a game that never ends must repeat. What is left is a loop. Its length keeps a clean integer: every loop observed so far is a multiple of 52, one more than the 51 cards in play.',
    svgs: [plate4('land'), plate4('port')], chips: [['CERT', 'each listed cycle replays exactly'], ['PROVED', 'two-queue loops: L = 2·lcm(a, 26, 25 − a), a multiple of 52'], ['OPEN', 'a loop that keeps three queues live']],
    note: 'Why 52: once one queue is empty, the game is War with the winning card placed first. For odd decks its loops alternate winners (Spivey 2010), and alternation forces the period 2·lcm(a, 26, 25 − a). Those are exactly the 12 lengths drawn here. Complete censuses of every state for 5, 7, 9 and 11 cards find only lengths divisible by n + 1, and no loop with three live queues; 12 odd deck sizes up to 51 were also sampled. Among even decks, 4, 6, 8 and 12 cards never loop. Compare Volume I: the silver cascade leaves an exact rational void, 1/28 of the cone. Same shape of result (messy process, clean remnant); not the same mathematics.' },
  { id: 'plate-5', num: 'V', h: 'Order twins.', lead: 'In Prospect 51, poker reads a hand as a set and ignores the order. The archive lock reads the order. Swap the two red jacks of the archive key and poker cannot tell the difference. The lock can.',
    svgs: [plate5('land'), plate5('port')], chips: [['PROVED', 'same poker category, checked by the shipped engine'], ['PROVED', 'only the key order opens the lock']],
    note: 'This has the same logical shape as the orientation firewall in Dossier §69C: a test that is symmetric under swapping cannot see what the swap changes. The shape is shared; the theorems are different.' }
];
const chip = ([s, t]) => `<li><span class="tw-chip tw-${s.toLowerCase().replace(/[^a-z]/g, '')}">${esc(s)}</span>${esc(t)}</li>`;
const nav = `<a href="/area-51/">The lab</a><a href="/area-51/invariant/">Invariant</a><a href="/area-51/blackjack-51/">Blackjack 51</a><a href="/area-51/telescope-51/">Telescope 51</a><a href="/area-51/sedaps-51/">51 SEDAPS</a><a href="/area-51/memory-51/">Memory 51</a><a href="/area-51/prospect-51/">Prospect 51</a><a href="/finance/live.html">Finance ↗</a><a href="/">Main site</a>`;
const html = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="dark"><meta name="theme-color" content="#000000">
<title>51 Twins · Area 51</title>
<meta name="description" content="Two runs obey the same rule for a long time; one gate lets only one through. Exact still plates: zeta and its Davenport–Heilbronn twin, the four pasts of a 51 SEDAPS present, the periodic remnant, and order twins in Prospect 51.">
<link rel="canonical" href="https://cerebralgraphix.com/area-51/twins-51/"><link rel="icon" href="/favicon.svg">
<meta name="author" content="Jeffery Lyn Huckstead"><meta name="citation_author" content="Jeffery Lyn Huckstead"><meta name="citation_title" content="51 Twins"><meta name="citation_public_url" content="https://cerebralgraphix.com/area-51/twins-51/">
<meta property="og:title" content="51 Twins · Area 51"><meta property="og:description" content="Same rule, one gate: which twin keeps going."><meta property="og:url" content="https://cerebralgraphix.com/area-51/twins-51/"><meta property="og:type" content="website">
<link rel="author" href="https://orcid.org/0009-0007-0234-2177">
<link rel="stylesheet" href="/area-51/assets/area51-v2.css"><link rel="stylesheet" href="/area-51/assets/card-ui-v2-5.css"><link rel="stylesheet" href="twins-v1.css">
</head>
<body class="a51-page tw-page" data-game="twins">
<div class="a51-shell">
<header class="game-header"><a href="/area-51/" class="game-brand"><span>Ⅰ</span>AREA 51 / CEREBRAL GRAPHIX</a><details class="game-switch"><summary>Games ▾</summary><nav aria-label="Area 51 games">${nav}</nav></details></header>
<main>
<section class="a51-intro tw-intro"><div><p class="a51-eyebrow">Exhibit · exact still plates · RH OPEN</p><h1>51 <span class="tw-gold">Twins.</span></h1>
<p>Two runs obey the same rule for a long time. Then a gate lets only one of them through. Each plate below is drawn from checked data. Nothing on this page is a simulation, and nothing is a claim about the Riemann hypothesis.</p></div></section>
<nav class="tw-toc" aria-label="Plates">${plates.map(p => `<a href="#${p.id}"><b>${p.num}</b> ${esc(p.h.replace('.', ''))}</a>`).join('')}</nav>
${plates.map(p => `<figure class="tw-plate" id="${p.id}">
<figcaption><span class="tw-num">${p.num}</span><div><h2>${esc(p.h)}</h2><p>${esc(p.lead)}</p></div></figcaption>
<div class="tw-frame">${p.svgs.join('')}</div>
${p.run ? `<div class="tw-run" data-for="${p.id}"><div class="tw-guess" role="group" aria-label="Guess which past reaches the deal"><span>Which past reaches the deal?</span>${['00', '01', '10', '11'].map(bb => `<button type="button" data-guess="${bb}" aria-pressed="false">${bb}</button>`).join('')}</div><div class="tw-run-actions"><button type="button" class="primary" data-run>Run the tape</button><button type="button" data-stop hidden>Stop the loop</button></div><p class="tw-run-status" role="status" aria-live="polite">Pick a past, then run the tape backward from turn 85.</p></div>` : ''}
<ul class="tw-chips">${p.chips.map(chip).join('')}</ul>
<p class="tw-note">${p.note}</p>
</figure>`).join('\n')}
<section class="tw-copy" id="game"><p class="a51-eyebrow">51 Twins as a game system · proposed, not built</p><h2>Same rule, one gate.</h2>
<p>A “twin” is any pair of runs that one rule cannot separate and another rule can. That gives each table a natural twin mode:</p>
<ul><li><strong>SEDAPS · Twin Gate.</strong> Show a present and its legal pasts. The player names the past that reaches a fair deal, then runs the tape. The answer is exact and checkable, and some presents admit more than one (plate III).</li>
<li><strong>Prospect · Order Twin.</strong> When a hand holds the archive key's five cards in the wrong order, show its twin: same poker award, closed lock.</li>
<li><strong>The ladder.</strong> Twins can agree for a very long time. On the sampled range, the first detected split between ζ and its twin comes at rung 16,589. Where the first split falls is itself the thing to study.</li></ul>
<p>These are proposals for the author. No jbits are staked or paid on this page.</p></section>
<section class="tw-copy" id="ledger"><p class="a51-eyebrow">Status ledger</p><h2>What each plate rests on.</h2>
<table class="tw-ledger"><thead><tr><th>Statement</th><th>Status</th><th>Where</th></tr></thead><tbody>
<tr><td>The Davenport–Heilbronn twin fails some Widder rung</td><td>PROVED</td><td>Dossier v5.2 Theorem 69A.1</td></tr>
<tr><td>Finite-census scans detect W<sub>16589</sub>(7140.07) &lt; 0; earlier sampled tests are positive (finite zero list; 40-, 60- and 100-digit rechecks agree)</td><td>EVID</td><td>Dossier §69A; <a href="calibration.html">calibration report</a></td></tr>
<tr><td>ζ passes every rung k ≤ K<sub>H</sub> ≈ 4.7 × 10<sup>12</sup></td><td>CERT (verified height)</td><td>Reading Volume §R13</td></tr>
<tr><td>ζ passes every rung</td><td>OPEN (⇔ RH)</td><td>Reading Volume (R.4)</td></tr>
<tr><td>Turn-85 pasts 01 and 11 cannot come from a 17–17–17 deal</td><td>PROVED</td><td>mod-3 clock, SEDAPS update v0.4 §2</td></tr>
<tr><td>Turn-85 past 10 cannot come from a 17–17–17 deal in 84 turns</td><td>COMPUTED</td><td>exhaustive search under the proved shape lemma</td></tr>
<tr><td>Past 10 does come from 17–17–17 deals at turns 24, 27, 30 and 33, and at no other turn</td><td>CERT + COMPUTED</td><td><code>past10-certificates-v0-4-1.json</code>, <code>verify-past10-v0-4-1.cjs</code></td></tr>
<tr><td>Turn-85 present cycles from turn 356 with period 3,744; turn-32 present with period 780</td><td>CERT</td><td>deterministic replay, <code>verify-twins-v1.cjs</code></td></tr>
<tr><td>Four legal pasts all reached from deals (turns 32, 35, 41, 50, 53)</td><td>CERT</td><td><code>dstart4-certificates-v0-4.json</code></td></tr>
<tr><td>Every observed cycle length is a multiple of 52</td><td>EVID</td><td>2,000 seeded deals; 12 sampled odd deck sizes from 7 to 51</td></tr>
<tr><td>A two-queue loop has length 2·lcm(α/2, (n+1)/2, (n−1−α)/2), a multiple of n + 1</td><td>PROVED (alternation: Spivey 2010)</td><td>SEDAPS update v0.4.1 §2; complete censuses n ≤ 11</td></tr>
<tr><td>No loop keeps three queues live</td><td>false at n = 12 (CERT); none for n ≤ 11 or n = 13</td><td>complete censuses; SEDAPS update v0.4.1 §2</td></tr>
<tr><td>No such loop is reachable from an equal deal</td><td>COMPUTED for n = 9, 12, 15; OPEN at 51</td><td>the mod-3 clock keeps equal-deal sizes congruent; exhaustive search at n = 12</td></tr>
<tr><td>Key and order twin share a poker category; only the key opens the lock</td><td>PROVED</td><td>Prospect 51 engine</td></tr>
</tbody></table>
<p class="tw-note">Replay the card results: <code>node area-51/twins-51/verify-twins-v1.cjs</code> rebuilds <a href="twins-data-v1.js">twins-data-v1.js</a> from the shipped SEDAPS rule, certificates and Prospect engine and checks it byte for byte. Its analytic constants are copied from the Dossier evidence; that command does not independently recompute or certify them. The two rung signs at k = 16,588 and 16,589 are recomputed separately by <code>evidence/dh_twin_highprec.py</code>. <code>build-twins-page-v1.cjs</code> redraws this page from that data.</p></section>
<section class="tw-copy" id="cite"><p class="a51-eyebrow">Cite</p><p>Jeffery Lyn Huckstead, <em>51 Twins v1: exact still plates</em>, Cerebral Graphix, 2026. Part of <em>Project 51: Reading the Record Across Rules</em>, <a href="https://doi.org/10.5281/zenodo.23004789">10.5281/zenodo.23004789</a>. The TN Postmaster numbers cite Volume I v5.2, <a href="https://doi.org/10.5281/zenodo.23004335">10.5281/zenodo.23004335</a> (version series <a href="https://doi.org/10.5281/zenodo.21968915">10.5281/zenodo.21968915</a>).</p></section>
<section class="tw-copy" id="sources"><p class="a51-eyebrow">Read further</p><div class="a51-actions"><a class="a51-button primary" href="calibration.html">Twin calibration report</a><a class="a51-button" href="/area-51/sedaps-51/">Play 51 SEDAPS</a><a class="a51-button" href="/area-51/prospect-51/">Play Prospect 51</a><a class="a51-button soft" href="/research/postmaster/">TN Postmaster</a><a class="a51-button soft" href="/papers/Volume_I_Exact_Geometry_and_Symbolic_Foundations.pdf">Volume I · trapped tip</a></div></section>
</main>
<footer class="a51-foot"><span>51 Twins v1 · Jeffery Lyn Huckstead / Cerebral Graphix · CC BY 4.0</span><span>RH STATUS: OPEN</span></footer>
</div>
<script src="twins-data-v1.js"></script><script src="twins-v1.js"></script>
</body>
</html>
`;
const out = here('index.html');
if (process.argv.includes('--write')) { fs.writeFileSync(out, html); console.log('wrote', out, html.length, 'bytes'); }
else if (fs.readFileSync(out, 'utf8') !== html) { console.error('index.html is stale; run with --write'); process.exit(1); }
else console.log('index.html matches the data');
