# Candidature n° 6 (prompt v4, 2026-09-08) : « Le programme de Post en complexité — séparer des classes par les propriétés structurelles de leurs ensembles complets (autoréductibilité, mitoticité) » — instruction du Réfuteur (PR-009)

**Verdict : SURVIT — sous conditions, comme LIGNE DOCUMENTAIRE** (la
première de la catégorie créée par le prompt v4). La direction est
absente de la matrice (grep : 0 occurrence d'autoréductibilité, de
mitoticité, de Post), les deux lemmes de lecture sont VRAIS sur le texte
ouvert (arXiv math/9807185), la chaîne est écrite honnêtement (flèche
vers P ≠ NP ABSENTE, déclarée), et la cellule a un contenu que l'Atlas
n'a nulle part : un mécanisme non-relativisant PAR THÉORÈME (Thm 4.1
contre Thm 4.2) dont la portée est **confinée par nature aux écarts de
ressources** — il ne peut séparer que des classes de ressources de
natures différentes (temps/espace, hiérarchie/exponentielle), et P vs NP
oppose deux classes de même ressource. Ce confinement — que la
candidature sous-estime en « à confirmer » — est la prise de
l'instruction, et c'est ce que la cellule doit dire. Deux revendications
de gain sont recalibrées (le « théorème dans les deux sens » est un
win-win standard ; le « troisième mécanisme non-relativisant » est le
second exemplaire de celui que la ligne 1 nomme déjà pour Williams 2025,
via HCC+93), une lecture est corrigée (ligne 5 de la Figure 7), une
nuance est ajoutée (le plafond du moteur positif est O(log n), pas une
constante), et la dormance est datée (2020). Entrée conditionnée à
l'audit fondateur (précédents A-021/A-022).

> **⚠ ADDENDUM MARQUÉ (2026-09-08, règle utilisateur — après la
> question « pourquoi écris-tu SURVIT s'il n'y a pas de flèche vers
> P ≠ NP ? »)** : « une ligne de la matrice devrait exiger au moins une
> flèche OUVERTE vers P vs NP ; les directions à flèche EXCLUE vont au
> registre des éliminations ». Le « SURVIT » ci-dessus portait sur la
> CANDIDATURE (forme v4 irréprochable, lemmes vrais), pas sur la VOIE
> (nulle pour la mission : flèche EXCLUE, prise 1). Conséquence : pas
> de ligne, pas d'audit A-025 ; la direction entre au registre des
> éliminations de la matrice (entrée E-2, avec les deux mécanismes
> transversaux). Verdict réétiqueté : « ENTRE AU REGISTRE DES
> ÉLIMINATIONS ». L'analyse ci-dessous est inchangée.

Contexte : sixième candidature, première sous prompt v4 ; l'en-tête
déclare une dérogation à la règle 1 (candidature interne, comme
PR-005). Procédure CLAUDE.md §5 ; tâche PR-009 déclarée au backlog
avant exécution ; lecture exécutable `checks/pr009_lecture_bfvmt.py`,
verbatims dans `data/pr009_lecture_bfvmt.md`.

## 1. Reformulation (§5.1)

Inscrire dans l'Atlas, comme ligne documentaire, le programme de Post
transposé en complexité (Buhrman-Fortnow-van Melkebeek-Torenvliet,
SICOMP 2000) : séparer deux classes en montrant que tous les ensembles
complets de l'une ont une propriété structurelle (autoréductibilité)
qu'un ensemble complet de l'autre n'a pas ; moteur positif = la
vérifiabilité locale des calculs (EXP et niveaux constants de la
hiérarchie exponentielle), moteur négatif = diagonalisation avec codage
(EEXPSPACE) ; théorème-signature = la Figure 7, où trancher une
question structurelle ouverte sépare des classes quelle que soit la
réponse — sans jamais atteindre P ≠ NP.

## 2. Ce qui tient

- **La forme v4, à la lettre** : cible propre (un théorème de structure,
  pas le problème), chaîne à trois étiquettes avec la flèche ABSENTE
  écrite telle quelle, test du faux raccord rempli (« le mécanisme ne
  sait pas ce qu'est NP ; tout le contenu-NP vient du transfert »),
  plafond déclaré sans avatar (« un ensemble fini est autoréductible par
  table ») et type DOCUMENTAIRE assumé avec sa liste de dix textes.
  C'est la première candidature qui ne laisse au Réfuteur aucun régime
  d'échec constitué à citer.
- **La direction est absente** : grep du dépôt entier — les seuls
  « Buhrman » sont des co-signatures TFNP/MKtP sans rapport ;
  autoréductibilité, mitoticité, Post : 0.
- **Les deux lemmes de lecture sont VRAIS sur le texte** (data §i-ii) :
  (i) la Figure 7 (cinq questions, verbatim) ne contient aucune case
  P ≠ NP — la seule occurrence de « P = NP » du papier est dans la
  preuve du Lemme 5.2, comme conséquence de NP = NL ; (ii) « *we only
  get the proof to work for constant k* » et « *failed to account for
  the growth of the running time when recursively computing previous
  players' moves* » sont dans le texte arXiv (l'erreur est celle de la
  version de conférence [6], FOCS 1995 — la candidature inversait les
  rôles des versions, sans conséquence).
