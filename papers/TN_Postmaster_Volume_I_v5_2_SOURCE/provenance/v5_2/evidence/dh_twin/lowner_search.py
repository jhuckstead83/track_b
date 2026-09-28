"""Smallest non-PSD Löwner matrix of h = x S(x) for the DH twin (principal-route twin test).
Kernel: K(x,y) = sum_listed q/((x+q)(y+q))  +  divided difference of the tail T = h_source - h_listed.
Search: for N = 2.., minimize the smallest eigenvalue of the normalized matrix over node sets."""
import math, random, json, sys
from lowner import S_twin, S_zeta, ORB

def h_listed(x):
    return x * sum(((1 / (x + q)).real if w == 1 else 2 * (1 / (x + q)).real) for q, w in ORB)
# The tail T = h_source - h_listed comes from zeros above height 260 (q > 67,600), so it is
# very smooth on the search window; fit it once by Chebyshev interpolation in u = log x.
LO, HI, NCH = math.log(7344.72) - 0.75, math.log(7344.72) + 0.75, 36
_nodes = [math.cos(math.pi * (k + 0.5) / NCH) for k in range(NCH)]
_vals = [(lambda x: x * S_twin(x) - h_listed(x))(math.exp((LO + HI) / 2 + (HI - LO) / 2 * c)) for c in _nodes]
_coef = [2 / NCH * sum(v * math.cos(math.pi * j * (k + 0.5) / NCH) for k, v in enumerate(_vals)) for j in range(NCH)]
_coef[0] /= 2
def _cheb(t, deriv=False):
    b1 = b2 = 0.0; d1 = d2 = 0.0
    for c in reversed(_coef[1:]):
        b1, b2 = 2 * t * b1 - b2 + c, b1
    val = t * b1 - b2 + _coef[0]
    if not deriv: return val
    # derivative via Chebyshev-derivative coefficients
    n = len(_coef); dc = [0.0] * (n + 1)
    for j in range(n - 1, 0, -1): dc[j - 1] = dc[j + 1] + 2 * j * _coef[j]
    dc[0] /= 2; b1 = b2 = 0.0
    for c in reversed(dc[1:n]): b1, b2 = 2 * t * b1 - b2 + c, b1
    return t * b1 - b2 + dc[0]
def _t(x): return (2 * math.log(x) - LO - HI) / (HI - LO)
def tail(x): return _cheb(_t(x))
def tail_d(x): return _cheb(_t(x), True) * 2 / (HI - LO) / x
# self-check of the fit at two off-grid points
for _x in [7000.0, 9100.0]:
    _e = abs(tail(_x) - (_x * S_twin(_x) - h_listed(_x)))
    assert _e < 1e-9, ('tail fit', _x, _e)

def K_listed(a, b):
    t = 0.0
    for q, w in ORB:
        v = q / ((a + q) * (b + q))
        t += v.real if w == 1 else 2 * v.real
    return t

def lowner(xs):
    n = len(xs); M = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            k = K_listed(xs[i], xs[j])
            k += tail_d(xs[i]) if i == j else (tail(xs[i]) - tail(xs[j])) / (xs[i] - xs[j])
            M[i][j] = M[j][i] = k
    return M

def eigmin(A):
    n = len(A); a = [r[:] for r in A]
    for _ in range(100):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < 1e-30: break
        for p in range(n):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-300: continue
                th = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = (1 if th >= 0 else -1) / (abs(th) + math.sqrt(th * th + 1)); c = 1 / math.sqrt(t * t + 1); s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]; a[k][p] = c * akp - s * akq; a[k][q] = s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]; a[p][k] = c * apk - s * aqk; a[q][k] = s * apk + c * aqk
    return min(a[i][i] for i in range(n))

def score(xs):
    M = lowner(xs); d = [math.sqrt(M[i][i]) for i in range(len(xs))]
    C = [[M[i][j] / (d[i] * d[j]) for j in range(len(xs))] for i in range(len(xs))]
    return eigmin(C)

def search(N, center, width, iters, seed):
    rnd = random.Random(seed); best = (1e9, None)
    for restart in range(6):
        v = sorted(rnd.uniform(-width, width) for _ in range(N))
        cur = score([center * math.exp(u) for u in v]); step = width / 4
        for it in range(iters):
            i = rnd.randrange(N); u = v[:]; u[i] += rnd.gauss(0, step)
            if len(set(round(z, 9) for z in u)) < N: continue
            sc = score([center * math.exp(z) for z in u])
            if sc < cur: v, cur = u, sc
            if it % 60 == 59: step *= 0.7
        if cur < best[0]: best = (cur, sorted(center * math.exp(z) for z in v))
    return best

if __name__ == '__main__':
    center = 7344.72; out = []
    for N in range(2, int(sys.argv[1]) + 1 if len(sys.argv) > 1 else 9):
        mn, xs = search(N, center, 0.6, 400, N)
        print(f'N={N}: min normalized eigenvalue {mn:+.4e}  nodes {[round(x, 3) for x in xs]}', flush=True)
        out.append({'N': N, 'min_eig_normalized': mn, 'nodes': xs})
    json.dump(out, open('lowner_search.json', 'w'), indent=1)
