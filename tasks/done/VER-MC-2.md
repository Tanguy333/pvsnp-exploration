# VER-MC-2 — La passe adverse tierce du bloc MC-011..013 : les six preuves TIENNENT sous double re-dérivation et triple ré-implémentation — une correction de consignation, deux avertissements armés pour l'aval

`Rattachement :` Instrument pour Atlas ligne 7 — cellule
`barriers/depot_vs_rr.md` §3 bis : la passe exigée par les réserves des
trois fiches du bloc (5 théorèmes + 2 lemmes de session, dont l'argument
des bandes, sans relecture).
**Relu à la clôture : la cellule visée a-t-elle bougé ? OUI** — le bloc
MC-011..013 passe au statut CONTRE-VÉRIFIÉ ; les trois lois de
fibres-points démontrées (comparable, (1,1), linéaire) sont désormais des
théorèmes RELUS ; et la passe a armé deux garde-fous pour la suite du
front (frontière m ≥ 1 du lemme singleton ; prérequis ω_l ≥ 1).

`Test de plafond :` une faille dans l'induction ou les bandes aurait
invalidé une à trois familles de lois ; le verdict est la confirmation,
avec des vérifications PLUS FORTES que celles du dépôt sur deux points
(contre-exemple au lemme singleton cherché par solveur jusqu'à ref+4 ;
borne interne de la branche 3 (1,1) prouvée EXACTE par
INFEASIBLE/FEASIBLE).

<!--DISTANCE-->
Énoncé visé : « le bloc MC-011..013 est-il correct ? » — OUI, contre-
vérifié par trois vérificateurs indépendants (deux re-dérivations
complètes des preuves + une triple ré-implémentation des calculs).
Classe de complexité qui y figure : NP (la chaîne MinSYM+ que le bloc
sert).
Chaîne vers P vs NP : bloc contre-vérifié → les lois de fibres-points
sont des acquis fiables de la chaîne de totalisation → MinSYM+ →
échappatoire RR de la ligne 7. [maillon le plus faible : les INFEASIBLE
ν ≥ 5 restent des assertions de solveur, chez les vérificateurs comme au
dépôt]
<!--/DISTANCE-->

## Dispositif

Trois vérificateurs indépendants (2026-08-07/08), consigne « présumer
faux », dépôt en lecture seule, instruments réécrits de zéro :
- **V1** — re-dérivation des preuves de MC-011 (lemme singleton,
  inductions comparable et (1,1)) et MC-012 (forçage d'égalité de la
  base, corollaires) + force brute exhaustive ν ≤ 4 + CP-SAT ν = 5 ;
- **V2** — re-dérivation de MC-013 (bandes) et de la CHAÎNE D'ASSEMBLAGE
  trans-fiches (base → branches → bandes), arithmétique refaite ligne à
  ligne, audit de population (44 séparateurs) ;
- **V3** — ré-implémentation des calculs sous DEUX encodages neufs
  (booléens de signe ; Möbius sans variables a_S) + force brute,
  conventions de bits inversées ; certificats ν = 8 rejoués ; audit des
  trois scripts ; cohérence fiches ↔ sorties (rejeux).
(Interruption réelle en cours de passe : extinction du PC — V3 relancé à
neuf, V1 lancé après le retour du lanceur ; V2 était complet avant.)

## Verdicts

1. **Les six preuves : CONFIRMÉES, zéro faille** — lemme singleton
   (V1+V3), induction comparable ∀o (V1), induction (1,1) ∀o (V1, avec
   la borne interne de la branche 3 prouvée EXACTE : INFEASIBLE à 3o+1,
   faisable à 3o+2 — une branche qu'aucun optimum réel ne réalise,
   testée sous contraintes forcées), base linéaire au sol (V1+V2, la
   frontière b ≥ 2 localisée exactement : le statut de zéro de {j}),
   lemme des bandes (V2+V3, arithmétique refaite), théorème
   d'assemblage MC-013 (V2 — « la couture qui devait lâcher » tient :
   la base vaut pour un séparateur ARBITRAIRE, la trichotomie est
   exhaustive à chaque niveau via ω_l ≥ 1).
2. **Les calculs : zéro écart** — les 148 paires ν ≤ 4 sous trois
   méthodes concordantes ; 8/8 cœurs ν = 5 ; les 19 cœurs de MC-011
   jusqu'à ν = 7 ; 5/5 certificats rejoués sous encodage neuf (dont
   (4,4), (3,5), (2,6) à ν = 8 : INFEASIBLE à 9, témoins à 10
   re-vérifiés en Python pur) ; le lemme des bandes ré-encodé : 15/15,
   même minimum mesuré (b + 2 + 2o).
3. **Les scripts : aucun bug de validité** — l'encodage des bandes de
   mc013 est exact et son cap ne tronque pas ; l'exclusion multi-O de
   mc011 est correcte ; le cap de décision de mc012 porte bien sur le
   poids total. Points d'audit mineurs consignés (bornes d'énumération
   du mode singleton = {loi, loi+1}, comblées par les tests V3 à ref+4 ;
   FAISABLE de mc012 non re-vérifié pur Python dans le script — fait par
   V3).

## Les prises (toutes traitées ce jour)

1. **CORRECTION réelle (V3)** — MC-012, audit : « les optima réalisent
   EXACTEMENT la construction linéaire » réfuté au rejeu (à (1,2), le
   solveur rend un AUTRE optimum de poids 4 : c = 2, σ_B = 2) — c'était
   une propriété des témoins d'un run, pas des cœurs ; fiche corrigée,
   théorème intact. Idem les durées « 35-58 s chacun » (des cumuls).
2. **AVERTISSEMENT armé (V1)** — la frontière m ≥ 1 du lemme singleton
   est RÉELLE : 21 contre-exemples explicites à m ≥ 1 (l'unité d'un
   léger portée par un monôme mixte) — tout usage futur du lemme sur une
   configuration à M non vide sans réduction M préalable serait FAUX.
   Bandeau ajouté à MC-011 §1. Les usages du bloc sont propres (m = 0).
3. **Prérequis explicité (V1+V2)** — l'exhaustivité de la trichotomie
   repose sur ω_l ≥ 1 ∀l (vrai, prouvé par le préambule du lemme) ;
   formulation existentielle précisée dans MC-013 §3.
4. Mineurs : « ν ≤ 7 » → ν ≤ 6 (MC-011) ; docstring de mc013 (« attendu
   b+2+o ») corrigé ; note de marge V2 : la chaîne d'assemblage est
   tendue à zéro au niveau o′ = 1 — sain, à surveiller pour l'analogue
   couronne.

## Statut du bloc et réserves

**MC-011..013 : CONTRE-VÉRIFIÉ.** Résidu : les INFEASIBLE ν ≥ 5 restent
des assertions de solveur (deux implémentations et deux encodages
concordants, mais même moteur CP-SAT) ; le comptage « 1 140 séparateurs »
du mode singleton n'est recoupé intégralement que sur une ligne (44/2/0,
identique) — le lemme est confirmé plus fortement par ailleurs ; une
relecture humaine reste l'étalon supérieur.

## Pièces

Rapports V1/V2/V3 archivés dans les sorties de session (scripts
vérificateurs : scratchpad v2a_*, v2b_*, v2c_*) ; corrections appliquées
dans `tasks/done/MC-011.md`, `MC-012.md`, `MC-013.md`,
`checks/mc013_bandes.py`.
