# The exact DNF complexity of the inner product function

> **Draft for arXiv (English), NOTE-001, 2026-07-23.** Markdown master —
> to be converted to LaTeX before submission. Author: Tanguy Le Mer.
> Remaining gate before submission: independent expert proofreading
> (see the French master note §6 for the reserve journal).

## Abstract

Let IP_{2n}(x, y) = Σᵢ xᵢyᵢ mod 2 be the inner product function on 2n
variables. We determine its exact DNF complexity: the minimum number of
terms in a DNF (OR of ANDs of literals, unbounded fan-in) computing
IP_{2n} is exactly (3ⁿ − 1)/2, and the minimum DNF is unique — IP_{2n}
has exactly (3ⁿ − 1)/2 prime implicants, each of which is essential.
Dually, CNF_min(IP_{2n}) = (3ⁿ + 1)/2. We further prove a
correspondence theorem: the minimum L1 weight of a real polynomial
threshold representation of IP_{2n} (monomial basis over {0,1}) equals
(3ⁿ − 1)/2 as well, with matching upper bound (the exact multilinear
polynomial) and lower bound (an explicit diagonal dual certificate all
of whose subcube moments are ±1). In terms of the total number of
variables N = 2n, the DNF size is (3^{N/2} − 1)/2 ≈ 2^{0.7925N} —
strictly between polynomial size and the generic 2^{N−1} of parity.
After an extended literature search (detailed in Section 5) we believe
the exact constant is not recorded; the result complements the active
line of work on the depth-3 complexity of inner product by settling the
depth-2 base case exactly. All statements are verified by exhaustive
computation and exact-arithmetic certificates at small sizes.

## 1. Statement

**Theorem 1 (DNF).** DNF_min(IP_{2n}) = (3ⁿ − 1)/2. Moreover IP_{2n}
has exactly aₙ = (3ⁿ − 1)/2 prime implicants, each essential (each
admits a witness point covered by it alone); the minimum DNF is
therefore unique and equals the disjunction of all prime implicants.
The companion count for the complement is |primes(¬IP_{2n})| =
bₙ = (3ⁿ + 1)/2.

**Theorem 2 (CNF).** CNF_min(IP_{2n}) = (3ⁿ + 1)/2.

**Theorem 3 (weight-PTF correspondence).** For every n ≥ 1, the
minimum L1 coefficient weight of a real polynomial p (monomial basis
over {0,1}^{2n}, unbounded degree) with p ≥ 1 on IP⁻¹(1) and p ≤ 0 on
IP⁻¹(0) is exactly (3ⁿ − 1)/2 = DNF_min(IP_{2n}).

## 2. Proof of Theorem 1

The engine is the disjoint XOR bi-decomposition

  IP_{2(n+1)}(x, y, x_{n+1}, y_{n+1}) = IP_{2n}(x, y) ⊕ (x_{n+1} ∧ y_{n+1}).

**(A) Classification of prime implicants.** Every prime implicant of
IP_{2(n+1)} is of exactly one of three forms:

- **A1**: x_{n+1} ∧ y_{n+1} ∧ M₀, with M₀ a prime implicant of ¬IP_{2n};
- **A2a**: ¬x_{n+1} ∧ M₀, with M₀ a prime implicant of IP_{2n};
- **A2b**: ¬y_{n+1} ∧ M₀, with M₀ a prime implicant of IP_{2n}.

Indeed, a term leaving the pair (x_{n+1}, y_{n+1}) free would force
IP_{2n} = ¬IP_{2n} on its projection; and ¬x_{n+1} ∧ ¬y_{n+1} ∧ M₀ is
never prime (it weakens to A2a or A2b).

**(B) Recurrence and closed form.** Writing aₙ = |primes(IP_{2n})| and
bₙ = |primes(¬IP_{2n})|, the classification gives

  a_{n+1} = 2aₙ + bₙ,  b_{n+1} = aₙ + 2bₙ,  (a₁, b₁) = (1, 2),

whence aₙ + bₙ = 3ⁿ and bₙ − aₙ = 1 by induction, so
aₙ = (3ⁿ − 1)/2 and bₙ = (3ⁿ + 1)/2.

**(C) Essentiality (lower bound).** For each prime implicant M we
construct a point covered by M and by no other prime implicant, by
induction. If M = ¬x_{n+1} ∧ M₀ (class A2a), take the inductive
witness x₀ of M₀ in IP_{2n} and append (x_{n+1}, y_{n+1}) = (0, 1);
the fixed pair excludes all A1 terms and all A2b terms with the
mirrored coordinate, and the inductive property excludes competing A2a
terms. Symmetrically for A2b with (1, 0), and for A1 with (1, 1) using
the witness of M₀ in ¬IP_{2n}. Every DNF for IP_{2(n+1)} must
therefore contain every prime implicant, so DNF_min = aₙ. ∎

## 3. Proof of Theorem 2

By De Morgan, CNF_min(f) = DNF_min(¬f). The key observation is that
the XOR bi-decomposition is invariant under complementation:

  ¬IP_{2(n+1)} = ¬IP_{2n} ⊕ (x_{n+1} ∧ y_{n+1}),

