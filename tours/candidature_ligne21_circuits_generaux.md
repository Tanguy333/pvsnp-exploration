# Candidature n° 21 (Qwen, 2026-09-08) : « Bornes inférieures de circuits généraux pour NP — la route principale (élimination de portes, dispersers affines) et le pincement des barrières » — instruction du Réfuteur (PR-007)

**Verdict : LACUNE RÉPARABLE — sous conditions.** Le trou dans l'Atlas
est RÉEL (aucune ligne ne porte la seule technique qui produit des
bornes explicites sur circuits généraux) et la carte est en grande
partie exacte ; mais (1) la chaîne colle l'énoncé du problème entier
(« SAT ∉ SIZE(n^k) ∀k ») sur une technique qui n'y mène par aucune
flèche, même conjecturale — ses fonctions dures sont dans P et sa cible
réelle est « 10n pour une fonction explicite », ouvert (Li-Yang,
verbatim) ; (2) le « pincement » attribue à RR un blocage qui, à la
frontière réelle de la route (cn → superlinéaire), n'existe pas —
l'obstruction y est un théorème de limite de méthode (GHKK) et
l'absence d'idées, pas une barrière ; (3) le test de plafond vise le
mauvais phénomène (l'existence, triviale par comptage dès n = 8, au lieu
de l'EXPLICITÉ, sans avatar atelier à aucun n) ; (4) le seul morceau du
sous-lemme présenté comme contributif (fermer XOR₄ ∈ [10, 12] de PR-002)
est un théorème des années 1970 (Red'kin, 4n − 4 — verbatim via
Kombarov 2011), et Markov 1958 + Schnorr le bornaient déjà à ≥ 11 sans
solveur. La ligne 21 peut entrer — comme cellule DOCUMENTAIRE, fondée par
un audit A-024, avec un énoncé recalibré et un verrou d'un type nouveau
pour la matrice (plafond de méthode). Pas de fil atelier : la
candidature dit elle-même que son premier pas « ne peut pas blesser la
famille » — et une mesure qui ne peut rien blesser n'est pas un premier
pas.

> **⚠ ADDENDUM MARQUÉ (2026-09-08, règle utilisateur)** : « une ligne de
> la matrice devrait exiger au moins une flèche OUVERTE vers P vs NP ;
> les directions à flèche EXCLUE vont au registre des éliminations ».
> La chaîne de cette candidature n'a aucune flèche OUVERTE (flèche 1
> ABSENTE — §3, charge 1). Conséquence : pas de ligne 21, pas d'audit
> A-024 ; la direction entre au registre des éliminations de la matrice
> (entrée E-1). Le verdict « LACUNE RÉPARABLE — ligne documentaire
> possible après audit » est remplacé par « ENTRE AU REGISTRE DES
> ÉLIMINATIONS » ; l'analyse ci-dessous est inchangée.

Contexte : quatrième candidature externe ; prompt v3 (19 familles) plus
historique PR-005/PR-006 fourni hors prompt (la candidature les cite).
Procédure CLAUDE.md §5. Tâche PR-007 déclarée au backlog avant
exécution ; instrument INDÉPENDANT `checks/pr007_synthese_exacte.py`
(SAT/CaDiCaL, encodage KKY/Knuth — distinct du CP-SAT de PR-002).

## 1. Reformulation (§5.1)

Inscrire dans l'Atlas, comme « ligne-mère » des lignes 4/5/6/11, la
route directe vers NP ⊄ P/poly — les bornes inférieures pour circuits
généraux par élimination de portes (Blum 3n, 1984 → FGHK (3 + 1/86)n,
2016 → Li-Yang 3,1n − o(n), 2022, sur dispersers affines) — avec son
théorème de limite (GHKK 2016/2018), sa lecture algorithmique (CDJ,
avril 2026) et la route indirecte (échelle de Kannan → S₂E ⊄ SIZE(2ⁿ/n),
2024) ; premier pas : une double calibration de synthèse exacte
(Schnorr sur U₂, Knuth sur B4) dont la candidature déclare qu'elle ne
teste pas la famille.

## 2. Ce qui tient (à charge de fairness)

