// 51 SEDAPS v0.4.1 — turn-indexed reachability of the four legal pasts of the turn-85 present.
// Trusts the shipped rule (sedaps-core-v0-2.js) and lemma (sedaps-lemma-v0-4.js) only.
// Usage: node verify-past10-v0-4-1.cjs            (writes VERIFY_v0_4_1.json)
// Place this file and past10-certificates-v0-4-1.json in area-51/sedaps-51/ of the site (v2.8.0 or later).
//
// Results:
//   01, 11  all-live pasts whose queue sizes are not congruent mod 3: excluded at EVERY elapsed turn (PROVED, mod-3 clock).
//   10      reached from a 17-17-17 deal exactly at elapsed turns 24, 27, 30, 33 (CERT, past10-certificates-v0-4-1.json);
//           no deal reaches it at any other elapsed turn (COMPUTED: complete backward search under the proved shape lemma
//           for turns 17..84; from turn 82 on no search checks a turn below 17, so the lemma sees the turn only mod 3 and
//           the verdict is 3-periodic for every later turn). The 3-periodicity is the mod-3 clock itself: for t >= 17 the
//           lemma reads t only through the clock residue (17 - t) mod 3 of the all-live phase, plus the threshold t >= 17.
//           The clock cannot exclude turn 84 on its own, since 24, 27, 30, 33 and 84 are all 0 mod 3; the search does.
//   00      the recorded past at turn 84 (CERT, reachable-certificate-v0-3.json).
//   Search soundness: the shape test is necessary on reached states with at least two live queues (PROVED,
//   RESEARCH_UPDATE_v0_4_1.md §1.1); check 5 replays it on 2,000 seeded deals, including their terminal states.
// So at elapsed turn 85 the present has exactly one past from a fair deal (zero history bits, given the turn count);
// if the turn count is not known, two pasts (00 and 10) survive and the leading bit alone recovers the past.
'use strict';
const path = require('path'), fs = require('fs'), vm = require('vm'), assert = require('assert/strict'), crypto = require('crypto');
const here = f => path.join(__dirname, f);
for (const f of ['sedaps-core-v0-2.js', 'sedaps-lemma-v0-4.js']) vm.runInThisContext(fs.readFileSync(here(f), 'utf8'), { filename: f });
const C = globalThis.SedapsCore, L = globalThis.SedapsLemma;
const cert85 = JSON.parse(fs.readFileSync(here('reachable-certificate-v0-3.json'), 'utf8'));
const past10 = JSON.parse(fs.readFileSync(here('past10-certificates-v0-4-1.json'), 'utf8'));
const canon = y => y.map(q => q.join(',')).join('|');
const sha = y => crypto.createHash('sha256').update(canon(y), 'utf8').digest('hex');
const receipt = { version: '0.4.1', rule: 'sedaps-core-v0-2.js', lemma: 'sedaps-lemma-v0-4.js', RH_STATUS: 'OPEN', checks: [] };
const ok = (name, detail) => { receipt.checks.push({ name, pass: true, ...(detail ? { detail } : {}) }); console.log('PASS', name, detail ? JSON.stringify(detail) : ''); };

const x85 = cert85.states[85], pre = C.predecessors(x85);
const bySize = Object.fromEntries(pre.map((p, i) => [p.map(q => q.length).join(','), { bits: C.BITS[i], p }]));
const P00 = bySize['36,15,0'], P01 = bySize['36,14,1'], P10 = bySize['34,17,0'], P11 = bySize['33,17,1'];
assert.equal(pre.length, 4); assert.equal(sha(x85), past10.present.sha256); assert.equal(sha(P10.p), past10.past10.sha256);
assert.equal(P00.bits, '00'); assert.equal(P01.bits, '01'); assert.equal(P10.bits, '10'); assert.equal(P11.bits, '11');

// 1. 01 and 11: three live queues whose sizes fall in three different residue classes mod 3.
for (const { p } of [P01, P11]) { assert.ok(p.every(q => q.length)); assert.equal(new Set(p.map(q => q.length % 3)).size, 3); }
ok('01 and 11 fail the mod-3 clock at every elapsed turn', { '01': P01.p.map(q => q.length), '11': P11.p.map(q => q.length) });

