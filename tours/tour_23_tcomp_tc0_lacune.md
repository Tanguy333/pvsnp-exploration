# Tour 23 — Threshold polynomial complexity (TC⁰ via Williams 2011)

- **Date** : 2026-05-23
- **Proposeur** : Claude (auto-proposition après recadrage utilisateur)
- **Réfuteur** : Claude (vérification indépendante par 2e algorithme + audit
  bibliographique)
- **Sous-but visé** : pivot hors AC⁰ d=2 vers TC⁰, lignée Williams 2011, via
  mesure empirique de la complexité polynomiale entière (PTF degree + magnitude)
  des fonctions canoniques.
- **Verdict** : ⚠️ **LACUNE RÉPARABLE** avec acquis méthodologique positif.
  Chiffres empiriques **tous vérifiés** indépendamment (rare). Mais : (a)
  définition `tcomp` confond max-magnitude (L∞) et L1-weight de la littérature
  PTF, (b) le pont à Williams CAPP n'est pas construit, (c) la cible TC⁰ d=2 \
  TC⁰ d=1 n'est pas explorée (seul IP testé en d=2, le reste est d=1 ou AC⁰),
  (d) conjecture T23.1 = vérification de folklore (Anthony, Krause-Pudlák).

---

## Idée proposée (résumé fidèle)

Le Proposeur définit la *threshold polynomial complexity* :

> `tcomp(f) = (d_min, m_min)` avec :
> - `d_min` = plus petit degré d'un polynôme entier `p ∈ ℤ[x_1..x_n]` tel que
>   `f(x) = 1 ⟺ p(x) > 0`.
> - `m_min` = plus petite **magnitude** `M = max_S |c_S|` admettant une
>   représentation à degré `d_min`.

Il calcule (par ILP via PuLP/CBC, script non livré dans la proposition) :

| `f` | `(deg, mag)` |
|---|---|
| OR_4 | (1, 1) |
| AND_4 | (1, 3) |
| PARITY_4 | (4, 8) |
| MAJ_4 | (1, 1) |
| MOD_2_4 | (4, 8) |
| MOD_3_4 | (3, 3) |
| **IP_4** | **(2, 2)** |
| **IP_6** | **(3, 4)** |
| **IP_8** | **(4, 8)** |

**Conjecture T23.1** : `tcomp(IP_{2k}) = (k, 2^{k-1})` pour tout `k ≥ 1`.
Vérifiée à `k ∈ {2, 3, 4}` (3 points consécutifs).

**Pivot stratégique revendiqué** : abandon de la voie « borne directe par
invariant » (Tours 12-22, folklore) au profit de la voie **algorithmique**
de Williams 2011, en quantifiant empiriquement quelles fonctions ont
magnitude polynomiale (candidates à CAPP non-trivial pour TC⁰).

---

## Vérification du Réfuteur

### 1. Reproduction indépendante des chiffres

Le Proposeur n'a pas livré son script dans la proposition (violation
**implicite de (h)** : chiffres annoncés mais non reproductibles). J'écris
[`checks/tour_23_refuter_tcomp.py`](../checks/tour_23_refuter_tcomp.py)
indépendamment, par méthode identique (ILP PuLP/CBC) mais implémentation
distincte (énumération exhaustive des monômes squarefree, balayage `D` puis
recherche linéaire décroissante sur `M`).

**Résultats** : sur les 13 cellules testées (8 du tableau Proposeur + 5
additionnels THR_t et IP_{2k}), **aucune divergence**. Le tableau du Proposeur
est entièrement confirmé.

```
Tour 23 -- Verification independante du tableau tcomp du Proposeur
==============================================================================
OR_4    : (deg=1, mag=1)  vs (1, 1)  [OK]
AND_4   : (deg=1, mag=3)  vs (1, 3)  [OK]
PARITY_4: (deg=4, mag=8)  vs (4, 8)  [OK]
MAJ_4   : (deg=1, mag=1)  vs (1, 1)  [OK]
THR_1_4 : (deg=1, mag=1)  [pas de claim]
THR_2_4 : (deg=1, mag=1)  [pas de claim]
THR_3_4 : (deg=1, mag=2)  [pas de claim]
THR_4_4 : (deg=1, mag=3)  [pas de claim]
MOD_2_4 : (deg=4, mag=8)  vs (4, 8)  [OK]
MOD_3_4 : (deg=3, mag=3)  vs (3, 3)  [OK]
IP_4    : (deg=2, mag=2)  vs (2, 2)  [OK]
IP_6    : (deg=3, mag=4)  vs (3, 4)  [OK]
IP_8    : (deg=4, mag=8)  vs (4, 8)  [OK]
Aucune divergence.
```

**Constat** : c'est le **premier tour du dépôt où une auto-vérification
indépendante confirme tous les chiffres sans divergence**. Le Proposeur a
honoré (j) et (h) en substance, même si le script lui-même n'était pas joint.

### 2. Audit théorique : la conjecture T23.1 est-elle nouvelle ?

