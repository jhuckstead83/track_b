/* 51 SEDAPS v0.4 — start-class reachability for the three-queue rule.
   Copyright Jeffery Lyn Huckstead / Cerebral Graphix. CC BY 4.0.

   Time-aware shape lemma (PROVED; RESEARCH_UPDATE_v0_4.md §2). From a 17–17–17
   deal, after s played turns:
   - three queues live: every queue is a partial front of p cards followed by
     3-card packets, each led by its largest card, where p = 17 − s for s < 17
     and p ≡ 17 − s (mod 3), 0 ≤ p ≤ 2, for s ≥ 17. In particular every queue
     length is ≡ 17 − s (mod 3): the "mod-3 clock";
   - two queues live: s ≥ 17, and each live queue is at most 2 front cards,
     then 3-card packets, then 2-card packets, each packet led by its largest.
   A state with at least two live queues that fails the test at turn s is
   unreachable at turn s. Terminal states, in which one queue holds every card,
   always fail the test and are outside its scope; the backward search never
   evaluates them, because every legal predecessor has at least two live queues.
   Passing the test is necessary, not sufficient; reachability verdicts come
   from explicit deals. (Scope clause added in v0.4.1 after Blue Team PP275;
   code unchanged. Necessity proof: RESEARCH_UPDATE_v0_4_1.md §1.1.) */
(function (root) {
  'use strict';
  const headMax = (q, s, L) => { for (let k = s + 1; k < s + L; k++) if (q[k] > q[s]) return false; return true; };
  function shapeOK(y, s) {
    const live = [0, 1, 2].filter(i => y[i].length);
    if (live.length === 3) {
      for (const q of y) {
        const n = q.length, p = s < 17 ? 17 - s : ((17 - s) % 3 + 3) % 3;
        if (n < p || (n - p) % 3) return false;
        for (let k = p; k < n; k += 3) if (!headMax(q, k, 3)) return false;
      }
      return true;
    }
    if (live.length !== 2 || s < 17) return false;
    for (const i of live) {
      const q = y[i], n = q.length; let ok = false;
      for (let b = n; b >= 0 && !ok; b -= 2) {
        if (b < n && !headMax(q, b, 2)) break;
        for (let a = b; a >= 0; a -= 3) { if (a < b && !headMax(q, a, 3)) break; if (a <= 2) { ok = true; break; } }
      }
      if (!ok) return false;
    }
    return true;
  }
  /* The mod-3 clock alone: with all three queues live at turn s, each length ≡ 17 − s (mod 3). */
  function clockFails(y, s) {
    if (y.some(q => !q.length)) return null;
    const want = ((17 - s) % 3 + 3) % 3, bad = y.map(q => q.length).filter(n => n % 3 !== want);
    return bad.length ? { want, lengths: y.map(q => q.length) } : null;
  }
  /* Legal predecessors; the same enumeration as SedapsCore.predecessors, without the replay check. */
  function preds(y) {
    const B = [0, 1, 2].filter(i => y[i].length), out = [];
    for (let mask = 1; mask < 8; mask++) {
      const A = [0, 1, 2].filter(i => mask & (1 << i));
      if (A.length < 2 || B.some(i => !A.includes(i))) continue;
      for (const w of B) {
        const L = A.length, q = y[w];
        if (q.length < L) continue;
        const cap = q.slice(q.length - L);
        if (cap.slice(1).some(c => c > cap[0])) continue;
        const p = y.map(h => h.slice()); p[w].length -= L;
        const order = [0, 1, 2].map(o => (w + o) % 3).filter(i => A.includes(i));
        order.forEach((pl, k) => p[pl].unshift(cap[k]));
        out.push(p);
      }
    }
    return out;
  }
  const key = y => y.map(q => q.join(',')).join('|');
  /* Exhaustive backward exploration from state y at turn s, pruned by the shape lemma.
     Returns the lowest turn any backward history survives to, the number of distinct
     states expanded, whether a 17–17–17 deal is reached, and one deepest surviving path. */
  function explore(y, s, cap = 250000) {
    const seen = new Set(), st = { low: Infinity, nodes: 0, deal: null, capped: false, deepest: null };
    const path = [];
    (function go(z, t) {
      if (st.capped || !shapeOK(z, t)) return;
      path.push(z);
      if (t < st.low) { st.low = t; st.deepest = path.slice(); }
      if (t === 0) { if (z.every(q => q.length === 17) && !st.deal) st.deal = z; path.pop(); return; }
      const k = t + '#' + key(z);
      if (!seen.has(k)) {
        seen.add(k); if (++st.nodes > cap) { st.capped = true; path.pop(); return; }
        for (const p of preds(z)) go(p, t - 1);
      }
      path.pop();
    })(y, s);
    return { lowestTurn: st.low === Infinity ? null : st.low, statesExpanded: st.nodes, reachesDeal: !!st.deal,
      deal: st.deal, deepestPath: st.deepest, capped: st.capped };
  }
  /* Start-class verdicts for the four legal pasts of a certified endpoint.
     The recorded past is certified by the certificate's own replay; the others are searched. */
  function startVerdicts(core, certificate) {
    const T = certificate.turns, x = certificate.states[T], pre = core.predecessors(x);
    return pre.map((p, i) => {
      const bits = core.BITS[i];
      if (core.same(p, certificate.states[T - 1])) {
        return { bits, verdict: 'REACHABLE', reason: 'recorded', stopTurn: 0, statesExpanded: 0,
          note: 'Certified: the recorded 17–17–17 deal reaches it.' };
      }
      const clock = clockFails(p, T - 1);
      const e = explore(p, T - 1);
      if (e.capped) return { bits, verdict: 'OPEN', reason: 'budget', stopTurn: e.lowestTurn, statesExpanded: e.statesExpanded };
      if (e.reachesDeal) return { bits, verdict: 'REACHABLE', reason: 'search', stopTurn: 0, statesExpanded: e.statesExpanded, deal: e.deal };
      return { bits, verdict: 'EXCLUDED', reason: clock ? 'mod3' : 'search', stopTurn: e.lowestTurn, statesExpanded: e.statesExpanded,
        clock, note: clock ? 'Mod-3 clock: at turn ' + (T - 1) + ' every live length must be ≡ ' + clock.want + ' (mod 3).'
          : 'The deepest backward history reaches turn ' + e.lowestTurn + '; none gets further back.' };
    });
  }
  const api = Object.freeze({ shapeOK, clockFails, preds, key, explore, startVerdicts });
  root.SedapsLemma = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
