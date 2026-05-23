# Tour 08 — Atlas de Boij-Söderberg des fonctions monotones (n=4)

- **Date** : 2026-05-23
- **Proposeur** : Qwen Max
- **Réfuteur** : Claude
- **Sous-but visé** : objet certifié (catalogage), abandon de P vs NP au tour.
- **Verdict** : ⚠️ **LACUNE RÉPARABLE** (3e consécutive) — direction et mouvement stratégique excellents, mais le seul résultat « mathématiquement solide » revendiqué (Lemme 4) est faux à grande échelle.

---

## Idée proposée (résumé fidèle)

**Renoncement explicite à P vs NP.** Produire un atlas des 168 fonctions
monotones sur `n = 4` variables : pour chacune, la table de Betti de
l'idéal de Stanley-Reisner `I_f`, sa **décomposition de Boij-Söderberg**, et
des invariants dérivés (richesse spectrale `r`, entropie `H_BS`, étendue
des shifts `Δ`). Comparer ces invariants avec les complexités monotones
classiques `D_m`, `L_m`, `C_m`.

Quatre lemmes :
- **L1** : calcul exhaustif des résolutions minimales.
- **L2** : définition des invariants `r, H_BS, Δ`.
- **L3** : corrélations Spearman conjecturées entre invariants algébriques
  et complexités.
- **L4** : *« OR_n et AND_n sont les seules fonctions monotones dont la
  décomposition de Boij-Söderberg est triviale (r=1). »* Le Proposeur le
  revendique comme **prouvable inconditionnellement** pour tout n —
  unique résultat « mathématiquement solide » de la proposition.

Livrable promis : fichier CSV + script SageMath/Macaulay2 + énoncé formel
du Lemme 4 avec preuve. *Aucun de ces livrables n'est dans la
proposition.*

---

## Réfutation

### 1. Reformulation

Cataloguer les Betti tables des 168 fonctions monotones sur `n = 4` via leurs
décompositions de Boij-Söderberg, et démontrer que seules OR_n et AND_n
échappent à toute richesse spectrale.

### 2. Constat préliminaire — un mouvement stratégique excellent

Le Proposeur a **entendu** la condition (i) du Tour 8. Il :
- abandonne explicitement la prétention à P vs NP (« à des années-lumière
  de la question originelle, et c'est assumé ») ;
- vise un objet de catalogage finiment vérifiable ;
- propose un seul résultat asymptotique (L4) qu'il prétend prouvable.

C'est exactement la posture que le sous-but Tour 8 réclamait : produire un
objet certifié plutôt que reformuler P vs NP. **Bravo pour le mouvement.**

Mais (h) reste non honorée : *« un fichier `betti_atlas_n4.csv`, un script
`betti_boij_soederberg.sage` reproductible »* — au **futur**. Aucun chiffre
livré, aucun atlas livré. Je l'effectue à sa place — c'est devenu la
norme.

### 3. Le Lemme 4 est faux dès n = 3

Le Lemme 4 affirme : `OR_n` et `AND_n` sont les seules fonctions monotones
à résolution pure. **Contre-exemple direct : MAJ_3.**

`MAJ_3 = (x_0 ∧ x_1) ∨ (x_0 ∧ x_2) ∨ (x_1 ∧ x_2)`, dont l'idéal monomial est
`I = (x_0 x_1, x_0 x_2, x_1 x_2) = I(K_3)`. Sa résolution minimale :

```
0 → R(−3)² → R(−2)³ → I → 0
```

Betti(I) : `β_{0, 2} = 3, β_{1, 3} = 2`, tous les autres nuls. **Une seule
entrée non-nulle par index homologique** → résolution pure. r = 1.

`MAJ_3` n'est ni `OR_3` ni `AND_3`. **Le Lemme 4 est faux dès n = 3.**

### 4. Sur n = 4 : 95 fonctions à résolution pure, pas 2

J'ai énuméré les **168 fonctions monotones** sur `n = 4` (nombre de
Dedekind `M(4)`), calculé leur Betti table via Hochster, et identifié
celles à résolution pure (cf. [`checks/tour_08_atlas_boij_soderberg.py`](../checks/tour_08_atlas_boij_soderberg.py)).

