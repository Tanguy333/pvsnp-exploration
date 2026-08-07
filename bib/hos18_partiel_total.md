# MC-004 — Audit du gabarit partiel → total de Hirahara-Oliveira-Santhanam (CCC 2018) et son transfert à MinSYM+

> Tâche type A, exécutée le 2026-08-07. Source PRIMAIRE, lue sur texte
> intégral : S. Hirahara, I. C. Oliveira, R. Santhanam, « NP-hardness of
> Minimum Circuit Size Problem for OR-AND-MOD Circuits », CCC 2018, LIPIcs
> 102, art. 5, 31 p. — PDF officiel DROPS téléchargé
> (`bib/pdf/hos18_ccc2018.pdf`, gitignoré), texte extrait et versionné
> (`bib/pdf/hos18_ccc2018_texte.txt`, 31 pages). Les numéros de ligne
> ci-dessous renvoient à ce fichier texte. Objet : la question laissée par
> MC-002 §3.3 — le pipeline Th.8 → Th.16 → Th.24 transfère-t-il à la tête
> SYM pondérée (MinSYM+) ?

## 1. Le pipeline HOS18, sur texte

### 1.1 Th.8 — dureté de la variante partielle, ET la compression

« *(DNF◦MODm)-MCSP∗ is NP-hard under (zero-error) randomized polynomial-time
many-one reductions* » (l. 492-493). Mécanisme (l. 497-524) : instance de
r-Bounded Set Cover sur [n] → chaque élément i devient un point ALÉATOIRE
v_i ∈ Z_m^t ; chaque ensemble S devient le sous-espace linéaire span(v_S) ;
f := 1 sur les v_i, 0 hors de ∪_S span(v_S), ∗ ailleurs. **La compression
est ALGÉBRIQUE** : t est choisi tel que m^t = (nm)^{O(r)} (Claim 10,
l. 557) — la table est polynomiale parce que la structure d'appartenance
« élément ∈ ensemble » est réalisée par l'algèbre linéaire de la couche
MOD_m du bas (un terme AND∘MOD accepte exactement un sous-espace affine),
PAS par la combinatoire booléenne. Un terme couvrant plusieurs v_i force
(avec forte probabilité) un ensemble légal — à facteur 2 près (affine vs
linéaire, l. 536-550), d'où le recours à l'inapproximabilité de Set Cover
(facteur 2, Th.5/Feige).

### 1.2 Th.16 — la totalisation, à coût additif exact

« *There is a (zero-error) randomized polynomial-time many-one reduction
from (DNF◦MODm)-MCSP∗ to (DNF◦MODm)-MCSP* » (l. 797-798). Construction
(l. 799-836) : s := ⌈4(t+1)log m + 2⌉ coordonnées fraîches y ;
g(x, y) := f(x) si f(x) ∈ {0,1} et y = 0^s ; 1 si f(x) = ∗ et y ∈ L_x
(sous-espace linéaire ALÉATOIRE de dimension r := t+2 dans la fibre) ;
0 sinon. Résultat exact (l. 1001-1002) : « *DNFMODm(g) = DNFMODm(f) +
|f⁻¹(∗)|* » pour une collection « scattered ».

Les quatre pièces de la preuve, chacune avec son ingrédient spécifique :

1. **Claim 17 (≤, le gating)** : C′ := ⋁_k (C_k(x) ∧ (y₁=0) ∧ … ∧ (y_s=0))
   ∨ ⋁_{x*} C_{x*} (l. 850-859) — chaque terme original est CONFINÉ à la
   tranche y = 0 par conjonction locale. *Ingrédient : la couche du bas
   sait tester y = 0, et la tête OR compose sans interaction.*
2. **Def. 18 + Claim 19 (scattered)** : |L_x| = m^r et L_x \ L_x′ = {0^s}
   deux à deux ; probabilité ≥ 1/2 dès s ≥ (2r+2t)log m + 2 (l. 863-921) ;
   **vérifiable en temps polynomial** (l. 922-925) — d'où le zero-error :
   on retire jusqu'à obtenir une collection scattered.
