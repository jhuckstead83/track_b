---
title: "Triangular-n Postmaster: From the Triangular Primitive to the Completed Source Frontier"
subtitle: "Volume I — The Reading Volume -- v5.2"
author:
  - "Jeffery Huckstead"
  - "ORCID 0009-0007-0234-2177"
  - "Cerebral Graphix"
date: "September 2026"
lang: en-US
fontsize: 11pt
toc: true
toc-depth: 2
---

\newpage

# Abstract

The triangular primitive $T_n=n(n+1)/2$ becomes a reflection-invariant
coordinate after centering at the half-step. Its analytic continuation gives
$q=s(1-s)=-2T_{s-1}=1/4-(s-1/2)^2$. This volume follows that coordinate from
finite arithmetic into the completed Riemann function, its folded resolvent,
and the exact positivity criteria it supports. Throughout,
$[\rho]=\{\rho,1-\rho\}$ is one functional-equation reflection orbit with
multiplicity $m_\rho$: an off-line quartet supplies two conjugate folded
nodes, not one full-symmetry state. The reciprocal coordinate $1/q$ retains
the folded node; taking a real part is a separate operation and is not part
of this fold.

The central identities express every reduced Widder rung as one finite row
of the signed Pascal triangle and connect the folded moments to Li's
coefficients. The inherited source ledger establishes the first six rungs,
analytically at $W_1$ and by the bundled v5.0 interval certificates at
$W_2$--$W_6$. A separate verified-height argument establishes a much longer
finite prefix. Neither channel supplies the all-order quantifier.
The all-node inequality $L_\Gamma-L_P\succeq0$, the next independent source
rung $W_7$, and the stated source-energy and exact-divisor bounds retain
their distinct open obligations. The Riemann hypothesis is not proved here.

Version 5.2 adds a calibration. A Dirichlet series with the reflection
$F(s)=F(1-s)$ of $\xi$, a different Gamma factor and no Euler product passes
every computed rung through $k=16{,}588$ and fails at $k=16{,}589$ (Dossier
§69A). So a long finite rung prefix does not by itself rule out off-line
zeros. Two
firewalls proved in v0.3 are restored, and no inherited status changes.

# Start here

## A triangle you already know

Stack bowling pins. Count handshakes in a room. Add up $1+2+\cdots+n$.
The same numbers appear:

$$
1,\;3,\;6,\;10,\;15,\;21,\;28,\;36,\;45,\;55,\;\ldots
\qquad
\boxed{T_n=\frac{n(n+1)}{2}}
\tag{R.1}
$$

Two facts about them are usually met once and then walked past.

**The triangular numbers are a column of Pascal's triangle.** Not a
resemblance — an identity, and one Pascal knew [90]:

$$
\binom{k}{2}=\frac{k(k-1)}{2}=T_{k-1}
\tag{R.1a}
$$

Read Pascal's triangle down its third column and you are reading
$1,3,6,10,15,\ldots$ exactly. The next column over is the running
sum of *those*: $\binom{k}{3}=T_1+T_2+\cdots+T_{k-2}$.

