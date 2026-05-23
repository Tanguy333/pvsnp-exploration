# Tour 05 — Obstruction CPT+C sur l'hypercube sémantique (jeux de pavage bijectifs + canonisation de Dawar)

- **Date** : 2026-05-23
- **Proposeur** : Qwen Max
- **Réfuteur** : Claude
- **Sous-but visé** : 5 conditions du Tour 4 + (f) contribution technique concrète.
- **Verdict** : ❌ **FAILLE FATALE** — le Lemme 3 est *trivialement impossible* dans l'encodage choisi, et la condition (f) n'est pas satisfaite.

---

## Idée proposée (résumé fidèle)

Pivot vers la **Complexité Descriptive**. Coder chaque fonction booléenne `f` par
l'hypercube coloré `H_f = ({0,1}^n, ~, f)` (univers = affectations, voisinage = Hamming, prédicat
unaire = `f`). L'invariant proposé est l'**indistinguabilité par CPT+C** (Choiceless
Polynomial Time with Counting), mesurée par les jeux de pavage bijectifs de
Hella.

Squelette :
- **Lemme 1 (Dawar)** : si `P = NP`, alors `GI ∈ P`, ce qui implique « CPT+C
  capture NP sur la classe des hypercubes colorés ».
- **Lemme 2 (CFI sur hypercube)** : il existe une famille `(f_n, g_n)` avec
  `f_n` UNSAT, `g_n` SAT, et `H_{f_n}` ≡ `H_{g_n}` localement.
- **Lemme 3** : le Duplicateur a une stratégie gagnante dans le `k`-jeu de
  pavage bijectif entre `H_{f_n}` et `H_{g_n}`, même sur le graphe étendu
  `~_{n^c}` (sauts polynomiaux). Donc CPT+C ne distingue pas SAT de UNSAT.
- **Lemme 4** : par contraposée du Lemme 1, `P ≠ NP`.

Aveux du Proposeur : Lemme 2 (CFI sur hypercube) est un programme ouvert ;
extension Hamming-`n^c` (Lemme 3) hautement spéculative ; le théorème de
Dawar du Lemme 1 demande vérification technique ; *« pas de preuve
complète »*, *« feuille de route »*.

---

## Réfutation

### 1. Reformulation

Coder SAT comme coloration de l'hypercube et invoquer un théorème de Dawar
(supposé) pour dire que CPT+C devrait capturer NP, puis exhiber (lemme à
inventer) des paires UNSAT/SAT indistinguables par CPT+C, d'où contradiction.

### 2. Constat préliminaire — (f) non satisfaite

Le Proposeur reconnaît explicitement : *« ceci est une feuille de route... le
Lemme 2 reste à inventer »*. La condition (f) (contribution technique
concrète) du sous-but Tour 5 n'est donc PAS cochée. Pour rappel : cette
condition vient précisément du fait que la piste 4 reformulait le programme
Williams sans contribuer ; ici, la piste 5 reformule le programme Dawar-
Grohe-Blass-Gurevich sans contribuer.

Le rejet pour absence de (f) suffirait à clore le tour, mais le contenu
technique présente *en plus* une faille fatale calculable. C'est celle-ci que
je documente, parce qu'elle invalide la stratégie *même si* on inventait le
Lemme 2.

### 3. Faille fatale — **Lemme 3 est trivialement impossible**

Le Proposeur veut deux fonctions `f` (UNSAT) et `g` (SAT) telles que
`H_f ≡_{CPT+C} H_g`. **Impossible** dans l'encodage choisi, parce que la
propriété distinguante est trivialement définissable au PREMIER ORDRE.

Considérons la sentence FO suivante sur la signature `(~, f)` :

```
phi_SAT  :=  ∃ x . f(x) = 1
```

Cette sentence ne contient qu'un quantificateur et un prédicat unaire. Sur
`H_f` (UNSAT) : aucun sommet n'est coloré 1, donc `phi_SAT` est *fausse*. Sur
`H_g` (SAT) : au moins un sommet est coloré 1, donc `phi_SAT` est *vraie*.

Chaîne d'inclusion standard en complexité descriptive :
```
FO  ⊂  FO+C  ⊂  CPT+C
```

Donc `phi_SAT` est CPT+C-définissable. Donc CPT+C distingue immédiatement
`H_f` de `H_g`, **quels que soient `f` et `g`** avec statuts SAT différents.

