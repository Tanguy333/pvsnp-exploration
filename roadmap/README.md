# `roadmap/` — Squelette procédural de preuve P vs NP

Ce dossier contient **18 prompts indépendants** prêts à coller dans une nouvelle
session Claude, organisés en 4 sections selon les approches connues du problème
P vs NP :

* **A — P ≠ NP via bornes inférieures de circuit** (approche dominante, 5 étapes).
* **B — P = NP via algorithme** (approche minoritaire, 4 étapes).
* **C — Approches indirectes** (méta-complexité, descriptive, GCT, Williams, 4 étapes).
* **D — Inventions à produire** (techniques manquantes pour franchir les barrières, 5 étapes).

## Structure

```
roadmap/
├── README.md                    ← ce fichier
├── A_P_neq_NP/
│   ├── A1_choose_target.md
│   ├── A2_lower_bound.md
│   ├── A3_test_barriers.md
│   ├── A4_deduce_P_neq_NP.md
│   └── A5_verification.md
├── B_P_eq_NP/
│   ├── B1_algorithm.md
│   ├── B2_correctness.md
│   ├── B3_complexity.md
│   └── B4_deduce_P_eq_NP.md
├── C_indirect/
│   ├── C1_meta_complexity.md
│   ├── C2_descriptive_complexity.md
│   ├── C3_GCT.md
│   └── C4_Williams_extension.md
└── D_inventions/
    ├── D1_non_relativizing.md
    ├── D2_non_natural.md
    ├── D3_non_algebrizing.md
    ├── D4_logical_equivalence_invariant.md
    └── D5_monotone_to_general.md
```

## Format de chaque fichier

Chaque prompt suit le canevas :

1. **Objectif formel** — ce que l'étape doit établir mathématiquement.
2. **Statut actuel (2026)** — état du front de recherche.
3. **Prompt pour Claude** — le texte à copier-coller dans une session neuve.
4. **Critères d'acceptation** — ce qui compte comme succès, même partiel.
5. **Modes d'échec attendus** — ce qu'on apprend si ça échoue.
6. **Références à embarquer** — bibliographie minimale pour la session.
7. **Conditions du cahier en vigueur** — quelles conditions (a)-(r) doivent
   être honorées.

## Usage

Pour chaque étape :

1. Copier le bloc « Prompt pour Claude » dans une nouvelle session
   (idéalement avec sous-agent dédié).
2. Joindre le cahier de bord en contexte.
3. Joindre les références §7 du cahier.
4. Lancer la session.
5. Si la session conclut « gap structurel » : noter le gap dans le cahier
   de bord §4 (questions ouvertes) et passer à l'étape suivante.
6. Si la session conclut « contribution partielle » : auditer rigoureusement
   selon procédure Réfuteur du `prompts/refuteur.md`.

## Ordre d'exécution recommandé

```
A1 → A2 → A3 → A4 → A5    (séquence principale, 5 étapes)
                                  │
                                  ▼
                         si bloqué à A2 : explorer D1-D5
                                  │
                                  ▼
                         si bloqué à A4 : explorer C1-C4

B1-B4 : à explorer seulement si conviction P = NP forte (rarement le cas)
```

## Liens

* [`../cahier_de_bord.md`](../cahier_de_bord.md) — état actuel de
  l'exploration (24 tours dont 5 ❌ FAILLE FATALE, 8 ✅ ÉTABLIS folklore).
* [`../prompts/proposeur.md`](../prompts/proposeur.md) — rôle Proposeur.
* [`../prompts/refuteur.md`](../prompts/refuteur.md) — rôle Réfuteur.
