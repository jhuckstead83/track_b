import {ProspectSounds} from './sounds-v2-6.js';

// The approved engine decides the category. This only locates its contributing cards.
export function scoringSlots(hand,category){
  if(!category||hand.length!==5)return [];
  if([4,5,6,8,9].includes(category))return [0,1,2,3,4];
  const counts=new Map();for(const card of hand){const rank=card.slice(0,-1);counts.set(rank,(counts.get(rank)||0)+1);}
  const count=category===7?4:category===3?3:2;
  return hand.flatMap((card,i)=>counts.get(card.slice(0,-1))===count?[i]:[]);
}

export class ProspectRewards {
  constructor({machine,rotors,layer,bank,soundButton}){
    this.machine=machine;this.rotors=rotors;this.layer=layer;this.bank=bank;
    this.sound=new ProspectSounds(soundButton);this.seen=new Set();this.frame=null;this.timer=null;this.counter=null;
  }
  sync({hand,score,result,eligible,preview=false}){
    const slots=eligible&&score?scoringSlots(hand,score.category):[];
    const paid=eligible&&!!(result?.totalCents||preview&&score?.grossCents);
    this.machine.classList.toggle('reward-win',paid);
    this.machine.classList.toggle('archive-award',!!(eligible&&result?.bonusCents));
    this.machine.dataset.reward=paid?(preview?'example':result?.bonusCents?'jackpot':result?.netCents===0?'return':'win'):'none';
    for(const [i,rotor]of [...this.rotors.children].entries()){
      const winner=slots.includes(i);rotor.classList.toggle('scoring-rotor',winner);
      const face=rotor.querySelector('.reel-face');face.classList.toggle('scoring-card',winner);
      if(winner)face.setAttribute('aria-label',face.getAttribute('aria-label')+' · scoring card');
    }
    if(this.counter)this.writeCount(this.counter.value);
    return slots;
  }
  writeCount(value){const node=this.machine.querySelector('.award-count');if(node)node.textContent=(value/100).toFixed(2);}
  finish(){
    if(this.frame!==null)cancelAnimationFrame(this.frame);if(this.timer!==null)clearTimeout(this.timer);
    this.frame=this.timer=null;
    if(this.counter)this.writeCount(this.counter.total);this.counter=null;
    this.layer.replaceChildren();this.machine.classList.remove('celebrating');this.bank.classList.remove('jbit-arrival');this.sound.silence();
  }
  celebrate({key,hand,result,reduced=false,preview=false}){
    if(this.seen.has(key))return false;this.seen.add(key);
    // Bound presentation memory without making it part of the financial ledger.
    if(this.seen.size>40)this.seen.delete(this.seen.values().next().value);
    this.finish();
    if(!result||result.totalCents<=0||document.hidden)return false;
    this.sound.award(result);
    if(reduced||result.netCents<=0)return false;
    this.machine.classList.add('celebrating');
    const slots=scoringSlots(hand,result.category),box=this.machine.getBoundingClientRect();
    const target=(preview?this.machine.querySelector('#result-title'):this.bank).getBoundingClientRect();
    const end={x:target.left-box.left+target.width/2,y:target.top-box.top+target.height/2};
    const origins=slots.length?slots.map(i=>this.rotors.children[i].querySelector('.reel-face')):[this.machine.querySelector('.vault')];
    const count=result.bonusCents||result.category>=7?20:12;
    for(let i=0;i<count;i++){
      const origin=origins[i%origins.length].getBoundingClientRect();
      const x=origin.left-box.left+origin.width/2,y=origin.top-box.top+origin.height/2;
      const coin=document.createElement('span');coin.className='jbit-coin';coin.textContent='j';
      const dx=end.x-x,dy=end.y-y;
      for(const [name,value]of Object.entries({'left':x+'px','top':y+'px','--dx':dx+'px','--dy':dy+'px','--arc-x':(dx*.45+Math.sin(i*2.4)*34)+'px','--arc-y':(Math.min(-38,dy*.45)-28-i%3*9)+'px','--delay':(i*48)+'ms','--turn':(i%2?22:-22)+'deg'}))coin.style.setProperty(name,value);
      this.layer.appendChild(coin);
    }
    const total=result.totalCents,duration=1400,started=performance.now();
    if(!preview){
      this.counter={total,value:0};this.writeCount(0);this.bank.classList.add('jbit-arrival');
      const tick=now=>{
        if(!this.counter)return;
        const progress=Math.max(0,Math.min(1,(now-started)/duration));
        this.counter.value=Math.round(total*(1-Math.pow(1-progress,3)));this.writeCount(this.counter.value);
        if(progress<1)this.frame=requestAnimationFrame(tick);else this.frame=null;
      };
      this.frame=requestAnimationFrame(tick);
    }
    this.timer=setTimeout(()=>this.finish(),2400);return true;
  }
}