**Résultat :**

| Statistique | Valeur |
|---|---|
| Fonctions monotones sur n=4 | 168 |
| Fonctions non-constantes analysées | 167 |
| À résolution pure (r = 1) | **95** |
| À résolution non-pure | 72 |

Le Lemme 4 prédisait **2** (OR_4 + AND_4). Réalité : **95**. Erreur d'un
facteur ~47.

### 5. Sommaire structurel de l'atlas pure

Les 95 fonctions à résolution pure se distribuent comme suit (par taille
maximale d'implicant premier et nombre d'implicants) :

| #impl | max_size | count | Inclut |
|---:|---:|---:|---|
| 1 | 0 | 1 | constante 1 |
| 1 | 1 | 4 | littéraux seuls (x_i) |
| 1 | 2 | 6 | AND de 2 variables |
| 1 | 3 | 4 | AND de 3 variables |
| 1 | 4 | 1 | **THRESHOLD_4 = AND_4** |
| 2 | 1 | 6 | OR de 2 littéraux |
| 2 | 2 | 15 | (incl. paires d'arêtes disjointes, shifts (2,4)) |
| 2 | 3 | 6 | OR de 2 AND_3 |
| 3 | 1 | 4 | OR de 3 littéraux |
| 3 | 2 | 20 | OR de 3 paires |
| 3 | 3 | 4 | OR de 3 AND_3 |
| 4 | 1 | 1 | **THRESHOLD_1 = OR_4** |
| 4 | 2 | 15 | OR de 4 paires |
| 4 | 3 | 1 | **THRESHOLD_3** |
| 5 | 2 | 6 | OR de 5 paires |
| 6 | 2 | 1 | **THRESHOLD_2 (= MAJ_4)** |

Les **4 fonctions threshold** (OR_4, MAJ_4, THRESHOLD_3, AND_4) sont
toutes pures, ce qui était prévisible (idéaux de Veronese squarefree,
résolutions de type Eagon-Northcott). Mais aussi de nombreuses autres
classes : tous les littéraux seuls, tous les AND simples, tous les OR
simples de quelques mintermes de taille fixe, et certaines combinaisons
particulières (les paires d'arêtes disjointes ont shifts non-consécutifs
(2, 4), un cas pédagogiquement intéressant).

### 6. Pourquoi la prétention « prouvable inconditionnellement » est fausse

Le Proposeur écrit : *« Le Lemme 4 est prouvable inconditionnellement pour
tout n, pas seulement n=4. […] conséquence directe de la classification
des idéaux à résolution pure : pour un idéal de Stanley-Reisner, la pureté
équivaut (par un théorème de Herzog-Kühl) à être soit un idéal linéaire
(cas OR_n), soit un idéal principal (cas AND_n), à isomorphisme près. »*

**Confusion mathématique.** Herzog-Kühl 1984 dit autre chose :

> *Une résolution graduée pure donne des contraintes sur les coefficients
> de Betti via la formule Π (d_j − d_i) — elle ne dit pas que les seules
> résolutions pures sont les linéaires + principales.*

En réalité, **toute résolution pure** (au sens de « une seule entrée non
nulle par index homologique ») existe pour de nombreux idéaux qui ne sont
ni linéaires ni principaux. Les idéaux de Veronese squarefree
`m^{(d)}` (pour tout `d`) en sont des exemples (résolutions Eagon-
Northcott pures). Les idéaux d'arêtes de certains graphes aussi (e.g.
graphes chordaux). Etc.

La caractérisation correcte est de la forme : *« I a résolution pure ssi
le quotient R/I appartient à une classe homologiquement régulière (Cohen-
Macaulay avec h-vector spécifique). »* Cette classe est riche, pas binaire.

### 7. Test des barrières

Le Proposeur a raison sur ce point : les trois barrières sont **inapplicables**
au tour 8 puisqu'il s'agit d'un objet fini, non d'une borne asymptotique.

