# Tour 07 — Obstruction homologique duale (résolutions libres minimales + dualité d'Alexander)

- **Date** : 2026-05-23
- **Proposeur** : Qwen Max
- **Réfuteur** : Claude
- **Sous-but visé** : 8 conditions du Tour 7 (incluant (h) : calcul vérificateur effectivement exécuté).
- **Verdict** : ⚠️ **LACUNE RÉPARABLE** — chiffres livrés corrects, mais le Lemme 2 conjectural est réfuté par contre-exemple (OR_n).

---

## Idée proposée (résumé fidèle)

Pivot vers l'**algèbre commutative computationnelle**. Pour `f` monotone,
associer l'idéal monomial des mintermes `I_f = ⟨ ∏_{i ∈ M} x_i : M minterme de f ⟩`.
L'invariant proposé est la **table de Betti graduée** `β_{i,j}(I_f)` de la
résolution libre minimale, avec :
- **L1 (sémantique algébrique)** : `I_f` est un invariant sémantique complet.
- **L2 (obstruction de profondeur)** : `D_m(f) ≥ Ω(pd(I_f))` + défaut de Scarf.
- **L3 (Eagon-Reiner)** : dualité d'Alexander pour relier I_f et son dual.
- **Calcul livré** : Betti(I_{C_4}) = (4, 4, 1, 0) ; Betti(I_{K_4}) = (6, 8, 3, 0).

Aveux : L2 conjectural, sans preuve formelle ; cadre limité aux formules
monotones, pas aux circuits.

---

## Réfutation

### 1. Reformulation

Utiliser la résolution libre minimale d'un idéal monomial squarefree comme
invariant non-relativisant et non-algébrisant, en conjecturant que sa
profondeur projective minore la profondeur de formule monotone.

### 2. Constat préliminaire — un vrai progrès

Le Proposeur a clairement intégré les leçons des Tours 1-6 :
- Pivot correct (Tour 6) de la topologie simpliciale `Δ_f` vers l'**idéal**
  `I_f` — exactement la correction structurelle que j'avais notée.
- Direction techniquement saine (résolutions libres, Hochster, Eagon-Reiner)
  → algèbre commutative bien établie.
- (h) satisfaite : calculs analytiques livrés pour C_4 et K_4.

C'est le tour le plus mathématiquement compétent à ce stade.

### 3. Vérification indépendante des chiffres (Hochster)

J'ai implémenté la **formule de Hochster** :

```
β_{i, σ}(R/I_Δ) = dim_k H̃_{|σ| − i − 1}(Δ|_σ; k)
```

et confronté avec les chiffres du Proposeur sur les deux exemples livrés.
Cf. [`checks/tour_07_resolutions_libres.py`](../checks/tour_07_resolutions_libres.py).

| Idéal | Betti(I) prédit | Betti(I) calculé | pd | reg | Statut |
|---|---|---|---:|---:|---|
| `I(C_4)` | `(4, 4, 1, 0)` | **`[4, 4, 1]`** | 2 | 2 | ✓ correct |
| `I(K_4)` | `(6, 8, 3, 0)` | **`[6, 8, 3]`** | 2 | 2 | ✓ correct |

Les chiffres sont **mathématiquement justes**. Le Proposeur a fait un travail
honnête.

### 4. La faille fatale — **Lemme 2 réfuté par OR_n**

Le Proposeur conjecture (Aveu 1 — sans preuve) : `D_m(f) ≥ Ω(pd(I_f))`.

**Contre-exemple : `f = OR_n = x_1 ∨ x_2 ∨ … ∨ x_n`.**

- `I_{OR_n} = (x_1, …, x_n) = m`, l'idéal maximal.
- Résolution libre minimale = **complexe de Koszul** :
  `0 → R(−n) → R(−n+1)^{C(n,n-1)} → … → R(−1)^n → R → R/m → 0`.
- `pd(R/m) = n` donc **`pd(I_{OR_n}) = n − 1`**.
- `D_m(OR_n) = 1` (un seul gate OR de fan-in n) ou `log_2 n` (binaire).

**Vérification numérique pour n = 3, 4, 5, 6 :**

| n | Betti(I_{OR_n}) | pd(I) | D_m | L2 prédit (c=1) | Violation ? |
|---:|---|---:|---:|---:|---|
| 3 | `[3, 3, 1]` | 2 | 1 | `≥ 2` | ✗ |
| 4 | `[4, 6, 4, 1]` | 3 | 1 | `≥ 3` | ✗ |
| 5 | `[5, 10, 10, 5, 1]` | 4 | 1 | `≥ 4` | ✗ |
| 6 | `[6, 15, 20, 15, 6, 1]` | 5 | 1 | `≥ 5` | ✗ |

