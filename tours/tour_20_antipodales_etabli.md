# Tour 20 — Fonctions antipodales : caractérisation des cas à défaut maximal hors (α)/(β) (✅ Établi pour (i)-(iv), conjecture pour L20.5)

- **Date** : 2026-05-23
- **Proposeur** : Qwen Max
- **Réfuteur** : Claude
- **Sous-but visé** : option 3 du Tour 20 — fonctions hors (α)/(β).
- **Verdict** : ✅ **ÉTABLI POUR P vs NP** sur le théorème (i)-(iv) (prouvé
  pour tout n) — 8e objet. L20.5 (unicité des antipodales comme cas
  extrêmes) reste **conjecturée**, vérifiée n=3, 4 exhaustivement.

---

## Idée proposée (résumé fidèle)

**Théorème L20.** Soit `f_α(x) = 1 ⟺ x ∉ {α, ¬α}` (fonction « antipodale »
sur la paire `{α, ¬α}`). Alors pour tout n ≥ 3 :

1. `|f_α^{-1}(1)| = 2^n − 2`.
2. `|primes(f_α)| = n(n − 1)` (les `x_i ∧ ~x_j` pour i ≠ j).
3. `DNF_min(f_α) = n` (atteint par tout cycle dirigé sur [n]).
4. `défaut = |primes| − DNF_min = n(n − 2)`.

**L20.5 (corollaire conjectural)** : *les fonctions antipodales sont les
seules à atteindre le défaut maximal n(n − 2)*. Vérifié n=3 (4/4) et
n=4 (8/8) exhaustivement.

---

## Vérification du Réfuteur

### 1. Reproduction des chiffres

Script `tour_20_antipodal_verification.py` exécuté indépendamment :

| n | #antipodales | \|f^{-1}(1)\| | \|primes\| | DNF_min | défaut |
|---:|---:|---:|---:|---:|---:|
| 3 | 4 (= 2²) | 6 | 6 | 3 | 3 (= 3·1) ✓ |
| 4 | 8 (= 2³) | 14 | 12 | 4 | 8 (= 4·2) ✓ |
| 5 | 16 (= 2⁴) | 30 | 20 | 5 | 15 (= 5·3) ✓ |

### 2. Audit des preuves L20 (i)-(iv) pour tout n

WLOG `α = 0...0`, donc `f^{-1}(0) = {0...0, 1...1}`.

**(i)** `|f^{-1}(1)| = 2^n − |f^{-1}(0)| = 2^n − 2`. ✓ trivial.

**(ii)** `|primes(f_α)| = n(n − 1)`.

Un AND M implicant ⟺ `M(x) = 1 ⇒ x ∉ {0...0, 1...1}`, équivalent à :
- `M(0...0) = 0` : M contient au moins un littéral positif `x_i`.
- `M(1...1) = 0` : M contient au moins un littéral négatif `~x_j`.

M *premier* : taille minimale = exactement 1 positif + 1 négatif. Donc
`M = x_i ∧ ~x_j` pour `i ≠ j` (le cas `i = j` donne `x_i ∧ ~x_i = ⊥`
insatisfaisable).

Vérification que `x_i ∧ ~x_j` est implicant : satisfait par `2^{n-2}`
affectations (x_i = 1, x_j = 0, autres libres), toutes ≠ 0...0
(x_i = 1) et ≠ 1...1 (x_j = 0). ✓

Vérification de primalité : suppression de x_i → `~x_j` (satisfait par
0...0, non-implicant). Suppression de ~x_j → `x_i` (satisfait par 1...1,
non-implicant). ✓

Comptage : n choix pour i × (n−1) choix pour j ≠ i = **n(n−1)**. ✓

**(iii) DNF_min ≤ n par construction cyclique** :

Soit `C = {x_0 ∧ ~x_1, x_1 ∧ ~x_2, …, x_{n-1} ∧ ~x_0}` (n implicants
dans un cycle dirigé).

