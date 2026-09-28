import {ready,getCreditSnapshot,subscribeCredits,formatCredits} from '../assets/credits.js';
import {peekIdentity,settleTicket,recordTwinExposure} from './wallet.js';
await ready;

  (function(){
    'use strict';

    var VERSION='2.0-table-v0.1-rule';
    let walletBusy=false;
    var RANKS=['A','2','3','4','5','6','7','8','9','10','J','Q','K'];
    var SUITS=['S','H','D','C'];
    var SUIT_GLYPH={S:'♠',H:'♥',D:'♦',C:'♣'};
    var DECK_A=('AS AH AD AC 2S 2H 2D 3S 3H 3D 3C 4S 4H 4D 4C 5S 5H 5D 5C 6S 6H 6D 6C 7S 7H 7D 7C 8S 8H 8D 8C 9S 9H 9D 9C QD KH 10H KD QH QS JS 10C JC QC KC 10S JD JH KS 10D').split(' ');
    var DECK_B=DECK_A.slice();
    DECK_B[49]=DECK_A[50];
    DECK_B[50]=DECK_A[49];
    var DEPTHS=[
      {id:'value',letter:'V',label:'Value',reward:4,count:15222,fn:blackjackValue},
      {id:'rank',letter:'R',label:'Rank',reward:17,count:3760,fn:naturalRank},
      {id:'color',letter:'C',label:'Color',reward:51,count:1220,fn:colorSign},
      {id:'suit',letter:'S',label:'Suit',reward:100,count:623,fn:suitBit}
    ];
    var state;
    var peekTimeouts=[null,null,null];

    var els={
      statusline:document.getElementById('statusline'),
      roundMetric:document.getElementById('roundMetric'),
      balanceMetric:document.getElementById('balanceMetric'),
      branchA:document.getElementById('branchA'),
      branchB:document.getElementById('branchB'),
      restartButton:document.getElementById('restartButton'),
      receiptButton:document.getElementById('receiptButton'),
      ruleWord:document.getElementById('ruleWord'),
      wordNote:document.getElementById('wordNote'),
      depthGrid:document.getElementById('depthGrid'),
      playerTable:document.getElementById('playerTable'),
      resultBox:document.getElementById('resultBox'),
      ledgerRows:document.getElementById('ledgerRows'),
      fiberRail:document.getElementById('fiberRail'),
      twinPanel:document.getElementById('twinPanel')
    };

    function rankName(card){return card.slice(0,-1)}
    function suitName(card){return card.slice(-1)}
    function naturalRank(card){return RANKS.indexOf(rankName(card))+1}
    function blackjackValue(card){
      var r=rankName(card);
      return (r==='10'||r==='J'||r==='Q'||r==='K')?10:naturalRank(card);
    }
    function colorSign(card){return (suitName(card)==='H'||suitName(card)==='D')?1:-1}
    function suitBit(card){return (suitName(card)==='D'||suitName(card)==='C')?1:0}
    function isRed(card){return colorSign(card)===1}
    function displayCard(card){return rankName(card)+SUIT_GLYPH[suitName(card)]}
    function activeDeck(){return state.branch==='A'?DECK_A:DECK_B}
    function otherDeck(){return state.branch==='A'?DECK_B:DECK_A}
    function roundCards(deck,round){return deck.slice(round*3,round*3+3)}
    function gcd(a,b){while(b){var t=a%b;a=b;b=t}return a}
    function fraction(n,d){
      if(n===0)return '0';
      var g=gcd(Math.abs(n),Math.abs(d));
      return (n/g)+'/'+(d/g);
    }
    function reciprocal(n){return '1/'+n}
    function escapeText(s){
      return String(s).replace(/[&<>"']/g,function(ch){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]});
    }

    function evaluate(cards){
      var leaders=[0,1,2];
      var trace=[];
      for(var d=0;d<DEPTHS.length;d++){
        var before=leaders.slice();
        var values=cards.map(DEPTHS[d].fn);
        var max=Math.max.apply(null,before.map(function(i){return values[i]}));
        leaders=before.filter(function(i){return values[i]===max});
        var numerator=before.length-leaders.length;
        var denominator=before.length*leaders.length;
        trace.push({
          depth:d,
          id:DEPTHS[d].id,
          letter:DEPTHS[d].letter,
          label:DEPTHS[d].label,
          values:values,
          before:before,
          after:leaders.slice(),
          reciprocalBefore:reciprocal(before.length),
          reciprocalAfter:reciprocal(leaders.length),
          delta:fraction(numerator,denominator)
        });
        if(leaders.length===1){
          return {depth:d,letter:DEPTHS[d].letter,winner:leaders[0],trace:trace,cards:cards.slice()};
        }
      }
      throw new Error('Suit identity did not resolve distinct cards.');
    }

    function newState(branch){
      return {
        branch:branch||'A',
        round:0,
        balance:getCreditSnapshot().balanceCents/100,
        selectedDepth:null,
        selectedPlayer:null,
        peeked:[false,false,false],
        peeking:[false,false,false],
        resolving:false,
        settled:false,
        started:false,
        funded:false,
        word:[],
        ledger:[],
        stage:-1,
        candidates:[0,1,2],
        result:null,
        twinOpened:false,
        rounds:[]
      };
    }

    function clearPeekTimers(){
      peekTimeouts.forEach(function(id,i){if(id){clearTimeout(id);peekTimeouts[i]=null}});
    }

    function reset(branch){
      if(walletBusy||state?.resolving)return;
      clearPeekTimers();
      state=newState(branch||state&&state.branch||'A');
      els.twinPanel.hidden=true;
      els.twinPanel.innerHTML='';
      renderAll();
    }

    function renderAll(){
      renderHeader();
      renderDepths();
      renderWord();
      renderPlayers();
      renderLedger();
      renderFiber();
      renderResult();
    }

    function renderHeader(){
      els.roundMetric.textContent=(state.round+1)+' / 17';
      els.balanceMetric.textContent=String(state.balance);
      els.branchA.setAttribute('aria-pressed',String(state.branch==='A'));
      els.branchB.setAttribute('aria-pressed',String(state.branch==='B'));
      els.branchA.disabled=state.started;
      els.branchB.disabled=state.started;
      els.restartButton.disabled=walletBusy||state.resolving;
      if(state.resolving)els.statusline.textContent='Round '+(state.round+1)+' · opening the rule chain';
      else if(state.settled)els.statusline.textContent='Round '+(state.round+1)+' settled · '+state.result.letter+' resolves for P'+(state.result.winner+1);
      else els.statusline.textContent='Round '+(state.round+1)+' of 17 · choose a rule depth and a player';
    }

    function renderDepths(){
      els.depthGrid.innerHTML='';
      DEPTHS.forEach(function(depth,index){
        var button=document.createElement('button');
        button.type='button';
        button.className='depth-button';
        button.setAttribute('aria-pressed',String(state.selectedDepth===index));
        button.disabled=walletBusy||state.resolving||state.settled;
        button.innerHTML='<strong>'+depth.letter+' · '+depth.label+'</strong><span>'+depth.count.toLocaleString()+' triples · pays '+depth.reward+'</span>';
        button.addEventListener('click',function(){
          state.selectedDepth=index;
          renderDepths();
          renderPlayers();
          renderResult();
        });
        els.depthGrid.appendChild(button);
      });
    }

    function renderWord(){
      els.ruleWord.innerHTML='';
      var groups=[4,4,4,5];
      var cursor=0;
      groups.forEach(function(size){
        var group=document.createElement('div');
        group.className='word-group';
        for(var j=0;j<size;j++){
          var index=cursor+j;
          var cell=document.createElement('span');
          cell.className='letter';
          if(index<state.word.length){cell.classList.add('filled');cell.textContent=state.word[index]}
          else{cell.textContent='·'}
          if(index===state.round&&!state.settled)cell.classList.add('current');
          cell.setAttribute('aria-label','Round '+(index+1)+(index<state.word.length?': '+state.word[index]:': unread'));
          group.appendChild(cell);
        }
        cursor+=size;
        els.ruleWord.appendChild(group);
      });
      if(state.word.length===17)els.wordNote.textContent='Complete finite word · middle echo SSCV × 2 · no periodic-tail claim.';
      else if(state.word.length>=12&&state.word.slice(4,8).join('')===state.word.slice(8,12).join(''))els.wordNote.textContent='Finite echo found: rounds 5–8 repeat at 9–12. No periodic-tail claim.';
      else els.wordNote.textContent='The unread tail stays hidden.';
    }

    function cardStageContent(card,player){
      if(state.peeking[player]||state.settled){
        return {stage:state.peeking[player]?'Paid peek':'Full identity',main:displayCard(card),sub:card==='3H'?'Lucky sentinel · unchanged':'One of 51 active identities',red:isRed(card)};
      }
      if(state.resolving&&state.stage>=0){
        if(state.stage===0)return {stage:'Value',main:String(blackjackValue(card)),sub:'10/J/Q/K share 10',red:false};
        if(state.stage===1)return {stage:'Natural rank',main:rankName(card),sub:'A=1 through K=13',red:false};
        if(state.stage===2)return {stage:'Color sign',main:colorSign(card)>0?'+1':'−1',sub:colorSign(card)>0?'Red':'Black',red:isRed(card)};
        return {stage:'Suit identity',main:SUIT_GLYPH[suitName(card)],sub:suitName(card)==='D'||suitName(card)==='C'?'High within color':'Low within color',red:isRed(card)};
      }
      return {stage:'Hidden identity',main:'?',sub:'one of 51 · identity hidden',red:false};
    }

    function renderPlayers(){
      var cards=roundCards(activeDeck(),state.round);
      els.playerTable.innerHTML='';
      cards.forEach(function(card,player){
        var panel=document.createElement('section');
        panel.className='player';
        if(state.selectedPlayer===player)panel.classList.add('selected');
        if(state.resolving){
          if(state.candidates.indexOf(player)>=0)panel.classList.add('leader');
          else panel.classList.add('eliminated');
        }
        if(state.settled&&state.result.winner===player)panel.classList.add('winner');

        var head=document.createElement('div');
        head.className='player-head';
        head.innerHTML='<b>Player '+(player+1)+'</b>';
        var choose=document.createElement('button');
        choose.type='button';
        choose.className='choose-player';
        choose.textContent=state.selectedPlayer===player?'Winner selected':'Choose winner';
        choose.setAttribute('aria-pressed',String(state.selectedPlayer===player));
        choose.disabled=walletBusy||state.resolving||state.settled;
        choose.addEventListener('click',function(){
          state.selectedPlayer=player;
          renderPlayers();
          renderResult();
        });
        head.appendChild(choose);
        panel.appendChild(head);

        var content=cardStageContent(card,player);
        var visual=document.createElement('div');
        visual.className='card'+(content.red?' red':'');
        visual.setAttribute('aria-label','Player '+(player+1)+' card: '+(state.peeking[player]||state.settled?displayCard(card):content.stage+' '+content.main));
        visual.innerHTML='<span class="stage">'+escapeText(content.stage)+'</span><span class="main">'+escapeText(content.main)+'</span><span class="sub">'+escapeText(content.sub)+'</span>';
        if((state.peeking[player]||state.settled)&&card==='3H'){
          var lucky=document.createElement('span');lucky.className='lucky';lucky.textContent='lucky 3♥';visual.appendChild(lucky);
        }
        panel.appendChild(visual);

        var peek=document.createElement('button');
        peek.type='button';
        peek.className='peek';
        peek.textContent=state.peeked[player]?'Peek spent':(state.peeking[player]?'Remember it…':'Peek 1.6s · 6 jbits');
        peek.disabled=state.peeked[player]||walletBusy||state.resolving||state.settled||state.balance<6;
        peek.addEventListener('click',function(){peekCard(player)});
        panel.appendChild(peek);

        var account=document.createElement('div');
        account.className='player-account';
        account.innerHTML='<span>'+((walletBusy||state.resolving||state.settled)?(state.candidates.indexOf(player)>=0||state.result&&state.result.winner===player?'leader':'released'):'candidate')+'</span><span>'+(state.peeked[player]?'peek used':'unseen')+'</span>';
        panel.appendChild(account);

        var slot=document.createElement('div');
        slot.className='action-slot';
        if(state.selectedPlayer===player&&!state.resolving&&!state.settled){
          var lock=document.createElement('button');
          lock.type='button';lock.className='primary';
          if(state.selectedDepth===null){lock.textContent='Choose a rule depth';lock.disabled=true}
          else{
            var funded=state.balance>0;
            lock.textContent=(funded?'Lock 1 jbit':'Lock study ticket')+' · P'+(player+1)+' / '+DEPTHS[state.selectedDepth].letter;
            lock.disabled=false;
          }
          lock.addEventListener('click',function(){settleRound(false)});
          slot.appendChild(lock);
        }
        panel.appendChild(slot);
        els.playerTable.appendChild(panel);
      });
    }

    async function peekCard(player){
      if(state.peeked[player]||state.balance<6||walletBusy||state.resolving||state.settled)return;
      walletBusy=true;renderAll();
      try{const paid=await peekIdentity(state.branch,state.round,player);state.balance=paid.snapshot.balanceCents/100;}catch(error){els.resultBox.textContent=error.message;return;}finally{walletBusy=false;renderPlayers();}
      state.peeked[player]=true;
      state.peeking[player]=true;
      renderAll();
      peekTimeouts[player]=setTimeout(function(){
        state.peeking[player]=false;
        peekTimeouts[player]=null;
        renderPlayers();
        renderHeader();
      },1600);
    }

    function renderLedger(){
      if(!state.ledger.length){
        els.ledgerRows.innerHTML='<p class="micro">The ledger begins at three candidates: 1/3. Rule contributions telescope to 1, for total change 2/3.</p>';
        return;
      }
      els.ledgerRows.innerHTML='';
      state.ledger.forEach(function(row){
        var div=document.createElement('div');
        div.className='ledger-row';
        div.innerHTML='<b>'+row.letter+' · '+row.label+'</b><span>'+row.before.length+' → '+row.after.length+' candidates</span><span>'+row.reciprocalBefore+' → '+row.reciprocalAfter+' · Δ '+row.delta+'</span>';
        els.ledgerRows.appendChild(div);
      });
      if(state.settled){
        var total=document.createElement('p');
        total.className='micro';
        total.innerHTML='<strong>Telescoped total:</strong> 1 − 1/3 = 2/3. This is reciprocal ambiguity accounting, not an empirical probability.';
        els.ledgerRows.appendChild(total);
      }
    }

    function fiberSizes(card){
      return [
        51,
        DECK_A.filter(function(c){return blackjackValue(c)===blackjackValue(card)}).length,
        DECK_A.filter(function(c){return naturalRank(c)===naturalRank(card)}).length,
        DECK_A.filter(function(c){return naturalRank(c)===naturalRank(card)&&colorSign(c)===colorSign(card)}).length,
        1
      ];
    }

    function renderFiber(){
      if(!state.settled||!state.result){
        els.fiberRail.innerHTML='<p class="micro">Revealed after settlement. This is reciprocal fiber size under the uniform active-card convention, not entropy.</p>';
        return;
      }
      var card=state.result.cards[state.result.winner];
      var sizes=fiberSizes(card);
      var labels=['active','value','rank','color','identity'];
      var html='<p><strong>'+escapeText(displayCard(card))+'</strong> · winning identity</p><div class="fiber-rail">';
      sizes.forEach(function(n,i){
        if(i)html+='<span class="fiber-arrow" aria-hidden="true">→</span>';
        html+='<span class="fiber-node">'+reciprocal(n)+'</span>';
      });
      html+='</div><p class="micro">'+labels.map(function(label,i){return label+' '+reciprocal(sizes[i])}).join(' · ')+'</p>';
      els.fiberRail.innerHTML=html;
    }

    function renderResult(){
      if(state.resolving){
        var depth=state.stage>=0?DEPTHS[state.stage].label:'first rule';
        els.resultBox.innerHTML='<strong>Opening '+escapeText(depth)+'…</strong><p>Only tied leaders continue to the next rule.</p>';
        return;
      }
      if(state.settled&&state.result){
        var rec=state.rounds[state.round];
        var correct=rec.correct;
        var funding=rec.funded?'Funded ticket':'Study ticket';
        var headline=state.result.letter+' · '+DEPTHS[state.result.depth].label+' resolves for P'+(state.result.winner+1);
        var body=funding+'. Prediction: P'+(rec.predictedPlayer+1)+' / '+DEPTHS[rec.predictedDepth].letter+'. '+(correct?(rec.funded?'Correct · +'+rec.payout+' gross jbits.':'Correct · no payout on a study ticket.'):'No payout.')+' Balance '+state.balance+'.';
        var buttons='<div class="after-actions"><button type="button" class="quiet" id="twinButton">'+(state.twinOpened?'Twin opened':'Open adjacent twin')+'</button>';
        if(state.round<16)buttons+='<button type="button" class="next-button" id="nextButton">Next round →</button>';
        else buttons+='<button type="button" class="next-button" id="completeButton">Read the complete word</button>';
        buttons+='</div>';
        els.resultBox.innerHTML='<strong>'+escapeText(headline)+'</strong><p>'+escapeText(body)+'</p>'+buttons;
        var twinButton=document.getElementById('twinButton');
        twinButton.disabled=state.twinOpened;
        twinButton.addEventListener('click',openTwin);
        var next=document.getElementById('nextButton');
        if(next)next.addEventListener('click',nextRound);
        var complete=document.getElementById('completeButton');
        if(complete)complete.addEventListener('click',function(){
          els.wordNote.textContent='Complete finite word · middle echo SSCV × 2 · no periodic-tail claim.';
          els.ruleWord.scrollIntoView({behavior:'smooth',block:'center'});
        });
        return;
      }
      var selectedDepth=state.selectedDepth===null?'no depth':DEPTHS[state.selectedDepth].label;
      var selectedPlayer=state.selectedPlayer===null?'no player':'P'+(state.selectedPlayer+1);
      els.resultBox.innerHTML='<strong>Ticket: '+escapeText(selectedDepth)+' / '+escapeText(selectedPlayer)+'</strong><p>Peeks cost 6 jbits. Select both fields; the lock button moves under your predicted winner.</p>';
    }

    function wait(ms){return new Promise(function(resolve){setTimeout(resolve,ms)})}
    function motionDelay(){
      return window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches?20:520;
    }

    async function settleRound(instant){
      if(walletBusy||state.resolving||state.settled||state.selectedDepth===null||state.selectedPlayer===null)return;
      clearPeekTimers();
      state.peeking=[false,false,false];
      state.started=true;
      walletBusy=true;renderAll();
      var outcome=evaluate(roundCards(activeDeck(),state.round)),settlement;
      try{const paid=await settleTicket({branch:state.branch,round:state.round,correct:state.selectedDepth===outcome.depth&&state.selectedPlayer===outcome.winner,reward:DEPTHS[outcome.depth].reward,evidence:{depth:state.selectedDepth,player:state.selectedPlayer,peeked:state.peeked.slice()}});settlement=paid.value;state.funded=settlement.funded;state.balance=paid.snapshot.balanceCents/100;}
      catch(error){walletBusy=false;els.resultBox.textContent=error.message;renderPlayers();return;}
      walletBusy=false;
      state.resolving=true;
      state.stage=-1;
      state.ledger=[];
      state.candidates=[0,1,2];
      var cards=roundCards(activeDeck(),state.round);
      var result=evaluate(cards);
      renderAll();
      for(var i=0;i<result.trace.length;i++){
        state.stage=i;
        state.ledger.push(result.trace[i]);
        state.candidates=result.trace[i].after.slice();
        renderAll();
        if(!instant)await wait(motionDelay());
      }
      state.resolving=false;
      state.settled=true;
      state.result=result;
      var correct=state.selectedDepth===result.depth&&state.selectedPlayer===result.winner;
      var payout=settlement.payout;
      state.word.push(result.letter);
      state.rounds[state.round]={
        round:state.round+1,
        branch:state.branch,
        cards:cards.slice(),
        predictedDepth:state.selectedDepth,
        predictedDepthLetter:DEPTHS[state.selectedDepth].letter,
        predictedPlayer:state.selectedPlayer,
        peekedPlayers:state.peeked.map(function(v,i){return v?i+1:null}).filter(Boolean),
        funded:state.funded,
        stake:state.funded?1:0,
        actualDepth:result.depth,
        actualDepthLetter:result.letter,
        actualPlayer:result.winner,
        trace:result.trace,
        correct:correct,
        payout:payout,
        endingBalance:state.balance,
        twinOpened:false
      };
      renderAll();
    }

    async function openTwin(){
      if(!state.settled||state.twinOpened)return;
      if(walletBusy)return;walletBusy=true;
      try{await recordTwinExposure(state.branch==='A'?'B':'A',state.round);}catch(error){els.resultBox.textContent=error.message;return;}finally{walletBusy=false;}
      state.twinOpened=true;
      var cards=roundCards(otherDeck(),state.round);
      var twin=evaluate(cards);
      var sameDepth=twin.depth===state.result.depth;
      var sameWinner=twin.winner===state.result.winner;
      state.rounds[state.round].twinOpened=true;
      state.rounds[state.round].twin={
        branch:state.branch==='A'?'B':'A',
        cards:cards.slice(),
        depth:twin.depth,
        depthLetter:twin.letter,
        winner:twin.winner,
        sameDepth:sameDepth,
        sameWinner:sameWinner
      };
      var currentBranch=state.branch;
      var otherBranch=currentBranch==='A'?'B':'A';
      var note=sameDepth&&sameWinner?'Same depth and winner.':(sameDepth?'Same '+twin.letter+' depth; winner moves from P'+(state.result.winner+1)+' to P'+(twin.winner+1)+'.':'Resolution depth changes from '+state.result.letter+' to '+twin.letter+'.');
      els.twinPanel.innerHTML='<strong>Adjacent twin · branch '+otherBranch+'</strong><div class="twin-cards">'+cards.map(function(c,i){return '<span class="twin-card">P'+(i+1)+' '+escapeText(displayCard(c))+'</span>'}).join('')+'</div><p>'+escapeText(note)+'</p>';
      els.twinPanel.hidden=false;
      renderResult();
    }

    function nextRound(){
      if(walletBusy||state.resolving)return;
      if(!state.settled||state.round>=16)return;
      state.round+=1;
      state.selectedDepth=null;
      state.selectedPlayer=null;
      state.peeked=[false,false,false];
      state.peeking=[false,false,false];
      state.resolving=false;
      state.settled=false;
      state.funded=false;
      state.ledger=[];
      state.stage=-1;
      state.candidates=[0,1,2];
      state.result=null;
      state.twinOpened=false;
      els.twinPanel.hidden=true;
      els.twinPanel.innerHTML='';
      renderAll();
      document.getElementById('game-title').scrollIntoView({behavior:'smooth',block:'start'});
    }

    function saveReceipt(){
      var receipt={
        schema:'cerebral-graphix.telescope-51.local-receipt.v1',
        version:VERSION,
        title:'Telescope 51',
        author:'Jeffery Lyn Huckstead',
        based_on:{title:'The Line Game | Surprise Is Not Meaning',version:'7.2',doi:'10.5281/zenodo.22851517'},
        collected:false,
        collection_statement:'Generated locally. Nothing was transmitted by this page.',
        design_status:'Post-publication informed design; not a blind test.',
        branch:state.branch,
        active_deck_disclosure:state.word.length===17?'complete_after_walk':'withheld_until_walk_complete',
        exact_active_deck:state.word.length===17?activeDeck().slice():null,
        marker:'2C',
        rules:DEPTHS.map(function(d){return {letter:d.letter,label:d.label,reference_triples:d.count,draft_reward:d.reward}}),
        bank_unit:'jbit', starting_bank:'shared wallet; no per-walk grant',
        rounds:state.rounds.filter(Boolean),
        resolution_word:state.word.join(''),
        current_balance:state.balance
      };
      var blob=new Blob([JSON.stringify(receipt,null,2)+'\n'],{type:'application/json'});
      var url=URL.createObjectURL(blob);
      var a=document.createElement('a');
      a.href=url;a.download='Telescope_51_Local_Receipt.json';document.body.appendChild(a);a.click();a.remove();
      setTimeout(function(){URL.revokeObjectURL(url)},1000);
    }

    function init(){
      if(DECK_A.length!==51||new Set(DECK_A).size!==51)throw new Error('Invalid active deck.');
      if(DECK_A[49]!=='KS'||DECK_A[50]!=='10D'||DECK_B[49]!=='10D'||DECK_B[50]!=='KS')throw new Error('Adjacent pair mismatch.');
      els.branchA.addEventListener('click',function(){if(!state.started)reset('A')});
      els.branchB.addEventListener('click',function(){if(!state.started)reset('B')});
      els.restartButton.addEventListener('click',function(){reset(state.branch)});
      els.receiptButton.addEventListener('click',saveReceipt);
      reset('A');
    }

    window.__telescope51={
      version:VERSION,
      decks:{A:DECK_A.slice(),B:DECK_B.slice()},
      depths:DEPTHS.map(function(d){return {id:d.id,letter:d.letter,label:d.label,reward:d.reward,count:d.count}}),
      evaluate:function(cards){return evaluate(cards.slice())},
      exactWord:function(branch){
        var deck=branch==='B'?DECK_B:DECK_A;
        var out=[];
        for(var i=0;i<17;i++)out.push(evaluate(roundCards(deck,i)).letter);
        return out.join('');
      },
      exactWinners:function(branch){
        var deck=branch==='B'?DECK_B:DECK_A;
        var out=[];
        for(var i=0;i<17;i++)out.push(evaluate(roundCards(deck,i)).winner+1);
        return out;
      },
      fiberSizes:fiberSizes,
      getState:function(){return JSON.parse(JSON.stringify(state))},
      select:function(depth,player){state.selectedDepth=depth;state.selectedPlayer=player;renderAll()},
      settleInstant:function(){return settleRound(true)},
      next:nextRound,
      openTwin:openTwin,
      reset:reset
    };

    init();
    subscribeCredits(s=>{state.balance=s.balanceCents/100;renderHeader();if(!state.resolving&&!walletBusy)renderPlayers();});
  }());
  