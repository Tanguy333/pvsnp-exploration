# Atlas des impasses — matrice barrières × approches pour P vs NP

> **Livrable central du dépôt** (tâche ATLAS-001, assemblée le 2026-06-09).
> Synthèse de 25 tours adverses (2026-05-23), 8 audits bibliographiques sur
> textes (`bib/`), 4 cellules barrières (`barriers/`), et 2 mesures
> exécutables (`checks/`, `data/`). Chaque cellule renvoie à sa pièce.
>
> **Lecture** : ✖ = l'approche est tuée par cette barrière (témoin connu) ;
> ✓ = barrière franchie ou évitée (avec le mécanisme) ; ◌ = sans objet
> structurel ; ⚠ = exposée/présumée ; — = non analysé. La colonne
> « Verrou réel » donne ce qui bloque *effectivement* l'approche aujourd'hui.

## La matrice

| # | Famille d'approches | Relativisation (BGS 1975) | Preuves naturelles (RR 1997) | Algébrisation (AW 2008) | Monotone (Tardos 1988) | **Verrou réel** |
|---|---|---|---|---|---|---|
| 1 | **Diagonalisation / simulation pures** | ✖ oracles A, B contradictoires ([bib/bgs_1975.md](../bib/bgs_1975.md)) | ◌ (pas une propriété — [A-007 §5.3](../bib/razborov_rudich_1997.md)) | ✖ a fortiori (AW généralise BGS) | ◌ | BGS : la technique est boîte-noire par essence |
| 2 | **Méta-complexité naïve (Kt, compressibilité)** | ✖ Kt relativise — Tour 1 ([tours/tour_01](../tours/tour_01_kolmogorov.md)) | — | ✖ | ◌ | Circularité conditionnel/inconditionnel + BGS |
| 3 | **Arithmétisation pure (sumcheck, IP=PSPACE)** | ✓ ne relativise pas | ◌ | ✖ tout ce qui arithmétise algébrise — témoin NP^Ã = P^A ([bib/aaronson_wigderson_2008.md](../bib/aaronson_wigderson_2008.md)) | ◌ | AW : il faut exploiter la structure au-delà du bas degré |
| 4 | **Méthode polynomiale modulaire (Razborov-Smolensky)** | ✓ combinatoire | ⚠ naturalise (exemple canonique RR — [bib/razborov_rudich_1997.md §4](../bib/razborov_rudich_1997.md)) | ◌ | ◌ | **Modules composés** : « AC⁰[6] vs Majority » ouvert depuis 1987 ([bib/razborov_smolensky_1987.md](../bib/razborov_smolensky_1987.md)) |
| 5 | **Bornes monotones / tropicales / min-plus** | ✓ | ◌ (RR vise le non-monotone) | ◌ | ✖ **témoin θ̄-perturbée ∈ P à complexité monotone exp(n^{1/6})** ([bib/tardos_1988.md](../bib/tardos_1988.md)) ; tropical = monotone arith. (Jerrum-Snir, [Tour 24](../tours/tour_24_tropical_refutee.md)) | Tardos : le gap est intrinsèque au modèle, pas à la dureté |
| 6 | **Combinatoire profondeur 2 / DNF-MIN (Tours 12-22)** | ✓ | ✓ propriétés non-larges (fonctions uniques) | ◌ | ◌ | **Sans portée** : AC⁰ d=2 ⊊ P connu depuis FSS 1981 ; 8/9 objets folklore ([cahier §3 audit](../cahier_de_bord.md)) ; seul L18 non recensé ([bib/l18_status.md](../bib/l18_status.md)) |
| 7 | **Méthode algorithmique (Williams 2011)** | ✓ **démontré** — oracle NEXP^A ⊂ ACC^A ([bib/williams_2011.md §6](../bib/williams_2011.md)) | ✓ double sortie ([barriers/williams_vs_rr.md](../barriers/williams_vs_rr.md)) | ✓ **démontré** (même oracle, version algébrique) | ◌ | **Extension** : aucun algorithme SAT non-trivial au-delà d'ACC⁰. Précision (F-003) : la transformation Beigel-Tarui manquante pour TC⁰ concerne les portes **THR à poids non bornés** (objets-frontière : THR∘THR) — IP est *trivial* en SYM∘AND (= PARITY∘AND₂, poids k, prouvé optimal) ; ce dont IP témoigne est la weight **PTF** exponentielle : 20→119→640, et exactement (3^k−1)/2 par T-F006 ([tasks/done/F-001.md](../tasks/done/F-001.md), [F-006](../tasks/done/F-006.md), [F-003](../tasks/done/F-003.md)) |
| 8 | **GCT (permanent vs déterminant)** | ◌ présumé (pas d'oracle) | ⚠ présumé franchi, non démontré | ◌ présumé ([barriers/gct_vs_aw.md](../barriers/gct_vs_aw.md)) | ◌ | **Barrière interne BIP 2019** : pas d'occurrence obstructions ; multiplicity obstructions sans technique connue |
| 9 | **Complexité descriptive (CFI / FPC / CPT)** | ◌ | ◌ pour FPC — mais l'immunité = distance à P vs NP ([barriers/cfi_vs_rr.md](../barriers/cfi_vs_rr.md)) | ◌ | ◌ | **Aucune technique pour CPT ⊊ P** (les CFI ne témoignent pas contre CPT — DRR 2008, [bib/cfi_abd.md](../bib/cfi_abd.md)) ; transposition à SAT fermée ([Tour 25](../tours/tour_25_cfi_sat_refute.md), q.15) |
| 10 | **Hardness magnification (MCSP/MKtP)** | — (réductions relativisantes) | ✓ par construction (refuter les propriétés naturelles EST la stratégie) | — | ◌ | **Barrière de localité** : toutes les techniques connues localisent ([barriers/magnif_vs_locality.md](../barriers/magnif_vs_locality.md), CHOPRS 2020) |
| 11 | **PTF / threshold polynomials (Tours 23, F-001)** | ✓ ILP fini | ✓ fonctions individuelles | ◌ | ◌ | Instrument de mesure, pas une approche de séparation ; poly-weight ⊊ TC⁰ d=2 strictement (EXACT_k vs IP, [data/weight_tc0_d2.csv](../data/weight_tc0_d2.csv)) |
| 12 | **Invariants topologiques/homologiques sémantiques (Tours 3, 6, 7)** | ✓ | ✖ invariants constructifs et larges (Tour 6, q.7) | ◌ | ✖ pour les variantes monotones (Tour 7, test OR_n q.8) | Non-invariance sous équivalence logique + effondrement sous sauts polynomiaux (q.1, q.2) |

## Les trois lectures de la matrice

### 1. Une seule ligne franchit les 4 colonnes : la ligne 7 (Williams)

Et son franchissement de relativisation + algébrisation est *démontré*
(oracle d'Aaronson), pas seulement argumenté. La raison structurelle, citée
du texte ([A-001](../bib/williams_2011.md)) : *« improvements over
exhaustive search necessarily exploit structure in instances that black-box
methods cannot see »*. Le coût : la borne ne descend pas sous NEXP, et
l'extension à TC⁰ exige un ingrédient algorithmique que personne n'a
(quantifié empiriquement par F-001 : la représentation à la Beigel-Tarui
n'existe pas pour TC⁰ d=2, IP en témoin).

### 2. Les barrières classiques ne sont plus le front

Les programmes vivants (lignes 7-10) ont tous, par construction, réglé leur
rapport aux 3 barrières classiques. Ce qui les bloque est **chaque fois une
barrière interne propre** : modules composés (ligne 4), algorithme SAT
manquant (ligne 7), BIP 2019 (ligne 8), absence de technique CPT (ligne 9),
localité (ligne 10). La méta-leçon : *toute stratégie assez précise pour
être exécutable engendre l'analyse de sa propre impossibilité*. Demander
« franchissez-vous les 3 barrières ? » est nécessaire mais très loin d'être
suffisant.

### 3. Les patterns d'échec du dépôt sont tous dans la matrice

Les 25 tours du dépôt se classent sans reste : Tours 1-2 (lignes 2-3),
Tour 3/6/7 (ligne 12), Tours 6-10 dérive (hors matrice — pas une approche
de P vs NP), Tours 12-22 (ligne 6), Tour 23 + F-001 (ligne 11), Tour 24
(ligne 5), Tour 25 (ligne 9). Aucun tour n'a travaillé les lignes 7, 8, 10
*avec une contribution technique* — ce sont les seules lignes où les
verrous réels sont des problèmes mathématiques ouverts identifiés plutôt
que des impossibilités démontrées.

## Zones génératrices de cibles (règle d'ouverture d'un Tour 26+, cf. CLAUDE.md §8)

Les seules cellules « ouvertes avec verrou identifié » — par ordre de
précision du verrou :

1. **Ligne 7, extension TC⁰** : trouver une représentation exacte
   évaluable-rapidement pour TC⁰ d=2 (le verrou est précis : F-001 + A-002
   montrent ce qui ne marche pas). Front de recherche mondial depuis 2011.
2. **Ligne 4, modules composés** : structure des polynômes mod 6 — front
   depuis 1987.
3. **Ligne 10, technique non-localisante** : une borne faible pour MCSP gap
   qui ne s'étende pas aux circuits-oracle small fan-in.
4. **Ligne 9, borne CPT** : au-delà du rang borné (DRR 2008).
5. **Ligne 8, multiplicity obstructions** : techniques de calcul de
   multiplicités au-delà de BIP 2019.

Aucune de ces cibles n'est à la portée d'un tour LLM + vérification
exécutable — ce sont des fronts de recherche. Le critère d'ouverture d'un
Tour 26+ doit donc être : *un sous-lemme vérifiable d'une de ces cinq
zones*, pas la zone elle-même.

## Inventaire des pièces

- **Audits sur textes** : `bib/bgs_1975.md`, `bib/razborov_rudich_1997.md`,
  `bib/aaronson_wigderson_2008.md`, `bib/tardos_1988.md`,
  `bib/razborov_smolensky_1987.md`, `bib/beigel_tarui_1994.md`,
  `bib/williams_2011.md`, `bib/cfi_abd.md`, `bib/l18_status.md`.
- **Cellules détaillées** : `barriers/williams_vs_rr.md`,
  `barriers/gct_vs_aw.md`, `barriers/cfi_vs_rr.md`,
  `barriers/magnif_vs_locality.md`.
- **Mesures exécutables** : `checks/task_f001_weight_tc0_d2.py` +
  `data/weight_tc0_d2.csv` (weight L1, TC⁰ d=2), ~30 scripts `checks/`
  des tours.
- **Archives des 25 tours** : `tours/tour_01_*.md` … `tours/tour_25_*.md`.
- **Journal complet** : `cahier_de_bord.md` (§2 pistes, §3 lemmes,
  §4 questions q.1-q.16, §7 bibliographie).
