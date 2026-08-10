# Instruction de candidature — « TFNP structurel (PLS, PPAD, CLS) » — SURVIT (sous conditions)

Date : 2026-08-09. Tâche : PR-004. Troisième candidature du générateur
(Proposeur : Qwen, prompt v3 — la première produite avec l'historique
§2 ter en main). Instruction par le Réfuteur (CLAUDE.md §5).

## 0. La candidature, fidèlement résumée

Famille : les problèmes de recherche TOTAUX (TFNP) et leur structure
fine — PPAD (parité d'un graphe implicite ; Nash complet), PLS
(potentiel décroissant ; optimum local), CLS = PPAD ∩ PLS (descente de
gradient complète — FGHS STOC 2021, inconditionnel), effondrements
2022 (EOPL = PLS ∩ PPAD, SOPL). Énoncé visé : FP ⊊ TFNP (concrètement
PPAD ⊄ FP ou PLS ⊄ FP). Chaîne EN DEUX FLÈCHES : PPAD ⊄ FP [OUVERTE]
⟹ TFNP ≠ FP [inclusion] ⟹ P ≠ NP [Megiddo-Papadimitriou 1991].
Honnêteté déclarée : TFNP ≠ FP est STRICTEMENT plus fort que P ≠ NP —
même statut que NP ⊄ P/poly (précédent de la moitié de la matrice).
Invariant central : la dureté ne peut pas venir de l'inexistence
(tout est total) — elle vient de la LONGUEUR du chemin implicite que
le principe d'existence force à parcourir. Trois étages : requêtes
(prouvé, boîte noire), structure inconditionnelle (effondrements),
crypto white-box (LWE/Fiat-Shamir ⟹ PPAD-dur) — le dernier est la
frontière. Sous-lemme à double calibration : minimax exact de
requêtes, Sperner-1D (⌈log₂ N⌉ attendu) contre Sperner-2D
(sur-logarithmique attendu).

## 1. Vérifications de la chaîne

La flèche 2 (TFNP ≠ FP ⟹ P ≠ NP, contraposée : P = NP ⟹ TFNP = FP)
est l'auto-réductibilité standard : avec un oracle de décision NP, la
solution d'un problème de recherche total à vérifieur polynomial se
construit bit à bit (« existe-t-il une solution prolongeant ce
préfixe ? »). Attribution Megiddo-Papadimitriou 1991 — plausible et
standard ; VERBATIM À CONFIRMER par l'audit fondateur (A-022). La
flèche 1 (inclusion) est triviale. La déclaration de force
(strictement plus fort, pas de réciproque connue) est EXACTE et
portée par la candidature elle-même — le précédent NP ⊄ P/poly est
recevable.

## 2. Contre-vérification exécutée (`checks/pr004_sperner_minimax.py`)

Implémentation INDÉPENDANTE du Réfuteur : minimax mémoïsé exact,
adversaire à domaines (bords bicolores, intérieur libre — toute
affectation respectant les domaines est une entrée Sperner valide,
l'adversaire est donc sans contrainte globale), gain = simplexe
entièrement interrogé trichrome (2D) / segment bicolore (1D).

**Résultats (2026-08-09, mesurés)** :

| instance | requêtes EXACTES | référence | verdict |
|---|---|---|---|
| 1D, N = 4 | 2 | ⌈log₂ 4⌉ = 2 | CONFORME |
| 1D, N = 8 | 3 | ⌈log₂ 8⌉ = 3 | CONFORME |
| 1D, N = 16 | 4 | ⌈log₂ 16⌉ = 4 | CONFORME (3 s) |
| 2D, k = 2 | **3** | log₂ 4 = 2.00 | au-dessus |
| 2D, k = 3 | **4** | log₂ 9 = 3.17 | au-dessus |
| 2D, k = 4 | **6** | log₂ 16 = 4.00 | au-dessus, écart croissant (3 s) |

La DOUBLE CALIBRATION passe intégralement : l'effondrement 1D valide
l'instrument (la dichotomie est optimale), la résistance 2D atteste le
mécanisme central à l'échelle atelier (3, 4, 6 — sur-logarithmique aux
trois points, sans extrapolation d'une « linéarité » sur 3 points).
Le compte de la candidature (~14 000 colorations à k = 4) est exact :
13 824. Antériorité : DÉCLARÉE D'AVANCE par la candidature
(asymptotiques connues, Hirsch-Papadimitriou-Vavasis 1989 ; les
valeurs exactes à petit k = réplication + mesure de constantes — la
table ci-dessus est ce livrable secondaire).

## 3. Positionnement et grille

| Champ | État |
|---|---|
| Énoncé, classes, chaîne | Conformes ; la chaîne la plus courte de la matrice (2 flèches), force déclarée honnêtement |
| Test de plafond | EXACT — vérifié par l'exécution même (13 824 colorations, 3 s) |
| Folklore-check | Le meilleur des trois candidatures : Papadimitriou 94, FGHS 21, GHJMPRT 22, CHKPRR 19/JKKZ 21 — les bonnes pièces ; ET l'antériorité du sous-lemme déclarée d'avance (leçon SRE intégrée) |
| Sous-lemme | Double calibration exécutée, DEUX régimes conformes — le format d'excellence du prompt v3, réalisé |
| Positionnement | Ligne 15 correctement analysée (équivalences boîte-noire ≠ séparation uniforme white-box) — MAIS **la ligne 16 (Avoid/APEPP) est ABSENTE de l'analyse** : Avoid est aussi une recherche totale (TFΣ₂, vérifieur coNP — distinct de TFNP, mais c'est la même hiérarchie de la recherche totale, et Korten y relie les bornes de circuits) ; la distinction tient probablement, à INSTRUIRE SUR TEXTES (A-022) |
| Barrières | Relativisation traitée DE FRONT comme verrou n° 1 (oracles dans les deux sens ; les bornes de requêtes prouvées ne concluent pas ; le candidat-mécanisme white-box est nommé et déclaré conditionnel) ; algébrisation signalée là où elle mord (Fiat-Shamir arithmétise — la leçon de la candidature n° 1, explicitement évitée) ; PN sans objet avec raison structurelle ; monotone sans objet |
| Régimes d'échec | AUCUN constitué ; l'aveu « la cible dépasse P ≠ NP » et la clause de surveillance du rattachement futur sont écrits PAR la candidature (règle 7 intériorisée) |

## 4. VERDICT : SURVIT (sous conditions) — recevable comme candidature de ligne 20

La meilleure candidature reçue : famille majeure absente de la
matrice, chaîne la plus courte, honnêteté épistémique complète,
sous-lemme exécuté conforme dans ses deux régimes, verrou réel nommé
par la candidature elle-même (« aucune technique inconditionnelle
white-box ; le boîte-noire relativise, le cryptographique est
conditionnel — l'exact analogue de l'algorithme SAT manquant de la
ligne 7 »).

**Conditions posées à la création de la ligne 20** (garde-fou
anti-auto-référence, précédents ATLAS-013/A-021) :

1. **Audit type A fondateur préalable (A-022 candidate)** : Megiddo-
   Papadimitriou 1991 (la flèche, verbatim) ; Papadimitriou 1994 (les
   classes par argument d'existence) ; FGHS STOC 2021/JACM (CLS =
   PPAD ∩ PLS) et les effondrements 2022 ; la route crypto (CHKPRR
   STOC 2019, JKKZ STOC 2021 — hypothèses exactes) ; les
   correspondances TFNP ↔ systèmes de preuves (pour trancher la
   frontière ligne 15) ; la relation à la ligne 16 (Avoid/APEPP,
   TFΣ₂ vs TFNP — l'angle manqué par la candidature) ; le paysage des
   oracles (les deux sens, attributions exactes).
2. Le verrou de la ligne s'écrira depuis l'audit ; les trois manques
   listés par la candidature y entrent tels quels.
3. La table exacte de Sperner (§2) entre dans `data/` comme
   réplication + constantes, étiquetée comme la candidature l'a
   elle-même demandé.

## 5. Pièces

`checks/pr004_sperner_minimax.py` (implémentation indépendante,
sortie intégrale dans le journal) ; fiche : `tasks/done/PR-004.md`.
