/* 51 Twins v1 — "Run the tape". A playhead over the static plate; it computes nothing new.
   Backward from the present, each lane lights until its recorded stop; forward, the present
   enters its cycle and a marker circles the loop until stopped. CC BY 4.0. */
(() => {
  'use strict';
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const data = globalThis.TWINS51 && globalThis.TWINS51.sedaps85;
  for (const panel of document.querySelectorAll('.tw-run')) {
    const fig = document.getElementById(panel.dataset.for);
    const svgs = [...fig.querySelectorAll('svg.tw-svg')];
    const status = panel.querySelector('.tw-run-status');
    const runBtn = panel.querySelector('[data-run]'), stopBtn = panel.querySelector('[data-stop]');
    const guessBtns = [...panel.querySelectorAll('[data-guess]')];
    if (!data) { panel.hidden = true; continue; }
    const T0 = data.turn, lane = bits => data.lanes.find(l => l.bits === bits);
    let guess = null, timer = 0, raf = 0, token = 0;
    const say = text => { status.textContent = text; };
    const light = t => { for (const s of svgs) for (const el of s.querySelectorAll('.tw-step')) el.classList.toggle('on', Number(el.dataset.t) >= t); };
    const forward = on => { for (const s of svgs) for (const el of s.querySelectorAll('.tw-fwd')) el.classList.toggle('on', on); };
    const orbitGeometry = s => { const ring = s.querySelector('circle.tw-fwd'); return ring && { cx: +ring.getAttribute('cx'), cy: +ring.getAttribute('cy'), r: +ring.getAttribute('r'), dot: s.querySelector('.tw-orbit') }; };
    const placeOrbit = angle => { for (const s of svgs) { const g = orbitGeometry(s); if (!g || !g.dot) continue; g.dot.setAttribute('cx', (g.cx + g.r * Math.cos(Math.PI + angle)).toFixed(1)); g.dot.setAttribute('cy', (g.cy + g.r * Math.sin(Math.PI + angle)).toFixed(1)); } };
    function stopLoop(final) {
      cancelAnimationFrame(raf); clearTimeout(timer); raf = 0; token++;
      for (const s of svgs) s.classList.remove('is-running');
      light(0); forward(true); placeOrbit(0);
      stopBtn.hidden = true; runBtn.disabled = false; guessBtns.forEach(b => { b.disabled = false; });
      if (final) say(final);
    }
    function verdictLine() {
      if (!guess) return 'Only 00 reaches the deal.';
      const L = lane(guess);
      if (L.verdict === 'REACHABLE') return 'You picked ' + guess + ': it reaches the 17–17–17 deal.';
      return 'You picked ' + guess + ': it stops ' + (L.reason === 'mod3' || L.stopTurn == null ? 'at once (mod-3 clock)' : 'at turn ' + L.stopTurn) + '. Only 00 reaches the deal.';
    }
    function loop() {
      const period = data.forward.period, start = performance.now(), my = token;
      forward(true); stopBtn.hidden = false; runBtn.disabled = false;
      say(verdictLine() + ' Forward, the present enters a cycle at turn ' + data.forward.enters + ' and repeats every ' + period.toLocaleString('en-US') + ' turns. It never ends.');
      const frame = now => { if (my !== token) return; placeOrbit(((now - start) / 2600) * 2 * Math.PI); raf = requestAnimationFrame(frame); };
      raf = requestAnimationFrame(frame);
    }
    guessBtns.forEach(b => { b.onclick = () => { guess = b.dataset.guess; guessBtns.forEach(x => x.setAttribute('aria-pressed', String(x === b))); say('You picked ' + guess + '. Run the tape.'); }; });
    stopBtn.onclick = () => stopLoop('Stopped. The loop itself does not stop: period ' + data.forward.period.toLocaleString('en-US') + ' = 52 × ' + data.forward.periodOver52 + '.');
    document.addEventListener('visibilitychange', () => { if (document.hidden && raf) stopLoop('Paused while the page was hidden.'); });
    runBtn.onclick = () => {
      stopLoop(); const my = ++token;
      if (motion.matches) { light(0); forward(true); say(verdictLine() + ' Forward: a cycle from turn ' + data.forward.enters + ' with period ' + data.forward.period.toLocaleString('en-US') + '.'); return; }
      runBtn.disabled = true; guessBtns.forEach(b => { b.disabled = true; });
      for (const s of svgs) s.classList.add('is-running');
      forward(false); light(T0 - 1);
      const notes = { [T0 - 1]: 'Turn 84: 01 and 11 fail the mod-3 clock at once.', 66: 'Turn 66: 10 has no earlier past. Every one of its histories has died.', 0: 'Turn 0: 00 reaches the 17–17–17 deal.' };
      let t = T0 - 1;
      const step = () => {
        if (my !== token) return;
        light(t);
        if (notes[t]) say(notes[t]); else if (t % 5 === 0) say('Running backward · turn ' + t);
        if (t === 0) { timer = setTimeout(() => { if (my === token) loop(); }, 900); return; }
        t--; timer = setTimeout(step, notes[t + 1] ? 700 : 45);
      };
      timer = setTimeout(step, 300);
    };
  }
})();
