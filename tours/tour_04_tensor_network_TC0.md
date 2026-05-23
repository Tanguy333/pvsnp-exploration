# Tour 04 — Contraction tensorielle pour CAPP sur TC⁰ (méthode Williams + low-entanglement)

- **Date** : 2026-05-23
- **Proposeur** : Qwen Max
- **Réfuteur** : Claude
- **Sous-but visé** : classe restreinte + non-relativisant + non-algébrisant + invariance logique + robustesse aux sauts polynomiaux.
- **Verdict** : ❌ **FAILLE FATALE** sur le mécanisme proposé (le Lemme 1 est faux comme contre-exemple explicite). Ce qui reste n'est pas une piste mais une reformulation du programme Williams.

---

## Idée proposée (résumé fidèle)

Compiler tout circuit `TC⁰` de profondeur `d` et taille `S` en un **réseau de
tenseurs** (MERA ou PEPS) de bond dimension `χ = S^{O(d)}` polynomiale.
Exploiter la décroissance des valeurs singulières pour contracter ce réseau
en temps `2^n / n^{ω(1)}` (algorithme CAPP non-trivial pour `TC⁰`). Par le
théorème de Williams, en déduire `NEXP ⊄ TC⁰`. Par hardness magnification,
amplifier en `NP ⊄ TC⁰`.

Barrières revendiquées toutes franchies : relativisation (Williams),
algébrisation (Williams), preuves naturelles (propriété de classe), invariance
logique (cible = classe de fonctions), sauts polynomiaux (TC⁰ les modélise
nativement).

Aveux du Proposeur : (1) Lemme 2 (la contraction efficace) est un mur ; (2)
l'amplification à NP est conditionnelle ; (3) « ceci est une feuille de route,
pas une démonstration ».

---

## Réfutation

### 1. Reformulation

Importer les outils des tensor networks de physique quantique (MERA, PEPS,
SVD adaptative) dans le programme algorithmique de Williams pour TC⁰, en
postulant que les fonctions TC⁰ ont une « faible intrication » exploitable
algorithmiquement.

### 2. Constat préliminaire — les 5 conditions formelles sont cochées

Honnêtement, l'idée passe la grille de bon sens préalable :
- (a) **Classe restreinte** : TC⁰, classe de fonctions bien définie. ✓
- (b) **Non-relativisant** : la méthode algorithmique de Williams est l'unique
  technique connue ayant franchi BGS frontalement. ✓ (revendication crédible)
- (c) **Non-algébrisant** : Williams 2011 (NEXP ⊄ ACC⁰) est explicitement non-
  algébrisant (Aaronson-Wigderson 2008 cite ce résultat comme exemple). ✓
- (d) **Invariance logique** : la complexité en circuits est invariante sous
  équivalence logique. ✓
- (e) **Sauts polynomiaux** : TC⁰ peut additionner / multiplier des entiers,
  donc modifier `n^c` bits en profondeur constante. ✓

C'est la première piste qui *traverse* la grille préalable. Il faut donc
attaquer le contenu technique, pas les conditions formelles.

### 3. La faille tueuse — **Lemme 1 est faux** (vérifié par calcul)

Le Proposeur affirme : *« tout circuit TC⁰ de profondeur `d` et taille `S`
se représente comme un tensor network de bond dimension χ = S^{O(d)} »*.

Pour `S = poly(n)` et `d = O(1)`, cela donnerait χ polynomial. **C'est faux.**

**Contre-exemple : la fonction Inner Product modulo 2.**

`IP_n(x, y) = (x · y) mod 2` sur `2n` variables. Faits classiques :

- `IP_n ∈ TC⁰` — circuit de profondeur **2** et taille polynomiale (XOR de AND
  via portes à seuil ; cf. Hajnal-Maass-Pudlák-Szegedy 1993). Donc `S = poly(n)`,
  `d = 2`. Le Lemme 1 prédirait `χ = poly(n)^{O(1)} = poly(n)`.
- La bond dimension d'une fonction `f` à travers la coupe `A | B` est, par
  définition standard, le rang (sur ℝ, le corps des tensor networks
  physiques) de la matrice `M[a, b] = f(a, b)`. C'est exactement la
  dimension de la liaison dans toute décomposition MPS/PEPS à cette coupe.

**Vérification empirique (cf. [`checks/tour_04_tensor_network_TC0.py`](../checks/tour_04_tensor_network_TC0.py)) :**

