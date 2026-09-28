/* Compact identity notation. No hidden game action is attached to flipping a token. */
(function(g){'use strict';
 const records=new Map(g.P51_DATA.map(x=>[x.card,x]));
 const suits={S:'\u2660',H:'\u2665',D:'\u2666',C:'\u2663'}, suitNames={S:'spades',H:'hearts',D:'diamonds',C:'clubs'};
 class P51Token extends HTMLElement{
  static get observedAttributes(){return ['card','face','size','static'];}
  constructor(){super();this.attachShadow({mode:'open'});}
  connectedCallback(){this.render();}
  attributeChangedCallback(){if(this.isConnected)this.render();}
  render(){
   const hadFocus=!!this.shadowRoot.activeElement;
   const card=this.getAttribute('card'),d=records.get(card),symbol=this.getAttribute('face')==='symbol',passive=this.hasAttribute('static');
   const isMarker=card==='2C',rank=d?d.rank:isMarker?'2':'',suit=d?d.suit:isMarker?'C':'';
   const label=d?`${rank} of ${suitNames[suit]}; ${d.role}, ${d.codePoint}. ${passive?'':symbol?'Show card face':'Show paper symbol'}`:isMarker?'2 of clubs, outside marker Ⅰ':'Undealt rotor';
   const tag=passive?'span':'button';
   this.shadowRoot.innerHTML=`<style>
    :host{display:inline-flex;vertical-align:-.24em;--size:var(--p51-size,1.8em);--r:calc(var(--size)*.29)}
    :host([size="reel"]){--size:var(--reel-size,64px)}
    .tile{box-sizing:border-box;width:var(--size);height:var(--size);padding:calc(var(--size)*.1);border:1px solid #c9d5cc;border-radius:calc(var(--size)*.12);background:#fffcf3;color:#193c33;display:flex;flex-direction:column;align-items:flex-start;justify-content:center;line-height:1;box-shadow:0 1px 1px #001a1018;text-decoration:none;font-family:Arial,sans-serif;flex:none;cursor:pointer;position:relative}
    .red{color:#b5263c}.rank{font-size:calc(var(--size)*.40);font-weight:750}.suit{font-size:calc(var(--size)*.35)}
    .glyph{width:100%;height:100%;overflow:visible;fill:currentColor}.empty{align-items:center;justify-content:center;background:#173d32;color:#adbbac;border:1px dashed #729285;box-shadow:none;font-family:Georgia,serif;font-size:calc(var(--size)*.52)}
    .tile:focus-visible{outline:3px solid #e3b963;outline-offset:3px}button:hover{border-color:#957538}span.tile{cursor:default}
    @media(prefers-contrast:more){.tile{border-color:currentColor}}
   </style><${tag} class="tile ${d&&d.color===1?'red':''} ${!d&&!isMarker?'empty':''}" ${passive?'role="img"':'type="button"'} aria-label="${label}">${d&&symbol?`<svg class="glyph" viewBox="${d.svgViewBox}" aria-hidden="true"><g transform="scale(1,-1)"><path d="${d.svgPath}"/></g></svg>`:d||isMarker?`<span class="rank" aria-hidden="true">${rank}</span><span class="suit" aria-hidden="true">${suits[suit]}</span>`:'<span aria-hidden="true">I</span>'}</${tag}>`;
   if(hadFocus&&!passive)this.shadowRoot.querySelector('button')?.focus({preventScroll:true});
   if(!passive&&d)this.shadowRoot.querySelector('button').onclick=()=>{this.setAttribute('face',symbol?'card':'symbol');this.dispatchEvent(new CustomEvent('p51-inspect',{detail:{card,face:symbol?'card':'symbol'},bubbles:true,composed:true}));};
  }
 }
 if(!customElements.get('p51-token'))customElements.define('p51-token',P51Token);
})(globalThis);
