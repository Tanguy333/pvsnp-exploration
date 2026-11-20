# Candidature n° 9 (prompt v4.4, 2026-09-12) : « L'apprentissage de classes de circuits ⟹ bornes inférieures — la face algorithmique des preuves naturelles » (présentée comme entrée de registre E-5) — instruction du Réfuteur (PR-014)

**Verdict : ENTRE AU REGISTRE (E-5) — avec deux précisions de théorème
et une prise d'instrument.** La candidature est la première instruite
sous le prompt v4.4 et la deuxième présentée d'emblée comme entrée de
registre. Son quadruplet (M, G, T, S) est correctement rempli et ses
théorèmes sont TOUS vérifiés sur texte (OS17 Th. 2, 3, 8, 9, 12, 13,
16, 17 ; CIKK Th. 1.1, 1.2 et la phrase ACC⁰ ; Williams 2016 Th. 1.1,
1.2, 1.7) ; son statut de G à trois étages — emprunté à ACC⁰, miroir au
niveau NEXP, exclu sous crypto dès TC⁰ — tient. Ce que l'instruction
corrige : (1) « G est PAR THÉORÈME une propriété naturelle » est un
raccourci qui confond OS17 Th. 8 (apprentissage ⟺ distingueurs à erreur
BORNÉE) et Th. 9 (preuves P-naturelles ⟺ distingueurs SANS erreur) —
les flèches exactes sont : naturel ⟹ apprentissage (CIKK Th. 1.1, un
sens) ; apprentissage ⟺ distingueur à erreur bornée (Th. 8) ; miroir =
Williams Th. 1.2 (constructif + utile, la densité en moins) ; exclusion
= Th. 2 avec ses réserves verbatim (« *requires non-uniformity, and is
established only in the exponential security regime* ») ; (2) la
cellule discriminante du sous-lemme est MIS-SPÉCIFIÉE : à n = 8, MOD₆
vaut 1 sur 29 points sur 256, et le polynôme constant atteint 227/256 ≥
7/8 — « adeg ≥ 3 » est faux tel qu'écrit, le seuil ε = 1/8 est vide par
déséquilibre (leçon d'instrument, versée au prompt) ; la moitié exacte
du témoin (degrés, Fourier, n = 12) est conforme et suffit au régime de
contrôle. Mécanismes transversaux versés : (8) le triangle
naturel / apprentissage / distingueur, avec ses flèches exactes ; (9)
l'échelle algorithmique RR-exposée — la vraie contribution de l'entrée :
elle dit POURQUOI la ligne 7 esquive RR (Williams Th. 1.2 : une borne
NEXP n'exige que constructivité et utilité) et pourquoi l'apprentissage
ne l'esquive pas (Th. 8 : apprendre, c'est distinguer les fonctions de C
des fonctions aléatoires — la densité est dans la définition).

Contexte : neuvième candidature ; en-tête déclarant une dérogation à la
règle 1 (candidature interne, précédents PR-005/009/010/011). Tâche
PR-014 déclarée au backlog avant exécution ; instrument
`checks/pr014_apprentissage_degres.py`, données
`data/pr014_apprentissage_degres.md` ; textes ouverts : OS17 (arXiv
1611.01190, 51 p.), CIKK16 (LIPIcs CCC 2016, 24 p.), Williams 2016
(arXiv 1212.1891 v3) — extraits et grepés.

## 1. Reformulation (§5.1)

Inscrire au registre la direction « apprendre une classe de circuits C
pour la séparer » : M = les apprenants par concentration de Fourier (LMN,
Jackson) ou par approximation polynomiale sur F_p (CIKK, lecture
algorithmique de Razborov-Smolensky) — ce qu'ils consomment : toute
fonction de C est proche d'un polynôme de bas degré sur un corps ; G =
un apprenant non trivial (2ⁿ/n^{ω(1)}, requêtes d'appartenance,
distribution uniforme) pour C = ACC⁰, puis TC⁰, puis P/poly ; T = OS17
Th. 12 (G ⟹ BPTIME(2^{O(n)}) ⊄ C[n^k]) et Th. 16 (ACC⁰ sous-exponentiel
⟹ REXP ⊄ ACC⁰) ; S = G est emprunté (ACC⁰ : une preuve naturelle de la
ligne 4 le fermerait, CIKK Th. 1.1), miroir (constructif + utile ⟺
NEXP ⊄ C, Williams Th. 1.2) et exclu sous crypto dès TC⁰ (dichotomie
PRF/apprentissage, OS17 Th. 2 ; Naor-Reingold ; Kearns-Valiant).

## 2. Ce qui tient — vérifié sur texte

- **T, verbatim** : OS17 Th. 12 « *Let C be any typical circuit class.
  If for each k, C[n^k] has non-trivial learning algorithms, then for
  each k, BPTIME(2^{O(n)}) ⊄ C[n^k].* » ; preuve par Th. 13 (« *There is
  a PSPACE-complete language L⋆ ∈ DSPACE(n)* […] [KKO13, FK09, IW01],
  *most crucially the construction of a downward self-reducible and
  random self-reducible PSPACE-complete language in [TV07]* ») — la
  candidature avait raison : pas d'easy witness pour Th. 12 (Th. 17,
  la branche preuves naturelles ⟹ ZPEXP, l'utilise). Th. 16 : « *If
  for every depth d and modulo m there is ε > 0 such that
  ACC⁰_{d,m}[2^{n^ε}] has non-trivial learning algorithms, then REXP ⊄
  ACC⁰[poly].* » Th. 3 (informel) confirme les trois conclusions
  BPEXP / REXP / ZPEXP.
- **L'emprunt, verbatim** : CIKK Th. 1.1 « *Natural proofs of circuit
  lower bounds imply learning algorithms for the same circuit class* »
  ; Th. 1.2 (AC⁰[p] en temps quasi-polynomial, requêtes d'appartenance,
  « *No learning algorithms for AC⁰[p] were previously known* ») ; et
  la phrase ACC⁰ exactement comme citée : « *A logical next step would
  be ACC⁰: if one can get a natural property useful against ACC⁰, for
  example by naturalizing Williams's proof, then a learning algorithm
  for ACC⁰ would follow.* »
- **Le miroir, verbatim** : Williams 2016 Th. 1.2 « *For all typical C,
  NEXP ⊄ C if and only if there is a polynomial-time algorithm that is
  useful against C* » ; et : « *any NEXP lower bound must meet
  precisely two of the three conditions of Natural Proofs
  (constructivity and usefulness)* ». Th. 1.7 : « *There are no
  P-natural properties useful against C* ⟺ *ZPE has C seeds* ».
- **L'exclusion crypto, verbatim** : OS17 Th. 2 (version informelle) :
  « *There are pseudo-random function generators computable by
  polynomial-size circuits from C that are secure against
  sub-exponential size Boolean circuits if and only if polynomial-size
  circuits from C are learnable non-uniformly in sub-exponential
  time.* »
- **La direction est absente** : atlas — deux mentions incidentes
  (KS06 en cellule 7 ; « apprentissage Th. 12 » de Pich-Santhanam en
  cellule 15) ; Linial 0, Jackson 0, Fourier 0 ; CIKK et
  Oliveira-Santhanam n'apparaissent qu'en bib. Voisines nommées (10,
  13 : MCSP — OS17 Th. 5 est dans le même texte) : exact.
- **La forme v4.4** : G structuré, T numéroté et vérifié, S déclaré à
  trois étages avec ses théorèmes, direction, type « entrée de
  registre » ; le test de l'emprunt formulé comme le prompt le demande.
  Aucun régime d'échec.

## 3. Attaque logique (§5.2) — les prises

### Prise 1 — « G est une propriété naturelle par théorème » : deux équivalences confondues

La candidature écrit (champ 4a) que Th. 8 et Th. 9 « *le rendent
équivalent à “distingueurs de complexité sous-exponentiels” et à
“preuves P-naturelles utiles contre C” — G est une propriété
naturelle* ». Verbatim : **Th. 8** (« *Algorithmic Equivalences* ») :
apprenants non triviaux ⟺ compression probabiliste ⟺ « *complexity
distinguishers running in time 2^{O(n)}* » — à erreur BORNÉE ; **Th. 9**
(« *Equivalences for zero-error algorithms* ») : preuves P-naturelles
⟺ ZPP-naturelles ⟺ « *zero-error complexity distinguishers* ». Ce sont
deux classes distinctes ; le pont de l'une à l'autre est CIKK Th. 1.1
(naturel ⟹ apprentissage) — UN sens ; le sens apprentissage ⟹ preuve
naturelle exigerait de dérandomiser le distingueur et n'est écrit nulle
part dans ces textes. Conséquence : le statut à trois étages tient
(emprunt par CIKK ; miroir par Williams Th. 1.2 sur la version
constructive + utile ; exclusion par Th. 2), mais la phrase de la
candidature doit se lire « G est équivalent à un distingueur à erreur
bornée (Th. 8), impliqué par toute preuve naturelle (CIKK), et
équivalent à une propriété constructive utile dès qu'on relâche la
densité (Williams) ». Pour le registre : le triangle avec ses flèches
exactes, pas l'identité.

### Prise 2 — L'exclusion crypto : sous quelles hypothèses exactement

Th. 2 porte ses propres réserves, verbatim : « *A caveat is that our
construction requires non-uniformity, and is established only in the
exponential security regime.* » L'exclusion de G pour TC⁰ via Th. 2
exige donc des PRF de TC⁰ sûres contre des circuits SOUS-EXPONENTIELS
(Naor-Reingold sous DDH sous-exponentiel), et ne vaut que pour
l'apprentissage non uniforme. La candidature écrit « EXCLU sous
DDH/factorisation » sans ces qualifications ; Kearns-Valiant 1994
(casser RSA/factorisation par un apprenant polynomial des circuits à
seuil de profondeur constante) couvre l'apprenant POLYNOMIAL, pas le
régime 2ⁿ/n^{ω(1)} de G. Précision, pas réfutation : l'exclusion tient,
sous hypothèse sous-exponentielle.

### Prise 3 — Le sous-lemme : la cellule discriminante est vide par déséquilibre (mesuré)

Champ 7 : « adeg_{F₂}(MOD₆) et adeg_{F₃}(MOD₆) tous deux ≥ 3 à n = 8 »
avec ε = 1/8. Mesuré (data §2a) : MOD₆ = [Σ ≡ 0 mod 6] vaut 1 sur 29
points sur 256 ; le polynôme constant 0 coïncide avec elle sur 227/256 =
88,7 % ≥ 224 = 7/8 : **adeg_{F,1/8}(MOD₆) = 0 sur les deux corps.**
L'énoncé est faux tel qu'écrit — parce que la mesure ne mesure pas le
phénomène à cette échelle : un seuil d'accord ε n'a de sens que si ε est
inférieur au biais de la fonction (0,113 ici ; 1/8 = 0,125 le dépasse).
Le régime de contrôle (PARITY/F₂ = 1 ; MOD₃/F₃ = 2 ; degrés exacts et
Fourier à n = 12 conformes au pré-calcul de la candidature) est
irréprochable ; le régime discriminant en degré approché ne l'est pas.
Correction du Réfuteur (ε = 1/16, seuil 240) : le constant ne suffit
plus ; aucun polynôme de degré ≤ 4 trouvé n'atteint 240 sur F₂ (meilleur
235) — sans certificat d'optimalité ; run ciblé en cours (data §2c). La
même leçon d'échelle que PR-005/PR-007 : le degré approché est une
mesure asymptotique (Ω(√n)) sans avatar propre à n = 8 pour une fonction
à 11 % de uns. **Pour l'entrée, rien n'en dépend** — l'élimination est
par théorèmes ; mais le prompt doit apprendre : toute mesure d'accord
doit être calibrée sur le biais (ou remplacée par l'avantage sur le
meilleur constant).

