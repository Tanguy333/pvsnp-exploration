# Instruction de candidature — « Algorithmes holographiques / signatures matchgate » — SURVIT (sous conditions)

Date : 2026-08-08. Tâche : PR-003. Deuxième candidature du générateur
PR-001 (Proposeur : Qwen), instruite par le Réfuteur (procédure
CLAUDE.md §5). **Pas un Tour adverse** : instruction d'une candidature
de ligne (la candidature s'intitule « 20ᵉ famille » — ce serait la
19ᵉ ligne, la matrice en compte 18 ; cosmétique).

## 0. La candidature, fidèlement résumée

Famille : algorithmes holographiques / signatures matchgate
(Valiant 2004/2008 ; Cai-Lu ; Cai-Lu-Xia) — gadgets pondérés composés
par couplages parfaits, changement de base commun T ∈ GL₂
(reconnaisseurs covariants T⊗k, générateurs contravariants (T⁻¹)ᵀ⊗k),
évaluation polynomiale par FKT/Pfaffien sur graphe plan. Mesure
centrale : la RÉALISABILITÉ d'un ensemble de signatures sous base
commune (système polynomial fini : parité + identités de matchgate).
Direction : P = NP (première candidature dans cette direction —
l'Atlas n'en a aucune), avec l'honnêteté affichée : « la probabilité
que cette famille aboutisse est minime ; sa valeur réaliste est
l'élimination documentée ». Sous-lemme SL-19 : réalisabilité
SIMULTANÉE {OR₃ = [0,1,1,1], =₃ = [1,0,0,1]} sous base commune —
attendu : infaisable sur ℚ(i), faisable sur F₇ (« miracle de
Valiant ») ; double calibration. Pré-calcul du Proposeur joint : OR₃
SEUL passe la parité (T = [[1,−2],[1,0]]) — d'où l'exigence de
simultanéité.

**Reformulation en une phrase** : cartographier jusqu'où montent les
annulations holographiques (les « accidents » à la Valiant), avec la
réalisabilité simultanée sous base commune comme instrument exécutable,
et les dichotomies de Cai-Lu-Xia comme verrou nommé.

## 1. Contre-vérification exécutée (`checks/pr003_holographique.py`)

