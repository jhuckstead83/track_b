/* Forge 51 / SEDAPS v0.3. A necessary queue-order invariant.
   Every queue from a 17-card start is a prefix of <=17 cards followed
   by legal returned packets. Removing its front preserves this language:
   a partially removed packet leaves at most 2 prefix cards. Appending
   a winning packet also preserves it. Acceptance is NOT sufficiency. */
(function (root) {
  'use strict';
  const core = root.SedapsCore;
  function prefixFloor(queue) {
    const cuts = new Set([queue.length]);
    for (let end=queue.length; end>=0; end--) {
      if (!cuts.has(end)) continue;
      for (const size of [2,3]) {
        if (end < size) continue;
        const packet = queue.slice(end-size,end);
        if (packet[0] === Math.max(...packet)) cuts.add(end-size);
      }
    }
    return {minimum:Math.min(...cuts),cuts:[...cuts].sort((a,b)=>a-b)};
  }
  function verifyCertificate(certificate) {
    if (!certificate || certificate.schema !== 'sedaps.reachable-certificate.v0.3') throw Error('Missing reachability certificate.');
    if (certificate.turns !== 85 || certificate.states.length !== 86 || certificate.predecessorIndices.length !== 85) throw Error('Certificate length changed.');
    const states = certificate.states;
    if (!states[0].every(q => q.length === 17)) throw Error('Certificate must start 17–17–17.');
    states.forEach(state => {
      core.assertState(state);
      if (state.some(q => prefixFloor(q).minimum > 17)) throw Error('Queue-order invariant failed.');
    });
    for (let i=0;i<certificate.turns;i++) {
      if (!core.same(core.transition(states[i]).after,states[i+1])) throw Error('Certificate replay failed at turn '+(i+1));
      const candidates = core.predecessors(states[i+1]);
      if (!core.same(candidates[certificate.predecessorIndices[i]],states[i])) throw Error('Branch ledger failed.');
    }
    const endpoint = states[85];
    const candidates = core.predecessors(endpoint);
    if (candidates.length !== 4) throw Error('Expected four legal predecessors.');
    const floors = candidates.map(s => s.map(q=>prefixFloor(q).minimum));
    if (JSON.stringify(floors) !== JSON.stringify(certificate.expectedPrefixFloors)) throw Error('Prefix-floor witness changed.');
    const admissibleBits = core.BITS.filter((bits,i) => floors[i].every(v=>v<=17));
    if (admissibleBits.join(',') !== '00,01,10') throw Error('Equal-start filter changed.');
    const actualIndex = candidates.findIndex(s => core.same(s,states[84]));
    if (actualIndex !== 0) throw Error('Recorded past changed.');
    if (prefixFloor(core.ENDPOINT[0]).minimum !== 44) throw Error('Constructed-witness obstruction changed.');
    return {pass:true,turns:85,endpointCounts:endpoint.map(q=>q.length),actualBits:core.BITS[actualIndex],
      candidates,endpoint,prefixFloors:floors,admissibleBits,
      constructedWitness:{minimumPrefix:44,reachableFromEqualDeal:false},
      remainingAlternativeReachability:'OPEN',fourPlayerAdapter:'OPEN'};
  }
  root.SedapsResearch = Object.freeze({prefixFloor,verifyCertificate});
  if (typeof module !== 'undefined' && module.exports) module.exports = root.SedapsResearch;
})(typeof globalThis !== 'undefined' ? globalThis : this);
