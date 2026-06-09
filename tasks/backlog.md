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
| F-006 | F | *(candidate, issue de F-005)* Résoudre le **LP dual réduit aux orbites** (O(k²) variables, testable jusqu'à k≈20) avec sélection d'un sommet canonique (zéros observés imposés : v(0,0,·)=v(0,1,·)=0, v(k,0,0)=1), chercher la forme close de u(a,b,c)/v(a,b,c), prouver (P) par identités binomiales → **clôturerait O-F002 en théorème complet**. | `data/orbit_dual.csv` + forme close ou échec honnête | pending |
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
> **B — Atlas exécutable** : répliquer les résultats-clés en code (B-001 Håstad, B-002 Smolensky, B-005 BBR mod 6).
> **C — Boucle adverse gelée** sauf zones 1-2 de l'Atlas, via F-003 (SYM∘AND) et mesures mod 6.
> Cadence : alterner A et B ; C gelée tant que F-003 n'a pas parlé. Plafond réaliste assumé : notes IPL + atlas de référence.

## Piste A/C — mesures en cours

| ID | Type | Tâche | Output | Statut |
|---|---|---|---|---|
| F-003 | F | **(zone 1 de l'Atlas)** Mesurer par ILP/SAT la taille minimale d'une représentation **SYM∘AND exacte** (format Beigel-Tarui : fonction symétrique d'un multiset de ANDs) d'IP à n=4, 6, 8. Quantifie le verrou Williams→TC⁰ dans le bon format (F-001 le mesurait côté PTF). | `data/symand_ip.csv` + script + verdict | pending |
| B-005 | B | **(zone 2 de l'Atlas)** Répliquer la surprise Barrington-Beigel-Rudich : OR_n admet des représentations polynomiales de degré O(√n) **mod 6** (impossible mod premier). Mesurer les degrés exacts mod 2, 3, 6 à n = 4..12. | `checks/repli_bbr_mod6.py` + tableau | pending |

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
