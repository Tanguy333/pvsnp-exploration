# Brouillon court — explication du moteur (pour Mossinghoff)

> À envoyer par Tanguy. Court, technique, exact.

---

On the engine: the search is a depth-first enumeration of strictly
increasing exponent tuples 1 <= t_1 < t_2 < ... < t_m, building the
partial product Prod (1 - x^{t_i}) incrementally and cutting a branch as
soon as either (a) the partial product's height exceeds a fixed transient
bound H, or (b) the remaining factors can no longer meet the degree
budget D. The inner step — multiply the current integer coefficient
vector by (1 - x^t) and test the height — is the part I run through
Numba, which JIT-compiles it to machine code via LLVM; everything is
exact integer arithmetic, so there are no precision issues.

Complexity: each node costs O(D), a single pass over a coefficient vector
of length <= D. The number of nodes is the real bottleneck — in the worst
case it is the number of admissible prefixes, of order C(D, m) (m-subsets
of {1,...,D}), which in the relevant regime D ≈ d(m) ≈ 0.67 m^2 is
super-exponential in m. The transient-height bound H is what makes it
tractable, and the cost grows sharply with H. Measured at m = 22,
D = 520, the size of the searched tree is

  H <= 1 :        748 thousand nodes
  H <= 2 :       39.6 million nodes   (x53)
  H <= 3 :        1.05 billion nodes  (x26)

at a steady ~19 million nodes/s and a flat ~0.1 GB of memory regardless
of H. So the constraint is purely time, not memory: extrapolating the
~25-50x per level, H <= 4 (which m = 22 seems to need for a non-trivial
product) is on the order of 30 minutes on one core, H <= 5 a day, H <= 6
out of reach single-threaded. A faster language buys only a constant
factor here; the real levers are a sharper height-aware prune or an
embarrassingly-parallel split of the first few levels across cores.
