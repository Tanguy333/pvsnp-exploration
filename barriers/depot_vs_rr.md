# D-005 : Le programme de mesure du dépôt × Preuves naturelles (RR) — l'auto-test

> Tâche type D. Exécutée le 2026-08-02. La cinquième cellule barrière du
> dépôt, et la première tournée **contre lui-même** : les Tours 26-27 avaient
> déclaré les barrières « sans objet » pour le fil SYM∘AND ; cette cellule
> applique enfin le critère (b) au programme de mesure. Sources : A-007
> (définitions RR verbatim), D-001 (`williams_vs_rr.md`, les deux sorties et
> Naor-Reingold), A-013 (le modèle = SYM+ de Williams), et les mesures
> exhaustives de ce jour (`checks/task_d005_largeness.py`,
> `checks/task_d005_comptage.py`).
>
> **Statut de contrôle** : contrairement aux cellules récentes, celle-ci n'a
> PAS encore subi de passe adverse par agents indépendants (lanceur de
> workflows indisponible au moment de la rédaction) — chaque maillon externe
> est cependant repris de pièces déjà auditées du dépôt, et chaque maillon
> nouveau est un calcul re-vérifiable. Passe adverse à faire au premier
> créneau ; jusque-là, cette cellule est au statut RÉDIGÉ-SOURCÉ, pas
> CONTRE-VÉRIFIÉ.
>
> **Mise à jour 2026-08-02 (MC-001)** : les distributions exhaustives n ≤ 4
> du §2 ont depuis été recalculées par un instrument INDÉPENDANT (énumérateur
> sans solveur, stratégie C de MC-001) — chiffres identiques ; le comptage a
> été étendu à n = 10, 12 ; et le maillon §3 a été retravaillé par un
> workflow adverse complet (§3 bis). Les §4-5 (applicabilité, verbatims)
> restent, eux, au statut RÉDIGÉ-SOURCÉ.

## 1. La question

Le dépôt a utilisé pendant 18 tâches la propriété « W(f) ≥ s » — W étant la
taille minimale d'un circuit SYM∘AND à variables seules (le format SYM+ de
Williams, A-013) — comme instrument de borne inférieure. **Cette propriété
est-elle NATURELLE au sens de Razborov-Rudich ?** Rappel des définitions
(A-007, verbatim sur texte) : *constructive* = décidable en temps polynomial
en la table de vérité (taille N = 2ⁿ) ; *large* = vraie pour une fraction
≥ 2^(−O(n)) des fonctions ; une propriété naturelle *utile* contre une classe
C contenant des PRG/PRF exponentiellement sûrs casserait ces générateurs —
donc, sous crypto standard, pas de preuve naturelle contre de telles classes.

## 2. La largeness : MESURÉE, puis PROUVÉE

**Mesuré (exhaustif, zéro cas non conclu, pondération par orbites vérifiée)** :

| coupe | n = 3 (256 f) | n = 4 (65 536 f) |
|---|---|---|
| W ≥ médiane | 70,31 % (W ≥ 3) | 67,60 % (W ≥ 6) |
| W ≥ médiane+1 | 32,81 % | 38,26 % |
| W ≥ max−1 | 32,81 % | 11,68 % |
| W = max | 4,69 % (W = 5) | 1,03 % (W = 9) |

Toutes les coupes sont des fractions **énormes** à l'échelle RR (le seuil de
largeness est 2^(−O(n))). **Prouvé (comptage, vérifié numériquement n = 3..8)** :
le nombre de fonctions séparables à poids ≤ s est majoré par
C(s+2ⁿ−1, 2ⁿ−1)·2^(s+1) (choix des coefficients × partition des valeurs) ;
il en résulte que la **médiane de W croît sans borne** — > 3 à n = 4, > 13 à
n = 6, > 53 à n = 8, > 211 à n = 10, > 843 à n = 12 (bornes prouvées,
extension n = 10, 12 exécutée le 2026-08-02 ; les médianes mesurées, 3 et 6,
sont au-dessus). La largeness de toute coupe utile n'est donc pas une extrapolation :
**c'est un théorème de comptage**. Verdict du maillon : **LARGE — PROUVÉ**.

*Note annexe, consignée avec son statut* : le maximum observé vaut 5 à n = 3
et 9 à n = 4 (motif 2^(n−1)+1), mais le motif est **CASSÉ à n = 2** (max = 2,
pas 3) — deux points ne font pas une loi (q.12), statut : observation, sans
suite.

## 3. La constructivité : OUVERTE — et c'est le maillon décisif

