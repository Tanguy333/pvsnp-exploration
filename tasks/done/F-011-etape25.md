# TÂCHE F-011, étape 25 (+25b) : la machine à ansätze — ✅ plate confirmée jusqu'à n = 20, certificats doublement vérifiés

- **Type** : F (balayage constructif + re-vérification indépendante)
- **Exécutée le** : 2026-06-11
- **Scripts** : [`task_f011e25_ansatz_machine.py`](../../checks/task_f011e25_ansatz_machine.py),
  [`task_f011e25b_reverify.py`](../../checks/task_f011e25b_reverify.py)

## e25 — toutes les cellules n = 14..20 tombent (0 s chacune)

| n | t | partition gagnante | structure |
|---|---|---|---|
| 14 | 7 | (2,5,7) — tripartition | mixte, 12+15 orbites |
| 15 | 8 | (7,8) — 1re bipartition | mixte 8+8 |
| 16 | 8 | (8,8) — 1re bipartition | mixte 7+9 |
| 17 | 9 | (8,9) — 1re bipartition | mixte 9+9 |
| 18 | 9 | (9,9) — 1re bipartition | mixte 10+10 |
| 19 | 10 | (3,7,9) — tripartition | mixte 17+22 |
| 20 | 10 | (4,7,9) — tripartition | mixte 26+29 |

> **L'hypothèse plate `deg₆(MAJ_n) = ⌈n/2⌉` est confirmée sur TOUT
> n = 4..20, plus 32.** Pattern net : t proche d'une puissance de 2
> (8, 9) → la première bipartition suffit ; les points durs (t = 7, 10,
> les 2t-anomalies) exigent des **tripartitions** — la symétrie requise
> baisse avec la distance aux puissances.

Vérification e25 : **par profils** (rigoureuse — l'invariance est par
construction). Note : CaDiCaL émet des messages « found falsified
original clause » (simplification d'entrée, anodins) ; la validité des
solutions repose sur nos vérifications, pas sur le statut SAT seul.

## e25b — re-vérification indépendante (demande utilisateur)

| Cellule | Chemins indépendants | Verdict |
|---|---|---|
| **n = 12** | identité de Vandermonde (49 profils) + couverture profils + **4096 points avec coïncidence forme close ↔ somme monomiale** | ✅✅ |
| **n = 13** | re-résolution fraîche (4,4,5) + **évaluateur réécrit** (masques de bits), 8192 points | ✅✅ |
| **n = 14** | re-dérivation (2,5,7) + **point-par-point 16384 points** (e25 n'avait que les profils) | ✅✅ |

La forme close de n = 12 est ainsi **établie** :
`V(S) = C(w,6) + C(a,3)·C(b,3) (mod 3)` — zéros sous 6 et couverture
sur [6, 12], identique à la somme monomiale en chaque point.

## Note pour le Théorème K′ (consignée)

Le K′ naïf (`C(w,t) + C(a,t/2)C(b,t/2)`) est **réfuté** hors t ∈ {2, 6} :
échoue à t = 4 (profil (4,2) : 21 ≡ 0) et t = 10 (profil (10,2) :
C(12,10) = 66 ≡ 0). La vraie généralisation devra épouser le pattern
bipartition/tripartition ci-dessus — question ouverte structurée, avec
8 certificats explicites comme données.
