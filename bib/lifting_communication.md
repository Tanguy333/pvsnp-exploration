# A-014 : La famille « théorèmes de lifting / complexité de communication » — sources et verbatims

> Tâche type A. Exécutée le 2026-08-02. Objectif : créer la **ligne 17**
> de l'Atlas — la famille lifting requête → communication, absente de la
> matrice alors qu'elle est le moteur moderne des lignes 5 (bornes
> monotones) et 15 (complexité des preuves). Convention de vérification,
> reprise de [veille_2026_07.md](veille_2026_07.md) : **[V-primaire]** =
> document ouvert pendant la tâche (au minimum l'abstract lu verbatim) ;
> **[V-métadonnées]** = titre/auteurs/lieu vérifiés, contenu non lu.
> Un résumé de moteur de recherche n'est jamais une source. Ce qui n'a
> pas été lu est marqué [NON TROUVÉ] et récapitulé en §9.
>
> **Seconde passe (2026-08-02, même jour)** : deux vérifications croisées
> (chasse aux références ; survente/format/cohérence) ont été intégrées.
> Corrections : TR25-073 (aucune revendication de primauté dans le texte,
> restriction one-way restituée, ancrage de version — pièce 23, §7.2) ;
> portée du verbatim Beame-Koroth (§6.1) ; pagination KLMS (74 p., pièce
> 13) ; localisation de l'incohérence Göös (§8). Deux [NON TROUVÉ] levés
> par la seconde passe (dblp) : venue FOCS 2020 de dRMNPR (pièce 7) ;
> version STOC 2025 de TR24-128 (pièce 24). Vérifications primaires
> refaites le même jour : le comparatif « approximation method » est
> verbatim dans l'abstract CCC 2025 (pièce 28, §7.4) ; orthographe
> « Tulasimohan Molli » confirmée sur dblp.

## 0. Sources

### Fondations, applications, barrières

1. **Raz-McKenzie**, *Separation of the monotone NC hierarchy*, FOCS 1997,
   pp. 234-243 — [V-primaire] (abstract complet lu verbatim sur deux
   supports ouverts : dépôt institutionnel Weizmann et scan U. Washington ;
   le PDF FOCS est un scan image, **texte intégral non extrait** — les
   « DART games » ne sont connus ici que par l'abstract). Version
   Combinatorica 19(3):403-435, 1999, doi:10.1007/s004930050062 —
   [V-métadonnées] (page Springer non ouverte).
2. **Göös-Pitassi-Watson**, *Deterministic Communication vs. Partition
   Number*, ECCC TR15-050 (avr. 2015) — [V-primaire] (PDF intégral
   téléchargé, pages 1-3 extraites : Théorèmes 1-3 et gadget verbatim).
   Version SICOMP 47(6):2435-2450, 2018, doi:10.1137/16M1059369 —
   [V-métadonnées] (déjà consignée au cahier §7.3).
3. **Göös-Pitassi-Watson**, *Query-to-Communication Lifting for BPP*,
   ECCC TR17-053 (mars 2017) — [V-primaire] (abstract verbatim).
   FOCS 2017, pp. 132-143, et SIAM J. Comput. 49(4), 2020 —
   [V-métadonnées] (API dblp ; pagination SICOMP non obtenue).
4. **Chattopadhyay-Filmus-Koroth-Meir-Pitassi**,
   *Query-to-Communication Lifting Using Low-Discrepancy Gadgets*,
   arXiv:1904.13056 — [V-primaire] (abstract verbatim). ICALP 2019,
   35:1-35:15 (sous le titre « …for BPP Using Inner Product ») et
   SICOMP 50(1):171-210, 2021 — [V-métadonnées].
5. **Garg-Göös-Kamath-Sokolov**, *Monotone Circuit Lower Bounds from
   Resolution*, ECCC TR17-175 (nov. 2017) — [V-primaire] (abstract
   verbatim sur deux supports : ECCC et Theory of Computing 16, art. 13,
   2020 ; §1 du TR lu pour la réciproque de l'interpolation monotone).
   STOC 2018, pp. 902-911 — [V-métadonnées] (dblp).
6. **Göös-Jain-Watson**, *Extension Complexity of Independent Set
   Polytopes*, ECCC TR16-070 (avr. 2016) — [V-primaire] (abstract
   verbatim). FOCS 2016 ; SICOMP, doi:10.1137/16M109884X —
   [V-métadonnées].
7. **de Rezende-Meir-Nordström-Pitassi-Robere**, *KRW Composition
   Theorems via Lifting* — [V-primaire] sur deux versions : ECCC
   TR20-099 rév. 1 (27 janv. 2021 ; PDF 57 p. téléchargé, pages 1-7
   extraites et citées verbatim) et arXiv:2007.02740 (v. mai 2025 ;
   abstract, §1, bibliographie). Version journal : computational
   complexity 33, art. 4, 2024, doi:10.1007/s00037-024-00250-7 —
   [V-métadonnées]. Venue FOCS 2020, pp. 43-49,
   doi:10.1109/FOCS46700.2020.00013 — [V-métadonnées] (confirmée en
   seconde passe, dblp ; l'audit initial la laissait « non vérifiée »).
8. **Karchmer-Raz-Wigderson**, *Super-logarithmic depth lower bounds via
   the direct sum in communication complexity*, Computational Complexity
   5(3/4):191-204, 1995 — [V-métadonnées] (énoncé de la conjecture KRW
   attesté verbatim DANS la pièce 7 ; texte original non ouvert).
9. **Karchmer-Wigderson**, SIAM J. Discrete Math. 3(2):255-265, 1990,
   doi:10.1137/0403021 — [V-métadonnées] (cahier §7.3 ; les énoncés
   D(f) = CC(KW_f) et mD(f) = CC(mKW_f) attestés verbatim dans la
   pièce 7, p. 4 et 6).
10. **Lovett-Meka-Mertz-Pitassi-Zhang**, *Lifting with Sunflowers*,
    ITCS 2022, LIPIcs 215, 104:1-104:24 (aussi ECCC TR20-111) —
    [V-primaire] (notice DROPS ouverte, abstract + §1 verbatim).
11. **Beame-Koroth**, *On Disperser/Lifting Properties of the Index and
    Inner-Product Functions*, ITCS 2023, LIPIcs 251, art. 14 —
    [V-primaire] (PDF DROPS ouvert, abstract verbatim ; **corps des
    preuves non lu**).
12. **Razborov-Rudich**, *Natural Proofs*, JCSS 55(1):24-35, 1997 —
    [V-primaire] (PDF intégral ouvert ; p. 24 et p. 26 extraites par
    script). Complète l'audit interne
    [razborov_rudich_1997.md](razborov_rudich_1997.md) (A-007), qui ne
    citait pas ces deux passages.
13. **Koucký-Loff-Molli-Saks**, *The Natural Proofs Barrier against
    Data-Structure Lower-Bounds*, STOC 2026,
    doi:10.1145/3798129.3800843 — [V-primaire] (version auteur du
    27/12/2025, 74 p., §5.5 lu en entier ; version ACM non ouverte,
    [V-métadonnées] ; orthographe « Tulasimohan Molli » revérifiée sur
    dblp en seconde passe).
14. **Aaronson-Wigderson**, *Algebrization* — [V-primaire] (version
    auteur ouverte, scottaaronson.com/papers/alg.pdf : abstract +
    intitulé §4.9 verbatim). Complète
    [aaronson_wigderson_2008.md](aaronson_wigderson_2008.md) (A-002).
15. **Tardos 1988** — pièce interne [tardos_1988.md](tardos_1988.md)
    (A-003, texte intégral lu le 2026-06-09).
16. **Håstad**, *The shrinkage exponent of De Morgan formulas is 2*,
    SIAM J. Comput. 27(1):48-64, 1998 — [V-métadonnées] (l'état de
    l'art (3−o(1))·log n est cité verbatim depuis la pièce 7, pas
    depuis Håstad).

### Veille 2024-2026 (recherche du 2026-08-02)

17. Page mot-clé ECCC « Lifting », eccc.weizmann.ac.il/keyword/18056/ —
    [V-primaire] (liste intégrale relevée : 17 rapports, dont 9 sur
    2024-2026).
18. **Alekseev-Filmus-Smal**, *Lifting dichotomies*, ECCC TR24-037
    (26 févr. 2024) — [V-primaire] (abstract intégral).
19. **Iyer**, *Lifting for Arbitrary Gadgets*, ECCC TR25-036
    (29 mars 2025) — [V-primaire] (abstract intégral). Lieu de
    publication : non trouvé.
20. **Manor-Meir**, *Lifting with Inner Functions of Polynomial
    Discrepancy*, arXiv:2404.07606 (11 avr. 2024) — [V-primaire]
    (abstract intégral). Lieu de publication : non trouvé.
21. **Podolskii-Shekhovtsov**, *Randomized Lifting to Semi-Structured
    Communication Complexity via Linear Diversity*, ECCC TR24-199
    (déc. 2024) — [V-primaire] ; ITCS 2025,
    doi:10.4230/LIPIcs.ITCS.2025.78 — [V-métadonnées].
22. **Mao-Yang-Zhang**, *Gadgetless Lifting Beats Round Elimination:
    Improved Lower Bounds for Pointer Chasing*, ECCC TR24-070
    (10 avr. 2024) + ITCS 2025, LIPIcs 325, 75:1-75:14,
    doi:10.4230/LIPIcs.ITCS.2025.75 — [V-primaire] (les deux notices).
23. **Yang-Zhang**, *Deterministic Lifting Theorems for One-Way
    Number-on-Forehead Communication*, ECCC TR25-073 — [V-primaire]
    (abstract intégral de la VERSION ORIGINALE du 14 juin 2025,
    toujours affiché sur la page ECCC ; la révision 3 du 5 juillet 2026
    reformule l'abstract, et la seule primauté qu'elle revendique porte
    sur la séparation obtenue, pas sur l'existence d'un lifting NOF).
    Lieu de publication : non trouvé.
24. **Alekseev-Itsykson**, *Lifting to Bounded-Depth and Regular
    Resolutions over Parities via Games*, ECCC TR24-128 (27 août 2024,
    rév. 2 du 29 juin 2025) — [V-primaire]. Version STOC 2025,
    pp. 584-595, doi:10.1145/3717823.3718150 — [V-métadonnées]
    (confirmée en seconde passe, dblp ; initialement connue seulement
    via la citation « [AI, STOC'25] » de la pièce 27).
25. **Chattopadhyay-Dvořák**, *Super-critical Trade-offs in Resolution
    over Parities Via Lifting*, ECCC TR24-132 (6 sept. 2024) —
    [V-primaire] (première phrase de l'abstract verbatim ; le reste en
    paraphrase d'outil de lecture).
26. **Efremenko-Itsykson**, *Strong ETH Holds for Bounded-Depth
    Resolution over Parities*, ECCC TR25-188 (20 nov. 2025) —
    [V-primaire] (extraits verbatim).
27. **Itsykson-Podolskii-Shekhovtsov**, *Resolution Width Lifts to
    Near-Quadratic-Depth Res(⊕) Size*, ECCC TR26-018 (12 févr. 2026) —
    [V-primaire] (abstract intégral).
28. **de Rezende-Vinyals**, *Lifting with Colourful Sunflowers*,
    CCC 2025, LIPIcs 339, 36:1-36:19, doi:10.4230/LIPIcs.CCC.2025.36 —
    [V-primaire] (notice Dagstuhl ouverte, abstract intégral, y compris
    le comparatif « approximation method » — verbatim au §7.4).
29. **de Rezende-Fleming-Janett-Nordström-Pang**, *Truly Supercritical
    Trade-offs for Resolution, Cutting Planes, Monotone Circuits, and
    Weisfeiler-Leman*, arXiv:2411.14267 (21 nov. 2024) — [V-primaire]
    (abstract intégral) ; STOC 2025, doi:10.1145/3717823.3718271 —
    [V-métadonnées].
30. **Göös-Newman-Riazanov-Sokolov**, *Hardness Condensation by
    Restriction*, ECCC TR23-181 (21 nov. 2023) — [V-primaire] ;
    STOC 2024, pp. 2016-2027, doi:10.1145/3618260.3649711 —
    [V-métadonnées].
31. **Kayal-Mittal-Nalli-Paraashar-Polisetty-Sarma-Saurabh**, *Bounds
    for Hardness Condensation in the Query Model*, arXiv:2602.00754
    (v2 du 21 mai 2026 ; acceptation CCC 2026 annoncée dans le texte,
    actes non parus) — [V-primaire]. (Attention : dblp n'indexe encore
    que la v1 — autre titre, quatre auteurs — retard d'indexation
    constaté en seconde passe, pas une erreur de la présente fiche.)
32. Périphérie, métadonnées seules (via la pièce 17, contenu non lu) :
    ECCC TR25-039 (Efremenko-Itsykson, *Amortized Closure…*) ;
    TR25-193 (Göös et al., *Pseudodeterministic Communication
    Complexity*) ; TR26-125 (Hu-van Melkebeek, *Lifting Polynomial
    Complexity Measures Using Error-Correcting Codes* — lifting
    ALGÉBRIQUE, hors communication ; page ouverte mais abstract
    restitué en paraphrase, à traiter en [V-métadonnées]).

## 1. Ce qu'EST un théorème de lifting (définitions verbatim, lignée)

Deux formulations, documents ouverts :

> « *Lifting theorems are theorems that relate the query complexity of a
> function f:{0,1}^n→{0,1} to the communication complexity of the
> composed function f∘g^n, for some "gadget"
> g:{0,1}^b×{0,1}^b→{0,1}. Such theorems allow transferring lower
> bounds from query complexity to the communication complexity* »
> (pièce 4, abstract)

> « *A lifted search problem S⋄gd is obtained by composing a search
> problem S with an appropriate "gadget" function gd. A lifting theorem
> is a theorem that translates a lower bound for S in a weak model of
> computation to a lower bound for S⋄gd in a strong model.* » Puis :
> « *Fix a gadget gd : {0,1}^t×{0,1}^t→{0,1} of input length t. A few
> lifting theorems [RM99, CKLM19, WYY17, CFK+19] establish that if the
> gadget gd satisfies certain conditions, then CC(S⋄gd) = Ω(Q(S)·t).* »
> (pièce 7, TR20-099, p. 6-7)

**Lignée.** La référence fondatrice est Raz-McKenzie (pièce 1),
abstract verbatim : « *Our argument is more general: we define a new
class of communication complexity search problems, referred to below as
DART games, and we prove a tight lower bound for the communication
complexity of every member of this class.* » La forme moderne « pour
tout f » est due à GPW, qui attribuent et généralisent (pièce 2, p. 2) :

> « *We use tools that were introduced already in 1997 by Raz and
> McKenzie [RM99] (building on [EIRS01]). They proved a simulation
> theorem that converts a deterministic protocol for F := f∘g^n (where
> f is arbitrary but the gadget g is chosen carefully) into a
> deterministic decision tree for f. Unfortunately, their result was
> originally formulated only in case f was a certain "structured"
> search problem (canonical search problem associated with a DNF
> tautology) [...] we observe that, with minor modifications, their
> proof actually works without any assumptions on f.* »

## 2. Les théorèmes principaux, avec leur régime exact

1. **Lifting déterministe — PROUVÉ** (pièce 2, Théorème 3 verbatim,
   p. 2) : « *Theorem 3 (Simulation Theorem). There is a gadget
   g : X×Y→{0,1} where the size of Alice's input is log|X| = Θ(log n)
   bits such that for all f : {0,1}^n→{0,1} we have
   P^cc(f∘g^n) = P^dt(f)·Θ(log n).* » Gadget verbatim : « *The gadget
   in the above can be taken to be the usual indexing function
   g : [m]×{0,1}^m→{0,1} where m := poly(n) and g(x,y) := y_x.* »
   Le paramètre qui compte : coût Θ(log n) bits par gadget ; l'exposant
   exact du poly(n) est fixé plus loin dans le papier, **non lu**
   ([NON TROUVÉ], §9.1).
2. **Lifting BPP (randomisé) — PROUVÉ** (pièce 3, abstract verbatim) :
   « *For any n-bit boolean function f, we show that the randomized
   communication complexity of the composed function f∘g^n, where g is
   an index gadget, is characterized by the randomized decision tree
   complexity of f.* »
3. **Gadgets à petite discrépance, taille logarithmique — PROUVÉ**
   (pièce 4, abstract verbatim) : « *We prove a new lifting theorem
   that works for all gadgets g that have logarithmic length and
   exponentially-small discrepancy, for both deterministic and
   randomized communication complexity. [...] our work is the first to
   prove a randomized lifting theorem for logarithmic-size gadgets.* »
   (IP inclus — titre ICALP 2019 : « …for BPP Using Inner Product ».)
4. **Frontière de la taille de gadget — OUVERT** (pièce 10, verbatim) :
   « *proving lifting theorems with improved gadget size - one of the
   main challenges in the area. Focusing on one of the most widely used
   gadgets - the index gadget - existing lifting techniques are known
   to require at least a quadratic gadget size. Our new approach [...]
   allows us to reduce the gadget size to near linear. We conjecture
   that it can be further improved to polylogarithmic.* » §1 :
   « *It has remained an open problem to break through this quadratic
   barrier. [...] our simplified proof immediately gives us a gadget of
   size n^{1+ε}* ». Développement 2025 : Iyer (pièce 19), lifting
   sensibilité → communication pour gadget ARBITRAIRE — « *We prove a
   sensitivity-to-communication lifting theorem for arbitrary
   gadgets* », D(f∘g) ≥ s·(Ω(D(g))/log rk(g) − log rk(g)) — bornes plus
   faibles, mais sans condition sur le gadget.
5. **Dichotomie interne — PROUVÉ** (pièce 18, verbatim) : dans quatre
   cadres classifiés complètement, « *there is no intermediate cases —
   for every gadget there is either a polynomial lifting or no lifting
   at all* ». Sous-produit : log-rank prouvée pour les fonctions de la
   forme f∘OR∘XOR.

## 3. Les applications qui ont fait la réputation de la famille

1. **Profondeur monotone via jeux KW — séparation de la hiérarchie
   monotone** (pièce 1, abstract verbatim) : « *We prove tight lower
   bounds, of up to n^ε, for the monotone depth of functions in
   monotone-P. As a result we achieve the separation of the following
   classes. 1. monotone-NC ≠ monotone-P. 2. For all i≥1,
   monotone-NC^i ≠ monotone-NC^{i+1}.* [...] *For st-connectivity, we
   get a tight lower bound of Ω(log²n).* [...] *For the k-clique
   function, with k≤n^ε, we get a tight lower bound of Ω(k log n).* »
   Le pont KW lui-même (pièce 9) est attesté verbatim dans la pièce 7 :
   « *Karchmer and Wigderson [KW90] observed that D(f) = CC(KW_f)* »
   (p. 4) et « *mD(f) = CC(mKW_f)* » (p. 6).
2. **Cutting Planes et circuits monotones depuis Résolution** (pièce 5,
   abstract verbatim) : « *For any unsatisfiable CNF formula F that is
   hard to refute in the Resolution proof system, we show that a
   gadget-composed version of F is hard to refute in any proof system
   whose lines are computed by efficient communication protocols—or,
   equivalently, that a monotone function associated with F has large
   monotone circuit complexity. Our result extends to monotone real
   circuits, which yields new lower bounds for the Cutting Planes proof
   system.* » Le §1 du TR ajoute le câble exact vers la ligne 15 :
   « *The result can be interpreted as a converse to monotone feasible
   interpolation [BPR97, Kra97]* [...] *A theorem of this type was
   conjectured by Beame, Pitassi, and Huynh [BHP10, §6]* ».
3. **Extension complexity** (pièce 6, abstract verbatim) : « *We
   exhibit an n-node graph whose independent set polytope requires
   extended formulations of size exponential in Ω(n/log n). Previously,
   no explicit examples of n-dimensional 0/1-polytopes were known with
   extension complexity larger than exponential in Θ(√n).* »
4. **Lien avec les lignes 5 et 15 de la matrice.** Ligne 5 : les
   produits ci-dessus (hiérarchie mNC, clique, st-connectivité,
   circuits monotones réels) sont exactement des bornes MONOTONES —
   donc toutes sous la barrière Tardos documentée en
   [tardos_1988.md](tardos_1988.md) §6 ; le lifting est le MOTEUR
   moderne de cette ligne, pas une sortie de sa barrière. Ligne 15 :
   la colonne monotone de la ligne 15 (interpolation faisable =
   Résolution, Cutting Planes — [proof_complexity.md](proof_complexity.md)
   §5) est alimentée par GGKS via composition par gadget ; TR20-099
   §2.7.2 recense aussi un « Lifting from Nullstellensatz degree »
   (table des matières lue ; **contenu de section non lu**).

## 4. Ce que la famille N'A PAS produit — bornes non monotones

1. **État de l'art non monotone, verbatim** (pièce 7, p. 4 — texte de
   2020/2021, à dater comme tel) : « *A major frontier [...] is proving
   super-logarithmic lower bounds on the depth complexity of an
   explicit function, i.e., proving that P ⊄ NC¹. [...] The state of
   the art is the work of Håstad [Hås98], which proved a lower bound of
   (3−o(1))·log n [...] This lower bound has not been improved for more
   than two decades except for the lower order terms [Tal14].* »
   Contraste : côté monotone, le même moteur donne n^ε (pièce 1).
2. **Pourquoi le pont KW général n'a pas été franchi — ce que le texte
   dit lui-même** (pièce 7, p. 4-7) : (i) la voie déclarée vers
   P ⊄ NC¹ est la conjecture KRW (pièce 8), « *D(f⋄g) ≈ D(f) + D(g)* » ;
   (ii) « *The state of the art is that the KRW conjecture is known to
   hold for every outer function f, but only when combined with two
   specific choices of the inner function g: the parity function, and
   the universal relation. There are no results proving the KRW
   conjecture for a broader family of inner functions.* » ; (iii) la
   pénurie est structurelle : « *the relations U_n, KW_⊕, and MUX are
   more or less the only relations that are well-understood. Thus, we
   have a shortage of good candidates g for this program. As a way out
   of this shortage, we propose to consider monotone depth
   complexity* » ; (iv) le résultat lifting du papier est confiné :
   « *though we are now working in the monotone rather than the
   non-monotone setting* », et la composition « semi-monotone » vaut
   « *only for a specific choice of the outer function f* » (abstract) ;
   (v) l'aveu de hiérarchie des difficultés : « *if we cannot prove the
   KRW conjecture in the monotone setting, what hope do we have to
   prove it in the non-monotone setting, which is far less
   understood?* »
3. **Mécanisme structurel** : la sortie de la chaîne
   requête → communication chez GGKS est « *a monotone function
   associated with F* » — l'objet-circuit produit est monotone PAR
   CONSTRUCTION. Aucun texte ouvert ici ne revendique de borne de
   circuits généraux issue d'un lifting ; ce que la famille produit de
   non monotone reste du niveau communication/preuves (partition
   number, Clique vs Independent Set, log-rank — pièce 2 ; Res(⊕),
   NOF — §7). **Attention au statut** : ce constat est un état de
   l'art, PAS une déclaration d'impossibilité — aucune phrase « le
   lifting ne produit pas de bornes non monotones » n'existe dans les
   textes ouverts ([NON TROUVÉ], §9.5).

## 5. Profil de barrières (pour la ligne 17)

- **Relativisation : ◌ sans objet structurel, avec pièce.** Aucun texte
  de lifting ouvert ne discute la relativisation de ses propres bornes
  (grep négatif sur 6 PDF — [NON TROUVÉ]). La pièce la plus proche est
  PRIMAIRE : RR 1997, p. 24, à propos du corpus combinatoire des années
  80 dont la liste de références inclut Karchmer-Wigderson [17] :
  « *These techniques are highly combinatorial, and in principle they
  are not subject to relativization.* » Analyse structurelle du dépôt
  (pas une pièce) : les sorties du lifting sont des bornes non
  uniformes sur modèles concrets (profondeur de formule, circuits
  monotones, taille de preuve) ; BGS parle de machines à oracle — la
  question croix/coche ne se pose pas littéralement. Renversement
  documenté : chez AW 2008 (pièce 14), la communication est l'AMONT de
  l'appareil de barrières, pas sa victime — §4.9, « *Communication
  lower bounds imply algebraic query lower bounds* » ; même position
  amont que Missing-String pour la ligne 16 (remarque du dépôt). Le
  [Tour 11 §1](../tours/tour_11_lifting_rejete.md) avait accepté sans
  pièce la revendication du Proposeur « lifting theorems sont
  effectivement non-relativisants et non-algébrisants » — la ligne 17
  n'hérite pas de cette phrase non sourcée.
- **Preuves naturelles : ✓ évitée, deux mécanismes textuellement
  attestés.** (1) Versant monotone — RR 1997 eux-mêmes, p. 26 :
  « *Another exception to our scheme is the list of strong lower bounds
  proofs against monotone circuit models [...]. Here the issue is not
  constructivity—the properties used in these proofs are all
  feasible—but that there appears to be no good formal analogue of the
  largeness condition. In particular, no one has formulated a workable
  definition of a "random monotone function."* » L'essentiel de ce que
  le lifting prouve (circuits monotones, real monotones) vit dans cette
  exception. (Divergence de codage assumée, signalée dans la cellule :
  la ligne 5 code ce même fait ◌ — « RR vise le non-monotone » — du
  point de vue de l'approche monotone ; la ligne 17 le code ✓ du point
  de vue de la famille lifting. Même pièce, deux perspectives, pas une
  contradiction.) (2) Versant général — KLMS (pièce 13), §5.5, « *The
  single exception we know: Lifting theorems* » : « *Lifting theorems
  fail to be natural because they only address functions of the form
  f = h∘g, and most functions are not of composed form, so the
  largeness property fails.* » Avec leur nuance, à ne pas escamoter :
  « *in this limited sense the used property is large (among composed
  functions) and constructive, and one might informally say that the
  proof has the flavor of a "natural" proof. [...] Nonetheless, lifting
  theorems are not natural proofs in the strict sense we have defined
  here [...] This is also the main hope of the KRW conjecture* ». Leurs
  obstacles propres sont internes aux structures de données, pas
  transférables tels quels.
- **Algébrisation : — non analysé.** [NON TROUVÉ] : aucune discussion
  d'AW appliquée au lifting dans les textes ouverts (grep « algebriz »
  négatif sur les 6 PDF hors AW lui-même). Seule note légitime, avec
  pièce : le renversement ci-dessus — chez AW la communication FABRIQUE
  les oracles algébriques (§4.9), la famille est instrument de la
  barrière, non analysée comme cible.
- **Monotone : ⚠ exposée par destination.** La barrière ne tue pas la
  famille — Res(⊕), NOF, extension complexity, structures de données
  sont non monotones — mais plafonne son débouché principal : tout le
  versant monotone (pièces 1, 5, 28) est borné par Tardos 1988 (gap
  monotone/général exponentiel, témoin θ̄-perturbée ∈ P,
  [tardos_1988.md](tardos_1988.md)) ; aucune borne monotone liftée ne
  transfère au général. Renvoi explicite : ligne 5.

## 6. Le verrou réel — trois éléments

1. **Gadgets de taille constante — OUVERT.** Pourquoi il compte,
   verbatim (pièce 10, §1) : « *An ideal lifting theorem - one with
   constant gadget size - would give a unified way to prove tight lower
   bounds in several models of computation. [...] Improving the gadget
   size from poly(n) to O(1) (or even poly log(n)) would improve the
   best known lower bounds for extended formulations and monotone
   circuit size to 2^Ω̃(n).* » (Sorties encore monotones, donc sous
   Tardos.) L'énoncé du verrou, verbatim (pièce 11, abstract) : « *A
   number of important complexity questions could be resolved if we
   could make substantial improvements in the input size required for
   lifting with the Index function, which is a universal gadget for
   lifting, from its current near-linear size down to polylogarithmic
   in the number of inputs N of the original function or, ideally,
   constant.* » ET la barrière interne DÉMONTRÉE dans la famille, même
   abstract : « *The conjecture of Lovett et al. is false when the size
   of the Index gadget is less than logarithmic in N. The same
   limitation applies to the Inner-Product function.* » — sous le seuil
   logarithmique, la propriété disperseur au cœur de la conjecture de
   LMMPZ est réfutée, pour Index et Inner-Product ; le verbatim ne
   porte que sur ces deux gadgets et cette propriété — rien n'y est
   affirmé sur « toutes les techniques actuelles » (formulation
   antérieure de cette fiche, retirée en seconde passe).
2. **Le pont KW général (KRW) — OUVERT, et son plafond.** Pièce 7,
   abstract : « *One of the major open problems in complexity theory is
   proving super-logarithmic lower bounds on the depth of circuits
   (i.e., P ⊄ NC1). Karchmer, Raz, and Wigderson [KRW95] suggested to
   approach this problem by proving that depth complexity behaves "as
   expected" with respect to the composition of functions f ⋄ g. They
   showed that the validity of this conjecture would imply that
   P ⊄ NC1.* » État général gelé : (3−o(1))·log n (§4.1 ci-dessus).
   **Test de plafond de la ligne — analyse structurelle du dépôt, à
   étiqueter comme telle** : même la résolution COMPLÈTE de la
   conjecture KRW donne P ⊄ NC¹, pas P ≠ NP — le pont KW général vise
   la profondeur de formule, deux étages sous la séparation de la
   matrice.
3. **Le plafond Tardos du versant monotone** (§5, colonne monotone ;
   ligne 5 de la matrice).

## 7. État 2024-2026 (veille du 2026-08-02)

Point d'entrée systématique : la page mot-clé « Lifting » de l'ECCC
(pièce 17) — 17 rapports, dont 9 sur 2024-2026. La famille est dense et
en expansion.

1. **Front « gadget constant »** : toujours ouvert en deux-partis
   général — « *the major open problem in this area is to prove a
   lifting theorem for gadgets of constant size* » (pièce 21) — mais
   contourné sur trois voies : gadget arbitraire au prix d'une mesure
   plus faible (pièce 19) ; communication semi-structurée, résultats
   serrés pour Ind_m, IP_m, MAJ_m « *for all m* » (pièce 21) ; tout
   gadget de discrépance inverse-polynomiale (pièce 20). Et ACQUIS en
   Res(⊕) : gadget de taille 3 — « *any 1-stifling gadget g (for
   example, g=MAJ_3)* » (pièce 27).
2. **Nouveaux modèles** : un NOUVEAU lifting deux-partis → NOF one-way
   — « *a deterministic lifting theorem that translates one-way
   two-party communication lower bounds into one-way NOF lower
   bounds* » —, avec une fonction explicite à Ω(n/2^k) en NOF
   randomisé, améliorant Babai-Nisan-Szegedy 1989 (pièce 23 ;
   citations de l'abstract original du 14 juin 2025, la rév. 3 du
   5 juillet 2026 reformule ; le texte dit « *new lifting theorem* »,
   il ne revendique PAS « first », et aucune primauté n'est affirmée
   ici) ; « gadgetless lifting », applicable à des fonctions non
   composées — Ω(n/k + k) pour le pointer chasing, contre le majorant
   Õ(n/k + k) de Nisan-Wigderson (pièce 22). La définition même de la
   famille bouge.
3. **Cluster Res(⊕) du mot-clé ECCC, entièrement propulsé par lifting
   (nourrit la ligne 15)** : le dag-like général reste OUVERT —
   « *Proving superpolynomial lower bounds on proof size in the proof
   system resolution over parities (Res(⊕)) remains a significant open
   challenge* » (pièce 24) — avec quatre jalons vérifiés : Tseitin
   lifté par MAJ₅ → borne exponentielle top-regular Res(⊕) (pièce 24) ;
   trade-offs supercritiques tree-like via extension d'un lifting
   (pièce 25) ; bornes type SETH pour depth-n Res(⊕), « *a lossless
   lifting achieved by assigning distinct, randomly chosen gadgets to
   each variable* » (pièce 26) ; largeur de résolution → profondeur
   quasi-quadratique Res(⊕), gadget MAJ₃ (pièce 27).
4. **Monotone et Cutting Planes (nourrit les lignes 5 et 15)** : le
   lifting DAG-like par tournesols colorés donne des bornes monotones
   MEILLEURES que la méthode d'approximation — comparatif verbatim de
   l'abstract, revérifié en seconde passe sur la notice DROPS :
   « *yields lower bounds on the monotone circuit complexity and proof
   complexity of natural functions and formulas that are better than
   previously known results obtained using the approximation method* »,
   avec les chiffres : « *an n^Ω(k) lower bound for the clique function
   up to k ≤ n^{1/2-ε}, and an exp(Ω(n^{1/3-ε})) lower bound for a
   function in P* » (pièce 28) ; les premiers trade-offs « *truly
   supercritical* » pour Résolution et Cutting Planes, plus circuits
   monotones et Weisfeiler-Leman, avec la cheville : « *Our other
   results follow from improved lifting theorems* » (pièce 29). Une
   seule machinerie alimente simultanément les lignes 5 et 15 —
   l'argument le plus net pour créer la ligne 17.
5. **Résultats négatifs internes** : dichotomie complète des gadgets
   dans les quatre cadres classifiés (pièce 18, §2.5) ; condensation de
   dureté — « *Query complexity cannot be condensed in general* »
   (pièce 30), block sensitivity et certificate complexity « *cannot be
   condensed losslessly* » (pièce 31). La famille possède ses propres
   limites internes — exactement le format « barrière interne » des
   autres lignes.

## 8. Contexte interne du dépôt (vérifié sur pièces)

- **Tour 11** ([tour_11_lifting_rejete.md](../tours/tour_11_lifting_rejete.md),
  2026-05-23) : la chaîne lifting+KW du Proposeur a été REJETÉE pour
  erreur factuelle (2COL ∈ P) et chaîne conjecturale ; le cadre y est
  qualifié de « légitime » (§7), mais le §1 accepte sans pièce
  « lifting theorems sont effectivement non-relativisants et
  non-algébrisants » — phrase que le présent audit remplace par les
  pièces du §5. La famille n'avait jamais eu de ligne dans la matrice.
- **Cahier §7.3** porte déjà les deux références pivots avec DOI :
  KW 1990 (doi:10.1137/0403021) et GPW SICOMP 47(6):2435-2450, 2018
  (doi:10.1137/16M1059369).
- **Incohérence interne à signaler — échange Göös, localisée dans le
  cahier lui-même** (localisation corrigée en seconde passe et
  revérifiée sur fichier). La ligne « Attentes externes » du cahier
  (§6, l. 949) et l'énoncé de la tâche A-014 disent « écrit à M. Göös
  le 2026-06-09, sans réponse consignée » ; or le MÊME cahier consigne
  une réponse quelques sections plus bas (§ « Échange externe — Mika
  Göös (2026-06-12) », l. 1352-1359) : « *Sorry, I don't know any
  reference off the top of my head. These days you could also ask
  ChatGPT :)* ». La contradiction est donc interne au cahier
  (l. 949 contre l. 1352) ; le backlog (ligne EXT, l. 253) dit
  seulement « en attente » — périmé lui aussi, mais non contradictoire.
  Cet échange concernait le folklore-check DNF-MIN/IP (lignes 6/11),
  PAS le lifting : il ne peut servir de pièce à la ligne 17, et la
  double mise à jour (cahier l. 949, backlog l. 253) est à la main de
  l'utilisateur.
- **Liens croisés** : ligne 5 (le lifting est son moteur moderne, sous
  plafond Tardos — §3.4, §5) ; ligne 15 (réciproque de l'interpolation
  faisable, cluster Res(⊕), Cutting Planes — §3.2, §7.3-7.4) ;
  ligne 16 (position amont vis-à-vis des barrières, analogue de
  Missing-String — §5, remarque du dépôt).

## 9. Ce qui reste [NON TROUVÉ]

1. L'exposant exact du m = poly(n) du gadget d'indexation dans GPW
   (pièce 2) : les pages lues (1-3) disent seulement « m := poly(n) » ;
   seule quantification lue ailleurs : « au moins quadratique »
   (pièce 10).
2. Le texte intégral de Raz-McKenzie : scan image, 0 texte extractible ;
   les « DART games » et la structure de leur théorème de simulation
   n'ont pas été lus au-delà de l'abstract ; version Combinatorica non
   ouverte.
3. La pagination de la version SICOMP 49(4), 2020, du lifting BPP.
4. Non ouverts, à ne pas citer sans audit : Fiorini-Massar-Pokutta-
   Tiwary-de Wolf (extension complexity du TSP — voie PRÉ-lifting) ;
   Kothari-Meka-Raghavendra (LP/Sherali-Adams) ; Lee-Raghavendra-
   Steurer (SDP) ; Pudlák 1997 (interpolation CP) ; WYY17 (cité dans
   TR20-099, métadonnées non résolues) ; Håstad 1998 et Tal 2014 (cités
   verbatim via TR20-099 seulement) ; KRW 1995 (contenu) ; section
   2.7.2 « Lifting from Nullstellensatz degree » de TR20-099 ; corps
   des preuves de Beame-Koroth.
5. Une phrase des textes eux-mêmes déclarant « le lifting ne produit
   pas de bornes non monotones » : le constat du §4 repose sur les
   verbatims de TR20-099 et la structure des énoncés, pas sur une
   déclaration d'impossibilité — qui n'existe dans aucun texte ouvert.
6. Relativisation des bornes liftées : aucun énoncé dans les textes de
   lifting ouverts ; algébrisation du lifting : rien non plus — d'où ◌
   (avec pièce indirecte RR p. 24) et tiret au §5.
7. Un survey dédié signé Göös : non localisé ; sa thèse (Toronto 2016)
   non ouverte. Le rôle panoramique est tenu ici par LMMPZ §1 et
   KLMS §5.5.
8. Un analogue « preuves naturelles » propre à la complexité de
   communication elle-même : rien de canonique au-delà de KLMS (qui
   porte sur les structures de données) — ne rien affirmer là-dessus.
9. Veille : application neuve 2024-2026 à l'extension complexity —
   rien remonté (absence non démontrée) ; idem data structures ;
   progrès de fond 2024-2026 sur KRW — seules des versions journal de
   travaux antérieurs ; lieux de publication de TR25-036, TR25-073 et
   arXiv:2404.07606 ; abstracts verbatim complets de TR24-132 et
   TR26-125 ; [IK, ITCS'26], [BC, ECCC'25], [BI, arXiv'25] connus
   uniquement par la citation de TR26-018 — à ne pas porter en cellule
   sans ouverture. (Levés en seconde passe, dblp : la venue FOCS 2020
   de dRMNPR — pièce 7 — et la version STOC 2025 de TR24-128 —
   pièce 24.)
10. Réserve de fraîcheur : arXiv:2602.00754 est annoncé CCC 2026 par
    son propre texte, actes non parus ; TR26-125 avait neuf jours au
    moment de la veille ; KLMS (pièce 13) est lu sur version auteur,
    la version ACM STOC 2026 n'est pas ouverte.
