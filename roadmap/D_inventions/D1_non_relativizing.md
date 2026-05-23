# Étape D.1 — Inventer une technique non-relativisante nouvelle

## Objectif formel

Identifier ou inventer une technique mathématique $\tau$ qui :

* (NR1) Permet de prouver des bornes inférieures de circuit.
* (NR2) **N'est pas valable** relativement à des oracles arbitraires
  (échappe à Baker-Gill-Solovay 1975).
* (NR3) S'applique à au moins une famille de fonctions non-triviale.

## Statut actuel (2026)

Trois techniques connues comme non-relativisantes :

* **Arithmétisation à la Shamir** (IP = PSPACE) : transforme une formule
  booléenne en polynôme sur un corps fini. Non-relativisante car
  l'oracle ne peut pas être arithmétisé fidèlement à bas degré.
* **Méthode algorithmique de Williams 2011** : combine arithmétisation
  Beigel-Tarui avec énumération non-triviale d'algorithmes. Le mécanisme
  exact de non-relativisation reste partiellement opaque.
* **Méthode polynomiale modulaire** (Razborov-Smolensky 1987) :
  approximation par polynômes de bas degré sur $\mathbb{F}_p$. Non-relativisante
  pour AC⁰[p] vs AC⁰.

**Toutes** ces techniques sont algébrisantes au sens Aaronson-Wigderson
2008 (sauf Williams 2011, qui est aussi non-algébrisant). Donc trouver
une 4e famille non-relativisante *et* non-algébrisante est un défi
ouvert.

## Prompt pour Claude (à coller en session neuve)

> Tu es chercheur en théorie de la complexité fondamentale.
>
> Mission : identifier ou inventer une 4e famille de techniques
> non-relativisantes (différente de Shamir, Williams 2011,
> Razborov-Smolensky).
>
> Procédure :
>
> 1. **Comprendre le mécanisme de non-relativisation** :
>    - Shamir : l'arithmétisation transforme une question booléenne en
>      question algébrique. Un oracle booléen `A` n'a pas
>      d'arithmétisation polynomiale qui préserve la sémantique.
>    - Williams 2011 : l'énumération d'algorithmes brise la symétrie
>      des oracles — un algorithme spécifique n'a pas son équivalent
>      pour `A` arbitraire.
>    - Razborov-Smolensky : pas immédiatement non-relativisant — c'est
>      la méthode polynomiale qui le rend.
>
> 2. **Identifier les sources structurelles de non-relativisation** :
>    - (a) Structure algébrique cachée dans le booléen (arithmétisation).
>    - (b) Énumération syntaxique (Williams).
>    - (c) ?
>
> 3. **Proposer une (c)** :
>    - Candidat : *complexité descriptive* (logique capturant P, jeux
>      d'Ehrenfeucht-Fraïssé) — non-relativisante par nature car les jeux
>      logiques ne se relativisent pas trivialement.
>    - Candidat : *information-theoretic locality* (techniques de
>      Forster, sign-rank, query complexity raffinée).
>    - Candidat : *topological/geometric invariants* sur les fonctions
>      booléennes (Tour 3 a échoué, mais une variante invariante sous
>      équivalence logique pourrait passer).
>    - Candidat : *quantum query lower bounds* appliqués à des problèmes
>      classiques.
>
> 4. **Test rigoureux de non-relativisation** :
>    - Exhiber un oracle `A` tel que `P^A = NP^A`.
>    - Vérifier ligne-à-ligne que la technique candidate ne tient pas
>      relativement à `A`.
>
> 5. **Test additionnel de non-algébrisation** :
>    - Exhiber un oracle algébrique `Õ`.
>    - Vérifier non-algébrisation.
>
> 6. **Application candidate** : identifier une famille de fonctions sur
>    laquelle la technique pourrait donner une borne nouvelle.
>
> Livrable : technique candidate + preuve de non-relativisation + audit
> non-algébrisation + application.

## Critères d'acceptation

* **Succès complet** : nouvelle technique non-relativisante + application
  à une séparation de classe inédite.
* **Succès partiel** : technique candidate identifiée, non-relativisation
  partiellement prouvée.
* **Échec acceptable** : audit complet des candidats + identification
  des obstacles structurels.

## Modes d'échec attendus

* Re-proposition de Shamir / Williams / Razborov-Smolensky sous forme
  déguisée.
* Technique candidate qui s'avère relativisante au test rigoureux.
* Technique non-relativisante mais algébrisante (cas Razborov-Smolensky)
  — n'aide pas pour P vs NP.

## Références à embarquer

* Baker-Gill-Solovay 1975.
* Shamir 1992, *« IP = PSPACE »*.
* Williams 2011.
* Aaronson-Wigderson 2008.
* Razborov-Smolensky 1987.
* Forster 2002 (sign-rank lower bounds).

## Conditions du cahier en vigueur

* `(b)` non-relativisant : c'est l'objet même de cette étape.
* `(c)` non-algébrisant : doit être *additionnellement* honoré.
* `(q)` audit bibliographique préemptif.
