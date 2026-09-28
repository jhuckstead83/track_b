import cmath, math, random
from dh import *

# 1) Hurwitz/zeta sanity: zeta(2)=pi^2/6, zeta(1/2+14.134725141734693i)~0
print('zeta(2) err', abs(zeta(2) - math.pi ** 2 / 6))
print('|zeta(rho1)|', abs(zeta(complex(0.5, 14.134725141734693))))
# 2) N-independence of f at height ~250
s = complex(0.7, 250.3)
print('f stability', abs(hurwitz(s, 0.2, N=200) - hurwitz(s, 0.2)), abs(f(s)))
# 3) functional equation F(s)=F(1-s) at random points
random.seed(1)
worst = 0
for _ in range(8):
    s = complex(random.uniform(-0.5, 1.5), random.uniform(5, 200))
    a, b = logF(s), logF(1 - s)
    d = abs(cmath.exp(a - b) - 1); worst = max(worst, d)
print('functional equation max rel err', worst)
# 4) Z real on the line
print('Z(50) imag/abs', abs(Z(50).imag) / abs(Z(50)))
# 5) check PP199 zero and the literature zero
for r in [complex(1.10078201, 86.14311231), complex(0.808517, 85.699348)]:
    print(r, '|f| =', abs(f(r)))
# 6) zero-free abscissa: sum_{n>=2} |a_n| n^-sigma = 1
def tail(sig):
    return 5 ** (-sig) * sum(abs(c) * hurwitz(complex(sig, 0), r / 5).real for r, c in COEF.items()) - 1
lo, hi = 1.0001, 3.0
for _ in range(60):
    mid = (lo + hi) / 2
    if tail(mid) > 1: lo = mid
    else: hi = mid
print('zero-free for sigma >=', hi, ' kappa', KAPPA)
