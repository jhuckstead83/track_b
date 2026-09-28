// 51 SEDAPS v0.4.1 — exact number of 17–17–17 deals whose play reaches a given present at a given turn.
// Trusts the shipped rule (sedaps-core-v0-2.js) and lemma (sedaps-lemma-v0-4.js) only.
// Usage: node count-histories-v0-4-1.cjs            (writes HISTORY_COUNTS_v0_4_1.json)
//        node count-histories-v0-4-1.cjs --brute    (also enumerates the small cases deal by deal)
//
// Method (RESEARCH_UPDATE_v0_4_1.md §1.2). Forward play is deterministic, so the backward histories of a
// present form a tree and the number of deals is the number of its leaves.
//  - Above turn 17 the tree is explored with the shape test (a proof of completeness is in §1.1).
//  - At a three-live state at turn t <= 16 the queues are their last 17 - t dealt cards followed by a, b, c
//    whole 3-packets, with a + b + c = t. Each backward step removes the last packet of one queue that has
//    one, so the counts obey Pascal's rule and the number of deals is the multinomial t! / (a! b! c!).
'use strict';
const path = require('path'), fs = require('fs'), vm = require('vm'), assert = require('assert/strict');
const here = f => path.join(__dirname, f);
for (const f of ['sedaps-core-v0-2.js', 'sedaps-lemma-v0-4.js']) vm.runInThisContext(fs.readFileSync(here(f), 'utf8'), { filename: f });
const C = globalThis.SedapsCore, L = globalThis.SedapsLemma;
const fact = [1n]; for (let i = 1; i <= 51; i++) fact.push(fact[i - 1] * BigInt(i));

function count(y, T) {
  let nodes = 0, boundary = 0;
  const go = (z, t) => {
    if (!L.shapeOK(z, t)) return 0n;
    nodes++;
    if (t <= 16 && z.every(q => q.length)) {
      const k = z.map(q => (q.length - (17 - t)) / 3);
      assert.equal(k[0] + k[1] + k[2], t); boundary++;
      return fact[t] / (fact[k[0]] * fact[k[1]] * fact[k[2]]);
    }
    if (t === 0) return z.every(q => q.length === 17) ? 1n : 0n;
    let s = 0n; for (const p of L.preds(z)) s += go(p, t - 1); return s;
  };
  const deals = go(y, T);
  return { deals, nodes, boundary };
}
function brute(y, T) {
  let deals = 0;
  (function go(z, t) {
    if (!L.shapeOK(z, t)) return;
    if (t === 0) { if (z.every(q => q.length === 17)) deals++; return; }
    for (const p of L.preds(z)) go(p, t - 1);
  })(y, T);
  return deals;
}

const cert = JSON.parse(fs.readFileSync(here('dstart4-certificates-v0-4.json'), 'utf8'));
const c85 = JSON.parse(fs.readFileSync(here('reachable-certificate-v0-3.json'), 'utf8'));
const receipt = { version: '0.4.1', rule: 'sedaps-core-v0-2.js', lemma: 'sedaps-lemma-v0-4.js', RH_STATUS: 'OPEN',
  meaning: 'number of 17-17-17 deals whose play reaches the state at the stated elapsed turn', presents: [], turn85: {}, checks: [] };

for (const c of cert.certificates) {
  const r = count(c.endpoint, c.t);
  const pasts = C.predecessors(c.endpoint).map((p, i) => ({ bits: C.BITS[i], dealsAtTurn: c.t - 1, deals: count(p, c.t - 1).deals.toString() }));
  assert.equal(pasts.reduce((s, p) => s + BigInt(p.deals), 0n), r.deals);
  assert.ok(pasts.every(p => BigInt(p.deals) > 0n));
  receipt.presents.push({ turn: c.t, deals: r.deals.toString(), statesSearched: r.nodes, boundaryStates: r.boundary, pasts });
  console.log(`turn ${c.t}: ${r.deals} deals (pasts ${pasts.map(p => p.bits + ' ' + p.deals).join(', ')})`);
}
const P = C.predecessors(c85.states[85]), p00 = P[C.BITS.indexOf('00')], p10 = P[C.BITS.indexOf('10')];
const n85 = count(c85.states[85], 85).deals, n00 = count(p00, 84).deals;
assert.equal(n85, n00);
receipt.turn85 = { present: n85.toString(), viaPast00AtTurn84: n00.toString(),
  past10: [24, 27, 30, 33].map(s => ({ turn: s, deals: count(p10, s).deals.toString() })) };
console.log(`turn 85: ${n85} deals, all through past 00; past 10 at turns 24/27/30/33: ${receipt.turn85.past10.map(r => r.deals).join(', ')}`);
receipt.checks.push({ name: 'every past of the five four-for-four presents is reached by at least one deal, and the pasts sum to the present', pass: true });
receipt.checks.push({ name: 'the turn-85 present is reached only through past 00', pass: true });

if (process.argv.includes('--brute')) {
  const cases = [[p10, 24], [p10, 27], [p10, 30], [p10, 33]];
  for (const [i, p] of C.predecessors(cert.certificates[0].endpoint).entries()) if (C.BITS[i] === '10') cases.push([p, 31]);
  for (const [y, t] of cases) { const b = brute(y, t), e = count(y, t).deals; assert.equal(BigInt(b), e); console.log(`brute force at turn ${t}: ${b} = formula`); }
  receipt.checks.push({ name: 'deal-by-deal enumeration equals the formula on five cases (past 10 of the turn-85 present at turns 24-33; past 10 of the turn-32 present)', pass: true });
}
receipt.status = 'PASS';
fs.writeFileSync(here('HISTORY_COUNTS_v0_4_1.json'), JSON.stringify(receipt, null, 1) + '\n');