- Le dépôt calcule W par CP-SAT et par énumération — exponentiel en N. La
  décision « W(f) ≤ s » par force brute coûte N^{O(s)} (énumération des
  vecteurs de coefficients) : **quasi-polynomial en N pour s = polylog(N)**,
  pas polynomial. Aucun algorithme poly(N) n'est connu du dépôt. [OUVERT]
- Y a-t-il une raison de croire le calcul de W **dur** ? L'analogie est
  frontale : calculer CC(f) est NP-dur (Hirahara-Ilango-Loff 2025, pièce
  [V-primaire] au dépôt, A-015), et « calculer une mesure de complexité est
  dur » est le motif entier de la ligne 13 (MCSP). W est une mesure de ce
  type — la dureté est **PLAUSIBLE, non prouvée**. [CONJECTURE]

### 3 bis. Mise à jour MC-001 (2026-08-02) — le maillon a bougé

Tâche dédiée `tasks/done/MC-001.md` (workflow 5 agents, passe adverse
comprise, + 3ᵉ passe de session en force brute pure). État du maillon après
MC-001 :

- **MinSYM+ ∈ NP, PROUVÉ inconditionnellement** — le témoin injectif
  Σ 2^i·xᵢ donne W(f) ≤ N−1 pour toute f, et l'objectif borne lui-même les
  coefficients : la question est désormais exactement « **NP-complet ?** ».
- **Deux variantes partielles sont NP-COMPLÈTES** (points listés avec
  B = {0} : = Set Cover à valeur exacte ; prescrite-unilatérale à don't
  cares : = Min-DNF(∗) via rails doubles) — la dureté du cas total est
  rendue plus plausible, PAS prouvée ; les deux verrous restants sont nommés
  (étranglement logarithmique, contrôle du zoo F-022).
- **Les trois constructivisations évidentes sont fermées par témoins** :
  aucun des 15 invariants naturels poly(N) ni leur uplet complet ne
  détermine W à n = 4 (deux fonctions à invariants identiques, W = 4 vs 6) ;
  la relaxation LP est vacueuse (diséquations, gap infini) et même à
  orientation fixée W_ℝ(MAJ₄) = 3 < 4 ; pas de statistique suffisante pour
  une programmation dynamique. [FERMÉ PAR TÉMOINS, n ≤ 4 — q.12, aucune
  extrapolation]
- **La transposition directe de HIL est morte** (obstruction diophantienne :
  f(1^m) = 0 sous tout bourrage-zéro, strata positifs vides ; aucun pont
  fonctionnel W = g(χ₁), W dépendant de l'encodage quand χ₁ n'en dépend
  pas) ; un pont par inégalité reste ouvert.
- **Réserve F6, contraignante** : même une NP-dureté totale prouvée ne
  fermerait pas MÉCANIQUEMENT l'échappatoire de constructivité — une autre
  propriété large facile pourrait impliquer les mêmes bornes (nuance
  standard du débat MCSP-naturalness). L'échappatoire resterait plaidable,
  pas acquise.
- **Antériorité vérifiée (MC-002, 2026-08-07)** : la question totale est
  VIERGE dans la littérature — vérification systématique quatre lignes,
  documents ouverts (`bib/minsym_antecedents.md`) ; le plus proche est
  HOS18 (OR∘AND∘MOD_m, tête OR, où la tête seuil reste une extension
  spéculative), et le gabarit de l'étape manquante (partiel → total) est
  leur Th.16.
- **Première voie du cas total ÉLIMINÉE (MC-003, 2026-08-07)** : la voie
  nommée par MC-001 (« packing contre échafaudage ») est réfutée par mesure
  exhaustive n ≤ 3 (88 instances, zéro non-conclu) — le packing sature à
  2n observé pendant que W croît, W(f_g) n'est pas fonction de dnf-size(g),
  et la séparation stricte des plages casse dès n = 3 (W = 9 et W = 10
  réalisés par deux valeurs de r chacune). Mécanisme : les uns de f_g
  forment une antichaîne — les optima donnent aux uns une valeur commune
  (régime « couvert à valeur exacte », tête ETHR de fait), découplé de la
  structure DNF. Voies restantes en lice : le gabarit HOS18 Th.16 (MC-004)
  et l'additivité de W sous somme disjointe (trou (b) de MC-001).
  Pièces : `tasks/done/MC-003.md`, `data/mc003_rails_doubles.md`.
