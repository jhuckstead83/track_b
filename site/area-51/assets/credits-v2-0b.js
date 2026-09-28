import {SCHEMA,POLICY,fresh,migrate,validate,accrue,post,recall} from './wallet-core-v2-0b.js';
export {POLICY};
export const CREDIT_STORAGE_KEY='cerebralgraphix.area51.credits.v1';
export const CREDIT_RULE=Object.freeze({startCents:800,recoveryCapCents:800,recoveryIntervalMs:POLICY.interval,passiveGeneratorEnabled:true});
const subscribers=new Set(),clone=x=>JSON.parse(JSON.stringify(x));
let cached=null,dbPromise,channel;
try{channel=new BroadcastChannel('cg-area51-bank-v2');}catch{}
function open(){
  if(!dbPromise)dbPromise=new Promise((resolve,reject)=>{
    if(typeof indexedDB==='undefined'){reject(Error('Browser storage is unavailable. Jbits were not reset.'));return;}
    const r=indexedDB.open('cerebralgraphix-area51-v2',1);
    r.onupgradeneeded=()=>r.result.createObjectStore('bank');
    r.onsuccess=()=>resolve(r.result);r.onerror=()=>reject(r.error);
  });return dbPromise;
}
function initial(){
  const at=Date.now();let raw;
  try{raw=localStorage.getItem(CREDIT_STORAGE_KEY);}catch{return fresh(at);}
  if(!raw)return fresh(at);
  try{return migrate(JSON.parse(raw),at);}catch{return fresh(at);}
}
function load(raw,at){
  if(!raw)return {state:initial(),recovered:true};
  try{return {state:validate(raw),recovered:false};}
  catch{try{return {state:migrate(raw,at),recovered:true};}catch{return {state:fresh(at),recovered:true};}}
}
export function snapshotOf(s=cached){
  if(!s)return {schema:SCHEMA,balanceCents:0,balance:0,revision:0,sequence:0,ready:false,entries:[],recoveryCursorAt:Date.now(),activeLearningMs:0,recallPaid:0};
  return {schema:s.schema,balanceCents:s.balanceCents,balance:s.balanceCents/100,revision:s.revision,sequence:s.revision,ready:true,recoveryCursorAt:s.recoveryCursorAt,nextRecoveryAt:s.recoveryCursorAt+POLICY.interval,entries:clone(s.entries),activeLearningMs:0,recallPaid:s.recallPaid,now:Date.now()};
}
function publish(state,broadcast){cached=state;const snap=snapshotOf();for(const fn of subscribers){try{fn(snap);}catch{}}if(broadcast)channel?.postMessage({revision:state.revision});}
// The callback is synchronous. Wallet, receipt and game checkpoint commit together.
export async function atomic(work){
  const db=await open();return new Promise((resolve,reject)=>{
    const tx=db.transaction('bank','readwrite'),bucket=tx.objectStore('bank'),request=bucket.get('main');let state,result,failure;
    request.onsuccess=()=>{try{state=load(request.result,Date.now()).state;accrue(state,Date.now());result=work(state);if(result?.then)throw Error('Wallet transaction cannot await external work.');state.revision++;validate(state);bucket.put(state,'main');}catch(e){failure=e;tx.abort();}};
    tx.oncomplete=()=>{publish(state,true);resolve({value:clone(result??null),snapshot:snapshotOf(state)});};
    tx.onabort=()=>reject(failure||tx.error||Error('Bank update interrupted. No replacement jbits were issued.'));tx.onerror=()=>{};
  });
}
export async function refreshCredits(){
  const db=await open();return new Promise((resolve,reject)=>{
    const tx=db.transaction('bank','readwrite'),bucket=tx.objectStore('bank'),request=bucket.get('main');let state,changed=false,failure;
    request.onsuccess=()=>{try{const loaded=load(request.result,Date.now());state=loaded.state;const before=state.balanceCents;accrue(state,Date.now());changed=loaded.recovered||state.balanceCents!==before;if(changed){state.revision++;bucket.put(state,'main');}}catch(e){failure=e;tx.abort();}};
    tx.oncomplete=()=>{publish(state,changed);resolve(snapshotOf(state));};tx.onabort=()=>reject(failure||tx.error);tx.onerror=()=>{};
  });
}
export function getCreditSnapshot(){return snapshotOf();}
export async function transact(tx){const r=await atomic(s=>post(s,tx,Date.now()));return {...r.value,snapshot:r.snapshot};}
export const spend=tx=>transact({...tx,deltaCents:-tx.amountCents});
export const award=tx=>transact({...tx,deltaCents:tx.amountCents});
export async function recordRecall(tx){const r=await atomic(s=>recall(s,tx,Date.now()));return {...r.value,snapshot:r.snapshot};}
export function subscribeCredits(fn){subscribers.add(fn);if(cached)fn(snapshotOf());return ()=>subscribers.delete(fn);}
export function formatCredits(cents){return (Number(cents)/100).toFixed(2).replace(/\.00$/,'').replace(/(\.\d)0$/,'$1');}
export function recoveryCountdown(s=snapshotOf(),at=Date.now()){if(!s.ready)return 'Opening bank…';if(s.balanceCents>=800)return 'Reserve full';const seconds=Math.ceil(Math.max(0,POLICY.interval-(Math.max(0,at-s.recoveryCursorAt)%POLICY.interval))/1000);return '+1 in '+Math.floor(seconds/60)+':'+String(seconds%60).padStart(2,'0');}
if(channel)channel.addEventListener('message',()=>refreshCredits().catch(()=>{}));
export const ready=refreshCredits();ready.catch(()=>{});
export async function readWallet(){await refreshCredits();return clone(cached);}
