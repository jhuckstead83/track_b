'use strict';
(()=>{
  const suits=['S','H','D','C'], suitGlyph={S:'♠',H:'♥',D:'♦',C:'♣'}, ranks=['A','2','3','4','5','6','7','8','9','10','J','Q','K'];
  const face=q=>ranks[Math.floor(q/4)]+suitGlyph[suits[q%4]];
  const U=[6,...Array.from({length:44},(_,i)=>i+8)];
  const endpoint=[U.concat([5,3,1]),[4,2,0],[]];
  const branches={
    '00':[[0].concat(U,[5,3,1]),[2,4],[]],
    '01':[[0].concat(U,[5,3,1]),[4],[2]],
    '10':[[3].concat(U,[5]),[1,4,2,0],[]],
    '11':[[5].concat(U),[3,4,2,0],[1]]
  };
  const clone=s=>s.map(h=>h.slice());
  const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
  function step(state){
    const h=clone(state), live=h.map((q,i)=>q.length?i:null).filter(i=>i!==null);
    if(live.length<2)return h;
    const draws={}; for(const i of live)draws[i]=h[i].shift();
    const winner=live.reduce((a,b)=>draws[a]>draws[b]?a:b);
    const pot=[draws[winner]];
    for(let d=1;d<3;d++){const i=(winner+d)%3;if(Object.prototype.hasOwnProperty.call(draws,i))pot.push(draws[i]);}
    h[winner].push(...pot); return h;
  }
  function queueSummary(q){
    if(!q.length)return '—';
    const faces=q.map(face); if(faces.length<=7)return faces.join(' ');
    return faces.slice(0,3).join(' ')+' … '+faces.slice(-3).join(' ');
  }
  function renderBranches(){
    for(const [bits,state] of Object.entries(branches)){
      const root=document.querySelector('[data-slot="'+bits+'"] .queue-row');
      root.innerHTML=state.map((q,i)=>'<div class="queue"><b>H'+i+'</b><span class="count">'+q.length+'</span><span class="cards-mini">'+queueSummary(q)+'</span></div>').join('');
    }
  }
  const checks=Object.entries(branches).map(([bits,s])=>({bits,ok:s.flat().length===51&&same(step(s),endpoint)}));
  const allPass=checks.every(x=>x.ok)&&endpoint.flat().length===51&&!endpoint.flat().includes(7);
  document.getElementById('integrity-tag').textContent=allPass?'EXACT WITNESS · PASS':'IMPLEMENTATION FAILURE';
  document.getElementById('integrity-tag').className='tag '+(allPass?'pass':'fail');
  document.getElementById('footer-status').textContent=allPass?'Exact witness check: PASS.':'Exact witness check: FAIL.';
  document.getElementById('audit').textContent=JSON.stringify({marker:'2C / address 7 held outside',endpointCounts:endpoint.map(x=>x.length),checks},null,2);
  renderBranches();

  let hidden=null,shown=0,mode='backward';
  const cards=()=>[...document.querySelectorAll('.branch')];
  function setStatus(title,sub){document.getElementById('status-title').textContent=title;document.getElementById('status-sub').textContent=sub;}
  function applyFilter(){
    const known=hidden?hidden.slice(0,shown):'';
    for(const el of cards()){
      const bits=el.dataset.slot,keep=!hidden||bits.startsWith(known);el.classList.toggle('out',!keep);el.classList.toggle('actual',hidden&&shown===2&&bits===hidden);
    }
    document.getElementById('bit-readout').textContent=hidden?(hidden.slice(0,shown)+'·'.repeat(2-shown)):'··';
  }
  function reset(){hidden=null;shown=0;applyFilter();document.getElementById('reveal-1').disabled=true;document.getElementById('reveal-2').disabled=true;document.getElementById('replay').disabled=true;setStatus(mode==='backward'?'What happened one move ago?':'One complete state has one next state.',mode==='backward'?'Four legal answers share this endpoint. Deal a hidden past, then recover it.':'Select backward read to inspect the four-way predecessor fiber.');}
  document.getElementById('deal-past').onclick=()=>{if(!allPass)return;const keys=Object.keys(branches);hidden=keys[Math.floor(Math.random()*keys.length)];shown=0;applyFilter();document.getElementById('reveal-1').disabled=false;document.getElementById('reveal-2').disabled=true;document.getElementById('replay').disabled=true;setStatus('Hidden past dealt.','Four branches remain possible. Reveal only enough ledger to recover it.');};
  document.getElementById('reveal-1').onclick=()=>{if(!hidden)return;shown=1;applyFilter();document.getElementById('reveal-1').disabled=true;document.getElementById('reveal-2').disabled=false;setStatus('One bit received.','Two legal predecessor branches remain.');};
  document.getElementById('reveal-2').onclick=()=>{if(!hidden)return;shown=2;applyFilter();document.getElementById('reveal-2').disabled=true;document.getElementById('replay').disabled=false;setStatus('Past recovered.','The two-bit branch address selects one predecessor from the four-way fiber.');};
  document.getElementById('replay').onclick=()=>{if(!hidden||shown<2)return;const ok=same(step(branches[hidden]),endpoint);setStatus(ok?'Replay verified.':'Replay failed.',ok?'That predecessor reaches the displayed present in exactly one published-rule move.':'Implementation mismatch: stop and audit the transition.');};
  document.getElementById('reset').onclick=reset;
  function modeSwitch(next){mode=next;document.getElementById('forward-mode').classList.toggle('active',next==='forward');document.getElementById('backward-mode').classList.toggle('active',next==='backward');document.getElementById('deal-past').disabled=next==='forward';document.getElementById('reveal-1').disabled=true;document.getElementById('reveal-2').disabled=true;document.getElementById('replay').disabled=true;hidden=null;shown=0;applyFilter();setStatus(next==='forward'?'Complete state → one next state.':'One endpoint ← up to four legal pasts.',next==='forward'?'The published played-turn rule is deterministic on a complete state.':'Deal a hidden past to explore the predecessor fiber.');}
  document.getElementById('forward-mode').onclick=()=>modeSwitch('forward');
  document.getElementById('backward-mode').onclick=()=>modeSwitch('backward');
  reset();
})();