- **Les deux voies restantes CONVERGENT (MC-004, 2026-08-07)** : audit sur
  texte intégral du pipeline HOS18 (`bib/hos18_partiel_total.md`) — le
  gabarit Th.16 ne transfère pas en l'état (gating-réciproque, extraction
  affine + ablation OR, coût additif exact, compression algébrique : chaque
  pièce exige la localité de la tête OR ou l'algèbre MOD_m), et sa
  totalisation pour SYM+ PASSE PAR le lemme d'additivité/extraction de W.
  **Le front se concentre donc sur UNE question : l'additivité de W sous
  structures disjointes/étiquetées** — munie d'un acquis (slice-gating
  gratuit à y = 1^s) et de deux patrons (zero-error vérifiable,
  amplification multiplicative à la Th.45). Réserve : analyse
  d'obstruction, pas théorème — un schéma de totalisation entièrement
  différent n'est pas exclu. Prochaine tâche = MC-005 (additivité), 5ᵉ du
  fil : bilan de la règle 9 obligatoire.
- **Premier fondement mesuré du schéma (MC-005, 2026-08-07)** : sur
  l'exhaustif 2+2 (105 paires non constantes), le combineur à SÉLECTEUR —
  la forme même du schéma Th.16 — est **strictement super-additif
  partout** (105/105, écarts +1..+5, jamais de partage de coût) ; le ⊕
  n'est jamais sous-additif (points A-013 re-vérifiés par deux méthodes :
  6, 14) ; ∧/∨ PARTAGENT (21/105) — la colle d'un gadget doit être de type
  sélecteur/⊕, pas ∧/∨. Deux bornes prouvées encadrent la question :
  appariement W(h) ≤ W(f) + (W(f)+1)·W(g) et restriction
  W(h) ≥ max(W(f), W(g)) — 588 tests, 0 violation. **Le pas suivant est
  une PREUVE** (super-additivité du sélecteur à tout n, ou minoration
  certifiable de l'écart) — la mesure ne peut plus trancher (q.12 :
  fondement mesuré à 2+2, pas un théorème). Bilan de fil (règle 9) écrit :
  `tasks/done/MC-005.md` §3 ; témoins : `atlas/temoins.md` (3 lignes MC).
  Pièces : `checks/mc005_additivite.py`, `data/mc005_additivite.md`.
- **LA PREUVE EST FAITE (MC-006, 2026-08-07) — Théorème** : (i) pour toute
  fibre à BLOCS DISJOINTS sélectionnée par motifs (h arbitraire hors des
  tranches réalisantes), W(h) ≥ Σᵢ W(fᵢ) — le coût ne se partage JAMAIS, à
  toute taille ; (ii) strict pour le MUX à 1 bit : W ≥ W(f) + W(g) + 1
  (bras 0 non constant) ; (iii) borne atteinte (W(MUX(id,id)) = 3 ; 21/105
  paires à +1). Preuve élémentaire (charge par classes disjointes +
  collision de valeurs), complète dans `tasks/done/MC-006.md` ; batterie de
  falsification 0 violation (dont 12 instances à tranches-poubelle,
  `checks/mc006_preuve_selecteur.py`). Le fondement du schéma de
  totalisation passe de MESURÉ à **PROUVÉ** dans cette géométrie ; bonus :
  premier outil de CERTIFICATION de W par théorème (contre le verrou (c) de
  MC-001). **Verrou requalifié, nommé** : la polynomialité interdit les
  blocs disjoints au-delà de O(log) fibres — la géométrie exigée est la
  fibre à coordonnées PARTAGÉES (HOS18), où les classes de charge se
  recouvrent : c'est le candidat MC-007, et la compression reste l'autre
  verrou. Réserve : preuve de session, falsifiée par batterie mais sans
  passe adverse tierce (trou de contrôle du fil).
- **La carte de la fibre partagée (MC-007, 2026-08-07) — le verrou tranché
  dans sa forme naïve, reformulé dans sa forme utile** : exhaustif complet
  à s = 2, 3 (toute fonction sur 1+s variables lue par tranches). La
  super-additivité INCONDITIONNELLE est morte — 34 % des paires de fibres
  distinctes partagent à s = 3, et 156 paires atteignent le plancher B2
  (W(h) = max : la fibre bon marché vient gratuitement). Mais le régime
  STRUCTURÉ vit : le marqueur [y = 1^s] n'est presque jamais absorbé
  (1/254), et les points épars — l'analogue du « scattered » de HOS18 —
  sont quasi additifs (g ∈ {−1 : 9, 0 : 40, +1 : 7}), leurs 9 exceptions
  obéissant à une règle exacte — ~~l'emboîtement directionnel~~
  **CORRIGÉE par MC-008 : le RECOUVREMENT descendant** (g = d − max(d, 2)
  pour c₁ ⊊ c₀ non vide, d = |c₀\c₁| — formule re-corrigée par VER-MC-1,
  le « d − 2 » initial étant faux dès d ≥ 3 ; l'emboîtement profond ne
  partage pas — la caractérisation initiale était un sur-ajustement,
  3 contre-exemples).
  **Condition de non-partage : l'antichaîne de supports, SUFFISANTE** —
  l'obstacle de MC-003 devenu condition de la solution, désormais dérivée
  des lois (MC-008). Base 2 bits : ~~échantillon entièrement
  super-additif~~ [CORRIGÉ par VER-MC-1 : bug d'encodage (6 variables
  déclarées pour 4) — sur l'objet réel, 5/10 tirages SOUS-additifs,
  min −4 : le partage est courant à base 2 bits aussi, la nécessité de
  fibres structurées renforcée]. [q.12 : s ≤ 3]
  Pièces : `tasks/done/MC-007.md`, `data/mc007_fibre_partagee.md`,
  `checks/mc007_fibre_partagee.py`.
