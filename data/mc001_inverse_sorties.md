# MC-001 stratégie C (mc001-inverse) — sorties exactes consignées

Scripts : `mc001_inverse_algorithmes.py` (sous-commandes exact / valide /
invariants / strata / sym / lp / lpgap), `mc001_wr_classes_n4.py` (+ mode mono).
Tous dans ce scratchpad. Dépôt en lecture seule respecté.

## 1. Tables exactes exhaustives de W (SANS solveur — B&B, approfondissement itératif)

- n=2 : {0:2, 1:6, 2:8}
- n=3 : {0:2, 1:14, 2:60, 3:96, 4:72, 5:12} — médiane 3, max 5 (12 f)
- n=4 : {0:2, 1:30, 2:320, 3:1680, 4:5860, 5:13344, 6:19228, 7:17416,
  8:6984, 9:672} — médiane 6, max 9 ; W>=6 : 67,60 %, W>=7 : 38,26 %,
  W>=8 : 11,68 %, W=9 : 672/65536 = 1,025 %
- temps : < 1 s pour les 1992 classes n=4 (instrument nouveau, cf. CP-SAT
  du dépôt : 60 s de time-limit PAR classe dans task_d005_largeness.py)

## 2. Validation croisée (protocole du dépôt)

- Distributions identiques aux pourcentages publiés de D-005 (70,31 % /
  4,69 % à n=3 ; 67,60 % / 38,26 % / 11,68 % / ~1,03 % à n=4).
- Spot-check CP-SAT du dépôt (task_a013_cout_convention.poids_min) sur
  12 masques n=4 aléatoires (seed 20260802) : 12/12 accords.
- Chaque témoin optimal re-vérifié par énumération indépendante (fonction
  `reverifie`).

## 3. Batterie LP/MILP (sous-commande lp)

| instance | n | W | W_R (coefs réels, orientation exacte) | LP totale relaxée | LP_couv(f) | LP_couv(non f) |
|---|---|---|---|---|---|---|
| PARITY_3 | 3 | 3 | 3.0 | 0.0 | — | — |
| MAJ_3 | 3 | 3 | 3.0 | 0.0 | 3.0 | — |
| AND_3 | 3 | 1 | 1.0 | 0.0 | 1.0 | — |
| OR_3 | 3 | 3 | 3.0 | 0.0 | 3.0 | — |
| NOR_3 | 3 | 3 | 3.0 | 0.0 | — | 3.0 |
| THR2_3 | 3 | 3 | 3.0 | 0.0 | 3.0 | — |
| PARITY_4 | 4 | 4 | 4.0 | 0.0 | — | — |
| MAJ_4 | 4 | 4 | **3.0** | 0.0 | 4.0 | — |
| AND_4 | 4 | 1 | 1.0 | 0.0 | 1.0 | — |
| OR_4 | 4 | 4 | 4.0 | 0.0 | 4.0 | — |
| NOR_4 | 4 | 4 | 4.0 | 0.0 | — | 4.0 |
| THR2_4 | 4 | 4 | 4.0 | 0.0 | 6.0 | — |
| IP_4 | 4 | 2 | 2.0 | 0.0 | — | — |
| AND(OR2^2) | 4 | 4 | 4.0 | 0.0 | 4.0 | — |
| XOR(OR2^2) | 4 | 6 | 6.0 | 0.0 | — | — |
| MAJ3(OR2^3) | 6 | 12 | 12.0 | 0.0 | 12.0 | — |
| AND2(MAJ3^2) | 6 | 6 | 6.0 | 0.0 | 9.0 | — |

- Témoin W_R(MAJ_4) = 3 vérifié indépendamment : les 6 paires à coefficient
  1/2 ; valeurs uns {1.5, 3}, zéros {0, 0.5}, gap minimal exactement 1.0.
- « LP totale relaxée = 0 » partout = la vacuité (théorème d'une ligne :
  a≡0, d≡1/2 est admissible dès M>=2).
- LP_couv = LP du stratum unilatéral (monômes légaux = up-cube inclus dans
  les uns ; distincte de la borne inf « cover_lp » de F-020, qui n'impose
  pas la légalité et ne contraint que les uns minimaux — objets différents,
  pas de contradiction avec « LP couverture = 3 » de F-020).

## 4. W_R sur les 1992 classes n=4 (mc001_wr_classes_n4.py)

ratio W/W_R : 1.0 → 1944 classes ; 1.067 → 4 ; 1.077 → 16 ; 1.091 → 12 ;
1.111 → 6 ; 1.2 → 4 ; 1.25 → 2 ; 1.333 → 2. Pire ratio 4/3 (classe 6015 =
classe de MAJ_4/complément, W=4, W_R=3.0). 1 échec MILP (time-limit 60 s),
re-essayé à part (voir mc001_wr_echec.log).

## 4bis. Reprise de l'échec MILP (classe 15851, W=7)

- scipy/HiGHS : « HiGHS Status 4: Solve error » (échec numérique big-M,
  reproduit à tl=600) — fragilité d'instrument consignée.
