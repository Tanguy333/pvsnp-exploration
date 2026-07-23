# ATLAS-006 : extraction quantitative de la séparation sym/asym de KV (TR24-074) — la preuve est effective, et ses seuils ferment la zone 6

> Tâche type A/D. Exécutée le 2026-07-23. Texte : ECCC TR24-074
> (38 p., téléchargé et greppé cette session). Objectif de la zone 6
> de la matrice : « où (w, ε, degré, n) la séparation prouvée de KV
> devient-elle visible ? » — réponse chiffrée ci-dessous.

## 1. Les énoncés exacts (verbatim)

**Théorème 1.3.1 (KV)** : « Let 0 ≤ w ≤ n. Any symmetric torus
polynomial that approximates the ∆w function within an error of 1/2n
must have degree d at least Ω(√(n/log(n))). »

**Borne sup asymétrique (BHLR, citée par KV)** : « We prove that any
torus polynomial approximating AND within an error of 1/2n must have
degree at least Ω(log(n)). Compare this with an upper bound of
log₂(n), which follows from Bhrushundi, Hosseini, Lovett and Rao. »

**La séparation (KV, §1)** : « our lower bound holds for AND = ∆n.
However, [BHLR] proved that low degree torus polynomials can
approximate AND within an inverse linear error. Hence, asymmetric
torus polynomials afford more power than symmetric torus polynomials,
even when approximating symmetric Boolean functions. »

## 2. La preuve est EFFECTIVE (Lemme 3.7 — pigeonhole à la Siegel)

Le cœur : parmi les 2^{⌈n/2⌉+1} vecteurs g ∈ {0,1}^{n+1} supportés
sur une fenêtre, deux ont le même label Mg dès que

> **n^{(d+1)²} < 2^{⌈n/2⌉+1}**  (comptage verbatim du texte)

et γ = g − g′ ∈ null(M) à coefficients {−1,0,1}, ‖γ‖₁ ≤ n, avec
γ_w ≠ 0 pour TOUT w via le lemme de décalage (Lemme 3.8, colonnes de
B = décalages). D'où : la borne symétrique vaut pour tout degré

> **d ≤ d_max(n) = max{d : (d+1)²·log₂ n < ⌈n/2⌉+1}
> ≈ √(n / (2 log₂ n)) − 1.**

(Seuils à petits facteurs près — le comptage exact des labels ajuste
d'une unité au plus.)

## 3. Les trois seuils calculés (le verdict de la zone 6)

| Seuil | Valeur | Signification |
|---|---|---|
| **Vacuité** | n ≤ 40 : d_max = 0 | La borne symétrique de KV ne dit RIEN (pas même « degré > 1 ») pour tout n ≤ 40. Premier contenu à **n = 41** (d_max = 1). |
| **Instrument** | n = 7, 8 : d_max = 0 | ATLAS-005 (« gain invisible à n ≤ 7 ») est EXPLIQUÉ STRUCTURELLEMENT : ce n'était pas un défaut de mesure — le théorème est vide là. |
| **Croisement prouvé** | **n ≈ 4050** | d_max(n) > log₂(n) : la séparation sym/asym PROUVÉE (borne inf sym > borne sup asym) devient visible. À n = 4050 : d_max = 12 > log₂ = 12,0. |

## 4. Clôture de la zone 6

1. **« Pointer l'instrument sur la séparation prouvée » est impossible
   par trois ordres de grandeur** : MILP exact ≤ n ≈ 8 ; croisement
   prouvé ≈ 4·10³. La zone 6 telle que formulée est FERMÉE.
2. **Le no-man's land est 8 ≤ n ≤ ~4000** : le théorème y est muet
   (ou plus faible que log₂ n) et l'instrument n'y va pas. La VRAIE
   séparation (degrés exacts) commence peut-être bien avant 4050 — la
   borne de KV n'est pas serrée (facteur log vs la construction
   √(n log n) réelle) — mais aucun des deux outils ne peut le dire.
3. **Leçon pour la ligne 14** : la seule voie survivante de la route
   torique (l'asymétrique, Conjecture 3 de BHLR / Conjecture 13 de KV)
   vit dans un régime que ni preuve effective ni instrument ne touche
   aujourd'hui en dessous de n ~ milliers — cohérent avec le dossier
   AS (la Conjecture 13 réduite à un scalaire, l'estimée hors boucle).

## 5. Statut épistémique

Énoncés : verbatim du texte. d_max et les seuils : dérivés du comptage
VERBATIM du Lemme 3.7 (n^{(d+1)²} < 2^{⌈n/2⌉+1}), calcul exact par
script (session, voir ATLAS-006.md) — précision ±1 sur d_max selon
les facteurs 2·+1 du comptage des labels, sans effet sur les
conclusions (ordres de grandeur).