- **Les lois des fibres-points (MC-008, 2026-08-07)** : loi G PROUVÉE —
  W([w = u]) = ν − |u| + 1 (u ≠ 0), ν (u = 0) ; construction explicite +
  packing (Lemme 4, exact sur les points après avoir saturé sur les
  antichaînes). Loi F (deux points) : constante sur les classes
  (a, b, m) comme la symétrie l'exige, forme close **C-MC008** en trois
  régimes — recouvrement F = ν − m − [m = 0] (PROUVÉ), comparable
  F = 2ν − b − 2m + [m ≥ 1], incomparable F = 2(ν − m) − max(2, a, b) —
  53/53 groupes conformes (exhaustif ν ≤ 4 + tous les groupes ν = 5),
  statut CONJECTURE hors recouvrement (le minorant incomparable exige un
  argument de valeurs : le packing y sature). **Corollaire** : pour les
  fibres-points à base 1 bit, g = −1 au recouvrement descendant (d = 1 ;
  formule générale g = d − max(d, 2), corrigée par VER-MC-1),
  g ≥ 0 partout ailleurs (incomparables : dérivé des lois) — la brique
  « fibres sans partage certifiées » du schéma a ses lois. Cible suivante
  (MC-009 candidat) : PROUVER C-MC008 (minorant incomparable). Pièces :
  `tasks/done/MC-008.md`, `data/mc008_lois_points.md`,
  `checks/mc008_lois_points.py`.
  **[Correction MC-009, même jour : la branche incomparable de C-MC008
  est RÉFUTÉE dès a ≥ 3 — voir le point suivant.]**
- **C-MC008 réfutée, réduction M et majorants PROUVÉS (MC-009,
  2026-08-07)** : la branche incomparable de C-MC008 meurt hors de sa
  plage d'ajustement (a ≤ 2) — trois contre-exemples certifiés,
  (3,3,0,0) : F = 8 ≠ 9, (3,4,0,0) : 9 ≠ 10, (3,3,0,1) : 10 ≠ 11 ;
  mécanisme : la construction COURONNE (a+b+2+2o) bat la linéaire dès
  a ≥ 3 — cinquième prise q.12 du fil, deuxième interne, attrapée par
  l'extraction de témoins à ν = 6. **Acquis positifs** : (i) la
  RÉDUCTION M est un THÉORÈME (x_i := 1 pour ≥ ; étiquetage par M pour
  ≤ ; le +1 comparable = le coefficient forcé du singleton m_i) — tout se
  ramène aux cœurs m = 0 ; (ii) loi corrigée **C-MC009** (comparable
  b + 2o ; incomparable 2(a+b+o) − max(b, 2, a+b−2)) conforme à TOUTE la
  donnée (7/7 points neufs ν ≤ 7, dont 2 discriminants) ; (iii) les
  MAJORANTS de C-MC009 sont PROUVÉS partout par trois constructions
  générales (comparable, linéaire, couronne — séparation démontrée,
  vérification par blocs a, b ≤ 8, o ≤ 8) : la loi est en sandwich — ≤
  prouvé, = certifié-solveur sur tout le domaine testé. **Reste OUVERT :
  les minorants des cœurs** (le packing sature ; l'esquisse de cascade a
  un trou identifié — familles D_j non disjointes — et n'est pas
  revendiquée) : cible MC-010. La passe adverse tierce du bloc
  MC-003..009 est CRITIQUE (3 preuves de session, 2 réfutations internes
  successives). Pièces : `tasks/done/MC-009.md`, `data/mc009_preuve_F.md`,
  `checks/mc009_preuve_F.py`, `checks/mc009_regles.py`.
