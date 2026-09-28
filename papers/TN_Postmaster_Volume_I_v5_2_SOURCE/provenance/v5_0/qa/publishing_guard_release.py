#!/usr/bin/env python3
"""Hard v4.3 publication gates, separate from the retained 90-page advisory.

Uses the Pandoc document tree for Markdown images, checks raw TeX images,
requires BOTH source/PDF bindings, and compares the appended facsimile pages.
A hard failure exits nonzero. This is not an analytic proof verifier.
"""
from pathlib import Path
import hashlib,json,re,subprocess,sys
from collections import Counter
import pymupdf as fitz
ROOT=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks=[];assets=[]
def ck(name,ok,detail=None):checks.append({'name':name,'passed':bool(ok),'detail':detail})
def images(node):
    if isinstance(node,dict):
        if node.get('t')=='Image':yield node['c'][2][0]
        for v in node.values():yield from images(v)
    elif isinstance(node,list):
        for v in node:yield from images(v)
def parse_md(text):
    return json.loads(subprocess.run(['pandoc','--from=markdown','--to=json'],input=text,text=True,capture_output=True,check=True).stdout)
probe='![With [h(x)-h(y)]/(x-y) in the caption](figures/v26c_two_node_compatibility.png)'
ck('bracket-caption parser regression',list(images(parse_md(probe)))==['figures/v26c_two_node_compatibility.png'])
ck('missing-image negative control',not (ROOT/'figures/INTENTIONALLY_ABSENT_GUARD_CONTROL.png').exists())
rows=json.loads((ROOT/'qa/BUILD_BINDING.json').read_text())
ck('exactly two final bindings',len(rows)==2 and {r['tag'] for r in rows}=={'reading','dossier'})
text={}
for row in rows:
    tag=row['tag'];src=ROOT/row['source'];pre=ROOT/f'src/preamble_v43_{tag}.tex';pdf=ROOT/row['pdf'];tex=ROOT/f'tmp/{tag}/{tag}.tex'
    body=src.read_text();text[tag]=body
    ck(f'{tag}: final source bound',sha(src)==row['src_sha256'])
    ck(f'{tag}: final preamble bound',sha(pre)==row['preamble_sha256'])
    ck(f'{tag}: generated TeX bound',sha(tex)==row['tex_sha256'])
    ck(f'{tag}: delivered PDF bound',sha(pdf)==row['pdf_sha256'])
    ck(f'{tag}: two-pass stable state',len(row['passes'])>=3 and row['passes'][-3]['state']==row['passes'][-2]['state'])
    logs=[ROOT/z['log'] for z in row['passes']]
    ck(f'{tag}: all successful build logs retained',all(p.exists() for p in logs))
    final=(ROOT/f'tmp/{tag}/final.log').read_text(errors='replace')
    ck(f'{tag}: final log no fatal errors, missing glyphs, or undefined refs',not re.search(r'^!|Missing character|undefined|Label\(s\) may have changed',final,re.M|re.I))
    ck(f'{tag}: no overfull boxes',not row['overfull_boxes_pt'],row['overfull_boxes_pt'])
    paths=set(images(parse_md(body)))
    paths.update(re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}',body+'\n'+pre.read_text()))
    missing=[p for p in sorted(paths) if not (ROOT/p).is_file()]
    ck(f'{tag}: all parsed figure paths resolve',not missing,{'unique_paths':len(paths),'missing':missing})
    assets.extend({'document':tag,'path':p,'sha256':sha(ROOT/p)} for p in sorted(paths) if (ROOT/p).is_file())
    headings=re.findall(r'^## ((?:R)?\d+[A-Z]*)\.',body,re.M)
    ck(f'{tag}: heading IDs unique',len(headings)==len(set(headings)))
    tags=re.findall(r'\\tag\{([^}]+)\}',body)
    ck(f'{tag}: equation tags unique',len(tags)==len(set(tags)),len(tags))
    with fitz.open(pdf) as doc:
        ck(f'{tag}: PDF readable and page count bound',len(doc)==row['pages'],len(doc))
        ck(f'{tag}: standing page ceiling',len(doc)<=(99 if tag=='reading' else 299),len(doc))
        ck(f'{tag}: new local version on body footer','v4.3' in doc[10].get_text())
        # Check machine-readable text for off-page material; facsimiles are preserved.
        outside=[]
        for i,pg in enumerate(doc):
            if tag=='dossier' and i>=row['body_pages']:continue
            for b in pg.get_text('blocks'):
                if b[6]==0 and (b[0]<-1 or b[1]<-1 or b[2]>pg.rect.width+1 or b[3]>pg.rect.height+1):outside.append(i+1)
        ck(f'{tag}: no off-page text blocks',not outside,sorted(set(outside)))