Le Lemme 3 du Proposeur (existence d'une stratégie du Duplicateur) est
contradictoire avec la simple existence de cette sentence FO : le Spoiler
gagne en **1 tour**. Il marque dans `H_g` un sommet `x*` colorié 1
(possible puisque `g` est SAT) ; le Duplicateur doit choisir une bijection
`H_f → H_g` et un sommet correspondant dans `H_f` ; mais aucun sommet de
`H_f` n'est colorié 1 (puisque `f` est UNSAT), donc *toute* bijection
échoue à préserver la coloration de `x*`. Le Duplicateur perd.

**Vérification empirique (cf. [`checks/tour_05_cpt_jeux_pavage.py`](../checks/tour_05_cpt_jeux_pavage.py)) :**
trois paires (UNSAT, SAT) sur `m = 6` variables. Le multiset des couleurs
`(#col 0, #col 1)` :

| Paire | UNSAT `(#col 0, #col 1)` | SAT `(#col 0, #col 1)` | `∃ x. f(x)` ? |
|---|---|---|---|
| (1) `x_0 ∧ ¬x_0` vs `x_0` | (64, 0) | (32, 32) | False ≠ True |
| (2) `8 clauses` vs `(x∨y∨z)∧(...)` | (64, 0) | (15, 49) | False ≠ True |
| (3) `8 clauses` vs `(x_0∨x_1∨x_2)` | (64, 0) | (8, 56) | False ≠ True |

CPT+C distingue immédiatement les trois paires.

### 4. Faille structurelle — le mauvais encodage

Le problème est plus profond que « cette sentence FO casse l'argument » : il
vient de l'encodage. En posant `H_f = ({0,1}^n, ~, f)`, le Proposeur a
encodé la propriété distinguante (SAT vs UNSAT) directement dans la
coloration — donc dans le langage de premier ordre de la structure. Toute
question définissable à partir des couleurs est trivialement définissable en
FO.

Une vraie construction CFI évite cela en encodant la propriété distinguante
dans la *structure relationnelle* (le graphe, les relations entre sommets),
pas dans une coloration directe. Sur l'hypercube avec coloration explicite,
la marge est nulle.

Pour faire fonctionner l'idée, il faudrait :
- Encoder la formule `φ` comme une structure relationnelle (variables =
  constantes, clauses = relations ternaires sur les littéraux).
- Étudier la classe des structures `S_φ` (pas `H_f`).
- La propriété « `φ` est satisfaisable » n'est alors plus FO-définissable
  trivialement (il faut « savoir » comment évaluer la formule).

Mais cette reformulation correcte conduit *au programme Dawar-Grohe classique*
sur les structures de formules — qui est exactement le programme ouvert que
le Proposeur prétend faire avancer sans le faire avancer.

### 5. Faille au Lemme 1 — le théorème de Dawar invoqué n'existe pas

Le Proposeur écrit : *« si P = NP, alors GI ∈ P. Par le théorème de Dawar
[...] CPT+C capture NP sur la classe des hypercubes colorés »*. Deux
problèmes :

1. **Pas de tel théorème.** Le théorème classique de Dawar (et la conjecture
   Blass-Gurevich) est : « CPT+C capture P sur toutes les structures finies »
   — c'est une **conjecture ouverte**, pas un théorème. Et elle ne mentionne
   pas la canonisation des hypercubes spécifiquement.

2. **Confusion d'implication.** Si `P = NP`, trivialement tout NP est dans P
   donc dans CPT+C *si* CPT+C = P. Mais la conclusion utile irait dans
   l'autre sens : il faudrait prouver inconditionnellement `CPT+C ≠ NP` (en
   exhibant une propriété NP non CPT+C-définissable), ce qui, conditionnel à
   la conjecture Blass-Gurevich (`CPT+C = P`), donnerait `P ≠ NP`. Mais
   alors le résultat est *conditionnel à la conjecture Blass-Gurevich*, pas
   inconditionnel.

Le programme de la complexité descriptive pour P ≠ NP existe ; c'est même un
des plus prometteurs en bornes inférieures structurelles. Mais il est
conditionnel à des conjectures ouvertes, et il n'a pas la forme contradictive
suggérée par le Proposeur.

