# NOTE-002 — Note de synthèse du fil SYM∘AND + antériorité des théorèmes

- **Type** : C (consolidation + antériorité)
- **Exécutée le** : 2026-07-23
- **Output** : [`notes/symand_synthese.md`](../../notes/symand_synthese.md)

## Contenu de la note

Le dossier F-012..022 structuré en 9 sections : le modèle (définition,
provenance Beigel-Tarui/ligne 7), 17 valeurs exactes + 2 fenêtres, les
4 théorèmes AVEC preuves (tranche, comptage, alternance, fenêtre ANF),
les 2 constructions et leurs régimes de serrage, les 3 réfutations et
le zoo, l'asymptotique honnête, l'antériorité, l'ingénierie, la
distance à P vs NP.

## Antériorité (2 vérifications faites cette session)

1. **alt(f) = la « decrease » d(f) de MARKOV 1957** (complexité
   d'inversion, ⌈log₂(d+1)⌉ portes NOT) — quantité CLASSIQUE,
   attribuée dans la note ; notre théorème T3 (W ≥ alt dans le modèle
   à séparation par valeurs) semble un usage neuf.
2. **La suite |ANF(MAJ_m)| est ABSENTE de l'OEIS** (API, 2 fenêtres de
   recherche : « AUCUN résultat ») — 3, 3, 7, 15, 35, 35, 71, 255,
   627, 627, 1419, 3003, 6435, 6435, 12871, 65535, 155363, 155363,
   354331. Candidate à soumission OEIS (main de Tanguy, avec le m=20).
3. Rappel des passes antérieures : seuils en escalier (T4) — rien
   trouvé (2 passes) ; ANF de MAJ en littérature (Méaux 2019, non
   refait).

Réserve globale : le modèle est house-made — les théorèmes T1-T4 y
semblent neufs SANS garantie ; relecture experte avant toute diffusion.