**And they collide with the rest of the triangle in a way nobody can
fully explain.** The number $3003=T_{77}$ occupies four distinct positions
$\binom{3003}{1}=\binom{78}{2}=\binom{15}{5}=\binom{14}{6}=3003$.
Each of those four positions has a mirror copy, so
$3003$ occurs **eight** times in all. No integer is known to occur
more often, and whether any does is open (Singmaster's problem [89]).
\figref{fig:widder-grid} of this volume prints the row where that
happens.

![The familiar triangle, before any sign is attached. The tinted column is the triangular numbers themselves; the circled row is the one that makes $3003$ famous. Both features survive into the signed grid this volume actually uses.](figures/v32_pascal_teaser.png)

These are not decorations. This volume is about what one signed version
of that same triangle does when it is pointed at the Riemann zeta
function.

## Put a sign on it

Alternate the signs along each row:

$$
\boxed{c_{k,j}=(-1)^j\binom{k}{j}},
\qquad
\sum_{j=0}^{k}c_{k,j}z^{j}=(1-z)^{k}
\tag{R.1b}
$$

Row $k$ is nothing more exotic than the coefficient list of $(1-z)^k$.
Row $6$ reads $1,-6,15,-20,15,-6,1$. Every row is generated from the one
above it by a single subtraction, $c_{k+1,j}=c_{k,j}-c_{k,j-1}$, from the
seed $c_{0,0}=+1$. You can write row $17$ without computing rows $1$
through $16$. Nothing in this grid is hard, and nothing in it is
approximate.

## What each row is for

Zeta's zeros are hard to look at directly. Fold them. With
$q=s(1-s)$ — the same reflection $n\mapsto -n-1$ that centres $T_n$,
now on the complex plane — every zero $\rho$ of the completed function
$\xi$ becomes a single point $q_\rho$, and its mirror partner
$1-\rho$ lands on top of it. Build the resolvent of that folded set,

$$
S_\xi(x)=\sum_{[\rho]}\frac{m_\rho}{x+q_\rho},
\qquad
Z_r(x)=\sum_{[\rho]}\frac{m_\rho}{(x+q_\rho)^{r}}
\tag{R.1c}
$$

so $Z_1=S_\xi$ and each $Z_r$ is one more derivative of it; the sum runs over
folded zero orbits $[\rho]$ with multiplicity $m_\rho$ (§R10).

Now the point of the grid. Define the $k$-th **rung**

$$
\boxed{
W_k(x)=(-1)^{k-1}D_x^{2k-1}\bigl[x^{k}S_\xi(x)\bigr]
=(2k-1)!\sum_{[\rho]}m_\rho
\left(\frac{q_\rho}{(x+q_\rho)^{2}}\right)^{k}}
\tag{R.3}
$$

and row $k$ of the signed triangle is exactly its recipe, the identity
(SW.4b) established in §R12A:

```{=latex}
\begin{tnclosed}{Every rung is a finite row of the grid}
```
$$
\frac{W_k(x)}{(2k-1)!}
=\sum_{j=0}^{k}c_{k,j}\,x^{j}Z_{k+j}(x)
=Z_k-kxZ_{k+1}+\binom{k}{2}x^{2}Z_{k+2}-\cdots
$$
```{=latex}
\end{tnclosed}
```

This is an identity, not an approximation and not a truncation. The rung
$W_k$ is a $(k+1)$-term combination of consecutive derivatives of one
function, and the coefficients are read straight off row $k$. The
grid is not computationally irreducible, and no simulation is hiding in it.

## Why zeta cares

Look at the right-hand side of (R.3). It is a sum of $k$-th powers of one
quantity, the **carrier** (11.1) of §R11,

$$
u_x(q)=\frac{q}{(x+q)^{2}}
$$

On the critical line $\Re s=1/2$ the carrier is a squared modulus, so
$u_x\ge0$ and every power of it is nonnegative. Off the critical line it
need not be, and its powers can rotate. Widder's characterization of
Stieltjes functions [16, 115] converts the whole family into an exact statement
with nothing left over:

```{=latex}
\begin{tnequiv}{Exact criterion}
```
$$
\boxed{\mathrm{RH}\iff W_k(x)\ge0
\ \text{ for every }k\ge1\text{ and every }x>0}
\tag{R.4}
$$
```{=latex}
\end{tnequiv}
```

So the Riemann hypothesis, in this volume's coordinates, reads:

> Does every row of a signed Pascal triangle, applied to the derivatives
> of one explicit function, come out nonnegative?

Both quantifiers are load-bearing. **No finite collection of rungs is an
RH statement.** Nothing in this volume promotes one, and every place a
finite result could be mistaken for the full one is marked.

## Where this work sits in the classical literature

Most of the machinery in this volume is classical, and the argument depends on
that. The table maps each layer to its classical sources and states what this
volume adds. "Adds" means a construction, an exact identity in the volume's
coordinates, a certificate or a NO-GO theorem. It is not a claim of priority.
No systematic MathSciNet or zbMATH search has been made, so read every entry in
the last column as "proved or organized here," not as "new."

| layer (sections) | classical sources | what this volume adds |
|------------------|---------------------------|----------------------------------------|
| Triangular numbers, Pascal's column, power sums (§§R1--R3) | Nicomachus [83]; Pascal [90]; Faulhaber [84]; Jacobi [85]; Knuth [86]; Singmaster [89] | one chart for the mirror $n\mapsto-n-1$ ($T_n$ fixed, $j_n\mapsto-j_n$); the adjacent-pair identities (TDP.1)--(TDP.5); the factorial diagonal defect |
| Reciprocal triangular numbers and the Basel sum (§R4) | Mengoli [91]; Euler [92]; Hausdorff [19, 20] | the dyadic telescope; the moment (Hausdorff and Hankel) reading of $1/T_k$ |
| Euler's constant (§R4A) | Euler [93]; Stirling [94]; Raabe [95]; Cesàro [96]; Ramanujan [119], with Villarino and Chen [97--99]; DeTemple and Wang [100, 120]; Boya [101]; Nyman and Beurling [106, 107] | the mirror explanation of Ramanujan's expansion; four readings of $\log2\pi-\gamma_{\mathrm E}$; a simplex ladder |
| Completion and folding (§§R6--R9A) | Riemann [74]; Hadamard [110]; von Mangoldt [111]; Davenport [112]; Edwards [118] | the folded coordinate $q=s(1-s)=-2T_{s-1}$ as the working variable; genus zero in $q$ |
| Stieltjes, Bernstein and heat representations (§§R10--R10B) | Stieltjes [113]; Bernstein [114]; Schilling, Song and Vondraček [23] | explicit positive realizations of the folded resolvent; the heat defect left by an off-line zero |
| The rung criterion (§§R11--R14) | Widder [16, 115]; Hausdorff [19, 20]; Pringsheim [21]; Platt and Trudgian [42] | each rung is one row of the signed Pascal triangle (SW.4b); the height-to-sector theorem; computer-assisted source certificates for $W_2$--$W_6$ |
| Li coefficients and Löwner matrices (§§R15--R17E) | Li [4]; Keiper [58]; Bombieri and Lagarias [5]; Löwner [22]; Dobsch [43]; Donoghue [44] | the central-Pascal boundary dictionary; the Gamma/prime Löwner split and the limits of that split |
| Energy, cutoffs and exact divisors (§§R17F--R17I) | Nyman [106]; Beurling [107]; Báez-Duarte and coauthors [25, 108, 109]; M. Riesz [24]; Eisenberg [60] | the completed Bernstein row and its energy; exponential cutoff theorems; the taper exponent (DIV.3a) |
| Explicit formula and reflection (§§R18--R21B) | Weil [116]; Connes and coauthors [48--50] | the reflection-contour normal form; the one-node strict defect; why stationary symbols are blind |
| Limits of the approach (§R25) | — | an unconditional NO-GO ledger |

Every row keeps the status tags of its own sections. A classical source is
cited for what it proves. It is never cited as evidence for the Riemann
hypothesis.

## Master status key — where this volume actually stands

This is the **single status key for the Reading Volume and Dossier**. Later
\PROVED{}, \CERT{}, \EQUIV{}, \EVID{} and \OPENSTAT{} tags stand on their own
and refer back here; the legend is not repeated elsewhere.

\statuslegend

| the claim | status |
|---|---|
| Every rung is a finite row of the grid, (SW.4b) | \PROVED{} closed form |
| $\mathrm{RH}\iff W_k\ge0$ for all $k\ge1,x>0$, (R.4) | \EQUIV{} |
| $W_1,\ldots,W_6>0$ for all $x>0$, from the source | \PROVED{} analytic ($W_1$); \CERT{} A-CAT through $F^{(12)}$ ($W_2$--$W_6$) |
| $W_k>0$ for all $x>0$, every $k\le4{,}712{,}664{,}392{,}502$ | \CERT{} verified-height channel |
| $4x-1<R_x$ at every fixed scale, (13A.2); $\Delta<1$ is *not* proved | \PROVED{} analytic, pointwise in $x$ |
| $W_7\rightsquigarrow F^{(14)}$ from the independent source | \OPENSTAT{} |
| $W_k>0$ for all $x>0$, every $k\ge1$ | \OPENSTAT{} |
| $L_\Gamma-L_P\succeq0$ on every finite node set, (23.1) | \EQUIV{} \OPENSTAT{} |
| $\mathscr E_N[P](2)\le5$ for every degree $N$, (166B.12a) | \EQUIV{} \OPENSTAT{} |
| A real finite test sees an off-line folded pair only at second order, (TW.1) | \PROVED{} |
| The functional-equation twin of Dossier §69A fails some Widder rung | \PROVED{} |
| Twin rungs positive through $k=16{,}588$ where computed; $W_{16589}<0$; Löwner failure first at $N=105$ (exact, best tested centre) | \EVID{} |

**Where the certificates are.** The five certified source rungs rest on one
certificate, bundled with this edition and re-executed by the v5.0 build on two
independent arithmetic backends (Dossier §74A). The enclosures of $q_1$, $q_2$
and $\lambda_1$ printed in §R12 were recomputed by that v5.0 build (Dossier
§96A.5). The verified-height row uses the external input named in §R13.
Software versions, precisions and run dates belong to the package's QA receipt
and are not carried in the text.

**How far the criterion has been checked — and why that is not progress.**
The $K_H$ row is not a sample. Section R13 proves that if every zero up to a
height $H$ lies on the critical line, then every rung with index at most
$\lfloor\pi/(2\arctan(1/H))\rfloor$ is positive at every $x>0$. Platt and
Trudgian's verified height puts the lowest $12{,}363{,}153{,}437{,}138$ zeros
on the line, and the resulting index, exact at (13.6), is

$$
\boxed{K_H=4{,}712{,}664{,}392{,}502}.
$$

Thus (R.4) holds for the first four and a half trillion rungs, and the first
**six** also have an independent source certificate. It is still not evidence
for RH: (R.4) quantifies over every $k$, and a larger verified height only makes
a finite prefix larger.
The live pair is
$$
\boxed{W_7\rightsquigarrow F^{(14)}\qquad\text{and}\qquad
L_\Gamma-L_P\succeq0\ \text{on every finite positive node set}.}
\tag{R.2}
$$
The first is the next scalar source rung; the second is RH-equivalent.
They are not equal in reach. The Davenport–Heilbronn function has the
reflection $F(s)=F(1-s)$ of $\xi$ with a different Gamma factor, no Euler
product, and zeros off the line. By the argument behind (R.4), some rung of its ladder fails. \PROVED{}
Computed, it passes $W_7$ and every rung through $W_{16588}$ and first fails
at $W_{16589}$ (Dossier §69A). \EVID{} So a proof of $W_7$ extends a finite
prefix that this twin also passes. The reason is exact. A real test at real
nodes sees an off-line pair only at second order in its displacement, (TW.1).
The second line's finite sections detect the twin, but only at about a
hundred nodes (first failure $N=105$ at the best tested centre) and with deciding eigenvalues
near $10^{-141}$. By the
fitted detection scale (TW.3), an off-line zeta zero just above the verified
height would first break the ladder near $k\sim10^{27}$, far beyond $K_H$.


## The live frontier: one line per route

What remains is **one line per route, and no reduction between the routes is
known**. Section R23 lists the live targets and marks each one as equivalent,
sufficient, or necessary. The principal matrix route asks for

$$
\boxed{L_\Gamma-L_P\succeq0\quad\text{for every finite positive node set}.}
$$

Here $L_\Gamma$ and $L_P$ are the Gamma and prime Löwner blocks built in
§§R16–R17E. That inequality is RH-equivalent, but it is not proved to subsume
the distinct curvature, fixed-scale energy, or exact-divisor routes. The
unconditional implications actually known between targets are recorded in the
lattice at §R12; Part VIII collects the routes that have been closed by NO-GO
theorems.

# Reader's study spine

> **Why read this.** Triangular coordinates lead to the completed source of
> the Riemann zeta function, to exact criteria stated in that coordinate, and
> to the proof obligations that remain. The Riemann hypothesis remains open.

![The reading map for this volume. Arrows give the reading order, not an implication from a finite certificate to RH. Section R12 controls the rung status; §R23 states the all-node frontier.](figures/v32_triangular_root_map.png)

## How to read this volume

The work is published in two documents: this **Reading Volume**, the
continuous argument in reader sections §R1–§R25 across Parts I–VIII, and the
**Technical Dossier**, the proofs, certificates and empirical context in plain
numbered sections with lettered insertions; see §R24. **A number without an R is in the Dossier.**
Equation tags are global, so (SW.4b) and (166C.25) name the same equations in
both. Every reader section states its own quantifiers, and this volume can be
read straight through before the Dossier is opened.

The dependency route is root to frontier: triangular coordinate → fold and
completion → Widder/Hausdorff rungs → Li/Löwner source split → source energy and
exact-divisor residual → reflection defects → the live targets of §R23 and the
NO-GO ledger of §R25. The section-level map is printed once, in §R24.

**What changed in v5.2.** Dossier §§69A–69C add a functional-equation
twin, the parity lemma (TW.1), a local Gaussian form (TW.2) and a measured
detection law (TW.3), and restore two firewalls proved in the v0.3 edition.
Here the live pair (R.2) is ranked by reach, §R25 gains two rows, and
reference [66] is corrected. No inherited status changed. The v5.0
certificates of §74A were not re-executed for this revision; earlier
version notes are kept in the package provenance.

**How to cite.** Use the concept DOI
[10.5281/zenodo.21968915](https://doi.org/10.5281/zenodo.21968915), which
always resolves to the newest version, and name the version you read.


## Notation visible at every analytic interface

The Riemann variable will never be allowed to hide its two real axes:

| role | notation | exact reading |
|---|---|---|
| point | $s$ | $s=\sigma+it$ |
| reflection | $1-s$ | $(1-\sigma)-it$ |
| conjugate | $\bar s$ | $\sigma-it$ |
| reflected conjugate | $1-\bar s$ | $(1-\sigma)+it$ |
| folded coordinate | $q=s(1-s)$ | $\sigma(1-\sigma)+t^2+i\,t(1-2\sigma)$ |
| analytic triangular coordinate | $T_{s-1}=s(s-1)/2$ | $(\sigma^2-\sigma-t^2)/2+i\,t(\sigma-1/2)$ |
| safe real source branch | $s_x$ | $(1+\sqrt{1+4x})/2>1$ |
| source Jacobian | $R$ | $R=2s_x-1=\sqrt{1+4x}$ |
| integer odd coordinate | $j_n$ | $j_n=2n+1$ |
| rung odd coordinate | $j_k$ | $j_k=2k+1$ |

The symbols $s$, $\rho$, and $s_x$ distinguish an arbitrary point, a zero, and
the safe source branch by mathematical role. Reflection $s\mapsto1-s$ and
conjugation $s\mapsto\bar s$ coincide exactly on $\sigma=1/2$; identifying the
two off that line is the positivity problem of §R20.

## Working vocabulary

A few ordinary words carry a narrow technical meaning in this volume. Each is
defined once here.

| term | meaning in this volume |
|--------------|------------------------------------------------------------------|
| **mirror** | the involution $n\mapsto-n-1$; equivalently $u=n+\tfrac12\mapsto-u$, or $s\mapsto1-s$ |
| **fold** | the substitution $q=s(1-s)=-2T_{s-1}$, which sends $s$ and $1-s$ to one point; on integers it is $T_n=T_{-n-1}$ |
| **source** | the defining formula (9.5): the Gamma factor and the prime sum, evaluated where both converge, with no zero data |
| **source-side proof** | a proof that uses only the source, and never zero locations or verified heights |
| **zero-assisted** | a result that uses the rigorously verified location of finitely many zeros (§R13) |
| **rung** $W_k$ | the $k$-th Widder sign condition (R.3); all rungs together are equivalent to RH (R.4) |
| **carrier** | $u_x(q)=q/(x+q)^2$, whose powers the rungs sum (§R11) |
| **owner** | used mainly in the Dossier: the explicit object (a measure, kernel, matrix or derivative expression) that carries a quantity and from which its sign is read; "the owner of $W_7$ reaches $F^{(14)}$" means that the source expression for $W_7$ uses derivatives of $F(s)=(s-1)\zeta(s)$ through order fourteen |
| **rail** | a progression of distinguished points, such as the even-triangular rail $2T_{2n}$ of §R5C |
| **A-CAT** | a computer-assisted theorem: a rigorous finite certificate in interval arithmetic, joined to an analytic proof for the remaining range |
| **certificate of record** | the executable and receipt that establish a \CERT{} row; for the source rungs it is bundled with this edition and re-run by the v5.0 build |
| **firewall** | a proved statement that blocks a tempting but invalid inference |
| **NO-GO** | an unconditional theorem showing that a proposed route cannot work as stated |
| **frontier** | the first inequality on a route that is not proved |


\Needspace{18\baselineskip}

# Part I. The triangular coordinate

The triangular coordinate, its half-step reflection and its Pascal column
supply the arithmetic vocabulary for the analytic constructions that
follow. All identities in this Part stand independently of zeta zeros.

## R1. Discrete primitive and centered square

Triangular numbers integrate the integer sequence by one forward difference:

$$
T_n-T_{n-1}=n
\qquad
T_n=1+2+\cdots+n
\tag{1.1}
$$

A square displays both triangular copies at once. Split an
$(n+1)\times(n+1)$ grid into the entries above the diagonal, the entries
below it, and the diagonal itself:

$$
\boxed{2T_n+(n+1)=(n+1)^2
\qquad T_n+T_{n+1}=(n+1)^2}
\tag{SQ.1}
$$

The two strict triangular halves each contain $T_n$ cells, and the
shared diagonal contains $n+1$. The border ending at $n^2$ and the
border beginning there are consecutive members of one odd sequence:

$$
\boxed{n^2-(n-1)^2=2n-1,\qquad (n+1)^2-n^2=2n+1}
\tag{SQ.2}
$$

Summing the first identity gives $n^2=\sum_{k=1}^n(2k-1)$.
Equivalently $n^2=T_{n-1}+T_n$; taking successive differences of
this adjacent-triangle identity gives the same borders. Thus $2n-1$
and $2n+1$ describe the incoming and outgoing layers at the same square,
with the index shift stated explicitly.

![A 10 by 10 square splits into two 45-cell triangles and a 10-cell diagonal: $2T_9+10=100$. The diagonal is counted once. This exact counting diagram also prepares the reflected index pairs used later in matrices.](figures/v27_square_diagonal.png)

Introduce the centered odd coordinate

$$
j_n:=2n+1
\tag{1.2}
$$

Then

$$
\boxed{8T_n+1=j_n^2,\qquad
T_n=\frac{j_n^2-1}{8}
=\frac12\left(n+\frac12\right)^2-\frac18}
\tag{1.3}
$$

The reflection $n\mapsto-n-1$ becomes $j_n\mapsto-j_n$ while $T_n$ is
fixed. Thus $T_n$ is the invariant coordinate and $j_n$ is its signed sheet
coordinate. This is the elementary model for the analytic fold used later.
In particular the two border counts in (SQ.2) are $j_{n-1}$ and $j_n$.
Their squared difference recovers the primitive exactly:
$j_n^2-j_{n-1}^2=8(T_n-T_{n-1})=8n$.
The same mirror reflects the completed function in §R9, and §R4A gives it a
third role: it is a parity of the harmonic numbers, which is why Ramanujan's
expansion of $H_n$ is a series in $1/T_n$.

The paper will keep three exact readings beside one another whenever doing so
exposes structure rather than adding notation:

| mainstream form | triangular form | centered form |
|---|---|---|
| $n(n+1)$ | $2T_n$ | $(j_n^2-1)/4$ |
| $n+(n+1)$ | $T_{n+1}-T_{n-1}$ | $j_n$ |
| $n\mapsto-n-1$ | $T_n\mapsto T_n$ | $j_n\mapsto-j_n$ |

This “three-language line” is an editorial convention, not a claim that every
formula becomes simpler after triangularization.

![Triangular numbers are the discrete primitive; centering at the half-step turns reflection into a sign change.](figures/triangular_primitive.png)

## R1A. The general discrete primitive and its reflection

The same polynomial identities hold for real or complex inputs. Define

$$
T_x=\frac{x(x+1)}2,\qquad j_x=2x+1
$$

Then

$$
T_x-T_{x-1}=x,\qquad
T_{x+1}-T_x=x+1,\qquad
\Delta^2T_x=1
$$

while the adjacent sum is

$$
\boxed{T_x+T_{x-1}=x^2}
\tag{TDP.1}
$$

Factoring through the primitive difference gives the cubic identity

$$
\boxed{
T_x^2-T_{x-1}^2
=(T_x-T_{x-1})(T_x+T_{x-1})=x^3
}
\tag{TDP.2}
$$

The same adjacent pair also resolves the square index:

$$
\boxed{T_{x^2}=T_{x-1}^2+T_x^2}
\tag{TDP.3}
$$

Indeed, the right side is
$x^2((x-1)^2+(x+1)^2)/4=x^2(x^2+1)/2$.

The forward adjacent product and its reflection can be kept on one line:

$$
\boxed{
2T_x=(T_x-T_{x-1})(T_{x+1}-T_x),\qquad
T_{-x-1}=T_x}
\tag{TDP.4}
$$

With $j_x=2x+1$, the centered sheet coordinate is visible without a new symbol collision:

$$
\boxed{
T_x=\frac{j_x^2-1}{8}
=\frac12\left(x+\frac12\right)^2-\frac18}
\tag{TDP.5}
$$

Thus the half-shift and the value $-1/8$ are not numerical coincidences.  They
are the split-norm coordinates of two consecutive counting legs.

More generally, for a fixed gap $D\ge0$,

$$
x(x+D)=\left(x+\frac D2\right)^2-\left(\frac D2\right)^2
$$

This is the common null-coordinate grammar behind the Casimir square,
complementary phase states, and reciprocal uniformization.  It is a scalar
grammar; a shared operator must still be proved separately in each family.


The square-index recurrence and the two Pell constructions are proved in
Dossier §5 (Theorems TDP-A–TDP-C); the identities above are the algebraic
reference used below.

## R2. Odd and even power sums

Let $S_p(n)=\sum_{k=1}^n k^p$. Reflection about $n=-1/2$ forces the
classical Faulhaber parity split [84--86]

$$
\boxed{
S_{2m+1}(n)=P_m(T_n),\qquad
S_{2m}(n)=j_nQ_m(T_n),\qquad j_n=2n+1}
\tag{2.1}
$$

for polynomials $P_m,Q_m$, with $m\ge0$ in the odd formula and
$m\ge1$ in the even formula. The case $S_0(n)=n$ is excluded from the
even formula. The first examples are

$$
\begin{aligned}
S_1&=T_n
&S_2&=\frac{j_nT_n}{3}=\frac{(2n+1)T_n}{3}\\
S_3&=T_n^2
&S_4&=\frac{j_nT_n(6T_n-1)}{15}\\
S_5&=\frac{T_n^2(4T_n-1)}3
&S_6&=\frac{j_nT_n(12T_n^2-6T_n+1)}{21}
\end{aligned}
\tag{2.2}
$$

The square-sum formula follows from these same adjacent quantities,
without a separate counting hypothesis. Set $A(n)=j_nT_n$. Then

$$
A(n)-A(n-1)=(2n+1)T_n-(2n-1)T_{n-1}=3n^2
\tag{2.2a}
$$

Since $A(0)=0$, summation proves $3S_2(n)=j_nT_n$, which is the case $r=1$
of a product decomposition of Wituła and coauthors [87, (13)].
Factoring $T_n^2-T_{n-1}^2$ uses the same primitive difference $n$
and adjacent sum $n^2$, giving (2.3). The square and cube branches
therefore follow from one adjacent-triangle calculation.

In the half-step variable $u=n+1/2$, odd power sums are polynomials in
$u^2$ while even sums are $u$ times polynomials in $u^2$. The factor
$j_n=2n+1$ is therefore not an accessory: it records the odd sheet of the same
centered geometry.

The cubic identity, known to Nicomachus [83], is the cleanest instance:

$$
\boxed{T_n^2-T_{n-1}^2=n^3,\qquad
1^3+\cdots+n^3=T_n^2}
\tag{2.3}
$$

The same adjacent pair resolves a square-index triangular number:

$$
\boxed{T_{n^2}=T_{n-1}^2+T_n^2}
\tag{2.4}
$$

**Classical forms of the split.** Write $S_{2m+1}(n)=P_m(T_n)$ as in (2.1).
Faulhaber's inverse form [86] expresses the powers of $T_n$ through odd power
sums,

$$
2^{m-1}T_n^{\,m}=\sum_{j\ge1}\binom{m}{2j-1}S_{2m-2j+1}(n),
\qquad\text{for example}\quad T_n^2=S_3,\quad 4T_n^3=3S_5+S_3,
\tag{2.5}
$$

and the even sums follow by differentiation [86]:

$$
S_{2m}(n)=\frac1{2m+1}\,\frac{d}{dn}S_{2m+1}(n)
=\frac{n+\frac12}{2m+1}\,P_m'(T_n).
\tag{2.6}
$$

The factor $n+\tfrac12=dT_n/dn=j_n/2$ is the Jacobian of the triangular
chart; it returns as the source Jacobian $R=2s-1$ in (5.1). Inverting the
other way, $n^{p+1}=\sum_{j=0}^{p}(-1)^{p-j}\binom{p+1}{j}S_j(n)$: the matrix
that turns power sums back into powers is a signed Pascal triangle, the same
array that carries the rungs in (SW.4b). Derby [88] computes the power-sum
coefficients by inverting a matrix of Pascal rows.

## R3. Factorial switch and diagonal defect

The factorial form makes the triangular polynomial appear by exact
cancellation:

$$
\boxed{
\frac{(n+1)!}{2(n-1)!}
=\left(\frac{n!}{2}\right)
 \left(\frac{n+1}{(n-1)!}\right)
=\frac{n(n+1)}2=T_n}
\tag{3.1}
$$

The two-variable continuation

$$
F_\triangle(x,y)=\frac{\Gamma(y+2)}{2\Gamma(x)}
\tag{3.2}
$$

restricts to $T_x$ on the diagonal. At regular points with $T_x\ne0$,
its exact relative defect is

$$
\boxed{
\frac{F_\triangle(x,y)}{T_x}
=\frac{\Gamma(y+2)}{\Gamma(x+2)},\qquad
\frac{F_\triangle(x,x+\varepsilon)-T_x}{T_x}
=\varepsilon\psi(x+2)+O(\varepsilon^2)}
\tag{3.3}
$$

The reduced factor $(n+1)/(2(n-1)!)$ still carries the successor-prime
numerator gate before multiplication. After the factorial cancellation, the
whole expression is the integer $T_n$; the reduced-numerator signal is not a
separate invariant of the product.

## R4. Reciprocal triangular numbers as moments

The reciprocal triangle starts with Mengoli's telescope [91],

$$
\frac1{T_n}=\frac2{n(n+1)}
=2\left(\frac1n-\frac1{n+1}\right),
\qquad
\sum_{n\ge1}\frac1{T_n}=2.
\tag{4.1}
$$

The adjacent pair retains the centered coordinate $j_n=2n+1$:

$$
\frac1n-\frac1{n+1}=\frac1{2T_n},\qquad
\frac1n+\frac1{n+1}=\frac{j_n}{2T_n}.
\tag{4.2}
$$

Squaring and summing gives an exact bridge to Euler's Basel sum [92]

$$
\boxed{\sum_{n\ge1}\frac1{T_n^2}=8\zeta(2)-12,
\qquad
\zeta(2)=\frac32+\frac18\sum_{n\ge1}\frac1{T_n^2}.}
\tag{4.4}
$$

The cubic reciprocal identity needed later is

$$
\boxed{\sum_{n\ge1}\frac1{T_n^3}
=8-6\sum_{n\ge1}\frac1{T_n^2}
=80-48\zeta(2).}
\tag{4.4f}
$$

More generally, with
$R_m(n)=n^{-m}+(n+1)^{-m}$, the adjacent roots $1/n$ and $1/(n+1)$
give

$$
R_m(n)=\frac{j_n}{2T_n}R_{m-1}(n)
-\frac1{2T_n}R_{m-2}(n),
\qquad R_0=2,
\quad R_1=\frac{j_n}{2T_n}.
\tag{4.4b}
$$

Thus the higher reciprocal identities are one recurrence, not isolated
simplifications.  The distinction between reciprocating each term and
reciprocating a completed sum is retained throughout the volume.

Finally the reciprocal triangle is already a compact moment sequence:

$$
\boxed{\frac1{T_{k+1}}
=\int_0^1u^k\,2(1-u)\,du.}
\tag{4.5}
$$

This positive Hausdorff measure [19, 20] later supplies Hankel and Gram
models. It is an auxiliary triangular measure and must not be identified with
the signed Gamma or completed-zero measures. Section R4A uses the same moments
to reach Euler's constant.

## R4A. Euler's constant on the triangular coordinate

Euler's constant, $\gamma_{\mathrm E}=\lim_{n\to\infty}(H_n-\log n)=0.5772156649\ldots$
[93, 103], first appears in this volume inside the first Li coefficient (9.8).
It can already be seen in Part I. Three classical facts connect it to the
triangular coordinate, and each follows in a few lines from what Part I has
established. They also give a third reason for the mirror $n\mapsto-n-1$ of
(1.3). The mirror folds the index, and it reflects the completed function. It
is also a parity of the harmonic numbers.

Nothing in this section concerns where the zeros lie. The full proofs, the
coefficient tables and an interval-arithmetic replay are in Dossier §96A. Every
statement below is \PROVED{}. None is claimed as new; no priority search
beyond the cited literature has been made.

**The mirror in the harmonic numbers.** Put $u=n+\tfrac12=j_n/2$. By (1.3),
$2T_n=u^2-\tfrac14$, and the mirror is $u\mapsto-u$. The digamma expansion
with shift $\tfrac12$ [2, §5.11] involves only Bernoulli polynomials evaluated
at $\tfrac12$. Those of odd order vanish there, because
$B_k(1-x)=(-1)^kB_k(x)$. So once the logarithm is centered at
$\tfrac12\log(2T_n)=\tfrac12\log(u^2-\tfrac14)$, the harmonic numbers see only
even powers of $u$:

$$
H_n-\gamma_{\mathrm E}-\tfrac12\log(2T_n)\sim\sum_{m\ge1}\frac{c_m}{u^{2m}},
\qquad
c_m=\frac{(1-2^{1-2m})B_{2m}+2^{-2m}}{2m}.
\tag{GA.1}
$$

Since $u^2=2T_n+\tfrac14$, the right side is a series in $1/T_n$. It is
Ramanujan's expansion, Entry 9 of Chapter 38 in Berndt's edition of the
notebooks [119], with modern proofs and error bounds in [97--99]; its first two
terms go back to Cesàro [96].

```{=latex}
\begin{tnclosed}{Ramanujan's expansion, and why it is a series in $T_n$}
```
$$
H_n\sim\gamma_{\mathrm E}+\frac12\log(2T_n)+\frac1{12T_n}-\frac1{120T_n^2}
+\frac1{630T_n^3}-\frac1{1680T_n^4}+\cdots
\tag{GA.2}
$$
The mirror $n\mapsto-n-1$ fixes $T_n$, and it leaves this expansion unchanged.
```{=latex}
\end{tnclosed}
```

The mirror now appears in three roles: as the invariance of the folded index
(1.3), as the reflection $\xi(s)=\xi(1-s)$ with $T_{s-1}=T_{-s}$ (SC.2), and as
the parity of an asymptotic expansion. The half-integer approximation of
DeTemple and Wang [100, 120], which subtracts $\log(n+\tfrac12)$, is the same
parity with a differently centered logarithm, and Villarino derives (GA.2) from
it [97]. With
six terms, the error at $n=10$ is below $10^{-15}$ (\figref{fig:gamma-bridge}).

One warning. The first two coefficients equal $-\zeta(-1)$ and $-\zeta(-3)$,
but the third is $1/630$, not $-\zeta(-5)=1/252$. The pattern does not continue.

**A reciprocal-triangular zeta series.** By (4.5),
$1/T_k=\int_0^1u^{k-1}\,2(1-u)\,du$. The Taylor series
$\sum_{k\ge2}\zeta(k)u^{k-1}=-\gamma_{\mathrm E}-\psi(1-u)$ turns the sum over $k$
into one digamma moment, and Raabe's integral $\int_0^1\log\Gamma=\tfrac12\log2\pi$
[95] evaluates it:

$$
\boxed{\sum_{k\ge2}\frac{\zeta(k)}{T_k}=\log(2\pi)-\gamma_{\mathrm E}=1.2606614015\ldots}
\tag{GA.3}
$$

This is Boya's relation [101]; the ingredients are in Whittaker and Watson
[102, Ch. 12]. The
reciprocal generating function (94.3) gives a second proof, with an exact finite
form. For the truncated zeta function $\zeta_M(k)=\sum_{m\le M}m^{-k}$,

$$
\sum_{k\ge2}\frac{\zeta_M(k)}{T_k}=2M-H_M-2\log\frac{M^M}{M!}.
\tag{GA.4}
$$

Stirling's formula [94] and $H_M-\log M\to\gamma_{\mathrm E}$ then return (GA.3),
with error $-1/(3M)+O(M^{-2})$. Replacing every $\zeta(k)$ by $1$ gives
Mengoli's $\sum_{k\ge2}1/T_k=1$ [91].

**The same constant as a norm.** Term by term, (GA.4) is a sum of integrals
over unit intervals:

$$
\sum_{k\ge2}\frac{m^{-k}}{T_k}=\int_{m-1}^{m}\left(\frac{\{x\}}x\right)^2dx
\qquad(m\ge1).
\tag{GA.5}
$$

Now sum over $m$. For $0<\Re s<1$, Titchmarsh's formula [3, (2.1.5)], after the
substitution $x\mapsto1/x$, reads $\zeta(s)/s=-\int_0^\infty\{1/x\}x^{s-1}dx$, and
the Mellin--Plancherel theorem [117] applies on $\Re s=\tfrac12$. Together these
give four expressions for one constant:

```{=latex}
\begin{tnclosed}{one constant, four readings}
```
$$
\begin{aligned}
\log(2\pi)-\gamma_{\mathrm E}
&=\sum_{k\ge2}\frac{\zeta(k)}{T_k}
=\int_0^\infty\!\left(\frac{\{x\}}x\right)^{\!2}dx\\
&=\frac1{2\pi}\int_{-\infty}^{\infty}\frac{|\zeta(\tfrac12+it)|^2}{\tfrac14+t^2}\,dt
=\sum_{n\ge0}\bigl(b_n^{\rm den}\bigr)^2.
\end{aligned}
\tag{GA.6}
$$
```{=latex}
\end{tnclosed}
```

The weight $\tfrac14+t^2$ is the folded coordinate $q=s(1-s)$ on the critical
line (9.2). The fractional-part function is the one in the Nyman--Beurling
approximation problem [106--108]. The last expression is the denominator norm of
§R17I, where the same constant returns. (GA.6) is an identity about $|\zeta|^2$
on the critical line. It says nothing about where the zeros are.

```{=latex}
\begin{figure}[!tb]
\centering
\makebox[\textwidth][c]{\includegraphics[width=7.0in]{figures/v48_gamma_bridge.png}}
\caption{Euler's constant on the triangular coordinate. A: the squared fractional part $(\{x\}/x)^2$ carries, on each unit interval $[m-1,m]$, exactly the mass $\sum_{k\ge2}m^{-k}/T_k$ of (GA.5); the masses add up to $\log(2\pi)-\gamma_{\mathrm E}$. B: subtracting $\log n$ leaves the odd term $1/2n$, while subtracting the centered logarithm $\frac12\log(2T_n)$ leaves a series in $1/T_n$ whose partial sums converge rapidly, as in (GA.2).}
\label{fig:gamma-bridge}
\end{figure}
```

**A simplex ladder.** The moment formula (4.5) is the case $d=2$ of the Beta
identity
$1/\binom{k+d-1}{d}=d\int_0^1u^{k-1}(1-u)^{d-1}\,du$ for the $d$-dimensional
simplex numbers. The same argument then gives, for every $d\ge2$,

$$
\sum_{k\ge2}\frac{\zeta(k)}{\binom{k+d-1}{d}}
=d(d-1)\int_0^1u^{d-2}\log\Gamma(u)\,du-\gamma_{\mathrm E}.
\tag{GA.7}
$$

The moments of $\log\Gamma$ on the right are classical [104]. The first three
rungs are

$$
\begin{aligned}
d=2\ \text{(triangular)}:&\quad \log(2\pi)-\gamma_{\mathrm E},\\
d=3\ \text{(tetrahedral)}:&\quad \tfrac32\log(2\pi)-6\log A-\gamma_{\mathrm E},\\
d=4\ \text{(pentatope)}:&\quad 2\log(2\pi)-12\log A+\frac{3\zeta(3)}{\pi^2}-\gamma_{\mathrm E}.
\end{aligned}
$$

Here $A$ is the Glaisher--Kinkelin constant, $\log A=\tfrac1{12}-\zeta'(-1)$
[105]. Written in the constants $\log(2\pi)$, $\gamma_{\mathrm E}$ and
$\zeta'(-j)$, the pattern is fixed:

- every rung contains $\tfrac d2\log(2\pi)$, and it contains $-\gamma_{\mathrm E}$
  with coefficient exactly one;
- rung $d$ adds one new constant, $\zeta'(2-d)$;
- $\zeta(3)$ first enters at $d=4$, because $\zeta'(-2)=-\zeta(3)/(4\pi^2)$ is a
  derivative taken at a trivial zero.

With every $\zeta(k)$ replaced by $1$, the left side of (GA.7) becomes the
reciprocal simplex telescope of Dossier §76, whose full sum from $k=1$ is
$d/(d-1)$.

**Where Euler's constant meets the zeros.** The first Li coefficient (9.8) is
$\lambda_1=\sum_{[\rho]}m_\rho/q_\rho=1+\gamma_{\mathrm E}/2-\log(2\sqrt\pi)$,
the classical value of $\sum_\rho\rho^{-1}$ [112, Ch. 12; 118]. Adding twice
$\lambda_1$ to (GA.3) cancels both $\gamma_{\mathrm E}$ and $\log\pi$:

$$
\boxed{\sum_{k\ge2}\frac{\zeta(k)}{T_k}+2\sum_{[\rho]}\frac{m_\rho}{q_\rho}
=\sum_{k\ge1}\frac1{T_k}-\log2=2-\log2.}
\tag{GA.8}
$$

A series of zeta values over reciprocal triangular numbers and a series over the
folded zeros add up to an elementary constant. This is the folded form of the
classical evaluation of $\sum_\rho\rho^{-1}$. It is an identity between two
convergent sums, not a sign condition. $\lambda_1>0$ is known unconditionally,
and it is only the first of the infinitely many Li conditions of §R15.

**What is classical, and what this section adds.** The substance of
(GA.1)--(GA.8) is classical:

- (GA.2): Ramanujan and Cesàro [96--99, 119];
- (GA.3): Boya, with Raabe's integral and the classical Gamma-function series
  [95, 101, 102];
- the setting of (GA.6): Titchmarsh, Nyman, Beurling, and Báez-Duarte, Balazard,
  Landreau and Saias [3, 106--109];
- the moments in (GA.7): Espinosa and Moll [104];
- $\lambda_1$: Hadamard and Davenport [110, 112].

This volume's contribution is organizational:

- the mirror reading of (GA.1)--(GA.2);
- the interval identity (GA.5), which joins the reciprocal telescope to the
  fractional-part norm;
- the simplex normalization of (GA.7);
- the identification of the §R17I denominator constant with (GA.3).

The replay `qa/audit_gamma_bridge.py` checks every display in this section,
including an interval-arithmetic enclosure of $\lambda_1$.

## R5. The triangular coordinate as a real analytic chart

Replace the integer index by a real source variable $s>1$ and define

$$
x=s(s-1)=2T_{s-1}
\qquad
R=2s-1=\sqrt{1+4x}
\tag{5.1}
$$

At $s=n+1$ this reads

$$
\boxed{x=2T_n,\qquad R=2n+1}
\tag{5.2}
$$

Thus the repeatedly occurring $2n+1$ is the Jacobian $dx/ds$ of the folded
safe-axis coordinate. The integer centered coordinate and the analytic
source Jacobian are the same object on this lattice.
Writing $R(x)=\sqrt{1+4x}$ makes both neighboring values visible, for
$n\ge2$ on the open source half-line:

$$
R(2T_{n-1})=2n-1,\qquad R(2T_n)=2n+1,\qquad
D_x=\frac1R D_s
\tag{5.2a}
$$

This is the route by which the elementary odd coordinate enters the
source derivatives. Dossier §34 uses this differential operator to
obtain the rung denominators, and §146 derives its Bessel polynomials.

A noninteger example makes the interpolation visible:

$$
\boxed{T_3=6<T_\pi=\frac{\pi(\pi+1)}2<7,\qquad
T_\pi\approx6.5055985273}
\tag{5.3}
$$

Indeed, $T_z$ is increasing for real $z>-1/2$, and $3<\pi<22/7$ gives
$6<T_\pi<T_{22/7}=319/49<7$. The value lies close to, but above,
the midpoint $6.5$. At $s=\pi+1$, the source chart has $x=2T_\pi$;
the same reflection identity holds exactly: $T_\pi=T_{-\pi-1}$.

Value scaling and horizontal-coordinate scaling must be separated. The
polynomial $T_x$ has zeros at $-1,0$; its reciprocal has poles there.
Multiplying its value by $2$ leaves those locations fixed. Replacing the
horizontal coordinate by $u=2x$ changes the displayed locations:

| expression | symmetry center | zeros; poles of its reciprocal |
|---|---|---|
| $T_x=x(x+1)/2$ | $x=-1/2$ | $x=-1,0$ |
| $2T_x=x(x+1)$ | $x=-1/2$ | $x=-1,0$ |
| $2T_{u/2}=u(u+2)/4$ | $u=-1$ | $u=-2,0$ |

The general coordinate rule, for $c>0$, is

$$
T_{u/c}=\frac{u(u+c)}{2c^2},\qquad
\frac1{T_{u/c}}=\frac{2c^2}{u(u+c)},\qquad
u_{\rm center}=-\frac c2
\tag{SC.1}
$$

The centered coordinate carries the same change explicitly. In the
shifted input $s$ used by the completed function,

$$
j_{s-1}=2s-1,\qquad 8T_{s-1}+1=(2s-1)^2
\qquad T_{s-1}=T_{-s}
\tag{SC.2}
$$

The symmetry center is now $s=1/2$, with reciprocal poles at $s=0,1$.
For the particular squared-root condition $(2s-1)^2=2$, the two branches
are $s=(1\pm\sqrt2)/2$ and $T_{s-1}=1/8$. Squaring removes the sign
of the centered coordinate; keeping $j_{s-1}$ retains the branch. This
is why the integer $2n+1$, its shifted real version, and the imaginary
$2it$ will continue to be printed beside the triangular fold.

Equations (5.1)--(5.2) are the safe-axis specialization of the full discrete
primitive and centered split recorded in §R1A, especially (TDP.4)--(TDP.5).

![The real triangular safe axis $x=s(s-1)=2T_{s-1}$ with its inverse $R=2s-1=\sqrt{1+4x}$, and the self-dual magnitude: $x^{-\sigma}$ and $x^{-(1-\sigma)}$ agree for every $x$ exactly at $\sigma=\tfrac12$. The reflection and conjugation involutions and the two components of the fold, which earlier editions drew here as well, are in §R10C, where they move with one orbit.](figures/figure74_safe_axis_and_self_dual.png)

## R5C. The even-triangular rail and the half-step sequence

The even-index subsequence deserves its own visible line. For $n\ge1$, put

$$
\boxed{a_n=2n+\frac12=\frac{j_{2n}}2,\qquad
a_n^2-\frac14=2n(2n+1)=2T_{2n}}
\tag{TR.1}
$$

Geometrically, $2T_{2n}$ is the $2n$ by $(2n+1)$ rectangle formed by
two equal triangles. Centering the two side lengths at $a_n$ writes its
area as $a_n^2-(1/2)^2$. This is why the quarter-square and odd
coordinate occur together. The even indices also pair successive factors
in the odd factorial, as (PR.6) will show. Its reciprocal sequence is

$$
\boxed{A_n:=\frac1{2T_{2n}}
=\frac1{2n}-\frac1{2n+1}
=\frac1{a_n^2-1/4}}
\tag{TR.2}
$$

| $n$ | even triangle $T_{2n}$ | adjacent product $2T_{2n}$ | reciprocal $A_n$ | centered root $a_n$ |
|---:|---:|---:|---:|---:|
| 1 | 3 | 6 | $1/6$ | $5/2$ |
| 2 | 10 | 20 | $1/20$ | $9/2$ |
| 3 | 21 | 42 | $1/42$ | $13/2$ |
| 4 | 36 | 72 | $1/72$ | $17/2$ |
| 5 | 55 | 110 | $1/110$ | $21/2$ |

The same fractions have two useful sums:

$$
\boxed{\log2=1-\sum_{n\ge1}A_n,\qquad
\zeta(2)=3-2\log2+\sum_{n\ge1}A_n^2}
\tag{TR.3}
$$

The first follows from the alternating harmonic series. For the second,
square the adjacent reciprocal difference and use
$\sum_{n\ge1}[(2n)^{-2}+(2n+1)^{-2}]=\zeta(2)-1$.
These are ordinary convergent sums of positive terms.

This selection by even index is distinct from the gcd selection in Dossier §170.
The latter groups rational rays and their multiplicities; here we select a
specific adjacent-product sequence. Both remain rooted in $T_x$.
In the later real source chart the same entry is
$x=2T_{2n}$, $s=2n+1$, and $R=2s-1=4n+1=2a_n$.


Later, the Gamma scaffold has poles at $-2T_{2n}$ (§R17). Voros's auxiliary
half-step sequence is precisely $a_n$ [56, equation (59)]. Equation (TR.1)
therefore supplies an exact triangular dictionary for that sequence. The
analytic continuation built from $A_n$ will be introduced only after the
completed source has been defined (§R17A). Its regularized values are a
different operation from the convergent sums in (TR.3).

**Consecutive squares.** The rail also has an elementary arithmetic face. For
every $n\ge1$, the $n+1$ consecutive squares that start at $T_{2n}$ add up to
the next $n$ squares, as in $3^2+4^2=5^2$ and $10^2+11^2+12^2=13^2+14^2$:

$$
\sum_{j=0}^{n}(T_{2n}+j)^2=\sum_{j=n+1}^{2n}(T_{2n}+j)^2.
\tag{TR.4}
$$

The starting point is forced. For a run that starts at $p$, the left side
minus the right side is $(p-T_{2n})(p+n)$, so the only positive start is the
even-triangular value in the table above. For first powers the runs start at
$n^2$, as in $4+5+6=7+8$. Derby [88] derives the starting point and searches
for analogues in higher powers; the quadratic printed there has the wrong sign
on its linear term.

## R5D. One real coordinate, several roles for $\pi$

The polynomial chart accepts real input without inventing a new interpolation:

$$
\boxed{T_x=\frac{x(x+1)}2
=\frac{\Gamma(x+2)}{2\Gamma(x)}
=\frac{(2x+1)^2-1}{8}.}
\tag{PR.1}
$$

At $x=\pi$, the adjacent reflected values satisfy
$T_\pi-T_{-\pi}=\pi$ and $T_\pi+T_{-\pi}=\pi^2$; these identities describe
the input rather than evaluate it.  An evaluation from integer triangular
numbers follows instead from (4.4) and Euler's Basel identity:

$$
\boxed{\pi
=3\sqrt{1+\frac1{12}\sum_{n\ge1}\frac1{T_n^2}}
=\sqrt{10-\frac18\sum_{n\ge1}\frac1{T_n^3}}.}
\tag{PR.4a}
$$

The square root acts on the whole expression.  This is the only reading used
later when the same constant enters the source-energy cap.

Euler's sine product gives the analytic bridge from ordinary integers to the
even triangular subfamily:

$$
\frac{\sin(\pi x)}{\pi x}
=\sum_{m\ge0}\frac{(-1)^m(\pi x)^{2m}}{(2m+1)!}
=\prod_{n\ge1}\left(1-\frac{x^2}{n^2}\right),
\tag{PR.5}
$$

and

$$
\boxed{(2m+1)!=\prod_{r=1}^{m}(2r)(2r+1)
=\prod_{r=1}^{m}2T_{2r}.}
\tag{PR.6}
$$

The same normalization gives

$$
(2m+1)!=T_{2m+1}(m!)^2C_m,
\qquad
\frac{4^m(m!)^2}{(2m+1)!}\frac{C_m}{4^m}
=\frac1{T_{2m+1}},
\tag{PR.7a}
$$

where $C_m$ is the $m$th Catalan number.  These coefficient identities are
comparison structure; no completed-source sign follows from them.

Gamma reflection supplies the normalized sine directly,

$$
\frac{\sin(\pi x)}{\pi x}
=\frac1{\Gamma(1+x)\Gamma(1-x)}.
\tag{PR.8}
$$

The half-step constants that recur in the later determinant and pole
calculations are

$$
\boxed{\Gamma(1/2)=\sqrt\pi,\qquad
\Gamma(3/2)=\frac{\sqrt\pi}{2},}
\tag{PR.10a}
$$

and

$$
\boxed{\frac{\Gamma(m+3/2)}{\Gamma(m+1/2)}
=m+\frac12=\frac{j_m}{2},\qquad
\frac{\Gamma(m+1/2)}{m!\Gamma(1/2)}
=\frac{\binom{2m}{m}}{4^m}.}
\tag{PR.10b}
$$

The first pair is used in the triangular determinant calculation (PC.7) of
§R17C; the normalized ratio supplies the pole coefficients (PC.1) of the same
section.  The central-binomial row is also the local inverse-Jacobian series

$$
R(x)^{-1}=(1+4x)^{-1/2}
=\sum_{m\ge0}(-1)^m\binom{2m}{m}x^m,
\qquad |x|<\frac14.
\tag{PR.10c}
$$

A final centered product closes the elementary loop:

$$
\boxed{\pi=4\prod_{n\ge1}\frac{8T_n}{8T_n+1}
=4\prod_{n\ge1}\frac{(2n)(2n+2)}{(2n+1)^2}.}
\tag{PR.10d}
$$

Changing logarithmic scale does not alter the Mellin phase if its Jacobian is
retained.  For $v=\log_{10}n$,

$$
n^{-s}=10^{-\sigma v}e^{-it(\ln10)v},\qquad
\overline{n^{-s}}=10^{-\sigma v}e^{+it(\ln10)v}.
\tag{PR.11}
$$

The full earlier catalog of angle and decimal examples is preserved in
earlier editions (Zenodo version chain).  The current Reading Volume keeps only the identities
that re-enter the analytic argument.

## R5E. The half-step and the reflected pair

The finite odd-factorial product has an integer upper limit.  Its analytic
continuation is supplied separately by Gamma duplication:

$$
\mathcal C(m):=\frac1{\Gamma(2m+2)}
=\frac{\sqrt\pi}{2^{2m+1}\Gamma(m+1)\Gamma(m+3/2)}.
\tag{HS.1}
$$

Now make the shift explicit, $m=s-1$.  On the critical line,

$$
s=\frac12+it
\Longrightarrow
m=-\frac12+it,
\quad T_m=-\frac18-\frac{t^2}{2},
\quad q(s)=-2T_m=\frac14+t^2.
\tag{HS.2}
$$

The conjugate pair has the exact positive Gamma product

$$
\boxed{\mathcal C(-\tfrac12+it)\mathcal C(-\tfrac12-it)
=\frac{\sinh(2\pi t)}{2\pi t}
=\prod_{n\ge1}\left(1+\frac{4t^2}{n^2}\right).}
\tag{HS.3}
$$

This is a Gamma identity, not the completed zeta source: the Euler-prime term
has not disappeared.

Three involutions recur later and should not be conflated:
conjugation $z\mapsto\bar z$, inversion $z\mapsto1/z$, and reflection
$z\mapsto1-z$.  Conjugation and reflection agree on $\Re s=1/2$; the Cayley
coordinate of §R7 converts reflection into inversion.  Away from those loci
they remain different operations.

For the fold $q=s(1-s)$,

$$
(2s-1)^2=1-4q=1+8T_{s-1},
\qquad
s=\frac{1\pm\sqrt{1-4q}}2.
\tag{HS.8}
$$

Reflection exchanges the two inverse branches.  If $q>1/4$ is real they are
the conjugate pair $1/2\pm i\sqrt{q-1/4}$; for complex $q$, conjugation also
moves $q$ to $\bar q$.  This branch distinction is the only part of the former
power-tower comparison needed downstream; the longer fixed-point discussion is
retained in earlier editions.

# Part II. From the half-step to the complex fold

The fold $q=s(1-s)$ identifies the reflection pair, the Cayley chart
expresses it as inversion, and the Mellin factor fixes the weight
$1/\sqrt n$. Equation (6.4) is the key conclusion: a folded zero is real
exactly when its zero lies on the critical line.

## R6. Folding the two axes of $s=\sigma+it$

Define

$$
q=q(s)=s(1-s)
=\sigma(1-\sigma)+t^2+i\,t(1-2\sigma)
\tag{6.1}
$$

The centered identity is

$$
\boxed{q=\frac14-\left(s-\frac12\right)^2}
\tag{6.2}
$$

This is the analytic continuation of the centered split in (TDP.5): the
signed coordinate $2s-1$ is squared and the two sheets $s$ and $1-s$ fold to
the same $q$.

Three specializations should be kept side by side:

| locus in the $s$-plane | condition | folded image |
|---|---|---|
| critical line | $s=1/2+it$ | $q=1/4+t^2\in\mathbb R_{>0}$ |
| real safe sheet | $s>1$, $t=0$ | $q=-s(s-1)=-x<0$ |
| general point | $s=\sigma+it$ | $\Im q=t(1-2\sigma)$ |

There is no omitted real-zero branch. For $0<\sigma<1$, the alternating
Dirichlet eta function satisfies

$$
\eta(\sigma)=(1-2^{1-\sigma})\zeta(\sigma)>0
\tag{6.3}
$$

Since $1-2^{1-\sigma}<0$, one has $\zeta(\sigma)<0$. Thus every nontrivial
zero $\rho=\beta+i\gamma$ has $\gamma\ne0$, and

$$
q_\rho\in\mathbb R
\iff \gamma(1-2\beta)=0
\iff \beta=\frac12
\tag{6.4}
$$

Therefore RH is exactly the assertion that all folded zero orbits land on the
positive real $q$-axis.

## R6A. Sum to product, and the model in which the hypothesis is true

Equation (6.4) says RH is the assertion that every folded orbit $q_\rho$ is
real and positive. Before six Parts are spent on it, it is worth writing down
the assertion's **model**: a node set for which it holds, whose product is
closed in elementary terms, and which the volume has been carrying since
Part I without saying what it was for.

**One dictionary.** Let $A=\{a_j\}$ be positive with multiplicities $m_j$ and
$\sum_jm_j/a_j<\infty$. Put

$$
E_A(x)=\prod_j\Bigl(1+\frac x{a_j}\Bigr)^{m_j},
\qquad
S_A(x)=\frac{E_A'}{E_A}(x)=\sum_j\frac{m_j}{x+a_j},
\qquad
\exp\Bigl(-\int_0^xS_A\Bigr)=\frac1{E_A(x)}
\tag{6A.1}
$$

Sum becomes product here by one operation: integrate the resolvent and
exponentiate. Three objects are compared through it.

| instance | nodes $a_j$ | resolvent | product |
|---|---|---|---|
| triangular ladder | $2T_n=n(n+1)$ | (6A.3) | (6A.2), closed |
| folded zeros | $q_\rho=\rho(1-\rho)$ | $S_\xi$, (9.5) | $X(-x)/X(0)$, §12B |
| primes | *not a node product* | $P$, §R16 | $\zeta(s_x)/\zeta(2)$, Euler |

The prime row is the odd one, and the distinction is not cosmetic: its
passage from sum to product is unique factorization, a product over primes
rather than over the nodes of a resolvent, absolutely convergent only for
$\Re s>1$. Its three cutoffs must be kept apart: the prime-power
cutoff, the truncated Euler product and the finite Dirichlet sum are three
different objects, equal at $X=2$ to $\exp(2^{-s})$, $(1-2^{-s})^{-1}$ and
$1+2^{-s}$. The two node rows are what this section compares.

**The triangular instance is closed, and it is already proved.** Dossier §11
evaluates $\Pi_\triangle(u)=\prod_n(1-u/T_n)=1/\bigl[\Gamma(1+s)\Gamma(2-s)\bigr]$
under $u=s(s-1)/2$. That substitution is the fold: $x=-2u=s(1-s)=q(s)$. In
the fold coordinate, with $\nu=\sqrt{x-\tfrac14}$ (imaginary for
$x<\tfrac14$), the same identity reads

```{=latex}
\begin{tnclosed}{the triangular model}
```
$$
\boxed{\ \prod_{n\ge1}\Bigl(1+\frac x{2T_n}\Bigr)
=\frac{\sin\pi s}{\pi\,q(s)}
=\frac{\cosh\pi\nu}{\pi x}\ },
\qquad
\boxed{\ \sum_{n\ge1}\frac1{x+2T_n}=\frac{\pi\tanh\pi\nu}{2\nu}-\frac1x\ }
\tag{6A.2--6A.3}
$$
```{=latex}
\end{tnclosed}
```

the second being the logarithmic derivative of the first, and $\Gamma$
reflection carrying one form to the other. The removable values are $1$ at
$x=0$ and $4/\pi$ at $x=\tfrac14$.

**Keep the parameter signs visible.** The numerator $\cosh\pi\nu$ is entire
of order one-half in this model parameter; its zeros are exactly
$x=-2T_n$ for $n\ge0$. Division by $\pi x$ removes the zero mode.
The model's reflection variable gives $z=q(s)$ and
$E_\triangle(q(1/2))=4/\pi$. The completed source instead uses
$x=-q(s)$, so its centered value is $E_\xi(-1/4)=X(1/4)/X(0)$.
At the common positive comparison parameter $x=1/4$, its value is
$X(-1/4)/X(0)$. These are distinct evaluations, not an identification of
spectral measures.

The completed determinant $E_\xi(x)=X(-x)/X(0)$ also has order one-half,
but the property shared with the triangular model is a zero-set condition:

$$
\boxed{\mathrm{RH}\iff E_\xi(x)=X(-x)/X(0)
\text{ has all its zeros on the negative real axis}.}
\tag{6A.4}
$$

Equal order does not mean equal type. Dossier Section 12B proves,
unconditionally, $\log E_\triangle(x)\sim\pi\sqrt x$ whereas
$\log E_\xi(x)\sim\sqrt x\log x/4$. The model has finite type $\pi$;
the completed determinant has infinite type at order one-half.
An independent positive realization of the completed product remains missing.

**A multiplicity-one operator.** Dossier Section 12A realizes the product
by $A_\triangle=-d^2/d\theta^2-1/4$ on $(0,\pi)$, with
$f(0)=0$, $f'(\pi)=0$. Its normalized half-integer sine eigenfunctions
have eigenvalues $2T_m$; removing $m=0$ gives
$\det(I+xA_+^{-1})$ equal to (6A.2). Unlike the full spherical Laplacian,
this realization uses each positive degree once.

The same modes are unitary images of the reflected polynomials in
Section R15. With $n=2m+1$ they satisfy

$$
\frac1n\mathcal P_m\!\left(4\sin^2\frac{\pi u}{n}\right)
=\frac{\operatorname{sinc}_\pi(u)}{\operatorname{sinc}_\pi(u/n)}
\longrightarrow\operatorname{sinc}_\pi(u).
\tag{6A.5}
$$

Their squares are finite Fejer kernels: the pair counts give
$n+2T_{n-1}=n^2$. The finite sine projection has an interior sine-kernel
limit; at the boundary its reflected-sum term survives. Section 61A
matches its bandwidth to $N\sim T^2\log(T/(2\pi))/2$. This is a proved
comparison limit, not a completed-source kernel limit or a theorem about
zeta pair correlation. The latter prediction uses
$1-\operatorname{sinc}_\pi(u)^2$, not the nearest-neighbor gap density [79].

**Three entries, with their status.**

| quantity | triangular model | folded zeros |
|---|---|---|
| $\sum_jm_j/a_j$ | $\sum_n1/(2T_n)=1$ exactly | $S_\xi(0)=\lambda_1=0.0230957\ldots$ (9.8) |
| at comparison parameter $1/4$ | $E_\triangle(1/4)=4/\pi$ | $E_\xi(1/4)=X(-1/4)/X(0)$ |
| odd-factorial layer | $(2m+1)!=\prod_r2T_{2r}$ (PR.6) | rung weight $(2k-1)!$ (13A.3) |

The model nodes start at $2$, while the zeta nodes start near $200$.
The shared odd-factorial and hyperbolic identities therefore identify
constructions, not their measures: nothing transfers without a source
theorem, and no bound on $\Delta$ of (13A.2) follows from the model.
An operator with spectrum $q_\rho$ has not been supplied. That is precisely
the input this volume cannot supply for $\zeta$.

## R7. Reflection, conjugation, and the Cayley circle

Use the global Cayley coordinate

$$
z_C(s)=\frac{s}{1-s}
\qquad
s=\frac{z_C}{1+z_C}
\qquad
q=\frac{z_C}{(1+z_C)^2}
\tag{7.1}
$$

Then

$$
\boxed{\frac1q=2+z_C+\frac1{z_C}}
\tag{7.2}
$$

This is the reciprocal coordinate of Dossier §171: $y_C=z_C+z_C^{-1}$. The
same Pascal recurrence now has coefficients expressed through $q(s)$,
so the arithmetic reciprocal fold returns here as an exact analytic
identity, with its inverse branches retained.

Reflection becomes inversion $z_C\mapsto1/z_C$, while conjugation becomes
$z_C\mapsto\bar z_C$. They agree on the unit circle. Hence

$$
\Re s=\frac12
\iff |z_C|=1
\iff 1-s=\bar s
\tag{7.3}
$$

The subscript $C$ distinguishes this global $s$-plane coordinate from the
scale-dependent Cayley complement $c_x(q)=(q-x)/(q+x)$ used in §R11.

This is a useful uniformization, not a proof engine. Differentiating a
self-inversive reformulation does not import the Cohn or Speiser one-sided
conditions: the derivative zeros of the completed symmetric function inherit
inversion symmetry. The point $z_C=-1$ is an isolated essential singularity
of $\xi(z_C/(1+z_C))$, with transformed zeros accumulating there.

The Li coordinate of §R15 is this one inverted and reflected,
$w=1-1/s=-z_C^{-1}$, so (7.2) also reads $1/q=2-w-w^{-1}$. Section R10C carries
that dictionary and what it does to a single orbit.

## R8. The self-dual Mellin magnitude

For $n>0$,

$$
n^{-s}=n^{-\sigma}e^{-it\log n}
\qquad
n^{-\bar s}=n^{-\sigma}e^{+it\log n}
=\overline{n^{-s}}
\qquad
\left|n^{-s}\right|=n^{-\sigma}
\tag{8.1}
$$

Every negative-frequency factor is therefore carried together with its
positive-frequency conjugate. Their sum and product are

$$
n^{-s}+n^{-\bar s}=2n^{-\sigma}\cos(t\log n)
\qquad
n^{-s}n^{-\bar s}=n^{-2\sigma}
\tag{8.1a}
$$

Reflection and conjugation give two products:

$$
n^{-s}n^{-(1-s)}=\frac1n
\qquad
n^{-s}\overline{n^{-s}}=\frac1{n^{2\sigma}}
\tag{8.2}
$$

They agree for every $n$ exactly at $\sigma=1/2$. The common factor per
side is

$$
\boxed{n^{-1/2}=\frac1{\sqrt n}}
\tag{8.3}
$$

The conjugate pair $e^{\mp it\log n}$ changes phase but not length. This explains
the self-dual $\Lambda(n)/\sqrt n$ normalization in the completed explicit
formula. It does not identify the Gauss circle error term with the zeta zero
problem; the shared square-root scale is geometric, while the arithmetic
coefficients and summation problems are different.

```{=latex}
\begin{figure}[!tb]
\centering
\makebox[\textwidth][c]{\includegraphics[width=7.4in]{figures/v36_mellin_self_dual.png}}
\caption{Why $1/\sqrt n$. The modulus of $n^{-s}$ does not see the imaginary part; reflection and conjugation give two different products of a term with its partner; and those two products agree, for every $n$, at exactly one abscissa. The shared square-root scale is geometric, and does not identify two different problems.}
\label{fig:mellin}
\end{figure}
```

# Part III. Completion and the folded zero resolvent

Completion removes the pole and trivial zeros of $\zeta$, leaving the
entire function $\xi$ with symmetry $s\mapsto1-s$. Folding halves its
order and gives one point per orbit $\{\rho,1-\rho\}$. Its logarithmic
derivative is the absolutely convergent simple-pole sum $S_\xi$ in (9.7).
Section R9 gives the Gamma--prime source formula; Sections R10--R10B give
the zero-side criteria, positive realizations and off-line heat trace.
Part IV differentiates this same resolvent.

## R9. The completed function

The completed Riemann function is

$$
\xi(s)=\frac12s(s-1)\pi^{-s/2}\Gamma(s/2)\zeta(s)
\qquad
\xi(s)=\xi(1-s)
\tag{9.1}
$$

Here the half-Gamma value in (PR.10a) fixes a normalization:
$\pi^{-1/2}\Gamma(1/2)=1$ and
$\lim_{s\to1}(s-1)\zeta(s)=1$ give $\xi(1)=1/2$.
On the critical line, however, the argument of this Gamma factor is
$s/2=1/4+it/2$. The distinction between the source variable and the
Gamma argument matters when using a half-integer identity.

Because it is invariant under reflection, it factors through the fold:

$$
\boxed{
\xi(s)=X(q),\qquad
q=s(1-s)=-2T_{s-1},\qquad
4q=1-(2s-1)^2}
\tag{9.2}
$$

for an entire function $X$. Define

$$
M_\xi(q)=-\frac{X'(q)}{X(q)}
\qquad
S_\xi(x)=M_\xi(-x),\quad x>0
\tag{9.3}
$$

On the safe real sheet

$$
s_x=\frac{1+\sqrt{1+4x}}2=\sigma_x+i0>1
\tag{9.4}
$$

one has the absolutely convergent source formula

$$
\boxed{S_\xi(x)=\frac1R\left[
\frac1{s_x}+\frac1{s_x-1}-\frac12\log\pi
+\frac12\psi(s_x/2)
-\sum_{n\ge2}\frac{\Lambda_{\rm vM}(n)}{n^{s_x}}
\right]}
\tag{9.5}
$$

This formula is the source-side entry: Gamma and primes are evaluated where
their defining expansions converge.

**Where the zeros enter.** Write $[\rho]$ for one functional-equation orbit
$\{\rho,1-\rho\}$ and $m_\rho$ for its multiplicity; an off-line quartet
contributes two conjugate folded values, each counted once. This convention is
used in every folded sum in the volume.

$\xi$ is entire of order one. Since $q=s(1-s)$ is quadratic in $s$, the entire
function $X$ of (9.2) has order one **half** in $q$, so it has genus zero: its
Hadamard product needs no exponential factors and converges absolutely [5, 110],

$$
X(q)=X(0)\prod_{[\rho]}\left(1-\frac{q}{q_\rho}\right)^{m_\rho}
\tag{9.6}
$$

Taking $-X'/X$ and evaluating at $q=-x$ turns that product into the identity
every later Part differentiates:

$$
\boxed{S_\xi(x)=\sum_{[\rho]}\frac{m_\rho}{x+q_\rho},
\qquad
Z_r(x)=\sum_{[\rho]}\frac{m_\rho}{(x+q_\rho)^{r}}}
\tag{9.7}
$$

**This is what the fold buys, and it is worth being explicit about it.** In the
$s$-plane $\xi$ has order one and genus one: the Hadamard product carries a
factor $e^{s/\rho}$ at every zero, and $\sum_\rho\rho^{-1}$ needs a symmetric
grouping to converge; pairing $\rho$ with $1-\rho$ supplies one. The fold
performs that pairing in the variable itself. The order halves, the
exponential factors disappear, and $\sum_{[\rho]}m_\rho q_\rho^{-1}$ converges
absolutely on its own. The underlying resolvent is an absolutely convergent sum of simple poles
at $x=-q_\rho$, all in the open left half-plane. They lie on the negative
real axis exactly under RH. Higher resolvents and derivatives have higher
pole orders on the same set; the safe-axis source formulas use $x>0$.

One number, for orientation. At $x=0$,

$$
S_\xi(0)=\sum_{[\rho]}\frac{m_\rho}{q_\rho}
=1+\frac{\gamma_{\mathrm E}}2-\log\bigl(2\sqrt\pi\bigr)
=0.0230957089661\ldots
\tag{9.8}
$$

with $\gamma_{\mathrm E}$ Euler's constant. The middle expression is the classical
value of $\sum_\rho\rho^{-1}$ [112, Ch. 12], and the pairing
$\rho^{-1}+(1-\rho)^{-1}=q_\rho^{-1}$ is why the folded sum reproduces it. This
same number returns as the boundary moment $\mu_0$ in §R12 and as Li's
$\lambda_1$ in §R15. **Three names, one number, and it is the value at $x=0$ of
the function in (9.7).** Section R4A pairs it with a series of zeta values:
by (GA.8), twice this number plus $\sum_{k\ge2}\zeta(k)/T_k$ equals
$2-\log2$.

### The folded-state contract

The definition of $[\rho]$ above is a definition of the index set, not a
positivity hypothesis. Conjugation acts on this set: away from the critical
line, $[\bar\rho]$ is a second orbit and $q_{\bar\rho}=\bar q_\rho$.
Multiplicity is the common zero order of the two members of the reflection
pair; it is not multiplied by the size of a four-slot symmetry list.
An off-line quartet of multiplicity $m$ therefore contributes
$m/q+m/\bar q$ to (9.8), while a critical-line reflection pair of
multiplicity $m$ contributes $m/q$.

The fold identifies exactly the two inverse branches. For arbitrary
complex $s_1,s_2$,

$$
q(s_1)-q(s_2)=(s_1-s_2)(1-s_1-s_2),\qquad
q(s_1)=q(s_2)\iff s_2=s_1\ \text{or}\ s_2=1-s_1.
\tag{IF.1}
$$

For a nontrivial zero, which is nonreal, critical-line membership is
therefore retained by $q$: it is equivalent to $q\in(1/4,\infty)$.
The changes $q\mapsto-q$ and $q\mapsto1/q$ are invertible on the folded
zero set. They do not create a new loss of information. A later real-valued
observation, aggregation of conjugate nodes, or probability normalization
must be defined separately; none changes what $[\rho]$ means here.

This is the complete interface a downstream construction needs to inherit:
the reflection orbit, its multiplicity, the complex folded coordinate,
and the absolutely convergent first-Li identity (9.8). Positivity of a
separately chosen scalar does not establish the Stieltjes property of the
complex folded resolvent. Dossier Section 32 records the same contract.

```{=latex}
\begin{figure}[!tb]
\centering
\makebox[\textwidth][c]{\includegraphics[width=7.0in]{figures/v36_fold_and_poles.png}}
\caption{One orbit, one point, one pole. The zeros of $\xi$ come in orbits $\{\rho,1-\rho\}$; $q=s(1-s)$ sends both members of an orbit to a single point, real exactly when the orbit lies on the critical line; and $S_\xi$ has one simple pole per orbit, at $x=-q_\rho$. Every argument in this volume is made to the right of all of them.}
\label{fig:fold-poles}
\end{figure}
```

## R9A. The first zero, in these coordinates

The volume is written in $q$ and $x$ and never evaluates them. One worked orbit
fixes the scale of everything that follows, and the natural one is the lowest.

The first zero of $\zeta$ on the critical line sits at
$\gamma_1=14.134725141734693790\ldots$, so by (9.2) its folded coordinate is

$$
\boxed{q_1=\tfrac14+\gamma_1^2=200.0404548323868594\ldots=-2T_{\rho_1-1}}
\tag{9.9}
$$

The second equality is (9.2) read at $s=\rho_1$: **the folded image of a zero is
$-2$ times the triangular number at its centered index.** For a critical-line
zero that index is $-\tfrac12+i\gamma$, and
$(-\tfrac12+i\gamma)(\tfrac12+i\gamma)=-(\tfrac14+\gamma^2)$, which is why $q$
is real there and, by (6.4), nowhere else.

**What this one orbit carries.** By (9.8) the folded resolvent at the origin is
$0.0230957\ldots$; the first orbit supplies $1/q_1=0.004998989\ldots$ of it,
just under $22\%$. The second orbit sits at $q_2=442.1761\ldots$, so the ratio
that governs the boundary of the whole ladder is

$$
\frac{q_1}{q_2}=0.4523999\ldots
\tag{9.10}
$$

Section R12 uses exactly this number.

**On the prime side the same zero is the slowest wave.** In Riemann's formula
[74] each zero contributes an oscillation of period $2\pi/\gamma$ in $\log x$,
so $\rho_1$ gives $2\pi/\gamma_1=0.4445212\ldots$ — the longest wavelength in
the prime error, repeating every multiplicative factor
$e^{2\pi/\gamma_1}=1.5597432\ldots$ Everything faster comes from higher zeros.
The rungs and the primes are reading the same list of numbers in two different
coordinates.

**Riemann's own count does not locate it.** The smooth part of the
zero-counting function is
$N_0(T)=\frac{T}{2\pi}\log\frac{T}{2\pi}-\frac{T}{2\pi}+\frac78$, which differs
from $\theta(T)/\pi+1$ by $1/(48\pi T)+O(T^{-3})$ (Stirling; this is the
$0.0022$ between the two heights below), so it first reaches $1$ essentially where
the Riemann--Siegel angle first vanishes: at $T=17.8478\ldots$, against a first
Gram point at $17.8456\ldots$ The first zero is at $14.1347\ldots$, lower by
$3.71$. At this height the smooth term is not in charge and the entire
discrepancy is carried by the oscillating part $S(T)$ — the term every
effective result in the subject has to bound, and the reason a *counting*
statement and a *location* statement are different problems.

**One constant, printed three times.** The $7/8$ above is not a third $7/8$.
It is the same number as the value $\mathfrak Z_\xi(0)=7/8$ computed exactly at
(TV.2), and as the coefficient of $1/x$ in the large-$x$ expansion (OP.1) of
$S_\xi$. The three agree for one reason: by the Mellin representation, the
coefficient of $x^{-1}$ in $\sum_{[\rho]}m_\rho(x+q_\rho)^{-1}$ is the value at
$p=0$ of $\sum_{[\rho]}m_\rho q_\rho^{-p}$, the regularized number of orbits;
and for a spectrum whose counting function is a smooth main term plus $7/8$
plus a mean-zero oscillation, the main term contributes to the *poles* of
$\mathfrak Z_\xi$ and only the constant survives at the origin. So the constant
in Riemann's counting formula, the regularized count of folded orbits, and the
$1/x$ coefficient of the source expansion are one number.

*The mechanism, displayed.* From
$(x+q)^{-1}=\frac1{2\pi i}\int_{(c)}\frac{\pi}{\sin\pi p}x^{-p}q^{p-1}dp$
($0<c<1$), summing over orbits for $0<c<\tfrac12$,

$$
S_\xi(x)=\frac1{2\pi i}\int_{(c)}\frac{\pi}{\sin\pi p}\,
\mathfrak Z_\xi(1-p)\,x^{-p}\,dp
\tag{9.11}
$$

Moving the contour right: the double pole of $\mathfrak Z_\xi(1-p)$ at
$p=\tfrac12$, inherited from the smooth count, gives the $x^{-1/2}\log x$ and $x^{-1/2}$ terms of
(OP.1); the simple pole of $\pi/\sin\pi p$ at $p=1$, where $\mathfrak Z_\xi$ is
regular by (TV.2), gives $+\mathfrak Z_\xi(0)/x=\tfrac78/x$. The oscillating
part $S(T)$ contributes to no pole at $p\le1$.

That identification is checked in the source package from the **source side
alone**: computing $S_\xi$ from (9.5), with Gamma and primes only and no zero
used anywhere,
$x\bigl(S_\xi(x)-\frac{\log x-2\log2\pi}{8\sqrt x}\bigr)$ takes the value
$0.87495\ldots$ at $x=10^7$; the limit as $x\to\infty$ is $7/8$. A finite
evaluation is not the limit, and the two are printed separately.

**Grade.** The identities in (9.9) and (9.10) are exact; their printed
decimals are approximations. The prime-side period is classical. The
$7/8$ identification is an identity among quantities the volume already
carries, confirmed to four digits by an independent computation that uses no
zero. **None of it is evidence for or against the hypothesis.** It is the scale
of the objects, and it is here because a reader is entitled to see the
coordinates carry a number at least once.

## R10. Heat, Stieltjes, and complete Bernstein representations

The folded heat trace and its Laplace transform are

$$
\Theta_\xi(u)=\sum_{[\rho]}m_\rho e^{-uq_\rho}
\qquad
S_\xi(x)=\int_0^\infty e^{-xu}\Theta_\xi(u)\,du
\tag{10.1}
$$

**Three classes of function, and what each one contributes.** The chain below
uses them, and they are worth stating plainly.

- A **Stieltjes function** on $(0,\infty)$ is one of the form
  $a+\int_0^\infty(x+u)^{-1}d\mu(u)$ with $a\ge0$ and $\mu$ a positive measure:
  exactly a nonnegative constant plus a superposition of simple poles on the
  negative axis, with positive weights. Comparing with (9.7), $S_\xi$ is of that
  shape already — one pole per orbit — and **the whole content of the class
  membership is that the poles are real and the weights are positive**.
- A **complete Bernstein function** is one whose quotient by $x$ is Stieltjes;
  equivalently it has an integral representation with the same positive measure,
  read one power lower. It is the form in which the criterion becomes a
  statement about $h(x)=xS_\xi(x)$ rather than about $S_\xi$.
- $h$ is **operator monotone** on $(0,\infty)$ if $A\preceq B$ implies
  $h(A)\preceq h(B)$ for all positive operators. Among nonnegative functions, Löwner's theorem identifies
  this class with the complete Bernstein functions. Operator monotonicity
  alone is not sufficient for that class. The actual $h=xS_\xi$ is positive.

**Widder's theorem** is the discrete counterpart used from Part IV onward: it
characterizes the same class by the sign of every derivative combination
$(-1)^{k-1}D^{2k-1}[x^kf]$, which is precisely the family $W_k$. So the rungs of
Part IV are not a new criterion. **They are this same equivalence, read one
derivative at a time.**

The exact equivalence chain is

$$
\boxed{\begin{aligned}
\mathrm{RH}&\iff S_\xi\ \text{is Stieltjes}\\
&\iff h(x):=xS_\xi(x)\ \text{is complete Bernstein}\\
&\iff h\ \text{is operator monotone on }(0,\infty)
\end{aligned}}
\tag{10.2}
$$

For positive nodes $x_1,\ldots,x_N$, the Löwner matrix of $h$ is

$$
[\mathcal L_h]_{ij}=
\begin{cases}
\dfrac{h(x_i)-h(x_j)}{x_i-x_j},&i\ne j\\[2mm]
h'(x_i),&i=j
\end{cases}
\tag{10.3}
$$

Löwner's theorem gives the all-node criterion

$$
\boxed{
\mathrm{RH}\iff
\mathcal L_h(x_1,\ldots,x_N)\succeq0
\quad\text{for every finite positive node set}}
\tag{10.4}
$$

This is one global matrix criterion. The scalar Widder rungs of Part IV are
local derivative shadows of it. In particular, its one-node entry is
$h'(x)=W_1(x)$. Higher $W_k$ are not additional diagonal entries of this
same matrix: their exact connection uses the derivative array and boundary
moment matrices developed in §§R12–R15.

## R10A. Positive realizations: trace and finite-vector forms

An operator model must reproduce the particular scalar function $S_\xi$.
Two compatible positive representations have different normalizations:

| representation | scalar resolvent | Gram vector for $\mathcal L_h$ |
|---|---|---|
| positive trace-class operator $D$ | $\operatorname{Tr}[D(I+xD)^{-1}]$ | $D^{1/2}(I+xD)^{-1}$ in Hilbert--Schmidt space |
| positive operator $D$ and finite vector $v$ | $\langle(I+xD)^{-1}v,v\rangle$ | $(I+xD)^{-1}v$ in Hilbert space |

In either row, equality with $S_\xi(x)$ for every $x>0$ supplies a positive
Löwner matrix. The proof is the elementary resolvent identity: the divided
difference of $x/(1+xd)$ is $[(1+xd)(1+yd)]^{-1}$.
The trace route has $\operatorname{Tr}D=\lambda_1$; the finite-vector route
has $\|v\|^2=\lambda_1$, where $S_\xi(0)=\lambda_1$ is the first of Li's
coefficients, defined at (15.1a) and equal to the boundary moment $\mu_0$.

The source itself fixes which normalization is possible. Expanding (9.5),

$$
\boxed{S_\xi(x)=
\frac{\log x-2\log(2\pi)}{8\sqrt x}
+\frac7{8x}
+O\!\left(\frac{\log x}{x^{3/2}}\right)}
\tag{OP.1}
$$

Consequently $xS_\xi(x)\to\infty$. A proposed finite-vector formula
$S_\xi=\langle D(I+xD)^{-1}v,v\rangle$ would instead imply
$xS_\xi\le\|v\|^2$. It fails even under RH. The extra factor $D$ is valid
inside a trace, or for the different finite-vector function
$[S_\xi(0)-S_\xi(x)]/x$; it cannot be silently moved between the two rows.

For the canonical folded diagonal $C_\xi$, the eigenvalues are
$d_\rho=1/q_\rho$, counted once per reflection orbit. It is a normal
trace-class operator unconditionally. The classical zero-counting estimate
gives

$$
\boxed{C_\xi\in\mathcal S_p\iff p>\frac12}
\tag{OP.2}
$$

Positivity of this diagonal is equivalent to RH. It is a useful exact
spectral representation; an independent positivity theorem is still needed.
In particular, an ordered model with $d_n=O(n^{-2})$ has a critical trace
sum with at most a simple pole at $p=1/2$. Section R17A will exhibit the
double pole required by the completed source.

A fixed indefinite quartet metric has another limitation. Congruence
preserves its inertia, so a matrix of signature $(2,2)$ cannot become a
positive metric merely by changing coordinates. This says nothing against
a different positive realization proved from the full source. Zero-indexed
representations are not automatically circular; assuming their positivity
would be the missing step.

## R10B. What an off-line orbit leaves in the heat trace

The triangular imaginary part is an exact off-line marker. Write
$q_\rho=a_\rho+ib_\rho$ in this section, with explicitly defined real
coordinates

$$
\boxed{a_\rho=\gamma^2+\beta(1-\beta)>0,\qquad
b_\rho=\gamma(1-2\beta)
=-2\Im T_{\rho-1}}
\tag{HT.1}
$$

Since $\gamma\ne0$, $b_\rho=0$ exactly on the critical line. A conjugate
pair of folded orbits contributes

$$
\underbrace{2m e^{-ua}\cos(ub)}_{\text{heat contribution}}
\qquad\text{against}\qquad
\underbrace{2m e^{-ua}}_{\text{phase removed}},\qquad u>0
\tag{HT.2}
$$

Thus off-line geometry creates an oscillatory heat contribution. The total
heat trace does not vanish under RH; it is then a positive sum of decaying
exponentials. The meaningful absence statement concerns the off-line
defect, not the whole trace.

Define the real-part envelope and its gap by

$$
\Theta_{\rm env}(u)=\sum_{[\rho]}m_\rho e^{-ua_\rho}
\qquad \mathcal D_H(u)=\Theta_{\rm env}(u)-\Theta_\xi(u)
\tag{HT.3}
$$

Conjugate pairing gives the nonnegative identity

$$
\boxed{\mathcal D_H(u)
=\sum_{[\rho]}m_\rho e^{-ua_\rho}
[1-\cos(ub_\rho)]\ge0}
\tag{HT.4}
$$

All sums converge absolutely for $u>0$. Therefore different orbits cannot
cancel in this gap. A single orbit can still have a resonant zero at
$ub\in2\pi\mathbb Z$. Vanishing throughout any open interval of $u$
excludes every nonzero $b$, whereas vanishing at one selected time alone
does not supply that argument.

A resonance-free version uses the squared imaginary coordinate:

$$
\boxed{\mathcal E_H(u):=\sum_{[\rho]}m_\rho b_\rho^2e^{-ua_\rho}
=4\sum_{[\rho]}m_\rho(\Im T_{\rho-1})^2e^{-ua_\rho}}
\tag{HT.5}
$$

For every fixed $u>0$, each off-line orbit contributes strictly positively.
The sum is finite, since $b_\rho^2\le\gamma^2$ and Gaussian decay dominates
the zero count. Consequently

$$
\boxed{\mathcal E_H(u)=0\iff\mathrm{RH}\qquad
\text{at any one prescribed }u>0}
\tag{HT.6}
$$

This is an exact detector, not an independent source estimate. Its weights
still use the unknown transverse zero coordinates. In the language of
§R21, it has the regularized distributional representation
$\mathcal E_H(u)=(4\pi)^{-1}\langle\Delta\log|\xi|,
(\Im q)^2e^{-u\Re q}\rangle$ over the critical strip. This supplies a
source representation but leaves the zero-forcing bound unproved.

There is also a direct bridge back to resolvents. Put
$S_{\rm env}(x)=\sum_{[\rho]}m_\rho/(x+a_\rho)$. For $x>0$,

$$
\boxed{\begin{aligned}
S_{\rm env}(x)-S_\xi(x)
&=\int_0^\infty e^{-xu}\mathcal D_H(u)du\\
&=\sum_{[\rho]}m_\rho
\frac{b_\rho^2}{(x+a_\rho)[(x+a_\rho)^2+b_\rho^2]}
\ge0
\end{aligned}}
\tag{HT.7}
$$

To prove the displayed fraction, integrate
$e^{-(x+a)u}[1-\cos(bu)]$, obtaining
$1/(x+a)-(x+a)/[(x+a)^2+b^2]$. Every nonzero $b$ gives a strictly
positive summand. Thus equality in (HT.7) at one prescribed $x$ is again
equivalent to RH. The missing step would be an independent source proof
of the reverse inequality $S_{\rm env}(x)\le S_\xi(x)$, or a source proof
that $\mathcal E_H(u)\le0$. The envelope itself is not presently recovered
from an independently positive source model.

The established heat criterion remains

$$
\boxed{\mathrm{RH}\iff
(-1)^k\Theta_\xi^{(k)}(u)\ge0
\quad\text{for every }k\ge0,\ u>0}
\tag{HT.8}
$$

This is complete monotonicity, stronger than positivity of the total heat
trace. For example, the synthetic folded spectrum with two atoms at $1$
and one at each of $2\pm i$ has
$\Theta(u)=2e^{-u}+2e^{-2u}\cos u>0$ for all $u>0$, despite its
nonreal pair. It is not asserted to be the Riemann spectrum.

![Synthetic heat traces: the total trace stays positive despite a nonreal pair, while the normalized off-line heat gap has isolated resonant zeros. The squared-imaginary-coordinate detector avoids those resonances.](figures/figure84_v26_heat_defect.png)

Finally, the source already retains the prime heat term explicitly:

$$
\Theta_\xi(u)=1+\Theta_\Gamma(u)-\Theta_P(u),\qquad
\Theta_P(u)=\frac{e^{-u/4}}{2\sqrt{\pi u}}
\sum_{n\ge2}\frac{\Lambda_{\rm vM}(n)}{\sqrt n}
e^{-(\log n)^2/(4u)}
\tag{HT.9}
$$

The prime term is beyond all algebraic orders as $u\downarrow0$. This
explains why matching the regularized fractions and the complete algebraic
short-time expansion need not identify the heat trace itself. Conversely,
a hypothetical off-line zero above the verified height contributes the
factor $e^{-ua_\rho}$ with $a_\rho>H^2$: at fixed time its signal can be
extremely small. Proving its exact absence is a source theorem, not a
numerical detection threshold.

## R10C. One orbit, four coordinates

Sections R6–R10 have put four names on the same folded zero orbit, in four
different places. This section writes the dictionary between them once, because
the rung chain of Part IV and the Li chain of §R15 are the same folded data read
in two of these coordinates, and the conversion between them is exact.

Fix one orbit $[\rho]=\{\rho,1-\rho\}$ with $\rho$ nonreal, and set

$$
q=\rho(1-\rho),
\qquad
p=-q,
\qquad
y=\frac1q=-\frac1p,
\qquad
w=1-\frac1\rho
\tag{10C.1}
$$

- $q$ is the **folded point** of §R6: one point per orbit, because the
  reflection $\rho\mapsto1-\rho$ fixes it.
- $p=-q$ is the **resolvent pole** of §R10: the kernel $(x+q)^{-1}$ summed in
  (10.1) is singular at $x=p$ and nowhere else, with value $1/q$ at the origin.
  When $q>0$ is real, the kernel on $x>0$ is positive and decreasing; for
  nonreal $q$ no real-order statement is attached to the individual kernel.
- $y=1/q$ is the **reciprocal coordinate** of (7.2), the one in which the
  central-Pascal rows of §R15 are polynomial.
- $w$ is the **Li coordinate** of (15.1a). It is the Cayley coordinate of §R7
  inverted and reflected, $w=-z_C^{-1}$, so the reflection $\rho\mapsto1-\rho$
  acts as $w\mapsto w^{-1}$, exactly as it acts as $z_C\mapsto z_C^{-1}$ there.

The link between the last two is (7.2) rewritten. Substituting $w=-z_C^{-1}$,

$$
\boxed{\;y=\frac1q=2-w-\frac1w\;}
\tag{10C.2}
$$

so the pole position alone fixes $w$ up to the inversion $w\mapsto w^{-1}$ that
folding has already quotiented out.

**The orbit carries a whole Li column.** Write the reflection pair's
contribution to the $n$-th Li coefficient as

$$
Q_n(y)=2-w^n-w^{-n},
\qquad
\lambda_n=\sum_{[\rho]}m_\rho\,Q_n(y_\rho)
\tag{10C.3}
$$

the second equality being (15.1a) grouped by orbit. Since $w^n+w^{-n}$ satisfies
the Chebyshev recurrence with ratio $w+w^{-1}=2-y$, so does $Q_n$:

$$
\boxed{\;Q_0=0,\qquad Q_1=y,\qquad
Q_{n+1}=2y+(2-y)\,Q_n-Q_{n-1}\;}
\tag{10C.4}
$$

Every $Q_n$ is therefore a polynomial in $y$ with integer coefficients and no
constant term, generated from the single number $y=-1/p$:

$$
Q_1=y,
\qquad
Q_2=4y-y^2,
\qquad
Q_3=9y-6y^2+y^3,
\tag{10C.5}
$$

that is $q^{-1}$, $4q^{-1}-q^{-2}$ and $9q^{-1}-6q^{-2}+q^{-3}$. At $n=1$ this
is (15.1b): $Q_1=1/q$ is the value at the origin of that orbit's resolvent
kernel, and summing gives $\lambda_1=S_\xi(0)=\mu_0$. This is the precise sense
in which the pole is not merely a location: its reciprocal is the seed and the
coefficient of the entire one-orbit Li recurrence.

**What the critical line does.** For nonreal $\rho$ the fold has
$\Im q=t(1-2\beta)$, so $q$ is real exactly on $\beta=\tfrac12$ (6.4), where
$q=\tfrac14+t^2$. Hence

$$
\boxed{\;\Re\rho=\tfrac12
\iff q\in(\tfrac14,\infty)
\iff p\in(-\infty,-\tfrac14)
\iff y\in(0,4)
\iff |w|=1\;}
\tag{10C.6}
$$

the last equivalence because $|w|=1$ says $|\rho-1|=|\rho|$. The four conditions
are one condition in four coordinates; the excluded endpoint $y=4$,
$q=\tfrac14$, $w=-1$ is the collision $\rho=1-\rho$. On that range the
characteristic equation $r^2-(2-y)r+1=0$ of (10C.4) has both roots on the unit
circle — their product is $1$ and their sum $2-y$ lies in $(-2,2)$ — so
$w=e^{i\theta}$ with $2\cos\theta=2-y$, and (10C.3) becomes

$$
Q_n(y)=4\sin^2\frac{n\theta}{2}\ \ge\ 0,
\qquad
\sin^2\frac{\theta}{2}=\frac1{4q}
\tag{10C.7}
$$

**Both identities in (10C.7) hold for that orbit only under $\Re\rho=\tfrac12$.**
Off the line $w$ leaves the unit circle, $y$ leaves $(0,4)$, $q$ leaves the
positive real axis, and $Q_n$ takes complex values whose real parts carry no
sign constraint.

The nonnegativity in (10C.7) is not only trigonometric. Dossier §155A factors
the same polynomials on the same interval:

$$
Q_{2m+1}(y)=y\,\mathcal P_m(y)^2,
\qquad
Q_{2m}(y)=y(4-y)\,\mathcal B_{m-1}(y)^2
\tag{10C.8}
$$

with $\mathcal P_m$ the triangular-coefficient polynomials of (155A.2) and
$\mathcal B_r(y)=U_r(1-y/2)$ of (155A.4), the second being the diagonal $r=s$ of
that identity. The two weights $y$ and $y(4-y)$ are nonnegative exactly on
$[0,4]$, which is (10C.6) once more. So each individual reflected rung is an
algebraic square against an explicit weight, and the first few read

$$
Q_1=y,\quad
Q_2=y(4-y),\quad
Q_3=y(3-y)^2,\quad
Q_4=y(4-y)(2-y)^2,\quad
Q_5=y\,(y^2-5y+5)^2 .
\tag{10C.9}
$$

**What this does not do.** (10C.6) is a statement about one orbit and (10C.8) is
an identity in $y$; neither locates a zero. The coefficient $\lambda_n$ is a sum
over all orbits, and the criterion is $\lambda_n\ge0$ for **every** $n$ (15.1).
An orbit on the line contributes nonnegatively to every rung, and an orbit off
the line is not by itself in contradiction with any finite set of $\lambda_n$:
the sum can absorb a negative term. This section is a change of coordinates, not
a proof engine, and it leaves the position recorded in §R12 unchanged.

![One orbit in the four coordinates of (10C.1), at one height, with $\beta$ moved off $\tfrac12$. On the line the fold $q$ sits on the positive ray, the Li coordinate sits on the unit circle so that $w^{-1}=\bar w$, and every rung $Q_n$ is a square. Off the line the three break together: $\Im(1/q)\neq0$, $|w|\neq1$, and the rung column leaves the nonnegative axis. Every printed value is computed from $\beta$ and $t$ by the formulas of this section, and the rung column is generated from $y=1/q$ by (10C.4) alone. One orbit constrains nothing; §R12 and (15.1) are unchanged.](figures/figure75A_r10c_one_orbit_four_coordinates.png)


# Part IV. The Widder ladder and the sector geometry

This Part develops the reduced-Widder rung $W_k$ of
(R.3), and the criterion (R.4), proved by Stieltjes characterization
in Dossier (33.1).
**No finite prefix of this family is an RH statement.** Section R12 states the
position once: $W_1,\ldots,W_6>0$ is proved from the source alone, analytically
at the first rung and by one bundled certificate at the next five; a longer but
zero-assisted prefix comes from the verified height. Section R11 fixes the carrier,
R12A the shifted-resolvent basis, R13 the sector rectangle, and R14 one
prescribed scale.

## R11. Carrier, Cayley complement, and rungs

Everything in this Part is built from one identity of Part III: $S_\xi$ is the
sum of one simple pole per folded orbit, (9.7). Differentiating it produces the
resolvents $Z_r$; combining those produces the rungs. The object that makes the
combination work is the carrier.

For $x>0$ define

$$
\mathcal F_x(s)=\frac{1-s}{x+q(s)}
\qquad
u_x(q)=\mathcal F_x(s)\mathcal F_x(1-s)
=\frac{q}{(x+q)^2}
\tag{11.1}
$$

On the critical line $s=1/2+it$,

$$
\mathcal F_x\!\left(\frac12+it\right)
=\frac{\frac12-it}{t^2+x+\frac14}
\qquad
u_x(q)=\left|\mathcal F_x\!\left(\frac12+it\right)\right|^2\ge0
\tag{11.2}
$$

The reduced-Widder ladder is

$$
\boxed{
W_k(x)=j_{k-1}!\sum_{[\rho]}m_\rho
\left(\frac{q_\rho}{(x+q_\rho)^2}\right)^k
\qquad j_{k-1}=2k-1}
\tag{11.3}
$$

**Phase and the complete sum.** For positive $q$, the carrier is positive
and peaks at $q=x$. A nonreal conjugate pair contributes
$2|u_x|^k\cos(k\arg u_x)$. For $q=|q|e^{i\theta}$ and
$s_0=\log(x/|q|)$,
$4x|u_x(q)|=2/(\cosh s_0+\cos\theta)\le\sec^2(\theta/2)$,
with equality at $x=|q|$, where its phase vanishes. Also
$\arg u_x(q)=\theta\tanh(s_0/2)+O(\theta^3)$.
At a fixed nonzero phase $\phi$, this individual pair first becomes
strictly negative at $k=\lfloor\pi/(2|\phi|)\rfloor+1$.
This does not locate the first negative rung of the complete sum.

The correct all-zero evaluation retains the complex shifted ordinate:

$$
\begin{gathered}
\tau_\rho=(\rho-1/2)/i=\gamma+i(1/2-\beta),\qquad
q_\rho=1/4+\tau_\rho^2,\\
f_{k,x}(t)=\left[\frac{4x(t^2+1/4)}{(t^2+x+1/4)^2}\right]^k,\qquad
W_k(x)=\frac{(2k-1)!}{2(4x)^k}\sum_{\rho\ {\rm all}}m_\rho f_{k,x}(\tau_\rho).
\end{gathered}
\tag{11.3a}
$$

The factor one-half converts all zeros to reflection orbits.
Only on the line is $\tau_\rho$ the real ordinate $\gamma$.
Theorem 22A.1 proves at least $k$ Fourier sign changes on the positive
axis. Its $k=1$ transform is
$\frac\pi a e^{-a|u|}[4x-\frac{2x^2}{a^2}(1+a|u|)]$,
$a=\sqrt{x+1/4}$, negative beyond $(1+1/(2x))/a$ (below $\log2$
when $x>2.68$). The exponential-polynomial transform is not compactly
supported. Scalar Fourier nonnegativity cannot prove the rung sign;
a completed Weil-form or two-variable source argument is not excluded.
The verified-height sector result gives a lower bound on the earliest
possible negative rung, not an upper bound on how late it may occur.

```{=latex}
\begin{figure}[!tb]
\centering
\makebox[\textwidth][c]{\includegraphics[width=7.0in]{figures/v36_carrier.png}}
\caption{The carrier. \textbf{A:} $u_x(q)=q/(x+q)^2$ is positive for every $q>0$ and peaks at $q=x$. \textbf{B:} on the critical line it coincides with $|\mathcal F_x(\tfrac12+it)|^2$, so every power of it is nonnegative --- that is the whole of the positivity the hypothesis gives the rungs for free. \textbf{C:} off the line a conjugate pair contributes $2|u_x|^k\cos(k\arg u_x)$, the sector theorem of \S R13 excludes negative complete rungs through its stated finite order.}
\label{fig:carrier}
\end{figure}
```

The normalized Cayley complement

$$
t_x(q)=4xu_x(q)=\frac{4xq}{(x+q)^2}
\tag{11.4}
$$

lies in $(0,1]$ for $q>0$. Equivalently, with the scale-dependent coordinate

$$
c_x(q)=\frac{q-x}{q+x}
\tag{11.5}
$$

one has

$$
\boxed{u_x(q)=\frac{1-c_x(q)^2}{4x},\qquad
t_x(q)=1-c_x(q)^2}
\tag{11.6}
$$

In the log-scale variable $s=\log(q/x)$ these are hyperbolic functions:

$$
\boxed{c_x(q)=\tanh\frac s2,\qquad
u_x(q)=\frac{\operatorname{sech}^2(s/2)}{4x},\qquad
t_x(q)=\operatorname{sech}^2\frac s2}
\tag{11.7}
$$

and (11.6) is $1-\tanh^2=\operatorname{sech}^2$. So the rung (11.3) is a sum
of $\operatorname{sech}^{2k}$ bumps centred on the orbits in log-scale. The
half-maximum interval is exactly $|s|\le2\operatorname{arcosh}(2^{1/2k})$, so
the **half**-width is $\sim1.665109/\sqrt k$ and the **full** width is
$\approx3.330218/\sqrt k$. Multiplying the full window by the smooth mean
density gives a smoothed count
$\approx1.665\,k^{-1/2}\sqrt x\log(\sqrt x/2\pi)/2\pi$ of zeros a rung sees with
weight above one half. That is a high-height smoothed estimate and not a
bound on the actual count: at $x=q_1$ the first zero carries weight one for
every $k$, so no literal count there is below one. This is the same quadratic complement
that appears in the compact Hausdorff/Beta geometry. The disk fact $|c_x(q_\rho)|<1$ follows already from
$\Re q_\rho>0$ and carries no RH content by itself.


## R12. One ladder: explicit rungs, boundary moments, and proof channels

Write $S=S_\xi$. The differential and zero-side definitions are the same
object:

$$
\boxed{
W_k(x)=(-1)^{k-1}D_x^{2k-1}[x^kS(x)]
=(2k-1)!\sum_{[\rho]}m_\rho
\frac{q_\rho^k}{(x+q_\rho)^{2k}}}
\tag{12.1}
$$

The first six rows are

$$
\begin{aligned}
W_1={}&S+xS'\\
W_2={}&-6S'-6xS''-x^2S'''\\
W_3={}&60S''+60xS'''+15x^2S^{(4)}+x^3S^{(5)}\\
W_4={}&-840S'''-840xS^{(4)}-252x^2S^{(5)}
-28x^3S^{(6)}-x^4S^{(7)}\\
W_5={}&15120S^{(4)}+15120xS^{(5)}+5040x^2S^{(6)}\\
&+720x^3S^{(7)}+45x^4S^{(8)}+x^5S^{(9)}
\end{aligned}
\tag{12.2}
$$

$$
\begin{aligned}
W_6={}&-332640S^{(5)}-332640xS^{(6)}-118800x^2S^{(7)}\\
&-19800x^3S^{(8)}-1650x^4S^{(9)}-66x^5S^{(10)}-x^6S^{(11)}
\end{aligned}
\tag{12.2a}
$$

Leibniz's rule gives the coefficient of $x^jS^{(k+j-1)}$ as
$(-1)^{k-1}(2k-1)!\binom{k}{j}/(k+j-1)!$ for $0\le j\le k$.
They are the factorially weighted rows of \figref{fig:widder-grid}; equation (SW.6)
gives the exact conversion and the coefficient form of the recurrence.


Every next row is generated by the same centered odd coefficient:

$$
\boxed{
W_{k+1}=-j_kW_k'-xW_k''
=-x^{-2k}D_x\!\left[x^{2k+1}W_k'\right]
\qquad j_k=2k+1}
\tag{12.3}
$$

The repeated $2k+1$ is therefore the rung version of the centered coordinate
$j_n=2n+1$; it is also the odd derivative/factorial index in the confluent
Löwner hierarchy. For $k=4$,

$$
\boxed{W_5=-x^{-8}(x^9W_4')'}
\tag{12.4}
$$

Define the folded boundary moments
$\mu_r=\sum_{[\rho]}m_\rho q_\rho^{-r-1}$, for $r\ge0$. Then the exact
comparison at every rung is

```{=latex}
\begin{tnclosed}{boundary value of every rung}
```
$$
\boxed{\frac{W_k(0)}{(2k-1)!}=\mu_{k-1}=Z_k(0)}
\tag{12.4a}
$$
```{=latex}
\end{tnclosed}
```

Here $Z_r(x)=\sum_{[\rho]}m_\rho(x+q_\rho)^{-r}$ is the $r$-th shifted
resolvent, defined again with its derivative reading at (SW.2). Li's $\lambda$-coefficient expressions are printed in §R15.

\Needspace{12\baselineskip}

Here $F(s)=(s-1)\zeta(s)$ is the regularized source, distinct from the two-index
functional $F_{n,k}$ of (13.2).

| rungs | exact boundary value | proved positive for every $x>0$? | route, and the deepest source jet used |
|---|---|---|---|
| $W_1$ | $\mu_0$ | \PROVED{} analytic | source, through $F^{(2)}$ |
| $W_2,\ldots,W_6$ | $(2k-1)!\,\mu_{k-1}$ | \CERT{} A-CAT | source, one certificate, through $F^{(12)}$ (Dossier §74A) |
| $W_k$, $7\le k\le K_H$ | $(2k-1)!\,\mu_{k-1}$ | \CERT{} zero-assisted | verified height, §R13 |
| $W_k$, $k>K_H$ | $(2k-1)!\,\mu_{k-1}$ | \OPENSTAT{} | — |

**This is the position, stated once.** The first six rungs are positive for
every $x>0$, proved from the Gamma--prime source alone, with no zero ordinate,
no verified height and no use of RH: the first rung analytically, the next five
by the certificate of Dossier §74A, which covers $1\le s\le128$ by a complete
rational partition of continuum cells and $s\ge128$ by an exact analytic tail.
That certificate is bundled with this edition and re-executed by the v5.0 build on
two independent arithmetic backends. The verified-height theorem of §R13 is a
different channel — it uses verified zero locations — and it reaches every rung
index up to $K_H=4{,}712{,}664{,}392{,}502$, fixed exactly at (13.6), and none
beyond. From $W_7$ on, the source channel is open; all rungs at once is the
Riemann hypothesis itself.

This table is the controlling rung-status record for the whole volume; other
sections point to it rather than restate what is open.

**The boundary column does not need certifying.** The second column is
$W_k(0)=(2k-1)!\,\mu_{k-1}$, and those values are governed by one number.

```{=latex}
\begin{tnclosed}{boundary dominance}
```
Order the folded orbits so that $q_1<q_2\le|q_\rho|$ for every other orbit.
Then for every $k\ge1$

$$
\left|q_1^{\,k}\mu_{k-1}-1\right|\le C\left(\frac{q_1}{q_2}\right)^{\!k},
\qquad
C=q_2\!\!\sum_{[\rho]\neq[\rho_1]}\frac{m_\rho}{|q_\rho|}<\infty
\tag{12.7}
$$

With the verified zero data $q_1/q_2=0.45240\ldots$ of (9.10) and
$C=8.0019\ldots$, so the right-hand side falls below $1$ at $k=3$ and

$$
\boxed{W_k(0)>0\ \text{ for every }k\ge3,\ \text{with no hypothesis assumed}}
\tag{12.8}
$$
```{=latex}
\end{tnclosed}
```

*Proof.* Multiply (12.4a) by $q_1^{k}$: the first orbit contributes $1$ and each
other contributes $m_\rho(q_1/q_\rho)^k$. For $k\ge1$ and $|q_\rho|\ge q_2$,
$|q_1/q_\rho|^{k}\le(q_1/q_2)^{k}\,q_2/|q_\rho|$; summing gives (12.7). The
series converges because $|q_\rho|\asymp\gamma^2$ while the zero count is
$O(T\log T)$. When the bound is below $1$ the left side cannot reach $-1$, so
$q_1^{k}\mu_{k-1}>0$. $\square$

The constant $C$ has an exact bound that needs no zero-counting tail
estimate. Every orbit obeys $|\arg q|<\arctan(1/H)$ at the verified height
$H$, so $1/|q|\le\sqrt{1+H^{-2}}\,\Re(1/q)$, and absolute convergence gives

$$
\boxed{\ 0\le C-C_0\le q_2\lambda_1\bigl(\sqrt{1+H^{-2}}-1\bigr)\le\frac{q_2\lambda_1}{2H^2}\ },
\qquad C_0=q_2\Bigl(\lambda_1-\frac1{q_1}\Bigr)
\tag{12.7a}
$$

using $\sqrt{1+h}-1\le h/2$. The enclosures of $q_1$, $q_2$ and $\lambda_1$ are
recomputed in interval arithmetic by the v5.0 build (Dossier §96A.5), and
with (12.7a) they give, with no hypothesis,

$$
8.00193804616020\le C\le8.00193804616021.
$$

**What it says, and what it refuses to say.** It says the boundary values are
asymptotically a single real number, $\mu_{k-1}\sim q_1^{-k}$, with a geometric
error fixed by the first two zeros: the constant in (12.7) is
$C=q_2(\lambda_1-1/q_1)$ up to less than $6\times10^{-25}$ from orbits above
the verified height, and
$C(q_1/q_2)^3=0.741<1$ while $C(q_1/q_2)^2=1.64$, so $k\ge3$ in (12.8) is
where this argument starts. It also says that positivity **at the boundary
is free**: for $k\ge3$ it follows from the lowest zero being real, and would
survive almost any rearrangement of the zeros above the verified height.

So the boundary column of this table is not where the hypothesis lives. The
criterion (R.4) quantifies over every $k$ **and every $x>0$**, and $x=0$ is the
one place where the family is positive for reasons that have nothing to do with
the question. **A verification of boundary positivity, finite or infinite, is
not evidence for RH.** Positive boundary values do not control interference
between all orbits at positive scales. The single-orbit carrier identities
do not confine the complete sum to half-gap windows.

**The boundary, in the classical literature.** The boundary column is the
power-sum side of Newton's identities. With $e_n$ the Taylor coefficients of

$$
\frac{\xi\bigl(\tfrac12+\sqrt{\tfrac14+x}\bigr)}{\xi(1)}
=\prod_{[\rho]}\Bigl(1+\frac{x}{q_\rho}\Bigr)^{m_\rho}
=\sum_{n\ge0}e_nx^n,
\qquad
n\,e_n=\sum_{i=1}^{n}(-1)^{i-1}e_{n-i}\,\frac{W_i(0)}{(2i-1)!}
\tag{12.9}
$$

The ordinary coefficients $e_n$ in (12.9), normalized at $x=0$, form a
PF$_\infty$ sequence exactly when the completed genus-zero function has
only negative real zeros, hence exactly under RH [75]. This criterion
concerns every Toeplitz minor of this specified ordinary sequence.
The cited Turan and Jensen results [7,76--78] concern their own coefficient
normalizations and polynomial families. No transfer to these $e_n$ and all
these minors is proved here, so those finite-minor statuses are not assigned
to (12.9). The boundary power sums and the complete PF hierarchy are
different sign questions.

```{=latex}
\begin{figure}[!tb]
\centering
\makebox[\textwidth][c]{\includegraphics[width=7.0in]{figures/v37_first_zero.png}}
\caption{The first zero, in the volume's coordinates. \textbf{A:} the deviation
$q_1^{\,k}\mu_{k-1}-1$ against the bound of (12.7); from $k=3$ the bound is
below one, which is (12.8). \textbf{B:} Riemann's smooth count reaches one at
the first Gram point, while the first zero sits well below it; the gap is the
oscillating part $S(T)$, and at this height it is in charge.}
\label{fig:first-zero}
\end{figure}
```

Thus

$$
\boxed{W_1(x),W_2(x),W_3(x),W_4(x),W_5(x),W_6(x)>0\quad(x>0)}
\tag{12.5}
$$

The source certificate now closes the derivative sign

$$
\boxed{(x^9W_4')'<0
\quad\Longleftrightarrow\quad W_5>0}
\tag{12.6}
$$

without importing zero data, and the same certificate proves $W_6>0$.
Thus the independent Gamma--prime source prefix is $W_1,\ldots,W_6$.
The next scalar source task is
$W_7=-x^{-12}(x^{13}W_6')'>0$, equivalently
$(x^{13}W_6')'<0$, whose source expression reaches $F^{(14)}$. The recurrence remains
non-raising: a longer certified prefix does not supply an all-order induction.
The zero-assisted theorem in §R13 still extends much farther, to
$W_j>0$ for $1\le j\le K_H$.

\Needspace{10\baselineskip}

**One grid, several bases.** The coefficient-shape crosswalk in Section R12A
distinguishes row $k$, a segment of row $2k$, reflected positions, the central
column and Pascal anti-diagonals. The conversions are exact, but the lists
are not literally one row. Section R15 displays the worked $W_6$ triple.

| family | one entry is | how it meets the grid | defined at |
|---|---|---|---|
| $c_{k,j}$ | the grid entry itself | $(-1)^j\binom{k}{j}$ | (R.1b) |
| $u_x(q)$ | the carrier at one orbit | its $k$-th power expands using row $k$ | (11.1) |
| $Z_r(x)$ | the $r$-th shifted resolvent | the objects a row multiplies | (R.1c), (SW.2) |
| $W_k(x)$ | rung $k$ | row $k$ against $Z_k,\ldots,Z_{2k}$ | (R.3), (SW.4b) |
| $A_{k,j}$ | the coefficient of $x^jS^{(k+j-1)}$ | row $k$, factorially weighted | (SW.6) |
| $F_{n,k}(x)$ | the full Widder functional | row $k$, resolvent index shifted by $n$ | (13.2) |
| $\mu_r$ | the boundary moment $W_{r+1}(0)/(2r+1)!$ | row $k$ read at $x=0$ | §R12, (12.4a) |
| $h_n(x_0)$ | a Hausdorff entry at one scale | row $r$ is difference order $r$ | (14.1), (14.3a) |
| $\lambda_n$ | Li's coefficient | row $2k$ converts $\lambda$ to $\mu_{k-1}$ | (15.1a), (15.3a) |
| $B_{N,j}(a)$ | a completed Bernstein coefficient | row $N-j$ | §R17F |

**Implication lattice: direct arrows only.** Pairwise equivalence through RH
is mathematically true for the equivalent criteria but does not compare their
source difficulty, so those vacuous edges are not drawn. A displayed arrow
below is included only when the paper proves it without assuming RH.

| target | logical status | direct information retained here |
|---|---|---|
| all Widder signs (R.4) | **equivalent** | implies the necessary $W_7$ sign immediately |
| one-scale Hausdorff condition (14.2) | **equivalent** | no independent arrow to another source target is used |
| row-variation bound (BR.4) | **equivalent** | $\Longleftrightarrow$ (BE.3) by $\sqrt{\mathscr E_N}\le\mathcal V_N\le\sqrt{N+1}\sqrt{\mathscr E_N}$ |
| Laguerre-energy bound (BE.3) | **equivalent** | same direct row/energy equivalence as above |
| all-node Löwner sign (23.1) | **equivalent** | $\Longrightarrow$ the Stieltjes/Widder condition (R.4) by the Löwner–Pick/Stieltjes chain of §§R16–R17E |
| fixed taper $U_N=O_\epsilon(N^\epsilon)$, (155J.5) | **equivalent for that specified family** | no direct arrow to the matrix/source targets is proved |
| either curvature/boundary bound in (23.4) | **sufficient** | each $\Longrightarrow\mathrm{RH}$; no converse claimed |
| exact-prefix norm bound (155H.6) | **sufficient for the specified family** | no converse for arbitrary extensions |
| $W_7>0$ from the independent source | **necessary under RH; not sufficient** | next scalar source task only |

The only nontrivial arrows used by the program are therefore sparse. All other
connections either pass through RH itself or remain unknown. Part VIII records
ruled-out arrows and shortcuts; blanks are intentional information, not missing
editorial work.

## R12A. The same rungs in the shifted-zeta basis

The differential coefficients in (12.2) become ordinary Pascal coefficients
in a shifted resolvent basis. Define

$$
\mathcal Z(p;v)=\sum_{[\rho]}m_\rho(\tau_\rho^2+v)^{-p}
\qquad \tau_\rho=\frac{\rho-1/2}{i},\qquad
q_\rho=\tau_\rho^2+\frac14
\tag{SW.1}
$$

Here $\tau_\rho$ need not be real: this notation does not assume RH.
For $v=x+1/4$, $x\ge0$, the principal-power series is absolutely
convergent when $\Re p>1/2$. Conjugate folded orbits are retained together.
For positive integers $r$, write

$$
\boxed{Z_r(x):=\mathcal Z(r;x+1/4)
=\sum_{[\rho]}\frac{m_\rho}{(x+q_\rho)^r}
=\frac{(-1)^{r-1}}{(r-1)!}S_\xi^{(r-1)}(x)}
\tag{SW.2}
$$

For integers $n,k\ge0$, define the full Widder functional

$$
F_{n,k}[S_\xi](x)
=(-1)^nD_x^{n+k}[x^kS_\xi(x)]
=(n+k)!\sum_{[\rho]}m_\rho
\frac{q_\rho^k}{(x+q_\rho)^{n+k+1}}
\tag{13.2}
$$

Voros's shift identity [56, §6.1] reads
$\partial_v\mathcal Z(p;v)=-p\mathcal Z(p+1;v)$.
The elementary expansion $q=(x+q)-x$ now gives the full array:

$$
\boxed{\frac{F_{n,k}(x)}{(n+k)!}
=\sum_{j=0}^k(-1)^j\binom{k}{j}x^jZ_{n+j+1}(x)}
\tag{SW.3}
$$

For fixed $k$, every value of $n$ uses the same signed row $k$ of
\figref{fig:widder-grid}; only the resolvent index shifts. Its seed row is valid in this
full array: $F_{n,0}/n!=Z_{n+1}$ for $n\ge0$, and $F_{0,0}=Z_1=S_\xi$.
The reduced ladder instead selects $n=k-1$, which requires $k\ge1$.

In particular, with the odd factorial $(2k-1)!$ always in the denominator,

$$
\begin{aligned}
\tfrac{W_1}{1!}&=Z_1-xZ_2,
&\tfrac{W_2}{3!}&=Z_2-2xZ_3+x^2Z_4,
&\tfrac{W_3}{5!}&=Z_3-3xZ_4+3x^2Z_5-x^3Z_6,\\
\tfrac{W_4}{7!}&=\mathrlap{Z_4-4xZ_5+6x^2Z_6-4x^3Z_7+x^4Z_8,}\\
\tfrac{W_5}{9!}&=\mathrlap{Z_5-5xZ_6+10x^2Z_7-10x^3Z_8+5x^4Z_9-x^5Z_{10}}
\end{aligned}
\tag{SW.4}
$$

$$
\boxed{\ \tfrac{W_6}{11!}=Z_6-6xZ_7+15x^2Z_8-20x^3Z_9+15x^4Z_{10}-6x^5Z_{11}+x^6Z_{12}\ }
\tag{SW.4a}
$$

For all $k\ge1$, the diagonal $n=k-1$ of (SW.3) is

```{=latex}
\begin{tnclosed}{rung $k$ in $k+1$ terms, for every $k\ge1$}
```
$$
\frac{W_k}{(2k-1)!}
=\sum_{j=0}^k(-1)^j\binom{k}{j}x^jZ_{k+j}
=\sum_{j=0}^{k}c_{k,j}\,x^{j}Z_{k+j}
\tag{SW.4b}
$$
```{=latex}
\end{tnclosed}
```

No row of this identity is a truncation, an asymptotic, or a numerical fit.
Row $k$ of the grid is the complete answer for rung $k$, and the grid's own
recurrence writes any row directly. What the closed form does **not** supply
is the sign: knowing every coefficient of $W_k$ exactly says nothing on its
own about whether the sum is nonnegative, and that sign is the whole of the
open problem.

At $x=0$, (SW.4b) reduces to
$W_k(0)=(2k-1)!Z_k(0)=(2k-1)!\mu_{k-1}$, joining the Li dictionary in §R15.

```{=latex}
\begin{figure}[p]
\centering
\makebox[\textwidth][c]{\includegraphics[width=7.4in]{figures/v30c_widder_pascal_grid.pdf}}
\caption{The complete signed coefficient grid beside the $W_k$ arrays
(SW.4)--(SW.4a): all 171 entries $c_{k,j}=(-1)^j\binom{k}{j}$ for
$0\le k\le17$, $0\le j\le k$. The shaded seed is $c_{0,0}=+1$;
in the full array it gives $F_{0,0}=S_\xi$, without defining a reduced $W_0$.
For $k\ge1$, row $k$ multiplies $x^jZ_{k+j}$ in $W_k/(2k-1)!$.
Both edges and both halves are printed.}
\label{fig:widder-grid}
\end{figure}
```


**One grid, several coefficient chains.** With the convention
$c_{k,j}=0$ outside $0\le j\le k$, the signed Pascal array starts at

$$
\begin{gathered}
c_{k,j}=(-1)^j\binom{k}{j},\qquad c_{0,0}=+1,\\
c_{k+1,j}=c_{k,j}-c_{k,j-1},\qquad
\sum_{j=0}^k c_{k,j}z^j=(1-z)^k\quad(k\ge0).
\end{gathered}
\tag{SW.5}
$$

The row sum is $1$ at $k=0$ and $0$ for $k\ge1$, so the top-left $+1$ is the
algebraic seed of every displayed row.

**Raising the carrier to a power is the same act as taking a row.** Write $q=(x+q)-x$ and expand:

```{=latex}
\begin{tnclosed}{the carrier and the grid are one object}
```
$$
u_x(q)^{k}=\frac{q^{k}}{(x+q)^{2k}}
=\sum_{j=0}^{k}c_{k,j}\,\frac{x^{j}}{(x+q)^{k+j}}
\tag{SW.5a}
$$
```{=latex}
\end{tnclosed}
```

Summing (SW.5a) over the folded zeros with multiplicity gives (SW.4b)
immediately.

**Not every family occupies a whole row.** The table in §R12 gave the chains
and the identity that defines each; this one gives the shapes the remaining
families occupy. All index formulas continue beyond the finite rows printed in
\figref{fig:widder-grid}.

| family and location | shape in the grid | reading \figref{fig:widder-grid} |
|---|---|---|
| Li boundary rows, §R15 | **row segment** | Row $2k$, columns $k-1$ down to $0$, with common sign $(-1)^{k+1}$. |
| Half-Gamma, inverse Jacobian and pole ladder, (PR.10b)--(PR.10c), §R17C | **centre column** | The central entries $c_{2m,m}$, with the displayed sign and scale. |
| Reciprocal polynomials, Dossier §171 | **paired rows** | Two unsigned rows and the neighbouring-cell difference in (RP.3a). |
| Bernstein rows and Laguerre, §§R17F--R17G | **rescaled rows** | Row $N-j$ for each Bernstein entry; row $r$ divided by $j!$ for $L_r$. |
| Pascal energy matrix, §R17G | **anti-diagonals** | Entry $(r,s)$ is $(-1)^rc_{r+s,r}$: its anti-diagonal $r+s=k$ is unsigned row $k$, and its row $r=2$ is the triangular track $M(2,s)=T_{s+1}$. |
| Triangular tracks, this section | **columns** | Column $j=2$ is $T_{k-1}$; column $j=3$ is the running sum of triangular numbers. |

A shared shape is a shared coefficient list and nothing else. It transports
identities, and it transports no inequality: two families can occupy the same
row and still have unrelated signs, because the objects the coefficients
multiply are different.

**Two external instances, one each way.** The arrangement is not peculiar to
this volume. In a line running from Cloitre's tauberian approach of 2011 [67],
through the floor-function characterization that introduces *regular
arithmetic functions* [68], to the two-volume treatment of 2026 [69], a
triangular two-index kernel $G(n,k)$ with $G(n,n)\ne0$ is solved rank by rank
and assigned a *regularity index*: the exponent at which its partial sums
change behaviour. The Riemann hypothesis appears there as the statement that
Ingham's kernel $G(n,k)=(k/n)\lfloor n/k\rfloor$ has index $1/2$. The shared
triangular shape and the shared rank-by-rank solve carry structure and an
equivalence across, and carry no inequality: that index is a growth exponent,
not a sign. Read the other way, Xu [70] obtains positivity in every degree for
Chenevier's critical vectors by controlling the sign of every Verblunsky
coefficient of an associated circle measure. There the inequality does
transport, through a named mechanism rather than through a shared shape. The
two together mark the gap in which this volume works. Both are recorded as
read and are verified nowhere in this work.

**On the $k/n$ coordinate.** The reduced rational address $z=a/q$ of Dossier
§171 and the ratio $k/n$ inside Ingham's kernel are the same coordinate,
reached by different routes; the constructions raised on it are not the same
object, and the two indices are not the same quantity. The present work
reached its coordinate independently and without knowledge of [67]--[69],
which have priority in the published record.

For the differential basis write $W_k=\sum_{j=0}^k
A_{k,j}x^jS^{(k+j-1)}$, with $A_{k,j}=0$ outside this range. Then

$$
\begin{aligned}
A_{k,j}&=(-1)^{k+j-1}\frac{(2k-1)!}{(k+j-1)!}\,c_{k,j},\\
A_{k+1,j}&=-A_{k,j-1}-(2k+2j+1)A_{k,j}\\
&\hspace{9mm}-(j+1)(2k+j+1)A_{k,j+1},\qquad k\ge1.
\end{aligned}
\tag{SW.6}
$$

The first line is the substitution (SW.2); the second follows by
differentiating each term in (12.3). It generates the displayed arrays
from $A_{1,0}=A_{1,1}=1$. The polynomial source-jet arrays in Dossier
§§34--38 add the Jacobian substitution $S=L/R$, $D_x=R^{-1}D_s$ to
these same weighted rows; their additional factors are stated there.

The remaining finite arithmetic of the grid itself — how its columns read as
tracks, the reflection identity, the interior triangular collisions including
the eight positions of $3003$, the $k=0$ seed, and the odd factorial as an
accumulated triangular product — is worked in Dossier §173. None of it is used
below. The alternating rows encode cancellation, and neither they nor those
collisions supply positivity: the proof channels and their current depth are
exactly those tabled in §R12. Pearce-Crump [82] gives a recent external
example in which Selberg's single mollifier square is replaced by a
positive-semidefinite sum of three squared mollifiers and the resulting
arithmetic quadratic form is optimized; this is a methodological analogy only,
with no transfer asserted to the completed source here.

Dossier Theorem 32A.1 also represents every $F_{n,k}$ as a Laguerre
transform of the heat trace. Its scalar kernel has exactly $k$ simple
sign changes for $k\ge1$; an undifferentiated positive heat trace alone
does not supply the required sign.

## R13. Height-to-sector theorem and the full finite rectangle

For $q=a+ib$ with $a>0$,

$$
\arg u_x(q)=\arg q-2\arg(x+q)
\tag{13.1}
$$

As $x$ runs from $0$ to $\infty$, this phase moves continuously from
$-\arg q$ to $+\arg q$, crosses zero at $x=|q|$, and remains inside that
closed angular band. Consequently a folded zero cannot rotate a fixed power
outside the right half-plane once its height reaches the explicit threshold
$H\ge\cot(\pi/2M)$ proved below.

The full functional $F_{n,k}$ is defined at (13.2) in §R12A; its reduced
diagonal is $W_j=F_{j-1,j}$.

\Needspace{8\baselineskip}

> **Full zero-assisted sector theorem.** Suppose every nontrivial zero with
> $0<|\Im\rho|\le H$ lies on the critical line. Put
> $M=\max\{k,n+1\}$. Then
> $$
> \boxed{
> H\ge\cot\!\left(\frac{\pi}{2M}\right)
> \Longrightarrow F_{n,k}[S_\xi](x)>0\quad(x>0)}
> \tag{13.3}
> $$

To see the full two-index phase, put $\theta=\arg q$ and
$\phi=\arg(x+q)$. A summand has phase

$$
\alpha=k\theta-(n+k+1)\phi,\qquad
|\alpha|<\max\{k,n+1\}|\theta|\quad(\theta\ne0)
\tag{13.3a}
$$

For $x>0$, $\phi$ lies strictly between $0$ and $\theta$ when
$\theta\ne0$. If $\theta=0$, the summand is positive real and the strict
angular inequality is not needed. For an unverified zero above height $H$,
$|\theta|<\arctan(1/H)$, since
$\Re q=\gamma^2+\beta(1-\beta)>\gamma^2$ and
$|\Im q|=|\gamma(1-2\beta)|<|\gamma|$. Conjugate folded summands have
opposite phases, so their real sum is strictly positive under (13.3).

Platt and Trudgian proved the verified height

$$
H=3{,}000{,}175{,}332{,}800
\tag{13.4}
$$

and, in the same theorem, the full integer count: the lowest

$$
\boxed{12{,}363{,}153{,}437{,}138}
\tag{13.5}
$$

nontrivial zeros lie on the critical line [42]. The largest integer admitted
by the displayed height condition is now certified:

$$
\boxed{K_H=\left\lfloor\frac{\pi}{2\arctan(1/H)}\right\rfloor
=4{,}712{,}664{,}392{,}502}
\tag{13.6}
$$

Exact rational enclosures prove that the number inside the floor lies
strictly between $4{,}712{,}664{,}392{,}502$ and
$4{,}712{,}664{,}392{,}503$. Thus (13.3) gives

$$
\boxed{
F_{n,k}[S_\xi](x)>0
\quad
(x>0,\ 0\le n\le K_H-1,\ 0\le k\le K_H)}
\tag{13.7}
$$

The exact lineage is

$$
\boxed{\begin{aligned}
W_j&=F_{j-1,j}\\
G_{n,k}(x)&=\frac{x^n}{(n+k+1)!}F_{n,k+1}[S_\xi](x)\\
G_{r-1,r-1}&=\frac{x^{r-1}}{(2r-1)!}W_r
=\frac{x^{r-1}}{j_{r-1}!}W_r
\end{aligned}}
\tag{13.8}
$$

Hence the same theorem gives $G_{n,k}(x)>0$ for every $x>0$ and
$0\le n,k\le K_H-1$. The fixed-$x=56$ theorem instead bounds $n$ by
$6{,}901{,}269{,}318$ and permits every $k\ge0$; the two rectangles are
incomparable. On the reduced $W_j$ diagonal, the height-to-sector rectangle is stronger.

Differentiating the summands also gives

$$
\boxed{F_{n,k}'=-F_{n+1,k},\qquad
F_{n,k+1}=(n+k+1)F_{n,k}-xF_{n+1,k}}
\tag{13.9}
$$

Hence the certified rectangle includes finite strings of alternating
derivative signs. In its interior, $0\le n\le K_H-2$ and
$0\le k\le K_H-1$, one has

$$
0<-\frac{xF_{n,k}'}{F_{n,k}}<n+k+1
\tag{13.10}
$$

This is a finite, zero-assisted, computer-assisted theorem (A-CAT). It does not prove the
source-side $F^{(14)}$ inequality, and a finite rectangle—however large—does
not replace the all-order quantifier in RH.

![Four views of the sector mechanism: phase band, first cosine crossing, linear height-to-rung scale, and the blind-radius band pass.](figures/figure81_v26_widder_sector_atlas.png)

## R13A. How far the ladder is from the hypothesis, in one number

Dossier §48 writes the ladder at scale $x$ as a power series
$\mathcal G_x(z)=\sum_{k\ge1}W_k(x)z^{k-1}/(2k-1)!$ whose poles sit at
$z_x(q_\rho)=(x+q_\rho)^2/q_\rho$, and Dossier §49 proves that its radius
$R_x$ satisfies $R_x\ge4x$ for every $x$ exactly when RH holds. Three facts
locate the hypothesis inside that radius.

**The deficit identity.** For $q=|q|e^{i\theta}$ with $\Re q>0$ and $x>0$,

$$
\boxed{4x-|z_x(q)|=4x\sin^2\frac\theta2-\frac{(|q|-x)^2}{|q|}},
\qquad
\max_{x>0}\bigl(4x-|z_x(q)|\bigr)=\frac{(|q|-\Re q)(3|q|-\Re q)}{|q|}
\tag{13A.1}
$$

the maximum at $x=2|q|-\Re q$; at the blind radius $x=|q|$ the deficit is the
strictly smaller $2(|q|-\Re q)$, which for a zero at abscissa $\beta$ and
ordinate $\gamma$ is $(2\beta-1)^2(1+O(\gamma^{-2}))$. An off-line zero cuts
the radius at its own scale by a **height-free** reading of its distance from
the line.

**The exact remainder.** Write $d=2\beta-1$, $v=\gamma^2$, $c=\beta(1-\beta)$,
$A=\Re q=v+c$ and $w=|q|-A\ge0$, so that $w(2A+w)=vd^2$. The gap between the
deficit and the squared transverse displacement is not an estimate but an
identity, every factor positive off the line:

$$
\boxed{\ d^2-\max_{x>0}\bigl(4x-|z_x(q)|\bigr)
=\frac{w\bigl[w^2+c(3|q|-A)\bigr]}{v\,|q|}>0\ }
\tag{13A.1a}
$$

together with the two-sided chain

$$
\frac{4\gamma^2}{4\gamma^2+1}\,d^2\;<\;2w\;<\;\max_{x>0}\bigl(4x-|z_x(q)|\bigr)\;<\;d^2
\tag{13A.1b}
$$

Both are proved at Dossier (48.29)–(48.30); the lower bound reduces to
$v<v+\tfrac14$. This replaces the parabola estimate of earlier editions,
which carried an unnecessary height factor. On-line orbits have deficit
$-(q-x)^2/q\le0$. Hence

```{=latex}
\begin{tnclosed}{the last unit of radius}
```
$$
\boxed{\;4x-1<R_x\quad\text{for every fixed }x>0,\ \text{with no hypothesis assumed}\;}
\tag{13A.2}
$$

Put $\Delta=\sup_{x>0}(4x-R_x)$ and $d_\ast=\sup_\rho|2\Re\rho-1|$. The minimum
defining $R_x$ is attained at each $x$, so (13A.1a) gives
$\Delta\le d_\ast^2\le1$. **The displayed theorem is pointwise in $x$ and does
not assert $\Delta<1$.** A uniform restriction $\delta\le\Re\rho\le1-\delta$
gives $\Delta\le(1-2\delta)^2<1$; conversely $d_\ast=1$ forces $\Delta=1$ by
(13A.1b). Here $d_\ast=1$ is not attained: $\zeta(1+it)\ne0$ excludes a zero on
$\Re s=1$, so $d_\ast=1$ forces a sequence with
$|2\Re\rho_n-1|\to1$. Finiteness of the zero count below any fixed height then
forces $|\Im\rho_n|\to\infty$, and the factor
$4\gamma_n^2/(4\gamma_n^2+1)\to1$ in (13A.1b), giving $\Delta=1$. Thus
$\Delta<1$ is equivalent to a uniform zero-free strip of positive
width along **both** boundaries of the critical strip — not to the one-sided
$\Re s<1-\delta$ of earlier editions, which names the wrong region and, read
literally, excludes the line the known zeros are on. No such strip is known.
And $\Delta=0$ is RH (Dossier §49). Proofs: (48.31)–(48.32).

Two consequences. The high-scale statistic is strictly weaker: (48.33) gives
$\limsup_{x\to\infty}(4x-R_x)=\limsup_{|\gamma|\to\infty}(2\beta-1)^2$, and a
zero value there leaves finitely many off-line exceptions, or displacements
tending to zero, untouched. And at the verified height
$H=3{,}000{,}175{,}332{,}800$,

$$
0\le d_\ast^2-\Delta\le\frac1{4H^2+1}
=\frac1{36{,}004{,}208{,}110{,}166{,}363{,}023{,}360{,}001}
<2.8\times10^{-26}
\tag{13A.2a}
$$

Conditional on the carried height input, the displayed amount bounds the
gap between the two suprema. It is an error estimate, not a lower bound on
computational distinguishability or a numerical-impossibility theorem.
A uniform source estimate is still required to force $\Delta=0$.
```{=latex}
\end{tnclosed}
```

So the Euler product, whose absolute convergence stops at the parabola,
reaches the deficit $1$ and not one digit further — $1$ is the width of the
critical strip in these units, $(2\beta-1)^2\le1$ — and **the whole of the
hypothesis at scale $x$ is the last unit of $R_x$**. The deficit records
extremal transverse displacement and nothing else; relating it to
zero-density estimates or growth hypotheses needs a separate theorem with
explicit quantifiers, which the radius identity does not supply. (23.1) is
the statement that a source-side argument claims the whole unit.

**Where the series comes from.** With $a_k=(4x)^kW_k(x)/(2k-1)!
=\sum_{[\rho]}m_\rho t_x(q_\rho)^k$ and $w=\sin^2(\varphi/2)$,

$$
\boxed{\sum_{k\ge1}a_k(x)\,w^k
=4xw\,\frac{h(xe^{-i\varphi})-h(xe^{i\varphi})}{xe^{-i\varphi}-xe^{i\varphi}}
=2\tan\frac\varphi2\;\Im\,h\bigl(xe^{i\varphi}\bigr)},
\qquad h=xS_\xi
\tag{13A.3}
$$

The factorization
$1-t_x(q)w=(q+xe^{i\varphi})(q+xe^{-i\varphi})/(x+q)^2$ and
$\cos\varphi=1-2w$ prove the identity in its Taylor convergence disk,
with meromorphic continuation where defined. The rungs are its Taylor
coefficients in $w$. Here $h$ is the function whose Pick property is at
issue, not an unconditionally known Pick function. The conjugate-node
formula retains the reflection data that Section R20 requires.
The Euler-source representation (9.5) applies where
$\Re s_{xe^{i\varphi}}>1$; its domain is not a proof of the full Pick sign.

```{=latex}
\begin{figure}[!tb]
\centering
\makebox[\textwidth][c]{\includegraphics[width=7.0in]{figures/v38_last_unit.png}}
\caption{The last unit of radius. \textbf{A:} the deficit
$4x-|z_x(q)|$ for one on-line orbit and three planted off-line orbits at
height $45$. The blind-radius value $2(|q|-\Re q)$ and the larger maximum
at $x=2|q|-\Re q$ approach $(2\beta-1)^2$ as height tends to infinity.
\textbf{B:} the strictly positive single-orbit remainder $d^2-D(q)$,
with envelope $1/(4\gamma^2+1)$ and the carried height marker.
The weak global comparison $0\le d_*^2-\Delta\le(4H^2+1)^{-1}$
is an error bound, not a computational-impossibility statement. A uniform
boundary strip would imply $\Delta<1$; no such source estimate is proved.}
\label{fig:last-unit}
\end{figure}
```

## R14. One prescribed scale and the Hausdorff theorem

Fix any $x_0>0$ and define

$$
h_n(x_0)=(4x_0)^n\frac{W_{n+1}(x_0)}{(2n+1)!}
\tag{14.1}
$$

Then

$$
\boxed{
\mathrm{RH}\iff(h_n(x_0))_{n\ge0}
\text{ is a Hausdorff moment sequence on }[0,1]}
\tag{14.2}
$$

Equivalently,

$$
(-1)^r\Delta^rh_n(x_0)\ge0
\qquad(n,r\ge0)
\tag{14.3}
$$

With $\Delta h_n=h_{n+1}-h_n$, \figref{fig:widder-grid} supplies the difference weights:

$$
(-1)^r\Delta^rh_n(x_0)=\sum_{j=0}^r c_{r,j}h_{n+j}(x_0).
\tag{14.3a}
$$

Thus row $r$ tests difference order $r$; the seed row $r=0$ simply
returns $h_n$. The weights alone do not determine the sign of the sum.

The theorem holds at any one scale chosen in advance, but it requires all
orders at that scale. It is not a finite stopping rule.

# Part V. Li data, Löwner matrices, and the source-energy construction

The boundary values $\mu_{k-1}=W_k(0)/(2k-1)!$ connect the rungs to Li's
coefficients through (15.2). Section R15 gives that dictionary and the
positive reserve with its explicit arithmetic defect. Sections R16--R17E
separate the completed Gamma--prime matrix from its comparison models.
Sections R17F--R17H construct the fixed-scale energy and its cutoffs.
Section R17I connects an exact-divisor error to the same zeta denominator.
The source upper bounds remain unproved.

## R15. The central-Pascal boundary dictionary

Write $\xi$ for the completed function of §R9 and let $\rho$ run over its
zeros with multiplicity, folded as in §R9 so that $\rho$ and $1-\rho$ share
the single point $q_\rho=\rho(1-\rho)$. **Li's coefficients** are

$$
\boxed{\lambda_n=\sum_\rho\left[1-\left(1-\frac1\rho\right)^{\!n}\right]
=\frac1{(n-1)!}\,\frac{d^n}{ds^n}
\Bigl[s^{\,n-1}\log\xi(s)\Bigr]_{s=1}}
\tag{15.1a}
$$

the symmetrically grouped zero sum agreeing with the derivative definition
[5]. The normalization is Li's:
$\lambda_n$ is $n$ times Keiper's coefficient [57–58]. The first is the one this volume
uses, because it is a sum over the very orbits that carry the rungs: pairing
each zero with its mirror gives
$\rho^{-1}+(1-\rho)^{-1}=q_\rho^{-1}$, so at $n=1$

$$
\lambda_1=\sum_{[\rho]}\frac{m_\rho}{q_\rho}=S_\xi(0)=\mu_0,
\tag{15.1b}
$$

which is the value already used in §R10A. The rung chain and the Li chain are
therefore two readings of one set of folded data, and (15.2) below is the
conversion between them. Section R10C writes the one-orbit form of the same
reading: the resolvent pole $-q_\rho$ fixes $w_\rho$ through (10C.2), and the
recurrence (10C.4) then generates that orbit's whole column
$Q_n(q_\rho^{-1})$, of which the term displayed above is $n=1$.

Li's coefficients satisfy

$$
\mathrm{RH}\iff\lambda_n\ge0\quad(n\ge1)
\tag{15.1}
$$

The two chains are related by a single alternating transform on a doubled row
index. It is an identity, proved from (15.1a) and the folded resolvent, and it
is insensitive to where the zeros lie: the folded moments $\mu_{k-1}$ satisfy

$$
\boxed{
\mu_{k-1}=\sum_{j=1}^k(-1)^{j+1}
\binom{2k}{k-j}\lambda_j
\qquad
W_k(0)=(2k-1)!\mu_{k-1}}
\tag{15.2}
$$

The first six rows are printed because the indexing matters:

$$
\begin{aligned}
\mu_0&=\lambda_1\\
\mu_1&=4\lambda_1-\lambda_2\\
\mu_2&=15\lambda_1-6\lambda_2+\lambda_3\\
\mu_3&=56\lambda_1-28\lambda_2+8\lambda_3-\lambda_4\\
\mu_4&=210\lambda_1-120\lambda_2+45\lambda_3-10\lambda_4+\lambda_5\\
\mu_5&=792\lambda_1-495\lambda_2+220\lambda_3-66\lambda_4
+12\lambda_5-\lambda_6
\end{aligned}
\tag{15.3}
$$

These are exact segments of \figref{fig:widder-grid}, with a doubled row index:

$$
\mu_{k-1}=(-1)^{k+1}\sum_{j=1}^k c_{2k,k-j}\lambda_j.
\tag{15.3a}
$$

Read columns $k-1,k-2,\ldots,0$ of row $2k$, then apply the common
sign $(-1)^{k+1}$. For $k=6$, row 12 contributes
$(-792,495,-220,66,-12,1)$; reversing the common sign gives
$(792,-495,220,-66,12,-1)$ in the $\mu_5$ line. The $-220$ at
column 3 equals the reflected entry at column 9 in (SW.4h), Dossier §173,
and becomes
$+220\lambda_3$ here. The seven-term resolvent row for $W_6$ is row 6;
its six-term Li boundary row is this segment of row 12.

Thus $W_5(0)\leftrightarrow\mu_4$; the row ending
$+12\lambda_5-\lambda_6$ is $\mu_5=W_6(0)/11!$, not the $W_5$ row. This
alternating transform is exact but increasingly ill-conditioned, so it is a
dictionary rather than a stable numerical inversion method.

**One row, three readings.** At $k=6$, the signed grid
\figref{fig:widder-grid} gives these linked but distinct expressions:

$$
\begin{aligned}
\frac{W_6}{11!}&=Z_6-6xZ_7+15x^2Z_8-20x^3Z_9+15x^4Z_{10}-6x^5Z_{11}+x^6Z_{12}
&&\text{(SW.4a)}\\[3pt]
W_6&=-332640S^{(5)}-332640xS^{(6)}-118800x^2S^{(7)}-\cdots-x^6S^{(11)}
&&\text{(12.2a)}\\[3pt]
\mu_5&=792\lambda_1-495\lambda_2+220\lambda_3-66\lambda_4+12\lambda_5-\lambda_6
&&\text{(15.3)}
\end{aligned}
$$

The first two use row $6$, $1,-6,15,-20,15,-6,1$; the last uses
row $\mathbf{12}$, columns $5$ down to $0$. In the differential row,
the factorial weights $11!/(5+j)!$ are
$332640,55440,7920,990,110,11,1$.
The derivative conversion $Z_{6+j}=(-1)^{5+j}S^{(5+j)}/(5+j)!$
cancels the column alternation and leaves the common negative sign;
a global sign alone cannot cancel alternating columns.
The first expression is the scalar rung, the second is the source-derivative
basis, and the third is their Li boundary dictionary. A coefficient
conversion does not introduce an evaluated-source sign.

The same boundary moments occupy the confluent matrix; this is the precise
connection between the triangular coefficient image and the matrix image.
Locally at the origin,

$$
S_\xi(x)=\sum_{r\ge0}(-1)^r\mu_rx^r,\qquad
\frac{h^{(i+j+1)}(0)}{(i+j+1)!}=(-1)^{i+j}\mu_{i+j}
\tag{15.4}
$$

With indices $i,j=0,\ldots,N-1$, set
$H_N=[\mu_{i+j}]$ and $D_N=\operatorname{diag}((-1)^i)$. The normalized
confluent matrix is $C_N(0)=D_NH_ND_N$, so it has the same inertia as $H_N$.
For example,

$$
\boxed{H_3=\begin{pmatrix}
\mu_0&\mu_1&\mu_2\\
\mu_1&\mu_2&\mu_3\\
\mu_2&\mu_3&\mu_4
\end{pmatrix},\qquad
(H_3)_{ii}=\frac{W_{2i+1}(0)}{(4i+1)!},\quad i=0,1,2}
\tag{15.5}
$$

Thus the first five boundary rungs determine every entry of $H_3$.
Positive entries alone do not prove its principal minors positive; for
example, the first $2\times2$ condition is
$\mu_0\mu_2-\mu_1^2\ge0$. At positive nodes the corresponding object is the Löwner
divided-difference matrix $\mathcal L_h$ of (10.3), with
diagonal $W_1(x_i)$; its off-diagonal compatibility is the source comparison
in §R16. The all-size Hankel condition and the all-node Löwner condition are
RH-equivalent, whereas the finite scalar table in §R12 is already proved.

**The reflected odd form.** Define $\mathcal P_0=1$,
$\mathcal P_1=3-y$, and
$\mathcal P_{m+1}=(2-y)\mathcal P_m-\mathcal P_{m-1}$, with
$\mathcal P_m(y)=\sum_jd_{m,j}y^j$ and
$d_{m,j}=(-1)^j(2m+1)(m+j)!/((m-j)!(2j+1)!)$.
Dossier Section 155A proves

$$
\boxed{K_N=\mathsf C_NH_N\mathsf C_N^{\mathsf T},\qquad
K_{r,s}=\lambda_{r+s+1}-\lambda_{|r-s|},\qquad
K_{m,m}=\lambda_{2m+1},}
\tag{15.6}
$$

where $\mathsf C_N=[d_{r,j}]$ and $\lambda_0=0$. Its determinant is
$\pm1$, so the two matrices have identical inertia. For example,
$\lambda_3=9\mu_0-6\mu_1+\mu_2$: an odd Li diagonal already tests
original off-diagonal information. For the actual $\xi$, all odd Li
signs, even eventual ones, are RH-equivalent (Theorem 155A.2).
They are not the already positive boundary rung values.

Beta filtering $\mu_j\mapsto b_j^k\mu_j$ makes every fixed block with
positive diagonal positive at sufficiently large depth. Only one depth
fixed before all ranks retains the criterion (Section 104A). Signed
recovery uses $2m+1$ observations for $\lambda_{2m+1}$; positive outputs
alone need not give a positive value. Section 166E controls common-source
error at positive scale, not the regularized boundary of Section 155B.

**An explicit positive comparison.** Section 155C now constructs

$$
\boxed{K_N=\mathsf R_N-\mathsf D_N,\qquad \mathsf R_N\succ0,\qquad
c_* =\frac\pi4+\frac{\log2}{2}-1.}
\tag{15.7}
$$

The reserve is a Catalan-density Gram form weighted by a resolvent trace
of the even triangular sine modes. Its linear anchor is $c_*$ rather
than $\lambda_1$; the full cost
$(c_*-\lambda_1)(2\min(r,s)+1)$ stays in the arithmetic defect.
The original positive scalar reserve is indefinite as a matrix already
at rank two. All-rank domination $\mathsf D_N\preceq\mathsf R_N$ remains
unproved. Section 155D proves that any finite, polynomial, or all-rate
subexponential upper relative bound would suffice. Under RH the upper
extreme tends to one and the absolute norm grows linearly; a nonreal folded
point forces both signs at an exponential rate. Only a constant absolute
bound is ruled out. Section 155E's cosine basis makes the compensation
$\delta I$ and the remaining matrix explicit in one curvature sequence.

The recurring diagonal pictures now have a precise crosswalk:

| construction | diagonal operation | exact value or object |
|---|---|---|
| factorial extension (§R3) | identify the two input coordinates | the triangular value $T_x$ |
| Widder array (§R13) | select $(n,k)=(j-1,j)$ | $F_{j-1,j}=W_j$ |
| boundary Hankel matrix | set $i=j$ | $\mu_{2i}=W_{2i+1}(0)/(4i+1)!$ |
| positive-node Löwner matrix | coalesce the two nodes | $h'(x_i)=W_1(x_i)$ |

Each picture records its own exact specialization. The derivative and
moment identities above supply the links between them; matching diagonal
values alone does not settle the off-diagonal source comparison.


## R16. What $L_\Gamma$ and $L_P$ actually mean

Split the safe-axis formula (9.5) as

$$
S_\xi(x)=\frac1x+G(x)-P(x)
\tag{16.1}
$$

where

$$
G(x)=\frac{\psi((1+R)/4)-\log\pi}{2R}
\qquad
P(x)=\frac1R\sum_{n\ge2}\frac{\Lambda_{\rm vM}(n)}{n^{s_x}}
\quad R=\sqrt{1+4x}
\tag{16.2}
$$

Define the scalar channel functions

$$
h_\Gamma(x)=xG(x)
\qquad
h_P(x)=xP(x)
\qquad
h(x)=1+h_\Gamma(x)-h_P(x)
\tag{16.3}
$$

$L_\Gamma$ and $L_P$ are the ordinary Löwner divided-difference matrices of
the Gamma channel and the prime channel. Explicitly,

$$
[L_\Gamma]_{ij}=
\begin{cases}
\dfrac{h_\Gamma(x_i)-h_\Gamma(x_j)}{x_i-x_j},&i\ne j\\[2mm]
h_\Gamma'(x_i),&i=j
\end{cases}
\tag{16.4}
$$

and the same formula with $h_P$ gives $L_P$. Since the constant $1$ drops
out of divided differences,

$$
\boxed{\mathcal L_h=L_\Gamma-L_P}
\tag{16.5}
$$

The open statement is therefore a comparison:

$$
\boxed{
c^*(L_\Gamma-L_P)c\ge0
\quad\text{for every finite positive node set and every }c}
\tag{16.6}
$$

Neither channel is asserted positive separately. In fact $L_\Gamma$ already
has a negative $1\times1$ value near $x=0$:

$$
\lim_{x\downarrow0}h_\Gamma'(x)
=-\frac{\gamma_E+\log(4\pi)}2<0
\tag{16.7}
$$

Completion is therefore cancellation-first. The theorem, if proved, must
control the difference rather than dominate a negative prime matrix by an
independently positive Gamma matrix.

![One dictionary, two levels of positivity: the central-Pascal rows identify the boundary moments, and the Hankel and Löwner matrices test their compatibility. The rung status is controlled by §R12; the completed all-node sign remains open.](figures/figure75_li_pp97_loewner_study_atlas.png)

## R17. The Gamma triangular scaffold—and why it is not $L_\Gamma$

Antisymmetrize the Gamma logarithmic derivative across the two reflection
sheets. The result is the exact Cauchy transform

$$
\boxed{
\mathfrak G_\triangle(q)
=\frac12\sum_{m=0}^\infty
\frac1{q+2T_{2m}}}
\tag{17.1}
$$

Its poles are

$$
q=-2T_{2m}=0,-6,-20,-42,-72,\ldots
\tag{17.2}
$$

and its normalized form has an all-order positive Löwner Gram
representation. This is a genuine triangular theorem. It is nevertheless a
different object from the one-sheet safe-axis $h_\Gamma$ in (16.3). In the
completed function, the elementary and zeta terms cancel every pole of
(17.1). Substituting the positive scaffold for $L_\Gamma$ would therefore
discard the very completion coupling that the source problem requires.

![The Gamma triangular scaffold is positive before completion; completion cancels its apparent triangular poles.](figures/figure69_gamma_triangular_scaffold.png)

The quarter shift makes this normalization explicit:
$C(q)=\Gamma(s/2)\Gamma((1-s)/2)$, $q=s(1-s)$, satisfies
$-(\log C)'=2G_\triangle$.
Dossier Section 133A derives its even-triangular product and a positive
Li comparison model; neither replaces the completed source.

## R17A. The completed spectral zeta and its source signature

The sequence $A_n=1/(2T_{2n})$ of (TR.2) and the folded Riemann sequence
define two different
spectral zeta functions:

$$
\boxed{Z_A(p)=\sum_{n\ge1}(2T_{2n})^{-p},\qquad
\mathfrak Z_\xi(p)=\sum_{[\rho]}m_\rho q_\rho^{-p}
=\mathcal Z(p;1/4)}
\tag{VZ.1}
$$

Both series converge absolutely for $\Re p>1/2$. The first is built from
positive triangular numbers. The second uses the principal powers of
possibly complex, conjugate-paired $q_\rho$; positivity of those locations
is exactly the RH question. Their common critical exponent does not identify
their spectra.

For $1/2<\Re p<1$, the scalar Mellin resolvent identity gives

$$
\boxed{\mathfrak Z_\xi(p)
=\frac{\sin\pi p}{\pi}\int_0^\infty x^{-p}S_\xi(x)\,dx
=\frac{\sin\pi p}{\pi}\int_1^\infty
[s(s-1)]^{-p}\frac{\xi'(s)}{\xi(s)}\,ds}
\tag{VZ.2}
$$

In the second integral $x=s(s-1)=2T_{s-1}$ and $dx=(2s-1)ds$:
the source Jacobian cancels exactly. Completion must be combined before
integration near $s=1$; its separate elementary and prime poles cancel there.

Subtracting the large-$x$ terms of (OP.1) continues this expression across
the critical exponent. With $p=1/2+\varepsilon$,

$$
\boxed{\mathfrak Z_\xi(1/2+\varepsilon)
=\frac1{8\pi\varepsilon^2}
-\frac{\log(2\pi)}{4\pi\varepsilon}+O(1),\qquad
\mathfrak Z_\xi(0)=\frac78}
\tag{VZ.3}
$$

These are classical formulas of Voros [56, equations (40)--(41)], recovered
here from the completed source. The value at zero is an analytic
continuation value, not the ordinary trace of an infinite identity operator.
The two Laurent coefficients test more than the exponent $1/2$ alone.

Voros normalizes his completed function as $\Xi_V=2\xi$, so
$\Xi_V(0)=\Xi_V(1)=1$. This normalization leaves logarithmic derivatives
unchanged but matters when comparing determinants.

## R17B. Regularized triangular values: the fraction sequence

The continuation of (VZ.1) has a particularly simple triangular relation
at nonpositive integers. Let the signed Euler numbers be defined by

$$
\operatorname{sech}t=\sum_{j\ge0}E_{2j}\frac{t^{2j}}{(2j)!}
\qquad E_0,E_2,E_4,E_6,E_8=1,-1,5,-61,1385
\tag{TV.1}
$$

> **Triangular trace identity.** For every integer $m\ge0$, the analytic
> continuations satisfy
> $$
> \boxed{\mathfrak Z_\xi(-m)
> =\frac12\delta_{m0}+\frac{(-1)^{m+1}}2Z_A(-m)}
> \tag{TV.2}
> $$

The first values make both the sign pattern and the factor of two visible:

| $m$ | completed value $\mathfrak Z_\xi(-m)$ | triangular value $Z_A(-m)$ |
|---:|---:|---:|
| 0 | $7/8$ | $-3/4$ |
| 1 | $-1/16$ | $-1/8$ |
| 2 | $-1/16$ | $1/8$ |
| 3 | $-5/32$ | $-5/16$ |
| 4 | $-13/16$ | $13/8$ |
| 5 | $-227/32$ | $-227/16$ |

These are finite regularized values of divergent power sums. The negative
signs do not contradict positivity of an ordinary positive spectrum:
analytic continuation is not a positive summation operation.

**Proof.** The centered triangular identity gives

$$
2T_{2n}=4\left[\left(n+\frac14\right)^2-\frac1{16}\right]
\tag{TV.3}
$$

Expanding in the constant shift and continuing by the Hurwitz zeta function
yields, at $p=-m$,

$$
Z_A(-m)=4^m\sum_{j=0}^m\binom mj
\left(-\frac1{16}\right)^j
\zeta\!\left(-2(m-j),\frac54\right)
\tag{TV.4}
$$

Here the Hurwitz series is being continued as a family before the integer
is substituted. The Bernoulli-polynomial and Hurwitz identities [2, §25.11]

$$
\begin{aligned}
\zeta(-2r,a)&=-\frac{B_{2r+1}(a)}{2r+1}\\
B_{2r+1}(1/4)&=-\frac{(2r+1)E_{2r}}{4^{2r+1}}\\
\zeta(-2r,5/4)&=\frac{E_{2r}-4}{4^{2r+1}}
\end{aligned}
\tag{TV.5}
$$

reduce (TV.4) to a finite rational sum. Independently, the completed
Stirling expansion in (VZ.2), or Voros's trace formula [56, §6.1 and
Table 1], gives

$$
\boxed{\mathfrak Z_\xi(-m)=\delta_{m0}
-\frac1{2\,4^{m+1}}
\sum_{j=0}^m(-1)^j\binom mj E_{2j}}
\tag{TV.6}
$$

Substitution proves (TV.2), including the separate constant term at $m=0$.
Thus the result is an exact cross-identification of classical continuation
formulas with our triangular scaffold, with no claim of literature priority.

Replacing $p$ by $-1$ before continuing would suggest
$4\zeta(-2)+2\zeta(-1)=-1/6$. The continuation of $Z_A(p)$ instead gives
$Z_A(-1)=-1/8$. In an uncentered binomial continuation a coefficient
vanishing at $p=-1$ multiplies a zeta pole and leaves $+1/24$.
Equation (TV.4) keeps this contribution correctly. Formal linearity between
different regularization families would lose it.

The value $\zeta(-1)=-1/12$ of Dossier §172 reappears in that tempting
calculation; it does not by itself define the continuation of a quadratic
triangular family.

The identity at integers does not assert
$\mathfrak Z_\xi(p)=\tfrac12(-1)^{p+1}Z_A(p)$ as a function of $p$.
In fact their poles at $p=1/2$ have different orders. It also does not assert
that a completed zero equals a triangular scaffold pole.

## R17C. The odd-coordinate pole ladder and the determinant

The shifted family makes another coefficient sequence visible. At
$p=1/2-m$, the coefficient of the double pole of
$\mathcal Z(p;v)$ is

$$
C_m(v)=\frac1{8\pi}\frac{\Gamma(m+1/2)}{m!\Gamma(1/2)}v^m
=\frac1{8\pi}\binom{2m}{m}\left(\frac v4\right)^m
\tag{PC.1}
$$

This follows by shifting the leading double pole of the centered family
[56, equations (91)--(94)]. At $v=1/4$, write $C_m(1/4)=c_m/(8\pi)$.
Then

$$
\boxed{c_m=\frac{\binom{2m}{m}}{16^m},\qquad
c_0,c_1,c_2,c_3,c_4=1,\frac18,\frac3{128},\frac5{1024},\frac{35}{32768}}
\tag{PC.2}
$$

\figref{fig:widder-grid} makes this pole chain explicit:
$c_m=(-1)^m c_{2m,m}/16^m$, and
$C_m(v)=(-1)^m c_{2m,m}(v/4)^m/(8\pi)$.
Here the one-index $c_m$ denotes the scaled pole coefficient, while
the two-index $c_{k,j}$ denotes a signed grid entry. In particular,
the value $c_0=1$ uses the newly printed grid seed $c_{0,0}=+1$.

The recurring odd index has a direct coefficient role:

$$
\boxed{\frac{c_{m+1}}{c_m}
=\frac{2m+1}{8(m+1)}=\frac{j_m}{8(m+1)}}
\tag{PC.3}
$$

Compare the two recurrences horizontally, with $m\ge1$ in the Widder row:

$$
\underbrace{W_{m+1}=-j_mW_m'-xW_m''}_{\text{Widder differential ladder}}
\qquad
\underbrace{c_{m+1}=\frac{j_m}{8(m+1)}c_m}_{\text{central-binomial pole ladder}}
\tag{PC.4}
$$

They expose the same odd integer $2m+1$, through different operations.
One recurrence does not prove positivity of the other. A related determinant
count is exact rather than heuristic: a Vandermonde on $n$ nodes scales with
degree $T_{n-1}$, and for confluent multiplicities $m_i$ the surviving degree is
$T_{n-1}-\sum_iT_{m_i-1}=\sum_{i<j}m_im_j$. Raw derivative columns also
carry $\prod_i\prod_{j=0}^{m_i-1}j!$; Taylor-normalized jets remove that
factor. This is a bookkeeping check for confluent determinants, not a source sign.
At the first lower pole, for example,

$$
\mathfrak Z_\xi(-1/2+\varepsilon)
=\frac1{64\pi\varepsilon^2}
-\frac{3\log(2\pi)+4}{96\pi\varepsilon}+O(1)
\tag{PC.5}
$$

There is also a logarithmic companion to (TV.2):

$$
\boxed{Z_A'(0)=-\frac12\log(2\pi),\qquad
\mathfrak Z_\xi'(0)=\frac14\log(8\pi)
=\frac12\log2-\frac12Z_A'(0)}
\tag{PC.6}
$$

For completeness, differentiating the centered Hurwitz expansion of $Z_A$
at zero gives

$$
\begin{aligned}
Z_A'(0)
&=\frac34\log4+2\zeta'(0,5/4)
+\sum_{r\ge1}\frac{\zeta(2r,5/4)}{r16^r}\\
&=\frac34\log4-\log(2\pi)
+\log\Gamma(3/2)+\log\Gamma(1)\\
&=-\frac12\log(2\pi)
\end{aligned}
\tag{PC.7}
$$

The Gamma product identity sums the absolutely convergent series in the
first line, using $\zeta'(0,a)=\log\Gamma(a)-\tfrac12\log(2\pi)$
[2, equation 25.11.18]. Voros gives the completed value in (PC.6)
[56, equation (41)].
Both statements concern specified regularized determinants, not ordinary
products of infinitely many positive numbers.

More strongly, the full shifted derivative is

$$
\boxed{\left.\partial_p\mathcal Z(p;x+1/4)\right|_{p=0}
=\frac14\log(8\pi)-\log\frac{\xi(s_x)}{\xi(1)}}
\tag{PC.8}
$$

Indeed, differentiating the left side in $x$ gives $-S_\xi(x)$; its value
at $x=0$ is (PC.6). Thus a proposed positive model must match the full
$x$-dependent function on the safe axis, or its logarithmic derivative
together with the normalization at $x=0$. The determinant
$\xi(s_x)/\xi(1)$ is entire in $x$; its logarithm is not entire.
Matching a finite list of regularized constants does not establish this identity.

## R17D. What the triangular--Volterra benchmark establishes

The scaffold can be enlarged to have the correct critical pole order.
Let $A$ be the diagonal with entries $A_n=1/(2T_{2n})$ from (TR.2), and
let $B_a$
have eigenvalues $[\pi^2(n+a)^2]^{-1}$, $n\ge0$, $a>0$. Then

$$
Z_{A\otimes B_a}(p)=Z_A(p)\pi^{-2p}\zeta(2p,a)
\tag{BM.1}
$$

![Two spectral objects: the triangular--Volterra benchmark can match specified scalar data, whereas an exact realization of $S_\xi$ must match the whole function and its completed source. Calibration does not supply that equality.](figures/v26c_two_objects.png)

Define the convergent constant

$$
\kappa_\triangle=\frac{\gamma_E-\log2}{2}
+\sum_{n\ge1}\left(\frac1{\sqrt{2T_{2n}}}-\frac1{2n}\right)
\tag{BM.2}
$$

The double-pole coefficient of (BM.1) agrees with (VZ.3). Its simple-pole
coefficient agrees exactly when

$$
\boxed{\psi(a_*)=\log2+2\kappa_\triangle,\qquad
\frac74<a_*<2}
\tag{BM.3}
$$

Strict monotonicity of $\psi$ gives uniqueness. The bracket is supported
by an exact rational interval certificate; $a_*\approx1.75164355$ is
only a numerical orientation. It is not the exact quarter-step $7/4$.

At zero, however,

$$
Z_{A\otimes B_{a_*}}(0)=\frac34(a_*-1/2),\qquad
Z_{A\otimes B_{a_*}}(0)-\frac78
=\delta:=\frac{3a_*-5}{4}\in(1/16,1/4)
\tag{BM.4}
$$

An exact infinite-row adjustment matches this coefficient: replace the first
row $A_1B_{a_*}$ by $A_1B_b$, where
$b=a_*+\delta=(7a_*-5)/4$. Its zeta correction is

$$
A_1^p\pi^{-2p}\bigl[\zeta(2p,b)-\zeta(2p,a_*)\bigr]
\tag{BM.5}
$$

The correction is regular at $p=1/2$ and equals $-\delta$ at $p=0$.
The row perturbation has entries $O(n^{-3})$ and belongs to
$\mathcal S_p$ for $p>1/3$; it is infinite rank. Replacing a finite list
of positive entries by another list of the same length leaves all three
regularized data unchanged. By choosing a sufficiently long list, its sum
can also be adjusted to $\lambda_1$ while the untouched tail stays fixed.

Consequently positive models can match the two critical Laurent
coefficients, the value $7/8$, and the trace $\lambda_1$. The benchmark
is exact; it does not select the source:
redistributing two positive replacement entries at fixed sum changes
$\operatorname{Tr}D^2$ and therefore changes the resolvent.
The derivative (PC.6), lower poles such as (PC.5), and the exact fractions
in (TV.2) are additional tests. The decisive target remains (PC.8) for
every $x$, together with an independent proof of positivity.

The raw triangular--Volterra tensor is still easier to exclude. For
$(Vf)(u)=\int_0^u f(t)dt$ on $L^2[0,1]$, $V^*V$ has kernel
$1-\max(u,v)$ and trace $1/2$. Thus

$$
\operatorname{Tr}(A\otimes V^*V)=\frac{1-\log2}{2}\ne\lambda_1
\tag{BM.6}
$$

Its positivity is exact; its scalar source is different. No inference here
requires the particular tensor architecture to be unique.

## R17E. What the continuation retains about primes

The regularized fractions and polar coefficients are unusually explicit
because $\log\zeta(s)$ is exponentially small as real $s\to+\infty$.
It contributes no term to the algebraic Stirling expansion used in
(TV.6). Therefore even an entire ladder of those asymptotic coefficients
does not determine the prime-dependent remainder of the source.

Voros supplies a complementary integral that retains that remainder. Let
$\mathcal Z_c(p)=\mathcal Z(p;0)$ and distinguish the linear half-step
zeta function

$$
\mathcal S_{1/2}(z)=\sum_{n\ge1}(2n+1/2)^{-z}
=2^{-z}\zeta(z,5/4)
\tag{VP.1}
$$

For $0<\Re p<1/2$, his regular-integrand continuation is

$$
\begin{aligned}
\mathcal Z_c(p)
={}&-\frac{\mathcal S_{1/2}(2p)}{2\cos\pi p}\\
&+\frac{\sin\pi p}{\pi}\int_0^\infty t^{-2p}
\left[\frac{\zeta'}{\zeta}(1/2+t)+\frac1{t-1/2}\right]dt
\end{aligned}
\tag{VP.2}
$$

The apparent singularity of the bracket at $t=1/2$ is removable: the
zeta logarithmic derivative has residue $-1$ at its pole. Keep the two
terms inside the bracket combined. This is an unconditional continuation
formula [56, equation (74)], with a different centered parameter from
$\mathfrak Z_\xi(p)=\mathcal Z(p;1/4)$.

Equation (VP.2) is useful for deriving a completed source remainder before
seeking a sign. It does not display a positive kernel. The prime series
for $\zeta'/\zeta(1/2+t)$ converges only when $t>1/2$, so termwise use
of that series throughout the integral is invalid. Voros's separate raw
prime-cutoff resummation in equation (79) explicitly invokes RH; it cannot
serve as an unconditional forcing step here.

The same center gives another odd-index sequence [56, equation (81)]:

$$
\boxed{(\log|\zeta|)^{(2m+1)}(1/2)
=\frac{(2m)!}{2}(2^{2m+1}-1)\zeta(2m+1)
+\frac{\pi^{2m+1}}4|E_{2m}|,\quad m\ge1}
\tag{VP.3}
$$

For example, the third and fifth derivatives are
$7\zeta(3)+\pi^3/4$ and $372\zeta(5)+5\pi^5/4$.
These are derivatives in the real $s$ direction at $1/2$. They express
the vanishing odd derivatives of $\log\xi$ at its reflection center.
They do not fix the even derivatives or the all-node Löwner sign.

The first Stieltjes cumulant is
$\gamma_1^c=\gamma_1+\gamma_E^2/2\approx0.093773116$ [56–57].
The normalization is Li's. These conventions govern the sequence tables.

## R17F. The completed Bernstein row

Fix one prescribed scale $a>0$ and define the completed derivative row

$$
\boxed{B_{N,j}(a)=\frac{a^j}{j!(N-j)!}F_{j,N-j}(a),
\qquad0\le j\le N.}
\tag{BR.1}
$$

With $\theta=a/(a+q)$, each folded zero contributes a Bernstein row,

$$
B_{N,j}(a)=\sum_{[\rho]}\frac{m_\rho}{a+q_\rho}
\binom Nj\theta_\rho^j(1-\theta_\rho)^{N-j}.
\tag{BR.2}
$$

The scalar Widder carrier is the fold
$t_a(q)=4\theta(1-\theta)$; the full row retains $\theta$ and $1-\theta$
separately.  Its signed mass is exactly conserved,

$$
\sum_{j=0}^NB_{N,j}(a)=S_\xi(a),
\qquad
\mathcal V_N(a)=\sum_j|B_{N,j}(a)|\ge S_\xi(a).
\tag{BR.3}
$$

The existing scalar ladder sits on the central entries:
$B_{2k-1,k-1}=a^{k-1}W_k/[(k-1)!k!]$.  Thus the source-certified
$W_1,\ldots,W_6$ are visible inside the row, but no finite set of central
entries controls its total variation.

Section 164 proves the ordinary root-growth limit.  Consequently RH is
equivalent, at one fixed $a>0$, to the still-open source estimate

$$
\boxed{\forall\varepsilon>0\ \exists C_{a,\varepsilon}<\infty\ \forall N:\quad
\mathcal V_N(a)\le C_{a,\varepsilon}(1+\varepsilon)^N.}
\tag{BR.4}
$$

The verified-height theorem makes the row positive over an enormous finite
prefix; (BR.4) is an all-degree statement and is not supplied by that prefix.

## R17G. The same row as a positive energy

The Bernstein coefficients have an exact Laguerre realization

$$
\mathcal Q_N(t;a)=\sum_{j=0}^NB_{N,j}(a)L_j^{(0)}(t),
\qquad
\mathscr E_N(a)=\int_0^\infty e^{-t}|\mathcal Q_N(t;a)|^2dt
=\sum_{j=0}^NB_{N,j}(a)^2.
\tag{BE.2}
$$

Hence
$\sqrt{\mathscr E_N}\le\mathcal V_N\le\sqrt{N+1}\sqrt{\mathscr E_N}$.
Theorem 164.2 gives
$\mathscr E_N(a)\sim\mathcal K(a)\mathcal R(a)^{2N}/\sqrt N$, where
$\mathcal R(a)=\sup_q(a+|q|)/|a+q|$.  Under RH the energy decays like
$N^{-1/2}$; any off-line folded pair forces exponential growth.  The source
obligation is therefore equivalently

$$
\boxed{\forall\varepsilon>0\ \exists C_{a,\varepsilon}<\infty\ \forall N:\quad
\mathscr E_N(a)\le C_{a,\varepsilon}(1+\varepsilon)^{2N}.}
\tag{BE.3}
$$

The Gamma channel has a finite signed Stieltjes variation, so §166B isolates
the same open condition in the full prime source.  At the concrete scale
$a=2$ it becomes

$$
\boxed{\forall N\ge0:\quad
\mathscr E_N[P](2)\le\left(1+\log2+\frac\pi6\right)^2.}
\tag{BE.5}
$$

Theorem 166B.1 proves that this all-degree cap is RH-equivalent; it does not
prove the cap. The full derivations of the Bernstein involution, Pascal
Gram matrix and energy asymptotics are in earlier editions (Zenodo version
chain); this Reader keeps the objects and the exact unsupported line.

## R17H. What the prime-cutoff attack proves

The cap in (BE.5) is a statement about the full prime source at every
degree. Dossier §166C examines the natural attempt to pass to it from
finite Euler sums $P_X$. The sums include prime powers $n\le X$.
For each fixed degree their derivatives converge to those of $P$.
That convergence is not uniform over all degrees.

The sharp distinction appears in the last Bernstein coefficient:

$$
\boxed{B_{N,N}[P](a)\to\frac1a,\qquad
B_{N,N}[P_X](a)\to0\quad(X\text{ fixed})}
\tag{CUT.1}
$$

Both statements are unconditional. The full endpoint comes from the pole
$1/x$ after completion; the finite sum has only its signed continuous
cut measure. Their energy-norm distance therefore has lower limit at
least $1/a$. A fixed cutoff cannot approximate all degrees, even if RH
is true.

The positive contributions to this endpoint define an exact probability
distribution on prime powers. Theorem 166C.3 proves that their logarithms
have center $(N+1)/a$, variance $(N+1)(2/a+1/a^2)$, and a normal
limit. At $a=2$, half the endpoint mass is asymptotically captured near
$X=\exp((N+1)/2)$; fixed normal quantiles occur at

$$
\boxed{\log X_N=\frac{N+1}{2}
+v\sqrt{\frac{5(N+1)}4},\qquad
B_{N,N}[P_{X_N}](2)\to\frac{\Phi(v)}2}
\tag{CUT.2}
$$

Here $\Phi$ is the standard normal distribution function. This theorem
comes from the moving pole at $x=\omega(1+\omega)=2T_\omega$
of the shifted source $-\zeta'/\zeta(s_x-\omega)/R_x$.
It needs neither RH nor the prime number theorem. The triangular
coordinate is part of the residue calculation.

There is a second, stronger restriction on the cutoff strategy:

$$
\boxed{\sup_{X\ge2,\ N\ge0}
\frac{\mathscr E_N[P_X](2)}{(1.01)^{2N}}=\infty}
\tag{CUT.3}
$$

Theorem 166C.4 proves this by the exact row generating function and
the pole of zeta at one. A uniform bound over all raw cutoffs would
force bounded Euler partial sums at $s=3/4+i/4$, contradicting that
pole by Abel summation. The obstruction is independent of zero locations.

Theorem 166D.1 now proves the full-row error bound for the prescribed
schedule $X_N=20^{N+1}$ at $a=2$, with an explicit remainder tending to
zero. Endpoint recovery alone is insufficient, but this entire-row
approximation is proved. What remains open is the RH-equivalent bound
$\sup_N\|\mathcal Q_N[P_{20^{N+1}}](\cdot;2)\|_{L^2(e^{-t}dt)}<\infty$
of (166D.2). Section 166E transfers the same error to fixed-degree
filtered outputs at a positive scale, not to unregularized boundary data.

**Growing approximations at one fixed scale.** Section 166D also proves
whole-row convergence for $X_N=13^{N+1}$. Direct Cauchy estimates in
Section 166E control every recovered degree $2m\le N$ at $5^{N+1}$.
These are different bounds. For the full degree-below-$d$ mixed jet block,
Section 166F uses the sharper constant
$\Sigma_d=9(9^d-9^{-d})/128+3d/8$ and cutoff $X_d=5^{2d-1}$.
Its reserve-normalized common error tends to zero.
The target there is a separately defined completed matrix at $a=2$,
not a boundary Li matrix. A polynomial upper bound on its largest
normalized cutoff-defect eigenvalue would imply RH; that bound remains
unproved. Neither convergence nor a finite computed prefix supplies it.


**A separate route to the actual boundary.** Section 166G forms the
finite Taylor polynomial

$$
\widehat S_d(z)=\sum_{\ell=0}^{15d-1}
 \frac{S_{8^{15d}}^{(\ell)}(2)}{\ell!}(z-2)^\ell.
\tag{CUT.4}
$$

It evaluates this polynomial at zero, never the raw cutoff. Both the
completed Taylor remainder and the finite prime-tail error are controlled;
the full boundary rank-$d$ error, normalized by the same reserve, is
$O(d\Theta^d)$ with $\Theta=36(18/23)^{15}<1$.
The boundary defect's polynomial upper bound remains unproved.
Independent coefficient rounding has an additional error budget.

## R17I. Exact divisors and one denominator residual

Accurate boundary reconstruction leaves an arithmetic question: why should
the actual signed source remain bounded? Sections 155F--155G test what
information a proof must use. The regularized direct curvature formula
keeps a polynomial counterterm and a finite endpoint. A PNT-size envelope
alone, even with nonnegative integer weights, admits a fixed countermodel
with superexponential positive even curvature. A second model retains
actual prime-power support, any fixed exact prime prefix, positive Euler
coefficients and the same envelope, yet has exponentially growing
curvature on every fixed progression. Neither model retains the actual
completed source or all its divisor identities.

The actual denominator is $\mathcal B(z)=z\zeta(1/(1-z))$, with its
removable value $\mathcal B(0)=1$. Its Taylor coefficients
$b_n^{\rm den}$ obey the signed convolution (155G.3); they are not the
Beta weights of Section 104A. They are not all positive: already
$b_1^{\rm den}=\gamma_E-1<0$, and after the numerically positive run
$b_2^{\rm den},\ldots,b_{16}^{\rm den}$ the directed enclosure
$b_{17}^{\rm den}<0$ shows the sign changing again. Their square sum
$\log(2\pi)-\gamma_E$, the constant of (GA.3) and (GA.6), does not supply a
lower bound for the denominator.
Section 155I connects this denominator to a different use of the exact
arithmetic, rather than inferring positivity from its coefficients.

Write $\mu(d)$ for the Möbius function. The actual laws
$\Lambda*1=\log$ and $\mu*1=\delta_1$ imply, for
$N=\lfloor X\rfloor$,

$$
 \sum_{k=1}^N M\!\left(\log\frac Xk\right)
 =\log(N!)-XH_N+N,\qquad H_N=\sum_{k=1}^N\frac1k.
\tag{DIV.1}
$$

Now take finitely supported real coefficients $c_d$ with
$\sum c_d/d=0$ and set $D_c(s)=\sum c_dd^{-s}$,
$h_c(x)=1-\sum c_d\lfloor x/d\rfloor$. Balance cancels the linear
term in the floors. The resulting squared error is

$$
\boxed{\mathscr N(c)=\int_1^\infty h_c(x)^2\frac{dx}{x^2}
=\sum_{n\ge1}\frac{h_c(n)^2}{n(n+1)}.}
\tag{DIV.2}
$$

Here $1/[n(n+1)]=1/(2T_n)$ is the integral over one unit interval.
The square follows the signed arithmetic sum; it does not replace each
term by an independent absolute budget. If $c_d=\mu(d)$ for $d\le K$,
then $h_c=0$ on $[1,K+1)$. Every zero $\rho=\sigma+i\gamma$ with
$\sigma>1/2$ would force

$$
\boxed{\mathscr N(c)\ge
\frac{2\sigma-1}{|\rho|^2}(K+1)^{2\sigma-1}.}
\tag{DIV.3}
$$

Section 155H proves this by Mellin evaluation at the zero and
Cauchy--Schwarz on the remaining tail. Section 155J now fixes one explicit
linear-taper family
$V_N(s)=\sum_{d\le N}\mu(d)(1-d/N)d^{-s}$ and proves
$$
\boxed{\lim_{N\to\infty}
\frac{\log(1+U_N)}{\log N}=2\Theta_\zeta-1},
\qquad \Theta_\zeta=\sup_\rho\Re\rho .
\tag{DIV.3a}
$$
Its balanced dyadic plateau has the same exponent. Hence RH is equivalent,
for this specified family, to $U_N=O_\epsilon(N^\epsilon)$ for every
$\epsilon>0$; one fixed unbounded index set is enough. The proof uses the
classical zero-free-half-plane estimate quoted in [25] and the exact-prefix
lower bound above. It does not prove boundedness or convergence under RH.

The same section also records a distinct scalar target
$B_{\log}(x)=1-\sum_{d\le x}(\mu(d)/d)\log(x/d)$. RH is equivalent to
$B_{\log}(n)\le C_\epsilon n^{-1/2+\epsilon}$ on the eventual integer
tail. Section 155J now proves a logarithmic-chord interpolation theorem: it is
enough to verify the corresponding bound at all sufficiently large fourth
powers $k^4$, or at the squared triangular samples $T_k^2$. This is structured
sampling, not permission to use an arbitrary sparse set. The canonical prefix
family is also shown to have exact power exponent $2\Theta_\zeta-1$, while
the fixed taper has the unconditional bound
$U_N\ll N\exp(-c\sqrt{\log N})$ for some $c>0$. None is yet subpower
unconditionally.

The two approaches meet in one exact identity. Put
$\mathcal C_c(z)=D_c(1/(1-z))/z$, filling its removable value. Then

$$
\boxed{\begin{aligned}
1-\mathcal B(z)\mathcal C_c(z)&=\sum_{n\ge0}r_n(c)z^n,\\
r_n(c)&=\int_0^\infty e^{-u}h_c(e^u)L_n^{(0)}(u)du,\\
\mathscr N(c)&=\sum_{n\ge0}|r_n(c)|^2.
\end{aligned}}
\tag{DIV.4}
$$

This is the normalized Hardy coefficient norm, proved by the complete
Laguerre expansion in Section 155I. It is not the finite row energy
$\mathscr E_N$ or the curvature sequence $I_n$. Section 155J further writes
the same norm as a weighted sine integral and isolates the signed mixed
Möbius sum $\mathcal X_N$, with
$U_N-\mathcal X_N=\kappa\log N+\kappa_0+o(1)$. Thus the closing arithmetic
task may be stated as a one-sided subpower bound for $\mathcal X_N$, or as
the scalar $B_{\log}$ decay above. Neither bound is established. A finite
coefficient prefix still gives only a lower bound on the full norm.


# Part VI. Translation defects and reflection contours

The defects record what an off-line zero would leave behind. Sections
R18--R18B compare the translation, Beta and varying-endpoint forms;
R19 gives stationary-symbol blindness; R20 gives the reflection contour
and the missing conjugation. Sections R21--R21B connect strict one-node
defects, heat and signed-row growth. The completed detectors vanish under
RH, but none has been forced to vanish from the source.

## R18. Positive defects with a negative scalar anchor

On the resolvent test span, the archimedean channel admits the exact
translation-defect form

$$
\boxed{
Q_\Gamma(F)=a_\Gamma\|F\|_2^2
+\frac12\int_0^\infty
\|(I-\tau_v)F\|_2^2\,
\frac{e^{v/2}}{2\sinh v}\,dv}
\tag{18.1}
$$

with

$$
a_\Gamma=\frac12\left(\psi\!\left(\frac14\right)-\log\pi\right)
=-\frac{\zeta'}{\zeta}\!\left(\frac12\right)<0
\tag{18.2}
$$

The identity is exact; the right side is not manifestly nonnegative because
the scalar anchor is negative. The equality in (18.2) uses analytic
continuation at the functional-equation center. It is not the divergent prime
mass $\sum\Lambda(n)/\sqrt n$.

The compact Beta measure $2(1-u)\,du$ of (4.5) and the Gamma defect density
in (18.1)
are different measures with different supports, total masses, and moment
growth. Their shared triangular language does not make them interchangeable.

![Compact Beta moments and the infinite Gamma translation-defect measure must remain separate.](figures/figure78_beta_and_gamma_measure_separation.png)

## R18A. Beta and Volterra forms side by side

The compact triangular moment measure and the Volterra operator are both
positive, but they produce different quadratic forms. For $F\in L^2[0,1]$,
put

$$
\mathcal B[F]=2\int_0^1(1-u)|F(u)|^2du
\qquad \mathcal Q[F]=2\|VF\|_2^2
\tag{VG.1}
$$

With $K(u,v)=1-\max(u,v)$, their exact difference is

$$
\boxed{\begin{aligned}
\mathcal B[F]-\mathcal Q[F]
={}&\int_0^1(1-u)^2|F(u)|^2du\\
&+\int_0^1\!\int_0^1K(u,v)|F(u)-F(v)|^2du\,dv>0
\end{aligned}}
\tag{VG.2}
$$

for nonzero $F$. To check the coefficients, use
$\int_0^1K(u,v)dv=(1-u^2)/2$ and expand the square.
The strict difference supplies an exact comparison, not an equality with
the completed Gamma--prime form.

For logarithmic characters $e_L(u)=e^{2\pi iLu}$, use the inner product
conjugate-linear in its first slot, and set
$E(t)=\int_0^1e^{2\pi itu}du$. The Volterra Gram entries are

$$
\boxed{Q(L,M):=2\langle Ve_L,Ve_M\rangle
=\frac{E(M-L)-E(-L)-E(M)+1}{2\pi^2LM}}
\tag{VG.3}
$$

The values at $L=0$ or $M=0$ are defined by continuous extension. In
particular,

$$
Q(L,L)=\frac{1-\sin(2\pi L)/(2\pi L)}{\pi^2L^2}
\qquad Q(0,0)=\frac23
\tag{VG.4}
$$

The negative phases in (VG.3) are the conjugates of the positive phases;
$Q(M,L)=\overline{Q(L,M)}$. Positivity follows from its Gram definition.
Nevertheless, normalized adjacent entries satisfy

$$
\frac{Q(\log n,\log(n+1))}
{\sqrt{Q(\log n,\log n)Q(\log(n+1),\log(n+1))}}
\longrightarrow1
\tag{VG.5}
$$

The fixed interval therefore leaves neighboring logarithmic frequencies
strongly coherent. Positivity alone does not give the cancellation required
by the completed source.

## R18B. A varying-endpoint Gram candidate

One way to change that coherence is to let the interval length vary with
the integer label. Define

$$
\phi_n(u)=n^{-1/2}{\bf1}_{[0,n]}(u)e^{2\pi i(\log n)u}
\qquad J_L(a)=\int_0^L e^{2\pi iau}du
\tag{EG.1}
$$

Its exact Gram matrix is

$$
K_{mn}=\langle\phi_m,\phi_n\rangle
=\frac{J_{\min(m,n)}(\log(n/m))}{\sqrt{mn}}
\qquad K_{nn}=1,\quad K_{nm}=\overline{K_{mn}}
\tag{EG.2}
$$

For every fixed positive integer $k$,

$$
\boxed{K_{n+k,n}=-\frac{k}{2n}+O_k(n^{-2})}
\tag{EG.3}
$$

Indeed, $n\log(1+k/n)=k-k^2/(2n)+O_k(n^{-2})$; the leading
phase is an integer multiple of $2\pi$. This gives a contrasting pair of
adjacent limits: fixed-interval Volterra coherence tends to $1$, whereas
the varying-endpoint Gram entry tends to $0$.

The estimate is for fixed $k$ and is not a uniform bound on growing
matrices. For any fixed signed nonzero integer $k$, its leading term is
$-|k|/(2n)$; (EG.3) uses $k>0$. Also, the $2\pi$ frequency scale and endpoint length must be
transported together: removing $2\pi$ while leaving the endpoints unchanged
destroys the integer-phase cancellation.

> **Candidate boundary.** The Gram positivity in (EG.2) is proved.
> Section 161 now excludes its fixed ordinary tensor-norm translation lift
> as the completed realization, for finite sums and strongly convergent series.
> Singular form limits or a different source-defined realization remain
> open and must match the complete source, with a specified domain and topology.

For example, expanding a candidate norm involving
$\phi_n\otimes(I-\tau_{\log n})F$ introduces mixed translations
$\log(n/m)$. Equal reduced ratios must be grouped before a coefficient
is declared noncancellable. The stronger obstruction in §161 uses the
absolutely continuous Fourier density of the regular lift; mixed shifts
alone do not prove a no-go theorem.

## R19. Why stationary symbols are blind

Put

$$
\Phi(s)=\frac{\xi'(s)}{\xi(s)},\qquad s=\sigma+it
\tag{19.1}
$$

Away from zero ordinates, $\xi(1/2+it)$ is real, so

$$
\Re\Phi\!\left(\frac12+it\right)=0
\tag{19.2}
$$

In the distributional boundary value, a functional-equation pair at
$\beta=1/2\pm\delta$ cancels exactly. The surviving stationary symbol is

$$
\Omega(t)=\pi\sum_{\rho:\,\Re\rho=1/2}
m_\rho\delta_{\Im\rho}(t)\ge0
\tag{19.3}
$$

unconditionally. Thus a construction that collapses internally to this
scalar multiplier has erased the off-line information. The no-go is scoped:
it rejects premature stationary compression, not the translation covariance
of the final Weil form.

**The scalar-weight class is closed too, and by an inequality rather than a
cancellation.** For real $\alpha\neq0$,
$-\alpha g_F(v)=\tfrac12\lVert(I-\alpha\tau_v)F\rVert_2^2-\tfrac{1+\alpha^2}2\lVert F\rVert_2^2$,
so rewriting the prime channel with per-frequency scalar weights $\alpha_m>0$
forces a coefficient of $\lVert F\rVert^2$ equal to
$\sum_m\lambda_m(\alpha_m+\alpha_m^{-1})/2\ge\sum_m\lambda_m=+\infty$, with
$\lambda_m=\Lambda(m)/\sqrt m$, because $\alpha+\alpha^{-1}\ge2$. The
divergence of the scalar defect is therefore not an artifact of the unit
weight; it is forced by the arithmetic--geometric mean. The surviving class
is the *operator*-weighted one, and it is open.

## R20. Reflection contour and the missing conjugation

For a finite positive node set and real coefficients define

$$
\Psi_X(q)=\sum_{i=1}^N\frac{c_i}{x_i+q}
\qquad
\mathscr L_F(s)=q(s)\Psi_X(q(s))^2
\tag{20.1}
$$

Use the explicitly meromorphic carrier
$\mathcal F_X(s)=(1-s)\Psi_X(q(s))$, so
$\mathscr L_F(s)=\mathcal F_X(s)\mathcal F_X(1-s)$.
The real-frequency symbol is its boundary restriction
$\widehat F(t)=\mathcal F_X(1/2+it)$. Here the convention is
$\widehat F(t)=\int_{\mathbb R}F(u)e^{-itu}\,du$ for the real
resolvent combination $F=\sum_i c_if_{x_i}$ defined in (153.5).
The positive-sign transform is $\overline{\widehat F(t)}$ and has
numerator $1/2+it$ in each summand. Only the meromorphic carrier is
evaluated at complex zeros; a real-frequency Fourier formula is not
silently continued there.

The test symbol is reflection-even, while $\Phi$ is reflection-odd:

$$
\mathscr L_F(1-s)=\mathscr L_F(s)
\qquad
\Phi(1-s)=-\Phi(s)
\tag{20.2}
$$

For

$$
1<\sigma_0<\min_i\frac{1+\sqrt{1+4x_i}}2
\tag{20.3}
$$

the exact folded zero form is

$$
\boxed{
Q_X(c)=\sum_{[\rho]}m_\rho\mathscr L_F(\rho)
=\frac1{2\pi i}\int_{(\sigma_0)}
\mathscr L_F(s)\Phi(s)\,ds}
\tag{20.4}
$$

At $s=1/2+it$,

$$
\mathscr L_F\!\left(\frac12+it\right)=|\widehat F(t)|^2\ge0
\qquad
\Phi\!\left(\frac12+it\right)\in i\mathbb R
\tag{20.5}
$$

The positive terminal object and the pairing are orthogonal. The critical-line
integral is zero only as a symmetrically indented principal value; the
integrand is not zero. The RH content lies in shifting the contour and
collecting residues.

The type mismatch can now be stated without shorthand:

$$
\underbrace{\mathcal F_X(\rho)\mathcal F_X(1-\rho)}_{\text{reflection; bilinear}}
\quad\hbox{versus}\quad
\underbrace{\mathcal F_X(\rho)\overline{\mathcal F_X(\rho)}}_{\text{conjugation; Hermitian}}
\tag{20.6}
$$

For a fixed real-coefficient test and $0<\Re s<1$, away from the
test poles, their pointwise agreement is exactly

$$
\mathcal F_X(s)\mathcal F_X(1-s)=|\mathcal F_X(s)|^2
\iff \sigma=1/2\ \text{or}\ \Psi_X(q(s))=0
\tag{20.6a}
$$

For example, nodes $(1,2,3)$ and coefficients $(1289,-5330,4553)$ give

$$
\Psi_X(q)=\frac{512[(q-19/16)^2+1/4]}{(q+1)(q+2)(q+3)}
\tag{20.6b}
$$

which annihilates the synthetic off-line point $s=1/4+i$. This point is
not asserted to be a zeta zero. A single multinode test can therefore hide
an off-line orbit. The RH equivalence requires a separating family; a
nonzero one-node carrier has no such accidental zero. A successful
source construction must create the identification

$$
\boxed{s\mapsto1-s\quad\text{with}\quad s\mapsto\bar s}
\tag{20.7}
$$

without assuming RH.

![The reflection contour, principal-value center, and jump law. The plotted jump profile is schematic; the identity is exact.](figures/figure76_reflection_contour_and_jump_law.png)

## R21. The one-node strict defect

For the one-node carrier $u_x(q)=q/(x+q)^2$ of (11.1), define the Hermitian
comparison

$$
\mathscr H_x
=\frac12\sum_{\rho\ \mathrm{all}}m_\rho
|\mathcal F_x(\rho)|^2
\tag{21.1}
$$

Pairing every zero with its reflected-conjugate partner gives the exact
global square

$$
\boxed{
\mathscr H_x-W_1(x)
=\frac14\sum_{\rho\ \mathrm{all}}m_\rho
\left|\mathcal F_x(\rho)
-\overline{\mathcal F_x(1-\rho)}\right|^2\ge0}
\tag{21.2}
$$

For this carrier the defect is individually strict for every off-line
quartet, so equality is equivalent to RH. For a general multinode test,
accidental agreement is possible (§R20).

The same one-node carrier produces a positive measure on zero abscissae. Put

$$
w_x(s)=\frac{q(s)}{[x+q(s)]^2}
\tag{21.3}
$$

and group conjugate ordinates at each real part:

$$
d\nu_x(\sigma)=
\sum_\beta\left(
\sum_{\Re\rho=\beta}m_\rho w_x(\rho)
\right)\delta_\beta(d\sigma)
\tag{21.4}
$$

Then

$$
d\nu_x\ge0,\qquad
\nu_x(\mathbb R)=2W_1(x)
\tag{21.5}
$$

The positivity is termwise after conjugate pairing. If $q=a+ib$, $a>0$,

$$
2\Re\frac{q}{(x+q)^2}
=\frac{2[a(x+a)^2+(a+2x)b^2]}{[(x+a)^2+b^2]^2}>0
\tag{21.5a}
$$

The weights are absolutely summable: they are $O(\gamma^{-2})$ at large
height and the zero-counting function is $O(T\log T)$. Thus grouping
conjugate ordinates does not depend on a conditional ordering.

The topology must be stated with its closure:

$$
\boxed{
\operatorname{Atoms}(\nu_x)=\{\Re\rho\}
\qquad
\operatorname{supp}\nu_x=
\overline{\{\Re\rho:\xi(\rho)=0\}}}
\tag{21.6}
$$

Reflection centers this measure at $1/2$. Its unnormalized centered second
moment is

$$
\boxed{
M_{2,x}:=\int\left(\sigma-\frac12\right)^2d\nu_x(\sigma)\ge0
\qquad
M_{2,x}=0\iff\mathrm{RH}}
\tag{21.7}
$$

The probability measure $\nu_x/[2W_1(x)]$ has variance
$M_{2,x}/[2W_1(x)]$. Nonnegativity is automatic on the zero side; forcing
this moment to vanish from the source is the hard direction.

Exact regularized Riesz/Green representations are available. With

$$
U=\log|\xi|
\qquad
d_x(s)=\left|\mathcal F_x(s)
-\overline{\mathcal F_x(1-s)}\right|^2
\tag{21.8}
$$

one has, as improper distributional pairings over admissibly truncated
strips,

$$
\boxed{
\mathscr H_x=\frac1{4\pi}
\left\langle\Delta U,|\mathcal F_x|^2\right\rangle
\qquad
\mathscr H_x-W_1(x)=\frac1{8\pi}
\left\langle\Delta U,d_x\right\rangle}
\tag{21.9}
$$

Also, for

$$
h_x^{\perp}(s)=
\left(\Re s-\frac12\right)^2
\Re\!\left(\frac{s(1-s)}{[x+s(1-s)]^2}\right)
\tag{21.10}
$$

$$
\boxed{M_{2,x}=\frac1{2\pi}
\left\langle\Delta U,h_x^{\perp}\right\rangle}
\tag{21.11}
$$

These are source representations; they do not provide the missing reverse
sign. No one-variable meromorphic function can equal
$|\mathcal F_x(s)|^2$ on an open set, since
$\partial_{\bar s}|\mathcal F_x|^2$ is generically nonzero. The surviving
source representation must therefore remain two-variable, nonlocal, distributional,
or discrete.

For the one-dimensional source contour, begin with the meromorphic weight
$w_x$ in (21.3) and define, on zero-free vertical lines,

$$
I_x(\sigma)=\frac1{2\pi}\lim_{T_j\to\infty}
\int_{-T_j}^{T_j}w_x(\sigma+it)\Phi(\sigma+it)\,dt
\tag{21.12a}
$$

The heights $T_j$ avoid zero ordinates and make the horizontal contour
remainders vanish. On lines through zeros, symmetric indentation and
midpoint boundary values specify the principal-value representative.
The residue theorem then identifies that source contour with

$$
I_x(\sigma)=-W_1(x)+\nu_x((0,\sigma))
+\frac12\nu_x(\{\sigma\})
\tag{21.12}
$$

Then

$$
\boxed{
M_{2,x}=\frac{W_1(x)}2
-4\int_{1/2}^{1}\left(\sigma-\frac12\right)I_x(\sigma)\,d\sigma}
\tag{21.13}
$$

The first unsupported reverse forcing line is

$$
\boxed{
\int_{1/2}^{1}\left(\sigma-\frac12\right)I_x(\sigma)\,d\sigma
\ge\frac{W_1(x)}8}
\tag{21.14}
$$

The positive zero measure gives the opposite inequality. An independent
source proof of (21.14) would force equality and RH.

![The two reflection sheets, the strict one-node defect, and the bilinear versus Hermitian pairings.](figures/figure82_v26_carrier_and_defect.png)

## R21A. Strict defects and the Green boundary

The one-node reflection defect factors exactly:

$$
d_x(s)=|f(s)-\overline{g(s)}|^2
=(1-2\sigma)^2\frac{|x+(1-s)\bar s|^2}{|x+q(s)|^4}\ge0,
\tag{GM.1}
$$

and vanishes precisely on $\sigma=1/2$.  Its Laplacian is strictly positive
away from carrier poles.  Therefore the Green identity for
$U=\log|\xi|$ necessarily contains both bulk and boundary terms; adding a
constant to $U$ transfers mass between them while leaving the zero sum
unchanged.  A bulk sign alone cannot force the defect to vanish.

The heat-resolvent version is even shorter.  For $q=A+ib$,

$$
r_x=\frac1{x+A}-\Re\frac1{x+q}
=\frac{b^2}{(x+A)|x+q|^2}\ge0.
\tag{GM.3a}
$$

The same transverse coordinate controls the higher moment sequence.  If
$M_{2m,x}$ is the $2m$th centered abscissa moment, then
$[M_{2m,x}/(2W_1(x))]^{1/(2m)}$ tends to the support radius
$\sup_\rho|\Re\rho-1/2|$.  This is an exact support diagnostic, not a
source-side upper bound.

## R21B. Heat, transverse distance, and source-energy growth

For a nontrivial zero $\rho=\beta+i\gamma$ write
$q=A+ib$.  Then

$$
b=\gamma(1-2\beta),\qquad b^2=4\gamma^2(\beta-1/2)^2.
\tag{HG.1}
$$

The off-line heat defect
$\mathcal E_H(h)=\sum m_\rho b_\rho^2e^{-hA_\rho}$ vanishes for one (hence
every) $h>0$ exactly under RH.  At fixed source scale $a>0$, the Bernstein
row sees the same transverse quantity through

$$
\boxed{R_q(a)^2-1
=\frac{2ab^2}{(|q|+A)|a+q|^2}
=\frac{2a(a+A)}{|q|+A}\,d_a(q).}
\tag{HG.4}
$$

Thus the heat defect, the row-growth factor and the distance from the critical
line are three readings of the same $b^2$.  Theorem 164.2 converts that
geometry into the ordinary energy-growth limit.  None of these exact detectors
supplies the remaining source estimate; they identify what an off-line zero
would force if it existed.

# Part VII. Results and the research boundary

Section R22 records results with their quantifiers; R23 states the first
unsupported source inequality; R24 maps the reading routes. Comparison
positivity and finite certificates remain distinct from the all-order
completed-source assertion.

## R22. Results and their quantifiers

| mathematical layer | established result | status, and what is still required |
|---|---|---|
| Triangular arithmetic | primitive, factorial, reciprocal, cyclic and Pell identities | \PROVED{} Reader §§R1–R5E and the Dossier arithmetic chapters. \EVID{} empirical spacing comparisons remain separate (§168). |
| Euler's constant on the triangular coordinate | the mirror parity of Ramanujan's expansion; $\sum_{k\ge2}\zeta(k)/T_k=\log2\pi-\gamma_{\mathrm E}$ and its four readings; the simplex ladder; the pairing (GA.8) with $\lambda_1$ | \PROVED{} §R4A and Dossier §96A; classical in substance [95--109]. It carries no sign information about the zeros. |
| Completion and exact criteria | heat, Stieltjes, Widder, Hausdorff, Li and Loewner criteria; scalar curvature and admissible progressions | \EQUIV{} Each retains its stated full quantifier; Sections 155D--155E and 166F--166G add growth targets, not their source bounds. |
| Source rungs | $W_1$–$W_6>0$ globally from the source | \PROVED{} analytic $W_1$; \CERT{} A-CAT $W_2$–$W_6$, one bundled certificate on two independent arithmetic backends (§R12, Dossier §74A). \OPENSTAT{} the independent $W_7\rightsquigarrow F^{(14)}$ proof. |
| Verified-height rectangle | $F_{n,k}>0$ for all $x>0$, $n\le K_H-1$, $k\le K_H$ | \CERT{} $K_H=4{,}712{,}664{,}392{,}502$; includes $W_5,W_6>0$ with zero-assisted input (§R13). |
| Finite matrices | global order eight; rank twelve at $x=56$ | \CERT{} with different quantifiers. \OPENSTAT{} global order nine and the all-node sign (§§92–93, 138). |
| Positive comparison and reserve growth | triangular sine projection, compensated Catalan reserve, exact linear/exponential defect alternatives | \PROVED{} Sections 12A--12B, 61A, 95A, 155C--155D. \OPENSTAT{} the one-sided arithmetic upper bound. |
| Reflection and heat defects | exact nonnegative detectors; vanishing is RH-equivalent | \EQUIV{} \OPENSTAT{} contour and Green representations exist; the reverse forcing signs do not (§§R20–R21B). |
| Completed and prime energy | exact rows, Pascal/Laguerre norm, boundedness equivalence and prime plateau | \PROVED{} signed Gamma measure. \EQUIV{} \OPENSTAT{} the full-prime all-degree cap (BE.5), §§163–166B. |
| Prime cutoffs and boundary reconstruction | whole rows at $20^{N+1}$ and $13^{N+1}$; shifted block at $5^{2d-1}$; actual boundary from degree $15d-1$ and cutoff $8^{15d}$ | \PROVED{} Sections 166C--166G. \OPENSTAT{} the uniform or polynomial source bounds; convergence alone supplies no sign. |
| Exact-divisor residual | Mellin/Hardy/Laguerre/sine norm, plateau/canonical exponents, scalar transfer and structured sampling | \PROVED{} Sections 155H--155J. The fixed taper and canonical family have exponent $2\Theta_\zeta-1$; fourth powers and $T_k^2$ suffice for the scalar criterion. \OPENSTAT{} the subpower mixed-sum bound or the required scalar upper decay. |
| Radius deficit | exact single-orbit remainder, two-sided chain, and the separation of $\Delta$ from its high-scale limsup | \PROVED{} §§R13A, 48A. \OPENSTAT{} $\Delta<1$, equivalently a uniform zero-free boundary strip. |
| NO-GO ledger | scalar-Fourier, Gamma-sublattice, tensor-lift, large-sieve, cutoff-envelope and finite-prefix shortcuts | \PROVED{} unconditional limitations collected once in §R25; proofs remain at their Dossier homes. |

One entry in the second row now has a machine-checkable statement of record:
the Li criterion has been formalized in Lean against the ambient library's own
Riemann-hypothesis predicate, stated without hypothesis binders and reporting
only the three standard axioms [71]. It is recorded here as read and not
built: the project was not compiled in the course of this work, so this is a
report of someone else's certificate and not a certificate of this volume. It
formalizes the equivalence, and it asserts nothing about the sign of the
coefficients.

A finite certificate proves its stated finite region. None replaces the
all-order quantifier in an RH criterion. The table separates an open
statement from an open independent proof of an already established sign.

## R23. The first unsupported lines, by route

There is no proved reduction of all surviving routes to one source inequality.
The matrix route begins with:

```{=latex}
\begin{tnopen}{equivalent to RH; not proved here or anywhere in the Dossier}
```
$$
\boxed{\begin{gathered}
\text{No source-side argument presently proves}\\
L_\Gamma-L_P\succeq0\\
\text{for every finite positive node set}
\end{gathered}}
\tag{23.1}
$$
```{=latex}
\end{tnopen}
```

Equivalently, no source-side argument proves

$$
\sum_{[\rho]}m_\rho\mathscr L_F(\rho)\ge0
\tag{23.2}
$$

for every rational-resolvent test. The surviving design target is a positive
two-sheet form before compression that preserves reflection information, whose final
compression recovers the reflection contour and the translation covariance
of the Weil functional.

**A distinct compact-window problem.** Zhu [72] reports half-width $0.8$;
Liu [81] reports $1$ and $17/16$ plus a localization NO-GO beyond $\log8/2$.
Liu's manuscript is submitted, not peer-reviewed or on arXiv, and not yet
externally reproduced. These are comparison results only: the rung transforms
here are noncompact, so the fixed-window bounds do not transfer as stated.

At one node the same boundary is (21.14), or equivalently the missing
independent upper sign in the Green identity for $d_x$. The source-rung
prefix now reaches $W_6$ independently. The first scalar rung not yet proved
directly from the Gamma--prime source is
$W_7=-x^{-12}(x^{13}W_6')'>0$, whose source expression reaches $F^{(14)}$. These are
different compressions of the frontier; no finite source prefix replaces the
all-order condition.

For a positive trace-class model $D$, the corresponding concrete target is

$$
\boxed{\det(I+xD)=\frac{\xi(s_x)}{\xi(1)}\quad(x\ge0)}
\tag{23.3}
$$

Differentiation would identify its resolvent with $S_\xi$ and yield the
positive Gram form in §R10A. The continued zeta identities and the
triangular--Volterra benchmark constrain this target; they do not establish
it. The ordinary strongly convergent tensor lift is ruled out in §161 and
listed with the other finished limitations in §R25; singular-form and
source-defined discrete realizations remain candidates.

Section R17F now supplies a specific source-defined discrete sequence. Its
next source target is (BR.4): for one fixed $a>0$, bound the
completed row variation by $C_{a,\varepsilon}(1+\varepsilon)^N$ for
every $\varepsilon>0$ and every $N$. By the growth criterion of §164, quoted above, that bound at one prescribed
$a>0$ is not merely sufficient for RH but equivalent to it. Equivalently one may
bound the exact Laguerre energy in (BE.3). Lemma 166A.1 supplies the
elementary/Gamma growth estimate. The signed measure in §166B further
reduces the question to the explicit bounded full-prime criterion (BE.5).
That all-degree source inequality remains open. The heat identity
(HG.4) shows that the excess growth detects the same squared imaginary
folded coordinate as the off-line heat defect. This gives a common coordinate
for two distinct source obligations.

**A proposed transfer, not an identified theorem.** The growth exponent of
Theorem 164.1 invites comparison with the regular-arithmetic-function
framework [67--69] and its Tauberian/Volterra methods [73]. The differential
rung recurrence $W_{k+1}=-j_kW_k'-xW_k''$ does not by itself verify the
hypotheses of a rank-by-rank arithmetic transfer theorem. Applicability to
(BR.4) is open. It is not claimed
here in either direction; these external statements were read, not verified.

**Two concrete source targets.** The curvature already defined in Section
155B is $I_n=\int_0^\infty e^{-u}M(u)L_{n+1}^{(0)}(u)du$, with
$M(u)=\Psi(e^u)-e^u+1$. Section 155E proves that a one-sided polynomial
upper bound on either parity separately would suffice. Its progression
argument uses an explicit pole-angle condition to prevent cancellation;
it does not license arbitrary sparse scalar sampling. Independently,
Section 166F defines the cutoff defect at fixed scale $a=2$ and proves
its growing-block error tends to zero. The remaining alternatives are

$$
\boxed{\begin{aligned}
I_{2m}&\le C(m+1)^A\quad(m\text{ sufficiently large}),\\
\text{or}\qquad \widehat\beta_{2,d}^+&\le C'(1+d)^{A'}\quad(d\ge1).
\end{aligned}}
\tag{23.4}
$$

Each alternative requires fixed finite constants; each would imply RH.
Neither is established. The odd-curvature alternative uses $I_{2m+1}$.
Section 166G now gives a separate controlled boundary reconstruction;
a polynomial upper bound on $\widehat\beta_d^{\partial,+}$ would also
suffice. Section R17I gives a fixed exact-divisor alternative: for the linear taper
$V_N$, RH is equivalent to $U_N=O_\epsilon(N^\epsilon)$ for every
$\epsilon>0$ (even on one fixed unbounded index set). Equivalently one may
attack the signed mixed sum $\mathcal X_N$. For the scalar $B_{\log}$ route,
Section 155J proves that the eventual-integer premise may be replaced by all
sufficiently large fourth powers, or by the squared triangular mesh $T_k^2$,
with the stated endpoint decay. Neither required arithmetic estimate is
proved.
The original full-row cap (BE.5), the bounded cutoff norms in
(166D.2)/(166D.4), and the one-sided reserve growth theorem remain valid
routes to the same obligation. The compensation, complete prime-error
kernel and its regularization stay present throughout. A smaller cutoff,
a positive comparison model, or a finite sign list does not supply the
missing uniform source estimate.

## R24. Proof map and reading routes

The Dossier chapters follow mathematical dependencies: triangular
arithmetic and geometry, completion, flux and source rungs, moment and
matrix criteria, arithmetic cancellation, and the completed discrete energy.
Reader sections carry an **R** prefix and Dossier sections keep their
existing identifiers, so section numbers need not increase at every chapter
boundary; the convention is stated in full in the notation table of the study
spine.

| question | reader entry | full proof or comparison |
|---|---|---|
| What does the triangular primitive generate? | §§R1–R1A, R3–R5E | Dossier §§5–14, 76–78, 94–98 (including 95A and 96A), 156, 162, 167–168 |
| How does Euler's constant enter? | §R4A, (9.8) | §96A; compare §§155G–155I |
| How do reflection and the complex fold connect? | §§R6–R10 | §§12A, 16–18, 20–31, 61A, 152–153 |
| Which scalar signs are proved from the source? | §§R11–R13 | §§32–38, 74–75, 55; §49 supplies the general negative-rung converse |
| Why do moments become matrices? | §§R14–R16 | §§48–54, 104, 136, 145; finite gates in §§85–93 and 138 |
| Which positive Gamma models match the source? | §§R17–R17E | §§131–133; compare the source split in §54 and the reserve/defect in §155C |
| What remains in prime oscillation? | §R13 and the source split | §§56–61, 105–113, 118, 129; each route states its own limit and uniformity |
| What do finite Weil models establish? | §§R10A, R18–R18B | §§19, 44, 123–125; cutoff, band and prime limits remain separate |
| Where does conjugation enter? | §§R18–R21B | §§103, 137, 148–149, 154, 157–161 |
| What is the fixed-scale source-energy task? | §§R17F–R17H, R21B | §§163–166E; the all-degree full-prime cap (166B.11) is open |
| What degree growth would force the source sign? | Sections R15, R23 | Sections 155D--155E: reserve growth, curvature and progression proofs |
| Which cutoff approximates its own matrix target? | Sections R17H, R23 | Sections 166D--166G: whole row, shifted block, and actual boundary reconstruction |
![The proof map for this volume. Each criterion retains its full quantifiers. The source identities are exact; the surviving all-order source bounds are listed by route in §R23.](figures/v30_rh_equivalence_map.png)

For the new boundary reconstruction, read R17H with Dossier Section 166G.
For exact-divisor cancellation and its denominator residual, read R17I
with Sections 155H--155J; Sections 155F--155G explain the countermodels
that motivate this use of actual arithmetic.

The map uses the same completed object $S_\xi$, with $h=xS_\xi$.
Auxiliary Gamma and triangular models retain their own measures.
Reproducibility details and the section review are in the source package.


# Part VIII. What this approach cannot do

The proofs stay at their original Dossier locations; this Part is the single
NO-GO ledger. Each row names the shortcut killed and the corridor left open.

## R25. No-go ledger and the surviving corridor

| exact limitation | what it kills | what survives |
|---|---|---|
| Theorem 22A.1: every scalar rung test has at least $k$ Fourier sign changes and is not positive definite | scalar Fourier positivity as a rung proof | completed/two-variable Weil forms and the arithmetic source |
| §48C: centered Gamma-pole terms have a universal rank-two negative direction, and neither pole-index sublattice absorbs the prime channel with a finite baseline | “unused Gamma poles” as a positive Löwner reserve | the repaired reserve and the full signed prime-error estimate |
| §49 and §69: a fixed positive rung/Li/Hankel prefix can coexist with later failure | any finite certificate as an infinite stopping rule | the full quantifiers in §§R12, R14, R23 |
| §161: ordinary strongly convergent tensor/vector-multiplier realizations cannot represent the completed meromorphic Stieltjes target | the regular translation-energy tensor lift | singular-form, atomic/discrete, or different source-norm representations |
| Theorems 107.1 and 112.1: the loose diagonal is exponent-self-limiting, and the classical blockwise large sieve misses the short-shift target by at least $X^{1/2+o(1)}$ | those two coarse analytic closures | the exact-diagonal/interior-saddle route or a stronger arithmetic mechanism |
| §§155F–155G and (H07): PNT-quality envelopes, positive prime-power support, sparse support counts, long prefixes and meromorphic Euler products do not force the needed curvature/source sign | replacing the actual signed arithmetic remainder by support or envelope domination | exact divisor arithmetic and the weighted completed prime error |
| §69C, proved in v0.3: a conjugation-symmetric linear zero functional erases the orientation bit, and compact Euler-ray data cannot continuously recover the zero defect | first-order detection by symmetric real-axis tests; extraction from finite-order ray data | half-plane projections and one-sided routes such as §R17I; identities using zeta's complete prime and Gamma data |
| §§69A–69B: a Dirichlet series with the reflection of $\xi$ (different Gamma factor) and no Euler product fails some rung (computed: first at $W_{16589}$), and (TW.1) | functional-equation-only proofs of all rungs; a finite rung prefix read as progress | arguments using the Euler product together with the functional equation |

These are unconditional theorems about what this approach cannot do. They are
finished and explain the surviving corridor; none is evidence for RH or against
it.

# Summary: the object, the results, and the remaining line

The starting object is the triangular primitive, not a conjectured zero
pattern. Its half-step symmetry continues to the exact fold
$q=s(1-s)=-2T_{s-1}$. The completed function factors as $\xi(s)=X(q)$,
and one reflection orbit $[\rho]=\{\rho,1-\rho\}$ gives one folded node
$q_\rho$, one resolvent pole $-q_\rho$, and one reciprocal seed
$y_\rho=1/q_\rho$. An off-line quartet remains two conjugate folded nodes,
each carrying its original multiplicity. The branch label is folded away;
critical-line membership is not.

From these nodes the volume constructs the absolutely convergent resolvent
$S_\xi$, the Widder rungs, the moment and Li dictionaries, the source
matrices, and the completed energies. The signed Pascal identity is exact
at every rung. Its existence does not decide the sign of every rung.
The proved source prefix reaches $W_6$ on the inherited v5.0 certificates;
the verified-height channel reaches a much longer but still finite range.
Those are different proof channels with different inputs. The next
independent source proof is $W_7\rightsquigarrow F^{(14)}$.

The full statement remains the one printed near the beginning:
$\mathrm{RH}\iff W_k(x)\ge0$ for every $k\ge1$ and every $x>0$.
The all-node Gamma-minus-prime matrix inequality is a second equivalent
form. Sections R17F--R17I and R23 give additional exact energy and divisor
routes with their own unproved uniform bounds; no unproved reduction among
those routes is used. A positive comparison model, a real-part scalar, or
a finite certificate cannot supply a missing full quantifier.

Version 5.2 preserves that research boundary and measures one side of it.
A twin with the reflection of $\xi$, a different Gamma factor and no Euler
product passes thousands of computed rungs, and a hundred Löwner nodes at the
tested centres, before failing. What must be
proved therefore has to use the Euler product and the functional equation
together. The arithmetic identities and finite certificates stand on their
stated domains. The uniform completed-source positivity required by RH
remains open.

# References

\begingroup
\small

1. E. Bombieri, *The Riemann Hypothesis - official problem description*, Clay
   Mathematics Institute, Millennium Prize Problems,
   [Clay problem description](https://www.claymath.org/millennium/riemann-hypothesis/).
2. NIST Digital Library of Mathematical Functions, Sections 5.5, 5.7--5.9, 5.11,
   24.4, 25.4, 25.10, 25.11, and 25.16; in particular
   [Hurwitz special values and derivatives](https://dlmf.nist.gov/25.11),
   [zero counting](https://dlmf.nist.gov/25.10), and
   [Gamma and digamma asymptotics](https://dlmf.nist.gov/5.11).
3. E. C. Titchmarsh, revised by D. R. Heath-Brown, *The Theory of the Riemann
   Zeta-Function*, 2nd ed., Oxford University Press, 1986.
4. X.-J. Li, "The positivity of a sequence of numbers and the Riemann
   hypothesis," *Journal of Number Theory* 65 (1997), no. 2, 325--333,
   [DOI 10.1006/jnth.1997.2137](https://doi.org/10.1006/jnth.1997.2137).
5. E. Bombieri and J. C. Lagarias, "Complements to Li's criterion for the
   Riemann hypothesis," *Journal of Number Theory* 77 (1999), no. 2, 274--287,
   [DOI 10.1006/jnth.1999.2392](https://doi.org/10.1006/jnth.1999.2392).
6. L. de Branges, *Hilbert Spaces of Entire Functions*, Prentice-Hall, 1968.
7. G. Csordas, T. S. Norfolk, and R. S. Varga, "The Riemann hypothesis and the
   Turan inequalities," *Transactions of the American Mathematical Society*
   296 (1986), 521-541.
8. J. Huckstead, *Divisor-Band Bijections and Totient Shells in the
   Triangular-Fractional Grid*, version 5, Zenodo (2026),
   DOI 10.5281/zenodo.21440877.
9. J. Huckstead, *Triangular Addressing, Null Coordinates, and
   Reciprocal-Metallic Locks in a Scale-Covariant Plane Geometry*, Working
   Draft III, Zenodo (2026), DOI 10.5281/zenodo.21444929.
10. J. Huckstead, *From Measure to Flux: Energy-Conjugate Bookkeeping and Exact
    Semidiscrete Scattering in Finite Radial Wave Models*, publication layer
    v0.6.13, Zenodo (2026), DOI 10.5281/zenodo.21444339.
11. J. Huckstead, *Two-Term Asymptotics for the Total Variation of
    Exponentially Weighted Laguerre Polynomials*, v0.1, Zenodo (2026),
    DOI 10.5281/zenodo.21861619.
12. J. Sondow and C. Dumitrescu, "A monotonicity property of Riemann's
    xi function and a reformulation of the Riemann hypothesis,"
    *Periodica Mathematica Hungarica* 60 (2010), 37-40,
    DOI 10.1007/s10998-010-1037-3; arXiv:1005.1104.
13. Y. Matiyasevich, F. Saidak, and P. Zvengrowski, "Horizontal monotonicity
    of the modulus of the Riemann zeta function and related functions,"
    arXiv:1205.2773 (2012).
14. J. C. Lagarias, "On a positivity property of the Riemann xi-function,"
    *Acta Arithmetica* 89 (1999), 217-234.
15. A. D. Sokal, "Real-variables characterization of generalized Stieltjes
    functions," *Expositiones Mathematicae* 28 (2010), 179-185;
    arXiv:0902.0065.
16. D. V. Widder, "The Stieltjes transform," *Transactions of the American
    Mathematical Society* 43 (1938), 7-60.
17. F. Johansson, "Rigorous high-precision computation of the Hurwitz zeta
    function and its derivatives," arXiv:1309.2877 (2013).
18. GNU MPFR Project, *GNU MPFR 4.2.2 Manual*,
    https://www.mpfr.org/mpfr-current/mpfr.html.
19. F. Hausdorff, "Summationsmethoden und Momentfolgen. I,"
    *Mathematische Zeitschrift* 9 (1921), 74-109,
    DOI 10.1007/BF01378337.
20. F. Hausdorff, "Summationsmethoden und Momentfolgen. II,"
    *Mathematische Zeitschrift* 9 (1921), 280-299,
    DOI 10.1007/BF01279032.
21. A. Pringsheim, "Ueber Functionen, welche in gewissen Punkten endliche
    Differentialquotienten jeder endlichen Ordnung, aber keine Taylor'sche
    Reihenentwickelung besitzen," *Mathematische Annalen* 44 (1894), 41-56,
    EuDML 157700.
22. K. Löwner, "Über monotone Matrixfunktionen," *Mathematische Zeitschrift*
    38 (1934), 177-216, DOI 10.1007/BF01170633.
23. R. L. Schilling, R. Song, and Z. Vondraček, *Bernstein Functions:
    Theory and Applications*, 2nd ed., De Gruyter, 2012,
    DOI 10.1515/9783110269338.
24. M. Riesz, "Sur l'hypothèse de Riemann," *Acta Mathematica* 40 (1916),
    185-190, DOI 10.1007/BF02418544.
25. L. Báez-Duarte, "A sequential Riesz-like criterion for the Riemann
    hypothesis," *International Journal of Mathematics and Mathematical
    Sciences* 2005, 3527-3537, DOI 10.1155/IJMMS.2005.3527.
26. A. Agarwal, M. Garg, and B. Maji, "Riesz-type criteria for the Riemann
    hypothesis," *Proceedings of the American Mathematical Society* 150
    (2022), DOI 10.1090/proc/16064.
27. H. L. Montgomery and R. C. Vaughan, "Hilbert's inequality,"
    *Journal of the London Mathematical Society* (2) 8 (1974), 73--82.
28. H. L. Montgomery, *Ten Lectures on the Interface Between Analytic Number
    Theory and Harmonic Analysis*, CBMS Regional Conference Series in
    Mathematics 84, American Mathematical Society, 1994.
29. H. Iwaniec and E. Kowalski, *Analytic Number Theory*, American
    Mathematical Society Colloquium Publications 53, 2004.
30. J. B. Conrey and A. Gamburd, "Pseudomoments of the Riemann zeta-function
    and pseudomagic squares," arXiv:math/0307213v2; *Journal of Number
    Theory* 117 (2006).
31. M. Wahl, "On the mod-Gaussian convergence of a sum over primes,"
    arXiv:1201.5295v3 (2013), especially equation (1.4).
32. M. Gerspach and Y. Lamzouri, "Low pseudomoments of Euler products,"
    arXiv:2103.03870 (2021).
33. A. Connes, "The Riemann Hypothesis: Past, Present and a Letter Through
    Time," arXiv:2602.04022v1 (2026).
34. D. S. P. Salazar, "Order-Moment Transport and Hankel Determinants in
    Special-Function Inequalities," arXiv:2606.31647v2 (2026).
35. M. Bhowmik, A. Chatterjee, and M. Putinar, "Holomorphic Interpolation of
    Multivariate Completely Monotone Functions," arXiv:2606.12102 (2026).
36. L. Guth and J. Maynard, "New large value estimates for Dirichlet
    polynomials," *Annals of Mathematics* 203 (2026), no. 2, 623--675,
    DOI 10.4007/annals.2026.203.2.6; arXiv:2405.20552v2.
37. B. Chen, V. Gupta, and Y. C. Li, "Large Value Estimates for Dirichlet
    Polynomials with Characters and Zero Density of Dirichlet $L$-Functions,"
    arXiv:2507.08296v2 (2026).
38. A. Bondarenko, O. F. Brevig, E. Saksman, K. Seip, and J. Zhao,
    "Pseudomoments of the Riemann zeta function," *Bulletin of the London
    Mathematical Society* 50 (2018), no. 4, 709--724,
    DOI 10.1112/blms.12183; arXiv:1701.06842v3.
39. E. Lill, "Résolution graphique des équations numériques de tous les
    degrés à une seule inconnue, et description d'un instrument inventé dans
    ce but," *Nouvelles Annales de Mathématiques*, 2e série, 6 (1867),
    359--362.
40. E. Lill, "Résolution graphique des équations algébriques qui ont des
    racines imaginaires," *Nouvelles Annales de Mathématiques*, 2e série,
    7 (1868), 363--367.
41. B. Bellotti and P.-J. Wong, "Improved estimates for the argument and
    zero-counting function of the Riemann zeta-function," arXiv:2412.15470v2
    (2025), accepted by *Mathematics of Computation*.
42. D. J. Platt and T. S. Trudgian, "The Riemann hypothesis is true up to
    $3\cdot10^{12}$," *Bulletin of the London Mathematical Society* 53
    (2021), 792--797; arXiv:2004.09765.
43. O. Dobsch, "Matrixfunktionen beschränkter Schwankung,"
    *Mathematische Zeitschrift* 43 (1938), 353--388.
44. W. F. Donoghue, Jr., *Monotone Matrix Functions and Analytic
    Continuation*, Grundlehren der mathematischen Wissenschaften 207,
    Springer, 1974.
45. Euclid, *The Thirteen Books of The Elements*, translated with
    introduction and commentary by T. L. Heath, 2nd ed., Dover, 1956,
    Book VII, Definition 22, and Book IX, Proposition 36.
46. L. E. Dickson, *History of the Theory of Numbers*, Volume I: Divisibility
    and Primality, Carnegie Institution of Washington, 1919, Chapter I.
47. A. Groskin, "A finite Guinand--Weil dictionary and archimedean tail order
    for the truncated Weil quadratic form," arXiv:2607.02828v3 (2026),
    archival DOI 10.5281/zenodo.21124802.
48. A. Connes, C. Consani, and H. Moscovici, "Zeta Spectral Triples,"
    arXiv:2511.22755v1 (2025), forthcoming in the EMS Lecture Notes in
    Mathematics volume *Applications of Noncommutative Geometry to Gauge
    Theories, Field Theories, and Quantum Space-Time*.
49. A. Connes and W. D. van Suijlekom, "Quadratic Forms, Real Zeros and
    Echoes of the Spectral Action," arXiv:2511.23257v1 (2025).
50. A. Connes, C. Consani, and H. Moscovici, "Zeta zeros and prolate wave
    operators," arXiv:2310.18423v2 (2024).
51. M. Suzuki, "Weil's quadratic form via the screw function,"
    arXiv:2606.09096v2 (2026).
52. A. Groskin, "High-Precision Approximation of Riemann Zeros via the
    Truncated Weil Form," arXiv:2605.20224v4 (2026), archival DOI
    10.5281/zenodo.19546514.
53. E. W. Weisstein, "Gamma Function," *MathWorld--A Wolfram Web Resource*,
    [MathWorld entry](https://mathworld.wolfram.com/GammaFunction.html),
    page captured 27 August 2026.
54. *Hermitian Spaces*, Chapter 12 lecture slides, CIS 5150, University of
    Pennsylvania, Sections 12.1--12.2, especially the definitions of
    sesquilinear/Hermitian forms and the complex polarization identities,
    https://www.cis.upenn.edu/~cis5150/cis515-20-sl9.pdf.

55. J. Huckstead, *The Polar Shell Renderer: A Lens, Not a Law*,
    revised 9 July 2026, Zenodo, DOI 10.5281/zenodo.21280464.

56. A. Voros, "Zeta functions for the Riemann zeros," *Annales de
    l'Institut Fourier* 53 (2003), no. 3, 665--699; first preprint 2001,
    [arXiv:math/0104051v4](https://arxiv.org/abs/math/0104051v4).
    Equations (40)--(41), (59), (74), (81), and (91)--(95), and Table 1
    supply the classical spectral-zeta formulas used here.
57. A. Voros, "Erratum - Zeta functions for the Riemann zeros,"
    *Annales de l'Institut Fourier* 54 (2004), no. 4, 1139,
    [DOI 10.5802/aif.2046](https://aif.centre-mersenne.org/articles/10.5802/aif.2046/).
58. J. B. Keiper, "Power series expansions of Riemann's $\xi$ function,"
    *Mathematics of Computation* 58 (1992), no. 198, 765--773,
    [DOI 10.2307/2153215](https://doi.org/10.2307/2153215).

59. NIST, *Digital Library of Mathematical Functions*, §§5.4--5.5,
    Gamma special values, recurrence, reflection, and duplication.
    [Official formulas](https://dlmf.nist.gov/5.5).
60. S. M. Eisenberg, “Moment Sequences and the Bernstein Polynomials,”
    *Canadian Mathematical Bulletin* 12 (1969), no. 4, 401--411.
    [DOI 10.4153/CMB-1969-050-8](https://doi.org/10.4153/CMB-1969-050-8).
    Classical background; the source-specific growth argument is printed
    independently in §164, without a claim of literature novelty.
61. *A Search-Adjusted Audit of Row-Sector Modulus Signals in Terminal
    Zeta-Zero Spacing Residuals*, unpublished historical report (2026),
    10 pages. Only its reported tables are used; its raw arrays and
    permutation replay are not part of this work.
62. *A Finite-Count Search for Localized Enrichment Near 2.75 in Unfolded
    Riemann Zeta-Zero Gap Coordinates*, unpublished historical report,
    May 2026, 24 pages. Its reported counts and stated design are compared in
    §168.
63. NIST, *Digital Library of Mathematical Functions*, sine
    [Maclaurin series](https://dlmf.nist.gov/4.19.E1) and
    [Euler infinite product](https://dlmf.nist.gov/4.22.E1), and the
    [fourth-kind Chebyshev representation](https://dlmf.nist.gov/18.5.E4).
    The triangular factorization in (PR.6) is a direct regrouping of
    the factorial coefficients; Gamma reflection is covered by [59].

64. L. Euler, *De formulis exponentialibus replicatis*, E489 (1778),
    [original paper in the Euler Archive](https://scholarlycommons.pacific.edu/euler-works/489/).
    The fixed-point differentiation and stability calculation used here
    are displayed in §R5E.

65. A. Edelman and G. Strang, *Pascal Matrices*,
    [MIT course essay](https://web.mit.edu/18.06/www/Essays/pascal-work.pdf).
    Classical symmetric Pascal matrix, Vandermonde factorization, and
    determinant one. Section 163A identifies this matrix inside the
    completed-source energy.

66. Y. Lamzouri, *A new proof that more than 2/3 of the zeros of the
    Riemann zeta function are simple and on the critical line*,
    [arXiv:2609.02882v2](https://arxiv.org/abs/2609.02882), 17 pages.
    Proposition 2.1, Lemma 3.1 and Theorem 1.1 are the statements compared in
    §159. Its notation is local to that paper; in particular its
    critical-line counting symbol is not the smooth approximation $N_0$
    of §168.

Entries 67--73 are external work consulted while the v5.0 edition was
prepared. Each was read at the level its entry states and **none is
verified anywhere in this work**; they are cited for what they say, not
as support for anything claimed here.

67. B. Cloitre, *A tauberian approach to RH*,
    [arXiv:1107.0812](https://arxiv.org/abs/1107.0812), submitted 5 July 2011.
    Introduces functions of good variation and the family approaching
    $x\mapsto x^{-1}\lfloor x\rfloor$, by the author's account inspired by the
    Ingham summation process. Cited in §R12A for the shared coordinate and in §R23
    for the exponent route.

68. B. Cloitre, *A tauberian characterization of the Riemann hypothesis through
    the floor function*,
    [arXiv:2407.18859](https://arxiv.org/abs/2407.18859), submitted 26 July 2024.
    The term *regular arithmetic function* and the floor-function
    characterization appear here.

69. B. Cloitre, *Regular arithmetic functions, Volume I: theory, applications,
    examples*,
    [arXiv:2609.09366](https://arxiv.org/abs/2609.09366), submitted 8 September
    2026, 374 pages. The kernel $G(n,k)$, the regularity index, and the
    statement that the hypothesis holds exactly when Ingham's kernel has index
    $1/2$. Abstract read; the body is not read.

70. S. Xu, *Positivity and asymptotics for Chenevier's orthogonal polynomials*,
    [arXiv:2609.10328](https://arxiv.org/abs/2609.10328), submitted 9 September
    2026. Positivity in every degree from strict negativity of all Verblunsky
    coefficients of an associated circle measure. Cited in §R12A as the transporting case. Abstract read.

71. Lean formalization of the Li criterion against the ambient library's own
    Riemann-hypothesis predicate, public repository
    `li-criterion-rh-equivalence-lean`, registry entry
    `PALOMAR-2026-09-05-000005`. Statement and sources read at file level; the
    project was not compiled in the course of this work, and the axiom report
    quoted in §R22 is the one the sources declare.

72. X. Zhu, *Weil positivity in compact windows: a finite reduction, certified
    two-sided bounds, and a Landau--Widom decay law*,
    [arXiv:2608.24827](https://arxiv.org/abs/2608.24827), submitted 25 August
    2026, revised 2 September 2026, 34 pages. The certified window bound and the two-sided
    decay law quoted in §R23. Abstract, discussion and failed-route sections
    read; the body is not read.

73. B. Cloitre, *On the orthorecursive expansion of unity*,
    [arXiv:2505.09645](https://arxiv.org/abs/2505.09645), submitted 11 May 2025.
    The tauberian transfer from a discrete recurrence to a Volterra integral
    equation referred to in §R23. Abstract read.

74. B. Riemann, *Ueber die Anzahl der Primzahlen unter einer gegebenen
    Grösse*, Monatsberichte der Königlich Preussischen Akademie der
    Wissenschaften zu Berlin, November 1859. The source of the hypothesis, of
    the explicit formula whose oscillation periods are quoted in §R9A, and of
    the counting statement completed by von Mangoldt.

75. M. Aissen, I. J. Schoenberg, and A. Whitney, "On the generating functions
    of totally positive sequences I," *Journal d'Analyse Mathématique* 2
    (1952), 93–103; A. Edrei, "On the generating functions of totally
    positive sequences II," *ibid.*, 104–109. Announced in M. Aissen,
    A. Edrei, I. J. Schoenberg and A. Whitney, "On the generating functions of
    totally positive sequences," *Proceedings of the National Academy of
    Sciences* 37 (1951), 303–307, which carries all four names on one note;
    the 1952 sequel is the two-part paper cited first. The characterization of
    Pólya frequency sequences used at (12.9).

76. D. K. Dimitrov and F. R. Lucas, "Higher order Turán inequalities for the
    Riemann $\xi$-function," *Proceedings of the American Mathematical
    Society* 139 (2011), 1013–1022.

77. M. Griffin, K. Ono, L. Rolen, and D. Zagier, "Jensen polynomials for the
    Riemann zeta function and other sequences," *Proceedings of the National
    Academy of Sciences* 116 (2019), 11103–11110. Hyperbolicity of every fixed
    degree for all large $n$; all degrees for all $n$ is the hypothesis.

78. J. Holland, *A new hyperbolicity wedge and a joint semicircle limit for
    Jensen polynomials of Riemann's $\xi$-function*,
    [arXiv:2608.08682](https://arxiv.org/abs/2608.08682), submitted 9 August
    2026. Reports the threshold $n^3\log^2(n+2)\ge Kd^5$ for its own Jensen
    family; no transfer to the ordinary-coefficient minors in (12.9) is
    asserted. Abstract and statement of the wedge read; the body is not read.

79. H. L. Montgomery, "The pair correlation of zeros of the zeta function,"
    in *Analytic Number Theory*, Proceedings of Symposia in Pure Mathematics 24,
    American Mathematical Society, 1973, 181--193. The historical theorem and conjectured density
    are distinguished in Section 61A; the comparison does not import the
    conjecture as an actual-source estimate.

80. L. Elaissaoui and Z. E.-A. Guennoun, "Fourier expansion of the Riemann
    zeta function and applications," *Journal of Number Theory* 211 (2020),
    113--138,
    [DOI 10.1016/j.jnt.2019.09.025](https://doi.org/10.1016/j.jnt.2019.09.025);
    preprint arXiv:1809.02829. Theorem 1.1 and Corollary 2.4 of the preprint
    (v2): the zeta Fourier-coefficient and Parseval identities. Section 155G
    re-derives the Mellin normalization independently.

81. V. Liu, *Certified Weil Positivity Beyond the Unit Window*, manuscript
    submitted to *Mathematics of Computation*, 14 September 2026; reproducible
    source repository `luciferyu666/certified-weil-positivity`. Fixed-window
    claims only; not peer-reviewed, not on arXiv, and the repository states
    that external reproduction has not yet been completed. Cited in §R23 only
    as an external comparison and NO-GO for a specified localization.

82. A. Pearce-Crump, *Optimising Selberg's method for critical zeros*,
    arXiv:2609.15329v1, 14 September 2026. Theorem 1.1 proves
    $\kappa_0>0.0700162$ by a positive-semidefinite sum of three squared
    mollifiers; cited in §R12 only as a methodological comparison.

Entries 83--120 were added in the previous edition. They are the classical primary sources, and
the modern accounts, for results that this volume uses or re-derives. Each is
cited for the statement named where it is used.

83. Nicomachus of Gerasa, *Introduction to Arithmetic* (c. 100 CE), end of
    Chapter 20; used at (2.3).
84. J. Faulhaber, *Academia Algebrae*, Augsburg, 1631; used at (2.1).
85. C. G. J. Jacobi, "De usu legitimo formulae summatoriae Maclaurinianae,"
    *Journal für die reine und angewandte Mathematik* 12 (1834), 263--272,
    [DOI 10.1515/crll.1834.12.263](https://doi.org/10.1515/crll.1834.12.263).
    The first general proof of Faulhaber's assertion.
86. D. E. Knuth, "Johann Faulhaber and sums of powers," *Mathematics of
    Computation* 61 (1993), no. 203, 277--294,
    [DOI 10.2307/2152953](https://doi.org/10.2307/2152953). The inverse form
    and derivative rule of §R2.
87. R. Wituła, K. Kaczmarek, P. Lorenc, E. Hetmaniok, and M. Pleszczyński,
    "Jordan numbers, Stirling numbers and sums of powers," *Discussiones
    Mathematicae – General Algebra and Applications* 34 (2014), 155--166,
    [DOI 10.7151/dmgaa.1225](https://doi.org/10.7151/dmgaa.1225). The case
    $r=1$ of their product decomposition (13) is $3S_2=j_nT_n$, the summed form
    of (2.2a).
88. N. Derby, "A search for sums of powers," *The Mathematical Gazette* 99
    (2015), no. 546, 416--421,
    [DOI 10.1017/mag.2015.77](https://doi.org/10.1017/mag.2015.77). Used in
    §§R2 and R5C; the printed quadratic should read $(p-T_{2n})(p+n)=0$.
89. D. Singmaster, "How often does an integer occur as a binomial
    coefficient?" (Research Problems), *American Mathematical Monthly* 78
    (1971), no. 4, 385--386,
    [DOI 10.2307/2316907](https://doi.org/10.2307/2316907).
90. B. Pascal, *Traité du triangle arithmétique*, Paris, 1665 (written 1654).
91. P. Mengoli, *Novae quadraturae arithmeticae, seu de additione
    fractionum*, Bologna, 1650; the telescope (4.1).
92. L. Euler, "De summis serierum reciprocarum," *Commentarii academiae
    scientiarum Petropolitanae* 7 (1740), 123--134; Euler Archive E41,
    [scholarlycommons.pacific.edu/euler-works/41](https://scholarlycommons.pacific.edu/euler-works/41/).
93. L. Euler, "De progressionibus harmonicis observationes," *Commentarii
    academiae scientiarum Petropolitanae* 7 (1740), 150--161; Euler Archive
    E43,
    [scholarlycommons.pacific.edu/euler-works/43](https://scholarlycommons.pacific.edu/euler-works/43/).
    The paper that introduces Euler's constant.
94. J. Stirling, *Methodus Differentialis: sive Tractatus de Summatione et
    Interpolatione Serierum Infinitarum*, London, 1730.
95. J. L. Raabe, "Angenäherte Bestimmung der Factorenfolge
    $1\cdot2\cdot3\cdot4\cdot5\cdots n=\Gamma(1+n)=\int x^ne^{-x}\,dx$, wenn $n$ eine
    sehr grosse Zahl ist,"
    *Journal für die reine und angewandte Mathematik* 25 (1843), 146--159,
    [DOI 10.1515/crll.1843.25.146](https://doi.org/10.1515/crll.1843.25.146).
    The source of Raabe's integral $\int_0^1\log\Gamma=\tfrac12\log2\pi$.
96. E. Cesàro, "Sur la série harmonique," *Nouvelles Annales de
    Mathématiques* (3) 4 (1885), 295--296.
97. M. B. Villarino, "Ramanujan's harmonic number expansion into negative
    powers of a triangular number," preprint (2007),
    [arXiv:0707.3950](https://arxiv.org/abs/0707.3950); see also
    "Ramanujan's harmonic number expansion," preprint (2005),
    [arXiv:math/0511335](https://arxiv.org/abs/math/0511335). Derives (GA.2),
    with an error estimate, from [120].
98. C. Mortici and M. B. Villarino, "On the Ramanujan--Lodge harmonic number
    expansion," *Applied Mathematics and Computation* 251 (2015), 423--430,
    [DOI 10.1016/j.amc.2014.11.088](https://doi.org/10.1016/j.amc.2014.11.088).
99. C.-P. Chen, "On the coefficients of asymptotic expansion for the harmonic
    number by Ramanujan," *The Ramanujan Journal* 40 (2016), 279--290,
    [DOI 10.1007/s11139-015-9670-3](https://doi.org/10.1007/s11139-015-9670-3);
    and "Ramanujan's formula for the harmonic number," *Applied Mathematics and
    Computation* 317 (2018), 121--128,
    [DOI 10.1016/j.amc.2017.08.053](https://doi.org/10.1016/j.amc.2017.08.053).
100. D. W. DeTemple, "A quicker convergence to Euler's constant," *American
    Mathematical Monthly* 100 (1993), no. 5, 468--470,
    [DOI 10.2307/2324300](https://doi.org/10.2307/2324300).
101. L. J. Boya, "Another relation between $\pi$, $e$, $\gamma$ and
    $\zeta(n)$," *RACSAM* 102 (2008), no. 2, 199--202,
    [DOI 10.1007/BF03191819](https://doi.org/10.1007/BF03191819). The
    reciprocal-triangular series (GA.3), obtained from Stirling's formula.
102. E. T. Whittaker and G. N. Watson, *A Course of Modern Analysis*, 5th ed.,
    Cambridge University Press, 2021, Chapter 12 (the Gamma function),
    [DOI 10.1017/9781009004091](https://doi.org/10.1017/9781009004091).
103. J. C. Lagarias, "Euler's constant: Euler's work and modern developments,"
    *Bulletin of the American Mathematical Society* 50 (2013), no. 4,
    527--628,
    [DOI 10.1090/S0273-0979-2013-01423-X](https://doi.org/10.1090/S0273-0979-2013-01423-X).
104. O. Espinosa and V. H. Moll, "On some integrals involving the Hurwitz zeta
    function: Part 1," *The Ramanujan Journal* 6 (2002), 159--188,
    [DOI 10.1023/A:1015706300169](https://doi.org/10.1023/A:1015706300169).
105. H. Kinkelin, "Ueber eine mit der Gammafunction verwandte Transcendente und
    deren Anwendung auf die Integralrechnung," *Journal für die reine und
    angewandte Mathematik* 57 (1860), 122--138,
    [DOI 10.1515/crll.1860.57.122](https://doi.org/10.1515/crll.1860.57.122);
    J. W. L. Glaisher, "On the product $1^1\cdot2^2\cdot3^3\cdots n^n$,"
    *Messenger of Mathematics* 7 (1878), 43--47.
106. B. Nyman, *On Some Groups and Semigroups of Translations*, thesis,
    Uppsala, 1950.
107. A. Beurling, "A closure problem related to the Riemann zeta-function,"
    *Proceedings of the National Academy of Sciences* 41 (1955), no. 5,
    312--314,
    [DOI 10.1073/pnas.41.5.312](https://doi.org/10.1073/pnas.41.5.312).
108. L. Báez-Duarte, M. Balazard, B. Landreau, and E. Saias, "Notes sur la
    fonction $\zeta$ de Riemann, 3," *Advances in Mathematics* 149 (2000),
    130--144,
    [DOI 10.1006/aima.1999.1861](https://doi.org/10.1006/aima.1999.1861).
109. L. Báez-Duarte, M. Balazard, B. Landreau, and E. Saias, "Étude de
    l'autocorrélation multiplicative de la fonction « partie
    fractionnaire »," *The Ramanujan Journal* 9 (2005), 215--240,
    [DOI 10.1007/s11139-005-0834-4](https://doi.org/10.1007/s11139-005-0834-4).
110. J. Hadamard, "Étude sur les propriétés des fonctions entières et en
    particulier d'une fonction considérée par Riemann," *Journal de
    Mathématiques Pures et Appliquées* (4) 9 (1893), 171--215,
    [Numdam](http://www.numdam.org/item/JMPA_1893_4_9__171_0/).
111. H. von Mangoldt, "Zur Verteilung der Nullstellen der Riemannschen
    Funktion $\xi(t)$," *Mathematische Annalen* 60 (1905), 1--19,
    [DOI 10.1007/BF01447494](https://doi.org/10.1007/BF01447494).
112. H. Davenport, *Multiplicative Number Theory*, 3rd ed., revised by
    H. L. Montgomery, Graduate Texts in Mathematics 74, Springer, 2000,
    Chapter 12,
    [DOI 10.1007/978-1-4757-5927-3](https://doi.org/10.1007/978-1-4757-5927-3).
    The Hadamard constant $B=-\tfrac12\gamma_{\mathrm E}-1+\tfrac12\log4\pi$
    and $\sum_\rho\Re\rho^{-1}=-B$.
113. T.-J. Stieltjes, "Recherches sur les fractions continues," *Annales de la
    Faculté des Sciences de Toulouse* (1) 8 (1894), no. 4, J1--J122,
    [Numdam](http://www.numdam.org/item/AFST_1894_1_8_4_J1_0/).
114. S. Bernstein, "Sur les fonctions absolument monotones," *Acta
    Mathematica* 52 (1929), 1--66,
    [DOI 10.1007/BF02592679](https://doi.org/10.1007/BF02592679).
115. D. V. Widder, *The Laplace Transform*, Princeton University Press, 1941.
116. A. Weil, "Sur les « formules explicites » de la théorie des nombres
    premiers," *Communications du Séminaire Mathématique de l'Université de
    Lund*, tome supplémentaire (1952), 252--265.
117. E. C. Titchmarsh, *Introduction to the Theory of Fourier Integrals*,
    2nd ed., Oxford University Press, 1948. Mellin inversion and the
    Mellin--Plancherel theorem used at (GA.6).
118. H. M. Edwards, *Riemann's Zeta Function*, Academic Press, 1974.
119. B. C. Berndt, *Ramanujan's Notebooks, Part V*, Springer-Verlag, New York,
    1998, Chapter 38, Entry 9, p. 521; the expansion (GA.2).
120. D. W. DeTemple and S.-H. Wang, "Half-integer approximations for the
    partial sums of the harmonic series," *Journal of Mathematical Analysis
    and Applications* 160 (1991), no. 1, 149--156,
    [DOI 10.1016/0022-247X(91)90296-C](https://doi.org/10.1016/0022-247X(91)90296-C).

\endgroup
