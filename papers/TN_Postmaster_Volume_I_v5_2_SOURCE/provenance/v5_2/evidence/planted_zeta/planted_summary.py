import json, glob, math, statistics as st
rows = []
for f in sorted(glob.glob('planted_zeros_*.log')):
    for line in open(f):
        rows.append(json.loads(line))
flags = [r for r in rows if not isinstance(r['kFirst'], int)]
print('plants:', len(rows), ' unresolved/flagged:', len(flags), flags[:3])
ok = [r for r in rows if isinstance(r['kFirst'], int)]
print(f"{'height':>14} {'delta':>6} {'n':>3} {'law ratio median':>17} {'min':>6} {'max':>6}   {'k*theta^2 median':>16}  {'example k*':>24}")
by = {}
for r in ok: by.setdefault((round(r['height'], -1 if r['height'] < 1e5 else -3), r['delta']), []).append(r)
for (h, d), g in sorted(by.items()):
    lr = [x['law_ratio'] for x in g]; kt = [x['kTheta2'] for x in g]
    print(f"{h:14.0f} {d:6.2f} {len(g):3d} {st.median(lr):17.3f} {min(lr):6.3f} {max(lr):6.3f}   {st.median(kt):16.4f}  {g[0]['kFirst']:>24d}")
allr = [r['law_ratio'] for r in ok]
print(f"all plants: law ratio median {st.median(allr):.3f}, 10-90% range {sorted(allr)[len(allr)//10]:.3f}-{sorted(allr)[9*len(allr)//10]:.3f}, full {min(allr):.3f}-{max(allr):.3f}")
allk = [r['kTheta2'] for r in ok]
print(f"k*theta^2: full range {min(allk):.4f}-{max(allk):.4f} (ratio {max(allk)/min(allk):.1f}x)  vs law ratio spread {max(allr)/min(allr):.1f}x")
json.dump(ok, open('planted_all.json', 'w'), indent=1)
