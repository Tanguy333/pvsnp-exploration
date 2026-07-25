# Témoins exécutables — cellule → script → commande → sortie → durée

> **Ce que ce fichier est.** L'instrument de rejouabilité de
> [`matrice_barrieres.md`](matrice_barrieres.md). Pour chaque cellule de l'Atlas
> adossée à un calcul : le script exact, la commande exacte, la ligne de sortie
> qui porte le résultat, la durée observée, et le statut. Un tiers doit pouvoir
> refaire n'importe quel chiffre cité par une cellule sans avoir à lire le reste
> du dépôt.
>
> **Le trou qu'il comble.** `checks/` contient **188 scripts** (compte réel au
> 2026-07-25) et **aucun n'est cité par le corps de la matrice** : les cellules
> renvoient à des fiches `tasks/done/`, qui renvoient aux scripts. Ce tableau est
> le maillon manquant. Il ne liste pas les 188 : seulement les **17 scripts
> (18 lignes)** qui portent une cellule ou un chiffre cité dans l'Atlas — voir
> §4 pour ce qui est exclu et pourquoi.
>
> **Ce fichier ne prouve rien de neuf.** Il rend vérifiable ce qui est déjà
> écrit ailleurs. Chaque ligne dit d'où vient sa sortie attendue : re-exécution
> datée du 2026-07-25 (ATLAS-010), ou fiche `tasks/done/` citée.

## 1. Conventions de lecture

**Deux répertoires d'exécution, et ce n'est pas cosmétique.** Le dépôt a deux
familles de scripts :

- ceux qui **importent un module frère** (`from task_v004_kv_conjecture5 import …`,
  `import task_v001_torus as T`) — ils exigent `checks/` comme répertoire
  courant, sinon `ModuleNotFoundError` ;
- ceux qui **écrivent dans `data/`** par chemin relatif
  (`open("data/weight_tc0_d2.csv", "w")`) — ils exigent la **racine du dépôt**
  comme répertoire courant, sinon le CSV atterrit ailleurs ou le run échoue.

La colonne « Commande » donne le répertoire à chaque fois. Aucun script du
tableau ne relève des deux familles à la fois.

**Colonne « Ligne de sortie attendue »** : verbatim, telle que le script
l'imprime (accents absents dans les sorties : les scripts sont en ASCII). Quand
la ligne contient une durée entre parenthèses, cette durée est celle du run
d'origine — c'est le contenu, pas le chronomètre, qui doit coïncider.

**Colonne « Statut »** : `REJOUÉ <date>` = ré-exécuté et sortie reproduite lors
d'ATLAS-010 ; `NON REJOUÉ` = sortie et durée reprises de la fiche `tasks/done/`
citée ; suivi de l'étiquette épistémique de ce que le témoin atteste
(MESURÉ / PROUVÉ / RÉPLIQUE).

**`[NON VÉRIFIÉ]`** marque toute durée qu'aucune fiche ni aucun log du dépôt
n'écrit.

## 2. Le tableau

