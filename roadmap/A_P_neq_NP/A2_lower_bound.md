# Étape A.2 — Borne inférieure non-triviale $\text{size}_{\mathcal{C}}(f_n) \geq n^{\omega(1)}$

## Objectif formel

Étant donné `(f_n, C_n)` fixé en A.1, prouver une borne inférieure de
taille super-polynomiale (ou idéalement $2^{n^{\Omega(1)}}$ exponentielle)
sur la complexité de $f_n$ dans la classe $\mathcal{C}_n$, **sans
contrainte d'uniformité**.

## Statut actuel (2026)

* **Connu** :
  * AC⁰ : $\text{size}_{AC^0_d}(\text{PARITY}_n) \geq 2^{\Omega(n^{1/(d-1)})}$
    (Håstad 1986).
  * AC⁰[p] (p premier) : Razborov 1987, Smolensky 1987.
  * NEXP ⊄ ACC⁰ (Williams 2011) — *seul* exemple non-uniforme
    non-relativisant et non-algébrisant en haut de la hiérarchie.
* **Ouvert** :
  * TC⁰ : aucune borne inférieure super-polynomiale pour fonction explicite.
  * NC¹ : aucune borne sur P/poly (équivalent à $\text{NC}^1 \subsetneq P/poly$).
  * P/poly : NP ⊂ P/poly est ouvert ; séparation directe = P vs NP.

## Prompt pour Claude (à coller en session neuve)

> Tu es un chercheur en bornes inférieures de circuit. Tu reçois le couple
> `(f_n, C_n)` validé en étape A.1 (à fournir dans le message d'amorce).
>
> Mission : exhiber une technique de borne inférieure
> `size_C(f_n) >= n^{w(1)}` (idéalement `2^{n^{Omega(1)}}`).
>
> Procédure attendue :
>
> 1. **Auditer les techniques connues** applicables à `C_n` :
>    Switching Lemma (Håstad), méthode polynomiale (Razborov-Smolensky),
>    méthode algorithmique (Williams), approximation par polynômes,
>    communication complexity (KW), discrepancy, rang, sign-rank, etc.
> 2. **Identifier la barrière naturelle qui bloque chacune** sur `C_n`.
>    *Exemple : pour TC⁰, Hajnal-Maass-Pudlák-Szegedy 1993 ferme la voie
>    communication ; pour NC¹, KKL fixe la difficulté.*
> 3. **Proposer une variante hybride** ou un sous-problème tractable où
>    une borne partielle serait nouvelle. Argumenter pourquoi cette
>    variante n'est pas couverte par les barrières §1 du cahier.
> 4. **Identifier explicitement l'invention nécessaire** (renvoyer vers
>    section D si applicable).
>
> Livrable (≤ 1500 mots) :
>
> * Tableau des 5-8 techniques connues × leur statut sur `C_n`.
> * Identification précise de l'ingrédient manquant.
> * Sous-problème tractable proposé (sous-classe de `C_n`, ou
>   sous-famille de `f_n`).
> * Auto-aveu honnête si la session ne peut pas faire mieux que cataloguer.

## Critères d'acceptation

* **Succès complet** : nouvelle borne inférieure prouvée. *Improbable*
  (problème ouvert depuis 40+ ans pour la plupart des classes).
* **Succès partiel** : cartographie rigoureuse des techniques connues +
  identification du gap. *Réalisable, utile pour le dépôt.*
* **Échec acceptable** : la session conclut « inventaire complet, aucune
  technique connue ne fonctionne, voici les inventions D.x requises ».

## Modes d'échec attendus

* Re-prouver folklore (e.g. PARITY ∉ AC⁰ d=2 — déjà Tour 12).
* Proposer une « hybridation » qui réintroduit un objet relativisant
  (Tour 1) ou algébrisant (Tour 2).
* Proposer une borne pour une sous-classe triviale (e.g. circuits
  monotones — Tardos 1988 ferme).

## Références à embarquer

* Furst-Saxe-Sipser 1981, *« Parity, circuits, and the polynomial-time
  hierarchy »*.
* Håstad 1986, *« Almost optimal lower bounds for small depth circuits »*.
* Razborov 1985, Smolensky 1987.
* Williams 2011 + Williams 2014 *(« Natural proofs versus derandomization »)*.
* Aaronson-Wigderson 2008 (algébrisation).
* Allender 2014 surveys.
* Cavalar-Göös 2025 (monotone matching).

## Conditions du cahier en vigueur

* `(b)`, `(c)`, `(q)`, `(r)`, et le test Tardos 1988 (§4 q.14).
* `(a)` classe restreinte explicite.
* `(g)` encodage non-trivialisant.