- Voie indépendante (CP-SAT à dénominateur : b_S entiers, |q(x)-q(y)| >= D,
  min sum(b)/D, optima prouvés) : W_D/D = 7.0 pour D = 1, 2, 3, 4, 6, 12.
  Aucun gain rationnel jusqu'au dénominateur 12 — la classe est tight
  pour tout D <= 12 (pas un certificat pour D arbitraire).

## 8. Détermination brute (test le plus généreux)

- Uplets BRUTS (non symétrisés) des 15 invariants, n=4 : 3 689 classes,
  122 AMBIGUËS, 4 692 fonctions concernées. Témoin écart max :
  f=0000011011110000 (masque 1776) W=4 vs f=0000001011101100 (masque 748)
  W=6 — égalité des 15 invariants vérifiée valeur par valeur.

## 9. Note structurelle (stratum {0,1} dégénéré)

Tout séparateur dont les valeurs sont dans {0,1} (uns -> {1},
zéros -> {0}) a AU PLUS UN monôme : si S1 != S2 sont dans le support,
l'entrée u = S1 union S2 reçoit p(u) >= a_S1 + a_S2 >= 2, hors {0,1}.
L'« analogue partition-χ₁ » du paysage (partition disjointe des uns par
up-cubes) N'EXISTE PAS comme stratum de MinSYM+ — correction à la
formalisation acquise, pertinente pour tout mapping HIL futur.

## 5. Gap LP/ILP de la couverture unilatérale (lpgap)

- n=3 : 8 (classe, orientation) faisables, gap max = 1.000
- n=4 : 28 (classe, orientation) faisables, gap max = 1.000
La LP de couverture légale est INTÈGRE sur toutes les instances faisables
à n<=4.

## 6. Monotones (mc001_wr_classes_n4.py mono)

- n=3 : 20 monotones, 0 écart W vs #uns minimaux.
- n=4 : 168 monotones, 1 écart : THR2_4 (f=1111111011101000), W=4 <
  couvert=6 — le zoo monotone (comptage symétrique) commence dès n=4.

## 7bis. Détermination n=4 (LE RÉSULTAT CENTRAL DE LA PISTE c)

- 65 534 fonctions non constantes. AUCUN des 15 invariants seuls ne
  détermine W. Le 15-UPLET COMPLET SYMÉTRISÉ ne détermine pas W :
  42 classes ambiguës / 1874, 3 456 fonctions concernées.
- Test encore plus généreux, uplets BRUTS (non symétrisés, partition
  plus fine) : 122 classes ambiguës / 3 689, 4 692 fonctions concernées.
- TÉMOIN (uplets bruts, écart max) : f=0000011011110000 (masque 1776),
  W=4 vs f=0000001011101100 (masque 748), W=6 — les 15 invariants
  identiques valeur par valeur, W différant de 2. Vérifié.
- Témoin symétrisé (écart max) : masque 8186 (W=4) vs masque 968 (W=6),
  15-uplets symétrisés identiques.
- Égalités exactes n=4 : toutes s'effondrent (W=anf 22,6 % ; W=nones-sym
  25,5 % ; le reste < 20 %).
- W >= alt : 0 violation à n=4 aussi ; ratio W/alt max = 5.0, médiane 1.75
  (l'alternance s'affaiblit avec n : max 3.0 à n=3).
- ATTENTION artefact : « wuni : 1 seule classe ambiguë » n'est PAS un
  succès — la classe ambiguë est (-1,-1) = stratum infaisable, qui
  contient 99,5 % des fonctions.

## 7ter. Strata n=4 et symétriques n=4

- Strata n=4 : 65 202/65 534 (99,5 %) sans AUCUN séparateur unilatéral
  (deux orientations) ; 330 avec W = couvert ; 2 (la paire THR2_4 /
  complément) où l'arithmétique bat un couvert existant (4 < 6).
- Symétriques n=4 : 30/30 W = W_sym (l'optimum est atteint par un
  séparateur symétrique) ; toutes les symétriques non constantes ont
  W = 4 sauf AND_4 et son complément (W = 1).

## 7. Invariants / détermination / strata / sym : n=3

- n=3, 254 non constantes : AUCUN invariant seul ne détermine W (le moins
  mauvais : wuni, 1 classe ambiguë sur 4 ; anf : 4/7 ambiguës). Le
  15-uplet complet détermine W (37 classes, 0 ambiguë) — petite taille.
- Égalités exactes n=3 : W=anf 56,7 % ; W=sens 46,5 % ; W=degR 44,1 % ;
  W=alt 41,7 % ; toutes loin de 100 %.
- Théorème W >= alt : 0 violation (n=3) ; ratio W/alt max = 3.0.
- Strata n=3 : 218/254 (85,8 %) sans AUCUN séparateur unilatéral (dans les
  deux orientations) ; 36/254 (14,2 %) W = couvert ; 0 cas où
  l'arithmétique bat un couvert existant.
- Symétriques n=3 : 14/14 W = W_sym (optimum atteint symétriquement).
