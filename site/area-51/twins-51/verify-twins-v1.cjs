// 51 Twins v1 — replay the card results and rebuild the exhibit data.
// Analytic constants below are imported claims, not recomputed certificates.
// Card replay uses the shipped files: the SEDAPS core, its v0.3 certificate, the v0.4
// d_start = 4 certificates and lemma, and the Prospect 51 engine.
// Usage: node verify-twins-v1.cjs          (verify twins-data-v1.js)
//        node verify-twins-v1.cjs --write  (rewrite twins-data-v1.js)
'use strict';
const path = require('path'), fs = require('fs'), vm = require('vm'), assert = require('assert/strict');
const here = (...p) => path.join(__dirname, ...p);
// area-51/package.json declares ES modules, so the browser scripts are run as classic scripts.
const script = f => vm.runInThisContext(fs.readFileSync(here(f), 'utf8'), { filename: f });
script('../sedaps-51/sedaps-core-v0-2.js'); script('../sedaps-51/sedaps-lemma-v0-4.js');
const C = globalThis.SedapsCore, L = globalThis.SedapsLemma;
const cert85 = JSON.parse(fs.readFileSync(here('../sedaps-51/reachable-certificate-v0-3.json'), 'utf8'));
const cert4 = JSON.parse(fs.readFileSync(here('../sedaps-51/dstart4-certificates-v0-4.json'), 'utf8'));
const sizes = y => y.map(q => q.length);
const key = y => y.map(q => q.join(',')).join('|');

// Forward fate from a state at turn t: end, or the cycle it falls into.
function fate(y, t, sample = 0) {
  const seen = new Map(), trace = [];
  while (true) {
    if (sample && (t % sample === 0)) trace.push([t, ...sizes(y)]);
    if (y.filter(q => q.length).length < 2) return { kind: 'end', turn: t, trace };
    const k = key(y);
    if (seen.has(k)) return { kind: 'cycle', enters: seen.get(k), period: t - seen.get(k), trace };
    seen.set(k, t); y = C.transition(y).after; t++;
  }
}

// ---- Plate II: the v0.3 turn-85 present and its four legal pasts
const T = cert85.turns, x85 = cert85.states[T];
cert85.states.forEach((s, i) => { if (i < T) assert.ok(C.same(C.transition(s).after, cert85.states[i + 1]), 'certificate replay ' + i); });
const verdicts = L.startVerdicts(C, cert85);
assert.deepEqual(verdicts.map(v => v.verdict), ['REACHABLE', 'EXCLUDED', 'EXCLUDED', 'EXCLUDED']);
assert.deepEqual(verdicts.map(v => v.reason), ['recorded', 'mod3', 'search', 'mod3']);
const p10 = C.predecessors(x85)[2], e10 = L.explore(p10, T - 1);
assert.equal(e10.lowestTurn, 66); assert.equal(e10.reachesDeal, false);
e10.deepestPath.forEach((z, i) => { if (i) assert.ok(C.same(C.transition(z).after, e10.deepestPath[i - 1]), 'deepest path replays forward'); });
const f85 = fate(x85, T, 8);
assert.equal(f85.kind, 'cycle'); assert.equal(f85.enters, 356); assert.equal(f85.period, 3744); assert.equal(f85.period % 52, 0);
const lanes85 = verdicts.map((v, i) => {
  const p = C.predecessors(x85)[i];
  const lane = { bits: v.bits, verdict: v.verdict, reason: v.reason, predecessorSizes: sizes(p), stopTurn: v.stopTurn, statesExpanded: v.statesExpanded };
  if (v.reason === 'recorded') lane.path = cert85.states.slice(0, T).map(sizes);            // turns 0..84
  if (v.reason === 'search') lane.path = e10.deepestPath.slice().reverse().map(sizes);      // turns 66..84
  if (v.clock) lane.clock = v.clock;
  return lane;
});

// ---- Companion: a certified present at turn 32 whose four pasts all come from 17–17–17 deals
const c32 = cert4.certificates.find(c => c.t === 32);
const x32 = c32.endpoint, pre32 = C.predecessors(x32);
assert.equal(pre32.length, 4);
const lanes32 = c32.branches.map((b, i) => {
  assert.ok(C.same(pre32[i], b.predecessor)); assert.ok(b.deal.every(q => q.length === 17));
  let y = b.deal; const path = [sizes(y)];
  for (let k = 0; k < c32.t - 1; k++) { y = C.transition(y).after; path.push(sizes(y)); }
  assert.ok(C.same(y, b.predecessor)); assert.ok(C.same(C.transition(y).after, x32));
  return { bits: b.bits, verdict: 'REACHABLE', path };
});
const f32 = fate(x32, 32, 8);
assert.equal(f32.kind, 'cycle'); assert.equal(f32.period % 52, 0);

