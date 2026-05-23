# Étape A.1 — Choix de la fonction-cible $f_n$ et de la classe $\mathcal{C}_n$

## Objectif formel

Identifier une fonction explicite $f_n : \{0,1\}^n \to \{0,1\}$ dans NP
(typiquement NP-complète) **et** une classe de circuits $\mathcal{C}_n$
contenant $P$, telles que la séparation $f_n \notin \mathcal{C}_n$
impliquerait $P \neq NP$.

## Statut actuel (2026)

* SAT, CLIQUE_k, 3-COLORATION, Subset-Sum, HAM-CYCLE : toutes NP-complètes,
  séparation $f \notin P/\text{poly}$ ouverte pour chacune.
* P/poly contient strictement P et est la classe la plus large où une
  séparation $f \notin P/\text{poly}$ donne $P \neq NP$.
* Choix de cible **n'est pas neutre** : Razborov 1985 a réussi pour
  CLIQUE en monotone car CLIQUE est naturellement monotone ; pas pour SAT.

## Prompt pour Claude (à coller en session neuve)

> Tu es un chercheur expérimenté en théorie de la complexité. Ta mission :
> identifier le couple `(f_n, C_n)` optimal pour attaquer P ≠ NP via bornes
> inférieures de circuit.
>
> Critères :
>
> 1. `f_n` doit être NP-complète et explicite.
> 2. `C_n` doit contenir P et permettre l'application de techniques
>    non-relativisantes connues (au moins une).
> 3. Argumenter pourquoi ce choix maximise les chances vs les choix
>    concurrents (SAT, CLIQUE_k, 3-COL, Subset-Sum, HAM-CYCLE).
> 4. Identifier explicitement les techniques de borne inférieure
>    historiques pour `f_n` (Razborov 1985 pour CLIQUE monotone, etc.) et
>    pourquoi elles ne s'étendent pas (Tardos 1988, etc.).
>
> Livrable (≤ 800 mots) :
>
> * Couple `(f_n, C_n)` retenu.
> * Justification structurée vs 3 alternatives au minimum.
> * Liste des 3-5 obstacles techniques identifiés.
> * Position vis-à-vis des 4 barrières (relativisation, RR, algébrisation,
>   monotone Razborov-Tardos).
> * Citation explicite d'au moins 5 références (Cook 1971, Razborov 1985,
>   Tardos 1988, Williams 2011, Aaronson-Wigderson 2008 — ou équivalentes).

## Critères d'acceptation

* **Succès complet** : couple `(f_n, C_n)` justifié, techniques connues
  cataloguées, obstacles identifiés. *Réalisable* — c'est de la synthèse.
* **Succès partiel** : choix justifié mais obstacles non-cartographiés
  exhaustivement.
* **Échec acceptable** : la session conclut que le choix optimal *dépend*
  de l'invention à venir (renvoie vers section D).

## Modes d'échec attendus

* Re-choix de cible classique (SAT) sans valeur ajoutée → folklore.
* Choix exotique sans justification (e.g. cible artificielle) →
  Razborov-Rudich risque (propriété pas naturelle).
* Omission de Tardos 1988 → réplication du Tour 24 (FAILLE FATALE
  tropicale).

## Références à embarquer

* Cook 1971, *« The complexity of theorem-proving procedures »*.
* Karp 1972, *« Reducibility among combinatorial problems »*.
* Razborov 1985, *« Lower bounds on the monotone complexity of some
  Boolean functions »*.
* Tardos 1988, *« The gap between monotone and non-monotone circuit
  complexity is exponential »*.
* Williams 2011, *« Non-uniform ACC circuit lower bounds »*.
* Aaronson-Wigderson 2008, *« Algebrization: A new barrier in complexity
  theory »*.

## Conditions du cahier en vigueur

* `(a)` classe restreinte : `C_n` doit être explicite.
* `(b)` non-relativisant : justification obligatoire.
* `(c)` non-algébrisant : justification obligatoire.
* `(k)` lien à P vs NP : direct par construction.
* `(q)` audit bibliographique préemptif.
