"""
TACHE AS-004 -- (b) certification (7,2)/(7,1) par rayon raffine + cap 150M ;
(c) profil des fibres THR_w (structure du theoreme de padding).

(a) est documentaire : (7,4) dist=0 contre-verifie par le MILP independant
d'ATLAS-003 (eps*(7,4) = 0 sym et general, autre code, autre formulation).

(c) : le padding MAJ_{n+2}(x,a,b) decompose en 4 fibres de seuils
THR_{t-1}, THR_t, THR_t, THR_{t+1} sur x. L'egalite mesuree
dist^2(n+2) = 4 dist^2(n) suggere que les fibres contribuent egalement --
mesurer dist^2(n, d, THR_w) pour tout w tranche cette structure.
"""

from __future__ import annotations

import itertools
import sys
import time
from fractions import Fraction

import numpy as np
from sympy import Matrix, Rational

from svp_turbo import turbo_lll
from task_as002_cvp import kernel_basis, monomial_matrix
from task_as003_cvp2 import babai_ub, cvp_enum


def prepare_thr(n, d, thr):
    N = 1 << n
    f = [1 if bin(x).count("1") >= thr else 0 for x in range(N)]
    A, monos = monomial_matrix(n, d)
    m = len(monos)
    At = [[A[x][j] for x in range(N)] for j in range(m)]
    C = kernel_basis(At)
    C = [[int(t) for t in row] for row in turbo_lll(C)]
    r = len(C)
    Cf = np.array([sum(C[i][x] * f[x] for x in range(N)) for i in range(r)],
                  dtype=np.int64)
    Cnp = np.array(C, dtype=np.float64)
    G = Cnp @ Cnp.T
    Q = np.linalg.inv(G)
    M = np.linalg.cholesky(Q).T
    return C, Cf, M, r


def local_refine(M, Cf, r, u):
    """descente locale par coordonnee (pas +-2 = parite fixe)."""
    u = u.copy()
    val = float(np.sum((M @ u) ** 2))
    improved = True
    while improved:
        improved = False
        for i in range(r):
            for delta in (2.0, -2.0):
                u2 = u.copy()
                u2[i] += delta
                v2 = float(np.sum((M @ u2) ** 2))
                if v2 < val - 1e-12:
                    u, val = u2, v2
                    improved = True
    return u, val


def solve_cell(n, d, thr, cap=150_000_000):
    C, Cf, M, r = prepare_thr(n, d, thr)
    u0, ub = babai_ub(M, Cf, r)
    u1, ub1 = local_refine(M, Cf, r, u0)
    best, best_u, nodes, capped = cvp_enum(M, Cf, r, ub1 * (1 + 1e-9) + 1e-9,
                                           node_cap=cap)
    if best_u is None:
        best_u = u1
    Cm = Matrix(C)
    G = Cm * Cm.T
    uvec = Matrix([int(round(x)) for x in best_u])
    sol = G.LUsolve(uvec)
    val = (uvec.T * sol)[0, 0]
    dist2 = Rational(val, 4)
    q = Fraction(int(dist2.p), int(dist2.q) * (1 << n))
    return dist2, q, nodes, capped, r


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "thr"
    with open("as004_log.txt", "a", encoding="utf-8") as fh:
        if mode == "certif":
            for n, d in [(7, 2), (7, 1)]:
                t0 = time.time()
                dist2, q, nodes, capped, r = solve_cell(n, d, (n + 1) // 2)
                line = (f"[CERTIF] n={n} d={d} r={r} : dist^2={dist2} q={q} "
                        f"nodes={nodes}"
                        f"{' CAP (borne sup)' if capped else ' CERTIFIE'} "
                        f"({time.time()-t0:.0f}s)")
                print(line, flush=True)
                fh.write(line + "\n")
                fh.flush()
        else:
            # profil des fibres : dist^2(n, d, THR_w), n=5, tout w
            n = 5
            for d in (1, 2, 3):
                for w in range(1, n + 1):
                    t0 = time.time()
                    dist2, q, nodes, capped, r = solve_cell(n, d, w,
                                                            cap=30_000_000)
                    line = (f"[THR] n={n} d={d} w={w} : dist^2={dist2} "
                            f"q={q}{' CAP' if capped else ''} "
                            f"({time.time()-t0:.0f}s)")
                    print(line, flush=True)
                    fh.write(line + "\n")
                    fh.flush()


if __name__ == "__main__":
    main()
