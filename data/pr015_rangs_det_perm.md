# PR-015 — Rangs de dérivées de det_n et perm_n : témoin exécutable de l'entrée E-6 (réplication déclarée + mesure)

Date : 2026-11-20. Instrument : `checks/pr015_rangs_det_perm.py`
(implémentation INDÉPENDANTE de la candidature n° 10 : polynômes en
dictionnaires, dérivées multilinéaires, rang exact sur F_p, p = 2³¹ − 1,
par python-flint `nmod_mat`). Commande :
`python -u checks/pr015_rangs_det_perm.py --big` — 13 s au total.

Mesures : PD_k(f) = dim span{∂^k f/∂x^S : |S| = k} ; SPD_{k,ℓ}(f) =
dim span{x^m · ∂^k f : |m| = ℓ} (décalages par tous les monômes de
degré ℓ, avec répétition).

## 1. Contrôle — PD_k = C(n,k)² pour det et perm (Nisan-Wigderson 1997, réplication)

| n | k = 1 | k = 2 | k = 3 | k = 4 |
|---|---|---|---|---|
| 3 | 9 / 9 | 9 / 9 | — | — |
| 4 | 16 / 16 | 36 / 36 | 16 / 16 | — |
| 5 | 25 / 25 | 100 / 100 | 100 / 100 | 25 / 25 |

(det / perm ; toutes = C(n,k)².) La mesure de Nisan-Wigderson est
aveugle à det contre perm.

## 2. Discriminant — SPD_{k,ℓ}, det contre perm

| (n, k, ℓ) | det | perm | écart |
|---|---|---|---|
| (3, 1, 1) | 65 | 77 | **12** |
| (3, 1, 2) | 270 | 333 | 63 |
| (3, 2, 1) | 45 | 45 | 0 |
| (3, 2, 2) | 165 | 165 | 0 |
| (4, 1, 1) | 226 | 250 | **24** |
| (4, 2, 1) | 416 | 512 | 96 |
| (4, 3, 1) | 136 | 136 | 0 |
| (4, 2, 2) | 2 651 | 3 287 | 636 |

**Les 19 valeurs de la candidature sont reproduites à l'identique.**

## 3. Le sous-lemme fin : l'écart à (k, ℓ) = (1, 1) vaut 2n(n − 1)

Mesuré : 12 à n = 3, 24 à n = 4 — soit 2n(n − 1) aux deux points.
Explication (argumentée, compatible avec les deux mesures) : les n² × n²
produits x_ab · ∂f/∂x_cd vérifient, pour perm comme pour det, les
identités d'Euler par ligne et par colonne (Σ_j x_ij ∂f/∂x_ij = f pour
chaque ligne i, idem par colonne) — 2n expressions égales à f, avec une
dépendance formelle (somme des lignes = somme des colonnes), soit
2n − 2 relations : 81 − 77 = 4 = 2·3 − 2 pour perm à n = 3. Le
déterminant porte EN PLUS les relations de Laplace-Cramer hors
diagonale, Σ_j x_ij ∂det/∂x_kj = 0 pour i ≠ k (n(n − 1) par lignes) et
leurs transposées par colonnes (n(n − 1)) : 2n(n − 1) relations, que le
permanent n'a pas. C'est exactement l'écart mesuré. La mesure décalée
voit donc une identité ALGÉBRIQUE du déterminant (le développement de
Laplace et la formule de Cramer), pas la classe VP : l'IMM, aussi dans
VP, n'a pas ces syzygies et a des SPD élevées (KLSS, LST).

## 4. Réserves

- Contrôle = réplication (Nisan-Wigderson 1997). Les valeurs SPD à
  n = 3, 4 : [NON TROUVÉ] dans la littérature consultée — mesures.
- La formule 2n(n − 1) est vérifiée à deux points et argumentée ; pas
  prouvée pour tout n ici.
- Rang sur F_p avec p = 2³¹ − 1 : un rang sur ℚ peut différer en
  principe ; les coefficients en jeu sont ±1, sans effet attendu.
