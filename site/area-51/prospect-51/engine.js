/* Prospect 51 rule engine v0.3 (first released as Rotor 51). Pure rules. No wallet, DOM, network, or implicit random fallback. */
(function (g) {
  'use strict';
  const DATA = g.P51_DATA || (typeof require === 'function' ? require('./data.js') : null);
  if (!DATA || DATA.length !== 51) throw new Error('The frozen 51-identity dictionary is required.');
  const CARDS = Object.freeze(DATA.map(x => x.card));
  const BY_ID = new Map(DATA.map(x => [x.card, x]));
  const ARCHIVE_KEY = Object.freeze(['10S','JD','JH','KS','10D']);
  const CATEGORIES = Object.freeze(['No award','Jacks or better','Two pair','Three of a kind','Straight','Flush','Full house','Four of a kind','Straight flush','Royal flush']);
  const PAYS = Object.freeze([0,1,2,3,4,6,9,25,50,250]); // gross points, 1-point entry
  const SCHEMA = 'project51.rotor51.demo.v0.3'; // original id kept on purpose: renaming it would orphan saved hands
  const mod = (x,m) => ((x%m)+m)%m;
  function gcd(a,b) { while(b) [a,b]=[b,a%b]; return Math.abs(a); }
  function choose(n,k) { if(k<0||k>n)return 0; let v=1;for(let i=1;i<=Math.min(k,n-k);i++)v=v*(n-i+1)/i;return Math.round(v); }
  function randBelow(m, fill) {
    if (!Number.isInteger(m)||m<1||m>0x100000000) throw new Error('Invalid random bound.');
    const fn=fill || (g.crypto && (a=>g.crypto.getRandomValues(a)));
    if(!fn)throw new Error('Secure browser randomness is unavailable. Random play is disabled; examples remain available.');
    const word=new Uint32Array(1), limit=0x100000000-(0x100000000%m);
    do {fn(word);} while(word[0]>=limit);
    return word[0]%m;
  }
  function gear(m,j,wire) {
    if(wire==='straight')return 1;
    if(wire!=='geared')throw new Error('Unknown rotor wiring.');
    let a=mod(2*j+1,m);while(gcd(a,m)!==1)a=mod(a+1,m);return a;
  }
  function draw(pool, slots, settings, random=randBelow, carry=0) {
    if(!Array.isArray(pool)||new Set(pool).size!==pool.length||pool.some(c=>!BY_ID.has(c)))throw new Error('Invalid remaining inventory.');
    if(!Number.isInteger(settings.knob)||settings.knob<0||settings.knob>50)throw new Error('Invalid ring setting.');
    if(!Array.isArray(slots)||new Set(slots).size!==slots.length||slots.some(x=>!Number.isInteger(x)||x<0||x>4)||slots.length>pool.length)throw new Error('Invalid rotor slots.');
    const left=pool.slice(),cards=[],trace=[];
    for(const slot of slots){
      const j=slot+1,m=left.length,a=gear(m,j,settings.wire),b=mod(settings.knob+j*(j+1)/2+carry,m),d=random(m);
      if(!Number.isInteger(d)||d<0||d>=m)throw new Error('Random source returned an invalid digit.');
      const e=mod(a*d+b,m),card=left.splice(e,1)[0];
      cards.push(card);trace.push({slot,j,m,a,b,d,e,card});carry+=e+1;
    }
    return {cards,remaining:left,trace};
  }
  function assertHand(hand){if(!Array.isArray(hand)||hand.length!==5||new Set(hand).size!==5||hand.some(c=>!BY_ID.has(c)))throw new Error('A hand must contain five distinct active identities.');}
  // Fast evaluator used by exact enumeration; callers validate the source hand/pool.
  function scoreFast(hand) {
    const ranks=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];let suit=null,flush=true;
    for(const c of hand){const d=BY_ID.get(c),r=d.natural===1?14:d.natural;ranks[r]++;if(suit===null)suit=d.suit;else if(d.suit!==suit)flush=false;}
    let pairs=0,trips=0,fours=0,highPair=false,unique=0,low=15,high=0;
    for(let r=2;r<=14;r++){const n=ranks[r];if(n){unique++;low=Math.min(low,r);high=r;}if(n===2){pairs++;if(r>=11)highPair=true;}if(n===3)trips++;if(n===4)fours++;}
    const wheel=unique===5&&ranks[14]&&ranks[2]&&ranks[3]&&ranks[4]&&ranks[5];
    const straight=unique===5&&(high-low===4||wheel);
    if(straight&&flush)return !wheel&&low===10?9:8;
    if(fours)return 7;if(trips&&pairs)return 6;if(flush)return 5;if(straight)return 4;
    if(trips)return 3;if(pairs===2)return 2;if(pairs===1&&highPair)return 1;return 0;
  }
  function score(hand){assertHand(hand);const category=scoreFast(hand);return {category,name:CATEGORIES[category],grossCents:PAYS[category]*100};}
  function isKey(hand){return hand.length===5&&hand.every((c,i)=>c===ARCHIVE_KEY[i]);}
  function fresh(){return {schema:SCHEMA,balanceCents:10000,meterCents:5100,roundNo:0,phase:'ready',round:null,history:[]};}
  function validate(s){
    if(!s||s.schema!==SCHEMA||!['ready','hold','settled'].includes(s.phase)||!Number.isSafeInteger(s.balanceCents)||s.balanceCents<0||!Number.isSafeInteger(s.meterCents)||s.meterCents<5100||!Number.isSafeInteger(s.roundNo)||s.roundNo<0||!Array.isArray(s.history))throw new Error('Demo save is invalid. Use Reset demo to start a new isolated bank.');
    const checkResult=(result,hand)=>{
      if(!result||result.category!==score(hand).category||result.name!==CATEGORIES[result.category]||result.grossCents!==PAYS[result.category]*100||!Number.isSafeInteger(result.bonusCents)||result.bonusCents<0||result.totalCents!==result.grossCents+result.bonusCents||result.netCents!==result.totalCents-100)throw new Error('Invalid saved settlement.');
    };
    if(s.history.length>12)throw new Error('Invalid saved history.');
    for(const h of s.history){if(!h||!Number.isSafeInteger(h.id)||h.id<1||h.id>s.roundNo)throw new Error('Invalid history entry.');assertHand(h.initial);assertHand(h.hand);checkResult(h.result,h.hand);}
    if(s.phase==='ready'&&(s.round!==null||s.roundNo!==0||s.history.length!==0))throw new Error('Invalid ready state.');
    if(s.phase!=='ready'){
      const r=s.round;if(!r||r.id!==s.roundNo)throw new Error('Missing saved round.');
      assertHand(r.initial);assertHand(r.hand);
      if(!r.settings||!['straight','geared'].includes(r.settings.wire)||!Number.isInteger(r.settings.knob)||r.settings.knob<0||r.settings.knob>50)throw new Error('Invalid saved settings.');
      if(!Array.isArray(r.trace)||r.trace.length<5||r.trace.length>10||r.trace.some(t=>!t||!Number.isInteger(t.slot)||t.slot<0||t.slot>4||t.j!==t.slot+1||!Number.isInteger(t.m)||t.m<42||t.m>51||!Number.isInteger(t.a)||gcd(t.a,t.m)!==1||!Number.isInteger(t.b)||t.b<0||t.b>=t.m||!Number.isInteger(t.d)||t.d<0||t.d>=t.m||t.e!==mod(t.a*t.d+t.b,t.m)||!BY_ID.has(t.card)))throw new Error('Invalid saved rotor record.');
      if(!Array.isArray(r.holds)||r.holds.length!==5||r.holds.some(x=>typeof x!=='boolean'))throw new Error('Invalid saved hold mask.');
      if(!Array.isArray(r.remaining)||new Set(r.remaining).size!==r.remaining.length||r.remaining.some(c=>!BY_ID.has(c)||r.initial.includes(c)||r.hand.includes(c)))throw new Error('Invalid saved inventory.');
      if(s.phase==='hold'&&(r.remaining.length!==46||r.hand.some((c,i)=>c!==r.initial[i])||r.settled))throw new Error('Invalid unsettled round.');
      if(!Number.isSafeInteger(r.pendingBonusCents)||r.pendingBonusCents<0||(!isKey(r.initial)&&r.pendingBonusCents!==0))throw new Error('Invalid saved award.');
      if(s.phase==='settled'){
        if(!r.settled||r.remaining.length!==46-r.hand.filter(c=>!r.initial.includes(c)).length)throw new Error('Invalid settled inventory.');
        checkResult(r.result,r.hand);if(r.result.bonusCents!==r.pendingBonusCents)throw new Error('Invalid saved bonus.');
      }
    }
    return s;
  }
  const clone=x=>JSON.parse(JSON.stringify(x));
  function deal(s,settings,random){
    validate(s);if(s.phase==='hold')throw new Error('Finish the current hand first.');if(s.balanceCents<100)throw new Error('The demo bank needs one point. Reset demo to practice again.');
    const n=clone(s);n.roundNo++;const d=draw(CARDS,[0,1,2,3,4],settings,random,n.roundNo);
    n.balanceCents-=100;n.meterCents++;
    const pending=isKey(d.cards)?n.meterCents:0;if(pending)n.meterCents=5100;
    n.round={id:n.roundNo,settings:clone(settings),initial:d.cards.slice(),hand:d.cards,remaining:d.remaining,trace:d.trace,holds:[false,false,false,false,false],pendingBonusCents:pending,settled:false};n.phase='hold';return validate(n);
  }
  function hold(s,i){validate(s);if(s.phase!=='hold'||!Number.isInteger(i)||i<0||i>4)throw new Error('Hold is not available.');const n=clone(s);n.round.holds[i]=!n.round.holds[i];return n;}
  function finish(s,redraw,random){
    validate(s);if(s.phase!=='hold')throw new Error('This hand has already been settled, or no hand is active.');
    const n=clone(s),r=n.round;
    if(redraw){const slots=[0,1,2,3,4].filter(i=>!r.holds[i]);const d=draw(r.remaining,slots,r.settings,random,n.roundNo+51);slots.forEach((i,k)=>r.hand[i]=d.cards[k]);r.remaining=d.remaining;r.trace.push(...d.trace);}
    const result=score(r.hand);r.result={...result,bonusCents:r.pendingBonusCents,totalCents:result.grossCents+r.pendingBonusCents,netCents:result.grossCents+r.pendingBonusCents-100};r.settled=true;n.phase='settled';n.balanceCents+=r.result.totalCents;
    n.history.unshift({id:r.id,initial:r.initial,hand:r.hand.slice(),holds:r.holds.slice(),result:r.result});n.history=n.history.slice(0,12);return validate(n);
  }
  function* combinations(pool,k,start=0,prefix=[]){if(k===0){yield prefix;return;}for(let i=start;i<=pool.length-k;i++)yield*combinations(pool,k-1,i+1,[...prefix,pool[i]]);}
  function drawOdds(initial,holds){
    assertHand(initial);if(!Array.isArray(holds)||holds.length!==5||holds.some(x=>typeof x!=='boolean'))throw new Error('Invalid hold mask.');
    const kept=initial.filter((c,i)=>holds[i]),pool=CARDS.filter(c=>!initial.includes(c)),k=5-kept.length;
    return {kept,k,total:choose(46,k),iterator:combinations(pool,k)};
  }
  g.P51Engine=Object.freeze({DATA,CARDS,BY_ID,ARCHIVE_KEY,CATEGORIES,PAYS,SCHEMA,mod,gcd,choose,randBelow,gear,draw,scoreFast,score,isKey,fresh,validate,deal,hold,finish,combinations,drawOdds});
  if(typeof module!=='undefined'&&module.exports)module.exports=g.P51Engine;
})(globalThis);