rv=text['reading'];td=text['dossier'];flat=lambda t:re.sub(r'\s+',' ',t)
ck('Reader all-order Fourier status synchronized', 'at least $k$ Fourier sign changes' in rv and 'Theorem 22A.1' in rv and 'numerically for\n$k\\le4$' not in rv)
ck('Reader false remainder-open statements removed','The all-coefficient remainder\nin (166C.25) is still unproved' not in rv and 'degree-dependent cutoff still needs\nan all-coefficient error bound' not in rv)
ck('Reader stale fourth-rung wording removed','open fourth rung' not in rv and 'fourth-rung multiprecision receipt is not bundled' in rv)
ck('actual-source boundary retains both subtractions',r'\int_0^T L_{n-1}^{(1)}(u)du' in td and r'L_{n-1}^{(2)}(u)-n' in td and 'Omitting either subtraction changes the' in td)
ck('six sections carried from v4.0a occur exactly once',all(len(re.findall(r'^## '+i+r'\.',td,re.M))==1 for i in ('155A','155B','38A','104A','133A','166E')))
ck('positive-scale and boundary scope retained',
   'Setting $a=0$' in td and 'boundary transfer' in td
   and 'No upper bound in (166F.8) is proved' in flat(td))
ck('fixed versus moving depth distinction retained',r'\forall N\ \exists k(N)' in td and 'one fixed finite integer $k' in td)
ck('polynomial negative control and no rank-nine promotion retained','not an actual-zeta counterexample' in td and 'not every rank-nine' in td)
ck('source-prime cutoff and full-node obligations still open','The uniform cutoff-row norm' in td and r'\OPENSTAT{}' in rv and 'for every finite positive node set' in rv)
ck('build driver fails on errors and uses halt flag',all(t in (ROOT/'qa/build_release.py').read_text() for t in ('-halt-on-error','result.returncode','raise RuntimeError')))
ck('no font files redistributed',not [p for p in ROOT.rglob('*') if p.is_file() and p.suffix.lower() in ('.ttf','.otf','.woff','.woff2','.pfb','.pfa')])
dr=next(r for r in rows if r['tag']=='dossier')
with fitz.open(ROOT/dr['pdf']) as doc,fitz.open(ROOT/'src/facsimile_pages_11_13.pdf') as fac:
    matches=[doc[dr['body_pages']+j].get_pixmap(matrix=fitz.Matrix(.5,.5)).samples==fac[j].get_pixmap(matrix=fitz.Matrix(.5,.5)).samples for j in range(3)]
    ck('three facsimiles appended once and render-identical',len(doc)==dr['body_pages']+3 and len(fac)==3 and all(matches),matches)
legacy=json.loads((ROOT/'qa/LEGACY_VERIFY.json').read_text())
ck('both legacy page-target advisories are explicitly retained, not hidden',
   legacy['total']==312 and legacy['passed']==310 and legacy['failed']==[
   'Reading Volume at or under the standing target of 90 (advisory)',
   'Technical Dossier at or under the standing target of 275'])
# v4.2 integration gates. They supplement, rather than replace, the inherited gates.
ck('four Dossier sections introduced in v4.1 remain exactly once',
   all(len(re.findall(r'^## '+i+r'\.',td,re.M))==1 for i in ('95A','12A','61A','155C')))
