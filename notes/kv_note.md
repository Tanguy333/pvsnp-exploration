# Note — On Conjecture 5 of Krishan–Vishwanathan (torus polynomials, ECCC TR24-074)

> **Pour Tanguy** : mini-note de synthèse du fil V (V-001..V-011), en
> anglais, base du second email aux auteurs (brouillon en fin de
> fichier). Statut : résultats vérifiés exécutablement
> (`checks/task_v00*.py`), preuves courtes incluses, aucune relecture
> externe. Divulgation IA incluse.

---

## 1. Setting

Krishan and Vishwanathan (ECCC TR24-074) reduce torus-polynomial lower
bounds for the ∆_w functions — a step in the
Bhrushundi–Hosseini–Lovett–Rao program towards MAJORITY ∉ ACC — to:

> **Conjecture 5 (KV).** For the basis B (columns
> B[i,k] = (−1)^{i−k}·C(d+1, i−k), i = 0..n, k = 0..n−d−1), the lattice
> L(B) contains a vector γ of smallest ℓ₂ norm with γ_n = 1.

We report a reformulation, a structure theorem, proofs of the conjecture
in a large regime, and the precise frontier of what remains.

## 2. Two symmetries and a reformulation

**Lemma S (shift).** If γ ∈ L(B) has γ_i = 0 for i < k, its left shift
by k lies in L(B). *(B is lower triangular with unit diagonal, so the
first k lattice coefficients vanish; re-index the columns.)*

**Lemma R (reversal).** γ_i ↦ γ_{n−i} maps L(B) to itself.
*(R(col_k) = (−1)^{d+1} col_{n−d−1−k}.)*

**Theorem 1 (reformulation).** The following are equivalent:
(a) Conjecture 5; (b) some shortest vector has its first nonzero
coordinate equal to ±1; (c) some shortest vector has its leading lattice
coefficient equal to ±1. *(Shift, then reverse; triangularity for
(b)⟺(c).)*

Empirically the stronger form holds: in every cell we tested
(n ≤ 20, d ≤ 9), **every** shortest vector has unit first coordinate.

## 3. The polynomial form: an ℓ₂ Prouhet–Tarry–Escott problem

**Theorem 2.** The sign conjugation f_i = (−1)^i γ_i is a norm-preserving
bijection between L(B) and
`{ f ∈ Z[x] : (1+x)^{d+1} | f, deg f ≤ n }`.
*(γ = Σ a_k col_k with b_k = (−1)^k a_k gives f = (Σ b_k x^k)·(1+x)^{d+1}.)*

So the shortest-vector problem **is** the problem of minimal-ℓ₂-norm
integer multiples of a binomial power with bounded degree — a relative
of the Prouhet–Tarry–Escott (PTE) and Erdős–Szekeres pure-product
problems. Conjecture 5 says: some minimizer has unit trailing
(equivalently leading) coefficient.

## 4. The main theorem

Write f = Σ σ_i x^{a_i} (σ_i ≠ 0, a_i distinct) and t_i = σ_i(−1)^{a_i}.
Divisibility by (1+x)^{d+1} is equivalent to Σ t_i·a_i^j = 0 for
j = 0, …, d.

**Theorem 3 (uniform bound and characterization).**
(i) Every nonzero multiple of (1+x)^{d+1} satisfies ‖f‖² ≥ 2(d+1).
(ii) Equality holds iff f is flat (all coefficients in {0, ±1}) and the
± split of its exponents by sign of t_i is an **ideal PTE solution of
size d+1** (equal power sums 1..d).

*Proof.* Let A (resp. B) be the multiset of exponents counted with
multiplicity |σ_i| for t_i > 0 (resp. < 0). The j = 0 condition gives
|A| = |B| =: m; conditions j = 1..d give equal power sums 1..d. Now
‖f‖² = Σσ_i² ≥ Σ|σ_i| = 2m. If ‖f‖² < 2(d+1) then m ≤ d, and power sums
1..m (a fortiori 1..d) determine a multiset of size m over ℚ (Newton
identities), so A = B. But each exponent carries a single monomial,
hence a single sign of t — it cannot lie in both A and B. Thus
A = B = ∅ and f = 0, a contradiction. For equality, Σσ² = Σ|σ| forces
|σ_i| = 1 and m = d+1 (which escapes the Newton argument), and the
split is an ideal PTE solution. ∎

