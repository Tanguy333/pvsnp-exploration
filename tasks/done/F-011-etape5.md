# TÂCHE F-011, étape 5 : fenêtre glissante mod 3 — ✅ Lemme 2 validé + loi de l'obstruction collective confirmée

- **Type** : F (reformulation + test de loi)
- **Exécutée le** : 2026-06-10
- **Script** : [`checks/task_f011e5_sliding.py`](../../checks/task_f011e5_sliding.py)

## Lemme 2 (reformulation par différences finies — prouvé et cross-validé)

> Une fonction g : [0,n] → F₃ a un degré de Mahler ≤ d **ssi**
> `Δ^{d+1} g(j) ≡ 0 (mod 3)` pour tout j = 0..n−d−1.
> Donc `deg₃^sym(THR_{t,n}) ≤ d` ssi il existe une suite (0 sur [0,t),
> ±1 sur [t,n]) satisfaisant une contrainte **locale glissante** de
> largeur d+2 — décidable par automate fini (DP sur les d+1 dernières
> valeurs).

**Preuve** : base de Mahler standard (a_i = Δ^i g(0) ; degré ≤ d ⟺
différences d'ordre > d nulles, et sur une fenêtre finie il suffit de
l'ordre d+1 en tout point).
**Cross-validation** : DP ≡ solveur exact sur **126/126** cellules
(t ≤ 6, n ≤ 24, 0 désaccord).

## Loi de l'obstruction collective (C-F011e, confirmée sur 26 points conclus)

> `deg₃^sym(OR_n) = max( B_block(n), n − 3^⌊log₃ n⌋ )`

| n | 1-2 | 3-6 | 7 | 8 | 9-18 | 19 | 22 | 26 | ≥ 27 |
|---|---|---|---|---|---|---|---|---|---|
| deg₃ | 1 | 3 | 4 | 5 | 9 | 10 | 13 | 17 | ≥ 27 (blocage prouvé) |

Les deux rampes (n−3 pour n=7,8 ; **n−9 pour n=19..26**) collent point
par point. Le premier terme (blocage mono-poids) est déjà un théorème
(T-F011b) ; le second — le terme *collectif* qui manquait à l'étape 4 —
a maintenant une forme close confirmée.

## L'outil de preuve identifié (pour l'étape 6)

Sur F₃, Lucas donne `C(3^b, k) ≡ 0` sauf k ∈ {0, 3^b}, donc :

> **`Δ^{3^b} = S^{3^b} − id`** (S = décalage) — « degré < 3^b » ⟺
> « g est 3^b-périodique ».

Conséquences immédiates (esquisse d'étape 6) :
1. g a un préfixe de zéros et doit être ±1 sur [t, n] : la périodicité
   3^b force un zéro en t−1+3^b... → infaisabilité dès que la fenêtre
   contient un point à distance 3^b du préfixe — c'est une **re-preuve
   structurelle du blocage** aux puissances.
2. Pour d+1 = 3^b + r : `Δ^{d+1} = (S^{3^b} − id) ∘ Δ^r` — la contrainte
   devient « Δ^r g est 3^b-périodique ». Le terme n − 3^b de la rampe
   devrait suivre du comptage des périodes disponibles : c'est la cible
   de preuve précise pour clore C-F011e.

## État du fil F-011 après 5 étapes

| Acquis | Statut |
|---|---|
| Lemme 1 (noyau), T-F011a (mod 2 exact), T-F011b + anomalies, MAJ_32 = 27 | ✅ prouvés (étape 3) |
| Lemme 2 (fenêtre glissante, décision par automate) | ✅ prouvé + validé 126/126 (étape 5) |
| C-F011 (loi MAJ, 47/47) ; C-F011e (loi OR mod 3, 26/26) | 🔶 confirmées, preuves en cours |
| C-F011d (blocage exact partout) | ❌ réfutée (étape 4) — remplacée par blocage + terme collectif |
| Étape 6 (cible) | prouver C-F011e via la factorisation Δ^{3^b} = S^{3^b} − id |