| Ligne Atlas | Script | Commande (répertoire courant) | Ligne de sortie attendue | Durée observée | Statut |
|---|---|---|---|---|---|
| **14** — toriques, régime utile | [`checks/task_v004_kv_conjecture5.py`](../checks/task_v004_kv_conjecture5.py) | `cd checks && python task_v004_kv_conjecture5.py` | `CONJECTURE 5 : CONFIRMEE sur toute la grille testee.` (grille n = 6..16, d ≤ 8) | **0,8 s** | REJOUÉ 2026-07-25 · MESURÉ |
| **14** — réfutation Conj. 5, détection exacte | [`checks/task_v017c_verif_exacte.py`](../checks/task_v017c_verif_exacte.py) | `cd checks && python task_v017c_verif_exacte.py` | `[SUSPECT] (d=21, n=30) : min EXACT = 517673216, 2 minima ; 2-bouts : non ; KV (haut/bas +-1) : NON/NON` (13 suspects NON/NON, 3 témoins sains OUI/OUI) | **0,4 s** (16 cellules) | REJOUÉ 2026-07-25 · MESURÉ |
| **14** — réfutation Conj. 5, consolidation | [`checks/task_v018_contre_exemple.py`](../checks/task_v018_contre_exemple.py) | `cd checks && python task_v018_contre_exemple.py` | `CONTRE-EXEMPLE ETABLI : a (d=21, n=30), AUCUN plus court` / `vecteur n'a gamma_n = +-1` ; en amont `(1-x)^22 divise v : True` et `vecteurs gamma_n = +-1 de norme <= 517673216 : 0` | **0,8 s** | REJOUÉ 2026-07-25 · PROUVÉ (par contre-exemple) |
| **14** — moteurs SVP | [`checks/svp_turbo.py`](../checks/svp_turbo.py), [`checks/svp_sym.py`](../checks/svp_sym.py) | *aucune* — bibliothèques sans CLI, importées par les scripts `task_v0*` | API : `turbo_shortest(G) -> (min_exact, [minimaux])` — énumération Schnorr-Euchner compilée Numba, **vérification finale en entiers Python exacts** | n/a | MOTEUR · (exactitude portée par les appelants) |
| **14** — asymétrie MAJ, n = 7 | [`checks/task_atlas003_maj7.py`](../checks/task_atlas003_maj7.py) | `cd checks && python task_atlas003_maj7.py` | `VERDICT n=7 : egalite sym = general partout, CERTIFIEE` | d = 2 et d = 3 : **240 s chacun** (`time_limit` relevé pour obtenir la certification) ; total **[NON VÉRIFIÉ]** | NON REJOUÉ · MESURÉ ([ATLAS-003](../tasks/done/ATLAS-003.md)) |
| **14** — contrôle positif Δ_w | [`checks/task_atlas005_delta_controle.py`](../checks/task_atlas005_delta_controle.py) | `cd checks && python task_atlas005_delta_controle.py` | `BILAN gains asymetriques certifies : AUCUN` | log bancarisé [`checks/atlas005_controle_log.txt`](../checks/atlas005_controle_log.txt) (run complémentaire n = 6, 7) : 13 cellules, **570 s** cumulées, dont 4 à la limite de 120 s | NON REJOUÉ · MESURÉ ([ATLAS-005](../tasks/done/ATLAS-005.md)) |
| **7** — SYM∘AND, étalonnage du moteur | [`checks/tour_27_s2_espace_entier_cpsat.py`](../checks/tour_27_s2_espace_entier_cpsat.py) | `cd checks && python tour_27_s2_espace_entier_cpsat.py calib` | `ETALONNAGE : MOTEUR VALIDE sur verite terrain` (k = 3 : cap 11 UNSAT / cap 12 SAT ; k = 4 : cap 19 UNSAT / cap 20 SAT ; k = 5 : cap 19 UNSAT) | **89 s** au rejeu (0 / 0 / 5 / 7 / 77 s) ; fiche d'origine : 0 / 0 / 3 / 4 / 41 s | REJOUÉ 2026-07-25 · RÉPLIQUE (vérité terrain reproduite) |
| **7** — SYM∘AND, barreau haut | [`checks/tour_27_s2_espace_entier_cpsat.py`](../checks/tour_27_s2_espace_entier_cpsat.py) | `cd checks && python tour_27_s2_espace_entier_cpsat.py 29 4000` | `cap=29 : UNSAT (3517s) — THEOREME NEUF : W(MAJ_5(OR2^5)) >= 30` | **3 517 s** pour ce seul barreau ; **≈ 3 h 20** pour l'échelle 19 → 29 (11 barreaux, 58 s → 3 517 s) | NON REJOUÉ · MESURÉ, certifié-solveur sous cassage de symétrie, sans certificat DRAT — voir §3 réserve 2 ([T27-S2 §4](../tasks/done/T27-S2.md)) |
| **7** — SYM∘AND, classe décomposable | [`checks/task_t26s1_dec_exhaustif.py`](../checks/task_t26s1_dec_exhaustif.py) | `cd checks && python task_t26s1_dec_exhaustif.py 3 4 5` | `k=5 : W_dec = 30 = k(k+1), LOI CONFIRMEE  (total 0s)` | **< 1 s** (les trois k) | REJOUÉ 2026-07-25 · PROUVÉ dans la classe (exhaustif sans solveur, **sous le plafond consigné `w_bloc ≤ cible − 2(k−1)`**, [T26-S1 §2](../tasks/done/T26-S1.md)) |
| **7** — SYM∘AND, le point k = 9 | [`checks/task_t26s1_dec_exhaustif.py`](../checks/task_t26s1_dec_exhaustif.py) | `cd checks && python task_t26s1_dec_exhaustif.py 9` | `k=9 : W_dec = 90 = k(k+1), LOI CONFIRMEE` (format du script ; en amont, `k=9 W=85 : vide` … `k=9 W=90 : REALISABLE` — chaque niveau vide est une borne inférieure prouvée) | **15 884 s** au total (≈ 4 h 25) : niveaux 85→89 à 1 312–2 363 s chacun, niveau 90 réalisable en 2 601 s | NON REJOUÉ · PROUVÉ dans la classe, **sous le même plafond consigné** ([T26-S1 §2 et §5](../tasks/done/T26-S1.md)) |
| **7** — SYM∘AND, fenêtres du Tour 26 | [`checks/task_t27s3_fenetres.py`](../checks/task_t27s3_fenetres.py) | `cd checks && python task_t27s3_fenetres.py 300 both` | `  ==> FENETRE FERMEE : W(THR_3(OR2^4)) = 20` puis `  ==> FENETRE FERMEE : W(MAJ_3(MAJ3^3)) = 12` | THR₃ : **139 s** (cap 20 SAT 15 s ; 18 UNSAT 53 s ; 19 UNSAT 71 s). MAJ₃(MAJ3³) : cap 12 SAT **54 s** ; caps 4→11 UNSAT, **13 à 42 s** chacun | NON REJOUÉ · MESURÉ, certifié-solveur (mêmes réserves qu'au barreau haut — §3 réserve 2, [T27-S3](../tasks/done/T27-S3.md)) |
| **7** — IP est trivial en SYM∘AND | [`checks/task_f003_symand_ip.py`](../checks/task_f003_symand_ip.py) | `cd checks && python task_f003_symand_ip.py` | `  k=2 : poids minimal = 2 (statut Optimal)   = k (construction triviale optimale)` puis `CONCLUSION : le poids SYM o AND de IP est lineaire (= k).` | **0,9 s** | REJOUÉ 2026-07-25 · MESURÉ (ILP, optimalité certifiée) |
| **7** — la weight PTF d'IP, forme close | [`checks/task_f006b_certificate_proof.py`](../checks/task_f006b_certificate_proof.py) | `cd checks && python task_f006b_certificate_proof.py` | `CERTIFICAT VALIDE EN ARITHMETIQUE EXACTE.` puis `T-F006 : W_L1(IP_{2k}) = (3^k-1)/2 = DNF_min(IP_{2k}), sur R,` (orbites en Fractions k = 1..14 ; force brute k = 1..4) | **0,2 s** | REJOUÉ 2026-07-25 · PROUVÉ (preuve d'une page, vérifiée mécaniquement) |
| **7 + 11** — weight L1 des PTF, TC⁰ d = 2 | [`checks/task_f001_weight_tc0_d2.py`](../checks/task_f001_weight_tc0_d2.py) | `python checks/task_f001_weight_tc0_d2.py` **depuis la racine** (réécrit [`data/weight_tc0_d2.csv`](../data/weight_tc0_d2.csv)) | `  IP_8 : degre min = 4, L1 au degre min = 640` (suite 20 → 119 → 640 aux degrés minimaux ; `EXACT_2`/`EXACT_3` INFEASIBLE à D = 1) | **≈ 70 s**, dont IP_8 à D = 5 : **57,7 s** | NON REJOUÉ (réécrit `data/`) · MESURÉ ([F-001](../tasks/done/F-001.md)) |
| **4** — MAJ mod 6 vs OR mod 6 | [`checks/task_f009_maj_mod6.py`](../checks/task_f009_maj_mod6.py) | `cd checks && python task_f009_maj_mod6.py` | `  30 \|     16 \|   >cap \|     16 \|                4` — à n = 30 : MAJ mod 6 = **16**, OR mod 6 = **4** (colonnes : n, mod 2, mod 3, mod 6, OR mod 6) | **2,5 s** | REJOUÉ 2026-07-25 · MESURÉ (exact dans la classe symétrique) |
| **4** — la loi de deg₆^sym(MAJ_n) | [`checks/task_f011_maj_law.py`](../checks/task_f011_maj_law.py) | `cd checks && python task_f011_maj_law.py` | `Anomalies vs L1 (n, t, d6, L1) : [(4, 2, 3, 2), (16, 8, 9, 8)]` (2 anomalies sur n = 1..44) | **19,7 s** | REJOUÉ 2026-07-25 · MESURÉ → CONJECTURE C-F011 |
| **4** — la « plate » deg₆(MAJ_n) = ⌈n/2⌉ | [`checks/task_f011e25_ansatz_machine.py`](../checks/task_f011e25_ansatz_machine.py) | `cd checks && python task_f011e25_ansatz_machine.py` | `PLATE CONFIRMEE jusqu'a n = 20 (avec 4..13, 16, 32 deja acquis).` | **0,7 s** (chaque cellule à 0 s) | REJOUÉ 2026-07-25 · MESURÉ (certificats explicites) |
| **4** — famille infinie K′ | [`checks/task_f011e26_theorem_kprime.py`](../checks/task_f011e26_theorem_kprime.py) | `cd checks && python task_f011e26_theorem_kprime.py` | `THEOREME K' VERIFIE sur k = 0..3 (t = 2, 6, 18, 54).` | **0,1 s** | REJOUÉ 2026-07-25 · PROUVÉ (3 lemmes de Lucas) + vérifié |

