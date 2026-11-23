# An alternative proof of Kurkov's logarithmic-polynomial recursion and its Leonov–Shiryaev interpretation

**Authors:** Haobo Ma, Wenlin Zhang

We give an alternative proof of Mikhail Kurkov's conjecture in OEIS A263634, FORMULA of 30 March 2025 (entry revision #166, 5 November 2025), identifying its all-column array as a specialization of the Leonov–Shiryaev product-cumulant theorem (1959). The quotient method appears in xpaul (2019), and IV_ (2020) connects its first column to logarithmic polynomials. For Kurkov's quadratic recursive array we establish R(n,k)=(n-1)![t^(n-1)]F^(k)(t)/F(t), where F(t)=1+sum_(i>=1)x_i t^i/i!. Differentiating these quotients gives the recurrence directly. We also rederive classical coefficient and Appell identities, correct a factorial normalization in the source's Appell comments, and recover the exponential-polynomial exception of Craven and Csordas (1994).

- PDF: [frozen public file](paper.pdf)
- License: CC-BY-4.0
- Version: 2
- Mathesis record: [kurkov-a263634-log-polynomials](https://mathesis-omega-research.apps.chrono-ai.fun/papers/kurkov-a263634-log-polynomials?version=2)

## How to cite

Haobo Ma, Wenlin Zhang (2026). An alternative proof of Kurkov's logarithmic-polynomial recursion and its Leonov–Shiryaev interpretation. Mathesis, version 2. https://mathesis-omega-research.apps.chrono-ai.fun/papers/kurkov-a263634-log-polynomials?version=2

## Statement progress

| Statement | Formalization status | Source | Verification basis |
|---|---|---|---|
| Theorem (s1) | preparing | [Lean source](https://github.com/the-omega-institute/trureturing/blob/6a3b29c88128eeed17f731783f03e7f9ff92ae62/D5/S3/Combinatorics/PowerSeries/KurkovA263634LogPolynomials.lean) | No public receipt |
| Corollary (s2) | preparing | [Lean source](https://github.com/the-omega-institute/trureturing/blob/6a3b29c88128eeed17f731783f03e7f9ff92ae62/D5/S3/Combinatorics/PowerSeries/KurkovA263634LogPolynomials.lean) | No public receipt |
| Corollary (s3) | preparing | [Lean source](https://github.com/the-omega-institute/trureturing/blob/6a3b29c88128eeed17f731783f03e7f9ff92ae62/D5/S3/Combinatorics/PowerSeries/KurkovA263634LogPolynomials.lean) | No public receipt |

## Contributions

Original authors are listed above. Formalization contributors and attribution are retained in `formalization/nodes.json`; repository pull requests do not confer verification or credit. Submit formalization attempts through the Mathesis attempt path described in [CONTRIBUTING.md](CONTRIBUTING.md).
