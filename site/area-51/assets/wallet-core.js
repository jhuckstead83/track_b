// All arithmetic is in integer hundredths of a jbit. No real-money value.
export const SCHEMA='cerebralgraphix.area51.wallet.v2';
export const POLICY=Object.freeze({opening:800,cap:800,interval:310000,reveal:600,recallReward:200,recallDailyCap:800});
const clone=x=>JSON.parse(JSON.stringify(x));
export function fresh(at){return {schema:SCHEMA,revision:0,balanceCents:POLICY.opening,recoveryCursorAt:at,receipts:{},entries:[{id:'opening:v2',source:'area51',kind:'opening',deltaCents:800,balanceCents:800,at}],apps:{},recallDay:'',recallPaid:0};}
export function validate(s){if(s?.schema!==SCHEMA||!Number.isSafeInteger(s.balanceCents)||s.balanceCents<0||!Number.isSafeInteger(s.recoveryCursorAt)||!Number.isSafeInteger(s.revision)||!Array.isArray(s.entries)||!s.receipts||!s.apps)throw Error('Saved jbit bank cannot be verified. No replacement balance was issued.');return s;}
export function migrate(old,at){
  if(!old)return fresh(at);
  const legacySchemas=['cerebralgraphix.area51.credits.v1','cerebralgraphix.area51.credit-ledger.v1','cerebralgraphix.area51.economy.v1'];
  const cents=Number.isSafeInteger(old.balanceCents)?old.balanceCents:(Number.isFinite(old.balance)&&old.balance>=0?Math.round(old.balance*100):NaN);
  if(!legacySchemas.includes(old.schema)||!Number.isSafeInteger(cents)||cents<0)throw Error('Previous bank cannot be verified. Its data has been retained.');
  const s=fresh(at);s.balanceCents=cents;s.entries=Array.isArray(old.entries)?clone(old.entries):[];s.receipts=clone(old.receipts||{});
  for(const e of s.entries)if(e.id&&!s.receipts[e.id])s.receipts[e.id]={id:e.id,deltaCents:e.deltaCents,source:e.source,kind:e.kind};
  const cursor=Number.isSafeInteger(old.recoveryCursorAt)?old.recoveryCursorAt:Number.isSafeInteger(old.nextRecoveryAt)?old.nextRecoveryAt-POLICY.interval:at;
  s.recoveryCursorAt=Math.max(0,cursor);s.migratedFrom=old.schema;return s;
}
export function accrue(s,at){
  if(!Number.isSafeInteger(at)||at<0)throw Error('Invalid wallet clock.');
  if(s.balanceCents>=POLICY.cap){s.recoveryCursorAt=Math.max(s.recoveryCursorAt,at);return 0;}
  const steps=Math.floor(Math.max(0,at-s.recoveryCursorAt)/POLICY.interval);if(!steps)return 0;
  const amount=Math.min(steps*100,POLICY.cap-s.balanceCents);s.balanceCents+=amount;
  s.recoveryCursorAt+=Math.min(steps,Math.ceil(amount/100))*POLICY.interval;
  if(s.balanceCents>=POLICY.cap)s.recoveryCursorAt=Math.max(s.recoveryCursorAt,at);
  s.entries.push({id:'timer:'+s.recoveryCursorAt,source:'timer',kind:'refill',deltaCents:amount,balanceCents:s.balanceCents,at});return amount;
}
export function post(s,tx,at){
  if(typeof tx.id!=='string'||!tx.id||tx.id.length>240||!Number.isSafeInteger(tx.deltaCents)||Math.abs(tx.deltaCents)>1e11||!tx.source||!tx.kind)throw Error('Invalid jbit transaction.');
  const old=s.receipts[tx.id];
  if(old){if(old.deltaCents!==tx.deltaCents||old.source!==tx.source||old.kind!==tx.kind)throw Error('Receipt reused with different terms.');return {applied:false,duplicate:true,entry:clone(old)};}
  const after=s.balanceCents+tx.deltaCents;if(after<0||!Number.isSafeInteger(after))throw Error('Not enough jbits.');
  if(s.balanceCents>=POLICY.cap&&after<POLICY.cap)s.recoveryCursorAt=Math.max(s.recoveryCursorAt,at);
  s.balanceCents=after;if(after>=POLICY.cap)s.recoveryCursorAt=Math.max(s.recoveryCursorAt,at);
  const entry={...clone(tx),balanceCents:after,at};s.receipts[tx.id]=entry;s.entries.push(entry);return {applied:true,duplicate:false,entry:clone(entry)};
}
export function recall(s,{id,correct,assisted,options=4,evidence={}},at){
  const key='recall:'+id,old=s.receipts[key];if(old)return {applied:false,duplicate:true,entry:clone(old)};
  if(typeof id!=='string'||!id||options!==4||typeof correct!=='boolean'||typeof assisted!=='boolean')throw Error('Invalid recall result.');
  const day=new Date(at).toISOString().slice(0,10);if(s.recallDay!==day){s.recallDay=day;s.recallPaid=0;}
  const amount=correct&&!assisted?Math.min(POLICY.recallReward,Math.max(0,POLICY.recallDailyCap-s.recallPaid)):0;
  const result=post(s,{id:key,source:'memory51',kind:'four-way-recall',deltaCents:amount,evidence:{...evidence,correct,assisted,options}},at);s.recallPaid+=amount;return result;
}
