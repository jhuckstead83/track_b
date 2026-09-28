// 51 SEDAPS v0.4 verifier. Trusts the shipped rule (sedaps-core-v0-2.js) for every forward step.
// Usage: node verify-sedaps-v0-4.cjs [--decks]     (--decks adds the deck-size sweep, a few minutes)
'use strict';
const path = require('path'), fs = require('fs'), vm = require('vm'), assert = require('assert/strict');
const here = f => path.join(__dirname, f);
// area-51/package.json declares ES modules, so the browser scripts are run as classic scripts.
for (const f of ['sedaps-core-v0-2.js', 'sedaps-research-v0-3.js', 'sedaps-lemma-v0-4.js']) vm.runInThisContext(fs.readFileSync(here(f), 'utf8'), { filename: f });
const C = globalThis.SedapsCore, R = globalThis.SedapsResearch, L = globalThis.SedapsLemma;
const cert85 = JSON.parse(fs.readFileSync(here('reachable-certificate-v0-3.json'), 'utf8'));
const { certificates } = JSON.parse(fs.readFileSync(here('dstart4-certificates-v0-4.json'), 'utf8'));
const key = y => y.map(q => q.join(',')).join('|'), sizes = y => y.map(q => q.length);
const receipt = { version: '0.4', rule: 'sedaps-core-v0-2.js', RH_STATUS: 'OPEN', checks: [] };
const ok = (name, detail) => { receipt.checks.push({ name, pass: true, ...(detail ? { detail } : {}) }); console.log('PASS', name, detail ? JSON.stringify(detail) : ''); };

// 1. The v0.3 certificate and constructed-witness obstruction still verify.
const rep = R.verifyCertificate(cert85);
assert.equal(R.prefixFloor(C.ENDPOINT[0]).minimum, 44);
ok('v0.3 certificate replays; constructed witness needs a 44-card prefix', { admissibleByPrefixFloor: rep.admissibleBits });

// 2. Start-class verdicts for the turn-85 present.
const v = L.startVerdicts(C, cert85);
assert.equal(v.map(x => `${x.bits}:${x.verdict}:${x.reason}:${x.stopTurn}`).join(','), '00:REACHABLE:recorded:0,01:EXCLUDED:mod3:null,10:EXCLUDED:search:66,11:EXCLUDED:mod3:null');
const pre = C.predecessors(cert85.states[85]);
for (const i of [1, 3]) { const c = L.clockFails(pre[i], 84); assert.ok(c && c.want === 2, 'mod-3 clock rejects ' + C.BITS[i]); }
const e10 = L.explore(pre[2], 84);
assert.ok(!e10.capped && !e10.reachesDeal && e10.lowestTurn === 66);
e10.deepestPath.forEach((z, i) => { if (i) assert.ok(C.same(C.transition(z).after, e10.deepestPath[i - 1])); });
ok('turn 85: only 00 comes from a 17-17-17 deal', { '01': pre[1].map(q => q.length), '11': pre[3].map(q => q.length), '10': { lowestTurn: 66, statesExpanded: e10.statesExpanded } });

// 3. Four for four: five presents whose four legal pasts all come from 17-17-17 deals.
for (const c of certificates) {
  const p = C.predecessors(c.endpoint); assert.equal(p.length, 4);
  c.branches.forEach((b, i) => {
    assert.ok(C.same(p[i], b.predecessor)); assert.ok(b.deal.every(q => q.length === 17)); C.assertState(b.deal);
    let y = b.deal; for (let k = 0; k < c.t - 1; k++) y = C.transition(y).after;
    assert.ok(C.same(y, b.predecessor)); assert.ok(C.same(C.transition(y).after, c.endpoint));
  });
}
ok('four-for-four certificates replay', { turns: certificates.map(c => c.t) });

// 4. Shape-lemma soundness on seeded play (an implementation check; the lemma itself is proved).
function mulberry32(a) { return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
function deal(seed, deck = C.ACTIVE) { const r = mulberry32(seed), d = deck.slice(); for (let i = d.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [d[i], d[j]] = [d[j], d[i]]; } const y = [[], [], []]; d.forEach((c, i) => y[i % 3].push(c)); return y; }
let pairs = 0;
for (let seed = 1; seed <= 300; seed++) { let y = deal(seed); for (let t = 0; t < 1500 && y.filter(q => q.length).length >= 2; t++) { assert.ok(L.shapeOK(y, t), `shape lemma rejected a reached state (seed ${seed}, turn ${t})`); pairs++; y = C.transition(y).after; } }
ok('shape lemma accepts every reached (state, turn) in 300 seeded games', { pairs });

// 5. Forward fates: the shared presents keep going and are trapped in loops.
function fate(y, t, deck) { const seen = new Map(); while (true) { if (y.filter(q => q.length).length < 2) return { kind: 'end', turn: t }; const k = key(y); if (seen.has(k)) return { kind: 'cycle', enters: seen.get(k), period: t - seen.get(k) }; seen.set(k, t); y = C.transition(y, deck).after; t++; } }
const f85 = fate(cert85.states[85], 85);
assert.deepEqual(f85, { kind: 'cycle', enters: 356, period: 3744 });
const fates = certificates.map(c => ({ t: c.t, ...fate(c.endpoint, c.t) }));
ok('turn-85 present: loop from turn 356, period 3,744', { fourForFour: fates });

// 6. The periodic remnant: 2,000 seeded deals.
const gcd = (a, b) => b ? gcd(b, a % b) : a; let g = 0, ends = 0, cycles = 0; const periods = new Map();
for (let seed = 1; seed <= 2000; seed++) { const f = fate(deal(seed), 0); if (f.kind === 'end') ends++; else { cycles++; g = gcd(g, f.period); periods.set(f.period, (periods.get(f.period) || 0) + 1); } }
assert.equal(g, 52); assert.equal(cycles, 1652);
ok('periodic remnant: every observed loop length is a multiple of 52 (EVID)', { deals: 2000, ends, cycles, gcd: g, periods: [...periods].sort((a, b) => a[0] - b[0]) });

// 7. Optional deck-size sweep: loop lengths versus n + 1.
if (process.argv.includes('--decks')) {
  const rows = [];
  for (const n of [6, 7, 8, 9, 10, 11, 12, 13, 15, 17, 20, 21, 24, 27, 30, 33, 39, 45, 48, 51]) {
    const deck = Array.from({ length: n }, (_, i) => i); let gg = 0, cyc = 0; const ps = new Set();
    for (let seed = 1; seed <= 300; seed++) { const r = mulberry32(seed * 7919 + n), d = deck.slice(); for (let i = n - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [d[i], d[j]] = [d[j], d[i]]; } const y = [[], [], []]; d.forEach((c, i) => y[i % 3].push(c)); const f = fate(y, 0, deck); if (f.kind === 'cycle') { cyc++; gg = gcd(gg, f.period); ps.add(f.period); } }
    rows.push({ n, cycles: cyc, gcd: gg, allDivisibleByNplus1: cyc ? [...ps].every(p => p % (n + 1) === 0) : null });
  }
  ok('deck-size sweep (EVID)', { rows });
}
receipt.status = 'PASS';
fs.writeFileSync(here('VERIFY_v0_4.json'), JSON.stringify(receipt, null, 1) + '\n');
