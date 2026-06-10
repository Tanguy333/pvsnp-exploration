# TÂCHE F-011, étape 6 : théorème de périodicité + lemme de descente — ✅ PROUVÉS

- **Type** : F (preuve)
- **Exécutée le** : 2026-06-10
- **Script** : [`checks/task_f011e6_periodicity.py`](../../checks/task_f011e6_periodicity.py)

## Théorème T-F011c (périodicité vs préfixe)

> Pour toute puissance `P = 3^b ≤ n − t + 1` :
> `deg₃^sym(THR_{t,n}) ≥ P`. En particulier
> `deg₃^sym(OR_n) ≥ 3^⌊log₃ n⌋`.

**Preuve.** Sur F₃, Lucas donne `C(P,k) ≡ 0` pour 0 < k < P, et P est
impair, donc **`Δ^P = S^P − id`** (identité vérifiée exécutablement,
150/150 fenêtres aléatoires, P = 3, 9, 27). Si deg(g) ≤ d < P, alors
Δ^P g ≡ 0 sur [0, n−P] (toute différence d'ordre > d s'annule), donc g
est P-périodique sur son domaine. Or g(t−1) = 0 (préfixe) et, dès que
t−1+P ≤ n, la périodicité force `g(t−1+P) = 0` — qui doit pourtant être
dans {1, 2} (fenêtre de couverture). Contradiction. ∎

**Vérification** : aucune violation sur les 138 valeurs exactes (DP,
t ≤ 6, n ≤ 26).

## Lemme 3 (descente)

> Si deg(g) ≤ d et P = 3^b ≤ d+1, alors `G := g(·+P) − g` a un degré de
> Mahler ≤ d − P sur [0, n−P].

**Preuve.** `Δ^{d+1−P} G = Δ^{d+1−P}(S^P − id)g = Δ^{d+1−P} Δ^P g
= Δ^{d+1} g ≡ 0`. ∎

**Vérification** : 2000/2000 fonctions aléatoires de bas degré (P = 3, 9).

## Ce que ça donne, et ce qui manque encore

- T-F011c **re-prouve structurellement** le blocage aux puissances (la
  partie de T-F011b correspondant à w = puissance de 3) par un argument
  *dynamique* (périodicité) plutôt que combinatoire (annulation de
  binômes) — deux preuves indépendantes du même mur.
- Lemme 3 est l'**outil de récurrence** : il transporte toute borne sur le
  problème réduit (G = différence décalée, fonction F₃ générale avec
  G(0) ≠ 0) en borne +P sur le problème initial. La rampe exacte
  (`deg₃(OR_n) = n − 3^b` pour 2·3^b < n < 3^{b+1}, confirmée 26/26)
  demande de borner le problème réduit — **encore conjecturale** : G perd
  la structure ±1 (valeurs dans tout F₃), et l'argument fin n'est pas
  encore trouvé. Dit tel quel.

## Tableau de bord du fil F-011 (6 étapes)

| # | Énoncé | Statut |
|---|---|---|
| 1 | Lemme 1 (noyau de Mahler) | ✅ prouvé |
| 2 | T-F011a (forme close exacte mod 2, famille THR) | ✅ prouvé |
| 3 | T-F011b (infaisabilité mod 6) + 3 anomalies | ✅ prouvé |
| 4 | deg₆^sym(MAJ_32) = 27 | ✅ prouvé |
| 5 | Lemme 2 (fenêtre glissante / automate) | ✅ prouvé + 126/126 |
| 6 | T-F011c (périodicité) | ✅ prouvé + 138/138 |
| 7 | Lemme 3 (descente) | ✅ prouvé + 2000/2000 |
| — | C-F011 (loi MAJ, 47/47) ; C-F011e (rampe OR mod 3, 26/26) | 🔶 conjectures étayées |
| — | C-F011d | ❌ réfutée |
