# TÂCHE F-011, étape 24 : n = 12 ET n = 13 fermés par ansätze symétriques — ✅✅

- **Type** : F (voie structurelle — succès complet)
- **Exécutée le** : 2026-06-11
- **Scripts** : [`task_f011e24_ansatz_n12.py`](../../checks/task_f011e24_ansatz_n12.py),
  [`task_f011e24b_n13.py`](../../checks/task_f011e24b_n13.py),
  [`task_f011e24c_n13_multi.py`](../../checks/task_f011e24c_n13_multi.py)

## Les deux cellules tombent en 0 seconde chacune

| n | ansatz gagnant | solution | vérification |
|---|---|---|---|
| **12** | **S₆×S₆** (7 orbites, énumération exacte 280k) | **purement mod 3** : v_k = (1,1,1,2,1,1,1) — coefficient 1 partout, **2 sur les monômes équilibrés** | 4096 points ✓ |
| **13** | **S₄×S₄×S₅** (mini-SAT, 1re tripartition testée) | mixte u/v (orbites listées dans la sortie) | 8192 points ✓ |

> **deg₆(MAJ_12) = 6 et deg₆(MAJ_13) = 7 — l'hypothèse plate tient sur
> TOUS les points testés : n = 4..13, 16, 32.**

## La forme close de n = 12 (candidate à généralisation)

Par Vandermonde, la solution S₆×S₆ s'écrit :
> `V(S) = C(w, 6) + C(a, 3)·C(b, 3) (mod 3)` — e₆ corrigé par le terme
> des splits équilibrés. C'est l'extension du Théorème K au premier
> point 2t hors puissances de 2 : **candidate pour un « Théorème K′ »**
> (tout t pair ? mécanisme du terme correcteur à élucider).

## La leçon de méthode (en or)

| Approche | Coût | Verdict |
|---|---|---|
| SAT brut, 5 configurations (e20-22) | **~4,5 h** | INDÉCIS |
| run long 4 h (e23) | tué par la veille | — |
| **Ansatz symétrique** (e24) | **0 s + 0 s** | **les deux cellules fermées** |

Le CDCL ne voyait pas les orbites ; la solution vivait sur un sous-espace
invariant minuscule (7 variables pour n = 12 !). *Chercher la structure
avant le muscle.* — la même leçon que l'e21 (SAT vs recuit/ILP), un cran
plus haut. Contraste informatif : n = 12 a une solution bipartite très
symétrique, n = 13 exige une tripartition (symétrie plus basse) — les
6 bipartitions de n = 13 échouent toutes.

## Statut des « problèmes ouverts exécutables » d'e22

**Supersédés** : les deux cellules sont fermées (ce fichier).
L'hypothèse plate `deg₆(MAJ_n) = ⌈n/2⌉` reste une conjecture pour le cas
général, désormais sans aucun point d'ombre ≤ 13 — et la voie vers une
preuve générale passe par la généralisation de la forme close ci-dessus
(Théorème K′, candidate e25).
