# Étape A.4 — Déduction $P \neq NP$ à partir de la borne inférieure

## Objectif formel

Étant donné une preuve $\Pi$ validée en A.2 et auditée en A.3, conclure
rigoureusement $P \neq NP$ (ou $NP \not\subseteq P/poly$ selon variante).

Chaîne logique :

1. $f_n \in NP$ (typiquement par construction : $f_n$ choisie NP-complète
   en A.1).
2. $f_n \notin \mathcal{C}_n$ (par A.2 + A.3 validés).
3. $P \subseteq \mathcal{C}_n$ (par construction de $\mathcal{C}_n$ en A.1).
4. **Donc** $f_n \notin P$, ce qui donne $NP \not\subseteq P$, soit
   $P \subsetneq NP$.

## Statut actuel (2026)

* Étape *purement déductive* — triviale **si** A.1 a fixé
  $\mathcal{C}_n \supseteq P$ et A.2-A.3 sont valides.
* Subtilité : $\mathcal{C}_n = P/poly$ donne $NP \not\subseteq P/poly$
  qui implique $P \subsetneq NP$ (car $P \subseteq P/poly$).
* Si $\mathcal{C}_n =$ machines de Turing déterministes uniformes en
  temps $n^k$ : ne donne *que* $f \notin DTIME(n^k)$, donc $P \neq NP$
  exige une borne valable pour *tout* $k$ (= borne non-uniforme).

## Prompt pour Claude (à coller en session neuve)

> Tu reçois `(f_n, C_n, Π)` validés en A.1-A.3.
>
> Mission : effectuer la déduction `f_n ∈ NP ∧ f_n ∉ C_n ∧ P ⊆ C_n ⟹ P ≠ NP`
> de manière rigoureuse, en explicitant chaque inclusion.
>
> Procédure :
>
> 1. Prouver `f_n ∈ NP` :
>    - Si `f_n` est NP-complète par réduction depuis SAT, citer la
>      réduction (typiquement Karp 1972).
>    - Vérifier que la réduction est polynomiale **et** que les certificats
>      passent par la réduction.
>
> 2. Rappeler `f_n ∉ C_n` (par A.2 + A.3).
>
> 3. Prouver `P ⊆ C_n` :
>    - Si `C_n = P/poly` : trivial par définition (toute MT déterministe
>      polynomiale a un circuit Boolean polynomial uniforme).
>    - Si `C_n` plus restreint : justifier l'inclusion.
>
> 4. Conclure `f_n ∉ P` (par contraposée de `P ⊆ C_n` et `f_n ∉ C_n`).
>
> 5. Conclure `P ⊊ NP` : `f_n ∈ NP \ P`.
>
> 6. **Sanity check** : vérifier qu'il n'y a pas d'erreur d'uniformité
>    cachée (cas Williams 2011 : NEXP ⊄ ACC⁰ ne donne *pas* directement
>    NP ⊄ ACC⁰).
>
> Livrable : déduction formelle (≤ 600 mots) avec chaque inclusion citée
> et chaque réduction explicitée.

## Critères d'acceptation

* **Succès complet** : déduction rigoureuse, P ≠ NP établi.
  *Conditionnel à A.2-A.3 succès complet.*
* **Succès partiel** : déduction conditionnelle (« si A.2 réussit, alors
  P ≠ NP par cette chaîne »).
* **Échec acceptable** : identification d'un gap d'uniformité ou d'une
  ambiguïté de classe.

## Modes d'échec attendus

* Confusion uniforme/non-uniforme (Williams 2011 ne donne pas P ≠ NP
  directement, malgré l'apparence).
* Mauvais choix de `C_n` (e.g. `C_n = P` uniforme rend l'étape 3 fausse :
  une borne uniforme ne suffit pas, il faut non-uniforme).
* Réduction polynomiale floue : `f_n` revendiquée NP-complète mais sans
  réduction Karp explicite.

## Références à embarquer

* Karp 1972, *« Reducibility among combinatorial problems »*.
* Sipser, *Introduction to the Theory of Computation* (sections sur
  P/poly et uniformité).
* Williams 2011 (pour comprendre le gap uniforme/non-uniforme).

## Conditions du cahier en vigueur

* `(k)` lien à P vs NP : *automatique* par construction de cette étape.
* `(g)` encodage non-trivialisant : vérifier la réduction Karp.
