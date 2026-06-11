# TÂCHE F-011, étape 33 : plate n = 25..31 + départage t = 36 — ✅/⚠ mixte

- **Type** : F (extension + test de prédiction)
- **Exécutée le** : 2026-06-11
- **Script** : [`checks/task_f011e33_plate_25_31.py`](../../checks/task_f011e33_plate_25_31.py)

## [A] La plate : 3 cellules neuves fermées, 4 à la limite de l'outil

| n | t | verdict |
|---|---|---|
| 25 | 13 | ✅ fermé — quadripartition (3,5,8,9), 13 s |
| 29 | 15 | ✅ fermé — quadripartition (3,3,8,15), 49 s |
| 31 | 16 | ✅ fermé — bipartition (15,16) instantanée (famille K) |
| **26, 27, 28, 30** | 13-15 | ⚠ **OUVERTS** — 268-318 partitions essayées, limite du catalogue (orbites ≤ 220, ≤ 5 parts, 300 s) |

> **Plate confirmée : n = 4..25, 29, 31, 32.** Trous restants : 26, 27,
> 28, 30 — *frontière d'outil* (pas de verdict), candidates pour un
> catalogue élargi (parts ≥ 6, orbites > 220) ou des techniques neuves.
> Pattern persistant : les 2t-points des t insolubles (13, 14, 15)
> sont les plus durs.

## [B] t = 36 = 4·9 : INSOLUBLE — le sporadique 12 est confirmé isolé

Les 36 bipartitions de n = 72 échouent toutes (1 s). **Il n'y a pas de
famille {4·3^b}** : la classification d'e32 est stable —
solubles = {2^a} ∪ {3^b} ∪ {2·3^b} ∪ sporadiques {5, 12}, et les
sporadiques n'engendrent pas de familles (5² et 4·9 cassent tous deux).