**Corollary 4.** If an ideal PTE solution of size d+1 fits in degree
≤ n, then the minimum is 2(d+1), the shifted flat witness ends at
position n with coefficient ±1, and **Conjecture 5 holds for (d, n)**.
By the known ideal-solution tables (sizes ≤ 10 and 12): the conjecture
holds in the stable regime for **d ≤ 9 and d = 11**.

For d ≤ 9 and n ≤ 20 below the stable regime, the conjecture holds by
exhaustive shortest-vector enumeration (LLL + Fincke–Pohst, exact
integer arithmetic) — 109+ cells, all confirmed, and in every cell all
minimizers have unit first coordinate.

## 5. The lattice rediscovers 1851

The first n at which the lattice minimum reaches 2(d+1), measured purely
by shortest-vector computations, is n\* = 6, 6, 11, 18 for d = 1..4 —
exactly the minimal degrees of the classical ideal PTE solutions
({0,4,5}/{1,2,6} for size 3, {0,4,7,11}/{1,2,9,10} for size 4, …). At
d = 5 the grid (n ≤ 20) never reaches 12, consistent with the minimal
size-6 ideal solution having degree 23.

## 6. What remains, honestly

1. **The small-n regime** (below the PTE transition): minima are not
   flat (e.g. coefficients ±3 at (n,d) = (7,3); ±15 at (16,8)), not
   Chebyshev-like (weak correlation with the LP duals of the torus
   programs), and not always cyclotomic (e.g. the flat minimizer
   1 + x − x⁶ − x⁹ + x¹⁰ − x¹² of (1+x)³ is not a product of
   cyclotomics). Unit first coordinates persist empirically — but we
   have no structural explanation there. This is where Conjecture 5
   genuinely lives.
2. **d = 10 and d ≥ 12 (stable regime)**: Corollary 4 is conditioned on
   the existence of ideal PTE solutions of size d+1 — open since the
   19th century for large sizes. In this regime, Conjecture 5 and the
   ideal-PTE existence problem are intertwined.

## 6bis. The size/degree map and the d = 10 wall (added 2026-06-11, after V-014/V-015)

Ideal PTE solutions are known for sizes 3..10 and 12; none is known for
size 11 nor for any size >= 13 (open since the 19th century). Through
Theorem V11 this translates degree by degree:

| known ideal sizes | degrees d closable in the stable regime |
|---|---|
| 3..10 | d = 2..9 |
| 11 : none known | **d = 10 : no witness — the first true wall** |
| 12 | d = 11 |
| >= 13 : none known | d >= 12 |

Status after V-013/V-014/V-015: Conjecture 5 is **closed for d <= 5 and
d = 7 (all n)**; d = 6 is closed except n in [82, 101] (Escott 1910
verified exactly closes n >= 102; our lattice exhaustion certifies that
no size-7 ideal solution has support in [0, 81], so n*(6) in (81, 102]).
At the transition n*(7) = 50 the lattice rediscovered Tarry 1913 and
certified its minimality (no size-8 ideal solution has support <= 49).

Consequences:

1. **d = 10 is the first degree where the witness-shift closure is
   impossible in principle** (not merely computationally): if no ideal
   solution of size 11 exists, the lattice minimum stays > 22 for all n,
   and the closure scheme has nothing to shift. The same holds for all
   d >= 12.
2. The conjecture may well survive there: on the d = 6 plateau
   (n = 33..81) all minimizers are non-ideal (size-8) solutions and the
   +-1-ends property holds throughout. So Conjecture 5 at d = 10 is
   plausibly true but, by present means, verifiable only cell by cell.
3. Cartographically: **if the torus-polynomial route needs Conjecture 5
   for unbounded d, it inherits the difficulty of the ideal
   Prouhet-Tarry-Escott existence problem, open since 1851.** This is
   the precise sense in which this route to MAJ not in ACC is hard.
