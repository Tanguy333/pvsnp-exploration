"""
TACHE AS-015 -- LA RECURSION RENFORCEE (preuve + verifications).

Derivation (voir tasks/done/AS-015.md) : en fixant UNE variable,
p(x,a) = p0(x) + a q(x) avec deg q <= d-1 ; moindres carres orthogonaux
joints => IDENTITE EXACTE

  D(n+1,d,t) = min_{S == Z' (mod 2)} [ 1/2 ||P_d(S + g/2)||^2
                                     + 1/2 ||P_{d-1}(Z' + delta/2)||^2 ]
  g = f_t + f_{t-1},  delta = f_t - f_{t-1} = -Delta_{t-1},

et en decouplant la parite, la BORNE

  D(n+1,d,t) >= 1/2 D_Delta(n,d,t-1) + 1/2 D_Delta(n,d-1,t-1).

Verifications :
 1. IDENTITE exacte par force brute (les minima couples se separent par
    motif de parite pi in {0,1}^{2^n}) sur (3,1,2) et (4,2,2) ;
 2. INEGALITE sur toutes les cellules a LHS connu (solveur poids-espace
    pour les classes Delta).
"""

from __future__ import annotations

import itertools
import time
from fractions import Fraction as F
from math import comb

import numpy as np
from sympy import Matrix, Rational

from task_as002_cvp import monomial_matrix
from task_as003_cvp2 import cvp_enum
from task_as002_cvp import kernel_basis
from svp_turbo import turbo_lll


def projector(n, d):
    A, monos = monomial_matrix(n, d)
    Am = Matrix(A)
    P = Matrix.eye(1 << n) - Am * (Am.T * Am).inv() * Am.T
    N = 1 << n
    return np.array([[float(P[i, j]) for j in range(N)] for i in range(N)]), P


def brute_coupled(n1, d, t):
    """RHS de l'identite : min sur S==Z' (mod 2) — separable par parite."""
    n = n1 - 1
    N = 1 << n
    wt = [bin(x).count("1") for x in range(N)]
    ft = np.array([1.0 if w >= t else 0.0 for w in wt])
    ft1 = np.array([1.0 if w >= t - 1 else 0.0 for w in wt])
    g2 = (ft + ft1) / 2.0
    dl2 = (ft - ft1) / 2.0
    Pd, _ = projector(n, d)
    Pd1, _ = projector(n, d - 1)
    # candidats par coordonnee : v in {pi-2, pi, pi+2} (cible dans [-1,1])
    best = None
    for pi in itertools.product((0, 1), repeat=N):
        cands = [np.array(v, dtype=float)
                 for v in itertools.product(*[(p - 2, p, p + 2) for p in pi])]
        Vs = np.stack(cands)
        h1 = np.min(np.sum((Vs + g2) @ Pd.T * ((Vs + g2) @ Pd.T), axis=1))
        h2 = np.min(np.sum((Vs + dl2) @ Pd1.T * ((Vs + dl2) @ Pd1.T), axis=1))
        val = 0.5 * h1 + 0.5 * h2
        if best is None or val < best:
            best = val
    return best


def solve_weight_target(n, d, f):
    """solveur poids-espace pour une cible 0/1 quelconque (dont Delta_w)."""
    from task_as006b import weight_form
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
    uv = Matrix([int(round(x)) for x in bu])
    D = Rational((uv.T * Qb * uv)[0, 0], 4)
    return F(int(D.p), int(D.q)), capped


def D_delta(n, d, w):
    if d < 1:
        # d = 0 : distance a l'espace des constantes
        pass
    f = [1 if k == w else 0 for k in range(n + 1)]
    return solve_weight_target(n, d, f)


def main():
    print("=== 1. IDENTITE exacte (force brute, parites separees) ===")
    for (n1, d, t, lhs) in [(3, 1, 2, F(1, 8)), (4, 2, 2, F(5, 64))]:
        t0 = time.time()
        rhs = brute_coupled(n1, d, t)
        ok = abs(rhs - float(lhs)) < 1e-9
        print(f"  (n+1={n1}, d={d}, t={t}) : LHS connu = {lhs} ; "
              f"RHS couple = {rhs:.6f}  [{'IDENTITE VERIFIEE' if ok else '** ECART **'}] "
              f"({time.time()-t0:.0f}s)", flush=True)

    print("=== 2. INEGALITE D(n+1,d,t) >= 1/2 D_D(n,d,t-1) + 1/2 D_D(n,d-1,t-1) ===")
    known = {(5, 2, 3): F(5, 32), (5, 3, 3): F(1, 32), (7, 2, 4): F(7, 8),
             (7, 3, 4): F(1, 8), (9, 3, 5): F(387, 512),
             (11, 3, 6): F(63, 16), (13, 3, 7): F(9749, 512)}
    for (n1, d, t), lhs in sorted(known.items()):
        n = n1 - 1
        Da, ca = D_delta(n, d, t - 1)
        Db, cb = D_delta(n, d - 1, t - 1)
        rhs = F(1, 2) * Da + F(1, 2) * Db
        ok = lhs >= rhs
        print(f"  ({n1},{d},{t}) : {lhs} >= {rhs}"
              f" = (1/2)({Da}) + (1/2)({Db})"
              f"{' ~' if ca or cb else ''}  [{'OK' if ok else '** VIOLATION **'}]",
              flush=True)


if __name__ == "__main__":
    main()
