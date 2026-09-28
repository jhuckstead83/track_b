'use strict';
(() => {
  const apiReady=import('../assets/credits.js');let snap=null;
  const conflict=()=>Object.assign(Error('Another tab updated this table.'),{code:'CONFLICT'});
  const replay=data=>BJ51.Engine.replay(data);
  function sync(wallet,record){
    const e=replay(record.state.engine),difference=Math.round(wallet.balanceCents-e.bank*100)/100;
    if(difference){e.reconcile(difference,'wallet-sync:'+wallet.revision);record={...record,revision:record.revision+1,state:{...record.state,engine:e.snapshot(),lastAccrualAt:Date.now()}};wallet.apps.blackjack=record;}
    return record;
  }
  globalThis.CGBlackjack51Store={
    kind:'area51-shared',now:()=>Date.now(),walletSnapshot:()=>snap,
    async read(){
      const api=await apiReady,wallet=await api.readWallet();snap=api.snapshotOf(wallet);
      const record=wallet.apps.blackjack;if(!record)return {revision:0,state:null,initialBalance:wallet.balanceCents/100};
      if(Math.round(record.state.engine.bank*100)===wallet.balanceCents)return record;
      const result=await api.atomic(w=>sync(w,w.apps.blackjack));snap=result.snapshot;return result.value;
    },
    async compareAndSwap({expectedRevision,operationId,state}){
      const api=await apiReady;
      const result=await api.atomic(wallet=>{
        const current=wallet.apps.blackjack;
        if(current?.lastOperationId===operationId)return sync(wallet,current);
        if((current?.revision||0)!==expectedRevision)throw conflict();
        const proposed=replay(state.engine),previous=current?replay(current.state.engine):null;
        if(previous){
          if(proposed.openingBalance!==previous.openingBalance||JSON.stringify(proposed.commands.slice(0,previous.commands.length))!==JSON.stringify(previous.commands))throw Error('The game checkpoint does not extend the saved hand.');
        }else if(proposed.commands.length||Math.round(proposed.openingBalance*100)!==wallet.balanceCents)throw conflict();
        for(const event of proposed.events.slice(previous?.events.length||proposed.events.length)){
          let amount=event.type==='stake'?-event.stake:event.type==='settlement'?event.payout:event.type==='site-credit'?event.credits:0;
          if(event.type==='refill')throw Error('Only the shared bank can issue timed jbits.');
          if(amount){const cents=Math.round(amount*100);if(!Number.isSafeInteger(cents))throw Error('Invalid jbit amount.');
            // Same transaction as the game checkpoint; no separate wallet/hand write.
            const id='blackjack:'+operationId+':'+event.seq,old=wallet.receipts[id];
            if(old)throw Error('Duplicate blackjack event.');
            if(wallet.balanceCents+cents<0)throw Error('Not enough jbits.');
            const before=wallet.balanceCents;wallet.balanceCents+=cents;
            if(before>=800||wallet.balanceCents>=800)wallet.recoveryCursorAt=Math.max(wallet.recoveryCursorAt,Date.now());
            const row={id,source:'blackjack51',kind:event.type,deltaCents:cents,balanceCents:wallet.balanceCents,at:Date.now(),event:event.seq};wallet.receipts[id]=row;wallet.entries.push(row);
          }
        }
        const delta=Math.round(wallet.balanceCents-proposed.bank*100)/100;if(delta)proposed.reconcile(delta,'wallet-sync:'+(wallet.revision+1));
        const record={revision:expectedRevision+1,lastOperationId:operationId,state:{schema:'cg-blackjack51-bank-v1',lastAccrualAt:Date.now(),engine:proposed.snapshot()}};
        wallet.apps.blackjack=record;return record;
      });snap=result.snapshot;return result.value;
    }
  };
  globalThis.CGBlackjack51Memory={async open(){
    const popup=window.open('../memory-51/?return=blackjack51','cg-memory51','popup=yes,width=1040,height=860,resizable=yes,scrollbars=yes');
    if(!popup){location.href='../memory-51/?return=blackjack51';return;}
    await new Promise(resolve=>{const timer=setInterval(()=>{if(popup.closed){clearInterval(timer);resolve();}},350);});
  }};
})();
