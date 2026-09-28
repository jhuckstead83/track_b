#!/usr/bin/env python3
"""Replay v4.3 finite audits and hard publishing checks after building both PDFs.

Reference inputs under provenance are never modified. Generated qa outputs are
replaced, so verify_package.py should be run BEFORE this replay. An aggregate
exit of 1 is deliberately retained when only the inherited 90/275-page targets
fail. Hard mathematical/build failures are not relabelled as advisories.
"""
from pathlib import Path
import hashlib, json, shutil, subprocess, sys, time
R=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
results=[]
def run(name,args,log):
    started=time.monotonic()
    with (R/log).open('w') as f:
        proc=subprocess.run([sys.executable]+args,cwd=R,stdout=f,stderr=subprocess.STDOUT)
    row={'name':name,'command':['python3']+args,'exit_code':proc.returncode,
         'log':log,'seconds':round(time.monotonic()-started,3),
         'script_sha256':sha(R/args[0])}
    results.append(row);print(json.dumps(row),flush=True)
    return proc.returncode
run('ten_inherited_mathematical_audits',['qa/replay_math.py'],'qa/math_replay_execution.log')
target=R/'qa/new_returns_replay'
if target.exists():shutil.rmtree(target)
run('eight_accepted_return_audits',[
 'provenance/v43/accepted_returns/scripts/replay_bundle.py',
 '--output-dir','qa/new_returns_replay','--timeout','120'],'qa/new_returns_replay_execution.log')
run('preserved_inputs_and_receipt_comparison',['qa/audit_inputs_v43.py'],'qa/input_integrity_execution.log')
run('source_and_figure_preservation',['qa/check_preservation.py'],'qa/preservation_execution.log')
run('legacy_regression',['qa/verify_legacy_adapted.py'],'qa/legacy_verify_execution.log')
run('hard_publishing_guard',['qa/publishing_guard_release.py'],'qa/publishing_guard.log')
legacy=json.loads((R/'qa/LEGACY_VERIFY.json').read_text())
expected=[
 'Reading Volume at or under the standing target of 90 (advisory)',
 'Technical Dossier at or under the standing target of 275']
only_expected=legacy.get('failed')==expected
hard_ok=all(x['exit_code']==0 for x in results if x['name']!='legacy_regression')
code=1 if any(x['exit_code'] for x in results) else 0
ledger={'status':'HARD_GATES_PASS_WITH_RETAINED_ADVISORIES' if hard_ok and only_expected else 'REVIEW_RESULTS_REQUIRED',
        'runs':results,'legacy_advisory':legacy.get('failed',[]),
        'aggregate_exit_code':code,
        'scope':'Finite audit and publication replay. No RH source upper bound or historical interval certificate is proved by this runner.'}
(R/'qa/REPLAY_EXIT_LEDGER.json').write_text(json.dumps(ledger,indent=2)+'\n')
print(ledger['status'],flush=True)
raise SystemExit(code)
