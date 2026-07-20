# Brouillon — synthèse Conjecture 13 pour Vaibhav Krishan

> À envoyer par Tanguy uniquement. Fait suite à l'échange sur la
> Conjecture 5 (« would be happy to hear back if you have more thoughts »).
> Tout est vérifié par calcul exact ; statuts épistémiques en fin de note.

---

**Subject:** Re: Conjecture 5 — some computations and a small theorem on your Conjecture 13

Dear Vaibhav,

Following up on your kind reply — we took your main conjecture
(Conjecture 13) as the next target and computed, as far as we know for
the first time, its exact values at small sizes. Three things came out
that may interest you: exact data, a padding recursion, and a small
unconditional theorem. Everything below is exact arithmetic (no floating
point in the certified statements); code and tables are available.

**0. The statement, to fix notation.** Throughout, we mean your
Conjecture 13 (ECCC TR24-074): with P(n,d) the projection onto the
orthogonal complement of the evaluations of degree-≤d polynomials on
{0,1}ⁿ, and MAJ_n the 0/1 majority vector,

  min_{Z ∈ Z^{2^n}} ‖P(n,d)·(Z + MAJ_n/2)‖ ≥ 2^{n/2}/n^{O(1)}
  for every d = o(√n / log n)

— i.e. the nearest point of the integer-shift lattice to MAJ_n/2, after
quotienting out real degree-≤d polynomials, stays at essentially the
trivial distance scale. (This is the ℓ₂ torus-polynomial hardness of
majority; via BHLR it feeds your Conjecture 3 and the MAJ ∉ ACC
program.) We work with the SQUARED distance D(n,d) =
min_Z ‖P(n,d)(Z + MAJ_n/2)‖², so your conjectured bound reads
D(n,d) ≥ 2ⁿ/n^{O(1)}, and we also use the normalization q = D/2ⁿ
(the conjecture: q ≥ 1/poly). For thresholds other than the central
one we write D(n, d, t) with THR_t in place of MAJ.

**1. Exact values.** Certified values (complete enumeration + exact
verification), scaled as q = D/2^n, in units of 1/1024:

  d=1: 19/1024 (n=5) ... saturating ≈ 22.4/1024 by n≈23
  d=2: 5 (n=5), 7 (n=7), 8.73, 10.05, 11.18 (n=9,11,13)
  d=3: 1 (n=5), 1 (n=7), 1.51, 1.97, 2.38, 2.79 (n=9..15)

(n ≥ 9 computed in the weight-space reduction below.) No collapse
anywhere: q grows with n at every fixed d in the accessible range —
consistent with your conjecture, with room to spare.

**2. A padding recursion.** Fixing two variables decomposes MAJ_{n+2}
into four fibers with thresholds (t, t−1, t−1, t−2), and restriction
preserves degree ≤ d, which gives the unconditional inequality

  D(n+2, d, t) ≥ D(n, d, t) + 2·D(n, d, t−1) + D(n, d, t−2),

a (1,2,1)-convolution over thresholds. Empirically this is TIGHT at the
central threshold ((7,2) and (7,3): equality, exact rationals) and strict
off-center. The mechanism: the optimal residual at the center factorizes
exactly fiber-by-fiber — for every one of the 21 choices of the fixed
pair simultaneously — while off-center the patching constraint forces a
quantifiable excess (e.g. the THR_0 fiber is forced to carry 25/256 where
0 is freely achievable).

**3. A small theorem on Conjecture 13 at constant degree.** Iterating
the recursion gives binomial weights, and the central binomial matches
the 2^n normalization exactly. With the certified base profile at n₀ = 5
(S_d = Σ_w D(5,d,w) = 35/16, 31/32, 3/16 for d = 1, 2, 3):

  D(n, d, (n+1)/2) ≥ S_d · C(n−5, (n−5)/2 + 2) ≥ S_d · 2^{n−5}/(8√n),

