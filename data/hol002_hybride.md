# HOL-002 — Mesures : l'hybride des quatre îles et la croissance du min-support de jauge

Tâche : HOL-002 (piste utilisateur « orbite de jauge », 2026-08-08).
Scripts : `checks/hol002_hybride.py` (campagne, session) +
`checks/explo_jauge_quatre_iles.py` et `checks/explo_min_support_jauge.py`
(utilisateur, REJOUÉS par la session — réplication vérifiante).
Régime : w = 0 (Z = #SAT, le régime dur) pour la campagne ; w ∈ {0, 0.3}
pour les réplications.

## 1. Réplication des scripts utilisateur — CONFORME

- `explo_jauge_quatre_iles.py` : invariance de jauge vérifiée (jauges
  aléatoires : somme des 2^E termes = Z à ~10⁻¹²) ; à la jauge BP, les
  excitations simples s'annulent (max ~10⁻¹³-10⁻²⁷) ; arbre → 1 terme
  non nul (Z_Bethe = Z exact) ; instance à boucles → 625 termes non
  nuls (le chiffre annoncé, retrouvé) ; corrections sur les boucles
  généralisées. [Dernier bloc E = 21 tombé juste après la
  consignation : CONFORME — invariance 1.8e-12, et **18 381 boucles
  généralisées sur 2^21** contre 625 à E = 15 (×29 pour +6 arêtes) :
  l'explosion du point (d) mesurée dans le script utilisateur
  lui-même.]
- `explo_min_support_jauge.py` : S(identité) = #SAT = 16 (w = 0) et
  2^n = 32 (w = 0.3) ✓ ; S(BP) = 625 ✓ ; S(Hadamard) = 1024 ;
  **S(alignée-clause) = 10 — MEILLEUR que la borne 2^m = 32 annoncée
  par l'en-tête du script** ; exhaustif {I,C}¹⁵ ET recuit : min S = 10,
  atteint par l'alignée-clause pure. Toutes les sommes re-vérifiées = Z.

## 2. La campagne (hol002_hybride.py) — la table

Jauges : I (identité), C (alignée-clause), H (Hadamard), B (BP) ;
S_min = min(dictionnaire) puis recuit par arête (120/60 pas, sauf
n = 8 : jauges-îles seules). Chaque somme re-vérifiée contre Z exact.

| instance | n | m | E | Z = #SAT | S(I) | S(C) | S(H) | S(B) | S_min |
|---|---|---|---|---|---|---|---|---|---|
| utilisateur (répliquée) | 5 | 5 | 15 | 16 | 16 | **10** | 1024 | 625 | 10 |
| arbre + 0 corde | 9 | 4 | 12 | 294 | 294 | 10 | 8 | **1** | 1 |
| arbre + 1 corde | 9 | 5 | 15 | 262 | 262 | 13 | 64 | **5** | 5 |
| arbre + 2 cordes | 9 | 6 | 18 | 233 | 233 | **23** | 512 | 50 | 23 |
| dure n=4 (g=1,2,3) | 4 | 4 | 12 | 8/10/8 | =Z | **5/7/5** | 256 | 175 | 5/7/5 |
| dure n=5 (g=1,2,3) | 5 | 5 | 15 | 15/16/18 | =Z | **8/10/10** | 1024 | 625 | 8/10/10 |
| dure n=6 (g=1,2,3) | 6 | 6 | 18 | 27/29/28 | =Z | **14/17/14** | 4096 | 2250 | 14/17/14 |
| dure n=7 (g=1,2,3) | 7 | 7 | 21 | 52/49/56 | =Z | **27/26/30** | 16384 | 8125 | 27/26/30 |
| dure n=8 (g=1) | 8 | 8 | 24 | 81 | 81 | **33** | 65536 | 29375 | 33 |

## 3. La courbe S_min(n) — famille dure (hors des quatre îles)

| n | S_min (3 graines) | #SAT | 2^n | S_min / #SAT |
|---|---|---|---|---|
| 4 | 5, 7, 5 | 8, 10, 8 | 16 | 0.63, 0.70, 0.63 |
| 5 | 8, 10, 10 | 15, 16, 18 | 32 | 0.53, 0.63, 0.56 |
| 6 | 14, 17, 14 | 27, 29, 28 | 64 | 0.52, 0.59, 0.50 |
| 7 | 27, 26, 30 | 52, 49, 56 | 128 | 0.52, 0.53, 0.54 |
| 8 | 33 | 81 | 256 | 0.41 |

## 4. Lecture

1. **Le mur est mesuré : hors des îles, S_min croît comme Z lui-même**
   — S_min ≈ 0.4-0.6 × #SAT à tous les points, ratios de croissance
   ×1.6 → ×1.9 par pas de n : EXPONENTIEL. Le point (d) du script
   utilisateur (« la jauge réorganise l'exponentielle, elle ne la
   comprime que sur les îles ») est désormais quantitatif : la
   compression plafonne à un facteur ~2 sous le comptage des solutions.
2. **Le minimum vit SUR les îles pures — 17/17 instances** : famille
   dure → alignée-clause pure (le recuit n'a JAMAIS amélioré, 0/13) ;
   arbres → BP pure (S = 1 sur l'arbre : l'île exacte) ; l'instance
   à 2 cordes → alignée-clause. L'orbite de jauge UNIFIE les îles
   (l'invariance est vraie et vérifiée) mais ne les ÉTEND pas : aucun
   minimum hybride strictement entre les îles n'a été observé.
3. L'île gagnante se choisit par structure : boucles rares → BP ;
   dense/frustré → alignée-clause. Observation (hypothèse de lecture,
   non prouvée) : la section alignée-clause est une
   inclusion-exclusion sur les clauses déguisée — S(C) ≈ #SAT/2 en
   serait la trace ; à trancher avec le folklore-check.
4. **Réponse à la demande « un hybride qui calculerait Z en temps
   polynomial »** : l'hybride est construit et calcule Z en polynomial
   exactement là où une île pure le faisait déjà. La mesure dit
   pourquoi il ne fait pas plus : son support croît comme Z/2 hors
   des îles.

## 5. Réserves

- S_min = minimum sur le DICTIONNAIRE (4 jauges par arête) + recuit
  budgété : l'orbite CONTINUE GL₂^E n'est explorée que par ses
  sections remarquables — un minimum continu strictement meilleur
  n'est pas exclu par la mesure (mais la charge de la preuve est
  déplacée : c'est lui qu'il faudrait exhiber).
- Régime w = 0 seul pour la campagne ; une seule graine à n = 8 ;
  recuit modeste (120/60 pas).
- Le folklore-check du « min-support de jauge » comme objet est
  [À SOURCER] (gauging de réseaux de tenseurs, troncatures de séries
  de boucles) — aucune revendication de nouveauté ; A-021 en cours
  pour le paysage.

## 6. Addendum 2026-08-09 — la réserve « orbite continue » traitée (fil utilisateur EXPLO-JAUGE, répliqué)

Le commit utilisateur 1122902 (8 scripts, 2 040 lignes) répond à la
réserve du §5. RÉPLICATION SESSION des deux pièces pivots, conformes
ligne à ligne :

- `explo_refutation_A_dictionnaire.py` : bloc G (n = 6, m = 3, E = 9,
  #SAT = 45) — jauges pures I/C/H/B : S = 45/8/8/2 ; exhaustif
  {I,C,H,B}⁹ = 262 144 : **min par bloc = 2** (config BHBBHBBHB,
  70 s) ; multiplicativité sur T₂ (12 vars) : #SAT = 45² = 2025,
  S(C) = 8² = 64, S(B) = 2² = 4, meilleure-config-dupliquée = 2² —
  ⟹ **S ≥ 2^r sur T_r pour TOUT choix du dictionnaire : NON-A
  (dictionnaire) prouvée**. Réserve du script lui-même : « A reste
  ouverte pour des familles de jauges non encore construites. »
- `explo_test_theta.py` : θ (3 clauses partageant u, v ; Z = 25) —
  lemme de rigidité VÉRIFIÉ ; S(identité/Möbius/Hadamard/BP/aligné) =
  25/8/16/5/4 ; recuit complexe 40 redémarrages : minima {4 : 12,
  5 : 8, 8 : 10, 512 : 10}, **jamais sous 4** (45 s) ; lecture du
  script : recherche = borne SUP, l'exacte demanderait l'élimination
  des quantificateurs sur GL₂(ℂ)⁹.

Statut consolidé : NON-A PROUVÉE pour le dictionnaire constructible ;
la voie absolue (bloc θ, chaîne min-S(θ) ≥ 2 ⟹ min-S(Θ_r) ≥ 2^r ⟹
NON-A_exist) AVANCÉE NON CLOSE (368 survivants archivés
`checks/theta_survivants_totale.txt`, balayage restant — leçon L20.5
du fil : pas de clôture maquillée) ; RENVERSEMENT consigné : la jauge
monodromie-compagnon (hors dictionnaire, poly-constructible) atteint
S = 1 sur T_r en calculant tr(M) — « une bonne jauge EST un calcul
déjà fait » ; portée honnête du fil, verbatim : borne de MODÈLE
(Θ_r est facile : Z = 25^r — « le Tardos de jauge auto-réalisé »),
indépendante de #P vs FP dans les deux sens, zéro barrière franchie ;
parenté [à sourcer] : Verstraete-Cirac (formes canoniques des réseaux
à boucles).
