# Tour 25 — CFI-rigidification de 3-SAT (FAILLE FATALE sur L25.1 + L25.2)

- **Date** : 2026-05-23
- **Proposeur** : Claude (auto-proposition)
- **Réfuteur** : Claude
- **Sous-but visé** : pivot direct sur P vs NP via complexité descriptive +
  construction CFI explicite sur 3-SAT ; viser une réduction à la question de
  Gurevich 1988 (logique pour PTIME sur structures non-ordonnées).
- **Verdict** : ❌ **FAILLE FATALE** sur L25.1 + L25.2. La « CFI-rigidification »
  proposée n'a *pas* le groupe d'automorphismes revendiqué : la construction
  est équivalente à introduire `¬x_i` comme nouvelle variable, et le « swap »
  `(x_i^0, x_i^1)` est équivalent à flipper `x_i`, qui ne préserve
  généralement pas SAT. Vérifié à 100% sur 20 formules 3-SAT random à n=3.

- **Note** : Tour 24 (proposition « complexité tropicale » par Qwen Max
  dans une session parallèle) a déjà été archivé en `tour_24_tropical_refutee.md`,
  également ❌ FAILLE FATALE. Le présent Tour 25 est traité en continuité.

---

## Idée proposée (résumé fidèle)

Construction CFI-rigidification `φ → φ̃` revendiquant 3 propriétés :

1. **L25.1 (construction)** : pour chaque variable `x_i` de φ, jumelée
   `(x_i^0, x_i^1)` avec contrainte XOR `x_i^0 ⊕ x_i^1 = 1`. Pour chaque
   clause `C` de φ, clause jumelée `C̃` sur les variables jumelées.
   Revendication : `SAT(φ) ⟺ SAT(φ̃)`.

2. **L25.2 (symétrie)** : `G = (ℤ/2)^n` agit sur φ̃ par swap indépendant
   `(x_i^0, x_i^1)` pour chaque i ; chaque élément de G est un automorphisme
   préservant SAT.

3. **L25.3 (borne inférieure conjecturale)** : tout circuit invariant sous G
   décidant `SAT(φ̃_n)` requiert taille `exp(Ω(n))`.

4. **L25.4 + L25.5** : enchaînement vers la question de Gurevich 1988
   (« symmetric P = P sur structures non-ordonnées »).

---

## Vérification du Réfuteur

### 1. Audit bibliographique préemptif (condition (q))

Le Proposeur invoque CFI 1992 et Anderson-Dawar 2017 mais sans audit complet.
Trois références critiques manquent :

#### 1.1 Atserias-Bulatov-Dawar 2007 : la *vraie* CFI pour CSP

