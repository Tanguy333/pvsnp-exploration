# Note de synthèse — Le poids SYM∘AND des compositions de seuils (fil F-012..F-022)

> Consolidation NOTE-002, 2026-07-23. Le dossier « barreau 1 » : l'étude
> exécutable du verrou TC⁰ de la ligne 7 de l'Atlas, à l'échelle jouet.
> Tout énoncé est PROUVÉ (preuve dans cette note ou la consignation
> citée), MESURÉ (optimum solveur re-vérifié par énumération
> indépendante), ou OUVERT — jamais entre deux.

## 1. Le modèle

**Définition** (héritée de F-003). Pour f : {0,1}ⁿ → {0,1}, le *poids
SYM∘AND* W(f) est le minimum de Σ_S a_S sur les polynômes
p(z) = Σ_S a_S·m_S(z) à coefficients ENTIERS ≥ 0 sur les monômes
positifs non vides, tels que les ensembles de valeurs {p(z) : f=1} et
{p(z) : f=0} soient DISJOINTS (la porte symétrique lit p et décide).

**Provenance — TRANCHÉE le 2026-07-25 (tâche A-013).** *Une version de ce
paragraphe, écrite plus tôt le même jour, affirmait « ce n'est pas ce format ».
Elle était FAUSSE et est rétractée ici.* Le modèle ci-dessus **est** le format
SYM+ tel que Williams le définit — *Nonuniform ACC Circuit Lower Bounds*,
J. ACM 61(1), art. 2, 2014, p. 2:6 : « *a depth-two circuit which computes some
symmetric function at the output gate, and computes ANDs of input variables on
the second layer* », et p. 2:15 : « *We stress that the transformation from ACC
to SYM+ results in a circuit with no negated variables.* » Les négations sont
consommées **avant** l'apparition des ∧ du bas (annexe A, Transformation 1 :
les NOT deviennent des MOD_m). La contrainte « coefficients entiers ≥ 0 » n'est
pas non plus une restriction : un coefficient y est une **multiplicité de
portes ∧**, la réduction modulo p^k étant absorbée par la porte symétrique
(Williams 2014, annexe A ; Buss 2017 p. 15 ; Green-Köbler-Regan-Schwentick-
Torán, JCSS 50(3), 1995, cor. 6.4).

> **Donc W(f) = le nombre minimal de portes ∧ d'un circuit SYM∘AND à variables
> seules** — le format même qui alimente l'Evaluation Lemma de Williams.

Réserves qui subsistent, nommées : le **texte primaire** de Beigel-Tarui reste
illisible (PS 1995, polices bitmap) et ce que ses auteurs écrivent du format de
leurs ∧ demeure **[NON TROUVÉ]** ; la convention **à littéraux** existe aussi
dans la littérature (Williams l'atteste note 3 p. 2:6, et l'adopte lui-même en
Theory of Computing 14(17), 2018) — les deux sont inter-convertibles à taille
quasi-polynomiale préservée, **pas à nombre de portes** ; enfin les bornes
supérieures d'ici ne nourrissent l'algorithme que si la porte symétrique est
**évaluable rapidement**, ce que ce modèle n'exige pas. Écart de convention
mesuré sur THR_t(OR2^k) : k contre k(k+1), soit un facteur **k+1, croissant**.
Détail : [`../atlas/matrice_barrieres.md`](../atlas/matrice_barrieres.md)
ligne 7 et [`../tasks/done/A-013.md`](../tasks/done/A-013.md).

**Repères** : f symétrique ⟹ W ≤ n (p = Σz) ; encodage injectif ⟹
W ≤ 2ⁿ−1 ; p est toujours MONOTONE et supermodulaire (coefficients ≥ 0).

## 2. Les valeurs exactes (optima prouvés, re-vérifiés)

