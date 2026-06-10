# TÂCHE F-011, étape 7 : LA RAMPE EST PROUVÉE (Théorème E) — ✅

- **Type** : F (preuve — le morceau dur du fil)
- **Exécutée le** : 2026-06-10
- **Script** : [`checks/task_f011e7_ramp.py`](../../checks/task_f011e7_ramp.py)
  (4 maillons vérifiés : identité D=0..60, paires interdites, 10/10 points
  du régime, loi complète 26/26)

## Théorème E

> Pour P = 3^b et 2P < n < 3P : `deg₃^sym(OR_n) ≥ n − P`.
> Avec le Théorème D : **`deg₃^sym(OR_n) ≥ max(3^⌊log₃n⌋, n − 3^⌊log₃n⌋)`
> pour tout n** — et cette borne est *exactement atteinte* sur toutes les
> cellules calculées (n ≤ 26).

## Preuve (chaîne de 4 maillons)

Soit g : [0,n] → F₃ avec g(0) = 0, g ∈ {1,2} sur [1,n], deg(g) = d.
Supposons d < n − P (on sait d ≥ P par le Théorème D).

1. **Descente** (Lemme 3) : `G := g(·+P) − g` a deg(G) ≤ d − P < n−2P < P,
   domaine [0, n−P].
2. **Périodicité** (argument du Théorème D appliqué à G) : deg(G) < P ⟹
   Δ^P G ≡ 0 ⟹ `G(j+P) = G(j)` pour j ∈ [0, n−2P].
3. **Paires interdites** : G(j+P) = G(j) se réécrit
   `g(j+2P) = 2g(j+P) − g(j) (mod 3)`. Pour j ∈ [1, n−2P], les trois
   valeurs sont dans {1,2} ; or (1,2) donnerait g(j+2P) = 0 et (2,1)
   aussi — interdites. Donc **G(j) = 0 pour tout j ∈ [1, n−2P]**, alors
   que `G(0) = g(P) ≠ 0`.
4. **Interpolation de Mahler** : posons D := deg(G) ≤ n−2P−1. G est
   déterminée par ses valeurs sur [0, D] : c ≠ 0 puis des zéros. Ses
   coefficients valent a_i = (−1)^i c, d'où, par l'identité
   `Σ_{i=0}^{D} (−1)^i C(D+1,i) = (−1)^D` :
   `G(D+1) = c·(−1)^D ≠ 0`. Mais D+1 ≤ n−2P, donc G(D+1) = 0 par (3).
   **Contradiction.** ∎

## Ce que ça change

- **La borne inférieure de C-F011e est entièrement prouvée** — il ne
  manque plus que les constructions générales (borne sup) pour en faire
  une loi exacte théorème ; les certificats DP existent pour chaque
  n ≤ 26.
- La preuve est **entièrement élémentaire** (Lucas, Pascal, Mahler,
  un argument de parité de paires) et chaque maillon est vérifié
  exécutablement — le standard du fil.
- Le schéma de preuve (descente → périodicité → contrainte de valeurs →
  interpolation) est un **gabarit réutilisable** : c'est le candidat
  naturel pour la loi MAJ mod 6 (C-F011) et pour le cas t général.

## Tableau de bord du fil F-011 (7 étapes)

**8 théorèmes prouvés** : Lemme 1 (noyau) · Lemme 2 (automate) · Lemme 3
(descente) · T-F011a (mod 2 exact, famille) · T-F011b (infaisabilité
mod 6) + anomalies · deg₆^sym(MAJ_32) = 27 · T-F011c (périodicité) ·
**T-F011e/Théorème E (la rampe)**.
**Conjectures restantes** : C-F011 (loi MAJ mod 6, 47/47) ; borne sup
générale de la loi OR mod 3 (constructions).
