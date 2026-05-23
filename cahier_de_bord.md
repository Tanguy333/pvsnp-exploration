# Cahier de bord — Exploration P vs NP

> Document vivant. À joindre en contexte à **chaque** tour, pour le Proposeur comme pour le Réfuteur.
> Règle d'or : on ne réexplore jamais une impasse déjà documentée. On mesure le progrès par la compréhension accumulée, pas par « a-t-on la preuve ».

---

## 0. Méta

- **Question** : tout problème dont une solution candidate est vérifiable en temps polynomial est-il aussi résoluble en temps polynomial ? (P vs NP)
- **Direction choisie** : séparation **P ≠ NP**, via une classe restreinte à structure algébrique/géométrique ; cadre principal = complexité descriptive, ouverture GCT ; outils encouragés = méta-complexité / Kolmogorov.
- **Démarré le** : 2026-05-23
- **Dernière mise à jour** : 2026-05-23 (fin tour 6)
- **Nombre de tours effectués** : 6

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
| 7 |  |  |  | *(à venir)* |

---

## 3. Lemmes et résultats

### ✅ Établis (vérifiés / démontrés rigoureusement)
- *(aucun pour l'instant)*

### ❓ Conjecturaux (plausibles mais non prouvés)
- *(aucun retenu pour l'instant)*

### ⚠️ Lacunes réparables (direction légitime mais énoncé spécifique faux)

- **Piste 6 — « Gap homologique sémantique sur Stanley-Reisner ».** Première piste à ne PAS être en faille fatale. Direction correcte (topologie sémantique pour fonctions monotones, lignée Razborov 1985 / Knill-Forman / Björner-Wachs / Reiner-Welker), mais énoncé du Proposeur faux :
  - **Lemme 2 réfuté empiriquement** (cf. [`checks/tour_06_stanley_reisner.py`](checks/tour_06_stanley_reisner.py)) : sur les 168 fonctions monotones de `n = 4`, **52 ont `β_1(Δ_f) > 0`**, et **les 52 violent** la borne « taille > #faces maximales ». Contre-exemple canonique : `f = (x_0 ∧ x_2) ∨ (x_1 ∧ x_3)`, dont `Δ_f` est le complexe de drapeau du 4-cycle C_4 (β_1 = 1), mais taille de circuit = 2 < 4 = #faces maximales.
  - **Lemme 1 imprécis** : confond le complexe `Δ_f` avec l'**idéal** `I_{Δ_f}` (engendré par les non-faces minimales). Les implicants premiers sont les générateurs de l'idéal, *pas* des faces de Δ_f. Reformulé correctement, L1 devient une tautologie définitionnelle.
  - **(f) non satisfaite** : calcul promis (« je m'engage à concevoir un script SageMath ») non livré ; je l'ai effectué à la place, et il a réfuté la conjecture sous-jacente.
  - **Signe d'alarme RR** : l'invariant `β_i` est calculable en temps polynomial sur la table de vérité (constructif), et `β_1 > 0` est large (31 % à n=4). Si la borne marchait, elle serait *naturelle* au sens de Razborov-Rudich, donc condamnée par les preuves naturelles sous crypto standard.

  Pour réparer : reformuler en termes d'idéal de Stanley-Reisner et invoquer des invariants algébriques plus fins (régularité de Castelnuovo-Mumford, profondeur projective, Betti gradués / formule de Hochster). Mais alors la piste sort du cadre « calcul exhaustif sur n=5 » et entre dans l'algèbre commutative computationnelle — direction active mais bien plus difficile. La lacune est précise (énoncé à raffiner) mais sa réparation déplace hors du sous-but Tour 6.

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
5. **Existe-t-il une obstruction non-locale et non-algébrique** qui survive aux sauts polynomiaux *et* à l'équivalence logique ? GCT (permanent vs déterminant) est la seule réponse sérieuse aujourd'hui, mais elle est au point mort depuis 2017 (Bürgisser-Ikenmeyer-Panova : pas d'obstruction par occurrences).
6. Côté complexité descriptive : la conjecture de Gurevich (logique capturant P) offre-t-elle un angle non-relativisant **et** non-algébrisant exploitable ?
7. Williams 2011 (NEXP ⊄ ACC⁰) reste l'unique précédent ayant franchi les trois barrières. La voie « algorithmic method + circuit lower bound » se généralise-t-elle à TC⁰ ? *(Question ouverte centrale de la complexité depuis 15 ans — invoquer cette voie n'est pas une piste, c'est rejoindre le front de la recherche.)*

---

## 5. Sous-but du tour courant

> Un seul objectif concret et, si possible, vérifiable.

- **Tour 7** : les 7 conditions du Tour 6 restent en vigueur. Une **8ème condition** s'ajoute :
  - (h) **Le calcul vérificateur doit être effectivement exécuté par le Proposeur** avant soumission, avec résultat numérique livré dans la proposition. Pas de promesse (« je m'engage à concevoir le script ») — un résultat. Sinon le Réfuteur effectue le travail à sa place et réfute trivialement la conjecture.

  Le Tour 6 a montré que la direction (topologie/algèbre commutative pour fonctions monotones) est légitime ; mais la formulation spécifique tombait sur des contre-exemples triviaux que le Proposeur aurait identifiés en exécutant ses propres scripts. C'est un gain d'efficacité majeur pour la boucle.

  Conseil de direction : continuer dans la veine du Tour 6 (micro-progrès vérifiable sur classe ultra-restreinte) mais en garantissant la livraison du calcul. Alternativement, viser une **formalisation Lean** d'un sous-lemme déjà connu (e.g. théorème de hiérarchie de temps), pour produire au moins un objet certifié, même non original.

---

## 6. Prochaine action

- [ ] Proposeur : générer une idée pour le sous-but ci-dessus (non-relativisante + classe restreinte)
- [ ] Réfuteur : attaquer l'idée, vérifier en priorité relativisation ET algébrisation
- [ ] Confronter à la littérature réelle (recherche web) : l'idée correspond-elle à une tentative déjà publiée/écartée ?
- [ ] Si « survit » : isoler un sous-lemme vérifiable / tenter une formalisation (Lean)
- [ ] Consigner le résultat (succès **ou** échec documenté) dans les sections 2 et 3
