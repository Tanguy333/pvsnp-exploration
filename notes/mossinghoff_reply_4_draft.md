# Brouillon — réponse 4 à Michael Mossinghoff (consolidée)

> À envoyer par Tanguy. Remplace les brouillons 3 + engine-note.
> Couvre : (1) moteur + complexité ; (2) nouveaux polynômes m=22, m=23 ;
> (3) temps de vérification au-delà de m=23 ; (4) limite technique (m max).
> Section temps/limite : chiffres ancrés sur calibrations m=24/25 (à finaliser).

---

**Subject:** Engine, complexity, and new minimal pure products for m = 22, 23

Dear Michael,

Thank you again. Here is a fuller picture of the search and what it has
now produced.

## The engine

The search is a depth-first enumeration of non-decreasing exponent tuples
1 <= t_1 <= t_2 <= ... <= t_m, building the partial product
Prod (1 - x^{t_i}) incrementally and cutting a branch as soon as either
(a) the partial product's height exceeds a fixed transient bound H, or
(b) a branch-and-bound test shows the remaining factors cannot beat the
best degree found so far. The inner step -- multiply the current integer
coefficient vector by (1 - x^t) and test the height -- runs through Numba,
which JIT-compiles it to machine code via LLVM, so it is effectively at C
speed without leaving Python. All arithmetic is exact integer, and every
champion is re-verified independently (height 1 and order of vanishing at
1) in exact Python before being reported.

## Complexity

Each node costs O(D), a single pass over a coefficient vector of length
<= D (the degree budget). The number of nodes is the bottleneck. Measured
at m = 22, the tree grows steeply with the allowed transient height H:

  H <= 1 :   748 thousand nodes
  H <= 2 :  39.6 million nodes   (x53)
  H <= 3 :   1.05 billion nodes  (x26)

at a steady ~19 million nodes/s and a flat ~0.1 GB of memory regardless of
H. The budget D matters similarly: at fixed H the tree grows by roughly a
factor 5 per +40 of degree. So the binding constraint is the exponential
branching, not per-node speed or memory -- a faster language buys only a
constant factor; real reach comes from the branch-and-bound prune and, if
needed, splitting the first levels across cores.

## New minimal pure products: m = 22 and m = 23

Extending your Table 1 (which stops at m = 21), I get, for the smallest
flat pure product Prod (1 - x^{t_i}) divisible by (1 - x)^m:

- **m = 22 : degree 473**, attained by [your m=21 champion] x (1 - x^179),
  i.e. exponents {1,2,3,4,5,6,7,9,10,11,13,15,16,17,19,21,23,25,27,29,31,
  179}. Proven minimal among pure products up to transient height 5
  (a complete branch-and-bound search below 474). m = 22 appears to be a
  "hard" rung: no compact champion exists -- the minimum is just the m=21
  champion extended by one large binomial (the smallest flat extension is
  x^179, since smaller shifts collide a +1 onto a -1).

- **m = 23 : degree 439**, exponents {1,2,3,5,6,7,8,9,11,13,14,15,16,17,
  19,20,22,23,25,29,31,37,106}. Non-trivial (its 22-factor prefix is not
  itself a low-degree flat product), and proven minimal among pure
  products up to transient height 6.

Note the non-monotonicity: d(23) = 439 < d(22) = 473. m = 23 has a genuine
compact champion while m = 22 does not. (As with your m <= 21 extremals,
these are pure products; whether they coincide with the overall minimal
height-1 degree for m = 22, 23 I have not separately verified -- so I'd
state them as smallest known pure products, i.e. upper bounds, pending
your view.)

## Your Table 1 entries are minimal pure products (certified)

A byproduct you may find satisfying: I ran complete branch-and-bound
searches strictly below each of your Table 1 values for m = 11..21
(pure products, transient height <= 4). None can be improved: every
entry -- 69, 93, 112, 120, 141, 159, 185, 207, 245, (307,) 294 -- is in
fact the exact minimum among pure products within that transient bound,
not merely the smallest known. (The searches take seconds; the whole
sweep is ~5 s on one core. Whether the overall height-1 minima coincide
remains open beyond your proofs for m <= 10, of course.)

## A correction to my earlier transit data