Soit `x ∈ f^{-1}(1)`. Alors `x ≠ 0...0` (au moins un 1) et `x ≠ 1...1`
(au moins un 0). En parcourant cycliquement les coordonnées, il existe
au moins un i tel que `x_i = 1` et `x_{(i+1) mod n} = 0`. Donc x satisfait
`x_i ∧ ~x_{(i+1) mod n} ∈ C`. C couvre `f^{-1}(1)`, donc `DNF_min ≤ n`.
∎

**(iii) DNF_min ≥ n par les n vecteurs unitaires** :

Pour chaque i ∈ [n], soit `e_i` l'affectation avec un seul 1 à la
position i. Alors `e_i ∈ f^{-1}(1)` (ni 0...0 ni 1...1).

Pour couvrir `e_i`, il faut un implicant `x_{i'} ∧ ~x_{j'}` satisfait
par `e_i`. Donc `x_{i'} = 1` dans `e_i` ⇒ i' = i (l'unique position à 1).
Et `x_{j'} = 0` dans `e_i` ⇒ j' ≠ i (n'importe quel autre indice).

Donc tout DNF couvrant `f^{-1}(1)` doit contenir au moins un implicant
"sortant de i" (de la forme `x_i ∧ ~x_j`) pour chaque i. Donc
`|DNF| ≥ n`. ∎

**(iv) défaut = n(n−1) − n = n(n−2)**. ✓

**L20 (i)-(iv) prouvé combinatoirement pour tout n ≥ 3.**

### 3. Statut de L20.5 (unicité)

**Énoncé** : les antipodales sont les SEULES fonctions à atteindre
défaut maximal n(n−2).

**Vérification empirique** :
- n=3 (254 fonctions non-constantes) : 4 fonctions à défaut 3 (max),
  toutes antipodales (alpha ∈ {000, 001, 010, 011}). ✓
- n=4 (65 534 fonctions) : 8 fonctions à défaut 8 (max), toutes
  antipodales (alpha ∈ {0000, …, 0111}). ✓
- n ≥ 5 : énumération de `2^{2^n}` fonctions infaisable.

**Statut** : conjecturé pour tout n. Pas de preuve structurelle fournie.
**Honnêtement reconnu** par le Proposeur. Pour démontrer, il faudrait
montrer : toute fonction non-antipodale a défaut < n(n−2).

### 4. Test des barrières

- **Relativisation** : argument combinatoire sans oracle. ✓
- **RR** : la classe des antipodales est petite (`2^{n-1}` parmi `2^{2^n}`).
  Non-large. RR sans objet. ✓
- **Algébrisation** : pas d'arithmétisation. ✓

### 5. ⚠️ Note importante sur le lien à P vs NP

Le Proposeur écrit :
> *« Les fonctions antipodales constituent une famille polynomiale sur
> laquelle un solveur DNF doit faire un vrai set cover non-trivial. C'est
> une **barrière structurelle** pour les heuristiques de minimisation. »*

**Je nuance** :

- **Sur les antipodales spécifiquement, DNF-MIN est facile** : `DNF_min = n`,
  trivialement calculable par le cycle (n est petit, calcul polynomial).
- Le « défaut maximal » signifie que **beaucoup d'implicants premiers
  sont redondants** dans le DNF canonique. Mais cela ne signifie pas que
  la minimisation est NP-difficile sur cette famille. Au contraire, sur
  les antipodales, on connaît le DNF minimal en temps O(n).
- La Σ₂^P-difficulté de DNF-MIN (Umans 1999) vient de réductions
  complexes depuis SAT généralisé, pas des antipodales.

Donc **les antipodales sont une famille avec défaut explicite, pas un
témoin de Σ₂^P-difficulté**. Le lien à P vs NP est plus faible que
revendiqué : c'est un exemple combinatoire élégant, pas un certificat de
difficulté pour DNF-MIN.

L20 reste cependant un théorème valide et utile pour cartographier le
paysage des fonctions DNF.