## 3. Environnement de référence

Mesuré sur la machine du dépôt le **2026-07-25** :

| Composant | Version |
|---|---|
| Python | **3.13.14** (MSC v.1944, 64 bit, Windows 11) |
| numpy | 2.2.0 |
| sympy | 1.14.0 |
| scipy | 1.17.1 (MILP = HiGHS embarqué — lignes toriques) |
| PuLP | 3.3.1 (ILP = CBC embarqué — F-001, F-003, F-006) |
| Numba | 0.65.1 (cœur d'énumération de `svp_turbo`) |
| OR-Tools / CP-SAT | 9.15.6755 (T26/T27) |
| `tools/cryptominisat5.exe` | v5.14.5, **non versionné** (`.gitignore`) — provenance dans [`tools/README.md`](../tools/README.md) ; utilisé par la seule étape F-011 e21c, hors tableau |

Trois réserves de reproductibilité, à ne pas escamoter :

1. **Les durées CP-SAT dépendent du matériel.** Les scripts T26/T27 fixent
   `num_search_workers = 8` en dur ; sur une machine à moins de 8 cœurs réels,
   les durées ci-dessus sont des minorants. Le rejeu du 2026-07-25 sur
   l'étalonnage T27-S2 a donné **89 s** contre 48 s pour la même séquence dans la
   fiche d'origine — un facteur ~1,9 sans changement de code.
2. **Un UNSAT de CP-SAT n'est pas un certificat.** Les lignes 7 « barreau haut »
   et « fenêtres » reposent sur un cassage de symétrie (lex-leader) non
   re-vérifiable par énumération, et **l'échelle en dépend entièrement** :
   T27-S2 §4 consigne que les caps 19 et 20 relancés **sans** cassage de
   symétrie retombent en `UNKNOWN`. C'est précisément pourquoi le mode `calib`
   existe, et pourquoi il figure **avant** les barreaux dans ce tableau.
   L'export DRAT n'a pas été tenté ([T27-S2](../tasks/done/T27-S2.md) §4).
3. `task_f011e25_ansatz_machine.py` imprime des lignes
   `c found falsified original clause` du solveur SAT sous-jacent : messages de
   simplification d'entrée, **anodins** — la validité repose sur la
   re-vérification par profils du script, pas sur le statut SAT seul.

## 4. Ce que ce tableau ne contient pas

**17 scripts sur 188.** Les 171 autres ne sont pas listés parce qu'aucune
cellule de l'Atlas ne les cite. Ils se répartissent en trois familles, et la
distinction importe :

- **les étapes intermédiaires d'un fil** (36 scripts `task_f011e*`, 36
  `task_as*`, 34 `task_v*`) : chacune a produit un résultat vrai, consigné dans
  sa fiche `tasks/done/` ; le tableau ne retient que celles dont un chiffre
  remonte jusqu'à une cellule ;