ck('Reader retains three v4.1 bridge anchors',
   all(r'\tag{'+i+'}' in rv for i in ('PR.7a','6A.5','15.7')))
ck('quotient zero set excludes removed zero mode',
   '$x=-2T_n$, $n\\ge1$; $x=0$ has removable value one, not a zero.' in td)
ck('Reader preserves distinct numerator zero at n=0',
   'its zeros are exactly' in rv and '$x=-2T_n$ for $n\\ge0$' in rv)
ck('sharp reserve states its restricted family and all ranks',
   'The sharpness assertion is within the family (155C.2)' in flat(td)
   and r'\tag{155C.4}' in td and r'\hbox{for every }N\ge1' in td)
ck('complete compensation retained in actual arithmetic defect',
   r'+\delta(2\min(r,s)+1)' in td and r'\Phi_0(u)=0' in td
   and 'would change the source' in td and r'\tag{155C.14}' in td)
ck('reserve domination stays open in both volumes',
   'All-rank domination' in rv and 'remains unproved' in flat(rv)
   and 'RH-equivalent and remains unproved' in flat(td))
ck('weighted trace endpoint divergence is explicit',
   r'At $y=0$ this trace diverges' in td and 'not the unweighted resolvent' in td)
ck('comparison operator uses unitary images and removes zero mode',
   'unitary images, not the bare polynomials' in flat(td)
   and 'Remove the $m=0$ zero mode' in td)
ck('comparison limit does not replace source kernel obligation',
   'no limit from the completed-source Pick kernel to the sine kernel' in flat(td)
   and 'the missing completed-source Pick-kernel limit' in flat(td))
ck('source arithmetic regularization remains unchanged',
   r'M(u)=\Psi(e^u)-e^u+1' in td and r'\Phi_n(u)=L_{n-1}^{(2)}(u)-n' in td)
ck('Catalan and orthogonality measures remain distinct',
   'orthogonality measure is $\\omega$, not $\\nu_C$' in flat(td))
ck('odd-prime transition is scoped by its exact two indices',
   '$p-1\\to p$ for an odd prime $p$' in rv)
ck('no nonprinting control characters in active sources',
   all(not any(ord(c)<32 and c not in '\n\r\t' for c in z) for z in (rv,td)))
for tag,s in (('reading',rv),('dossier',td)):
    suffix='READING_VOLUME' if tag=='reading' else 'TECHNICAL_DOSSIER'
    old=(ROOT/f'provenance/v42/src/TN_Postmaster_Volume_I_v4_2_{suffix}.md').read_text()
    oldtags=set(re.findall(r'\\tag\{([^}]+)\}',old))
    nowtags=set(re.findall(r'\\tag\{([^}]+)\}',s))
    ck(f'{tag}: all inherited numbered equation tags retained',oldtags<=nowtags,
       {'before':len(oldtags),'after':len(nowtags),'missing':sorted(oldtags-nowtags)})
    row=next(z for z in rows if z['tag']==tag)
    with fitz.open(ROOT/row['pdf']) as d:
        ck(f'{tag}: release number is visible on cover','v4.3' in d[0].get_text())
oldmanifest=json.loads((ROOT/'provenance/v42/PACKAGE_MANIFEST.json').read_text())
fignames=[z for z in oldmanifest['files'] if z['path'].startswith('figures/')]
changedfigs=[z['path'] for z in fignames if sha(ROOT/z['path'])!=z['sha256']]
ck('90 inherited figures present and all byte-identical to v4.2',
   len(fignames)==90 and all((ROOT/z['path']).is_file() for z in fignames)
   and changedfigs==[],changedfigs)
for name,path,countkey,total,script in [
    ('sine','SINE_BRIDGE.json','exact_checks',1435,'audit_sine_bridge.py'),
    ('Lighthouse','LIGHTHOUSE_TIEOUT.json','exact_assertions',3841,'audit_lighthouse_tieout.py')]:
    z=json.loads((ROOT/'qa'/path).read_text())
    ck(f'{name}: fresh exact audit output bound to executed script',
       z[countkey]==total and z['script_sha256']==sha(ROOT/'qa'/script),z[countkey])


