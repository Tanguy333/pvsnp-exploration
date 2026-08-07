# MC-009 — Données : réfutation de C-MC008, loi corrigée C-MC009, témoins et constructions

> Produit par `checks/mc009_preuve_F.py` (modes temoins, confirme,
> reduction, constructions) + `checks/mc009_regles.py`, 2026-08-07.
> Cœurs m = 0 : A = support propre de u (|A| = a), B = support propre de
> v (|B| = b ≥ a), O = dehors (|O| = o) ; points u = A, v = B (u = 0-point
> si a = 0). W exact : CP-SAT OPTIMAL, témoins re-vérifiés.

## 1. LA RÉFUTATION de C-MC008 (branche incomparable)

Trois points hors de la plage d'ajustement (qui était a ≤ 2, imposé par
ν ≤ 5) :

| point | C-MC008 prédisait | F mesuré (OPTIMAL) |
|---|---|---|
| (a=3, b=3, m=0, o=0), ν=6 | 9 | **8** |
| (a=3, b=4, m=0, o=0), ν=7 | 10 | **9** |
| (a=3, b=3, m=0, o=1), ν=7 | 11 | **10** |

Témoin de (3,3,0,0), poids 8, en signatures (|S∩A|, |S∩B|, |S∩O|) :
{(3,0,0): [1], (0,3,0): [1], (2,1,0)... [ligne complétée par VER-MC-1 :
le profil complet est {(0,3,0): [1], (1,3,0): [1,1,1], (3,0,0): [1],
(3,1,0): [1,1,1]}] — exactement la construction COURONNE :
m_A + m_B + les trois m_{A∪{j}} + les trois m_{B∪{i}}, poids a + b + 2 = 8.
**Le mécanisme** : la couronne bat la branche linéaire 2a + b dès a ≥ 3 ;
toutes les données d'ajustement de C-MC008 avaient a ≤ 2, où
couronne ≥ linéaire. Cinquième prise q.12 du fil (deuxième interne).

## 2. La loi corrigée C-MC009

- **Cœur comparable** (a = 0, b ≥ 2) : F = b + 2o.
- **Cœur incomparable** (1 ≤ a ≤ b) :
  **F = 2(a+b+o) − max(b, 2, a+b−2)** — de façon équivalente :
  (1,1) : 2 + 2o ; a = 1, b ≥ 2 : 2 + b + 2o (branche linéaire) ;
  a ≥ 2 : min(2a+b, a+b+2) + 2o, la couronne prenant le dessus dès a ≥ 3.
- Hors cœurs : la RÉDUCTION M (prouvée, fiche §2) ramène tout (a, b, m, o)
  au cœur sur ν − m variables, avec +1 à la transition comparable
  m = 1 → 0.

### Points de contrôle NEUFS (tous hors plage d'ajustement de C-MC008)

| point | ν | C-MC009 | mesuré |
|---|---|---|---|
| (1,5,0) | 6 | 7 | **7** ✓ |
| (3,3,1) | 7 | 10 | **10** ✓ (discriminant : C-MC008 disait 11) |
| (3,4,0) | 7 | 9 | **9** ✓ (discriminant : 10) |
| (2,5,0) | 7 | 9 | **9** ✓ |
| (1,5,1) | 7 | 9 | **9** ✓ |
| (1,6,0) | 7 | 8 | **8** ✓ |
| (2,4,1) | 7 | 10 | **10** ✓ |

7/7 conformes, dont 2 discriminants. Avec les 27 témoins de cœurs ν ≤ 6
(tous conformes une fois la loi corrigée) et la table exhaustive ν ≤ 4 de
MC-008 : **C-MC009 est conforme à TOUTE la donnée disponible (ν ≤ 7,
a ≤ 3, b ≤ 6)**. Statut : CONJECTURE pour les minorants ; les MAJORANTS
sont PROUVÉS (§4 de la fiche) — C-MC009 est donc une borne supérieure
démontrée, et une valeur exacte certifiée-solveur sur tout ν ≤ 7 testé.

## 3. La réduction M — vérification numérique

`reduction` : F(a,b,m,o) = F(a,b,0,o; ν−m) + [a = 0]·[m ≥ 1] vérifié sur
TOUTE la grille ν ≤ 5 (0 écart) — en plus de la preuve papier (fiche §2).

## 4. Les trois constructions générales (majorants) — vérifiées par blocs

`constructions` (+ `mc009_regles.py`) : évaluation par comptages de blocs
sur la grille a, b ≤ 8, o ≤ 8 — **toutes séparantes, toutes exactement au
poids C-MC009** ((1,1) traité à part : témoins directs ν ≤ 5).

| construction | poids | domaine |
|---|---|---|
| comparable : p = Σ_{i∈B∪O} y_i + o·m_B | b + 2o | b ≥ 2 (b = 1 : G fait mieux) |
| linéaire : p = y_A + m_B + Σ_j m_{A∪{j}} + Σ_l (m_{A∪{l}} + m_{B∪{l}}) | 2 + b + 2o | a = 1, b ≥ 2 |
| couronne : p = m_A + m_B + Σ_j m_{A∪{j}} + Σ_i m_{B∪{i}} + Σ_l (m_{A∪{l}} + m_{B∪{l}}) | a + b + 2 + 2o | a, b ≥ 1 |

## 5. Témoins des cœurs (ν ≤ 6, extraits en signatures)

Sortie complète du mode `temoins` archivée dans le run du 2026-08-07 ;
faits saillants : les témoins comparables sont exactement la construction
comparable (coefficient o sur m_B — la « pénalité de collision » croît
avec le dehors) ; les témoins a = 1 sont exactement la construction
linéaire ; (2,2) réalise la couronne = linéaire (égalité des branches à
a = 2) ; (1,1,o) casse la bloc-symétrie (un singleton O à coefficient 2).

## Réserves

- Minorants : OUVERTS au-delà des certificats solveur (ν ≤ 7) et du
  minorant-singletons du comparable (W ≥ ν, prouvé) — c'est la cible
  restante ; l'esquisse de cascade a un trou identifié (les familles
  D_j intérieures ne sont pas disjointes) et n'est PAS revendiquée.
- C-MC009 ajustée sur a ≤ 3, b ≤ 6, o ≤ 3 : deux conjectures sont déjà
  mortes hors plage dans ce fil — le statut CONJECTURE n'est pas une
  formalité.
- Optima ν ≥ 5 : assertions de solveur (réserve T27-S2 §4).
