import {SCHEMA,POLICY,fresh,migrate,validate,accrue,post,recall} from './wallet-core-v2-0b3.js';

export {POLICY};
export const CREDIT_STORAGE_KEY='cerebralgraphix.area51.credits.v1';
export const CREDIT_RULE=Object.freeze({startCents:800,recoveryCapCents:800,recoveryIntervalMs:POLICY.interval,passiveGeneratorEnabled:true});

const FALLBACK_STORAGE_KEY='cerebralgraphix.area51.wallet.v2.fallback';
const FINANCE_POSITIONS_KEY='cerebralgraphix.finance.positions.v1';

function financeHoldingsCents(){
  try{
    if(typeof localStorage==='undefined')return 0;
    const raw=JSON.parse(localStorage.getItem(FINANCE_POSITIONS_KEY)||'{}');
    if(!raw||typeof raw!=='object'||Array.isArray(raw))return 0;
    let total=0;
    for(const pos of Object.values(raw)){
      const n=Number(pos?.lastValueCents??pos?.stakeCents);
      if(!Number.isFinite(n)||n<=0)continue;
      total+=Math.max(0,Math.round(n));
      if(!Number.isSafeInteger(total)||total>1e11)return 1e11;
    }
    return total;
  }catch{return 0;}
}
const IDB_OPEN_TIMEOUT_MS=1000;
const subscribers=new Set();
const clone=value=>JSON.parse(JSON.stringify(value));
let cached=null,backendPromise,memoryState=null,localQueue=Promise.resolve(),channel;

try{channel=new BroadcastChannel('cg-area51-bank-v2');}catch{}

function load(raw,at){
  if(!raw)return {state:fresh(at),recovered:true};
  try{return {state:validate(raw),recovered:false};}
  catch{
    try{return {state:migrate(raw,at),recovered:true};}
    catch{throw Error('The saved jbit bank cannot be verified. Its data has been retained; no replacement balance was issued.');}
  }
}

function readJson(key){
  let raw;
  try{if(typeof localStorage==='undefined')return null;raw=localStorage.getItem(key);}
  catch{return null;}
  if(raw===null)return null;
  try{return JSON.parse(raw);}
  catch{throw Error('The saved jbit bank cannot be read. Its data has been retained.');}
}

function legacyInitial(at){
  const legacy=readJson(CREDIT_STORAGE_KEY);
  return legacy?load(legacy,at):{state:fresh(at),recovered:true};
}

function initial(at){
  const current=readJson(FALLBACK_STORAGE_KEY);
  if(current)return load(current,at);
  if(memoryState)return load(clone(memoryState),at);
  return legacyInitial(at);
}

function hasFallbackRecord(){
  if(memoryState)return true;
  try{return typeof localStorage!=='undefined'&&localStorage.getItem(FALLBACK_STORAGE_KEY)!==null;}
  catch{return false;}
}

function writeFallback(state){
  try{
    if(typeof localStorage==='undefined')throw Error('No persistent storage.');
    localStorage.setItem(FALLBACK_STORAGE_KEY,JSON.stringify(state));
  }catch{throw Error('This browser could not save the shared bank. No move was charged. Enable site storage to play.');}
  memoryState=clone(state);
}
function lockedFallback(work){
  if(!globalThis.navigator?.locks?.request)throw Error('This browser cannot safely update the shared bank while its database is unavailable. Please reopen the page with site storage enabled.');
  return navigator.locks.request('cg-area51-bank-fallback-v2',work);
}

function openIndexedDb(){
  return new Promise((resolve,reject)=>{
    if(typeof indexedDB==='undefined'){reject(Error('IndexedDB is unavailable.'));return;}
    let settled=false,request;
    const finish=(fn,value)=>{if(settled){if(fn===resolve)value?.close?.();return;}settled=true;clearTimeout(timer);fn(value);};
    const timer=setTimeout(()=>finish(reject,Error('IndexedDB did not open in time.')),IDB_OPEN_TIMEOUT_MS);
    try{request=indexedDB.open('cerebralgraphix-area51-v2',1);}catch(error){finish(reject,error);return;}
    request.onupgradeneeded=()=>{if(!request.result.objectStoreNames.contains('bank'))request.result.createObjectStore('bank');};
    request.onsuccess=()=>finish(resolve,request.result);
    request.onerror=()=>finish(reject,request.error||Error('The jbit bank could not be opened.'));
    request.onblocked=()=>finish(reject,Error('The jbit bank is blocked by another browser context.'));
  });
}

async function backend(){
  if(!backendPromise)backendPromise=(async()=>{
    if(hasFallbackRecord())return {kind:'fallback'};
    try{return {kind:'indexeddb',db:await openIndexedDb()};}
    catch{return {kind:'fallback'};}
  })();
  return backendPromise;
}

export function snapshotOf(state=cached){
  const holdingsCents=financeHoldingsCents();
  if(!state)return {schema:SCHEMA,balanceCents:0,balance:0,holdingsCents,ownedCents:holdingsCents,revision:0,sequence:0,ready:false,entries:[],recoveryCursorAt:Date.now(),activeLearningMs:0,recallPaid:0};
  return {schema:state.schema,balanceCents:state.balanceCents,balance:state.balanceCents/100,holdingsCents,ownedCents:state.balanceCents+holdingsCents,revision:state.revision,sequence:state.revision,ready:true,recoveryCursorAt:state.recoveryCursorAt,nextRecoveryAt:state.recoveryCursorAt+POLICY.interval,entries:clone(state.entries),activeLearningMs:0,recallPaid:state.recallPaid,now:Date.now()};
}

