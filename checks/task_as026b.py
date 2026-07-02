"""
TACHE AS-026b -- le vrai optimum a d=32 par enumeration RAYONNEE PAR LA
FAMILLE : le certificat de renormalisation (norme 2.1258, AS-026) sert
d'incumbent initial ; si l'arbre se referme sous le cap, on obtient le
certificat optimal exact de d=32, sa factorisation donne le VRAI q3 et
corrige la recurrence (devinee sur 2 points seulement : q1 = 1-x(1-x)
confirme a d=8, q2 = q1^2 - x(1-x)^2 confirme a d=16/17).
"""

from __future__ import annotations

import sys
import time
from fractions import Fraction as F
from math import comb

sys.path.insert(0, "checks")
from task_as006b import kernel_basis  # noqa: E402
from task_as023 import lll_gram  # noqa: E402
from task_as024 import cert_lattice, parity_func  # noqa: E402
from task_as025 import poly_mul, family, parity  # noqa: E402
from task_as026 import poly_divide_exact  # noqa: E402


def renorm_seq(levels):
    qs = [[1, -1, 1]]
    for l in range(1, levels):
        sq = poly_mul(qs[-1], qs[-1])
        sub = [0] * (2 ** (l - 1)) + [1]
        for _ in range(2 ** l):
            sub = poly_mul(sub, [1, -1])
        m = [0] * max(len(sq), len(sub))
        for i, c in enumerate(sq):
            m[i] += c
        for i, c in enumerate(sub):
            m[i] -= c
        while m and m[-1] == 0:
            m.pop()
        qs.append(m)
    return qs


def mu_seeded(d, a_init, node_cap=300_000_000):
    """Copie de mu_d (AS-024) avec incumbent initial a_init."""
    import math
    n, A = cert_lattice(d)
    r = d + 1
    pars = [parity_func(n, d, v) for v in A]
    i0 = pars.index(1)
    v0 = A[i0]
    basis = []
    for i, v in enumerate(A):
        if i == i0:
            continue
        if pars[i]:
            v = [v[k] - v0[k] for k in range(n + 1)]
        basis.append(v)
    gens = [[2 * x for x in v0]] + basis
    wgt = [F(1, comb(n, k)) for k in range(n + 1)]

    def dot(u, v):
        return sum(wgt[k] * u[k] * v[k] for k in range(n + 1))

    print(f"  [gram + LLL exacte dim {r}...]", flush=True)
    G = [[dot(gens[i], gens[j]) for j in range(r)] for i in range(r)]
    U = lll_gram(G)
    gr = [[sum(U[a][i] * gens[a][k] for a in range(r))
           for k in range(n + 1)] for i in range(r)]
    bv = [dot(gr[i], v0) for i in range(r)]
    c0 = dot(v0, v0)
    L = [[F(1) if i == j else F(0) for j in range(r)] for i in range(r)]
    Dg = [F(0)] * r
    for i in range(r):
        Dg[i] = G[i][i] - sum(L[i][j] ** 2 * Dg[j] for j in range(i))
        for k in range(i + 1, r):
            L[k][i] = (G[k][i] - sum(L[k][j] * L[i][j] * Dg[j]
                                     for j in range(i))) / Dg[i]
    wv = [F(0)] * r
    for i in range(r):
        wv[i] = -bv[i] - sum(L[i][j] * wv[j] for j in range(i))
    zv = [wv[i] / Dg[i] for i in range(r)]
    ystar = [F(0)] * r
    for i in range(r - 1, -1, -1):
        ystar[i] = zv[i] - sum(L[k][i] * ystar[k] for k in range(i + 1, r))
    v0v0 = c0 + sum(bv[i] * ystar[i] for i in range(r))
    Lf = [[float(L[i][j]) for j in range(r)] for i in range(r)]
    Df = [float(x) for x in Dg]
    ysf = [float(x) for x in ystar]
    init_val = dot(a_init, a_init)
    E_init = float(init_val - v0v0) * (1 + 1e-9) + 1e-12
    best = [E_init, None]
    nodes = [0]
    y = [0] * r
    print(f"  [enumeration, rayon initial = {float(init_val):.4f}...]",
          flush=True)

    def dfs(i, part):
        if nodes[0] > node_cap:
            return
        if i < 0:
            if part < best[0]:
                best[0], best[1] = part, y.copy()
            return
        s = sum(Lf[j][i] * y[j] for j in range(i + 1, r))
        zi = ysf[i] + sum(Lf[j][i] * ysf[j] for j in range(i + 1, r))
        center = zi - s
        if part > best[0]:
            return
        k0 = round(center)
        left, right = k0 - 1, k0 + 1
        kk = k0
        while True:
            nodes[0] += 1
            if nodes[0] > node_cap:
                return
            t = part + Df[i] * (kk - center) ** 2
            if t > best[0] + 1e-15:
                break
            y[i] = kk
            dfs(i - 1, t)
            y[i] = 0
            if abs(left - center) <= abs(right - center):
                kk, left = left, left - 1
            else:
                kk, right = right, right + 1

    dfs(r - 1, 0.0)
    capped = nodes[0] > node_cap
    if best[1] is None:
        return init_val, a_init, nodes[0], capped, False
    a = [v0[k] + sum(gr[i][k] * best[1][i] for i in range(r))
         for k in range(n + 1)]
    val = dot(a, a)
    return val, a, nodes[0], capped, True


def main():
    d = 32
    qs = renorm_seq(4)
    R = [1]
    for _ in range(11):
        R = poly_mul(R, [1, -1])
    R = poly_mul(R, qs[1])          # q2
    R = poly_mul(R, qs[3])          # q4 (deg 16)
    a_init = family(d, 0, R)
    assert a_init is not None and parity(d, a_init) == 1
    t0 = time.time()
    val, a, nodes, capped, improved = mu_seeded(d, a_init)
    print(f"d=32 : mu = {float(val):.6f} ({nodes} noeuds, "
          f"{'CAP' if capped else 'complet'}, "
          f"{'ameliore' if improved else 'incumbent = optimum du rayon'}, "
          f"{time.time() - t0:.0f}s)", flush=True)
    lead = next(i for i in range(len(a)) if a[i] != 0)
    sgn = 1 if a[lead] > 0 else -1
    A = [sgn * x for x in a[lead:]]
    while A and A[-1] == 0:
        A.pop()
    print(f"a (des k={lead}) = {A}")
    D = [comb(d + 1, i) for i in range(d + 2)]
    Rr = poly_divide_exact(A, D)
    if Rr is None:
        print("division inexacte ?!")
        return
    Ri = [int(c) for c in Rr]
    from sympy import symbols, Poly, factor_list
    x = symbols("x")
    print("R =", factor_list(Poly(list(reversed(Ri)), x).as_expr()))


if __name__ == "__main__":
    main()
