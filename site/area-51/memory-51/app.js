import {ready,refreshCredits,recordRecall,formatCredits,recoveryCountdown,subscribeCredits,getCreditSnapshot} from '../assets/credits.js';
const {symbols:SYMBOLS}=await (await fetch('../assets/SYMBOLS_51.json')).json();
const $=id=>document.getElementById(id),SUITS={S:'♠',H:'♥',D:'♦',C:'♣'},KEY='cerebralgraphix.area51.memory51.v2';
let stats;try{stats=JSON.parse(localStorage.getItem(KEY)||'null');}catch{}
if(!stats||!Array.isArray(stats.history))stats={completed:0,correct:0,streak:0,notes:{},history:[],direction:'mixed'};
let prompt,busy=false,bag=[],readyForRewards=false;
const random=max=>{const x=new Uint32Array(1),lim=4294967296-4294967296%max;do{crypto.getRandomValues(x);}while(x[0]>=lim);return x[0]%max;};
function shuffle(a){for(let i=a.length-1;i>0;i--){const j=random(i+1);[a[i],a[j]]=[a[j],a[i]];}return a;}
function save(){try{localStorage.setItem(KEY,JSON.stringify(stats));}catch{$('message-sub').textContent+=' Local notes could not be saved.';}}
const face=c=>c.slice(0,-1)+SUITS[c.slice(-1)];
function card(c){const r=c.slice(0,-1),s=SUITS[c.slice(-1)];return '<span class="a51-card '+(/[HD]$/.test(c)?'is-red':'')+'" role="img" aria-label="'+face(c)+'"><span class="corner">'+r+'<small>'+s+'</small></span><span aria-hidden="true">'+s+'</span><span class="corner bottom" aria-hidden="true">'+r+'<small>'+s+'</small></span></span>';}
function setMessage(a,b){$('message-title').textContent=a;$('message-sub').textContent=b;}
function renderStats(){$('completed').textContent=stats.completed;$('correct').textContent=stats.correct;$('streak').textContent=stats.streak;$('accuracy').textContent=stats.completed?Math.round(stats.correct*100/stats.completed)+'%':'—';}
function renderBank(s){$('bank').textContent=s.ready?formatCredits(s.balanceCents):'—';$('bank-clock').textContent=recoveryCountdown(s);$('learning-progress').textContent=formatCredits(s.recallPaid||0)+' / 8 jbits';$('learning-fill').style.width=Math.min(100,(s.recallPaid||0)/8)+'%';}
function renderPair(){const disclosed=prompt&&(prompt.assisted||prompt.answered);$('pair-title').textContent=disclosed?face(prompt.target.card)+' ↔ '+prompt.target.symbol:'Your pair appears after recall.';$('pair-detail').textContent=disclosed?prompt.target.id+' · '+prompt.target.codePoint+' · exact reversible key.':'Answer first, or choose Study to reveal the pair.';$('meaning').value=disclosed?(stats.notes[prompt.target.id]||''):'';$('meaning').disabled=$('save-meaning').disabled=!disclosed;}
function render(){const x=prompt.target,d=prompt.direction;
$('prompt-kind').textContent=d==='card-symbol'?'Card → component symbol':'Component symbol → card';
$('prompt-object').innerHTML=d==='card-symbol'?card(x.card):'<div class="cg51-symbol" role="img" aria-label="Component '+x.id+' '+x.codePoint+'">'+x.symbol+'</div>';
$('answers').innerHTML=prompt.options.map(o=>'<button class="cg51-answer" data-answer="'+o.id+'" '+(busy||prompt.answered?'disabled':'')+'>'+(d==='card-symbol'?o.symbol+' · '+o.id:face(o.card))+'</button>').join('');
for(const b of $('answers').querySelectorAll('button')){b.onclick=()=>answer(b.dataset.answer);if(prompt.answered){if(b.dataset.answer===x.id)b.classList.add('correct');else if(b.dataset.answer===prompt.selected)b.classList.add('wrong');}}
$('study').disabled=busy||prompt.answered;$('next').disabled=busy;$('direction').disabled=busy;renderPair();renderStats();}
function next(){if(busy)return;if(!bag.length)bag=shuffle(SYMBOLS.slice());const target=bag.pop(),other=shuffle(SYMBOLS.filter(s=>s.id!==target.id)).slice(0,3);const dir=$('direction').value;prompt={id:crypto.randomUUID(),target,direction:dir==='mixed'?(random(2)?'card-symbol':'symbol-card'):dir,options:shuffle([target,...other]),assisted:false,answered:false,started:performance.now()};render();setMessage('Make the match.','Four choices. A correct unassisted answer earns 2 jbits, up to 8 per day.');}
async function answer(id){if(busy||prompt.answered||!prompt.options.some(s=>s.id===id))return;busy=true;render();const correct=id===prompt.target.id;try{
  if(!readyForRewards)await ready;
  const result=await recordRecall({id:prompt.id,correct,assisted:prompt.assisted,options:4,evidence:{symbolId:prompt.target.id,card:prompt.target.card,direction:prompt.direction}});
  prompt.answered=true;prompt.selected=id;stats.completed++;if(correct){stats.correct++;stats.streak++;}else stats.streak=0;
  stats.history.push({id:prompt.id,card:prompt.target.card,symbolId:prompt.target.id,direction:prompt.direction,correct,assisted:prompt.assisted,responseMs:Math.round(performance.now()-prompt.started),jbits:result.entry.deltaCents/100});
  if(stats.history.length>500)stats.history=stats.history.slice(-500);save();
  const earned=result.entry.deltaCents/100;setMessage(correct?'You found the pair.':'Here is the pair.',face(prompt.target.card)+' ↔ '+prompt.target.symbol+(earned?' · +'+earned+' jbits.':prompt.assisted?' · Study round; no award.':correct?' · Daily recall award reached. Keep practicing.':' · No award. Try the next card.'));renderBank(result.snapshot);
}catch(e){setMessage('Bank update unavailable.',e.message+' You can retry this answer.');}finally{busy=false;render();}}
$('study').onclick=()=>{if(busy||prompt.answered)return;prompt.assisted=true;renderPair();setMessage('Study the pair.',face(prompt.target.card)+' ↔ '+prompt.target.symbol+' · This answer is practice, with no jbit award.');};
$('next').onclick=next;$('direction').value=stats.direction||'mixed';$('direction').onchange=()=>{stats.direction=$('direction').value;save();next();};
$('save-meaning').onclick=()=>{if(!prompt.assisted&&!prompt.answered)return;stats.notes[prompt.target.id]=$('meaning').value.trim();save();setMessage('Note saved.',stats.notes[prompt.target.id]||'The note for this pair is cleared.');};
$('reset-session').onclick=()=>{if(busy)return;stats.completed=stats.correct=stats.streak=0;stats.history=[];save();renderStats();setMessage('Session statistics reset.','Your shared jbits, daily award counter and notes are unchanged.');};
$('save-receipt').onclick=()=>{const receipt={schema:'memory51-v2',collected:false,alphabet:'line-game-v7.2-components-51',completed:stats.completed,correct:stats.correct,history:stats.history,pricing:{fourChoiceCorrectUnassisted:2,dailyCap:8},bank:getCreditSnapshot()};const url=URL.createObjectURL(new Blob([JSON.stringify(receipt,null,2)],{type:'application/json'})),a=document.createElement('a');a.href=url;a.download='Memory_51_v2_receipt.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
if(new URLSearchParams(location.search).get('return')==='blackjack51'){$('return-blackjack').hidden=false;$('return-blackjack').onclick=e=>{if(window.opener&&!window.opener.closed){e.preventDefault();window.close();}};}
subscribeCredits(renderBank);ready.then(()=>{readyForRewards=true;}).catch(e=>setMessage('Practice is available.',e.message));
next();setInterval(()=>refreshCredits().catch(()=>{}),1000);