- **les échafaudages de tour** (36 scripts `tour_*`, dont
  `tour_26_proposeur_*`, `tour_27_proposeur_*`, `tour_27_refuteur_*`) :
  subsumés a posteriori par le moteur de T27-S2, ils restent l'historique de
  construction de l'instrument ;
- **les répliques** (`repli_smolensky.py`, `repli_hastad_switching.py`,
  `repli_bbr_mod6.py`, `repli_williams_eval.py`) : réplications vérifiantes de
  résultats connus, seule exception admise à la directive « on ne refait pas la
  littérature ». Elles n'appuient aucune cellule et n'ont pas vocation à le
  faire.

**Réserves de sourçage.**

- L'énumération exhaustive de **tous** les vecteurs minimaux aux cellules
  (17, 30) et (22, 28), qui renforce la réfutation de la Conjecture 5
  ([V-055](../tasks/done/V-055.md) §E3), **n'a pas de script dédié dans
  `checks/`** : **[NON TROUVÉ]**. La fiche V-055 ne nomme que
  `checks/task_v052_borne_sup.py`, qui porte son erratum E1 (le fit
  exponentiel), pas E3. Ce qui est rejouable en une commande, c'est la cellule
  (21, 30) — le contre-exemple publiable — et le fait que (22, 28) a exactement
  2 minima, tous deux `NON/NON`, via `task_v017c_verif_exacte.py`.