- **Les minorants (MC-010, 2026-08-07) — la première tranche de la loi F
  au-delà du recouvrement devient un THÉORÈME complet** : par l'argument
  des COPIES DÉCALÉES (chaque bit extérieur translate le cube intérieur ;
  l'interdiction de retomber sur la valeur protégée P force la dichotomie
  léger/lourd), trois théorèmes de minorants — (A) comparable, μ = 0 :
  W ≥ b + 2o pour tout o ; (B) comparable INCONDITIONNEL pour o ≤ 7 (via
  l'inégalité de recouvrement (d−1) + ⌈C(k,d)/C(k−2,d−2)⌉ ≥ k, vraie pour
  k ≤ 7, premier échec (8,5) — zone résiduelle cartographiée) ; (C) cœur
  (1,1) : 2 + 2o pour o ≤ 2, et tout o sous μ = 0. **Corollaire (avec les
  majorants et la réduction M de MC-009) : F(0, b, m, o) = b + 2o + [m≥1]
  est PROUVÉ pour tout b ≥ 2, m, et o ≤ 7.** Audit : les inégalités de la
  preuve tiennent sur 10/10 témoins optimaux — qui ont TOUS μ = 0 : le
  chaînon manquant du cas général est un LEMME DE NORMALISATION (« il
  existe toujours un optimum sans monômes multi-extérieurs »), MC-011
  candidat. Certificats hors preuve : 15/15 INFEASIBLE au cap = loi − 1
  (dont tous les cœurs incomparables testés, ν ≤ 7). Réserve : 6 preuves
  de session dans le bloc MC-003..010, zéro relecture tierce — CRITIQUE.
  Pièces : `tasks/done/MC-010.md`, `data/mc010_minorants.md`,
  `checks/mc010_minorants.py`.
- **LA PASSE ADVERSE TIERCE EST FAITE (VER-MC-1, 2026-08-07)** — trois
  vérificateurs indépendants (re-dérivation des 6 preuves de session ;
  ré-implémentation de zéro des calculs décisifs ; audit des scripts et
  consignations), consigne « présumer faux ». **Le cœur du bloc
  MC-003..010 TIENT** : les 6 preuves re-dérivées sans faille de fond
  (~15 000 instances numériques V1 ; 220 configs de constructions V2 ;
  force brute exhaustive 148/148 et les 3 points de réfutation de C-MC008
  reproduits sous 2 encodages neufs V3 ; la carte s = 3 de MC-007
  recalculée intégralement à l'identique). **Prises de la passe,
  corrigées le jour même** : (1) BUG t2 de MC-007 — 6 variables déclarées
  pour 4, seule donnée consignée invalide du bloc : sur l'objet réel,
  5/10 tirages sous-additifs (conclusion inversée, consignée) ;
  (2) le majorant (1,1) n'était couvert par aucune construction —
  construction réparatrice fournie par V2, intégrée et vérifiée ;
  (3) lacune dans la preuve écrite du Théorème C (F1 inapplicable à
  (1,1)) — lemme réparateur inséré ; (4) formule g = d − 2 fausse dès
  d ≥ 3 — remplacée par g = d − max(d, 2), signe inchangé ; (5) trois
  comptes corrigés (3 984 classes ; 28 groupes ν = 5 ; 31 témoins).
  **Prise transverse** : bug ortools 9.15 isolé par V2 (OPTIMAL faux
  sous Minimize + `!=` direct entre expressions liées) — les scripts du
  dépôt n'y sont pas exposés (formulation par variables intermédiaires +
  assert du témoin), mais la réserve T27-S2 §4 en sort renforcée : un
  INFEASIBLE de solveur reste une assertion sans équivalent de
  l'assert-témoin. **Statut du bloc : CONTRE-VÉRIFIÉ** (résidu : les
  optima/INFEASIBLE ν ≥ 5 restent des assertions de solveur, chez les
  vérificateurs comme ici). Pièces : `tasks/done/VER-MC-1.md`.
