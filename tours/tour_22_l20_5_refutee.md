# Tour 22 — Réfutation de L20.5 par contre-exemple à n=5 + acquis L22.A (cas dégénéré)

- **Date** : 2026-05-23
- **Proposeur** : Qwen Max
- **Réfuteur** : Claude (vérification indépendante par 2e algorithme)
- **Sous-but visé** : option 1 du Tour 22 (compléter L21.D pour clore L20.5).
- **Verdict** : ✅ **Tour réussi** mais par négation : L20.5 (Tour 20) et
  L21.D (Tour 21) sont **RÉFUTÉES** par contre-exemple double-vérifié.
  Acquis positif : **L22.A (cas dégénéré)** structurellement prouvée.

---

## Idée proposée (résumé fidèle)

Le Proposeur livre un contre-exemple direct à L20.5 :

> **Témoin canonique** : `Z = {00000, 00011, 00101, 11001, 11110}` (= `{0, 3,
> 5, 25, 30}` en décimal) sur `n = 5`, soit `f(x) = 1 ⟺ x ∉ Z`.
> Alors `|primes(f)| = 25`, `DNF_min(f) = 8`, défaut = `17 > n(n−2) = 15`.

Le tour livre aussi un acquis structurel positif :

> **L22.A (cas dégénéré, prouvé)** : si `Z = f^{-1}(0)` est coord-dégénéré sur
> une position `j` (toutes les affectations de Z ont la même valeur sur `j`),
> alors `défaut(f) = défaut(g) ≤ (n−1)(n−3) < n(n−2)` où `g` est la fonction
> à n−1 variables obtenue en éliminant `j`.

---

## Vérification du Réfuteur

### 1. Audit structurel du témoin

- **Z antipodal ?** Pour chaque `z ∈ Z`, je vérifie si `¬z ∈ Z` :
  - `0 (00000) ↔ 31 (11111)` ? 31 ∉ Z. ✗
  - `3 (00011) ↔ 28 (11100)` ? 28 ∉ Z. ✗
  - `5 (00101) ↔ 26 (11010)` ? 26 ∉ Z. ✗
  - `25 (11001) ↔ 6 (00110)` ? 6 ∉ Z. ✗
  - `30 (11110) ↔ 1 (00001)` ? 1 ∉ Z. ✗

  Aucune paire antipodale. ✓ Z n'est pas antipodal.

- **Z coord-dégénéré ?** Bits par position :
  - bit 4 : (0, 0, 0, 1, 1) mix
  - bit 3 : (0, 0, 0, 1, 1) mix
  - bit 2 : (0, 0, 1, 0, 1) mix
  - bit 1 : (0, 1, 0, 0, 1) mix
  - bit 0 : (0, 1, 1, 1, 0) mix

  Toutes les positions mixées. ✓ Coord-non-dégénéré.

### 2. Vérification indépendante du triplet par 2e algorithme

J'ai écrit [`checks/tour_22_refuter_l20_5.py`](../checks/tour_22_refuter_l20_5.py)
qui calcule `(|primes|, DNF_min)` par méthode **distincte** de celle du
Proposeur :
- Énumération exhaustive des 3^5 = 243 ANDs.
- Test d'implication direct via la table de vérité.
- Set cover via PuLP/CBC (ILP exact).

**Résultat** :
```
|primes| = 25
DNF_min = 8
défaut = 17

Distribution des tailles : {2: 2, 3: 21, 4: 2}
```

**Triplet (25, 8, 17) confirmé indépendamment.** Bug d'implémentation
exclu : deux algorithmes distincts (Proposeur : hitting sets ;
Réfuteur : ANDs+ILP) convergent sur le même résultat.

`défaut = 17 > 15 = n(n−2)`. **L20.5 réfutée.**

### 3. Audit de L22.A (cas dégénéré)

**Énoncé** : si Z est coord-dégénéré sur position j avec valeur b (tous
z ∈ Z ont `z_j = b`), alors :
- `ℓ_j = (x_j si b=0, ¬x_j si b=1)` est l'unique prime de taille 1
  associé à cette dégénérescence.