- `checks/task_f006_orbit_dual.py` (LP de découverte du certificat dual, écrit
  [`data/orbit_dual.csv`](../data/orbit_dual.csv)) n'est pas au tableau : c'est
  `task_f006b_certificate_proof.py` qui **vérifie** le théorème T-F006. Le
  premier a trouvé la forme close aux petits k, le second la prouve pour tous.
- `checks/task_v002_torus_n56.py` (égalité sym = général à n = 5, 6, cité par la
  ligne 14) n'est pas au tableau : `task_atlas003_maj7.py` étend la même mesure à
  n = 7 **avec certification exigée**, et [ATLAS-003](../tasks/done/ATLAS-003.md)
  documente que le verdict non certifié était trop fort. Un incumbent ne prouve
  rien.
- `checks/task_f011e33_plate_25_31.py` n'est pas au tableau : il documente une
  **frontière d'outil** (n = 26, 27, 28, 30 restés ouverts) et ne porte aucun
  chiffre cité par une cellule.
- Le log `checks/atlas005_controle_log.txt` provient d'un run
  **complémentaire** (n = 6, 7) et se termine par
  `BILAN complementaire : gains certifies = AUCUN`, alors que le script
  committé boucle sur n = 5, 6. Le tableau cite la ligne du script (rejouable)
  et renvoie au log pour les durées, sans prétendre que l'un produit l'autre.

## 5. Note de plafond

**Ce tableau mesure des durées, pas une portée.** Rejouer une commande reproduit
un chiffre exact ; cela ne dit pas que le chiffre mord sur la cellule. La
question à poser avant d'ajouter une ligne ici est celle de
[`echelle_instrument.md`](echelle_instrument.md) : *à quelle échelle le phénomène
visé commence-t-il, et est-elle sous le plafond de l'instrument ?*

Les deux écarts déjà chiffrés par le dépôt :

| Ligne | Échelle du phénomène | Plafond de l'instrument | Écart |
|---|---|---|---|
| **14** | borne symétrique KV **vide pour tout n ≤ 40**, premier contenu à **n = 41**, croisement prouvé sym/asym à **n ≈ 4050** | MILP torique certifié **n ≤ 7** ; CVP du fil AS **n ≤ 8** | **~500× en n** |
| **7** | seuil Beigel-Tarui utile : dépasser 2^{(log S)^{O(1)}}, soit **≈ 1,9 × 10¹³** à n = 100 — chiffre obtenu en instanciant O(1) := 2 et S := n (2^{(log₂ 100)²}), instanciation du rédacteur et non du théorème, minorante puisque S ≥ n | famille mesurée plafonnée à **O_g(k²)**, soit **2 550** à n = 100 ; W = 30 fermé à n = 10 en 3 h 20 | **~10 ordres de grandeur** |

Conséquence opératoire, à appliquer avant toute campagne : **exiger que
l'instrument voie un effet déjà prouvé de même nature dans son domaine
accessible.** Le mode `calib` de `tour_27_s2_espace_entier_cpsat.py` est la
forme aboutie de ce contrôle — il rejoue le moteur complet, cassage de symétrie
compris, sur les deux instances (k = 3, k = 4) où la réponse est connue
indépendamment. À l'inverse, `task_atlas005_delta_controle.py` est le contrôle
qui **échoue** : le gain asymétrique *prouvé* par Krishan-Vishwanathan est
invisible à n ≤ 7, donc les égalités MAJ à ces tailles ne discriminaient rien.
Les deux scripts sont au tableau pour cette raison : **un témoin de contrôle vaut
un témoin de résultat.**

## 6. Ce que ce fichier ne revendique pas

Aucune revendication de nouveauté n'est faite ici, et aucun folklore-check n'y
était donc requis. Les étiquettes `PROUVÉ` de la colonne Statut portent sur des
théorèmes **du dépôt**, dont l'antériorité est traitée là où ils sont énoncés
(cellules de [`matrice_barrieres.md`](matrice_barrieres.md), fiches
`tasks/done/`, audits `bib/`) — pas ici.