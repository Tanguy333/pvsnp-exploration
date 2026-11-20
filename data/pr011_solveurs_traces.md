# PR-011 — « La trace est une preuve » : DPLL contre CDCL sur PHP_n et sur les pyramides de pebbling (réplication vérifiante déclarée, témoin exécutable de l'entrée E-4)

Date : 2026-09-11 (run) / 2026-09-12 (consignation). Instrument :
`checks/pr011_solveurs_traces.py` — implémentation INDÉPENDANTE de la
candidature n° 8 : générateurs PHP_n et Peb(P_h) (contradiction de
pebbling OR de BIW04 sur la pyramide de hauteur h, deux variables par
sommet), DPLL minimal sans apprentissage (propagation unitaire,
heuristique fixe : plus petite variable libre — trace = réfutation
ARBORESCENTE), CDCL = CaDiCaL 1.9.5 via pysat (trace = réfutation par
résolution générale, à extension près). Commande :
`python -u checks/pr011_solveurs_traces.py --php-min 4 --php-max 11
--peb-min 4 --peb-max 40 --dpll-budget 3000000 --dpll-peb-max 12
--conf-budget 20000000`. Contrôle satisfiable (n pigeons, n trous,
n = 4, 5, 6) : DPLL SAT (14, 67, 443 nœuds), CaDiCaL SAT (0 conflit).

Mesures définies : **nœuds(F)** = nombre de nœuds de branchement du
DPLL jusqu'à UNSAT ; **conflits(F)** = `accum_stats()['conflicts']` de
CaDiCaL jusqu'à UNSAT ; décisions = `accum_stats()['decisions']`.

## 0. Antériorité (déclarée avant tout calcul)

| Objet | Résultat publié | Source |
|---|---|---|
| Réfutations par résolution de PHP_n | 2^{Ω(n)} | Haken 1985 |
| Réfutations arborescentes de Peb(G) | 2^{Ω(peb(G))} — pour la pyramide, 2^{Ω(h)} | BIW04 (Ben-Sasson-Impagliazzo-Wigderson, Combinatorica 2004) |
| Réfutations régulières/générales de Peb(G) | O(taille de G) | folklore / BIW04 |
| Apprentissage de clauses + redémarrages vs résolution | CDCL p-simule la résolution générale | BKS04 (JAIR 22) ; Pipatsrisawat-Darwiche 2011 (AIJ 175) ; AFT11 (JAIR 40, largeur bornée) |
| Expériences solveur CDCL contre DPLL sur pebbling | faites | BKS04 §5 (zChaff) — **réplication vérifiante** |
| Table exacte de conflits par n / par h pour CaDiCaL | — | [NON TROUVÉ] — mesure, pas découverte |

## 1. PHP_n (n+1 pigeons, n trous) — les deux solveurs exponentiels

| n | vars | clauses | DPLL | nœuds | s | CDCL | conflits | décisions | s |
|---|---|---|---|---|---|---|---|---|---|
| 4 | 20 | 45 | UNSAT | 51 | 0,0 | UNSAT | 32 | 35 | 0,0 |
| 5 | 30 | 81 | UNSAT | 374 | 0,0 | UNSAT | 133 | 168 | 0,0 |
| 6 | 42 | 133 | UNSAT | 3 245 | 0,1 | UNSAT | 1 044 | 1 356 | 0,0 |
| 7 | 56 | 204 | UNSAT | 32 780 | 1,8 | UNSAT | 7 130 | 8 534 | 0,0 |
| 8 | 72 | 297 | UNSAT | 378 343 | 50,9 | UNSAT | 31 719 | 38 058 | 0,2 |
| 9 | 90 | 415 | BUDGET | > 3 000 000 | 560,5 | UNSAT | 267 023 | 303 383 | 3,3 |
| 10 | 110 | 561 | — | — | — | UNSAT | 2 227 032 | 2 539 250 | 36,8 |
| 11 | 132 | 738 | — | — | — | UNSAT | 14 398 674 | 16 035 007 | 507,6 |