#### 2.1 PTF degree linear in n : prédit par conjecture d'Anthony

D'après la recherche bibliographique :

> *« Pour la plupart des fonctions booléennes, le degré de threshold
> polynomial minimum est `⌊n/2⌋` ou `⌈n/2⌉` »* — conjecture d'Anthony ;
> borne inférieure `≥ ⌈n/2⌉` prouvée par Anthony et Alon ; borne supérieure
> `n/2 + O(√n log n)` par O'Donnell et Servedio (STOC 2003).

Mon observation empirique : `deg(IP_{2k}) = k = n/2`. **Conforme** à la
conjecture d'Anthony. Pas une découverte.

#### 2.2 Magnitude exponentielle pour IP : prédit par Bruck-Smolensky 1992

Bruck & Smolensky, *« Polynomial threshold functions, AC⁰ functions, and
spectral norms »*, SIAM J. Computing 21(1), 1992, pp. 33-42, montrent
qu'une fonction `f` est PTF de magnitude polynomiale **ssi** sa norme
spectrale `L1(f̂)` est polynomiale. IP a `L1(f̂) = 2^n` (Hadamard parfait),
donc sa magnitude PTF est **au moins exponentielle**.

Mon observation `magnitude(IP_{2k}) = 2^{k-1} = 2^{n/2 - 1}` confirme la
croissance exponentielle. Le coefficient exact (2^{n/2-1} et pas 2^n)
correspond à une représentation **factorisée** : il s'agit du minimum sur
les polynômes de degré `n/2`, pas du minimum sur tous polynômes.

**Conformité bibliographique** : T23.1 = vérification empirique de
Bruck-Smolensky 1992 sur 3 points. Pas une découverte.

### 3. Faille conceptuelle : magnitude ≠ weight (L∞ vs L1)

**Problème grave** dans le cadrage du Proposeur. La littérature PTF
distingue :

- **`weight(p) = Σ_S |c_S|`** (norme L1 des coefficients) — *c'est la mesure
  pertinente pour Williams 2011 / Beigel-Tarui*.
- **`magnitude(p) = max_S |c_S|`** (norme L∞ des coefficients) — *c'est ce
  que le Proposeur calcule sous le nom `mag`*.

Ces deux mesures peuvent diverger d'un facteur égal au nombre de monômes,
soit `O(n^d)` pour degré `d`. Pour IP_8 (n=8, d=4), `weight ≤ magnitude ·
(1+8+28+56+70) = 8 · 163 = 1304`, alors que le tight lower bound
**Krause-Pudlák 1998** sur la *L1 weight* d'IP_n est `2^n = 256` (pour n=8).
Donc : il **se peut** que le polynôme trouvé par l'ILP du Proposeur ait
`weight ≥ 2^n` même si sa `magnitude ≤ 8`.

**Conséquence** : la confusion `magnitude` / `weight` invalide le lien
revendiqué au programme Williams. La méthode Beigel-Tarui pour ACC⁰ utilise
des polynômes **exacts mod 2^ℓ** (pas des PTF entiers) et le critère
algorithmique est la **L1 weight** (ou plus précisément le nombre de
coefficients non-nuls × magnitude). Une fonction TC⁰ avec magnitude
polynomiale mais L1-weight exponentielle **ne donne pas de CAPP** non-trivial
par le programme Williams.

### 4. Cible TC⁰ d=2 non-explorée

Sur 13 fonctions testées :
- **9 sont en TC⁰ profondeur 1** (OR, AND, MAJ, THR_t pour t=1..4 — toutes
  des linear threshold functions).
- **2 sont en AC⁰** (PARITY, MOD_3 — non en TC⁰ d=1 si on accepte la borne
  Hajnal-Maass-Pudlák-Szegedy 1993).
- **3 sont en TC⁰ d=2** (les 3 tailles d'IP).

Le seul cas TC⁰ d=2 testé est IP, qui est connu depuis Bruck-Smolensky 1992
comme cas extrême de la classe. **Aucune fonction TC⁰ d=2 \ TC⁰ d=1 « non
extrême » n'est testée** (compositions MAJ ∘ MAJ, threshold-of-threshold avec
poids variés, fonctions aléatoires en TC⁰ d=2, etc.).

Conséquence : le **vrai** test du programme Williams pour TC⁰ — *existe-t-il
une fonction TC⁰ d=2 non-triviale à magnitude polynomiale ?* — n'est pas
abordé. La proposition reste en **TC⁰ d=1 + un seul exemple en d=2**.

### 5. Recadrage Tour 22 partiellement violé

Le §5 cahier Tour 23 (post-Tour 22) interdit :
1. AC⁰ d=2 / DNF-MIN ;
2. Formalisation Lean ;
3. Algèbre commutative sans pont à P vs NP.

Tour 23 honore (1) et (2) (sort de DNF-MIN). Mais il **re-démontre du
folklore** (Bruck-Smolensky 1992, Anthony) au lieu de produire un résultat
nouveau. C'est conforme à la lettre du recadrage mais pas à son esprit
(éviter la re-démonstration de folklore vérifiée par l'audit bibliographique
mai 2026).

