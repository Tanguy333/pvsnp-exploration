"""
TACHE AS-003 -- CVP direct pour la Conjecture 13 : rayon serre (Babai),
deux conventions de seuil, n = 7 (le point decisif de la n-invariance).

Ameliorations vs AS-002 :
 - enumeration CVP DIRECTE sur la forme quadratique Q = G^{-1}
   (G = Gram du noyau sature LLL-reduit), variables a parite fixee
   u = Cf + 2v -- plus de plongement de Kannan, plus de flood k=0 ;
 - rayon initial = Babai (nearest plane) + descente locale => l'arbre
   d'enumeration reste minuscule (fix de l'OOM de (6,3)) ;
 - conventions : MAJ 'inclusive' (|x| >= ceil((n+1)/2), la notre) et
   'stricte' (|x| > n/2, celle de KV pour n pair) ;
 - verification EXACTE (sympy, rationnels) de la valeur optimale ;
   geometrie float (Cholesky) -> completude sous reserve de
   conditionnement, rayon gonfle de 1e-9 relatif, cap de noeuds honnete.

Validation obligatoire : reproduire la table AS-002 (n=3,4,5).
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


def build_f(n, strict):
    thr = (n // 2) + 1 if strict else (n + 1) // 2
    return [1 if bin(x).count("1") >= thr else 0 for x in range(1 << n)], thr


def prepare(n, d, strict=False):
    N = 1 << n
    f, thr = build_f(n, strict)
    A, monos = monomial_matrix(n, d)
    m = len(monos)
    At = [[A[x][j] for x in range(N)] for j in range(m)]
    C = kernel_basis(At)
    C = [[int(t) for t in row] for row in turbo_lll(C)]
    r = len(C)
    assert r == N - m
    Cf = np.array([sum(C[i][x] * f[x] for x in range(N)) for i in range(r)],
                  dtype=np.int64)
    Cnp = np.array(C, dtype=np.float64)
    G = Cnp @ Cnp.T
    Q = np.linalg.inv(G)
    M = np.linalg.cholesky(Q).T          # upper : val(u) = ||M u||^2
    return C, Cf, M, r, thr


def babai_ub(M, Cf, r):
    """Babai nearest-plane sur u = Cf + 2v (parite fixee) : bon rayon."""
    u = np.zeros(r)
    for i in range(r - 1, -1, -1):
        s = M[i, i + 1:] @ u[i + 1:]
        center = -s / M[i, i]
        k = round((center - Cf[i]) / 2.0)
        u[i] = Cf[i] + 2 * k
    return u, float(np.sum((M @ u) ** 2))


def cvp_enum(M, Cf, r, radius2, node_cap=20_000_000):
    """DFS exact (geometrie float) : min ||M u||^2, u_i = Cf_i + 2 v_i."""
    best = radius2
    best_u = None
    nodes = 0
    capped = False
    u = np.zeros(r)
    part = np.zeros(r + 1)               # somme partielle des carres

    def rec(i):
        nonlocal best, best_u, nodes, capped
        if capped:
            return
        if i < 0:
            if part[0] < best:
                best = part[0]
                best_u = u.copy()
            return
        s = M[i, i + 1:] @ u[i + 1:]
        center = -s / M[i, i]
        k0 = round((center - Cf[i]) / 2.0)
        step = 0
        while True:
            done = 0
            for k in ({k0} if step == 0 else {k0 - step, k0 + step}):
                nodes += 1
                if nodes > node_cap:
                    capped = True
                    return
                ui = Cf[i] + 2 * k
                contrib = (M[i, i] * ui + s) ** 2
                if part[i + 1] + contrib <= best + 1e-12:
                    u[i] = ui
                    part[i] = part[i + 1] + contrib
                    rec(i - 1)
                    done += 1
            if done == 0 and step > 0:
                break
            step += 1

    rec(r - 1)
    return best, best_u, nodes, capped


def rho_exact3(n, d, strict=False):
    C, Cf, M, r, thr = prepare(n, d, strict)
    u0, ub = babai_ub(M, Cf, r)
    best, best_u, nodes, capped = cvp_enum(M, Cf, r, ub * (1 + 1e-9) + 1e-9)
    if best_u is None:
        best_u = u0
    # verification exacte : dist^2 = (u^T G^{-1} u)/4 en rationnels
    Cm = Matrix(C)
    G = Cm * Cm.T
    uvec = Matrix([int(round(x)) for x in best_u])
    sol = G.LUsolve(uvec)
    val = (uvec.T * sol)[0, 0]
    dist2 = Rational(val, 4)
    q = Fraction(int(dist2.p), int(dist2.q) * (1 << n))
    rho = float(dist2) ** 0.5 / 2 ** (n / 2)
    return dict(n=n, d=d, r=r, thr=thr, dist2=dist2, q=q, rho=rho,
                nodes=nodes, capped=capped)


def run(cells, tag):
    with open("as003_profile.txt", "a", encoding="utf-8") as fh:
        for n, d, strict in cells:
            t0 = time.time()
            try:
                R = rho_exact3(n, d, strict)
                line = (f"[{tag}] n={n} d={d} thr={R['thr']} r={R['r']} : "
                        f"dist^2={R['dist2']} q={R['q']} rho={R['rho']:.5f} "
                        f"nodes={R['nodes']}"
                        f"{' CAP ATTEINT (borne sup seulement)' if R['capped'] else ''} "
                        f"({time.time()-t0:.0f}s)")
            except Exception as e:
                line = f"[{tag}] n={n} d={d} : ECHEC {type(e).__name__}: {e}"
            print(line, flush=True)
            fh.write(line + "\n")
            fh.flush()


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "valid"
    if mode == "valid":
        run([(3, 1, False), (3, 2, False), (4, 1, False), (4, 2, False),
             (4, 3, False), (5, 1, False), (5, 2, False), (5, 3, False)],
            "VALID")
    elif mode == "n6":
        run([(6, 3, False), (6, 1, True), (6, 2, True), (6, 3, True),
             (4, 1, True), (4, 2, True)], "N6+STRICT")
    elif mode == "n7":
        run([(7, 4, False), (7, 3, False), (7, 2, False), (7, 1, False)],
            "N7")