- **Le trou est réel.** Grep de la matrice : « élimination de portes »,
  Blum, FGHK, Li-Yang — 0 occurrence ; les 3 occurrences du cluster
  sont l'échelle Kannan/S₂E (lignes 1 et 16) et un homonyme
  « disperseur » (ligne 17, Beame-Koroth). PR-002 avait déjà utilisé
  « le plafond gate-elimination (Schnorr 74 → FGHK 16) » pour tuer la
  SRE — sans que la matrice le consigne. L'Atlas des impasses n'a pas
  de cellule pour la technique qui produit LES SEULES bornes explicites
  sur circuits généraux : lacune de l'Atlas, pas de la candidature.
- **Le folklore-check est riche et, sur les pièces vérifiées ici,
  exact** : CDJ arXiv 2604.23958 (27 avril 2026) existe et est résumé
  fidèlement — abstract verbatim : « *Gate elimination is the primary
  technique for proving explicit lower bounds against general Boolean
  circuits* […] *gate elimination arguments are algorithms* » ;
  refuteurs pour XOR, multiplexeur, dispersers affines ; et « *given any
  DeMorgan circuit of size 3(n−1) that fails to compute XOR_n, we can
  efficiently produce a counterexample* » (caractérisation complète des
  circuits optimaux de XOR). CJSW (FOCS 2021 / TheoretiCS 2024) :
  « *for most major open problems in lower bounds against P, ZPP, and
  BPP, including P ≠ NP* […] *any proof of the separation would further
  imply a constructive separation* » — exact. GHKK (MFCS 2016, LIPIcs
  58, 46) verbatim : « *All known lower bounds are based on the
  so-called gate elimination technique* […] *this method cannot achieve
  linear bounds of cn beyond a certain constant c, where c depends only
  on the number of substitutions made at a single step of the
  induction* ». AW 2008 : la phrase « *why we have superlinear circuit
  lower bounds for PromiseMA but not for NP* » est déjà auditée dans
  `bib/aaronson_wigderson_2008.md`. Knuth : le « 12 » à n = 5 est
  confirmé par source secondaire (Goucher 2019 : « *all but one could be
  managed in 11 gates, and therefore the last one required exactly
  12* » — une seule classe NPN sur 616 126) ; le « 7 » à n = 4 est
  MESURÉ ici (§5). KPS (arXiv 2102.12579 = MFCS 2022) verbatim : « *it
  may take more than a week to search for a circuit of size thirteen* ».
  Chow (arXiv 0805.1385) : largeur relâchée à 2^{−q(n)}, q
  quasi-polynomial, sous la même hypothèse que RR — conforme.
- **La chaîne est honnête dans sa forme** (deux flèches prouvées, la
  première = le problème) et la **portée du sous-lemme est dite
  d'avance** — la leçon PR-005 est appliquée à la lettre.
- **Barrières de la route indirecte** : correctement cartographiées
  (BGS via Wilson 1985 — cité via secondaires, non vérifié ici non
  plus ; AW — verbatim dans le dépôt ; Chen-Hu-Ren ITCS 2026 — déjà en
  cellule 16).

## 3. Attaque logique (§5.2) — les charges

### Charge 1 — Le faux raccord : le mécanisme ne pointe pas vers l'énoncé

