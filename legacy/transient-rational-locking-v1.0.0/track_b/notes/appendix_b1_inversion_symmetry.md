## Appendix B.1: Inversion Symmetry of Spectral Fingerprints

### 1. Algebraic Statement
For a fixed base $\beta > 0$ (with $\beta \neq 1$), the rotation number of a constant $\alpha > 0$ is defined as:
$$\rho(\alpha; \beta) = \left\{\frac{\log \alpha}{\log \beta}\right\}$$
where $\{x\}$ denotes the fractional part.

Assuming $\frac{\log \alpha}{\log \beta} \notin \mathbb{Z}$, evaluating the multiplicative inverse of the numerator constant $1/\alpha$ negates the argument of the fractional part, yielding the reflection:
$$\rho(1/\alpha; \beta) = \left\{-\frac{\log \alpha}{\log \beta}\right\} = 1 - \rho(\alpha; \beta)$$

*(In the edge case where $\frac{\log \alpha}{\log \beta}$ is an integer, both rotation numbers are $0$.)*

### 2. Carrier Consequence
If the original orbit is well-approximated by a dominant rational carrier $p/q$ with a dephasing error $\delta$, then
$$\rho \approx \frac{p}{q} + \delta$$
and therefore
$$1 - \rho \approx \frac{q-p}{q} - \delta.$$

This guarantees a strict, predictable transformation of the spectral fingerprint under inversion:
- **Sector Count (Denominator):** $q \mapsto q$
- **Rational Carrier:** $p/q \mapsto (q-p)/q$
- **Dephasing Error:** $\delta \mapsto -\delta$
- **Lock Scale:** $N_{\mathrm{lock}} = \frac{1}{|\delta|}$ remains unchanged

### 3. Empirical Verification
- $\phi/\pi \to 8/19$ and $\phi^{-1}/\pi \to 11/19$
- $(1+\sqrt{2})/\pi \to 10/13$ and $(\sqrt{2}-1)/\pi \to 3/13$

These matched pairs preserve denominator, lock scale, and commensurability while mirroring the carrier and reversing the drift direction.