### Prise 4 — Ce que l'entrée apporte vraiment : la raison de l'exception de la ligne 7

La candidature nomme le mécanisme (9), « l'échelle algorithmique
RR-exposée », et c'est la pièce la plus utile à l'Atlas — plus que la
direction rayée. Les deux échelles ont la même forme (algorithme ⟹
borne uniforme) et les mêmes conclusions (des barreaux de Williams :
BPE/REXP ⊄ ACC⁰ contre NEXP ⊄ ACC⁰) ; l'une esquive RR, l'autre y est
soumise par théorème. La raison est écrite dans les textes : Williams
Th. 1.2 — une borne NEXP n'exige que constructivité et utilité (« *two
of the three conditions* ») ; OS17 Th. 8 — apprendre, c'est distinguer
les fonctions de C des fonctions ALÉATOIRES, donc la densité est dans la
définition même de G ; Th. 2 — et une PRF dans C rend cette distinction
impossible. La cellule 7 (D-005) disait que la double sortie de Williams
« ne se transmet pas au programme de mesure du dépôt » ; E-5 en donne la
version générale : elle ne se transmet à AUCUNE échelle dont le G est un
distingueur contre l'aléatoire. À consigner tel quel.

### Prise 5 — Précisions

(a) « Th. 15 pour toute sous-classe close par projections » : non
extrait ; Th. 3 (informel) dit « *Let C be any circuit class closed
under projections* » — cohérent, numéro à confirmer si la cellule le
cite. (b) « Learning algorithms from circuit lower bounds » (CC 2024) :
[TEXTE NON OUVERT] par la candidature comme par l'instruction — dette
notée, sans conséquence sur le registre (il ne peut que renforcer une
équivalence, pas ouvrir G). (c) Le pré-calcul de la candidature (deg,
Fourier, n = 12) est exact ; sa DNF diffère par la graine (deg_F₃ 11
contre 12, W 0,938 contre 0,934).

