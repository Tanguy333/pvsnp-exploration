# MC-005 — Données : l'additivité de W sous combinaison à variables disjointes

> Produit par `checks/mc005_additivite.py` (modes 2p2, bornes, nor),
> 2026-08-07. W exact : force brute (≤ 4 variables) et CP-SAT canal de
> valeurs (5-7 variables, OPTIMAL exigé, témoin re-vérifié par évaluation
> indépendante). Exhaustif : toutes les paires non ordonnées (f, g) de
> fonctions NON CONSTANTES sur 2+2 variables (105 paires). Écart :=
> W(f ⋄ g) − (W(f) + W(g)).

## 1. Exhaustif 2+2 — verdict par combineur (105 paires)

| combineur | sous-additif | égal | super-additif | distribution des écarts |
|---|---|---|---|---|
| ∧ | 21/105 | 43/105 | 41/105 | pire sous : −1 (f=g=2 : W=3 < 4) ; pire super : +3 |
| ∨ | 21/105 | 43/105 | 41/105 | pire sous : −1 (f=1, g=3) ; pire super : +3 |
| ⊕ | **0/105** | 78/105 | 27/105 | {0 : 78, +1 : 24, +2 : 3} |
| MUX | **0/105** | **0/105** | **105/105** | {+1 : 21, +2 : 42, +3 : 33, +4 : 8, +5 : 1} |

- **∧ et ∨ PARTAGENT du coût** (21/105 sous-additifs chacun) — témoins :
  ∧ de deux fonctions-point ([x=01] ∧ [y=01] = point sur 4 variables,
  W = 3 < 2+2) ; inutilisables pour des constructions à structures
  obligatoires. Les comptes identiques ∧/∨ sont une vérification interne :
  f ∨ g = ¬(¬f ∧ ¬g) et W(¬f) = W(f) (MC-001) — la bijection est exacte.
- **⊕ n'est JAMAIS sous-additif** sur cet espace (78 exactement additifs).
- **MUX (le sélecteur, la forme du schéma Th.16) est STRICTEMENT
  super-additif partout** : écart minimal +1, maximal +5 (f=1, g=14 :
  W = 9 vs 4). Jamais égal — le surcoût du sélecteur n'est pas nul.
- Lien MUX/⊕ : W(MUX(f,g)) − W(f⊕g) ∈ {+1, +2, +3}
  (distribution {1 : 24, 2 : 56, 3 : 25}) — le MUX domine strictement le ⊕
  sur les 105 paires.

## 2. Bornes prouvées B1/B2 — vérification numérique

588 tests (toutes paires ordonnées × {∧, ∨, ⊕} non constants) :
**0 violation** de B1 (appariement : W(h) ≤ W(f) + (V_f+1)·W(g)) et
**0 violation** de B2 (restriction : W(h) ≥ max(W(f), W(g))).
Preuves dans `tasks/done/MC-005.md` §1.

## 3. Famille NOR — points exacts (re-vérification A-013 comprise)

| instance | variables | W | méthode | note |
|---|---|---|---|---|
| NOR₂ | 2 | 2 | brute | |
| NOR₃ | 3 | 3 | brute | |
| NOR₂ ⊕ NOR₂ | 4 | **6** | brute | **CONFORME A-013** (certifié sans solveur là-bas) ; somme 4, écart +2 |
| NOR₃ ⊕ NOR₃ | 6 | **14** | CP-SAT OPTIMAL | **CONFORME A-013** ; somme 6, écart +8 |
| NOR₂ ∧ NOR₂ | 4 | 4 | brute | exactement additif |
| NOR₂ ∨ NOR₂ | 4 | 4 | brute | exactement additif |
| MUX(NOR₂, NOR₂) | 5 | 8 | CP-SAT OPTIMAL | somme 4, écart +4 |
| MUX(NOR₃, NOR₃) | 7 | 14 | CP-SAT OPTIMAL | somme 6, écart +8 |

La croissance de l'écart ⊕ sur la famille (A-013 : W(F_m) = 6, 14, 24 à
m = 2, 3, 4 contre 2m) et l'écart MUX (+4 puis +8) croissent avec m —
observations à 2-3 points de taille, **q.12 : aucune loi revendiquée**.
Curiosité consignée sans interprétation : MUX(NOR₃, NOR₃) = 14 =
NOR₃ ⊕ NOR₃.

## Réserves

- Exhaustif limité à 2+2 (n = 4-5 variables au total) ; famille NOR
  jusqu'à 7 variables — q.12, aucune extrapolation : « strictement
  super-additif partout » est un fait de CET espace.
- Optima CP-SAT : assertion de solveur (réserve T27-S2 §4) ; tous les cas
  ≤ 4 variables sont en force brute pure.
- Durée : 2+2 en 8 s ; durée totale du run non journalisée [NON VÉRIFIÉ].
