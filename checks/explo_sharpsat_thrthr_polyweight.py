"""
#SAT pour THR o THR a POIDS POLYNOMIAUX -- algorithme exact + mesure.

REPLICATION VERIFIANTE (declaree) : le fait que le comptage soit faisable
sous poids polynomiaux + peu de portes est du folklore (DP sur sommes
partielles ; cf. la lignee IPS FOCS 2013 / Chen-Santhanam-Srinivasan CCC
2016 / Kabanets-Lu pour le regime creux 2^{n-n^eps}). Ce script ne
revendique aucune nouveaute : il CONSTRUIT l'algorithme, le CALIBRE contre
la force brute, et MESURE le point exact ou il cesse de battre 2^n --
pour SITUER le repo sur la carte de la ligne 7 / ligne 11 (PTF).

MODELE : circuit THR o THR sur n variables booleennes.
  - m portes basses : g_j(x) = [ sum_i w[j][i] x_i >= t_j ], poids ENTIERS.
  - porte haute : F(x) = [ sum_j v_j g_j(x) >= T ].
  #SAT(F) = #{ x in {0,1}^n : F(x) = 1 }.

ALGORITHME (DP sur l'etat-produit des sommes partielles) :
  etat = (s_1, ..., s_m), s_j = somme partielle de la porte j.
  Chaque s_j vit dans [min, max] de largeur <= n*W (W = |poids| max).
  => au plus (nW+1)^m etats DISTINCTS, quel que soit 2^n.
  Temps = O(n * #etats-atteints). Comptage EXACT en fin de DP.

LE LEVIER EST LE POIDS POLYNOMIAL : si W = poly(n), chaque coordonnee a
poly(n) valeurs -> etat-espace (poly)^m. Avec des poids EXPONENTIELS
(w_i = 2^i), s_j distingue les 2^n affectations : AUCUNE fusion, le DP
s'effondre sur la force brute. Ce script le montre aussi (calibration
negative).

DOUBLE CALIBRATION :
  (+) exactitude : DP == force brute sur instances aleatoires (n<=18).
  (+/-) le meme instrument, deux regimes de poids : poly (fusion massive,
        #etats poly^m) vs 2^i (zero fusion, #etats = 2^n).
CROISEMENT MESURE : #etats ~ (nW)^m croise 2^n a m ~ n / log2(nW) --
au-dela, le DP ne bat plus la force brute (c'est le regime DENSE, mur de
Williams : 2^{n-n^eps} pour THR o THR dense reste OUVERT).
"""

from __future__ import annotations

import itertools
import math
import sys
import time
from collections import defaultdict

import numpy as np


def make_random_circuit(n, m, W, rng):
    bottom = []
    for _ in range(m):
        w = [int(rng.integers(-W, W + 1)) for _ in range(n)]
        # seuil aleatoire dans la plage atteignable
        lo = sum(min(0, wi) for wi in w)
        hi = sum(max(0, wi) for wi in w)
        t = int(rng.integers(lo, hi + 1)) if hi > lo else lo
        bottom.append((w, t))
    v = [int(rng.integers(1, W + 1)) for _ in range(m)]
    T = int(rng.integers(1, sum(v) + 1)) if m else 0
    return bottom, (v, T)


def brute_count(n, bottom, top):
    m = len(bottom)
    v, T = top
    total = 0
    for x in itertools.product((0, 1), repeat=n):
        fires = 0
        acc = 0
        for j, (w, t) in enumerate(bottom):
            s = sum(w[i] for i in range(n) if x[i])
            if s >= t:
                acc += v[j]
        if acc >= T:
            total += 1
    return total


def dp_count(n, bottom, top):
    """ DP sur l'etat-produit ; renvoie (#SAT, #etats-max-atteints). """
    m = len(bottom)
    v, T = top
    states = {tuple([0] * m): 1}
    max_states = 1
    for i in range(n):
        new = defaultdict(int)
        incr = tuple(bottom[j][0][i] for j in range(m))
        for st, cnt in states.items():
            new[st] += cnt                                  # x_i = 0
            st1 = tuple(st[j] + incr[j] for j in range(m))  # x_i = 1
            new[st1] += cnt
        states = new
        max_states = max(max_states, len(states))
    total = 0
    for st, cnt in states.items():
        acc = sum(v[j] for j in range(m) if st[j] >= bottom[j][1])
        if acc >= T:
            total += cnt
    return total, max_states