// ---- The periodic remnant: forward fates of seeded 17–17–17 deals
function mulberry32(a) { return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const gcd = (a, b) => b ? gcd(b, a % b) : a;
const DEALS = 2000; let ends = 0, cycles = 0, g = 0; const periods = new Map();
for (let seed = 1; seed <= DEALS; seed++) {
  const r = mulberry32(seed), deck = C.ACTIVE.slice();
  for (let i = deck.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [deck[i], deck[j]] = [deck[j], deck[i]]; }
  const deal = [[], [], []]; deck.forEach((c, i) => deal[i % 3].push(c));
  const f = fate(deal, 0);
  if (f.kind === 'end') ends++; else { cycles++; g = gcd(g, f.period); periods.set(f.period, (periods.get(f.period) || 0) + 1); }
}
assert.equal(g, 52);

// ---- Plate III: Prospect 51 archive key and its order twin
const sandbox = { globalThis: {} }; sandbox.globalThis = sandbox; vm.createContext(sandbox);
for (const f of ['../prospect-51/data.js', '../prospect-51/engine.js']) vm.runInContext(fs.readFileSync(here(f), 'utf8'), sandbox, { filename: f });
const E = sandbox.P51Engine; assert.ok(E, 'Prospect engine loads');
const keyHand = [...E.ARCHIVE_KEY], twinHand = [keyHand[0], keyHand[2], keyHand[1], keyHand[3], keyHand[4]];
const sKey = E.score(keyHand), sTwin = E.score(twinHand);
assert.equal(sKey.category, sTwin.category); assert.equal(E.isKey(keyHand), true); assert.equal(E.isKey(twinHand), false);

// ---- Plate I inset: zeros below height 100
// ζ: the first 29 ordinates of the zeros_1438.txt fixture shipped in the Project 51 v0.3 package.
const zetaZeros = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062, 37.586178, 40.918719, 43.327073, 48.005151,
  49.773832, 52.970321, 56.446248, 59.347044, 60.831779, 65.112544, 67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
  79.337375, 82.910381, 84.735493, 87.425275, 88.809111, 92.491899, 94.651344, 95.870634, 98.831194];
const dh = JSON.parse(fs.readFileSync(here('evidence/dh-zeros-T260.json'), 'utf8'));
const twinOn = dh.online.filter(t => t < 100).map(t => +t.toFixed(6));
const twinOff = dh.offline.filter(([, t]) => t < 100).map(([s, t]) => [+s.toFixed(9), +t.toFixed(9)]);
assert.equal(twinOn.length, 52); assert.deepEqual(twinOff, [[0.808517182, 85.699348485]]);

const data = {
  version: '1.0', rh: 'OPEN',
  zeros: { zeta: zetaZeros, twinOnLine: twinOn, twinOffLine: twinOff },
  zeta: { // Technical Dossier v5.2 §§69A–69B; evidence in TN_Postmaster_Volume_I_v5_2_SOURCE/provenance/v5_2/evidence
    sectorSafe: 218, lastShared: 16588, firstFail: 16589, failX: 7140.066, offLineZero: '0.808517182 + 85.699348485i',
    w16588: 1.7592739e-4, w16589: -4.6600915e-5, KH: 4712664392502, lownerPsdThrough: 100, lownerFailsBy: 105, lownerSizesTested: 'multiples of 5', lownerExactFirstFail: { '0.97': 105, '1.00': 106, '1.03': 107 },
    detectionMedian: 0.806, detectionZeros: 15 },
  sedaps85: { turn: T, seed: cert85.seed, endpointSizes: sizes(x85), lanes: lanes85,
    forward: { enters: f85.enters, period: f85.period, periodOver52: f85.period / 52, trace: f85.trace.filter(r => r[0] <= f85.enters + f85.period) } },
  sedaps32: { turn: 32, endpointSizes: sizes(x32), lanes: lanes32, forward: { enters: f32.enters, period: f32.period, periodOver52: f32.period / 52 } },
  remnant: { deals: DEALS, ends, cycles, gcd: g, periods: [...periods].sort((a, b) => a[0] - b[0]) },
  prospect: { key: keyHand, twin: twinHand, category: sKey.name, grossPoints: sKey.grossCents / 100, keyOpens: true, twinOpens: false }
};
const out = here('twins-data-v1.js');
const text = '/* 51 Twins v1 exhibit data. Generated and checked by verify-twins-v1.cjs. CC BY 4.0. */\nglobalThis.TWINS51 = ' + JSON.stringify(data) + ';\n';
if (process.argv.includes('--write')) { fs.writeFileSync(out, text); console.log('wrote', out, text.length, 'bytes'); }
else { assert.equal(fs.readFileSync(out, 'utf8'), text, 'twins-data-v1.js differs from a fresh rebuild'); }
console.log(JSON.stringify({
  pass: true,
  turn85: lanes85.map(l => `${l.bits}:${l.verdict}(${l.reason}${l.stopTurn != null ? ', reaches turn ' + l.stopTurn : ''})`),
  forward85: `enters cycle at turn ${f85.enters}, period ${f85.period} = 52 x ${f85.period / 52}`,
  turn32: `four pasts, four deals; forward cycle at ${f32.enters}, period ${f32.period} = 52 x ${f32.period / 52}`,
  remnant: `${cycles}/${DEALS} cycle, ${ends} end; gcd of periods ${g}`,
  prospect: `${keyHand.join(' ')} vs ${twinHand.join(' ')}: both ${sKey.name}; only the first opens the archive`
}, null, 1));
