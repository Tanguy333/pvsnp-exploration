# Étape D.3 — Inventer une technique non-algébrisante

## Objectif formel

Trouver une technique de borne inférieure $\tau$ qui :

* (NA1) **Ne se restreint pas** à un oracle algébrique $\tilde A$
  relativement auquel $P^{\tilde A} = NP^{\tilde A}$.
* (NA2) S'applique à au moins une famille de fonctions non-triviale.

## Statut actuel (2026)

* Aaronson-Wigderson 2008 ont montré que **toutes** les techniques
  d'arithmétisation classique (Shamir, Lund-Fortnow-Karloff-Nisan,
  Razborov-Smolensky) algébrisent.
* **Williams 2011** est l'unique exemple connu de technique
  non-relativisante *et* non-algébrisante. Le mécanisme exact reste
  partiellement opaque.
* Question ouverte : peut-on **construire systématiquement** des
  techniques non-algébrisantes ?

## Prompt pour Claude (à coller en session neuve)

> Tu es chercheur sur la barrière d'algébrisation.
>
> Mission : identifier ou inventer une technique non-algébrisante autre
> que Williams 2011.
>
> Procédure :
>
> 1. **Comprendre l'algébrisation** :
>    - Définition AW 2008 : une preuve algébrise s'il existe une
>      extension polynomiale `Ã` de tout oracle `A` tel que la preuve
>      relativise par rapport à `Ã`.
>    - Conséquence : toute technique d'arithmétisation à polynômes de
>      bas degré algébrise.
>
> 2. **Analyser Williams 2011 plus finement** :
>    - Pourquoi ne s'extend-elle pas à un oracle algébrique ?
>    - Indice : l'énumération non-triviale d'algorithmes ne s'étend pas
>      à un objet d'oracle algébrique sans rupture structurelle.
>
> 3. **Identifier les pistes hors arithmétisation** :
>    - (a) Méthodes **topologiques** : invariants combinatoires
>      sans arithmétisation. Risque Tour 3 (invariant non-invariant
>      sous équivalence logique) — à éviter explicitement.
>    - (b) Méthodes **information-théoriques** : mutual information,
>      query complexity, communication complexity. Risque algébrisation
>      via interpolation polynomiale — à auditer.
>    - (c) Méthodes **logiques** : complexité descriptive (Immerman,
>      Gurevich, Dawar). Naturellement non-algébrisante car les jeux
>      d'EF ne s'arithmétisent pas trivialement.
>    - (d) Méthodes **quantiques** : sign-rank, query complexity
>      quantique. Aaronson 2011 a montré que certaines bornes
>      quantiques échappent à algébrisation classique.
>
> 4. **Test rigoureux** :
>    - Pour chaque candidate, exhiber un oracle algébrique `Õ` tel que
>      `P^Õ = NP^Õ`.
>    - Vérifier ligne-à-ligne que la technique ne tient pas
>      relativement à `Õ`.
>
> 5. **Application** : famille de fonctions où la technique donne
>    une borne nouvelle.
>
> Livrable : technique candidate + preuve non-algébrisation rigoureuse
> + application.

## Critères d'acceptation

* **Succès complet** : technique non-algébrisante nouvelle + application.
* **Succès partiel** : technique candidate, audit non-algébrisation
  partiel.
* **Échec acceptable** : cartographie des techniques connues
  (Williams + candidates) + obstacles structurels.

## Modes d'échec attendus

* Technique d'arithmétisation déguisée (algébrise par construction).
* Méthode quantique qui s'arithmétise en classique
  (algorithm-by-algorithm).
* Confusion algébrisation / non-relativisation (les deux sont distincts).

## Références à embarquer

* Aaronson-Wigderson 2008, *« Algebrization: A new barrier in complexity
  theory »*.
* Williams 2011.
* Aaronson 2010, *« A counterexample to the generalized Linial-Nisan
  conjecture »* (utilise des techniques quantiques).
* Forster 2002 (sign-rank).
* Sherstov 2008+ (sign-rank lower bounds).

## Conditions du cahier en vigueur

* `(c)` algébrisation : c'est l'objet.
* `(b)` non-relativisant : doit être *additionnellement* honoré (les
  deux sont indépendants).
* Test du Tour 4 : pas de « pointer vers Williams ne suffit pas ».
