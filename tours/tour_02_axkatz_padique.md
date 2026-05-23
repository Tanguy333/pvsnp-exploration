# Tour 02 — Signature p-adique de l'espace des témoins (invariant d'Ax-Katz pour vérificateurs AC⁰)

- **Date** : 2026-05-23
- **Proposeur** : Qwen Max
- **Réfuteur** : Claude
- **Sous-but visé** : idée ciblant une classe restreinte (NP\_{AC⁰}) et démontrant son caractère non-relativisant.
- **Verdict** : ❌ **FAILLE FATALE**

---

## Idée proposée (résumé fidèle)

Restreindre l'attaque à `NP_{AC^0}` (problèmes NP dont le vérificateur est un
circuit `AC⁰`), arithmétiser ce vérificateur en un polynôme `Ṽ(x, w)` sur
`F_p`, et exploiter la **valuation p-adique du nombre de témoins algébriques**
`N_x = |{w ∈ F̄_p^m : Ṽ(x,w)=1}|` comme invariant.

Squelette :
- **Lemme 1** : un circuit `AC⁰` de profondeur `c`, taille `S`, s'arithmétise
  en polynôme de degré `d = (log S)^{O(c)}` — polylog.
- **Lemme 2** : Ax–Katz force `p^μ | N_x` avec `μ ≈ m/d`, polynomial.
- **Lemme 3** : si SAT ∈ P, l'algorithme de recherche s'arithmétise en `Ã` de
  degré `D` ; l'image de `Ã` est une variété de degré borné.
- **Lemme 4** : il existe des familles SAT où l'espace des témoins est « trop
  riche » pour être l'image d'une `Ã` polynomiale sans violer Ax-Katz.

Barrière revendiquée comme franchie : **relativisation** (l'invariant exige le
code source du vérificateur, pas une boîte noire). Algébrisation revendiquée
contournée (l'oracle algébrique `Õ` d'Aaronson-Wigderson « ne respecterait pas
la contrainte de degré polylog »). Preuves naturelles évitées.

Aveux du Proposeur : (1) saut booléen↔algébrique non comblé ; (2) arithmétisation
de P explose en degré ; (3) pas d'instance explicite pour le Lemme 4.

---

## Réfutation

### 1. Reformulation

Compter les témoins du vérificateur sur `F_p`, et utiliser le fait qu'Ax-Katz
force une grande divisibilité par `p` (parce que le degré est polylog) pour
exhiber une obstruction qu'aucun algorithme polynomial ne pourrait reproduire.

### 2. Le point de rupture : **deux failles indépendantes, dont une calculable**

#### (a) Lemme 1 — confusion entre **approximation** polynomiale et **arithmétisation exacte**

Le Proposeur affirme « tout circuit `AC⁰` s'arithmétise en degré polylog ». C'est
**faux** pour l'arithmétisation exacte, qui est ce qu'exige Ax-Katz. Plus
précisément :

- Razborov-Smolensky (1987) donne une **approximation probabiliste** de
  `AC⁰[p]` par des polynômes de degré polylog : pour tout `ε > 0`, il existe un
  polynôme aléatoire `P` de degré `(log(1/ε) · log S)^{O(c)}` qui calcule la
  fonction sauf sur une fraction `ε` des entrées. L'égalité n'est jamais
  exacte sur tout l'espace.
- L'arithmétisation **exacte** d'une porte `OR_n` est `1 − ∏(1 − x_i)`, de
  degré exactement `n`. Pour un `AC⁰` typique (et a fortiori pour le
  vérificateur SAT, dont l'AND-de-clauses agrégé est arithmétisé en produit),
  le degré exact est **polynomial en la taille de l'entrée**.

Or Ax-Katz s'applique à des variétés *algébriques* définies par des polynômes
*exacts*. Une approximation probabiliste ne définit pas une variété — elle
définit une distribution sur des variétés différentes selon le choix aléatoire.
La valuation p-adique du nombre de zéros d'un *polynôme aléatoire* n'a pas de
sens géométrique fixe.

**Vérification numérique (cf. [`checks/tour_02_axkatz_p_adique.py`](../checks/tour_02_axkatz_p_adique.py)) :** pour les trois 3-CNF
testés à `m = 6` variables, l'arithmétisation exacte (produit des clauses
arithmétisées `c̃_j`) a un degré strictement égal à `3k`, où `k` est le nombre
de clauses :