- **Le plafond est levé (MC-011, 2026-08-07) — les lois comparable et
  (1,1) sont PROUVÉES POUR TOUT o** : une induction sur o remplace le
  lemme de normalisation — trichotomie par extérieur l : lourd
  (restriction x_l := 0 perd ω_l + μ_l ≥ 2), léger à μ_l ≥ 1 (perd
  1 + μ_l ≥ 2), ou tous-légers-μ=0 (le théorème A de MC-010 conclut via
  D_j ≥ o+1 et la convexité). Avec le **LEMME léger ⟹ singleton étendu à
  TOUS les cœurs** (via les zéros u∪{l}, v∪{l} — généralise la
  réparation VER-MC-1). **Sandwich fermé sans condition :
  F(0, b, m, o) = b + 2o + [m ≥ 1] et F(1,1,0,o) = 2 + 2o, théorèmes
  pour tous paramètres** — hors de portée de tout solveur ; le théorème B
  de MC-010 (o ≤ 7, inégalité de recouvrement) est supplanté, la zone
  d'échec (8,5) sort du chemin critique. Le lemme de normalisation
  devient une observation (vraie sur tous les cas testés). **Reste
  ouvert, resserré** : la base incomparable o = 0 (a ≥ 1 au-delà de
  (1,1)) et la branche tous-légers de son induction ; puis fibres
  composées et compression. Réserve : MC-011 est postérieure à VER-MC-1 —
  ses preuves attendent la prochaine passe tierce. Pièces :
  `tasks/done/MC-011.md`, `checks/mc011_induction_o.py`.
  **[Contre-vérifié par VER-MC-2, 2026-08-08 — avec un avertissement
  armé : le lemme singleton est FAUX à m ≥ 1 (21 contre-exemples), tout
  usage futur doit passer par la réduction M d'abord.]**
- **LA PASSE ADVERSE TIERCE n°2 (VER-MC-2, 2026-08-08) — le bloc
  MC-011..013 TIENT : statut CONTRE-VÉRIFIÉ.** Trois vérificateurs
  indépendants (deux re-dérivations complètes des six preuves + une
  triple ré-implémentation : booléens de signe, encodage Möbius, force
  brute) : zéro faille dans les preuves, zéro écart lois/vérité (148
  paires ν ≤ 4 sous trois méthodes, 19 cœurs jusqu'à ν = 7, 5/5
  certificats ν = 8 rejoués), aucun bug de validité dans les scripts —
  et la chaîne d'assemblage trans-fiches (« la couture qui devait
  lâcher ») confirmée : la base vaut pour un séparateur arbitraire, la
  trichotomie est exhaustive via ω_l ≥ 1. Vérifications PLUS FORTES que
  celles du dépôt sur deux points (contre-exemple au lemme singleton
  cherché par solveur jusqu'à ref+4 : INFEASIBLE ; borne interne de la
  branche 3 (1,1) prouvée EXACTE, 3o+2). **Prises, toutes traitées** :
  une correction de consignation (l'« EXACTEMENT la construction
  linéaire » de MC-012 — propriété d'un run, pas des cœurs — corrigée),
  l'avertissement m ≥ 1 (bandeau posé sur MC-011 §1), le prérequis
  ω_l ≥ 1 explicité (MC-013 §3), trois imprécisions mineures. Résidu :
  les INFEASIBLE ν ≥ 5 restent des assertions de solveur ; relecture
  humaine = étalon supérieur. Pièces : `tasks/done/VER-MC-2.md`.
- **La base couronne, partiel structuré (MC-014, 2026-08-08)** : trois
  outils PROUVÉS — (T1) la réduction par tranche vers un point (x_i := 1
  élimine v, la loi G minore : W ≥ b + 1 + a_{{i}} ∀i ∈ A) ; (T2) la
  tranche pleine à DEUX VALEURS PROTÉGÉES (q = p(A∪·) − P_A, poids
  exactement W_B + X, zéros hors {0, Δ = P_B − P_A} — le mécanisme des
  bandes resurgit SANS o) ; (T3) l'identité de comptage
  (W ≤ a+b+1 ⟹ h_A + h_B + R ≤ π + 1). **Cinq régimes du minorant
  F ≥ a+b+2 FERMÉS** — singleton lourd, bloc pur lourd, structure haute,
  et **tout Δ = 1** (E_j ≥ 2 partout + le coin (b = a, W_A = 1) tué par
  collision des singletons de B). **Résidu découpé : Δ = 0 et Δ ≥ 2 sous
  les WLOG accumulés** — et fait mesuré : les six optima extraits vivent
  TOUS à Δ = 0 (W_A = W_B = 1, tout en mixte) : le résidu est l'habitat
  des optima, là où la loi est serrée. Mécanismes candidats nommés :
  système d'échange w_{ij} (Δ = 0), saut au-dessus de Δ (Δ ≥ 2) —
  MC-015. Certificats : 9/9 INFEASIBLE au cap a+b+1 jusqu'à ν = 8.
  Réserve : preuves de session post-VER-MC-2. Pièces :
  `tasks/done/MC-014.md`, `checks/mc014_couronne.py`.
- **Le multi-fibres conditionnel : la condition d'antichaîne est RÉFUTÉE
  à base ≥ 2 (MC-015, 2026-08-08)** — la route-but (fibres composées)
  mesurée à (t, s) = (2, 4), ν = 6 : 4 fibres-points en espace de fibre
  PARTAGÉ, 636 résolutions OPTIMAL, 0 non-conclu. **456/456 affectations
  d'antichaînes sous-additives** (g ∈ {−2 majoritaire, −1}) — la brique
  « fibres sans partage sous condition combinatoire », candidate depuis
  MC-007/008, N'EXISTE PAS en espace partagé ; et l'additivité des
  chaînes du premier passage était un artefact d'alignement (6/24
  affectations seulement, 3 classes × 2, mécanisme OUVERT ; minimum
  g = −3, sous celui des antichaînes). L'image s'INVERSE entre 2 fibres
  (base 1 : seuls les emboîtements partagent — corollaire désormais
  assis sur les lois PROUVÉES, 53/56 cases théorème, volet A) et 4
  fibres (base 2 : les antichaînes partagent toujours). Le seul
  mécanisme d'additivité prouvé reste le sélecteur à blocs DISJOINTS
  (MC-006). **Fait neuf : le déficit est petit et borné** — g ≥ −3
  partout, antichaînes concentrées à g = −2 = t. **Verrou requalifié :
  la LOI DE CROISSANCE du déficit** (si |g| = O(t) ou O(k), la
  totalisation par fibres partagées reste additive à terme contrôlé
  près ; si |g| = Θ(Σ), elle meurt) → MC-016. Pièces :
  `tasks/done/MC-015.md`, `checks/mc015_multifibres.py`,
  `data/mc015_multifibres.md`.
