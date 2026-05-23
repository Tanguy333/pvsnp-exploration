# Tour 21 — Preuve partielle de L20.5 (⚠️ LACUNE RÉPARABLE)

- **Date** : 2026-05-23
- **Proposeur** : Qwen Max
- **Réfuteur** : Claude
- **Sous-but visé** : option 2 du Tour 21 — démontrer L20.5 structurellement.
- **Verdict** : ⚠️ **LACUNE RÉPARABLE**. L21.A, L21.B, L21.C prouvés
  rigoureusement (L21.C **complétée par le Réfuteur**) ; **L21.D reste
  ouverte structurellement** (vérification empirique seulement n=4). L20.5
  n'est donc pas encore complètement prouvée pour tout n.

---

## Idée proposée (résumé fidèle)

**Théorème L21 (conjectural)** : pour tout `n ≥ 3` et toute fonction booléenne
non-constante `f`, `défaut(f) ≤ n(n−2)`, avec égalité ssi `f` est antipodale.

Décomposition par cas selon `k = |f^{-1}(0)|` :
- L21.A : k = 1 → défaut = 0.
- L21.B : k = 2 antipodal → défaut = n(n−2) (= Tour 20).
- L21.C : k = 2 non-antipodal → défaut < n(n−2).
- L21.D : k ≥ 3 → défaut < n(n−2).

**Vérification empirique n=4** : 65 534 fonctions énumérées, 8 fonctions à
défaut maximal 8, toutes antipodales. L20.5 confirmée n=4.

---

## Audit du Réfuteur

### 1. L21.A (k=1) — prouvé

Si `f^{-1}(0) = {α}`, alors les implicants premiers de f sont exactement
les littéraux `l_i^α` (conflictuels avec α sur la position i). Il y en a
exactement `n` ; chacun a `α ⊕ e_i` comme témoin essentiel unique. Donc
`|primes| = DNF_min = n`, défaut = 0. ✓

### 2. L21.B (k=2 antipodal) — prouvé Tour 20

Voir [`tours/tour_20_antipodales_etabli.md`](tour_20_antipodales_etabli.md).
`|primes| = n(n−1)`, `DNF_min = n`, défaut = `n(n−2)`. ✓

### 3. L21.C (k=2 non-antipodal) — **prouvé rigoureusement par le Réfuteur**

Le Proposeur a esquissé l'argument sans le compléter. Je détaille.

WLOG `α = 0^n`, `β = 1^d 0^{n-d}` avec `1 ≤ d ≤ n − 1`. Donc
`f^{-1}(0) = {α, β}`, `d = dist_H(α, β) < n`.

**Caractérisation des implicants premiers de f**.

Un AND `M` est implicant de f ssi `M(α) = 0` et `M(β) = 0`.
- `M(α) = 0` ⟺ M contient au moins un littéral positif `x_i`.
- `M(β) = 0` ⟺ M contient au moins un littéral négatif sur les `d`
  premières positions (où `β_i = 1`), OU au moins un littéral positif sur
  les `n − d` dernières positions (où `β_i = 0`).

**Classification des implicants premiers par cas** :

- **Cas 1** : `M = x_i` pour `i ∈ {d+1, …, n}` (positif sur position
  commune avec valeur 0 pour α et β).
  - `M(α) = 0` ✓ (positif).
  - `M(β) = β_i = 0` ✓ (i > d).
  - Implicant de taille 1. Premier trivialement.
  - Nombre : `n − d`.

- **Cas 2** : `M = x_i ∧ ~x_j` pour `i, j ∈ {1, …, d}`, `i ≠ j`.
  - `M(α) = 0 · 1 = 0` ✓.
  - `M(β) = β_i · ~β_j = 1 · 0 = 0` ✓.
  - Premier : enlever `x_i` → `M' = ~x_j`, `M'(α) = ~α_j = 1` ✗, non-implicant.
    Enlever `~x_j` → `M' = x_i`, `M'(β) = β_i = 1` ✗ (i ≤ d), non-implicant.
  - Nombre : `d(d − 1)`.

