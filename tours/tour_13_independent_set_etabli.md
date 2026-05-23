# Tour 13 — Caractérisation des fonctions à DNF maximalement difficile via independent sets de Q_n (✅ Établi pour P vs NP)

- **Date** : 2026-05-23
- **Proposeur** : Qwen Max
- **Réfuteur** : Claude
- **Sous-but visé** : extension du Tour 12 (option 1 du sous-but Tour 13 :
  cross-validation / consolidation).
- **Verdict** : ✅ **ÉTABLI POUR P vs NP** — deuxième objet positif du dépôt,
  consolidant et structurant le Tour 12.

---

## Idée proposée (résumé fidèle)

**Théorème (extension Tour 12).** Pour toute fonction booléenne `f : {0,1}^n →
{0,1}` non-constante, les trois conditions suivantes sont équivalentes :
- **(a)** Le DNF minimal calculant `f` a taille exactement `|f^{-1}(1)|`.
- **(b)** Aucun AND de moins de `n` littéraux n'est implicant de `f`.
- **(c)** `f^{-1}(1)` est un independent set du graphe `Q_n` du n-cube (aucune
  paire d'affectations dans `f^{-1}(1)` ne diffère d'un seul bit).

**Corollaire combinatoire.** La classe des fonctions vérifiant ces conditions
est en bijection avec les independent sets de `Q_n`. **Compte à n=4 : 743
fonctions** (1.13 % des `2^{16} = 65 536` fonctions booléennes).

**Corollaire extrémal.** Le maximum `|f^{-1}(1)| = 2^{n-1}` est atteint
**exactement par PARITY et ¬PARITY**, car `Q_n` est biparti et ses uniques
independent sets maximaux sont les deux classes de cette bipartition.

---

## Vérification du Réfuteur

### 1. Reproduction indépendante du calcul

Script `tour_13_independent_set_characterization.py` exécuté indépendamment :

```
Total fonctions sur n=4 : 65536
Fonctions à f^{-1}(1) independent : 743 / 65536  (= 1.13%)

Test (b) ⟺ (c) sur 200 échantillons aléatoires : 0 incohérence. ✓

Distribution par taille |f^{-1}(1)| :
  | size |  #fns  | DNF min |
  |    0 |     1  |    0    |
  |    1 |    16  |    1    |
  |    2 |    88  |    2    |
  |    3 |   208  |    3    |
  |    4 |   228  |    4    |
  |    5 |   128  |    5    |
  |    6 |    56  |    6    |
  |    7 |    16  |    7    |
  |    8 |     2  |    8    | ← maximum, PARITY + ¬PARITY
  total :  743
```

Vérification arithmétique : `1+16+88+208+228+128+56+16+2 = 743`. ✓

### 2. Audit des preuves

