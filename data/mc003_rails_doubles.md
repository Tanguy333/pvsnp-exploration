# MC-003 — Données : W(f_g) vs dnf-size(g) sur les instances rails-doubles

> Produit par `checks/mc003_rails_doubles.py` (modes n2, n3, frontiere),
> 2026-08-07. f_g(y, z) = [z = ȳ ∧ g(y)] sur 2n variables (Prop. 5 de
> MC-001). W exact : CP-SAT canal de valeurs, statut OPTIMAL exigé, témoin
> re-vérifié par évaluation indépendante ; à n = 2, recoupé par force brute
> pure (10/10 accords). r = dnf-size exacte (implicants premiers + couverture
> minimale). Classes sous S_n. Deux exécutions complètes : valeurs
> identiques.

## n = 2 — les 10 classes (f_g sur 4 variables)

| g (canon) | #uns | r | W(f_g) | packing |
|---|---|---|---|---|
| 1 | 1 | 1 | 3 | 3 |
| 2 | 1 | 1 | 3 | 3 |
| 3 | 2 | 1 | 4 | 3 |
| 6 | 2 | 2 | 6 | 3 |
| 7 | 3 | 2 | 5 | 4 |
| 8 | 1 | 1 | 3 | 3 |
| 9 | 2 | 2 | 6 | 3 |
| 10 | 2 | 1 | 4 | 3 |
| 11 | 3 | 2 | 5 | 4 |
| 14 | 3 | 2 | 5 | 4 |