# v4.2 changes reviewed across Green, Blue, Orange and Lighthouse.
for i in ('12B','155D','155E','166F'):
    ck(f'new Dossier section {i} appears exactly once',len(re.findall(r'^## '+i+r'\.',td,re.M))==1)
ck('Reader contains the two current source targets',
   r'\tag{23.4}' in rv and r'I_{2m}' in rv and r'\widehat\beta_{2,d}' in rv)
ck('comparison/source coordinate signs are distinguished',
   r'E_\xi(-1/4)=X(1/4)/X(0)' in flat(rv) and r'x=-q(s)' in rv)
ck('same order is not incorrectly equated with same type',
   'in type, a' not in rv and 'That is the same type as' not in td
   and 'infinite type' in rv and 'finite type' in rv and r'\tag{12B.2}' in td)
ck('corrected carrier retains complex displacement and all-zero factor',
   r'\tau_\rho=(\rho-1/2)/i' in rv and r'\frac{(2k-1)!}{2(4x)^k}' in rv
   and r'f_{k,x}(\tau_\rho)' in rv)
ck('Fourier support and finite-height direction are explicit',
   'not compactly supported' in flat(rv)
   and 'lower bound on the earliest' in rv
   and 'not an upper bound on how late' in rv)
ck('unsupported numerical-impossibility claim absent in both bodies',
   'No computation at a reachable height' not in td
   and 'no computation at a reachable height' not in rv
   and 'why the radius cannot be attacked' not in td)
figsrc=(ROOT/'qa/figsrc/fig_last_unit.py').read_text()
ck('Figure 14 source annotation is an error bound rather than impossibility',
   'prove a computational limitation' in figsrc
   and 'cannot be attacked numerically' not in figsrc)
ck('PF criterion does not import unrelated finite statuses',
   'No transfer to these' in rv and 'finite-minor statuses are not assigned' in flat(rv))
ck('constant absolute no-go distinguished from linear growth',
   r'\|\mathsf Z_N\|_{\mathrm{op}}=\Theta(N)' in td
   and 'rank-independent absolute bound is impossible' in td
   and 'Neither conclusion rules out degree-dependent absolute bounds' in td)
ck('finite one-sided theorem includes proved compact-support step',
   'Hamburger theorem' in td and 'proves compact support' in td
   and r'\tag{155D.3}' in td)
ck('exact growth proof handles tied points, variable phase and tail',
   'annihilates all other maximizing points' in td
   and r'Choose $\phi_n$' in td and r'$O(r_1^{2n})$' in td)
ck('all-rate matrix estimate names cofinal-rank and rate quantifiers',
   r'\tag{155D.11}' in td and 'fixed unbounded sequence of ranks' in td
   and 'not its enumeration index' in td)
ck('compensation is retained and bounded rather than deleted',
   r'125\delta N^2' in td and r'\mathcal D[p]=\delta\mathcal H[p]+\mathcal E[p]' in td)
ck('curvature retains initial data and ordinary Laguerre parameter',
   r'\mathcal E_0=\mathcal E_1=0' in td
   and r'L_{n+1}^{(0)}' in td and r'\tag{155E.1}' in td)
ck('scalar rate is a signwise limsup, not an eventual lower bound',
   r'\tag{155E.6}' in td and 'limsup statements, not eventual signed lower bounds' in td)
ck('curvature generating function has regularization and genuine residue',
   r'H_{\rm reg}' in td and r'\tag{155E.4}' in td and r'\tag{155E.5}' in td)
ck('progression theorem states pole-angle noncollision condition',
   r'h\Theta_H<\pi' in td and 'Raising these poles' in td
   and 'injective' in td and r'\tag{155E.11}' in td)
ck('progression proof preserves both signs and actual stride exponent',
   r'=\mathfrak L^h' in td and r'I_{hm+a}' in td
   and 'same is true with $I$ replaced by $-I$' in td)
