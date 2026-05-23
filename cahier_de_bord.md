# Cahier de bord — Exploration P vs NP

> Document vivant. À joindre en contexte à **chaque** tour, pour le Proposeur comme pour le Réfuteur.
> Règle d'or : on ne réexplore jamais une impasse déjà documentée. On mesure le progrès par la compréhension accumulée, pas par « a-t-on la preuve ».

> **Recadrage (fin tour 9).** Le but du dépôt est **P vs NP**. Les Tours 8-9 ont
> dérivé vers de l'algèbre commutative pure (catalogage Boij-Söderberg,
> caractérisation des résolutions pures) — objets mathématiquement valables mais
> **sans lien démontré à P vs NP**. Les objets « ✅ Établis » du §3 sont conservés
> pour leur intérêt mathématique propre, mais **ne comptent pas comme progrès
> sur P vs NP**. Toute idée future doit avoir un lien explicite à la question
> originelle — voir conditions (i) corrigée et (k) ajoutée au §5.

---

## 0. Méta

- **Question** : tout problème dont une solution candidate est vérifiable en temps polynomial est-il aussi résoluble en temps polynomial ? (P vs NP)
- **Direction choisie** : séparation **P ≠ NP**, via une classe restreinte à structure algébrique/géométrique ; cadre principal = complexité descriptive, ouverture GCT ; outils encouragés = méta-complexité / Kolmogorov.
- **Démarré le** : 2026-05-23
- **Dernière mise à jour** : 2026-05-23 (fin tour 20 — antipodales établies, 8 objets, paradigme AC⁰ d=2 cartographié bidirectionnellement)
- **Nombre de tours effectués** : 20

---

## 1. Barrières connues (à garder sous les yeux en permanence)

| Barrière | En une ligne | Statut dans notre exploration |
|---|---|---|
| Relativisation (Baker–Gill–Solovay) | Une preuve qui « relativise » ne peut pas trancher P vs NP. | **ACTIVE** — a tué la piste 1. Tout outil relativisant (Kt, auto-réductibilité, recherche↔décision) est suspect. Exiger des techniques non-relativisantes (ex. arithmétisation à la Williams). |
| Preuves naturelles (Razborov–Rudich) | Les bornes inférieures « naturelles » échouent sous hypothèses cryptographiques standard. | Pertinente uniquement pour les arguments de type table de vérité / circuit. Ne s'applique pas aux arguments purement informationnels — donc « l'éviter » ne prouve rien en soi. |
| Algébrisation (Aaronson–Wigderson) | Généralise la relativisation aux techniques algébriques. | **ACTIVE** — a tué la piste 2. Toute technique mobilisant l'arithmétisation doit démontrer son caractère non-algébrisant (exhiber un oracle algébrique relativement auquel l'invariant proposé sépare P de NP). |

> Toute idée nouvelle DOIT dire laquelle de ces barrières elle prétend franchir, et comment. **Et explicitement traiter la relativisation.**

---

## 2. Pistes explorées

