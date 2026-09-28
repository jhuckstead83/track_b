import cmath, math, random
import dh
from dh import hurwitz, loggamma, KAPPA

def make(coef):
    def f(s):
        s = complex(s); return 5 ** (-s) * sum(c * hurwitz(s, r / 5) for r, c in coef.items())
    return f

def fe_err(f):
    random.seed(2); worst = 0
    for _ in range(6):
        s = complex(random.uniform(-0.5, 1.5), random.uniform(5, 150))
        F = lambda z: cmath.exp((z / 2) * math.log(5 / math.pi) + loggamma((z + 1) / 2)) * f(z)
        worst = max(worst, abs(F(s) / F(1 - s) - 1))
    return worst

p = complex(1.10078201, 86.14311231)
variants = {
    'standard (1, k, -k, -1)': {1: 1, 2: KAPPA, 3: -KAPPA, 4: -1},
    'kappa sign flipped (1, -k, k, -1)': {1: 1, 2: -KAPPA, 3: KAPPA, 4: -1},
}
for name, c in variants.items():
    f = make(c)
    print(f'{name:34s} |f(PP199 point)| = {abs(f(p)):.3e}   functional-eq rel err = {fe_err(f):.2e}')

# Newton-polish the PP199 point under the flipped variant, to see if it is a genuine zero there
f = make(variants['kappa sign flipped (1, -k, k, -1)'])
z = p
for _ in range(30):
    h = 1e-7; d = (f(z + h) - f(z - h)) / (2 * h); z -= f(z) / d
print('flipped-variant zero near PP199 point:', z, '|f| =', abs(f(z)))
