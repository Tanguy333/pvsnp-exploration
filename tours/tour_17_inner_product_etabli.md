# Tour 17 — `DNF_min(IP_{2n}) = (3^n − 1)/2` vérifié à n=1,2,3,4 (✅ Établi empiriquement, conjecture pour tout n)

- **Date** : 2026-05-23
- **Proposeur** : Qwen Max
- **Réfuteur** : Claude (test n=4 ajouté)
- **Sous-but visé** : direction ouverte Tour 17, option 4 (INNER PRODUCT,
  lignée Karchmer-Wigderson).
- **Verdict** : ✅ **ÉTABLI POUR P vs NP** au sens empirique fort (4 points
  consécutifs vérifiés par ILP exact) — sixième objet positif du dépôt,
  avec **note explicite** : la formule reste **conjecturale** pour `n ≥ 5`,
  faute de preuve structurelle.

---

## Idée proposée (résumé fidèle)

**Conjecture L17.** *Pour tout `n ≥ 1`, `DNF_min(IP_{2n}) = (3^n − 1)/2`,
où `IP_{2n}(x_0, …, x_{n−1}, y_0, …, y_{n−1}) = ∑_i x_i y_i (mod 2)`.*

Cette fonction est :
- **Non-monotone** : `IP_4(1, 0, 1, 0) = 1` et `IP_4(1, 1, 1, 0) = 1`, mais
  `IP_4(0, 0, 1, 0) = 0`. Flipper certains bits change la valeur.
- **Non-symétrique** : la dépendance en `x` est différente de celle en `y`.
- **Hors classe L13** : `IP^{-1}(1)` n'est pas un independent set de
  `Q_{2n}` (vérifié explicitement : voisins Hamming-1 dans `IP^{-1}(1)`).

L13 (Tour 13) prédit donc `DNF_min(IP_{2n}) < |IP^{-1}(1)|` strictement. Le
calcul direct le confirme :

| n | 2n | \|IP^{-1}(1)\| | (3^n − 1)/2 |
|---:|---:|---:|---:|
| 1 | 2 | 1 | 1 |
| 2 | 4 | 6 | 4 |
| 3 | 6 | 28 | 13 |
| 4 | 8 | 120 | 40 |

---

## Vérification du Réfuteur

### 1. Reproduction du calcul du Proposeur (n=1, 2, 3)

Script `tour_17_inner_product_dnf.py` exécuté indépendamment, n=2 et n=3 :

- **n=2** : 81 ANDs, 10 implicants, 4 implicants premiers (tous taille 3),
  DNF_min = 4 par set cover exhaustif. ✓
- **n=3** : 729 ANDs, 76 implicants, 13 implicants premiers (12 de taille 4
  + 1 de taille 6), DNF_min = 13 par set cover exhaustif. ✓

### 2. Extension à n=4 (effectuée par le Réfuteur)

Le set cover exhaustif explose à n=4 (potentiellement
`C(|primes|, 40)` combinaisons). J'ai installé **PuLP** et écrit
[`checks/tour_17_extension_n4.py`](../checks/tour_17_extension_n4.py) qui
résout le set cover par **ILP exact** (solveur CBC).

**Résultat n=4** :
- 6561 ANDs énumérés.
- 520 implicants identifiés.
- **40 implicants premiers** (32 de taille 5 + 8 de taille 7).
- ILP set cover résolu en 0.0s.
- **DNF_min(IP_8) = 40 = (3^4 − 1)/2.** ✓

**Conjecture confirmée à n=4.**

### 3. Observation structurelle remarquable

| n | \|primes\| | DNF_min | Distribution tailles |
|---:|---:|---:|---|
| 2 | 4 | 4 | tous taille 3 (= 2n−1) |
| 3 | 13 | 13 | 12 taille 4 (= 2n−2) + 1 taille 6 (= 2n) |
| 4 | 40 | 40 | 32 taille 5 (= 2n−3) + 8 taille 7 (= 2n−1) |

**À chaque n testé, `|primes| = DNF_min`.** Cela signifie que **tous les
implicants premiers sont nécessaires** dans le DNF minimal (couverture
non-redondante).

Si on prouvait structurellement :
1. `|primes(IP_{2n})| = (3^n − 1)/2`, et
2. tous les implicants premiers sont nécessaires (chaque affectation
   `x ∈ IP^{-1}(1)` est couverte par un unique implicant premier minimal),

alors L17 serait prouvé pour tout `n`.

**Observation 2 vérifiée empiriquement** à n=2, 3, 4 (ILP donne
exactement `|primes|`, donc chaque implicant premier est requis).

**Observation 1 reste conjecturale**. La formule (3^n − 1)/2 et le pattern
de tailles d'implicants ne semblent pas découler d'une formule combinatoire
évidente.

### 4. Test des barrières

- **Relativisation** : preuve combinatoire et calcul exhaustif sans oracle. ✓
- **Razborov-Rudich** : la propriété « f = IP_{2n} » caractérise une
  fonction unique parmi `2^{2^{2n}}`. Non-large, RR sans objet. ✓
- **Algébrisation** : pas d'arithmétisation polynomiale. Note : IP a une
  représentation polynomiale `IP(x, y) = (1 − ∏_i (1 − 2 x_i y_i))/2`, mais
  on ne l'utilise pas. Argument combinatoire pur. ✓

