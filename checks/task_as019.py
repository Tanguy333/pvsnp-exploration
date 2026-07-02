"""
TACHE AS-019 -- le couplage gratuit du premier pas (7/7) : explication F2.

Theorie : l'egalite D_MAJ(n+1,d) = 1/2 D_Delta(n,d) + 1/2 D_Delta(n,d-1)
vaut ssi des optima S* (terme d) et Z'* (terme d-1) existent avec
S* == Z'* (mod 2). La liberte de parite d'un optimum est EXACTEMENT
Par(V_d cap Z^{n+1}) = span_F2{ (C(w,i) mod 2)_w : i <= d } (les
polynomes a valeurs entieres = base binomiale ; Lucas). Condition
suffisante de gratuite :

  p_A XOR p_B  in  span_F2{ C(w,i) mod 2 : i <= d }

ou p_A, p_B = parites (vecteurs de niveaux mod 2) d'optima quelconques
des deux termes. On extrait p_A, p_B des solutions CVP exactes
(Z entier resolu par reduction unimodulaire de C) et on teste.
"""

from __future__ import annotations

from fractions import Fraction as F
from math import comb

import numpy as np
from sympy import Matrix, Rational

from task_as003_cvp2 import cvp_enum
from task_as006b import weight_form


def solve_with_u(n, d, f):
    C, Cm, Qb = weight_form(n, d)
    r = len(C)
    Cf = np.array([sum(C[i][k] * f[k] for k in range(n + 1))
                   for i in range(r)], dtype=np.int64)
    Qf = np.array([[float(Qb[i, j]) for j in range(r)] for i in range(r)])
    M = np.linalg.cholesky(Qf).T
    u = np.zeros(r)
    for i in range(r - 1, -1, -1):
        s = M[i, i + 1:] @ u[i + 1:]
        u[i] = Cf[i] + 2 * round((-s / M[i, i] - Cf[i]) / 2.0)
    ubf = float(np.sum((M @ u) ** 2))
    best, bu, nodes, capped = cvp_enum(M, Cf, r, ubf * (1 + 1e-9) + 1e-9,
                                       node_cap=40_000_000)
    if bu is None:
        bu = u
    uv = [int(round(x)) for x in bu]
    val = Rational((Matrix(uv).T * Qb * Matrix(uv))[0, 0], 4)
    return C, Cf, uv, val


def integer_solve(C, v):
    """Z entier avec C Z = v (C sature r x (n+1)) via reduction de colonnes."""
    r, m = len(C), len(C[0])
    A = [list(row) for row in C]
    U = [[1 if i == j else 0 for j in range(m)] for i in range(m)]
    piv = 0
    for row in range(r):
        while True:
            nz = [j for j in range(piv, m) if A[row][j] != 0]
            if not nz:
                break
            jm = min(nz, key=lambda j: abs(A[row][j]))
            for rr in range(r):
                A[rr][piv], A[rr][jm] = A[rr][jm], A[rr][piv]
            for rr in range(m):
                U[rr][piv], U[rr][jm] = U[rr][jm], U[rr][piv]
            done = True
            for j in range(piv + 1, m):
                if A[row][j]:
                    q = -(A[row][j] // A[row][piv])
                    for rr in range(r):
                        A[rr][j] += q * A[rr][piv]
                    for rr in range(m):
                        U[rr][j] += q * U[rr][piv]
                    if A[row][j]:
                        done = False
            if done:
                break
        piv += 1
    H = Matrix([[A[i][j] for j in range(r)] for i in range(r)])
    x = H.LUsolve(Matrix(v))
    assert all(xi == int(xi) for xi in x), "H non unimodulaire ?"
    xs = [int(xi) for xi in x] + [0] * (m - r)
    Z = [sum(U[i][j] * xs[j] for j in range(m)) for i in range(m)]
    for i in range(r):
        assert sum(C[i][k] * Z[k] for k in range(m)) == v[i]
    return Z


def parity_of_optimum(n, d, w):
    f = [1 if k == w else 0 for k in range(n + 1)]
    C, Cf, u, val = solve_with_u(n, d, f)
    v = [(u[i] - Cf[i]) // 2 for i in range(len(C))]
    Z = integer_solve(C, v)
    return [z % 2 for z in Z], val


def lucas_span_contains(n, d, vec):
    """vec (n+1 bits) in span_F2{C(w,i) mod 2 : i<=d} ?"""
    rows = [[comb(w, i) % 2 for w in range(n + 1)] for i in range(d + 1)]
    rows.append(list(vec))
    # rang F2 avec/sans vec
    def rank2(rs):
        rs = [int(''.join(map(str, r)), 2) for r in rs]
        rk = 0
        for b in range(n, -1, -1):
            piv = None
            for i, x in enumerate(rs):
                if (x >> b) & 1:
                    piv = i
                    break
            if piv is None:
                continue
            p = rs.pop(piv)
            rs = [x ^ p if (x >> b) & 1 else x for x in rs]
            rk += 1
        return rk
    base = [[comb(w, i) % 2 for w in range(n + 1)] for i in range(d + 1)]
    return rank2(base + [list(vec)]) == rank2(base)


def main():
    cells = [(4, 2, 2), (4, 3, 2), (6, 2, 3), (6, 3, 3), (8, 3, 4),
             (10, 3, 5), (12, 3, 6)]
    print("cellule (n, d_haut, w) : parites des optima Delta aux degres d et d-1,")
    print("p_A xor p_B in span_F2{Lucas <= d} ? (condition SUFFISANTE de gratuite)")
    for (n, d, w) in cells:
        pA, vA = parity_of_optimum(n, d, w)
        pB, vB = parity_of_optimum(n, d - 1, w)
        x = [a ^ b for a, b in zip(pA, pB)]
        inspan = lucas_span_contains(n, d, x)
        print(f"  (n={n:>2}, d={d}, w={w}) : pA={''.join(map(str,pA))} "
              f"pB={''.join(map(str,pB))} xor={''.join(map(str,x))} "
              f"-> {'GRATUIT (dans le span)' if inspan else 'HORS SPAN (pour CES optima)'}",
              flush=True)


if __name__ == "__main__":
    main()
