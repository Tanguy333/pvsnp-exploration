# TOUR 27 — Le quotient symétrique : ÉCHEC HONNÊTE sur la cible, TROIS ACQUIS PROUVÉS (dont un par le Réfuteur)

- **Date** : 2026-07-24. Proposeur : Qwen. Réfuteur : Claude.
- **Cible** ([`tour_27_cible.md`](tour_27_cible.md)) : trou unique
  « décomposable ⇒ global » — prouver W = W_dec = k(k+1), ou témoin
  global < 30 à k = 5.
- **Scripts du Proposeur** : `checks/tour_27_proposeur_symopt.py`,
  `_classes.py`, `_anneal.py` — livrés exécutés, ré-exécutés par le
  Réfuteur. **Script du Réfuteur** :
  `checks/tour_27_refuteur_classeA.py` (la prédiction exécutée).

## 1. Reformulation (une phrase)

Quotienter le problème par le groupe G = S_k ⋉ (S₂)^k réduit la
classe symétrique à un programme d'orbites minuscule — fermé
exactement (théorème L27.1 : W_sym = k(k+1), k ≤ 8) — puis
cartographier négativement la moitié asymétrique et proposer la
fermeture de la classe A comme sous-lemme décidable.

## 2. Audit du Réfuteur

**Validé** :
- **L27.1 REPRODUIT 6/6** (programme d'orbites OPTIMAL k = 3..8,
  bornes égales ; solution k = 5 dépliée re-vérifiée disjointe sur
  1024 points). Logique du quotient auditée : la valeur d'un
  polynôme G-symétrique ne dépend que du type (a, b) de la
  configuration — correct. **Toute la classe symétrique est fermée
  à k(k+1) pour k ≤ 8 : toute réfutation possible est asymétrique.**
- **L27.2** (lemme de span) : correct, une ligne — un monôme
  couvrant r blocs n'agit qu'à m ≥ r ; p = p_{span≤2} + p_lift.
- Les 8 candidats manuels collisionnent (reproduit) ; le recuit et
  l'impuissance CP-SAT à n = 10 : constats mesurés, honnêtes.
- La bascule structurelle expliquée : l'optimum symétrique est
  l'orbite croisée (0,2) à k = 3, puis les orbites décomposables
  dès k = 4 — la coexistence de F-021 élucidée.

**Erreur attrapée (portée, pas fond)** : le corollaire (ii) affirme
que le run de 25 min du dossier « ne pouvait structurellement rien
trouver » — FAUX : ce run utilisait un cassage de symétrie par ordre
des masses (recherche sur des représentants de TOUTES les solutions,
asymétriques comprises), pas une restriction aux solutions
symétriques. Son évidence négative reste valable. La première moitié
de (ii) (tout témoin < 30 est non-G-symétrique) est correcte.

## 3. LA PRÉDICTION EXÉCUTÉE (l'acquis du Réfuteur)

Le Proposeur a dessiné la fermeture de la classe A (intra individuels
+ faisceaux de paires) sans la réaliser, avec prédiction falsifiable
« ≥ 30 ». Le Réfuteur l'a implémentée : 288 d-vecteurs canoniques
(graphes pondérés sur 5 sommets, Σd ≤ 7, canonisation par S₅), DFS
sur les triples intra (0 autorisé — l'argument a,b ≥ 1 ne tient plus
avec croisés) avec élagage partiel sain, valeurs par configuration
(4⁵ états, croisés d_ij·s_i·s_j). **Résultat (270 s, exhaustif) :
AUCUN séparateur de classe A de poids ≤ 29 — CLASSE A ≥ 30, la
prédiction est PROUVÉE.**

## 4. Verdict : **ÉCHEC HONNÊTE sur la cible, ACQUIS VALIDÉS**

La cible (décomposable ⇒ global, ou témoin < 30) n'est fermée dans
aucun sens — dit par le Proposeur lui-même, sans pivot. Le tour
laisse néanmoins la fenêtre [20, 30] STRUCTURELLEMENT rétrécie :

> Tout témoin < 30 à k = 5 est nécessairement (i) asymétrique
> (L27.1), (ii) hors classe A (Réfuteur), (iii) contraint par le
> span (L27.2 : sa partie visible du côté 0 est de span ≤ 2).

Acquis consignés : L27.1 (théorème symétrique k ≤ 8), L27.2,
fermeture classe A, cartographie négative, bascule croisé/décomposable
expliquée. Sous-lemme prioritaire suivant : **fermer la classe B**
(paires croisées individuelles, non plus en faisceaux) par la même
machine d-branchée — puis span-2 complet ; chaque fermeture rétrécit
l'espace des témoins possibles, et une non-fermeture exhibe le témoin.

## 5. Post-tour (T27-S1, Réfuteur) : la CLASSE B est FERMÉE elle aussi

Exécuté le jour même ([`tasks/done/T27-S1.md`](../tasks/done/T27-S1.md)).
La machine d-branchée du DFS a plafonné (C = 1, mur à W_intra = 21
en 480 s — partiel prouvé : C = 1 vide jusqu'au poids total 22).
La fermeture est venue d'un moteur CP-SAT neuf
([`checks/tour_27_refuteur_classeB_cpsat.py`](../checks/tour_27_refuteur_classeB_cpsat.py)) :
**canal de valeurs** (les valeurs vivent dans [0, cap] → 30 booléens
+ 1024 contraintes element au lieu de 97 308 désidentités) +
**lex-leader sound** sur les 9 involutions génératrices de G.
Échelle 19/22/25/27/29 TOUTE UNSAT (12 à 219 s), avec étalon :
cap 19 reproduit exactement la borne ≥ 20 du Tour 26 (théorème
indépendant), et contrôle positif cap 30 SAT re-vérifié par
énumération.

> **Classe B ≥ 30** (minimum de classe = 30, le décomposable
> (1,1,4)⁵) — subsume la classe A et le cas décomposable. Le point
> (ii) du verdict devient : tout témoin < 30 est asymétrique, hors
> A, hors B — **il doit employer un monôme de taille ≥ 3 touchant
> ≥ 2 blocs**. Suite : span-2 complet (105 coefs), puis l'espace
> entier (1023 monômes) par échelle de caps — chaque UNSAT y est
> une borne inférieure neuve sur le vrai W(MAJ₅(OR2⁵)).

## 6. Post-tour (T27-S2, Réfuteur) : LA CIBLE EST FERMÉE À k = 5

Le jour même encore ([`tasks/done/T27-S2.md`](../tasks/done/T27-S2.md)) :
le moteur canal de valeurs + lex-leader, généralisé à l'ESPACE
ENTIER des 1023 monômes
([`checks/tour_27_s2_espace_entier_cpsat.py`](../checks/tour_27_s2_espace_entier_cpsat.py)),
a monté l'échelle complète : caps 19 (étalon Tour 26 reproduit),
20, 21, ..., 29 — **onze UNSAT consécutifs** (58 s → 3517 s,
~3 h 20 au total), contrôle positif cap 30 SAT énuméré.

> **W(MAJ₅(OR2⁵)) = 30 = k(k+1), sur l'espace entier.** La cible de
> ce tour — « décomposable ⇒ global, ou témoin < 30 » — qui n'était
> « fermée dans aucun sens », est fermée dans le premier sens à
> k = 5. C26 est certifiée en pleine généralité aux points
> k = 3, 4, 5. Les fermetures de classes de ce tour (symétrique, A,
> B) sont subsumées — elles furent l'échafaudage du moteur qui a
> tout fermé.
