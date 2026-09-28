/* SEDAPS: inspect legal histories and an exact, disclosed reachable history. */
'use strict';
(() => {
  const $ = id => document.getElementById(id), core = globalThis.SedapsCore;
  const research = globalThis.SedapsResearch, certificate = globalThis.SedapsCertificate;
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  let report, scene = 'reached', mode = 'backward', hiddenBranch = null;
  let shown = 0, forwardBranch = '00', useStart = false, busy = false;
  const ranks = ['A','2','3','4','5','6','7','8','9','10','J','Q','K'];
  const glyphs = ['♠','♥','♦','♣'], suits = ['spades','hearts','diamonds','clubs'];
  const endpoint = () => scene === 'reached' ? report.endpoint : core.ENDPOINT;
  const branches = () => scene === 'reached' ? Object.fromEntries(core.BITS.map((b,i)=>[b,report.candidates[i]])) : core.BRANCHES;
  function fail(error) {
    $('demo').hidden=true; $('boot-status').hidden=true; $('implementation-failure').hidden=false;
    $('failure-detail').textContent='The rule or certificate check failed. '+error.message;
    $('footer-status').textContent='Exact checks: FAIL.';
  }
  function guard(action, paced=false) {
    return async () => {
      if (busy) return;
      try {
        if (paced && !motion.matches) {
          busy=true; $('case-select').disabled=true; $('demo').setAttribute('aria-busy','true'); $('demo').classList.add('thinking');
          await new Promise(resolve=>setTimeout(resolve,600));
        }
        action();
      } catch(error) { fail(error); }
      finally {busy=false; $('case-select').disabled=false; $('demo').removeAttribute('aria-busy'); $('demo').classList.remove('thinking');}
    };
  }
  function card(q) {
    return '<span class="card-token'+([1,2].includes(q%4)?' red':'')+'" data-q="'+q+'" aria-label="'+ranks[Math.floor(q/4)]+' of '+suits[q%4]+'"><span>'+ranks[Math.floor(q/4)]+'</span><span aria-hidden="true">'+glyphs[q%4]+'</span></span>';
  }
  function tokens(queue) {
    if(!queue.length) return '<span class="empty">Empty</span>';
    if(queue.length>9 && !core.U.every((q,j)=>queue.includes(q) && queue.indexOf(q)===queue.indexOf(core.U[0])+j)) {
      return '<details class="queue-overflow"><summary><span class="tokens">'+queue.slice(0,2).map(card).join('')+'<span class="shared-run" title="Expand complete queue">+'+(queue.length-4)+'</span>'+queue.slice(-2).map(card).join('')+'</span></summary><span class="tokens expanded-queue">'+queue.map(card).join('')+'</span></details>';
    }
    let html='';
    for(let i=0;i<queue.length;i++) {
      if(core.U.every((q,j)=>queue[i+j]===q)) {html+='<span class="shared-run" aria-label="U, fixed ordered block of 45 cards">U · 45</span>';i+=core.U.length-1;}
      else html+=card(queue[i]);
    }
    return html;
  }
  function renderQueues(target,state) {
    target.innerHTML=state.map((q,p)=>'<div class="queue" data-player="'+p+'"><span class="queue-name">H'+p+'<span class="queue-count">'+q.length+' cards</span></span><span class="tokens">'+tokens(q)+'</span></div>').join('');
    target.dataset.state=JSON.stringify(state);
  }
  function status(title,detail) {$('status-title').textContent=title;$('status-sub').textContent=detail;}
  function clearTurn() {
    $('turn-display').hidden=true;
    $('center-state').classList.remove('confirmed');$('forward-after-panel').classList.remove('confirmed');
    $('center-note').textContent=endpoint().map(q=>q.length).join(' + ')+' cards';
    delete $('turn-display').dataset.branch;delete $('turn-display').dataset.verified;
  }
  function filterBranches() {
    const prefix=hiddenBranch===null?'':hiddenBranch.slice(0,shown);
    let count=0;
    for(const panel of document.querySelectorAll('.branch')) {
      const ruledOut=scene==='reached' && useStart && !report.admissibleBits.includes(panel.dataset.slot);
      const possible=!ruledOut && panel.dataset.slot.startsWith(prefix), recovered=possible && shown===2;
      if(possible) count++;
      panel.classList.toggle('excluded',!possible);panel.classList.toggle('recovered',recovered);
      panel.dataset.possible=String(possible);
      const label=recovered?'Recovered':ruledOut?'Needs ≥33 initial cards':possible?(useStart?'Not ruled out':'Legal past'):'Bit excludes';
      panel.querySelector('.branch-state').textContent=label;
      panel.setAttribute('aria-label','Candidate past '+panel.dataset.slot+': '+label);
    }
    $('bit-readout').textContent=prefix+'·'.repeat(2-shown);
    $('bit-readout').setAttribute('aria-label',shown?shown+' history bits revealed: '+prefix:'No history bits revealed');
    for(const step of $('recovery-steps').children) {
      if(Number(step.dataset.stage)===shown) step.setAttribute('aria-current','step');else step.removeAttribute('aria-current');
    }
    $('recovery-steps').children[0].textContent=useStart?'3 not ruled out':'4 legal pasts';
    return count;
  }
  function resetBackward() {
    hiddenBranch=null;shown=0;clearTurn();filterBranches();
    $('reveal-1').disabled=true;$('reveal-2').disabled=true;$('replay').disabled=true;
    status('What happened one move ago?',scene==='reached'?'This present was reached after 85 turns from 17–17–17. Hide its recorded past, then recover it.':'Four legal pasts share this constructed present. This example cannot come from 17–17–17.');
  }
  function renderForward() {
    clearTurn();
    for(const b of document.querySelectorAll('[data-forward]')) {b.classList.toggle('active',b.dataset.forward===forwardBranch);b.setAttribute('aria-pressed',String(b.dataset.forward===forwardBranch));}
    $('forward-before-title').textContent='Complete state '+forwardBranch;
    renderQueues($('forward-before'),branches()[forwardBranch]);
    $('forward-after-title').textContent='Ready to play';$('forward-after').innerHTML='<p class="waiting">Play one turn to reveal the resulting queues.</p>';delete $('forward-after').dataset.state;
    $('play-turn').disabled=false;$('bit-readout').textContent='→';$('bit-readout').setAttribute('aria-label','Forward transition');
    status('One complete state. One next state.',scene==='reached'&&forwardBranch==='11'?'State 11 is a legal state, but cannot arise from a 17–17–17 deal.':'Choose any legal predecessor and replay its exact next turn.');
  }
  function showTurn(bits) {
    const move=core.transition(branches()[bits]);
    if(!core.same(move.after,endpoint())) throw Error('Forward replay missed the endpoint.');
    $('turn-title').textContent='Branch '+bits+' · H'+move.winner+' wins';
    $('turn-draws').innerHTML=move.draws.map(d=>'<div class="drawn-card'+(d.player===move.winner?' winner':'')+'"><span>H'+d.player+(d.player===move.winner?' · winner':'')+'</span>'+card(d.card)+'</div>').join('');
    $('capture-label').textContent='H'+move.winner+' appends, in order:';$('turn-capture').innerHTML=move.capture.map(card).join('');
    $('turn-display').dataset.branch=bits;$('turn-display').dataset.verified='true';$('turn-display').hidden=false;
    return move;
  }
  function switchMode(next) {
    mode=next;
    for(const d of ['backward','forward']) {$(d+'-mode').classList.toggle('active',d===next);$(d+'-mode').setAttribute('aria-pressed',String(d===next));}
    $('backward-board').hidden=next!=='backward';$('backward-controls').hidden=next!=='backward';$('recovery-steps').hidden=next!=='backward';$('forward-board').hidden=next!=='forward';document.querySelector('.start-context').hidden=next!=='backward';
    if(next==='backward') resetBackward();else renderForward();
  }
  function renderScene() {
    useStart=false;forwardBranch='00';
    $('apply-start').setAttribute('aria-pressed','false');$('apply-start').hidden=scene!=='reached';
    $('start-note').textContent=scene==='reached'?'The start filter is necessary, not sufficient. Only the recorded past is certified reachable.':'The original example needs an initial queue of at least 44 cards. Its four legal pasts still verify.';
    $('case-note').textContent=scene==='reached'?'Reached from an equal deal · turn 85 · expand a queue to inspect its full order.':'Constructed witness · legal states · unreachable from an equal deal.';
    $('deal-past').textContent=scene==='reached'?'Hide recorded past':'Deal hidden past';
    $('integrity-tag').textContent=scene==='reached'?'85-TURN REPLAY · PASS':'LEGAL WITNESS · PASS';
    document.querySelector('.common-run').hidden=scene!=='constructed';
    renderQueues($('endpoint-queues'),endpoint());
    for(const bits of core.BITS) renderQueues(document.querySelector('[data-slot="'+bits+'"] .queue-row'),branches()[bits]);
    $('exact-states').textContent=['q = 4(rank − 1) + suit; suits S,H,D,C = 0,1,2,3. Address 7 (2C) is outside.','Endpoint: '+JSON.stringify(endpoint()),...core.BITS.map(b=>b+': '+JSON.stringify(branches()[b]))].join('\n\n');
    switchMode(mode);
  }
  function inspectTurn() {
    const turn=Number($('trajectory-step').value);
    $('trajectory-label').textContent='After '+turn+' / 85 turns';renderQueues($('trajectory-state'),certificate.states[turn]);
  }
  try {
    if(!core||!research||!certificate) throw Error('Research engine did not load.');
    const witness=core.verifyWitness();report=research.verifyCertificate(certificate);
    $('audit').textContent=JSON.stringify({witness,certificate:{pass:report.pass,turns:report.turns,endpointCounts:report.endpointCounts,prefixFloors:report.prefixFloors,admissibleBits:report.admissibleBits,actualBits:report.actualBits,remainingAlternativeReachability:'OPEN'}},null,2);
    $('common-cards').innerHTML=core.U.map(card).join('');
    $('case-select').onchange=guard(()=>{scene=$('case-select').value;renderScene();});
    $('deal-past').onclick=guard(()=>{
      if(mode!=='backward')return;
      hiddenBranch=scene==='reached'?report.actualBits:core.BITS[Math.floor(Math.random()*4)];shown=0;clearTurn();const n=filterBranches();
      $('reveal-1').disabled=false;$('reveal-2').disabled=true;$('replay').disabled=true;
      status(scene==='reached'?'Recorded past hidden.':'Hidden past dealt.',n+' candidates remain. Reveal the first bit.');
    },true);
    $('apply-start').onclick=guard(()=>{
      useStart=!useStart;$('apply-start').setAttribute('aria-pressed',String(useStart));
      const n=filterBranches();
      status(useStart?'The starting condition excludes 11.':'All legal predecessors shown.',useStart?n+' candidate'+(n===1?'':'s')+' remain. Branch 11 needs at least 33 initial cards in H0; our deal starts with 17.':'All four pass the forward rule. Reachability is a separate question.');
    },true);
    $('reveal-1').onclick=guard(()=>{
      if(hiddenBranch===null||shown!==0||mode!=='backward')return;shown=1;const n=filterBranches();
      $('reveal-1').disabled=true;$('reveal-2').disabled=false;
      status('First bit: '+hiddenBranch[0]+'.',(hiddenBranch[0]==='0'?'H1':'H0')+' won. '+n+' candidates remain.');$('reveal-2').focus({preventScroll:true});
    },true);
    $('reveal-2').onclick=guard(()=>{
      if(hiddenBranch===null||shown!==1||mode!=='backward')return;shown=2;filterBranches();
      $('reveal-2').disabled=true;$('replay').disabled=false;
      status('Past '+hiddenBranch+' recovered.',hiddenBranch[1]==='1'?'H2 participated. Replay the turn to check.':'H2 was empty. Replay the turn to check.');$('replay').focus({preventScroll:true});
    },true);
    $('replay').onclick=guard(()=>{if(hiddenBranch===null||shown!==2||mode!=='backward')return;showTurn(hiddenBranch);$('center-state').classList.add('confirmed');$('center-note').textContent='Exact endpoint verified ✓';status('Replay verified.','Branch '+hiddenBranch+' reaches the present in one played turn.');},true);
    $('reset').onclick=guard(resetBackward);
    $('backward-mode').onclick=guard(()=>switchMode('backward'));$('forward-mode').onclick=guard(()=>switchMode('forward'));
    for(const b of document.querySelectorAll('[data-forward]')) b.onclick=guard(()=>{forwardBranch=b.dataset.forward;renderForward();});
    $('play-turn').onclick=guard(()=>{if(mode!=='forward'||$('play-turn').disabled)return;const move=showTurn(forwardBranch);renderQueues($('forward-after'),move.after);$('forward-after-title').textContent='One shared endpoint';$('forward-after-panel').classList.add('confirmed');$('play-turn').disabled=true;status('One turn played.','H'+move.winner+' wins and appends the exposed cards in the fixed order.');},true);
    $('forward-reset').onclick=guard(renderForward);$('trajectory-step').oninput=guard(inspectTurn);
    inspectTurn();renderScene();$('footer-status').textContent='Legal witness + 85-turn certificate: PASS · v0.3';$('boot-status').hidden=true;$('demo').hidden=false;
  } catch(error) {fail(error);}
})();
