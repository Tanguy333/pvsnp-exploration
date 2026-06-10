# TÂCHE F-011, étape 4 : C-F011d (critère de blocage exact) — ❌ RÉFUTÉE, avec structure

- **Type** : F (test de conjecture — issue : réfutation honnête)
- **Exécutée le** : 2026-06-10
- **Script** : [`checks/task_f011e4_blocking.py`](../../checks/task_f011e4_blocking.py)

## La conjecture testée

C-F011d (unifiante, formée à chaud) : `deg_m^sym(THR_{t,n}) = B_m(t,n)` =
premier degré d tel qu'aucun poids unique w ∈ [t,n] ne soit m-bloqué sur
[t,d]. Le sens ≥ est le théorème T-F011b ; le test portait sur ≤.

## Verdict : réfutée — 150 contre-exemples sur 678 cellules (t ≤ 10, n ≤ 30)

| m | coïncidences | écarts | structure des écarts |
|---|---|---|---|
| 2 | 118 | 97 | t=1,2 surtout, n grand (ex : t=1, n=14 : critère 8, vrai 14) |
| 3 | 174 | 34 | idem (ex : t=1, n=22 : critère 9, vrai 13) |
| 6 | 236 | 19 | **tous en fenêtre longue** (t=1 : n≥9 ; t=2 : n≥18) |

## Les trois enseignements

1. **Les théorèmes de l'étape 3 sont intacts** — mieux : le solveur
   re-confirme T-F011a (pour OR mod 2, vraie valeur = n = exactement la
   forme close prouvée, puisque C(i−1,0) = 1 pour tout i ; le critère
   mono-poids, lui, plafonne à la puissance de 2). La réfutation ne touche
   que la *généralisation* hâtive.
2. **Régimes** : le critère coïncide en régime « fenêtre courte »
   (n ≲ 2t — le régime MAJ, où vivent toutes nos anomalies prouvées) et
   échoue en « fenêtre longue » (n ≫ 2t). **C-F011 (la loi MAJ, 47/47)
   n'est pas touchée** ; c'est sa version toute-la-famille qui meurt.
3. **L'obstruction manquante est collective/globale.** Sur F₂ on sait
   exactement laquelle : l'unicité de la fonction échelon (T-F011a) — une
   contrainte de parité *globale* sur la fenêtre, invisible au blocage
   mono-poids. L'analogue mod 3/6 en fenêtre longue (quelle structure
   force les écarts +1, +2, +4 observés ?) est la **prochaine vraie
   question** du fil.

## Conformité épistémique

Conjecture formée, testée massivement *le jour même*, réfutée par les
données, théorèmes antérieurs préservés — le pipeline fait exactement ce
pour quoi il est conçu (q.12 : aucune extrapolation n'a été présentée
comme théorème ; C-F011d était étiquetée conjecture dès sa formulation).

## Prochaine cible (étape 5, candidate)

Caractériser l'obstruction collective mod 3 en fenêtre longue : sur F₃ la
couverture n'est plus unique (patterns ±1), mais les écarts observés
(+1..+4 par rapport au blocage) suggèrent une contrainte de type
« somme signée des différences finies » analogue au télescope mod 2.
Approche : extraire du solveur, pour les cellules en écart, les patterns
±1 *réalisables* au degré vrai et comparer aux patterns interdits au degré
critère — chercher l'invariant qui les sépare.
