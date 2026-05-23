# Étape D.5 — Passage monotone → non-monotone (franchir Tardos 1988)

## Objectif formel

Trouver une technique $\tau$ qui :

* (MN1) Permet de prouver une borne inférieure sur les circuits
  **monotones** d'une fonction $f$.
* (MN2) **Passe au non-monotone** : la même technique (ou une variante
  serrée) donne une borne inférieure sur les circuits non-monotones de
  $f$ (ou d'une fonction proche).

La fonction de **Tardos 1988** est le contre-exemple structurel : dans
$P$, mais complexité monotone $\exp(\Omega(n^{1/6-o(1)}))$. Toute
technique $\tau$ candidate doit échouer sur Tardos (sinon elle donnerait
une fausse borne).

## Statut actuel (2026)

* **Razborov 1985** : CLIQUE_n a complexité monotone
  $\exp(\Omega(\sqrt{n/\log n}))$. **Ne passe pas au non-monotone**.
* **Tardos 1988** : fonction explicite (Lovász θ-function based) dans P,
  complexité monotone $\exp(\Omega(n^{1/6}))$. Tue tout passage naïf.
* **Karchmer-Wigderson 1990** : profondeur monotone = complexité de
  communication du jeu KW. Passage au non-monotone reste ouvert.
* **Programme de Göös-Pitassi-Watson 2018** sur lifting : monotone
  formulas → general formulas, mais préserve le gap monotone-vs-non-monotone.

## Prompt pour Claude (à coller en session neuve)

> Tu es chercheur sur la barrière monotone Razborov-Tardos.
>
> Mission : identifier une technique $\tau$ qui (MN1) prouve une borne
> monotone *et* (MN2) passe au non-monotone, en franchissant Tardos 1988.
>
> Procédure :
>
> 1. **Comprendre Tardos 1988** :
>    - La fonction Tardos est basée sur la θ-fonction de Lovász, qui est
>      calculable en temps polynomial via SDP (Grötschel-Lovász-Schrijver).
>    - La complexité monotone est exponentielle car la monotonie force
>      à explorer la combinatoire de tous les sous-ensembles.
>    - **Le passage NON-monotone exploite la possibilité de négation
>      cachée**, ce qui change radicalement la nature du calcul.
>
> 2. **Identifier la « source » du gap monotone-non-monotone** :
>    - Toute fonction `f` peut être écrite comme `f = (f_+) ⊕ (f_-)` où
>      `f_+` est monotone et `f_-` capture les corrections par négation.
>    - Pour Tardos `f`, `f_-` est polynomial même si `f_+` est
>      exponentiel.
>    - Toute technique monotone capturera `f_+` mais pas `f_-`.
>
> 3. **Stratégies possibles** :
>    - (a) Identifier une famille de fonctions où `f_- ≡ 0` (ou très
>      simple). Par exemple : fonctions monotones *fortement
>      symétriques* (sans corrections par négation).
>    - (b) Inventer une mesure de complexité qui *additionne* `f_+` et
>      `f_-` honnêtement.
>    - (c) Approche via formules de Karchmer-Wigderson : la
>      communication game pour `f` non-monotone est plus restrictive,
>      mais pas suffisamment.
>    - (d) Approche via *quantum* communication ou *parity* circuits
>      (XOR au lieu de OR).
>
> 4. **Test obligatoire** :
>    - Pour toute technique candidate `τ`, vérifier qu'elle ne donne
>      *pas* une borne exponentielle sur Tardos 1988.
>    - Si la borne sur Tardos via `τ` est polynomiale ou sub-exponentielle,
>      `τ` survit. Si elle est exponentielle, `τ` est invalide
>      (faux positif).
>
> 5. **Application** : famille candidate `f_n` non-monotone où `τ`
>    donne une borne nouvelle.
>
> Livrable : technique candidate + audit Tardos + application.

## Critères d'acceptation

* **Succès complet** : technique `τ` MN1 + MN2 + franchit Tardos +
  application non-triviale. *Sans précédent.*
* **Succès partiel** : technique passant Tardos sur sous-famille
  spécifique.
* **Échec acceptable** : audit complet des candidats + identification
  de la raison structurelle de l'impossibilité.

## Modes d'échec attendus

* Technique `τ` qui donne une borne exponentielle sur Tardos → invalide.
* Technique qui s'effondre dans le non-monotone (Razborov 1985 pur).
* Confondre monotone formula vs monotone circuit (KW capture formula,
  pas circuit).

## Références à embarquer

* Razborov 1985, *« Lower bounds on the monotone complexity of some
  Boolean functions »*.
* Tardos 1988, *« The gap between monotone and non-monotone circuit
  complexity is exponential »*.
* Karchmer-Wigderson 1990.
* Göös-Pitassi-Watson 2018 (lifting).
* Cavalar-Göös 2025, *« Monotone Circuit Complexity of Matching »*
  (ECCC TR25-102).
* Jukna *Boolean Function Complexity* (2012), chapitres sur monotone.

## Conditions du cahier en vigueur

* §1 4e barrière : monotone Razborov-Tardos.
* §4 q.14 : test Tardos 1988 obligatoire.
* `(b)`, `(c)`, `(q)`, `(r)` toutes en vigueur.
