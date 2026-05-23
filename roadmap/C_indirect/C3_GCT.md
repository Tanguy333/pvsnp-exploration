# Étape C.3 — Geometric Complexity Theory (Mulmuley-Sohoni)

## Objectif formel

Programme GCT : prouver $\text{perm}_n \neq \text{det}_m$ pour tout
$m = \text{poly}(n)$ (permanent vs déterminant), ce qui impliquerait
$\text{VP} \neq \text{VNP}$ (équivalent algébrique de $P \neq NP$).

Méthode : théorie des représentations de $GL_{n^2}$ et géométrie
algébrique des variétés d'orbites.

## Statut actuel (2026)

* **Mulmuley-Sohoni 2001-2008** : programme initial. Cible : montrer
  que la variété d'orbite du permanent contient une représentation
  irréductible que la variété d'orbite du déterminant ne contient pas.
* **Bürgisser-Ikenmeyer-Panova 2017** : l'approche par *occurrences*
  (compter les multiplicités de représentations irréductibles) ne peut
  pas marcher — il existe des classes pour lesquelles les multiplicités
  coïncident.
* **Programme survit** : alternatives via positivity, équations
  fonctionnelles, etc. Mais aucune piste claire depuis 2017.
* GCT est *non-relativisant* et *non-algébrisant* en principe, mais
  reste à voir si cela tient pour les versions raffinées.

## Prompt pour Claude (à coller en session neuve)

> Tu es chercheur en théorie des représentations et géométrie algébrique
> appliquée à la complexité.
>
> Mission : avancer sur GCT post-2017 (après le résultat négatif
> Bürgisser-Ikenmeyer-Panova).
>
> Procédure :
>
> 1. **Auditer l'état post-2017** :
>    - Quelles approches alternatives ont émergé ?
>      (positivity, équations fonctionnelles, GCT-VI, etc.)
>    - Quels résultats positifs ont été obtenus en complexité algébrique
>      depuis 2017 ? (Forbes-Shpilka, Limaye-Srinivasan-Tavenas 2022 sur
>      VNP ⊄ VP[set-multilinear], etc.)
>
> 2. **Cibler un sous-théorème accessible** :
>    - Par exemple : montrer que `perm_n` n'est pas dans la classe
>      `VP[depth-d set-multilinear formulas]` pour un `d` raisonnable.
>    - Limaye-Srinivasan-Tavenas 2022 a déjà prouvé un résultat de ce
>      type pour `d = log log n` — étendre à `d = log n` ?
>
> 3. **Test des barrières** :
>    - Relativisation : GCT n'a pas vraiment de notion d'oracle car les
>      objets sont des polynômes, pas des fonctions booléennes. La
>      barrière BGS est *probablement* contournée structurellement,
>      mais à vérifier.
>    - RR : GCT manipule des polynômes algébriques, pas des invariants
>      combinatoires constructifs. *Probablement* anti-natural au sens
>      RR.
>    - Algébrisation AW : c'est *exactement* le type de barrière qui
>      vise GCT. Aaronson-Wigderson 2008 montre que les techniques
>      d'arithmétisation classique algébrisent. GCT échappe ? À vérifier.
>
> 4. **Pivot vers P vs NP** : `perm_n ≠ det_poly` implique `VP ≠ VNP`,
>    qui sous l'hypothèse `GRH` implique `P ≠ NP/poly`. Le passage est
>    *conditionnel* à GRH.
>
> Livrable : audit post-2017 + cible sous-théorème + audit barrières
> rigoureux (en particulier algébrisation).

## Critères d'acceptation

* **Succès complet** : `perm ≠ det` prouvé. *Jalon historique.*
* **Succès partiel** : nouveau résultat sur VP/VNP / set-multilinear /
  permanent.
* **Échec acceptable** : audit complet du front post-2017 + identification
  du gap structural.

## Modes d'échec attendus

* Approche par occurrences (déjà fermée par BIP 2017).
* Calcul de multiplicités explicites trop coûteux.
* Approche oubliant que `VP ≠ VNP` *n'implique pas* `P ≠ NP`
  inconditionnellement.

## Références à embarquer

* Mulmuley-Sohoni 2001, 2008 (programme initial).
* Bürgisser-Ikenmeyer-Panova 2017, *« No occurrence obstructions in
  geometric complexity theory »*.
* Limaye-Srinivasan-Tavenas 2022, *« Superpolynomial Lower Bounds
  Against Low-Depth Algebraic Circuits »*.
* Garg-Ikenmeyer-Makam-Mulmuley-Wigderson 2019.
* Saptharishi survey on arithmetic circuit complexity.

## Conditions du cahier en vigueur

* `(b)`, `(c)`, `(q)` toutes en vigueur.
* Algébrisation `(c)` est **critique** pour GCT : à auditer rigoureusement.
