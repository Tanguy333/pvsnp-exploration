# Brouillon — réponse à Vaibhav Krishan (suite à sa validation)

> À envoyer par Tanguy uniquement. Posture : offrir nos résultats VÉRIFIÉS
> les plus pertinents à SON but (SV-approach pour le tradeoff erreur-degré
> de AND, cas symétrique), en distinguant clairement prouvé / mesuré /
> conjecturé. Ne PAS surclaim de conséquences pour ACC ou P vs NP.
> Tout est vérifiable par calcul (scripts dispo sur demande).

---

**Subject:** Re: Conjecture 5 — structure of the counterexample, and what replaces it

Dear Vaibhav,

Thank you — I'm glad it's useful. Beyond "the conjecture is false," the
computations gave a fairly complete picture of WHY, which may be more
informative for the shortest-vector approach than the bare refutation. A
few points, all verified by exact computation (no floating point in the
final checks; scripts available):

**1. The minimum is not ±1, but it IS exactly characterized.**
The shortest vector of the cell (d, n) is, in the refuting regime, not a
flat ±1 ("ideal PTE") vector but a *cyclotomic packing* of height 2. The
smallest refuting witnesses are built from a universal core
2Φ₃ + x = 2x² + 3x + 2 (and 2Φ₃² − x² for a band of d); every refuting
minimum we found is ±(1−x)^{d+1}(1+x)^a Φ₃^b · core. The exact ℓ₂ norms
have a closed form: with P_j(D) = (2D)!(2j)!/(D!·j!·(D+j)!), the core norm
is 4P_{a+2} − 4P_{a+1} + P_a and the pure-product (±1) norm is
P_{a+2} − 2P_{a+1} + P_a, and the core beats the flat vector exactly when
D ≥ 5a + 8 (one-line criterion). So the SV bound does not vanish — it is
governed by these cyclotomic quantities, which one can compute against
whatever AND-error quantity the approach needs.

**2. There is a phase boundary, and in the d ≪ n regime the minimum is
cyclotomic, not PTE.** Define φ(m) = smallest n at which the cell
(m−1, n) first has a FLAT minimum. We measured φ(m) = the Borwein–
Mossinghoff degree d(m) for m = 3..11, 13, 14, but they SEPARATE at m = 12
and decisively from m = 15 on (a "decoupling threshold" m* = 15): beyond
it, the minimum at the BM degree is a *super-packing* of small cyclotomics
(height 2), e.g. at m = 15: (x−1)^{15}Φ₂⁶Φ₃³Φ₄²Φ₅²Φ₆Φ₇²Φ₈Φ₉Φ₁₀Φ₁₁Φ₁₃Φ₁₄Φ₁₇Φ₁₉.
The minimum stays cyclotomic (algebraic phase) up to roughly n ≈ 0.65 m²,
and only becomes a flat/PTE object above that. For the symmetric-AND
application, where d is small relative to n, this is exactly the regime
where the SV minimum reflects cyclotomic abundance, not the error
structure — which may be the cleanest way to see why the approach, as
stated, cannot give the intended tradeoff there.

**3. The corrected statement that DOES hold.** A reformulation of
Conjecture 5 holds for n − d ≤ 4 (proved, all d, via a Jacobi/Hankel
bound), and is supported in the opposite regime n ≫ d (the PTE-witness
regime). It fails precisely on the proven windows in between. So the
±1-end property is not globally false — it is false exactly on a
characterized band, born at d = 17 and full by d ≈ 42.

**4. A possibly useful by-product.** For the symmetric case specifically,
the coefficient-reversal map is a lattice isometry, and the eigen-
sublattices L± (palindromic / antipalindromic) have half the rank; the
minimum is self-symmetric throughout the regime we measured (no
asymmetric minimum for d ≥ 8 over a 29k-minima census), with parity tied
to multiplicity (palindrome ⟺ even multiplicity). If the AND application
is intrinsically symmetric, working inside L± may be the natural setting.

I'd be very glad to share the exact witnesses, the closed-form norms, or
the phase data in whatever form is useful — and equally glad to hear
which of these, if any, bears on the tradeoff you were after.

Best,
Tanguy

---

## Statut épistémique (pour Tanguy, hors email)
- §1 (cœurs, formes closes P_j(D), critère 5a+8) : PROUVÉ (V-028..V-033).
- §2 (φ(m), séparation m=12, seuil m*=15, super-empilements) : MESURÉ
  exact (V-046..V-048) ; la loi ~0,65 m² est empirique.
- §3 (n−d ≤ 4 prouvé via Jacobi ; bande d=17→42) : PROUVÉ + MESURÉ (V-019).
- §4 (symétrie, recensement 29k, L± rang moitié) : PROUVÉ (lemmes) +
  MESURÉ (V-042). Le « gain L± » est conditionnel (secteur symétrique).
- AUCUNE revendication de conséquence pour ACC / P vs NP — on s'arrête à
  « ce que la SV-approach donne réellement », son propre terrain.