- `|primes(f)| = 1 + |primes(g)|` où g = f restreint à `x_j = b`.
- `DNF_min(f) = 1 + DNF_min(g)`.
- défaut(f) = défaut(g) ≤ (n−1)(n−3) par récurrence.

**Audit (WLOG j = n−1, b = 0)** :

(a) `ℓ = x_{n-1}` est implicant : pour tout x avec `x_{n-1} = 1`, `x ∉ Z`
(car tous z ∈ Z ont `z_{n-1} = 0`). ✓

(b) `ℓ` est premier : taille 1, on ne peut rien enlever. ✓

(c) Tout autre prime M de f ne contient ni `x_{n-1}` ni `¬x_{n-1}` :
  - Si `x_{n-1} ∈ M`, alors `{x_{n-1}}` (qui est implicant) domine `M`,
    donc `M` non premier.
  - Si `¬x_{n-1} ∈ M` : le littéral `¬x_{n-1}` est satisfait par tous
    `z ∈ Z` (qui ont `z_{n-1} = 0`), donc inutile pour exclure Z.
    `M \ {¬x_{n-1}}` reste implicant, donc M non premier.

(d) Bijection `primes(f) \ {x_{n-1}} ↔ primes(g)` (par restriction).

(e) Pour DNF_min : le littéral `x_{n-1}` est nécessaire pour couvrir
les `(z', 1)` avec `z' ∈ Z_g` (qui sont dans `f^{-1}(1)` car
`(z', 1) ∉ Z`, mais ne sont couverts par aucun prime de g car
`g(z') = 0`). Donc `DNF_min(f) = 1 + DNF_min(g)`. ✓

(f) défaut(f) = (1 + |primes(g)|) − (1 + DNF_min(g)) = défaut(g). ✓

(g) Par récurrence sur n : défaut(g) ≤ (n−1)(n−3). Or (n−1)(n−3) < n(n−2)
⟺ `n² − 4n + 3 < n² − 2n` ⟺ `-4n + 3 < -2n` ⟺ `n > 3/2`. ✓ pour n ≥ 2.

**L22.A est correctement prouvée pour tout n ≥ 3.** ✓

### 4. Statistiques du Proposeur (1280 contre-exemples à n=5, k=5)

Le Proposeur rapporte :
- 320 fonctions à défaut 17 (= 15 + 2).
- 960 fonctions à défaut 16.
- Total 1280 contre-exemples à L20.5 sur 201 376 zero-sets de taille 5.
- 0 / 1280 coord-dégénérés (cohérent avec L22.A).
- 0 / 1280 contiennent une paire antipodale.

Je n'ai pas vérifié les 1280 individuellement, mais un seul contre-exemple
suffit à réfuter L20.5. La statistique du Proposeur indique que **ce n'est
pas un cas isolé** mais une famille substantielle de fonctions
« anti-antipodales » dépassant la borne `n(n−2)`.

### 5. Test des barrières

Sans objet pour une réfutation négative. Pas de borne inférieure de circuit
revendiquée → ni RR, ni algébrisation, ni relativisation ne s'appliquent.

### 6. Verdict détaillé

**Tour 20 (révision)** :
- L20 (i)-(iv) : ✅ **maintenu**. Les antipodales ont bien `|primes|=n(n−1)`,
  `DNF_min = n`, défaut = `n(n−2)`. Calcul correct.
- L20.5 (corollaire conjectural) : ❌ **RÉFUTÉ**. Les antipodales **ne sont
  pas** les seules à atteindre le défaut maximal. Pire, elles n'atteignent
  même pas le défaut maximum *réel* à n=5 (qui est ≥ 17 > 15).

**Tour 21 (révision)** :
- L21.A, L21.B, L21.C : ✅ maintenus.
- L21.D : ❌ **RÉFUTÉ**. Pour `k = 5`, défaut peut dépasser `n(n−2)`.
  La lacune du Tour 21 n'est pas réparable — elle est fausse.

**Tour 22** :
- L22.A (cas dégénéré) : ✅ **ÉTABLI** structurellement. Premier *vrai*
  acquis du tour.