- **Tous les autres cas ne sont pas premiers** :
  - `M = x_i` pour `i ≤ d` : `M(β) = 1` ✗.
  - `M = ~x_j` pour `j ≤ d` : `M(α) = 1` ✗.
  - `M = ~x_j` pour `j > d` : `M(α) = 1` ✗.
  - `M = x_i ∧ x_j` (deux positifs) : si i, j ≤ d, `M(β) = 1`. Si i ≤ d, j > d,
    on peut enlever `x_i` (Cas 1), donc M non premier. Si i, j > d, on peut
    enlever l'un des deux (Cas 1), non premier.
  - `M = x_i ∧ ~x_j` avec `i > d` : on peut enlever `~x_j` (Cas 1), non premier.
  - `M = x_i ∧ ~x_j` avec `i ≤ d, j > d` : `M(α) = 0 ✓`. `M(β) = β_i · ~β_j = 1 · 1 = 1` ✗, non-implicant.
  - ANDs de taille ≥ 3 : on peut enlever un littéral pour obtenir un implicant
    de taille ≤ 2 (Cas 1 ou 2), donc non premier.

**Comptage exact** :

$$|\mathrm{primes}(f)| = (n - d) + d(d - 1) = d^2 - 2d + n.$$

**Maximum sur `d ∈ {1, …, n−1}`** :

`d² − 2d + n` est croissant pour `d ≥ 1` (dérivée `2d − 2 ≥ 0`). Maximum à
`d = n − 1` :

$$|\mathrm{primes}|_{\max, \text{non-antipodal}} = (n-1)^2 - 2(n-1) + n = n^2 - 3n + 3.$$

**Comparaison à `n(n − 2) = n² − 2n`** :

$$n^2 - 3n + 3 < n^2 - 2n \iff -3n + 3 < -2n \iff 3 < n \iff n \geq 4.$$

**Cas n ≥ 4** : `|primes|_non-antipodal < n(n−2)`, donc `défaut ≤ |primes| <
n(n−2)`. ✓ L21.C prouvée.

**Cas n = 3** : `|primes|_max non-antipodal = 3 = n(n−2)`. Égalité possible
en `|primes|`. Mais on doit calculer le défaut, pas `|primes|`.

À n=3, `d = 2` (cas maximum), `f^{-1}(0) = {000, 110}`. Implicants premiers :
- Cas 1 (i > d = 2) : `x_3`. (1 implicant)
- Cas 2 (i, j ≤ 2, i ≠ j) : `x_1 ∧ ~x_2`, `x_2 ∧ ~x_1`. (2 implicants)
- Total : 3.

`f^{-1}(1) = {001, 010, 011, 100, 101, 111}` (6 affectations).

- `x_3` couvre {001, 011, 101, 111} (4 affectations).
- `x_1 ∧ ~x_2` couvre {100, 101} (2 affectations).
- `x_2 ∧ ~x_1` couvre {010, 011} (2 affectations).
- Tous nécessaires : sans `x_3`, 001 non couvert. Sans `x_1 ∧ ~x_2`, 100
  non couvert. Sans `x_2 ∧ ~x_1`, 010 non couvert.

Donc `DNF_min(f) = 3 = |primes|`, défaut = 0 < 3 = n(n−2). ✓ L21.C tient
aussi à n=3 pour d=2.

À n=3, `d = 1` : `f^{-1}(0) = {000, 100}`. `|primes| = 2 + 0 = 2`, défaut
≤ 2 < 3.

**Conclusion** : pour tout `n ≥ 3` et tout `d ∈ {1, …, n−1}`, défaut < n(n−2).
**L21.C prouvée**. ∎

### 4. L21.D (k ≥ 3) — non prouvée structurellement

Le Proposeur fournit uniquement une intuition (« plus de zéros = plus de
contraintes »). Pas de preuve formelle.

