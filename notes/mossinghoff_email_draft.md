# Brouillon — email à Michael Mossinghoff (rang m = 20 de BM 2000)

> À envoyer par Tanguy uniquement. Peter Borwein est décédé (2020) ;
> destinataire = M. J. Mossinghoff (CCR Princeton).
> Posture : construction vérifiée + question, PAS revendication de
> minimalité. Vérification d'antériorité post-2000 encore à faire.

---

**To:** Michael Mossinghoff
**Subject:** A height-1 pure product with a zero of order 20 at x=1 (Table 1 of your 2000 paper)

Dear Professor Mossinghoff,

I have been studying the minimal degree d(m) of a height-1 polynomial
(coefficients in {−1, 0, 1}) divisible by (1−x)^m, following your paper
with Peter Borwein, "Polynomials with height 1 and prescribed vanishing
at 1" (Experimental Mathematics 9 (2000), Table 1).

Two standard references seem to lack the value at **m = 20**: Table 1 of
your paper lists smallest-known degrees for m = 1..19 and m = 21 but has
no m = 20 row, and OEIS A059753 ("Minimal degree of a height one multiple
of (x−1)^n") currently stops at m = 14 (d = 120). If a value for m = 20
has appeared in later work, I would be grateful for the reference — my
search of the post-2000 literature may well be incomplete.

If the m = 20 entry is indeed open, here is a candidate, offered in the
same spirit as your own m = 15..21 entries (a smallest-known degree, i.e.
an upper bound, not a proven minimum). The pure product

  P(x) = ∏_{t ∈ S} (1 − x^t),   S = {1,2,3,4,5,7,8,9,11,12,13,
                                      15,17,19,21,23,27,29,31,50},

has **degree 307** and **height 1**. Two facts:

1. The order of vanishing at x = 1 is **exactly 20**, with no computation:
   each factor 1 − x^t = (1 − x)(1 + x + ... + x^{t−1}) contributes one
   factor (1 − x), and the cofactor equals t ≠ 0 at x = 1; with |S| = 20
   distinct positive exponents, the multiplicity is exactly 20.

2. The height-1 property (all coefficients in {−1, 0, 1}) I verified by
   exact integer expansion of the product.

Two remarks that may be of interest:

- **Non-monotonicity.** 307 exceeds 294, your m = 21 entry — so the
  column of extremal degrees is not monotone in m, something a missing
  m = 20 row would conceal.

- **A "transit" feature.** Among your extremals, the partial products
  (in increasing order of exponent) stay within height 2 for most ranks,
  but ranks m ∈ {15, 16, 17} require a transient height 3. The example
  above also requires transient height 3 — which may be why naive
  height-≤2 searches (including the natural pattern {1..9, 11, 13, …, 31}
  of degree 276, and its single-swap neighbours) do not reach it.

I want to be clear about what this is and is not: my search establishes
307 as minimal **only** within the bounded domain (ascending transient
height ≤ 3, degree ≤ 330). I have **not** proved d(20) = 307 — a pure
product of degree between 276 and 307 with transient height ≥ 4 is not
excluded by my search. So this is a smallest-known degree (a verified
upper bound) for the missing row, not a minimality claim — and quite
possibly improvable.

I would be very glad to know whether a value for d(20) is already
recorded somewhere, or whether this is new to you. All computations are
exact (Python, numpy/sympy) and available on request.

With thanks and best regards,
Tanguy Le Mer
