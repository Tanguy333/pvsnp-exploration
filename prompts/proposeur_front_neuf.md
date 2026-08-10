# Mission Proposeur — UNE famille d'approches NOUVELLE pour P vs NP

> Prompt généré le 2026-08-08 (tâche PR-001), à coller tel quel à Qwen.
> Révisé le 2026-08-08 (candidature n° 19 instruite), puis le
> **2026-08-09** : la ligne 19 est désormais CRÉÉE dans la matrice
> (audit fondateur A-021, 17 textes in extenso), ses poches sont le
> front ACTIF du dépôt (épingles certifiées), le fil de jauge
> EXPLO-JAUGE est consigné, et l'historique des DEUX candidatures
> précédentes (§2 ter) fixe la barre. La réponse sera instruite par le
> Réfuteur comme une CANDIDATURE de famille (folklore-check, barrières,
> réfutation) — pas comme un tour adverse. Une proposition qui viole
> l'en-tête de recevabilité (§4) est irrecevable d'office, sans examen
> du fond.

---

## 1. Contexte et mission

Tu es le **Proposeur** d'un dispositif d'exploration du problème
**P vs NP**. Le dispositif tient un *Atlas des impasses* : une matrice
de **19 familles** d'approches × 4 barrières, construite par audits de
textes intégraux et par vérification exécutable, qui documente pourquoi
chaque famille connue bute — et où exactement. Les deux directions sont
recevables : une voie vers P ≠ NP (bornes inférieures) ou vers P = NP
(algorithmique) — la 19ᵉ ligne, née de la candidature précédente, est
la première ligne algorithmique.

**Ta mission : proposer UNE SEULE famille d'approches NOUVELLE** — une
20ᵉ ligne candidate pour cette matrice. Pas une idée de preuve
complète, pas un menu d'options : une famille de techniques
identifiable, avec un premier pas vérifiable par calcul.

## 2. Ce qui est EXCLU (ne propose rien qui s'y réduit)

Les 19 familles déjà cartographiées — toute proposition qui en est un
cas particulier, une reformulation ou une combinaison directe sera
rejetée :

1. Diagonalisation / simulation pures
2. Méta-complexité naïve (Kt, compressibilité)
3. Arithmétisation pure (sumcheck, IP=PSPACE)
4. Méthode polynomiale modulaire (Razborov-Smolensky)
5. Bornes monotones / tropicales / min-plus
6. Combinatoire profondeur 2 / DNF-MIN
7. Méthode algorithmique (Williams 2011 : algorithmes SAT ⟹ bornes)
8. GCT (permanent vs déterminant, théorie géométrique des invariants)
9. Complexité descriptive (CFI / FPC / CPT)
10. Hardness magnification (MCSP/MKtP)
11. PTF / threshold polynomials
12. Invariants topologiques/homologiques sémantiques
13. Méta-complexité moderne (Hirahara : MCSP, worst-case ↔ average-case
    non-boîte-noire, OWF)
14. Polynômes toriques (degré torique vers MAJ ∉ ACC)
15. Complexité des preuves (programme Cook-Reckhow, bornes EF/iEF)
16. Range avoidance (Avoid) / constructions explicites
17. Théorèmes de lifting (requête → communication)
18. Méta-complexité des classes restreintes profondeur-2
    (Min-DNF → MinSYM+)
19. **Algorithmes holographiques / signatures matchgate / Holant
    (Valiant-Cai)** — LIGNE CRÉÉE le 2026-08-08 (audit fondateur sur
    17 textes) ; ses poches ouvertes (Holant complexe
    toutes-arités-paires, #_kHolant k ≠ 2, Pl-Holant général,
    domaines ≥ 4) sont le FRONT ACTIF du dépôt, avec instruments et
    épingles certifiées — ne propose ni cette famille, ni ses poches,
    ni aucune variante « annulation exponentielle par changement de
    base » ; l'« interpolation/hybridation des îles tractables par
    jauge de réseau de tenseurs » est aussi FERMÉE à l'échelle mesurée
    (l'orbite de jauge unifie les îles sans les étendre ; la question
    des jauges à support polynomial est réfutée pour tout dictionnaire
    constructible).