### 5. Apport au dépôt

**Diversification réussie** :
- Première fonction **hors classe L13** (`IP^{-1}(1)` non independent).
- Fonction **non-monotone non-symétrique**, structurellement distincte des
  THRESHOLD/PARITY/MOD.
- **Nouvelle méthode** : ILP set cover, réutilisable.
- **Nouveau coefficient exponentiel** : `log_2 3 ≈ 1.585` (vs `log_2 4 = 2`
  pour MAJ). Première distinction quantitative entre deux fonctions
  super-polynomiales du dépôt.

**Lignée Karchmer-Wigderson** ouverte : IP est la fonction canonique en
complexité de communication (Chor-Goldreich 1988, complexité communication
exactement `Θ(n)`).

**Application non-triviale de L13 par contraposée** : on utilise L13 pour
exclure `IP^{-1}(1)` de la classe L13 (en exhibant des voisins Hamming-1),
puis on calcule DNF_min par d'autres moyens. Validation de L13 comme outil
de classification.

### 6. Verdict : ✅ ÉTABLI POUR P vs NP (avec note conjecturale)

**Établi au sens empirique fort** :
- 4 points consécutifs (n=1, 2, 3, 4) vérifiés exactement.
- ILP exact donne DNF_min = (3^n − 1)/2 à n=4 (40 implicants premiers, tous
  requis).
- Méthode rigoureuse (énumération + ILP).

**Conjectural pour `n ≥ 5`** :
- Pas de preuve structurelle générale.
- Le Proposeur le note honnêtement en aveux.
- Le pattern (3^n − 1)/2 est suggéré par 4 points mais pas démontré.

**Différence avec Tours 12-16** :
- Tours 12-16 : théorème prouvé pour tout n + vérifié n=4.
- Tour 17 : vérifié n=1, 2, 3, 4 mais conjecture pour n ≥ 5.

C'est un **statut intermédiaire**, plus solide que conjecture pure (4 points
consécutifs sans exception) mais moins solide que théorème (sans preuve
générale). Marqué ✅ ÉTABLI avec note explicite.

---

## Nuance honnête

- **Conjecture L17.3 vérifiée à 4 points, pas prouvée**. C'est le seul ÉTABLI
  du dépôt sans preuve générale.

- **Théorème probablement classique**. La formule `DNF_min(IP_{2n}) = (3^n − 1)/2`
  est élégante ; il est probable qu'elle figure dans la littérature
  (Quine-McCluskey 1956+, BiSat optimization). Recherche bibliographique non
  effectuée par le Proposeur (limitation honnête notée).

- **Pas P vs NP.** `AC⁰ d=2 polynomial ⊊ P` est connu depuis FSS 1981 et
  acquis dès Tour 12. Tour 17 ajoute IP comme nouveau témoin de cette
  séparation, avec coefficient exponentiel `log_2 3` différent.

- **Diversification réussie** : sortie effective de la classe L13. La méthode
  ILP est complètement nouvelle pour le dépôt et réutilisable.

- **Conditions (a)–(n) honorées** :
  - (h) : script livré et exécuté à n=2, 3 par le Proposeur.
  - (j) : test à n=1, 2, 3 par le Proposeur ; **extension à n=4 par le Réfuteur** via ILP.
  - (i)(k) : lien P vs NP explicite (lignée FSS + Karchmer-Wigderson).
  - (l) : référence au cahier (mention de la condition (n) du Tour 16).
  - (m) : séparation par témoin, pas inclusion stricte.
  - (n) : pas d'application de L13 ; nouvelle méthode (ILP set cover).

- **Note sur la nuance (n)** : Tour 17 utilise L13 comme **diagnostic
  négatif** (vérifier que `IP^{-1}(1)` n'est pas independent), pas comme
  outil de production. Le calcul de DNF_min nécessite réellement une nouvelle
  méthode. La condition (n) est donc respectée.

## Sous-but Tour 18

Trois directions possibles, suite à L17 :

1. **Preuve structurelle de L17 pour tout n** : si le Proposeur (ou le
   Réfuteur) peut prouver `|primes(IP_{2n})| = (3^n − 1)/2` + non-redondance
   pour tout n, alors L17 devient un véritable théorème (et non plus une
   conjecture vérifiée à 4 points). Direction la plus aboutissante mais
   incertaine.

2. **Profondeur 3** : entrer dans le territoire FSS-Håstad sur n=4 avec une
   nouvelle fonction (par exemple IP). Beaucoup plus dur.

3. **Formalisation Lean** d'un sous-lemme acquis (par exemple L12.1 ou L13).
   Premier théorème certifié du dépôt.

## Scripts de vérification

- [`checks/tour_17_inner_product_dnf.py`](../checks/tour_17_inner_product_dnf.py)
  — livré par le Proposeur, vérification à n=1, 2, 3 par set cover exhaustif.

- [`checks/tour_17_extension_n4.py`](../checks/tour_17_extension_n4.py)
  — extension du Réfuteur à n=4 via ILP exact (PuLP + CBC). Confirme la
  conjecture à 40 = (3^4 − 1)/2.
