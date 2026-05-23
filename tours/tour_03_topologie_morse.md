# Tour 03 — Obstruction topologique par théorie de Morse discrète

- **Date** : 2026-05-23
- **Proposeur** : Qwen Max
- **Réfuteur** : Claude
- **Sous-but visé** : classe restreinte + non-relativisant ET non-algébrisant.
- **Verdict** : ❌ **FAILLE FATALE**

---

## Idée proposée (résumé fidèle)

Étudier le **paysage d'énergie** d'un CSP : pour chaque assignation `w ∈ {0,1}^m`,
définir `E(w)` = nombre de contraintes violées par `w`. Les sous-niveaux
`L_k = {w : E(w) ≤ k}` sont des complexes simpliciaux dans le cube booléen
muni de la métrique de Hamming. L'invariant proposé est la **somme des
nombres de Betti** `Σ β_i(L_k)`.

Squelette :
- **Lemme 1** : pour des familles CSP en phase RSB ou sur expandeurs,
  `Σ β_i(L_k)` croît exponentiellement.
- **Lemme 2 (LS discret)** : tout champ de vecteurs discret E-compatible
  (au sens de Forman) doit avoir `≥ Σ β_i(L_k)` cellules critiques.
- **Lemme 3** : un algorithme `P` est un champ de vecteurs **à sauts bornés**.
- **Lemme 4** : conjonction → tout algo `P` est piégé ou erre
  exponentiellement → SAT ∉ P.