| # | Idée (résumé en 1 ligne) | Barrière visée | Verdict du Réfuteur | Statut |
|---|---|---|---|---|
| 1 | Incompressibilité (Kt) des témoins SAT : P comprimerait les témoins, contredisant leur incompressibilité | Preuves naturelles (revendiqué) | Équivoque K(w) vs K(w\|x) ; argument relativisant | ❌ **FAILLE FATALE** |
| 2 | Signature p-adique des témoins (Ax-Katz pour vérificateurs AC⁰) | Relativisation (revendiqué) | Arithmétisation exacte ≠ polylog ; Ax-Katz trivial sous contrainte booléenne ; technique algébrisante | ❌ **FAILLE FATALE** |
| 3 | Obstruction topologique sur paysage d'énergie CSP (Morse discrète + Lusternik-Schnirelmann) | Relativisation + algébrisation (revendiqué) | Invariant non-invariant sous équivalence logique ; sauts polynomiaux effondrent les Betti | ❌ **FAILLE FATALE** |
| 4 | Compilation TC⁰ → tensor network à bond polynomiale + Williams + Hardness Magnification | Les 3 (revendiqué) | Lemme 1 faux : IP_n ∈ TC⁰ a bond dimension exponentielle (rang 2ⁿ−1 sur ℝ) ; parade F₂ détruit l'outillage analytique ; ce qui reste = reformulation du programme Williams ouvert | ❌ **FAILLE FATALE** sur le mécanisme |
| 5 | Indistinguabilité CPT+C des hypercubes colorés `H_f` (jeux de pavage bijectifs + canonisation Dawar) | Les 3 + (d) + (e) (revendiqué) | Lemme 3 trivialement impossible : `∃ x. f(x)` est FO ⊂ CPT+C et distingue toute paire SAT/UNSAT ; Lemme 1 invoque un théorème de Dawar qui n'existe pas sous cette forme ; (f) non satisfaite (feuille de route admise) | ❌ **FAILLE FATALE** |
| 6 | Gap homologique sémantique pour circuits monotones Σ Π fan-in borné (Stanley-Reisner) | Les 7 (revendiqué) | Lemme 2 réfuté empiriquement (52/168 contre-exemples sur n=4) ; Lemme 1 confond complexe et idéal de Stanley-Reisner ; calcul promis non livré | ⚠️ **LACUNE RÉPARABLE** (direction légitime, mais réparation déplace hors cadre) |
| 7 | Obstruction homologique duale (résolutions libres + dualité d'Alexander) pour profondeur de formule monotone | Les 8 (revendiqué) | Chiffres C_4, K_4 corrects ; mais Lemme 2 (D_m ≥ Ω(pd)) réfuté par OR_n : pd(I_{OR_n}) = n−1 alors que D_m = 1 ; cadre limité aux formules (pas circuits) | ⚠️ **LACUNE RÉPARABLE** |
| 8 | Atlas de Boij-Söderberg des fonctions monotones n=4 (renoncement à P vs NP) | Inapplicables (objet fini) | Mouvement stratégique correct ; mais Lemme 4 (OR/AND = seuls à résolution pure) massivement faux (95/167 contre-exemples) ; atlas livré par le Réfuteur | ⚠️ **LACUNE RÉPARABLE** + objet positif livré |
| 8 bis | Révision du Proposeur : « résolution pure ssi threshold » | Inapplicables | Mini-théorème révisé encore faux (4 thresholds prédits sur n=4, mais 95 fonctions pures ; ex : f = x_0 et f = (x_0∧x_1)∨(x_0∧x_2) sont pures et non-threshold) ; **violation immédiate de (j)** que le Réfuteur venait d'ajouter | ⚠️ **LACUNE RÉPARABLE** |
| 9 | Conjecture C9 : pure ⟺ equigenerated (caractérisation des résolutions pures pour fonctions monotones) | Inapplicables | (h) et (j) honorées pour la première fois par le Proposeur. Conjecture vérifiée n=4 (167 fonctions, tableau parfait 95/0/0/72). **Réfutée n=5** : 215 contre-exemples sur 7579. Contre-exemple minimal : `(x₁x₂x₃)∨(x₁x₂x₄)∨(x₀x₃x₄)` (equigenerated, mais Betti(I) a 2 shifts à l'index 1) | ⚠️ **LACUNE RÉPARABLE** (épistémologie correcte) |
| 10 | (a) Conjecture C10 « intersections uniformes » testée préemptivement et **retirée par le Proposeur** (1068 contre-exemples) ; (b) pivot proposé vers formalisation Lean de Koszul de `m_n` | (a) C10 testée mais inapplicable car pas de prétention asymptotique ; (b) Koszul Lean : aucune | Bon réflexe épistémologique (test (j) honoré 2e fois consécutive). Mais pivot Lean cible un théorème **hors-sujet vis-à-vis de P vs NP** (admis par le Proposeur). Direction prescrite Tour 11 : `PARITY ∉ AC⁰ profondeur 2` | ⚠️ **LACUNE RÉPARABLE** + recadrage utilisateur |
| 11 | Borne `D_m(2COL) ≥ Ω(n log n)` via lifting (Raz-McKenzie/GPW) + Karchmer-Wigderson + Tseitin sur expandeurs (Ben-Sasson-Wigderson) | Trois barrières revendiquées (lifting+KW non-relativisant et non-algébrisant ; RR fragile admis) | Direction enfin correcte vis-à-vis P vs NP. Mais : (1) **erreur factuelle** : 2-COLORATION ∈ P, pas NP-complet ; (2) 2COL n'est pas naturellement monotone ; (3) chaîne L10.5 conjecturale (pattern récurrent que le Proposeur reconnaît) ; (4) (j) régressée (test n=4,6,8 promis mais non livré) ; (5) redondance possible avec Garg-Göös-Knop-Watson 2018 non vérifiée | ⚠️ **LACUNE RÉPARABLE — rejet maintenu par utilisateur** |
| 12 | Mini-théorème : `PARITY_n ∉ AC⁰ profondeur 2` de taille `< 2^(n-1)` (= DNF minimal exactement `2^(n-1)` monômes) | Toutes traitées explicitement (relativisation : preuve combinatoire sans oracle ; RR : propriété pas large car ne caractérise que PARITY et ¬PARITY ; algébrisation : pas d'arithmétisation) | Calcul exhaustif n=4 livré AVANT soumission (81 ANDs, 8 implicants, bijection vérifiée). Argument structurel L12.1–L12.4 valable pour tout n, prouvé combinatoirement. Reproduction indépendante par le Réfuteur OK. **Toutes les 12 conditions (a)–(l) honorées pour la première fois.** | ✅ **ÉTABLI POUR P vs NP** |
| 13 | Caractérisation : `DNF_min(f) = |f^{-1}(1)|` ⟺ `f^{-1}(1)` est independent set de `Q_n` ⟺ aucun AND de `< n` littéraux n'est implicant. PARITY est l'élément maximal d'une classe combinatoire de **743 fonctions à n=4**. | Toutes (relativisation combinatoire, RR : caractérise une classe pas une fonction, algébrisation : sans objet) | Calcul exhaustif n=4 livré : 743 fonctions identifiées, équivalence (b)⟺(c) vérifiée sur 200 échantillons sans incohérence, distribution exacte par taille, PARITY+¬PARITY uniquement à |f^{-1}(1)|=8. Preuves L13.1–L13.4 combinatoires audités OK. Erreur référentielle OEIS (A006506 cité à tort, mais 743 est correct par calcul direct) | ✅ **ÉTABLI POUR P vs NP** (2e objet) |
| 14 | Mini-théorème : `DNF_min(MAJ_n) = C(n, ⌈n/2⌉) ~ 2^n/√n`, donc `MAJ_n ∉ AC⁰ d=2 polynomial`. Première apparition de TC⁰ dans le dépôt. | Toutes (relativisation combinatoire ; RR : « f=MAJ_n » caractérise une fonction unique, non-large ; algébrisation : sans objet) | Calcul exhaustif n=4 livré : 81 ANDs, 33 implicants, **6 implicants premiers** (= C(4,2)), tous positifs taille 2, non-redondance vérifiée. L14.1 initial buggé, **bug détecté et corrigé par le Proposeur via (j)** avant soumission. Preuves L14.1–L14.4 auditées correctes. | ✅ **ÉTABLI POUR P vs NP** (3e objet) — avec **correction de formulation** : la séparation est `TC⁰ d=1 ⊄ AC⁰ d=2 poly` (par témoin), pas l'inclusion stricte `AC⁰ d=2 poly ⊊ TC⁰ d=1 poly` revendiquée. Les deux classes sont en fait incomparables (contre-exemple : DISJ_n ∈ AC⁰ d=2 poly \ TC⁰ d=1). |
| 15a | Proposeur P1 : profondeur logique de Bennett pour séparer P de NP par contradiction | Revendiquées non-rel/non-RR/non-alg (mais sans objet, voir Verdict) | **Auto-réfuté par le Proposeur** dans son Lemme 3 (*« l'argument est circulaire »*). Pattern Tour 1 (circularité conditionnel/inconditionnel) avec « Bennett » à la place de « Kt ». Le cahier §3 dit explicitement « à ne jamais réessayer ». (j) et (h) non honorées. Régression méthodologique après 3 ÉTABLIS consécutifs. | ❌ **FAILLE FATALE** — pattern Tour 1 explicitement interdit |
| 15b | Proposeur P2 : `DNF_min(THRESHOLD_{t,n}) = C(n, t)` pour tout `t ∈ [1, n]` + dichotomie polynomial/exponentiel | Toutes (relativisation combinatoire ; RR : famille de `n` fonctions parmi `2^{2^n}`, non-large ; algébrisation : sans objet) | Calcul exhaustif n=4 livré pour `t ∈ {1,2,3,4}` : `C(4, t) = 4, 6, 4, 1` confirmés. Tous implicants premiers positifs, non-redondance vérifiée. Preuves L15.1–L15.4 = généralisation directe de L14.1–L14.4. **Condition (m) honorée explicitement dès la première application** : séparation par témoin (`TC⁰ d=1 ⊄ AC⁰ d=2 poly`), pas inclusion stricte. Nuance technique honnête sur la frontière exacte (`O(log n)` vs `O(log n / log log n)`). | ✅ **ÉTABLI POUR P vs NP** (4e objet) |
| 16 | `DNF_min(MOD_p_n) = Σ_{k ≡ 0 mod p} C(n, k)`, application directe de L13 (Tour 13) à la famille `MOD_p`. Ouverture de la lignée Razborov-Smolensky. | Toutes (relativisation combinatoire ; RR : famille de `n` fonctions parmi `2^{2^n}`, non-large ; algébrisation : sans objet) | Calcul exhaustif n=4 livré pour `p ∈ {2,3,4,5}`. Comptes confirmés : 8, 5, 2, 1. L16.1 (MOD_p^{-1}(1) independent dans Q_n) prouvée combinatoirement : `sum(y) = sum(x) ± 1` à distance Hamming 1, donc `≢ (mod p)` pour `p ≥ 2`. L16.2 par application directe de L13. L16.3 asymptotique par roots of unity filter. Note terminologique mineure : MOD_2 = ¬PARITY (pas PARITY au sens strict), même DNF_min par symétrie de la bipartition. | ✅ **ÉTABLI POUR P vs NP** (5e objet) |
| 17 | Conjecture `DNF_min(IP_{2n}) = (3^n − 1)/2` pour INNER PRODUCT mod 2, **première fonction hors classe L13** (non-monotone, non-symétrique). Méthode ILP set cover (nouvelle pour le dépôt). | Toutes (relativisation combinatoire + ILP exact ; RR : fonction unique parmi 2^{2^{2n}}, non-large ; algébrisation : pas d'arithmétisation) | Vérification empirique à n=1, 2, 3 par le Proposeur (set cover exhaustif) ; **extension à n=4 par le Réfuteur via PuLP/CBC ILP** : 40 = (3^4 − 1)/2 confirmé. 4 points consécutifs sans exception. Observation structurelle : `|implicants premiers| = DNF_min` à chaque n testé. **Tour 18 fournit la preuve structurelle pour tout n** (cf. ci-dessous). | ✅ **ÉTABLI structurellement (via Tour 18)** (6e objet) |
| 18 | Preuve structurelle de L17 pour tout n : classification des implicants premiers en 3 classes (A1, A2a, A2b) selon `(x_n, y_n)`, récurrence `a_{n+1} = 2a_n + b_n`, `b_{n+1} = a_n + 2b_n`, close-form `a_n = (3^n − 1)/2`, non-redondance par construction explicite du témoin. | Toutes (relativisation combinatoire ; RR : fonction unique ; algébrisation : pas d'arithmétisation) | L18.A (classification) preuve par cas exhaustifs auditée OK. L18.B (récurrence + close-form) par induction triviale, auditée OK. L18.C (non-redondance) esquissée par le Proposeur, **détaillée par le Réfuteur** : construction explicite du témoin `(x_0, x_n=0, y_n=1)` pour A2a, etc. Vérification empirique n=1..4 cohérente avec la récurrence (1, 4, 13, 40). Prédiction n=5: 121, n=6: 364 (non-vérifiables par énumération directe). | ✅ **ÉTABLI STRUCTURELLEMENT** — promeut Tour 17 d'empirique à structurel |
| 19 | Théorème de caractérisation L19 : `DNF_min(f) = |primes(f)|` ⟺ chaque implicant premier admet un témoin essentiel. L13 ⊊ (α)/(β) strictement (témoin MAJ_3). | Toutes (relativisation combinatoire ; RR : *signal d'alarme* — propriété constructive et large à n=4 (36%), mais théorème ne dérive pas de borne inférieure générale, donc compatible ; algébrisation : sans objet) | L19.A et L19.B preuves combinatoires auditées (classiques Quine-McCluskey 1952-1956). Vérification empirique : 202/254 (n=3) et 23862/65534 (n=4) fonctions dans la classe. Unifie Tours 12-18 sous une caractérisation unique. Conjecture asymptotique « fraction → 0 » non démontrée (2 points). | ✅ **ÉTABLI** (7e objet) — théorème classique reformulé, unifie le paradigme |
| 20 | Théorème L20 : fonctions antipodales `f_α(x) = 1 ⟺ x ∉ {α, ¬α}` ont `|primes| = n(n−1)`, `DNF_min = n`, défaut maximal `n(n−2)`. **Pôle extrême opposé à L19**. | Toutes (relativisation combinatoire ; RR : famille petite `2^(n-1)`, non-large ; algébrisation : sans objet) | (i)-(iv) prouvées combinatoirement pour tout n ≥ 3 et auditées (audit du Réfuteur : impl. premier ⟺ 1 positif + 1 négatif ; couverture cyclique ; borne par vecteurs unitaires). Vérification empirique exhaustive n=3 (4 antipodales, défaut 3), n=4 (8, défaut 8), n=5 (16, défaut 15). L20.5 (unicité antipodales = seules à défaut max) conjecturée, vérifiée n=3, 4 par énumération exhaustive. **Note importante** : lien P vs NP plus faible que revendiqué — sur les antipodales, DNF-MIN est facile (calculable en O(n)), pas un témoin de Σ₂^P-difficulté. | ✅ **ÉTABLI** (8e objet) sur (i)-(iv) ; L20.5 conjecturée pour n ≥ 5 |
| 21 |  |  |  | *(à venir)* |

---

## 3. Lemmes et résultats

### ✅ Établis pour P vs NP (vérifiés / démontrés rigoureusement)

- **Mini-théorème** (Tour 12) : *`PARITY_n ∉ AC⁰ profondeur 2` de taille `< 2^(n-1)`*. Plus précisément : la taille minimale d'un DNF (OR de ANDs, fan-in arbitraire) calculant `parity_n(x) = x_0 ⊕ … ⊕ x_{n-1}` est **exactement `2^(n-1)`**. Cf. [`tours/tour_12_parity_ac0_etabli.md`](tours/tour_12_parity_ac0_etabli.md) et [`checks/tour_12_parity_ac0.py`](checks/tour_12_parity_ac0.py).

  **Preuve structurelle** (valable tout n, 4 pas combinatoires) :
  1. Tout AND de < n littéraux a une variable libre → admet satisfaisants de parités opposées → non-implicant.
  2. Donc implicants premiers = mintermes complets correspondant aux 2^(n-1) affectations impaires.
  3. Chaque minterm est satisfait par une unique affectation → tous requis dans tout DNF.
  4. Borne inférieure 2^(n-1) atteinte par DNF canonique. ∎

  **Vérification exhaustive n=4** : 81 ANDs énumérés, 8 implicants identifiés, bijection avec les 8 affectations impaires confirmée, DNF canonique de taille 8 calcule `parity_4`.

  **Lien à P vs NP** : `parity_n ∈ P` (calculable en `O(n)`), donc l'impossibilité d'un DNF de taille polynomiale (puisque `2^(n-1)` est exponentiel) montre que **`AC⁰ profondeur 2 ⊊ P`**. Premier maillon de la chaîne FSS 1981 → Håstad 1986 → Razborov-Smolensky 1987 → Williams 2011 (NEXP ⊄ ACC⁰, seul résultat ayant franchi les trois barrières).

  **Barrières** : non-relativisant (preuve combinatoire sans oracle), pas en tension avec RR (propriété trop spécifique pour être large : seules `parity` et `¬parity` la satisfont), non-algébrisant (pas d'arithmétisation).

  **Premier objet positif aligné sur P vs NP du dépôt** après 11 itérations.

- **Théorème de caractérisation** (Tour 13) : *Pour `f : {0,1}^n → {0,1}` non-constante, les trois conditions sont équivalentes :*
  - *(a) `DNF_min(f) = |f^{-1}(1)|`,*
  - *(b) aucun AND de `< n` littéraux n'est implicant de `f`,*
  - *(c) `f^{-1}(1)` est un independent set du graphe `Q_n` du n-cube.*

  Cf. [`tours/tour_13_independent_set_etabli.md`](tours/tour_13_independent_set_etabli.md) et [`checks/tour_13_independent_set_characterization.py`](checks/tour_13_independent_set_characterization.py).

  **Corollaire 1 (compte exact à n=4)** : la classe des fonctions vérifiant (a)/(b)/(c) sur n=4 contient exactement **743 fonctions** (= nombre d'independent sets de `Q_4`), distribuées par taille `|f^{-1}(1)|` selon `[1, 16, 88, 208, 228, 128, 56, 16, 2]`. La séquence des `|IS(Q_n)|` est `2, 3, 7, 35, 743, ...` (n=0,1,2,3,4,...).

  **Corollaire 2 (extrémalité PARITY)** : le maximum `|f^{-1}(1)| = 2^{n-1}` est atteint **exactement par PARITY et ¬PARITY** (les deux classes de la bipartition de `Q_n`). PARITY n'est plus un cas isolé du Tour 12 ; c'est l'élément maximal d'une classe combinatoire de 743 fonctions.

  **Preuves** : L13.1 (a)⟺(b) reprend Tour 12 généralisé. L13.2 (b)⟺(c) preuve directe par sous-cubes / arêtes de `Q_n`. L13.3 bijection triviale. L13.4 extrémalité par bipartition de `Q_n`.

  **Barrières** : non-relativisant (combinatoire sans oracle), RR non applicable (la propriété caractérise une classe, pas une fonction individuelle), non-algébrisant (pas d'arithmétisation).

  **Apport au dépôt** : *consolide et structure* le Tour 12. PARITY identifié comme élément maximal d'une classe identifiable (et non un cas isolé). Deuxième objet ÉTABLI.

  **Note (erreur référentielle mineure)** : le Proposeur cite OEIS A006506 pour le compte 743, mais A006506 = nombres de Dedekind (`2, 3, 6, 20, 168, 7581`). La séquence correcte est différente. Le chiffre 743 lui-même est correct par calcul exhaustif.

- **Théorème de la majorité** (Tour 14) : *`DNF_min(MAJ_n) = C(n, ⌈n/2⌉) ~ 2^n/√n`. Donc `MAJ_n ∉ AC⁰ d=2 polynomial`.*

  Cf. [`tours/tour_14_majority_etabli.md`](tours/tour_14_majority_etabli.md) et [`checks/tour_14_majority_dnf_lower_bound.py`](checks/tour_14_majority_dnf_lower_bound.py).

  **Preuves** :
  - L14.1 : `M` implicant de `MAJ_n` ⟺ `pos(M) ≥ ⌈n/2⌉` (force libres à 0 → sum minimal = pos(M)).
  - L14.2 : implicants premiers sans littéraux négatifs (suppression d'un `~x_i` préserve l'implication par L14.1).
  - L14.3 : implicants premiers = ANDs positifs de taille exactement `⌈n/2⌉`. Nombre = `C(n, ⌈n/2⌉)`.
  - L14.4 : pour chaque sous-ensemble `S` de taille `t = ⌈n/2⌉`, `χ_S` satisfait uniquement `M_S`. Donc tous les `C(n, t)` implicants premiers sont requis.

  **Vérification exhaustive n=4** : 81 ANDs, 33 implicants (incluant non-premiers), 6 implicants premiers (= C(4,2)) tous positifs taille 2, non-redondance vérifiée, DNF canonique de taille 6 calcule `MAJ_4`.

  **Note de bug corrigé** : la version initiale de L14.1 était erronée (« aucun implicant n'a de littéral négatif » — faux, 22 contre-exemples sur 81 ANDs). Le Proposeur a détecté le bug *via le calcul (j)* et corrigé en distinguant *implicant* / *implicant premier* avant soumission. Exemple parfait du rôle de la condition (j).

  **⚠️ Correction de formulation sur la séparation entre classes**. Le Proposeur a écrit comme conclusion : *« AC⁰ d=2 polynomial ⊊ TC⁰ d=1 polynomial »*. **Cette inclusion stricte est mal énoncée**. Ce que le théorème établit *réellement* est `MAJ_n ∈ TC⁰ d=1 \ AC⁰ d=2 polynomial`, donc **`TC⁰ d=1 ⊄ AC⁰ d=2 polynomial`** (séparation par témoin). L'inclusion réciproque `AC⁰ d=2 polynomial ⊆ TC⁰ d=1` est **fausse** : contre-exemple `DISJ_n(x, y) = ⋁_i (x_i ∧ ¬y_i)`, qui est dans AC⁰ d=2 polynomial mais pas dans TC⁰ d=1 (complexité communication non-triviale). Les deux classes sont **incomparables**. Erreur logique sur les classes (similaire à 2COL ∈ P du Tour 11) mais sans toucher le théorème central.

  **Barrières** : relativisation (preuve combinatoire sans oracle), RR (la propriété « f=MAJ_n » est unique parmi `2^{2^n}`, non-large), algébrisation (pas d'arithmétisation). ✓

  **Apport au dépôt** : *troisième objet ÉTABLI*, sur une fonction nouvelle (MAJ ≠ PARITY), avec borne sub-exponentielle `~ 2^n/√n` (pas exponentielle comme Tour 12). Première apparition de `TC⁰` dans la lignée FSS → Williams 2011. PARITY (Tour 12) et MAJ (Tour 14) constituent les deux fonctions canoniques séparant respectivement AC⁰ de classes plus puissantes.

- **Théorème de la famille seuil** (Tour 15-B) : *Pour tout `t ∈ [1, n]`, `DNF_min(THRESHOLD_{t, n}) = C(n, t)`. Par conséquent, `THRESHOLD_{t, n} ∉ AC⁰ d=2 polynomial` ssi `t = Θ(n)` (avec ratio strict).*

  Cf. [`tours/tour_15b_threshold_etabli.md`](tours/tour_15b_threshold_etabli.md) et [`checks/tour_15_threshold_dichotomy.py`](checks/tour_15_threshold_dichotomy.py).

  **Preuves** : L15.1–L15.4 sont la généralisation directe de L14.1–L14.4 (Tour 14) avec `t` quelconque en place de `⌈n/2⌉`. Tous les arguments restent valides.

  **Vérification exhaustive n=4** : pour `t ∈ {1, 2, 3, 4}`, comptes `C(4, t) = 4, 6, 4, 1` confirmés. Implicants premiers tous positifs, non-redondance vérifiée.

  **Dichotomie qualitative** : `C(n, t)` polynomial en `n` ssi `t` est constant ou (sub-)logarithmique (et symétriquement `n − t`). Pour `t = Θ(n)`, `C(n, t) ~ 2^n/√n` super-polynomial. Frontière exacte (nuance technique honnêtement notée par le Proposeur) : `t = O(log n / log log n)`, pas exactement `O(log n)`.

  **Cas particuliers unifiés** :
  - `t = 1` : `OR_n`, `C(n, 1) = n` polynomial → OR ∈ AC⁰ d=2 polynomial.
  - `t = ⌈n/2⌉` : `MAJ_n` (Tour 14), `C(n, ⌈n/2⌉) ~ 2^n/√n` non-polynomial.
  - `t = n` : `AND_n`, `C(n, n) = 1` trivial.

  **Condition (m) honorée explicitement** dès le premier tour suivant son ajout : séparation `TC⁰ d=1 ⊄ AC⁰ d=2 polynomial` par témoin (tout `THRESHOLD_{Θ(n)}`), pas inclusion stricte. Bon réflexe.

  **Barrières** : relativisation (preuve combinatoire), RR (famille de `n` fonctions parmi `2^{2^n}`, non-large), algébrisation (pas d'arithmétisation). ✓

  **Apport au dépôt** : *quatrième objet ÉTABLI*, première vraie **unification paramétrique**. Tours 12 (PARITY, `t = ?`), 14 (MAJ_n = THRESHOLD_{⌈n/2⌉}), 15 (THRESHOLD_t pour tout `t`) forment désormais une famille cohérente. La dichotomie polynomial/exponentiel comme fonction de `t` est un fait paramétrique nouveau pour le dépôt.

  **Risque noté** : 4 itérations dans la même veine (FSS profondeur 2). Le Tour 16 devrait diversifier (profondeur 3, ou Lean, ou autre famille de fonctions) pour ne pas saturer le paradigme.

- **Théorème de la famille MOD_p** (Tour 16) : *Pour tout `p ≥ 2` et tout `n`, `DNF_min(MOD_p_n) = |MOD_p^{-1}(1)| = Σ_{0 ≤ k ≤ n, k ≡ 0 (mod p)} C(n, k)`.*

  Cf. [`tours/tour_16_mod_p_etabli.md`](tours/tour_16_mod_p_etabli.md) et [`checks/tour_16_mod_p_dnf.py`](checks/tour_16_mod_p_dnf.py).

  **Preuves** :
  - L16.1 : `MOD_p^{-1}(1)` est independent set de `Q_n`. Argument : `dist_H(x, y) = 1` implique `sum(y) = sum(x) ± 1`, donc `sum(y) ≢ sum(x) (mod p)` pour `p ≥ 2`. Donc `x ∈ MOD_p^{-1}(1) ⇒ y ∉ MOD_p^{-1}(1)`.
  - L16.2 : application directe de L13 (Tour 13) — la condition « `f^{-1}(1)` independent dans `Q_n` » est satisfaite par L16.1, donc `DNF_min(f) = |f^{-1}(1)|`.
  - L16.3 : asymptotique par roots of unity filter — `|MOD_p^{-1}(1)| ~ 2^n/p`, super-polynomial pour `p` fixé.

  **Vérification exhaustive n=4** : pour `p ∈ {2,3,4,5}`, comptes `8, 5, 2, 1` confirmés. Independent set vérifié (distance Hamming minimale ≥ 2).

  **Diversification réussie** : sortie partielle du paradigme THRESHOLD. La famille `MOD_p` est **non-monotone** (flipper un bit change `sum mod p`), distincte de la famille THRESHOLD (monotone). Ouvre la lignée Razborov-Smolensky 1987 (qui prouve `MOD_p ∉ AC⁰[q]` à profondeur arbitraire pour `p ≠ q` premiers, par méthode polynomiale modulaire). Tour 16 traite seulement le cas profondeur 2 par application combinatoire de L13.

  **Apport au théorème L13** : Tour 13 n'avait été appliqué explicitement qu'à PARITY. Tour 16 utilise L13 comme **outil de production** pour identifier une nouvelle famille canonique. Le théorème de caractérisation gagne en valeur a posteriori.

  **Condition (m) honorée** : séparation par témoin (`MOD_p ∈ P \ AC⁰ d=2 poly`), pas d'affirmation d'inclusion stricte.

  **Note terminologique** : `MOD_2(x) = 1 ssi sum pair = ¬PARITY(x)` au sens strict (convention standard où `PARITY(x) = 1` ssi sum impair). `|MOD_2^{-1}(1)| = |¬PARITY^{-1}(1)| = 2^(n-1)` par symétrie de la bipartition de `Q_n`. Le résultat est cohérent avec Tour 12, mais l'identification « MOD_2 = PARITY » du Proposeur est imprécise.

  **Apport au dépôt** : *cinquième objet ÉTABLI*. Mais 5 itérations consécutives dans `AC⁰ d=2` — saturation persistante. Le Tour 17 doit *vraiment* diversifier.

- **Conjecture vérifiée à 4 points : INNER PRODUCT mod 2** (Tour 17) : *`DNF_min(IP_{2n}) = (3^n − 1)/2` pour `n ∈ {1, 2, 3, 4}`, conjecture pour tout `n ≥ 1`.*

  Cf. [`tours/tour_17_inner_product_etabli.md`](tours/tour_17_inner_product_etabli.md), [`checks/tour_17_inner_product_dnf.py`](checks/tour_17_inner_product_dnf.py) (Proposeur, n=1,2,3) et [`checks/tour_17_extension_n4.py`](checks/tour_17_extension_n4.py) (Réfuteur, n=4 via PuLP/CBC ILP).

  **IP est la première fonction HORS classe L13** du dépôt :
  - Non-monotone (flipper certains bits change `IP`).
  - Non-symétrique (`x` et `y` jouent des rôles distincts).
  - `IP^{-1}(1)` n'est PAS un independent set de `Q_{2n}` (vérifié : voisins Hamming-1 dans `IP^{-1}(1)`, ex. `(0,1,0,1) ↔ (1,1,0,1)`).

  **Validation à n=4 via ILP exact** : 6561 ANDs, 520 implicants, **40 implicants premiers** (32 de taille 5 + 8 de taille 7), set cover résolu par CBC en < 1s. DNF_min = 40 = (3^4 − 1)/2. ✓

  **Observation structurelle remarquable** : à chaque `n ∈ {2, 3, 4}`, `|implicants premiers(IP_{2n})| = DNF_min(IP_{2n})`. Cela signifie que **tous les implicants premiers sont nécessaires** dans le DNF minimal. Si on prouvait : (1) `|primes(IP_{2n})| = (3^n − 1)/2` pour tout `n`, et (2) non-redondance complète, alors le théorème serait acquis pour tout `n`.

  **Coefficient exponentiel `log_2 3 ≈ 1.585`** : strictement inférieur à `log_2 4 = 2` pour MAJ_{2n}. Première distinction quantitative entre deux fonctions super-polynomiales dans le dépôt.

  **Statut épistémique nouveau** : différent des Tours 12-16. Ces derniers étaient des théorèmes structurels prouvés pour tout `n` + vérifiés à n=4. Tour 17 était initialement une **conjecture vérifiée à 4 points consécutifs**, sans preuve générale. **Promotion au Tour 18** : la conjecture est désormais prouvée structurellement pour tout n.

  **Méthode ILP set cover** : nouveau dans le dépôt, réutilisable pour toute future fonction hors classe L13. Installation de PuLP/CBC pour cela.

  **Condition (n) honorée** : pas d'application de L13 ; nouvelle méthode (ILP). Diversification réelle.

- **Preuve structurelle de L17** (Tour 18) : *`DNF_min(IP_{2n}) = (3^n − 1)/2` prouvé pour tout n ≥ 1 par récurrence combinatoire.*

  Cf. [`tours/tour_18_ip_recurrence_etabli.md`](tours/tour_18_ip_recurrence_etabli.md) et [`checks/tour_18_ip_recurrence_proof.py`](checks/tour_18_ip_recurrence_proof.py).

  **Décomposition fondamentale** : `IP_{2(n+1)}(x_0..x_n, y_0..y_n) = x_n · y_n ⊕ IP_{2n}(x_0..x_{n-1}, y_0..y_{n-1})`. Cette décomposition permet la récurrence sur n.

  **L18.A (classification)** : par cas exhaustifs sur `(x_n, y_n)`, tout implicant premier de `IP_{2(n+1)}` appartient à exactement l'une des trois classes :
  - **A1** : `x_n ∧ y_n ∧ M_0` où M_0 est implicant premier de `¬IP_{2n}`.
  - **A2a** : `~x_n ∧ M_0` où M_0 est implicant premier de `IP_{2n}`.
  - **A2b** : `~y_n ∧ M_0` où M_0 est implicant premier de `IP_{2n}`.

  Tous les autres cas sont soit impossibles (paire libre forcerait IP_{2n} = ¬IP_{2n}), soit non-premiers (e.g. `~x_n ∧ ~y_n ∧ M_0` se simplifie en `~x_n ∧ M_0` ou `~y_n ∧ M_0`).

  **L18.B (récurrence + close-form)** : par L18.A, `a_{n+1} = 2a_n + b_n` et `b_{n+1} = a_n + 2b_n` (où `a_n = |primes(IP_{2n})|`, `b_n = |primes(¬IP_{2n})|`). Conditions initiales `a_1 = 1, b_1 = 2`. Close-form `a_n = (3^n − 1)/2, b_n = (3^n + 1)/2` par induction triviale.

  **L18.C (non-redondance)** : pour chaque implicant premier `M`, construction explicite du témoin unique :
  - A2a : `x = (x_0, x_n=0, y_n=1)` où x_0 est témoin unique de M_0 dans IP_{2n}^{-1}(1).
  - A2b : `x = (x_0, x_n=1, y_n=0)`.
  - A1 : `x = (x_0, x_n=1, y_n=1)` où x_0 est témoin unique de M_0 dans ¬IP_{2n}^{-1}(1).

  Vérification de couverture unique par cas (les autres classes ne couvrent pas le témoin à cause des fixations x_n/y_n). Par récurrence, tous les implicants premiers ont un témoin unique. ✓

  **Conclusion** : `DNF_min(IP_{2n}) = a_n = (3^n − 1)/2` pour tout n ≥ 1.

  **Vérification empirique** : récurrence et énumération directe coïncident pour n=1, 2, 3, 4. Prédiction récurrence pour n=5 (121), n=6 (364).

  **Apport méthodologique nouveau** : *premier tour qui consolide un tour précédent* en bouchant un trou dans sa preuve. Chaîne Tour 17 (empirique) → Tour 18 (structurel) illustre la suite « vérifier → identifier le pattern → prouver ». Pattern précieux pour d'autres conjectures potentielles.

  **Note** : L18.C esquissée par le Proposeur, détaillée par le Réfuteur. La construction explicite du témoin pour chaque classe + vérification de couverture unique complète rigoureusement la preuve.

  **Conséquence** : le 6e objet ÉTABLI du dépôt passe d'« empirique n=1..4 + conjecture pour n ≥ 5 » à « théorème prouvé pour tout n ≥ 1 ». Tous les 6 objets sont désormais structurels.

- **Théorème de caractérisation d'essentialité** (Tour 19) : *pour toute fonction booléenne non-constante `f`, `DNF_min(f) = |primes(f)|` ⟺ chaque implicant premier admet un témoin essentiel.*

  Cf. [`tours/tour_19_essentialite_etabli.md`](tours/tour_19_essentialite_etabli.md) et [`checks/tour_19_primes_eq_dnfmin.py`](checks/tour_19_primes_eq_dnfmin.py).

  **Définition** : *témoin essentiel* d'un implicant premier `M` = une affectation `x ∈ f^{-1}(1)` que `M` est l'unique implicant premier à satisfaire.

  **Preuve** :
  - L19.A : (α) ⇒ (β) par contrapositive (si M sans témoin essentiel, primes\{M} couvre f^{-1}(1), donc DNF_min < |primes|).
  - L19.B : (β) ⇒ (α) (chaque M force son inclusion dans tout DNF minimal via son témoin essentiel).
  - L19.D : L13 ⊊ (α)/(β) avec témoin MAJ_3 (dans (α)/(β) mais MAJ_3^{-1}(1) pas independent dans Q_3).

  **Vérification empirique** : à n=3, 202/254 (79.5%) fonctions dans la classe ; à n=4, 23862/65534 (36.4%). Distribution du défaut `|primes| − DNF_min` à n=4 : 23408 fonctions à diff=1, 9856 à diff=2, …, 8 à diff=8.

  **Unification des Tours 12-18** : tous les 6 théorèmes précédents deviennent des spécialisations de L19. Chaque famille (PARITY, MAJ, THRESHOLD_t, MOD_p, IP) est dans (α)/(β) et a `|primes|` calculé explicitement. L19 fournit le **théorème-cadre** qui caractérise pourquoi.

  **Risque RR** : la propriété (β) est constructive (poly en `2^n`) et large à n=4 (36%). Si on prétendait dériver une borne inférieure générale, RR s'appliquerait. Le théorème actuel ne le fait pas — il caractérise une classe sans en tirer de borne universelle. Compatible avec RR dans son usage actuel.

  **Conjecture asymptotique** : « la fraction `|(α)/(β)| / 2^{2^n}` tend vers 0 quand n → ∞ ». Suggérée par 79.5% (n=3) → 36.4% (n=4), mais non démontrée. Pas un théorème.

  **Lien à P vs NP** : L19 caractérise précisément les fonctions où DNF minimization est en P (algo glouton optimal). Hors classe, le problème est Σ₂^P-difficile (Umans 1999). Lien indirect via la hiérarchie polynomiale.

  **Apport au dépôt** : *unification conceptuelle*. Le paradigme « AC⁰ d=2 par essentialité » est désormais saturé : continuer à cataloguer des familles dans (α)/(β) ne donnerait rien de nouveau.

  **Apport mathématique** : zéro (théorème classique de Quine-McCluskey 1952-1956). Mais l'unification conceptuelle est un acquis réel pour le dépôt.

- **Théorème des fonctions antipodales** (Tour 20) : *pour `f_α(x) = 1 ⟺ x ∉ {α, ¬α}` (n ≥ 3) :*
  - *(i) `|f_α^{-1}(1)| = 2^n − 2`,*
  - *(ii) `|primes(f_α)| = n(n − 1)` (les `x_i ∧ ~x_j` pour i ≠ j),*
  - *(iii) `DNF_min(f_α) = n` (atteint par tout cycle dirigé),*
  - *(iv) défaut = `n(n − 2)`.*

  Cf. [`tours/tour_20_antipodales_etabli.md`](tours/tour_20_antipodales_etabli.md) et [`checks/tour_20_antipodal_verification.py`](checks/tour_20_antipodal_verification.py).

  **Preuves auditées** (WLOG α = 0...0) :
  - (ii) M implicant ⟺ M(0...0)=0 et M(1...1)=0 ⟺ M contient au moins un positif et un négatif. Premier ⟺ exactement 1 positif + 1 négatif. Comptage n·(n−1).
  - (iii) ≤ : cycle `{x_i ∧ ~x_{(i+1) mod n}}`. Toute x ∈ f^{-1}(1) a au moins une transition cyclique 1→0, satisfaite par un implicant du cycle. ≥ : pour chaque e_i (Hamming weight 1), l'unique implicant le couvrant a forme `x_i ∧ ~x_j`. Donc ≥ n implicants requis.

  **L20.5 (corollaire conjectural)** : seules les antipodales atteignent le défaut maximal n(n−2). Vérifié exhaustivement n=3 (4/4) et n=4 (8/8). Conjecturé pour n ≥ 5 (énumération de `2^{2^n}` infaisable).

  **Vérification empirique** : n=3 → 4 antipodales (défaut 3 = 3·1), n=4 → 8 (défaut 8 = 4·2), n=5 → 16 (défaut 15 = 5·3). Tous conformes à la formule.

  **Lien P vs NP** : Tour 20 caractérise les fonctions à *défaut maximal* dans le paysage post-Tour 19. Pôle extrême opposé à la classe (α)/(β). **Note importante** : le lien à la Σ₂^P-difficulté de DNF-MIN (revendiqué par le Proposeur) est *plus faible que présenté*. Sur les antipodales, DNF-MIN est facile (`DNF_min = n` en O(n)) ; le défaut élevé concerne la redondance de l'algorithme glouton, pas la difficulté intrinsèque du problème. La Σ₂^P-difficulté d'Umans 1999 vient d'autres familles.

  **Apport au dépôt** : *cartographie bidirectionnelle* du paradigme AC⁰ d=2. L19 (pôle « facile ») + L20 (pôle « défaut maximal ») délimitent les deux extrêmes.

  **Risque (RR)** : famille petite (`2^{n-1}`), non-large. RR sans objet.

  **Saut qualitatif réel ?** Partiel. Tour 20 sort de (α)/(β) mais reste dans le paradigme AC⁰ d=2. Pas de profondeur 3, pas de Lean, pas de Razborov. **Le Tour 21 doit faire un saut qualitatif vrai** (cf. directions infra).

### ❓ Conjecturaux pour P vs NP (plausibles mais non prouvés)
- *(aucun retenu pour l'instant)*

### 📚 Acquis hors-but principal (objets mathématiques sans lien démontré à P vs NP)

> **Note de recadrage (fin tour 9).** Les objets ci-dessous sont mathématiquement
> corrects et vérifiables, mais leur lien à P vs NP n'a pas été établi. Ils sont
> conservés pour leur intérêt mathématique propre (algèbre commutative
> computationnelle des fonctions monotones), mais ne comptent **pas** comme
> progrès sur la question du dépôt. Pour qu'ils en deviennent un, il faudrait
> exhiber un pont vers une borne de complexité — pont qui a échoué à chaque
> tentative (cf. Tour 7 : pd ne capture pas D_m via le contre-exemple OR_n).

- **Atlas des 95 fonctions monotones n=4 à résolution pure** (Tour 8, cf. [`checks/tour_08_atlas_boij_soderberg.py`](checks/tour_08_atlas_boij_soderberg.py)) — sur les 168 fonctions monotones non-constantes sur n=4 variables, exactement **95** ont un idéal de Stanley-Reisner à résolution libre minimale pure (au sens Boij-Söderberg : un seul shift par index homologique). La distribution par taille d'implicants + nombre d'implicants est tabulée dans le tour 8. *Lien à P vs NP : aucun démontré.*

- **Théorème L9.1** (Tour 9) : *pure ⇒ equigenerated*. Pour toute fonction monotone non-constante `f`, si `I_f` admet une résolution libre minimale pure alors tous ses implicants premiers ont la même taille. **Preuve triviale par contrapositive** : deux degrés différents `t_1 ≠ t_2` impliquent `β_{0,t_1}(I) > 0` et `β_{0,t_2}(I) > 0`, donc deux shifts à l'index 0, non-pure. Vérifié empiriquement sur n=4 (0 contre-exemple sur 167) et n=5 (0 contre-exemple sur 7579). *Lien à P vs NP : aucun démontré.*

- **Fait empirique** (Tour 9, cf. [`checks/tour_09_extension_n5.py`](checks/tour_09_extension_n5.py)) : la réciproque *equigenerated ⇒ pure* est **vraie sur n=4** (167 fonctions sans exception) mais **fausse sur n=5** (215 contre-exemples sur 7579). Contre-exemple minimal canonique : `f = (x₁∧x₂∧x₃) ∨ (x₁∧x₂∧x₄) ∨ (x₀∧x₃∧x₄)` ; tous mintermes de taille 3 (equigenerated), mais `β_{0,3}(I)=3, β_{1,4}(I)=1, β_{1,5}(I)=1` (deux shifts à l'index 1, donc non-pure). Causé par hétérogénéité des syzygies linéaires (deg 4) et quadratiques (deg 5) à l'intérieur du même idéal. *Lien à P vs NP : aucun démontré.*

- **Tableau de contingence n=5** :
  ```
                  | equi=True | equi=False
  pure=True       |      1894 |          0
  pure=False      |       215 |       5470
  ```

- **Fait empirique négatif sur la conjecture C10** (Tour 10, cf. [`checks/tour_10_intersection_uniform_conjecture.py`](checks/tour_10_intersection_uniform_conjecture.py)) : la caractérisation candidate *« pour `f` equigenerated, `I_f` pure ⟺ toutes les intersections non-vides entre paires de mintermes ont la même taille »* est **fausse dans les deux directions** sur n=5. Sur 2110 fonctions equigenerated non-constantes : **1068 contre-exemples** (893 cas pure-mais-non-uniform + 175 cas uniform-mais-non-pure). Cf. tableau :
  ```
                  | uniform=True | uniform=False
  pure=True       |         1002 |           893
  pure=False      |          175 |            40
  ```
  Le Proposeur a effectué ce test **avant** de soumettre la conjecture (condition (j) honorée pour la 2e fois consécutive) et a retiré C10 sans la proposer. *Lien à P vs NP : aucun démontré.*

### ⚠️ Lacunes réparables (direction légitime mais énoncé spécifique faux)

- **Piste 6 — « Gap homologique sémantique sur Stanley-Reisner ».** Première piste à ne PAS être en faille fatale. Direction correcte (topologie sémantique pour fonctions monotones, lignée Razborov 1985 / Knill-Forman / Björner-Wachs / Reiner-Welker), mais énoncé du Proposeur faux :
  - **Lemme 2 réfuté empiriquement** (cf. [`checks/tour_06_stanley_reisner.py`](checks/tour_06_stanley_reisner.py)) : sur les 168 fonctions monotones de `n = 4`, **52 ont `β_1(Δ_f) > 0`**, et **les 52 violent** la borne « taille > #faces maximales ». Contre-exemple canonique : `f = (x_0 ∧ x_2) ∨ (x_1 ∧ x_3)`, dont `Δ_f` est le complexe de drapeau du 4-cycle C_4 (β_1 = 1), mais taille de circuit = 2 < 4 = #faces maximales.
  - **Lemme 1 imprécis** : confond le complexe `Δ_f` avec l'**idéal** `I_{Δ_f}` (engendré par les non-faces minimales). Les implicants premiers sont les générateurs de l'idéal, *pas* des faces de Δ_f. Reformulé correctement, L1 devient une tautologie définitionnelle.
  - **(f) non satisfaite** : calcul promis (« je m'engage à concevoir un script SageMath ») non livré ; je l'ai effectué à la place, et il a réfuté la conjecture sous-jacente.
  - **Signe d'alarme RR** : l'invariant `β_i` est calculable en temps polynomial sur la table de vérité (constructif), et `β_1 > 0` est large (31 % à n=4). Si la borne marchait, elle serait *naturelle* au sens de Razborov-Rudich, donc condamnée par les preuves naturelles sous crypto standard.

  Pour réparer : reformuler en termes d'idéal de Stanley-Reisner et invoquer des invariants algébriques plus fins (régularité de Castelnuovo-Mumford, profondeur projective, Betti gradués / formule de Hochster). Mais alors la piste sort du cadre « calcul exhaustif sur n=5 » et entre dans l'algèbre commutative computationnelle — direction active mais bien plus difficile. La lacune est précise (énoncé à raffiner) mais sa réparation déplace hors du sous-but Tour 6.

- **Piste 7 — « Obstruction homologique duale (résolutions libres + dualité d'Alexander) ».** Le Proposeur a fait le pivot exact suggéré au Tour 6 : `Δ_f` → idéal `I_f`, avec résolutions libres minimales et dualité d'Alexander/Eagon-Reiner. Premier tour à honorer **(h)** : chiffres livrés (`Betti(I_{C_4}) = (4,4,1,0)`, `Betti(I_{K_4}) = (6,8,3,0)`, pd = 2 pour les deux), vérifiés indépendamment par implémentation de Hochster (cf. [`checks/tour_07_resolutions_libres.py`](checks/tour_07_resolutions_libres.py)). Mais **le Lemme 2 conjectural (D_m(f) ≥ Ω(pd(I_f))) est réfuté par contre-exemple OR_n** :
  - `I_{OR_n} = m = (x_1, …, x_n)`, résolution Koszul → pd(I) = n − 1.
  - `D_m(OR_n) = 1` (un OR de fan-in n) ou `log_2 n` (binaire).
  - Pour n = 3, 4, 5, 6 : pd(I) ∈ {2, 3, 4, 5}, D_m = 1 partout. Aucune constante c > 0 ne sauve L2.

  **Raison structurelle profonde** : toute fonction monotone non-constante admet une DNF de profondeur 2, donc `D_m(f) ≤ 2` sans contrainte de taille. Aucune inégalité `D_m ≥ f(pd)` non-bornée ne peut tenir, OR_n étant le cas extrême. Même MAJ_n viole L2 pour n ≥ 7 (D_m=2, pd=⌊n/2⌋−1).

  Le Proposeur lui-même admet (Aveu 1) que L2 est conjectural, et (Aveu 2) que le cadre se limite aux formules monotones — pas aux circuits, donc même un L2 valide ne donnerait pas P vs NP.

  **Verdict ⚠️ LACUNE RÉPARABLE** (meilleur tour à ce stade) : direction techniquement saine, chiffres corrects, (h) honorée. La lacune précise est l'**invariant algébrique manquant** : `pd` ne capture pas `D_m`. Toute proposition future doit passer le test OR_n (où pd explose mais D_m reste petit).

- **Piste 8 — « Atlas de Boij-Söderberg des fonctions monotones n=4 ».** Premier tour à abandonner explicitement la prétention à P vs NP (condition (i) honorée) au profit d'un objet de catalogage fini. Mouvement stratégique correct. Mais le Lemme 4 (« OR_n et AND_n sont les seules fonctions monotones à résolution pure, prouvable inconditionnellement pour tout n ») est **massivement faux** (cf. [`checks/tour_08_atlas_boij_soderberg.py`](checks/tour_08_atlas_boij_soderberg.py)) :
  - Faux dès n=3 : `MAJ_3 = I(K_3) = (x_0 x_1, x_0 x_2, x_1 x_2)` a Betti(I) = (3, 2) à shifts (2, 3) — résolution pure (r=1), pourtant ni OR_3 ni AND_3.
  - Sur n=4 : **95 fonctions monotones sur 167 non-constantes** ont des résolutions pures, pas 2. Erreur d'un facteur ~47. La 4-classe des fonctions threshold (OR_4, MAJ_4, THRESHOLD_3, AND_4) est pure (par Veronese squarefree), plus de nombreuses autres : OR de littéraux, paires d'arêtes disjointes (shifts non-consécutifs (2,4)), AND simples, etc.
  - Justification mathématique invoquée (Herzog-Kühl) mal interprétée : HK 1984 donne des contraintes sur Betti pour résolutions pures, pas une caractérisation binaire « linéaire ou principal ».
  - (h) toujours non honorée : aucun script livré, aucun CSV, aucun calcul. Le Réfuteur effectue le travail à sa place.

  **Atlas livré (sous-produit positif) :** classification des 95 fonctions monotones n=4 à résolution pure, avec mintermes et shift sequences. C'est le **premier objet mathématique positif** du dépôt, au-delà des réfutations. Reproductible via `checks/tour_08_atlas_boij_soderberg.py`.

  **Verdict ⚠️ LACUNE RÉPARABLE (3e consécutive)** : posture stratégique correcte, direction valide, atlas utile produit ; mais l'unique théorème revendiqué est faux. Pattern persistant sur 8 tours : le Proposeur corrige le défaut tour précédent mais introduit une nouvelle conjecture qui se révèle fausse à l'examen.

- **Piste 8 bis — Révision du Proposeur** (réponse au verdict ci-dessus). Admission honnête de l'erreur du Lemme 4, retrait, et révision en : *« I_f a résolution pure ssi f est une fonction threshold TH_t, à permutation près »*. **Encore faux** :
  - Prédit 4 fonctions threshold pures sur n=4. Réalité (mon atlas) : 95.
  - 4 contre-exemples concrets dans l'atlas même : `f = x_0` (1 minterme, pas threshold), `f = x_0 ∨ x_1` (2 mintermes, pas threshold), `f = (x_0∧x_1) ∨ (x_0∧x_2)` (2 mintermes de taille 2, mais TH_2 = MAJ_4 en a 6), `f = (x_0∧x_1∧x_2) ∨ (x_0∧x_1∧x_3)`.
  - Plus précisément : les sous-OR et sous-AND (fonctions dépendant de < n variables) ont toutes des résolutions pures et ne sont pas thresholds.
  - **Violation immédiate de (j)** : le Proposeur a soumis ce mini-théorème révisé sans avoir vérifié contre l'atlas n=4 que je venais de produire et publier. C'est exactement la condition (j) que (j) cherchait à empêcher, violée en temps réel.

  Pattern désormais établi sur 9 itérations (8 tours + 1 révision) : le Proposeur articule des théorèmes asymptotiques sans calcul empirique préalable, même quand la condition est explicitement énoncée. La boucle adverse (Réfuteur exécutant les calculs) est apparemment **nécessaire en permanence** pour catalyser une rigueur empirique que le Proposeur seul ne maintient pas.

- **Piste 9 — « Conjecture C9 : pure ⟺ equigenerated ».** Premier tour où le Proposeur honore vraiment (h) et (j) : il livre le script `checks/tour_09_equigeneration_conjecture.py` qui vérifie sa conjecture à n=4 (tableau parfait 95/0/0/72) avant soumission. Il anticipe explicitement le risque de réfutation à n=5 (Aveu 1). C'est un saut épistémologique réel.
  - **L9.1 (pure ⇒ equigen)** : triviale par contrapositive, confirmée. ✓ Établi.
  - **L9.2 (equigen ⇒ pure)** : vraie sur n=4 mais **fausse sur n=5**. J'ai écrit `tour_09_extension_n5.py` qui énumère les 7581 fonctions monotones n=5 via récursion de Dedekind, identifie 215 contre-exemples. Contre-exemple minimal : `(x₁x₂x₃) ∨ (x₁x₂x₄) ∨ (x₀x₃x₄)`, equigenerated mais avec deux shifts (4 et 5) à l'index 1 — due à coexistence de syzygies linéaires (deg 4, paires partageant 2 var) et quadratiques (deg 5, paires partageant 1 var).
  - **Verdict ⚠️ LACUNE RÉPARABLE (4e consécutive)** avec note positive : la conjecture est réfutée, mais l'**épistémologie est correcte**. Le Proposeur a posé une conjecture testable et falsifiable, anticipé le risque, et apporté un script vérifiable. C'est le meilleur tour à ce stade.

  La conjecture raffinée (à venir, problème ouvert) : *quelles conditions combinatoires distinguent les 1894 cas où equigen ⇒ pure tient des 215 cas où elle échoue ?* Question d'algèbre commutative intéressante en soi.

- **Piste 10 — Test préemptif de C10 + pivot Lean Koszul (rejeté).** Deux mouvements distincts :
  - **(a) Excellente épistémologie** : le Proposeur a testé sa conjecture candidate C10 (« intersections uniformes ») sur les 2110 fonctions equigenerated n=5 *avant* de la soumettre. 1068 contre-exemples identifiés. **Conjecture retirée par le Proposeur lui-même.** (j) honorée pour la 2e fois consécutive. Pattern « conjecture spéculative → réfutation » enfin brisé.
  - **(b) Pivot mal ciblé** : faute de C10, le Proposeur propose de formaliser en Lean la résolution de Koszul de `m_n = (x_1, …, x_n)`. **Bon mouvement stratégique** (sortir de la spéculation, viser certification mécanique) mais **mauvais théorème cible** : Koszul de `m_n` est hors-sujet vis-à-vis de P vs NP. Le Proposeur l'admet explicitement (*« Distance à P vs NP : maximale, assumée »*). Viole (i) corrigée et (k) ajoutée.

  **Recadrage utilisateur** : direction prescrite pour Tour 11 = **mini-théorème `PARITY ∉ AC⁰` profondeur 2 sur n=4 ou n=5**. Calcul exhaustif Python (énumérer les DNF/CNF de taille bornée, vérifier qu'aucun ne calcule `parity_n`) + perspective formalisation Lean. Lié à P vs NP via la lignée Furst-Saxe-Sipser 1981 → Razborov-Smolensky 1987 → Williams 2011.

  **Verdict ⚠️ LACUNE RÉPARABLE** : épistémologie excellente, mais direction à corriger.

- **Piste 11 — Lifting (Raz-McKenzie / GPW) + Karchmer-Wigderson + Tseitin sur expandeur → `D_m(2COL_G) ≥ Ω(n log n)`.** Première proposition recentrée sur P vs NP après le recadrage. Cadre théorique réel (Ben-Sasson-Wigderson 2001, Raz-McKenzie 1999, Göös-Pitassi-Watson 2018, Karchmer-Wigderson 1990). Conditions (i), (k), (l) honorées. **Mais** :
  - **Erreur factuelle décisive** : 2-COLORATION = test de bipartiteness, **dans P** (BFS/DFS linéaire), **pas NP-complet**. Toute la motivation revendiquée (« fonction monotone NP ») s'effondre. 3-COL est NP-complète, CLIQUE_k aussi ; 2COL ne l'est pas. Erreur de niveau cours de licence en complexité.
  - **Erreur de cadre** : 2COL n'est pas naturellement monotone (ni en coloration ni en arêtes). Karchmer-Wigderson exige une fonction monotone identifiée, ce qui n'est pas le cas.
  - **Chaîne L10.5 conjecturale** : la transposition « lifted Tseitin → 2COL via KW » est admise non prouvée par le Proposeur (Aveu 2). Pattern récurrent qui a tué les Tours 4, 7, 9.
  - **(j) régressée** : test empirique sur n=4, 6, 8 promis mais aucun script livré, aucun résultat numérique. Régression par rapport aux Tours 9 et 10 où (j) avait été honorée.
  - **Redondance possible** avec Garg-Göös-Knop-Watson 2018 non vérifiée bibliographiquement.

  Réparations possibles : remplacer 2COL par **CLIQUE_k** (monotone et NP-complète, exactement Razborov 1985), livrer le test empirique, vérifier GGKW 2018 et la chaîne L10.5. Mais ces réparations sont substantielles et le pattern conjecture-pont persiste.

  **Décision utilisateur (option 1)** : rejet maintenu, prescription Tour 12 = prescription Tour 11 du recadrage réaffirmée = **`PARITY_n ∉ AC⁰ profondeur 2` sur n=4 par calcul exhaustif Python**.

  **Note méthodologique** : c'est la 2e fois consécutive (Tours 10 et 11) que le Réfuteur doit *prescrire* la direction plutôt que réfuter une proposition cohérente. La boucle adverse à un Proposeur LLM, après 10 itérations, a épuisé l'espace des « grandes idées spéculatives » et doit se rabattre sur des cibles techniques précises et bornées.

- **Piste 12 — Mini-théorème `PARITY_n ∉ AC⁰ profondeur 2` de taille `< 2^(n-1)`.** Le Proposeur accepte intégralement la prescription du recadrage, exécute le calcul *avant* soumission, livre le script `tour_12_parity_ac0.py` et les chiffres exacts. **Toutes les 12 conditions (a)–(l) honorées pour la première fois.**
  - L'argument structurel L12.1–L12.4 est combinatoire élémentaire et valable pour tout n, prouvé.
  - Vérification exhaustive n=4 : 81 ANDs énumérés, 8 implicants tous de taille 4, bijection avec les 8 affectations impaires, DNF canonique de taille 8 calcule `parity_4`. Reproduit indépendamment par le Réfuteur.
  - Test des trois barrières confirmé : relativisation (preuve combinatoire sans oracle), preuves naturelles (propriété pas large : seules `parity` et `¬parity` ont implicants tous de taille n, donc `2/2^{2^n}` ≪ `2^{-O(n)}`), algébrisation (pas d'arithmétisation).
  - **Premier objet ✅ ÉTABLI POUR P vs NP du dépôt.** Après 11 itérations dont 5 FAILLE FATALE et 6 LACUNE RÉPARABLE / rejets, le dépôt a enfin un théorème prouvé et aligné sur la question.
  - *Novelty mathématique : zéro* (théorème de FSS 1981 profondeur 2, dans tout manuel). Mais *novelty épistémique pour le dépôt* : premier théorème réellement démontré et lié à P vs NP, ce qui n'avait jamais été fait dans les 11 tours précédents.

  Cf. [`tours/tour_12_parity_ac0_etabli.md`](tours/tour_12_parity_ac0_etabli.md).

### ❌ Réfutés (faux — et pourquoi, pour ne pas y revenir)
- **Piste 1 — « contradiction de compressibilité des témoins ».** Le sophisme central : la confrontation oppose un Kt **inconditionnel** (Lemme 1, incompressibilité Ω(n)) à un Kt qui n'est petit que **conditionnellement à x** (Lemme 2, vrai sous la forme K(w|x)=O(1), pas K(w)=O(log n) — la description doit embarquer x, de taille poly(n)). En unifiant les deux quantités, la contradiction disparaît : soit Lemme 2 redevient faux (inconditionnel), soit Lemme 1 redevient faux (conditionnel, car le témoin lex-premier est déterminé par x). Le fossé entre conditionnel et inconditionnel **est** P vs NP → circularité.
- **De plus : la piste 1 relativise** (Kt, auto-réductibilité, recherche↔décision relativisent tous). Par BGS, elle ne peut donc structurellement pas séparer P de NP, même réparée. À NE JAMAIS réessayer sous cette forme.

- **Piste 2 — « signature p-adique des témoins (Ax-Katz pour AC⁰) ».** Quatre failles convergentes, deux vérifiées par calcul (cf. [`checks/tour_02_axkatz_p_adique.py`](checks/tour_02_axkatz_p_adique.py)) :
  1. Le « Lemme 1 » revendique une arithmétisation AC⁰ → degré polylog. Faux pour l'arithmétisation **exacte** : la version polylog (Razborov-Smolensky) est une **approximation probabiliste**, et Ax-Katz exige des polynômes exacts. Empiriquement, l'arithmétisation exacte d'un 3-CNF à `k` clauses a un degré strictement égal à `3k = poly(m)`.
  2. Le « Lemme 2 » (Ax-Katz force `μ ≈ m/d` polynomial) **s'écroule sous la contrainte booléenne** `w_i² = w_i`. Les `m` équations ajoutées (degré 2 chacune) font passer le minorant à `⌈(m − d − 2m) / max⌉ ≤ 0` — **trivial dans tous les cas**. Ax-Katz ne dit absolument rien sur le nombre de témoins booléens. C'est précisément pour cela qu'on n'utilise pas Ax-Katz en complexité booléenne.
  3. La technique **algébrise** au sens d'Aaronson-Wigderson : l'invariant `v_p(N_x)` est une fonction d'une extension algébrique du vérificateur, donc relativise par rapport aux oracles algébriques relativement auxquels `P^Õ = NP^Õ`. L'argument anti-algébrisation du Proposeur (« `Õ` ne respecte pas le degré polylog ») est circulaire : la contrainte de degré polylog est sa propre invention, pas une propriété du cadre AW.
  4. « Lemme 3 » (arithmétisation de P) faux par le même mécanisme que (1) : un algorithme polynomial en temps `n^k` s'arithmétise à la Shamir en degré `n^{O(k)}` polynomial, pas polylog. La « contrainte géométrique » du Lemme 4 disparaît.

  À NE JAMAIS réessayer sous cette forme. **Nuance honnête** : le programme algébrique-géométrique en complexité existe (GCT, permanent vs déterminant), mais il n'utilise pas Ax-Katz pour les raisons ci-dessus. Confondre comptage algébrique (Ax-Katz) et existence booléenne (P vs NP) est l'erreur centrale.

- **Piste 3 — « obstruction topologique sur le paysage d'énergie d'un CSP ».** Deux failles fatales indépendantes, vérifiées par calcul (cf. [`checks/tour_03_topologie_morse.py`](checks/tour_03_topologie_morse.py)) :
  1. **L'invariant `Σ β_i(L_k(φ))` n'est pas une fonction de la fonction booléenne, mais de sa présentation syntaxique.** Le Proposeur l'admet (« deux formules équivalentes peuvent avoir des paysages différents ») sans en mesurer la conséquence. Démontré numériquement : pour ψ = (x_0∨x_1) ∧ (x_2∨x_3) ∧ (x_4∨x_5) et ψ' = ψ avec chaque clause triplée (mêmes 27 témoins, fonction booléenne identique), `Σ β_i(L_1)` vaut **92 pour ψ et 29 pour ψ'** (facteur 3) ; à `k=2`, **125 vs 29** (facteur 4). Conséquence : un algorithme P pour SAT peut préprocesser toute CNF en forme canonique en temps poly avant de décider — toute borne inférieure dérivée d'un invariant variant sous équivalence logique s'évanouit. `P` et `NP` étant des classes de fonctions/langages, un tel invariant ne peut structurellement pas les séparer. Ce n'est pas RR, c'est plus grave : on sort du cadre P vs NP.
  2. **Le Lemme 3 (MT modélisée comme champ de vecteurs à sauts bornés) est faux.** Une MT en temps `n^c` peut modifier `n^c` bits par étape ; le graphe pertinent est `G_{n^c}` = cube avec arêtes Hamming ≤ `n^c`. Dès `r = 2`, les Betti s'effondrent. Démontré sur CSP `x_i = x_{i+3}` (8 témoins sur la diagonale) : `β_0 = 8` à `r = 1`, mais `β_0 = 1` dès `r = 2`. La théorie de Morse discrète (Forman 1998) est strictement à 1-saut ; sa généralisation aux sauts polynomiaux trivialise l'obstruction. *Sans* Lemme 3, le Lemme 4 ne se prouve pas.

  À NE JAMAIS réessayer sous cette forme. **Nuance honnête** : le clustering topologique des CSP en phase RSB (Mézard-Parisi-Zecchina, Achlioptas et al.) borne effectivement les algorithmes **locaux** — pas P entier. Confondre « bornes pour algos locaux » et « bornes pour P » est l'erreur centrale.

- **Piste 4 — « compilation TC⁰ → tensor network à bond polynomiale + Williams + hardness magnification ».** Première piste à cocher formellement les 5 conditions du sous-but ; les attaques portent donc sur le contenu technique. Faille fatale principale, vérifiée par calcul (cf. [`checks/tour_04_tensor_network_TC0.py`](checks/tour_04_tensor_network_TC0.py)) :
  1. **Le Lemme 1 (« tout circuit TC⁰ de profondeur d et taille S compile en bond dimension χ = S^{O(d)} ») est faux.** Contre-exemple direct : `IP_n(x,y) = (x · y) mod 2`, calculable par un circuit TC⁰ de profondeur 2 et taille polynomiale (Hajnal-Maass-Pudlák-Szegedy 1993). Sa matrice de communication à la coupe `x|y` a un rang sur ℝ valant exactement `2ⁿ − 1` (essentiellement la matrice de Hadamard à un facteur près). Bond dimension = `2ⁿ − 1`, exponentielle, calculée pour `n ∈ [1, 8]`.
  2. **La parade « passer à F₂ »** (où le rang chute à `n`) **détruit l'outillage**. Le mécanisme proposé (SVD adaptative, décroissance des valeurs singulières, troncation analytique) est intrinsèquement analytique sur ℝ/ℂ — pas de SVD ni de norme L² sur F₂. De plus, un rang `n` sur F₂ représente `n × 2ⁿ` bits, sans gain sur la table de vérité.
  3. **Confusion structurelle :** le Proposeur conflate « TC⁰ est petit en circuit » et « TC⁰ a faible intrication ». Or TC⁰ peut calculer IP_n donc atteindre la complexité de communication maximale `Θ(n)`. Les techniques de rang/discrépance/communication, qui marchent pour AC⁰, **échouent toutes pour TC⁰** depuis 1993 — exactement la raison pour laquelle les bornes inférieures pour TC⁰ restent ouvertes.
  4. **Sans le Lemme 1**, l'idée se réduit à « trouver un algorithme CAPP non-trivial pour TC⁰ et appliquer Williams ». C'est le programme de recherche actif de la communauté depuis 2010 (Williams, Murray, Chen, Tamaki, Servedio, Tal...) — pas une contribution.
  5. **Bonus** : la hardness magnification (utilisée pour passer de NEXP à NP) a ses propres barrières internes connues (Chen-Hirahara-Oliveira-Pich-Rajgopal-Santhanam 2019, « Beyond Natural Proofs »).

  À NE JAMAIS réessayer sous cette forme spécifique. **Nuance honnête** : la *direction générale* (Williams pour TC⁰) reste la plus prometteuse aujourd'hui — mais sans algorithme nouveau, ce n'est pas une piste exploitable dans notre boucle adverse. Le Proposeur a entendu le feedback (cible adéquate, conditions formelles cochées) mais n'a apporté aucune contribution technique au-delà de la stratégie globale.

- **Piste 5 — « indistinguabilité CPT+C des hypercubes colorés `H_f` (jeux de pavage bijectifs + canonisation Dawar) ».** Pivot vers la complexité descriptive. Triple faille (cf. [`checks/tour_05_cpt_jeux_pavage.py`](checks/tour_05_cpt_jeux_pavage.py)) :
  1. **Lemme 3 trivialement impossible** : le Proposeur veut `H_f` (UNSAT) ≡_{CPT+C} `H_g` (SAT). Or la sentence FO `∃ x. f(x) = 1` distingue toute paire (UNSAT n'a aucun sommet colorié 1, SAT en a au moins un), et FO ⊂ FO+C ⊂ CPT+C. Le Spoiler gagne en 1 tour. Vérifié pour 3 paires explicites : multiset `(#col 0, #col 1)` toujours `(64, 0)` UNSAT vs `(<64, ≥1)` SAT.
  2. **Mauvais encodage** : la propriété distinguante (SAT vs UNSAT) est encodée *en surface* (la coloration), donc trivialement FO-définissable. Une vraie construction CFI doit cacher la propriété dans la structure relationnelle (graphe, relations entre sommets), pas dans une coloration directe.
  3. **Lemme 1 mal formulé** : le « théorème de Dawar » invoqué (« GI ∈ P ⇒ CPT+C capture NP sur les hypercubes ») n'existe pas. La conjecture Blass-Gurevich correcte (`CPT+C = P`) reste ouverte ; tout résultat est *conditionnel* à cette conjecture, donc jamais inconditionnel pour P vs NP.
  4. **Condition (f) non satisfaite** : aveu explicite *« feuille de route »*, pas de contribution.

  À NE JAMAIS réessayer sous cette forme. **Nuance honnête** : la complexité descriptive (Immerman, Vardi, Gurevich, Dawar, Grohe) est un programme actif et prometteur, avec des avancées récentes sur graphes structurés. Mais elle ne peut pas être empruntée par l'encodage trivial de SAT comme coloration de l'hypercube — il faut une structure relationnelle non-triviale.

---

## 4. Questions ouvertes prioritaires

1. **Tout invariant proposé doit être explicitement invariant sous équivalence logique** des présentations du problème. *(Piste 3 a échoué là-dessus.)*
2. **Tout argument « tout algo P est contraint par X » doit démontrer que X survit aux sauts polynomiaux**, i.e. à l'extension `Hamming-1 → G_{n^c}`. *(Piste 3 a échoué là aussi.)*
3. **Tout argument « low-X pour TC⁰ » (low-rank, low-bond-dim, low-degree) doit d'abord exhiber un test positif sur IP_n**, où toutes ces quantités sont exponentielles. *(Piste 4 a échoué sur ce test.)*
4. **Toute piste doit apporter une contribution technique concrète**, pas seulement une stratégie globale ou un cadre à explorer. Pointer vers Williams 2011 ne suffit pas — il faut un sous-théorème prouvable, un calcul vérifiable, ou un ingrédient algorithmique nouveau. *(Pistes 4 et 5 ont échoué sur ce test.)*
5. **Tout argument « encoder un problème NP sous forme X et invoquer une obstruction sur X »** doit d'abord vérifier que la propriété d'intérêt n'est pas trivialement définissable dans le langage des outils utilisés. Sanity-check préalable au cadre. *(Piste 5 a échoué dessus : SAT comme coloration → trivialement FO-définissable.)*
6. **Toute conjecture topologique sur les circuits monotones doit être empiriquement testée sur les 168 fonctions monotones de `n = 4` avant publication**, faute de quoi des contre-exemples triviaux la réfutent. *(Piste 6 : 52 contre-exemples sur 168.)*
7. **L'invariant topologique « β_i(Δ_f) > 0 » est constructif et large** — il tombe sous Razborov-Rudich (preuves naturelles) si on prétendait en tirer une vraie borne inférieure. Tout invariant calculable en temps polynomial sur la table de vérité et vrai pour ≥ 2^{-n} des fonctions doit être traité comme suspect.
8. **Tout invariant algébrique conjecturé borner `D_m(f)` doit passer le test OR_n** : la fonction OR_n a `pd(I_{OR_n}) = n − 1`, `reg = 1`, Scarf défaut 0, mais `D_m = 1`. Tout invariant qui ne distingue pas ce cas extrême du cas générique est inutilement large.
9. **Le cadre formule monotone n'est pas suffisant pour P vs NP** : même un théorème inattaquable sur D_m (profondeur de formule monotone) ne donne pas de borne pour les **circuits** ou les **machines de Turing**, qui sont les objets de P vs NP. La sous-classe est trop restreinte.
10. **Tout théorème asymptotique revendiqué doit être vérifié empiriquement à n=4 ou n=5 avant soumission.** Le Lemme 4 du Tour 8 prétendait à un théorème *inconditionnel pour tout n*, et il aurait été réfuté en 30 secondes par énumération à n=3 ou n=4. *(Pattern persistant sur 8 tours.)*
11. **Question ouverte mathématique positive** : *quelle est la caractérisation exacte des fonctions monotones à résolution pure ?* Pas juste threshold (qui en est une sous-classe stricte), pas juste linéaire + principal (idée fausse), pas seulement « threshold à permutation près » (réfuté Tour 8 bis), mais quelque chose de structurel. Question intéressante en soi, indépendamment de P vs NP. **Donnée empirique acquise** : 95 fonctions sur 167 non-constantes monotones n=4 (cf. atlas tour 8). La caractérisation devra englober au minimum : OR_n, AND_n, MAJ_n, autres TH_t, sous-OR (fonctions linéaires sur k < n variables), sous-AND, paires d'arêtes disjointes (shifts non-consécutifs), et autres.
5. **Existe-t-il une obstruction non-locale et non-algébrique** qui survive aux sauts polynomiaux *et* à l'équivalence logique ? GCT (permanent vs déterminant) est la seule réponse sérieuse aujourd'hui, mais elle est au point mort depuis 2017 (Bürgisser-Ikenmeyer-Panova : pas d'obstruction par occurrences).
6. Côté complexité descriptive : la conjecture de Gurevich (logique capturant P) offre-t-elle un angle non-relativisant **et** non-algébrisant exploitable ?
7. Williams 2011 (NEXP ⊄ ACC⁰) reste l'unique précédent ayant franchi les trois barrières. La voie « algorithmic method + circuit lower bound » se généralise-t-elle à TC⁰ ? *(Question ouverte centrale de la complexité depuis 15 ans — invoquer cette voie n'est pas une piste, c'est rejoindre le front de la recherche.)*

---

## 5. Sous-but du tour courant

> Un seul objectif concret et, si possible, vérifiable.

- **Tour 21** : **Saut qualitatif obligatoire**. Tours 12-20 ont cartographié le paradigme AC⁰ d=2 bidirectionnellement (L19 pôle facile, L20 pôle défaut maximal). **Toute nouvelle famille dans ce paradigme sera rejetée d'office**. Les conditions (a)-(o) restent en vigueur, et une **16e** s'ajoute :

  - (p) **AJOUTÉE** : toute proposition restant dans le paradigme AC⁰ d=2 / DNF-minimization sans saut technique vers (a) profondeur 3, (b) formalisation Lean, ou (c) une nouvelle lignée méthodologique (Razborov monotone, communication complexity directe, etc.) sera **rejetée d'office** au titre de la saturation bidirectionnelle.

  Directions acceptables pour le Tour 21 (par accessibilité décroissante) :

  1. **Formalisation Lean** d'un sous-lemme acquis. Direction la plus accessible et productive (objet certifié dans Mathlib). Sous-lemmes candidats : L12.1 (PARITY ∉ AC⁰ d=2), L13 (caractérisation IS), L14.1 (MAJ), L15.1 (THRESHOLD), L16.1 (MOD_p), L18.A (classification IP), L19.A-B (essentialité), L20 (i)-(iv) (antipodales). **Recommandée comme direction principale.**

  2. **Démontrer L20.5** pour tout n : preuve structurelle que les seules fonctions à défaut maximal sont les antipodales. Question ouverte directe.

  3. **Démontrer la conjecture asymptotique de L19** : `|(α)/(β)| / 2^{2^n} → 0`. Argument combinatoire à construire.

  4. **Profondeur 3** : entrer dans FSS-Håstad. Significativement plus dur.

  5. **Razborov 1985 monotone CLIQUE** : nouvelle lignée distincte.

  **Direction interdite** : *toute* nouvelle caractérisation dans AC⁰ d=2 / DNF-MIN sans saut technique. Le Proposeur a livré 9 ÉTABLIS dans cette zone (Tours 12-20) — c'est suffisant. Le Tour 21 doit basculer en mode formalisation Lean ou tenter une vraie difficulté nouvelle.

  **Note méta** : après 20 tours, le dépôt a 8 objets ÉTABLIS, tous dans la même zone (AC⁰ d=2 cartographiée des deux pôles). **Continuer dans cette zone n'apportera plus rien**. Le Tour 21 est l'épreuve : soit produire un objet Lean certifié (consolidation utile), soit tenter un vrai saut (profondeur 3 ou Razborov), soit déclarer le travail achevé sur cette zone et basculer en mode formalisation.

---

## 6. Prochaine action

- [ ] Proposeur : générer une idée pour le sous-but ci-dessus (non-relativisante + classe restreinte)
- [ ] Réfuteur : attaquer l'idée, vérifier en priorité relativisation ET algébrisation
- [ ] Confronter à la littérature réelle (recherche web) : l'idée correspond-elle à une tentative déjà publiée/écartée ?
- [ ] Si « survit » : isoler un sous-lemme vérifiable / tenter une formalisation (Lean)
- [ ] Consigner le résultat (succès **ou** échec documenté) dans les sections 2 et 3
