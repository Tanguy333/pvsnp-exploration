# CANDIDATURE PR-005 — La frontière algorithmique THR∘THR : attaquer le seul moteur qui convertit des algorithmes en séparations, au point exact que le dépôt instrumente

> **⚠ CORRECTION MARQUÉE (2026-08-11, ALG-001 — le sous-lemme exécuté
> a pris SON PROPRE AUTEUR)** : la candidature confond DEUX mesures —
> le mur 20/119/640 de F-001 est le poids **PTF** (représentation en
> signe), tandis que les lois du corpus MC sont le poids **MinSYM+**
> (couvert exact) ; or W_MinSYM+(IP_{2k}) ≤ k trivialement (p = Σ
> m_{paires} : valeurs impaires/paires disjointes — IP est un SYM∘AND
> de k portes, structure Beigel-Tarui). La prémisse « le mur F-001
> est mesuré par les lois MC » est FAUSSE telle qu'écrite ; le champ 6
> a fait exactement son travail en la falsifiant en secondes
> (`data/alg001_poids_restrictions.md`). Le verrou de la ligne 7 et la
> direction du fil restent ; le PARAMÈTRE à mesurer est recalibré :
> le poids PTF sous restrictions (ALG-002 candidate), en attente de
> l'audit A-023 sur le paramètre exact que le transfert consomme.

