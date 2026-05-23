# Cahier de bord — Exploration P vs NP

> Document vivant. À joindre en contexte à **chaque** tour, pour le Proposeur comme pour le Réfuteur.
> Règle d'or : on ne réexplore jamais une impasse déjà documentée. On mesure le progrès par la compréhension accumulée, pas par « a-t-on la preuve ».

---

## 0. Méta

- **Question** : tout problème dont une solution candidate est vérifiable en temps polynomial est-il aussi résoluble en temps polynomial ? (P vs NP)
- **Direction choisie** : séparation **P ≠ NP**, via une classe restreinte à structure algébrique/géométrique ; cadre principal = complexité descriptive, ouverture GCT ; outils encouragés = méta-complexité / Kolmogorov.
- **Démarré le** : 2026-05-23
- **Dernière mise à jour** : 2026-05-23 (fin tour 3)
- **Nombre de tours effectués** : 3

---

## 1. Barrières connues (à garder sous les yeux en permanence)

| Barrière | En une ligne | Statut dans notre exploration |
|---|---|---|
| Relativisation (Baker–Gill–Solovay) | Une preuve qui « relativise » ne peut pas trancher P vs NP. | **ACTIVE** — a tué la piste 1. Tout outil relativisant (Kt, auto-réductibilité, recherche↔décision) est suspect. Exiger des techniques non-relativisantes (ex. arithmétisation à la Williams). |
| Preuves naturelles (Razborov–Rudich) | Les bornes inférieures « naturelles » échouent sous hypothèses cryptographiques standard. | Pertinente uniquement pour les arguments de type table de vérité / circuit. Ne s'applique pas aux arguments purement informationnels — donc « l'éviter » ne prouve rien en soi. |
| Algébrisation (Aaronson–Wigderson) | Généralise la relativisation aux techniques algébriques. | **ACTIVE** — a tué la piste 2. Toute technique mobilisant l'arithmétisation doit démontrer son caractère non-algébrisant (exhiber un oracle algébrique relativement auquel l'invariant proposé sépare P de NP). |

> Toute idée nouvelle DOIT dire laquelle de ces barrières elle prétend franchir, et comment. **Et explicitement traiter la relativisation.**

---

## 2. Pistes explorées

| # | Idée (résumé en 1 ligne) | Barrière visée | Verdict du Réfuteur | Statut |
|---|---|---|---|---|
| 1 | Incompressibilité (Kt) des témoins SAT : P comprimerait les témoins, contredisant leur incompressibilité | Preuves naturelles (revendiqué) | Équivoque K(w) vs K(w\|x) ; argument relativisant | ❌ **FAILLE FATALE** |
| 2 | Signature p-adique des témoins (Ax-Katz pour vérificateurs AC⁰) | Relativisation (revendiqué) | Arithmétisation exacte ≠ polylog ; Ax-Katz trivial sous contrainte booléenne ; technique algébrisante | ❌ **FAILLE FATALE** |
| 3 | Obstruction topologique sur paysage d'énergie CSP (Morse discrète + Lusternik-Schnirelmann) | Relativisation + algébrisation (revendiqué) | Invariant non-invariant sous équivalence logique ; sauts polynomiaux effondrent les Betti | ❌ **FAILLE FATALE** |
| 4 |  |  |  | *(à venir)* |

---

## 3. Lemmes et résultats

