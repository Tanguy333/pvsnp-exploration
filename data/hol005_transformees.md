# HOL-005 — Mesures : les certificats de transformées de la première épingle

Tâche : HOL-005. Script : `checks/hol005_transformees.py`. Dates :
2026-08-08/09. Épingle (HOL-004) : **f(0000) = i, f(0001) = 1,
f(1110) = 1, 0 ailleurs** (bit k de x = (x >> k) & 1).

## Les verdicts

| test | méthode | résultat |
|---|---|---|
| (M) M-transformable | EXACT — ∃T ∈ GL₂ : (=₂)T⊗² ∈ M ∧ adj(T)⊗⁴f ∈ M (parité + MGI arité 4) ; 4 combinaisons de parités, Gröbner, det saturé | **PAS M-transformable** — 1 ∈ idéal 4/4 (< 0,1 s) |
| (A) A-transformable | relaxation SÛRE — 307 plats affines × O₂(ℂ) (rot/refl) × {I, diag(1,α), α⁴ = −1} ; zéros hors plat + puissances 4èmes égales | **PAS A-transformable** — 0 branche faisable sur 1 228 (6 s) |
| (P) P-transformable, 1ère passe | relaxation zéros-hors-motif seule | NON CONCLU (12 branches faisables — relaxation trop faible, DIAGNOSTIQUÉ : la factorisation des valeurs manquait) |
| (P2) P-transformable, RENFORCÉ | zéros hors motif + MINORS de factorisation (rang 1 par composante libre) — essentiellement EXACT sous la réduction ; 681 structures × 4 variantes | **PAS P-transformable** — 0 branche faisable sur 2 724 (8 s) |
| (R) réel-transformable | O₂(ℂ) réalifié (6 inconnues réelles, 18 équations + λ normalisé), Gröbner | **PAS réel-transformable** — 1 ∈ idéal (rot ET refl, < 1 s) |

## Lecture

Combinés aux verdicts de la grille HOL-004 (irréductible, non
symétrique, non réelle, zone K-mixte — hors huit-vertex/HW≥/HW≤/
single-weighted/vanishing —, hors A/P/M/L directes), ces certificats
font de l'épingle **la première signature concrète du dépôt certifiée
hors de : M-transformable (exact), A-transformable, P-transformable,
et réel-transformable** — c'est-à-dire hors de 4 des 5 familles
tractables transformées pertinentes pour le coin toutes-arités-paires.

**Ce qui manque, nommé** : (a) **L-transformable NON TESTÉ** (∃M ∈
GL₂ : (=₂)M ∈ L ∧ M⁻¹f ∈ L — le shift-L à matrice inconnue est plus
lourd ; HOL-006 candidate) ; (b) le périmètre des réductions : les
certificats couvrent les variantes citées (O₂(ℂ) × compagnons CGW pour
A/P ; GL₂ général pour M et pour le réel sous O₂) — toute classe
transformée définie au-delà resterait à tester ; (c) AUCUNE #P-dureté
décidée — l'épingle est hors des classes tractables décidées, ce qui
est exactement sa valeur : un objet concret du coin OÙ LA DICHOTOMIE
N'EXISTE PAS ENCORE.

## Détail de la première passe P (la leçon)

La relaxation initiale (zéros hors motif seuls) laissait 12 branches
faisables — dont le motif {0000, 0001, 1110, 1111} : support produit
{x₁ libre} × {x₂x₃x₄ ∈ {000, 111}}, mais P exige AUSSI
g[0]·g[15] = g[1]·g[14] (le minor de factorisation). Le renforcement
P2 (minors par composante libre) a fermé les 12 branches et toutes les
autres. Consigné comme rappel : une relaxation trop faible ne conclut
jamais positivement — le diagnostic de SES branches faisables est ce
qui la renforce.
