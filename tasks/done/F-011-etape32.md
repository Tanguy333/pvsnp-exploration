# TÂCHE F-011, étape 32 : THÉORÈME K″ + stratification — ✅ la classification de la frontière est complète (t ≤ 27)

- **Type** : F (théorème + classification)
- **Exécutée le** : 2026-06-11
- **Script** : [`checks/task_f011e32_kseconde.py`](../../checks/task_f011e32_kseconde.py)

## Théorème K″ (troisième famille infinie)

> Pour t = 3^k, n = 2t : **V = e_t (mod 3)** est une représentation
> faible **symétrique** de THR_{t,2t} — deg₆ = t.
> **Preuve (une ligne de Lucas)** : pour w ∈ [t, 2t], le digit de
> position k de w en base 3 vaut 1 ou 2, donc C(w,t) ≡ C(digit, 1) ∈
> {1, 2} ≢ 0 mod 3. ∎

Vérifié k = 0..5 (jusqu'à n = 486). C'est le théorème le plus simple
du fil — t = 3^k n'est même pas un point d'anomalie (le mod 3 ne meurt
jamais sur la fenêtre).

## La stratification (vérifiée t = 2..27, `sym ⇒ bipartite` sans exception)

| Strate | t solubles | Explication |
|---|---|---|
| symétrique pure mod 3 | {3, 9, 27} = 3^b | **Théorème K″** |
| symétrique jointe | {4} | e_t, couverture croisée des moduli |
| quasi-symétrique | {8, 16} (2^a) | **Théorème K** (e_t mod 2 + 1 monôme) |
| correction centrale | {2, 6, 18} (2·3^b) | **Théorème K′** |
| sporadiques | {5, 12} | formes closes établies (e29) |
| **insolubles** | tout le reste ≤ 27 | multipartitions nécessaires |

> **Chaque t bipartite-soluble (t ≤ 27) a désormais un théorème ou une
> forme close explicite.** La frontière bipartite est *classifiée* —
> trois familles infinies (K, K′, K″) + un point joint + deux
> sporadiques. La question résiduelle du fil : les certificats
> multipartites des t insolubles (7, 10, 11, …) et la plate au-delà de
> n = 24.

## Note de strate

t = 2 n'est PAS symétrique-soluble (C(4,2) = 6 ≡ 0 mod 6 — l'anomalie
historique) mais est bipartite-soluble (K′, k = 0) : la hiérarchie
sym ⊊ bipartite est stricte dès t = 2.