- **Les verbatims-clés existent** : Post's Program (p. 2), l'argument
  d'accès à l'oracle (p. 2, [8] = Fortnow, Bull. EATCS 52, 1994), la
  non-relativisation par théorème (p. 12 : Thm 4.2, et « *applies to any
  complexity class containing EXP that has Property 4.1* »), Thm 3.1,
  4.1, 4.3, 4.4, 4.9, Lemme 5.2, Lemme 5.5.
- **Les barrières relativisation et monotone** : traitées exactement.

## 3. Attaque logique (§5.2) — les prises

### Prise 1 — La flèche absente n'est pas « à confirmer » : elle est STRUCTURELLE, et c'est le contenu de la cellule

La candidature écrit que P vs NP « n'a pas de levier d'effondrement
analogue dans le tableau (à confirmer) ». Le texte permet de trancher
davantage. Le Lemme 5.2 fournit DEUX machines sous NP = NL : M1 (temps
t^{O(c)}) — dont la preuve n'utilise que coNP = NP et NP = P, deux
conséquences de P = NP aussi — et M2 (espace nondéterministe
O(c log t)) — qui utilise P = NL et le padding DTIME ⊆ NSPACE[log].
L'hypothèse MINIMALE du Lemme 5.5, « coNP ⊆ NP ∩ NSPACE[log^{O(1)} n] »,
dit ce que le transfert consomme : une économie d'ESPACE. P = NP n'en
fournit aucune. Toutes les conclusions de la Figure 7 opposent des
ressources de natures différentes (P/PSPACE, NL/NP, PH/EXP, PH/PSPACE,
EXP/EXPSPACE) ; P vs NP oppose deux classes de même ressource. **Le
mécanisme — un écart de ressources entre la réduction (polynomiale) et
le calcul (exponentiel) — est aveugle à toute question posée à
ressources égales.** (Attribution machine par machine : inférence sur la
structure des preuves, à confirmer sur la preuve du Lemme 3.4 à
l'audit.) Conséquence pour l'Atlas : la cellule n'écrit pas « flèche
absente », elle écrit « flèche EXCLUE par le type de ressource » — une
élimination documentée, pas un manque.

### Prise 2 — Le « troisième mécanisme non-relativisant » est le second exemplaire d'un mécanisme que la matrice nomme déjà

La cellule ligne 1 consigne, pour Williams STOC 2025 (A-020), la
non-relativisation « par accès à l'oracle » sourcée à
Hartmanis-Chang-Chari-Ranjan-Rohatgi 1993 ([HCC+93], monde-oracle
TIME^A = SPACE^A, Thm 6, texte ouvert dans
`bib/williams_2025_espace.md`) ; BFvMT citent Fortnow 1994, qui
prolonge HCC+93. C'est la même famille d'explications : la preuve ne
relativise pas parce que les deux côtés n'accèdent pas à l'oracle avec
les mêmes ressources. Réponse à la question d'audit de la candidature :
OUI, même phénomène ; la matrice tient un mécanisme trans-lignes
(1, ligne candidate), à consigner comme tel. Et sa limite est intrinsèque :
l'asymétrie d'accès n'existe qu'entre ressources différentes —
**ce mécanisme ne pourra jamais servir P vs NP**, où les deux côtés
sont polynomiaux. La candidature vend l'atout sans sa borne.

### Prise 3 — « Une cellule d'un type nouveau (le théorème dans les deux sens) » : un win-win standard

Le raisonnement « trancher X, quelle que soit la réponse, sépare » est
le win-win de Kannan 1982 (Σ₂ ⊄ SIZE(n^k) par cas sur NP ⊆ P/poly) et
le « win-win itératif » de Chen-Hirahara-Ren STOC 2024 (déjà en ligne
16). La matrice ne nomme pas « win-win » (grep 0) — c'est une lacune
d'écriture de la matrice, pas un type de cellule nouveau. À consigner
comme MÉCANISME transversal (lignes 1, 16, ligne candidate), pas comme
type.

### Prise 4 — Une lecture corrigée, une nuance ajoutée

(a) Figure 7, ligne 5 : « P ≠ PSPACE » est dans la colonne NON
(Théorème 4.6 : « *a negative answer to the last question implies EXP ≠
EXPSPACE and P ≠ PSPACE* »), pas dans la colonne oui comme l'écrit la
candidature (« aux lignes 2, 4, 5 »). (b) Le plafond du moteur positif
n'est pas « k constant » : Conclusion, verbatim — « *Theorem 4.3 goes
through for k(n) ∈ O(log n). Perhaps one can exploit this leeway in the
coding of Lemma 3.4 and narrow the gap* ». La bande va de O(log n)
alternances à exponentiellement beaucoup (EXPSPACE) : le verrou est un
plafond de méthode à O(log n), et les auteurs nomment eux-mêmes la
marge inexploitée.

### Prise 5 — La dormance est datée, et l'analogie de Post a une histoire

Zhang-Quweider-Lei-Khan, TCS 822 (2020) : mitoticité faible des
ensembles bdtt/bctt-autoréductibles, un ensemble creux de EXP
2-tt-autoréductible non faiblement T-mitotique — la « dormance
2020-2026 » commence en 2020 ; aucune pièce trouvée ne remplit une case
de la Figure 7 [NON TROUVÉ, recherche non exhaustive]. Contexte pour la
cellule (culture générale du Réfuteur, sourcée sur PNAS) : le programme
de Post (1944) a ÉCHOUÉ pour la réductibilité de Turing — le problème
de Post a été résolu par Friedberg et Muchnik (1956-57) par diagonalisation
(méthode de priorité) — puis a été vindiqué en 1991 par Harrington-Soare
(PNAS 88 : une propriété du premier ordre, définissable dans le treillis
des ensembles r.e., garantit l'incomplétude, et un tel ensemble existe).
BFvMT le savent (« *Perhaps another concept from computability theory or
a more artificial property can be used* ») : l'histoire du modèle dit
que les propriétés structurelles ont fini par séparer — 47 ans plus
tard, avec une propriété « artificielle », et pour une séparation déjà
acquise par diagonalisation. C'est exactement la position que BFvMT
déclarent : « *we do not separate any classes not already separable by
known diagonalization techniques* ».

## 4. Barrières (§5.4)

- **Relativisation** : traitée de front et exacte — le moteur positif
  ne relativise pas PAR THÉORÈME (Thm 4.1 vrai, Thm 4.2 : un oracle où
  EXP a un ≤ᵖ_{2-T}-complet non autoréductible ; « *applies to any
  complexity class containing EXP that has Property 4.1* ») ; le moteur
  négatif (diagonalisation) relativise. Mécanisme : accès à l'oracle
  (HCC+93/Fortnow 1994 — même famille que la ligne 1).
- **Preuves naturelles** : sans objet — raison structurelle énoncée
  (ensembles et réductions, aucune propriété de tables de vérité ;
  cibles uniformes). Conforme.
- **Algébrisation** : la candidature la laisse « non tranchée ».
  Argument du Réfuteur (à auditer sur AW 2008 §5, la notion pour un
  énoncé qui n'est pas une inclusion) : l'asymétrie d'accès porte sur
  la LONGUEUR des requêtes (polynomiale contre exponentielle), pas sur
  leur nature algébrique — une extension bas-degré Ã de l'oracle ne
  raccourcit pas les requêtes du calcul exponentiel ; l'énoncé échouant
  déjà avec le MÊME oracle des deux côtés (Thm 4.2), il échoue a fortiori
  avec (A, Ã). Le moteur positif serait donc non-algébrisant — un atout
  réel, avec la même borne : uniquement entre ressources différentes.
- **Monotone** : sans objet. Conforme.
- **Le verrou réel** (pas une barrière, nommé comme tel — règle v4) :
  (i) plafond de méthode du moteur positif à O(log n) alternances
  (récursion sur les coups des joueurs) ; (ii) plancher du moteur
  négatif à EEXPSPACE (Thm 3.1 ; échec pour 2-tt, et en non-uniforme) ;
  (iii) entre les deux, la bande où vivent les cinq questions ;
  (iv) **confinement par type de ressource** : le mécanisme ne sépare
  que des ressources de natures différentes — P vs NP hors de portée
  par construction. Critères (a)/(b) : (a) actif (cellule absente,
  contenu neuf) ; (b) actif — la ligne teste la relativisation par
  théorème et en exhibe la limite.

## 5. Contre-vérification (§5.3) — la lecture exécutable

Pas de sous-lemme fini (déclaré, exact). Les deux lemmes de lecture ont
été exécutés sur le texte ouvert par `checks/pr009_lecture_bfvmt.py`
(extraction pypdf, 25 pages, motifs tolérants à la typographie de
1998) : Figure 7 verbatim (cinq lignes, colonnes oui/non), preuve du
Théorème 5.1, Lemmes 5.2 et 5.5, la note sur la version [6], les
Théorèmes 3.1, 4.1-4.4, 4.9, la Conclusion (O(log n)). Résultats et
verbatims : `data/pr009_lecture_bfvmt.md`. Lemme (i) : VRAI (P ≠ NP
absent ; une case mal placée par la candidature) ; lemme (ii) : VRAI
avec nuance (O(log n)).

## 6. Folklore-check — bilan

Vérifié : BFvMT (texte) ; Harrington-Soare 1991 (PNAS) ; Zhang et al.
2020 (TCS 822) ; HCC+93/Fortnow 1994 (via le dépôt, ligne 1). Non
ouverts dans cette instruction, à l'audit : GOPSZ 2005/2007, GPSZ
2008, GNRSW 2013/2014, Nguyen-Selman 2014, Hitchcock-Shafei 2016/2022,
Beigel-Feigenbaum 1992, Buhrman-Torenvliet 1994, Agrawal-Watanabe 2009,
KMR 1995 / FFK 1996 — la candidature les cite avec précision ; aucun
n'a été contredit ici.

## 7. Verdict (§5.5) et conditions

**SURVIT — sous conditions, ligne documentaire.**

- **Constitué contre la candidature** : deux gains surévalués (prises 2
  et 3) ; une lecture erronée (ligne 5) ; une nuance manquée (O(log n)) ;
  une sous-estimation de sa propre thèse (prise 1 : l'absence est une
  exclusion structurelle) ; une dormance mal datée. Aucun régime
  d'échec.
- **Debout** : la direction absente ; la forme v4 exemplaire ; les
  lemmes de lecture vrais ; les barrières relativisation/monotone
  exactes ; un mécanisme non-relativisant par théorème, dont la
  confinement est le vrai contenu de la cellule.
- **Conditions d'entrée** (précédents A-021/A-022 : une ligne naît de
  son audit) — **audit fondateur A-025** (A-024 étant réservé à la ligne
  circuits généraux, PR-007) sur les dix textes de la candidature PLUS :
  Harrington-Soare 1991 (l'issue du programme de Post) ; Zhang et al.
  2020 (dormance) ; la preuve du Lemme 3.4 (quelle machine du Lemme 5.2
  chaque ligne de la Figure 7 consomme — pour asseoir la prise 1 sur
  texte) ; SICOMP 2000 si accessible (alignement des numéros) ; AW 2008
  §5 pour la colonne algébrisation. **Énoncé de la cellule** : « les
  propriétés structurelles des ensembles complets séparent des classes
  de RESSOURCES DIFFÉRENTES (Figure 7 : P/PSPACE, NL/NP, PH/EXP), par
  un mécanisme non-relativisant par théorème ; P vs NP est hors de
  portée par type de ressource ; verrou = plafond O(log n) du moteur
  positif contre plancher EEXPSPACE du moteur négatif ». **Mécanismes
  transversaux à consigner** : accès à l'oracle (HCC+93 — lignes 1 et
  candidate) ; win-win (Kannan, CHR — lignes 1, 16 et candidate).
- **Refusé** : tout fil atelier (aucun avatar fini — exact) ; et la
  formule « un troisième mécanisme non-relativisant » sans sa borne.
- **Numérotation** : ligne 21 ou 22 selon l'ordre des audits (la ligne
  circuits généraux, PR-007, attend le sien).
- **Leçon pour le prompt (v4.1, sans réécriture)** : les « gains pour
  la matrice » doivent être vérifiés contre les mécanismes que la
  matrice nomme déjà — ajouter au §2 bis la liste des mécanismes
  transversaux consignés (accès à l'oracle, win-win) pour que le
  Proposeur ne les redécouvre pas.

## 8. Pièces et sources

`checks/pr009_lecture_bfvmt.py` ; `data/pr009_lecture_bfvmt.md` ;
`tasks/done/PR-009.md`. Ouverts ici :
[BFvMT, arXiv math/9807185 (v1, 1998)](https://arxiv.org/abs/math/9807185) ;
[Harrington-Soare, PNAS 88 (1991)](https://www.pnas.org/doi/10.1073/pnas.88.22.10242) ;
[Zhang-Quweider-Lei-Khan, TCS 822 (2020)](https://www.sciencedirect.com/science/article/pii/S0304397520302024) ;
dépôt : `bib/williams_2025_espace.md` (HCC+93), `bib/bgs_1975.md`
(Fortnow 1994 cité). Non ouverts : SICOMP 2000 ; les neuf autres textes
de la liste de la candidature (à l'audit).
