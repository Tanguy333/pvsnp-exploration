"""
Base VERIFIEE pour l'exploration du regime DENSE de THR o THR a poids poly.
Regime dense = m = Theta(n) portes basses, chacune sur les n variables
(n^2 fils), poids entiers dans [-W, W], W = poly(n). C'est le mur de
Williams : #SAT/SAT en 2^{n-n^eps} y est OUVERT.

Ce module fournit :
  - make_dense_circuit(n, m, W, rng, rank=None) : circuit dense, option
    de matrice de poids de RANG borne (lever structurel a tester).
  - brute_count : force brute exacte (reference).
  - dp_count : DP etat-produit (renvoie #SAT et #etats max atteints).
  - fires_pattern : le vecteur (g_1..g_m) sur une entree (pour MITM).
Toutes les fonctions sont calibrees : brute vs dp doivent coincider.
"""

from __future__ import annotations

import itertools
from collections import defaultdict

import numpy as np


def make_dense_circuit(n, m, W, rng, rank=None):
    """ m portes basses denses (chacune depend des n variables).
        rank=r : matrice de poids m x n de rang <= r (lever structurel). """
    if rank is None:
        Wmat = rng.integers(-W, W + 1, size=(m, n))
    else:
        A = rng.integers(-W, W + 1, size=(m, rank))
        B = rng.integers(-3, 4, size=(rank, n))
        Wmat = (A @ B)
        # renormaliser pour garder des entrees raisonnables
        mx = np.abs(Wmat).max() or 1
        Wmat = np.round(Wmat * W / mx).astype(int)
    bottom = []
    for j in range(m):
        w = [int(Wmat[j, i]) for i in range(n)]
        lo = sum(min(0, wi) for wi in w)
        hi = sum(max(0, wi) for wi in w)
        t = int(rng.integers(lo, hi + 1)) if hi > lo else lo
        bottom.append((w, t))
    v = [int(rng.integers(1, W + 1)) for _ in range(m)]
    T = int(rng.integers(1, sum(v) + 1)) if m else 0
    return bottom, (v, T)


def gate_fires(w, t, x):
    return 1 if sum(w[i] for i in range(len(w)) if x[i]) >= t else 0


def evaluate(n, bottom, top, x):
    v, T = top
    acc = sum(v[j] for j, (w, t) in enumerate(bottom) if gate_fires(w, t, x))
    return 1 if acc >= T else 0


def brute_count(n, bottom, top):
    return sum(1 for x in itertools.product((0, 1), repeat=n)
               if evaluate(n, bottom, top, x))


def dp_count(n, bottom, top, cap=None):
    """ DP etat-produit. cap : si #etats depasse cap, on abandonne le DP
        et on renvoie (None, cap+1) -- utile pour mesurer le croisement
        sans exploser la memoire. """
    m = len(bottom)
    v, T = top
    states = {tuple([0] * m): 1}
    max_states = 1
    for i in range(n):
        new = defaultdict(int)
        incr = tuple(bottom[j][0][i] for j in range(m))
        for st, cnt in states.items():
            new[st] += cnt
            st1 = tuple(st[j] + incr[j] for j in range(m))
            new[st1] += cnt
        states = new
        max_states = max(max_states, len(states))
        if cap is not None and len(states) > cap:
            return None, len(states)
    total = 0
    for st, cnt in states.items():
        acc = sum(v[j] for j in range(m) if st[j] >= bottom[j][1])
        if acc >= T:
            total += cnt
    return total, max_states


if __name__ == "__main__":
    rng = np.random.default_rng(1)
    print("Calibration base dense (brute == dp) :")
    ok = True
    for _ in range(5):
        n = 14
        m = int(rng.integers(6, 14))          # dense : m ~ n
        W = n
        bottom, top = make_dense_circuit(n, m, W, rng)
        cb = brute_count(n, bottom, top)
        cd, st = dp_count(n, bottom, top)
        match = cb == cd
        ok &= match
        print(f"  n={n} m={m} W={W} : brute={cb} dp={cd} etats={st} "
              f"{'OK' if match else 'ECART'}")
    print("calibration:", "OK" if ok else "ECHEC")
