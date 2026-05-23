# Tour 14 — `DNF_min(MAJ_n) = C(n, ⌈n/2⌉)` (✅ Établi pour P vs NP, avec correction de formulation)

- **Date** : 2026-05-23
- **Proposeur** : Qwen Max
- **Réfuteur** : Claude
- **Sous-but visé** : direction ouverte du Tour 14 — option « extension lignée
  FSS, première apparition de TC⁰ dans le dépôt ».
- **Verdict** : ✅ **ÉTABLI POUR P vs NP** sur le théorème central. ⚠️ **Note
  de correction** sur la formulation de la séparation entre classes (l'erreur
  est notée mais ne touche pas le contenu mathématique).

---

## Idée proposée (résumé fidèle)

**Mini-théorème.** Soit `MAJ_n : {0,1}^n → {0,1}` la fonction majorité
(`MAJ_n(x) = 1` ssi `sum(x) ≥ ⌈n/2⌉`). La taille minimale (nombre de monômes)
d'un DNF calculant `MAJ_n` est exactement `C(n, ⌈n/2⌉) ~ 2^n / √n`.

**Conclusion revendiquée par le Proposeur** : *« AC⁰ profondeur 2 polynomial
⊊ TC⁰ profondeur 1 polynomial. Première séparation entre deux classes
restreintes. »*

---

## Vérification — partie A : théorème central confirmé

### 1. Reproduction indépendante du calcul

Script `tour_14_majority_dnf_lower_bound.py` exécuté indépendamment :

```
MAJ_4 : 11 affectations à 1 sur 16 (= Σ_{k≥2} C(4,k))
Total ANDs sur 4 vars : 81 (= 3^4)
Implicants de MAJ_4 (incluant non-premiers) : 33
Implicants premiers : 6 (= C(4,2))

Liste des 6 implicants premiers :
  x_0 ∧ x_1, x_0 ∧ x_2, x_0 ∧ x_3,
  x_1 ∧ x_2, x_1 ∧ x_3, x_2 ∧ x_3

✓ Tous positifs, taille 2 exactement.
✓ Chaque assignation à 2 ones (il y en a 6) satisfait
  exactement 1 implicant premier.
✓ DNF canonique de taille 6 calcule MAJ_4 correctement.
```

**`DNF_min(MAJ_4) = 6 = C(4,2)` confirmé.**

### 2. Audit des preuves L14.1–L14.4

**L14.1** (caractérisation implicant) : *`M` implicant de `MAJ_n` ssi
`pos(M) ≥ t`* où `t = ⌈n/2⌉`.

Preuve correcte : (⇒) si `pos(M) < t`, on force les variables libres à 0 et
les variables négativement contraintes à 0 ; alors `sum(x) = pos(M) < t`,
donc `MAJ(x) = 0`, contradiction. (⇐) si `pos(M) ≥ t`, toute assignation
satisfaisant `M` a au moins `pos(M) ≥ t` 1s, donc `MAJ = 1`. ∎

**Vérifié empiriquement** sur les 81 ANDs (n=4) sans contre-exemple.

**L14.2** (implicants premiers sans littéraux négatifs) : si `~x_i ∈ M`,
alors `M' = M \ {~x_i}` a `pos(M') = pos(M) ≥ t`, donc `M'` aussi implicant.
`M'` strictement moins contraint que `M`, donc `M` non premier. ∎

**L14.3** (compte exact) : par L14.1 + L14.2, implicants premiers = ANDs
positifs de taille ≥ t qui sont minimaux. Minimalité ⇒ taille = t. Nombre
= `C(n, t)`. ∎

**Note méthodologique** : la version *initiale* de l'argument du Proposeur
contenait un bug — il prétendait *« aucun implicant n'a de littéral
négatif »* (faux : `x_1 ∧ x_2 ∧ ~x_3` est implicant de `MAJ_4` mais non
premier). **Le calcul a immédiatement révélé le bug** (22 contre-exemples sur
81 ANDs), et le Proposeur a corrigé en distinguant *implicant* / *implicant
premier* avant soumission. **Exactement le rôle de la condition (j).**

