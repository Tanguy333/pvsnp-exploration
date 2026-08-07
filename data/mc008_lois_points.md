# MC-008 — Données : les lois G et F des fonctions à 1 et 2 points

> Produit par `checks/mc008_lois_points.py` (modes g1, f2, f5, cor),
> 2026-08-07. W exact : force brute pure (ν ≤ 4), CP-SAT OPTIMAL témoin
> re-vérifié (ν = 5). Notation : pour deux points u, v ∈ {0,1}^ν,
> (a, b, m, o) := (|u\v|, |v\u|, |u∩v|, ν − a − b − m), normalisé a ≤ b.

## 1. La loi G (fonctions à un point) — PROUVÉE, confirmée exhaustivement

**G(u ; ν) = ν − |u| + 1 si u ≠ 0 ; ν si u = 0.**
Vérification exhaustive : ν = 2 (4 points), ν = 3 (8), ν = 4 (16) —
**0 écart**. Preuve complète dans la fiche (`tasks/done/MC-008.md` §2) :
majorant par la construction p = m_u + Σ_{j∉u} m_{u∪{j}} ; minorant par
packing (Lemme 4 de MC-001).

## 2. La table de F (fonctions à deux points) — exhaustive ν = 3, 4, contrôles ν = 5

La symétrie S_ν exige que F ne dépende que de (a, b, m, ν) — vérifié :
une seule valeur de W par groupe, sur tous les groupes.

### ν = 3 (28 paires, 9 groupes) et ν = 4 (120 paires, 17 groupes)

| (a, b, m) | o(ν=3) : F | o(ν=4) : F | conjecture |
|---|---|---|---|
| (0,1,0) | 2 : **2** | 3 : **3** | ν−1 |
| (0,1,1) | 1 : **2** | 2 : **3** | ν−1 |
| (0,1,2) | 0 : **1** | 1 : **2** | ν−2 |
| (0,1,3) | — | 0 : **1** | ν−3 |
| (0,2,0) | 1 : **4** | 2 : **6** | 2ν−2 |
| (0,2,1) | 0 : **3** | 1 : **5** | 2ν−3 |
| (0,2,2) | — | 0 : **3** | 2ν−5 |
| (0,3,0) | 0 : **3** | 1 : **5** | 2ν−3 |
| (0,3,1) | — | 0 : **4** | 2ν−4 |
| (0,4,0) | — | 0 : **4** | 2ν−4 |
| (1,1,0) | 1 : **4** | 2 : **6** | 2ν−2 |
| (1,1,1) | 0 : **2** | 1 : **4** | 2ν−4 |
| (1,1,2) | — | 0 : **2** | 2ν−6 |
| (1,2,0) | 0 : **4** | 1 : **6** | 2ν−2 |
| (1,2,1) | — | 0 : **4** | 2ν−4 |
| (1,3,0) | — | 0 : **5** | 2ν−3 |
| (2,2,0) | — | 0 : **6** | 2ν−2 |

### La forme close (CONJECTURE C-MC008, zéro exception sur 53 groupes)

> **RÉFUTÉE (MC-009, 2026-08-07)** : la branche incomparable est fausse
> dès a ≥ 3 — (3,3,0,0) : F = 8 ≠ 9 prédit (la plage d'ajustement ν ≤ 5
> imposait a ≤ 2). Loi corrigée et majorants prouvés :
> `data/mc009_preuve_F.md`. Les branches recouvrement et comparable
> tiennent sur toute la donnée.

- **Recouvrement** (a = 0, b = 1 — v couvre u) :
  **F = ν − m − [m = 0]** — CE CAS EST PROUVÉ (fiche §3).
- **Comparable** (a = 0, b ≥ 2 — u ⊂ v à distance ≥ 2) :
  **F = 2ν − b − 2m + [m ≥ 1]**.
- **Incomparable** (a ≥ 1) : **F = 2(ν − m) − max(2, a, b)**.

### Contrôles ν = 5 (27 groupes testés sur 28 réalisables, CP-SAT) — tous conformes

> [Précision VER-MC-1 : la boucle de `run_f5` bornait b ≤ 4, omettant le
> groupe (0,5,0) — vérifié conforme (F = 5) par le vérificateur V3 ;
> ν = 5 est donc couvert en entier, 28/28.]

(0,1,·) : 4, 4, 3, 2, 1 ; (0,2,·) : 8, 7, 5, 3 ; (0,3,·) : 7, 6, 4 ;
(0,4,·) : 6, 5 ; (1,1,·) : 8, 6, 4, 2 ; (1,2,·) : 8, 6, 4 ;
(1,3,·) : 7, 5 ; (1,4,0) : 6 ; (2,2,·) : 8, 6 ; (2,3,0) : 7.
**53/53 groupes conformes (ν ≤ 5). Statut : MESURÉ exhaustif ν ≤ 4 +
échantillon complet des groupes ν = 5 ; CONJECTURE au-delà (q.12).**

## 3. Le corollaire fibre — et la CORRECTION de la règle de MC-007

Base 1 bit, fibres [y = c₀] (x = 0) et [y = c₁] (x = 1), s = 3 :
recalcul de g via F et G — distribution retrouvée : {−1 : 9, 0 : 40,
+1 : 7} ✓. MAIS le test de la règle consignée par MC-007 (« g < 0 ⟺
supp(c₁) ⊊ supp(c₀), c₁ ≠ 0 ») produit **trois contre-exemples** :
(c₀ = 111, c₁ ∈ {001, 010, 100}) — emboîtés directionnels, g = 0.

**La règle exacte, dérivée des lois** (pour c₁ ⊊ c₀, c₁ ≠ 0, en posant
k = |c₀ \ c₁|) : ~~g = k − 2~~ **[CORRIGÉ par VER-MC-1 : g = k − max(k, 2)
— identique sur le domaine mesuré s = 3 (k ≤ 2), mais « k − 2 » est
fausse dès k ≥ 3 : contre-exemple vérifié à s = 4, (1111, 0001) →
g = 0 ≠ 1]**. Seul le RECOUVREMENT descendant (k = 1)
partage, et d'exactement 1 ; l'emboîtement profond (k ≥ 2) ne partage pas.
Les 9 paires partageantes de MC-007 sont exactement les 9 recouvrements
descendants — la règle « emboîtement » était un sur-ajustement (les 12
paires emboîtées contiennent 3 non-couvrantes, toutes à g = 0).
Autres cas, dérivés des lois : c₀ ⊊ c₁ (vers le haut) : g = 0 ;
c₁ = 0 : g = |c₀| + 1 − max(2, |c₀|) ≥ 0 ; incomparables (k₀, k₁ ≥ 1) :
**g = k₀ + k₁ − max(2, k₀, k₁ + 1) ≥ 0 toujours** — la condition
d'antichaîne de MC-007 reste SUFFISANTE pour le non-partage ; la
caractérisation exacte du partage est le recouvrement descendant.

## Réserves

- F : conjecture au-delà de ν = 5 (le corollaire général en dépend) —
  la preuve complète de F est la cible suivante.
- Optima ν = 5 : assertion de solveur ; ν ≤ 4 : force brute pure.
- La dérivation du corollaire général utilise la forme close de F aux
  paramètres (a, b) arbitraires — prouvée seulement pour le régime
  recouvrement ; ailleurs elle a le statut de la conjecture.
