# MC-010 — Données : minorants des cœurs — audit de preuve, certificats, cartographie

> Produit par `checks/mc010_minorants.py` (modes audit, certificats,
> incomparable, inegalite), 2026-08-07. Notation de la fiche MC-010 :
> classes W_B / ω_l / μ, lights (ω_l = 1), D_j = P − p(B∖{j}).

## 1. Audit — les inégalités de la preuve sur les témoins optimaux (10/10)

| cœur | W = loi | W_B | ω | μ |
|---|---|---|---|---|
| (0,2,1) | 4 | 3 | [1] | 0 |
| (0,2,2) | 6 | 4 | [1,1] | 0 |
| (0,2,3) | 8 | 5 | [1,1,1] | 0 |
| (0,3,1) | 5 | 4 | [1] | 0 |
| (0,3,2) | 7 | 5 | [1,1] | 0 |
| (0,3,3) | 9 | 6 | [1,1,1] | 0 |
| (1,1,1) | 4 | 2 | [2] | 0 |
| (1,1,2) | 6 | 2 | [2,2] | 0 |
| (1,1,3) | 8 | 2 | [2,2,2] | 0 |
| (1,1,4) | 10 | 2 | [2,2,2,2] | 0 |

F1 (singletons ≥ 1, cas comparable) : ✓ partout ; « tout léger porte son
singleton » : ✓ partout ; décomposition W = W_B + Σω + μ : ✓ partout.
**Fait structurel : μ = 0 sur TOUS les optima observés** — les témoins
comparables sont des lights purs (le poids extra est dans W_B, coefficient
croissant sur m_B) ; les témoins (1,1) sont des heavies purs (ω = 2).

## 2. Certificats hors preuve — 15/15 INFEASIBLE au cap = loi − 1

Comparable et (1,1) (zone o ≥ 3 où la preuve inconditionnelle s'arrêtait
avant MC-010, désormais couverte jusqu'à o ≤ 7 par le théorème B) :
(0,2,3) ν5 cap 7 ; (0,2,4) ν6 cap 9 ; (0,3,3) ν6 cap 8 ; (0,2,5) ν7
cap 11 ; (1,1,3) ν5 cap 7 ; (1,1,4) ν6 cap 9 ; (1,1,5) ν7 cap 11 —
tous INFEASIBLE.
Incomparables (zone entièrement hors preuve de minorant) : (1,2,2) ν5
cap 7 ; (1,2,3) ν6 cap 9 ; (2,2,2) ν6 cap 9 ; (1,3,2) ν6 cap 8 ;
(2,3,1) ν6 cap 8 ; (3,3,1) ν7 cap 9 ; (2,2,3) ν7 cap 11 ; (1,4,2) ν7
cap 9 — tous INFEASIBLE. [Assertions de solveur, réserve T27-S2 §4.]

## 3. L'inégalité de recouvrement — cartographie (k ≤ 40)

(d−1) + ⌈C(k,d)/C(k−2,d−2)⌉ ≥ k pour 2 ≤ d ≤ k :
**aucun échec pour k ≤ 7** ⟹ le théorème B (comparable inconditionnel)
vaut pour o ≤ 7. Échecs : k = 8 : d ∈ {5,6} ; k = 9 : {5..7} ;
k = 10 : {5..8} ; k = 11 : {5..9} ; k = 12 : {5..10} ; k = 13 : {5..11} ;
k = 14 : {6..12} ; k = 15 : {6..13}. Premier échec : **(k, d) = (8, 5)** —
la zone résiduelle exacte de la preuve.

## Réserves

- Certificats : INFEASIBLE de solveur, non ré-énumérables à ν ≥ 5.
- L'observation « μ = 0 sur tous les optima » porte sur 10 témoins —
  c'est un indice pour le lemme de normalisation, pas un théorème.
