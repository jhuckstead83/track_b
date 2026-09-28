#!/usr/bin/env python3
"""Source and asset preservation against the supplied v4.2 masters."""
from pathlib import Path
from collections import Counter
import hashlib,re,json,difflib,sys
R=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
norm=lambda s:re.sub(r'\s+','',s)
report={}
for kind,suffix in [('reading','READING_VOLUME'),('dossier','TECHNICAL_DOSSIER')]:
    oldp=R/f'provenance/v42/src/TN_Postmaster_Volume_I_v4_2_{suffix}.md'
    newp=R/f'src/TN_Postmaster_Volume_I_v4_3_{suffix}.md'
    old,new=oldp.read_text(),newp.read_text()
    tags=lambda t:Counter(re.findall(r'\\tag\{([^}]+)\}',t))
    a,b=tags(old),tags(new)
    blocks=lambda t:re.findall(r'\$\$(.*?)\$\$',t,re.S)
    oldblocks,newblocks=blocks(old),blocks(new)
    bytag=lambda bs:{t:x for x in bs for t in re.findall(r'\\tag\{([^}]+)\}',x)}
    ob,nb=bytag(oldblocks),bytag(newblocks)
    changed={k:{'before':ob[k].strip(),'after':nb[k].strip()} for k in ob if k in nb and norm(ob[k])!=norm(nb[k])}
    untagged_old=[x for x in oldblocks if not re.search(r'\\tag\{',x)]
    untagged_new={norm(x) for x in newblocks}
    missing=[x.strip() for x in untagged_old if norm(x) not in untagged_new]
    report[kind]={'old_source_sha256':sha(oldp),'new_source_sha256':sha(newp),'old_tag_count':sum(a.values()),'new_tag_count':sum(b.values()),'missing_tags':list((a-b).elements()),'new_tags':list((b-a).elements()),'duplicate_tags':{k:v for k,v in b.items() if v>1},'changed_numbered_displays':changed,'changed_or_removed_untagged_displays':missing}
    (R/f'qa/{suffix}_V42_TO_V43.diff').write_text(''.join(difflib.unified_diff(old.splitlines(keepends=True),new.splitlines(keepends=True),fromfile=str(oldp.relative_to(R)),tofile=str(newp.relative_to(R)))))
oldmanifest=json.loads((R/'provenance/v42/PACKAGE_MANIFEST.json').read_text())
figures=[x for x in oldmanifest['files'] if x['path'].startswith('figures/')]
report['figures']={'total':len(figures),'unchanged':[],'changed':[],'missing':[]}
for x in figures:
    p=R/x['path']
    if not p.is_file():report['figures']['missing'].append(x['path'])
    elif sha(p)==x['sha256']:report['figures']['unchanged'].append(x['path'])
    else:report['figures']['changed'].append({'path':x['path'],'old_sha256':x['sha256'],'new_sha256':sha(p)})
report['grid']={'path':'figures/v30c_widder_pascal_grid.pdf','byte_identical':'figures/v30c_widder_pascal_grid.pdf' in report['figures']['unchanged'],'expected_cells':sum(range(1,19)),'seed':1}
for k in ('reading','dossier'):
    print(k,report[k]['old_tag_count'],'->',report[k]['new_tag_count'],'changed numbered',list(report[k]['changed_numbered_displays']),'changed untagged',len(report[k]['changed_or_removed_untagged_displays']))
print('Figures:',len(report['figures']['unchanged']),'unchanged;',len(report['figures']['changed']),'changed')
(R/'qa/PRESERVATION_V43.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
assert all(not report[k]['missing_tags'] and not report[k]['duplicate_tags'] for k in ('reading','dossier'))
assert not report['figures']['missing']
assert not report['figures']['changed']
assert all(not report[k]['changed_numbered_displays'] and not report[k]['changed_or_removed_untagged_displays'] for k in ('reading','dossier'))