// 2. 10: four frozen certificates, replayed with the shipped rule.
for (const c of past10.certificates) {
  assert.ok(c.deal.every(q => q.length === 17)); C.assertState(c.deal); assert.equal(sha(c.deal), c.dealSha256);
  let y = c.deal; for (let k = 0; k < c.elapsedTurn; k++) y = C.transition(y).after;
  assert.ok(C.same(y, P10.p)); assert.equal(sha(y), c.past10Sha256); assert.ok(C.same(C.transition(y).after, x85));
}
ok('10 is reached from 17-17-17 deals at elapsed turns 24, 27, 30, 33 (frozen certificates)', { turns: past10.certificates.map(c => c.elapsedTurn) });

// 3. 10: complete searches at every other elapsed turn 17..84, and the 3-periodic closure.
const rows = [];
for (let s = 17; s <= 84; s++) {
  if (past10.certificates.some(c => c.elapsedTurn === s)) continue;
  const e = L.explore(P10.p, s);
  assert.ok(!e.capped, 'search capped at ' + s); assert.ok(!e.reachesDeal, 'unexpected deal at ' + s);
  rows.push([s, e.statesExpanded, e.lowestTurn]);
}
// lowestTurn is the lowest turn of a state that PASSED the test; its predecessors are tested one turn lower.
// So lowestTurn >= 18 means every test in the search is at a turn >= 17, where the lemma sees t only mod 3.
for (const s of [82, 83, 84]) assert.ok(rows.find(r => r[0] === s)[2] >= 18, 'closure needs every check at turn >= 17');
ok('10 is reached from no 17-17-17 deal at any other elapsed turn (turns 17-84 searched; 3-periodic from turn 82)', { searched: rows.length, turn84: rows.find(r => r[0] === 84) });

// 4. 00: the recorded past at turn 84.
cert85.states.forEach((s, i) => { if (i < 85) assert.ok(C.same(C.transition(s).after, cert85.states[i + 1])); });
assert.ok(C.same(cert85.states[84], P00.p));
ok('00 is the recorded past at turn 84 (v0.3 certificate replays)', { seed: cert85.seed });

// 5. Scope of the shape lemma (PP275): necessary on every reached state with at least two live queues;
//    terminal states (one queue holds all 51 cards) fail it by construction and are never predecessors.
function mulberry32(a) { return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
function deal(seed, deck = C.ACTIVE) { const r = mulberry32(seed), d = deck.slice(); for (let i = d.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [d[i], d[j]] = [d[j], d[i]]; } const y = [[], [], []]; d.forEach((c, i) => y[i % 3].push(c)); return y; }
let livePairs = 0, terminal = 0;
for (let seed = 1; seed <= 2000; seed++) {
  let y = deal(seed);
  for (let t = 0; t <= 6000; t++) {
    const k = y.filter(q => q.length).length;
    if (k < 2) { assert.ok(!L.shapeOK(y, t)); assert.equal(C.predecessors(y).every(p => p.filter(q => q.length).length >= 2), true); terminal++; break; }
    assert.ok(L.shapeOK(y, t), `shape lemma rejected a reached state (seed ${seed}, turn ${t})`); livePairs++;
    y = C.transition(y).after;
  }
}
assert.equal(terminal, 348);
ok('shape lemma scope: passes every reached state with >= 2 live queues; fails exactly the terminal states (2,000 seeded deals, to the end or turn 6,000)', { livePairs, terminalStates: terminal });

receipt.summary = {
  atTurn85: 'exactly one past from a fair deal (00): zero history bits, given the turn count',
  turnUnknown: 'two pasts from fair deals (00 at elapsed turn 84; 10 at elapsed turns 24, 27, 30, 33): the leading bit recovers the past',
  presentAlsoReachedAt: past10.certificates.map(c => c.presentTurn)
};
receipt.searchTable = rows;
receipt.status = 'PASS';
fs.writeFileSync(here('VERIFY_v0_4_1.json'), JSON.stringify(receipt, null, 1) + '\n');
console.log(JSON.stringify(receipt.summary, null, 1));
