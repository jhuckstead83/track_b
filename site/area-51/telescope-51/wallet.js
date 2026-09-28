import {atomic,spend} from '../assets/credits.js';
import {post} from '../assets/wallet-core.js';
function keyOf(branch,round){if(!['A','B'].includes(branch)||!Number.isInteger(round)||round<0||round>16)throw Error('Invalid Telescope position.');return branch+':'+round;}
export async function peekIdentity(branch,round,player){keyOf(branch,round);if(![0,1,2].includes(player))throw Error('Invalid player.');return spend({id:'telescope:v2:peek:'+branch+':'+round+':'+player,source:'telescope51',kind:'identity-reveal',amountCents:600});}
export async function settleTicket({branch,round,correct,reward,evidence}){
 const key=keyOf(branch,round);if(typeof correct!=='boolean'||![4,17,51,100].includes(reward))throw Error('Invalid ticket.');
 return atomic(s=>{s.apps.telescopeTickets||={};s.apps.telescopeExposed||={};if(s.apps.telescopeTickets[key]||s.apps.telescopeExposed[key])return {funded:false,payout:0,repeat:true};
  const funded=s.balanceCents>=100,payout=funded&&correct?reward:0,id='telescope:v2:'+key;
  post(s,{id:id+':entry',source:'telescope51',kind:funded?'ticket-stake':'study-entry',deltaCents:funded?-100:0,evidence},Date.now());
  if(payout)post(s,{id:id+':return',source:'telescope51',kind:'ticket-return',deltaCents:payout*100},Date.now());
  const result={funded,payout,repeat:false};s.apps.telescopeTickets[key]={...result,evidence};return result;
 });
}
export async function recordTwinExposure(branch,round){const key=keyOf(branch,round);return atomic(s=>{s.apps.telescopeExposed||={};s.apps.telescopeExposed[key]=true;});}
