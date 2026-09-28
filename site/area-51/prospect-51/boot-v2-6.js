/* One versioned entrypoint owns startup. Old presentation code cannot bind new markup. */
const bankNode=document.getElementById('bank'),errorNode=document.getElementById('error');
try{
  const {ready,subscribeCredits,formatCredits}=await import('../assets/credits-v2-0b3.js');
  await ready;
  subscribeCredits(bank=>{bankNode.textContent=bank.ready?formatCredits(bank.balanceCents):'—';});
  // Keep the approved engine, dictionary and inline token renderer byte-for-byte intact.
  for(const source of ['./data.js','./engine.js','./tokens.js','./card-actions-v2-4.js'])await import(source);
  await import('./app-v2-6.js');
}catch(error){
  errorNode.hidden=false;
  errorNode.textContent='Prospect could not finish loading. '+(error.message||'Reload to fetch the current game files.')+' Your saved bank and hand have been retained.';
  document.getElementById('primary-move').disabled=true;
  const retry=document.getElementById('retry-start');retry.hidden=false;retry.onclick=()=>location.reload();
  document.getElementById('save-status').textContent='Game loading paused';
}
