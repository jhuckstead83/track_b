/* Reel travel is presentation. The account commits before play() is called. */
const attr=(el,name,value)=>{if(value==null)el.removeAttribute(name);else if(el.getAttribute(name)!==String(value))el.setAttribute(name,String(value));};
export class ProspectReels{
  constructor(root,cards){this.root=root;this.cards=cards.slice();this.active=new Set();this.current=null;this.rotors=[];}
  bind(){this.rotors=[...this.root.querySelectorAll('.rotor')];}
  neighbors(slot){return [this.cards[(slot*11+7)%51],this.cards[(slot*11+29)%51]];}
  cell(card,face){
    const cell=document.createElement('div');cell.className='reel-cell';
    const token=document.createElement('p51-token');token.setAttribute('size','reel');token.setAttribute('static','');
    if(card)token.setAttribute('card',card);token.setAttribute('face',face);cell.append(token);return cell;
  }
  syncSlot(slot,card,face){
    if(this.active.has(slot))return;
    const rotor=this.rotors[slot],token=rotor.querySelector('.reel-face p51-token');
    attr(token,'card',card);attr(token,'face',face);
    for(const [i,selector]of ['.reel-above','.reel-below'].entries()){
      const ghost=rotor.querySelector(selector+' p51-token');attr(ghost,'card',this.neighbors(slot)[i]);attr(ghost,'face',face);
    }
  }
  play({slots,before,after,faceFor,instant,onStop,onDone}){
    if(this.current)throw Error('Reels are already turning.');
    const job={pending:new Set(slots),tracks:new Map(),onStop,onDone,frame:null,started:null};
    this.current=job;this.active=new Set(slots);this.root.classList.add('spinning');this.root.setAttribute('aria-busy','true');
    job.watchdog=setTimeout(()=>this.skip(),4000);
    if(instant||!slots.length){queueMicrotask(()=>this.skip());return;}
    try{
      for(const [order,slot]of slots.entries()){
        const rotor=this.rotors[slot],strip=rotor.querySelector('.reel-strip'),[top,bottom]=this.neighbors(slot);
        const travel=Array.from({length:20+slot*3},(_,k)=>this.cards[(slot*13+k*7)%51]);
        const sequence=[top,after[slot],bottom,...travel,top,before[slot]||null,bottom];
        strip.replaceChildren(...sequence.map(card=>this.cell(card,faceFor(card))));
        const height=rotor.querySelector('.reel-face').getBoundingClientRect().height;
        if(!(height>0))throw Error('Reel window has no height.');
        const track={strip,start:-(sequence.length-2)*height,end:-height,duration:1250+order*190};
        strip.style.transform=`translate3d(0,${track.start}px,0)`;
        job.tracks.set(slot,track);rotor.classList.add('is-spinning');rotor.setAttribute('aria-busy','true');
      }
      // Move the actual symbol bands on every frame. Window/glass overlays never move.
      const tick=now=>{
        if(this.current!==job)return;
        if(job.started===null)job.started=now;
        for(const slot of [...job.pending]){
          const t=job.tracks.get(slot),p=Math.min(1,(now-job.started)/t.duration),ease=1-Math.pow(1-p,3);
          t.strip.style.transform=`translate3d(0,${t.start+(t.end-t.start)*ease}px,0)`;
          if(p===1)this.stop(slot);
        }
        if(this.current===job)job.frame=requestAnimationFrame(tick);
      };
      job.frame=requestAnimationFrame(tick);
    }catch(error){this.skip();}
  }
  stop(slot){
    const job=this.current;if(!job||!job.pending.has(slot))return;
    job.pending.delete(slot);this.active.delete(slot);
    const rotor=this.rotors[slot],strip=rotor.querySelector('.reel-strip');
    rotor.classList.remove('is-spinning');rotor.setAttribute('aria-busy','false');strip.replaceChildren();strip.style.transform='';
    job.onStop(slot);
    if(!job.pending.size)this.complete(job);
  }
  complete(job){if(this.current!==job)return;cancelAnimationFrame(job.frame);clearTimeout(job.watchdog);this.current=null;this.root.classList.remove('spinning');this.root.setAttribute('aria-busy','false');job.onDone();}
  skip(){const job=this.current;if(!job)return;for(const slot of [...job.pending])this.stop(slot);if(this.current===job&&!job.pending.size)this.complete(job);}
}