| `n` | taille `M` | rang ℝ | rang F₂ | `2ⁿ` |
|---:|:---:|---:|---:|---:|
| 1 | 2 × 2 | 1 | 1 | 2 |
| 2 | 4 × 4 | 3 | 2 | 4 |
| 3 | 8 × 8 | 7 | 3 | 8 |
| 4 | 16 × 16 | 15 | 4 | 16 |
| 5 | 32 × 32 | 31 | 5 | 32 |
| 6 | 64 × 64 | 63 | 6 | 64 |
| 7 | 128 × 128 | 127 | 7 | 128 |
| 8 | 256 × 256 | **255** | 8 | 256 |

Le rang sur ℝ vaut `2ⁿ − 1` (la matrice est essentiellement la matrice de
Hadamard à un facteur près : `M = (J − H)/2` avec `H[x, y] = (−1)^{x·y}`).

**Bond dimension = 2ⁿ − 1 pour IP_n. Exponentielle.**

Pour un circuit TC⁰ de profondeur 2 et taille polynomiale, le Lemme 1
prédisait polynomial. Il prédit faux d'un facteur exponentiel.

### 4. La parade « passer à F₂ » ne sauve pas

On voit dans le tableau que le rang sur F₂ vaut `n` — polynomial. Le
Proposeur pourrait répliquer : *« je travaille sur F₂, donc bond dimension
polynomiale ».*

Cette parade échoue pour deux raisons :

1. **Le mécanisme de contraction proposé exige une structure métrique.** La
   « SVD adaptative » et la « décroissance des valeurs singulières » que le
   Proposeur invoque (Lemme 2) sont des objets analytiques sur ℝ ou ℂ : il
   n'existe pas de SVD sur F₂, pas de norme L², pas de notion de troncation
   par seuil. Travailler sur F₂ détruit précisément l'outillage emprunté à
   la physique quantique. La « faible intrication » au sens de von Neumann /
   Rényi est une notion strictement analytique.