Barrières revendiquées : relativisation (Hamming exige du white-box),
algébrisation (Õ détruit la structure discrète), Razborov-Rudich (l'invariant
n'est pas une propriété de la fonction).

Aveux : (1) saut MT→cube non rigoureux ; (2) calcul Betti #P-dur ; (3)
LS-discret-à-sauts est un problème ouvert ; (4) pas de preuve complète.

---

## Réfutation

### 1. Reformulation

Mesurer la « difficulté physique » d'un CSP par les nombres de Betti des
sous-niveaux de son énergie syntaxique, et invoquer un théorème de
Lusternik-Schnirelmann discret pour minorer le temps de calcul de tout
algorithme polynomial.

### 2. Failles structurelles — deux fatales, vérifiées par calcul

#### (a) **L'invariant n'est PAS un invariant de la fonction booléenne** *(faille terminale)*

Le Proposeur le dit lui-même, sans en mesurer la conséquence :
> *« Deux formules logiquement équivalentes peuvent avoir des paysages
> topologiques radicalement différents. »*

C'est *exactement* ce qui condamne l'idée. Soient `ψ` et `ψ'` deux CNF qui
calculent la même fonction booléenne (mêmes témoins, même classification
SAT/UNSAT). Pour que l'argument du Proposeur sépare `P` de `NP`, il faut
que l'invariant `β_i(L_k(φ))` soit invariant sous équivalence logique —
sinon, l'algorithme `P` qui décide la fonction (et non la présentation) n'a
aucune raison d'« hériter » de la complexité topologique d'une présentation
particulière.

**Vérification empirique (cf. [`checks/tour_03_topologie_morse.py`](../checks/tour_03_topologie_morse.py), partie A) :**

Prenons sur `m = 6` variables :
- `ψ  = (x_0 ∨ x_1) ∧ (x_2 ∨ x_3) ∧ (x_4 ∨ x_5)`             (3 clauses)
- `ψ' = ψ avec chaque clause triplée`                          (9 clauses)

Les deux ont **exactement 27 témoins identiques** (fonction booléenne
identique). On calcule l'invariant `Σ β_i(L_k)` proposé. Le 6-cube est
biparti, donc Hamming-1 n'a pas de triangles → le complexe de drapeau est un
1-complexe pur, donc `β_i = 0` pour `i ≥ 2`, et `Σ β_i = β_0 + β_1` avec
`β_1 = |E| − |V| + β_0`.

| k | \|L_k(ψ)\| | β_0 | β_1 | **Σ β_i(ψ)** | \|L_k(ψ')\| | β_0 | β_1 | **Σ β_i(ψ')** |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 27 | 1 | 28  | **29** | 27 | 1 | 28 | **29** |
| 1 | 54 | 1 | 91  | **92** | 27 | 1 | 28 | **29** |
| 2 | 63 | 1 | 124 | **125** | 27 | 1 | 28 | **29** |

À `k = 0`, l'invariant coïncide (les témoins eux-mêmes sont invariants sous
équivalence logique — c'est attendu). Mais dès `k = 1`, l'invariant diverge
d'un **facteur 3** (92 vs 29) ; à `k = 2`, d'un facteur **4** (125 vs 29).
Pour deux CNF qui calculent **exactement la même fonction booléenne**.

L'invariant `Σ β_i(L_k)` du Proposeur n'est donc **pas** une fonction de la
fonction booléenne calculée — c'est une fonction de la présentation
syntaxique du CSP. Conséquence directe : un algorithme polynomial pour SAT
prend en entrée une CNF arbitraire ; il peut **préprocesser** cette CNF en
une forme canonique (déduplication des clauses, propagation unitaire, ordre
lexicographique des littéraux, etc.) en temps polynomial avant de décider.
Toute borne inférieure du type « tout algo P sur input `φ` doit prendre temps
`≥ Σ β_i(L_k(φ))` » s'évanouit : l'algorithme exhibe `φ_canon` équivalente
avec un invariant arbitrairement plus petit, et décide en temps borné par
`Σ β_i(L_k(φ_canon))`. Aucune borne inférieure uniforme sur le temps de
décision de la **fonction booléenne** ne peut donc se déduire de cet invariant.

Or `P` et `NP` sont des classes de **langages / fonctions**. Un séparateur de
ces classes doit produire une borne inférieure qui ne s'effondre pas sous
préprocessing polynomial. Le `Σ β_i(L_k)` ne satisfait pas cette condition →
il ne peut pas séparer `P` de `NP`.

> **Aside** : ce n'est pas la barrière des preuves naturelles (RR) — c'est
> plus grave. RR dit qu'une propriété naturelle ne peut pas distinguer
> fonctions faciles et difficiles ; ici, l'invariant ne distingue même pas
> fonctions **équivalentes entre elles**.

#### (b) **Le Lemme 3 est faux : les sauts polynomiaux effondrent la topologie** *(faille calculée)*

Forman 1998 (Morse discrète) s'applique à des champs de vecteurs
combinatoires sur le 1-squelette du cube — c'est-à-dire des arêtes de
longueur Hamming 1. Le Proposeur conjecture que la théorie « survit aux
sauts bornés ». **Faux.**

Une machine de Turing en temps `n^c` peut modifier jusqu'à `n^c` bits avant
de répondre. Le « champ de vecteurs » associé est donc défini sur le graphe
`G_{n^c}` = cube avec arêtes pour toute paire à distance Hamming ≤ `n^c`.
Et la topologie du complexe simplicial sur ce graphe s'effondre rapidement
en fonction du rayon.

**Vérification empirique (partie B) :** CSP `φ` à 6 variables avec contraintes
`x_i = x_{i+3}` pour `i = 0, 1, 2`. Témoins = diagonale `{(a,b,c,a,b,c)}`,
soit 8 témoins, distances Hamming mutuelles ∈ {2, 4, 6}.

| Rayon de saut `r` | `β_0` (composantes connexes des témoins) |
|---:|---:|
| 1 | **8** (toutes isolées — Forman strict) |
| 2 | **1** (effondrement immédiat) |
| 3 | 1 |
| ≥ 4 | 1 (graphe complet) |

Dès `r = 2`, `β_0` chute de 8 à 1. La conclusion s'étend à tous les Betti
supérieurs (le graphe devient un cube complet sur les patterns `(a,b,c)`,
qui est contractile). Pour `r = n^c`, le graphe est *complet*, tous les
Betti supérieurs sont nuls.

Le « champ de vecteurs à sauts bornés » du Lemme 3 n'a aucune obstruction
topologique à offrir : c'est précisément la liberté de saut qui rend
l'obstruction vide.

#### (c) **Bonus structurel : Aveu 1 défait la construction**

Le Proposeur reconnaît qu'une MT doit être modélisée sur un espace étendu
`{0,1}^m × États`. Soit. Mais alors les sous-niveaux `L_k` ne vivent plus
dans le cube booléen pur ; ils vivent dans un produit dont la topologie est
trivialement contrôlée par celle du facteur « États » (typiquement
contractile : c'est un graphe de calcul). La topologie du facteur Hamming
disparaît dans le produit. Le Lemme 1 (Betti exponentiels) ne porte que
sur le facteur Hamming et n'a aucune raison de remonter au produit.

### 3. Test des barrières

**Relativisation.** L'argument du Proposeur (« l'oracle n'a pas de Hamming »)
est techniquement correct mais sans force : on peut imaginer un oracle qui
fournit `E(w)` directement, et la « blackboxité » disparaît. Plus profondément,
l'argument relativise dès qu'on remplace le CSP par sa fonction caractéristique
oracularisée : le Lemme 4 s'applique alors à toute famille `O` avec sous-niveaux
topologiquement riches — y compris des oracles `O` pour lesquels `P^O = NP^O`.
Donc l'argument relativise par contre-exemple (BGS-style).

**Algébrisation.** L'argument du Proposeur (« Õ détruit Hamming ») est, comme
au Tour 2, une *définition personnelle* de l'oracle algébrique, pas le cadre
d'Aaronson-Wigderson. AW autorise toute extension polynomiale de bas degré,
y compris des extensions qui préservent ou simulent la structure
combinatoire discrète. Le simple fait que la topologie change quand on
plonge dans `F_q` ne suffit pas — il faudrait exhiber un oracle algébrique
`Õ` témoignant `P^O ≠ NP^O` que l'argument prouve, ce que le Proposeur ne
fait pas.

En outre, étant donné l'effondrement (b), l'argument ne prouve même pas
`P ≠ NP` dans le monde de base — la question d'algébrisation est secondaire.

**Preuves naturelles.** L'évacuation du Proposeur (« propriété de la
présentation, pas de la fonction ») est précisément (a) ci-dessus, mais
retournée : il croit échapper à RR ; il se condamne plus radicalement, en
sortant carrément du cadre P vs NP.

### 4. Verdict : ❌ FAILLE FATALE

Deux failles fatales **indépendantes** :

1. **Niveau d'objet** : l'invariant porte sur la présentation, pas sur la
   fonction. *(calculé : ψ ≡ ψ' avec topologies différentes)*. Conséquence :
   ne peut pas séparer P de NP en tant que classes de fonctions.
2. **Niveau de mécanisme** : le Lemme 3 (MT → champ à sauts bornés) est faux,
   les sauts polynomiaux trivialisent la topologie. *(calculé : β_0 = 8 → 1
   pour r = 2)*. Conséquence : il n'y a pas d'obstruction topologique au
   temps polynomial.

Sans Lemme 3, le Lemme 4 ne se prouve pas. Et même si le Lemme 3 se prouvait
par miracle, la faille (a) le rendrait inutile. Aucune lacune réparable :
il faudrait à la fois (i) redéfinir P et NP comme classes de présentations
(ce qui n'est pas P vs NP), et (ii) inventer une notion de Morse discrète
qui survive aux sauts polynomiaux (problème ouvert, et empiriquement faux
sur petits cas).

---

## Nuance honnête

Le **clustering topologique des CSP** en phase RSB est un sujet réel et actif
(physique statistique des verres de spins, Mézard-Parisi-Zecchina, Achlioptas
et al.). La connexion avec la dureté algorithmique fait l'objet d'analyses
sérieuses pour les algorithmes **locaux** (Glauber, simulated annealing,
survey propagation), qui *sont* effectivement contraints par la géométrie du
paysage d'énergie. Mais :

- Cette littérature ne sépare **pas** P de NP — elle sépare seulement « algos
  locaux » de « algos quelconques », ce qui n'est pas la même question.
- Les bornes obtenues sont **conditionnelles** à l'hypothèse RSB, qui est
  elle-même conjecturale même pour k-SAT aléatoire.
- Aucun de ces résultats ne franchit la barrière algébrisation, parce qu'ils
  ne franchissent **pas** la barrière relativisation : ils sont des bornes
  inférieures pour des classes d'algorithmes restreintes (locales), pas pour
  P entier.

Confondre « bornes pour algos locaux » et « bornes pour P » est précisément
l'erreur centrale du Proposeur.

## Conséquences pour la suite

- Piste 3 classée **❌ Réfutée** dans le cahier de bord.
- Question ouverte ajoutée : tout invariant proposé doit être **explicitement
  invariant sous équivalence logique** des présentations du problème. C'est
  un test de bon sens préalable à toute analyse plus fine.
- Question ouverte ajoutée : tout argument du type « tout algorithme P est
  contraint par X » doit montrer que `X` survit aux sauts polynomiaux —
  c'est-à-dire, sur l'extension du graphe Hamming à `G_{n^c}`.
- Sous-but Tour 4 : viser un **modèle algébrique** (permanent vs déterminant
  via GCT, ou un cadre proche du Williams 2011) où la classe restreinte est
  manifestement invariante sous présentation, et où le franchissement de
  l'algébrisation est démontré par un exemple concret (oracle algébrique).

## Script de vérification

[`checks/tour_03_topologie_morse.py`](../checks/tour_03_topologie_morse.py) —
calcul direct par énumération + BFS de :
- (A) `|L_k(ψ)| ≠ |L_k(ψ')|` pour deux CNF équivalentes, `k ∈ {1, 2}` ;
- (B) `β_0(témoins)` en fonction du rayon de saut, montrant l'effondrement
  immédiat dès `r = 2`.

Exécution : `python checks/tour_03_topologie_morse.py`.
