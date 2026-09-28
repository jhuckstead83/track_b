function show(name){
  if(!document.querySelector('[data-pane="'+name+'"]'))return;
  for(const pane of document.querySelectorAll('[data-pane]'))pane.hidden=pane.dataset.pane!==name;
  for(const tab of document.querySelectorAll('[data-surface]')){if(tab.dataset.surface===name)tab.setAttribute('aria-current','page');else tab.removeAttribute('aria-current');}
  window.dispatchEvent(new CustomEvent('a51surfacechange',{detail:name}));
}
for(const tab of document.querySelectorAll('[data-surface]'))tab.addEventListener('click',()=>show(tab.dataset.surface));
window.addEventListener('hashchange',()=>show(location.hash.slice(1)||'play'));
show(location.hash.slice(1)||'play');