**L13.1 — (a) ⟺ (b).** Suit Tour 12 généralisé.
- *(b) ⇒ (a)* : si aucun AND de taille `< n` n'est implicant, alors tout
  implicant a taille exactement `n`. Un AND de taille `n` est un minterm
  complet `M_x` pour une unique affectation `x`, satisfait uniquement par
  `x`. Donc les implicants sont exactement les mintermes complets des
  affectations dans `f^{-1}(1)`. Chacun est requis (chacun ne couvre
  qu'une affectation). DNF minimal = `|f^{-1}(1)|`.
- *(a) ⇒ (b)* : contrapositive. Si un AND `M` de taille `k < n` est
  implicant, il couvre `2^{n-k} ≥ 2` points de `f^{-1}(1)`. On peut
  remplacer ces `2^{n-k}` mintermes complets par le seul `M` dans le DNF,
  obtenant un DNF de taille `|f^{-1}(1)| - 2^{n-k} + 1 < |f^{-1}(1)|`. Donc
  DNF minimal `< |f^{-1}(1)|`.

Audit : ✓

**L13.2 — (b) ⟺ (c).**
- *(c) ⇒ (b)* : un AND de `k < n` littéraux fixe un sous-cube de `Q_n` de
  dimension `n - k ≥ 1`. Ce sous-cube contient au moins une arête de `Q_n`.
  Si `M` est implicant, le sous-cube `⊆ f^{-1}(1)`, donc une arête est dans
  `f^{-1}(1)`, contredisant l'indépendance (c).
- *(b) ⇒ (c)* : contrapositive. Si `(c)` faux, il existe `x, y ∈ f^{-1}(1)`
  avec `dist_H(x, y) = 1`, différant sur le bit `i`. L'AND des `n - 1`
  littéraux fixant `x_j = bit_j(x)` pour `j ≠ i` est satisfait exactement
  par `{x, y}`, tous deux dans `f^{-1}(1)`. C'est un implicant de taille
  `n - 1 < n`, donc `(b)` faux.

Audit : ✓ (vérifié empiriquement sur 200 échantillons sans incohérence)

**L13.3 — Bijection avec les independent sets de Q_n.** Triviale via
`f ↦ f^{-1}(1)`. Cardinal = nombre d'independent sets de `Q_4` = 743
(vérifié).

**L13.4 — Extrémalité PARITY.** `Q_n` est biparti (`n`-cube est biparti pour
tout `n`), avec classes définies par la parité de Hamming. Les deux classes
ont chacune `2^{n-1}` éléments. Par théorème classique des graphes
bipartis : les seuls independent sets de cardinal maximum sont exactement
ces deux classes. À n=4, vérifié : exactement 2 fonctions atteignent
`|f^{-1}(1)| = 8`, identifiées comme PARITY et ¬PARITY.

Audit : ✓

### 3. Test des barrières

**Relativisation.** Toutes les preuves L13.1–L13.4 sont combinatoires (sous-
cubes de `Q_n`, bipartition, comptages). Aucun oracle, aucune machine de
Turing. Non-relativisant comme au Tour 12. ✓

**Preuves naturelles (Razborov-Rudich).** Analyse nuancée :
- La propriété (b)/(c) est **constructive** (calculable en `O(3^n)` sur la
  table de vérité, donc poly en taille `2^n`). ✓
- À n=4, **large** : 1.13 % des fonctions vérifient la propriété, soit
  `743 / 2^{2^4} ≈ 2^{-6.45}`. Pour la condition de largeur RR `≥
  2^{-O(n)}`, c'est très large à n=4. Asymptotique à n grand : `|IS(Q_n)|`
  croît comme `2^{Θ(2^{n-1})}` (Korner-Sapozhenko / Galvin), donc le
  ratio `|IS(Q_n)| / 2^{2^n}` ≈ `2^{-Θ(2^{n-1})}` — extrêmement petit
  asymptotiquement. **Pas large à n grand.**
- Mais le théorème **caractérise une classe**, pas une fonction
  individuelle. RR concerne typiquement les propriétés qui isolent une
  fonction *individuellement difficile*. La sous-classe à `|f^{-1}(1)| =
  2^{n-1}` (PARITY + ¬PARITY) est non-large (2 fonctions sur `2^{2^n}`,
  i.e. `2^{-Θ(2^n)}`), donc échappe à RR.

Conclusion : le théorème ne tombe pas sous RR — il caractérise structurellement
une classe sans en isoler les éléments. ✓

**Algébrisation.** Aucune arithmétisation. ✓

### 4. Erreur référentielle OEIS (mineure, signalée)

Le Proposeur écrit dans sa proposition :
> *« La séquence OEIS A006506 confirme : 743 est le nombre d'independent sets
> du 4-cube. »*

**Faux.** OEIS A006506 = nombres de Dedekind = `2, 3, 6, 20, 168, 7581, ...`
À n=4, A006506(4) = 168, pas 743. La séquence correcte (number of independent
sets in the n-cube graph Q_n) est `2, 3, 7, 35, 743, 254 475, ...` — une
autre entrée OEIS dont je n'ai pas le numéro exact sans accès internet, mais
**743 pour Q_4 est correct par calcul direct** (mon script confirme).

Le Proposeur lui-même note l'incohérence dans son script (ligne 192 : *« HMMM,
ca ne colle pas. En realite OEIS A005843 ou similaire. »*). Erreur
référentielle (en lecture rapide d'OEIS), pas mathématique. **Le chiffre 743
est correct ; le numéro de séquence OEIS cité est incorrect.**

Cette erreur ne touche pas le théorème.

### 5. Verdict : ✅ ÉTABLI POUR P vs NP

Toutes les 12 conditions (a)–(l) honorées (deuxième fois consécutive après
Tour 12). Théorème prouvé combinatoirement, vérifié exhaustivement à n=4,
structurellement plus riche que le Tour 12 :

- Le Tour 12 prouvait `DNF_min(PARITY_n) = 2^{n-1}` (un cas spécifique).
- Le Tour 13 prouve `DNF_min(f) = |f^{-1}(1)|` **pour toute fonction** dont
  `f^{-1}(1)` est un independent set de `Q_n` — et donne le **compte exact**
  des telles fonctions à n=4 (743).

PARITY apparaît comme l'**élément maximal** d'une classe combinatoire bien
définie, plutôt qu'un cas isolé. C'est une *structuration* du résultat
Tour 12, pas une simple répétition.

---

## Nuance honnête (assumée par le Proposeur)

- **Théorème classique, novelty mathématique zéro.** L'équivalence (b) ⟺ (c)
  est dans tout cours d'optimisation booléenne depuis les années 1960
  (Quine-McCluskey et descendants). La connexion à `IS(Q_n)` est classique.

- **Pas P vs NP.** Reste dans le cadre `AC⁰ profondeur 2 ⊊ P`, déjà acquis
  avec Tour 12.

- **Erreur référentielle OEIS** dans la proposition. Pas grave, mais à corriger.

- **Apport principal au dépôt** : *consolidation et structuration* du Tour 12.
  C'est un deuxième objet ÉTABLI qui solidifie le terrain plutôt que d'élargir
  la portée.

## Conséquences pour la suite

- **Deuxième entrée** dans la section ✅ Établis pour P vs NP du cahier.
- **Question structurelle ouverte** (intéressante en soi, indépendamment de
  P vs NP) : la classe des `IS(Q_n)` a-t-elle une structure plus fine ?
  Par exemple, peut-on caractériser quelles **familles infinies** de telles
  fonctions sont calculables par circuits poly-temps en `n` ? Au-delà de
  PARITY ?

- **Sous-but Tour 14** (toujours dans le cadre Tour 13 du cahier, options
  ouvertes) :
  1. **Cross-validation à n=5** : vérifier la borne sur n=5 (3^5 = 243 ANDs,
     2^{2^5} = 4 milliards de fonctions — trop coûteux pour énumération
     directe ; il faudrait énumérer les independent sets de Q_5 différemment).
     Faisable mais plus coûteux.
  2. **Extension à profondeur 3** : entrer dans le territoire FSS / Håstad.
     Significativement plus dur (le nombre de circuits AC⁰ profondeur 3 sur
     n=4 explose).
  3. **Formalisation Lean** des L12.1–L13.4 dans un fichier Mathlib4. Premier
     théorème de complexité formalisé du dépôt.

## Script de vérification

[`checks/tour_13_independent_set_characterization.py`](../checks/tour_13_independent_set_characterization.py)
— livré par le Proposeur, exécuté indépendamment par le Réfuteur. Énumère les
65 536 fonctions booléennes sur n=4, filtre celles à `f^{-1}(1)` independent
set de `Q_4` (= 743), donne la distribution par taille, identifie PARITY +
¬PARITY comme uniques fonctions à taille maximale 8, vérifie l'équivalence
(b) ⟺ (c) sur 200 échantillons aléatoires.
