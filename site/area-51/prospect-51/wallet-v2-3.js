import {atomic, ready, subscribeCredits, refreshCredits} from '../assets/credits-v2-0b3.js';
import {account, updateAccount} from './account-v2-3.js';
export {subscribeCredits, refreshCredits};
export async function readGame() {
  await ready;
  return atomic(w => account(w, globalThis.P51Engine));
}
export async function command(request) {
  await ready;
  return atomic(w => updateAccount(w, request, globalThis.P51Engine));
}