- **La loi de croissance est TRANCHÉE : le déficit croît en s ET en k,
  et le mécanisme est la VALEUR COMMUNE (MC-016, 2026-08-08)** —
  singletons : g = −(s−1) aux 3 points mesurés (s = 4, 5, 6 ; W =
  3s + 1), déficit linéaire en s, fraction constante de Σ ; k = 8 :
  −9 exact (quasi-antichaîne) et **g ∈ [−12, −7] PROUVÉ** (antichaîne
  pleine, ν = 8, intervalle borne-solveur + réalisable — l'instrument
  au plafond). Témoins extraits : les programmes optimaux donnent aux
  points incomparables UNE VALEUR COMMUNE (le mécanisme de MC-003 —
  couvert à valeur exacte — en géométrie de fibres) : **l'antichaîne
  ne bloque pas le partage, elle le PERMET** — le renversement de
  MC-015 est expliqué. Îlots d'additivité observés (chaîne alignée,
  paires quasi-disjointes) du côté disjonction, cohérents avec le
  sélecteur. **Conséquence de route : l'additivité en espace partagé
  est morte à toute échelle — le schéma paie les blocs disjoints
  (MC-006), et le chaînon restant de la route-but est LA COMPRESSION à
  tête symétrique (MC-017 candidate).** Réserves : lois à 3 points,
  grandes échelles à 1 tuple, certificats solveur. Pièces :
  `tasks/done/MC-016.md`, `checks/mc016_croissance.py`,
  `data/mc016_croissance.md`.
- **La base linéaire est fermée au sol (MC-012, 2026-08-07) — THÉORÈME
  F(1, b, 0, 0) = b + 2** : forçage d'égalité (si W ≤ b+1 : c = 1,
  E_j = 1 partout, pas de hauts-B ; puis cascade — c = 1 interdit
  a_j = 1, donc les paires portent tout, donc σ_B = 0, donc
  P_B = 0 = p(∅), collision un/zéro). Corollaires : F(1, b, m, 0) via la
  réduction M, et **b + 2 + o ≤ F(1, b, 0, o) ≤ b + 2 + 2o** par les
  branches 1-2 de l'induction MC-011 — la fermeture complète attend
  l'argument de bandes (deux valeurs protégées) de la branche
  tous-légers. **La frontière ν = 8 franchie pour la première fois** :
  (4,4), (3,5), (2,6) certifiés INFEASIBLE à loi − 1 et faisables à la
  loi (35-58 s) — trois points neufs de C-MC009 au plafond absolu de
  l'instrument ; la base a ≥ 2 reste OUVERTE (la collision-des-singletons
  perd sa prise quand P_A ≥ 2). Les optima (1, b) réalisent exactement
  la construction linéaire. Réserve : postérieure à VER-MC-1 (VER-MC-2 à
  prévoir avec MC-011). Pièces : `tasks/done/MC-012.md`,
  `checks/mc012_base_incomparable.py`.
