#!/usr/bin/env node
// Replays the witnesses in live3_construct_receipt.json with the site's own engine,
// sedaps-core-v0-2.js, and confirms each returns to itself after exactly its period with three
// queues live on every turn (RESEARCH_UPDATE_v0_4_1.md section 2, construction).
// At n = 51, rank r stands for the r-th card of the shipped deck (0..51 without the marker 7);
// the rule compares cards only by order, so the map preserves the game.
// Run: node live3_construct_check.cjs
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm');
const f = path.join(__dirname, '..', 'sedaps-core-v0-2.js');
vm.runInThisContext(fs.readFileSync(f, 'utf8'), { filename: f });   // as the other verifiers load it
const core = globalThis.SedapsCore;
const receipt = require(path.join(__dirname, 'live3_construct_receipt.json'));
let ok = true;
for (const w of receipt.witnesses) {
  const deck = w.n === 51 ? core.ACTIVE : Array.from({length: w.n}, (_, i) => i);
  const start = w.state.map(q => q.map(r => deck[r]));
  let s = core.copy(start), t = 0, returned = 0, allLive = true;
  while (t < w.period) {
    const move = core.transition(s, deck);
    if (move.live.length !== 3) allLive = false;
    s = move.after; t++;
    if (core.same(s, start)) { returned = t; break; }
  }
  const pass = returned === w.period && allLive;
  ok = ok && pass;
  console.log(JSON.stringify({n: w.n, period: w.period, returnedAfter: returned, threeLiveEveryTurn: allLive, pass}));
}
process.exit(ok ? 0 : 1);