| f | n | W | structure de l'optimum |
|---|---|---|---|
| PARITY_4 | 4 | 4 | p = Σz (alternance serrée) |
| IP_8 | 8 | 4 | les 4 AND₂ appariés (loi k de F-003) |
| THR4 = [4z₁+3z₂+2z₃+z₄ ≥ 4] | 4 | 3 | couvert des 3 uns minimaux |
| GT2 (comparaison 2 bits, poids ±) | 4 | 7 | — |
| OR(THR4,THR4) | 8 | 6 | = 3+3, tranche SERRÉE |
| XOR(THR4,THR4) | 8 | 14 | = 7+7 = 2·\|ANF\|, miroir, 0 croisé |
| XOR(GT2,GT2) | 8 | 16 | = 8+8 = 2·\|ANF\|, miroir, 0 croisé |
| XOR(OR2,OR2) | 4 | 6 | = 3+3 = 2·\|ANF\| |
| XOR3(MAJ3³) | 9 | 9 | = 3×3 = 3·\|ANF\| |
| XOR3(OR2³) | 6 | 9 | = 3·\|ANF\| |
| XOR(THR4,GT2) | 8 | 15 | = 7+8 (ANF-additive asymétrique) |
| XOR(AND2,THR4) | 6 | 6 | < 8 : POSITIONNEL (réfute l'additivité) |
| AND(OR2,OR2) | 4 | 4 | couvert (4 uns minimaux) |
| MAJ3(OR2³) | 6 | 12 | couvert (12 paires croisées, unilatéral) |
| MAJ3(AND2³) | 6 | 3 | comptage d'indicateurs (3 monômes-blocs) |
| AND2(MAJ3²) | 6 | 6 | < 9 : HYBRIDE q = C(s,2) (impairs) |
| MAJ3(OR2³) vs MAJ3(MAJ3³) | 9 | ≤ 27 | incumbent re-vérifié, optimalité ouverte |

Fenêtres résiduelles : OR(GT2,GT2) ∈ [25, 32], AND(GT2,GT2) ∈ [21, 38]
(50 min CP-SAT avec coupes — dureté computationnelle consignée).

## 3. Les quatre théorèmes

**T1 (tranche, F-013).** Si f(z_A, 0) = g_A et f(0, z_B) = g_B (blocs
disjoints), alors W(f) ≥ W(g_A) + W(g_B). *Preuve* : p(·,0) sépare g_A
en n'utilisant que les monômes S ⊆ A ; masses disjointes ; croisés ≥ 0.
Serré pour OR-monotone (6 = 3+3) ; STRICT pour XOR (14 > 6) et OR de
comparaisons (≥ 21 > 14) — le combineur et la monotonie décident.

**T2 (comptage, F-018).** Un p à monômes positifs à valeurs dans {0,1}
est un monôme unique. *Preuve* : deux monômes S ≠ T donnent
p(1_{S∪T}) ≥ 2 ; un coefficient ≥ 2 donne p ≥ 2. — Seul AND a un
indicateur exact : la ligne de partage MOD/MAJ (l'arrêt de
Beigel-Tarui, ACC vs TC⁰) prouvée au niveau du modèle.

**T3 (alternance, F-020).** W(f) ≥ alt(f), le nombre maximal
d'alternances de f le long d'une chaîne croissante du cube. *Preuve* :
p est monotone ; à chaque alternance la séparation force une
croissance stricte ; W ≥ p(1ⁿ) ≥ alt. **Attribution** : alt(f) est la
« decrease » d(f) de **Markov 1957** (complexité d'inversion :
⌈log₂(d(f)+1)⌉ portes NOT) — quantité classique, usage nouveau dans ce
modèle. SERRÉ sur PARITY_n (n) et IP_2k (k) — la loi IP de F-003
redémontrée en 3 lignes.

**T4 (fenêtre ANF, F-019).** Pour poids {1..k} et tout seuil
2 ≤ t ≤ k+1, la sparsité ANF de [Σ poids choisis ≥ t] vaut exactement
2^{k−1}−1. *Preuve* : induction de Shannon sur la variable de poids k ;
cas 2 ≤ t ≤ k : la branche haute est constante 1 (ANF = {∅}, ∅ ∉ S(g₀))
d'où N(k,t) = 2N(k−1,t)+1 ; cas t = k+1 : la branche haute est
OR_{k−1} (ANF = TOUS les non-vides) et le compte télescope SANS
hypothèse. Vérifié mécaniquement au niveau des ensembles (k ≤ 12).
Réduction utile : le coefficient ANF en A est la parité de
#{U ⊆ A : Σ(U) < t} (complémentation mod 2).

## 4. Les deux constructions prouvées (et leurs régimes de serrage)

**C1 (parité/ANF, F-016).** a_S = ANF_S(g) par bloc ⟹ p ≡ ⊕g_i mod 2 :
W(XOR de blocs) ≤ Σ\|ANF(g_i)\|. SERRÉE sur 6 optima fermés (blocs
équilibrés) ; les supports optimaux coïncident MONÔME POUR MONÔME avec
les ANF. Avec T4 : **W(XOR_j(THRW_m)) ≤ j(2^{m−1}−1) — la route parité
est EXACTEMENT exponentielle en la taille de bloc** : quasi-poly pour
blocs polylog (le régime ACC de Beigel-Tarui), morte pour blocs
polynomiaux (le régime TC⁰). Le mur de la ligne 7, quantifié et
démontré par en bas.

**C2 (couvert unilatéral, F-021).** Pour f monotone : support = monômes
S avec f(1_S) = 1 couvrant les uns minimaux, coefficients 1 ; poids =
#uns minimaux (chaque un minimal exige son propre support — tout
sous-monôme-un contredirait sa minimalité). Donc W(f) ≤ #implicants
premiers = DNF_min(f). SERRÉE sur MAJ₃(OR2³) = 12, AND(OR2²) = 4,
OR(THR4²) = 6, THR4 = 3.