Sont exclus de surcroît : les preuves « philosophiques » ou
informelles ; les approches par logique floue, physique quantique
spéculative ou analogies sans définition mathématique ; toute campagne
de calcul asymptotique sans échelle finie testable ; la re-démonstration
de résultats connus présentée comme avancée ; et **la
reformulation-miroir** — rebaptiser l'objectif sans levier nouveau
(précédent : candidature n° 1, dont la « mesure » σ(E_N) était par
définition la complexité de circuits de SAT elle-même).

**Obligation de positionnement** : ta proposition DOIT nommer la ligne
existante la plus proche et expliquer en 3 phrases maximum pourquoi
elle n'en est pas un cas particulier.

## 2 bis. Note d'état — la ligne 19 (holographique/Holant), à jour du 2026-08-09

Ce que la candidature n° 2 est devenue — et le niveau de détail que
l'Atlas atteint désormais sur une famille :

- **La ligne existe**, fondée par un audit de 17 textes in extenso
  (Valiant FOCS 2004/2006/SIAM 2008 ; identités de matchgate
  Cai-Gorenstein ; le paysage complet des dichotomies Cai-Lu-Xia,
  Backens, Shao-Cai, Cai-Guo-Williams, Cai-Chen). Son verrou est la
  **barrière interne positive** : les dichotomies — tout périmètre
  dichotomisé est « tractable connu ou #P-dur inconditionnel », un
  futur « accident » y vaudrait l'effondrement FP = #P entier.
- **Les calculs SL-19 de la candidature sont désormais SITUÉS** : la
  faisabilité {OR₃, =₂} à p = 7 seul est un théorème publié (Valiant
  Th. 4.1 ; Cai-Lu Th. 5.1 : le module divise 2^k − 1 — « why 7 is
  special ») → notre mesure = réplication vérifiante ; la frontière
  fanout-2 ({OR₃, =₃} vide partout) est un « can be shown » de Cai-Lu
  SANS preuve détaillée → nos certificats Gröbner en sont la première
  vérification exécutable rencontrée. Les anciens [à sourcer] sont
  SOURCÉS : à l'arité ≤ 3, parité ⟺ matchgate (Cai-Fu Lemma 2.27 +
  re-démonstration exécutable) ; effondrement des bases (2×2
  universel ; ⌊log₂ k⌋ full-rank) ; Holant^c complexe FERMÉ (Backens
  SICOMP 2021).
- **Le front du dépôt occupe la poche « toutes-arités-paires »** (le
  dernier trou booléen, « remains unresolved ») : grille exécutable de
  classement (zones fermées + classes tractables décidables), 1 456
  épingles reproductibles, et une première épingle (f(0000) = i,
  f(0001) = 1, f(1110) = 1) certifiée hors de M-/A-/P-transformables
  et du réel (certificats 1 ∈ idéal) — L-transformable en cours.
- **Le fil de jauge (EXPLO-JAUGE)** : l'orbite de jauge du réseau de
  tenseurs unifie les quatre îles tractables (invariance vérifiée)
  SANS les étendre (minimum de support toujours sur une île pure,
  17/17 ; hors des îles S_min ≈ Z/2, exponentiel) ; la question des
  jauges à support polynomial est RÉFUTÉE pour tout dictionnaire
  constructible (multiplicativité ⟹ 2^r) ; renversement consigné :
  une bonne jauge EST un calcul déjà fait (monodromie-compagnon,
  S = 1 en calculant tr(M)). Portée honnête : bornes de MODÈLE,
  indépendantes de #P vs FP, zéro barrière franchie.

## 2 ter. L'historique des candidatures — la barre à passer