### 6. Faille au Lemme 3 (variante sauts polynomiaux)

Même si l'encodage était corrigé, l'extension `~_{n^c}` proposée (Lemme 3)
pour « modéliser les sauts polynomiaux » a un effet pervers : dans
l'hypercube de Hamming `{0,1}^n`, le graphe `~_{n^c}` pour `n^c ≥ n` est
*complet*. Sur un graphe complet, deux structures avec coloration sont
CPT+C-équivalentes ssi le multiset des couleurs coïncide. Donc même *si* le
Proposeur réparait l'encodage pour cacher la propriété SAT dans la
structure, l'extension aux sauts polynomiaux la redécouvrirait par
comptage simple.

C'est l'analogue du Tour 3 (effondrement de la topologie sous sauts
polynomiaux) transposé au cadre logique.

### 7. Test des barrières

**Relativisation.** Plausible que CPT+C ne relativise pas — les jeux d'EF
sont structurels. Mais sans Lemme 3 valide, la question ne se pose pas.

**Algébrisation.** Plausible — le cadre est discret. Mais idem, sans Lemme 3.

**Preuves naturelles.** Pas applicable directement (l'argument ne porte pas
sur des tables de vérité). Pas une protection en soi.

### 8. Verdict : ❌ FAILLE FATALE

Triple faille :

1. **Condition (f) non satisfaite** : aveu explicite *« feuille de route »* ;
   pas de contribution technique au-delà de pointer vers un programme connu.
2. **Lemme 3 impossible** : la sentence FO `∃ x. f(x)` distingue toute paire
   SAT/UNSAT, donc le Duplicateur ne peut pas gagner. *(vérifié pour 3 paires)*
3. **Lemme 1 mal formulé** : le « théorème de Dawar » invoqué n'existe pas
   sous cette forme ; la conjecture Blass-Gurevich correcte (`CPT+C = P`)
   rendrait tout résultat *conditionnel*, jamais inconditionnel.

La direction (complexité descriptive) reste légitime pour P vs NP — c'est
même la voie historique d'Immerman, Vardi, Gurevich, Dawar, Grohe. Mais elle
ne peut pas être empruntée par l'encodage trivial de la fonction comme
coloration de l'hypercube. Et l'apport du Proposeur, retiré l'erreur
d'encodage, se réduit à *« explorer la complexité descriptive »* — pas une
piste vérifiable.

---

## Nuance honnête

La complexité descriptive **est** un programme de recherche actif et
prometteur pour P vs NP. Les résultats récents de Grohe sur la
caractérisation logique de P sur graphes structurés (planaires, bornés en
arbre/clique-width) sont des avancées réelles. La conjecture Blass-Gurevich
reste ouverte et active. Mais le Proposeur, comme au Tour 4, *pointe vers*
le programme sans y contribuer — et en plus, son encodage spécifique
(`H_f = hypercube coloré par la fonction`) est trivialement attaquable.

Ce qu'il faudrait pour une vraie piste dans cette direction : prendre une
structure relationnelle non-triviale (formules, graphes contraints,
codes...) et démontrer un sous-résultat positif vérifiable (par exemple,
montrer qu'une famille spécifique de structures a une borne inférieure
CPT+C démontrable, peut-être via un calcul de jeu EF sur petits cas).

## Conséquences pour la suite

- Piste 5 classée **❌ Réfutée** dans le cahier de bord.
- Question ouverte ajoutée : tout argument « encoder un problème NP sous
  forme X et invoquer une obstruction sur X » doit d'abord vérifier que la
  propriété d'intérêt n'est pas trivialement définissable dans le langage
  des outils utilisés. C'est un sanity-check préalable au cadre lui-même.
- Sous-but Tour 6 : les 6 conditions du Tour 5 + une **7ème condition (g)** :
  ne pas encoder la propriété distinguante en surface — vérifier qu'elle est
  effectivement « cachée » dans la structure et non triviale au premier ordre
  (ou son équivalent dans le formalisme choisi).

## Script de vérification

[`checks/tour_05_cpt_jeux_pavage.py`](../checks/tour_05_cpt_jeux_pavage.py)
— pour 3 paires explicites (UNSAT, SAT) sur `m = 6` variables, calcul des
invariants élémentaires (multiset de couleurs, sentence `∃ x. f(x)`),
démontrant la séparation immédiate.
