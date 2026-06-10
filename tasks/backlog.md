# Backlog des tâches atomiques

> Nouveau mode opératoire post-Tour 25 (validé utilisateur, 2026-06-09).
> Une session = une tâche. L'output de chaque tâche est spécifié AVANT exécution.
> Règles anti-esquive : voir CLAUDE.md §8. Taxonomie des types : voir bas de fichier.
>
> Workflow : sélectionner une tâche → la déplacer dans `active/` → exécuter →
> livrer l'output exact → validation utilisateur → `done/` (ou `failed/` avec
> diagnostic honnête) → commit + push après validation.

## Phase 1 — Solde des fils ouverts

| ID | Type | Tâche | Output | Statut |
|---|---|---|---|---|
| F-001 | F | Mesurer la **weight L1** (vs magnitude L∞) des PTF pour fonctions TC⁰ d=2 \ d=1 : EXACT_k (n=4,5,6) et IP (n=4,6,8), avec sanity checks MAJ/PARITY. Question cible de la prescription Tour 24 : existe-t-il f ∈ TC⁰ d=2 \ d=1 à weight polynomiale ? | `data/weight_tc0_d2.csv` + `checks/task_f001_weight_tc0_d2.py` + `tasks/done/F-001.md` | ✅ **done** (2026-06-09) — réponse : OUI (EXACT_k, O(n²) structurel) mais IP échappe (640 à n=8) → poly-weight ⊊ TC⁰ d=2 |
| F-002 | F | *(candidate, issue de F-001)* Tester l'observation `min_D W(IP_{2k}, D) = (3^k−1)/2 = DNF_min(IP_{2k})` au point suivant k=5 (n=10 : 1024 contraintes, prédiction 121) et chercher la construction explicite qui réalise cette weight. | `data/weight_ip_k5.csv` + verdict | ✅ **done** (2026-06-09) — **CONFIRMÉE et prouvée optimale** (CBC, 2.8 s) : 121 = (3^5−1)/2. Observation O-F002 à 4 points (4, 13, 40, 121). Profil : le min exige le degré plein (153 à D=9, 249 à D=8). Voir `tasks/done/F-002.md`. |
| F-004 | F | *(candidate, issue de F-002)* Extraire les solutions L1-optimales de l'ILP à k=2, 3 et analyser leur structure (support, signes, lien aux implicants premiers) — chemin vers la preuve structurelle de O-F002. Si prouvée : théorème de correspondance weight-PTF ↔ DNF_min, à intégrer à la note L18. | `data/optimal_ptf_structure.csv` + analyse | ✅ **done** (2026-06-09) — **T-F004 prouvé** : la borne sup `W ≤ (3^k−1)/2` est un théorème (polynôme multilinéaire exact, preuve 3 lignes, tout k). L'optimum ILP à k=2,3 EST p* (support apparié, coefficients (−1)^{|S|+1}2^{|S|−1}). Reste la borne inf (ouverte, prouvée k≤5 par ILP). Voir `tasks/done/F-004.md`. |
| F-005 | F | *(candidate, issue de F-004)* Extraire les **certificats duaux** LP de l'optimalité à k=2,3,4 (CBC les a prouvés), chercher leur structure (symétries d'IP, valeurs par orbite), tenter la construction générale → prouverait `W ≥ (3^k−1)/2` pour tout k et clôturerait O-F002 en théorème complet. Vérifier si optimum LP réel = optimum ILP. | `data/dual_certificates.csv` + analyse | ✅ **done** (2026-06-09) — **LP réels = (3^k−1)/2 à k=2..5** : borne valide sur ℝ. Duaux symétrisés vérifiés indépendamment (max\|μ\|=1.000000). Face duale dégénérée (toutes contraintes d'entrée serrées car p*=IP exactement) → cible structurelle exacte identifiée : problème (P) — mesure symétrique à moments appariés (−1)^{s+1}, autres moments dans [−1,1]. Voir `tasks/done/F-005.md`. |
| F-006 | F | *(candidate, issue de F-005)* Résoudre le **LP dual réduit aux orbites** (O(k²) variables, testable jusqu'à k≈20) avec sélection d'un sommet canonique (zéros observés imposés : v(0,0,·)=v(0,1,·)=0, v(k,0,0)=1), chercher la forme close de u(a,b,c)/v(a,b,c), prouver (P) par identités binomiales → **clôturerait O-F002 en théorème complet**. | `data/orbit_dual.csv` + forme close ou échec honnête | ✅ **done** (2026-06-09) — **THÉORÈME T-F006 DÉMONTRÉ** : `W_L1(IP_{2k}) = (3^k−1)/2 = DNF_min(IP_{2k})` sur ℝ, tout k. Forme close trouvée à k=2,3,4 (sommets propres, support diagonal b=0) : certificat `w(x,x) = (−1)^{\|x\|+1}2^{k−\|x\|}`, `w(0)= −(2^k−2)` — tous moments = ±1, preuve 1 page par dualité faible. Vérifié en arithmétique exacte k=1..14 + force brute k≤4. Nouveauté inconnue (folklore-check à étendre). Voir `tasks/done/F-006.md`. |
| L18-STATUS | A | Trancher le statut bibliographique de L18 (`DNF_min(IP_{2n}) = (3^n−1)/2`, Tour 18) : folklore obscur ou non-recensé ? Recherche systématique (DNF complexity of bent functions, inner product, Quine-McCluskey appliqué à IP). | `bib/l18_status.md` (verdict : référence trouvée OU « non trouvé après recherche de X sources listées ») | ✅ **done** (2026-06-09) — verdict : **NON RECENSÉ** après 10+ sources dont Jukna (587 p. greppées) et la lignée depth-3 2021-2026. Réserves : école russe Yablonskii + 2 sources Sasao-Butler inaccessibles (403). Plus proche parent : FGT22 (3^{n/2} côté 2-CNF). Candidat note courte. |
| L18-NOTE | C | *(candidate, débloquée par L18-STATUS)* Vérifier les 2 sources Sasao-Butler inaccessibles (Fast Method MSOP decomposable ; tutoriel crypto DTIC), puis si toujours non recensé, rédiger une note courte (énoncé + preuve Tour 18 + observation 3^{n/2} transverse + lien FGT22). | `notes/dnf_min_ip.md` (brouillon de note) | ✅ **done** (2026-06-09) — 2 sources obtenues et greppées : formule ABSENTE des deux (ASP-DAC'01 = AND/OR seulement, XOR hors cadre ; tutoriel DTIC = angle ANF). Réserves Sasao-Butler levées dans `bib/l18_status.md`. Brouillon de note rédigé. Reste avant soumission : relecture experte + vérification école russe. |

## Phase 2 — Construction de l'Atlas (audits biblio + matrice barrières)

### Audits bibliographiques (type A) — combler le déficit (q) qui a tué Tours 24-25

| ID | Paper | Output | Statut |
|---|---|---|---|
| A-001 | Williams 2011, *Nonuniform ACC circuit lower bounds* (JACM 2014) | `bib/williams_2011.md` | ✅ **done** (2026-06-09) — texte intégral CCC'11 greppé. Pièce maîtresse extraite verbatim : le « pourquoi » du franchissement des 3 barrières (diagonalisation pour RR + oracle d'Aaronson NEXP^A ⊂ ACC^A pour rel./alg.). Confirme Tour 23(d) : Lemma 4.1 = SYM+ (fonction symétrique de ANDs), pas PTF. |
| A-002 | Beigel-Tarui 1994, *On ACC* | `bib/beigel_tarui_1994.md` | ✅ **done** (2026-06-09) — source primaire (PS bitmap 1995) illisible ; énoncés exacts via Springer + Buss 2017 (re-preuve, 32 p. greppées). Théorème 2 verbatim : ACC taille S → profondeur 2 SYM∘AND, taille 2^{(log S)^{O(1)}}, fan-in polylog, coefficients ℤ magnitude quasi-poly. Cellule Atlas « Williams × TC⁰ » : 3 pièces réunies. |
| A-003 | Tardos 1988, *The gap between monotone and non-monotone circuit complexity is exponential* | `bib/tardos_1988.md` | ✅ **done** (2026-06-09) — texte intégral lu (2 p., scan Cornell). Mécanisme exact extrait : sandwich ω ≤ θ̄ ≤ χ + GLS/ellipsoïde + monotonisation par e(X). Divergence de millésime notée (scan : 7(4) 1987 ; Springer : 8, 1988). Cellule Atlas « monotone/tropical × Tardos » fermée avec témoin. |
| A-004 | Razborov 1987 + Smolensky 1987 (méthode polynomiale modulaire) | `bib/razborov_smolensky_1987.md` | ✅ **done** (2026-06-09) — via Goldreich 2023 (exposition dédiée, 21 p. greppées). Théorème exact : MAJ et MOD_q requièrent exp(Ω(n^{1/2d})) en AC⁰[p], p premier. Frontière verbatim : « we do not know a proof that AC⁰[6] cannot compute Majority » — ouverte 1987→2026. Cellule Atlas « poly modulaire × composite » fermée. |
| A-005 | Cai-Fürer-Immerman 1992 + Atserias-Bulatov-Dawar 2007 (CFI et extension CSP affine) | `bib/cfi_abd.md` | ✅ **done** (2026-06-09) — ABD lu en intégral ; CFI via DRR 2008 (33 p. greppées). Mécanisme de parité globale extrait verbatim (Definition 3) — l'invariant manquant au Tour 25. Cellules Atlas : « descriptive × FPC » fermée (FPC ⊊ P), « descriptive × CPT » ouverte (CPT distingue CFI, DRR 2008). |
| A-006 | Baker-Gill-Solovay 1975 (relativisation, énoncé exact des deux oracles) | `bib/bgs_1975.md` | ✅ **done** (2026-06-09) — via notes Katz UMD (2 p. intégrales, preuves complètes). Oracle A = PSPACE-complet (effondrement), oracle B = diagonalisation paresseuse sur L_B. Test opérationnel Atlas : l'argument survit-il à un oracle arbitraire ? Certificat moderne d'évitement = oracle d'Aaronson (A-001). |
| A-007 | Razborov-Rudich 1997 (preuves naturelles : définitions exactes de constructivité et largeness) | `bib/razborov_rudich_1997.md` | ✅ **done** (2026-06-09) — texte extrait du PS de la page Razborov (26 p.). Définitions verbatim (constructivity = P en la table, largeness ≥ 2^{−O(n)}), théorème principal (casse les PRG 2^{n^ε}), et **l'échappatoire explicite** : « a counting argument is presumably not a natural argument » — la sortie de Williams désignée par la barrière elle-même. 3 sorties documentées pour l'Atlas. |
| A-008 | Aaronson-Wigderson 2008 (algébrisation : définition exacte des oracles algébriques) | `bib/aaronson_wigderson_2008.md` | ✅ **done** (2026-06-09) — texte intégral (50 p.) greppé. Définition asymétrique exacte extraite (souvent mal citée : un seul côté reçoit Ã). Témoin : A PSPACE-complet + Ã multilinéaire → NP^Ã = P^A. Note interne du papier : les bornes small-depth (FSS/RS) NE SONT PAS couvertes par l'analyse. **Les 8 audits A-001..A-008 sont complets.** |

### Cellules critiques de la matrice (type D) — chaque cellule = verdict + témoin + référence

| ID | Cellule | Output | Statut |
|---|---|---|---|
| D-001 | Méthode Williams (algorithmic method) vs Razborov-Rudich : l'algorithme CAPP est-il « naturel » ? | `barriers/williams_vs_rr.md` | ✅ **done** (2026-06-09) — FRANCHISSEMENT par double sortie (diagonalisation = pas une propriété de tables ; ACC sans PRF). Réserve : argumenté fortement, pas démontré formellement (contrairement à rel./alg.). |
| D-002 | GCT vs algébrisation Aaronson-Wigderson | `barriers/gct_vs_aw.md` | ✅ **done** (2026-06-09) — SANS OBJET structurel pour AW (pas d'oracle, symétries explicites) mais présumé, non démontré. La vraie barrière de GCT est INTERNE : BIP 2019 (verbatim arXiv) tue les occurrence obstructions ; multiplicity obstructions ouvertes sans technique. |
| D-003 | CFI / CPT vs Razborov-Rudich | `barriers/cfi_vs_rr.md` | ✅ **done** (2026-06-09) — SANS OBJET pour FPC (pas une borne de circuit) ; mais l'immunité mesure la distance à P vs NP (les deux côtés dans P). L'immunité ne se transmet pas au programme complet (CPT ⊊ P ferait réapparaître RR). |
| D-004 | Hardness magnification vs barrière de localité (CHOPRS 2020) | `barriers/magnif_vs_locality.md` | ✅ **done** (2026-06-09) — texte intégral CHOPRS (52 p.) greppé. Définition exacte extraite : les théorèmes de magnification produisent inconditionnellement des circuits-oracle small fan-in pour Q ; toutes les techniques connues « localisent » → FERMÉE pour adaptations directes. Réfute l'Anti-Checker Hypothesis. |

### Assemblage

| ID | Tâche | Output | Statut |
|---|---|---|---|
| ATLAS-001 | Assembler la matrice barrières × approches : lignes = ~10 familles d'approches rencontrées aux Tours 1-25 + littérature, colonnes = 4 barrières (BGS, RR, AW, Tardos), chaque cellule = verdict + témoin + référence. Dépend de A-001..A-008 et D-001..D-004. | `atlas/matrice_barrieres.md` | ✅ **done** (2026-06-09) — matrice 12 lignes × 4 barrières + colonne « verrou réel ». 3 lectures : (1) seule la ligne Williams franchit tout, (2) les barrières classiques ne sont plus le front — chaque programme vivant a sa barrière interne, (3) les 25 tours se classent sans reste. 5 zones génératrices de cibles identifiées pour la règle d'ouverture Tour 26+. |

## Stratégie 2026-06 (validée) — 3 pistes

> **A — Fabrique à notes courtes** : pipeline répétable « mesure exacte → folklore-check → note si non recensé ». Candidats : F-002, fonctions bent au-delà d'IP.
> **B — Atlas exécutable** : répliquer les résultats-clés en code (B-001 Håstad ✅, B-002 Smolensky, B-005 BBR mod 6 ✅).
> **C — Boucle adverse gelée** sauf zones 1-2 de l'Atlas, via F-003 (SYM∘AND ✅ corrigée) et mesures mod 6.
> Cadence : alterner A et B ; C gelée tant que F-003 n'a pas parlé. Plafond réaliste assumé : notes IPL + atlas de référence.

| ID | Type | Tâche | Output | Statut |
|---|---|---|---|---|
| B-001 | B | Répliquer le **Switching Lemma de Håstad** : Pr[DTdepth(f\|ρ) ≥ s] ≤ (5pk)^s sur k-DNF aléatoires + TRIBES, profondeur DT exacte, 800k restrictions. | `checks/repli_hastad_switching.py` + tableau | ✅ **done** (2026-06-10) — borne respectée sur 4 configs. Tribes : décroissance géométrique visible, taux ≈ 1.3·pk (vs constante 5 de la borne). DNF aléatoires : borne très lâche. Voir `tasks/done/B-001.md`. |
| B-002 | B | Répliquer l'**approximation de Smolensky** : polynômes probabilistes bas degré sur F₃ pour MOD₂, mesurer l'erreur d'approximation empirique vs théorie à n=6..12. | `checks/repli_smolensky.py` + tableau | ✅ **done** (2026-06-10) — Pas 1 : erreur OR suit (1/3)^ℓ fidèlement. Pas 2 : accord max EXACT degré-d/PARITY par énumération du code (jusqu'à 3^16 mots) ≤ borne de comptage partout, serrée à d=2 ; fraction → 1/2. Bonus : à d=1, accord max = somme des 2 couches binomiales centrales (4 points). **Les 3 moteurs de la lignée AC⁰/ACC⁰ sont répliqués** (B-001, B-002, B-005). Voir `tasks/done/B-002.md`. |

## Piste A/C — mesures en cours

| ID | Type | Tâche | Output | Statut |
|---|---|---|---|---|
| F-003 | F | **(zone 1 de l'Atlas)** Mesurer par ILP/SAT la taille minimale d'une représentation **SYM∘AND exacte** (format Beigel-Tarui : fonction symétrique d'un multiset de ANDs) d'IP à n=4, 6, 8. Quantifie le verrou Williams→TC⁰ dans le bon format (F-001 le mesurait côté PTF). | `data/symand_ip.csv` + script + verdict | ✅ **done en correction de cadrage** (2026-06-09) — IP est **trivial** en SYM∘AND : = PARITY_k∘AND₂, poids k, prouvé optimal par ILP (k=2,3). Le cadrage de la tâche était erroné : IP témoigne du verrou en weight **PTF** (T-F006), pas en SYM∘AND ; les objets-frontière de ce format sont les **THR∘THR** à poids. Atlas ligne 7 précisée. Voir `tasks/done/F-003.md`. |
| F-003′ | F | *(reformulation de F-003)* Mesurer le poids SYM∘AND minimal de petites fonctions **THR∘THR à poids** (n = 4..6) — les vrais objets-frontière de l'extension Williams→TC⁰. Grand poids dès n=6 = quantification du mur ; petit poids partout = indice (faible) que la transformation existe. | `data/symand_thrthr.csv` + verdict | ✅ **done** (2026-06-09) — aucun mur visible à n≤6 (XOR(THR3,THR3) = 6, OR = 4, tous Optimal). **Défaut d'instances auto-signalé** : les seuils 2-var (2,1,t=2) dégénèrent en dictateurs — 4 instances sur 7 étaient triviales. 3e leçon « nommer/valider ce qu'on mesure ». Poursuite dépriorisée (exige n≥10 + SAT dédié). Voir `tasks/done/F-003p.md`. |
| B-005 | B | **(zone 2 de l'Atlas)** Répliquer la surprise Barrington-Beigel-Rudich : OR_n admet des représentations polynomiales de degré O(√n) **mod 6** (impossible mod premier). Mesurer les degrés exacts mod 2, 3, 6 à n = 4..12. | `checks/repli_bbr_mod6.py` + tableau | ✅ **done** (2026-06-09) — phénomène répliqué spectaculairement (n=144 : mod 6 → degré 9 ; n=18 : mod 2 → 18, mod 3 → 9, **mod 6 → 3**). Mécanisme 2^a·3^b visible mais pas exact (d=4 dès n=30, prédit 36) — l'écart Ω(log n)–O(√n) ouvert depuis 1994 est *visible dans les données*. Caveat symétrique documenté. Voir `tasks/done/B-005.md`. |
| B-005-OBS | A | *(candidate, issue de B-005)* La table exacte des degrés faibles symétriques de OR mod 6 (1,1,1,1,1,2,2,2,3,…) ne semble pas tabulée (BBR/TB donnent l'asymptotique). Folklore-check puis note courte ou soumission OEIS. | verdict + éventuelle note | pending |

## 🎯 Fil actif — F-011 : vers un théorème sur le front composite (zone 2)

| ID | Type | Tâche | Output | Statut |
|---|---|---|---|---|
| F-011-e1 | F | Cerner la loi de `deg₆^sym(MAJ_n)` (données n=1..44, anomalies, mécanisme) | conjecture | ✅ **done** (2026-06-10) — **C-F011 formulée** : L1(t) = plus petite puissance de 2 ou 3 ≥ t, sauf si q=2^a, n ≥ 2q et C(2q,q) ≡ 0 mod 3 (mécanisme vérifié 3/3 ; 40/42 points). **Prédiction falsifiable : deg₆^sym(MAJ_32) = 27.** Voir `tasks/done/F-011-etape1.md`. |
| F-011-e2 | F | Tester la prédiction MAJ_32 = 27 (caps élargis) + sonder les autres puissances critiques (t = 32 : C(64,32) mod 3 ?) | verdict prédiction | ✅ **done** (2026-06-10) — **PRÉDICTION CONFIRMÉE** : infaisable à d=16..26 (exhaustif), faisable à 27. Contrôle n=31→16 ✓, n=33..36→27 ✓. **C-F011 : 47/47** dont une prédiction a priori. Révélation structurelle : aux d=16..25 les noyaux sont de dim 1 — c'est le **rang des matrices binomiales sous le seuil** qui commande, cible précise pour la preuve. Voir `tasks/done/F-011-etape2.md`. |
| F-011-e3 | F | **Prouver C-F011** : borne sup par constructions e_q + corrections noyau ; borne inf par infaisabilité des combinaisons (Lucas, pipeline T-F006 sur les certificats). Si succès : 1re borne inférieure du dépôt sur le front composite (classe symétrique). | théorème ou échec honnête | ✅ **done partiel — 4 THÉORÈMES PROUVÉS** (2026-06-10) : Lemme 1 (noyau = span{e_i, t≤i≤d}, Mahler) ; **T-F011a** (forme close EXACTE de deg₂^sym(THR_{t,n}), toute la famille, via télescope Pascal + Lucas) ; **T-F011b** (lemme d'infaisabilité mod 6) + anomalies prouvées (≥3, ≥9, ≥27) ; **deg₆^sym(MAJ_32) = 27 prouvé** (certificat exact : e₁₆+e₁₈+e₂₅+e₂₇ mod 3 !). Reste conjectural : loi mod 3 exacte + loi complète C-F011. Voir `tasks/done/F-011-etape3.md`. |
| F-011-e4 | F | *(suite)* Loi mod 3 exacte (les valeurs 2·3^b : 6, 18 — analogue du télescope sur F₃ avec patterns {1,2}), puis loi complète C-F011, puis **lever la restriction symétrique** (vers le modèle général — chaque marche élargit vers les circuits). | théorèmes ou échec honnête | ✅ **done en réfutation** (2026-06-10) — la conjecture unifiante C-F011d (critère de blocage mono-poids exact) est **réfutée** : 150 contre-exemples / 678 cellules, tous en fenêtre longue (n ≫ 2t). Théorèmes de l'étape 3 intacts (solveur re-confirme T-F011a) ; C-F011 (régime MAJ, n ≈ 2t) non touchée. Enseignement : l'obstruction manquante est **collective/globale** (sur F₂ : l'unicité de l'échelon). Voir `tasks/done/F-011-etape4.md`. |
| F-011-e5 | F | *(candidate)* Caractériser l'obstruction collective mod 3 en fenêtre longue : extraire les patterns ±1 réalisables vs interdits aux cellules en écart, chercher l'invariant séparateur (analogue F₃ du télescope). | invariant ou échec honnête | ✅ **done** (2026-06-10) — **Lemme 2 prouvé + validé 126/126** : deg ≤ d ⟺ Δ^{d+1}g ≡ 0 (fenêtre glissante, décision par automate). **Loi C-F011e confirmée 26/26** : deg₃(OR_n) = max(blocage, n − 3^⌊log₃n⌋) — le terme collectif a une forme close. Outil de preuve identifié : Δ^{3^b} = S^{3^b} − id (Lucas) → degré < 3^b ⟺ périodicité. Voir `tasks/done/F-011-etape5.md`. |
| F-011-e6 | F | Prouver C-F011e via la factorisation `Δ^{3^b+r} = (S^{3^b} − id)∘Δ^r` : (1) re-preuve structurelle du blocage aux puissances (périodicité vs préfixe de zéros) ; (2) le terme collectif n − 3^b par comptage des périodes. | théorème ou échec honnête | ✅ **done partiel** (2026-06-10) — **T-F011c prouvé** (deg₃ ≥ 3^b dès que 3^b ≤ n−t+1, périodicité vs préfixe, vérifié 138/138) + **Lemme 3 prouvé** (descente : deg(g(·+P)−g) ≤ deg(g)−P, vérifié 2000/2000). Le fil monte à **7 théorèmes**. La rampe exacte n−3^b reste conjecturale : le problème réduit perd la structure ±1. Voir `tasks/done/F-011-etape6.md`. |
| F-011-e7 | F | *(candidate)* La borne fine de la rampe : caractériser le problème réduit (G à valeurs F₃, G(0) ≠ 0, ladder de descentes avec contrainte ±1 à chaque étage) — ou attaquer par l'automate (périodicité éventuelle des langages reconnus, Lemme 2). | théorème ou échec honnête | ✅ **done — THÉORÈME E PROUVÉ** (2026-06-10) : la rampe `deg₃^sym(OR_n) ≥ n−3^b` tombe par descente → périodicité → **paires interdites** (G ≡ 0 sur [1,n−2P], G(0) ≠ 0) → interpolation de Mahler. Borne inf de la loi OR mod 3 **entièrement prouvée** (max(P, n−P), exacte sur 26/26). Le fil monte à **8 théorèmes**. Gabarit réutilisable pour la loi MAJ. Voir `tasks/done/F-011-etape7.md`. |
| F-011-e8 | F | *(candidate)* (a) Borne sup générale de la loi OR mod 3 (constructions pour tout n) ; (b) appliquer le gabarit descente→paires→interpolation à la loi MAJ mod 6 (C-F011) et au cas t général. | théorèmes ou échec honnête | pending |
| F-011-SYNTH | — | Synthèse du fil : note structurée des 7 théorèmes + 2 conjectures + réfutation + questions ouvertes | `notes/front_composite.md` | ✅ **done** (2026-06-10) — note de référence du fil rédigée (théorèmes A-D + Lemmes 1-3 avec preuves, statut épistémique explicite, folklore-check dédié requis avant diffusion). |

## ⚠ Recadrage 2026-06-10 (utilisateur) : rester sur l'objectif P vs NP

> La piste A (notes de combinatoire booléenne) est **gelée** au-delà de la
> finalisation L18/T-F006 (attente externe Göös uniquement). Le travail
> actif = **les zones de l'Atlas**, seuls fronts P vs NP. F-008 gelée.

| ID | Type | Tâche | Output | Statut |
|---|---|---|---|---|
| F-009 | F | **(zone 2)** Degrés faibles symétriques de **MAJORITY mod 2/3/6** — la fonction de la conjecture ouverte de 1987. La magie composite opère-t-elle sur MAJ comme sur OR ? | `checks/task_f009_maj_mod6.py` + tableau | ✅ **done** (2026-06-10) — **NON** : MAJ mod 6 croît linéairement (16 à n=20-30 vs OR = 3-4), suit min(mod 2, mod 3) avec économies marginales. Mécanisme visible : ⌈n/2⌉ zéros forcés écrasent le noyau binomial (OR n'en force qu'un). Cohérent avec la conjecture MAJ ∉ AC⁰[6] au niveau polynomial faible. Voir `tasks/done/F-009.md`. |
| F-010 | F | *(candidate, zone 2)* Transition THR_t mod 6 quand t croît de 1 (OR, avantage composite ~√n) à ⌈n/2⌉ (MAJ, avantage mort) : **où l'avantage composite meurt-il ?** Courbe deg₆(THR_t,n) en fonction de t. | tableau + transition | ✅ **done** (2026-06-10) — **il meurt dès t=2** : d₆ saute de 3 à 8-9 au 2e zéro forcé. Falaise, pas pente : l'avantage BBR est une propriété au couteau de la couverture pure (1 seul zéro). Poches secondaires ≤ 3 (ressac de Lucas). Bonus : non-monotonie en t (d₃ remonte de 9 à 18). Éclaire pourquoi le composite n'a jamais été converti en attaque type-seuil depuis 1994. Voir `tasks/done/F-010.md`. |
| B-006 | B | **(zone 1)** Répliquer l'algorithme de Williams en exécutable : évaluation rapide d'un SYM∘AND (programmation dynamique) battant la force brute 2^n sur instances jouets — le cœur opérationnel de la seule méthode ayant franchi les 3 barrières. | `checks/repli_williams_eval.py` + benchmark | ✅ **done** (2026-06-10) — transformée zêta : coût **plat** en t (0.15-0.19 s de 10³ à 10⁷ portes, n=20) vs brute linéaire (gain ×178 700 à 10M). Égalité bit à bit ≤ 30k, échantillon au-delà. SAT-par-lots : 6 196 témoins en 0.18 s vs ~9 h brute, témoin re-vérifié. Incident de protocole consigné (1re version : brute non bornée > timeout). Ligne 7 de l'Atlas documentée de bout en bout. Voir `tasks/done/B-006.md`. |

## Piste A — suite T-F006 (cartographie de la correspondance) — GELÉE (recadrage)

| ID | Type | Tâche | Output | Statut |
|---|---|---|---|---|
| F-007 | F | Cartographie exhaustive `W_L1` vs `DNF_min` à n=3, 4 (65 788 fonctions, HiGHS). Îlot ou continent pour T-F006 ? | `data/w_vs_dnfmin.csv` + stats | ✅ **done** (2026-06-10) — classe d'égalité **rare** (11.8 % → 0.9 %), inégalité dans les deux sens (générique : W > D à 99 %), égalité ⊅ essentialité (78 contre-ex à n=4), W < D expliqué par le terme constant (¬AND₃ : W=2 < 3), **W réelle peut être fractionnaire (4.5)**. Renforce la valeur de T-F006. Voir `tasks/done/F-007.md`. |
| F-008 | F | *(candidate, issue de F-007)* Caractériser structurellement la classe d'égalité `W_L1 = DNF_min` (575 fonctions à n=4 en CSV) — l'analogue du théorème d'essentialité L19 pour la correspondance T-F006. | caractérisation ou échec honnête | pending |

## Post-plan — finalisation note L18

| ID | Type | Tâche | Output | Statut |
|---|---|---|---|---|
| L18-CHECK | A | Check communautaire : (0) vérifier qu'aucune question existante sur cstheory.SE ne couvre le sujet ; (1) préparer la question prête à poster + le mail à Göös ; (2) **Tanguy poste** (action sous son identité) ; (3) consigner le résultat. | `notes/folklore_check_drafts.md` + journal §3 du fichier | 🔶 **étapes 0-1 done** (2026-06-09 : aucune question existante ; 2 textes prêts). **Étapes 2-3 : à la main de Tanguy.** |

## Phase 3 — Synthèse publique

| ID | Tâche | Output | Statut |
|---|---|---|---|
| SYNTH-001 | Réécrire le README autour de l'Atlas : « pourquoi P vs NP résiste, pièce par pièce, avec code exécutable ». Dépend de ATLAS-001. | `README.md` révisé | ✅ **done** (2026-06-09) — README réécrit : Atlas en livrable central, arborescence des pièces, récit des 2 phases (adverse → tâches atomiques), acquis avec statut honnête, règle de réouverture, avertissement renforcé. **LES 3 PHASES DU BACKLOG SONT COMPLÈTES.** |

---

## Taxonomie des types de tâches

| Type | Nature | Output générique |
|---|---|---|
| A | Audit bibliographique d'un paper précis | `bib/AUTEUR_ANNEE.md` — 7 sections obligatoires (réf. canonique, théorème exact, hypothèses, outils, ce qu'il NE prouve PAS, lien biblio §7, lien aux tours) |
| B | Replication numérique d'un théorème | `checks/repli_*.py` produisant un chiffre attendu |
| C | Extraction d'énoncé formel (Lean-style, sans code Lean) | `formal/THM.txt` |
| D | Test d'une approche contre UNE barrière | `barriers/X_vs_Y.md` — franchissement explicite OU échec explicite avec témoin, OU « indéterminé » honnête |
| E | Cartographie d'un sous-problème (DAG de dépendances) | `maps/QUESTION.md` |
| F | Mesure empirique d'une quantité | `data/*.csv` + script |
| G | Comparaison d'approches sur critères fixés | `compare/PROBLEM.md` |

**Hors taxonomie (interdit)** : « proposer une idée », « explorer une piste », « conjecturer une borne », « réfléchir à une approche ». Un Tour 26+ ne peut être ouvert que si une cellule de l'Atlas révèle un trou précis.

## Règle d'ouverture d'un futur Tour

Un Tour adverse (Proposeur/Réfuteur) ne peut être rouvert que si :
1. Une cellule de `atlas/matrice_barrieres.md` est marquée « zone vide » ou « sous-lemme non couvert », ET
2. La proposition cite la cellule exacte qui la motive, ET
3. Le calcul de vérification est livré AVANT la soumission (condition (j) stricte).
