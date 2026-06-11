# TÂCHE F-011, étape 31 : prédictions t = 21..27 — ❌ loi v2 réfutée par t = 24

- **Type** : F (test de prédictions — issue : réfutation instructive)
- **Exécutée le** : 2026-06-11
- **Script** : [`checks/task_f011e31_predictions.py`](../../checks/task_f011e31_predictions.py)

## Verdicts

| t | prédiction (3-lisses ∪ {5}) | observé | |
|---|---|---|---|
| 21, 22, 23, 26 | insolubles | insolubles | ✓ |
| **25 = 5²** | insoluble (exception non propagée) | **insoluble** | ✓ |
| **24 = 2³·3** | soluble | **INSOLUBLE** | ✗ **contre-exemple** |
| 27 = 3³ | soluble | soluble (\|A\| = 1..5) | ✓ |

**7e conjecture du dépôt tuée le jour de sa formulation.**

## La lecture corrigée (table complète t = 2..27)

> Solubles : **{2, 3, 4, 5, 6, 8, 9, 12, 16, 18, 27}** ;
> insolubles : {7, 10, 11, 13, 14, 15, 17, 19, 20, 21, 22, 23, **24**, 25, 26}.

La solvabilité bipartite à n = 2t se confine aux **familles de nos
théorèmes** — {2^a} (Théorème K), {2·3^b} (Théorème K′), {3^b} — plus
deux sporadiques (5 et 12, tous deux à formes closes établies). t = 24 =
2³·3 casse alors que 12 = 2²·3 passe : même « 2^a·3 » n'est pas une
famille. **En grandissant, être bipartite-soluble est l'exception** —
la complexité arithmétique de t pousse vers les multipartitions.

## Prédictions restantes (e32 candidates, non engagées)

t = 32 = 2⁵ → soluble (K) ; t = 36 = 4·9 → ? (départage « 4·3^b » vs
sporadique 12) ; t = 54 = 2·27 → soluble (K′). La famille {3^b} mérite
son théorème (« K″ pour 3^b » : 27 soluble avec \|A\| = 1 — la
construction mono-bloc à élucider, candidate e32).
