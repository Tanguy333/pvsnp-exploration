# Tour 06 — Gap homologique sémantique pour circuits monotones Σ Π fan-in borné (Stanley-Reisner)

- **Date** : 2026-05-23
- **Proposeur** : Qwen Max
- **Réfuteur** : Claude
- **Sous-but visé** : micro-progrès vérifiable sur classe ultra-restreinte, conditions (a)-(g).
- **Verdict** : ⚠️ **LACUNE RÉPARABLE** — direction légitime, mais les Lemmes 1 et 2 spécifiques sont faux (réfutés empiriquement) ; la réparation correcte sort du cadre « calcul à n=5 ».

---

## Idée proposée (résumé fidèle)

Pour `f : {0,1}^n → {0,1}` monotone, définir le **complexe de Stanley-Reisner**
`Δ_f = {S ⊆ [n] : f(χ_S) = 0}`. Affirmer :

- **L1** : la taille minimale d'un circuit Σ Π monotone fan-in `k` calculant
  `f` = taille minimale d'un *recouvrement* de `Δ_f` par simplexes de
  dimension ≤ `k − 1`.
- **L2** : si `β_i(Δ_f) > 0`, tout recouvrement par simplexes de dimension
  `< i` exige une *redondance*, i.e. nombre de simplexes >
  #faces maximales de `Δ_f`.

**Engagement de calcul** (Lemme 3) : *« je m'engage à concevoir un script
SageMath »* qui identifie une `f*` sur `n = 5` avec `β_1 > 0` et un gap entre
taille de circuit et borne triviale.

Aveux du Proposeur : Lemme 3 promis sans être livré (*« sans avoir exécuté le
script SageMath à la seconde près, je ne peux pas nommer laquelle »*).

---

## Réfutation

### 1. Reformulation

Utiliser la topologie du complexe de Stanley-Reisner pour borner la taille
des circuits monotones de profondeur 2 à fan-in borné.

### 2. Constat préliminaire — première vraie tentative de (f), mais incomplète

Le Proposeur a entendu le feedback du Tour 5. Il :
- propose une classe ultra-restreinte (✓ a) ;
- argumente non-relativisation / non-algébrisation par la nature combinatoire
  pure (✓ b, c — plausible) ;
- assure l'invariance logique en partant de la fonction (✓ d) ;
- assume une restriction au fan-in borné pour traiter (e) ;
- pose la condition (g) en notant que `β_1` n'est pas FO-trivial (✓ g) ;
- **promet** un calcul vérifiable (tentative de f).

C'est la première piste qui s'engage dans la direction conseillée (micro-
progrès vérifiable). Bonne intuition globale. **Mais le calcul promis n'a
pas été exécuté.** Je l'ai effectué moi-même — et le résultat **réfute** la
conjecture sous-jacente.

### 3. Le calcul que le Proposeur aurait dû faire

Énumération exhaustive des **168 fonctions monotones sur n = 4** (nombre de
Dedekind `M(4) = 168`). Pour chaque `f`, j'ai calculé :
- le complexe `Δ_f` ;
- ses nombres de Betti sur `ℚ` ;
- ses implicants premiers (= générateurs minimaux de l'idéal de Stanley-
  Reisner) ;
- la taille du circuit Σ Π monotone (= nombre d'implicants premiers, par fait
  classique) ;
- le nombre de faces maximales de `Δ_f`.

**Résultats** (cf. [`checks/tour_06_stanley_reisner.py`](../checks/tour_06_stanley_reisner.py)) :

| Statistique | Valeur |
|---|---|
| Fonctions monotones sur `n = 4` | 168 |
| Avec `β_1(Δ_f) > 0` | **52** |
| ...satisfaisant `taille > #faces max` (Lemme 2) | **0** |
| ...violant `taille > #faces max` (= contre-exemples au Lemme 2) | **52 / 52** |

**Aucune fonction sur 168 ne satisfait le Lemme 2 du Proposeur.** Lorsque
`β_1 > 0`, la taille est *systématiquement* `≤` au nombre de faces maximales.

### 4. Le contre-exemple canonique — explicite et simple

Pour bien visualiser l'erreur, voici le contre-exemple le plus naturel
(deviné *a priori* avant le calcul, confirmé empiriquement) :

**Fonction.** `f(x₀, x₁, x₂, x₃) = (x₀ ∧ x₂) ∨ (x₁ ∧ x₃)` — DNF monotone à
2 monômes, fan-in 2.

**Complexe `Δ_f`.** Identifier `S ⊆ {0,1,2,3}` avec un sous-ensemble. `f(χ_S) = 1`
ssi `{0,2} ⊆ S` ou `{1,3} ⊆ S`. Donc `Δ_f = {S : ni {0,2} ⊆ S, ni {1,3} ⊆ S}` :

