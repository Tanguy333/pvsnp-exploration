"""
TACHE AS-006b -- reduction poids-espace du CVP de la Conjecture 13.

Hypothese (suggeree par l'isotropie AS-006 : exces identique sur les 21
paires => residu optimal symetrique) : l'optimum du CVP sur Z^{2^n} est
atteint par un decalage Z SYMETRIQUE (fonction de |x|). Alors :

  D(n,d,w) = min_{Z in Z^{n+1}} min_beta  (y - X beta)^T B (y - X beta),
  y = Z + f_w/2,  B = diag(C(n,k)),  X = [C(k,i)]_{k=0..n, i=0..d}

= CVP en dimension n-d : w~ = C y (C = noyau entier sature de X^T),
  forme Q_B = Y^T M Y (Y = C^T(CC^T)^{-1}, M = B - BX(X^T B X)^{-1}X^T B),
  u = 2 w~ parcourt 2Z^{n-d} + Cf.  Exact (sympy) + enumeration directe.

VALIDATION OBLIGATOIRE : concordance avec TOUTES les valeurs exactes
full-space (n=3,4,5 profils complets ; n=7 cellules certifiees). Toute
divergence = l'hypothese symetrique est FAUSSE a cette cellule (ce serait
une decouverte en soi : l'asymetrie aiderait le CVP l2).

Si validation OK : courbe q(n,d) pour n impair >> 7 -- le test numerique
direct du regime de la Conjecture 13.
"""

from __future__ import annotations

import sys
import time
from fractions import Fraction as F
from math import comb

import numpy as np
from sympy import Matrix, Rational

from task_as002_cvp import kernel_basis
from task_as003_cvp2 import cvp_enum


def weight_form(n, d):
    X = [[comb(k, i) for i in range(d + 1)] for k in range(n + 1)]
    B = [comb(n, k) for k in range(n + 1)]
    Xm = Matrix(X)
    Bm = Matrix.diag(*B)
    Mw = Bm - Bm * Xm * (Xm.T * Bm * Xm).inv() * Xm.T * Bm
    Xt = [[X[k][i] for k in range(n + 1)] for i in range(d + 1)]
    C = kernel_basis(Xt)                      # (n-d) x (n+1), sature
    Cm = Matrix(C)
    Y = Cm.T * (Cm * Cm.T).inv()
    Qb = Y.T * Mw * Y                          # (n-d) x (n-d) rationnel
    return C, Cm, Qb


def solve_weight(n, d, w):
    C, Cm, Qb = weight_form(n, d)
    r = len(C)
    f = [1 if k >= w else 0 for k in range(n + 1)]
    Cf = np.array([sum(C[i][k] * f[k] for k in range(n + 1))
                   for i in range(r)], dtype=np.int64)
    Qf = np.array([[float(Qb[i, j]) for j in range(r)] for i in range(r)])
    Mch = np.linalg.cholesky(Qf).T            # val_u = ||Mch u||^2 = 4 D
    # Babai + descente
    u = np.zeros(r)
    for i in range(r - 1, -1, -1):
        s = Mch[i, i + 1:] @ u[i + 1:]
        k0 = round((-s / Mch[i, i] - Cf[i]) / 2.0)
        u[i] = Cf[i] + 2 * k0
    ubf = float(np.sum((Mch @ u) ** 2))
    best, best_u, nodes, capped = cvp_enum(Mch, Cf, r, ubf * (1 + 1e-9) + 1e-9,
                                           node_cap=50_000_000)
    if best_u is None:
        best_u = u
    uv = Matrix([int(round(x)) for x in best_u])
    val = (uv.T * Qb * uv)[0, 0]
    D = Rational(val, 4)
    return F(int(D.p), int(D.q)), nodes, capped


# valeurs exactes full-space connues (AS-002..AS-005, certifiees)
KNOWN = {
    (3, 1, 2): F(1, 8), (3, 2, 2): F(0),
    (4, 1, 2): F(19, 64), (4, 2, 2): F(5, 64), (4, 3, 2): F(1, 64),
    (5, 1, 3): F(19, 32), (5, 2, 3): F(5, 32), (5, 3, 3): F(1, 32),
    (5, 3, 1): F(3, 64), (5, 3, 2): F(1, 32), (5, 3, 4): F(1, 32),
    (5, 3, 5): F(3, 64),
    (5, 2, 1): F(1, 8), (5, 2, 2): F(9, 32), (5, 2, 4): F(9, 32),
    (5, 2, 5): F(1, 8),
    (5, 1, 1): F(13, 64), (5, 1, 2): F(19, 32), (5, 1, 4): F(19, 32),
    (5, 1, 5): F(13, 64),
    (7, 3, 4): F(1, 8), (7, 2, 4): F(7, 8), (7, 3, 3): F(7, 32),
    (7, 3, 2): F(23, 64), (7, 3, 1): F(1, 8), (7, 4, 4): F(0),
    (7, 2, 1): F(99, 512), (7, 2, 6): F(93, 128),
}


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "valid"
    with open("as006b_poids.txt", "a", encoding="utf-8") as fh:
        if mode == "valid":
            ok = 0
            for (n, d, w), ref in sorted(KNOWN.items()):
                D, nodes, capped = solve_weight(n, d, w)
                match = (D == ref) and not capped
                ok += match
                line = (f"[VALID] (n={n},d={d},w={w}) : poids={D} vs "
                        f"full={ref} {'OK' if match else '** DIVERGENT **'}")
                print(line, flush=True)
                fh.write(line + "\n")
            tot = f"[VALID] {ok}/{len(KNOWN)} concordances"
            print(tot, flush=True)
            fh.write(tot + "\n")
        else:
            d = int(mode)
            for n in range(9, 26, 2):
                t0 = time.time()
                w = (n + 1) // 2
                D, nodes, capped = solve_weight(n, d, w)
                q = D / (1 << n)
                line = (f"[COURBE d={d}] n={n} : D={D} q=2^n-norm={q} "
                        f"(={float(q * 1024):.4f}/1024) "
                        f"{'CAP' if capped else ''} ({time.time()-t0:.0f}s)")
                print(line, flush=True)
                fh.write(line + "\n")
                fh.flush()


if __name__ == "__main__":
    main()