## 4. Barrières (§5.4)

- **Relativisation** : M lit le circuit (Fourier, polynômes) — sans
  objet structurel, conforme ; T repose sur la fonction PSPACE-complète
  auto-réductible de TV07 (arithmétisation) — la candidature le dit.
- **Preuves naturelles** : la barrière par théorème — c'est le contenu
  de l'entrée (prise 1 pour les flèches exactes, prise 4 pour la
  portée) ; mécanisme (4) « barrière héritée par implication » dans sa
  forme la plus forte : ici l'héritage est une équivalence à la densité
  près.
- **Algébrisation** : à auditer sur TV07 pour T ; la conclusion (BPE ⊄
  ACC⁰) est un barreau qu'AW ne barre pas — pas le verrou. Conforme.
- **Monotone** : sans objet. Conforme.
- **Verrou réel** : à ACC⁰, l'absence de propriété naturelle (le gap de
  la ligne 4 : pas de corps pour les modules composés — le témoin le
  montre à n = 12 : MOD₆ hors des trois îles) ; au-delà, RR par
  théorème (Th. 2). Critères (a)/(b) : (a) actif (entrée de registre,
  versant P ≠ NP, direction absente) ; (b) actif — l'entrée teste RR
  par théorème et en exhibe la raison structurelle.

