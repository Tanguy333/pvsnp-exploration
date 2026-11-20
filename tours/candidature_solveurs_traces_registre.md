# Candidature n° 8 (prompt v4.2, 2026-09-11) : « Les solveurs comme recherche de preuves — la direction P = NP par les algorithmes SAT et les relaxations convexes, éliminée par théorème famille par famille » (présentée comme entrée de registre E-4) — instruction du Réfuteur (PR-011)

**Verdict : ENTRE AU REGISTRE (E-4) — avec un périmètre recalibré et
une question de règle transmise à l'utilisateur.** La candidature est
la première présentée d'emblée comme entrée de registre, et la première
depuis PR-004 dont le sous-lemme est exécutable ET discriminant : la
double calibration (PHP_n contre pyramides de pebbling, DPLL contre
CDCL) a été implémentée indépendamment et reproduit le tableau 2 × 2
prédit par les théorèmes (Haken 1985 ; BIW04 ; BKS04) — y compris la
cellule qui teste le mécanisme (CDCL polynomial sur les pyramides :
≤ 2 004 conflits jusqu'à h = 40, contre > 3 M nœuds arborescents dès
h = 6). Ce qui est recalibré : le TITRE surestime le périmètre — ce
n'est pas « la direction P = NP par les algorithmes SAT » qui est
éliminée, c'est la direction *par les solveurs complets CERTIFIANTS*
dont la trace vit dans un système à borne inférieure connue ; tout
algorithme qui décide sans produire de preuve dans un tel système
(randomisé à erreur bornée, ou à trace dans Frege/EF) échappe au
mécanisme (6) — et là, comme la candidature le dit, la direction *est*
P = NP. Deux précisions de colonne : la colonne LP/SDP est aveugle à la
classe (Rothvoss 2014 : le polytope des couplages, un problème de P, a
une complexité d'extension 2^{Ω(n)}) — son théorème élimine une
REPRÉSENTATION, pas une route vers NP ; et les solveurs modernes (PR,
DRAT à extension) ont une trace à la frontière Frege/EF, c'est-à-dire
dans la zone ouverte — ce que la candidature réserve à l'audit.

Contexte : huitième candidature ; prompt v4.2 ; en-tête déclarant une
dérogation à la règle 1 (candidature interne, précédents PR-005/009/010).
Tâche PR-011 déclarée au backlog avant exécution ; instrument
`checks/pr011_solveurs_traces.py` ; données `data/pr011_solveurs_traces.md`.

## 1. Reformulation (§5.1)

Inscrire au registre des éliminations le versant P = NP le plus pratiqué
— les solveurs complets et les hiérarchies de relaxations — en le lisant
par le dictionnaire solveur ↔ système de preuves (Buss-Nordström,
Handbook ch. 7) : toute exécution d'un solveur complet sur une instance
insatisfaisable est une réfutation dans un système S fixé, donc les
bornes inférieures de complexité des preuves (Haken, Urquhart,
Chvátal-Szemerédi pour la résolution ; Razborov pour PC ; Pudlák pour
CP ; Grigoriev, Schoenebeck pour SoS ; FMPTW/LRS pour les formulations
étendues ; Krajíček pour OBDD) sont des bornes inférieures
inconditionnelles sur ces solveurs ; et là où S n'a pas de borne
(Frege/EF), la recherche de preuve est NP-dure dès la résolution
(Atserias-Müller 2020) — la direction y coïncide avec P = NP.

## 2. Ce qui tient

- **La forme v4.2** : cible propre ; chaîne avec flèche 1 EXCLUE par
  théorème colonne par colonne et OUVERTE PAR MIROIR au sommet, flèches
  2-3 prouvées (identité, Cook-Levin) ; test du faux raccord rempli avec
  le cas miroir CONSTITUÉ et assumé (« aucun objet NP-dur résolu ») ;
  plafond avec avatar fini exact ; type « entrée de registre ». Aucun
  régime d'échec.
- **La direction est absente de la matrice** (grep du jour : CDCL 0,
  DPLL 0, Lasserre 0, SoS 0, Urquhart 0, Schoenebeck 0, Chvátal 0 ;
  « Haken » n'apparaît qu'en `bib/proof_complexity.md` — la candidature
  écrivait « Haken 0 » pour bib aussi : inexact pour bib, exact pour la
  matrice, sans conséquence ; « automatisabilité » : ligne 13 et
  Pich-Santhanam, dans un autre rôle). La cellule 15 lit les bornes des
  systèmes faibles vers NP ≠ coNP et l'interpolation ; elle ne les lit
  pas vers les algorithmes.
- **Le folklore-check est exact partout où il a été vérifié** :
  Atserias-Müller (arXiv 1904.02991 v2, JACM 2020 : « *finding a
  Resolution refutation that is at most polynomially longer than a
  shortest one is NP-hard* » — sous P ≠ NP, pas ETH) ; Rothvoss STOC
  2014 / JACM 2017 (couplage parfait : 2^{Ω(n)}) — vérifiés ; les
  autres (BKS04, PD11, AFT11, GKMP20, dRGNPRS21, IR22, BPR00, KP98,
  Grigoriev 01, Schoenebeck 08, HKB17, Krishnamurthy 85, Urquhart 99)
  cités avec précision, non contredits.
- **Le sous-lemme** : exécuté (§5) — conforme dans ses quatre cellules.
- **Les barrières** : traitées exactement pour une famille algorithmique
  (sans objet structurel, avec la remarque juste : une preuve de P = NP
  devrait lire la formule, les solveurs le font, ce n'est pas là qu'ils
  meurent) ; le verrou réel nommé comme théorèmes de limite de méthode,
  un par colonne, plus le miroir au sommet.

## 3. Attaque logique (§5.2) — les prises

### Prise 1 — Le périmètre : « certifiant », pas « algorithmes SAT »

Le mécanisme (6) borne un algorithme PAR LA PREUVE QU'IL PRODUIT. Il ne
dit rien d'un algorithme qui décide UNSAT sans produire de réfutation
dans un S à borne connue : un algorithme randomisé à erreur bornée (le
« solveur incomplet » de Schöning est un algorithme de décision complet
au sens BPP, en temps exponentiel prouvé — la candidature l'écarte
comme « ne décidant pas », ce qui est faux au sens des classes), un
solveur dont la trace vit dans Frege/EF (colonne « OUVERTE PAR
MIROIR »), ou tout algorithme dont la correction est établie hors
trace. Formellement : si P = NP par un algorithme A, « les traces de
A » forment un système p-borné — sans contradiction avec aucune borne
connue. L'entrée élimine donc exactement les familles nommées, et rien
au-delà ; la candidature le sait (« au-delà la direction est P = NP
lui-même ») mais son titre dit « la direction P = NP par les
algorithmes SAT ». **Le registre doit porter le périmètre exact** : les
solveurs complets certifiants à trace dans {résolution, PC, CP, SoS de
degré borné, formulations étendues compactes, OBDD}.

### Prise 2 — La colonne LP/SDP est aveugle à la classe

FMPTW 2012 et LRS 2015 bornent la complexité d'extension des polytopes
TSP/coupe ; mais Rothvoss 2014 borne celle du polytope des couplages
parfaits — un problème de P — par 2^{Ω(n)}. Le théorème de la colonne
élimine une REPRÉSENTATION (un LP compact exact) indépendamment de la
classe du problème ; ce n'est pas une élimination « parce que
NP-dur ». C'est le profil de la ligne E-1 (une technique qui ne
distingue pas la classe), en miroir ; à consigner dans l'entrée pour
que la colonne ne soit pas relue comme une preuve de dureté.