- ∅ ; {0}, {1}, {2}, {3} ; {0,1}, {0,3}, {1,2}, {2,3}.

C'est exactement le **complexe de drapeau du 4-cycle C₄** (sommets = {0,1,2,3},
arêtes = côtés du carré). C'est un 1-complexe avec `β_0 = 1, β_1 = 1`.

**Faces maximales de `Δ_f`** : les 4 arêtes du carré. *#max = 4.*

**Implicants premiers de `f`** : `{0, 2}` et `{1, 3}` (les diagonales
manquantes — les non-faces minimales de `Δ_f`). *#impl = 2.*

**Confrontation avec le Lemme 2.**
- Lemme 2 prédit : `β_1 > 0 ⟹` taille `>` #faces max `= 4`.
- Réalité : taille `= 2 < 4`.

Le Lemme 2 est **faux** sur ce cas explicite. Et il est faux sur les 52
fonctions n=4 où `β_1 > 0`.

### 5. Pourquoi le Lemme 2 est faux structurellement

Le Proposeur conflate deux objets distincts :

- **Δ_f** : le complexe simplicial sur `[n]`.
- **L'idéal `I_{Δ_f}`** : l'idéal monomial squarefree dans `k[x_1, …, x_n]`
  dont les générateurs minimaux sont les non-faces minimales de `Δ_f`.

Ce sont des objets **duaux** : `Δ_f` = ensemble de faces (downset),
`I_{Δ_f}` = idéal engendré par les monômes des non-faces (upset). La taille
du circuit Σ Π monotone = nombre de générateurs minimaux de `I_{Δ_f}` —
**pas** un "recouvrement par simplexes de `Δ_f`".

Or `β_i(Δ_f)` mesure les "trous" du complexe, qui peuvent exister sans
augmenter le nombre de générateurs de l'idéal. C_4 en est l'exemple
canonique : un trou (β_1 = 1) avec seulement 2 générateurs d'idéal.

