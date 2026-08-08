# MC-017 — Mesures : la brique de totalisation minimale

Tâche : MC-017. Script : `checks/mc017_totalisation.py`. Date :
2026-08-08. Instrument : CP-SAT, OPTIMAL exigé, témoin re-vérifié ;
le solveur PARTIEL ne contraint que les paires U × B (les ∗ libres).
9 instances (3 exhaustives en complétions à s = 3, 4 à s = 4, 2 à
s = 5), ~90 résolutions au total (dont 80 pour les complétions
exhaustives), < 10 s.

Objets, pour une instance partielle (U, B = {0}) au format Th.2 de
MC-001 (points listés) : W_partiel ; complétions f₀ (∗→0), f₁ (∗→1),
min sur toutes les complétions (exhaustif si |∗| ≤ 6) ; totalisation
MUX minimale h(1, x) = f₀(x), h(0, x) = 𝟙_∗(x) sur s+1 bits.

## La table

| instance | s | W_partiel | W(f₀) | W(f₁) | W(𝟙_∗) | min-complétions | W(MUX) | δ = W(MUX) − (W(f₀)+W(𝟙_∗)+1) |
|---|---|---|---|---|---|---|---|---|
| I0a paires | 3 | 1 | 2 | 3 | 4 | **1 = W_partiel** (exhaustif, 32 ; atteint 1×) | 7 | +0 |
| I0b sing+paire | 3 | 2 | 4 | 3 | 3 | **2 = W_partiel** (exhaustif, 32 ; atteint 6×) | 7 | **−1** |
| I0c triangle | 3 | 2 | 3 | 3 | 3 | **2 = W_partiel** (exhaustif, 16 ; atteint 9×) | 6 | **−1** |
| I1 triangle | 4 | 2 | 5 | 4 | 6 | ≥ 2 (trivial) | 12 | +0 |
| I2 singletons | 4 | 4 | 4 | 4 | 4 | ≥ 4 (trivial) | 9 | +0 |
| I3 mixte | 4 | 2 | 5 | 4 | 7 | ≥ 2 (trivial) | 13 | +0 |
| I4 triples | 4 | 2 | 4 | 4 | 4 | ≥ 2 (trivial) | 9 | +0 |
| I5 étoile | 5 | 1 | 4 | 5 | 8 | ≥ 1 (trivial) | 15 | **+2** |
| I6 mixte | 5 | 2 | 6 | 5 | 8 | ≥ 2 (trivial) | 15 | +0 |

NB : la référence somme+1 n'est PAS un plancher ici — le théorème du
sélecteur (MC-006) exige des bras sur blocs DISJOINTS, or ce MUX
partage x entre ses deux bras. Les δ = −1 le confirment par l'exemple
(première version du script mal étiquetée « plancher MC-006 »,
corrigée avant consignation — les valeurs sont identiques).

## Lecture

1. **Q0 — fait central, favorable au schéma** : sur les 3 instances
   exhaustives, **la mesure partielle est ATTEINTE par une complétion**
   (min-complétions = W_partiel, 3/3). Si ce fait est général, une
   totalisation « à lecture min-complétion » lirait exactement la
   quantité que la NP-dureté partielle contrôle. Étiquette : MESURÉ à
   s = 3 (3 instances) — pas un théorème.
2. **Q1 — les complétions canoniques ratent la cible** : f₀ et f₁
   coûtent jusqu'à 2,5 × W_partiel (I1 : 5 contre 2) et l'optimum est
   réalisé par des complétions NON canoniques (I0a : 1 seule des 32).
   Une totalisation qui fige la complétion (∗→0) lit la mauvaise
   quantité.
3. **Q2 — le MUX minimal n'a pas de loi** : δ ∈ {−1, 0, +2} sur 9
   instances — ni plancher (espace partagé), ni décomposition stable.
   Le bras y=1 étant f₀, même une loi exacte lirait W(f₀), pas
   W_partiel.
4. **Verrou requalifié (la frontière de la ligne 18, précisée)** : la
   « totalisation à tête couplante » doit (i) forcer l'optimum du
   total à RÉALISER la complétion optimale (pas une complétion figée)
   et (ii) décoder son coût additivement — aucun des deux n'est fourni
   par le MUX à 1 bit. Cible suivante candidate (MC-018, sur
   décision) : le test de Q0 à plus grande échelle + les mécanismes de
   couplage à sélection multi-bits (la zone entre 1 bit et O(log)
   blocs disjoints).
