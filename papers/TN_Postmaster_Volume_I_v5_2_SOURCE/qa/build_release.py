#!/usr/bin/env python3
"""Build the two v5.2 volumes from the assembled Markdown masters.

Usage: python3 qa/build_release.py [reading|dossier|both]
Requires pandoc, pdflatex (TeX Live with the supplied preamble packages),
and PyMuPDF. No legacy tmp/stage inputs or network access are required.
Draft-mode passes stabilize references without re-embedding every image;
a checked final pass creates the PDF. Both final PDFs are bound by hash.
"""
from pathlib import Path
import argparse, hashlib, json, os, shutil, subprocess, time, re
import pymupdf as fitz
ROOT=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
STEMS={t:f'TN_Postmaster_Volume_I_v5_2_{s}' for t,s in [('reading','READING_VOLUME'),('dossier','TECHNICAL_DOSSIER')]}
ENV=dict(os.environ, SOURCE_DATE_EPOCH='1789603200', FORCE_SOURCE_DATE='1')

def command(args,log,cwd=ROOT):
    start=time.monotonic()
    with log.open('w') as f:
        result=subprocess.run(args,cwd=cwd,env=ENV,stdout=f,stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(f'command exit {result.returncode}: {args[0]}; see {log}')
    return time.monotonic()-start

def build(tag):
    stem=STEMS[tag];src=ROOT/'src'/f'{stem}.md';pre=ROOT/'src'/f'preamble_v52_{tag}.tex'
    if any(ord(c)<32 and c not in '\n\r\t' for c in src.read_text()):
        raise RuntimeError(f'{tag}: nonprinting control character in source')
    tmp=ROOT/'tmp'/tag
    if tmp.exists():shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    tex=tmp/f'{tag}.tex'
    command(['pandoc',str(src),'--standalone',f'--include-in-header={pre}',
             '--resource-path=.:src:figures','--top-level-division=chapter',
             '--pdf-engine=pdflatex',f'--output={tex}'],tmp/'pandoc.log')
    frozen=sha(tex)
    prev=None; passes=[];stable=False
    for i in range(6):
        log=tmp/f'draft{i}.log'
        seconds=command(['pdflatex','-draftmode','-interaction=nonstopmode','-halt-on-error',
                         '-file-line-error','-recorder',f'-output-directory={tmp}',str(tex)],log)
        files=[tmp/f'{tag}.{s}' for s in ('aux','toc','out')]
        state=hashlib.sha256(b''.join(p.read_bytes() for p in files if p.exists())).hexdigest()
        txt=log.read_text(errors='replace')
        passes.append({'kind':'draft','log':str(log.relative_to(ROOT)),'seconds':round(seconds,2),'state':state})
        if state==prev and not re.search(r'Rerun to get|Label\(s\) may have changed',txt):
            stable=True;break
        prev=state
    if not stable: raise RuntimeError(f'{tag}: references did not stabilize')
    final=tmp/'final.log'
    seconds=command(['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error',
                     '-recorder',f'-output-directory={tmp}',str(tex)],final)
    passes.append({'kind':'final','log':str(final.relative_to(ROOT)),'seconds':round(seconds,2)})
    txt=final.read_text(errors='replace')
    errors=re.findall(r'^!.*',txt,re.M)
    undefined=re.findall(r'[^\n]*undefined[^\n]*',txt,re.I)
    missing=re.findall(r'[^\n]*Missing character[^\n]*',txt)
    over=[float(x) for x in re.findall(r'Overfull \\hbox \(([0-9.]+)pt',txt)]
    if errors or undefined or missing or 'Label(s) may have changed' in txt:
        raise RuntimeError(f'{tag}: final log failed, see {final}')
    if frozen!=sha(tex):raise RuntimeError('TeX changed while compiling')
    body=tmp/f'{tag}.pdf';out=ROOT/'output/pdf'/f'{stem}.pdf';out.parent.mkdir(parents=True,exist_ok=True)
    bodyhash=sha(body)
    with fitz.open(body) as d:
        bodypages=len(d)
        if tag=='dossier':
            with fitz.open(ROOT/'src/facsimile_pages_11_13.pdf') as f:
                assert len(f)==3
                d.insert_pdf(f)
            d.save(out,garbage=4,deflate=True)
        else:shutil.copy2(body,out)
    with fitz.open(out) as d:pages=len(d)
    rec={'tag':tag,'stem':stem,'source':str(src.relative_to(ROOT)),'src_sha256':sha(src),
         'preamble_sha256':sha(pre),'tex_sha256':frozen,'body_pages':bodypages,'pages':pages,
         'body_pdf_sha256':bodyhash,'pdf_sha256':sha(out),'passes':passes,
         'undefined_refs':len(undefined),'missing_characters':len(missing),
         'overfull_boxes_pt':over,'overfull_over_30pt':[x for x in over if x>30],
         'pdf':str(out.relative_to(ROOT))}
    if tag=='dossier':rec['facsimile_sha256']=sha(ROOT/'src/facsimile_pages_11_13.pdf')
    (ROOT/'qa'/f'BUILD_{tag.upper()}.json').write_text(json.dumps(rec,indent=2)+'\n')
    print(json.dumps(rec,indent=2),flush=True)
    return rec

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('which',choices=['both','reading','dossier'],nargs='?',default='both');args=ap.parse_args()
    for tag in (['reading','dossier'] if args.which=='both' else [args.which]):build(tag)
    rows=[]
    for tag in STEMS:
        p=ROOT/'qa'/f'BUILD_{tag.upper()}.json'
        if p.exists():rows.append(json.loads(p.read_text()))
    (ROOT/'qa/BUILD_BINDING.json').write_text(json.dumps(rows,indent=2)+'\n')