hence dist ≥ (√S_d/16)·2^{n/2}/n^{1/4} for all odd n — i.e. **your
Conjecture 13 holds for every constant d ≤ 3** (the n^{1/4} loss is
within your n^{O(1)}). We checked the bound against all our certified
values: no violation, tight exactly at the two known centers. This
extends to a growing-degree slice: re-basing the same recursion at
n₀ = 2d+1, where the exact-representability map of point 5 below gives
the unconditional base D(2d+1, d, d+1) ≥ 1/2^{d+3} for EVERY d (the
window [0,d] always contains r = 0), yields

  D(n, d, (n+1)/2) ≥ C(n−2d−1, (n−2d−1)/2)/2^{d+3},
  i.e. dist ≥ 2^{(n−3d)/2 − 2}/(2n)^{1/4} —

so **Conjecture 13 holds unconditionally for all d ≤ (2K/3)·log₂ n,
any constant K**, with polynomial loss n^{K+1/4}. (We verified every
link numerically: the exact bases b_d for d = 2..7 — all ≥ 1/8 from
d = 3 on, exactly 1/8 at Mersenne d = 3, 7 — and the assembled chain
on five solver cells, no violation.) The 2^{3d/2} loss quantifies
precisely where this padding route dies: beyond d ~ log n one must
recover the ~4^d normalization gap, which is exactly the parity-coupling
problem of point 7. As far as we could verify, your §7 treats the Z = 0
(real polynomial) slice, and we found no asymptotic lower bound on
min_Z in the paper — but you would know better than us whether any of
this is folklore.

**4. Two structural facts you may find useful.** (i) On all 28 cells
where we could compare, the optimum over Z^{2^n} is attained by a
SYMMETRIC Z — which reduces the computation to dimension n−d and is how
we reached n = 23. One cell resists: at (n,d) = (7,1) the symmetric
optimum is 81/32 while the fiber bound gives 19/8 — either the central
tightness fails first at d = 1, or an asymmetric witness wins there;
we could not close it. (ii) The d-decay of q at fixed n is irregular
(successive ratios 1.9, 4.7, 2.5, 2.8 at n = 13) — no clean geometric
law; and d = 1 saturates to a constant, which suggests a closed form.

**5. A small theorem explaining your Theorem 1.4.** Measuring the
diagonal n = 2d−1 revealed a binary law, which we then proved
unconditionally (both directions, no symmetry assumption):

  MAJ_{2d−1} admits an EXACT degree-d torus representation (zero error)
  if and only if d is a power of 2 — and for other d,
  D(2d−1, d) ≥ 1/2^{d+3}.

The proof is elementary: in weight space the dual lattice is generated by
the shifted (1−x)^{d+1} stencils, the pairings with MAJ come out as
±C(d, r), and Lucas' theorem does the rest; the "only if" uses the
(d+1)-subcube parity duals, which produce the same binomials. This
generalizes to a complete unconditional characterization for every
threshold: THR_w on n variables has an EXACT degree-d torus
representation iff the interval [max(0, w−n+d), min(d, w−1)] contains no
binary submask of d (i.e. no r with C(d,r) odd), and otherwise
D ≥ 1/2^{d+3}. We verified this map against every value we ever measured
(and 1936/1936 cells n ≤ 18 against the direct kernel criterion). It
explains the d = 2^t condition in your Theorem 1.4: at (d, n, w) =
(2^t, 2d+1, d+1) the window contains r = 0, so exact representation is
impossible — while at n = 2d−1 it becomes possible, exactly for powers
of two.

**6. The Mersenne diagonal, and a parity ghost.** At n = 2d−1 the map
above gives exact representability precisely at powers of two; at
n = 2d+1 we find D = 1/8 exactly for d = 1, 3, 7 (certified) and, by an
explicit witness, D ≤ 1/8 for every Mersenne d = 2^k − 1 (verified
exactly up to d = 31). The closed form behind it: the optimal residual
is the PARITY function, R_k = (−1)^k/2^{d+2} on Hamming levels — its
B-orthogonality to degree ≤ d is just (1−x)^n divisible by (1−x)^{d+1},
its stencil pairings are ±1/2 by the binomial theorem, and integer
attainability of the half-alternating class is exactly Lucas' condition
(all C(d, r) odd ⟺ d Mersenne). So at the Mersenne diagonal, the nearest
torus point to MAJ/2 misses it by exactly a scaled parity vector — the
classic hard function for these algebraic models appearing as the
extremal direction of the majority problem. The matching lower bound
(D = 1/8 exactly for all Mersenne d) is certified for d ≤ 7 and open
beyond.