- **LA LOI LINÉAIRE COMPLÈTE (MC-013, 2026-08-07) — THÉORÈME :
  F(1, b, m, o) = b + 2 + 2o pour tous b ≥ 2, m, o.** La branche
  tous-légers fermée par l'ARGUMENT DES BANDES : en branche 3, les zéros
  du cube {x₁}∪B évitent les deux bandes [c−o, c] et [P−o, P] — le zéro
  ∅ force c, P ≥ o+1, la bande du haut force D_j ≥ o+1 partout, la
  convexité et le comptage E_j donnent W_AB ≥ b + 2o + 1, confortablement
  au-dessus du requis ; l'induction MC-011 + la base MC-012 assemblent.
  **Troisième famille de fibres-points entièrement démontrée** (après
  comparable et (1,1)). Lemme interne testé DIRECTEMENT au solveur
  (bandes par domaines interdits) : 15/15, et fait de structure mesuré —
  le minimum à bandes vaut b + 2 + 2o exactement (la bande simule le
  dehors) ; certificats 8/8 INFEASIBLE jusqu'à ν = 8. **Il ne reste, côté
  lois, que la base couronne (a ≥ 2)** — les forçages 1/3/4 du lemme sont
  déjà généraux, seul le comptage du sol manque ; puis fibres composées
  et compression. Réserve : MC-011/012/013 = trois tâches de preuve
  postérieures à VER-MC-1 — le trou de contrôle est revenu au niveau qui
  avait déclenché la première passe : VER-MC-2 recommandée AVANT la base
  couronne. Pièces : `tasks/done/MC-013.md`, `checks/mc013_bandes.py`.

- **Contre SYM+/ACC⁰ (le régime du fil)** : la sortie 2 de D-001 s'applique —
  Williams, verbatim (pièce du dépôt) : « *there is little evidence that ACC
  contains pseudorandom functions, so natural proofs may not be a barrier for
  ACC after all* ». Une propriété naturelle utilisée contre ACC⁰ n'est pas
  barrée, faute de PRF dans la classe. [CROYANCE STANDARD, documentée]
- **Mais la sortie 1 de Williams ne nous est PAS disponible** : sa preuve
  « n'est pas une propriété de tables de vérité » (diagonalisation) ; la
  nôtre **en est une**, mesurée table par table, et sa largeness est prouvée
  ci-dessus. Si la barrière s'applique un jour, nous n'avons pas cette porte.
- **Contre TC⁰ (l'extension visée par la ligne 7)** : TC⁰ contient les PRF de
  Naor-Reingold (D-001, sourcé) — la barrière RR y mord en plein. [STANDARD]

## 5. Verdict, à maillons étiquetés

> **Le programme de mesure du dépôt, tel qu'il a été mené (contre le format
> SYM+/ACC⁰), n'était PAS barré par les preuves naturelles** — non pas parce
> que la propriété échappe aux critères (elle est LARGE [PROUVÉ], de
> constructivité OUVERTE), mais parce que la classe attaquée ne contient
> vraisemblablement pas de PRF [CROYANCE STANDARD]. Sa vraie limite était le
> plafond polynomial O(k²), déjà consigné (clôture du fil, `echelle_instrument.md`).
>
> **Toute extension du programme à TC⁰ — le verrou même de la ligne 7 —
> rencontrerait RR de face** : la propriété est large par théorème, elle est
> une propriété de tables de vérité (pas de sortie-diagonalisation), et TC⁰
> contient les PRF de Naor-Reingold. Il ne lui resterait qu'UNE échappatoire :
> la **non-constructivité** — c'est-à-dire que calculer W soit dur. Le motif
> MCSP (ligne 13) deviendrait alors la *protection* du programme : ironie
> exacte, la méta-complexité de notre propre mesure décide si notre programme
> est barré. [ANALYSE du dépôt, dérivée de pièces sourcées]

## 6. Ce que ça change pour l'Atlas

- La ligne 7, colonne preuves naturelles, gagne le renvoi à cette cellule :
  la « double sortie » de Williams ne se transmet pas à un programme de
  mesure de tables de vérité — seule la sortie « classe faible » le protège,
  et elle expire à TC⁰.
- Question ouverte engendrée, bien posée et à la portée d'un audit : **quelle
  est la complexité de calculer W(f) ?** (NP-dureté à la Hirahara-Ilango-Loff
  plausible ; même leur technique — réduction depuis χ₁ — a un analogue
  candidat ici.) C'est la première question neuve que le dépôt pose où les
  lignes 7, 13 et 17 se rencontrent. **Prise en charge : MC-001
  (2026-08-02, §3 bis)** — appartenance NP prouvée, deux variantes
  partielles NP-complètes, transposition directe de HIL réfutée (la
  « réduction depuis χ₁ » annoncée ci-dessus comme analogue candidat NE
  marche PAS telle quelle), trois constructivisations évidentes fermées ;
  cas total OUVERT, voie suivante nommée dans `tasks/done/MC-001.md`.

## Références de la cellule

A-007 (`bib/razborov_rudich_1997.md`), D-001 (`williams_vs_rr.md`), A-013
(`tasks/done/A-013.md`), A-015 (`tasks/done/A-015.md`),
`checks/task_d005_largeness.py`, `checks/task_d005_comptage.py`,
distributions exhaustives n = 2, 3, 4 (sorties consignées dans la fiche
`tasks/done/D-005.md`).
