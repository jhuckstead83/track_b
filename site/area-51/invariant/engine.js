
const SUITS=['S','H','D','C'], RANKS=['A','2','3','4','5','6','7','8','9','10','J','Q','K'];
const FACES=RANKS.flatMap(r=>SUITS.map(s=>r+s));
const faceQ=c=>FACES.indexOf(c);
const cloneHands=h=>h.map(x=>x.slice());
const stateKey=h=>h.map(x=>x.join(',')).join('|');
const FACT=[1n];for(let i=1;i<=51;i++)FACT.push(FACT[i-1]*BigInt(i));
function rankDeck(deck){if(deck.length!==52||deck[51]!=='2C'||new Set(deck).size!==52||deck.some(c=>!FACES.includes(c)))throw new Error('Use every ordinary card exactly once, with 2C last.');let remaining=FACES.filter(c=>c!=='2C'),r=0n;for(let i=0;i<51;i++){const d=remaining.indexOf(deck[i]);r+=BigInt(d)*FACT[50-i];remaining.splice(d,1);}return r;}
function decimalRank(r){return `${r/1000000000000n}.${(r%1000000000000n).toString().padStart(12,'0')}`;}
class CardGame{
 constructor(initial,{forgiveness=false,nullFace='2C'}={}){const cards=initial.flat();if(initial.length!==3||cards.length!==51||new Set(cards).size!==51||cards.includes(nullFace)||cards.some(c=>!FACES.includes(c)))throw new Error('Invalid initial hands.');this.initial=cloneHands(initial);this.hands=cloneHands(initial);this.forgiveness=forgiveness;this.nullFace=nullFace;this.bank=[];this.turn=0;this.status='playing';this.winner=null;this.last=null;this.cycle=null;this.interventions=0;this.events=[];this.seen=new Map([[stateKey(this.hands),0]]);}
 snapshot(){return{turn:this.turn,status:this.status,winner:this.winner,counts:this.hands.map(h=>h.length),bank:this.bank.length,interventions:this.interventions,cycle:this.cycle};}
 checkEnd(){const live=this.hands.map((h,p)=>h.length?p:-1).filter(p=>p>=0);if(live.length<=1){this.status=live.length?'finished':'draw';this.winner=live.length?live[0]+1:null;return true;}return false;}
 replayStep(){if(this.status!=='cycle')throw new Error('Replay requires a certified cycle.');const c=this.cycle;this.status='playing';this.seen=new Map();this.step();this.status='cycle';this.cycle={entry:c.entry+1,repeat:c.repeat+1,period:c.period};return this.snapshot();}
 checkMass(){const all=this.hands.flat().concat(this.bank);if(all.length!==51||new Set(all).size!==51||all.includes(this.nullFace))throw new Error('Card-accounting invariant failed.');}
 forgive(){if(this.status!=='cycle')throw new Error('Concession requires an exact repeat.');const moved=[];this.hands.forEach((h,p)=>{if(h.length){const card=h.shift();this.bank.push(card);moved.push({player:p+1,card});}});if(moved.length<2)throw new Error('An active cycle needs at least two hands.');this.interventions++;this.events.push({kind:'forgive',turn:this.turn,cycle:this.cycle,moved,bank:this.bank.length});this.status='playing';this.cycle=null;this.seen=new Map([[stateKey(this.hands),this.turn]]);this.checkMass();this.checkEnd();}
 step(){if(this.status!=='playing')return this.snapshot();if(this.checkEnd())return this.snapshot();const drawn=[];this.hands.forEach((h,p)=>{if(h.length)drawn.push({player:p,card:h.shift()});});const win=drawn.reduce((a,b)=>faceQ(a.card)>faceQ(b.card)?a:b).player;const ordered=[];for(let k=0;k<3;k++){const d=drawn.find(x=>x.player===(win+k)%3);if(d)ordered.push(d.card);}this.hands[win].push(...ordered);this.turn++;this.last={drawn:drawn.map(d=>({player:d.player+1,card:d.card})),winner:win+1,returned:ordered};this.events.push({kind:'play',turn:this.turn,...this.last});this.checkMass();if(this.checkEnd())return this.snapshot();const key=stateKey(this.hands);if(this.seen.has(key)){this.cycle={entry:this.seen.get(key),repeat:this.turn,period:this.turn-this.seen.get(key)};this.status='cycle';if(this.forgiveness)this.forgive();}else this.seen.set(key,this.turn);return this.snapshot();}
}
globalThis.InvariantEngine={CardGame,rankDeck,decimalRank,FACES,FACT};