**7. Where your conjecture lives: the parity couplings of a binary
cascade.** Fixing one variable and minimizing jointly gives an EXACT
identity: D_f(n+1, d) equals a parity-coupled min of two terms — the
XOR-of-fibers class at degrees d and d−1. For MAJ the fiber-XOR is your
Δ function, and iterating, the classes follow Pascal-mod-2 dynamics
(Lucas rows). The decoupled bound D_f(n+1,d) ≥ ½D_h(n,d) + ½D_h(n,d−1)
is tight at MAJ centers on all 7 cells we tested (exact equality in
rationals) — but an exact dynamic-programming evaluation shows the
decoupled cascade guarantee collapses geometrically (~(1/3)^d) at
n ~ d², while the true value stays ~constant. Since the identity loses
nothing except one parity constraint per step, this localizes
Conjecture 13 completely: it is equivalent to the accumulated parity
couplings recovering a ~3^d factor along the cascade. Parity seems to
be the recurring actor here — it was also the mechanism refuting
Conjecture 5 (the ±2 ends), and the extremal residual at the Mersenne
diagonal. One more measurement worth reporting: the coupling gain is
DISTRIBUTED across essentially all cascade levels (replacing the cascade
by exact coupled values up to depth k recovers the truth only gradually,
~3-5% per level near the top) — so no bounded-depth coupled lemma can
close the gap; whatever proves your conjecture must control the parity
interactions globally. The couplings themselves have a clean algebraic
form: a cascade step is coupling-free iff optimal integer solutions of
the two Δ subproblems have parity difference equal to the threshold
offset modulo the REED-MULLER code RM(d, n) (the parity freedom of a
class is exactly integer degree-≤d polynomials mod 2) — verified on the
(5,2,3) decomposition. So your Conjecture 13 appears to be, at bottom, a
statement about Reed-Muller compatibility of delta-CVP optima along
Pascal-mod-2 dynamics. Unfolding one level further (S = pi + 2T), the
couplings are themselves CVPs on QUARTER-integer classes, whose own
couplings live on eighths, and so on: the analysis is self-similar
across an infinite dyadic tower — which we believe is the structural
reason no finite/local argument closes the gap. If anything proves the
conjecture along these lines, it would seem to need a fixed-point or
renormalization-type argument over this dyadic hierarchy.

**8. The diagonal base, certified far beyond our theorems.** Write
b_d = D(2d+1, d, d+1), the base your conjecture's padding transport
starts from. An emptiness test at radius 1/8 (exact LLL on the quotient
form — the enumeration trees collapse from ~10⁸ nodes to fewer than 20)
certifies: **b_d ≥ 1/8 for every d ≤ 16, with equality exactly at the
Mersenne d = 3, 7, 15** — in particular D(31, 15) = 1/8 exactly, the
matching lower bound for the Mersenne witness of point 6, which we had
only up to d = 7. Transference certificates (integer-pairing duals in
the parity×polynomial complement) give explicit lower bounds up to
d = 64, decreasing monotonically toward the Mersenne level 1/8 at
powers of two (μ-values 2.20, 2.10, 2.05, 2.016 at d = 8, 16, 32, 64,
each certified by exact enumeration — 261 nodes at dimension 33, 577 at
dimension 65).