L'énoncé visé est « SAT ∉ SIZE(n^k) pour tout k ». Le mécanisme de la
famille produit des bornes cn pour des fonctions explicites — et
Li-Yang le disent verbatim (ECCC TR21-023, abstract) : « *it remains
unknown whether there is an explicit function (for example, a function
in NP) not computable by circuits of size 10n* » ; les dispersers
affines sont « *a class of functions known to be constructible in P* ».
La route ne mobilise NP nulle part : ses fonctions dures sont dans P,
et **aucune fonction de P ne peut jamais porter l'énoncé visé**
(P ⊆ P/poly). Entre « cn pour une fonction de P » et « SAT ∉ SIZE(n^k) »
il n'y a donc AUCUNE flèche, même conjecturale : ni mécanisme
d'amplification (GHKK : la méthode formalisée ne dépasse pas cn), ni
rien dans la famille qui sache distinguer une fonction de NP \ P d'une
fonction de P. La candidature colle l'énoncé du problème entier sur une
technique linéaire indifférente à NP — le régime « confusion
énoncé/technique » infligé à PR-002, ici dans sa version honnête
(« l'objet où les deux routes pointent sans arriver »). Conséquence
pour la matrice : la cellule, si elle existe, ne s'intitule pas « la
route principale vers NP ⊄ P/poly » mais « la seule technique explicite
sur circuits généraux — plafonnée à cn, dont la cible réelle est
l'explicité (10n ouvert, même pour des fonctions de P), et qui ne
contient aucune flèche vers NP ». **L'énoncé du champ 1 est à
recalibrer** : la cible propre de la famille est « borne superlinéaire
pour une fonction explicite », pas NP ⊄ P/poly.

### Charge 2 — Le pincement est mal localisé : à la frontière, aucune barrière

« Preuves naturelles : la barrière de cette ligne — RR l'ont écrite
pour elle. » Vrai pour l'énoncé « ∀k » à son bout superpolynomial ;
FAUX à l'endroit où la route est réellement arrêtée. L'argument RR
distingue une propriété naturelle utile contre SIZE(n^k) d'une famille
PRF calculable en taille n^c : il bloque les k > c, et rien en dessous.
Pour k = 1, 2 — superlinéaire, quadratique ; « 10n » ouvert — une preuve
naturelle n'est bloquée par rien. AW bloquent les techniques
ALGÉBRISANTES pour NP superlinéaire (la remarque « PromiseMA mais pas
NP ») ; BGS les relativisantes ; l'élimination de portes n'est ni l'une
ni l'autre — la candidature le dit (« sans objet structurel »).
Monotone : sans objet. Donc **à la frontière cn → superlinéaire, aucune
des quatre colonnes ne s'applique** ; ce qui arrête la route est (i) un
théorème de limite de la méthode (GHKK — un plafond cn sur une
formalisation de l'élimination de portes, pas une barrière au sens de
l'Atlas) et (ii) l'absence d'autre idée depuis 1984. C'est un verrou
d'un type nouveau pour la matrice — la ligne 19 avait « les dichotomies
comme barrière positive interne » ; ici « le théorème de limite de la
seule méthode » — et la candidature le nomme (§ Ce qui manque, 1) mais
l'enveloppe dans un « pincement » où RR joue le premier rôle. Deux
questions restent pour l'audit, PAS tranchées ici : (a) le verbatim RR
sur les bornes générales — [NON TROUVÉ dans cette instruction : ACM,
ScienceDirect et la page de Razborov renvoient 403/404] ; (b) la
naturalité même de l'élimination de portes n'est pas évidente : la
propriété « f est un disperser affine de dimension d » exige, lue sur
la table de vérité (N = 2ⁿ), d'énumérer ~2^{Θ(dn)} = N^{Θ(n)}
sous-espaces pour d = Θ(n) — pas visiblement constructive au sens RR ;
si la preuve n'utilise qu'une sous-propriété constructive, l'audit doit
la nommer. (c) Le plafond GHKK porte sur UNE formalisation (compte de
portes et d'entrées, substitutions par étape) ; Li-Yang 2022 en
discutent dans le corps de leur texte (pas dans l'abstract) — savoir si
3,1n reste sous ce plafond ou le contourne est une question de lecture,
ouverte ici.

### Charge 3 — Le test de plafond vise le mauvais phénomène

La candidature définit « le phénomène exploité » comme « une fonction
explicite exige > 3n portes » et constate son absence à n ≤ 5 (max
C(f) = 7 et 12 contre 3n = 12 et 15). Deux erreurs de catégorie :
(a) l'EXISTENCE d'une fonction à > 3n portes est une trivialité de
comptage dès **n = 8** (mesuré, §5 : le nombre de chaînes de 24 portes
sur 8 entrées est < 2^{256}) — non explicite ; la difficulté de la
ligne est l'EXPLICITÉ, et l'explicité n'a d'avatar à aucun petit n :
à n ≤ 12 toute fonction est « explicite » (c'est une table) ;
(b) comparer max C(f) à 3n mélange le régime de Shannon (max ~ 2ⁿ/n,
exponentiel — 7, 12, puis ~2ⁿ/n) et le régime linéaire (cn − o(n), où
le −o(n) rend « 3n − o(n) » vide à n = 5). Le « constat chiffré de
l'absence du phénomène » ne mesure donc pas la ligne. L'avatar honnête
du mécanisme serait la chute d'élimination C(f) − C(f|ρ) sous
substitution ; à n ≤ 5 elle est dominée par l'effet de Shannon
(restreindre une fonction de coût 12 à 4 variables donne un coût ≤ 7 :
chute ≥ 5 partout, sans rapport avec Blum). Conclusion : **cette
famille n'a aucun avatar à l'échelle atelier** — la candidature le dit
à moitié (« documentaire ») ; la règle 7 (test de plafond : ni déjà
connu, ni hors d'atteinte) est violée sur ses deux branches, et la
transparence lève l'accusation de dissimulation, pas la règle.

### Charge 4 — Le folklore-check du sous-lemme est troué là où il se voulait contributif

Le seul morceau présenté comme non-réplication — fermer la réserve
PR-002, XOR₄ ∈ [10, 12] en NOT-payant — est un THÉORÈME des années
1970 : Red'kin, « L(c ⊕ x₁ ⊕ … ⊕ xₙ) = 4n − 4 в базисе {x&y, x∨y, x̄} »
(verbatim de Kombarov, Vestnik MGU 2011, réf. [4] Red'kin 1970 ;
Red'kin, Problemy Kibernetiki 1973, « Proof of minimality of circuits
consisting of functional elements » — date de la référence primaire à
fixer à l'audit). Plus court encore : **Markov 1958** (nombre minimal de
NOT = ⌈log₂(d(f) + 1)⌉, d = chutes 1→0 sur une chaîne croissante ;
d(XOR₄) = 2, mesuré) + **Schnorr 1974** (≥ 3(n − 1) = 9 portes binaires
après absorption des NOT) donnent ≥ 11 SANS solveur. Et Kombarov 2011
décrit la structure de TOUS les circuits minimaux (n − 1 blocs
standard) — le jumeau {∧, ∨, ¬} de la « *complete characterization of
the set of optimal circuits computing XOR* » que la candidature cite
chez CDJ pour la base DeMorgan. Le sous-lemme est donc réplication à
100 % (Schnorr, Red'kin, Knuth) — déclarée pour deux tiers, manquée
pour le tiers « contributif » — et la réserve PR-002 elle-même était
fermable par citation. Régime n° 3 (re-démonstration de folklore) sous
sa forme bénigne (réplication déclarée), aggravé de la citation
manquée.

### Charge 5 — Un premier pas qui « ne peut pas blesser » n'est pas un premier pas

Le champ 6 du prompt exige un sous-lemme dont les deux issues bougent
la cellule. Ici les deux issues (conforme / écart) parlent de
l'instrument, pas de la famille — la candidature le dit. C'est
exactement le profil « carte » : une ligne documentaire n'a pas de
premier pas atelier, elle a un audit fondateur. Le premier pas d'une
ligne 21 est A-024, pas une synthèse exacte.

## 4. Barrières (§5.4)

- **Relativisation** : route directe sans objet structurel (lit le
  circuit) — conforme ; route indirecte : bloquée à la marche NP (Wilson
  1985 — à vérifier sur texte, comme la candidature le dit).
- **Preuves naturelles** : s'applique au bout superpolynomial de
  l'énoncé, PAS à la frontière (charge 2) ; naturalité de l'élimination
  de portes à établir sur texte (constructivité du disperser affine
  douteuse) ; Chow : la largeur relâchée à 2^{−quasipoly} suffit — la
  barrière est fragile là même où elle s'applique.
- **Algébrisation** : route directe non arithmétisée — sans objet ;
  route indirecte : AW verbatim (dépôt) + Chen-Hu-Ren ITCS 2026 (cellule
  16) — bloquée deux fois à NP.
- **Monotone** : ligne 5, pas de transfert — conforme.
- **Le verrou réel de la ligne** (recalibré) : pas une barrière — un
  THÉORÈME DE LIMITE DE MÉTHODE (GHKK) sur la seule technique, plus
  l'explicité (10n ouvert pour des fonctions de P), plus l'absence de
  toute flèche de la famille vers NP. Les critères (a) (remplir une
  cellule) et (b) (tester une barrière) : (a) est actif — la cellule
  n'existe pas et sa carte de barrières est atypique (quatre colonnes
  « sans objet à la frontière ») ; (b) n'est pas éteint à vide — la
  ligne teste précisément que les barrières classiques ne sont PAS ce
  qui arrête la route directe.

## 5. Contre-vérification exécutable (§5.3) — instrument indépendant

Antériorité chiffrée AVANT calcul : Schnorr 1974 (U₂ : 3(n − 1) = 3, 6,
9) ; Red'kin 1970/73 (NOT-payant : 4(n − 1) = 4, 8, 12) ; Markov 1958
(+ Schnorr ⟹ XOR₄ ≥ 11) ; Knuth 7.1.2 (B4 : max 7 ; B5 : max 12, une
classe — Goucher 2019). Tout ce qui suit est RÉPLICATION VÉRIFIANTE
DÉCLARÉE, et sert de témoin exécutable à la cellule.

Instrument : `checks/pr007_synthese_exacte.py` — synthèse exacte par
SAT (pysat / CaDiCaL 1.9.5), encodage KKY 2009 / Knuth 7.2.2.2 (paire
d'entrées par porte, 4 bits de fonction, valeurs par ligne ; cassages de
symétrie : porte non finale lue, pas de doublon, ordre lexicographique
des portes indépendantes — désactivables par `--nosym`) ; témoin
re-vérifié par simulation indépendante ; UNSAT = certificat solveur
sans DRAT (réserve habituelle). Classes NPN par numpy (222 classes,
Σ tailles = 65 536, assertions).

Résultats — voir `data/pr007_synthese_exacte.md` pour les commandes,
durées et témoins :

| Mesure | Attendu (antériorité) | Mesuré |
|---|---|---|
| d(XOR_n), n = 2..6 (Markov) | ⌊n/2⌋ | 1, 1, 2, 2, 3 — conforme ; ⟹ XOR₄ ≥ 9 + 2 = 11 |
| Seuil de comptage : premier n où une fonction (non explicite) exige > 3n portes | — | **n = 8** (s* = 24 = 3n ; s* = 2, 4, 7, 13 pour n = 4..7) |
| C_{U₂}(XOR_n), n = 2, 3, 4 | 3, 6, 9 (Schnorr) | **3, 6, 9** (n = 4 : 8 UNSAT en 1 099 s, 9 SAT en 11 s, témoin en trois blocs de 3 re-vérifié) |
| C_{NOT-payant}(XOR_n), n = 2, 3, 4 | 4, 8, 12 (Red'kin) ; ≥ 11 (Markov + Schnorr) | 4, 8 (= PR-002) ; **n = 4 : 10 UNSAT (603 s) ; 11 UNSAT dans l'unique configuration possible (9 binaires, 2 NOT), avec ET sans cassage de symétrie (304 s / 308 s) ; 12 SAT, témoin re-vérifié (194 s) ⟹ XOR₄ = 12** |
| C_{B₂}(XOR_n), n = 3, 4 | 2, 3 | 2, 3 |
| B4 sur B₂ : max sur les 222 classes NPN | 7 (Knuth) | **7** — 12 classes / 2 720 fonctions à coût 7 ; histogramme par fonctions 10 / 60 / 456 / 2 474 / 10 624 / 24 184 / 25 008 / 2 720 (= la table de Knuth, de mémoire — texte non ouvert) ; 222/222 conclues, 1 115 s |

**Ce que ces chiffres disent de la candidature** : rien qui puisse la
blesser — c'est écrit dans son texte — et rien qui la fonde : ils
calibrent un instrument que le dépôt possédait déjà (PR-002) sur des
valeurs publiées depuis 1958-1974 (Markov, Red'kin, Schnorr) et 2008
(Knuth). Le seul effet sur le dépôt est la fermeture de sa propre
réserve PR-002 — par citation d'abord, par solveur ensuite.

## 6. Folklore-check (§5, champ 5) — bilan

Exact et vérifié : CDJ 2026 ; CJSW 2021/2024 ; GHKK 2016 ; Li-Yang 2022
(abstract) ; AW 2008 ; Knuth n = 5 (secondaire) ; KPS 2022 ; Chow 2008.
Manqué par la candidature : **Red'kin 1970/73** (4n − 4 en {∧, ∨, ¬}),
**Markov 1958** (⌈log₂(d + 1)⌉ négations), **Kombarov 2011** (structure
de tous les circuits minimaux de XOR — le jumeau de CDJ). Non vérifiés
dans cette instruction, à l'audit : RR verbatim sur les bornes
générales ; Wilson 1985 ; corps de Li-Yang sur GHKK ; texte de Knuth
(le « 7 » est mesuré ici, pas lu).

## 7. Verdict (§5.5) et conditions

**LACUNE RÉPARABLE — sous conditions.**

- **Constitué** : le faux raccord énoncé/technique (charge 1 — à
  recalibrer, pas fatal : la famille existe, c'est son énoncé qui est
  mal étiqueté) ; le pincement mal localisé (charge 2) ; le test de
  plafond hors sujet (charge 3) ; le folklore-check troué sur le seul
  morceau « contributif » (charge 4) ; l'absence de premier pas
  discriminant (charge 5 — assumée).
- **Debout** : le trou de l'Atlas ; la carte des sources (CDJ, CJSW,
  GHKK, LY, AW, Chow, Kannan/S₂E) ; l'honnêteté de la portée déclarée ;
  la lecture « constructivité » (CJSW ⟹ CDJ) comme seul front vivant de
  la route.
- **Conditions d'entrée d'une ligne 21** (précédents A-021/A-022 : une
  ligne naît de son audit fondateur) — **A-024**, audit type A :
  (i) RR verbatim sur les bornes générales + la question de
  constructivité du disperser affine ; (ii) GHKK : la formalisation
  exacte et la valeur de c, et si Li-Yang 3,1n est sous ou hors de ce
  plafond (corps du texte) ; (iii) Blum 1984 / FGHK 2016 / LY 2022 :
  les énoncés numérotés et la classe des fonctions (dans P) ; (iv)
  CJSW : le théorème exact pour P ≠ NP (numéro) ; CDJ : les refuteurs
  numérotés ; (v) Wilson 1985 ; (vi) Red'kin (référence primaire et
  date), Kombarov 2011 (structure), Knuth 7.1.2 (le 7 et le 12 sur
  texte). **Énoncé visé recalibré** : « une fonction explicite (P ou NP)
  exige > cn portes pour c > 3,1 — puis superlinéaire — 10n ouvert » ;
  chaîne vers P vs NP : AUCUNE flèche de la famille (à écrire tel quel,
  comme le fait la ligne 20 pour sa flèche manquante). **Verrou** :
  théorème de limite de méthode + explicité ; barrières « sans objet à
  la frontière », RR au bout superpolynomial seulement.
- **Refusé** : la fusion en « route principale écrite en tête de la
  matrice » — la ligne est l'unité de l'Atlas ; un paragraphe de
  chapeau redeviendrait « citer le dossier au lieu de la cellule »
  (CLAUDE.md §5.4, dérive des Tours 26-27). Refusé aussi : tout fil
  atelier sur cette ligne — pas d'avatar ν ≤ 8 (charge 3), la leçon
  échelle payée trois fois (SYM∘AND, ALG, ici par théorème).
- **Leçon pour le prompt v4** : le champ 4 (test de plafond) doit
  nommer LE PHÉNOMÈNE DE LA TECHNIQUE (ce que le mécanisme consomme),
  pas un phénomène d'existence ; et une candidature qui déclare son
  sous-lemme non discriminant doit se présenter comme LIGNE
  DOCUMENTAIRE avec son audit pour premier pas — catégorie à créer dans
  le prompt (précédents : lignes 15, 16, 20 côté dépôt).

## 8. Pièces et sources

Instrument et données : `checks/pr007_synthese_exacte.py`,
`data/pr007_synthese_exacte.md` ; fiche : `tasks/done/PR-007.md`.
Sources ouvertes dans cette instruction (verbatims cités ci-dessus) :
[CDJ, arXiv 2604.23958](https://arxiv.org/abs/2604.23958) ;
[GHKK, MFCS 2016 (DROPS)](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.MFCS.2016.46) ;
[Li-Yang, ECCC TR21-023](https://eccc.weizmann.ac.il/report/2021/023/) ;
[Kombarov 2011 (CyberLeninka) — cite Red'kin](https://cyberleninka.ru/article/n/o-minimalnyh-shemah-dlya-lineynyh-bulevyh-funktsiy) ;
[Markov 1958 — énoncé via arXiv 1506.04485](https://arxiv.org/abs/1506.04485) ;
[CJSW — FOCS 2021 PDF](https://ieee-focs.org/FOCS-2021-Papers/pdfs/FOCS2021-5stbVHiOp5jRHWlSl41FkR/205500a646/205500a646.pdf) ;
[Chow, arXiv 0805.1385](https://arxiv.org/abs/0805.1385) ;
[KPS, arXiv 2102.12579](https://arxiv.org/abs/2102.12579) ;
[Goucher 2019, five-input circuits (Knuth n = 5)](https://cp4space.hatsya.com/2019/05/28/five-input-boolean-circuits/) ;
AW 2008 : `bib/aaronson_wigderson_2008.md` (dépôt). Non ouverts : RR
1994/97 (403/404), Wilson 1985, Knuth 7.1.2 (texte), Red'kin (texte
primaire), Kombarov lower_bounds.pdf (certificat TLS invalide).
