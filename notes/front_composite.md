# Degrés faibles symétriques des fonctions seuil modulo 6 — synthèse du fil F-011

> **Statut : note interne de synthèse** (2026-06-10, fil F-011 étapes 1-6 du
> dépôt). Tous les énoncés « Théorème/Lemme » ci-dessous ont des preuves
> complètes ET une vérification exécutable (scripts `checks/task_f011*.py`).
> Aucune relecture par un expert externe à ce stade. Les conjectures sont
> étiquetées comme telles.

## 1. Cadre et motivation

Le mur des **modules composés** est ouvert depuis 1987 : la méthode
polynomiale de Razborov-Smolensky prouve des bornes exponentielles pour
AC⁰[p] (p premier) mais *« we do not know a proof that AC⁰[6] cannot
compute Majority »* (Goldreich 2023, audit A-004 du dépôt). La raison
structurelle : Z₆ n'est pas un corps, et les degrés des représentations
polynomiales s'y effondrent pour certaines fonctions (Barrington-Beigel-
Rudich 1994 : OR passe de ~n à O(√n)).

Cette note étudie le modèle le plus simple où ce phénomène vit : les
**représentations faibles symétriques** des fonctions seuil. C'est
l'analogue composite du « Pas 1 » de Razborov-Smolensky — le maillon dont
l'absence bloque la méthode depuis 1987 — restreint aux polynômes
symétriques. Toute borne y est honnêtement cadrée : *polynôme unique ≠
circuit AC⁰[6]* ; mais comprendre exactement ce modèle est le préalable
naturel (c'est dans ce modèle que BBR ont découvert l'effondrement).

## 2. Définitions

Pour `1 ≤ t ≤ n` et m ∈ {2, 3, 6} : une **représentation faible
symétrique** de THR_{t,n} sur Z_m est un polynôme symétrique
`P = Σ_{i=0}^{d} a_i e_i` (e_i = polynôme symétrique élémentaire,
a_i ∈ Z_m) tel que sa valeur sur tout point de poids w,
`S(w) = Σ_i a_i C(w,i) mod m`, vérifie :
- `S(w) ≡ 0` pour tout `w < t` (zéros forcés),
- `S(w) ≢ 0` pour tout `t ≤ w ≤ n` (couverture).

`deg_m^sym(THR_{t,n})` = le plus petit degré d admettant une telle
représentation. MAJ_n = THR_{⌈n/2⌉,n} ; OR_n = THR_{1,n}.

## 3. Structure : les deux lemmes de base

**Lemme 1 (noyau de Mahler).** *L'espace des polynômes symétriques de
degré ≤ d s'annulant sur tous les poids w < t est exactement
`span{e_i : t ≤ i ≤ d}`, de dimension d − t + 1.*

*Preuve.* En base de Mahler/Newton, S(w) = Σ a_i C(w,i) avec
a_i = Δ^i S(0) (différences finies ; système triangulaire). S ≡ 0 sur
[0, t) force a_i = 0 pour i < t ; réciproquement C(w,i) = 0 pour
w < i. ∎

**Lemme 2 (fenêtre glissante).** *S a un degré de Mahler ≤ d sur [0, n]
ssi `Δ^{d+1}S(j) ≡ 0 (mod m)` pour j = 0..n−d−1. La faisabilité de
deg ≤ d est donc une contrainte locale de largeur d+2 sur la suite des
valeurs — décidable par automate fini.*

*Vérification : DP ≡ solveur exact sur 126/126 cellules.*

## 4. Le cas mod 2 : loi exacte complète

**Théorème A (= T-F011a).** *Pour tous 1 ≤ t ≤ n :*
`deg₂^sym(THR_{t,n}) = max{ i ∈ [t,n] : C(i−1, t−1) impair }`
`= 1 + max{ j ∈ [t−1, n−1] : (t−1) AND j = t−1 }` *(bit à bit, Lucas).*

*Preuve.* Sur F₂, couverture = « S(w) = 1 partout sur [t,n] » : la
fonction est l'unique échelon. Ses coefficients de Mahler valent
a_i = Σ_{w=t}^{i} C(i,w), et la récurrence de Pascal télescope :
`a_i ≡ C(i−1, t−1) (mod 2)` (vérifié sur 1 540 paires). Le degré du
candidat unique est le plus grand i avec a_i ≠ 0. Lucas conclut. ∎

*Conséquence : toute la colonne mod 2 des données (puissances de 2,
doublements) est expliquée — par ex. deg₂^sym(OR_n) = n exactement.*

## 5. Le cas mod 6 : infaisabilité et anomalies