**9. Where we currently believe your conjecture lives: a signed theta
series.** By Poisson summation on the weight-space quotient lattice,
the lower bound D ≥ (s²/4π)·ln(1/Θ(s)) holds for every s, with Θ a
dual theta series whose phases are ±1 given by Lucas-type parities of
the MAJ pairing. Three facts we verified about it: (i) the unsigned
series is ≥ 1 always (the zero coset lives in the same lattice), so
the bound is nontrivial ONLY through sign cancellation — and the
homogeneous lattice has constant packing (λ₁ ≈ 4 across all our cells)
while 4D grows like 2ⁿ/poly: your conjecture says the MAJ coset is a
DEEP HOLE of relative depth 2ⁿ/poly in a dense lattice, a purely
arithmetic property no lattice-geometric bound can see; (ii) the scale
at which the theta bound retains ≥ 90% of the truth follows the clean
law s²/4D = f(n−2d), the same for d = 2 and d = 3 (7 cells, predicted
then verified out of sample), numerically ≈ Θ(1/(n−d)) — Banaszczyk's
scale; (iii) the sign cancellation is hierarchical: grouping the dual
sum by m mod 2 splits it into 2^r signed class masses, and the net sum
is 25× (at n=9) then 2264× (at n=11) smaller than the total pairwise
imbalance — the cancellation deepens with n across all scales, which
matches the dyadic self-similarity of point 7 and suggests the right
tool is an exponential-sum/Gauss-factorization analysis rather than
any finite combinatorial lemma. One more measurement, which is the
single most direct piece of evidence we have for your conjecture:
writing ρ(x) for the signed-to-unsigned ratio at scale x = s²/4D, we
find ln(1/ρ) = π/x − c(n,d) with the SAME slope π on every cell we
tested (six cells, fitted slopes 3.16-3.34), and the correction
c(n,d) stays in the narrow band [0.7, 1.5] across a grid where the
squared distance itself spans two orders of magnitude (4D from 3 to
358; n = 9..13, d = 2, 3) — the cancellation profile is universal,
c shows no growth, and your conjecture is exactly the statement that
this scalar stays polylogarithmic. (Caveat: at three values of n a
slow log-growth would be invisible, and all of this is still the
regime n ≫ 2d.) The normalization is fully explicit:
det of the quotient form = ∏_k C(n,k)/det(XᵀBX) with the binomial
Hankel determinants in closed form (n·2^{2n−2}, n²(n−1)·2^{3n−7},
n³(n−1)²(n−2)·2^{4n−14}/3 for d = 1, 2, 3; verified exactly on 15
cells).

Caveats we want to state plainly: the n ≥ 9 curve values assume the
symmetric-optimum reduction (verified exhaustively for n ≤ 7 only); the
log n theorem is still far from your regime d = o(√n/log n) — the
4^d normalization loss at the base is geometric and no improvement of
b_d moves that frontier; the theta-scale law is measured on 7 cells and
extrapolation is a conjecture of curve; and we have no asymptotic claim
about the signed series itself — isolating and instrumenting it is
where our contribution stops.

Happy to share the code (exact CVP with certified enumeration), the full
tables, or the witnesses themselves if any of this is useful to you.

Best,
Tanguy

---

## Statut épistémique (hors email, pour Tanguy)
- Valeurs n ≤ 7 : CERTIFIÉES full-space (énumération complète + exact).
- Valeurs n ≥ 9 : exactes SOUS l'hypothèse symétrique (28/28 vérifiée
  n ≤ 7) — dit explicitement dans l'email.
- Lemme + théorème d ≤ 3 : PROUVÉS (AS-004/AS-008), contre-vérifiés 16/16.
- Théorème d = O(log n) : PROUVÉ (AS-022 = AS-011 + AS-004 assemblés,
  inconditionnel), maillons vérifiés (bases d=2..7 exactes, chaîne 5/5).
- Point 8 : loi b_d CERTIFIÉE d ≤ 16 (tests de vide exacts, AS-023) ;
  D(31,15) = 1/8 certifié ; μ_32/μ_64 certifiés par énumération exacte
  (AS-027/028).
- Point 9 : obstruction et λ₁ ≈ 4 (AS-039), loi x₉₀ 7 points
  (AS-037/040), formes closes des déterminants vérifiées 15/15
  (AS-040), anatomie hiérarchique 2 cellules (AS-041 — tendance de
  2 ordres de grandeur, d=2 non exécuté : dit « at n=9 / n=11 » sans
  généralisation). Aucune revendication asymptotique sur S_± —
  explicite dans l'email. Loi π/x + bande c ∈ [0,7 ; 1,5] : MESURÉ
  6 cellules (AS-042/043), caveat log-croissance et régime n ≫ 2d dit
  dans l'email.
- Antériorité : §6/§7 KV lus en entier ; réserve « folklore » laissée à
  Krishan — posture correcte. [Les formulations coset/thêta/trou
  profond n'ont pas d'équivalent dans les textes audités, SANS garantie
  d'originalité — l'email les présente comme « where we currently
  believe », pas comme des résultats de littérature.]
- (7,1) : ouvert, présenté comme tel.