def main():
    rng = np.random.default_rng(20260809)

    print("#SAT pour THR o THR a poids polynomiaux -- DP exact + mesure")
    print("=" * 72)

    # ---- (+) exactitude : DP == force brute ----
    print("\n[A] Calibration d'exactitude (DP vs force brute), n=16 :")
    ok = True
    for trial in range(6):
        n, m, W = 16, int(rng.integers(2, 5)), int(rng.integers(2, 8))
        bottom, top = make_random_circuit(n, m, W, rng)
        c_dp, states = dp_count(n, bottom, top)
        c_bf = brute_count(n, bottom, top)
        match = (c_dp == c_bf)
        ok &= match
        print(f"  n={n} m={m} W={W:>2} : #SAT_DP={c_dp:>6} #SAT_BF={c_bf:>6}"
              f"  etats={states:>6}  {'OK' if match else 'ECART !!'}")
    print(f"  exactitude : {'VERIFIEE' if ok else 'ECHEC'}")

    # ---- (+/-) le poids decide la fusion ----
    print("\n[B] Le POIDS decide : meme n, meme m -- poly vs 2^i :")
    n, m = 20, 2
    # poids polynomiaux (W = n)
    bottom_poly, top = make_random_circuit(n, m, n, rng)
    _, st_poly = dp_count(n, bottom_poly, top)
    # poids exponentiels (2^i) : une porte = somme ponderee binaire
    bottom_exp = [([2 ** i for i in range(n)], 2 ** (n - 1)),
                  ([2 ** i for i in range(n)], 2 ** (n - 1) + 1)][:m]
    while len(bottom_exp) < m:
        bottom_exp.append(([2 ** i for i in range(n)], 2 ** (n - 1)))
    _, st_exp = dp_count(n, bottom_exp, ([1] * m, 1))
    print(f"  n={n} m={m} : poids poly (W={n})  -> #etats max = {st_poly}")
    print(f"  n={n} m={m} : poids 2^i (exponent) -> #etats max = {st_exp}"
          f"   (= 2^n = {2**n} : ZERO fusion)")
    print(f"  ratio d'explosion : x{st_exp / max(st_poly,1):.0f}"
          "  -- LE POIDS POLYNOMIAL EST LE LEVIER")

    # ---- crossover : #etats(m) vs 2^n ----
    print("\n[C] Croisement : #etats(m) vs 2^n, n=20, W=20 (poids poly) :")
    n, W = 20, 20
    print(f"  {'m':>3} | {'#etats max':>12} | {'2^n':>10} | {'DP bat 2^n ?':>12}"
          f" | {'~ predit (nW+1)^m borne 2^n':>0}")
    prev = None
    for m in [1, 2, 3, 4, 6, 8, 10, 12, 14]:
        bottom, top = make_random_circuit(n, m, W, rng)
        t0 = time.time()
        c, states = dp_count(n, bottom, top)
        dt = time.time() - t0
        beats = states < 2 ** n
        print(f"  {m:>3} | {states:>12} | {2**n:>10} | "
              f"{'oui' if beats else 'NON':>12} | ({dt:.1f}s)")
    cross = n / math.log2(n * W + 1)
    print(f"  croisement predit m ~ n/log2(nW+1) = {cross:.1f}")

    # ---- regime subexponentiel : m = O(n^eps), n croissant ----
    print("\n[D] Regime m petit fixe : DP subexponentiel (n croissant, m=3, W=n) :")
    print(f"  {'n':>3} | {'#etats max':>12} | {'2^n':>14} | {'etats/2^n':>10}")
    for n in [16, 20, 24, 28, 32]:
        m, W = 3, n
        bottom, top = make_random_circuit(n, m, W, rng)
        c, states = dp_count(n, bottom, top)
        print(f"  {n:>3} | {states:>12} | {2**n:>14} | "
              f"{states / 2**n:.2e}")
    print("  -> #etats croit POLYNOMIALEMENT (poly(n)^m), pas en 2^n :")
    print("     comptage subexponentiel -- BIEN MIEUX que 2^{n-n^eps}.")

    print("\n" + "=" * 72)
    print("VERDICT (honnete, folklore situe) :")
    print("  * THR o THR poids poly + PEU de portes (m = O(n^eps/log n)) :")
    print("    #SAT en 2^{o(n)} (DP etat-produit) -- battu par ce script.")
    print("  * regime 2^{n-n^eps} EXACT = portes = Theta(n) CREUSES (fils")
    print("    n^{1+eps}) : IPS 2013 / CSS 2016 / Kabanets-Lu (PUBLIE).")
    print("  * THR o THR DENSE (Theta(n) portes, fils n^2), meme poids poly :")
    print("    #SAT/SAT en 2^{n-n^eps} reste OUVERT = mur de Williams,")
    print("    ligne 7 (un tel algo donnerait NEXP hors THR o THR).")
    print("  Le poids polynomial du repo (tcomp) EST le levier du DP :")
    print("    poids exponentiels -> zero fusion -> force brute (cf. [B]).")


if __name__ == "__main__":
    main()
