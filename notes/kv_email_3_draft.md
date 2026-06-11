# Brouillon — 3e email à Krishan & Vishwanathan (contre-exemple)

**Subject: A counterexample to Conjecture 5 (as stated)**

Dear Vaibhav Krishan and Sundar Vishwanathan,

Following up on my previous emails: continuing the lattice experiments,
we found that Conjecture 5 of TR24-074 fails as stated ("for any n, d").

At (d = 17, n = 30), the shortest vector of L(B) is unique up to sign:

  v = [2,-20,81,-156,90,182,-337,116,39,182,-116,-404,377,168,-136,
       -136,-136,168,377,-404,-116,182,39,116,-337,182,90,-156,81,-20,2]

(coefficients of x^0..x^30). It is divisible by (x-1)^18, palindromic,
of squared norm 1,217,928 — and its last coordinate is gamma_30 = 2.
No shortest vector of this cell has gamma_n = +-1.

This was verified in exact rational arithmetic by two independent
algorithms (full Fincke-Pohst enumeration, plus a constrained
enumeration showing the gamma_n = +-1 minimum is strictly larger), and
the power sums of the corresponding multisets were checked directly.

Two remarks that may be useful: the failures form a band in the (n, d)
plane (we mapped ~930 cells; first failure at d = 17, systematic for
d >= 42), while every cell we tested with d <= 16, as well as the
columns n = d+2 and n = d+3 for all d (proved), satisfies the
conjecture — so the regime your ACC application needs (d much smaller
than n) appears untouched. The conjecture likely needs a hypothesis
n >= f(d), and our map gives a first picture of f.

Same disclosure as before: AI-assisted exploration; every claim above
is verified by exact computation, and the replaying scripts are
available, as is a short note with the map and proofs.

Best regards,
Tanguy Le Mer
