"""
TACHE F-011, etape 2 -- Tester la prediction deg_6^sym(MAJ_32) = 27.

C-F011 predit : t = 16 = 2^4, C(32,16) = 0 mod 3 -> la puissance 16
echoue, valeur = puissance suivante = 27.

Note d'honnetete : a n=32, e_27 seul ne couvre PAS les poids 16..26
(C(w,27) = 0 pour w < 27). Si d=27 est faisable c'est par combinaison
dans le noyau ; si d in [16, 26] est faisable, la conjecture est FAUSSE.
Ce script teste d = 16..28 exhaustivement (noyaux complets, couverture
CRT), avec rapport par degre au fil de l'eau.

Egalement : n = 31 (controle : prediction 16, pas de w = 32) et
n = 33..36 (prediction 27 via L1 directement).
"""

from __future__ import annotations

import itertools
import time
from math import comb

import numpy as np

KER_CAP = 5_000_000


def binom_rows(n, d, p, ws):
    return np.array([[comb(w, i) % p for i in range(d + 1)] for w in ws],
                    dtype=np.int64)


def nullspace_mod_p(A, p):
    A = A.copy() % p
    r, c = A.shape
    pivots = []
    row = 0
    for col in range(c):
        piv = None
        for i in range(row, r):
            if A[i, col] % p != 0:
                piv = i
                break
        if piv is None:
            continue
        A[[row, piv]] = A[[piv, row]]
        inv = pow(int(A[row, col]), p - 2, p) if p > 2 else 1
        A[row] = (A[row] * inv) % p
        for i in range(r):
            if i != row and A[i, col] % p != 0:
                A[i] = (A[i] - A[i, col] * A[row]) % p
        pivots.append(col)
        row += 1
        if row == r:
            break
    free = [j for j in range(c) if j not in pivots]
    basis = []
    for fcol in free:
        v = np.zeros(c, dtype=np.int64)
        v[fcol] = 1
        for i, pcol in enumerate(pivots):
            v[pcol] = (-A[i, fcol]) % p
        basis.append(v % p)
    return basis


def kernel_matrix(n, t, d, p):
    """ Tous les elements du noyau, ou None si > KER_CAP. """
    lows = list(range(0, t))
    basis = nullspace_mod_p(binom_rows(n, d, p, lows), p)
    dim = len(basis)
    if p ** dim > KER_CAP:
        return None, dim
    if dim == 0:
        return np.zeros((1, d + 1), dtype=np.int64), 0
    B = np.array(basis, dtype=np.int64)
    coeffs = np.array(list(itertools.product(range(p), repeat=dim)),
                      dtype=np.int64)
    return (coeffs @ B) % p, dim


def feasible_mod6(n, t, d, verbose=False):
    highs = list(range(t, n + 1))
    ker2, dim2 = kernel_matrix(n, t, d, 2)
    ker3, dim3 = kernel_matrix(n, t, d, 3)
    if ker2 is None or ker3 is None:
        return None
    H2 = binom_rows(n, d, 2, highs)
    H3 = binom_rows(n, d, 3, highs)
    v2all = (ker2 @ H2.T) % 2
    if bool(np.all(v2all != 0, axis=1).any()):
        return True
    nz3 = ((ker3 @ H3.T) % 3) != 0   # |ker3| x |highs|
    if verbose:
        print(f"      (dim2={dim2}, dim3={dim3}, |ker2|={len(ker2)}, "
              f"|ker3|={len(ker3)})", flush=True)
    # ordonner les u par |W0| croissant (les plus prometteurs d'abord)
    w0sizes = (v2all == 0).sum(axis=1)
    order = np.argsort(w0sizes)
    for r in order:
        W0 = np.where(v2all[r] == 0)[0]
        if len(W0) == 0:
            return True
        if bool(np.all(nz3[:, W0], axis=1).any()):
            return True
    return False


def main() -> None:
    print("TACHE F-011 etape 2 -- prediction deg_6^sym(MAJ_32) = 27 ?")
    print("=" * 66, flush=True)

    # Controle n=31 (t=16, pas de w=32 : prediction 16)
    print("\nControle n=31 (prediction : 16)", flush=True)
    for d in [15, 16]:
        t0 = time.time()
        r = feasible_mod6(31, 16, d)
        print(f"  d={d} : {'faisable' if r else ('cap' if r is None else 'infaisable')}"
              f"   ({time.time()-t0:.0f}s)", flush=True)

    # Le test central : n=32, t=16, d = 16..28
    print("\nTest central n=32, t=16 (C-F011 predit : infaisable jusqu'a 26, "
          "faisable a 27)", flush=True)
    answer = None
    for d in range(16, 29):
        t0 = time.time()
        r = feasible_mod6(32, 16, d, verbose=(d in (16, 26, 27)))
        lab = 'FAISABLE' if r else ('>cap (non conclu)' if r is None else 'infaisable')
        print(f"  d={d} : {lab}   ({time.time()-t0:.0f}s)", flush=True)
        if r:
            answer = d
            break
    if answer is not None:
        verdict = ("PREDICTION CONFIRMEE" if answer == 27 else
                   f"PREDICTION REFUTEE : valeur = {answer}, pas 27")
        print(f"\n  deg_6^sym(MAJ_32) = {answer} -> {verdict}", flush=True)

    # n = 33..36 (predictions 27 via L1)
    print("\nComplements n=33..36 (prediction : 27)", flush=True)
    for n in [33, 34, 35, 36]:
        t = (n + 1) // 2
        for d in range(26, 29):
            r = feasible_mod6(n, t, d)
            if r:
                print(f"  n={n} (t={t}) : deg = {d}"
                      f"   [{'OK' if d == 27 else 'ecart'}]", flush=True)
                break
            if r is None:
                print(f"  n={n} (t={t}) : >cap a d={d}", flush=True)
                break


if __name__ == "__main__":
    main()
