## Appendix B.2: Base-Shift Identity of Derived Numerators

### 1. Algebraic Statement
For a fixed base $\beta > 0$ (with $\beta \neq 1$), the rotation number of a constant $\alpha > 0$ is
$$\rho(\alpha; \beta) = \left\{\frac{\log \alpha}{\log \beta}\right\}.$$

When evaluating a derived numerator of the form $\alpha/\beta$ against its own base $\beta$,
$$\rho(\alpha/\beta; \beta) = \left\{\frac{\log(\alpha/\beta)}{\log \beta}\right\}
= \left\{\frac{\log \alpha - \log \beta}{\log \beta}\right\}
= \left\{\frac{\log \alpha}{\log \beta} - 1\right\}
= \rho(\alpha; \beta).$$

### 2. Structural Consequence
If $(\alpha,\beta)$ is approximated by a rational carrier $p/q$ with dephasing error $\delta$, then
$$\rho(\alpha;\beta)\approx \frac{p}{q}+\delta
\implies
\rho(\alpha/\beta;\beta)\approx \frac{p}{q}+\delta.$$

The entire spectral fingerprint is inherited exactly and unchanged. A derived constant evaluated against its own base denominator does not generate new geometry.

### 3. Empirical Verification
- $\rho(\pi/e; e)$ reproduces $\rho(\pi; e) \to 1/7$
- $\rho(\sqrt{2}/\pi; \pi)$ reproduces $\rho(\sqrt{2}; \pi) \to 3/10$
- $\rho(\phi/\pi; \pi)$ reproduces $\rho(\phi; \pi) \to 8/19$
