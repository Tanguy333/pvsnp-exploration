# ATLAS-012 — Porter les recommandations de VEILLE-2026-2 dans la matrice : une ligne neuve, deux nuances, une note de colonne

`Rattachement :` Atlas ligne 16 (créée) + lignes 13 et 15 (nuancées) + colonne
« preuves naturelles » (note de bas de colonne). **Relu à la clôture : la cellule
visée a-t-elle bougé ? OUI** — une seizième famille d'approches entre dans le
livrable, et trois cellules existantes changent de contenu.

`Test de plafond :` sans objet au sens du calcul — cette tâche est une tâche de
**lecture**, sans mesure. Le plafond de l'instrument n'intervient pas ; c'est
précisément la catégorie de tâche que le recentrage a désignée comme la plus
rentable du dépôt (ATLAS-006, puis VEILLE-2026-2 elle-même).

<!--DISTANCE-->
Énoncé visé : la famille « range avoidance » a un profil de barrières documenté
et un double verrou démontré, dont l'un (AM ∩ coAM) est interne à l'approche.
Classe de complexité qui y figure : Σ₂E, S₂E, AM ∩ coAM, PH, NP.
Chaîne vers P vs NP : range avoidance → constructions explicites de fonctions
dures → bornes inférieures pour des classes uniformes → séparation.
[maillon le plus faible : les bornes obtenues vivent en Σ₂E/S₂E, au deuxième
étage de la hiérarchie exponentielle ou au-delà — très loin de NP]
<!--/DISTANCE-->

## Ce qui a été écrit

**Ligne 16 — range avoidance (Avoid) / constructions explicites.** Nouvelle
famille, au format des quinze autres. Son intérêt pour cet Atlas n'est pas
qu'elle progresse, mais qu'elle possède un **double plafond**, dont la moitié
est démontrée récemment et de l'intérieur :

- *(i) Plafond interne, 2025* : Avoid n'est **pas NP-dur sauf effondrement de
  PH** — tout langage réductible à Avoid par réduction Turing déterministe ou
  randomisée est dans **AM ∩ coAM** (Ghentiyala-Li-Stephens-Davidowitz, ECCC
  TR25-210, STOC 2026). C'est une barrière interne au sens de la lecture 2 de la
  matrice : la famille engendre elle-même l'analyse de sa limite.
- *(ii) Barrière classique* : la voie livre ses meilleures bornes pour Σ₂E / S₂E,
  près du maximum 2ⁿ/n — **et ces bornes relativisent**, ce que ses propres
  auteurs écrivent (« *relativizing algorithms for Range Avoidance are equivalent
  to decision trees for Missing-String* », Chen-Hu-Ren, ITCS 2026). BGS les borne
  donc exactement.

**Ligne 13 — verrou confirmé, avec une nuance qui change la question.** La
NP-dureté de la méta-complexité **se fractionne par type de réduction** :
NP-dureté sous réductions randomisées *half-Levin*, et impossibilité de NP-dureté
sous réductions de Levin randomisées, sous deux hypothèses (Goldberg-Juvekar-
Kabanets, ECCC TR26-091). « MCSP est-il NP-complet ? » n'a plus une réponse mais
une famille de réponses indexées par la notion de réduction. Hirahara-Ilango
FOCS 2025 est **signalé avec son contenu en [NON TROUVÉ]** — métadonnées
vérifiées, texte introuvable — et explicitement marqué « à ne pas citer comme
appui ».

**Ligne 15 — une formulation de l'Atlas est corrigée.** La cellule écrivait que
la barrière du programme Cook-Reckhow est « auto-référentielle par essence ».
Davis-Robere (ECCC TR26-055) montre qu'un système de preuve **peut** prouver de
fortes bornes contre lui-même dans un régime précis. L'auto-référence n'est donc
pas un obstacle *par nature* : elle l'est *dans le régime des tautologies
ordinaires*. Le verrou lui-même (AC⁰[p]-Frege entièrement vide) est inchangé.

**Colonne 2 — la barrière RR a désormais une version inconditionnelle dans un
sous-cas.** Pour les preuves naturelles à distingueurs AC⁰, aucune ne peut
prouver mieux que 2^{n^{7/(d−5)}} contre la profondeur d (Loff-Sherif-
Talebanfard-Ugazio, arXiv:2606.12631). Conséquence pour les lignes 4, 6 et 12 :
l'argument « la barrière RR n'est que conditionnelle » n'est plus disponible dans
le régime AC⁰. **Statut préprint explicite**, sans lieu de publication, non relu
au-delà de l'abstract.

## Ce qui n'a PAS été écrit, et pourquoi

- **Ligne 10** (hardness magnification) : la veille n'a rien trouvé de 2025-2026.
  `[NON TROUVÉ]` assumé, recherche non exhaustive — pas de remplissage cosmétique.
- **Lu-Santhanam-Tzameret**, recommandé par la synthèse de la veille pour la
  ligne 15, n'a pas été porté : je n'ai pas retrouvé sa fiche sourcée dans le
  corps de la note. Règle 4 (no invention) : on ne cite pas ce qu'on n'a pas vu.
  À reprendre si la référence est retrouvée.

## Antériorité

Aucune revendication : cette tâche **compile de la littérature vérifiée**, elle
ne produit aucun résultat. Les 35 références de VEILLE-2026-2 ont été contrôlées
une par une par un vérificateur adverse (titre, auteurs, année, lieu, et contenu
attribué), verdict « aucune référence inventée ».
