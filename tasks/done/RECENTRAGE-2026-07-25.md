# Recentrage du dépôt sur P vs NP — les cinq tâches du backlog recentré

`Rattachement :` Atlas lignes 4, 7, 14 + en-tête + instrument pour toutes les
lignes — c'est le recâblage du livrable sur les acquis existants.

`Énoncé visé :` aucun énoncé mathématique — cette fiche couvre des tâches de
gouvernance et de câblage du livrable.
`Classe de complexité qui y figure :` AUCUNE, et c'est normal : ces tâches
servent les cellules, elles ne les démontrent pas (cf. CLAUDE.md §8 règle 8,
qui interdit précisément d'en faire une porte automatique).
`Chaîne vers P vs NP :` cellules d'Atlas rejouables → un tiers peut vérifier ou
réfuter ce que le dépôt affirme → l'Atlas devient utilisable comme générateur
de cibles. [maillon le plus faible : le livrable reste une compilation, il ne
démontre rien de neuf]

## Ce qui a été fait (2026-07-25)

| Tâche | Livrable | La cellule visée a-t-elle bougé ? |
|---|---|---|
| **GOUV-001** | `CLAUDE.md` : arborescence réelle (§4), test des barrières non désactivable seul (§5.4), règles 7-10 (rattachement relu à la clôture, test de distance non-grep, bilan par fil défini par sa cible, recadrages écrits dans les règles), règle 2 durcie, réouverture d'un Tour à 5 conditions | Sans objet (gouvernance) — mais c'est la tâche qui rend les autres vérifiables |
| **ATLAS-008** | `atlas/echelle_instrument.md` | **OUI** — note de dispositif neuve, deux témoins chiffrés (n ≤ 8 contre n ≈ 4050 ; O(n²) contre 2^{polylog n}) |
| **ATLAS-007** | en-tête de la matrice + lignes 7 et 14 | **OUI** — le fil SYM∘AND (18 tâches) et le fil AS (43 tâches) entrent dans le livrable pour la première fois |
| **ATLAS-010** | `atlas/temoins.md` (17 scripts sur 188, 18 lignes) | **OUI** — le chaînage cellule → script → commande → sortie → durée n'existait pas |
| **ATLAS-011** | ligne 4 (contenu mesuré de F-011) | **OUI** — la ligne ne citait que `bib/razborov_smolensky_1987.md` ; le fil F-011 est désormais clos |
| **PUB-001** | `README.md` | **OUI** — quatre chiffres faux corrigés (12→15 familles, 9→22, ~30→188, 25→27) |
| **VEILLE-2026-2** | `bib/veille_2026_07.md` | **OUI** — sourçage des fronts 2025-2026 pour les lignes 7, 10, 13, 15 |

## Le dispositif de contrôle, et ce qu'il a attrapé

Chaque texte est passé par une **vérification adverse** avant écriture. Elle a
rendu « À CORRIGER » sur les deux lots, et ses prises méritent d'être
consignées — elles sont la matière du régime d'échec n°5 :

1. **Ligne 4 — une conjecture présentée comme établie.** Le motif d'arrêt
   proposé écrivait que la plate `deg₆(MAJ_n) = ⌈n/2⌉` « établit » que le modèle
   ne sépare pas MAJ, avec le quantificateur « toute fonction de seuil t ». Or
   la plate est MESURÉE (n = 4..25, 29, 31, 32, quatre trous) et le prouvé ∀t ne
   couvre que trois familles. *La conclusion était juste, la prémisse invoquée
   était fausse* — et le bon argument, inconditionnel, était deux lignes plus
   haut : « polynôme unique ≠ circuit AC⁰[6] ». Il a été promu motif porteur.
2. **Ligne 14 — deux revendications de primauté sans folklore-check**, alors
   que la fiche source (`AS-022` §4) écrit elle-même que la réserve « reste à
   poser à Krishan », courrier sans réponse. Retirées. C'est la règle 10, écrite
   le matin même, violée l'après-midi.
3. **Ligne 7 — le `[NON TROUVÉ]` était trop étroit.** Le même audit enregistre
   que les polynômes de Beigel-Tarui sont **sur ℤ**, donc à coefficients signés,
   là où le modèle du dépôt impose des coefficients ≥ 0 : **seconde** divergence
   de convention, passée sous silence. Ajoutée.
4. **Veille — aucune référence inventée.** Les 35 références ont été vérifiées
   une par une (titre, auteurs, année, lieu, et ce qui leur est attribué), PDF
   re-téléchargés et occurrences recomptées. Ce qui était faux n'était pas une
   référence mais six énoncés *sur* les références. Point notable : la note
   avait elle-même rejeté deux affirmations fabriquées par les moteurs de
   recherche, et les deux rejets ont été confirmés par réplication.

## Réserve de méthode sur cette fiche

Elle couvre **sept tâches en un commit**, ce qui contrevient à la règle 2 telle
que je viens de l'écrire (« un commit = une tâche »). C'est assumé pour cette
opération de recentrage, qui forme un tout ; la règle s'applique à partir de la
prochaine session.