Analyse : r=1 → W ∈ [3, 4] ; r=2 → W ∈ [5, 6] (dispersion dans chaque r) ;
frontière r=1|2 : **GAP STRICT** (4 < 5). (r, #uns) détermine W : 0/4
couples dispersés. Packing = W : 3/10, pire écart 3 (g=6/9 : W=6,
packing=3). Packing max observé = 4 = 2n.

## n = 3 — les 78 classes (f_g sur 6 variables), zéro non-conclu

```
g=  1 |uns|=1 r=1 W=4      g=  2 |uns|=1 r=1 W=4      g=  3 |uns|=2 r=1 W=6
g=  6 |uns|=2 r=2 W=8      g=  7 |uns|=3 r=2 W=7      g=  8 |uns|=1 r=1 W=4
g=  9 |uns|=2 r=2 W=8      g= 10 |uns|=2 r=1 W=6      g= 11 |uns|=3 r=2 W=7
g= 14 |uns|=3 r=2 W=7      g= 15 |uns|=4 r=1 W=6      g= 22 |uns|=3 r=3 W=9
g= 23 |uns|=4 r=3 W=9      g= 24 |uns|=2 r=2 W=8      g= 25 |uns|=3 r=2 W=8
g= 26 |uns|=3 r=2 W=8      g= 27 |uns|=4 r=2 W=8      g= 30 |uns|=4 r=3 W=10
g= 31 |uns|=5 r=2 W=9      g= 40 |uns|=2 r=2 W=8      g= 41 |uns|=3 r=3 W=9
g= 42 |uns|=3 r=2 W=7      g= 43 |uns|=4 r=3 W=9      g= 44 |uns|=3 r=2 W=8
g= 45 |uns|=4 r=3 W=10     g= 46 |uns|=4 r=2 W=8      g= 47 |uns|=5 r=2 W=9
g= 60 |uns|=4 r=2 W=8      g= 61 |uns|=5 r=3 W=9      g= 62 |uns|=5 r=3 W=9
g= 63 |uns|=6 r=2 W=8      g=104 |uns|=3 r=3 W=9      g=105 |uns|=4 r=4 W=10
g=106 |uns|=4 r=3 W=10     g=107 |uns|=5 r=4 W=11     g=110 |uns|=5 r=3 W=9
g=111 |uns|=6 r=3 W=10     g=126 |uns|=6 r=3 W=10     g=127 |uns|=7 r=3 W=9
g=128 |uns|=1 r=1 W=4      g=129 |uns|=2 r=2 W=8      g=130 |uns|=2 r=2 W=8
g=131 |uns|=3 r=2 W=8      g=134 |uns|=3 r=3 W=9      g=135 |uns|=4 r=3 W=10
g=136 |uns|=2 r=1 W=6      g=137 |uns|=3 r=2 W=8      g=138 |uns|=3 r=2 W=7
g=139 |uns|=4 r=2 W=8      g=142 |uns|=4 r=3 W=9      g=143 |uns|=5 r=2 W=9
g=150 |uns|=4 r=4 W=10     g=151 |uns|=5 r=4 W=11     g=152 |uns|=3 r=2 W=8
g=153 |uns|=4 r=2 W=8      g=154 |uns|=4 r=3 W=10     g=155 |uns|=5 r=3 W=9
g=158 |uns|=5 r=4 W=11     g=159 |uns|=6 r=3 W=10     g=168 |uns|=3 r=2 W=7
g=169 |uns|=4 r=3 W=10     g=170 |uns|=4 r=1 W=6      g=171 |uns|=5 r=2 W=9
g=172 |uns|=4 r=2 W=8      g=173 |uns|=5 r=3 W=9      g=174 |uns|=5 r=2 W=9
g=175 |uns|=6 r=2 W=8      g=188 |uns|=5 r=3 W=9      g=189 |uns|=6 r=3 W=10
g=190 |uns|=6 r=3 W=10     g=191 |uns|=7 r=3 W=9      g=232 |uns|=4 r=3 W=9
g=233 |uns|=5 r=4 W=11     g=234 |uns|=5 r=2 W=9      g=235 |uns|=6 r=3 W=10
g=238 |uns|=6 r=2 W=8      g=239 |uns|=7 r=3 W=9      g=254 |uns|=7 r=3 W=9
```

### Plages par r et frontières

| r | plage de W | #classes | frontière avec r+1 |
|---|---|---|---|
| 1 | [4, 6] | 9 | **GAP STRICT** (6 < 7) |
| 2 | [7, 9] | 33 | **CONTACT** — W = 9 partagé |
| 3 | [9, 10] | 30 | **CONTACT** — W = 10 partagé |
| 4 | [10, 11] | 6 | — |

Témoins des contacts (le fait décisif) :
- **W = 9** : réalisé par r = 2 (g ∈ {31, 47, 143, 171, 174, 234}) ET par
  r = 3 (18 classes : g ∈ {22, 23, 41, 43, 61, 62, 104, 110, 127, 134, 142,
  155, 173, 188, 191, 232, 239, 254}) ;
- **W = 10** : réalisé par r = 3 (12 classes) ET par r = 4 (g ∈ {105, 150}).

Aucune inversion (monotonie faible préservée). (r, #uns) ne détermine plus
W : 2/15 couples dispersés — (r=2, #uns=3) → W ∈ {7, 8} et (r=3, #uns=4) →
W ∈ {9, 10}. Le déterminisme (r, #uns) → W observé à n = 2 était un
artefact de petite taille.

### Packing (Lemme 4) sur les extrêmes de chaque r — tous OPTIMAL

| r | g | W | packing | écart |
|---|---|---|---|---|
| 1 | 1 | 4 | 4 | 0 |
| 1 | 170 | 6 | 5 | 1 |
| 2 | 7 | 7 | 5 | 2 |
| 2 | 234 | 9 | 6 | 3 |
| 3 | 22 | 9 | 6 | 3 |
| 3 | 235 | 10 | 6 | 4 |
| 4 | 105 | 10 | 6 | 4 |
| 4 | 233 | 11 | 6 | 5 |

**Le packing sature à 6 = 2n** (valeur maximale observée, comme 4 = 2n à
n = 2) pendant que W croît jusqu'à 11 : l'écart CROÎT avec r. Observation à
deux points de taille — q.12, aucune loi revendiquée.

### Témoins de frontière : la structure des optima (mécanisme)

| g | r | W | profil taille→coefficients | valeurs uns | valeurs zéros |
|---|---|---|---|---|---|
| 234 | 2 | 9 | {2: [2], 3: [1×5], 4: [1, 1]} | **{1}** | {0, 2, 3, 4, 5, 9} |
| 22 | 3 | 9 | {2: [2, 2, 2], 3: [1, 1, 1]} | **{1}** | {0, 2, 3, 4, 5, 6, 9} |
| 235 | 3 | 10 | {3: [1×6, 2, 2]} | **{1}** | {0, 2, 3, 4, 5, 6, 10} |
| 105 | 4 | 10 | {1: [1, 1], 2: [1×4], 3: [1×4]} | **{3}** | {0, 1, 2, 4, 6, 7, 10} |

Les quatre optima renvoyés donnent aux uns **une seule valeur commune** —
le régime effectif est un « couvert à valeur exacte » (tête ETHR de fait),
possible parce que les uns de f_g forment une **antichaîne** (tous au poids
de Hamming n). Observation sur les optima renvoyés par le solveur, pas un
théorème d'unicité.

## Faits structurels (prouvés, une ligne chacun)

- f_g(0) = 0 et f_g(1^{2n}) = 0 (la diagonale ne contient ni 0 ni 1^{2n}
  pour n ≥ 1) ⟹ **aucun implicant positif** (lemme d'obstruction MC-001) :
  les instances vivent entièrement dans le régime valeurs/zoo — vérifié par
  assertion sur les 88 instances.
- Les uns forment une antichaîne ⟹ **alternance (F-020) ≤ 2** : la borne
  combinatoire du fil est aveugle ici ; seul le packing pouvait concourir,
  et il sature.

## Réserves

- n ≤ 3 exhaustif, deux points de taille — q.12 : aucune extrapolation ;
  la réfutation vaut pour ces instances à ces tailles, mais le mécanisme
  identifié (antichaîne → valeur commune) est structurel, pas un accident
  numérique.
- Optimalité CP-SAT : statut OPTIMAL exigé partout (0 non-conclu) ; la
  minimalité repose sur l'assertion du solveur, non ré-énumérable à
  6 variables (réserve T27-S2 §4) — sauf n = 2, recoupé par force brute
  pure (10/10).
- Packing mesuré sur 8 extrêmes à n = 3 (tous à n = 2), pas sur les 78.
