# P vs NP — Exploration assistée par IA

> **Cadrage honnête.** Ce dépôt n'est **pas** une prétention à résoudre P vs NP.
> C'est un carnet d'exploration pédagogique : deux LLM jouent des rôles
> adverses (Proposeur / Réfuteur) pour générer des pistes, les démolir
> rigoureusement, et **documenter pourquoi** chaque approche échoue.
> La valeur recherchée est la compréhension accumulée, pas une preuve.

## Le problème

Tout problème dont une solution candidate est vérifiable en temps polynomial
(classe NP) est-il aussi *résoluble* en temps polynomial (classe P) ? C'est l'un
des sept problèmes du prix du millénaire, ouvert depuis 1971. Aucune preuve
valide n'existe à ce jour.

## Le dispositif

Une boucle à rôles séparés, conçue pour résister à la confabulation :

1. **Proposeur** — génère une idée neuve pour le sous-but courant (voir `prompts/proposeur.md`).
2. **Réfuteur** — a pour unique mission de la démolir (voir `prompts/refuteur.md`).
3. **Ancrage** — confrontation à la littérature réelle (recherche web) : l'idée est-elle déjà publiée/écartée ?
4. **Vérification** — toute idée qui survit voit un sous-lemme isolé, idéalement formalisé (Lean).
5. **Journal** — chaque tour est consigné, succès **ou** échec, dans le cahier de bord et `tours/`.

> Règle d'or : on ne réexplore jamais une impasse déjà documentée.

## Organisation

```
.
├── README.md              ← ce fichier
├── cahier_de_bord.md      ← document central, état vivant de l'exploration
├── prompts/
│   ├── proposeur.md       ← rôle figé du Proposeur
│   └── refuteur.md        ← rôle figé du Réfuteur
└── tours/
    └── tour_01_kolmogorov.md  ← archive : idée brute + réfutation complète
```

## Les trois barrières connues

Toute tentative sérieuse doit dire laquelle elle prétend franchir — et la plupart meurent là :

- **Relativisation** (Baker–Gill–Solovay, 1975) — une preuve qui « relativise » ne peut pas trancher P vs NP.
- **Preuves naturelles** (Razborov–Rudich, 1997) — les bornes inférieures « naturelles » échouent sous hypothèses cryptographiques standard.
- **Algébrisation** (Aaronson–Wigderson, 2008) — généralise la relativisation aux techniques algébriques.

## État courant

Voir `cahier_de_bord.md`. Au tour 1, une piste fondée sur la complexité de
Kolmogorov des témoins a été réfutée (équivoque conditionnel/inconditionnel +
argument relativisant). Archive complète dans `tours/tour_01_kolmogorov.md`.

## Avertissement

Ce projet est un exercice d'apprentissage et de méthode. Les « idées » produites
par les modèles sont spéculatives et systématiquement soumises à réfutation. Ne
citez aucun contenu de ce dépôt comme un résultat mathématique établi.