3. **Claims 21-22 (l'extraction)** : dans un circuit optimal pour g, le
   terme l(x) qui couvre la plus grande fraction de {x}×L_x est INJECTIF en
   x (Claim 21) et ne couvre aucun (x, 0^s) avec f(x) = 1 (Claim 22) — les
   deux par le même coup : trois points d'un sous-espace affine donnent le
   quatrième, (x₁,a) − (x₁,b) + (x₂,c) ∈ C_k⁻¹(1) (l. 977-1000), et la
   dispersion (scattered) produit la contradiction. *Ingrédient : la
   structure AFFINE des termes.*
4. **Claim 20 (≥, l'ablation)** : retirer les |f⁻¹(∗)| termes l(x) et
   restreindre les autres à y = 0 donne un circuit pour f à K − |f⁻¹(∗)|
   termes (l. 954-969). *Ingrédient : la tête OR — retirer des termes ne
   change pas la valeur des points encore couverts.*

### 1.3 Th.23-24 — dérandomisation ; et les deux bonus

- PRG « quick » à graine logarithmique contre AND∘MOD_m de taille
  arbitraire (Th.23, l. 1042-1046) : les sous-conditions de « nice /
  scattered » sont elles-mêmes testables par AND∘MOD_m, donc le PRG
  dérandomise les réductions → NP-dureté DÉTERMINISTE (Th.24, l. 1059).
- **Appendice B (l. 1720-1813)** : le pipeline refait pour la mesure
  « nombre TOTAL de portes » — possible parce que le coût par terme est
  exactement caractérisable (Lemma 42 : 1 + codim(A), l. 1734-1746) et
  ADDITIF sur les termes (taille = 1 + K + Σ codim, l. 1747-1753). Perte :
  approximation facteur 8 au lieu de 2 (l. 1804-1813).
- **Théorème 45 (l. 1824-1843)** : totalisation PRÉSERVANT l'approximation
  par AMPLIFICATION — g′(x,z,w) := f(x) si z ∈ f⁻¹(∗) et w ∈ L_z, 0 sinon,
  donne « *DNFMODm(g′) = |f⁻¹(∗)| · DNFMODm(f)* » : |f⁻¹(∗)| copies de f à
  sélecteurs scattered, coût MULTIPLICATIF exact. C'est le lemme de
  multiplicativité du modèle OR.

### 1.4 La mise en garde des auteurs eux-mêmes (l. 1006-1029)

Sur l'encodage binaire de Z_m (m > 2) : « *a binary encoding allows a
bottom-layer modular gate to access individual bits of this encoding […]
When this is the case, our argument no longer works* » ; « *when m > 2 our
techniques do not seem to be directly applicable to functions defined over
boolean inputs only* ». La machinerie est donc fragile HORS de son algèbre
native — aveu utile : le transfert à une autre couche basse n'est pas un
détail.

## 2. Le transfert à MinSYM+ : quatre points de rupture, trois acquis

Rappel du modèle cible : W(f) = min Σ a_S, monômes POSITIFS, la tête
symétrique lit p(x) = Σ_{S⊆supp(x)} a_S, ensembles de valeurs disjoints.

### 2.1 Les ruptures, pièce par pièce de la preuve

1. **Le gating (Claim 17) s'inverse mais survit** — voir acquis (i)
   ci-dessous. Ce qui NE survit PAS est sa réciproque implicite : rien ne
   force un séparateur optimal de g à respecter la partition
   tranche/fibres — un monôme non étiqueté contribue à p sur TOUTES les
   tranches au-dessus de lui. C'est le verrou (c) de F-022 (contrôle du
   mécanisme gagnant), que MC-003 vient de mesurer en régime antichaîne :
   les optima ignorent la structure prévue par le constructeur.
2. **L'extraction (Claims 20-22) n'a aucun analogue** : elle repose sur
   (a) la structure affine des termes — nos up-cubes n'ont pas de clôture
   affine — et (b) l'ablation OR — retirer un monôme de p change la valeur
   de TOUS les points au-dessus de S, donc potentiellement la classe de
   valeurs de chaque point. Il n'existe aujourd'hui AUCUN lemme « retirer
   la machinerie des fibres coûte exactement son poids » pour W.
3. **L'exactitude additive (W(g) = W(f) + coût des fibres)** est
   précisément une forme du **trou (b) de MC-001** (additivité de W sous
   structures disjointes) — non établi même pour la somme directe à
   variables disjointes. Le Th.45 (multiplicativité) montre à quoi le lemme
   devrait ressembler ; le modèle OR l'obtient par décomposition de la
   tête, ce que la tête symétrique interdit par construction.
4. **La compression (Th.8) est inapplicable** : elle est algébrique (couche
   MOD_m) ; SYM+ n'a pas de couche du bas expressive — et notre Th.1
   (effondrement monotone) interdit de la remplacer par de la couverture
   booléenne sur fonctions totales. MAIS ce point est le moins grave :
   pour la variante PARTIELLE, la compression est déjà acquise par
   HÉRITAGE — Th.3(i) (rails doubles) donne la NP-complétude de la
   variante prescrite-unilatérale-∗ sur TABLES de taille polynomiale
   (Masek produit n = O(log N)).

### 2.2 Les acquis (ce que l'audit rapporte de positif)

1. **Slice-gating gratuit pour SYM+** [OBSERVATION de cet audit, une
   ligne] : étiqueter un monôme S par l'ensemble Y des s variables
   fraîches (S ∪ Y) le rend actif EXACTEMENT sur la tranche y = 1^s
   (Y ⊆ supp(y) ⟺ y = 1^s), et le poids ne change pas (le coefficient est
   le même). L'inverse du gating HOS18 (leur tranche est y = 0, la nôtre
   y = 1^s), au même coût nul. Pièce neuve utilisable par toute future
   construction.