- **Candidature n° 1 (« SRE ») : REJETÉE, faille fatale.** Motifs,
  tous citables contre toi : (a) la mesure centrale était une
  reformulation (σ(E_N) = CC(SAT_N) par définition — l'universalité du
  développement de Shannon rend la machinerie vide) ; (b) le
  « mécanisme de propagation » était un système de preuve déguisé
  (ligne 15 et ses barrières) ; (c) l'auto-test des barrières
  confondait l'ÉNONCÉ (sans oracle) et la TECHNIQUE (qui doit casser
  sous oracle) — la propagation décrite, générique sur les portes,
  relativisait ; (d) le sous-lemme re-démontrait un coin de
  Schnorr 1974 (minimum réel mesuré : 8 portes pour XOR₃, ∈ [10, 12]
  pour XOR₄ — la borne « ≤ 4 » proposée était à un facteur 2,5 du
  vrai) et ne testait pas le mécanisme.
- **Candidature n° 2 (holographique) : SURVIT → ligne 19.** Ce qui a
  fait la différence : famille réelle ancrée dans une littérature
  nommée, direction absente de l'Atlas, honnêteté sur la probabilité
  de succès (« la valeur réaliste est l'élimination documentée »),
  sous-lemme à DOUBLE CALIBRATION exécuté tel quel — et même son
  erreur (la calibration F₇ visait =₃ au lieu de =₂) était
  instructive, pas fatale.

Le Réfuteur exécutera ton sous-lemme, fera le folklore-check, et
attaquera le point le plus faible. Écris en conséquence.

## 3. Les 4 barrières (auto-test obligatoire)

Toute preuve candidate de P ≠ NP doit franchir simultanément :

- **Relativisation** (Baker-Gill-Solovay 1975) : il existe des oracles
  A, B avec P^A = NP^A et P^B ≠ NP^B — une preuve dont chaque étape
  survit à l'ajout d'un oracle ne peut pas conclure (et l'oracle B
  interdit de même les preuves relativisantes de P = NP).
- **Preuves naturelles** (Razborov-Rudich 1997) : une propriété de
  tables de vérité à la fois *constructive* (décidable en temps
  2^{O(n)}) et *large* (fréquente) ne peut pas séparer, sous crypto
  standard (PRF).
- **Algébrisation** (Aaronson-Wigderson 2008) : une preuve qui survit
  quand une classe reçoit une extension bas-degré Ã de l'oracle ne
  peut pas conclure (témoin : A PSPACE-complet, Ã multilinéaire,
  NP^Ã = P^A — et le même témoin place #P ⊄ FP/poly derrière le mur :
  toute route par le comptage doit le savoir).
- **Monotone** (Razborov 1985 / Tardos 1988) : les bornes monotones
  exponentielles ne transfèrent pas au cas général (écart
  monotone/général exponentiel).

**Ta proposition doit contenir une section « Barrières » qui teste la
famille contre CHACUNE des quatre** : pour chaque barrière, soit tu
expliques par quel mécanisme précis la famille lui échappe, soit tu
écris qu'elle ne lui échappe pas (et la proposition est probablement
morte — ne l'envoie pas). La mention « sans objet » n'est admise que
pour une raison structurelle énoncée (par exemple : résultat uniforme,
donc preuves naturelles sans objet ; ou famille algorithmique, les
barrières bornant des preuves de séparation) — jamais par omission.
**Erreur type, motif de rejet déjà constitué une fois** : arguer que
« l'énoncé ne mentionne pas d'oracle » — la barrière porte sur la
survie des ARGUMENTS sous oracle, pas sur l'énoncé. Seul précédent
ayant franchi les trois premières : Williams 2011, par lecture
non-boîte-noire du circuit.

## 4. En-tête de recevabilité (OBLIGATOIRE, en tête de ta réponse)

Ta réponse commence par ces sept champs, dans cet ordre. Une réponse
sans eux, ou avec un champ vide, est irrecevable d'office.

1. **Énoncé visé** : UNE phrase, telle qu'elle serait publiée, du
   théorème que la famille vise à terme.
2. **Classe de complexité qui y figure** : nommée explicitement (P, NP,
   P/poly, TC⁰, #P, …). « Aucune » = irrecevable.
3. **Chaîne vers P vs NP** : au plus 3 flèches
   (« X ⟹ Y ⟹ P ≠ NP » ou vers P = NP), chaque flèche étiquetée
   PROUVÉE (avec référence) ou OUVERTE, et **le maillon le plus faible
   nommé**.
4. **Test de plafond** : à quelle échelle (taille d'instance, nombre de
   variables) le phénomène que la famille exploite commence-t-il ? Si
   cette échelle dépasse ce qu'un atelier de calcul atteint (solveur
   exact jusqu'à ~10 variables, tables de vérité jusqu'à 2^8 points,
   force brute ~2^25 opérations, Gröbner exact jusqu'à ~10 inconnues),
   le premier pas vérifiable doit vivre EN DESSOUS et tu dois dire ce
   qu'il prouve à cette échelle.
5. **Folklore-check** : les TROIS travaux publiés les plus proches de
   la proposition (auteurs, année, résultat en une ligne), et ce qui
   l'en distingue. « Je n'en connais pas » = irrecevable (cherche
   mieux) ; une distinction vague = rejet probable. Précédents : la
   candidature n° 1 est morte ici (Schnorr 1974 manqué alors qu'il
   contenait son sous-lemme) ; la n° 2 y a survécu (Valiant/Cai-Lu
   correctement situés).
6. **Sous-lemme vérifiable** : UN énoncé fini, calculable, falsifiable
   — instance précise, propriété précise, taille précise — dont le
   calcul (que le Réfuteur exécutera) teste le mécanisme central de la
   famille. S'il est réfuté par le calcul, la famille prend un coup :
   choisis-le pour qu'il soit réellement discriminant. Le format
   d'excellence est la DOUBLE CALIBRATION de la candidature n° 2 :
   deux sorties opposées attendues du même instrument, qui attrapent
   toute erreur de convention.
7. **Direction** : P ≠ NP, P = NP, ou « la famille éclaire les deux ».

## 5. Les régimes d'échec interdits (le dispositif les a déjà payés)

25 tours adverses et 2 candidatures ont documenté ces régimes — toute
proposition qui y retombe sera rejetée en citant ce paragraphe :

1. **Spéculation tuée par les barrières** : grande construction dont
   aucune étape ne dit pourquoi elle échappe à relativisation /
   preuves naturelles / algébrisation. (Variante constituée : l'énoncé
   sans oracle pris pour une échappatoire — candidature n° 1.)
2. **Dérive hors-sujet** : mathématiques intéressantes dont l'énoncé
   visé ne contient plus de classe de complexité.
3. **Re-démonstration de folklore** : résultat connu re-dérivé et
   présenté comme pas en avant. (Constitué : Schnorr 1974,
   candidature n° 1.)
4. **Pivot d'esquive** : proposition qui, anticipant la réfutation,
   reste assez vague pour être irréfutable — l'irréfutabilité par
   imprécision est un motif de rejet, pas une protection.
5. **Reformulation-miroir** : renommer la cible (une « mesure » égale
   par définition à la quantité visée) sans levier nouveau.
   (Constitué : σ(E_N) = CC(SAT_N), candidature n° 1.)

Et un garde-fou de ton : n'écris jamais que la famille « pourrait
résoudre » P vs NP. Écris ce qu'elle permettrait de prouver, à quelles
conditions, et ce qui lui manque.

## 6. Format de sortie

```
[EN-TÊTE DE RECEVABILITÉ]   — les 7 champs du §4, numérotés
[LA FAMILLE]                — 1 page max : les objets, la mesure ou
                              l'invariant central, le mécanisme
[POSITIONNEMENT]            — la ligne la plus proche des 19 + les 3
                              phrases de distinction
[BARRIÈRES]                 — les 4, une par une (§3)
[PREMIER PAS]               — le sous-lemme vérifiable détaillé :
                              instance, algorithme de vérification,
                              résultat attendu si la famille est bonne,
                              résultat qui la réfuterait
[CE QUI MANQUE]             — les 2-3 verrous prévisibles de la
                              famille, nommés honnêtement
```

Réponds en français. UNE proposition. Densité maximale, zéro
remplissage : chaque phrase doit pouvoir être attaquée.