| Instance | k | deg(V) | log(m)·constante |
|---|---|---|---|
| (A) UNSAT toutes ±x₀±x₁±x₂ | 8  | 24 | ≈ 2.6 |
| (B) SAT témoin unique      | 24 | 72 | ≈ 2.6 |
| (C) SAT 4 clauses          | 4  | 12 | ≈ 2.6 |

Le degré n'est **pas** polylog en `m`. Il croît linéairement en le nombre de
clauses, qui peut lui-même être polynomial en `m`.

#### (b) Lemme 2 — Ax-Katz devient **trivial** sur le cube booléen

Le théorème d'Ax-Katz (1971) : pour `r` polynômes `f_1,…,f_r ∈ F_q[X_1,…,X_n]`
de degrés `d_1,…,d_r`, le nombre `N` de zéros communs vérifie

```
q^μ | N,    μ ≥ ⌈(n − Σ d_i) / max d_i⌉.
```

Pour rester sur `{0,1}^m`, le Proposeur doit ajouter les `m` équations
`w_i² − w_i = 0` (degré 2 chacune). Le calcul direct :

```
n = m
Σ d_i = d_V + 2m       (un polynôme du vérificateur + m équations de degré 2)
max d_i = max(d_V, 2)
μ ≥ ⌈(m − d_V − 2m) / max(d_V, 2)⌉ = ⌈(−m − d_V) / max⌉  ≤ 0.
```

**La borne est triviale (`μ ≥ 0`, i.e. `p⁰ = 1` divise `N`) pour TOUT vérificateur
exact, indépendamment de son degré.** Ax-Katz ne dit rien sur le nombre de
témoins booléens. C'est exactement pour cela que ce théorème n'est pas utilisé
en complexité booléenne directement — l'aveu n°1 du Proposeur sous-estime
l'ampleur du problème : il ne s'agit pas d'un « lemme de transfert » à
trouver, c'est la borne elle-même qui s'écroule à zéro.

**Vérification numérique :** pour les 3 instances, à `p ∈ {3, 5, 7}`, la borne
d'Ax-Katz avec la contrainte booléenne donne **μ ≥ 0 dans tous les cas**
(résultats du script). Aucune information.

#### (c) Bonus calculable — la divisibilité observée est **triviale**, pas Ax-Katz

Plus subtil : le script révèle que `N_alg(F_p^6)` est effectivement divisible
par `p³` pour l'instance UNSAT (A) — `351 = 3³·13`, `875 = 5³·7`,
`18522 = 7³·54`. Cela pourrait faire croire à un effet d'Ax-Katz. Erreur :
l'instance (A) n'utilise que **3 des 6 variables** (les clauses portent toutes
sur `x_0, x_1, x_2`). Les variables `x_3, x_4, x_5` sont muettes, donc chaque
zéro algébrique se multiplie par `p³` libre. La divisibilité observée vient
d'un **fait combinatoire trivial** (variables non-utilisées), pas du théorème
d'Ax-Katz qui, lui, donne `μ ≥ 0` sans contenu.

Pour les instances (B) et (C), où toutes les variables apparaissent,
`v_p(N_alg)` retombe à `0` (ou `1` pour `p = 7, C`). Aucune divisibilité
structurelle.

| Instance | N_bool | N_alg(F₃) | v₃(N_alg) | v₃(N_bool) | Ax-Katz μ (bool) |
|---|---:|---:|---:|---:|---:|
| (A) UNSAT | 0 | 351   | 3 | ∞ | 0 (trivial) |
| (B) SAT-1 | 1 | 50    | 0 | 0 | 0 (trivial) |
| (C) SAT-34| 34 | 226  | 0 | 0 | 0 (trivial) |

`v_p(N_alg)` et `v_p(N_bool)` sont décorrélés ; la borne d'Ax-Katz est
triviale partout. L'invariant proposé ne sépare absolument rien.

### 3. Test des barrières

