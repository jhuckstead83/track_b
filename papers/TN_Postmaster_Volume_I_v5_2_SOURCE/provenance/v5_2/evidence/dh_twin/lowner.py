"""Twin test of the principal route L_Gamma - L_P >= 0 (Reading Volume §R16).
h(x) = x S(x), S(x) = sum_[rho] 1/(x+q_rho) = (Lambda'/Lambda)(s_x)/R, s_x = (1+R)/2, R = sqrt(1+4x).
Twin: Lambda = (5/pi)^{s/2} Gamma((s+1)/2) f(s); zeta: xi(s) = s(s-1)/2 pi^{-s/2} Gamma(s/2) zeta(s).
Löwner matrix L_ij = (h(x_i)-h(x_j))/(x_i-x_j), L_ii = h'(x_i)  ==  sum_[rho] q/((x_i+q)(x_j+q)).
"""
import cmath, math, json, random
from dh import f, hurwitz, KAPPA, _B

def digamma(z):
    z = complex(z); acc = 0j
    while z.real < 15: acc -= 1 / z; z += 1
    s = cmath.log(z) - 1 / (2 * z); zp = z * z; z2 = z * z
    for j in range(1, 16):
        s -= float(_B[2 * j]) / (2 * j) / zp; zp *= z2
    return s + acc

def dlog(fun, s, r=0.05, n=32):
    """fun'(s)/fun(s) via the Cauchy integral for fun' (fun analytic, no zero in the disc)."""
    acc = 0j
    for k in range(n):
        w = cmath.exp(2j * math.pi * k / n); acc += fun(s + r * w) / (r * w)
    return (acc / n) / fun(s)

def S_twin(x):
    R = math.sqrt(1 + 4 * x); s = (1 + R) / 2
    return (0.5 * math.log(5 / math.pi) + 0.5 * digamma((s + 1) / 2) + dlog(f, s)).real / R

def Fz(s):
    """(s-1) zeta(s), analytic at s=1 (value 1); Laurent form near 1 avoids the removable singularity."""
    s = complex(s)
    if abs(s - 1) < 1e-3:
        g = [0.5772156649015329, -0.0728158454836767, -0.0048451815964480]  # Stieltjes gamma_0..2
        d = s - 1
        return 1 + g[0] * d - g[1] * d * d + g[2] / 2 * d ** 3
    return (s - 1) * hurwitz(s, 1.0)
def S_zeta(x):
    R = math.sqrt(1 + 4 * x); s = (1 + R) / 2
    return (1 / s - 0.5 * math.log(math.pi) + 0.5 * digamma(s / 2) + dlog(Fz, s)).real / R

Z = json.load(open('dh_zeros.json'))
ORB = [(0.25 + g * g, 1) for g in Z['online']] + [(complex(s, t) * complex(1 - s, -t), 2) for s, t in Z['offline']]

def S_zero_sum(x):
    tot = 0.0
    for q, w in ORB:
        tot += (1 / (x + q)).real if w == 1 else 2 * (1 / (x + q)).real
    return tot

if __name__ == '__main__':
    for x in [1.0, 50.0, 1000.0, 7344.7]:
        a, b = S_twin(x), S_zero_sum(x)
        print(f'x={x:8.1f}  S_twin(source)={a:.12e}  zero-sum(T=260)={b:.12e}  rel diff={abs(a-b)/abs(a):.2e}')
    print('zeta S(0+) ~ lambda_1 check: S_zeta(1e-9) =', S_zeta(1e-9), ' (Li lambda_1 = 0.0230957089661...)')
