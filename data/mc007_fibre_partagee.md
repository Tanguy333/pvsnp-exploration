# MC-007 — Données : la carte du partage en géométrie de fibre partagée

> Produit par `checks/mc007_fibre_partagee.py` (modes s2, s3, struct, t2),
> 2026-08-07. Objet : h(x, y) = φ_x(y), base x (1 bit sauf §4), fibre y
> (s bits) PARTAGÉE — c'est-à-dire toute fonction sur 1+s variables lue
> par tranches : l'espace est exhaustif. Écart g(h) := W(h) − (W(φ₀) +
> W(φ₁)). W exact : force brute (3 vars) ; CP-SAT OPTIMAL sur les 3 984
> classes de S₄ propagé par orbites (4 vars, 62 s — compte corrigé par
> VER-MC-1) ; CP-SAT (4 vars, §3 — encodage corrigé par VER-MC-1).
> Encadrements prouvés : φ répétée ⟹ g = −W(φ) (partage total) ;
> B2 ⟹ g ≥ −min(W₀, W₁) toujours.

## 1. Exhaustif s = 2 (256 h) et s = 3 (65 536 h) — par catégorie de paire

| catégorie | s = 2 | s = 3 |
|---|---|---|
| répétée (φ₀ = φ₁) | g = {−2: 8, −1: 6} | g = {−5: 12, −4: 72, −3: 96, −2: 60, −1: 14} |
| complémentaire (φ₁ = ¬φ₀) | {−1: 6, 0: 8} | {−4: 12, −3: 42, −2: 84, −1: 82, 0: 34} |
| **distinctes non constantes** | {−1: 34, 0: 72, +1: 52, +2: 10} | {−4: 156, −3: 1338, −2: 5866, −1: 14642, 0: 19624, +1: 14846, +2: 5990, +3: 1426, +4: 108, +5: 12} |
| avec tranche constante | {0: 14, +1: 34, +2: 8, +3: 2} | {0: 254, +1: 338, +2: 198, +3: 206, +4: 22} |

**Bilan distinctes non constantes** : s = 2 → 34/168 sous-additives
(20 %), 72 égales, 62 super ; s = 3 → **22 002/64 008 sous-additives
(34 %)**, 19 624 égales, 22 382 super. **Le partage est GÉNÉRIQUE entre
fibres distinctes** — la super-additivité inconditionnelle est morte,
exhaustivement.

**Les pires témoins atteignent le plancher B2** (partage TOTAL entre
distinctes) : à s = 3, g = −4 sur 156 paires — exemples : h = 188
(φ₀ = 6, W = 4 ; φ₁ = 14, W = 5 ; W(h) = 5 = max), h = 508, 1208, 1276,
2255, 2828 : la fibre bon marché vient GRATUITEMENT. La catégorie
« répétée » vérifie g = −W(φ) partout (encadrement prouvé, 0 exception).

## 2. Cas structurés (consultation des tables exhaustives)

- **Marqueur bon marché** ([y = 1^s], W = 1, contre toute φ) : s = 2 →
  g = {−1: 1, 0: 4, +1: 8, +2: 1} ; s = 3 → g = {−1: 1, 0: 19, +1: 108,
  +2: 112, +3: 14}. **Le marqueur n'est presque jamais absorbé** (1 seul
  cas sur 254 à −1) — utilisable comme étiquette de gadget.
- **Points épars à la HOS18** ([y = c₀] vs [y = c₁], c₀ ≠ c₁, s = 3,
  56 paires ordonnées) : g = {−1: 9, 0: 40, +1: 7} — **quasi additifs**,
  jamais pire que −1. L'analogue direct du « scattered » de HOS18 tient à
  ±1 près.

### La règle des 9 exceptions — l'emboîtement directionnel

Décomposition des 56 paires par relation entre les supports de c₀ et c₁ :

| relation supp(c₀) / supp(c₁) | g = −1 | g = 0 | g = +1 |
|---|---|---|---|
| disjoints | 0 | 9 | 3 |
| incomparables-chevauchants | 0 | 6 | 0 |
| emboîtés | **9** | 25 | 4 |

Les 9 partages sont les paires (3,1), (3,2), (5,1), (5,4), (6,2), (6,4),
(7,3), (7,5), (7,6).

> **CORRECTION (MC-008, 2026-08-07)** : la caractérisation initialement
> écrite ici (« emboîtement strict directionnel : supp(c₁) ⊊ supp(c₀),
> c₁ ≠ 0 ») était un SUR-AJUSTEMENT — vraie sur les 9 paires, fausse en
> réciproque : (7,1), (7,2), (7,4) sont emboîtées directionnelles avec
> g = 0. **La règle exacte, dérivée des lois de MC-008** : pour c₁ ⊊ c₀,
> c₁ ≠ 0, g = |c₀ \ c₁| − 2 — seul le RECOUVREMENT descendant
> (|c₀ \ c₁| = 1) partage, et d'exactement 1. Les 9 paires ci-dessus sont
> exactement les 9 recouvrements descendants de la famille. Ce qui reste
> vrai tel quel : supports deux à deux non emboîtés ⟹ g ≥ 0 (la condition
> d'ANTICHAÎNE est suffisante — désormais dérivée des lois, voir
> `data/mc008_lois_points.md` §3, plus seulement mesurée).

## 3. Base 2 bits (4 fibres partagées, s = 2, 4 variables) — échantillon

> **CORRIGÉ (VER-MC-1, 2026-08-07).** La version initiale de ce tableau
> (g = +3..+12, « entièrement super-additif ») était un ARTEFACT
> D'ENCODAGE : le mode t2 déclarait 6 variables pour des points sur
> 4 bits — 48 zéros fantômes gonflaient W. Bug attrapé par la passe
> adverse tierce (ré-implémentation indépendante), corrigé dans le
> script, rejoué à la même graine.

10 quadruplets aléatoires (graine 20260807), tous OPTIMAL, < 1 s :
g = −1, +1, +3, −3, −1, +2, 0, −2, 0, −4 — **5/10 SOUS-additifs**
(pire : t2.9, φ = [13, 9, 9, 13], Σ W = 8, W(h) = 4, g = −4). À base
2 bits aussi, le partage est courant sur les tirages quelconques — la
nécessité de fibres STRUCTURÉES (régime §2) en sort renforcée.

## Réserves

- s ≤ 3 exhaustif, base 1 bit ; base 2 bits sur 10 tirages seulement —
  q.12 : aucune extrapolation ; « générique » et « quasi » sont des faits
  de ces espaces.
- W à 4 variables : optima CP-SAT par classes (assertion de solveur,
  réserve T27-S2 §4) ; 3 variables : force brute pure.
- La règle d'emboîtement directionnel vaut pour la famille points-épars à
  s = 3 ; sa généralité est la question de la tâche suivante, pas un
  acquis.
