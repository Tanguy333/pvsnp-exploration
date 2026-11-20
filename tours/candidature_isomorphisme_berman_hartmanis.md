# Candidature n° 7 (prompt v4.1, 2026-09-10) : « La structure des degrés NP-complets — la conjecture d'isomorphisme de Berman-Hartmanis et l'échelle des réducibilités (Agrawal) » — instruction du Réfuteur (PR-010)

**Verdict : N'ENTRE PAS comme ligne — ENTRE AU REGISTRE DES
ÉLIMINATIONS (E-3).** La candidature satisfait la règle du 2026-09-08 à
la lettre (flèche 1 OUVERTE, flèches 2 et 3 PROUVÉES et numérotées —
tous les numéros vérifiés sur le survey) et déclare elle-même
l'ambiguïté à trancher. L'instruction la tranche ainsi : **la flèche
ouverte est EMPRUNTÉE, pas propre**. Chaque barreau r de l'échelle
implique NP ⊄ r (argument de la Prop. 3.5 relativisé ; le survey
l'écrit pour L : « *any such result will separate NP from L* ») ; le
programme n'est prouvé qu'aux barreaux où la séparation est connue ou
triviale (1-L, NC⁰, AC⁰) et s'arrête là où elle est ouverte (L) ou là
où elle est connue mais la structure manque (AC⁰[2]) ; son auteur
prend P ≠ NP pour obstacle puis pour hypothèse (« *proving the
conjecture is hard because the problem of separating P from NP has
resisted all efforts so far* […] *Can one prove the conjecture assuming
a reasonable hypothesis such as P ≠ NP?* ») ; le seul mécanisme écrit
pour le sommet consomme une fonction à sens unique (Thm 7.1, Cor. 7.5)
et n'atteint que l'isomorphisme P/poly (§8). Le contenu utile à la
cible — la borne inférieure à chaque barreau — appartient aux lignes 4,
11 et 7 ; le mécanisme propre de la famille (théorèmes de structure des
réductions, Cantor-Bernstein polynomial, réductions construites par
OWF) n'ajoute qu'un énoncé PLUS FORT, jamais un chemin. Une famille dont
la seule flèche ouverte est portée par le verrou d'autres lignes n'est
pas une ligne : c'est l'ombre de l'échelle des bornes — l'expression
est de la candidature. **Interprétation de la règle, à valider par son
auteur** : « une flèche OUVERTE » doit s'entendre « ouverte POUR LE
MÉCANISME de la famille (champ 4b) » ; sinon toute conjecture plus forte
que P ≠ NP (IC, NP ⊄ P/poly, TFNP ≠ FP…) vaudrait ligne par simple
force. Si l'utilisateur lit la règle à la lettre, l'issue est une ligne
conditionnée à un audit fondateur (A-026, les dix textes de la
candidature) — l'analyse ci-dessous vaut dans les deux cas.

Contexte : septième candidature ; prompt v4.1 ; en-tête déclarant une
dérogation à la règle 1 (candidature interne, précédents PR-005 et
PR-009). Tâche PR-010 déclarée au backlog avant exécution ; lecture
exécutable `checks/pr010_lecture_agrawal.py`, verbatims dans
`data/pr010_lecture_agrawal.md`.

## 1. Reformulation (§5.1)

Inscrire dans l'Atlas le programme d'Agrawal : gravir l'échelle des
réducibilités r en prouvant, pour chaque r, que la complétude force la
structure (réductions 1-1, croissantes en taille, inversibles sur
l'image — le r-Complete Degree Conjecture) par un théorème de structure
des fonctions r-calculables ; au sommet r = P, la conjecture équivaut à
la conjecture d'isomorphisme de Berman-Hartmanis (Prop. 6.19), qui
implique P ≠ NP (Prop. 3.5) ; mécanisme conjecturé du sommet :
OWF 2^{n^ε}-sûre + conjecture du cylindre facile ⟹ isomorphisme
P/poly (Cor. 7.5).

## 2. Ce qui tient

- **La forme v4.1, à la lettre** : cible propre, chaîne à trois
  étiquettes avec numéros, test du faux raccord rempli (« sous le
  sommet, le mécanisme ne distingue pas NP ; ce qu'il distingue est C de
  r »), plafond déclaré sans avatar, type documentaire, ambiguïté
  déclarée d'avance avec l'issue E-3 nommée. Aucun régime d'échec.
- **La direction est absente** (grep : Berman/Mahaney/Kurtz/paddable
  absents de l'atlas et du cahier, présents seulement en bib comme
  citations) ; « isomorph » dans l'atlas = CFI (ligne 9), sans rapport.
- **Tous les numéros cités existent** (data) : Props 3.5, 4.1, 6.19 ;
  Thms 6.3, 6.4, 6.15, 6.16, 6.20, 7.1 ; Cor. 7.5 ; Easy Cylinder
  Conjecture ; objection de Goldreich ; les trois questions du §8 ;
  Thms 4.4 (KMR) et 4.5 (FFK). Rogers 1997 existe (JCSS 54(3):412-423)
  bien qu'absent du survey.
- **La distinction d'avec E-2 est exacte** : le transfert est
  l'argument des ensembles finis, il atterrit exactement sur P ≠ NP ; ce
  n'est pas un écart de ressources.

## 3. Attaque logique (§5.2) — les prises

### Prise 1 — La flèche ouverte est empruntée : l'échelle est l'ombre des bornes, et son auteur le dit

(a) *Barreau r ⟹ NP ⊄ r.* L'argument de la Prop. 3.5 se relativise :
si NP ⊆ r, un ensemble fini non trivial est r-complet et aucune
réduction 1-1 croissante ne l'atteint (vérifié à la main ; forme
générale [NON TROUVÉE dans le survey] ; cas L verbatim : « *does not
yield unconditional results as any such result will separate NP from
L* »). (b) *Où l'échelle est prouvée.* Exactement aux barreaux où la
séparation est acquise ou triviale : 1-L, 1-NL, 2-DFA, NC⁰, AC⁰
(Thm 6.20) — et par les OUTILS des bornes (lemme de switching pour le
gap AC⁰ → NC⁰, Thm 6.16). (c) *Où elle s'arrête.* Au barreau L, parce
que NP ≠ L est ouvert (verbatim) ; au barreau AC⁰[2], où NP ⊄ AC⁰[2]
est CONNU (Razborov-Smolensky) mais la structure manque — la seule
question propre de la famille (§8, première question) ne déplace donc
rien sur la cible. (d) *Le sommet.* « *Proving this, of course, is hard
as it implies P ≠ NP (Proposition 3.5). Can we prove this under a
reasonable assumption?* » — le programme prend P ≠ NP (via une OWF)
pour HYPOTHÈSE ; son mécanisme écrit (Thm 7.1 → Cor. 7.5) consomme une
OWF et n'atteint que P/poly (§8 : « *the Isomorphism Conjecture is true
only for P/poly-reductions* »). Conclusion : le contenu de chaque
barreau utile à la cible est la borne inférieure correspondante —
l'objet des lignes 4 (AC⁰[p]), 11/7 (TC⁰) ; le mécanisme propre de la
famille (structure, Cantor-Bernstein, OWF) n'ajoute que de la force.
**La flèche 1 est OUVERTE par emprunt** : elle est ouverte parce que
NP ⊄ P est ouvert, et rien dans la famille ne la fermerait sans que les
autres lignes l'aient fermée d'abord. La candidature le sait (« un
renforcement du programme des bornes, jamais un raccourci » ; « l'échelle
structurelle comme ombre de l'échelle des bornes ») — elle a préféré la
lettre de la règle ; l'instruction applique son esprit.

### Prise 2 — « Une conjecture et sa rivale renforcent toutes deux P ≠ NP » : une moitié est triviale

L'Encrypted Complete Set Conjecture énonce l'existence d'une fonction à
sens unique (« *There exists a 1-1, size-increasing, one-way function f
such that…* ») ; la Prop. 4.1 est donc « OWF ⟹ P ≠ NP » habillée
(preuve : sous P = NP toute fonction 1-1 croissante est inversible).
Le « fait structurel rare (1) » de la candidature — le monde P = NP est
celui où les deux sont fausses — est exact, mais son intérêt se réduit
à : IC ⟹ P ≠ NP (Prop. 3.5). Le vrai contenu structurel est ailleurs :
le survey soutient que les résultats aux barreaux faibles « *raise
doubts about the intuition behind the Encrypted Complete Set
Conjecture* » (toute fonction AC⁰ 1-1 croissante a un sous-ensemble
dense inversible) — un argument POUR IC, dont la candidature ne dit
rien.

### Prise 3 — Le barreau TC⁰ est une construction de la candidature, et la lecture RR est héritée, pas propre

TC⁰ : 0 occurrence dans le survey ; l'échelle d'Agrawal s'arrête à la
question AC⁰[2]. La candidature construit le barreau TC⁰ et le lit
« RR-lié par les PRF de Naor-Reingold ». C'est correct mais pas neuf ni
propre : un barreau r implique NP ⊄ r, donc toute preuve du barreau TC⁰
contient une preuve non-naturelle de NP ⊄ TC⁰ — la barrière est
HÉRITÉE du corollaire borne inférieure, exactement comme pour la ligne
11/7. « RR relu sur les réductions » est un renommage de « RR hérité
par implication ». Mécanisme transversal à consigner sous ce nom
exact.

### Prise 4 — Rogers, quatre mondes, et ce que le profil de relativisation dit vraiment

Le survey donne TROIS mondes (HH : les deux conjectures fausses, P = UP ;
KMR : la rivale vraie, oracle aléatoire ; FFK : IC vraie) ; la
candidature en cite un quatrième hors survey (Rogers 1997 : IC vraie +
OWF — vérifié : JCSS 54(3), « *every paddable 1-li-degree collapses to
an isomorphism type* »). Le profil est exact et il dit une chose
simple : aucune des deux conjectures n'est décidable par relativisation
— ce qui, pour une conjecture qui IMPLIQUE P ≠ NP, est la conséquence
attendue de BGS, pas un atout de la famille. Le mécanisme de l'échelle
« ne relativise pas parce qu'il ouvre le circuit » : vrai au barreau AC⁰
— c'est la non-relativisation des bornes AC⁰ (switching), héritée elle
aussi.

### Prise 5 — Dormance et vent contraire, confirmés

Dernier barreau : AC⁰ uniforme (Agrawal, JCSS 2011) ; question AC⁰[2]
posée en 2009 ; [NON TROUVÉ] 2012-2026 sur AC⁰[2]/TC⁰ (recherche non
exhaustive) ; apparentés 2018-2022 (Hitchcock-Shafei, non uniforme).
« *Most complexity theorists now believe the isomorphism conjecture is
false* » (secondaire) — ce n'est pas une exclusion (FFK, Rogers), mais
pour l'Atlas cela signifie qu'un programme dormant dont la communauté
tient la cible pour fausse ne peut pas être « la bonne voie ».

## 4. Barrières (§5.4)

- **Relativisation** : profil à quatre mondes exact (prise 4) ; la
  non-relativisation des barreaux prouvés est celle des bornes (AC⁰).
- **Preuves naturelles** : héritée par implication (barreau r ⟹ NP ⊄ r)
  — AC⁰[2] dernier barreau RR-libre, TC⁰ RR-lié (Naor-Reingold, seuil
  que la cellule 7 nomme déjà) ; la candidature le dit sous un autre
  nom.
- **Algébrisation** : le sommet exige du non-algébrisant (IC ⟹ P ≠ NP,
  témoin AW) — héritée aussi ; le barreau AC⁰[2] emploierait la méthode
  polynomiale (ligne 4) — non tranchée, et sans conséquence pour la
  cible (NP ⊄ AC⁰[2] est connu).
- **Monotone** : sans objet — conforme.
- **Le verrou réel** : pas une barrière — l'absence de théorème de
  structure pour AC⁰[2] (« gap » inexistant, 15 ans) ; puis, au-delà,
  le verrou des lignes 4/11/7 lui-même. Critères (a)/(b) : (a) actif
  (direction absente, entrée de registre) ; (b) actif — la ligne
  exhibe comment les barrières se transmettent par implication.

## 5. Contre-vérification (§5.3) — la lecture exécutable

Pas de sous-lemme fini (déclaré, exact : une réduction finie se
simplifie trivialement). Les lemmes de lecture ont été exécutés sur le
survey ouvert (23 pages) : (i) VRAI en substance (argument des ensembles
finis ; cas L verbatim ; forme générale non écrite) ; (ii) [NON
TROUVÉ] — aucun barreau au-dessus d'AC⁰ depuis 2011, TC⁰ absent du
survey ; (iii) question de recherche, [OUVERT]. Tous les numéros cités
sont exacts. Détail : `data/pr010_lecture_agrawal.md`.

## 6. Folklore-check — bilan

Vérifié : survey Agrawal (texte) ; Rogers 1997 (existence, énoncé) ;
absence de résultats 2012-2026 sur AC⁰[2] (non exhaustif). Non ouverts,
sans besoin (pas d'audit) : BH 1977, Mahaney 1982, AAR 1998, AAIPR
2001, Agrawal 2011, JY 1985, KMR 1995, FFK 1996, AW 2009, HHP,
Hitchcock-Shafei 2018/2022 — cités avec précision par la candidature ;
aucun contredit.

## 7. Verdict (§5.5) et suites

**N'ENTRE PAS comme ligne — ENTRE AU REGISTRE DES ÉLIMINATIONS (E-3).**

- **Constitué** : flèche 1 ouverte par emprunt (prise 1 — la charge
  décisive) ; moitié triviale du « fait rare » (prise 2) ; barreau TC⁰
  et « RR sur les réductions » = constructions et renommages d'un
  héritage (prise 3) ; profil de relativisation exact mais sans atout
  (prise 4) ; dormance et vent contraire (prise 5). Aucun régime
  d'échec du prompt.
- **Debout** : la forme ; la direction absente ; les numéros ; la
  distinction d'avec E-2 ; l'honnêteté de « jamais un raccourci ».
- **Entrée E-3** avec trois mécanismes transversaux : « l'ombre »
  (une conjecture de structure au-dessus d'une séparation — barreau
  r ⟹ NP ⊄ r, IC ⟹ P ≠ NP — dont le programme prend la séparation pour
  hypothèse) ; « la barrière héritée par implication » (RR, AW) ; « le
  profil de relativisation d'une conjecture et de sa rivale » (quatre
  mondes).
- **Si l'utilisateur lit la règle à la lettre** : ligne conditionnée à
  A-026 (les dix textes de la candidature + Rogers 1997 + Computability
  in Context 2011 pour la numérotation) — l'instruction ne le recommande
  pas : le seul contenu de la ligne utile à la cible serait recopié des
  lignes 4/11/7.
- **Leçon pour le prompt (v4.2, sans réécriture immédiate)** : préciser
  au champ 3 que « OUVERTE » se juge pour le mécanisme du champ 4b —
  une flèche ouverte parce que la cible l'est n'est pas une flèche de
  la famille.

## 8. Pièces et sources

`checks/pr010_lecture_agrawal.py` ; `data/pr010_lecture_agrawal.md` ;
`tasks/done/PR-010.md`. Ouverts : [Agrawal, The Isomorphism Conjecture
for NP (IITK, 2009)](https://www.cse.iitk.ac.in/users/manindra/survey/Isomorphism-Conjecture.pdf) ;
[Rogers, JCSS 54(3), 1997](https://dl.acm.org/doi/10.1006/jcss.1997.1486)
(existence et énoncé, via recherche). Non ouverts : les autres textes
de la liste de la candidature.
