import {readGame,command,subscribeCredits} from './wallet-v2-3.js';
import {getCreditSnapshot} from '../assets/credits-v2-0b3.js';
import {ProspectReels} from './reels-v2-4.js';
await (async function(){'use strict';
 const E=globalThis.P51Engine,$=id=>document.getElementById(id);
 let state=E.fresh(),preview=null,busy=false,display='card',oddsEpoch=0,saveInvalid=true,record=null,committing=false,countingOdds=false;
 const faces=new Map();
 const motionQuery=matchMedia('(prefers-reduced-motion: reduce)');
 let motionPreference='system';try{const saved=localStorage.getItem('prospect51.motion');if(['system','reels','reduced'].includes(saved))motionPreference=saved;}catch{}
 function instantMotion(){return motionPreference==='reduced'||(motionPreference==='system'&&motionQuery.matches);}
 function renderMotion(){$('reel-motion').value=motionPreference;$('motion-readout').textContent=instantMotion()?'Reduced motion · immediate result':'Scrolling reels';}
 $('reel-motion').onchange=()=>{motionPreference=$('reel-motion').value;try{localStorage.setItem('prospect51.motion',motionPreference);}catch{}renderMotion();};
 motionQuery.addEventListener?.('change',renderMotion);renderMotion();
 
 const reels=new ProspectReels($('rotors'),E.CARDS);
 motionQuery.addEventListener?.('change',()=>{if(instantMotion())reels.skip();});
 const money=n=>(n/100).toFixed(2),fmt=n=>n.toLocaleString('en-US');
 function error(err){$('error').hidden=false;$('error').textContent=err.message||String(err);}
 function save(){ $('save-status').textContent='Shared jbit bank · hand saved'; }
 function hydrate(){if(state.round){$('wiring').value=state.round.settings.wire;$('knob').value=state.round.settings.knob;$('knob-out').textContent=String(state.round.settings.knob);}}
 async function move(kind,extra={}){
  if(committing||busy||saveInvalid||preview)return false;
  committing=true;$('error').hidden=true;CardUI.close(false);render();
  try{
   const res=await command({kind,...extra,expectedRevision:record.revision,operationId:crypto.randomUUID()});
   record=res.value;state=record.state;hydrate();save();cancelOdds();return true;
  }catch(err){
   error(err);
   try{const res=await readGame();record=res.value;state=record.state;hydrate();}catch(e){error(e);saveInvalid=true;}
   return false;
  }finally{committing=false;render();}
 }
 function publishOdds(text){$('odds-result').textContent=text;const local=$('card-hold-odds');if(local){local.textContent=text;CardUI.refresh();}}
 function cancelOdds(){oddsEpoch++;countingOdds=false;publishOdds(state.phase==='hold'?'Choose a hold and count its possible draws.':'Deal a hand to compare a decision.');}
 for(let i=0;i<5;i++){
  const div=document.createElement('div');div.className='rotor';div.id='rotor-'+i;
  div.innerHTML=`<p class="rotor-label">ROTOR ${String(i+1).padStart(2,'0')}</p><div class="drum"><div class="reel-window"><div class="reel-rest"><div class="reel-cell reel-above" aria-hidden="true" inert><p51-token size="reel" static></p51-token></div><div class="reel-cell reel-face"><p51-token size="reel" id="token-${i}" static></p51-token></div><div class="reel-cell reel-below" aria-hidden="true" inert><p51-token size="reel" static></p51-token></div></div><div class="reel-strip" aria-hidden="true" inert></div></div></div><p class="residue" id="residue-${i}">mod ${51-i}</p><button class="hold" id="hold-${i}" type="button" aria-pressed="false" disabled>HOLD</button>`;
  $('rotors').appendChild(div);$('hold-'+i).onclick=()=>act(()=>move('hold',{slot:i}));
 }
 reels.bind();
 for(const card of E.ARCHIVE_KEY){const t=document.createElement('p51-token');t.setAttribute('card',card);$('archive-key').appendChild(t);}
 for(let i=9;i>=1;i--){const tr=document.createElement('tr');tr.id='pay-'+i;tr.innerHTML=`<td>${E.CATEGORIES[i]}</td><td>${E.PAYS[i]}</td>`;$('paytable').appendChild(tr);}
 document.addEventListener('p51-inspect',e=>{faces.set(e.detail.card,e.detail.face);});
 function act(fn){if(busy||committing||saveInvalid)return;try{$('error').hidden=true;Promise.resolve(fn()).catch(error);}catch(err){error(err);render();}}
 function settings(){return {wire:$('wiring').value,knob:Number($('knob').value)};}
 function animate(beforeHand,slots){
  if(!slots.length){busy=false;render();return;}
  busy=true;
  reels.play({slots,before:beforeHand,after:state.round.hand.slice(),faceFor:card=>faces.get(card)||display,instant:instantMotion()||document.hidden,onStop(){render();},onDone(){busy=false;render();}});
  render();
 }
 function render(){
  const locked=busy||committing||saveInvalid;
  const r=state.round,hand=preview?preview.hand:r?r.hand:[],active=state.phase==='hold'&&!preview,settled=state.phase==='settled'&&!preview;
  const bank=getCreditSnapshot();$('bank').textContent=bank.ready?money(bank.balanceCents):'—';$('meter').textContent=money(state.meterCents);$('example-banner').hidden=!preview;
  for(let i=0;i<5;i++){
   const c=hand[i];reels.syncSlot(i,c,c?(faces.get(c)||display):display,locked);
   const h=!preview&&r?.holds[i];$('rotor-'+i).classList.toggle('held',!!h);$('hold-'+i).textContent=h?'HELD ✓':'HOLD';$('hold-'+i).setAttribute('aria-pressed',String(!!h));$('hold-'+i).setAttribute('aria-label',(h?'Release':'Hold')+' card '+(i+1));$('hold-'+i).disabled=!active||locked;
   const rows=!preview&&r?r.trace.filter(t=>t.slot===i):[],tr=rows[rows.length-1];$('residue-'+i).innerHTML=tr?`<span>mod ${tr.m}</span><span>${tr.d} &rarr; ${tr.e}</span>`:`<span>mod ${51-i}</span><span>&nbsp;</span>`;
  }
  $('deal').hidden=active||!!preview;$('deal').disabled=locked||state.balanceCents<100;
  $('draw').hidden=!active;$('draw').disabled=!active||locked;
  $('draw').textContent=active&&r.holds.every(Boolean)?'Keep five · collect':'Draw '+(active?r.holds.filter(h=>!h).length:5)+' · free';
  $('exit-example').hidden=!preview;$('reel-motion').disabled=locked;
  $('wiring').disabled=active||locked;$('knob').disabled=active||locked;$('odds').disabled=!active||locked||countingOdds;
  $('show-cards').setAttribute('aria-pressed',String(display==='card'));$('show-symbols').setAttribute('aria-pressed',String(display==='symbol'));
  for(let i=1;i<=9;i++)$('pay-'+i).classList.remove('active');
  const s=hand.length&&!busy?E.score(hand):null;if(s&&s.category)$('pay-'+s.category).classList.add('active');
  $('result').classList.toggle('win',!!(s&&s.category&&(settled||preview)));
  if(busy){$('result-title').textContent='The reels are turning…';$('result-note').textContent='Held cards stay put.';}
  else if(preview){$('result-title').textContent=preview.name;$('result-note').textContent=E.score(preview.hand).name+' \u00b7 illustration only; no jbits awarded.';}
  else if(active){$('result-title').textContent='Choose your hold';$('result-note').textContent=s.name+' now. '+(r.pendingBonusCents?'Archive lock matched; '+money(r.pendingBonusCents)+' bonus secured for settlement.':'Hold what stays. Draw the rest once.');}
  else if(settled){$('result-title').textContent=r.result.name+(r.result.totalCents?' \u00b7 +'+money(r.result.totalCents):'');$('result-note').textContent='Gross '+money(r.result.totalCents)+'; net '+(r.result.netCents>=0?'+':'')+money(r.result.netCents)+' jbits after the one-jbit entry.';}
  else{$('result-title').textContent='A new reading of the same cards.';$('result-note').textContent='Five cards. One free draw.';}
  $('spin-status').textContent=committing?'Saving move…':busy?'Reels turning':active?'Choose your hold · one free draw':settled?'Hand settled':'Ready to spin';
  $('skip-reels').hidden=!busy;
  for(const b of document.querySelectorAll('[data-example],#show-cards,#show-symbols,#export-record'))b.disabled=busy||committing;
  bindCardActions(hand,active,locked);
  $('trace').replaceChildren();if(!preview&&r)for(const row of r.trace){const tr=document.createElement('tr');for(const val of [row.slot+1,row.m,row.a,row.b,row.d,row.e,row.card]){const td=document.createElement('td');if(typeof val==='string'){const t=document.createElement('p51-token');t.setAttribute('card',val);td.appendChild(t);}else td.textContent=val;tr.appendChild(td);}$('trace').appendChild(tr);}
  $('history').replaceChildren();for(const h of state.history){const div=document.createElement('div');div.className='history-row';const left=document.createElement('span'),right=document.createElement('span');left.textContent='#'+h.id+' \u00b7 '+h.result.name;right.textContent=money(h.result.totalCents)+' gross';div.append(left,right);$('history').appendChild(div);}
 }
 $('deal').onclick=()=>act(async()=>{const before=state.round?state.round.hand.slice():Array(5).fill(null);if(await move('deal',{settings:settings()}))animate(before,[0,1,2,3,4]);});
 $('draw').onclick=()=>act(async()=>{const before=state.round.hand.slice(),slots=[0,1,2,3,4].filter(i=>!state.round.holds[i]);if(await move(slots.length?'draw':'bank'))animate(before,slots);});
 $('skip-reels').onclick=()=>reels.skip();
 $('exit-example').onclick=()=>{if(busy||committing)return;preview=null;cancelOdds();render();};
 for(const b of document.querySelectorAll('[data-example]'))b.onclick=()=>{if(busy||committing)return;preview=b.dataset.example==='royal'?{name:'A royal, read two ways.',hand:['10H','JH','QH','KH','AH']}:{name:'The archive lock, exactly.',hand:E.ARCHIVE_KEY};cancelOdds();render();};
 for(const [id,mode]of[['show-cards','card'],['show-symbols','symbol']])$(id).onclick=()=>{if(busy||committing)return;display=mode;faces.clear();render();};
 $('knob').oninput=()=>$('knob-out').textContent=$('knob').value;
 $('export-record').onclick=()=>{const payload={format:'Prospect51-shared-jbits-v2.4',game:'Prospect 51',ruleVersion:'R51-0.3',createdAt:new Date().toISOString(),disclaimer:'Browser-local play currency, no cash value. Not a global jackpot or server fairness certificate.',accountRevision:record?.revision,state};const url=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='Prospect_51_jbit_receipt.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),2000);};
 $('odds').onclick=()=>act(async()=>{
  if(state.phase!=='hold'||preview||countingOdds)return;const epoch=++oddsEpoch,job=E.drawOdds(state.round.initial,state.round.holds);const counts=E.PAYS.map(()=>0);let done=0,gross=0;
  countingOdds=true;$('odds').disabled=true;
  publishOdds('Counting this hold…');
  function batch(){
   if(epoch!==oddsEpoch)return;let item;
   for(let n=0;n<3500;n++){
    item=job.iterator.next();if(item.done)break;const c=E.scoreFast(job.kept.concat(item.value));counts[c]++;gross+=E.PAYS[c];done++;
   }
   if(item&&item.done){countingOdds=false;const paid=done-counts[0];publishOdds(`${fmt(done)} equally likely completions. Award chance ${(100*paid/done).toFixed(4)}%. Royal: ${counts[9]} / ${fmt(done)}. Expected base gross: ${(gross/done).toFixed(6)} jbits. The entry is already paid; the archive bonus is fixed by the initial deal.`);$('odds').disabled=false;if($('card-count-odds'))$('card-count-odds').disabled=false;}
   else{publishOdds(`Counting ${fmt(done)} / ${fmt(job.total)} completions... Change a hold to cancel.`);setTimeout(batch,0);}
  }
  setTimeout(batch,0);
 });

 function bindCardActions(hand,active,locked){
  for(let i=0;i<5;i++){
   const node=$('rotor-'+i).querySelector('.reel-face');
   node.setAttribute('aria-disabled',String(locked));
   function openDecision(trigger){
    if(locked)return;
    const c=hand[i],d=E.BY_ID.get(c),symbol=(faces.get(c)||display)==='symbol';
    const actions=[];
    if(active)actions.push({label:state.round.holds[i]?'Release this card':'Hold this card',primary:true,run:()=>move('hold',{slot:i})});
    if(active)actions.push({label:'Count hold odds',disabled:countingOdds,run:()=>{$('odds').click();openDecision(node);}});
    if(c)actions.push({label:symbol?'Turn to card face':'Turn to paper mark',run:()=>{faces.set(c,symbol?'card':'symbol');render();}});
    actions.push({label:'Read these odds',run:()=>CardUI.reveal('odds')});
    let content;
    if(active){content=document.createElement('div');content.className='card-decision-readout';const summary=document.createElement('p');summary.textContent=state.round.holds.filter(Boolean).length+' / 5 held · '+E.score(hand).name+' now.';const odds=document.createElement('p');odds.id='card-hold-odds';odds.setAttribute('role','status');odds.setAttribute('aria-live','polite');odds.textContent=$('odds-result').textContent;content.append(summary,odds);}
    CardUI.open(trigger,{within:$('reel-stage'),title:c?d.rank+{S:'♠',H:'♥',D:'♦',C:'♣'}[d.suit]+' · rotor '+(i+1):'Rotor '+(i+1),info:active?'':preview?'Illustration only.':'Spin five with the table button to choose a hold.',content,actions,focusFallback:active?$('draw'):$('deal')});
    for(const button of document.querySelectorAll('#card-actions button'))if(button.textContent==='Count hold odds')button.id='card-count-odds';
   }
   CardUI.activate(node,openDecision,(hand[i]?'Rotor '+(i+1)+' '+dLabel(hand[i]):'Undealt rotor '+(i+1))+' · hold odds and card options');
  }
 }
 function dLabel(c){const d=E.BY_ID.get(c);return d.rank+{S:'♠',H:'♥',D:'♦',C:'♣'}[d.suit];}
 function lab(){const u=Number($('lab-u').value),v=Number($('lab-v').value),i=17*u+v,d=E.DATA[i];$('u-out').textContent=u;$('v-out').textContent=v;$('lab-token').setAttribute('card',d.card);$('lab-address').textContent=`i = ${i}; canonical identity a${i+1}; ${d.role}, ${d.codePoint}. Triangular address (${d.n}, ${d.k}).`;const a=Number($('lab-step').value),reach=new Set(Array.from({length:51},(_,j)=>(a*j)%51));$('lab-dots').replaceChildren();for(let j=0;j<51;j++){const s=document.createElement('span');s.className='dot'+(reach.has(j)?' on':'');$('lab-dots').appendChild(s);}$('lab-reach').textContent=`gcd(${a}, 51) = ${E.gcd(a,51)}. ${reach.size} of 51 positions reachable; ${E.gcd(a,51)} input digits per reachable output.`;}
 for(const id of ['lab-u','lab-v','lab-step'])$(id).oninput=lab;
 document.addEventListener('visibilitychange',()=>{if(document.hidden)reels.skip();});window.addEventListener('resize',()=>{if(busy)reels.skip();});
 if(!globalThis.crypto?.getRandomValues)error(new Error('Secure browser randomness is unavailable. Random deals will not run; examples and the mechanism lab remain available.'));
 function openHash(){const target=document.getElementById(location.hash.slice(1));if(!target)return;let p=target;while(p){if(p.tagName==='DETAILS')p.open=true;p=p.parentElement;}requestAnimationFrame(()=>target.scrollIntoView({block:'start'}));}
 addEventListener('hashchange',openHash);openHash();
 lab();render();
 try{const res=await readGame();record=res.value;state=record.state;saveInvalid=false;hydrate();save();render();}
 catch(e){error(e);render();}
 let lastRevision=0;
 subscribeCredits(snap=>{
  state.balanceCents=snap.balanceCents;
  if(snap.revision===lastRevision)return;lastRevision=snap.revision;
  if(!busy&&!committing)render();
 });
 // Read without creating a transaction/broadcast loop. Refresh the game checkpoint
 // when another tab committed a newer Prospect revision.
 const {readWallet}=await import('../assets/credits-v2-0b3.js');
 async function resume(){if(busy||committing)return;try{const w=await readWallet(),r=w.apps.prospect51;if(r&&r.revision!==record?.revision){record=r;state={...r.state,balanceCents:w.balanceCents};hydrate();cancelOdds();CardUI.close(false);render();}}catch(e){error(e);}}
 addEventListener('focus',resume);document.addEventListener('visibilitychange',()=>{if(!document.hidden)resume();});
 setInterval(resume,5000);
})();
