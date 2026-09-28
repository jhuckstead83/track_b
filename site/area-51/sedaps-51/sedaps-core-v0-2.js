/* 51 SEDAPS — the published three-queue played-turn rule.
   Copyright Jeffery Lyn Huckstead / Cerebral Graphix. CC BY 4.0.
   Terminal self-loops are deliberately excluded from this partial transition.
   The four-seat Spades adapter is a separate, unimplemented rule. */
(function (root) {
  'use strict';
  const freeze = value => {
    if (value && typeof value === 'object') {
      Object.values(value).forEach(freeze);
      Object.freeze(value);
    }
    return value;
  };
  const ACTIVE = freeze(Array.from({length:52}, (_,q) => q).filter(q => q !== 7));
  const U = freeze(ACTIVE.filter(q => q > 5));
  const BITS = freeze(['00','01','10','11']);
  const ENDPOINT = freeze([U.concat([5,3,1]),[4,2,0],[]]);
  const BRANCHES = freeze({
    '00':[[0].concat(U,[5,3,1]),[2,4],[]],
    '01':[[0].concat(U,[5,3,1]),[4],[2]],
    '10':[[3].concat(U,[5]),[1,4,2,0],[]],
    '11':[[5].concat(U),[3,4,2,0],[1]]
  });
  const copy = state => state.map(queue => queue.slice());
  const key = state => JSON.stringify(state);
  const same = (a,b) => key(a) === key(b);
  function assertState(state, deck = ACTIVE) {
    if (!Array.isArray(state) || state.length !== 3 || !state.every(Array.isArray)) throw Error('Expected three ordered queues.');
    const flat = state.flat();
    if (!deck.length || new Set(deck).size !== deck.length || !deck.every(Number.isInteger)) throw Error('Invalid reference alphabet.');
    if (flat.length !== deck.length || new Set(flat).size !== deck.length || flat.some(q => !deck.includes(q))) throw Error('Queues must partition the declared card alphabet exactly.');
    return true;
  }
  function transition(state, deck = ACTIVE) {
    assertState(state, deck);
    const after = copy(state);
    const live = [0,1,2].filter(i => after[i].length > 0);
    if (live.length < 2) throw Error('A terminal state has no played turn.');
    const draws = live.map(player => ({player, card:after[player].shift()}));
    const winner = draws.reduce((a,b) => a.card > b.card ? a : b).player;
    const capture = [0,1,2].map(offset => (winner + offset) % 3)
      .filter(player => live.includes(player))
      .map(player => draws.find(draw => draw.player === player).card);
    after[winner].push(...capture);
    assertState(after, deck);
    return {before:copy(state), after, live, draws, winner, capture};
  }
  function compareStates(a,b) {
    for (let player=0; player<3; player++) {
      for (let i=0; i<Math.min(a[player].length,b[player].length); i++) {
        if (a[player][i] !== b[player][i]) return a[player][i] - b[player][i];
      }
      if (a[player].length !== b[player].length) return a[player].length - b[player].length;
    }
    return 0;
  }
  function predecessors(state, deck = ACTIVE) {
    assertState(state, deck);
    const currentLive = [0,1,2].filter(i => state[i].length > 0);
    const found = new Map();
    // For a fixed previous live set A and winner w, the endpoint's final
    // |A| cards in H_w uniquely specify the returned pot and hence the past.
    // Candidate counts for 1,2,3 current live queues are respectively 3,4,3.
    for (let mask=1; mask<8; mask++) {
      const live = [0,1,2].filter(i => mask & (1<<i));
      if (live.length < 2 || currentLive.some(i => !live.includes(i))) continue;
      for (const winner of currentLive) {
        if (state[winner].length < live.length) continue;
        const capture = state[winner].slice(-live.length);
        if (capture.slice(1).some(q => q >= capture[0])) continue;
        const previous = copy(state);
        previous[winner].splice(-live.length);
        const playerOrder = [0,1,2].map(offset => (winner + offset) % 3).filter(i => live.includes(i));
        playerOrder.forEach((player,i) => previous[player].unshift(capture[i]));
        if (same(transition(previous,deck).after,state)) found.set(key(previous),previous);
      }
    }
    return [...found.values()].sort(compareStates);
  }
  function verifyWitness() {
    assertState(ENDPOINT);
    const recovered = predecessors(ENDPOINT);
    if (recovered.length !== 4) throw Error('Expected exactly four legal predecessors.');
    const checks = BITS.map((bits,i) => {
      const state = BRANCHES[bits];
      assertState(state);
      const move = transition(state);
      if (!same(move.after,ENDPOINT) || !same(recovered[i],state)) throw Error('Witness or branch ordering mismatch: ' + bits);
      // In this particular witness, bit 1 selects winner H1/H0; bit 2 says
      // whether H2 participated. This interpretation is not a general codec.
      if (move.winner !== (bits[0] === '0' ? 1 : 0) || move.live.includes(2) !== (bits[1] === '1')) throw Error('Witness bit interpretation mismatch.');
      return {bits,valid:true,replays:true,winner:move.winner,live:move.live,capture:move.capture};
    });
    return {pass:true,activeCards:51,marker:7,endpointCounts:ENDPOINT.map(q => q.length),predecessorCount:recovered.length,checks};
  }
  const api = Object.freeze({ACTIVE,U,BITS,ENDPOINT,BRANCHES,copy,key,same,assertState,transition,predecessors,verifyWitness});
  root.SedapsCore = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
