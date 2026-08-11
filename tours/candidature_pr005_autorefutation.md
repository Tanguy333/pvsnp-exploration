# Auto-réfutation de PR-005 (« la frontière algorithmique THR∘THR ») — LACUNE RÉPARABLE, à la limite de la faille fatale comme fil du dépôt

Date : 2026-08-11. Tâche : PR-006 (instruction de PR-005 par son
auteur, sur ordre utilisateur — le conflit de rôles déclaré dans la
candidature est résolu par l'auto-réfutation ; sa limite est dite en
§6). Procédure CLAUDE.md §5.

## 1. Reformulation (§5.1)

Armer le verrou de la ligne 7 (« un algorithme #SAT/CAPP non trivial
pour THR∘THR ⟹ NEXP ⊄ THR∘THR ») avec les instruments de poids du
dépôt, en commençant par mesurer le poids sous restrictions.

## 2. La faille CONSTITUÉE : la confusion de mesures (ALG-001)

Déjà infligée et marquée : la candidature confondait le poids PTF
(signe — le mur 20/119/640 de F-001) et le poids MinSYM+ (couvert
exact — les lois MC), alors que W_MinSYM+(IP_{2k}) ≤ k trivialement
(IP est un SYM∘AND de k portes). Le sous-lemme l'a falsifiée en
secondes. CONSÉQUENCE AGGRAVANTE, au-delà de la correction déjà
consignée : **la revendication centrale de la candidature — « des
instruments exacts que le dépôt est le seul à posséder » — est
RÉFUTÉE pour le paramètre recalibré.** Le poids PTF n'est pas un objet
du dépôt : c'est une mesure CLASSIQUE et massivement étudiée
(programme Sherstov ; bornes de sign-rank de Forster ; l'exponentialité
du poids PTF de IP est de la THÉORIE PUBLIÉE, pas une découverte de
F-001 — F-001 en a mesuré des constantes à n ≤ 8). L'avantage
comparatif du dépôt, pilier de la conviction affichée, ne survit pas
à la correction.

## 3. Attaque de la chaîne : « PROUVÉE modulo audit » = OUVERTE avec dette

Le champ 3 étiquetait la flèche 2 « PROUVÉE modulo audit ». C'est un
surétiquetage — le même auteur avait corrigé la flèche MP91 de PR-004
pour exactement ce motif. Points précis à charge :
(a) le transfert de Williams exige des CONDITIONS DE CLÔTURE de la
classe (le easy-witness plonge un vérifieur dans la classe ; il faut
typiquement la clôture sous conjonctions/compositions légères) — et
THR∘THR n'est PAS évidemment close sous ET de deux circuits (ET de
deux seuils-de-seuils = profondeur 3). Il est donc POSSIBLE que le
transfert exige un algorithme pour une classe STRICTEMENT PLUS GRANDE
que THR∘THR (p. ex. AND∘THR∘THR) — auquel cas l'énoncé visé du champ
1 est mal calibré. À trancher par A-023, verbatim ;
(b) l'état de la frontière 2014-2026 n'était PAS établi par le
folklore-check : des avancées partielles existent (ACW 2016 sur des
variantes creuses ; les bornes de Chen/Chen-Ren 2019-2020 sur la
famille ACC∘THR) — si une variante de THR∘THR est déjà tombée, ou si
un algorithme partiel existe déjà, la cible est déplacée. Une
candidature dont l'OUVERTURE de la cible n'est pas vérifiée a un trou
de folklore-check (champ 5), le régime d'échec n° 3 en embuscade.

## 4. Attaque du premier pas recalibré : le risque de réplication

ALG-002 (« le poids PTF sous restrictions ») est menacée de
non-discriminance : IP restreinte contient génériquement IP sur les
paires survivantes, et la théorie publiée (sign-rank de Forster et sa
descendance) borne déjà le poids PTF de tout IP_{2j} —
l'« effondrement ou résistance » risque d'être PRÉDICTIBLE par
théorème, c'est-à-dire une réplication d'asymptotiques connues avec
mesure de constantes. Ce n'est pas nul (le dépôt assume la
réplication vérifiante), mais ce n'est PAS un sous-lemme discriminant
au sens du prompt — le champ 6 recalibré ne teste plus le mécanisme
de la famille, seulement la théorie des autres. Antériorité à établir
AVANT tout lancement d'ALG-002 (directive permanente).

## 5. Attaque du test de plafond : le retour au régime rejeté

La leçon `echelle_instrument` (payée deux fois : n ≤ 8 contre
n ≈ 4050) s'applique frontalement : AUCUNE mesure à ν ≤ 8 ne peut
dérisquer la conception d'un algorithme asymptotique — au mieux elle
oriente. Les livrables réels du fil, après correction, sont : un
audit (A-023 — légitime et utile à la ligne 7 QUEL QUE SOIT le sort
du fil), des tables de réplication d'une mesure classique, et « le
vrai travail » (l'algorithme) qui est de la recherche de frontière
sans chemin de dérisquage atelier. **C'est le profil exact des fils
que l'utilisateur vient de clore** (« des cartes, pas des routes ») —
la candidature promettait d'en sortir ; corrigée, elle y retombe.

## 6. Barrières et limite de l'auto-réfutation

Barrières : la section la plus solide de la candidature — le
transfert hérite du seul précédent non-relativisant et
non-algébrisant (A-001), la direction algorithmique n'est pas une
propriété de tables (RR sans objet structurel), monotone sans objet.
Pas de faille ici. LIMITE DE L'EXERCICE, déclarée : une
auto-réfutation ne remplace pas une instruction tierce — l'auteur
peut avoir des angles morts symétriques à ses convictions ; la dette
d'instruction externe (Qwen en réfuteur, ou VER) reste ouverte si le
fil est refondé.

## 7. VERDICT : LACUNE RÉPARABLE — réparation étroite, sinon clôture

- **Constitué** : la confusion de mesures (faille, marquée) ; la
  réfutation de la revendication d'instruments uniques pour le
  paramètre pertinent ; le surétiquetage de la flèche 2 ; le trou de
  folklore-check sur l'état de la frontière ; le risque de
  non-discriminance d'ALG-002 ; le retour au profil « carte » que le
  fil prétendait dépasser.
- **Debout** : le verrou de la ligne 7 lui-même (réel, le plus fort
  de la matrice) ; la légitimité d'A-023 (l'audit sert la cellule
  ligne 7 indépendamment du fil) ; les barrières.
- **La réparation, étroite et conditionnelle** : attendre A-023 ; le
  fil n'est refondable QUE si l'audit révèle (i) la forme exacte du
  transfert pour THR∘THR avec une cible d'algorithme bien posée, ET
  (ii) un paramètre-goulot dont la mesure à l'échelle atelier serait
  RÉELLEMENT discriminante (ni folklore, ni réplication pure), ET
  (iii) une frontière encore ouverte à l'endroit visé. Si l'une des
  trois manque : CLÔTURE HONNÊTE du fil ALG à la chute d'A-023, avec
  A-023 versé à la cellule ligne 7 comme acquis.
- **Leçon pour le prompt (v4)** : régime d'échec n° 6 candidat — la
  CONFUSION DE MESURES (deux objets homonymes du même dépôt) ;
  exigence nouvelle au champ 6 : toute mesure invoquée doit être
  NOMMÉE AVEC SA DÉFINITION.

## 8. Pièces

`prompts/candidature_pr005_frontiere_algorithmique.md` (note de
correction en tête) ; `data/alg001_poids_restrictions.md` +
`tasks/done/ALG-001.md` (la faille exécutable) ; A-023 en cours
(l'arbitre de la réparation).