## 5. Les trois réfutations et le zoo (F-016, F-022)

1. **Injectivité** (un bloc quasi-injectif nécessaire pour XOR) :
   morte 2× — les optima 14 et 16 sont ANF-additifs sans croisés.
2. **Additivité ANF universelle** : XOR(AND2,THR4) = 6 < 8 — mécanisme
   POSITIONNEL (séparateur unilatéral de THR4 poids 3 + monôme AND
   scalé ×3) ; bloqué pour GT2 (unilatéral positif ⟹ monotone, or
   GT2(1111) = 0) — d'où la parité optimale côté GT.
3. **Invariant unique du comptage** (« W = DNF_min pour compositions
   monotones ») : morte 3× — (a) MAJ₅ singletons : 5 < 10 (comptage
   symétrique) ; (b) MAJ₅(AND2⁵) ≤ 5 < 10, RIGOUREUX par construction
   (l'exception de T2) ; (c) **AND2(MAJ3²) = 6 < 9, blocs non-AND —
   l'HYBRIDE : q = C(s,2) unilatéral à valeurs IMPAIRES {1,3}, somme
   de deux impairs = paire (positivité × parité)**.

**Verdict** : W = min d'un zoo d'au moins QUATRE mécanismes (couvert,
parité, positionnel, comptage d'indicateurs, hybrides) — aucun
invariant unique. La dureté de l'outil de borne inférieure du comptage
est DÉMONTRÉE par la diversité des optima, plus seulement pressentie.
C'est l'écho jouet le plus fidèle du verrou TC⁰ : ce qui manque à la
méthode algorithmique pour TC⁰ est un argument dominant cette
prolifération de régimes.

## 6. L'asymptotique (état honnête)

- **Régime parité : CLOS et prouvé des deux côtés** (C1 + T3 + T4).
- **Régime comptage : le mur commence à n = 9** (MAJ₃(MAJ3³) indécis
  en solveur) ; meilleurs outils de borne inf : facteur ×4 sous la
  vérité dès k = 3. Problème ouvert bien posé : W(MAJ_k(g^k)) ≫ k·W(g)
  pour g non-AND — l'estimée qui manque, hors boucle.
- \|ANF(MAJ_m)\| : **caractérisation digitale EXACTE établie**
  (dérivation 3 lignes + vérification contre zêta, m ≤ 16) : le
  coefficient ANF au degré d vaut la parité de Σ_{k<t} C(d,k) (Lucas),
  d'où \|ANF(MAJ_m)\| = Σ C(m,d) sur les d à compte impair de
  sous-masques sous le seuil. Deux sous-lois vérifiées : **m = 2^k+1 ⟹
  \|ANF\| = 2^{m−1}−1** (m = 3, 5, 9, 17) ; **paires égales
  \|ANF(MAJ_m)\| = \|ANF(MAJ_{m+1})\| pour m ≡ 2 mod 4** (5/5).
  Suite (3, 3, 7, 15, 35, 35, 71, 255, 627, …) **ABSENTE de l'OEIS**
  (API, 2 fenêtres) : candidate à soumission avec la formule.

## 7. Antériorité (réserves honnêtes)

Le modèle (poids L1 à séparation par valeurs) est house-made (F-003) ;
la mesure standard de la littérature SYM∘AND est le nombre de portes
(quasi-poly, Beigel-Tarui). alt = decrease de Markov 1957 (attribué).
T4 (seuils en escalier) : recherche à 2 passes, rien trouvé ; l'ANF de
MAJ est en littérature (Méaux 2019) — non refait. Les théorèmes T1-T4
dans CE modèle semblent neufs, SANS garantie — une relecture experte
trancherait avant toute diffusion.

## 8. Ingénierie (leçons consignées)

CP-SAT (OR-Tools) domine CBC d'un ordre de grandeur sur les
diségalités natives (IP_8 : 7 s vs 59 s ; XOR(THR4²) fermé en 26 s là
où CBC ne trouvait AUCUN incumbent en 9 min). Recette gagnante : hint
COMPLET + plafond + cassage de symétrie bloc-miroir + coupes de
tranche prouvées. **Re-vérification par énumération indépendante
OBLIGATOIRE** (incident F-016, attrapé par l'utilisateur). Deux autres
incidents consignés (budget tl, filtre par sous-chaîne).

## 9. Distance à P vs NP (le rappel permanent)

Échelle jouet (n ≤ 10), zéro asymptotique du comptage. La chaîne vers
P ≠ NP garde tous ses maillons manquants (asymptotique → transformation
TC⁰ → NEXP ⊄ TC⁰ → …). La valeur du fil est cartographique : le pied
du mur TC⁰ transformé en théorèmes, témoins exécutables et un problème
ouvert précis — la mission du dépôt, ni plus ni moins.
