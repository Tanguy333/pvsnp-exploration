# TÂCHE F-011, étape 19 : plate n = 10..13 (non conclu) + Théorème L (modèle fort)

- **Type** : F (sonde + bookkeeping théorique)
- **Exécutée le** : 2026-06-10
- **Script** : [`checks/task_f011e19_flat_strong.py`](../../checks/task_f011e19_flat_strong.py)
- **Incident consigné** : le cross-check de la forme close avait un bug
  (AND au lieu de OR pour « ≢ 0 mod 6 ») — corrigé, OK après correction.

## (a) Hypothèse plate à n = 10..13 — NON CONCLU (honnête)

Le recuit sous l'ansatz `u ≡ 1` (seul V cherché) **cale** : coûts
résiduels 42 (n=10), 28 (n=11), 180 (n=12), 756 (n=13). Deux limites
méthodologiques identifiées :
1. **L'ansatz est une restriction** — u asymétrique mod 2 pourrait
   réduire W_fail ; la recherche jointe (u, v) n'a pas été faite.
2. À n = 10 et 13 le système est **surcontraint** (266 vs 252 ; 2380 vs
   1716) — l'infaisabilité à degré t est plausible.

**Statut de l'hypothèse plate** : confirmée à n ≤ 9 et aux familles
d'anomalie (Théorème K : 16, 32) ; **indécise** à n = 10..13 — peut-être
fausse hors points spéciaux. La décision exacte exige mieux que le recuit
(2^252 × 3^252 hors énumération).

## (b) Théorème L (le modèle FORT expédié)

> Le polynôme multilinéaire représentant *exactement* une fonction
> booléenne sur Z_m est **unique** (Möbius). Pour MAJ_n :
> `deg_m^fort(MAJ_n) = max{k ≤ n : C(k−1, t−1) ≢ 0 (mod m)}`, et par CRT
> **`deg₆^fort = max(deg₂^fort, deg₃^fort)`** (vérifié n ≤ 40, forme
> close Lucas-OR vérifiée).

**La surprise de la table** : le modèle fort a des **chutes réelles** —
`deg₆^fort(MAJ_15) = 9 < 15` : MAJ_15 est *calculée exactement* par un
polynôme de degré 9 sur Z₆ (et MAJ_10..14 par degré 9 aussi). Le modèle
fort n'est pas « plein » : 22/39 valeurs de n ≤ 40 ont une chute.

## La photographie des trois modèles (bilan de la journée générale)

| Modèle mod 6 (MAJ) | Comportement | Statut |
|---|---|---|
| **Fort** (unique) | max(mod 2, mod 3), chutes réelles (15 → 9) | ✅ Théorème L, forme close |
| **Faible général** | plat = t aux points testés (n ≤ 9, 16, 32) ; indécis n = 10..13 | 🔶 hypothèse |
| **Faible symétrique** | riche (puissances, anomalies, répunits) | ✅ cartographié (15 étapes) |

La structure composite intéressante vit **entre** fort et faible — c'est
la conclusion de zone qui aiguille la suite (modèles à valeurs prescrites
partielles, approximations probabilistes = le vrai Pas-1 manquant).