## 5. Contre-vérification (§5.3)

Instrument indépendant ; antériorité déclarée (Smolensky, LMN). Régime
de contrôle CONFORME (n = 12 : PARITY 1/12/0,000 ; MOD₃ 11/2/0,115 ;
MOD₆ 11/12/0,512 ; DNF 11/11/0,938 ; n = 8 : adeg_{F₂}(PARITY) = 1,
adeg_{F₃}(MOD₃) = 2). Régime discriminant en degré approché : MIS-
SPÉCIFIÉ (prise 3) ; correction sans certificat ; run ciblé en cours.
Détail : `data/pr014_apprentissage_degres.md`.

## 6. Folklore-check — bilan

Vérifié sur texte : OS17 (Th. 2, 3, 8, 9, 12, 13, 16, 17, Cor. 4,
Lemme 7, réserve du Th. 2), CIKK (Th. 1.1, 1.2, phrase ACC⁰, trade-off
utilité/efficacité, RR : Razborov-Smolensky utiles contre 2^{n^γ}),
Williams 2016 (Th. 1.1, 1.2, 1.7, « two of the three conditions »).
Non ouverts : Fortnow-Klivans 2009, KKO13, Kearns-Valiant 1994,
Kharitonov 1993, Naor-Reingold 2004 (déjà en cellule 7), LMN, Jackson,
TV07, le texte CC 2024 — cités avec précision, non contredits.

## 7. Verdict (§5.5) et bilan du schéma v4.4

**ENTRE AU REGISTRE (E-5).** Constitué : la confusion Th. 8 / Th. 9
(prise 1) ; les réserves manquantes de l'exclusion crypto (prise 2) ; la
cellule discriminante vide par déséquilibre (prise 3 — leçon
d'instrument). Debout : le quadruplet complet et vérifié ; le statut à
trois étages ; la direction absente ; le mécanisme (9), qui explique
l'exception de la ligne 7. Mécanismes transversaux versés : (8) le
triangle naturel / apprentissage / distingueur avec ses flèches exactes ;
(9) l'échelle algorithmique RR-exposée. Aucun fil.

**Le schéma v4.4 a fait son travail** : la candidature s'est
auto-classée au registre parce que le champ 4 l'obligeait à écrire le
statut de G étage par étage, et ce statut a résisté à la vérification
sur texte. Les prises du Réfuteur ont porté sur la précision des
théorèmes (une confusion d'équivalences) et sur l'instrument (le biais),
pas sur la structure. Leçon pour le prompt (v4.5, sans réécriture
immédiate) : au champ 7, **toute mesure d'accord doit être calibrée sur
le biais de la fonction** (ε < biais, ou avantage sur le meilleur
constant) — la mis-spécification de la n° 9 est le pendant, côté
mesure, de la confusion de mesures de la n° 4.

## 8. Pièces et sources

`checks/pr014_apprentissage_degres.py` ; `data/pr014_apprentissage_degres.md` ;
`tasks/done/PR-014.md`. Ouverts et grepés :
[OS17, arXiv 1611.01190](https://arxiv.org/abs/1611.01190) ;
[CIKK, LIPIcs CCC 2016 / ECCC TR16-008](https://eccc.weizmann.ac.il/report/2016/008/) ;
[Williams, Natural Proofs Versus Derandomization, arXiv 1212.1891 v3](https://arxiv.org/abs/1212.1891).
