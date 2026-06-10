# Audit A-009 — le programme méta-complexité moderne (Hirahara et al., 2018-2023)

- **Sources lues** : Huang-Ilango-Ren, *NP-Hardness of Approximating
  Meta-Complexity: A Cryptographic Approach*, STOC 2023 (PDF intégral,
  9 p., extrait le 2026-06-11) ; survey Hirahara (Bulletin EATCS,
  référencé). Déclencheur : veille probabiliste
  (`bib/veille_probabilistes_2026.md`).
- **Distinction** : la ligne 2 de l'Atlas couvre la méta-complexité
  *naïve* (Kt, circularité — Tour 1). Ici : le **programme moderne**,
  structuré autour de MCSP et des réductions non-boîte-noire.

## Les objets et l'enjeu (verbatim)

- **MCSP** : « It is a long-standing open problem whether the Minimum
  Circuit Size Problem (MCSP) and related meta-complexity problems are
  NP-complete. » — et l'anecdote fondatrice : « Levin is reported to have
  delayed publishing his theory of NP-completeness in hopes of showing
  MCSP is NP-complete. » **Ouvert depuis 1971.**
- **Lien preuves naturelles** (constitutif) : « building on the natural
  proofs framework, Kabanets and Cai showed that if one-way functions
  exist, then MCSP is not in P. »

## Les percées (verbatim)

1. **La barrière boîte-noire et son contournement** : « there are barrier
   results against any NP-complete problem having a "black-box"
   worst-case to average-case reduction [Bogdanov-Trevisan…]. In a
   breakthrough result, **Hirahara [FOCS 2018] overcomes this barrier by
   giving a non-black-box worst-case to average-case reduction for
   approximating MCSP**. »
2. **La route anti-Heuristica** : « If one could show this approximation
   version of MCSP is NP-hard, then this would imply that NP does have a
   worst-case to average-case reduction and thus **rule out Heuristica** » ;
   Hirahara [2021] réduit encore : il suffit d'une approximation additive
   de GapMINcKT (méta-complexité « conditionnelle » — l'écho moderne de
   la question utilisateur sur les probabilités conditionnelles).
3. **Fonder la crypto sur P ≠ NP** : « Liu and Pass show that **one-way
   functions exist if and only if time-bounded Kolmogorov complexity is
   mildly hard on average** over the uniform distribution. »
4. **STOC 2023 (la source)** : NP-dureté d'approximation de la
   méta-complexité à gaps quasi-optimaux **par des constructions
   cryptographiques** (« the security of the cryptographic construction
   implies the correctness of the reduction ») ; et mvMCSP^O NP-dur
   p.p. sous oracle aléatoire via les CS Proofs de Micali.

## Test des barrières (le travail du Réfuteur)

| Barrière | Statut | Motif |
|---|---|---|
| Relativisation | ✓ **par construction** (avec nuance) | le cœur du programme est précisément *non-boîte-noire* (contournement démontré de Bogdanov-Trevisan) ; nuance : certains résultats (mvMCSP) ne valent que sous oracle aléatoire |
| Preuves naturelles | ⚠ **structurellement adjacent** | MCSP *est* le problème au cœur de RR (une propriété naturelle ≈ un algorithme pour une relaxation de MCSP) ; le programme marche sciemment sur cette frontière (Kabanets-Cai) — il ne la franchit ni n'y succombe : il en fait son objet |
| Algébrisation | — | [NON TROUVÉ DANS LES SOURCES] — les réductions cryptographiques (iO, CS Proofs) ne sont pas analysées sous AW dans les textes lus |
| Monotone | ◌ | sans objet |

## Verrou réel

**La NP-complétude de MCSP exact — ouverte depuis Levin.** Tous les
résultats sont conditionnels, approximatifs, partiels (partial-MCSP) ou
sous oracle. Et la portée vers P vs NP est **indirecte par essence** :
un succès complet exclurait Heuristica et fonderait les OWF sur P ≠ NP —
il **restructurerait les mondes d'Impagliazzo sans séparer P de NP**.
C'est le programme probabiliste le plus sophistiqué du moment, et un
chemin *vers l'écosystème* de P ≠ NP, pas une attaque frontale.

## Pour le dépôt

Pas de tâche exécutable petit-n naturelle (les objets sont des réductions,
pas des mesures) — la ligne 13 de l'Atlas documente la famille ; toute
proposition future invoquant MCSP devra citer cette cellule (règle Tour 26+).
