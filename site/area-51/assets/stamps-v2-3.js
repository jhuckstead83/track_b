import {atomic,readWallet} from './credits-v2-0b3.js';
import {recall} from './wallet-core-v2-0b3.js';
const alphabet=await (await fetch('/area-51/assets/SYMBOLS_51.json')).json();
export const STAMPS=alphabet.symbols;
const byCard=new Map(STAMPS.map(s=>[s.card,s]));
export const stampFor=card=>byCard.get(card);
export const cardName=card=>card?card.slice(0,-1)+{S:'♠',H:'♥',D:'♦',C:'♣'}[card.slice(-1)]:'';
const bookSchema='cerebralgraphix.card-stamps.v1';
function earnedMarks(wallet){
 const saved=wallet.apps.cardStamps;
 if(saved&&saved.schema!==bookSchema)throw Error('The stamp collection could not be read. It has been retained.');
 const marks={...(saved?.marks||{})};
 // Recover learning already certified in the shared bank; local practice notes are not awards.
 for(const e of wallet.entries){const x=e.evidence,s=x&&byCard.get(x.card);
  if(e.kind==='four-way-recall'&&x.correct===true&&x.assisted===false&&s?.id===x.symbolId&&!marks[x.card])marks[x.card]={card:x.card,symbolId:s.id,earnedAt:e.at,receipt:e.id};
 }
 return marks;
}
export async function readStampBook(){return earnedMarks(await readWallet());}
export async function recordStampedRecall(tx){
 const s=byCard.get(tx.evidence?.card);if(!s||s.id!==tx.evidence?.symbolId)throw Error('The recall pair does not match the published alphabet.');
 const result=await atomic(wallet=>{
  const marks=earnedMarks(wallet),had=!!marks[s.card],paid=recall(wallet,tx,Date.now());
  // The persisted receipt, including retries, is authoritative.
  const evidence=paid.entry.evidence;
  if(evidence?.correct===true&&evidence.assisted===false&&evidence.card===s.card&&evidence.symbolId===s.id){
   marks[s.card]||={card:s.card,symbolId:s.id,earnedAt:paid.entry.at,receipt:paid.entry.id};
   wallet.apps.cardStamps={schema:bookSchema,marks};
  }
  return {...paid,newStamp:!had&&!!marks[s.card],marks};
 });
 return {...result.value,snapshot:result.snapshot};
}
// Passing no card produces a genuinely anonymous back: no identity in DOM or labels.
export function houseCard({card=null,face='back',earned=false,label}={}){
 const s=byCard.get(card),known=!!s&&face!=='back',node=document.createElement('span');
 node.className='house-card '+(known&&face==='face'?'house-front':'house-back')+(known&&earned?' learned':'');
 node.setAttribute('role','img');node.setAttribute('aria-label',label||(known?(face==='face'?cardName(card):'Component '+s.id+' '+s.codePoint):'Unmarked house card back'));
 if(!known){const monogram=document.createElement('span');monogram.className='house-monogram';monogram.textContent='Ⅰ';monogram.setAttribute('aria-hidden','true');node.append(monogram);return node;}
 if(face==='face'){
  const red=/[HD]$/.test(card);node.classList.toggle('red',red);
  for(const where of ['top','bottom']){const corner=document.createElement('span');corner.className='house-corner '+where;corner.textContent=cardName(card);corner.setAttribute('aria-hidden','true');node.append(corner);}
  const pip=document.createElement('span');pip.className='house-pip';pip.textContent={S:'♠',H:'♥',D:'♦',C:'♣'}[card.slice(-1)];pip.setAttribute('aria-hidden','true');node.append(pip);
 }else{
  const mark=document.createElement('span');mark.className='house-stamp';mark.setAttribute('aria-hidden','true');
  const token=document.createElement('p51-token');token.setAttribute('card',card);token.setAttribute('face','symbol');token.setAttribute('static','');mark.append(token);node.append(mark);
 }
 return node;
}
export function mountStampLab({marks={},onInspect=()=>{},onPractice}={}){
 const grid=document.getElementById('stamp-collection'),select=document.getElementById('stamp-select'),preview=document.getElementById('stamp-preview'),flip=document.getElementById('stamp-flip'),practice=document.getElementById('stamp-practice');
 if(!grid)return {update(){}};
 let book=marks,chosen=null,face='stamp';
 for(const s of STAMPS){const o=document.createElement('option');o.value=s.card;o.textContent=cardName(s.card);select.append(o);}
 function show(card,notify=true){
  chosen=card;select.value=card;if(notify)onInspect(card);preview.replaceChildren(houseCard({card,face,earned:!!book[card]}));
  document.getElementById('stamp-pair').textContent=cardName(card)+' ↔ '+stampFor(card).id+' · '+(book[card]?'stamp earned':'practice to earn');
  flip.disabled=false;flip.textContent=face==='stamp'?'Turn to card face':'Turn to stamp';practice.hidden=false;practice.textContent='Practice this pair';
 }
 function render(){
  document.getElementById('stamp-count').textContent=Object.keys(book).length+' / 51';grid.replaceChildren();
  for(const s of STAMPS){const b=document.createElement('button');b.type='button';b.className='stamp-slot';b.disabled=!book[s.card];b.setAttribute('aria-label',book[s.card]?'Inspect earned '+cardName(s.card)+' stamp':'Uncollected stamp');b.append(houseCard({card:book[s.card]?s.card:null,face:'stamp',earned:!!book[s.card]}));if(book[s.card])b.onclick=()=>{face='stamp';show(s.card);};grid.append(b);}
  if(chosen)show(chosen,false);
 }
 select.onchange=()=>{if(byCard.has(select.value)){face='stamp';show(select.value);}};
 flip.onclick=()=>{if(!chosen)return;face=face==='stamp'?'face':'stamp';show(chosen);};
 practice.onclick=()=>{const target=chosen||STAMPS.find(s=>!book[s.card])?.card||STAMPS[0].card;if(onPractice)onPractice(target);else location.href='../memory-51/?card='+encodeURIComponent(target)+'&return=telescope51';};
 render();return {update(next){book=next;render();}};
}
