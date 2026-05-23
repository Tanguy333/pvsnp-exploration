# Étape B.4 — Déduire P = NP

## Objectif formel

À partir de B.1 (algorithme), B.2 (correction), B.3 (complexité
polynomiale), conclure $P = NP$.

Chaîne logique :

1. SAT $\in P$ (par B.1-B.2-B.3).
2. SAT est NP-complète (Cook 1971).
3. Donc tout problème de NP se réduit à SAT en temps polynomial.
4. Donc tout problème de NP est résoluble en temps polynomial.
5. **Donc** NP $\subseteq P$.
6. P $\subseteq$ NP est trivial.
7. **Donc** $P = NP$.

## Statut actuel (2026)

* Étape *purement déductive* — triviale si B.1-B.3 réussissent.
* Mais B.1-B.3 n'ont jamais réussi.

## Prompt pour Claude (à coller en session neuve)

> Tu reçois `A` validé B.1, prouvé correct B.2, polynomial B.3.
>
> Mission : effectuer la déduction `SAT ∈ P ⟹ NP ⊆ P ⟹ P = NP`.
>
> Procédure :
>
> 1. Énoncer le théorème de Cook 1971 : SAT est NP-complète.
>
> 2. Énoncer la conséquence : pour tout `L ∈ NP`, il existe une réduction
>    polynomiale `r_L : Σ* → CNF` telle que `L(x) ⟺ SAT(r_L(x))`.
>
> 3. Construire l'algorithme polynomial pour `L` :
>    `Algorithme_L(x) := A(r_L(x))`.
>
> 4. Borner la complexité : `time(r_L) ≤ |x|^c_L` (par hypothèse Karp) et
>    `time(A) ≤ |φ|^k` (par B.3), donc
>    `time(Algorithme_L) ≤ (|x|^c_L)^k = |x|^{c_L · k}`. Polynomial.
>
> 5. Conclure `L ∈ P`. Comme valable pour tout `L ∈ NP`, NP ⊆ P.
>
> 6. P ⊆ NP est trivial (toute MT déterministe polynomiale a un
>    certificat trivial).
>
> 7. Conclure P = NP.
>
> 8. **Conséquences immédiates** :
>    - Quelles autres classes s'effondrent ? (PH = P, BPP = P, etc.)
>    - Quelles cryptos s'effondrent ? (RSA, ECC, lattice-based,
>      hash-based à audit).
>    - Que doit faire la communauté immédiatement ?
>
> Livrable : déduction (≤ 500 mots) + conséquences pratiques.

## Critères d'acceptation

* **Succès complet** : P = NP établi. *Trivial conditionnel à B.1-B.3.*
* **Succès partiel** : déduction conditionnelle (« si B.3 réussit, alors
  P = NP par cette chaîne »).
* **Échec acceptable** : identification d'un gap dans la chaîne de
  réductions Karp pour une famille spécifique.

## Modes d'échec attendus

* Réduction Karp avec coût polynomial caché (typique : réduction
  3-SAT → CLIQUE_k a un facteur $n^k$ qui devient critique).
* Erreur d'uniformité (l'algo `A` est uniforme, donc les conséquences
  P = NP sont uniformes — cohérent).
* Le réel mode d'échec est en B.3, pas ici. B.4 est juste de
  l'arithmétique.

## Références à embarquer

* Cook 1971.
* Karp 1972 (réductions explicites).
* Sipser, *Introduction to the Theory of Computation*, chapitre 7.

## Conséquences pratiques si P = NP

Documentées historiquement (Aaronson, *« Why Philosophers Should Care
About Computational Complexity »*) :

* Mathématiques : toute conjecture vérifiable en temps polynomial peut
  être prouvée ou réfutée en temps polynomial → la créativité humaine
  est en grande partie automatisable.
* Cryptographie : effondrement de toute la crypto à clé publique
  classique. Migration urgente vers quantum-resistant alternatives.
* IA : training et inférence se simplifient considérablement.
* Optimisation : tout problème combinatoire (TSP, scheduling, planning)
  devient résoluble efficacement.

**Conséquence sociale** : prouver P = NP ouvre plus de questions
philosophiques et éthiques qu'il n'en résout.

## Conditions du cahier en vigueur

* `(k)` lien à P vs NP : tautologique pour cette étape.
* `(g)` encodage non-trivialisant : vérifier les réductions Karp utilisées.
