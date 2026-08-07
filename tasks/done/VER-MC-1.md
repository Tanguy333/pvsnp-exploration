# VER-MC-1 — La passe adverse tierce du bloc MC-003..010 : le cœur TIENT sous ré-implémentation indépendante — 5 prises corrigées le jour même, dont un bug qui inversait une conclusion consignée

`Rattachement :` Instrument pour Atlas ligne 7 — cellule
`barriers/depot_vs_rr.md` §3 bis : la contre-vérification indépendante du
bloc (6 preuves de session, 2 réfutations internes, 8 campagnes), exigée
par la méthode et consignée en réserve dans chaque fiche.
**Relu à la clôture : la cellule visée a-t-elle bougé ? OUI** — le bloc
passe au statut CONTRE-VÉRIFIÉ (avec son résidu nommé), la seule donnée
consignée invalide est corrigée (conclusion inversée), deux preuves sont
réparées, une formule et trois comptes rectifiés, et un bug de solveur
documenté renforce la réserve permanente de l'instrument.

`Test de plafond :` les deux issues prévues se sont produites : le cœur
confirmé (réfutation de C-MC008, loi C-MC009, réduction M, majorants,
minorants, cartes s ≤ 3 — tout reproduit indépendamment) ET des failles
réelles trouvées et corrigées — c'est exactement ce que la passe devait
départager.

