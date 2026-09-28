/* Original oscillator-made cues. No samples, recordings, network, or game state. */
export class ProspectSounds {
  constructor(button) {
    this.button=button;this.context=null;this.master=null;this.nodes=new Set();this.ratchet=null;this.unlocking=null;this.generation=0;
    this.enabled=false;this.unavailable=false;
    try{this.enabled=localStorage.getItem('prospect51.sound')==='on';}catch{}
    this.button.onclick=()=>{
      this.enabled=!this.enabled;
      try{localStorage.setItem('prospect51.sound',this.enabled?'on':'off');}catch{}
      if(this.enabled){this.unlock().then(ready=>{if(ready&&this.enabled)this.bell(880,0,.28,.11);});}
      else this.silence();
      this.render();
    };
    this.render();
  }
  render(){
    this.button.textContent=this.unavailable?'♪ Sound unavailable':this.enabled?'♪ Sound on':'♪ Sound off';
    this.button.setAttribute('aria-pressed',String(this.enabled&&!this.unavailable));
    this.button.setAttribute('aria-label',this.unavailable?'Slot sounds are unavailable in this browser':this.enabled?'Mute slot sounds':'Turn slot sounds on');
    this.button.disabled=this.unavailable;
  }
  async unlock(){
    if(!this.enabled||this.unavailable)return false;
    try{
      if(!this.context){
        const Audio=globalThis.AudioContext||globalThis.webkitAudioContext;
        if(!Audio){this.unavailable=true;this.render();return false;}
        this.context=new Audio();this.master=this.context.createGain();this.master.gain.value=.22;this.master.connect(this.context.destination);
      }
      if(this.context.state!=='running'){this.unlocking=this.context.resume();await this.unlocking;}
      return this.enabled&&this.context.state==='running';
    }catch{return false;}
  }
  tone(frequency,delay=0,duration=.12,volume=.12,type='sine',endFrequency=frequency){
    if(!this.enabled||!this.context||this.context.state!=='running'||document.hidden)return;
    try{
      const at=this.context.currentTime+delay,osc=this.context.createOscillator(),gain=this.context.createGain();
      osc.type=type;osc.frequency.setValueAtTime(frequency,at);osc.frequency.exponentialRampToValueAtTime(Math.max(30,endFrequency),at+duration);
      gain.gain.setValueAtTime(.0001,at);gain.gain.linearRampToValueAtTime(volume,at+.005);gain.gain.exponentialRampToValueAtTime(.0001,at+duration);
      osc.connect(gain);gain.connect(this.master);this.nodes.add(osc);
      osc.onended=()=>{this.nodes.delete(osc);osc.disconnect();gain.disconnect();};
      osc.start(at);osc.stop(at+duration+.02);
    }catch{/* Audio failure never interrupts a committed game action. */}
  }
  bell(frequency,delay=0,duration=.55,volume=.13){
    this.tone(frequency,delay,duration,volume);
    this.tone(frequency*2.76,delay,duration*.6,volume*.23);
    this.tone(frequency*4.2,delay,duration*.35,volume*.08);
  }
  hold(held){this.tone(held?640:420,0,.065,.13,'triangle');}
  startSpin(){
    this.stopSpin();let tick=0;
    const click=()=>{this.tone(170+(tick++%4)*24,0,.032,.085,'triangle',90);};
    click();this.ratchet=setInterval(click,105);
  }
  stopReel(slot){this.tone(130+slot*16,0,.08,.15,'triangle',65);this.tone(750+slot*70,0,.035,.065);}
  stopSpin(){if(this.ratchet!==null)clearInterval(this.ratchet);this.ratchet=null;}
  award({netCents,bonusCents=0,category=0}){
    this.stopSpin();
    if(!this.enabled||!this.context)return;
    if(this.context.state!=='running'){
      const generation=this.generation;
      this.unlocking?.then(()=>{if(this.generation===generation&&this.enabled&&this.context.state==='running')this.award({netCents,bonusCents,category});}).catch(()=>{});
      return;
    }
    if(netCents<0)return;
    if(netCents===0){this.bell(660,0,.24,.07);return;}
    const large=bonusCents>0||category>=7;
    const notes=large?[523.25,659.25,783.99,1046.5,1318.5,1567.98]:[659.25,783.99,1046.5];
    notes.forEach((f,i)=>this.bell(f,i*.14,large?.8:.55,.12));
    for(let i=0;i<(large?12:6);i++)this.tone(1250+(i%3)*180,.35+i*.1,.045,.04);
  }
  silence(){this.generation++;this.stopSpin();for(const node of [...this.nodes]){try{node.stop();}catch{}}this.nodes.clear();}
}
