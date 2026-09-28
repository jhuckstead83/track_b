#!/usr/bin/env python3
"""Verify preserved controlling inputs and bind fresh replay receipts.
Does not assert mathematical validity from a matching hash.
"""
from pathlib import Path
import hashlib, json, sys
R=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
records=[]
for label,home,manifest in [
 ('v4.2 publication',R/'provenance/v42',R/'provenance/v42/PACKAGE_MANIFEST.json'),
 ('accepted v4.2 returns',R/'provenance/v43/accepted_returns',R/'provenance/v43/accepted_returns/MANIFEST.json')]:
    data=json.loads(manifest.read_text());fails=[]
    for x in data['files']:
        p=home/x['path']
        if label=='v4.2 publication' and not p.is_file():
            # Shared inherited figures and older provenance remain in their original directories.
            p=R/x['path']
        if not p.resolve().is_relative_to(R):raise ValueError('unsafe input path')
        if not p.is_file() or p.stat().st_size!=x['bytes'] or sha(p)!=x['sha256']:
            fails.append(x['path'])
    records.append({'name':label,'manifest':str(manifest.relative_to(R)),
       'manifest_sha256':sha(manifest),'total':len(data['files']),
       'passed':len(data['files'])-len(fails),'failed':fails})
result={'status':'PASS' if all(not x['failed'] for x in records) else 'FAIL',
        'total':sum(x['total'] for x in records),'passed':sum(x['passed'] for x in records),'inputs':records}
(R/'qa/RECONCILIATION_INTEGRITY.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
files=['WEIGHTED_RESULTANTS.json','COMMON_SOURCE.json','INTEGRATED_BRIDGES.json',
'SINE_BRIDGE.json','LIGHTHOUSE_TIEOUT.json','BLUE_SHARPENING.json',
'ORANGE_CURVATURE.json','GREEN_BLUE_MERGE.json','GREEN_ORANGE_COMPARISON.json',
'CURVATURE_PROGRESSIONS.json']
comparisons=[]
for fn in files:
    a=R/'provenance/v42/qa'/fn;b=R/'qa'/fn
    same=a.is_file() and b.is_file() and a.read_bytes()==b.read_bytes()
    comparisons.append({'receipt':fn,'reference':str(a.relative_to(R)),
       'fresh':str(b.relative_to(R)),'identical':same,
       'reference_sha256':sha(a) if a.is_file() else None,
       'fresh_sha256':sha(b) if b.is_file() else None})
(R/'qa/AUDIT_RECEIPT_COMPARISON.json').write_text(json.dumps(comparisons,indent=2)+'\n')
print('Inherited receipt comparison:',sum(x['identical'] for x in comparisons),'/',len(comparisons))
raise SystemExit(0 if result['status']=='PASS' and all(x['identical'] for x in comparisons) else 1)
