# TÂCHE F-011, étape 27 : extension n = 21..24 + dissection tripartite — ✅/📊

- **Type** : F (données + extension)
- **Exécutée le** : 2026-06-11
- **Script** : [`checks/task_f011e27_tripartite_data.py`](../../checks/task_f011e27_tripartite_data.py)

## [A] La plate s'étend à n = 24

| n | t | partition | structure |
|---|---|---|---|
| 21 | 11 | **(3,5,5,8)** — quadripartition | 78+100 orbites |
| 22 | 11 | **(4,5,5,8)** — quadripartition | 91+118 |
| 23 | 12 | (8,15) — bipartition | 8+7 (creuse) |
| 24 | 12 | (7,17) — bipartition | **3+8 (très creuse)** |

> **`deg₆(MAJ_n) = ⌈n/2⌉` confirmé sur tout n = 4..24, plus 32.**
> Gradient de symétrie affiné : t = 11 exige des quadripartitions
> (4 niveaux : bi → tri → quadri en montant les t mixtes) ; t = 12
> retombe sur des bipartitions à solutions très creuses.

## [B] Dissection des certificats tripartites — la limite identifiée

Tables d'orbites complètes dumpées pour (13,(4,4,5)), (19,(3,7,9)),
(20,(4,7,9)). **Enseignement** : les solutions SAT sont *non
canoniques* — points arbitraires d'un espace de solutions, 13 à 30
orbites actives sans motif lisible. Le motif de n = 12 n'était
déchiffrable que parce que l'espace S₆×S₆ (7 orbites) était quasi
forcé. **Le pattern-mining sur du bruit SAT ne donnera pas K″.**

## La voie pour la suite (e28 candidate)

**Certificats minimaux par MaxSAT** (clauses souples ¬u_o, ¬v_o,
minimiser le support) : les solutions creuses — comme le 3+8 de
n = 24 — sont celles où la structure se lit. Cible : re-résoudre les
cellules t mixtes en minimisant, puis relire les formes closes.
