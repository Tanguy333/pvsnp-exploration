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
| F-002 | F | *(candidate, issue de F-001)* Tester l'observation `min_D W(IP_{2k}, D) = (3^k−1)/2 = DNF_min(IP_{2k})` au point suivant k=5 (n=10 : 1024 contraintes, prédiction 121) et chercher la construction explicite qui réalise cette weight. | `data/weight_ip_k5.csv` + verdict | pending |
| L18-STATUS | A | Trancher le statut bibliographique de L18 (`DNF_min(IP_{2n}) = (3^n−1)/2`, Tour 18) : folklore obscur ou non-recensé ? Recherche systématique (DNF complexity of bent functions, inner product, Quine-McCluskey appliqué à IP). | `bib/l18_status.md` (verdict : référence trouvée OU « non trouvé après recherche de X sources listées ») | ✅ **done** (2026-06-09) — verdict : **NON RECENSÉ** après 10+ sources dont Jukna (587 p. greppées) et la lignée depth-3 2021-2026. Réserves : école russe Yablonskii + 2 sources Sasao-Butler inaccessibles (403). Plus proche parent : FGT22 (3^{n/2} côté 2-CNF). Candidat note courte. |
| L18-NOTE | C | *(candidate, débloquée par L18-STATUS)* Vérifier les 2 sources Sasao-Butler inaccessibles (Fast Method MSOP decomposable ; tutoriel crypto DTIC), puis si toujours non recensé, rédiger une note courte (énoncé + preuve Tour 18 + observation 3^{n/2} transverse + lien FGT22). | `notes/dnf_min_ip.md` (brouillon de note) | ✅ **done** (2026-06-09) — 2 sources obtenues et greppées : formule ABSENTE des deux (ASP-DAC'01 = AND/OR seulement, XOR hors cadre ; tutoriel DTIC = angle ANF). Réserves Sasao-Butler levées dans `bib/l18_status.md`. Brouillon de note rédigé. Reste avant soumission : relecture experte + vérification école russe. |

## Phase 2 — Construction de l'Atlas (audits biblio + matrice barrières)

### Audits bibliographiques (type A) — combler le déficit (q) qui a tué Tours 24-25

| ID | Paper | Output | Statut |
|---|---|---|---|
| A-001 | Williams 2011, *Nonuniform ACC circuit lower bounds* (JACM 2014) | `bib/williams_2011.md` | pending |
| A-002 | Beigel-Tarui 1994, *On ACC* | `bib/beigel_tarui_1994.md` | pending |
| A-003 | Tardos 1988, *The gap between monotone and non-monotone circuit complexity is exponential* | `bib/tardos_1988.md` | pending |
| A-004 | Razborov 1987 + Smolensky 1987 (méthode polynomiale modulaire) | `bib/razborov_smolensky_1987.md` | pending |
| A-005 | Cai-Fürer-Immerman 1992 + Atserias-Bulatov-Dawar 2007 (CFI et extension CSP affine) | `bib/cfi_abd.md` | pending |
| A-006 | Baker-Gill-Solovay 1975 (relativisation, énoncé exact des deux oracles) | `bib/bgs_1975.md` | pending |
| A-007 | Razborov-Rudich 1997 (preuves naturelles : définitions exactes de constructivité et largeness) | `bib/razborov_rudich_1997.md` | pending |
| A-008 | Aaronson-Wigderson 2008 (algébrisation : définition exacte des oracles algébriques) | `bib/aaronson_wigderson_2008.md` | pending |

### Cellules critiques de la matrice (type D) — chaque cellule = verdict + témoin + référence

| ID | Cellule | Output | Statut |
|---|---|---|---|
| D-001 | Méthode Williams (algorithmic method) vs Razborov-Rudich : l'algorithme CAPP est-il « naturel » ? | `barriers/williams_vs_rr.md` | pending |
| D-002 | GCT vs algébrisation Aaronson-Wigderson | `barriers/gct_vs_aw.md` | pending |
| D-003 | CFI / CPT vs Razborov-Rudich | `barriers/cfi_vs_rr.md` | pending |
| D-004 | Hardness magnification vs barrière de localité (CHOPRS 2020) | `barriers/magnif_vs_locality.md` | pending |

### Assemblage

| ID | Tâche | Output | Statut |
|---|---|---|---|
| ATLAS-001 | Assembler la matrice barrières × approches : lignes = ~10 familles d'approches rencontrées aux Tours 1-25 + littérature, colonnes = 4 barrières (BGS, RR, AW, Tardos), chaque cellule = verdict + témoin + référence. Dépend de A-001..A-008 et D-001..D-004. | `atlas/matrice_barrieres.md` | pending (bloqué par Phase 2) |

## Phase 3 — Synthèse publique

| ID | Tâche | Output | Statut |
|---|---|---|---|
| SYNTH-001 | Réécrire le README autour de l'Atlas : « pourquoi P vs NP résiste, pièce par pièce, avec code exécutable ». Dépend de ATLAS-001. | `README.md` révisé | pending (bloqué par ATLAS-001) |

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
