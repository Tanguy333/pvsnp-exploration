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
