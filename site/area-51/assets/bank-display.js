import {ready,refreshCredits,subscribeCredits,formatCredits,recoveryCountdown} from './credits.js';
function render(s){for(const el of document.querySelectorAll('[data-play-bits]'))el.textContent=s.ready?formatCredits(s.balanceCents):'—';for(const el of document.querySelectorAll('[data-bank-clock]'))el.textContent=recoveryCountdown(s);}
subscribeCredits(render);ready.catch(e=>{for(const el of document.querySelectorAll('[data-bank-clock]'))el.textContent=e.message;});
setInterval(()=>refreshCredits().catch(()=>{}),1000);
