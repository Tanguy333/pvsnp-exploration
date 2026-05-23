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
- **Dernière mise à jour** : 2026-05-23 (fin tour 13 — deuxième théorème ÉTABLI pour P vs NP)
- **Nombre de tours effectués** : 13

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
| 14 |  |  |  | *(à venir)* |

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

- **Tour 14** : direction **ouverte** après l'établissement des Tours 12 et 13. Le dépôt a maintenant **deux objets ✅ Établis pour P vs NP**. Les directions possibles restent les mêmes qu'avant le Tour 13 :

  1. **Cross-validation à n = 5** : énumérer les `2^{2^5}` ≈ 4 milliards de fonctions est infaisable, mais l'énumération des independent sets de `Q_5` (= 254 475 par référence ; vérifiable directement) avec la distribution par taille consoliderait le théorème. Plus complexe que n=4 mais accessible.

  2. **Extension à profondeur 3** : entrer dans le territoire Furst-Saxe-Sipser / Håstad. Beaucoup plus dur — le nombre de circuits AC⁰ profondeur 3 sur n=4 explose, et l'argument simple « variable libre → flip change parity » ne suffit plus. Significativement plus ambitieux.

  3. **Formalisation Lean** des L12.1–L13.4 dans un fichier Mathlib4. Premier théorème de complexité formalisé du dépôt.

  Toutes les 12 conditions (a)–(l) restent en vigueur. Les Tours 12 et 13 montrent que le Proposeur peut les honorer simultanément ; cela doit être maintenu.

  **Toute proposition s'écartant de la direction P vs NP** (algèbre commutative décorrelée, raffinements de C9, etc.) sera rejetée d'office au titre de (i).
  **Toute conjecture-pont non vérifiée** sera rejetée au titre de (j).
  **Toute erreur factuelle élémentaire** sera rejetée au titre de la rigueur attendue.

  **Note (suite à l'erreur OEIS Tour 13)** : toute référence externe (OEIS, théorème nommé, séquence) doit être vérifiée avant citation. Citer A006506 pour les independent sets de Q_n est une erreur référentielle qui n'affecte pas le théorème mais nuit à la crédibilité. À éviter à l'avenir.

---

## 6. Prochaine action

- [ ] Proposeur : générer une idée pour le sous-but ci-dessus (non-relativisante + classe restreinte)
- [ ] Réfuteur : attaquer l'idée, vérifier en priorité relativisation ET algébrisation
- [ ] Confronter à la littérature réelle (recherche web) : l'idée correspond-elle à une tentative déjà publiée/écartée ?
- [ ] Si « survit » : isoler un sous-lemme vérifiable / tenter une formalisation (Lean)
- [ ] Consigner le résultat (succès **ou** échec documenté) dans les sections 2 et 3
