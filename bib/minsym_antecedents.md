# MC-002 — Antériorité de « MinSYM+ est-il NP-complet ? » : vérification bibliographique systématique

> Tâche type A, exécutée le 2026-08-07 (la réserve n°1 de MC-001 l'exigeait
> avant toute suite du front). Dispositif : quatre lignes de recherche en
> parallèle — (1) threshold logic / synthèse logique, (2) méta-complexité /
> MCSP, (3) aval de Beigel-Tarui / communication, (4) frappe directe par
> phrases exactes + compendiums — chacune sous la règle stricte : toute
> citation provient d'un document OUVERT (page arXiv/ECCC/DOI/dblp/PDF
> extrait), jamais d'un snippet de moteur ; abstract seul → déclaré.
> Moteurs : WebSearch, dblp API, arXiv (métadonnées), ECCC (pages mot-clé et
> auteurs — la recherche native est en 404), OpenAlex, Semantic Scholar
> (Google Scholar inaccessible : CAPTCHA). ~50 requêtes documentées dans les
> quatre rapports.

## 1. Verdict global

**[NON TROUVÉ], sur les quatre lignes.** Personne n'a posé, encore moins
classé, la minimisation depuis la table de vérité d'une forme profondeur-2 à
**tête symétrique** sur des AND — ni pour la taille, ni a fortiori pour le
poids W(f) à monômes positifs et ensembles de valeurs disjoints. La question
« MinSYM+ est-il NP-complet ? » tombe dans le no man's land entre :

- la ligne **MCSP-restreint**, arrêtée au sommet OR — Masek 1979 (Min-DNF),
  AHMPS 2008, Hirahara-Oliveira-Santhanam CCC 2018 (OR∘AND∘MOD_m),
  Ilango FOCS 2020 (formules profondeur d) ;
- la ligne **méta-communication**, arrêtée à 2 joueurs — Kushilevitz-Weinreb
  2009 (crypto-dur), HIL CCC 2021 (rondes constantes), HIL 2025 (CC NP-dur),
  et un unique concurrent 2025-2026 (§2.6), toujours sur CC.

MC-001 reste donc une question de preuve, pas un audit ; ses Th.2/Th.3 sont
des instances **non publiées** d'un motif **établi** (§3.1).

## 2. Les frontières établies (documents ouverts, verbatims)

### 2.1 Depuis la table, tête OR — le plancher du paysage