(Les Betti coïncident avec `C(n, k)` — confirmation de la résolution Koszul.)

**Aucune constante c > 0 ne peut sauver L2** : `pd(I_{OR_n}) = n − 1` est
linéaire en `n`, tandis que `D_m(OR_n) = 1` ou `log_2 n` est constant ou
sub-linéaire. Le Lemme 2 est **structurellement faux**.

### 5. Second contre-exemple — MAJ_n

Pour confirmation, vérifions `MAJ_n` (mintermes = sous-ensembles de taille
`⌈n/2⌉`). Formule classique : `pd(I_{MAJ_n}) = ⌊n/2⌋ − 1`.

| n | Betti(I_{MAJ_n}) | pd(I) | D_m | Violation ? |
|---:|---|---:|---:|---|
| 3 | `[3, 2]` | 1 | 2 | OK |
| 5 | `[10, 15, 6]` | 2 | 2 | OK trivial |
| 7 | `[35, 84, 70, 20]` | 3 | 2 | ✗ (`L2 ≥ 3` faux) |

À partir de `n = 7`, MAJ_n viole également L2. La même structure
(invariant algébrique qui croît, profondeur de formule qui reste plate)
se reproduit.

### 6. Pourquoi L2 ne peut PAS marcher

C'est plus profond qu'un simple contre-exemple. La raison structurelle :

**Toute fonction monotone sur n variables admet une formule monotone DNF de
profondeur 2** (`OR` des mintermes), sans contrainte de taille. Donc
`D_m(f) ≤ 2` pour TOUTE fonction monotone non-constante.

Pendant ce temps, `pd(I_f)` peut atteindre `n − 1` (cas extrême `OR_n`).

Donc `D_m(f)` est borné par 2 alors que `pd(I_f)` croît avec `n` — toute
inégalité `D_m ≥ f(pd)` avec `f` non-bornée échoue dès que `n` est grand.

La seule façon de sauver L2 serait d'introduire une contrainte de taille
(formules de taille polynomiale). Mais alors :
- `D_m^{poly}(OR_n) = log_2(n)` (formule binaire de taille `n`).
- `D_m^{poly}(MAJ_n) = O(log n)` (Valiant 1984).

Et `pd(I_{OR_n}) = n − 1` reste linéaire. Donc le contre-exemple persiste,
juste avec exposant différent (linéaire vs logarithmique).

### 7. Le « défaut de Scarf » ne rescue pas

Le Proposeur ajoute « défaut de Scarf » au cocktail (différence entre
Taylor et Betti minimaux). Pour `OR_n` : la résolution Koszul **est**
Taylor (parce que tous les `lcm` sont des sous-ensembles distincts).
Donc défaut de Scarf = 0 pour OR_n.

Si on définit `f(pd, scarf)` qui vaut `pd` quand scarf = 0, OR_n viole. Si
on définit `f` qui vaut `scarf`, alors OR_n donne 0, trivialement vrai,
mais C_4 (scarf substantielle, D_m = 2) violerait.

Aucune fonction `f(pd, scarf)` non-triviale ne peut simultanément :
- donner une borne intéressante (`> 2`) sur les fonctions non triviales,
- ET être satisfaite par OR_n (scarf=0, D_m=1).

### 8. Bonus structurel — limitation reconnue par le Proposeur

Aveu 2 du Proposeur : « *L'extension aux circuits (vs formules) :
l'obstruction homologique pourrait s'effondrer, car un circuit peut
"factoriser" les syzygies.* »

Même si L2 était vraie pour les formules monotones, ce ne serait pas
suffisant pour P vs NP, qui concerne les **circuits arbitraires** (ou les
machines de Turing). Les bornes inférieures pour formules monotones (e.g.
Karchmer-Wigderson 1990) sont une sous-spécialité réelle mais éloignée de
P vs NP.

### 9. Test des barrières

**Relativisation.** L'invariant `pd(I_f)` est calculé sur la structure
d'anneau de polynômes, qui n'existe pas pour un oracle BGS arbitraire.
Plausiblement non-relativisant — mais sans L2, la question est sans objet.

**Algébrisation.** L'invariant Betti gradué est un objet de combinatoire
algébrique discrète sur des idéaux monomiaux squarefree, distinct de
l'arithmétisation polynomiale de bas degré d'Aaronson-Wigderson. Crédible
comme non-algébrisant. Mais sans L2, idem.

