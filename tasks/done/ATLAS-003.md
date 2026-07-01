# ATLAS-003 — MAJ_7 sur le tore : l'asymétrie n'aide pas (certifié)

- **Type** : V (mesure, sous-lemme de la zone génératrice 6, ligne 14)
- **Exécutée le** : 2026-06-27
- **Script** : [`checks/task_atlas003_maj7.py`](../../checks/task_atlas003_maj7.py)
  (étend V-001/V-002 ; MILP scipy/HiGHS, K_BOUND = 5 hérité)

## Pourquoi cette mesure (l'enjeu P vs NP, en une chaîne)

BHLR ont PROUVÉ le mur Ω(√n/log n) pour les polynômes toriques
**symétriques** approximant MAJ (Thm 1.2) ; leur **Conjecture 1.5** exige
la même borne pour les polynômes **généraux** — et elle seule donne
MAJ ∉ ACC⁰ (voire P ≠ ACC via CLLO21). Tout l'écart prouvé/conjecturé
tient en une question : *un polynôme asymétrique peut-il approximer MAJ
strictement mieux que le meilleur symétrique ?* KV 2024 prouvent que OUI
pour d'autres fonctions symétriques (Δ_w, dont AND) — la symétrisation
WLOG est fausse en général, le transfert gratuit sym → général est
interdit. La frontière « où l'asymétrie mord » est donc LA donnée
empirique pertinente : chaque n où ε\*(sym) = ε\*(général) est un point
en faveur de la plausibilité de la Conjecture 1.5 pour MAJ.

## Résultat : n = 7, égalité certifiée à tous les degrés

| d | ε\*(sym) | ε\*(général) | statut |
|---|---|---|---|
| 1 | 0,1875 | 0,1875 | certifié |
| 2 | 0,125 | 0,125 | certifié (240 s) |
| 3 | 0,03125 | 0,03125 | certifié (240 s) |
| 4 | 0 | 0 | exact (degré plein atteint) |

**L'asymétrie n'aide pas MAJ à n = 7.** Frontière mise à jour :
Δ_w : l'asymétrie aide (PROUVÉ, KV) ; MAJ : n'aide pas pour n ≤ 7
(MESURÉ, MILP certifiés — V-001/V-002/ATLAS-003).

## Leçon de méthode (importante pour n = 8+)

Au budget solveur par défaut, les MILP généraux d = 2, 3 rendent des
**incumbents non certifiés** (0,150~ et 0,125~ — PIRES que l'optimum
symétrique, donc non informatifs : général ⊆ ⟹ ε\*_gen ≤ ε\*_sym). Le
premier verdict « = » était donc trop fort sur d = 2, 3 — corrigé en
étendant time_limit à 240 s : certification obtenue. Règle : **aucun
verdict d'égalité sans certification** (status optimal), un incumbent ne
prouve rien.

## Limites honnêtes

- Évidence à n fini : n'établit RIEN d'asymptotique (la Conjecture 1.5
  reste ouverte) ; c'est un point sur la carte, au sens de l'Atlas.
- K_BOUND = 5 (bornes sur les parties entières) hérité de V-001 — les
  décalages optimaux observés sont petits à ces tailles, mais c'est une
  hypothèse de modélisation, pas un théorème.
- Prochain point : n = 8 (256 points ; à chiffrer — les temps 20-34 s à
  n = 7 suggèrent que n = 8 est atteignable avec time_limit ~10-30 min
  par degré).
