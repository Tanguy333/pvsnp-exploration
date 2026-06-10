"""
TACHE F-011, etape 1 -- Cerner la loi exacte de deg_6^sym(MAJ_n).

Donnees F-009 (plateaux : 3, 4, 8, 9, 16) avec une anomalie a n=16
(9 observe la ou "plus petite puissance de 2 ou 3 >= t" predit 8).
On etend a tous les n = 1..44 et on confronte aux candidats de loi :

  L1(n) : min{ q : q = 2^a ou 3^b, q >= t }            (puissance >= seuil)
  L2(n) : min{ q : q = 2^a ou 3^b, q >= t, ET il existe une strategie
          de couverture... }  -- a affiner selon les ecarts observes.

On tabule aussi, pour diagnostic, deg_2^sym et deg_3^sym et le degre
exact ou l'anomalie apparait.
"""

from __future__ import annotations

import itertools
from math import comb

import numpy as np

KER_CAP = 4_000_000
PAIR_BUDGET = 80_000_000


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


def all_nullspace(basis, p, ncols):
    dim = len(basis)
    if p ** dim > KER_CAP:
        return None
    if dim == 0:
        return np.zeros((1, ncols), dtype=np.int64)
    B = np.array(basis, dtype=np.int64)
    coeffs = np.array(list(itertools.product(range(p), repeat=dim)),
                      dtype=np.int64)
    return (coeffs @ B) % p


def feasible_prime(n, t, d, p):
    lows = list(range(0, t))
    highs = list(range(t, n + 1))
    ker = all_nullspace(nullspace_mod_p(binom_rows(n, d, p, lows), p), p, d + 1)
    if ker is None:
        return None
    H = binom_rows(n, d, p, highs)
    vals = (ker @ H.T) % p
    return bool(np.all(vals != 0, axis=1).any())


def feasible_mod6(n, t, d):
    lows = list(range(0, t))
    highs = list(range(t, n + 1))
    ker2 = all_nullspace(nullspace_mod_p(binom_rows(n, d, 2, lows), 2), 2, d + 1)
    ker3 = all_nullspace(nullspace_mod_p(binom_rows(n, d, 3, lows), 3), 3, d + 1)
    if ker2 is None or ker3 is None:
        return None
    H2 = binom_rows(n, d, 2, highs)
    H3 = binom_rows(n, d, 3, highs)
    v2all = (ker2 @ H2.T) % 2
    if bool(np.all(v2all != 0, axis=1).any()):
        return True
    v3all = (ker3 @ H3.T) % 3
    nz3 = (v3all != 0)
    budget = PAIR_BUDGET
    for r in range(v2all.shape[0]):
        W0 = np.where(v2all[r] == 0)[0]
        cost = nz3.shape[0] * max(len(W0), 1)
        if cost > budget:
            return None
        budget -= cost
        if bool(np.all(nz3[:, W0], axis=1).any()):
            return True
    return False


def min_degree(n, t, m, d_cap=30):
    for d in range(0, d_cap + 1):
        r = feasible_mod6(n, t, d) if m == 6 else feasible_prime(n, t, d, m)
        if r is None:
            return f">c{d}"
        if r:
            return d
    return ">cap"


def law_candidate(t):
    """ L1 : plus petite puissance de 2 ou de 3 >= t. """
    q = 1
    best = None
    a = 1
    while a < 4 * t:
        if a >= t:
            best = a if best is None else min(best, a)
            break
        a *= 2
    b = 1
    while b < 4 * t:
        if b >= t:
            best = b if best is None else min(best, b)
            break
        b *= 3
    return best


def main() -> None:
    print("TACHE F-011 (etape 1) -- loi de deg_6^sym(MAJ_n), n = 1..44")
    print("=" * 70)
    print(f"{'n':>3} {'t':>3} | {'d2':>4} {'d3':>4} {'d6':>4} | "
          f"{'L1=min pow>=t':>13} | ecart d6-L1")
    print("-" * 70)
    anomalies = []
    for n in range(1, 45):
        t = (n + 1) // 2
        d2 = min_degree(n, t, 2)
        d3 = min_degree(n, t, 3)
        d6 = min_degree(n, t, 6)
        L1 = law_candidate(t)
        ecart = (d6 - L1) if isinstance(d6, int) else "?"
        if isinstance(ecart, int) and ecart != 0:
            anomalies.append((n, t, d6, L1))
        print(f"{n:>3} {t:>3} | {str(d2):>4} {str(d3):>4} {str(d6):>4} | "
              f"{L1:>13} | {str(ecart):>6}")
    print("-" * 70)
    print(f"Anomalies vs L1 (n, t, d6, L1) : {anomalies}")


if __name__ == "__main__":
    main()