**Preuves naturelles.** Calculer la résolution libre minimale est
PSPACE-dur (mais possiblement non-constructif au sens RR). Le Proposeur
revendique l'évitement, à juste titre. Mais une fois encore, sans L2,
l'évaluation est académique.

### 10. Verdict : ⚠️ LACUNE RÉPARABLE

**Pourquoi pas FAILLE FATALE :**
- Les chiffres du Proposeur (C_4, K_4) sont mathématiquement corrects.
- La direction (algèbre commutative pour fonctions monotones) est légitime
  et active en recherche (Bayer-Stillman, Eisenbud, Reiner-Welker,
  Engström-Norén sur les complexes simpliciaux et les Betti tables).
- (h) est satisfaite — premier tour à honorer cette condition.

**Pourquoi pas SURVIT :**
- Le Lemme 2 (pont algèbre → complexité) est conjectural ET empiriquement
  faux (OR_n, MAJ_n).
- Sans L2, les Betti tables sont des objets mathématiques intéressants
  mais sans conséquence pour P vs NP.

**La lacune précise à combler.** Pour réparer, il faudrait :
1. Identifier un invariant algébrique fin sur `I_f` (autre que `pd`, `reg`,
   Scarf défaut) qui corresponde réellement à `D_m`.
2. Démontrer cette correspondance pour une sous-classe non-triviale
   (e.g., monotone formulas avec contrainte de taille polynomiale).

Aucun tel invariant n'est connu dans la littérature actuelle. La
correspondance algèbre ↔ complexité existe pour des **classes très
restreintes** (e.g., Karchmer-Wigderson via communication, mais pas via
algèbre commutative). Le Proposeur a identifié le BON CADRE mathématique,
mais n'a pas trouvé (ni proposé concrètement) le PONT manquant — qui est
précisément ce qui rend les bornes inférieures pour formules monotones si
difficiles.

---

## Nuance honnête

C'est le tour le plus solide à ce stade. Le Proposeur :
- a fait un vrai pivot mathématique (Δ_f → I_f) en réponse à ma critique
  du Tour 6 ;
- a livré des calculs corrects, vérifiables, et matériels ;
- a explicitement reconnu les limites de son approche (formules vs
  circuits, L2 conjectural).

Le défaut n'est pas dans la rigueur ou l'honnêteté — il est dans **ce que
L2 prétend prouver**. Le Proposeur pose la bonne question (existe-t-il un
invariant algébrique qui borne D_m ?) mais propose la mauvaise réponse
(`pd(I_f)`).

La direction algèbre commutative / résolutions libres pour fonctions
monotones est un programme actif. Les Betti tables de Stanley-Reisner ont
des liens connus avec la combinatoire (Hochster), avec les graphes
chordaux (Fröberg), avec les "edge cover" (Villarreal), mais aucun lien
établi avec `D_m` au-delà de bornes triviales du type `D_m ≥ log #min-impl`.

## Conséquences pour la suite

- Piste 7 classée **⚠️ LACUNE RÉPARABLE** dans le cahier de bord.
- Question ouverte ajoutée : tout invariant algébrique conjecturé borner
  `D_m(f)` doit d'abord passer le test `OR_n` (où l'invariant explose en
  taille tandis que `D_m` reste petit).
- Question ouverte ajoutée : *existe-t-il un invariant algébrique fin sur
  `I_f` qui distingue `OR_n` (D_m petit) de C_4 / MAJ_n (D_m = 2 mais
  Scarf défaut substantiel) ?* Toute proposition future devrait s'attaquer
  à cette question.
- Sous-but Tour 8 : maintenir les 8 conditions, et viser cette fois un
  **micro-théorème prouvable**, pas une conjecture supplémentaire. Une
  formalisation Lean d'un mini-lemme (e.g. Auslander-Buchsbaum sur n=4) ou
  une vérification exhaustive d'une propriété simple sur les 168 fonctions
  monotones de n=4 — qui produirait *quelque chose* de définitivement
  acquis, même modeste.

## Script de vérification

[`checks/tour_07_resolutions_libres.py`](../checks/tour_07_resolutions_libres.py)
— implémentation Python directe de la formule de Hochster (via énumération
des Δ|_σ et calcul d'homologie réduite par matrices de bord). Vérifie les
chiffres du Proposeur pour C_4 et K_4 ; calcule Betti, pd, reg pour `OR_n`
(n=3..6) et `MAJ_n` (n=3,5,7) ; exhibe la violation de L2 sur ces cas.
