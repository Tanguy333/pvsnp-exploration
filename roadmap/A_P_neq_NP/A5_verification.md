# Étape A.5 — Vérification externe et formalisation

## Objectif formel

Soumettre la preuve $\Pi$ (validée A.2-A.3-A.4) à vérification externe :

* (V1) Soumission à conférence/journal majeur (STOC, FOCS, JACM, SICOMP).
* (V2) Peer review par 3-5 experts indépendants.
* (V3) Formalisation mécanique (Lean, Coq, Isabelle) — recommandée mais
  pas obligatoire historiquement, **devenue standard de fait** depuis
  PrimeCheck / Liquid Tensor / 4-Color Theorem.

## Statut actuel (2026)

* Aucune preuve P vs NP n'a passé V1+V2.
* ~100 prétentions P vs NP soumises à arXiv par an, ~0 retenues.
* arXiv a une catégorie *« P vs NP claims »* informellement modérée.
* Formalisation Lean de bornes inférieures de circuit : embryonnaire
  (Mathlib4 n'a pas encore de cadre standard).

## Prompt pour Claude (à coller en session neuve)

> Tu reçois `Π` validée A.1-A.4 (à fournir).
>
> Mission : préparer `Π` pour soumission externe selon standards
> académiques contemporains.
>
> Procédure :
>
> 1. **Pré-vérification interne** :
>    - Re-lire `Π` en simulant le rôle d'un reviewer hostile.
>    - Identifier 5 questions/objections les plus probables.
>    - Préparer une réponse à chacune.
>
> 2. **Comparaison à la littérature** :
>    - Vérifier qu'aucune partie de `Π` n'est implicitement folklore
>      (audit type Tour 12 / 14 / 19 du cahier).
>    - Identifier l'apport *strictement nouveau* en termes de :
>      (a) technique introduite, (b) lemme prouvé, (c) classe séparée.
>
> 3. **Formalisation Lean** :
>    - Identifier les 3-5 lemmes centraux de `Π`.
>    - Esquisser leur formalisation Lean 4 / Mathlib4
>      (définitions, énoncés, plan de preuve).
>    - Si Mathlib4 manque les définitions de base (circuits booléens,
>      classes de complexité), identifier les définitions à introduire.
>
> 4. **Préparation de soumission** :
>    - Titre, abstract, intro, structure du papier.
>    - Mention explicite des 4 barrières franchies et comment.
>    - Comparaison à Williams 2011 (le seul précédent comparable).
>
> Livrable : document de soumission de 15-30 pages, avec section
> formalisation Lean en annexe.

## Critères d'acceptation

* **Succès complet** : `Π` acceptée à STOC/FOCS, formalisée Lean.
  *Sans précédent.*
* **Succès partiel** : soumission préparée, reviews reçues, révisions
  itératives.
* **Échec acceptable** : reviewers identifient une faille rédhibitoire,
  retour à A.2 ou A.3.

## Modes d'échec attendus

* Reviewer 1 trouve un cas oublié dans la borne inférieure.
* Reviewer 2 trouve un oracle qui réfute la non-relativisation.
* Reviewer 3 trouve un papier antérieur prouvant l'équivalent (folklore).
* Formalisation Lean révèle une assomption tacite non-justifiée.

## Références à embarquer

* Brunerie 2016, *« On the homotopy groups of spheres in homotopy type
  theory »* (exemple de formalisation pour vérification mathématique).
* Avigad 2023+, *« Mathematics in Lean »*.
* PrimeCheck (Mathlib).
* Liquid Tensor Experiment (Scholze + community).

## Conditions du cahier en vigueur

* Toutes les conditions `(a)-(r)` doivent rester honorées dans la
  rédaction finale.
* **Nouvelle condition implicite pour V3** : tout lemme central doit être
  formalisable. Si Mathlib4 manque les définitions, c'est un sous-projet.