A. Atserias, A. Bulatov, A. Dawar, *« Affine systems of equations and counting
infinitary logic »*, Theoretical Computer Science 410(18), 2009 (ICALP 2007).
[PDF](https://www.cl.cam.ac.uk/~ad260/papers/abd-icalp07.pdf).

Citation directe (Semantic Scholar) :

> *« La construction CFI a été réinterprétée par Atserias, Bulatov et Dawar
> comme un encodage de systèmes spéciaux d'équations linéaires sur Z₂, où
> chaque variable apparaît dans précisément deux équations. »*

**La vraie CFI** repose sur :
- Un graphe de base où chaque arête est un *gadget twist* à 2 états.
- Une *parité globale* (somme XOR des twists) invariante sous l'action de G.
- La séparation entre G_T (parité 0) et G_F (parité 1) qui est *indistinguable*
  par counting logic mais distinguable en temps polynomial.

**La construction du Proposeur ne fait pas cela.** Sa « jumelée »
`(x_i^0, x_i^1)` avec contrainte `x_i^0 ⊕ x_i^1 = 1` est *équivalente* à
introduire `y_i = ¬x_i` comme nouvelle variable et ajouter la contrainte
`x_i ⊕ y_i = 1`. Le « swap » est alors un *flip* de la variable `x_i`.

Il n'y a **aucune parité globale** dans cette construction, donc pas
d'analogue de l'invariant CFI.

#### 1.2 Anderson-Dawar 2017 : symmetric circuits = FPC, pas « symmetric P »

M. Anderson, A. Dawar, *« On symmetric circuits and fixed-point logics »*,
Theory of Computing Systems 60, 2017, pp. 521-551 (STACS 2014).
[arXiv:1401.1125](https://arxiv.org/abs/1401.1125).

Résultat précis : *« Les requêtes définies par des familles uniformes de
circuits booléens symétriques (avec portes majority) sont **exactement**
celles définissables en logique des points fixes avec comptage (FPC). »*

**Implication critique pour L25.5** : Anderson-Dawar caractérise les circuits
symétriques par leur équivalence à FPC, qui est **strictement plus faible que
P** (puisque FPC échoue sur graphes CFI alors que SAT-graphes ∈ P). La
revendication L25.5 « symmetric P = P sur structures non-ordonnées »
**conflate trois objets distincts** :

- **FPC** : capturé par circuits symétriques (Anderson-Dawar 2017). FPC ⊊ P
  *prouvé* via CFI graphs.
- **CPT** (Choiceless Polynomial Time, Blass-Gurevich-Shelah 1999) :
  strictement plus puissant que FPC, mais on ne sait pas si CPT = P.
- **« Symmetric P »** au sens informel : sans définition précise dans la
  proposition, mais probablement = CPT pour rester cohérent.

Le pont L25.4 → L25.5 saute le niveau CPT. Si L25.3 ne donne qu'une borne
sur FPC (par Anderson-Dawar), elle ne sépare pas P, puisque FPC ⊊ P est déjà
connu sans aucune avancée sur P vs NP.

#### 1.3 Blass-Gurevich-Shelah 1999 / 2002 : CPT, la vraie question

A. Blass, Y. Gurevich, S. Shelah, *« Choiceless polynomial time »*, Annals
of Pure and Applied Logic 100(1-3), 1999, pp. 141-187. Et *« On polynomial
time computation over unordered structures »*, J. Symbolic Logic 67(3), 2002,
pp. 1093-1125.
[PDF Shelah 533](https://shelah.logic.at/files/180379/533.pdf).

C'est la *vraie* formulation de la question de Gurevich. Elle reste ouverte
depuis 1988. Aucune proposition Tour 25 / 24 ne peut la résoudre sans
nouvelle technique. Le Proposeur l'admet en §5 aveu 1 : *« Une réduction
entre deux problèmes ouverts équivalents en difficulté n'est pas un
progrès. »*

### 2. Réfutation empirique de L25.1 + L25.2

[`checks/tour_25_refuter_cfi_sat.py`](../checks/tour_25_refuter_cfi_sat.py)
implémente la construction (lecture A avec orientation `x_i^0 = "x_i vrai"`)
et teste si G agit comme groupe d'automorphismes.

#### Test 1 : `φ = x_1` (1 variable, 1 clause, SAT trivial)

```
phi-tilde a 1 solutions : [(1, 0)]
sigma = (1,) : sols apres swap = [(0, 1)] -- *** CASSE ***
```

L'unique solution `(x_1^0=1, x_1^1=0)` est envoyée par σ=(1) sur `(0, 1)`,
qui n'est PAS solution de φ̃ (la clause `x_1^0` exige `x_1^0 = 1`). Donc G
ne préserve pas l'ensemble des solutions.

#### Test 2 : `φ = (x_1 ∨ x_2) ∧ (¬x_1 ∨ x_2)`

```
phi-tilde a 2 solutions : [(0, 1, 1, 0), (1, 0, 1, 0)]
sigma = (0, 1) : *** CASSE ***
sigma = (1, 0) : preserve
sigma = (1, 1) : *** CASSE ***
```

Sur 3 swaps non-triviaux, 2 cassent, 1 préserve (par coïncidence sur cette
formule). L'action de G n'est PAS automorphique.

#### Test 4 : 20 formules 3-SAT random à n=3

```
Sur 20 formules 3-SAT random : 20 ont G action *cassee*.
Soit 100% de contre-exemples a L25.2.
```

**L25.2 est empiriquement réfuté avec 100% de contre-exemples.**

### 3. Pourquoi la construction ne peut pas être réparée naïvement

Deux lectures possibles de « clause jumelée » :

**(A) Avec orientation** (lecture testée) : choisir `x_i^0 = "x_i vrai"`,
traduire chaque littéral en l'index correspondant. *Lecture syntaxiquement
naturelle, mais brise la symétrie* : un swap sur `i` transforme
`(x_i^0)` en `(x_i^1)`, donc la clause traduite change, et la
satisfiabilité aussi.

**(B) Sans orientation** : remplacer chaque littéral `x_i` par une expression
G-invariante, e.g. `(x_i^0 ∨ x_i^1)`. *Sous la contrainte XOR, cette
expression est toujours TRUE*, donc toutes les clauses sont
tautologiques. **SAT(φ̃) = TRUE pour tout φ non-vide**, perdant l'équivalence
`SAT(φ) ⟺ SAT(φ̃)` de L25.1.

**Aucune lecture intermédiaire** ne sauve simultanément L25.1 et L25.2 dans
le cadre proposé. La vraie CFI évite ce dilemme via une *parité globale* sur
des gadgets twist couplés, mais ce mécanisme requiert une structure
combinatoire (graphe avec arêtes ou CSP avec équations sur Z_2) que SAT
n'admet pas naturellement.

### 4. Test des barrières (sans objet)

L'idée étant réfutée à la racine (L25.1 + L25.2 incohérents), tester
relativisation / RR / algébrisation est sans objet. La construction ne
définit pas un objet mathématique cohérent dont on pourrait évaluer la
relation aux barrières.

### 5. Aveux honnêtes du Proposeur (à valoriser)

Le Proposeur lui-même note plusieurs limitations dans §5 :

- **Aveu 1** : *« réduction entre deux problèmes ouverts équivalents en
  difficulté n'est pas un progrès — sauf si la nouvelle formulation rend
  l'attaque plus accessible. Je ne sais pas si c'est le cas ici. »*
- **Aveu 3** : *« Audit bibliographique (q) incomplet. La CFI-rigidification
  de 3-SAT a peut-être déjà été étudiée par Atserias-Bulatov-Dawar (2007 et
  suivants) sur Constraint Satisfaction Problems. »*
- **Aveu 4** : *« Risque RR caché [...] À tester empiriquement à n=4. »*
- **Aveu 5** : *« Calcul concret à livrer [...] À n=3 »* mais **non livré
  dans la soumission**.

Ces aveux honorent partiellement la *posture* (cf. §4 q.12 du cahier) mais
ne réparent pas la **faille structurelle** : la construction est incohérente
dès n=1, comme le calcul du Réfuteur le démontre. Le Proposeur aurait dû
livrer ce calcul lui-même avant soumission (violation de (j)).

### 6. Verdict détaillé

**❌ FAILLE FATALE** sur :

- **L25.1 + L25.2** : la construction n'admet pas le groupe G revendiqué.
  Vérifié empiriquement à 100% sur 20 formules 3-SAT random.
- **L25.3 + L25.4 + L25.5** : sans objet, puisque L25.1 + L25.2 ne tiennent
  pas. Mais *même si* la construction était salvée, L25.5 conflate FPC /
  CPT / P et n'établit pas le pont à Gurevich 1988.

**À NE JAMAIS réessayer sous cette forme** : transposer naïvement la
construction CFI (faite pour graphes ou CSP avec parité globale) à SAT
(qui n'a pas d'invariant de parité globale) ne fonctionne pas. La vraie
CFI pour CSP (Atserias-Bulatov-Dawar 2007) opère sur systèmes d'équations
sur Z_2, et la transposition à SAT (qui n'est pas affine sur Z_2)
n'est pas évidente.

#### Conditions (a)-(r) checklist (audit Réfuteur)

| Cond | Honorée ? | Comment |
|---|---|---|
| (a) classe restreinte | ✓ partiel | CFI gadgets explicites |
| (b) non-relativisant | ✓ | combinatoire fini |
| (c) non-algébrisant | ✓ | pas d'arithmétisation |
| (h) chiffres livrés | ✗ | calcul concret promis n=3, non livré |
| (i) lien P vs NP | ✓ direct | mais via réduction à problème ouvert (CPT) |
| (j) calcul avant soumission | ✗ | L25.2 réfutable à n=1 en 30 secondes |
| (l) erreur factuelle | ✗ | confusion FPC / CPT / symmetric P (L25.5) |
| (q) audit biblio | ✗ partiel | Atserias-Bulatov-Dawar 2007 non cités ; Blass-Gurevich-Shelah 1999 (CPT) non cités |
| (r) test au point suivant | n/a | construction déjà cassée à n=1 |

### 7. Pourquoi cette tentative était quand même intéressante

Quelques points positifs malgré la FAILLE FATALE :

1. **Direction correcte vis-à-vis P vs NP** : la complexité descriptive
   (Gurevich, Dawar, Grohe) est l'une des directions autorisées §5 du cahier.
   C'est la première proposition du dépôt à y revenir depuis Tour 5 (réfuté).

2. **Aveux honnêtes** : le Proposeur reconnaît plusieurs lacunes en §5,
   contrairement aux tours précédents où les conjectures étaient affirmées
   sans réserve.

3. **Pattern « réduction à problème ouvert » identifié comme tel** : l'aveu
   1 est techniquement correct (sauf si la nouvelle formulation est plus
   accessible). C'est un pas en avant épistémologique.

4. **Cible spécifique identifiée** : Gurevich 1988 / CPT est une vraie
   question ouverte, pas une fiction. La direction est légitime.

**Mais** ces points positifs ne sauvent pas la construction incohérente.
Le Tour 24 (vrai) reste un échec technique sur les premiers lemmes.

---

## Conséquences pour le cahier

1. **Table §2** : ligne 24 → ❌ **FAILLE FATALE**.
2. **§3 ❌ Réfutés** : nouvelle entrée *Piste 24 — CFI-rigidification de SAT*.
3. **§4 Questions ouvertes** : ajouter q.14 : *« avant d'invoquer CFI ou
   tout autre gadget combinatoire connu pour les graphes / CSP, vérifier
   explicitement que l'invariant central (parité globale, comptage,
   isomorphism) transporte au domaine cible. Pour SAT, qui n'a pas
   d'invariant de parité naturel, les gadgets CFI standards ne s'appliquent
   pas. »*
4. **§5 Sous-but Tour 25** : Tour 24 vrai a violé le sous-but Tour 24
   (TC⁰ d=2 \ d=1 avec L1 weight). Le Tour 25 doit le réessayer, OU
   choisir une autre direction parmi celles autorisées §5.
5. **§7 Bibliographie** : ajouter
   - Atserias-Bulatov-Dawar 2007 (CFI affine pour CSP).
   - Blass-Gurevich-Shelah 1999 (CPT).
   - Anderson-Dawar 2017 (symmetric circuits = FPC), en clarifiant que c'est
     FPC pas P.

## Apport méthodologique

- **2e tour avec auto-vérification rapide** : le Réfuteur a écrit le script
  de vérification en 1 itération et obtenu 100% de contre-exemples à
  L25.2 en quelques secondes. Le Proposeur aurait pu (et dû) faire ce test
  lui-même *avant* soumission — violation de (j).
- **Confusion FPC / CPT identifiée** : pattern d'erreur conceptuelle
  potentiellement reproductible (Tour 5 avait le même genre de confusion
  CPT+C / FO + nombres). À garder en tête pour les futurs tours en
  complexité descriptive.

## Nuance honnête

- **Pas un acquis pour P vs NP**, comme prévu par le Proposeur lui-même.
- **Direction descriptive valide** mais demande une construction
  techniquement correcte.
- **Distance à P vs NP** : inchangée, astronomique. La question de Gurevich
  1988 / CPT reste ouverte.

## Script de vérification

[`checks/tour_25_refuter_cfi_sat.py`](../checks/tour_25_refuter_cfi_sat.py) —
construction CFI-rigidification (lecture A), énumération exhaustive des
2^{2n} affectations, test G-invariance. 100% de contre-exemples à L25.2 sur
20 formules 3-SAT random n=3.