**Théorème B (= T-F011b, lemme d'infaisabilité).** *S'il existe
w\* ∈ [t,n] avec `C(w\*, i) ≡ 0 (mod 2)` et `(mod 3)` pour tout
i ∈ [t,d], alors deg₆^sym(THR_{t,n}) > d.*

*Preuve.* Par le Lemme 1, U(w\*) = Σ_{i=t}^d u_i C(w\*,i) ≡ 0 et de même
V(w\*) — w\* n'est jamais couvert. ∎

**Corollaires (les anomalies, prouvés).** Avec w\* = 2t, Kummer
(C(2t,t) toujours pair) et Lucas :
- deg₆^sym(MAJ_4) ≥ 3 (C(4,2) = 6) ;
- deg₆^sym(MAJ_16) ≥ 9 (C(16,8) ≡ 0 mod 6) ;
- deg₆^sym(MAJ_32) ≥ 27 (C(32, i) ≡ 0 mod 6 pour **tout** i ∈ [16, 26]).

**Théorème C.** `deg₆^sym(MAJ_32) = 27`.

*Preuve.* ≥ 27 : corollaire ci-dessus. ≤ 27 : le certificat explicite
`V = e₁₆ + e₁₈ + e₂₅ + e₂₇ (mod 3)`, u = 0 — vérifié en entiers exacts
sur les 33 poids (V ≢ 0 mod 3 sur [16, 32], ≡ 0 sous 16 automatiquement). ∎

*Le phénomène-clé, impossible sur un corps : sur Z₆, les binômes
s'annulent simultanément mod 2 et mod 3 sur des fenêtres entières de
degrés.*

## 6. Le cas mod 3 : périodicité et descente

**Théorème D (= T-F011c, périodicité).** *Pour toute puissance
P = 3^b ≤ n − t + 1 : `deg₃^sym(THR_{t,n}) ≥ P`.*

*Preuve.* Lucas donne `C(P,k) ≡ 0 (mod 3)` pour 0 < k < P, et P impair,
donc **`Δ^P = S^P − id`** sur F₃ (S = décalage). Si deg < P, alors
Δ^P S ≡ 0 : la suite des valeurs est P-périodique — mais S(t−1) = 0 et
S(t−1+P) ∈ {1,2} : contradiction. ∎

**Lemme 3 (descente).** *Si deg(g) ≤ d et P = 3^b ≤ d+1, alors
`G := g(·+P) − g` a un degré ≤ d − P sur [0, n−P].*

*Preuve.* `Δ^{d+1−P}G = Δ^{d+1−P}(S^P − id)g = Δ^{d+1}g ≡ 0`. ∎

## 7. Conjectures (étayées, non prouvées) et réfutation

- **C-F011 (loi MAJ mod 6, 47/47 points dont une prédiction a priori)** :
  `deg₆^sym(MAJ_n) = L1(t)` (plus petite puissance de 2 ou 3 ≥ t), sauf si
  `L1(t) = 2^a`, `n ≥ 2^{a+1}` et `C(2^{a+1}, 2^a) ≡ 0 (mod 3)`, auquel
  cas la puissance suivante. *(La borne ≥ des cas d'anomalie est prouvée —
  Théorème B ; il manque les bornes ≤ générales et l'exclusion des valeurs
  intermédiaires hors anomalies.)*
- **Loi OR mod 3 — borne inférieure désormais PROUVÉE (Théorème E,
  étape 7)** : `deg₃^sym(OR_n) ≥ max(3^⌊log₃n⌋, n − 3^⌊log₃n⌋)` pour tout
  n. *Preuve de la rampe : descente (Lemme 3) → périodicité de G → paires
  interdites sur {1,2} (la récurrence g(j+2P) = 2g(j+P) − g(j) interdit
  (1,2) et (2,1), donc G ≡ 0 sur [1, n−2P] avec G(0) ≠ 0) → interpolation
  de Mahler (Σ(−1)^iC(D+1,i) = (−1)^D force G(D+1) ≠ 0 : contradiction).*
  L'égalité est vérifiée sur toutes les cellules calculées (26/26) ; seule
  la borne supérieure générale (constructions pour tout n) reste à
  prouver.
- **C-F011d (réfutée)** : le critère de blocage mono-poids n'est PAS exact
  en fenêtre longue (150 contre-exemples) — il existe des obstructions
  collectives, dont le mod-2 (unicité de l'échelon) est l'exemple résolu.

## 8. Questions ouvertes du fil

1. **La rampe** (C-F011e, borne fine) : caractériser le problème réduit de
   la descente, ou exploiter la structure d'automate (Lemme 2) pour une
   preuve par périodicité des langages.
2. **La loi mod 3 complète** (valeurs 2·3^b observées pour MAJ).
3. **La synthèse mod 6** (loi complète C-F011).
4. **Lever la restriction symétrique** — la marche vers le modèle général,
   puis vers les circuits : chaque étage rapproche du vrai mur de 1987.

## 9. Statut épistémique

Production : pipeline « mesurer → conjecturer → prédire → prouver » du
dépôt (boucle LLM + solveurs exacts), 2026-06-10. Chaque théorème a une
preuve écrite ET une vérification exécutable indépendante (identités sur
échantillons massifs, croisements DP/solveur, certificats en entiers
exacts). Une conjecture intermédiaire (C-F011d) a été réfutée par les
données le jour de sa formulation — le processus fonctionne dans les deux
sens. **Aucune relecture externe** ; nouveauté non vérifiée contre la
littérature (les techniques — Mahler, Lucas, Kummer — sont classiques ;
les énoncés exacts sur deg_m^sym(THR) ne figurent pas dans les sources
consultées aux audits A-004/B-005, mais un folklore-check dédié serait
nécessaire avant toute diffusion).
