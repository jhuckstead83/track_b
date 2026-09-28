#!/usr/bin/env python3
"""v5.1 delta audit only; does not rerun inherited v5.0 certificates."""
from pathlib import Path
import hashlib,json,re,platform
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def check(name,test):
    checks.append({'name':name,'pass':bool(test)})
    if not test: raise AssertionError(name)
def H(p):return hashlib.sha256(p.read_bytes()).hexdigest()
s,t=sp.symbols('s t')
q=lambda z:z*(1-z)
check('centered fold',sp.expand(q(s)-(sp.Rational(1,4)-(s-sp.Rational(1,2))**2))==0)
check('reflection factorization',sp.expand(q(s)-q(t)-(s-t)*(1-s-t))==0)
check('triangular fold',sp.expand(q(s)+2*(s-1)*s/2)==0)
summary={}
for kind in ['READING_VOLUME','TECHNICAL_DOSSIER']:
    old=ROOT/'provenance/v5_0/src'/f'TN_Postmaster_Volume_I_v5_0_{kind}.md'
    new=ROOT/'src'/f'TN_Postmaster_Volume_I_v5_1_{kind}.md'
    a=old.read_text();b=new.read_text()
    oldtags=re.findall(r'\\tag\{([^}]+)\}',a)
    newtags=re.findall(r'\\tag\{([^}]+)\}',b)
    check(kind+': inherited equation-tag sequence preserved',
          [x for x in newtags if x!='IF.1']==oldtags)
    marks=['PROVED','CERT','EQUIV','EVID','OPENSTAT']
    check(kind+': inherited status-tag sequence preserved',
          re.findall(r'\\(?:'+'|'.join(marks)+r')\{\}',a)==
          re.findall(r'\\(?:'+'|'.join(marks)+r')\{\}',b))
    check(kind+': has abstract and summary', '# Abstract' in b and '# Summary' in b)
    check(kind+': no dependence on companion entropy article', 'Surprise Is Not Meaning' not in b)
    check(kind+': inherited replay scope disclosed', 'not been re-executed' in b or 'were not re-executed' in b)
    summary[kind]={'v50_sha256':H(old),'v51_sha256':H(new),
                   'inherited_equation_tags':len(oldtags),'new_equation_tags':len(newtags)}
# Exact v5.0 status-table rows, excluding the glossary entry whose build date was clarified.
a=(ROOT/'provenance/v5_0/src/TN_Postmaster_Volume_I_v5_0_READING_VOLUME.md').read_text()
b=(ROOT/'src/TN_Postmaster_Volume_I_v5_1_READING_VOLUME.md').read_text()
rows=[l for l in a.splitlines() if l.startswith('|') and any('\\'+x+'{' in l for x in ['PROVED','CERT','EQUIV','EVID','OPENSTAT']) and 'certificate of record' not in l]
check('all inherited mathematical status rows preserved verbatim',all(l in b for l in rows))
check('kernel order claim restricted to real positive folded nodes', 'When $q>0$ is real' in b and 'for\n  nonreal $q$ no real-order statement' in b)
for name in ['READING','DOSSIER']:
    p=ROOT/'qa'/f'BUILD_{name}.json'
    r=json.loads(p.read_text())
    check(name+': rebuilt without undefined references or missing characters',r['undefined_refs']==0 and r['missing_characters']==0)
    check(name+': rebuilt without overfull boxes',r['overfull_boxes_pt']==[])
receipt={'edition':'5.1','scope':'Editorial/interface delta, preservation and document build only. No v5.0 interval certificate rerun.',
         'python':platform.python_version(),'sympy':sp.__version__,'sources':summary,
         'checks':checks,'passed':len(checks),'status':'PASS'}
(ROOT/'qa/V51_INTERFACE_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