4. Conversely, the lattice machinery certifies PTE non-existence on
   bounded supports (e.g. n*(6) > 81) — a tool usable on the PTE side.

## 6ter. Where could a size-11 ideal solution live? (estimation, 2026-06-11)

Our certified minimal spans split sharply by parity:

| even sizes | 2 | 4 | 6 | 8 | law |
|---|---|---|---|---|---|
| minimal span | 6 | 11 | 22 | 50 | x ~2 per size (clean geometric) |

| odd sizes | 3 | 5 | 7 | 9 | 11 |
|---|---|---|---|---|---|
| minimal span | 6 | 18 | ~92 (in (81,102]) | <= 197 (known, not certified) | ? |

Extrapolations for size 11: geometric fit ~1,300; quadratic-in-size fit
of log(span) ~12,000. But the hard constraint flips the picture: every
known odd-size ideal solution is symmetric (we verified Escott is), and
the symmetric case is excluded up to height 3500, i.e. span 7000
(Coppersmith-Mossinghoff-Scheinerman-Vanderkam 2023, arXiv:2304.11254).
Hence:

- if size 11 follows its family pattern (symmetric): span > 7000,
  plausibly ~10^4 (quadratic fit);
- if a non-symmetric one exists, it could live much lower (our
  unconditional certificate: span > 70, being extended towards ~110) --
  but it would be the first non-symmetric ideal solution beyond size 8
  (survey arXiv:2506.11429: non-symmetric known only for sizes <= 8).

Either way, size 11 sits visibly OFF its own growth curve -- the naive
extrapolation (~10^3) is already excluded in the symmetric scenario.
This quantified outlier status is the signature of why the size has
resisted since the 1910s, and why Conjecture 5 at d = 10 is the degree
where the witness-closure route fails in principle. Caveat: 3 data
points, one calibration (size 9) not certified minimal -- order of
magnitude only. Whether size 11 admits ANY ideal solution is open in
both directions: the counting heuristic is negative from size 6 onward
(exponent 2s - s(s-1)/2 = -33 at s = 11) and only algebraic structure
(symmetry + elliptic curves, as at sizes 10 and 12) ever beats it;
no such structure is known at 11, yet there is no local obstruction
(ideal solutions exist mod p) and CMSV found symmetric solutions with
just 2 quadratic irrationals -- the integral obstruction is thin.

## 6quater. A COUNTEREXAMPLE to Conjecture 5 as stated (2026-06-11)

The MINIMAL counterexample is (d = 17, n = 30): the shortest vector of
L(B) is unique up to sign -- a palindrome of squared norm 1,217,928
whose last coordinate is gamma_30 = +-2. No shortest vector has
gamma_n = +-1. Hence Conjecture 5, as stated ("for any n, d"), is
FALSE. A second cell, (d = 21, n = 30) (palindromic minimum, squared
norm 517,673,216, gamma_30 = +-2), is independently double-verified as
well. Both doubly-verified counterexamples are palindromes with
gamma_n = +-2 -- a structure theorem for deep-subtransition minima
(palindromicity) looks like a strong candidate.

Verification stack (all replayable, checks/task_v018_contre_exemple.py):
exact-rational SVP (Fincke-Pohst over Fractions, no floats; sane
witnesses pass), symbolic lattice membership ((1-x)^22 | v, sympy), and
an independent constrained enumeration in the raw stencil basis showing
the gamma_n = +-1 minimum is strictly larger. Twelve further refuting
cells confirmed exactly at d = 22..29 (first failures at n-d = 6, 9).