<!--DISTANCE-->
Énoncé visé : « le bloc MC-003..010 est correct » — verdict : le cœur
OUI (contre-vérifié par trois voies indépendantes), cinq défauts réels
corrigés, un résidu d'assertion-solveur nommé.
Classe de complexité qui y figure : NP (la chaîne du front MC que le bloc
porte).
Chaîne vers P vs NP : contre-vérification → la chaîne de totalisation
repose sur des briques relues → MinSYM+ → échappatoire RR de la ligne 7.
[maillon le plus faible : les INFEASIBLE de solveur, assertions sans
équivalent de l'assert-témoin — désormais documenté par un bug réel]
<!--/DISTANCE-->

## Dispositif

Trois vérificateurs indépendants (agents), consigne « présumer faux »,
dépôt en lecture seule, instruments réécrits de zéro (interdiction
d'importer les modules du dépôt) : **V1** — re-dérivation des preuves
fondatrices (B1/B2, théorème du sélecteur, Lemme 4, lois G et
F-recouvrement) ; **V2** — re-dérivation des preuves récentes (réduction
M, trois constructions, théorèmes A/B/C des copies décalées) ; **V3** —
ré-implémentation des calculs décisifs (deux encodages CP-SAT neufs,
force brute exhaustive), audit des six scripts, cohérence
fiches ↔ données. Scripts des passes : `ver1_*`, `ver2_*`, `ver3_*`
(scratchpad de session).

## Verdicts

### Ce qui TIENT (contre-vérifié)

1. **Les 6 preuves de session re-dérivées sans faille de fond** :
   B1, B2, théorème du sélecteur (i)-(iii), Lemme 4, loi G,
   F-recouvrement (V1 : 8/8, ~15 000 instances numériques, 0 violation) ;
   réduction M (deux sens du +1 compris), les trois constructions,
   théorèmes A et B — inégalité de recouvrement re-vérifiée, même
   cartographie, premier échec (8,5) (V2).
2. **La réfutation de C-MC008 est exacte** : W(3,3,0,0) = 8 confirmé par
   V3 sous DEUX encodages neufs (faisable à 8 — solution différente du
   témoin du dépôt, re-vérifiée en Python pur — et INFEASIBLE à 7), ainsi
   que (3,4,0,0) = 9 et (3,3,0,1) = 10.
3. **La loi C-MC009 : zéro écart contre la force brute exhaustive** —
   28/28 paires ν = 3, 120/120 ν = 4, et les 28 classes ν = 5 en entier
   (dont le groupe (0,5,0) que le dépôt n'avait pas testé).
4. **Les cartes et mesures** : la carte s = 3 de MC-007 recalculée
   INTÉGRALEMENT (65 536 fonctions, orbites propres à V3) — identique ;
   MC-005 re-mesuré en entier (AND/OR/XOR/MUX, NOR) — identique ;
   MC-010 (audit, caps, inégalité) — conforme ; tables MC-003 aux points
   1-2 uns — conformes aux lois.
5. **Scripts sans bug de calcul** (hors t2 ci-dessous) : mc003, mc005,
   mc008 (calculs), mc009 + règles (le binôme d'évaluation par blocs
   validé dans les deux sens), mc010 ; `dnf_size` exacte ; `permute` et
   la propagation d'orbites valides ; conventions de tranches cohérentes
   entre mc007 et mc008.

### Les prises (toutes corrigées ce jour, marquées dans les porteurs)

1. **BUG RÉEL — mc007 `run_t2`** (V3) : 6 variables déclarées pour des
   points sur 4 bits → 48 zéros fantômes gonflaient W. **Seule donnée
   consignée invalide du bloc, et la conclusion s'INVERSE** : sur l'objet
   réel (rejoué même graine, script corrigé), g = [−4, −3, −2, −1, −1,
   0, 0, +1, +2, +3] — 5/10 tirages SOUS-additifs. « Le partage n'est pas
   générique aux grandes bases » était un artefact ; le partage est
   courant à base 2 bits aussi, et la nécessité de fibres STRUCTURÉES en
   sort renforcée. Corrigé : script, fiche MC-007, data, cellule,
   backlog, cahier.
2. **Couverture manquante — majorant (1,1)** (V2) : « majorants prouvés
   partout » (MC-009 §4) était une survente — aucune construction du
   dépôt ne couvrait (1,1) (la couronne donne 4 + 2o ≠ 2 + 2o) ; pour
   o ≥ 6 le majorant ne reposait sur rien. Construction réparatrice de
   V2 : p = y₁ + y₂ + Σ_l (m_{1l} + m_{2l}), poids 2 + 2o — intégrée à
   `mc009_regles.py`, vérifiée par blocs, insérée à la fiche MC-009 §4.
3. **Lacune de preuve — Théorème C (MC-010)** (V2) : « un léger porte son
   singleton » importé de F1, inapplicable à (1,1) (le 0-point y est un
   zéro). Lemme réparateur (via les zéros {1,l}, {2,l} : a_l = 0 ⟹
   ω_l ≥ 2, contradiction) inséré à la fiche, corroboré sur 440
   séparateurs énumérés.
4. **Formule fausse hors domaine** (V3) : « g = |c₀\c₁| − 2 » (corollaire
   MC-008) — la vraie est **g = d − max(d, 2)** (contre-exemple vérifié à
   s = 4 : (1111, 0001) → g = 0 ≠ 1) ; le SIGNE (partage ⟺ recouvrement)
   est inchangé et re-dérivé sous C-MC009. Corrigée dans les cinq
   porteurs.
5. **Trois comptes** (V3) : 3 984 classes de S₄ (pas 1 992 — étiquette
   S₄×complément recopiée d'A-013) ; 28 groupes réalisables à ν = 5, 27
   testés (le manquant (0,5,0) vérifié conforme par V3) ; 31 témoins de
   cœurs (pas 27). Corrigés (fiches, data, docstrings).

### Prise transverse — le bug ortools (V2)

ortools 9.15.6755 peut rendre un **statut OPTIMAL FAUX** quand `Minimize`
est combiné à des contraintes `!=` directes entre expressions linéaires
partageant des variables (isolé et reproduit ; la formulation par
variables intermédiaires — celle de TOUS les scripts du dépôt — n'y est
pas exposée, et l'assert-témoin couvre le sens majorant). Conséquence
durable : **la réserve T27-S2 §4 est renforcée** — un INFEASIBLE de
solveur reste une assertion sans équivalent de l'assert-témoin ;
atténuation disponible : encodages doubles indépendants (pratiqués par
V3, concordants partout).

### Nuances sans correction nécessaire (consignées)

B2-corollaire « ≥ max » : vaut sur le périmètre f, g non constantes (son
contexte) ; le théorème du sélecteur (ii) est vrai aussi pour f constante
(sous-revendication) ; docstring mc006 « motifs distincts » vs fiche
(cosmétique) ; `loi_coeur` de mc009 = l'ancienne loi conservée à dessein
comme détecteur (commenté depuis) ; `W_min` de mc010 sans re-vérification
du témoin (les certificats décisifs passent par `decision_infaisable`).

## Statut final du bloc

**MC-003..010 : CONTRE-VÉRIFIÉ** — trois voies indépendantes, cœur
confirmé, cinq défauts corrigés le jour même. Résidu permanent :
les optima/INFEASIBLE à ν ≥ 5 sont des assertions de solveur (chez les
vérificateurs comme au dépôt) ; la divergence C-MC008/C-MC009 au-delà de
ν = 7 est hors de portée de tout solveur — le statut CONJECTURE des
minorants hors tranches prouvées est le bon. Non re-vérifiés (mineurs,
rien de décisif n'en dépend) : 5 points de contrôle non discriminants de
MC-009, 3 certificats ν = 7 de MC-010, T3/T4 de MC-006.

## Réserves

- Les vérificateurs sont des agents de la même session (indépendance
  d'instruments et de dérivation, pas d'organisme) ; une relecture
  HUMAINE ou extérieure resterait l'étalon supérieur.
- Le bug ortools est documenté sur la version 9.15.6755 de la machine du
  dépôt ; à re-tester après toute montée de version.
