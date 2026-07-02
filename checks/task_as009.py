"""
TACHE AS-009 -- LA DIAGONALE : D(2d+c, d, centre) exact pour c = -1, 1, 3
et d croissant. Etape MESURER de la boucle mesurer -> deviner la loi ->
prouver (mode operatoire V-032 / V11 / lemme de padding).

Motivation (AS-008) : la recursion de padding transporte les bornes en n
a perte poly pres -- toute la Conjecture 13 se concentre sur la diagonale
n0 ~ 2d. Si D(2d+c, d) a une forme close, la conjecture devient
attaquable par algebre verifiable ; sinon, cloture du fil.

Sorties par cellule : D exact (min sur Z, poids-espace -- conditionnel a
l'hypothese symetrique verifiee 28/28 a n<=7), D0 exact (Z = 0, la queue
de Krawtchouk pure), et le ratio D/D0. Bancarisation ligne a ligne.
"""

from __future__ import annotations

import sys
import time
from fractions import Fraction as F

import numpy as np
from sympy import Matrix, Rational

from task_as003_cvp2 import cvp_enum
from task_as006b import weight_form


def diag_cell(n, d, cap=60_000_000):
    C, Cm, Qb = weight_form(n, d)
    r = len(C)
    w = (n + 1) // 2
    f = [1 if k >= w else 0 for k in range(n + 1)]
    Cf = np.array([sum(C[i][k] * f[k] for k in range(n + 1))
                   for i in range(r)], dtype=np.int64)
    # Z = 0 : u = Cf
    u0v = Matrix([int(x) for x in Cf])
    D0 = Rational((u0v.T * Qb * u0v)[0, 0], 4)
    Qf = np.array([[float(Qb[i, j]) for j in range(r)] for i in range(r)])
    Mch = np.linalg.cholesky(Qf).T
    u = np.zeros(r)
    for i in range(r - 1, -1, -1):
        s = Mch[i, i + 1:] @ u[i + 1:]
        k0 = round((-s / Mch[i, i] - Cf[i]) / 2.0)
        u[i] = Cf[i] + 2 * k0
    ubf = float(np.sum((Mch @ u) ** 2))
    best, best_u, nodes, capped = cvp_enum(Mch, Cf, r, ubf * (1 + 1e-9) + 1e-9,
                                           node_cap=cap)
    if best_u is None:
        best_u = u
    uv = Matrix([int(round(x)) for x in best_u])
    D = Rational((uv.T * Qb * uv)[0, 0], 4)
    return (F(int(D.p), int(D.q)), F(int(D0.p), int(D0.q)), capped, nodes)


def main():
    dmax = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    with open("as009_diagonale.txt", "a", encoding="utf-8") as fh:
        for c in (-1, 1, 3):
            head = f"=== diagonale c={c} : n = 2d{c:+d}, seuil centre ==="
            print(head, flush=True)
            fh.write(head + "\n")
            for d in range(1, dmax + 1):
                n = 2 * d + c
                if n < 3 or n % 2 == 0 or n - d < 1:
                    continue
                t0 = time.time()
                try:
                    D, D0, capped, nodes = diag_cell(n, d)
                    ratio = None if D0 == 0 else D / D0
                    line = (f"d={d:>2} n={n:>2} : D={D}  D*2^n={D * (1 << n)}  "
                            f"D0={D0}  D/D0={ratio}  "
                            f"{'CAP(borne sup)' if capped else 'exact'} "
                            f"({time.time()-t0:.0f}s)")
                except Exception as e:
                    line = f"d={d:>2} n={n:>2} : ECHEC {type(e).__name__}: {e}"
                print(line, flush=True)
                fh.write(line + "\n")
                fh.flush()


if __name__ == "__main__":
    main()
