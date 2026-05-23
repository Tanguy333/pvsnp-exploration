# Étape D.4 — Invariant survivant à l'équivalence logique mais pas aux sauts polynomiaux

## Objectif formel

Trouver un invariant $I(\phi)$ sur les formules CNF (ou structures
combinatoires) tel que :

* (LE1) **Invariance logique** : $\phi \equiv \phi' \Rightarrow I(\phi) = I(\phi')$.
  C'est la condition que Tour 3 a violée (Betti homologique des paysages
  d'énergie change selon la présentation syntaxique).
* (LE2) **Non-invariance par sauts polynomiaux** : pour $G_r$ = hypercube
  avec arêtes Hamming-$r$, $I(\phi)$ varie selon $r$. C'est la condition
  duale que Tour 3 a aussi violée (Betti s'effondre dès $r=2$).

(LE1) **et** (LE2) ensemble = invariant logique mais **non**-survival aux
algorithmes polynomiaux $\Rightarrow$ borne inférieure pour $P$.

## Statut actuel (2026)

* Tour 3 du cahier a tenté Morse + Lusternik-Schnirelmann sur paysages
  d'énergie CSP. Échec sur (LE1) et (LE2).
* Pattern général : tout invariant *combinatoire* sur formules CNF
  semble soit (i) variable sous équivalence logique (= dépendant de la
  syntaxe), soit (ii) invariant sous sauts polynomiaux (= ne sépare pas P).
* Question ouverte : existe-t-il un *seul* invariant satisfaisant LE1 *et*
  LE2 ?

## Prompt pour Claude (à coller en session neuve)

> Tu es chercheur sur les invariants combinatoires en complexité.
>
> Mission : identifier un invariant `I(φ)` satisfaisant (LE1) + (LE2).
>
> Procédure :
>
> 1. **Comprendre l'échec du Tour 3** :
>    - L'invariant `Σ β_i(L_k(φ))` n'est pas LE1 car
>      `(x_0∨x_1)∧(x_2∨x_3)∧(x_4∨x_5)` et sa version avec clauses
>      triplées ont des Betti différents.
>    - Pour LE2 : `β_0(témoins, r=1) = 8`, `β_0(témoins, r=2) = 1` —
>      effondrement immédiat.
>
> 2. **Identifier les candidats LE1** :
>    - Invariants définis *sur la fonction booléenne* (pas la formule) :
>      sensibilité, sensibilité par blocs, degré PTF, communication
>      complexity, sign-rank, etc.
>    - Tous LE1 par construction (dépendent de `f`, pas de `φ`).
>
> 3. **Tester LE2 sur les candidats** :
>    - Communication complexity : survit aux sauts polynomiaux car
>      reste sous-additif. *Non-LE2* — n'aide pas.
>    - Sensibilité : survit (lipschitz par construction). *Non-LE2*.
>    - Degré PTF : peut s'effondrer (rebondit selon `r`). À vérifier
>      empiriquement.
>    - Sign-rank : peut être très sensible à `r`. Candidat plausible.
>
> 4. **Construire un invariant hybride** :
>    - Composer un invariant LE1 avec un *opérateur* qui le rend
>      LE2-sensitif. Par exemple : `I_r(f) = `min` sur `r`-localisations
>      de la communication complexity.
>    - Risque : la composition peut casser LE1.
>
> 5. **Test empirique** :
>    - Sur 50-100 fonctions à `n=4, 5`, vérifier LE1 (par énumération
>      d'équivalences logiques) et LE2 (par variation de `r ∈ {1,2,3}`).
>    - Si l'invariant survit aux deux tests, candidat sérieux.
>
> 6. **Application** : si invariant trouvé, dériver une borne `time_P(L)
>    ≥ I(L)` pour un problème `L ∈ NP` candidat.
>
> Livrable : invariant candidat + tests empiriques LE1/LE2 +
> application.

## Critères d'acceptation

* **Succès complet** : invariant satisfaisant LE1 + LE2 +
  application borne inférieure. *Sans précédent.*
* **Succès partiel** : candidat partiel (LE1 mais LE2 partiel ou
  inversement).
* **Échec acceptable** : audit exhaustif des candidats + impossibilité
  argumentée.

## Modes d'échec attendus

* Invariant Tour 3 réfuté répété (Morse, Forman, Lusternik-Schnirelmann
  → tous syntaxiques).
* Invariant LE1 mais qui survit aux sauts polynomiaux (ne sépare pas P).
* Invariant LE2 mais syntaxique (Tour 3 répété).

## Références à embarquer

* Forman 1998 (Morse discret).
* Sergeraert (homotopy invariants).
* Crama-Hammer 2011 (DNF properties).
* Aaronson, *« P =? NP »* survey (Aaronson 2017).
* Mihai-Vassilevska 2007 (polynomial-jump hypercube).

## Conditions du cahier en vigueur

* §4 q.1 : invariance sous équivalence logique = LE1.
* §4 q.2 : survie aux sauts polynomiaux = LE2 dual.
* Test empirique `(j)` à `n=4, 5` obligatoire.
* `(r)` test à `n+1`.
