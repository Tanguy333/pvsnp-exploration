# TÂCHE F-011, étape 11 : sondage n = 65 — ❌ **C-F011 RÉFUTÉE** (et une valeur exacte nouvelle)

- **Type** : F (test adverse de conjecture — issue : réfutation)
- **Exécutée le** : 2026-06-10
- **Script** : [`checks/task_f011e11_probe65.py`](../../checks/task_f011e11_probe65.py)

## La logique du sondage

L'étape 10 a prouvé C-F011 sur n ∈ [2, 40] via H + I + J. En préparant la
clôture tout-n (e11), l'analyse du lemme d'existence du témoin J a révélé
un **régime sans témoin** : pour t = 33..40 (n = 65..80, q₂ = 64,
q₃ = 81), tout w ∈ [64, 80] a digit₂₇ = 2, donc 54 = (2,0,0,0)₃ est un
sous-ensemble de Lucas — `C(w, 54) ≢ 0 mod 3` partout. À n = 65, les
témoins Lucas-morts ne couvrent que d ≤ 35 (vérifié bloc [A]). La borne
inférieure de C-F011 au-delà n'avait **aucune preuve**, et la loi n'avait
**jamais été mesurée** dans ce régime (données : n ≤ 44).

## Verdict (bloc [B], énumération CRT complète)

| d | 33..39 | **40** |
|---|---|---|
| faisabilité | infaisable (exhaustif) | **FAISABLE** |

> **`deg₆^sym(MAJ_65) = 40`** — exactement (les deux côtés par énumération
> complète). C-F011 prédisait 64. **RÉFUTÉE.**

## La valeur vraie est parlante

**40 = 1 + 3 + 9 + 27 = (3⁴−1)/2** — le répunit en base 3 (digits
(1,1,1,1)₃). La vraie loi du régime fait intervenir des demi-sommes de
puissances de 3, pas seulement des puissances : la structure est plus
riche que C-F011. (Forme déjà croisée ailleurs dans le dépôt — (3^k−1)/2
de L18/T-F006 — probablement une coïncidence de forme, à ne pas
surinterpréter.)

## Ce qui survit, ce qui meurt

| Énoncé | Statut |
|---|---|
| Théorème H (deg ≤ L1) | ✅ tient (borne sup vraie — mais **pas serrée** dans le nouveau régime : 40 < 64) |
| Théorème I (deg ≥ L1 si n ≥ max(q₂,q₃)) | ✅ tient (le régime de 65 n'y est pas) |
| Théorème J (témoins par cellule, n ≤ 26) | ✅ tient |
| Anomalies (MAJ_4 = 3, MAJ_16 = 9, MAJ_32 = 27) | ✅ tiennent (prouvées des deux côtés) |
| **C-F011 comme loi générale** | ❌ **réfutée à n = 65** — artefact du domaine d'ajustement n ≤ 44 |

## Leçons

1. **Le pipeline adverse fonctionne dans les deux sens** : la même session
   a prouvé la loi sur son domaine et l'a tuée hors domaine — en ciblant
   *précisément* le régime où sa preuve ne s'étendait pas. C'est la
   deuxième conjecture du fil (après C-F011d) tuée par le test du
   « pourquoi la preuve ne passe-t-elle pas ? ».
2. La question vraie reste ouverte et s'enrichit : **quelle est la loi
   exacte de deg₆^sym(MAJ_n) ?** Nouvelle donnée dure : MAJ_65 = 40 =
   (3⁴−1)/2. Cible suivante naturelle : mesurer le régime t = 33..40
   complet (n = 66..80, d ≤ ~45 par paires CRT) et chercher la loi
   corrigée — avec cette fois le réflexe de sonder d'abord les régimes
   sans preuve.