### Verdict : ✅ ÉTABLI POUR P vs NP — 8e objet

Théorème L20 (i)-(iv) prouvé combinatoirement pour tout n ≥ 3, vérifié
empiriquement n=3, 4, 5. L20.5 (unicité) reste conjecturée pour n ≥ 5.

---

## Apport et nuance

### Apport au dépôt

- **Pôle extrême opposé à Tour 19**. Tour 19 caractérisait la classe
  (α)/(β) (« minimisation triviale, |primes| = DNF_min »). Tour 20
  identifie l'extrême opposé : les fonctions à *défaut maximal* parmi
  toutes les fonctions sur n variables.
- **Famille combinatoire élégante** : antipodales paramétrées par
  `2^{n-1}` paires, structure régulière (`#primes`, `DNF_min`, défaut
  identiques pour toutes).
- **Preuves combinatoires complètes** pour (i)-(iv).

### Nuance honnête

- **Théorème probablement classique** en logique booléenne (Karnaugh,
  Quine-McCluskey). Apport mathématique au front de la recherche : zéro.
- **L20.5 non démontrée** pour n ≥ 5. Conjecturé, vérification
  exhaustive infaisable.
- **Pas P vs NP**. Toujours dans le paradigme AC⁰ d=2 / minimisation DNF.
  Le lien à la Σ₂^P-difficulté de DNF-MIN est plus faible que revendiqué :
  sur les antipodales, DNF-MIN est polynomial (`n`).
- **Saut qualitatif partiel** : Tour 20 sort de (α)/(β) mais reste dans
  le paradigme AC⁰ d=2. Pas de profondeur 3, pas de Lean, pas de Razborov.

### Statut du dépôt après Tour 20

| Acquis | Tour | Statut |
|---|---|---|
| `DNF_min(PARITY)` exponentiel | 12 | ✅ |
| Caractérisation IS(Q_n) | 13 | ✅ |
| `DNF_min(MAJ_n)` | 14 | ✅ |
| `DNF_min(THRESHOLD_t)` + dichotomie | 15 | ✅ |
| `DNF_min(MOD_p)` | 16 | ✅ |
| `DNF_min(IP_{2n})` + preuve structurelle | 17 + 18 | ✅ |
| Caractérisation (α)/(β) | 19 | ✅ |
| **Antipodales = cas extrême** | **20** | ✅ |

**Le dépôt cartographie maintenant les deux pôles du paradigme AC⁰ d=2 :
classe (α)/(β) (minimisation triviale) et cas extrême antipodales
(défaut maximal n(n-2)).**

## Conséquences pour la suite

- **Huitième entrée** dans la section ✅ Établis pour P vs NP.
- **Le paradigme AC⁰ d=2 est désormais cartographié bidirectionnellement**.
- **Le Tour 21 doit faire un VRAI saut qualitatif** vers une autre voie.
  Recommandations strictes :
  1. **Profondeur 3** (FSS-Håstad partiel) — direction la plus naturelle
     pour sortir.
  2. **Formalisation Lean** — premier objet certifié, direction la plus
     concrètement réalisable.
  3. **Démontrer L20.5 pour tout n** (preuve structurelle).
  4. **Démontrer la conjecture asymptotique de L19** (fraction → 0).
  5. **Razborov 1985 monotone CLIQUE** — lignée distincte.

  **Direction interdite (saturation)** : toute nouvelle caractérisation
  ou famille dans le paradigme AC⁰ d=2 / DNF-MIN sans saut qualitatif.

## Script de vérification

[`checks/tour_20_antipodal_verification.py`](../checks/tour_20_antipodal_verification.py)
— livré par le Proposeur, exécuté indépendamment. Énumère pour n=3, 4, 5
les `2^{n-1}` fonctions antipodales, calcule |primes|, DNF_min, défaut
pour chacune. Tous conformes à la formule théorique.

Note : un second fichier `tour_20_extreme_defect.py` est présent dans
`checks/` mais n'est pas le script principal de la proposition.