ck('parity criterion retains carried-height qualification and collision control',
   r'\tag{155E.12}' in td and 'not a fresh zero' in td
   and r'$(1+16z^2)^{-1}$' in td and 'does not extend to arbitrary sparse' in td)
ck('cosine basis preserves exceptional first row and compensation',
   r'J_0=0' in td and r'\widetilde{\mathsf E}_{00}=0' in td
   and r'\delta I_d+\widetilde{\mathsf E}_d' in td
   and 'not an orthonormal basis for the reserve' in td)
ck('full admissible direct recovery and base-five schedule are scoped',
   r'\lfloor N/2\rfloor' in td and r'\tag{166E.9}' in td
   and 'Independent observation' in td)
ck('base-thirteen is a separate whole-row theorem',
   r'13^{N+1}' in td and r'\tag{166D.4}' in td
   and 'full-row' in td and 'Neither base nor disk is asserted optimal' in td)
ck('mixed-block bound retains exact finite-rank Sigma',
   r'\Sigma_d=\frac9{128}(9^d-9^{-d})+\frac{3d}{8}' in td
   and r'125\Sigma_d' in td)
ck('Cauchy theorem uses a holomorphic disk neighborhood',
   'Let $f$ be holomorphic' in td and r'neighborhood of $|x-2|\le3/4$' in td)
ck('positive-scale cutoff retains full completion and error sign',
   r'S_X(x)=\frac1x+G(x)-P_X(x)' in td
   and r'\mathsf D_{2,d}-\widehat{\mathsf D}_{2,d}=K_{2,d}[P-P_{X_d}]' in td)
ck('cutoff targets its own scale without claiming boundary transfer',
   r'X_d=5^{2d-1}' in td and 'bypasses a boundary transfer' in td
   and 'not an identification with the' in td and 'need not be monotone' in td)
ck('compensated and cutoff source inequalities remain unproved',
   'No source proof of the displayed upper estimate' in td
   and 'No upper bound in (166F.8) is proved' in td
   and 'Neither estimate is' in td)
ck('four distinct 3003 positions are stated without double-counting',
   r'\binom{3003}{1}=\binom{78}{2}=\binom{15}{5}=\binom{14}{6}=3003' in rv)
ck('operator-monotone equivalence is within the nonnegative class',
   'nonnegative functions' in rv or 'nonnegative function' in rv)
pr=json.loads((ROOT/'qa/PRESERVATION_V43.json').read_text())
ck('complete 171-entry grid asset including seed is unchanged',pr['grid']['byte_identical'] and pr['grid']['expected_cells']==171)
ck('every inherited untagged displayed formula is preserved',
   all(not pr[k]['changed_or_removed_untagged_displays'] for k in ('reading','dossier')))
ck('every inherited numbered displayed formula is preserved',
   not pr['reading']['changed_numbered_displays']
   and not pr['dossier']['changed_numbered_displays'])
ck('preservation report bound to final sources',
   all(pr[k]['new_source_sha256']==sha(ROOT/r['source'])
       for k in ('reading','dossier') for r in rows if r['tag']==k))
# Ten executed finite audits; counts are coverage, not independent proofs.
audit_specs=[
 ('WEIGHTED_RESULTANTS.json','audit_weighted_resultants.py','total_checks',30519),
 ('COMMON_SOURCE.json','audit_common_source_recovery.py','total_checks',1684),
 ('INTEGRATED_BRIDGES.json','audit_integrated_bridges.py','exact_checks',459),
 ('SINE_BRIDGE.json','audit_sine_bridge.py','exact_checks',1435),
 ('LIGHTHOUSE_TIEOUT.json','audit_lighthouse_tieout.py','exact_assertions',3841),
 ('BLUE_SHARPENING.json','audit_blue.py','total_assertions',17976),
 ('ORANGE_CURVATURE.json','audit_orange.py','total_assertions',9787),
 ('GREEN_BLUE_MERGE.json','audit_green_blue.py','total_assertions',7685),
 ('GREEN_ORANGE_COMPARISON.json','audit_green_orange.py','total_assertions',982),
 ('CURVATURE_PROGRESSIONS.json','audit_curvature_progressions.py','total_assertions',837)]
