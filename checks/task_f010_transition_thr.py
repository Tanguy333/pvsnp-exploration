"""
TACHE F-010 (zone 2) -- Transition de l'avantage composite : THR_t mod 6.

F-009 a montre : l'avantage composite (BBR) est massif pour OR (t=1, degre
~sqrt) et mort pour MAJ (t = n/2, degre lineaire). Ou meurt-il ?

Mesure : degre faible symetrique minimal de THR_{t,n} (S(w) = 0 mod m pour
w < t, != 0 pour w >= t) modulo 2, 3, 6, pour t = 1..ceil(n/2),
n in {16, 20, 24}. Avantage composite := min(d_2, d_3) - d_6.

Methode F-009 (noyaux binomiaux + couverture CRT), avec budget
d'enumeration : les cellules depassant le budget sont rapportees '>cap'
(honnete), jamais extrapolees.
"""

from __future__ import annotations

import itertools
from math import comb

import numpy as np

KER_CAP = 4_000_000      # taille max d'un noyau enumere
PAIR_BUDGET = 60_000_000  # budget de tests (|ker2| x |W0| x |ker3|) pour mod 6


def binom_rows(n: int, d: int, p: int, ws):
    return np.array([[comb(w, i) % p for i in range(d + 1)] for w in ws],
                    dtype=np.int64)


def nullspace_mod_p(A: np.ndarray, p: int):
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


def all_nullspace(basis, p: int, ncols: int):
    dim = len(basis)
    if p ** dim > KER_CAP:
        return None
    if dim == 0:
        return np.zeros((1, ncols), dtype=np.int64)
    B = np.array(basis, dtype=np.int64)
    coeffs = np.array(list(itertools.product(range(p), repeat=dim)),
                      dtype=np.int64)
    return (coeffs @ B) % p


def feasible_prime(n: int, t: int, d: int, p: int):
    lows = list(range(0, t))
    highs = list(range(t, n + 1))
    ker = all_nullspace(nullspace_mod_p(binom_rows(n, d, p, lows), p),
                        p, d + 1)
    if ker is None:
        return None  # cap
    H = binom_rows(n, d, p, highs)
    vals = (ker @ H.T) % p
    return bool(np.all(vals != 0, axis=1).any())


def feasible_mod6(n: int, t: int, d: int):
    lows = list(range(0, t))
    highs = list(range(t, n + 1))
    ker2 = all_nullspace(nullspace_mod_p(binom_rows(n, d, 2, lows), 2),
                         2, d + 1)
    ker3 = all_nullspace(nullspace_mod_p(binom_rows(n, d, 3, lows), 3),
                         3, d + 1)
    if ker2 is None or ker3 is None:
        return None
    H2 = binom_rows(n, d, 2, highs)
    H3 = binom_rows(n, d, 3, highs)
    v2all = (ker2 @ H2.T) % 2          # |ker2| x |highs|
    # cas u couvrant seul
    if bool(np.all(v2all != 0, axis=1).any()):
        return True
    v3all = (ker3 @ H3.T) % 3          # |ker3| x |highs|
    nz3 = (v3all != 0)
    budget = PAIR_BUDGET
    for r in range(v2all.shape[0]):
        W0 = np.where(v2all[r] == 0)[0]
        cost = nz3.shape[0] * len(W0)
        if cost > budget:
            return None  # budget epuise -- cap honnete
        budget -= cost
        if bool(np.all(nz3[:, W0], axis=1).any()):
            return True
    return False


def min_degree(n: int, t: int, m: int, d_cap: int = 24):
    for d in range(0, d_cap + 1):
        r = feasible_mod6(n, t, d) if m == 6 else feasible_prime(n, t, d, m)
        if r is None:
            return f">c{d}"  # cap atteint au degre d : minimum >= ? non conclu
        if r:
            return d
    return ">cap"


def main() -> None:
    print("TACHE F-010 -- transition de l'avantage composite : THR_t mod 6")
    print("=" * 70)
    for n in [16, 20, 24]:
        print(f"\nn = {n} :")
        print(f"  {'t':>3} | {'mod 2':>6} | {'mod 3':>6} | {'mod 6':>6} | "
              f"{'avantage min(d2,d3)-d6':>22}")
        print("  " + "-" * 58)
        for t in range(1, n // 2 + 2):
            d2 = min_degree(n, t, 2)
            d3 = min_degree(n, t, 3)
            d6 = min_degree(n, t, 6)
            if all(isinstance(x, int) for x in (d2, d3, d6)):
                adv = min(d2, d3) - d6
            else:
                adv = "?"
            print(f"  {t:>3} | {str(d2):>6} | {str(d3):>6} | {str(d6):>6} | "
                  f"{str(adv):>22}")
    print("\n('>cN' = budget/cap d'enumeration atteint en cherchant au degre N")
    print(" -- cellule non conclue, rapportee telle quelle.)")


if __name__ == "__main__":
    main()