function publish(state,broadcast){
  cached=clone(state);
  const snapshot=snapshotOf();
  for(const fn of subscribers){try{fn(snapshot);}catch{}}
  if(broadcast)channel?.postMessage({revision:state.revision});
}

function idbAtomic(db,work){
  return new Promise((resolve,reject)=>{
    let tx,bucket,request,state,result,failure;
    try{tx=db.transaction('bank','readwrite');bucket=tx.objectStore('bank');request=bucket.get('main');}
    catch(error){reject(error);return;}
    request.onsuccess=()=>{
      try{
        state=(request.result?load(request.result,Date.now()):legacyInitial(Date.now())).state;
        accrue(state,Date.now(),financeHoldingsCents());
        result=work(state);
        if(result?.then)throw Error('Wallet transaction cannot await external work.');
        state.revision++;
        validate(state);
        bucket.put(state,'main');
      }catch(error){failure=error;tx.abort();}
    };
    request.onerror=()=>{failure=request.error||Error('The jbit bank could not be read.');tx.abort();};
    tx.oncomplete=()=>{publish(state,true);resolve({value:clone(result??null),snapshot:snapshotOf(state)});};
    tx.onabort=()=>reject(failure||tx.error||Error('Bank update interrupted. No replacement jbits were issued.'));
    tx.onerror=()=>{};
  });
}

function idbRefresh(db){
  return new Promise((resolve,reject)=>{
    let tx,bucket,request,state,changed=false,failure;
    try{tx=db.transaction('bank','readwrite');bucket=tx.objectStore('bank');request=bucket.get('main');}
    catch(error){reject(error);return;}
    request.onsuccess=()=>{
      try{
        const loaded=request.result?load(request.result,Date.now()):legacyInitial(Date.now());
        state=loaded.state;
        const before=state.balanceCents;
        accrue(state,Date.now(),financeHoldingsCents());
        changed=loaded.recovered||state.balanceCents!==before;
        if(changed){state.revision++;bucket.put(state,'main');}
      }catch(error){failure=error;tx.abort();}
    };
    request.onerror=()=>{failure=request.error||Error('The jbit bank could not be read.');tx.abort();};
    tx.oncomplete=()=>{publish(state,changed);resolve(snapshotOf(state));};
    tx.onabort=()=>reject(failure||tx.error||Error('The jbit bank could not be refreshed.'));
    tx.onerror=()=>{};
  });
}

function queueLocal(work){
  const next=localQueue.then(work,work);
  localQueue=next.catch(()=>{});
  return next;
}

function fallbackAtomic(work){
  return queueLocal(()=>lockedFallback(()=>{
    const state=initial(Date.now()).state;
    accrue(state,Date.now(),financeHoldingsCents());
    const result=work(state);
    if(result?.then)throw Error('Wallet transaction cannot await external work.');
    state.revision++;
    validate(state);
    writeFallback(state);
    publish(state,true);
    return {value:clone(result??null),snapshot:snapshotOf(state)};
  }));
}

function fallbackRefresh(){
  return queueLocal(()=>lockedFallback(()=>{
    const loaded=initial(Date.now()),state=loaded.state,before=state.balanceCents;
    accrue(state,Date.now(),financeHoldingsCents());
    const changed=loaded.recovered||state.balanceCents!==before;
    if(changed){state.revision++;validate(state);writeFallback(state);}
    publish(state,changed);
    return snapshotOf(state);
  }));
}

// The callback is synchronous. Wallet, receipt and game checkpoint commit together.
export async function atomic(work){
  const store=await backend();
  return store.kind==='indexeddb'?idbAtomic(store.db,work):fallbackAtomic(work);
}

export async function refreshCredits(){
  const store=await backend();
  return store.kind==='indexeddb'?idbRefresh(store.db):fallbackRefresh();
}

export function getCreditSnapshot(){return snapshotOf();}
export async function transact(tx){const result=await atomic(state=>post(state,tx,Date.now()));return {...result.value,snapshot:result.snapshot};}
export const spend=tx=>transact({...tx,deltaCents:-tx.amountCents});
export const award=tx=>transact({...tx,deltaCents:tx.amountCents});
export async function recordRecall(tx){const result=await atomic(state=>recall(state,tx,Date.now()));return {...result.value,snapshot:result.snapshot};}
export function subscribeCredits(fn){subscribers.add(fn);if(cached)fn(snapshotOf());return ()=>subscribers.delete(fn);}
export function formatCredits(cents){return (Number(cents)/100).toFixed(2).replace(/\.00$/,'').replace(/(\.\d)0$/,'$1');}
export function recoveryCountdown(snapshot=snapshotOf(),at=Date.now()){if(!snapshot.ready)return 'Opening bank…';const holdingsCents=financeHoldingsCents(),ownedCents=Number(snapshot.balanceCents||0)+holdingsCents;if(snapshot.balanceCents>=POLICY.cap)return 'Reserve full';if(ownedCents>=POLICY.cap)return 'Reserve covered by holdings';const seconds=Math.ceil(Math.max(0,POLICY.interval-(Math.max(0,at-snapshot.recoveryCursorAt)%POLICY.interval))/1000);return '+1 in '+Math.floor(seconds/60)+':'+String(seconds%60).padStart(2,'0');}

if(channel)channel.addEventListener('message',()=>refreshCredits().catch(()=>{}));
if(typeof addEventListener==='function')addEventListener('storage',event=>{if(event.key===FALLBACK_STORAGE_KEY||event.key===FINANCE_POSITIONS_KEY)refreshCredits().catch(()=>{});});
export const ready=refreshCredits();
ready.catch(()=>{});
export async function readWallet(){await refreshCredits();return clone(cached);}
