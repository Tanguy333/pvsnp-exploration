# Étape B.2 — Prouver la correction de l'algorithme

## Objectif formel

Soit $A$ l'algorithme produit en B.1. Prouver :

* (C1) $\forall \phi$ satisfiable, $A(\phi) = 1$ (complétude).
* (C2) $\forall \phi$ insatisfiable, $A(\phi) = 0$ (correction).

Ces deux conditions sont **logiquement séparées** et doivent être prouvées
indépendamment.

## Statut actuel (2026)

* Méthodes standard pour prouver la correction d'algorithmes :
  invariants de boucle (Floyd 1967), récurrence sur la structure
  d'entrée, induction noéthérienne.
* Pour SAT, l'algorithme DPLL classique a correction triviale (recherche
  exhaustive avec backtracking) mais complexité exponentielle.
* La difficulté n'est *pas* la correction (B.2) mais la complexité (B.3) :
  un algorithme correct exponentiel se transforme en algorithme
  « polynomial » par erreur d'analyse, pas par modification réelle.

## Prompt pour Claude (à coller en session neuve)

> Tu reçois l'algorithme `A` produit en B.1.
>
> Mission : prouver la correction de `A` selon (C1) et (C2).
>
> Procédure :
>
> 1. **Énoncer l'invariant central** de `A`. Pour un algorithme à boucle,
>    c'est typiquement « après chaque itération, la variable d'état
>    représente fidèlement [propriété] ».
>
> 2. **Prouver l'invariant par induction** sur les itérations.
>
> 3. **Prouver (C1) à partir de l'invariant** :
>    si `φ` satisfiable, identifier la trace de `A` qui arrive à la
>    sortie `1`. Cette trace doit exister pour *toute* affectation
>    satisfaisante.
>
> 4. **Prouver (C2) à partir de l'invariant** :
>    si `φ` insatisfiable, montrer que toutes les traces de `A` arrivent
>    à `0`. C'est typiquement la partie difficile : prouver qu'aucun
>    « faux positif » n'est possible.
>
> 5. **Test empirique en parallèle** : sur 1000 instances 3-SAT aléatoires
>    (mix satisfiables et insatisfiables, n=20, m=85 au seuil),
>    comparer `A(φ)` à un oracle SAT (e.g. minisat). Tout désaccord
>    invalide soit (C1) soit (C2).
>
> 6. **Si la preuve formelle bloque** : identifier précisément
>    l'invariant manquant ou la branche pathologique.
>
> Livrable : preuve formelle (style Floyd / Hoare) + log des 1000 tests
> empiriques + verdict.

## Critères d'acceptation

* **Succès complet** : (C1) et (C2) prouvées. *Réalisable si `A` est
  effectivement correct.*
* **Succès partiel** : (C1) prouvée mais (C2) demande un cas spécifique
  (typique des algorithmes incomplets).
* **Échec acceptable** : identification d'une instance jouet où `A`
  retourne le mauvais résultat.

## Modes d'échec attendus

* Invariant trop fort (faux) ou trop faible (insuffisant).
* Cas pathologique où `A` retourne `1` sur insatisfiable (faux positif) —
  *typique des heuristiques* qui « voient » une affectation imaginaire.
* Cas où `A` retourne `0` sur satisfiable (faux négatif) — *typique des
  algorithmes incomplets* qui ne backtrack pas assez.

## Références à embarquer

* Floyd 1967, *« Assigning meanings to programs »*.
* Hoare 1969, *« An axiomatic basis for computer programming »*.
* Cook 1971 (réduction SAT).
* MiniSAT / Z3 (oracles modernes pour test empirique).

## Conditions du cahier en vigueur

* `(h)` script + log empirique livrés.
* `(j)` test sur 1000 instances *avant* claim de correction.
* `(r)` test au point suivant : si correction prouvée à `n=20`, vérifier
  à `n=40` aussi.
