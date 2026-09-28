/* Research stays below a live table, with anchor links opening the right disclosure. */
(() => {
  function revealHash(){
    const target=document.getElementById(location.hash.slice(1));
    if(!target)return;
    for(let node=target;node;node=node.parentElement)if(node.tagName==='DETAILS')node.open=true;
    requestAnimationFrame(()=>target.scrollIntoView({block:'start'}));
  }
  document.addEventListener('click',event=>{
    const link=event.target.closest('a[href^="#"]');
    if(!link)return;
    const id=link.getAttribute('href').slice(1),target=document.getElementById(id);
    if(!target)return;
    for(let node=target;node;node=node.parentElement)if(node.tagName==='DETAILS')node.open=true;
  });
  addEventListener('hashchange',revealHash);revealHash();
})();
