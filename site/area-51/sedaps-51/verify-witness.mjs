const U=[6,...Array.from({length:44},(_,i)=>i+8)];
const endpoint=[U.concat([5,3,1]),[4,2,0],[]];
const branches={
  '00':[[0].concat(U,[5,3,1]),[2,4],[]],
  '01':[[0].concat(U,[5,3,1]),[4],[2]],
  '10':[[3].concat(U,[5]),[1,4,2,0],[]],
  '11':[[5].concat(U),[3,4,2,0],[1]],
};
const clone=s=>s.map(h=>h.slice());
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
function step(state){
  const h=clone(state),live=h.map((q,i)=>q.length?i:null).filter(i=>i!==null);
  if(live.length<2)return h;
  const draws={};for(const i of live)draws[i]=h[i].shift();
  const winner=live.reduce((a,b)=>draws[a]>draws[b]?a:b);
  const pot=[draws[winner]];
  for(let d=1;d<3;d++){const i=(winner+d)%3;if(Object.prototype.hasOwnProperty.call(draws,i))pot.push(draws[i]);}
  h[winner].push(...pot);return h;
}
if(endpoint.flat().length!==51||endpoint.flat().includes(7))throw Error('Endpoint deck mismatch');
for(const [bits,s] of Object.entries(branches)){
  if(s.flat().length!==51)throw Error(bits+' does not contain 51 cards');
  if(new Set(s.flat()).size!==51)throw Error(bits+' repeats an active address');
  if(s.flat().includes(7))throw Error(bits+' includes marker address 7');
  if(!same(step(s),endpoint))throw Error(bits+' does not replay to endpoint');
}
console.log('51 SEDAPS exact witness: PASS (4/4 branches replay to endpoint)');
