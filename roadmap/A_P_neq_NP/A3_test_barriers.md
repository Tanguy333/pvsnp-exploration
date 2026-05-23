# Étape A.3 — Test des trois (quatre) barrières

## Objectif formel

Soit une preuve candidate $\Pi$ de $\text{size}_{\mathcal{C}}(f_n) \geq n^{\omega(1)}$
produite en A.2. Vérifier que $\Pi$ franchit explicitement chaque barrière :

* (B1) **Relativisation** (Baker-Gill-Solovay 1975).
* (B2) **Preuves naturelles** (Razborov-Rudich 1997).
* (B3) **Algébrisation** (Aaronson-Wigderson 2008).
* (B4) **Barrière monotone** (Razborov 1985 / Tardos 1988, ajoutée Tour 24
  du cahier).

Sans franchissement explicite des 4, $\Pi$ est invalide.

## Statut actuel (2026)

* Williams 2011 (NEXP ⊄ ACC⁰) est le **seul** précédent connu franchissant
  simultanément B1+B2+B3 pour une séparation de classe.
* Aucun précédent connu n'est rigoureusement à l'épreuve de B4 pour une
  séparation au-dessus du monotone.
* Les 4 barrières sont **indépendantes** : franchir l'une ne protège pas
  des autres.

## Prompt pour Claude (à coller en session neuve)

> Tu reçois une preuve candidate `Π` issue de l'étape A.2 (à fournir).
>
> Mission : auditer `Π` contre les 4 barrières.
>
> **Pour B1 (relativisation)** :
>
> 1. Exhiber un oracle `A` tel que `P^A = NP^A` (typiquement PSPACE-complet
>    sufit).
> 2. Vérifier ligne-à-ligne que `Π` ne tient *pas* relativement à `A`.
> 3. Si `Π` tient relativement à `A` → REJET, `Π` relativise.
>
> **Pour B2 (preuves naturelles)** :
>
> 1. Identifier la propriété combinatoire `P` utilisée par `Π`
>    (typiquement : « f a une borne X sur l'invariant Y »).
> 2. Vérifier (i) `P` est-elle constructive en temps polynomial sur la
>    table de vérité ? (ii) `P` est-elle vraie pour ≥ `2^{-n}` des
>    fonctions booléennes ?
> 3. Si (i) ET (ii) : `Π` est naturelle au sens RR → incompatible avec
>    crypto standard → REJET.
>
> **Pour B3 (algébrisation)** :
>
> 1. Exhiber un oracle algébrique `Õ` tel que `P^Õ = NP^Õ`.
> 2. Vérifier que `Π` n'utilise pas d'arithmétisation qui se restreint à
>    `Õ`.
> 3. Si `Π` algébrise → REJET.
>
> **Pour B4 (monotone Razborov-Tardos)** :
>
> 1. Identifier si `Π` se restreint à des circuits monotones, arithmétiques
>    monotones, tropicaux, min-plus.
> 2. Si oui : vérifier comment `Π` passe au non-monotone. Exhiber comment
>    `Π` traite la fonction de Tardos 1988 (dans P, complexité monotone
>    `exp(Ω(n^{1/6}))`).
> 3. Si `Π` n'a pas de réponse pour Tardos → REJET.
>
> Livrable : audit ligne-à-ligne, verdict B1/B2/B3/B4 chacun en {franchi /
> non-franchi / inapplicable}.

## Critères d'acceptation

* **Succès complet** : `Π` franchit B1 + B2 + B3 + B4. *Sans précédent
  pour B1+B2+B3+B4 simultanément.*
* **Succès partiel** : `Π` franchit 3 sur 4. Williams 2011 = précédent.
* **Échec acceptable** : audit identifie précisément laquelle des
  barrières tue `Π` et propose une variante candidate.

## Modes d'échec attendus

* `Π` relativise (cas Tour 1, Kt).
* `Π` algébrise (cas Tour 2, Ax-Katz).
* `Π` est naturelle (cas Tours 6 — invariants topologiques larges).
* `Π` est implicitement monotone (cas Tour 24, tropical).

## Références à embarquer

* Baker-Gill-Solovay 1975, *« Relativizations of the P =? NP question »*.
* Razborov-Rudich 1997, *« Natural proofs »*.
* Aaronson-Wigderson 2008, *« Algebrization »*.
* Razborov 1985 + Tardos 1988.
* Williams 2011 (le précédent).

## Conditions du cahier en vigueur

* `(b)`, `(c)` et test Tardos `(§4 q.14)` doivent être *prouvés*, pas
  *revendiqués* (cas Tours 4, 11, 24 qui revendiquaient sans prouver).
