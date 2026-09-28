/* Shared-jbit adapter for the unchanged R51-0.3 rule engine.
 * Caller runs this synchronous function inside the shared wallet transaction.
 * Engine balance is a working copy of the current wallet, never a second bank.
 */
import {post} from '../assets/wallet-core-v2-0b3.js';
export const ACCOUNT_SCHEMA = 'cerebralgraphix.prospect51.account.v1';
const clone = x => JSON.parse(JSON.stringify(x));
function conflict() { return Object.assign(Error('This hand changed in another tab. The saved hand has been reloaded; choose again.'), {code:'CONFLICT'}); }
export function account(w, E) {
  let r = w.apps.prospect51;
  if (!r) {
    const state = E.fresh(); state.balanceCents = w.balanceCents;
    r = {schema:ACCOUNT_SCHEMA, revision:1, state}; w.apps.prospect51 = r;
  }
  if (r.schema !== ACCOUNT_SCHEMA || !Number.isSafeInteger(r.revision) || r.revision < 1) throw Error('The saved Prospect hand cannot be verified. It has been retained.');
  E.validate(r.state);
  return {...clone(r), state:{...clone(r.state), balanceCents:w.balanceCents}};
}
export function updateAccount(w, request, E, now = Date.now()) {
  const current = account(w, E);
  const {kind, operationId, expectedRevision} = request;
  if (!['deal','hold','draw','bank'].includes(kind) || typeof operationId !== 'string' || !operationId || operationId.length > 100) throw Error('Invalid Prospect operation.');
  const terms = JSON.stringify({kind, slot:request.slot ?? null, settings:request.settings ?? null});
  if (current.lastOperationId === operationId) {
    if (current.lastTerms !== terms) throw Error('A saved operation was retried with different terms.');
    return current;
  }
  if (current.revision !== expectedRevision) throw conflict();
  let next;
  if (kind === 'deal') {
    next = E.deal(current.state, request.settings);
    post(w, {id:'prospect51:'+next.roundNo+':entry', source:'prospect51', kind:'entry', deltaCents:-100,
      evidence:{rule:'R51-0.3', initial:next.round.initial, settings:next.round.settings}}, now);
  } else if (kind === 'hold') next = E.hold(current.state, request.slot);
  else {
    next = E.finish(current.state, kind === 'draw');
    post(w, {id:'prospect51:'+next.roundNo+':settlement', source:'prospect51', kind:'settlement', deltaCents:next.round.result.totalCents,
      evidence:{rule:'R51-0.3', initial:next.round.initial, hand:next.round.hand, holds:next.round.holds, result:next.round.result}}, now);
  }
  if (next.balanceCents !== w.balanceCents) throw Error('Prospect hand and shared bank did not balance.');
  const record = {schema:ACCOUNT_SCHEMA, revision:current.revision+1, lastOperationId:operationId, lastTerms:terms, state:next};
  w.apps.prospect51 = record;
  return clone(record);
}
