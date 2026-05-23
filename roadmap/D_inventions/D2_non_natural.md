# Étape D.2 — Inventer une preuve non-naturelle (échapper à Razborov-Rudich)

## Objectif formel

Trouver une technique de borne inférieure $\tau$ qui utilise une propriété
combinatoire $\mathcal{P}$ telle que **au moins une** des deux conditions
de RR est *violée* :

* (RR1) $\mathcal{P}$ n'est pas calculable en temps polynomial sur la
  table de vérité (`non-constructive`).
* (RR2) $\mathcal{P}$ n'est pas vraie pour ≥ $2^{-n}$ des fonctions
  booléennes (`non-large`).

## Statut actuel (2026)

* La plupart des bornes connues utilisent des propriétés *naturelles*
  (constructives + larges) — donc bloquées par RR.
* Exceptions :
  * **Williams 2011** : utilise une énumération non-constructive (parcours
    de programmes), donc RR ne s'applique pas. C'est *non-naturel*.
  * **Hardness magnification** : la propriété « `f` est dur sur instances
    clairsemées » est *non-large* (peu de fonctions sont sparse).
  * **GCT** : la propriété « `f` a une certaine orbite de représentations »
    est *non-constructive* (calculer les multiplicités est PSPACE-dur).

## Prompt pour Claude (à coller en session neuve)

> Tu es chercheur sur la barrière des preuves naturelles.
>
> Mission : identifier ou inventer une propriété `P` qui (i) sert à
> prouver une borne inférieure non-triviale, (ii) viole au moins une des
> deux conditions de RR.
>
> Procédure :
>
> 1. **Choisir le mode de violation** :
>    - (a) Violer la **constructivité** : `P` doit être indécidable ou
>      PSPACE-hard ou EXP-hard à calculer.
>    - (b) Violer la **largeur** : `P` doit caractériser une classe
>      étroite de fonctions (taille `≤ 2^{(1-ε) 2^n}` pour grand `ε`).
>
> 2. **Pour (a) — propriétés non-constructives** :
>    - Candidats : « `f` a Kolmogorov-complexité super-polynomiale »
>      (indécidable), « `f` est dans `BPP^{SAT}` mais pas `P^{SAT}` »
>      (PSPACE-dur), Kt-complexity, GCT multiplicities.
>    - Risque : la propriété peut être *si* non-constructive qu'on ne
>      peut pas l'utiliser pour prouver quoi que ce soit (Tour 1 — Kt).
>
> 3. **Pour (b) — propriétés non-larges** :
>    - Candidats : « `f = SAT_n` » (une seule fonction → trivialement
>      non-large), « `f` est dans une famille spécifique » (Tour 14 MAJ,
>      Tour 19 essentialité — toutes non-larges).
>    - Risque : la propriété peut être *trop* étroite pour donner une
>      borne universelle (cas Tours 12-20 : non-larges mais
>      asymptotiquement faibles).
>
> 4. **Test rigoureux** :
>    - Constructivité : calculer explicitement la complexité de tester
>      `P(T)` sur table de vérité `T`. Si `≤ poly(2^n)` : *constructive*.
>      Si `≥ exp(2^n)` ou indécidable : *non-constructive*.
>    - Largeur : compter (ou borner) la fraction de fonctions
>      satisfaisant `P`. Si `≥ 2^{-n}` : *large*. Si `≤ 2^{-c n}` pour
>      `c > 1` : *non-large*.
>
> 5. **Application** : exhiber une famille de fonctions `f_n` et une
>    borne inférieure dérivée de `P`.
>
> Livrable : propriété `P` + audit (a)/(b) + application.

## Critères d'acceptation

* **Succès complet** : nouvelle propriété + nouvelle borne inférieure
  super-polynomiale.
* **Succès partiel** : propriété candidate + analyse rigoureuse de sa
  violation de RR.
* **Échec acceptable** : audit des candidats existants
  (Williams, GCT, MCSP-based, ...) + identification du gap.

## Modes d'échec attendus

* Propriété indécidable (Kt) qui ne peut pas être utilisée — Tour 1.
* Propriété non-large mais asymptotiquement faible — Tours 12-20 (folklore).
* Propriété revendiquée non-naturelle mais en réalité constructive (cas
  fréquent : la constructivité est sous-estimée).

## Références à embarquer

* Razborov-Rudich 1997.
* Naor-Reingold 1997 (one-way functions et conséquences).
* Williams 2014, *« Natural Proofs versus Derandomization »*.
* Chen-Hirahara-Oliveira-Pich-Rajgopal-Santhanam 2019, *« Beyond
  Natural Proofs »*.
* Allender 2021 surveys on meta-complexity.

## Conditions du cahier en vigueur

* `(b)` non-relativisant + RR : c'est l'objet.
* `(j)` test empirique : compter la fraction de fonctions à `n=4, 5` au
  moins.
* `(q)` audit biblio.