- **Masek 1979 / AHMPS** (ECCC TR05-126, SICOMP 2008,
  <https://eccc.weizmann.ac.il/report/2005/126/>) : Min-DNF NP-complet
  (« *the proof was never published* » — la preuve simple est dans AHMPS),
  inapproximable à (log N)^γ ; « *the fundamental computational problem,
  Min-R, asks for the minimum R-size of a boolean function presented as a
  truth table* ». Renforcé par Khot-Saket (n^ε).
- **Hirahara-Oliveira-Santhanam CCC 2018** (LIPIcs,
  <https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CCC.2018.5>) —
  **le parent structurel le plus proche de MinSYM+** : « *For every m ≥ 2,
  given the truth table of a function f : Z_m^n → {0,1}, it is NP-hard under
  polynomial-time deterministic many-one reductions to determine the size of
  the smallest OR∘AND∘MOD_m circuit C that computes f, where circuit size is
  measured as the top fan-in of C.* » Tête OR, mesure top fan-in (non
  pondérée). **La tête seuil n'y est qu'une extension spéculative** : « *it
  might be possible to extend our techniques to classes such as
  THR∘AND∘MOD and depth-3 AC0 circuits of small bottom fan-in* » — jamais
  réalisée depuis (vérifié 2018-2026). SYM n'est mentionné nulle part.
- **Ilango FOCS 2020** (version FOCS ouverte) : (AC⁰_d)-MCSP NP-dur sous
  réductions **Turing randomisées quasi-poly** pour tout d ≥ 2 ; MCSP⋆
  (table à ⋆) hors P sous **ETH** (déterministe). Têtes AND/OR seulement.
- **Allender, survey LATA 2020**
  (<https://people.cs.rutgers.edu/~allender/papers/lata.pdf>) : le trou
  nommé par la communauté est la profondeur 3 (« *it remains unknown what
  the complexity is of finding the smallest depth-three circuit* ») — pas la
  profondeur 2 symétrique, qui n'est nommée nulle part.

### 2.2 Versions partielles — le motif est ANCIEN et général

- **Levin 1973** : DNF-MCSP∗ était le **2ᵉ problème NP-complet de son papier
  fondateur** (verbatim via Hirahara TR22-119 : « *Levin's seminal paper
  [Lev73] presented six NP-complete problems; the second problem shown to be
  NP-complete was DNF-MCSP∗* »).
- **Points listés** : NP-complet pour les circuits généraux depuis
  **Hancock-Jiang-Li-Tromp 1996** et **Alekhnovich et al. 2008** — Ilango
  FOCS 2020, verbatim : « *it is known that the input/output pair
  representation version of MCSP⋆ is NP-complete [17], [18]. However, this
  result makes use of the succinctness of the input representation* » ;
  Ilango-Loff-Oliveira CCC 2020 (Def. 2 = le format points listés) :
  « *previous works in learning theory [HJLT96, ABF+08] implicitly contain a
  substantially simpler proof that Partial-MCSP is NP-hard, even under
  deterministic reductions.* »
- **Table complète à ⋆** : NP-dureté par **Hirahara FOCS 2022** (TR22-119,
  <https://eccc.weizmann.ac.il/report/2022/119/>) sous réductions
  **randomisées** : « *MCSP∗, NC1-MCSP∗, MKTP∗, and MINKT∗ are NP-hard under
  randomized polynomial-time reductions. Moreover, these problems are
  NP-hard to approximate within a factor of (log N)^ϵ* ». Barrière notée :
  Kabanets-Cai — dureté déterministe « naturelle » de MCSP(∗) ⟹
  EXP ⊄ P/poly.
- **La liste Simons 2023** (« Meta-Complexity Open Problems », PDF ouvert)
  nomme Formula-MCSP∗ (Problems 5-6) et AC⁰-Circuit-MCSP∗ (Problem 8) —
  **rien en profondeur-2 symétrique** parmi les 15 problèmes.

### 2.3 Tête seuil / symétrique — uniquement crypto ou spéculatif

- **Min-TC⁰** (AHMPS, TR05-126) : « *Under cryptographic assumptions, it is
  known that Min-Circuit, Min-NC1 and Min-TC0 are not polynomial-time
  solvable [2]. (Nothing is stated explicitly in [2] regarding Min-TC0, but
  it is implicit.) […] This still leaves open the interesting question of
  whether or not [they] are NP-complete.* » — la seule trace « minimisation
  à tête seuil depuis la table » de toute la littérature : crypto-dure,
  NP-complétude OUVERTE depuis 2005.
- **Hansen-Podolskii CCC 2010** (« Exact Threshold Circuits », PDF ouvert,
  texte intégral vérifié) : zéro occurrence de minimisation/synthèse/table —
  bornes inférieures et structure de classes uniquement.
- **Densité PTF depuis la table** : uniquement des heuristiques et bornes
  (Oztop 2009 — 0,75·2ⁿ, connu par snippets seulement, paywall ;
  arXiv:1504.01167, génétique) ; la page ECCC mot-clé PTF (11 rapports
  2012-2018) ne contient aucune minimisation-depuis-table. Aucun théorème de
  complexité publié.

### 2.4 Entrée-formule (régime différent, NE PAS confondre)

- **Buchfuhrer ISAAC 2008** (PDF auteur ouvert) : la minimisation **SPP**
  (= OR∘AND∘XOR, entrée = FORMULE) est **Σ₂ᵖ-complète** sous réductions
  Turing. Régime au-dessus de NP, incomparable au régime table (MinSYM+ ∈
  NP) — utile comme contraste, pas comme antériorité.
- **Threshold logic classique** (Muroga 1971, Winder 1962, Dertouzos 1965 —
  non ouverts, paywall/épuisés ; caractérisés par les surveys CAD ouverts,
  Zhang et al. DATE 2004 et Neutzling et al. TCAD 2018) : LP, tabulation,
  énumération, ≤ 10 variables — **procédural, antérieur à la théorie de la
  NP-complétude, aucun théorème de dureté**. Symptôme du champ CAD : Zhang
  2004 « prouve » sa dureté par « *Since ILP is NP-complete, our synthesis
  problem is NP-complete in theory* » — un non-sequitur.

### 2.5 ESOP / AND-XOR — la distinction positif/littéraux est connue, la classification absente

- **Riener-Ehlers-Schmitt-De Micheli 2018** (arXiv:1807.11103, ouvert) :
  « *Finding ESOP forms with a small or a minimum number of product terms is
  hard and numerous exact and heuristic synthesis methods have been
  proposed* » — « hard » au sens pratique ; **aucune preuve de NP-dureté ni
  problème ouvert formellement posé** n'a été trouvé pour Min-ESOP depuis la
  table. État de l'art exact : n ≤ 8.
- **Le cas positif est canonique et trivial** — la hiérarchie AND-EXOR le
  sait : « *A PPRM is an AND-EXOR expression without any negative
  literals* », « *The FPRM of f is uniquely obtained if the polarity vector
  is given* » (Hirayama et al. 2001, PDF ouvert) — PPRM = ANF, unique. Toute
  la difficulté ESOP vient des littéraux/polarités. **Ceci confirme
  l'asymétrie utilisée par le dépôt** (F-019 : sparsité ANF poly(N)) et
  éclaire MinSYM+ : à tête XOR le cas positif est facile par UNICITÉ ; à
  tête SYM libre l'unicité disparaît — c'est là que vit la question.

### 2.6 Méta-communication — la famille active la plus proche (2021-2026)

- **HIL CCC 2021** (TR21-030, DROPS ouvert) : la question méta posée en
  toutes lettres dès 2021 — « *How difficult is it to compute the
  communication complexity of a two-argument total Boolean function […] ?
  In 2009, Kushilevitz and Weinreb showed that this problem is
  cryptographically hard, but it is still open whether it is NP-hard. In
  this work, we show that it is NP-hard to approximate the size (number of
  leaves) of the smallest constant-round protocol* ».
- **HIL 2025** (arXiv:2507.10426 / TR25-094, pièce A-015 du dépôt) : CC(f)
  NP-dur. Texte intégral re-vérifié : **aucune** occurrence de
  multiparty/NOF/k-players — l'extension multipartie n'existe pas
  (« *abs:"number-on-forehead" AND abs:"NP-hard"* » → 0 résultat arXiv).
  Le pont Håstad-Goldmann « taille SYM∘AND ↔ coût NOF » n'a AUCUN analogue
  méta côté NOF.
- **PIÈCE NEUVE — le concurrent** : **Gaspers-He-Mackenzie**,
  « NP-Completeness of Deterministic Communication Complexity via Relaxed
  Interlacing », arXiv:2508.05597 (v1 : 2025-08-07 ; v4 : 2026-04-13 ;
  87 p.) — revendique la NP-**complétude** (pas seulement la dureté) de CC
  déterministe depuis la table, par réduction depuis {0,1}-Vector Bin
  Packing, cadre issu de Mackenzie-Saffidine STOC 2025 (réfutation de la
  direct-sum conjecture). Se déclare « *Independent concurrent work* » de
  HIL. **Précautions** : préprint sans venue ; le commentaire v4 avoue
  « *The previous lower-bound inheritance step (Lemma 6 in v3) was too
  strong as stated* ». → Candidate pour la cellule 17 à la prochaine passe
  de veille, avec ces réserves.
- **Loff-Milovanov** (TR24-034, STACS 2025) : dureté de la decision tree
  complexity — NC¹-dur depuis la table, PSPACE-dur depuis un circuit.

### 2.7 Autres voisins vérifiés

- **Représentation Z_m** : unique (interpolation) — le degré mod m depuis la
  table est trivialement poly(N) ; la question non triviale (degré FAIBLE,
  Tardos-Barrington/Grolmusz) n'a aucune étude de complexité. [NON TROUVÉ]
- **Compendiums** : MINIMUM TEST COLLECTION [SP6] (séparation par incidence
  0/1, sans poids ni sommes) est le plus proche parent classé — pas le même
  objet. Set Basis [SP7]/Stockmeyer : non vérifié sur document ouvert.
- **NMF exacte** (Vavasis, arXiv:0708.4149) : NP-dureté du rang non négatif
  — famille « poids positifs sur atomes rang-1 », mais égalité exacte, pas
  ensembles de valeurs disjoints.
- **Direction table → circuit** : la seule existante est la compression par
  preuves naturelles (CIKK CCC 2016, TR16-008), plafonnée à AC⁰[p] —
  ACC⁰/SYM∘AND exclu. Direction circuit → SYM∘AND : état de l'art
  Chen-Papakonstantinou FOCS 2016 (TR16-085, 2^{(log n)^{O(d)}}), jamais
  depuis une table.
- **Métadonnées arXiv « SYM+ circuits »** : 2 papiers (Karchmer 2311.06690,
  apprentissage agnostique ; Williams 1401.2444, bornes THR) — aucun sur la
  minimisation.

## 3. Conséquences pour le dépôt

1. **MC-001, Th.2/Th.3 — ancrages d'antériorité du MOTIF** (à citer dans
   toute reprise) : le phénomène « les versions partielles/listées de la
   minimisation sont NP-dures » date de Levin 1973 (DNF-MCSP∗) et, pour les
   points listés, de HJLT96/ABF+08 (circuits généraux, réductions
   déterministes). Nos Th.2/Th.3 en sont des instances **non publiées pour
   la classe SYM+ pondérée** — la valeur ajoutée est l'identification
   exacte (= Set Cover à valeur exacte ; = Min-DNF(∗)) et le blocage du zoo
   par construction, pas le phénomène. La fiche MC-001 disait « aucune
   revendication de nouveauté » : c'est désormais sourcé.
2. **Le folklore-check de MC-001 passe de « 8 requêtes web » à
   « vérification systématique »** : [NON TROUVÉ] confirmé. Réserve
   résiduelle : un folklore non publié (communauté synthèse logique/EDA, où
   l'entrée est une formule, pas une table) reste possible ; Muroga 1971 et
   UVSV 2006 n'ont pas pu être ouverts.
3. **LE GABARIT STRATÉGIQUE — HOS18, pipeline complet partiel → total** :
   Th. 8 ((DNF∘MOD_m)-MCSP∗ NP-dur via r-Bounded Set Cover — l'analogue de
   notre Th.2) → Th. 16 (réduction randomisée zero-error de MCSP∗ vers MCSP
   TOTAL, coût contrôlé par |f⁻¹(∗)|) → Th. 24 (dérandomisation par PRG).
   **C'est l'étape Th. 16 qui nous manque** : son transfert à la tête SYM
   pondérée — ou l'obstruction que le zoo y oppose — est la question
   précise du front. Candidate d'audit dédié (backlog [auto]).
4. **Notre régime déterministe est cohérent avec le paysage** : les classes
   restreintes à la Masek/HOS18 admettent des duretés déterministes
   many-one ; c'est le MCSP général qui bute sur Kabanets-Cai (et exige du
   randomisé, Hirahara 2022). Rien n'interdit une NP-complétude déterministe
   de MinSYM+.
5. **Pièces pour d'autres cellules** : Gaspers-He-Mackenzie 2508.05597
   (cellule 17, avec réserves v3→v4) ; HIL CCC 2021 (rondes constantes) et
   Loff-Milovanov TR24-034 (arbres de décision) — contexte de la famille
   « mesure-depuis-la-table » de la cellule 17.

## 4. Réserves globales

- **Non ouverts** (paywall/épuisés) : Muroga 1971, Winder 1962, Dertouzos
  1965 (caractérisés par surveys CAD ouverts) ; UVSV TCAD 2006 (scan sans
  texte) ; Oliveira-Sangiovanni LSAT ICCAD 1991 ; Oztop 2009/2015 ;
  Håstad-Goldmann, Razborov-Wigderson, BGKL, Grolmusz, Chattopadhyay-Mande,
  Kushilevitz-Weinreb (métadonnées/abstracts relayés seulement) ; version
  SICOMP d'Ilango 2020 (la version FOCS 10 p. a été lue).
- **Moteurs** : Google Scholar inaccessible (CAPTCHA) — les négatifs de
  phrases exactes reposent sur WebSearch/dblp/arXiv-métadonnées/OpenAlex
  (guillemets non honorés en fulltext) ; la recherche native ECCC est en
  404 (contournée par pages mot-clé/auteurs) ; un hit enfoui dans un plein
  texte non indexé resterait invisible.
- **Une absence de publication ne se prouve pas** — le négatif est daté :
  2026-08-07.
- Compteurs de citations (S2 = 0, OpenAlex = 0 pour arXiv:2507.10426)
  démontrés en retard : le PDF de 2508.05597 cite bien HIL. Ne pas utiliser
  ces zéros comme preuve d'absence de suites.

## 5. Rapports sources

Les quatre rapports d'agents (verbatims complets, tables requête → source →
résultat) sont archivés dans les sorties de session du 2026-08-07 ; ce
document en est la synthèse contre-vérifiée. Toute reprise d'une citation
doit se faire depuis le document primaire (URL ci-dessus), pas depuis cette
note.
