# TÂCHE F-011, étape 22 : cassage de symétrie pour n = 12, 13 — ⚠ INDÉCIS (consigné)

- **Type** : F (escalade d'outils — issue : non conclu, documenté)
- **Exécutée le** : 2026-06-11
- **Script** : [`checks/task_f011e22_symbreak.py`](../../checks/task_f011e22_symbreak.py)

## Ce qui a été tenté

Encodage XOR-natif (CMS) + **cassage de symétrie** : négation globale
mod 3 (v_{T₀} ≠ 2) et lex-leader `X ≤lex σ(X)` pour les n−1
transpositions adjacentes (bits u/v1/v2 des monômes déplacés, encodage
par préfixes égaux — relaxation saine). Budget 2400 s/instance.

## Verdict : INDÉCIS sur les deux instances

Le lex-leader sur transpositions adjacentes ne casse qu'une fraction de
S_n (|S_12| ≈ 4,8·10⁸) — insuffisant à ce budget.

## Bilan cumulé de la frontière n = 12, 13

| Outil | n = 12 | n = 13 |
|---|---|---|
| Recuit (e19/20) | échec | échec |
| ILP CBC (e20) | timeout | — |
| CaDiCaL (e21) | 36+45 min, rien | ~13 min, rien |
| CMS + Gauss (e21c) | 40 min, rien | 40 min, rien |
| CMS + Gauss + sym-break (e22) | 40 min, rien | 40 min, rien |

**~3,5 h cumulées, cinq configurations** — c'est une vraie frontière.
Escalades restantes : run long (heures), BreakID complet, ou théorie
(n = 12 = premier point 2t hors Théorème K : t = 6 n'est pas une
puissance de 2, la couverture mod 2 de e₆ meurt sur [8, 11]).

## Prochain pas (lancé)

Run CMS **4 h sur n = 12 seul** (la cellule décisive). Si toujours
INDÉCIS : la cellule rejoint le statut « problème ouvert exécutable »
(comme l'e20 avant le déblocage SAT) — et la voie redevient théorique.