2. **Sur F₂, le rang faible n'apporte pas la contraction sub-exponentielle.**
   Un rang `n` sur F₂ permet de représenter `M` comme une somme de `n`
   produits extérieurs sur F₂, soit `n × 2ⁿ` bits d'information — donc autant
   que la table de vérité elle-même au facteur `n` près. Aucun gain
   algorithmique pour la contraction (qui requiert un sketch *plus petit* que
   l'espace).

Donc *quel que soit le corps choisi*, l'argument « TC⁰ → low-bond-dim →
contraction efficace » ne fonctionne pas pour IP_n. Et IP_n n'est pas une
exotique : c'est le contre-exemple canonique en complexité de communication
(Chor-Goldreich 1988), précisément parce que TC⁰ peut calculer des fonctions
de complexité communication maximale.

### 5. La confusion structurelle sous-jacente

Le Proposeur conflate **« TC⁰ est petit »** et **« TC⁰ a faible intrication »**.
Ce sont deux choses différentes. Une fonction peut être calculable par un
petit circuit ET avoir une matrice de communication de rang plein.

C'est précisément pourquoi les bornes inférieures pour TC⁰ sont si dures :
les techniques de complexité communication (Yao, Razborov), de rang, de
discrépance, qui marchent pour AC⁰, **échouent toutes pour TC⁰**, parce que
TC⁰ peut calculer IP_n (et donc le produit scalaire mod 2, et donc atteindre
n'importe quelle complexité de communication Θ(n)). C'est connu depuis
30 ans. Le Proposeur ressuscite naïvement une technique d'évaluation de rang
sans savoir qu'elle a été tuée pour TC⁰ depuis Hajnal-Maass-Pudlák-Szegedy 1993.

### 6. Sans le Lemme 1, ce qui reste n'est pas une piste

Si on retire la revendication tensor-network-à-bond-polynomiale, l'idée se
réduit à :

> *« Trouver un algorithme CAPP en temps `2^n / n^{ω(1)}` pour TC⁰, et
> appliquer le théorème de Williams. »*

C'est **exactement** le programme de recherche actif en complexité depuis
2010, poursuivi par Williams, Murray, Chen, Tamaki, Servedio, Tal et
plusieurs autres. Aucun algorithme de ce type n'est connu pour TC⁰ (le
résultat actuel le plus fort est pour ACC⁰, c'est-à-dire la classe immédiatement
plus *faible* que TC⁰ ; pour TC⁰, même au niveau de profondeur 2, c'est ouvert).

Le Proposeur n'apporte aucune contribution algorithmique nouvelle. Il
suggère que les tensor networks « pourraient être le bon langage », sans
prouver ni même esquisser que cette approche progresse. Or il s'est lui-même
imposé (et acquiesçant à mon sous-but du Tour 4) la contrainte (c) :
*démontrer le caractère non-algébrisant par exhibition d'un oracle séparateur
ou argument équivalent à la Williams 2011*. Il ne le fait pas — il pointe
vers Williams 2011, sans contribuer.

### 7. Bonus structurel : la barrière de la *hardness magnification*

L'Aveu 2 du Proposeur (« l'amplification à NP est conditionnelle ») sous-
estime le problème. Depuis 2018, plusieurs résultats (Chen-Hirahara-Oliveira-
Pich-Rajgopal-Santhanam 2019 ; McKay-Murray-Williams 2019 ; Oliveira-Pich
2020) ont mis en évidence des **barrières internes** à la magnification :

- Les théorèmes de magnification connus traduisent une borne inférieure
  *faible mais explicite* (`MCSP` ou `MKtP` super-linéaire) en une borne
  inférieure *forte* (`NEXP ⊄ ACC⁰` ou similaire). Mais la pré-condition
  (borne faible) reste hors d'atteinte par les techniques actuelles.
- Plus profondément : certaines magnifications appliquées naïvement seraient
  *naturalisantes* au sens de Razborov-Rudich, donc condamnées par la
  barrière des preuves naturelles. Cf. Chen-Hirahara-Oliveira-Pich-Rajgopal-
  Santhanam 2019, *« Beyond Natural Proofs : Hardness Magnification »*, qui
  identifie un nouveau type de barrière interne à magnification.

Le Proposeur invoque la magnification comme si elle était un outil disponible.
Elle ne l'est pas : c'est un domaine actif avec ses propres barrières non
résolues.

### 8. Verdict : ❌ FAILLE FATALE sur le mécanisme proposé

Le mécanisme spécifique (compilation TC⁰ → tensor network à bond polynomiale,
contraction efficace, application du théorème de Williams) est :

- **Faux au Lemme 1** : IP_n est un contre-exemple direct, calculé. *(vérifié)*
- **Sans réparation** sur F₂ : l'outillage métrique nécessaire à la contraction
  efficace n'existe pas. *(argument structurel)*
- **Reposant sur un Lemme 2 ouvert** que le Proposeur reconnaît ne pas avoir.
- **Reposant sur une magnification dont les barrières internes sont elles-mêmes
  un domaine ouvert.**

Une fois l'erreur du Lemme 1 retirée, ce qui reste — « trouver un algorithme
CAPP pour TC⁰ et appliquer Williams » — n'est pas une piste mais une
reformulation du problème ouvert principal du domaine.

---

## Nuance honnête

C'est la première piste qui satisfait formellement les 5 conditions du
sous-but. Le Proposeur a entendu le feedback des Tours 1-3 et choisi un
cadre adéquat (TC⁰ + Williams). Le problème n'est plus dans la stratégie
globale — il est dans l'apport technique : aucun.

Le programme **Williams pour TC⁰** est légitimement la direction la plus
prometteuse aujourd'hui pour P vs NP, et il avance lentement mais réellement
(Chen-Williams 2019, Chen-Lyu-Williams 2020, etc. sur des sous-classes de
TC⁰). Les tensor networks ont effectivement été utilisés en complexité
quantique (Aaronson, Bravyi, Gosset), mais pour la complexité booléenne
classique, leur apport reste à démontrer. La conjecture « TC⁰ a faible
intrication » est *réfutée* par IP_n.

## Conséquences pour la suite

- Piste 4 classée **❌ Réfutée** (mécanisme tensor network) dans le cahier de
  bord.
- Note honnête ajoutée : la *direction générale* (Williams pour TC⁰) reste
  active, mais sans algorithme CAPP nouveau, ce n'est pas une piste pour
  notre boucle adverse — c'est un programme de recherche de la communauté.
- Question ouverte ajoutée : tout argument de type « low-something pour
  TC⁰ » (low-rank, low-bond-dim, low-degree) doit d'abord exhiber un test
  positif sur IP_n (où ces quantités sont exponentielles). C'est un sanity-
  check préalable.
- Sous-but Tour 5 : exiger une **contribution algorithmique ou structurelle
  CONCRÈTE** au-delà de la simple stratégie. Pas seulement « voici le bon
  cadre », mais « voici un sous-théorème prouvable, ou un calcul vérifiable
  qui fait progresser X ».

## Script de vérification

[`checks/tour_04_tensor_network_TC0.py`](../checks/tour_04_tensor_network_TC0.py)
— calcul direct du rang de la matrice `M[x, y] = (x · y) mod 2` pour
`n ∈ [1, 8]`, sur ℝ (via numpy) et sur F₂ (élimination de Gauss-Jordan
manuelle). Sur ℝ : rang = `2ⁿ − 1`. Bond dimension exponentielle.
