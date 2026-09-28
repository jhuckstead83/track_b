'use strict';
const assert = require('node:assert/strict');
const imported = require('./sedaps-core-v0-2.js');
const core = imported.verifyWitness ? imported : globalThis.SedapsCore;
const report = core.verifyWitness();

// Independent replay: players are sorted by clockwise distance from winner.
function referenceMove(state) {
  const queues = state.map(q => q.slice());
  const exposed = queues.map((q,player) => q.length ? {player,q:q.shift()} : null).filter(Boolean);
  if (exposed.length < 2) return null;
  const winner = exposed.slice().sort((a,b) => b.q-a.q)[0].player;
  exposed.sort((a,b) => (a.player-winner+3)%3 - (b.player-winner+3)%3);
  queues[winner].push(...exposed.map(x => x.q));
  return queues;
}
for (const bits of core.BITS) assert.deepEqual(referenceMove(core.BRANCHES[bits]),core.ENDPOINT);
assert.throws(() => core.transition([core.ACTIVE.slice(),[],[]]),/terminal/);
const bad = core.copy(core.ENDPOINT);bad[0][0] = 7;
assert.throws(() => core.assertState(bad),/partition/);
bad[0][0] = bad[0][1];
assert.throws(() => core.assertState(bad),/partition/);

// Exhaustive finite control, independent of the suffix-based inverse:
// 6! permutations × 28 ordered cut pairs = 20,160 labeled queue states.
function* permutations(values) {
  if (!values.length) {yield [];return;}
  for (let i=0;i<values.length;i++) {
    for (const tail of permutations(values.filter((_,j) => j!==i))) yield [values[i],...tail];
  }
}
const deck = [0,1,2,3,4,5], states = [], inverse = new Map();
let played = 0;
for (const order of permutations(deck)) for (let i=0;i<=6;i++) for (let j=i;j<=6;j++) {
  const state = [order.slice(0,i),order.slice(i,j),order.slice(j)];
  states.push(state);
  const after = referenceMove(state);
  if (!after) continue;
  played++;
  const key = JSON.stringify(after);
  if (!inverse.has(key)) inverse.set(key,[]);
  inverse.get(key).push(state);
  assert.deepEqual(core.transition(state,deck).after,after);
}
const histogram = {};
for (const state of states) {
  const expected = (inverse.get(JSON.stringify(state)) || []).map(JSON.stringify).sort();
  const actual = core.predecessors(state,deck).map(JSON.stringify).sort();
  assert.deepEqual(actual,expected);
  assert(actual.length<=4);
  histogram[actual.length]=(histogram[actual.length]||0)+1;
}
assert.equal(states.length,20160);assert.equal(played,18000);
assert.deepEqual(histogram,{'0':8160,'1':7200,'2':3660,'3':1080,'4':60});
console.log(JSON.stringify({witness:report,finiteControl:{states:states.length,played,histogram},status:'PASS'},null,2));