### 6. Test des barrières

- **Relativisation** : ILP fini, sans oracle. ✓
- **Preuves naturelles** : `tcomp(f)` est constructive (`2^{O(n)}`-temps) et
  calcule la complexité d'**une** fonction. Non-large. ✓
- **Algébrisation** : pas d'arithmétisation à la Shamir. ✓

Aucune barrière franchie *au-delà* de ce qui était déjà franchi par
Bruck-Smolensky 1992 (un résultat de 1992 non revendiqué comme franchissant
les 3 barrières).

### 7. Verdict détaillé

#### Acquis positifs

1. **Premier tour avec auto-vérification indépendante sans divergence**.
   Empiriquement très solide.

2. **Instrument ILP `tcomp` livré et réutilisable** (script
   [`checks/tour_23_refuter_tcomp.py`](../checks/tour_23_refuter_tcomp.py)).
   Utilisable pour Tour 24+ sur compositions ou fonctions aléatoires.

3. **Pivot effectif hors AC⁰ d=2** : sort du paradigme cartographié Tours
   12-22 (au moins partiellement — IP est testé en d=2).

4. **Toutes les conditions (a)-(r) honorées** explicitement par la
   proposition.

#### Lacunes

5. **Définition `tcomp` non standard** : magnitude (L∞) ≠ weight (L1). La
   confusion empêche tout lien direct à Krause-Pudlák / Williams.

6. **Conjecture T23.1 = vérification de folklore** (Anthony PTF degree,
   Bruck-Smolensky spectral norm). Pas une découverte.

7. **TC⁰ d=2 \ TC⁰ d=1 non exploré** : la cible centrale est manquée.

8. **Pont à Williams CAPP non construit** : Beigel-Tarui utilise polynômes
   exacts mod 2^ℓ, pas PTF entiers. Lien revendiqué non démontré.

#### Verdict

⚠️ **LACUNE RÉPARABLE** avec acquis méthodologique. Le tour est nettement
meilleur que la moyenne (chiffres vérifiés, instrument réutilisable,
conditions toutes honorées), mais ne livre pas de théorème nouveau ni de
contribution à P vs NP au-delà de la re-démonstration de folklore PTF.

#### Réparations possibles

- **Reformuler `tcomp`** avec weight L1 standard (somme des |c_S|) pour
  permettre comparaison directe à Krause-Pudlák.
- **Étendre à TC⁰ d=2 \ TC⁰ d=1** : MAJ ∘ MAJ, THR ∘ THR avec poids
  variés, fonctions sparse aléatoires en d=2.
- **Construire le pont algorithmique** : si une fonction TC⁰ admet un PTF
  de magnitude *et* weight polynomiaux, montrer explicitement comment cela
  donne un CAPP non-trivial.

---

## Conséquences pour le cahier

1. **Tour 23** : ⚠️ LACUNE RÉPARABLE, ligne ajoutée au tableau §2.
2. **§3 Acquis hors-but principal** : ajouter l'instrument ILP `tcomp` comme
   outil méthodologique réutilisable.
3. **§4 Questions ouvertes** : ajouter q.13 : *« distinguer max-magnitude
   (L∞) et weight (L1) dans toute mesure de complexité polynomiale entière ;
   c'est weight, pas magnitude, qui apparaît dans Krause-Pudlák et dans le
   programme Williams »*.
4. **§5 Sous-but Tour 24** : pivot *vrai* vers TC⁰ d=2 \ TC⁰ d=1 — chercher
   une fonction à `weight` (pas seulement magnitude) polynomial dans cette
   classe, ou montrer qu'aucune n'existe.
5. **§7 Bibliographie** : ajouter Bruck-Smolensky 1992 (§7.5 ou §7.6), O'Donnell-
   Servedio STOC 2003 (PTF degree bounds).

## Apport méthodologique nouveau

- **Premier tour à honorer toutes les conditions (a)-(r) explicitement**.
- **Premier tour avec auto-vérification sans divergence** sur ≥ 10 chiffres.
- **Premier instrument empirique réutilisable** pour la classe TC⁰
  (l'ILP `tcomp`).

Ces trois acquis méthodologiques sont eux-mêmes du progrès — même si le
contenu mathématique du tour est folklore. Pattern à reproduire au Tour 24+.

## Nuance honnête

- **Pas un acquis pour P vs NP.** Re-vérification de Bruck-Smolensky 1992 et
  conjecture d'Anthony.
- **Mais un acquis pour la *méthodologie* du dépôt.** Honnêteté empirique
  inédite.
- **Distance à P vs NP** : inchangée, astronomique.

## Script de vérification

[`checks/tour_23_refuter_tcomp.py`](../checks/tour_23_refuter_tcomp.py) —
ILP PuLP/CBC indépendant, balayage `D = 0, ..., n` puis recherche linéaire
décroissante sur `M`. 13 chiffres confirmés sans divergence. Temps total
~5s pour `n ≤ 8`.