i.e. the complement has exactly the same shape g ⊕ (x ∧ y) with base
¬IP_{2n}. The entire apparatus of Section 2 transfers verbatim with
IP ↔ ¬IP exchanged: the classification yields the second half of the
recurrence (b_{n+1} = aₙ + 2bₙ), and the witness construction yields
essentiality of every prime implicant of ¬IP_{2n} (base case n = 1:
¬IP₂ = ¬x₁ ∨ ¬y₁, two primes, witnesses (0,1) and (1,0)). Hence
DNF_min(¬IP_{2n}) = bₙ = (3ⁿ + 1)/2. ∎

## 4. Proof of Theorem 3

**Upper bound.** The exact multilinear polynomial
p* = (1 − Π(1 − 2xᵢyᵢ))/2 has coefficients (−1)^{|S|+1} 2^{|S|−1} on
the paired monomials Π_{i∈S} xᵢyᵢ, so its L1 weight is
Σ_s C(n,s) 2^{s−1} = (3ⁿ − 1)/2, and p* takes values exactly in {0,1},
hence is a valid threshold representation after the shift p ≥ 1 ⇔
p* = 1 (rescaling p = p* works since p* ∈ {0,1}).

**Lower bound (diagonal dual certificate).** Consider the signed
measure supported on the diagonal x = y:

  w(x, x) = (−1)^{|x|+1} 2^{n−|x|} for |x| ≥ 1,  w(0, 0) = −(2ⁿ − 2),

and w = 0 off the diagonal. A one-line computation shows every subcube
moment of w equals ±1 (the inner sum telescopes to
(−1)^{s+1} 2^{n−s−r} (2−1)^r with n − s − r = 0), and its positive
mass is Σ_{a odd} C(n,a) 2^{n−a} = (3ⁿ − 1)/2. Weak LP duality then
gives W_{L1} ≥ (3ⁿ − 1)/2 over the reals. ∎

The certificate lives on the diagonal x = y — where IP restricts to
parity. Note the coincidence DNF_min = W_{L1}: a priori the two
quantities are incomparable (neither bound implies the other); IP
realizes both at the same value.

**A transversal constant.** Three depth-2-type quantities for IP land
on the same scale 3^{n}:

| Model | Quantity | Value |
|---|---|---|
| DNF | DNF_min(IP_{2n}) | (3ⁿ − 1)/2 (this note, Thm 1) |
| CNF | CNF_min(IP_{2n}) | (3ⁿ + 1)/2 (this note, Thm 2) |
| Consistent 2-CNF | max satisfying assignments (Frankl-Gryaznov-Talebanfard, ITCS 2022) | 3ⁿ (tight) |
| Real PTF weight | min W_{L1}(IP_{2n}) | (3ⁿ − 1)/2 (this note, Thm 3) |

## 5. Related work and novelty status

The active line on the **depth-3** complexity of IP (Golovnev-Kulikov-
Williams ITCS'21; Frankl-Gryaznov-Talebanfard ITCS'22; Göös-Guan-
Mosnoi MFCS'23/I&C'24, Σ³₂ ∈ [2^{0.847n}, 2^{0.965n}]; Amano ISAAC'23;
Gurumukhani et al. 2026) never states the depth-2 case; this note
supplies its exact base point. Standard covering bounds give only
~2ⁿ − 1 (the essentiality of *all* primes is what pushes to 3ⁿ/2).
The switching-theory literature was checked at the source: Sasao-Butler
(ASP-DAC 2001) handle AND/OR-orthodox bi-decompositions — the XOR
case of IP is outside their calculus (verified on the full text); the
Butler-Sasao cryptographic tutorial treats IP as a bent function from
the ANF angle, with no SOP size. Compendia (Jukna 2012; Crama-Hammer
2011) state the prime-implicant framework but not this count. A
targeted search of the Russian school (Yablonskii and coll.,
*Problemy Kibernetiki*), in Russian and English, found no trace of the
function or the constant; non-digitized volumes remain the sole
residual reserve. We therefore present the exact constant as, to the
best of our knowledge, unrecorded — and would welcome any earlier
reference.

## 6. Computer verification

All claims are machine-verified in the accompanying repository:
DNF_min = 1, 4, 13, 40, 121 for n = 1..5 by exhaustive prime
enumeration plus exact set-cover ILP (CBC); prime counts and
essentiality on both IP and ¬IP for n = 1..4 by brute force; the dual
certificate of Theorem 3 in exact rational arithmetic for n = 1..14
plus brute-force cross-check for n ≤ 4; the LP optimum 40/121 at
n = 4, 5 matched by the symmetrized dual to 10⁻⁸.

## 7. Disclosure

This note results from an AI-assisted exploration (Claude, Anthropic),
with the adversarial-verification methodology of the repository
pvsnp-exploration: every claim above is either proved in full in this
note or backed by an executable exact-arithmetic check; the proofs
were human-read by the author. AI assistance is disclosed per arXiv
policy.
