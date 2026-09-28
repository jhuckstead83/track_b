/* UI for the exact witness. No wallet, probabilities for physical play,
   zero data, or four-player rules are introduced here. */
'use strict';
(() => {
  const $ = id => document.getElementById(id);
  const core = globalThis.SedapsCore;
  let mode = 'backward', hiddenBranch = null, shown = 0, forwardBranch = '00';
  const ranks = ['A','2','3','4','5','6','7','8','9','10','J','Q','K'];
  const glyphs = ['♠','♥','♦','♣'];
  const suitNames = ['spades','hearts','diamonds','clubs'];
  const face = q => ranks[Math.floor(q/4)] + glyphs[q%4];

  function fail(error) {
    $('demo').hidden = true;
    $('boot-status').hidden = true;
    $('implementation-failure').hidden = false;
    $('failure-detail').textContent = 'The rule or witness check failed. ' + error.message;
    $('footer-status').textContent = 'Exact witness check: FAIL.';
  }
  function guarded(action) {
    return () => {try {action();} catch (error) {fail(error);}};
  }
  function card(q) {
    const color = q%4 === 1 || q%4 === 2 ? ' red' : '';
    return '<span class="card-token'+color+'" data-q="'+q+'" aria-label="'+ranks[Math.floor(q/4)]+' of '+suitNames[q%4]+'"><span>'+ranks[Math.floor(q/4)]+'</span><span aria-hidden="true">'+glyphs[q%4]+'</span></span>';
  }
  function tokens(queue) {
    if (!queue.length) return '<span class="empty">Empty</span>';
    let html = '';
    for (let i=0;i<queue.length;i++) {
      if (core.U.every((q,j) => queue[i+j] === q)) {
        html += '<span class="shared-run" aria-label="U, the fixed ordered block of 45 cards">U · 45</span>';
        i += core.U.length-1;
      } else html += card(queue[i]);
    }
    return html;
  }
  function renderQueues(target, state) {
    target.innerHTML = state.map((queue,player) =>
      '<div class="queue" data-player="'+player+'"><span class="queue-name">H'+player+
      '<span class="queue-count">'+queue.length+' cards</span></span><span class="tokens">'+tokens(queue)+'</span></div>'
    ).join('');
    target.dataset.state = JSON.stringify(state);
  }
  function status(title, detail) {
    $('status-title').textContent = title;
    $('status-sub').textContent = detail;
  }
  function clearTurn() {
    $('turn-display').hidden = true;
    $('center-state').classList.remove('confirmed');
    $('forward-after-panel').classList.remove('confirmed');
    $('center-note').textContent = '48 + 3 + 0 cards';
    delete $('turn-display').dataset.branch;
    delete $('turn-display').dataset.verified;
  }
  function filterBranches() {
    const prefix = hiddenBranch === null ? '' : hiddenBranch.slice(0,shown);
    for (const panel of document.querySelectorAll('.branch')) {
      const possible = panel.dataset.slot.startsWith(prefix);
      const recovered = possible && shown === 2;
      panel.classList.toggle('excluded',!possible);
      panel.classList.toggle('recovered',recovered);
      panel.dataset.possible = String(possible);
      panel.querySelector('.branch-state').textContent = recovered ? 'Recovered' : possible ? 'Possible' : 'Excluded';
      panel.setAttribute('aria-label','Candidate past '+panel.dataset.slot+': '+(recovered ? 'recovered' : possible ? 'possible' : 'excluded'));
    }
    $('bit-readout').textContent = prefix + '·'.repeat(2-shown);
    $('bit-readout').setAttribute('aria-label',shown ? shown+' history bits revealed: '+prefix : 'No history bits revealed');
    for (const step of $('recovery-steps').children) {
      if (Number(step.dataset.stage) === shown) step.setAttribute('aria-current','step');
      else step.removeAttribute('aria-current');
    }
  }
  function resetBackward() {
    hiddenBranch = null;shown = 0;clearTurn();filterBranches();
    $('reveal-1').disabled = true;
    $('reveal-2').disabled = true;
    $('replay').disabled = true;
    status('What happened one move ago?','All four pasts reach this present. Deal one, then recover it.');
  }
  function renderForward() {
    clearTurn();
    for (const button of document.querySelectorAll('[data-forward]')) {
      const selected = button.dataset.forward === forwardBranch;
      button.classList.toggle('active',selected);
      button.setAttribute('aria-pressed',String(selected));
    }
    $('forward-before-title').textContent = 'Complete state '+forwardBranch;
    renderQueues($('forward-before'),core.BRANCHES[forwardBranch]);
    $('forward-after-title').textContent = 'Ready to play';
    $('forward-after').innerHTML = '<p class="waiting">Play one turn to reveal the resulting queues.</p>';
    delete $('forward-after').dataset.state;
    $('play-turn').disabled = false;
    $('bit-readout').textContent = '→';
    $('bit-readout').setAttribute('aria-label','Forward transition');
    status('One complete state. One next state.','Choose a starting state, then play its turn.');
  }
  function showTurn(bits) {
    const move = core.transition(core.BRANCHES[bits]);
    if (!core.same(move.after,core.ENDPOINT)) throw Error('Forward replay missed the endpoint.');
    $('turn-title').textContent = 'Branch '+bits+' · H'+move.winner+' wins';
    $('turn-draws').innerHTML = move.draws.map(draw =>
      '<div class="drawn-card'+(draw.player===move.winner?' winner':'')+'"><span>H'+draw.player+
      (draw.player===move.winner?' · winner':'')+'</span>'+card(draw.card)+'</div>').join('');
    $('capture-label').textContent = 'H'+move.winner+' appends, in order:';
    $('turn-capture').innerHTML = move.capture.map(card).join('');
    $('turn-display').dataset.branch = bits;
    $('turn-display').dataset.verified = 'true';
    $('turn-display').hidden = false;
    return move;
  }
  function switchMode(next) {
    mode = next;
    for (const direction of ['backward','forward']) {
      const active = direction === next;
      $(direction+'-mode').classList.toggle('active',active);
      $(direction+'-mode').setAttribute('aria-pressed',String(active));
    }
    $('backward-board').hidden = next !== 'backward';
    $('backward-controls').hidden = next !== 'backward';
    $('recovery-steps').hidden = next !== 'backward';
    $('forward-board').hidden = next !== 'forward';
    if (next === 'backward') resetBackward(); else renderForward();
  }

  try {
    if (!core || typeof core.verifyWitness !== 'function') throw Error('Rule engine did not load.');
    const report = core.verifyWitness();
    if (!report.pass) throw Error('Witness check did not pass.');
    renderQueues($('endpoint-queues'),core.ENDPOINT);
    for (const bits of core.BITS) renderQueues(document.querySelector('[data-slot="'+bits+'"] .queue-row'),core.BRANCHES[bits]);
    $('common-cards').innerHTML = core.U.map(card).join('');
    $('audit').textContent = JSON.stringify(report,null,2);
    $('exact-states').textContent = ['q = 4(rank − 1) + suit; suits S,H,D,C = 0,1,2,3. Address 7 (2C) is outside.',
      'Endpoint: '+JSON.stringify(core.ENDPOINT),...core.BITS.map(bits => bits+': '+JSON.stringify(core.BRANCHES[bits]))].join('\n\n');

    $('deal-past').onclick = guarded(() => {
      if (mode !== 'backward') return;
      hiddenBranch = core.BITS[Math.floor(Math.random()*core.BITS.length)];
      shown = 0;clearTurn();filterBranches();
      $('reveal-1').disabled = false;$('reveal-2').disabled = true;$('replay').disabled = true;
      status('Hidden past dealt.','4 possible pasts. Reveal the first bit.');
    });
    $('reveal-1').onclick = guarded(() => {
      if (hiddenBranch === null || shown !== 0 || mode !== 'backward') return;
      shown = 1;filterBranches();
      $('reveal-1').disabled = true;$('reveal-2').disabled = false;
      status('First bit: '+hiddenBranch[0]+'.',(hiddenBranch[0]==='0'?'H1':'H0')+' won. 2 possible pasts remain.');
      $('reveal-2').focus({preventScroll:true});
    });
    $('reveal-2').onclick = guarded(() => {
      if (hiddenBranch === null || shown !== 1 || mode !== 'backward') return;
      shown = 2;filterBranches();
      $('reveal-2').disabled = true;$('replay').disabled = false;
      status('Past '+hiddenBranch+' recovered.',hiddenBranch[1]==='1'?'H2 participated. Replay the turn to check.':'H2 was empty. Replay the turn to check.');
      $('replay').focus({preventScroll:true});
    });
    $('replay').onclick = guarded(() => {
      if (hiddenBranch === null || shown !== 2 || mode !== 'backward') return;
      showTurn(hiddenBranch);
      $('center-state').classList.add('confirmed');
      $('center-note').textContent = 'Exact endpoint verified ✓';
      status('Replay verified.','Branch '+hiddenBranch+' reaches the present in one played turn.');
    });
    $('reset').onclick = guarded(resetBackward);
    $('backward-mode').onclick = guarded(() => switchMode('backward'));
    $('forward-mode').onclick = guarded(() => switchMode('forward'));
    for (const button of document.querySelectorAll('[data-forward]')) button.onclick = guarded(() => {
      forwardBranch = button.dataset.forward;renderForward();
    });
    $('play-turn').onclick = guarded(() => {
      if (mode !== 'forward' || $('play-turn').disabled) return;
      const move = showTurn(forwardBranch);
      renderQueues($('forward-after'),move.after);
      $('forward-after-title').textContent = 'One shared endpoint';
      $('forward-after-panel').classList.add('confirmed');
      $('play-turn').disabled = true;
      status('One turn played.','H'+move.winner+' wins and appends the exposed cards in the fixed order.');
    });
    $('forward-reset').onclick = guarded(renderForward);
    resetBackward();
    $('footer-status').textContent = 'Exact witness: PASS · 4 / 4 replays · v0.2';
    $('boot-status').hidden = true;
    $('demo').hidden = false;
  } catch (error) { fail(error); }
})();