Le script re-dérive toutes les signatures transformées par calcul
symbolique générique (aucune formule manuscrite n'est crue sur parole),
implémente la CONDITION DE PARITÉ (nécessaire pour toute signature
matchgate ; les identités au-delà de la parité pour l'arité 3 :
[À TRANCHER SUR TEXTE Cai-Lu] — une infaisabilité sous parité seule
est donc un verdict SÛR, une faisabilité n'est qu'une candidature),
et sature det ≠ 0.

**Résultats (2026-08-08, mesurés)** :

| volet | résultat |
|---|---|
| A — pré-calcul du Proposeur | **CONFORME** : T = [[1,−2],[1,0]] rend OR₃ de parité paire (impaires [0,0,0,0], paires [−2,−2,−2,−2]) — le test individuel est bien non-discriminant |
| B — SL-19 char 0, {OR₃,=₃}, Gröbner sur ℚ, det saturé | **INFAISABLE dans les 4 combinaisons de parités** — certificat 1 ∈ idéal à chaque fois (< 0,1 s) : aucun corps de caractéristique 0 n'admet de base commune (verdict PLUS FORT que le ℚ(i) demandé) |
| C — force brute exhaustive GL₂(F_p), p ∈ {3, 5, 7, 11, 13} | {OR₃,**=₃**} : **infaisable PARTOUT, y compris p = 7** ; {OR₃,**=₂**} (contrôle ajouté par le Réfuteur — la vraie configuration lecture-deux-fois de Valiant 2004) : **FAISABLE UNIQUEMENT à p = 7** (72 bases, témoin T = [[1,2],[1,3]], det = 1) — infaisable à 3, 5, 11, 13 |

**Trois enseignements** :

1. La jambe porteuse de la calibration (char 0 infaisable) est
   CONFIRMÉE, en force maximale. C'est la première cellule de la
   future ligne, si elle est créée : « {OR₃, égalités} sous base
   commune est mort en caractéristique 0 dès le niveau parité ».
2. **PRISE de l'instruction : la candidature a mal spécifié sa
   calibration F₇.** Sa paire {OR₃, =₃} (lecture-trois-fois) est
   infaisable À p = 7 AUSSI — le « miracle de Valiant 2004 » est
   lecture-DEUX-fois (#₇Pl-**Rtw**-Mon-3CNF : =₂, pas =₃). Telle
   qu'écrite, la double calibration aurait échoué sur sa jambe F₇ non
   par défaut d'instrument mais par erreur de spécification. Le
   contrôle {OR₃, =₂} ajouté par l'instruction valide l'instrument ET
   rétablit la calibration : faisable à 7 (au niveau parité, cohérent
   avec le théorème de Valiant — construction complète à auditer sur
   texte), infaisable ailleurs.
3. Le balayage en p montre le miracle lecture-deux-fois UNIQUE à
   p = 7 dans {3, 5, 7, 11, 13} — la « spécialité de 7 » est un fait
   mesuré du scan, pas une légende. (Une dérivation manuscrite du
   Réfuteur prédisant « =₃ faisable à p = 7 par la condition p | 28 »
   a été CONTREDITE par la force brute et est RETIRÉE — les analyses
   de branches à la main des deux parties ont chacune fauté une fois
   dans cette instruction ; seul le calcul exhaustif a fait foi.)

## 1 bis. Contre-vérification croisée indépendante (ajout du 2026-08-08, même jour)

Un SECOND instrument, écrit indépendamment côté utilisateur
(`checks/pr001_sl19_holographique.py`), avec la **convention DUALE**
(générateur ↔ reconnaisseur inversés : =_k transformé par T⊗k, OR₃
par l'adjugate — la bijection T ↔ (Tᵀ)⁻¹ prédit l'équivalence), a été
RÉPLIQUÉ par la session. **Concordance totale, case par case** :

| case | instrument Réfuteur (pr003) | instrument utilisateur (pr001_sl19, répliqué) |
|---|---|---|
| {OR₃,=₃} sur ℂ | infaisable 4/4 (1 ∈ idéal) | infaisable 4/4 (1 ∈ idéal) |
| {OR₃,=₃} sur F₇ | infaisable (exhaustif) | infaisable 4/4 (exhaustif) |
| {OR₃,=₂} sur ℂ | — (contrôle char p seul) | **infaisable 4/4 (1 ∈ idéal)** — complète le tableau |
| {OR₃,=₂} sur F₇ | FAISABLE, 72 bases, témoin [[1,2],[1,3]] | FAISABLE, 72 = 36 (pair/pair, témoin T = (1,1,2,3)) + 36 (pair/impair) |

Le compte 72 concorde à travers les deux conventions ; le second
instrument ajoute le découpage par combinaison de parités et ferme
AUSSI {OR₃,=₂} sur ℂ (la case que pr003 n'avait testée qu'en char p).
Les deux lectures du même fait — « calibration mal spécifiée » (§1,
prise de l'instruction) et « découverte bonus : le miracle exige le
lu-deux-fois » (lecture utilisateur) — sont équivalentes ; la
formulation de cellule retenue : **la frontière du miracle mod 7 est
exactement le fanout 2, mesurée par calcul, par deux instruments
indépendants concordants**. La réserve « un seul cycle d'instruction /
lecture unique » de la fiche est LEVÉE pour le volet calcul.

## 1 ter. Retours de l'audit fondateur A-021 (ajout du 2026-08-08, même jour)

L'audit A-021 (`bib/holant_paysage.md`, 17 textes in extenso) a rendu
sur les pièces de cette instruction :

1. **PROMOTION DES INSTRUMENTS** : à l'arité ≤ 3, la condition de
   parité est nécessaire ET SUFFISANTE (matchgate ⟺ parité — Cai-Fu,
   Lemma 2.27 d'arXiv:1603.07046, source première Inf. Comput. 2014 ;
   re-démontré exécutablement par l'agent : MGI k ≤ 3 identiquement
   nulles sous parité). **Les verdicts « faisable » de PR-003/PR-001
   sont donc des RÉALISABILITÉS PROUVÉES, plus des candidatures** —
   la réserve « périmètre parité seule » ne subsiste que pour
   l'arité ≥ 4.
2. **Folklore-check des faits mesurés** : le fait (i) ({OR₃,=₂} à
   p = 7 seul) est un THÉORÈME PUBLIÉ (Valiant FOCS 2006 Th. 4.1 —
   témoins explicites — + Cai-Lu JCSS 2011 Th. 5.1 : le module divise
   2³ − 1, « why 7 is special ») → statut : réplication vérifiante
   par deux instruments indépendants. Le fait (ii) (frontière
   fanout-2) est ÉNONCÉ par Cai-Lu (§5.2 : « empty intersection on
   M », « can be shown ») SANS preuve détaillée → nos certificats
   (1 ∈ idéal char 0, exhaustif GL₂(F_p)) sont la première
   vérification exécutable avec certificats rencontrée par l'audit
   pour (l, k) = (3, 3) — la valeur est le certificat, pas l'énoncé.
   Le compte 72 bases : non recensé ; lecture d'audit = 2 orbites × 36
   du manifold M (calculable, non vérifiée).
3. **Correction d'identification** : « Accidental Algorithms » = FOCS
   **2006** (pas 2004 — erreur de la candidature reconduite par
   l'instruction ; FOCS 2004 = « Holographic algorithms (extended
   abstract) »). La méthode historique de découverte est le solveur
   formel (Singular) — notre instrument est une instance du SRP de
   Cai-Lu (problème nommé, décidable en P, Th. 4.1 JCSS 2011) :
   légitimité totale, originalité nulle, déclarée.
4. **La ligne 19 est CRÉÉE** (la condition du §3 est remplie) — voir
   la matrice et `bib/holant_paysage.md`.

## 2. Positionnement et recevabilité (grille PR-001)

| Champ | État |
|---|---|
| Énoncé, classes, chaîne | Conformes ; chaîne logiquement correcte, maillon faible honnêtement désigné (la 1ʳᵉ flèche, fermée dans les cadres dichotomisés) |
| Test de plafond | EXACT : le mécanisme vit à l'échelle des gadgets (4-8 inconnues) — vérifié par l'exécution même de SL-19 |
| Folklore-check | Adéquat comme minimum (Valiant 2004/2008, Cai-Lu, CLX) et honnête sur son statut (« un minimum, pas un acquis ») ; l'audit type A devra ajouter les dichotomies plus récentes (universalité planaire Cai-Fu, Holant complet) qui rétrécissent encore les poches |
| Sous-lemme | Exécutable, exécuté ; jambe char 0 confirmée ; jambe F₇ MAL SPÉCIFIÉE (=₃ au lieu de =₂), corrigée par l'instruction — le principe de double calibration reste valide et validé |
| Positionnement | Correct : distinct de la ligne 7 (algorithmes POUR le versant P = NP, sans détour par une borne) ; mécanisme (annulation par base commune + Pfaffien) et verrou (dichotomies) absents des 18 lignes ; premier front en direction P = NP, recevable depuis la mission 2026-08-07 |
| Barrières | Les « sans objet » sont structurellement défendables (les 3 barrières bornent des preuves de SÉPARATION ; RR exige des propriétés larges que la famille ne produit pas) — UNE imprécision : l'argument BGS cite la cohérence avec l'oracle A, mais l'oracle B (P^B ≠ NP^B) interdit aussi les preuves RELATIVISANTES de P = NP ; la vraie échappatoire est que la réduction holographique est une construction explicite non-boîte-noire. La lecture duale est correctement non survendue par la candidature elle-même |
| Régimes d'échec | Aucun constitué : pas de spéculation sous barrières (mécanisme prouvé sur des cas réels), pas de dérive (classes nommées partout), pas de folklore revendiqué (aucune nouveauté prétendue), pas d'esquive (sous-lemme falsifiable — et effectivement pris en défaut partiel par l'exécution) |

## 3. VERDICT : SURVIT (sous conditions) — recevable comme candidature de ligne 19

La candidature passe l'instruction : famille réelle et distincte des
18 lignes, direction absente de l'Atlas et recevable par la mission,
honnêteté épistémique conforme aux règles, sous-lemme exécuté avec une
jambe confirmée et une jambe corrigée (la correction étant elle-même
un produit de l'instruction, pas un rejet : le mécanisme visé existe —
à p = 7, en lecture-deux-fois).

**Conditions posées à la création de la ligne 19** (garde-fou
anti-auto-référence, précédent ATLAS-013 : l'ancrage bibliographique
précède et fonde la ligne) :

1. **Audit type A préalable sur textes** (A-021 candidate) : Valiant
   SIAM JC 2008 (le cadre), Valiant FOCS 2004 (le miracle mod 7,
   configuration exacte), Cai-Lu (identités de matchgate — trancher la
   question d'arité 3 laissée ouverte par le test parité-seule), le
   paysage des dichotomies (CLX ; universalité planaire) avec les
   attributions de #P-dureté exactes. La ligne citera le DOMAINE ;
   les pièces de PR-003 rempliront sa cellule « réalisabilité ».
2. Le verrou de la ligne s'écrira depuis l'audit (les dichotomies
   comme barrière interne de la famille), pas depuis la candidature.
3. Les trois manques listés par la candidature elle-même (planarité
   globale et unicité de base non testées ; char 0 vs char p ;
   dichotomies presque complètes) entrent au verrou tel quels.

**Corrections à porter si la ligne est créée** : la calibration
canonique de la famille est {OR₃, =₂} (pas =₃) ; « 19ᵉ ligne » (pas
20ᵉ) ; l'argument BGS reformulé (oracle B + non-boîte-noire).

## 4. Pièces

`checks/pr003_holographique.py` (volets A/B/C, re-dérivation
symbolique générique, Gröbner saturé, force brute exhaustive) ;
sortie complète dans le journal de session. Fiche :
`tasks/done/PR-003.md`.
