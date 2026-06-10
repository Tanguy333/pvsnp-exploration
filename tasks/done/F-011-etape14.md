# TÂCHE F-011, étape 14 : borne récursive CAND2 — ✅ 204/215 exacte, zéro violation

- **Type** : F (formalisation de la récursion + mesure d'écart)
- **Exécutée le** : 2026-06-10
- **Script** : [`checks/task_f011e14_recursion.py`](../../checks/task_f011e14_recursion.py)

## CAND2 (borne inférieure récursive — chaque ingrédient est un théorème du fil)

Pour P = 3^b, t ≤ P, P ≤ deg < 2P, n ≥ 2P + t, le 2e étage G = g(·+P) − g
est P-périodique, **non-nul sur tout [0, t)**, nul sur [t, n−2P] ; ses
obstructions : (i) interpolation (deg(G) ≥ n−2P−t+1) ; (ii) **témoins de
multiples** (z₁ non-nul, z₂ nul, Q | z₂−z₁ → deg(G) ≥ Q). Contribution :
`deg ≥ min(2P, P + max(i, ii))`. CAND2 = max(t, blocage, D-gen, ces
contributions).

## Résultats

- **Zéro violation** : CAND2 ≤ exact partout — la borne est saine (215
  cellules, t ≤ 10).
- **204/215 exactes (95 %)**. Écarts résiduels : 6 cellules à +1, 5 à +2
  — concentrés où la structure {1,2} *fine* des valeurs de G compte (le
  cas (2,24) analysé : les valeurs du préfixe de G sont contraintes à ±1,
  pas juste « non-nul », ce qui durcit l'interpolation d'un cran).
- **Table exacte complète publiée** (t ≤ 10, L ≤ 27) — la structure est
  visible : plateaux aux puissances, rampes, et les valeurs de 2e étage
  (12, 13, 14, 15, 18) = P + (rampe du problème réduit).

## Statut honnête

La loi exacte mod 3 du cas t général **est** l'automate (Lemme 2,
décidable) ; CAND2 en est l'approximation analytique prouvable à 95 %.
La fermeture des 11 cellules restantes demande l'interpolation à valeurs
contraintes ±1 — notée, non poursuivie ici.

## Suite (e15) : retour au mod 6 — l'hypothèse du sous-problème à trou

Dans la zone v2 (t = 33..40), U est morte par périodicité sur [64, n] :
la couverture y repose sur V seule. **Hypothèse H-v2** : deg₆ = min degré
d'un V mod 3 (zéros sous t) couvrant le trou [q₂, n] — sous-problème
« THR à trou » testable immédiatement contre les plateaux 40, 44, 46.
