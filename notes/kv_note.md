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