### Prise 3 — Les solveurs modernes vivent à la frontière ouverte

Le dictionnaire solveur → résolution est exact pour CDCL « pur » ; les
solveurs de 2017-2026 ajoutent des règles (PR, SDCL, extension DRAT)
dont la trace est entre résolution et EF — HKB17/SaDiCaL réfutent PHP
et Tseitin en temps polynomial. La candidature le réserve à l'audit
(« l'audit doit dater chaque technique et son système ») ; l'instruction
le tranche pour l'entrée : **la frontière de l'élimination passe à
l'intérieur des solveurs actuels**, et ce qui est éliminé est le noyau
résolution, pas « les solveurs SAT ». Le témoin exécutable le montre en
creux : CaDiCaL 1.9.5 reste géométrique sur PHP (×6,55 par pigeon
jusqu'à 14,4 M conflits) — son noyau n'a pas de raisonnement cardinal.

### Prise 4 — Précisions

(a) « La proposition formulations étendues rejetée le 2026-09-08 » :
[NON TROUVÉ dans le dépôt] — aucune candidature de ce nom n'a été
soumise ni instruite ; la colonne entre ici pour la première fois.
(b) « Première élimination par théorème sur l'algorithme du versant
P = NP » : exact au sens « théorèmes sur la MÉTHODE » — la ligne 19 est
bornée par des dichotomies, théorèmes sur les problèmes ; la
distinction est celle de la candidature et elle tient.
(c) Le mur des physiciens (transition de phase) « trouve son théorème »
chez Chvátal-Szemerédi : correct pour la résolution ; pour SoS, c'est
Schoenebeck — la phrase est juste.

## 4. La question de règle, instruite

La candidature signale que sous v4.2, le test miroir du champ 4c
(« l'objet le plus dur que la famille résout doit être NP-dur, sinon
flèche vers P = NP absente ») interdit par construction toute ligne
algorithmique : l'objet le plus dur résolu ne peut être NP-dur sans
que P = NP soit déjà prouvé. **L'observation est exacte.** Le
critère n'est pas symétrique de celui de la direction P ≠ NP, où une
famille passe si son mécanisme *distingue la classe* — la ligne 7
(Williams) a une flèche ouverte parce qu'un THÉORÈME DE TRANSFERT
prouvé (algorithme ⟹ séparation) porte sur NEXP, sans que la famille
ait prouvé la séparation. L'analogue côté P = NP serait : **un théorème
de transfert prouvé et numéroté « sous-but G ⟹ P = NP », où G est une
réussite algorithmique STRUCTURÉE, non connue équivalente à P = NP, et
que le mécanisme de la famille vise.** Les colonnes de l'entrée E-4
avaient toutes un tel G — « solveur S-tracé polynomial », « LP compact
exact du polytope TSP » — chacun réfuté par théorème ; au sommet,
G_EF = « EF p-borné et automatisable » est ouvert, implique P = NP, et
n'est pas connu équivalent — mais c'est le verrou Frege de la ligne 15
lu de l'autre côté : une refondation de la cellule 15, pas une ligne.
Sous ce critère, aucune direction algorithmique connue de l'Atlas n'a
aujourd'hui de flèche ouverte non-miroir — « ce qui est peut-être
exact », comme l'écrit la candidature. **Décision utilisateur** :
(i) garder le miroir tel quel (aucune ligne algorithmique, le versant
P = NP se remplit par le registre) ; (ii) l'amender par le critère de
transfert ci-dessus (recommandé par le Réfuteur — il est le symétrique
exact de la ligne 7, et il ne rouvre rien : E-4 reste au registre).

> **Décision utilisateur (2026-09-12, tâche PR-012)** : option (ii)
> retenue — le miroir est amendé dans CLAUDE.md (règle 10) et au champ
> 4c du prompt (v4.3). E-4 inchangée ; la lecture algorithmique du
> verrou Frege/EF de la ligne 15 est inscrite au backlog comme
> refondation de cellule à décider (`ATLAS-L15-alg [auto]`).

## 5. Contre-vérification exécutable (§5.3) — la double calibration

Instrument indépendant (générateurs, DPLL minimal, CaDiCaL via pysat),
contrôle satisfiable conforme. Résultats (`data/pr011_solveurs_traces.md`) :

| | DPLL (arborescent) | CDCL (résolution) |
|---|---|---|
| PHP_n, n = 4..11 | **×9,3 / pigeon** (n ≤ 8 ; budget 3 M dépassé à n = 9) | **×6,55 / pigeon** (PHP₁₁ : 14 398 674 conflits, 508 s) |
| Peb(P_h), h = 4..40 | **×243 / niveau** (budget dépassé dès h = 6) | **≤ 2 004 conflits pour tout h ≤ 40**, pente log-log 1,9 ; décisions ≈ h^{2,7} |

Les trois cellules de contrôle et la cellule discriminante sont
conformes aux théorèmes ; aucune des deux issues contraires nommées
par la candidature ne s'est produite. Artefact consigné : plateau de
conflits à ~2 000 dès h = 20 (passe de simplification de CaDiCaL —
elle-même de la résolution), verdict polynomial inchangé.

## 6. Barrières (§5.4)

Relativisation, preuves naturelles, algébrisation : sans objet
structurel pour une famille algorithmique — conforme, avec la remarque
exacte de la candidature (une preuve de P = NP doit lire la formule).
Monotone : sans objet ; dépendance notée — l'interpolation faisable
(colonne monotone de la ligne 15) est l'outil des bornes CP qui
éliminent la colonne pseudo-booléenne. Verrou réel : théorèmes de
limite de méthode, un par colonne, et le miroir (automatisation
NP-dure) au sommet — la frontière est celle de la ligne 15, à
l'intérieur des solveurs actuels (prise 3). Critères (a)/(b) : (a)
actif (entrée de registre neuve, versant P = NP) ; (b) sans objet
déclaré avec sa raison structurelle.

## 7. Verdict (§5.5)

**ENTRE AU REGISTRE (E-4)**, périmètre recalibré : « les solveurs
complets certifiants à trace dans un système à borne inférieure
connue » ; colonne LP/SDP marquée aveugle à la classe ; frontière
placée à l'intérieur des solveurs actuels (PR/EF). Mécanismes
transversaux versés : (6) *la trace est une preuve* ; (7)
*l'automatisation est un miroir*. Question de règle transmise (§4)
avec recommandation. Aucun fil ne suit : l'entrée n'a pas de suite,
c'est sa valeur.

## 8. Pièces et sources

`checks/pr011_solveurs_traces.py` ; `data/pr011_solveurs_traces.md` ;
`tasks/done/PR-011.md`. Vérifiés ici :
[Atserias-Müller, arXiv 1904.02991](https://arxiv.org/abs/1904.02991) ;
[Rothvoss, STOC 2014 / JACM 2017](https://dl.acm.org/doi/10.1145/3127497).
Théorèmes de calibration : Haken 1985 ; BIW04 ; BKS04 ; Chvátal-Szemerédi
1988 ; Urquhart 1987 (non ouverts ici — classiques, cités par la
candidature avec précision).
