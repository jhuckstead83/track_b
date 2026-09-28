// Real Chromium pass over the v2.8.6 archive (served locally, external feeds unreachable -> offline/reference mode).
const { chromium } = require('playwright');
const OUT = process.argv[2], BASE = 'http://127.0.0.1:8770';
const R = [];
const note = (view, name, ok, detail) => { R.push({ view, name, ok, detail }); console.log(ok ? 'OK  ' : 'FAIL', view, name, detail ? JSON.stringify(detail) : ''); };
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  for (const view of [{ tag: 'desktop', viewport: { width: 1280, height: 900 } }, { tag: 'phone', viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 }]) {
    const ctx = await b.newContext({ viewport: view.viewport, hasTouch: !!view.hasTouch, isMobile: !!view.isMobile, deviceScaleFactor: view.deviceScaleFactor || 1 });
    const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(String(e)));
    // Homepage hero
    await p.goto(BASE + '/', { waitUntil: 'load' }); await p.waitForTimeout(500);
    const sl = () => p.$eval('#home-feature-track', t => Math.round(t.scrollLeft));
    const pauseHidden = () => p.$eval('#feature-pause', e => e.hidden || getComputedStyle(e).display === 'none' || getComputedStyle(e).visibility === 'hidden');
    note(view.tag, 'pause control hidden at load', await pauseHidden());
    const s0 = await sl(); await p.waitForTimeout(6800); const s1 = await sl();
    note(view.tag, 'untouched hero advances within ~6 s', s1 > s0, { before: s0, after: s1 });
    note(view.tag, 'no bottom control bar / count / Open-Play footer', await p.evaluate(() => !document.querySelector('.home-feature-controls, .feature-count, .feature-footer')));
    const sw = await p.evaluate(() => document.documentElement.scrollWidth);
    note(view.tag, 'no horizontal overflow on homepage', sw <= view.viewport.width, { scrollWidth: sw });
    // arrows overlap check: arrows vs pause control boxes
    await p.screenshot({ path: `${OUT}/shots/home_${view.tag}.png`, clip: await p.$eval('.home-feature-carousel', e => { const r = e.getBoundingClientRect(); return { x: 0, y: Math.max(0, r.top + scrollY), width: innerWidth, height: Math.min(r.height, 900) }; }) });
    if (view.tag === 'desktop') {
      await p.hover('.home-feature-carousel'); await p.waitForTimeout(300);
      note(view.tag, 'hover reveals Play', !(await pauseHidden()) && (await p.$eval('#feature-pause', e => e.title)) === 'Play');
      const h1 = await sl(); await p.waitForTimeout(6500); note(view.tag, 'hover pauses rotation', (await sl()) === h1);
      await p.click('#feature-pause'); await p.waitForTimeout(6800); note(view.tag, 'explicit Play resumes', (await sl()) > h1);
      const boxes = await p.evaluate(() => ['#feature-prev', '#feature-next', '#feature-pause'].map(s => { const r = document.querySelector(s).getBoundingClientRect(); return [s, r.left, r.top, r.right, r.bottom]; }));
      const ov = (a, c) => !(a[3] <= c[1] || c[3] <= a[1] || a[4] <= c[2] || c[4] <= a[2]);
      note(view.tag, 'pause control does not overlap the ghost arrows', !ov(boxes[0], boxes[2]) && !ov(boxes[1], boxes[2]), boxes);
    } else {
      // real touch swipe via CDP gesture on the track
      const box = await p.$eval('#home-feature-track', e => { const r = e.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; });
      const cdp = await ctx.newCDPSession(p); const before = await sl();
      // real touch sequence: finger moves left across the card (synthesizeScrollGesture does not drive this element headless)
      await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: box.x + 120, y: box.y }] });
      for (let i = 1; i <= 12; i++) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: box.x + 120 - 22 * i, y: box.y }] }); await p.waitForTimeout(16); }
      await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
      await p.waitForTimeout(1200); const after = await sl();
      note(view.tag, 'touch swipe moves the carousel', after !== before, { before, after });
      note(view.tag, 'swipe pauses and reveals Play', !(await pauseHidden()) && (await p.$eval('#feature-pause', e => e.title)) === 'Play');
      await p.waitForTimeout(6800); note(view.tag, 'rotation stays paused after swipe', (await sl()) === after);
    }
    note(view.tag, 'homepage page errors', errs.length === 0, errs.slice(0, 3));
    // Finance dock on a game page
    const g = await ctx.newPage(); const gerr = []; g.on('pageerror', e => gerr.push(String(e)));
    await g.goto(BASE + '/area-51/sedaps-51/', { waitUntil: 'load' }); await g.waitForTimeout(800);
    note(view.tag, 'untouched dock stays hidden without real activity', await g.$eval('.finance-dock', d => d.hidden));
    note(view.tag, 'no dotted grip', await g.evaluate(() => !document.querySelector('.finance-dock-grip')));
    await g.click('.finance-monitor-settings'); await g.waitForTimeout(900);
    note(view.tag, 'footer restore shows the dock, grid open', !(await g.$eval('.finance-dock', d => d.hidden)) && (await g.$eval('.finance-dock-toggle', t => t.getAttribute('aria-expanded'))) === 'true');
    await g.screenshot({ path: `${OUT}/shots/dock_open_${view.tag}.png` });
    await g.click('.finance-dock-toggle'); await g.waitForTimeout(1200);
    note(view.tag, 'chevron collapses only the grid, tab stays, no dialog', (await g.$eval('.finance-dock-toggle', t => t.getAttribute('aria-expanded'))) === 'false' && !(await g.$eval('.finance-dock', d => d.hidden)) && !(await g.evaluate(() => [...document.querySelectorAll('dialog')].some(x => x.open))));
    const r0 = await g.$eval('.finance-dock', d => d.getBoundingClientRect().toJSON());
    const hb = await g.$eval('.finance-dock-handle', h => { const r = h.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; });
    if (view.tag === 'desktop') { await g.mouse.move(hb.x, hb.y); await g.mouse.down(); await g.mouse.move(hb.x - 200, hb.y - 150, { steps: 8 }); await g.mouse.up(); }
    else {
      const cdp = await ctx.newCDPSession(g);
      await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: hb.x, y: hb.y }] });
      for (let i = 1; i <= 8; i++) await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: hb.x - 12 * i, y: hb.y - 25 * i }] });
      await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
    }
    await g.waitForTimeout(500);
    const r1 = await g.$eval('.finance-dock', d => d.getBoundingClientRect().toJSON());
    const vw = view.viewport.width, vh = view.viewport.height;
    note(view.tag, 'dragging the Finance label moves the tab', r1.left !== r0.left || r1.top !== r0.top, { from: [Math.round(r0.left), Math.round(r0.top)], to: [Math.round(r1.left), Math.round(r1.top)] });
    note(view.tag, 'tab stays inside the viewport', r1.left >= 0 && r1.top >= 0 && r1.right <= vw && r1.bottom <= vh, { right: Math.round(r1.right), bottom: Math.round(r1.bottom) });
    note(view.tag, 'drag neither toggles nor dismisses', (await g.$eval('.finance-dock-toggle', t => t.getAttribute('aria-expanded'))) === 'false' && !(await g.$eval('.finance-dock', d => d.hidden)));
    await g.click('.finance-dock-hide'); await g.waitForTimeout(300);
    note(view.tag, 'X asks for confirmation', await g.evaluate(() => [...document.querySelectorAll('dialog')].some(x => x.open)));
    await g.screenshot({ path: `${OUT}/shots/dock_confirm_${view.tag}.png` });
    await g.click('[data-hide-cancel]'); await g.waitForTimeout(300);
    note(view.tag, 'Cancel keeps the tab', !(await g.$eval('.finance-dock', d => d.hidden)));
    await g.reload({ waitUntil: 'load' }); await g.waitForTimeout(800);
    const r2 = await g.$eval('.finance-dock', d => d.getBoundingClientRect().toJSON());
    note(view.tag, 'engaged tab and its position survive reload (offline)', !(await g.$eval('.finance-dock', d => d.hidden)) && Math.abs(r2.left - r1.left) < 2 && Math.abs(r2.top - r1.top) < 2, { left: Math.round(r2.left), top: Math.round(r2.top) });
    await g.click('.finance-dock-hide'); await g.click('[data-hide-confirm]'); await g.waitForTimeout(300);
    await g.reload({ waitUntil: 'load' }); await g.waitForTimeout(800);
    note(view.tag, 'confirmed hide persists across reload', await g.$eval('.finance-dock', d => d.hidden));
    note(view.tag, 'game page errors', gerr.length === 0, gerr.slice(0, 3));
    // Finance page boots in reference mode
    const f = await ctx.newPage(); const ferr = []; f.on('pageerror', e => ferr.push(String(e)));
    await f.goto(BASE + '/finance/live.html', { waitUntil: 'load' }); await f.waitForTimeout(1500);
    const fin = await f.evaluate(() => ({ tiles: document.querySelectorAll('#phiGrid .cell').length, state: (document.querySelector('#dataState') || {}).textContent, fresh: (document.querySelector('#freshnessText') || {}).textContent }));
    note(view.tag, 'Finance boots offline with 16 labelled reference tiles', fin.tiles === 16 && /GOOGLE/.test(fin.state || ''), fin);
    const fsw = await f.evaluate(() => document.documentElement.scrollWidth); note(view.tag, 'no horizontal overflow on Finance', fsw <= vw, { scrollWidth: fsw });
    await f.screenshot({ path: `${OUT}/shots/finance_${view.tag}.png` });
    note(view.tag, 'Finance page errors', ferr.length === 0, ferr.slice(0, 3));
    await ctx.close();
  }
  await b.close();
  require('fs').writeFileSync(`${OUT}/browser-ui-result.json`, JSON.stringify({ status: R.every(r => r.ok) ? 'PASS' : 'REVIEW', scope: 'Chromium (Playwright) against the extracted v2.8.6 archive served on localhost; external feeds unreachable, so Finance ran in its offline/reference mode. Touch via CDP synthetic gestures, not a physical device.', results: R }, null, 1) + '\n');
})();
