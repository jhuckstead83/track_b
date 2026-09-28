/* Card-local actions. No game rules or wallet values live here. */
(() => {
  'use strict';
  let panel, anchor, fallback, container;
  function close(restore = true) {
    if (!panel || panel.hidden) return;
    panel.hidden = true;
    anchor?.setAttribute('aria-expanded', 'false');
    if (restore) (anchor?.isConnected ? anchor : fallback)?.focus({preventScroll:true});
  }
  function position() {
    if (!panel || panel.hidden) return;
    if (!anchor?.isConnected) { close(false); return; }
    if(container){panel.style.maxHeight=Math.max(140,Math.min(innerHeight-32,container.getBoundingClientRect().height-16))+'px';return;}
    const r = anchor.getBoundingClientRect(), gap = 8;
    panel.style.maxHeight = Math.max(120, innerHeight - 24) + 'px';
    panel.style.left = Math.max(12, Math.min(innerWidth - panel.offsetWidth - 12, r.left + r.width / 2 - panel.offsetWidth / 2)) + 'px';
    const below = r.bottom + gap;
    panel.style.top = Math.max(12, below + panel.offsetHeight <= innerHeight - 12 ? below : r.top - panel.offsetHeight - gap) + 'px';
  }
  function open(trigger, {title, info = '', actions = [], content, focusFallback, within} = {}) {
    close(false);
    anchor = trigger; fallback = focusFallback; container = within;
    if (!panel) {
      panel = document.createElement('section'); panel.className = 'card-menu'; panel.id = 'card-actions';
      panel.setAttribute('role', 'dialog'); panel.setAttribute('aria-label', 'Card actions'); panel.tabIndex = -1;
      panel.hidden = true; document.body.append(panel);
      panel.addEventListener('keydown', e => {
        if (e.key === 'Escape') { e.preventDefault(); e.stopPropagation(); close(); }
        if (e.key === 'Tab') {
          const list = [...panel.querySelectorAll('button:not(:disabled), a[href]')];
          const first = list[0], last = list.at(-1);
          if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last?.focus(); }
          else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first?.focus(); }
        }
      });
    }
    (container||document.body).append(panel);
    panel.classList.toggle('reel-card-actions',!!container);
    panel.replaceChildren();
    const head = document.createElement('div'); head.className = 'card-menu-head';
    const name = document.createElement('strong'); name.textContent = title || 'Your move';
    const dismiss = document.createElement('button'); dismiss.type = 'button'; dismiss.textContent = '×'; dismiss.setAttribute('aria-label', 'Close card actions'); dismiss.onclick = () => close();
    if(container){const face=trigger.querySelector('p51-token')?.cloneNode(true);if(face){face.removeAttribute('id');face.removeAttribute('size');face.setAttribute('static','');head.append(face);}}
    head.append(name, dismiss); panel.append(head);
    if (content) panel.append(content);
    if (info) { const p = document.createElement('p'); p.textContent = info; panel.append(p); }
    const group = document.createElement('div'); group.className = 'card-menu-actions';
    for (const action of actions) {
      if (!action) continue;
      const b = document.createElement('button'); b.type = 'button'; b.textContent = action.label;
      b.disabled = !!action.disabled; if (action.primary) b.className = 'primary';
      if (action.description) b.title = action.description;
      b.onclick = () => { close(); action.run?.(); };
      group.append(b);
    }
    panel.append(group); panel.hidden = false;
    trigger.setAttribute('aria-expanded', 'true'); trigger.setAttribute('aria-controls', panel.id);
    position(); (group.querySelector('button:not(:disabled)') || dismiss).focus({preventScroll:true});
  }
  function fromButton(id, label, extra = {}) {
    const b = document.getElementById(id);
    return b ? {label: label || b.textContent.trim(), disabled: b.disabled || b.hidden, run: () => { if (!b.disabled && !b.hidden) b.click(); }, ...extra} : null;
  }
  function activate(el, handler, label) {
    if (label) el.setAttribute('aria-label', label);
    el.setAttribute('role', 'button'); el.tabIndex = 0; el.setAttribute('aria-haspopup', 'dialog');
    el.classList.add('card-target'); el.onclick = e => { e.stopPropagation(); handler(el); };
    el.onkeydown = e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); e.stopPropagation(); handler(el); } };
  }
  function reveal(id) {
    const target = typeof id === 'string' ? document.getElementById(id) : id;
    if (!target) return;
    close(false);
    for (let node = target; node; node = node.parentElement) {
      if (node.tagName === 'DETAILS') node.open = true;
    }
    const destination = target.tagName==='DETAILS' ? target.querySelector('summary') : target.disabled ? target.closest('details')?.querySelector('summary') || target : target;
    requestAnimationFrame(() => { destination.scrollIntoView({block:'center'}); destination.focus({preventScroll:true}); });
  }
  document.addEventListener('pointerdown', e => { if (panel && !panel.hidden && !panel.contains(e.target) && !anchor?.contains(e.target)) close(false); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
  addEventListener('resize', position); addEventListener('scroll', position, true);
  addEventListener('a51surfacechange', () => close(false));
  globalThis.CardUI = Object.freeze({open, close, activate, fromButton, reveal, refresh:position});
})();