SCOPE -- the essential nuance, now MAPPED: the refuting region is not
sporadic but a BAND. Offsets (n - d) in [2, 20] that refute, by d (~930 exact cells):
d <= 16: none; d = 17, 18, 19: {13}; d = 20: {15}; d = 21: {9};
d = 22..28: {6, 9, 10, 16..20 vary}; d = 29..41: progressive filling;
d = 42..49: full band [8, 20]; d = 60: 9..20; d = 80: 10..20;
d = 100: 11..20 -- all in
exact arithmetic, instantaneous (the small-window cost depends on the
rank n-d, not d). For d >= 60 the band fills everything above a slowly
growing threshold offset (~9 to 11 from d = 60 to 100) at least up to
offset 20. Offsets <= 6 always pass (rigid windows). What remains of
the conjecture: the narrow initial band plus, presumably, the regime
n >> d where PTE witnesses live -- which is the regime your ACC
application needs, and which all our ~290 cells at d <= 16 support.
The statement needs a hypothesis n >= f(d); our map gives the first
quantitative picture of f.

## 6quinquies. The window law, PROVED — the corrected conjecture in closed form (night of 2026-06-11)

Master formula (verified exactly): ||(1-x)^D (1+x)^j||^2 = P_j(D) =
(2D)!(2j)!/(D! j! (D+j)!). On the unit circle |Phi_3|^2 = (1+u)^2 and
|2Phi_3 + x|^2 = (3+2u)^2 (perfect squares, u = 2cos theta), hence
N_phi = P_{a+2} - 2P_{a+1} + P_a and N_core = 4P_{a+2} - 4P_{a+1} + P_a.

THEOREM (window law). Within the dressed family
{(1+x)^{a+2}, (1+x)^a Phi_3, (1+x)^a (2Phi_3+x)}:
(i) the core beats the Phi_3-dressing iff D >= 5a+8 (one line);
(ii) the core beats the pure product iff Q_a(D) > 0, where
Q_a(D) = -(D+a+1)(D+a+2) + 8(2a+1)(D+a+2) - 12(2a+1)(2a+3),
a downward quadratic: a FINITE window between explicit roots.
The strict window for a = 3 is D in [23, 30], i.e. d in [22, 29] --
the observed staircase step, to the integer. The edge ties are the
INTEGER ROOTS of these forms (D = 31 = root of Q_3: exact tie with
(1+x)^5; D = 22 = 5a+7: exact tie with (1+x)^3 Phi_3) -- verified by
full enumeration. Across hundreds of enumerated cells, every minimum
ever observed belongs to this dressed family: the theory is closed on
all observations.

For your purposes this gives the corrected statement candidate: the
conjecture holds for n - d <= 4 (proved, all d, via the Jacobi bound),
fails on the proven windows above, and is supported beyond them only
in the PTE-witness regime n >> d.

## 6sexies. The phase map of the lattice, the forbidden-rung theorem, and a missing rank filled (2026-06-12)

A day of structure results, all verified exactly (enumeration is exact
integer arithmetic throughout; the engine is a certified compiled
Schnorr–Euchner + LLL pipeline, cross-validated against the previous
exact-rational implementation on every cell class).

**(a) Symmetry lemmas.** The coefficient-reversal map is an isometry of
every cell preserving the multiplicity at x = 1. Elementary lemmas: a
palindromic (resp. antipalindromic) integer vector has even (resp. odd)
multiplicity at 1; a flat (±1) vector with odd set-sizes is never
palindromic. Census over 29,263 minima (162 cells, d = 2..11): not one
violation; minima are always self-symmetric below a degree-dependent
threshold n_asym(d) ≈ 2 × (span of the first symmetric witness of the
current rung), and NO asymmetric minimum was ever observed for d ≥ 8 —
matching the literature boundary (non-symmetric ideal solutions are
known only up to size 8).

**(b) Forbidden-rung theorem.** For odd d, any flat self-symmetric
vector of norm 2(d+2) in L_d is necessarily an antipalindromic IDEAL
solution of size d+2 (proof: parity of multiplicity + the cardinality
obstruction + multiplicity ≤ size). Hence the orphan rungs of the
odd-d lattices encode exactly the open odd-size ideal PTE problems
(d = 9 ↔ size 11, d = 11 ↔ size 13, ...), and the closed degrees
(d = 3, 5, 7) are precisely those whose odd ideal exists (sizes 5, 7, 9).