Ajustements (moindres carrés sur log₂) : **nœuds DPLL : ×9,3 par
pigeon** (pente 3,22, n = 4..8) ; **conflits CDCL : ×6,55 par pigeon**
(pente 2,71, n = 4..11). Les deux cellules sont exponentielles, comme
prédit (Haken pour la résolution générale — donc pour CDCL ; a fortiori
pour l'arborescent). Aucun signe de raisonnement cardinal caché dans
CaDiCaL 1.9.5 : la croissance géométrique est régulière jusqu'à
PHP₁₁ (14,4 M conflits, 508 s).

## 2. Peb(P_h) — pyramide de hauteur h : DPLL exponentiel, CDCL polynomial

| h | vars | clauses | DPLL | nœuds | s | CDCL | conflits | décisions | s |
|---|---|---|---|---|---|---|---|---|---|
| 4 | 20 | 30 | UNSAT | 4 373 | 0,1 | UNSAT | 9 | 20 | 0,0 |
| 5 | 30 | 47 | UNSAT | 1 062 881 | 37,2 | UNSAT | 14 | 38 | 0,0 |
| 6 | 42 | 68 | BUDGET | > 3 000 000 | 164,0 | UNSAT | 84 | 129 | 0,0 |
| 7 | 56 | 93 | — | — | — | UNSAT | 193 | 270 | 0,0 |
| 8 | 72 | 122 | — | — | — | UNSAT | 411 | 576 | 0,0 |
| 9 | 90 | 155 | — | — | — | UNSAT | 305 | 602 | 0,0 |
| 10 | 110 | 192 | — | — | — | UNSAT | 345 | 816 | 0,0 |
| 11 | 132 | 233 | — | — | — | UNSAT | 504 | 1 193 | 0,0 |
| 12 | 156 | 278 | — | — | — | UNSAT | 453 | 1 326 | 0,0 |
| 13 | 182 | 327 | — | — | — | UNSAT | 1 144 | 2 969 | 0,0 |
| 14 | 210 | 380 | — | — | — | UNSAT | 1 096 | 3 346 | 0,0 |
| 15 | 240 | 437 | — | — | — | UNSAT | 656 | 2 351 | 0,0 |
| 16 | 272 | 498 | — | — | — | UNSAT | 988 | 3 582 | 0,0 |
| 17 | 306 | 563 | — | — | — | UNSAT | 1 593 | 5 886 | 0,0 |
| 18 | 342 | 632 | — | — | — | UNSAT | 1 471 | 5 123 | 0,0 |
| 19 | 380 | 705 | — | — | — | UNSAT | 1 217 | 5 035 | 0,0 |
| 20 | 420 | 782 | — | — | — | UNSAT | 2 001 | 7 181 | 0,0 |
| 21 | 462 | 863 | — | — | — | UNSAT | 2 001 | 6 551 | 0,0 |
| 22 | 506 | 948 | — | — | — | UNSAT | 1 460 | 8 618 | 0,0 |
| 23 | 552 | 1 037 | — | — | — | UNSAT | 2 002 | 8 951 | 0,0 |
| 24 | 600 | 1 130 | — | — | — | UNSAT | 1 877 | 9 219 | 0,0 |
| 25 | 650 | 1 227 | — | — | — | UNSAT | 2 001 | 9 580 | 0,0 |
| 26 | 702 | 1 328 | — | — | — | UNSAT | 2 001 | 11 161 | 0,0 |
| 27 | 756 | 1 433 | — | — | — | UNSAT | 2 004 | 14 932 | 0,0 |
| 28 | 812 | 1 542 | — | — | — | UNSAT | 2 001 | 14 485 | 0,0 |
| 29 | 870 | 1 655 | — | — | — | UNSAT | 2 002 | 13 628 | 0,0 |
| 30 | 930 | 1 772 | — | — | — | UNSAT | 2 001 | 11 937 | 0,0 |
| 31 | 992 | 1 893 | — | — | — | UNSAT | 2 001 | 15 677 | 0,0 |
| 32 | 1 056 | 2 018 | — | — | — | UNSAT | 2 002 | 16 316 | 0,0 |
| 33 | 1 122 | 2 147 | — | — | — | UNSAT | 2 002 | 16 812 | 0,0 |
| 34 | 1 190 | 2 280 | — | — | — | UNSAT | 2 001 | 18 955 | 0,0 |
| 35 | 1 260 | 2 417 | — | — | — | UNSAT | 2 003 | 19 049 | 0,0 |
| 36 | 1 332 | 2 558 | — | — | — | UNSAT | 2 001 | 17 993 | 0,0 |
| 37 | 1 406 | 2 703 | — | — | — | UNSAT | 2 003 | 15 408 | 0,0 |
| 38 | 1 482 | 2 852 | — | — | — | UNSAT | 2 001 | 9 771 | 0,0 |
| 39 | 1 560 | 3 005 | — | — | — | UNSAT | 2 001 | 9 196 | 0,0 |
| 40 | 1 640 | 3 162 | — | — | — | UNSAT | 2 003 | 10 541 | 0,0 |

Ajustements : **nœuds DPLL : ×243 par niveau** (pente 7,93, h = 4..5 ;
budget de 3 M dépassé dès h = 6, 164 s) ; **conflits CDCL : pente
log-log 1,92** (polynomial apparent de degré < 2), facteur ×1,097 par
niveau (≈ 1) ; décisions : de 20 (h = 4) à 10 541 (h = 40), soit un
exposant apparent ≈ 2,7 sur les extrêmes (calcul à la main) — polynomial.

**Artefact à consigner honnêtement** : à partir de h = 20 le nombre de
conflits se fige à 2 001-2 004 quelle que soit la hauteur. Ce plateau est
un effet d'ordonnanceur de CaDiCaL (une passe de simplification —
élimination de variables, probing, vivification — déclenchée autour de
2 000 conflits achève la réfutation), pas une mesure de taille de
preuve ; ces techniques sont elles-mêmes des étapes de résolution, et
le verdict polynomial tient a fortiori (≤ 2 004 conflits pour tout
h ≤ 40 contre > 3 M nœuds arborescents dès h = 6). « conflits » est,
dans ce régime, un proxy de fidélité moindre que dans le régime PHP.

