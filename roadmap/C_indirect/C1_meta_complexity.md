# Étape C.1 — Méta-complexité (Hirahara, Williams) : NP-hardness de MCSP

## Objectif formel

Prouver que MCSP (Minimum Circuit Size Problem — étant donné une table de
vérité $T$ et un seuil $s$, décider si la fonction représentée par $T$ a
un circuit de taille $\leq s$) est NP-hard.

Si MCSP est NP-hard, alors :
* $MCSP \in P \Rightarrow P = NP$ (par définition de NP-hardness).
* La méta-complexité (complexité du problème de prouver des bornes
  inférieures) est elle-même NP-hard.

## Statut actuel (2026)

* MCSP $\in NP$ (trivial : on devine le circuit, on vérifie).
* MCSP NP-hard : **ouvert**.
* Hirahara 2018-2024 : proved many partial results, conditional reductions.
* Williams 2010s : hardness magnification — si MCSP est dur sur des
  instances « clairsemées », alors NP $\not\subset$ P/poly.
* Connection à one-way functions (Liu-Pass 2020).

## Prompt pour Claude (à coller en session neuve)

> Tu es chercheur en méta-complexité. Mission : avancer sur la
> NP-hardness de MCSP, ou identifier précisément le gap actuel.
>
> Procédure :
>
> 1. **Auditer l'état du programme Hirahara-Williams** :
>    - Quels sous-cas de MCSP sont NP-hard ?
>      (MKtP, GapMCSP, MCSP sur fonctions partielles, etc.)
>    - Quelles réductions conditionnelles existent ?
>    - Quels obstacles sont identifiés ?
>
> 2. **Identifier le gap principal** :
>    - Typiquement : passer de MKtP (Minimum Kt Problem) à MCSP exige une
>      réduction polynomiale de l'un à l'autre, qui est ouverte.
>    - Le passage du conditional (« MCSP NP-hard si crypto existe ») à
>      l'inconditionnel.
>
> 3. **Proposer une attaque** :
>    - Choisir un sous-cas où le gap semble réductible.
>    - Esquisser la réduction Karp candidate.
>    - Vérifier que la réduction est polynomiale et préserve les seuils
>      `s` de la définition MCSP.
>
> 4. **Test des barrières** :
>    - MCSP NP-hard implique-t-il des conséquences relativisantes ? Oui
>      (BGS), donc preuve obligatoirement non-relativisante.
>    - RR : la propriété « `T` a un petit circuit » est large
>      *si* on prouve qu'une fraction non-négligeable de fonctions a
>      petit circuit — ce qui contredit Shannon 1949.
>      Donc la propriété est *naturellement* anti-large (RR ne s'applique pas).
>
> 5. **Conséquences si MCSP est NP-hard** :
>    - Quelles séparations de classes deviennent inconditionnelles ?
>
> Livrable : audit + sous-cas ciblé + attaque candidate + audit barrières.

## Critères d'acceptation

* **Succès complet** : MCSP NP-hard prouvé inconditionnellement.
  *Sans précédent, jalon majeur.*
* **Succès partiel** : sous-cas non-trivial prouvé NP-hard (e.g. MKtP
  prouvé NP-hard inconditionnellement).
* **Échec acceptable** : cartographie du gap + sous-lemme à attaquer.

## Modes d'échec attendus

* Re-prouver Hirahara 2018 (folklore après 2018).
* Réduction conditionnelle revendiquée inconditionnelle.
* Confusion MCSP / GapMCSP / MKtP (les 3 ne sont *pas* équivalents).

## Références à embarquer

* Kabanets-Cai 2000 (MCSP introduction).
* Allender-Buhrman-Koucký 2008 (MKtP).
* Hirahara 2018, *« Non-black-box worst-case to average-case reductions
  within NP »*.
* Hirahara-Loff-Williams (2018-2024 series).
* Liu-Pass 2020 (MCSP and one-way functions).

## Conditions du cahier en vigueur

* `(b)`, `(c)`, `(q)`, `(r)` toutes en vigueur.
* La condition `(k)` est ici **substantielle** : MCSP NP-hard $\Rightarrow$
  P ≠ NP est un théorème classique, pas une revendication.