2. **La convergence des deux voies restantes** — le résultat principal de
   l'audit : la totalisation à la Th.16 pour SYM+ SE RÉDUIT à un lemme
   d'extraction/additivité pour W (points 2-3 ci-dessus). Autrement dit,
   les deux voies laissées en lice par MC-003 (« gabarit Th.16 » et
   « additivité de W ») ne sont PAS indépendantes : **la première passe
   par la seconde**. Le front MC se concentre donc sur UNE question
   mathématique : l'additivité (ou super-additivité contrôlée) de W sous
   structures disjointes/étiquetées — et elle est testable à l'échelle de
   nos instruments (formuler les variantes : somme directe à variables
   disjointes, fibres à sélecteurs, produit ∧).
3. **Deux patrons réutilisables** : le zero-error par structures aléatoires
   poly-vérifiables (indépendant du modèle — seule la structure change) ;
   et le cahier des charges d'un lemme d'amplification (Th.45) si
   l'additivité simple s'avérait fausse mais une multiplicativité
   accessible.

## 3. Verdict

**Le gabarit HOS18 ne transfère PAS en l'état** : chacune de ses quatre
pièces (gating-réciproque, extraction, additivité de coût, compression)
repose sur la localité de la tête OR ou sur l'algèbre de la couche MOD_m,
et chaque tentative de transfert retombe sur l'un des deux verrous déjà
nommés du front — contrôle du mécanisme (c) et additivité (b). Mais l'audit
transforme le paysage : **les deux voies survivantes convergent en une
seule question bien posée (l'additivité de W), munie d'un acquis de
construction (slice-gating gratuit) et de deux patrons de preuve.** La
prochaine tâche du front est donc la formalisation et le test de
l'additivité — et c'est la 5ᵉ tâche du fil MC : le bilan écrit de la
règle 9 y est obligatoire.

## Réserves

- Lecture unique par la session (pas de seconde lecture indépendante) ;
  les verbatims sont vérifiables dans `bib/pdf/hos18_ccc2018_texte.txt`
  (extraction pypdf du PDF officiel DROPS — la mise en page des formules
  est dégradée par l'extraction, les énoncés cités ont été relus en
  contexte).
- L'« observation slice-gating » est élémentaire — aucune revendication de
  nouveauté ; sa valeur est d'usage.
- La réduction « Th.16-pour-SYM+ ⟸ additivité » est une analyse
  d'obstruction (chaque pièce de leur preuve exige X, X manque), pas un
  théorème d'équivalence : une route de totalisation N'UTILISANT PAS le
  schéma fibres-à-coût-exact n'est pas exclue.