**Relativisation.** Le Proposeur a raison sur un point : un argument qui exige
l'accès au *code arithmétisé* du vérificateur est en principe non-relativisant
(un oracle booléen n'a pas de degré). Mais l'argument se brise *avant* d'arriver
à la non-relativisation : il n'y a tout simplement pas d'invariant à transporter.

**Algébrisation.** L'argument anti-algébrisation du Proposeur est circulaire.
Aaronson-Wigderson (2008) montrent que toute technique mobilisant
l'arithmétisation algébrise relativement à *toute* extension polynomiale `Õ` de
l'oracle — pas seulement celles de degré polylog. La contrainte de degré
polylog que le Proposeur impose à `Õ` est sa propre invention ; elle ne fait
pas partie du cadre de Aaronson-Wigderson. La technique se range donc parmi les
techniques **algébrisantes**, et bute sur les oracles algébriques relativement
auxquels `P^Õ = NP^Õ` (Aaronson-Wigderson, théorème de séparation algébrique).

Plus précisément : l'invariant `v_p(N_x)` est une fonction de l'extension
algébrique du vérificateur ; cette extension est exactement ce qu'un oracle
algébrique peut représenter. Toute borne inférieure dérivée de `v_p` se relève
donc à l'oracle algébrique — donc algébrise — donc ne peut pas trancher P vs NP.

**Preuves naturelles.** Non pertinent ici (l'argument ne porte pas sur des
tables de vérité). Pas d'angle d'attaque par ce côté.

### 4. Le Lemme 3 par-dessus le marché

Même en supposant les Lemmes 1 et 2 réparés (ils ne le sont pas), le Lemme 3
est faux pour la même raison structurelle : arithmétiser un algorithme
polynomial en temps `n^k` produit, dans le cadre standard à la Shamir, un
polynôme de degré `n^{O(k)}` — *polynomial*, jamais polylog. La « variété
image » a un degré supérieur ou égal à la dimension ambiante ; elle remplit
l'espace, et la « contrainte géométrique » du Lemme 4 disparaît.

### 5. Verdict : ❌ FAILLE FATALE

Quatre piliers de l'argument sont brisés indépendamment :
1. Lemme 1 confond approximation probabiliste et arithmétisation exacte ;
   le degré exact pour 3-SAT est `3k = poly(m)`, pas polylog. *(calculé)*
2. Lemme 2 (Ax-Katz) devient trivial dès qu'on ajoute la contrainte booléenne
   `w_i² = w_i`, `μ ≥ 0` partout. *(calculé)*
3. La technique algébrise au sens d'Aaronson-Wigderson : l'invariant
   `v_p(N_x)` est une fonction d'une extension algébrique, donc relativise
   par rapport aux oracles algébriques. *(structurel)*
4. Lemme 3 : arithmétiser P explose en degré `n^{O(k)}`, pas polylog —
   le Proposeur l'a lui-même admis. *(structurel)*

Aucun de ces quatre points n'est une lacune réparable ; chacun touche le cœur
de la construction. La réparation reviendrait à : trouver une arithmétisation
exacte de `AC⁰` en degré polylog (problème ouvert et probablement faux),
*ou* étendre Ax-Katz au cube booléen (problème ouvert depuis 50 ans, sans
candidat sérieux), *ou* échapper à Aaronson-Wigderson via une technique
non-algébrisante (programme entier de la recherche post-2008, un seul succès :
Williams 2011).

---

## Nuance honnête

Le programme **algébrique-géométrique** en complexité existe et est sérieux —
mais il s'incarne aujourd'hui dans la **GCT** (Geometric Complexity Theory de
Mulmuley-Sohoni), qui attaque permanent vs déterminant via théorie des
représentations, *pas* via Ax-Katz. Le théorème d'Ax-Katz, lui, sert
typiquement à étudier la complexité du **comptage** (variantes de #P sur les
corps finis, théorème de Beigel-Reingold-Spielman, etc.), pas l'existence
booléenne. Confondre les deux niveaux est exactement la confusion centrale du
Proposeur.

## Conséquences pour la suite

- Piste 2 classée **❌ Réfutée** dans le cahier de bord §2 / §3.
- Algébrisation passe à **ACTIVE** (rencontrée frontalement pour la première
  fois ; toute idée invoquant l'arithmétisation devra démontrer son caractère
  non-algébrisant — pas seulement non-relativisant).
- Question ouverte ouverte : un invariant **booléen** intrinsèque
  (e.g. complexité de Boolean rank, cohomologie d'un complexe simplicial
  attaché à la formule) plutôt qu'algébrique — quelque chose qui survit à
  la restriction au cube `{0,1}^m`.
- Contrainte ajoutée au tour 3 : toute idée arithmétisante doit *exhiber* un
  oracle algébrique relativement auquel l'invariant proposé sépare P de NP
  (sinon, par Aaronson-Wigderson, elle est tuée d'avance).

## Script de vérification

[`checks/tour_02_axkatz_p_adique.py`](../checks/tour_02_axkatz_p_adique.py) —
énumération exacte sur trois 3-CNF (UNSAT, SAT témoin unique, SAT à 4 clauses)
à 6 variables, calcul direct de `N_bool`, `N_alg(F_p^m)` et `v_p`, comparaison
avec les bornes d'Ax-Katz. Exécution : `python checks/tour_02_axkatz_p_adique.py`.