for fn,script,key,count in audit_specs:
    j=json.loads((ROOT/'qa'/fn).read_text())
    ck(f'fresh finite audit bound: {script}',j[key]==count and j['script_sha256']==sha(ROOT/'qa'/script),count)
rc=json.loads((ROOT/'qa/RECONCILIATION_INTEGRITY.json').read_text())
ck('reconciliation archive payloads hash and size verified',rc['passed']==rc['total'] and rc['total']>0,rc['total'])
replicas=json.loads((ROOT/'qa/AUDIT_RECEIPT_COMPARISON.json').read_text())
ck('replayed finite receipts match their input receipts byte for byte',all(x['identical'] for x in replicas),len(replicas))


# v4.3 integration gates: new source and approximation results retain their scopes.
for sec in ('155F','155G','155H','155I','166G'):
    ck(f'v4.3: section {sec} appears exactly once',len(re.findall(r'^## '+sec+r'\.',td,re.M))==1)
ck('v4.3: Reader arithmetic continuation integrated into the main sequence',
   len(re.findall(r'^## R17I\.',rv,re.M))==1 and all(r'\tag{DIV.'+str(i)+'}' in rv for i in range(1,5)))
ck('v4.3: raw cutoff and finite boundary polynomial remain different objects',
   r'\widehat S_d' in td and r'L_d=15d-1' in td and r'X_d=8^{15d}' in td
   and 'The raw cutoff $S_X=1/x+G-P_X$ has an uncancelled origin pole' in td
   and 'evaluates a finite Taylor polynomial at zero' in flat(td))
ck('v4.3: completed Taylor disk uses carried height, not an RH assumption',
   r'23/8' in td and r'16\lambda_1<1' in td and 'carried low-height exclusion' in td
   and 'not RH or an unknown positive folded measure' in flat(td))
ck('v4.3: both analytic boundary reconstruction errors remain in the bound',
   r'\tag{166G.4}' in td and r'\tag{166G.5}' in td and r'36\,18^{15}<23^{15}' in td)
ck('v4.3: full boundary matrix and independent coefficient error are included',
   r'\tag{166G.6}' in td and r'\tag{166G.10}' in td and 'Independent' in td)
ck('v4.3: no actual boundary source upper bound is claimed',
   'No bound in (166G.10) is proved from the arithmetic source' in flat(td))
ck('v4.3: direct curvature cutoff retains polynomial counterterm and negative endpoint',
   r'L_{k+1}^{(-2)}(U)' in td and r'-e^{-U}M(U)L_k^{(-1)}(U)' in td)
ck('v4.3: PNT real-variable cutoff and Taylor cutoff are explicitly distinct',
   'existence constants' in td and r'U_K' in td and 'much larger than the exponential-in-rank Taylor cutoff' in flat(td))
ck('v4.3: denominator coefficients are named separately from Beta weights',
   r'b_n^{\rm den}' in td and 'Beta' in td and r'\mathcal B(z)' in td)
ck('v4.3: denominator convolution retains all three signed terms',
   r'-(n+2)b_{n+2}^{\rm den}' in td and r'(2n+\gamma_E+1)b_{n+1}^{\rm den}' in td
   and r'(1-n)b_n^{\rm den}' in td)
ck('v4.3: negative denominator coefficient is not called a negative Li coefficient',
   'not a negative Li coefficient or Widder rung' in flat(td) and '-0.00127046270166113994821' in td)
ck('v4.3: square-energy and absolute coefficient contraction are distinguished',
   r'\log(2\pi)-\gamma_E' in td and r'\sum_{n\ge1}|b_n^{\rm den}|=\infty' in td)
ck('v4.3: prime-supported model keeps its finite prefix and is not actual zeta data',
   r'p\le P' in td and '$s_0=3/4+2i$ and its conjugate' in td and 'but not the actual divisor law or completion' in flat(td)
   and 'It is not a counterexample to RH' in flat(td))