Re-auditing my records, I must correct something I wrote in my first two
messages: I claimed the m = 20 example requires transient height 3 and
grouped it with {15, 16, 17}. That was wrong -- a confounded test on my
side (my transient-height-2 run had used a degree budget of 299 < 307, so
it could not have found the example at any height). In fact the m = 20
champion's partial products never exceed height 2, and a height-2 search
with an adequate budget finds it in under a second. The transit-3 family
is {15, 16, 17} only (re-verified: no flat pure product with transient
height <= 2 exists at degrees <= 141/159/185 for m = 15/16/17). So the
reason the example was missed is not the transient height -- your own
explanation, the outlying exponent 50 after the gap at 31, is the right
one.

## Time as a function of degree, and the technical limit

The wall is purely time (memory is flat ~0.1 GB throughout). The cost is
governed by the degree budget D, and the law is clean and measured (m=22,
transit 4, full tree, ~22M nodes/s on one core):

  D < 400 : 0.4 G nodes,  17 s
  D < 440 : 2.0 G nodes,  85 s
  D < 474 : 6.7 G nodes,  4.8 min

i.e. roughly **x5 per +40 of degree** (an order of magnitude every ~57).
Extrapolated, time(D) ~ 289 s * 5^((D-474)/40):

  D = 510 : ~20 min
  D = 550 : ~1.5 h
  D = 590 : ~8 h
  D = 630 : ~1.5 days
  D = 670 : ~8 days
  D = 710 : ~5 weeks
  D = 800 : ~4-5 years

Two corrections: each extra unit of transient height multiplies by ~10
(so at transit 5 a given time is reached ~57 degrees sooner); but larger m
runs *faster* at the same degree (packing -- m=24 at D=500 took 62 s, ~16x
below the m=22 curve), so the table is a conservative upper bound.

Since d(m) ~ 0.67 m^2 (m=33 -> ~730, m=35 -> ~820), a complete transit-<=5
certificate on one core is practical to about **m = 33-35** for regular
sizes, and much sooner for a "hard" size whose minimum jumps to a trivial
degree ~800 -- though I should say that in my data every size from 24 to
30 behaves as a hard size (nothing within reach of the 0.67 m^2 trend up
to transient height 7 for m = 26..30), so compact champions may simply
stop at m = 23. A parallel split over the first two exponents across k
cores buys one to two further values of m. The doubly-compounding growth
-- exponential in the degree D, with D itself ~quadratic in m -- is the
cap.

I'd be glad to record m = 20 (and, as upper bounds, m = 22, 23) in the
OEIS if you think it appropriate. Thank you for the encouragement.

Best,
Tanguy

---

## Statut épistémique (hors email)
- Moteur Numba/LLVM, B&B, vérif exacte : vrai (V-038, V-054).
- Croissance ×53/×26 par transit (m=22, budget 520), ×~5 par +40 budget,
  ~19M n/s, mémoire plate ~0,11 Go : mesuré.
- m=22 = 473 minimal transit ≤5 (71,4 G nœuds), m=23 = 439 minimal
  transit ≤6 (34,2 G nœuds) : prouvé. Non-monotone 439 < 473.
- Caveat produit-pur vs d(m) général : maintenu (pour m≤21 coïncident car
  extrémaux BM sont des produits purs ; 22/23 non vérifié).
- Temps/limite : loi temps-degré ancrée sur la série m=22 transit-4
  (×5 par +40 de degré, ~22M n/s) — chiffres fermes, plus de placeholder.
- Section « Time to verify sizes beyond m=23 » : RETIRÉE (demande de Tanguy).
- **Section correctif τ(20) AJOUTÉE (audit 2026-06-29, 26e auto-correction)** :
  les emails 1-2 envoyés affirmaient « m=20 exige transit 3, famille
  {15,16,17,20} » — FAUX pour 20 (τ=2, triple preuve, V-047 §6) ; les rangs
  15-17 re-vérifiés transit-3. Le correctif est dû à Mossinghoff (il a reçu
  la claim fausse 2×). L'explication du saut 31→50 (la sienne) tient.
- Hedge ajouté sur la limite m=33-35 (« si des rangs réguliers existent
  encore — m=24-30 sont tous durs »).