### ✅ Établis (vérifiés / démontrés rigoureusement)
- *(aucun pour l'instant)*

### ❓ Conjecturaux (plausibles mais non prouvés)
- *(aucun retenu pour l'instant)*

### ❌ Réfutés (faux — et pourquoi, pour ne pas y revenir)
- **Piste 1 — « contradiction de compressibilité des témoins ».** Le sophisme central : la confrontation oppose un Kt **inconditionnel** (Lemme 1, incompressibilité Ω(n)) à un Kt qui n'est petit que **conditionnellement à x** (Lemme 2, vrai sous la forme K(w|x)=O(1), pas K(w)=O(log n) — la description doit embarquer x, de taille poly(n)). En unifiant les deux quantités, la contradiction disparaît : soit Lemme 2 redevient faux (inconditionnel), soit Lemme 1 redevient faux (conditionnel, car le témoin lex-premier est déterminé par x). Le fossé entre conditionnel et inconditionnel **est** P vs NP → circularité.
- **De plus : la piste 1 relativise** (Kt, auto-réductibilité, recherche↔décision relativisent tous). Par BGS, elle ne peut donc structurellement pas séparer P de NP, même réparée. À NE JAMAIS réessayer sous cette forme.

- **Piste 2 — « signature p-adique des témoins (Ax-Katz pour AC⁰) ».** Quatre failles convergentes, deux vérifiées par calcul (cf. [`checks/tour_02_axkatz_p_adique.py`](checks/tour_02_axkatz_p_adique.py)) :
  1. Le « Lemme 1 » revendique une arithmétisation AC⁰ → degré polylog. Faux pour l'arithmétisation **exacte** : la version polylog (Razborov-Smolensky) est une **approximation probabiliste**, et Ax-Katz exige des polynômes exacts. Empiriquement, l'arithmétisation exacte d'un 3-CNF à `k` clauses a un degré strictement égal à `3k = poly(m)`.
  2. Le « Lemme 2 » (Ax-Katz force `μ ≈ m/d` polynomial) **s'écroule sous la contrainte booléenne** `w_i² = w_i`. Les `m` équations ajoutées (degré 2 chacune) font passer le minorant à `⌈(m − d − 2m) / max⌉ ≤ 0` — **trivial dans tous les cas**. Ax-Katz ne dit absolument rien sur le nombre de témoins booléens. C'est précisément pour cela qu'on n'utilise pas Ax-Katz en complexité booléenne.
  3. La technique **algébrise** au sens d'Aaronson-Wigderson : l'invariant `v_p(N_x)` est une fonction d'une extension algébrique du vérificateur, donc relativise par rapport aux oracles algébriques relativement auxquels `P^Õ = NP^Õ`. L'argument anti-algébrisation du Proposeur (« `Õ` ne respecte pas le degré polylog ») est circulaire : la contrainte de degré polylog est sa propre invention, pas une propriété du cadre AW.
  4. « Lemme 3 » (arithmétisation de P) faux par le même mécanisme que (1) : un algorithme polynomial en temps `n^k` s'arithmétise à la Shamir en degré `n^{O(k)}` polynomial, pas polylog. La « contrainte géométrique » du Lemme 4 disparaît.

  À NE JAMAIS réessayer sous cette forme. **Nuance honnête** : le programme algébrique-géométrique en complexité existe (GCT, permanent vs déterminant), mais il n'utilise pas Ax-Katz pour les raisons ci-dessus. Confondre comptage algébrique (Ax-Katz) et existence booléenne (P vs NP) est l'erreur centrale.

- **Piste 3 — « obstruction topologique sur le paysage d'énergie d'un CSP ».** Deux failles fatales indépendantes, vérifiées par calcul (cf. [`checks/tour_03_topologie_morse.py`](checks/tour_03_topologie_morse.py)) :
  1. **L'invariant `Σ β_i(L_k(φ))` n'est pas une fonction de la fonction booléenne, mais de sa présentation syntaxique.** Le Proposeur l'admet (« deux formules équivalentes peuvent avoir des paysages différents ») sans en mesurer la conséquence. Démontré numériquement : pour ψ = (x_0∨x_1) ∧ (x_2∨x_3) ∧ (x_4∨x_5) et ψ' = ψ avec chaque clause triplée (mêmes 27 témoins, fonction booléenne identique), `Σ β_i(L_1)` vaut **92 pour ψ et 29 pour ψ'** (facteur 3) ; à `k=2`, **125 vs 29** (facteur 4). Conséquence : un algorithme P pour SAT peut préprocesser toute CNF en forme canonique en temps poly avant de décider — toute borne inférieure dérivée d'un invariant variant sous équivalence logique s'évanouit. `P` et `NP` étant des classes de fonctions/langages, un tel invariant ne peut structurellement pas les séparer. Ce n'est pas RR, c'est plus grave : on sort du cadre P vs NP.
  2. **Le Lemme 3 (MT modélisée comme champ de vecteurs à sauts bornés) est faux.** Une MT en temps `n^c` peut modifier `n^c` bits par étape ; le graphe pertinent est `G_{n^c}` = cube avec arêtes Hamming ≤ `n^c`. Dès `r = 2`, les Betti s'effondrent. Démontré sur CSP `x_i = x_{i+3}` (8 témoins sur la diagonale) : `β_0 = 8` à `r = 1`, mais `β_0 = 1` dès `r = 2`. La théorie de Morse discrète (Forman 1998) est strictement à 1-saut ; sa généralisation aux sauts polynomiaux trivialise l'obstruction. *Sans* Lemme 3, le Lemme 4 ne se prouve pas.

  À NE JAMAIS réessayer sous cette forme. **Nuance honnête** : le clustering topologique des CSP en phase RSB (Mézard-Parisi-Zecchina, Achlioptas et al.) borne effectivement les algorithmes **locaux** — pas P entier. Confondre « bornes pour algos locaux » et « bornes pour P » est l'erreur centrale.

---

## 4. Questions ouvertes prioritaires

1. **Tout invariant proposé doit être explicitement invariant sous équivalence logique** des présentations du problème. C'est un test de bon sens préalable à toute analyse fine — la piste 3 a échoué là-dessus.
2. **Tout argument du type « tout algorithme P est contraint par X » doit démontrer que X survit aux sauts polynomiaux**, i.e. à l'extension du graphe Hamming-1 vers `G_{n^c}` (graphe avec arêtes ≤ `n^c` bits modifiés). La piste 3 a échoué sur ce test aussi.
3. **Existe-t-il une obstruction non-locale et non-algébrique** qui survive aux sauts polynomiaux *et* à l'équivalence logique ? GCT (permanent vs déterminant) est la seule réponse sérieuse aujourd'hui, mais elle est au point mort depuis 2017 (Bürgisser-Ikenmeyer-Panova : pas d'obstruction par occurrences).
4. Côté complexité descriptive : la question « existe-t-il une logique capturant exactement P ? » (conjecture de Gurevich) offre-t-elle un angle non-relativisant **et** non-algébrisant exploitable ?
5. Williams 2011 (NEXP ⊄ ACC⁰) reste l'unique précédent ayant franchi les trois barrières — analyser quel ingrédient spécifique (algorithmic method + circuit lower bound + amplification) a permis ce franchissement, et si la recette se généralise à P vs NP.

---

## 5. Sous-but du tour courant

> Un seul objectif concret et, si possible, vérifiable.

- **Tour 4** : le Proposeur doit livrer une idée qui satisfait simultanément :
  - (a) **classe restreinte** concrète (et bien définie au niveau des fonctions, pas des présentations) ;
  - (b) **non-relativisant** (démontré) ;
  - (c) **non-algébrisant** (démontré par exhibition d'un oracle algébrique séparateur, ou argument équivalent à la Williams 2011) ;
  - (d) **invariance sous équivalence logique** : l'invariant proposé doit être une fonction de la fonction booléenne calculée, pas de sa présentation syntaxique — sinon il sort du cadre P vs NP ;
  - (e) **robustesse aux sauts polynomiaux** : si l'argument repose sur une géométrie locale (graphe, complexe simplicial), il doit survivre à l'extension `Hamming-1 → Hamming-≤n^c` qui modélise une MT polynomiale.

  Conseil de direction : viser **GCT** (permanent vs déterminant, théorie des représentations) ou un cadre type Williams 2011 (algorithmic method + lower bound), où (d) et (e) sont structurellement assurés par construction.

---

## 6. Prochaine action

- [ ] Proposeur : générer une idée pour le sous-but ci-dessus (non-relativisante + classe restreinte)
- [ ] Réfuteur : attaquer l'idée, vérifier en priorité relativisation ET algébrisation
- [ ] Confronter à la littérature réelle (recherche web) : l'idée correspond-elle à une tentative déjà publiée/écartée ?
- [ ] Si « survit » : isoler un sous-lemme vérifiable / tenter une formalisation (Lean)
- [ ] Consigner le résultat (succès **ou** échec documenté) dans les sections 2 et 3
