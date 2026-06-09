"""
TACHE F-009 (zone 2 de l'Atlas) -- Degres faibles de MAJORITY modulo 6.

CONTEXTE : la conjecture ouverte depuis 1987 (audit A-004, verbatim
Goldreich : "we do not know a proof that AC0[6] cannot compute Majority").
B-005 a mesure OR mod 6 (bornes connues, BBR 1994). Ici on mesure LA
fonction du probleme ouvert : la magie composite qui effondre le degre de
OR opere-t-elle sur MAJ ?

Notion (representation faible symetrique, convention BBR) :
  P = sum_{i=0}^{d} a_i e_i (a_0 = terme constant), a_i in Z_m.
  Valeur sur le poids w : S(w) = sum_i a_i C(w, i) mod m.
  P represente faiblement MAJ_n (seuil t = ceil(n/2)) si :
      S(w) = 0 (mod m)  pour tout w < t      [zeros forces]
      S(w) != 0 (mod m) pour tout w >= t     [couverture]

Methode :
  - m premier p : les zeros forces definissent un systeme lineaire sur
    F_p -> base du noyau par Gauss ; enumerer le noyau et tester la
    couverture. min d = plus petit d faisable.
  - m = 6 : CRT -- u dans le noyau F_2, v dans le noyau F_3, et pour tout
    w >= t : S_2(w) != 0 OU S_3(w) != 0.
"""

from __future__ import annotations

import itertools
from math import comb

import numpy as np


def binom_rows(n: int, d: int, p: int, ws):
    """ Matrice [C(w,i) mod p] pour w dans ws, i = 0..d. """
    return np.array([[comb(w, i) % p for i in range(d + 1)] for w in ws],
                    dtype=np.int64)


def nullspace_mod_p(A: np.ndarray, p: int) -> list[np.ndarray]:
    """ Base du noyau de A sur F_p (Gauss). A : r x c. """
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


def all_nullspace(basis: list[np.ndarray], p: int, ncols: int,
                  cap: int = 2_000_000):
    """ Tous les elements du noyau (si p^dim <= cap). """
    dim = len(basis)
    if p ** dim > cap:
        return None
    if dim == 0:
        return [np.zeros(ncols, dtype=np.int64)]
    B = np.array(basis, dtype=np.int64)
    out = []
    for coeffs in itertools.product(range(p), repeat=dim):
        out.append((np.array(coeffs, dtype=np.int64) @ B) % p)
    return out


def feasible_prime(n: int, t: int, d: int, p: int) -> bool:
    lows = list(range(0, t))
    highs = list(range(t, n + 1))
    A_low = binom_rows(n, d, p, lows)
    ker = all_nullspace(nullspace_mod_p(A_low, p), p, d + 1)
    if ker is None:
        return False  # noyau trop grand pour enumeration -- rapporte comme cap
    A_high = binom_rows(n, d, p, highs)
    for v in ker:
        vals = (A_high @ v) % p
        if np.all(vals != 0):
            return True
    return False


def feasible_mod6(n: int, t: int, d: int) -> bool:
    lows = list(range(0, t))
    highs = list(range(t, n + 1))
    ker2 = all_nullspace(nullspace_mod_p(binom_rows(n, d, 2, lows), 2), 2, d + 1)
    ker3 = all_nullspace(nullspace_mod_p(binom_rows(n, d, 3, lows), 3), 3, d + 1)
    if ker2 is None or ker3 is None:
        return False
    H2 = binom_rows(n, d, 2, highs)
    H3 = binom_rows(n, d, 3, highs)
    vals3 = [(H3 @ v) % 3 for v in ker3]
    for u in ker2:
        v2 = (H2 @ u) % 2
        W0 = np.where(v2 == 0)[0]
        if len(W0) == 0:
            return True
        for v3 in vals3:
            if np.all(v3[W0] != 0):
                return True
    return False


def min_degree(n: int, m: int, d_cap: int):
    t = (n + 1) // 2
    for d in range(0, d_cap + 1):
        if m == 6:
            if feasible_mod6(n, t, d):
                return d
        else:
            if feasible_prime(n, t, d, m):
                return d
    return None


def main() -> None:
    print("TACHE F-009 -- degre faible symetrique de MAJ_n (seuil ceil(n/2))")
    print("zone 2 de l'Atlas : la fonction de la conjecture ouverte de 1987")
    print("=" * 68)
    print(f"{'n':>4} | {'mod 2':>6} | {'mod 3':>6} | {'mod 6':>6} | {'OR mod 6 (B-005)':>16}")
    print("-" * 68)
    or6 = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 2, 7: 2, 8: 2, 9: 3, 10: 3,
           12: 3, 14: 3, 16: 3, 18: 3, 20: 3, 24: 3, 27: 3, 30: 4}
    caps = {2: 24, 3: 24, 6: 24}
    for n in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 24, 27, 30]:
        row = {}
        for m in (2, 3, 6):
            row[m] = min_degree(n, m, caps[m])
        fmt = lambda x: str(x) if x is not None else ">cap"
        print(f"{n:>4} | {fmt(row[2]):>6} | {fmt(row[3]):>6} | "
              f"{fmt(row[6]):>6} | {str(or6.get(n, '')):>16}")
    print("-" * 68)
    print("Question : la magie composite (OR : degre ~sqrt) opere-t-elle")
    print("sur MAJ ? Si mod 6 ~ mod 2/3 -> non (coherent avec 1987 ouvert).")
    print("Si mod 6 s'effondre -> donnee neuve sur le front.")


if __name__ == "__main__":
    main()
