#!/usr/bin/env python3
"""Render each release page for visual review, plus full-size changed passages.
Images are review scratch output, not a substitute for proof verification.
"""
from pathlib import Path
import argparse,json
import pymupdf as fitz
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--out',default='qa/visual_v44');p.add_argument('--which',choices=['both','reading','dossier'],default='both');a=p.parse_args();out=Path(a.out);out=out if out.is_absolute() else ROOT/out;out.mkdir(parents=True,exist_ok=True)
report=json.loads((ROOT/'qa/VISUAL_RENDER_INDEX.json').read_text()) if (ROOT/'qa/VISUAL_RENDER_INDEX.json').exists() and a.which!='both' else {}
queries={
 'reading':['CUT.4','R17I. Exact','DIV.1','DIV.2','DIV.3','DIV.4','R22. Results','23.4','80. Elaissaoui'],
 'dossier':['155F.1','155F.2','155F.3','155F.4','155F.5','155F.6','155F.7','155F.8','155F.9',
 '155G.1','155G.4','155G.7','155G.10','155G.13','155G.15',
 '155H.1','155H.3','155H.5','155H.7','155H.11','155I.1','155I.2','155I.4','155I.6',
 '166G.1','166G.2','166G.4','166G.5','166G.7','166G.9','166G.10',
 '67. The remaining source','80. Elaissaoui']}
for tag,suffix in [('reading','READING_VOLUME'),('dossier','TECHNICAL_DOSSIER')]:
    if a.which not in ('both',tag):continue
    d=fitz.open(ROOT/f'output/pdf/TN_Postmaster_Volume_I_v4_4_{suffix}.pdf')
    text=[pg.get_text() for pg in d];hits={q:[i+1 for i,t in enumerate(text) if q in t and i>4] for q in queries[tag]}
    selected={1,2,len(d)}
    for ns in hits.values():
        for n in ns:
            selected.add(n)
            if tag=='dossier':selected.add(min(n+1,len(d)))
    if tag=='dossier':selected.update(range(len(d)-2,len(d)+1))
    sheets=[]
    w,h=320,432;pad=12;lab=22
    for start in range(0,len(d),24):
        sheet=Image.new('RGB',(4*(w+pad)+pad,6*(h+lab+pad)+pad),'#e4e7e9');draw=ImageDraw.Draw(sheet)
        for k in range(24):
            i=start+k
            if i>=len(d):break
            pix=d[i].get_pixmap(matrix=fitz.Matrix(.58,.58),alpha=False)
            im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);im.thumbnail((w,h))
            x=pad+(k%4)*(w+pad);y=pad+(k//4)*(h+lab+pad)
            sheet.paste(im,(x,y+lab));draw.text((x,y+4),f'{tag} PDF {i+1}',fill='black')
        fn=out/f'sheet_{tag}_{start+1:03}.jpg';sheet.save(fn,quality=88);sheets.append(str(fn.relative_to(ROOT)) if fn.is_relative_to(ROOT) else str(fn))
    for n in sorted(selected):
        d[n-1].get_pixmap(matrix=fitz.Matrix(1.6,1.6),alpha=False).save(out/f'{tag}_{n:03}.png')
    report[tag]={'total_pages_rendered':len(d),'pdf_sha256':__import__('hashlib').sha256((ROOT/f'output/pdf/TN_Postmaster_Volume_I_v4_4_{suffix}.pdf').read_bytes()).hexdigest(),'contact_sheets':sheets,'full_size_pages':sorted(selected),'passage_hits':hits}
    print(tag,len(d),'pages rendered',flush=True)
    d.close()
(ROOT/'qa/VISUAL_RENDER_INDEX.json').write_text(json.dumps(report,indent=2)+'\n')