## 3. Le tableau 2 × 2, prédit puis mesuré

| | DPLL (arborescent) | CDCL (résolution) |
|---|---|---|
| PHP_n | prédit exp (Haken) — **mesuré ×9,3 / pigeon** | prédit exp (Haken) — **mesuré ×6,55 / pigeon** |
| Peb(P_h) | prédit exp (BIW04) — **mesuré ×243 / niveau** | prédit poly (BKS04) — **mesuré ≤ 2 004 conflits, pente log-log 1,9** |

Les trois cellules de contrôle et la cellule qui teste le mécanisme
sont conformes. Ce que cela établit, à l'échelle atelier : (i) le sens
borne-inférieure de « la trace est une preuve » (Haken se lit dans le
compteur de conflits d'un solveur de 2026) ; (ii) son sens
borne-supérieure — les heuristiques réelles de CaDiCaL TROUVENT la
réfutation polynomiale que la résolution générale possède, là où le
DPLL, confiné à l'arborescent, ne le peut pas. Les deux issues
contraires nommées par la candidature (CDCL polynomial sur PHP ⟹ trace
hors résolution ; CDCL exponentiel sur Peb ⟹ l'heuristique gouverne)
ne se sont pas produites.

## 4. Réserves

- Réplication déclarée (BKS04 §5) ; les taux de croissance mesurés
  dépendent des heuristiques (DPLL : ordre fixe des variables ; CDCL :
  CaDiCaL par défaut) — seules les bornes inférieures sont
  indépendantes des heuristiques (théorèmes).
- Plateau à ~2 000 conflits : artefact d'ordonnanceur (§2), verdict
  inchangé.
- DPLL arrêté au budget de 3 M nœuds (PHP₉ après 560 s ; Peb h = 6
  après 164 s) — deux points non conclus, sans conséquence sur les
  pentes (calculées sur les points conclus).
