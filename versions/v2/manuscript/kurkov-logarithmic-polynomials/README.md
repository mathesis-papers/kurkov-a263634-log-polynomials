# Kurkov's logarithmic-polynomial recursion

This package contains an alternative proof of the identity

`R(n,k) = (n-1)! [t^(n-1)] F^(k)(t)/F(t)` for every `n,k >= 1`,
where `F(t) = 1 + sum_(i>=1) x_i t^i/i!`. Its first column proves
Mikhail Kurkov's conjecture in the FORMULA section of OEIS A263634,
dated 30 March 2025, entry revision #166 of 5 November 2025.

The entire array has the classical mixed-cumulant interpretation
`R(n,k)=kappa(Z^k,Z,...,Z)` with `n-1` copies of `Z`. Its recurrence is
a specialization of the Leonov–Shiryaev product-cumulant theorem (1959).
The note gives the exact translation using the two-factor identity in
Beuman–Turner–Vitelli, arXiv:1211.0993v1 (2012), Appendix A, (A10)–(A15),
and Burchardt's formal algebraic framework, arXiv:1803.09322v1 (2018),
Section 1.2 and Theorem 1.9. The quotient method is also credited to
xpaul (2019) and the A263634 connection to IV_ (2020).

The note also gives coefficient, reciprocal, Bell/cycle/Lah, matrix,
and Appell identities, with attribution to their earlier sources. It corrects
the power-sum normalization to `L_n = -(n-1)! sum_j rho_j^(-n)` for `n >= 2`
and exhibits `P_3(z) = (z+1)^2(z-2)` for `F(t)=(1-t)e^t`.
The exponential-polynomial exception is credited to Craven and Csordas
(1994, Proposition 4.1(2)).

## Files

- `note.tex`: complete LaTeX source, with its bibliography included.
- `note.pdf`: the mathematical note.
- `metadata.json`: title, creators, license, and the covered problem ID.
- `scientific-evidence.json`: statement, source, and verification coverage.
- `verify.py`: finite exact-polynomial comparisons using the Python standard library.
- `verification.json`: the corresponding output.

## Build

Use Tectonic 0.17.0:

```sh
tectonic note.tex
```

Alternatively, use a LaTeX distribution with `amsmath`, `amssymb`, `amsthm`,
`geometry`, `booktabs`, `array`, `fontenc`, `lmodern`, and `hyperref`:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

The bibliography is inline; no separate BibTeX database is required.
The commands work from the extracted package directory. The first Tectonic
build may download its standard TeX resources.

## Finite checks

Python 3.10 or newer is sufficient:

```sh
python3 verify.py > verification-new.json
cmp verification.json verification-new.json
```

Expected status: `pass`. The comparisons cover 60 all-column identities
(`1 <= n <= 10`, `1 <= k <= 6`), the first-column logarithm and partition
formula through row 10, all 44 displayed coefficients in rows 1--7 of
A263634, moment/Appell recurrences through degree 9, signed A130850 through
degree 9, cycle/Bell/Lah substitutions through row 7, and the normalization
and repeated-zero example through row 10. Rational arithmetic is exact.
The finite comparisons complement the general written proofs; they are not
an inference from a finite range to all indices.

## Formal statements

At commit `6a3b29c88128eeed17f731783f03e7f9ff92ae62`, the file
`D5/S3/Combinatorics/PowerSeries/KurkovA263634LogPolynomials.lean`
contains `result`, whose proposition is existence of the logarithmic family
and `R(n,1)=L_n` for all positive `n` over the rational polynomial ring.
Its helper `quotient_jet` expresses the all-column coefficient identity.
The note links this pinned file and the logarithmic-derivative dependency
`PositiveNewtonSums.lean` in its mathematical verification section.
The general algebra substitutions and the coefficient, Appell, and
zero-multiplicity consequences are covered by the written proofs.

## Creators and license

Haobo Ma — ChronoAI Pte Ltd, Singapore.

Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore.

Copyright 2026 Haobo Ma and Wenlin Zhang.
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