- L22.B (réfutation L20.5/L21.D par contre-exemple) : ✅ **CONFIRMÉ** par
  vérification indépendante. Réfutation établie.

### 7. Apport méthodologique

- **Premier tour qui réfute un ÉTABLI partiel précédent** du dépôt. Jusqu'ici,
  les réfutations ont concerné des FAILLES FATALES (audit initial) ou des
  LACUNES RÉPARABLES (audit initial). Tour 22 réfute un objet déjà accepté
  partiellement (Tour 20).

- **Confirme la condition (j)** : Tour 20 avait extrapolé L20.5 de 2 points
  (n=3, n=4) sans vérifier n=5. C'est le pattern réfuté par Tour 9 (« vraie
  n=4, fausse n=5 ») — **réapparu malgré l'avertissement explicite du cahier
  §4 question 10**. Le Réfuteur (moi) n'a pas insisté assez sur la
  vérification n=5 au Tour 20. Leçon : sur les conjectures asymptotiques
  basées sur 2 points, exiger systématiquement le test au point suivant
  avant ÉTABLISSEMENT.

- **Algorithme hitting set** plus rapide que énumération `3^n` ANDs pour
  `k << n`. Outil utile pour vérifier des contre-exemples plus larges (k=5,
  6, etc.) sur des n modérés.

---

## Conséquences pour le cahier

**Mise à jour requise** :

1. **Tour 20** : tableau ligne 20 doit indiquer L20.5 → ❌ Réfuté. Mais
   conserver L20 (i)-(iv) ÉTABLI. Statut global : ✅ partiel (sur (i)-(iv)).

2. **Tour 21** : tableau ligne 21 doit indiquer L21.D → ❌ Réfuté. L21
   passe de ⚠️ LACUNE RÉPARABLE à ❌ FAILLE FATALE (l'objectif initial,
   prouver L20.5, est impossible).

3. **Tour 22** : nouveau tableau ligne 22 : ✅ Réfutation + L22.A acquis.
   2 sous-objets : un négatif (réfutation), un positif (L22.A).

4. **Section ✅ Établis** :
   - L20 → garder mais limiter à (i)-(iv) ; retirer mention L20.5.
   - L22.A → ajouter comme 9e objet (cas dégénéré pour tout n).

5. **Section ❌ Réfutés** :
   - Ajouter L20.5 (antipodales pas uniques au défaut max).
   - Ajouter L21.D (défaut < n(n−2) faux pour k ≥ 3).

6. **§4 Questions ouvertes** :
   - Ajouter q. 12 : « toute extrapolation d'un théorème asymptotique à
     partir de ≤ 2 points est suspecte. Exiger systématiquement le test
     au point suivant avant ÉTABLISSEMENT ».

7. **Sous-but Tour 23** :
   - Soit étudier la nouvelle borne supérieure du défaut à n=5 (mais le
     Proposeur s'en abstient honnêtement pour ne pas reproduire l'erreur).
   - Soit pivoter vers profondeur 3 ou Razborov monotone (vraies
     directions ouvertes).
   - Soit poser une nouvelle question structurelle : *quelle est la classe
     des fonctions à défaut max pour n donné* ? Question ouverte légitime,
     mais possiblement Σ₂^P-difficile.

## Nuance honnête

- **Pas un acquis pour P vs NP.** C'est une correction de catalogage.
- **Acquis positif (L22.A) modeste** : caractérise le cas dégénéré.
- **Erreur méthodologique du Tour 20 répétée** : 2 points ne suffisent pas.
  Le cahier l'avait pourtant explicité (q.10). À tirer comme leçon.
- **Distance à P vs NP** : inchangée, astronomique.

## Script de vérification

[`checks/tour_22_refuter_l20_5.py`](../checks/tour_22_refuter_l20_5.py) —
vérification indépendante par méthode distincte (énumération 3^5 ANDs +
ILP PuLP/CBC). Confirme le triplet (25, 8, 17) pour le témoin canonique
`Z = {0, 3, 5, 25, 30}`. Bug d'implémentation exclu.