**L14.4** (non-redondance) : pour `S ⊆ [n]` avec `|S| = t`, l'assignation
`χ_S` (1 sur `S`, 0 ailleurs) satisfait `M_S = ∏_{i∈S} x_i` mais aucun
autre `M_T` avec `T ≠ S`, `|T| = t`. Donc tous les `C(n, t)` implicants
premiers sont requis. ∎

**Conclusion combinatoire** :

> `DNF_min(MAJ_n) = C(n, ⌈n/2⌉) ~ 2^n / √n` par Stirling.

Pour n=4 : `C(4, 2) = 6`. Pour n=5 : `C(5, 3) = 10`. Pour n=10 : `252`.
Croissance super-polynomiale.

### 3. Test des barrières

- **Relativisation** : preuve combinatoire sans oracle. ✓
- **Razborov-Rudich** : la propriété « `f = MAJ_n` » caractérise une fonction
  unique parmi `2^{2^n}`, donc largement non-large (`2^{-2^n}` ≪ `2^{-O(n)}`).
  RR non applicable. ✓
- **Algébrisation** : pas d'arithmétisation. ✓

---

## Vérification — partie B : correction de la formulation conclusionnelle

### Erreur de formulation détectée

Le Proposeur écrit comme conclusion :
> *« Donc `AC⁰ profondeur 2 polynomial ⊊ TC⁰ profondeur 1 polynomial`. »*

**Cette inclusion stricte est mal énoncée logiquement.**

### Ce que le théorème établit *réellement*

Le théorème combinatoire + le fait que `MAJ_n ∈ TC⁰ d=1` (une porte threshold
suffit) donnent :

- `MAJ_n ∈ TC⁰ d=1`
- `MAJ_n ∉ AC⁰ d=2 polynomial` (par L14.4, taille minimale `C(n, ⌈n/2⌉)` non
  polynomial)

Conclusion correcte :

> **`TC⁰ d=1 ⊄ AC⁰ d=2 polynomial`** (incomparabilité partielle, par témoin
> `MAJ_n`).

### Pourquoi l'inclusion stricte est *fausse*

`A ⊊ B` requiert deux choses : (i) `A ⊆ B`, et (ii) `B \ A ≠ ∅`. Le Proposeur
établit (ii) (par `MAJ_n`) mais **pas (i)**.

L'inclusion (i) `AC⁰ d=2 polynomial ⊆ TC⁰ d=1` est en fait **fausse**.

**Contre-exemple explicite.** Sur `2n` variables, considérons :

```
f(x_1, …, x_n, y_1, …, y_n) = ⋁_{i=1}^{n} (x_i ∧ ¬y_i)
```

- `f ∈ AC⁰ d=2 polynomial` : `n` monômes de 2 littéraux chacun.
- `f ∉ TC⁰ d=1` : `f` n'est pas une fonction de seuil linéaire à poids
  polynomiaux. Plus précisément, la complexité de communication de `f` sur
  la coupe `{x_i} | {y_i}` est `Θ(n)` (essentiellement DISJOINTNESS), ce qui
  est incompatible avec un seuil linéaire (qui aurait complexité `O(log n)`).

Donc `AC⁰ d=2 polynomial ⊄ TC⁰ d=1`. Les deux classes sont **incomparables**.

### Reformulation correcte

Le Tour 14 établit :

> *`MAJ_n` est une fonction explicite calculable en O(n) qui appartient à
> `TC⁰ d=1` mais n'appartient pas à `AC⁰ d=2 polynomial`. Par conséquent,
> ces deux classes sont incomparables par inclusion (incomparabilité partielle :
> `TC⁰ d=1 ⊄ AC⁰ d=2 polynomial` ; et symétriquement, par exemple via la
> fonction `DISJ_n` ci-dessus, `AC⁰ d=2 polynomial ⊄ TC⁰ d=1`).*

