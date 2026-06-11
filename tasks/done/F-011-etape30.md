# TÂCHE F-011, étape 30 : la frontière bipartite — ✅ loi « 3-lisses ∪ {5} »

- **Type** : F (données)
- **Exécutée le** : 2026-06-11
- **Script** : [`checks/task_f011e30_frontier.py`](../../checks/task_f011e30_frontier.py)

## La table complète (t = 2..20, solvabilité bipartite à n = 2t)

| verdict | t |
|---|---|
| **solubles** | 2, 3, 4, 5, 6, 8, 9, 12, **16, 18** |
| **insolubles** | 7, 10, 11, 13, **14, 15, 17, 19, 20** |

> **Loi raffinée (conjecture v2)** : soluble ⟺ **t = 2^a·3^b (3-lisse)
> OU t = 5** (exception sporadique). 19/19 points conformes. Lecture
> par facteurs : *tout multiple de 5 ou 7 casse* (10, 14, 15, 20 —
> alors que 5 seul passe), les purs {2,3}-produits passent tous.

Détails de structure : t = 16 → presque toutes les tailles \|A\|
marchent **sauf 12** ; t = 18 → \|A\| ∈ [9, 18] (moitié et plus).

## Conséquence sur la plate

Les n = 2t insolubles en bipartite (28, 30, 34, 38, 40) ne sont **pas
encore fermés** (notre vérification plate s'arrête à n = 24) — les
multipartitions y seront nécessaires (comme pour 13, 14, 19..22).
La plate reste confirmée n = 4..24 + 32 ; statut n = 26..40 : à faire.

## Prédictions falsifiables (e31 candidate)

t = 24 (3-lisse) → soluble ; t = 25 = 5² → **insoluble** (l'exception 5
ne devrait pas se propager) ; t = 27 = 3³ → soluble, \|A\| = 1.
