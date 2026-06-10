# TÂCHE F-011, étape 15 : hypothèse H-v2 (sous-problème à trou) — ❌ RÉFUTÉE 0/10

- **Type** : F (test d'hypothèse mécanistique — issue : réfutation)
- **Exécutée le** : 2026-06-10
- **Script** : [`checks/task_f011e15_gap_hypothesis.py`](../../checks/task_f011e15_gap_hypothesis.py)

## L'hypothèse et son verdict

H-v2 : dans la zone t = 33..40 (U morte par périodicité sur [64, n]),
`deg₆^sym(MAJ_n) = m3gap(t, n)` — le min-degré d'un V mod 3 couvrant le
trou [64, n] seul.

| t | m3gap (trou seul) | deg₆ vrai | écart |
|---|---|---|---|
| 33..35 | 36 | 40 | +4 |
| 36 | 36 | 44 | **+8** |
| 37 | 45 | 46 | +1 |

**0/10 — réfutée.** m3gap reste une borne inférieure valide du mécanisme
(aucune violation), mais la **couverture jointe de [t, 63]** (U mod 2 et
V mod 3 doivent se partager la fenêtre basse avec les MÊMES coefficients
qui couvrent le trou) contribue substantiellement — et de façon
non-uniforme (+1 à +8).

## Bilan de la journée sur la zone v2

- Le mécanisme qualitatif est prouvé (périodicité mod 2 → V seule sur le
  trou) ; sa quantification naïve (découplage trou/fenêtre) est fausse.
- **4e conjecture du fil tuée le jour de sa formulation** (C-F011d,
  C-F011, loi-à-un-étage, H-v2). Le pipeline adverse ne s'épargne rien.
- La loi exacte de la zone v2 reste *décidable* (CRT-énumération, fait
  pour t ≤ 37) mais sans forme close — état honnête : **question ouverte
  précise**, avec table exacte et bornes prouvées des deux côtés
  (m3gap ≤ deg₆ ≤ Théorème H).

## Où va le fil (e16+, candidates)

1. L'interaction jointe : caractériser ce que coûte le partage de la
   fenêtre basse (les +4/+8/+1 ont une structure base-3 à trouver).
2. Fermer les 11 cellules CAND2 (interpolation à valeurs ±1).
3. Mettre à jour la note de synthèse (étapes 10-15) — elle s'arrête à
   l'étape 11.