Le résultat reste positif et significatif (séparation par témoin), mais
pas sous la forme d'une inclusion stricte.

### Nature de l'erreur

Même type que l'erreur 2COL ∈ P du Tour 11 (erreur logique sur les classes,
pas mathématique sur les calculs). Mais ici l'erreur n'invalide pas le
théorème central ; seulement la phrase de conclusion.

C'est un **rappel précieux** que la rigueur sur les inclusions de classes est
distincte de la rigueur sur les calculs. Toute affirmation d'inclusion stricte
`⊊` doit être démontrée par deux pas séparés : `⊆` ET `⊋`.

---

## Verdict : ✅ ÉTABLI POUR P vs NP (avec correction notée)

**Théorème central acquis** : `DNF_min(MAJ_n) = C(n, ⌈n/2⌉)`, donc `MAJ_n ∉
AC⁰ d=2 polynomial`. Toutes les preuves L14.1–L14.4 auditées et correctes.
Calcul exhaustif n=4 confirmé.

**Correction explicite enregistrée** sur la formulation de la séparation entre
classes : le bon énoncé est `TC⁰ d=1 ⊄ AC⁰ d=2 polynomial` (séparation par
témoin), pas l'inclusion stricte `AC⁰ d=2 poly ⊊ TC⁰ d=1`.

**Conditions (a)–(l) honorées** sauf nuance logique sur la formulation
classes. Le théorème mathématique passe ; la conséquence inter-classes doit
être reformulée.

---

## Nuance honnête

- **Théorème classique**, dans tout cours de complexité. Apport mathématique
  : zéro. Apport au dépôt : *troisième objet ÉTABLI*, sur une nouvelle
  fonction (MAJ ≠ PARITY), avec borne sub-exponentielle non-triviale, et
  apparition explicite de TC⁰ dans la lignée FSS → Williams.

- **Le bug L14.1 initial** (corrigé par (j) avant soumission) montre la
  valeur du test empirique préalable. Sans (j), le Proposeur aurait soumis
  un argument incorrect. Cette correction « en place » est exactement le
  pattern souhaité.

- **L'erreur de formulation sur les classes** (inclusion stricte vs
  incomparabilité par témoin) est elle aussi du type « erreur logique de
  haut niveau », similaire au 2COL du Tour 11. Le théorème central est
  correct, mais la formulation des conséquences requiert rigueur séparée.

## Conséquences pour la suite

- **Troisième entrée** dans la section ✅ Établis pour P vs NP du cahier :
  `DNF_min(MAJ_n) = C(n, ⌈n/2⌉)`, avec note explicite sur la formulation
  correcte de la séparation (`TC⁰ d=1 ⊄ AC⁰ d=2 polynomial`).
- **Condition (m)** à ajouter : *« toute affirmation d'inclusion entre classes
  doit distinguer ⊊ (inclusion stricte) de ⊄ (incomparabilité par témoin).
  Une séparation par témoin requiert deux pas distincts pour devenir
  inclusion stricte. »*
- **Sous-but Tour 15** : options inchangées (cross-validation n=5,6,
  profondeur 3, formalisation Lean) + nouvelle option naturelle qui émerge
  du Tour 14 : étendre le théorème à toutes les fonctions seuil
  `THRESHOLD_t` (analogie immédiate : `DNF_min(TH_t) = C(n, t)`).

## Script de vérification

[`checks/tour_14_majority_dnf_lower_bound.py`](../checks/tour_14_majority_dnf_lower_bound.py)
— livré par le Proposeur (avec bug L14.1 initial détecté et corrigé par lui-
même avant soumission), exécuté indépendamment par le Réfuteur. Énumère les
81 ANDs sur n=4, identifie les 6 implicants premiers de `MAJ_4`, vérifie
L14.1–L14.4 numériquement, confirme le DNF canonique de taille 6.