ck('v4.3: exact divisor relation retains both subtraction terms',
   r'\log(N!)-XH_N+N' in td and r'\Lambda*1=\log' in td)
ck('v4.3: floor-sum norm requires balance and preserves its cross terms',
   r'\sum_dc_d/d=0' in td and r'\tag{155H.2}' in td and 'The square follows the signed divisor sum' in td)
ck('v4.3: Mellin transform and Plancherel normalization are both present',
   r'\frac{1-\zeta(s)D_c(s)}s' in td and r'|E_c(1/2+it)|^2' in td)
ck('v4.3: prefix condition gives exact initial cancellation and the zero lower bound',
   r'$c_d=\mu(d)$' in td and r'$h_c(x)=0$ for $1\le x<K+1$' in td
   and r'\frac{2\sigma-1}{|\rho|^2}(K+1)^{2\sigma-1}' in td)
ck('v4.3: subpower sufficient target is not a converse for arbitrary approximants',
   r'\tag{155H.6}' in td and 'No converse is asserted' in td
   and 'below every positive power' in td)
ck('v4.3: unconditional linear estimate and failed primitive product remain below the target',
   r'\mathscr N(c^{(K)})\le4(K+1)' in td and r'\frac{P^{1/3}}{18e^2}' in td
   and 'not an exact-prefix family' in td)
ck('v4.3: removable denominator quotient and its center value are explicit',
   r"\mathcal C_c(0)=D_c'(1)" in td and "$1-D_c'(1)$, not $1$" in td)
ck('v4.3: Hardy identity keeps completeness and signed convolution',
   r'\tag{155I.2}' in td and 'completeness' in td and 'convolution' in td)
ck('v4.3: prefix norm-preserving multiplier is scoped to vanishing support',
   'not a bounded multiplier on arbitrary' in flat(td))
ck('v4.3: finite coefficient sums are lower bounds, not omitted-tail upper certificates',
   'lower bound' in td and 'upper tail' in td)
ck('v4.3: common bibliography numbering 79 and 80 renders in both documents',
   all('79. H. L. Montgomery' in ''.join(fitz.open(ROOT/r['pdf'])[i].get_text() for i in range(r['body_pages']-8,r['body_pages']))
       and '80. Elaissaoui' in ''.join(fitz.open(ROOT/r['pdf'])[i].get_text() for i in range(r['body_pages']-8,r['body_pages'])) for r in rows))
newledger=json.loads((ROOT/'qa/new_returns_replay/REPLAY_RESULTS.json').read_text())
ck('v4.3: all eight new returns audits freshly executed and receipts matched',
   len(newledger)==8 and all(r['exit_code']==0 and r['byte_identical_to_reference'] for r in newledger))
ck('v4.3: new return receipts and script copies bind to their recorded inputs',
   all(sha(ROOT/'qa/new_returns_replay'/r['receipt'])==r['output_sha256']
       and sha(ROOT/'qa/new_returns_replay'/r['script'])==sha(ROOT/'provenance/v43/accepted_returns/scripts'/r['script']) for r in newledger))
ck('v4.3: combined publication stays within the inherited 398-page ceiling',
   sum(r['pages'] for r in rows)<=398,sum(r['pages'] for r in rows))

result={'status':'PASS' if all(z['passed'] for z in checks) else 'FAIL','passed':sum(z['passed'] for z in checks),'total':len(checks),'scope':'Hard build and publication gates; legacy advisory kept separately; not a proof audit.','checks':checks,'asset_bindings':assets,'source_pdf_bindings':rows}
(ROOT/'qa/PUBLISHING_GUARD.json').write_text(json.dumps(result,indent=2)+'\n')
print(f"{result['status']}: {result['passed']}/{result['total']} hard publication gates")
for z in checks:
    if not z['passed']:print('FAIL',z['name'],z['detail'])
sys.exit(0 if result['status']=='PASS' else 1)