> **⚠ SECONDE CORRECTION MARQUÉE (2026-08-11, A-023 tombé — la
> candidature est INSTRUITE ET CLOSE, le fil ALG avec elle)** :
> (1) L'ATTRIBUTION du champ 3 était fausse : la flèche « CAPP ou
> SAT poly-taille THR∘THR en 2ⁿ/n^{ω(1)} ⟹ NEXP ⊄ THR∘THR » est
> vraie mais n'est PAS un théorème de « Williams 2011 /
> Murray-Williams 2018 » (leurs clôtures ne tiennent pas pour
> THR∘THR — Williams a nommé l'obstacle en 2014, note 6) : c'est
> **Chen-Williams CCC 2019, Theorem 8** (⊕₂-clôture + PCPP à 2
> requêtes). (2) La FRONTIÈRE était périmée : CTW26 (STOC 2026,
> mars) donne CAPP déterministe pour ⊕₂∘THR∘THR jusqu'à n^{2.5−ε}
> portes et E^NP ⊄ THR∘THR[n^{2.5−ε}] ; poly-taille reste ouvert.
> (3) Le transfert ne consomme AUCUN paramètre de poids — le mur
> F-001 ne barre même pas la route CAPP (CW19 Cor 10) : le critère
> (ii) de PR-006 (paramètre-goulot atelier discriminant) MANQUE.
> ALG-002 annulée ; clôture par la règle pré-déclarée. Pièces :
> `bib/transfert_thrthr.md`, `tours/candidature_pr005_autorefutation.md`,
> `tasks/done/A-023.md`.

> Candidature INTERNE (Réfuteur devenu proposant, sur ordre utilisateur
> du 2026-08-11 : « refait moi une proposition et crois en toi » —
> dérogation PONCTUELLE à la règle 1 de CLAUDE.md §8, consignée ici).
> Conflit de rôles déclaré : l'instruction adverse de cette candidature
> ne peut pas être faite par son auteur — proposition : INVERSER le
> dispositif et confier la réfutation à Qwen (prompt réfuteur à
> préparer), ou à une passe VER dédiée. Ceci n'est PAS une 21ᵉ ligne :
> c'est un FIL, rattaché au verrou de la ligne 7 — et c'est voulu
> (voir POSITIONNEMENT).

---

[EN-TÊTE DE RECEVABILITÉ]

1. **Énoncé visé** : « Il existe un algorithme déterministe pour
   #SAT (ou CAPP) sur les circuits THR∘THR de taille polynomiale en
   temps 2ⁿ/n^{ω(1)} — et donc, par le transfert de Williams,
   NEXP ⊄ THR∘THR : la première séparation au-dessus d'ACC⁰ depuis
   2011. »
2. **Classes de complexité** : NEXP, THR∘THR (TC⁰ profondeur 2), ACC⁰,
   P, NP via l'échelle.
3. **Chaîne vers P vs NP** : algorithme #SAT/CAPP non trivial pour
   THR∘THR [OUVERTE — le cœur du fil] ⟹ NEXP ⊄ THR∘THR [PROUVÉE
   modulo audit : le cadre Williams 2011 / Murray-Williams 2018,
   easy-witness — les conditions exactes pour THR∘THR sont à
   verbatimer, audit fondateur A-023] — puis, HONNÊTETÉ TOTALE : il
   n'y a PAS de troisième flèche. NEXP ⊄ THR∘THR est un barreau, pas
   P ≠ NP ; c'est l'échelle de Williams (ACC⁰ → TC⁰ → NC¹ → P/poly)
   dont P vs NP est la limite, et c'est LE SEUL programme de toute la
   matrice qui ait jamais franchi les trois barrières (ligne 7,
   précédent unique). Maillon le plus faible : la première flèche —
   nommé depuis 2014 dans la littérature comme LA frontière ouverte
   du programme.
4. **Test de plafond** : le phénomène que le fil exploite — le poids
   SYM+ comme paramètre de contrôle de l'évaluation par lots — vit
   exactement à l'échelle du dépôt : les lois W sont PROUVÉES sur les
   fonctions à 1-2 points (corpus MC), les mesures exactes existent à
   n = 4, 6, 8 (F-001 : EXACT_k poly O(n²) contre IP exponentiel
   20/119/640), le solveur MinSYM+ est certifié à ν ≤ 8. Le premier
   pas (champ 6) est intégralement sous ce plafond. La cible
   asymptotique (l'algorithme) vit au-delà — le fil le sait et ne
   revendique que ce qu'il mesure.
5. **Folklore-check** : (a) Williams 2011 (JACM 2014) — le transfert
   algorithme ⟹ borne, NEXP ⊄ ACC⁰, seul franchissement des trois
   barrières (audits A-001/A-002b du dépôt) ; (b) Williams 2014
   (STOC) — SAT pour ACC∘THR en 2^{n−n^ε} via la représentation SYM+
   et l'évaluation rapide par multiplication de matrices : LE gabarit
   exact que le fil veut pousser d'un cran ; (c) Alman-Chan-Williams
   FOCS 2016 (polynômes probabilistes pour les seuils) et
   Murray-Williams STOC 2018 (easy witness raffiné, NTIME[2ⁿ]) — les
   outils de la frontière ; le problème « SAT non trivial pour
   THR∘THR » est NOMMÉ OUVERT dans cette littérature. Ce qui distingue
   le fil : il n'invente pas le programme, il l'attaque avec un
   instrument que la littérature n'a pas — les LOIS EXACTES du poids
   SYM+ (MinSYM+, objet du dépôt, [NON TROUVÉ] confirmé par MC-002
   sur ~50 requêtes) et leur comportement mesurable SOUS RESTRICTIONS.
6. **Sous-lemme vérifiable (double calibration, exécutable avec les
   instruments existants)** : le POIDS SOUS RESTRICTIONS. Pour
   ρ une restriction fixant aléatoirement la moitié des variables :
   (a) CONTRÔLE — W(EXACT_k|ρ) doit rester polynomial (la structure
   survit : EXACT_k restreint est un EXACT_j translaté) ; (b) LA
   QUESTION — W(IP_{2k}|ρ) pour k = 2, 3, 4 (ν = 4, 6, 8 : l'échelle
   certifiée du solveur), sur ≥ 20 restrictions aléatoires par
   taille : le poids exponentiel de IP (le mur mesuré de F-001)
   S'EFFONDRE-t-il en moyenne sous restriction, ou résiste-t-il ?
   Si effondrement (médiane W(IP|ρ) polynomiale en la taille
   restante) : la voie « restrictions puis SYM+ » vers l'algorithme
   THR∘THR a son premier fondement mesuré — le cœur dur est mince.
   Si résistance : le mur de F-001 est plus profond que mesuré, la
   voie directe est morte plus haut, et la cellule ligne 7 gagne un
   verrou quantifié neuf. Les deux issues bougent la cellule.
   Antériorité : le comportement de CE poids sous restrictions est
   vraisemblablement non publié (l'objet est propre au dépôt) — à
   re-vérifier néanmoins avant toute revendication (règle
   permanente) ; les analogues publiés (degré/corrélation sous
   restrictions, switching) sont le contexte, pas l'objet.
7. **Direction** : P ≠ NP (par l'échelle de Williams — la seule qui
   ait jamais avancé).

[LA FAMILLE / LE FIL]

Le fil ne propose pas une famille neuve : il propose d'ARMER la
famille la plus forte de la matrice. La ligne 7 est l'unique ligne
ayant franchi les quatre barrières, et son verrou est écrit depuis
2011 : « aucun algorithme SAT non trivial au-delà d'ACC⁰ ». Le dépôt
a passé des mois à construire, sans le viser, l'instrument exact de ce
verrou : la théorie du poids SYM+ minimal (MinSYM+) — lois prouvées
(G, F, sélecteur, bornes B1/B2), murs mesurés (le partage en espace
partagé, la croissance du déficit), et surtout la CARTE DU COÛT de la
représentation que l'algorithme de Williams 2014 consomme. L'invariant
central du fil : W(f) est le prix d'entrée de l'évaluation par lots ;
la sous-classe poly-W a un algorithme (gabarit Williams 2014) ; le
cœur exponentiel (IP et sa famille, F-001) est l'obstacle NOMMÉ ET
MESURÉ. Le mécanisme du fil : cartographier le cœur dur (est-il
mince ? s'effondre-t-il sous restrictions ? se décompose-t-il ?) avec
les lois exactes, jusqu'à ce que la structure révélée dicte soit un
algorithme (la cible), soit un verrou quantifié (l'élimination
documentée — la mission de l'Atlas dans les deux cas).

[POSITIONNEMENT]

Ligne la plus proche : la 7 — et ce fil EST son programme : c'est
assumé et c'est l'argument. Les trois candidatures précédentes ont
produit des lignes de carte (19, 20) dont l'utilisateur constate
qu'elles ne mènent pas à P vs NP ; la réponse honnête n'est pas une
carte de plus, c'est le seul verrou de la matrice dont l'ouverture a
un théorème de conversion au bout. Distinction d'avec les fils clos :
SYM∘AND (clos) visait la borne inférieure par le poids — plafonné
polynomialement, test de plafond violé ; MC (clos) visait la
NP-complétude de la MESURE — la méta-question ; ce fil vise
l'ALGORITHME que le poids contrôle — la question directe de la ligne
7, jamais ouverte par le dépôt. Lignes 11 et 18 : ses réservoirs
d'instruments, pas ses concurrentes.

[BARRIÈRES]

- Relativisation : le fil hérite du statut de la ligne 7 — le
  transfert de Williams est LE précédent non-relativisant (audit
  A-001 : « definitely avoids relativization and algebrization »,
  l'algorithme LIT le circuit) ; la direction algorithmique n'est pas
  un argument boîte-noire par nature.
- Preuves naturelles : la borne obtenue par transfert n'est pas une
  propriété large de tables (c'est l'argument de Williams lui-même —
  la non-constructivité vit dans le easy-witness) ; et D-005 (l'auto-
  test du dépôt) a établi que le programme de MESURE échapperait à RR
  par la non-constructivité — le versant algorithmique n'est pas
  concerné structurellement (il produit des algorithmes, pas des
  propriétés).
- Algébrisation : héritée franchie (même précédent, A-001) ; le point
  sera re-vérifié pour la variante THR∘THR dans l'audit fondateur
  (A-023) — pas d'exemption par omission.
- Monotone : sans objet (seuils signés, aucun modèle monotone).

[PREMIER PAS]

Instance : le sous-lemme du champ 6, exécutable AUJOURD'HUI avec
`checks/` existants (solveur MinSYM+ certifié ν ≤ 8, lois MC pour les
contrôles croisés, F-001 pour les valeurs non restreintes 20/119/640).
Protocole : pour k = 2, 3, 4, tirer ≥ 20 restrictions ρ (moitié des
variables, valeurs aléatoires, graine consignée) ; calculer W(IP|ρ) et
W(EXACT_k|ρ) EXACTS ; livrer médianes, extrêmes, et la comparaison
aux lois prouvées quand la fonction restreinte tombe dans une famille
connue (validation croisée interne). Résultat qui réfuterait le fil :
contrôle EXACT_k non polynomial (instrument faux) — ou, sur le fond,
une résistance totale du poids de IP sous restrictions ET sous les
décompositions de la deuxième vague (le fil devrait alors consigner
son propre mur et s'arrêter, règle 5 : échec honnête).

[CE QUI MANQUE]

1. Le transfert exact pour THR∘THR : les conditions de Murray-Williams
   (easy witness, clôtures de classe) doivent être verbatimées et
   vérifiées pour cette classe précise — audit fondateur A-023,
   PRÉALABLE à toute revendication de la flèche 2 (précédents
   ATLAS-013/A-021/A-022 : l'ancrage précède la ligne… ici, le fil).
2. Le fossé mesure→algorithme : même un cœur dur mince ne donne pas
   automatiquement l'algorithme — il faut le lemme d'évaluation par
   lots adapté (multiplication de matrices, à la Williams 2014) pour
   la partie poly-W et un traitement du cœur ; c'est le vrai travail,
   et il est nommé dès le départ.
3. Le plafond de l'échelle : ν ≤ 8 mesure des constantes, pas des
   asymptotiques (leçon `atlas/echelle_instrument.md`, payée deux
   fois) — chaque tâche du fil devra passer le test de plafond
   individuellement, et le fil accepte d'avance qu'un verdict
   asymptotique puisse être hors de portée de l'atelier : dans ce cas
   sa livraison est le verrou quantifié, pas l'algorithme.

---

*Pourquoi j'y crois — en une phrase, pour l'instruction adverse à
venir : toutes les autres voies de la matrice exigent une idée qui
n'existe pas encore ; celle-ci exige de pousser d'un cran une machine
qui a déjà tourné une fois (2011), avec des instruments exacts que le
dépôt est le seul à posséder — et elle est falsifiable dès la première
mesure.*
