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

## Prochain pas (lancé) — et son issue (e23)

Run CMS **4 h sur n = 12 seul** lancé (e23,
[`checks/task_f011e23_long_n12.py`](../../checks/task_f011e23_long_n12.py)).
**Issue : interrompu sans verdict** — le processus est mort en cours de
nuit (mise en veille machine / redémarrage de session), aucune ligne de
résultat. Pas un verdict du solveur.

## CLÔTURE DU FRONT DE CALCUL (2026-06-11)

**n = 12 et n = 13 sont classés « problème ouvert exécutable »** du
dépôt : `deg₆(MAJ_12) = 6 ?` et `deg₆(MAJ_13) = 7 ?` — instances
documentées (scripts e21c/e22 reproduisibles, encodage XOR-natif +
sym-break), résistantes à ~4 h cumulées sur 5 configurations.

Relance possible par l'utilisateur (machine sans veille, nuit complète) :
```
cd checks && python -X utf8 task_f011e23_long_n12.py
```
Sinon, la voie est **théorique** : n = 12 est le premier point 2t hors
Théorème K (t = 6 non puissance de 2 — la couverture mod 2 de e₆ meurt
sur [8, 11]) ; un argument d'infaisabilité ou une construction ad hoc
trancherait. Candidate de session future.
