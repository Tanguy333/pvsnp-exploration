# Étape C.4 — Extension du programme Williams (NEXP ⊄ ACC⁰ → NEXP ⊄ TC⁰ → NP ⊄ P/poly)

## Objectif formel

Étendre la méthode algorithmique de Williams 2011 (qui a prouvé
NEXP $\not\subset$ ACC⁰) à :
* (i) NEXP $\not\subset$ TC⁰, puis
* (ii) NEXP $\not\subset$ P/poly, puis
* (iii) NP $\not\subset$ P/poly (par hardness magnification).

Williams 2011 reste **l'unique séparation non-relativisante et
non-algébrisante** en haut de la hiérarchie. Son extension à TC⁰ et au-delà
est l'effort de recherche le plus actif en complexité depuis 2011.

## Statut actuel (2026)

* Williams 2011 : NEXP $\not\subset$ ACC⁰. Méthode = combinaison
  *algorithme CAPP non-trivial pour ACC⁰* + *théorème d'effondrement*
  (« si NEXP $\subset$ ACC⁰, alors un algorithme NTIME($2^n$) plus rapide
  que $2^n / n^{\omega(1)}$ existe pour SAT »).
* **Obstacle TC⁰** : il n'existe pas d'algorithme CAPP non-trivial pour
  TC⁰. La meilleure tentative (Tamaki, Chen, Servedio) reste insuffisante.
* **Obstacle P/poly** : encore plus dur. Même si CAPP TC⁰ marchait, le
  passage à P/poly demande un saut additionnel.
* **Hardness magnification** : Oliveira-Pich, McKay-Murray-Williams,
  Chen-Hirahara-Oliveira-Pich-Rajgopal-Santhanam 2019 (« Beyond Natural
  Proofs ») — programme qui *amplifie* de petites bornes en grandes,
  mais limites internes documentées.

## Prompt pour Claude (à coller en session neuve)

> Tu es chercheur sur la méthode algorithmique de Williams.
>
> Mission : avancer (même partiellement) sur l'extension NEXP $\not\subset$
> ACC⁰ → NEXP $\not\subset$ TC⁰.
>
> Procédure :
>
> 1. **Comprendre la structure de Williams 2011** :
>    - Algorithme CAPP pour ACC⁰ : Beigel-Tarui 1994 + Allender-Gore
>      simulation par polynômes en degré.
>    - Théorème d'effondrement : Impagliazzo-Kabanets-Wigderson 2002 +
>      raffinements.
>    - Comment Williams combine les deux.
>
> 2. **Identifier le goulot pour TC⁰** :
>    - Pourquoi Beigel-Tarui ne marche pas pour TC⁰ ? (le degré du
>      polynôme représentant explose : `weight L1` au lieu de
>      `magnitude L∞` — cf. Tour 23 du cahier).
>    - Quelles tentatives ont été faites depuis 2010 ?
>      (Tamaki 2014, Chen 2018, Servedio-Tan 2018, ...).
>
> 3. **Proposer une attaque** :
>    - Soit (a) trouver un algorithme CAPP non-trivial pour TC⁰ par
>      *nouvelle technique* (par exemple, exploiter la structure
>      symmetric polynomial de TC⁰ d=2).
>    - Soit (b) montrer que le théorème d'effondrement marche avec un
>      algorithme CAPP plus faible (réduire la qualité requise).
>    - Soit (c) hybridation avec hardness magnification : si on prouve
>      qu'une fonction *sparse* est dure dans TC⁰, on amplifie.
>
> 4. **Test des barrières** :
>    - Relativisation : la méthode de Williams est non-relativisante
>      *par construction* (utilise l'arithmétisation Beigel-Tarui +
>      énumération non-triviale).
>    - RR : la propriété « avoir un petit circuit TC⁰ » est large, mais
>      Williams contourne via méta-réduction.
>    - Algébrisation : Aaronson-Wigderson 2008 montre que Williams 2011
>      n'algébrise PAS. À auditer pour l'extension TC⁰.
>    - Tardos 1988 : sans objet car TC⁰ n'est pas monotone.
>
> 5. **Si bloqué** : identifier précisément l'invention manquante (renvoie
>    section D).
>
> Livrable : audit du gap TC⁰ + proposition d'attaque + audit barrières.

## Critères d'acceptation

* **Succès complet** : NEXP $\not\subset$ TC⁰ prouvé. *Jalon historique.*
* **Succès partiel** : nouveau résultat de hardness magnification
  applicable à TC⁰.
* **Échec acceptable** : cartographie précise du gap algorithmique CAPP
  pour TC⁰.

## Modes d'échec attendus

* Re-proposer la même technique Beigel-Tarui qui ne marche pas
  (folklore après 2014).
* Confondre TC⁰ d=2 (bond dimension exponentielle, Hajnal-Maass-Pudlák-Szegedy
  1993) et TC⁰ général.
* Hardness magnification mal appliquée (« Beyond Natural Proofs » a
  documenté ses limites).

## Références à embarquer

* Williams 2011, *« Non-uniform ACC circuit lower bounds »*.
* Beigel-Tarui 1994, *« On ACC »*.
* Tamaki 2014, *« A satisfiability algorithm for depth-2 circuits with
  a symmetric gate »*.
* Chen 2018+, McKay-Murray-Williams 2019.
* Chen-Hirahara-Oliveira-Pich-Rajgopal-Santhanam 2019, *« Beyond
  Natural Proofs »*.
* Murray-Williams 2018+.

## Conditions du cahier en vigueur

* `(a)`, `(b)`, `(c)`, `(f)`, `(q)` toutes en vigueur.
* **Test du Tour 4** : pour invoquer Williams, il faut une *contribution
  algorithmique nouvelle*, pas une « stratégie globale ».
