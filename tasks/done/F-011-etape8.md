# TÂCHE F-011, étape 8 : bornes supérieures — ✅ Théorème F + loi du régime 1 EXACTE

- **Type** : F (preuve + extraction de témoins)
- **Exécutée le** : 2026-06-10
- **Script** : [`checks/task_f011e8_upper.py`](../../checks/task_f011e8_upper.py)

## Théorème F (construction explicite)

> Pour P = 3^b et P ≤ n ≤ 2P, la suite `g = (0, 1^P, 2^{n−P})` vérifie
> `g(j+P) − g(j) ≡ 1` (constante) sur [0, n−P], donc deg(g) ≤ P.

**Preuve** : h(0) = g(P) − g(0) = 1 ; pour j ∈ [1, n−P] (donc j ≤ P et
j+P ≥ P+1) : h(j) = 2 − 1 = 1. Δ^{P+1}g = Δh ≡ 0. ∎
Vérifié pour P = 3, 9, 27 et tout n ∈ [P, 2P].

**Corollaire (avec Théorème D) — première loi de régime entièrement
prouvée** :

> `deg₃^sym(OR_n) = 3^b` **exactement**, pour tout n ∈ [3^b, 2·3^b].

## Témoins de la rampe (régime 2, vers la borne sup générale)

Témoins extraits par DP à d = n−P exactement :

| n | g (témoin) | h = g(·+9) − g | deg(h) | borne r = n−2P |
|---|---|---|---|---|
| 19 | 01121121121211211211 | 20120120120 | **1** | 1 |
| 20 | 011111111111211211211 | 100100100100 | **2** | 2 |
| 22 | 01111121211111211121111 | 10000120210000 | **4** | 4 |

`deg(h) = r` **exactement** — la chaîne de la preuve du Théorème E est
serrée à chaque maillon, et les h extraits montrent des structures
3-périodiques (201201…, 100100…) : la construction générale de la rampe
(borne sup pour tout n) semble être « h 3-périodique de degré r » —
candidate précise pour clore la loi OR mod 3, non prouvée ici.

## Certificats MAJ mod 6 (bornes sup des anomalies)

- `MAJ_16, d=9` : **V = e₈ + e₉ (mod 3)** — validé sur les 17 poids.
- `MAJ_4, d=3` : **V = e₂ + e₃ (mod 3)** (u = 0) — trouvé et validé.
- (Rappel n=32, d=27 : e₁₆+e₁₈+e₂₅+e₂₇, étape 3.)

**Pattern émergent** : les anomalies t = 2^a se résolvent par des sommes
d'élémentaires *consécutives* purement mod 3 (e_t + e_{t+1} pour les deux
premières ; structure plus riche à la 3e). Candidate : le certificat
général d'anomalie est mod-3 pur — à prouver pour clore C-F011.

## État du fil (8 étapes)

**9 théorèmes prouvés** (+ Théorème F et son corollaire de régime).
Restent : la borne sup de la rampe (construction 3-périodique, candidate
identifiée) et la loi MAJ générale (certificats mod 3 purs, pattern
identifié). Le modèle symétrique composite est aux trois quarts résolu.