### 8. Verdict : ⚠️ LACUNE RÉPARABLE (3e consécutive)

**Pourquoi pas FAILLE FATALE :**
- Le mouvement stratégique (abandon de P vs NP, focus catalogage) est correct
  et conforme au sous-but Tour 8.
- La direction (Boij-Söderberg pour fonctions monotones) est mathématiquement
  intéressante et faisable.
- L'atlas livré (par moi à sa place) est un objet réel, vrai, utile.

**Pourquoi pas SURVIT :**
- Le Lemme 4 — seul résultat « mathématiquement solide » revendiqué — est
  faux à grande échelle (95/167 fonctions le contredisent sur n=4 ; déjà
  faux sur n=3 avec MAJ_3).
- (h) toujours non honorée par le Proposeur : aucun script livré, aucun
  CSV, aucun calcul effectif.
- La justification mathématique invoquée (Herzog-Kühl) est mal interprétée.

**Le pattern persistant.** Sur 8 tours, le Proposeur :
- a clairement appris (cf. progression Tours 1 → 8) ;
- corrige précisément les défauts identifiés tour précédent ;
- mais introduit à chaque tour un nouveau Lemme conjectural ou un nouveau
  résultat revendiqué qui se révèle faux à l'examen.

C'est le pattern Razborov-Rudich « grand » : à chaque correction, le piège
se déplace mais ne disparaît jamais.

---

## Nuance honnête

Ce tour est **le meilleur stratégiquement** — premier vrai abandon de la
prétention à P vs NP en faveur d'un travail solide. Mais la composante
**technique** régresse : le Proposeur revendique un théorème solide
(Lemme 4) qu'il n'a pas vérifié à petite échelle.

L'atlas que j'ai produit (95 fonctions pures sur n=4) constitue lui un
**vrai livrable** : nouveau objet de classification mathématique, sans
prétention asymptotique, vérifiable et reproductible. Il pourrait servir
de base à une publication courte en algèbre commutative computationnelle
(à condition de vérifier qu'il n'a pas déjà été produit ; sphère Fløystad-
Vatne ou Engström-Norén à consulter).

## Conséquences pour la suite

- Piste 8 classée **⚠️ LACUNE RÉPARABLE** dans le cahier de bord.
- Atlas partiel livré : 95 fonctions monotones n=4 à résolution pure, avec
  leurs mintermes et shift sequences.
- Question ouverte mathématique (intéressante en soi) : *quelle est la
  caractérisation exacte des fonctions monotones à résolution pure ?* Pas
  juste threshold (qui en est une sous-classe), pas juste linéaire +
  principal (idée fausse du Proposeur), mais quelque chose de structurel.
- Sous-but Tour 9 : **si le Proposeur veut continuer**, exiger des
  résultats *prouvés* à petite échelle, pas seulement revendiqués. La
  condition (h) impose le calcul ; à elle s'ajoute **(j) tout théorème
  asymptotique revendiqué doit être vérifié empiriquement à n=4 ou n=5
  *avant* soumission** — sinon le Réfuteur fait le travail pédagogique
  de réfutation à la place.

Alternatives constructives à proposer au Proposeur :
- Caractériser exactement la classe des fonctions monotones à résolution
  pure sur petits n (peut-être une nouvelle conjecture à tester) ;
- Implémenter la décomposition Boij-Söderberg complète pour les 72
  fonctions non-pures n=4 et observer les corrélations effectives ;
- Formaliser en Lean un lemme classique de l'algèbre commutative (e.g.
  Auslander-Buchsbaum) pour produire un objet de référence certifié.

## Script de vérification et livrable

[`checks/tour_08_atlas_boij_soderberg.py`](../checks/tour_08_atlas_boij_soderberg.py)
— énumère les 168 fonctions monotones sur n=4 ; calcule Betti(I_f) via
Hochster (réutilise tour_07) ; identifie celles à résolution pure ; en
liste les 95 avec leurs mintermes et shift sequences ; produit le sommaire
par classe.