**(c) Phase map.** Let d(m) be Borwein–Mossinghoff's minimal degree of a
height-1 polynomial divisible by (1−x)^m, and φ(m) the smallest n at
which the cell (m−1, n) has a FLAT minimum (a quantity only exhaustive
lattice enumeration can compute). Measured: φ(m) = d(m) = 6, 11, 15,
22, 30, 41, 48, 61, 69, —, 112 for m = 3..11, 13 (our lattice values
reproduce the BM table exactly, by an independent method), with a
single separation at m = 12: φ(12) = 99 > d(12) = 93. The anomaly is
explained: at spans 86..98 the multiplicity-12 cyclotomic packing
(x−1)^12 Φ₂⁴Φ₃³Φ₄²Φ₅Φ₆Φ₇Φ₈Φ₉Φ₁₁Φ₁₃Φ₁₇ (degree 86, height 2, norm 40)
beats every flat; at n = 99 a flat of norm 40 (size 20, degree 11,
palindromic, 40 terms vs 52 for the BM extremal) TIES it — a
first-order-like coexistence at the boundary. Both curves grow like
≈ 0.65 m²: the quantitative wall for the d ≪ n regime relevant to the
ACC application.

**(d) A missing rank of the BM table, filled.** The BM table (Exp.
Math. 9 (2000), Table 1) has no entry at m = 20. We found the (unique,
within ascending-transit ≤ 3 and degree ≤ 330) flat pure product with
exactly 20 factors:

  t = {1,2,3,4,5,7,8,9,11,12,13,15,17,19,21,23,27,29,31,50},
  degree 307, multiplicity exactly 20 (verified by symbolic division).

It requires transient height 3 along ascending prefixes (the BM
extremals split into transit-2 ranks {≤14, 18, 19, 21} and transit-3
ranks {15, 16, 17, 20} — a new invariant), and exhibits a
non-monotonicity: 307 > 294 = the m = 21 entry. [Post-2000 literature
check pending before any external claim.]

## 7. Epistemic note

This work was carried out in an AI-assisted exploration loop
(Anthropic's Claude) under a verify-everything policy: every theorem
above has a short human-readable proof AND an exhaustive or exact
computational verification (Python scripts, numpy/sympy only, available
on request). Two intermediate hypotheses (Chebyshev structure,
cyclotomic structure of minimizers) were formulated and refuted by
computation during the work; an intermediate sampling artifact was
caught and corrected. No external review yet.

---

## Brouillon — second email aux auteurs

**Subject:** Re: Computational verification of Conjecture 5 — now with
proofs for d ≤ 9 (stable regime)

Dear Dr. Krishan, dear Prof. Vishwanathan,

Following up on my previous message: pushing the computational study
further led to short proofs rather than just verifications, and I
thought you would want to know.

In brief (details in the attached note):
1. Two elementary symmetries of L(B) (shift and reversal) show your
   Conjecture 5 is equivalent to: some shortest vector has unit leading
   lattice coefficient.
2. The sign conjugation identifies L(B) isometrically with the integer
   multiples of (1+x)^{d+1} of degree ≤ n — an ℓ₂ variant of the
   Prouhet–Tarry–Escott problem.
3. A ten-line Newton-identities argument gives: every nonzero multiple
   has ‖f‖² ≥ 2(d+1), with equality exactly for flat polynomials whose
   sign-split is an ideal PTE solution of size d+1. Hence Conjecture 5
   holds whenever an ideal PTE solution of size d+1 fits in degree ≤ n —
   i.e. for d ≤ 9 and d = 11 in the stable regime, by the known tables.
   (The measured lattice transitions n* = 6, 6, 11, 18 for d = 1..4 are
   exactly the minimal ideal-PTE degrees.)
4. Below the transition the minimizers are neither flat, nor
   Chebyshev-like, nor always cyclotomic — that small-n regime, and
   sizes where ideal PTE solutions are unknown, seem to be where the
   conjecture genuinely lives.

Same disclosure as before: AI-assisted exploration, every claim verified
by exact computation; scripts and the note available.

Best regards,
Tanguy Le Mer
