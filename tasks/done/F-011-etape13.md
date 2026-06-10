# TÂCHE F-011, étape 13 : loi mod 3 du cas t général — ✅ F-gen/E-gen prouvés, loi à un étage incomplète, structure récursive identifiée

- **Type** : F (preuves + test de loi)
- **Exécutée le** : 2026-06-10
- **Script** : [`checks/task_f011e13_general_t.py`](../../checks/task_f011e13_general_t.py)

## Théorèmes prouvés (généralisation de la machinerie t = 1)

**Théorème F-gen (borne sup, chaînes).** Pour P = 3^b ≥ t et n < 2P + t :
`deg₃^sym(THR_{t,n}) ≤ P`, par la suite `(0^t, 1^P, 2^{reste})` — les
chaînes de résidus (0→1→2 pour les résidus du préfixe, 1→2 pour les
autres) donnent h ≡ 1 constante. **Vérifié** : P = 3, 9, 27, tout t ≤ P,
tout n < 2P+t — aucun échec.

**Théorème E-gen (rampe, borne inf).** Pour P ≤ deg < 2P et n ≥ 2P + t :
`deg₃^sym(THR_{t,n}) ≥ n − P − t + 1`. La chaîne descente → périodicité →
paires interdites → interpolation passe au t général via **l'invariance du
degré de Mahler par décalage** (G(t−1) ≠ 0, G ≡ 0 sur [t, n−2P], décaler
de t−1). Cas t = 1 = Théorème E. Aucune violation sur la grille.

## La loi à un étage est INCOMPLÈTE (225/246, 21 écarts)

`max(t, rampes D+E-gen, blocage)` sous-estime systématiquement en fenêtre
L = n−t+1 ∈ [19, 23] pour t ≥ 2 : valeurs vraies 12 et 15 (vs 10-14).

## Le diagnostic : la récursion de descentes

Cas (t=3, n=21), vrai = 12 = 9 + 3 : si deg ≤ 11, alors G = g(·+9) − g a
deg ≤ 2 < 3, donc G est **3-périodique** ; or G(3) = 0 (paires interdites)
et G(0) = g(9) ≠ 0, positions séparées par 3 — contradiction. Donc
deg ≥ 9 + 3 = 12. ✓ (explique l'écart exactement)

> **La vraie loi mod 3 est un escalier de descentes base 3** : chaque
> descente (soustraire P) produit un problème réduit qui a ses propres
> zéros forcés et ses propres obstructions de périodicité — la loi à un
> étage ne capture que la première marche. Candidate structurelle : une
> récursion deg(t, n) = P + deg'(problème réduit), à formuler proprement.

## État

- **Prouvé aujourd'hui** : F-gen, E-gen (+ vérifications massives).
- **Réfuté aujourd'hui** : la loi à un étage (3e conjecture du fil tuée
  le jour de sa formulation — le pipeline tourne).
- **e14 (candidate)** : formaliser la récursion de descentes (l'analyse
  (3, 21) donne le gabarit : périodicité au 2e étage) et tester la loi
  récursive sur la grille ; puis composition mod 6 pour expliquer les
  plateaux 36, 40, 44, 46 de l'étape 12.
