# HOL-006 — Mesures : le test L-transformable de la première épingle

Tâche : HOL-006. Script : `checks/hol006_L_transformable.py`. Date :
2026-08-09. Épingle : f(0000) = i, f(0001) = 1, f(1110) = 1.

Méthode : relaxation SÛRE étagée de « ∃M ∈ GL₂(ℂ) : (=₂)M ∈ L ∧
M⁻¹f ∈ L » (définition MWXZ auditée ; L = local affine, CLX SODA
2018). Conditions imposées — toutes NÉCESSAIRES pour L :
- É1 : supp(adj(M)⊗⁴f) ⊆ plat affine S (invariance du support par les
  shifts diagonaux + A exige un plat) + det(M) ≠ 0 (saturation) ;
- É2 : + (−1)^⟨σ₀,x⟩·g_x⁴ constant sur S, pour σ₀ ∈ S (dérivé de
  D_{σ₀}g ∈ A : rapports de valeurs dans {±1, ±i}) ;
- É3 : + la condition compagnon sur h = (=₂)M⊗² (plats de GF(2)²,
  signes σ₂).
Infaisabilité partout (1 ∈ idéal, Gröbner exact, 5 inconnues) =
certificat « PAS L-transformable ». Branche vivante à É3 = NON CONCLU.

## Résultats

[EN COURS — exécution retardée par une panne du classificateur
d'outils ; à compléter à la chute du run.]

## Lecture

[À compléter.]