**Difficulté technique** : pour `k ≥ 3` affectations `α_1, …, α_k ∈
f^{-1}(0)`, les implicants premiers sont les hitting sets minimaux de la
famille `{B_i = {l_j^{α_i} : j ∈ [n]}}`. Le comptage et la classification
dépendent finement de la structure des `α_i` (intersections des `B_i`,
configurations relatives).

**Approche possible** (non développée ici) :
1. Borne universelle `|primes(f)| ≤ Φ(n, k)` pour une fonction Φ croissante
   en k.
2. Montrer `Φ(n, 3) < n(n − 2)` pour tout `n ≥ 3`.
3. Conclure défaut < n(n − 2) pour k ≥ 3.

**État empirique** : vérifié n=4 (tableau Tour 21 : pour k ∈ {3, …, 15},
défaut max ≤ 6 < 8). Mais infaisable n=5 et au-delà par énumération.

### 5. Verdict : ⚠️ **LACUNE RÉPARABLE**

L'objectif du Tour 21 (prouver L20.5 pour tout n) **n'est pas atteint**.

- L21.A, L21.B, L21.C : prouvés rigoureusement.
- **L21.D : reste ouverte** structurellement. Conjecture vérifiée n=4
  empiriquement.

L20.5 (unicité antipodale) n'est donc démontrée pour tout n que sur
l'**ensemble k ≤ 2**. Le cas `k ≥ 3` reste conjectural pour `n ≥ 5`.

**Différence avec Tour 18** : Tour 18 livrait une preuve **complète** par
récurrence pour tout n de L17. Tour 21 livre une preuve **partielle** (3
cas sur 4) avec un cas important (k ≥ 3) laissé ouvert.

---

## Apport et nuance

### Acquis réel

- **L21.C prouvée rigoureusement** (avec ma complétion). Pour tout `n ≥ 3`,
  les fonctions à k = 2 non-antipodal ont défaut < n(n−2). La preuve est
  élémentaire : comptage exact `|primes| = d² − 2d + n`, comparaison
  algébrique à `n² − 2n`.

- **Confirmation empirique n=4** : aucun contre-exemple à L20.5 parmi les
  65 534 fonctions non-constantes.

### Reste à faire

- **L21.D** : preuve structurelle pour `k ≥ 3`. Probablement faisable par
  argument hitting set / borne combinatoire, mais demande un effort non
  négligeable. C'est la *vraie partie difficile* de L20.5.

### Statut du dépôt après Tour 21

- 8 ÉTABLIS (Tours 12-20, paradigme AC⁰ d=2 cartographié).
- 1 ⚠️ LACUNE RÉPARABLE (Tour 21, L20.5 partielle).
- L20.5 reste conjecturée pour `n ≥ 5` sur le cas `k ≥ 3`.

### Conséquences pour la suite

- **Sous-but Tour 22** : trois options viables :
  1. **Compléter L21.D** : direction naturelle, transformerait L21 en
     ÉTABLI complet (+1 objet).
  2. **Formalisation Lean** (option 1 prescrite plusieurs fois sans réponse).
  3. **Direction qualitativement nouvelle** (profondeur 3, Razborov monotone).

  Toute proposition restant dans `AC⁰ d=2 / DNF-MIN` sans saut technique
  reste interdite par (p), sauf si elle vise spécifiquement à compléter L21.

- **Note méthodologique** : Tour 21 reproduit *partiellement* le pattern
  Tour 17 → Tour 18 (vérifier → prouver) mais avec une preuve incomplète.
  C'est moins satisfaisant que Tour 18 (qui avait prouvé tout pour tout n).

## Script de vérification

[`checks/tour_21_l20_5_structural.py`](../checks/tour_21_l20_5_structural.py)
— livré par le Proposeur, exécuté indépendamment. Énumère les 65 534
fonctions non-constantes à n=4, tabule défaut maximal par k = |f^{-1}(0)|,
confirme que seul k=2 atteint le défaut maximal `n(n−2) = 8`, et que parmi
les 120 fonctions à k=2, seules les 8 antipodales l'atteignent. L20.5
empirique n=4 ✓.