**À ce stade, le repository contient pour la première fois un objet
mathématique *positif* (l'atlas), au-delà des réfutations.**

---

## Addendum — Réponse du Proposeur et seconde réfutation

### Réponse du Proposeur (résumée fidèlement)

Le Proposeur accepte la réfutation, retire le Lemme 4, et propose une
**version corrigée** présentée comme « classique et bien plus belle » :

> *« Mini-théorème (correct, classique). Pour une fonction monotone f sur
> n variables, l'idéal de Stanley-Reisner I_f admet une résolution libre
> pure (donc r(f) = 1, H_BS(f) = 0) si et seulement si le complexe Δ_f
> est le squelette k-dimensionnel du simplexe Δ^{n-1} pour un certain k —
> c'est-à-dire si et seulement si f est une fonction threshold TH_t(x) =
> [|x| ≥ t], à permutation des variables près. »*

avec une « preuve esquisse » basée sur Herzog-Kühl 1986 et le théorème
d'Eagon-Northcott pour les idéaux de Veronese squarefree.

Conséquence revendiquée : OR_n, MAJ_n, AND_n, et toutes les TH_t partagent
r=1 et H_BS=0 — donc l'invariant ne distingue pas ces fonctions.

### Seconde réfutation

**Le mini-théorème révisé est encore faux**, et le contre-exemple est
*déjà* dans l'atlas que je viens de produire. Le Proposeur n'a pas
appliqué le constat élémentaire du calcul empirique avant de soumettre.

Sur n=4, les fonctions threshold sont exactement 4 : TH_1 (=OR_4),
TH_2 (=MAJ_4), TH_3, TH_4 (=AND_4). Le nouveau mini-théorème prédit donc
**4 fonctions pures**. L'énumération exhaustive en a trouvé **95**. Le
facteur d'erreur passe de 47 (Lemme 4 original) à 24 — réduction, certes,
mais le théorème reste massivement faux.

**Quatre contre-exemples concrets**, extraits directement du tableau ci-
dessus, qui sont à résolution pure mais pas threshold :

| # atlas | Mintermes | Expression | Pourquoi non-threshold |
|---:|---|---|---|
| #2 | `{0}` | `f = x_0` | 1 minterme de taille 1, mais TH_1 (OR_4) en a 4 |
| #6 | `{0}, {1}` | `f = x_0 ∨ x_1` | 2 mintermes de taille 1, mais TH_1 en a 4 |
| #23 | `{0,1}, {0,2}` | `f = (x_0∧x_1) ∨ (x_0∧x_2)` | 2 mintermes de taille 2, mais TH_2 en a 6 |
| #84 | `{0,1,2}, {0,1,3}` | `f = (x_0∧x_1∧x_2) ∨ (x_0∧x_1∧x_3)` | 2 mintermes de taille 3, mais TH_3 en a 4 |

Plus généralement, les **95 fonctions** identifiées comme pures incluent :
- toutes les sous-fonctions « dépendant de < n variables » (e.g. `f = x_0` ou `f = x_0 ∧ x_1` sur n=4) ;
- les paires d'arêtes disjointes (#30, #31, #35, shifts non-consécutifs (2, 4)) ;
- de nombreuses autres combinaisons.

Aucune de ces fonctions n'est une threshold sur 4 variables.

### Diagnostic — violation immédiate de la condition (j)

J'ai ajouté la condition (j) au sous-but Tour 9 dans le commit précédent :
*« Tout théorème asymptotique revendiqué doit être vérifié empiriquement à
n=4 ou n=5 par le Proposeur avant soumission. »*

Le Proposeur **n'a pas appliqué (j)** à son propre théorème révisé. Le
mini-théorème corrigé tient en **deux secondes** d'énumération sur l'atlas
n=4 que je venais de fournir, et il aurait été immédiatement écarté.

C'est précisément le pattern que (j) cherchait à briser : revendiquer un
résultat sans le vérifier sur les petits cas. Le Proposeur a réécrit son
erreur (passé de 2 à 4 prédictions) sans remarquer qu'il avait déjà 95
contre-exemples sous les yeux.

### Sur la « preuve esquisse » de Herzog-Kühl

Le Proposeur écrit : *« un idéal SR pur dont les générateurs ont tous même
degré t est, par rigidité combinatoire, soit un tel idéal de squelette,
soit (dans des cas dégénérés) un idéal linéaire ou principal, qui se
ramène à OR_n ou AND_n. »*

Cette affirmation a deux problèmes :

1. **Beaucoup d'idéaux SR purs ont des générateurs de degrés *différents*.**
   Exemple #30 dans l'atlas : `I = (x_0 x_3, x_1 x_2)`, générateurs tous de
   degré 2, mais les *shifts* sont (2, 4) — résolution `0 → R(-4) → R(-2)^2 → I`.
   C'est pure (un seul shift par index homologique) mais **pas Eagon-
   Northcott** : les deux générateurs ont supports disjoints, donc l'idéal
   est un produit `(x_0 x_3) · (x_1 x_2)` à un anti-isomorphisme près.

2. **Le "cas dégénéré"** (idéal linéaire) inclut toutes les sous-fonctions
   `f = x_{i_1} ∨ … ∨ x_{i_k}` pour k arbitraire, pas seulement k = n. Sur
   n=4, cela donne 14 classes pures (sous-OR), pas une seule. Le Proposeur
   les compte comme "dégénérescences de OR_n", mais elles ne sont pas TH_t
   pour aucun t.

Donc l'invocation de Herzog-Kühl pour conclure « pur ssi threshold » est
**incorrecte**. HK donne des contraintes (les coefficients de Betti
satisfont la formule de Herzog-Kühl), pas une classification binaire.

### Verdict pour cette révision : ⚠️ LACUNE RÉPARABLE (encore)

**Bon :**
- Admission immédiate de l'erreur du Lemme 4.
- Posture intellectuelle saine (humilité, transparence).
- Reconnaissance honnête de la distance à P vs NP (« années-lumière »).
- Cadre stratégique correct (renoncement, focus catalogage).

**Mauvais :**
- Le mini-théorème révisé est faux pour la même raison que L4 (manque de
  vérification empirique) — pattern non brisé.
- Violation immédiate de (j) qui venait juste d'être ajoutée.
- La « preuve esquisse » via Herzog-Kühl conflate des concepts distincts
  (résolution pure, résolution linéaire, idéal de Veronese squarefree).

### Direction effective pour le Tour 9

La caractérisation correcte des fonctions monotones à résolution pure est
un **vrai problème ouvert** intéressant (mathématique pure, indépendant
de P vs NP). Mon atlas (95 / 167 sur n=4) est une donnée empirique pour
l'attaquer. Le Proposeur pourrait :

1. **Renoncer à conjecturer une caractérisation** et se limiter au
   livrable atlas effectif (l'objet déjà acquis).
2. **Étudier la structure** des 95 fonctions pures : sous-classes
   évidentes (sous-OR, paires d'arêtes disjointes, idéaux Veronese, …),
   et formuler une **conjecture testable** sur n=5 (7581 fonctions —
   calcul faisable).
3. **Formaliser en Lean** un mini-théorème acquis (e.g., la résolution
   Koszul de l'idéal maximal `m`, ou Auslander-Buchsbaum sur n=3).

Aucune de ces directions ne s'approche de P vs NP. Toutes peuvent
produire un objet mathématique certifié, ce qui correspond au sous-but
Tour 9.

### Synthèse

Le Proposeur a fait le bon mouvement (renoncement, atlas), mais reproduit
au sein de ce mouvement *le même type d'erreur* (théorème non vérifié à
n=4). C'est la **9ème conjecture** introduite sur 8 tours, dont la 8ème
réfutée par calcul direct. Le pattern est désormais clair :

> Le Proposeur (un LLM) peut être pédagogiquement utile pour explorer des
> directions, mais il ne peut pas garantir la véracité de ses énoncés
> asymptotiques sans qu'un vérificateur exécutable les confronte.

C'est précisément le rôle que la boucle adverse a établi.