Plus formellement : pour un complexe simplicial `Δ`, le nombre de
générateurs minimaux de `I_Δ` (`= μ(I_Δ)`) et les nombres de Betti
`β_i(Δ)` sont liés par la **résolution libre minimale** de l'idéal de
Stanley-Reisner (Hochster's formula). Mais cette relation **n'est PAS** de
la forme « `β_i > 0 ⟹ μ ≥ #max faces` ». Hochster donne en réalité :

```
β_{i,σ}(I_Δ) = dim_k H̃_{|σ| − i − 2}(Δ|_σ; k)   (formule de Hochster)
```

ce qui exprime les Betti gradués de l'idéal en termes d'homologie réduite
des sous-complexes — relation profonde et intéressante, mais qui ne donne
**pas** la borne naïve revendiquée par le Proposeur.

### 6. Le Lemme 1 est une tautologie déguisée

L'« équivalence sémantique » entre taille de circuit et « recouvrement
simplicial » se réduit, correctement écrite, à :

> *La taille minimale du circuit Σ Π monotone calculant `f` est égale au
> nombre de générateurs minimaux de l'idéal de Stanley-Reisner `I_{Δ_f}`,
> = nombre d'implicants premiers de `f`.*

C'est vrai par définition (canon de représentation des fonctions monotones)
mais ce n'est PAS une nouvelle découverte. Et la formulation du Proposeur
(« recouvrement de `Δ_f` par simplexes de dimension ≤ k − 1 ») est inexacte
au moins linguistiquement : les implicants premiers ne sont pas des faces
de `Δ_f`, ce sont les non-faces minimales (générateurs d'un idéal).

### 7. Test des barrières

**Relativisation.** Plausible que l'invariant `β_i(Δ_f)` ne relativise pas
(structures combinatoires sans analogue oracle). Mais l'invariant ne donne
pas la borne souhaitée, donc la question ne se pose pas en pratique.

**Algébrisation.** Plausible — combinatoire discrète. Idem, sans Lemme 2,
non pertinent.

**Preuves naturelles.** L'invariant `β_i` est calculable en temps polynomial
sur la table de vérité (par les matrices de bord), donc **est** constructif
au sens de RR. La propriété est-elle large ? Sur n=4, 52/168 ≈ 31 % ont
β_1 > 0 — c'est large. Donc l'invariant `β_i > 0`, s'il donnait une vraie
borne, serait une propriété naturelle — et tomberait sous Razborov-Rudich
sous hypothèses cryptographiques. C'est un signe d'alarme supplémentaire :
même si on réparait L2, l'argument naturalisant le condamnerait.

### 8. Verdict : ⚠️ LACUNE RÉPARABLE

**Pourquoi pas FAILLE FATALE :** la direction (topologie sémantique pour
fonctions monotones) est légitime. Le programme existe en littérature :
Razborov 1985 (bornes inférieures monotones pour CLIQUE par méthode
d'approximation, *pas* via Stanley-Reisner directement) ; Knill 1994,
Forman 2000 sur Morse discrète et évasivité ; Björner-Wachs sur poset
topology ; Reiner-Welker sur algèbre commutative et combinatoire. Stanley-
Reisner *est* le bon objet ; l'erreur est dans l'énoncé spécifique.

**Pourquoi pas SURVIT :** les Lemmes 1 et 2 tels qu'écrits sont
empiriquement faux. Le Proposeur n'a pas livré la contribution technique
qu'il revendiquait — il l'a *promise*, et le calcul que j'ai effectué pour
combler la promesse réfute sa conjecture.

**La lacune précise à combler.** Pour faire fonctionner l'idée :

1. **Reformuler L1** en termes d'**idéal** `I_{Δ_f}` (= idéal monomial des
   implicants premiers), pas de `Δ_f` lui-même.
2. **Remplacer L2** par un énoncé topologique correct. Pistes possibles :
   - Borne via la **régularité de Castelnuovo-Mumford** de `I_{Δ_f}`
     (théorème classique en algèbre commutative) ;
   - Borne via la **profondeur projective** (`pd(I_{Δ_f})`) ;
   - Borne via les **Betti gradués** `β_{i,j}(I_{Δ_f})` (formule de Hochster).
   Mais aucune de ces bornes ne se réduit à `β_i(Δ_f) > 0` ; toutes
   demandent des invariants algébriques plus fins.

**Limite structurelle de la réparation.** Une fois reformulé correctement,
le programme entre dans l'algèbre commutative computationnelle (résolutions
libres minimales, syzygies, complexes de Taylor) — domaine actif mais
**fondamentalement plus difficile** que « calcul exhaustif sur n = 5 ».
Pour `n = 5`, calculer `β_{i,j}(I_{Δ_f})` est faisable (logiciels :
Macaulay2, Sage) ; pour `n` grand, la complexité explose. La direction n'est
pas un « micro-progrès vérifiable » au sens où le sous-but du Tour 6
l'entendait.

Donc : **direction légitime, mais l'effort de réparation déplace la piste
hors du cadre micro-progrès vérifiable.** Le Proposeur a fait un pas
correct ; mais il reste à voir si quiconque (Proposeur, Réfuteur, ou
recherche active) peut transformer cette intuition en théorème non-trivial.

---

## Nuance honnête

C'est, **conditionnellement à la définition de « piste »**, le meilleur
Tour à ce stade :
- direction de fond correcte ;
- classe restreinte précise ;
- engagement vers la vérifiabilité (même imparfaitement tenu) ;
- conditions formelles cochées.

L'erreur est dans l'énoncé spécifique des Lemmes 1 et 2 — pas dans la
stratégie globale. C'est un échec **technique** plutôt que **structurel**,
contrairement aux Tours précédents qui échouaient sur des oublis de
barrières ou d'encodage. Le Proposeur progresse.

La direction Stanley-Reisner / Hochster / Castelnuovo-Mumford reste
mathématiquement vivante, et certains résultats partiels existent dans
cette veine. Mais aucun ne donne (à ma connaissance) une borne du type
revendiqué par le Proposeur, et la nature des théorèmes existants suggère
que la borne souhaitée n'est probablement pas vraie en général.

## Conséquences pour la suite

- Piste 6 classée **⚠️ Lacune réparable** dans le cahier de bord. Première
  piste à ne pas être marquée FAILLE FATALE.
- Question ouverte ajoutée : **toute conjecture topologique sur les
  circuits monotones doit être empiriquement testée sur les 168 fonctions
  monotones de n=4 avant publication**, faute de quoi des contre-exemples
  triviaux la réfutent.
- Sous-but Tour 7 : maintenir les 7 conditions, et **exiger en plus que le
  calcul vérificateur soit effectivement exécuté par le Proposeur** avant
  soumission — pas une promesse, un résultat. Sinon je me retrouve à faire
  le travail à sa place et la valeur de la boucle adverse diminue.

## Script de vérification

[`checks/tour_06_stanley_reisner.py`](../checks/tour_06_stanley_reisner.py)
— énumération brute des 168 fonctions monotones sur `n = 4` ; calcul de
`Δ_f`, des Betti via matrices de bord (numpy), des implicants premiers ;
agrégation des cas où `β_1 > 0` et comparaison avec le Lemme 2. Affiche
aussi le contre-exemple C_4 explicite.
