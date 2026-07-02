"""
TACHE AS-027 -- le vrai q3 (troisieme niveau de la hierarchie de
renormalisation des certificats duaux, d = 32).

Phase 1 (ANSATZ EN u) : q3 = x^4 p3(u), u = x + 1/x, p3 quartique
MONIQUE entier (palindromie automatique). Pour chaque structure
R = (1-x)^w q1^a q2^b q3 et decalage s, la norme est QUADRATIQUE en
les 4 coefficients libres de p3 : minimum reel en dim 4 + enumeration
entiere +/-3 autour + filtre de parite lineaire mod 2. Prediction a
battre : p3 = p2^2 - (u-2)^2 = u^4 - 6u^3 + 14u^2 - 14u + 5, et la
norme famille 2.1258 (AS-026).

Phase 2 (CERTIFICATION EXACTE) : test de vide sur le reseau de
certificats (dim 33) au rayon du meilleur candidat, avec parcours en
RATIONNELS EXACTS (le float64 est mort a cette dimension : 30 ordres
de grandeur — AS-026b). Arbre vrai attendu petit (163 noeuds a d=16).
"""

from __future__ import annotations

import sys
import time
from fractions import Fraction as F
from math import comb

import numpy as np

sys.path.insert(0, "checks")
from task_as006b import kernel_basis  # noqa: E402
from task_as023 import lll_gram  # noqa: E402
from task_as024 import cert_lattice, parity_func  # noqa: E402
from task_as025 import poly_mul, family, parity  # noqa: E402
from task_as026 import poly_divide_exact  # noqa: E402

D = 32
N = 2 * D + 1
Q1 = [1, -1, 1]
Q2 = [1, -3, 5, -3, 1]


def u_mono(j):
    """x^4 u^j comme x-polynome (liste, bas degre en tete)."""
    p = [0] * (4 - j) + [comb(j, i) for i in range(j + 1)]
    out = [0] * (4 + j + 1)
    # x^{4-j} (1 + x^2)^j : u^j = sum C(j,i) x^{j-2i} => x^4 u^j =
    # sum C(j,i) x^{4+j-2i}
    out = [0] * (4 + j + 1)
    for i in range(j + 1):
        out[4 + j - 2 * i] += comb(j, i)
    return out


def base_poly(w, a, b):
    R = [1]
    for _ in range(w):
        R = poly_mul(R, [1, -1])
    for _ in range(a):
        R = poly_mul(R, Q1)
    for _ in range(b):
        R = poly_mul(R, Q2)
    return R


def phase1():
    wgt = np.array([1.0 / comb(N, k) for k in range(N + 1)])
    best = None
    t0 = time.time()
    nstruct = 0
    for w in range(0, 16):
        for a in range(0, 6):
            for b in range(0, 4):
                degR = w + 2 * a + 4 * b + 8
                if degR > D:
                    continue
                Base = base_poly(w, a, b)
                # vecteurs a : fixe (u^4) + 4 libres (u^0..u^3)
                vecs = []
                for j in [4, 0, 1, 2, 3]:
                    P = poly_mul(Base, u_mono(j))
                    vecs.append(P)
                for s in range(0, 6):
                    avs = []
                    ok = True
                    for P in vecs:
                        av = family(D, s, P)
                        if av is None:
                            ok = False
                            break
                        avs.append(np.array(av, dtype=float))
                    if not ok:
                        continue
                    nstruct += 1
                    a0, A4 = avs[0], np.stack(avs[1:], axis=1)
                    # parites lineaires mod 2
                    p0 = int(sum(int(round(x))
                                 for x in a0[D + 1:]) % 2)
                    pj = [int(sum(int(round(x)) for x in A4[D + 1:, j])
                              % 2) for j in range(4)]
                    # min reel du quadratique
                    M = A4.T @ (A4 * wgt[:, None])
                    rhs = -(A4.T @ (a0 * wgt))
                    try:
                        creal = np.linalg.solve(M, rhs)
                    except np.linalg.LinAlgError:
                        continue
                    c0 = np.round(creal).astype(int)
                    for d0 in range(-3, 4):
                        for d1 in range(-3, 4):
                            for d2 in range(-3, 4):
                                for d3 in range(-3, 4):
                                    c = c0 + np.array([d0, d1, d2, d3])
                                    par = (p0 + sum(int(c[j]) * pj[j]
                                                    for j in range(4))) % 2
                                    if par != 1:
                                        continue
                                    av = a0 + A4 @ c.astype(float)
                                    v = float(np.sum(av * av * wgt))
                                    if best is None or v < best[0]:
                                        best = (v, w, a, b, s,
                                                c.tolist())
    v, w, a, b, s, c = best
    print(f"phase 1 : {nstruct} structures, {time.time() - t0:.0f}s")
    print(f"  meilleur : norme ~ {v:.6f} ; structure "
          f"(1-x)^{w} q1^{a} q2^{b} q3, s={s}")
    print(f"  p3(u) = u^4 + {c[3]} u^3 + {c[2]} u^2 + {c[1]} u + {c[0]}")
    print(f"  (prediction refutee ou confirmee : "
          f"pred = u^4 -6u^3 +14u^2 -14u +5)")
    # reconstruire exactement
    P3 = [x for x in u_mono(4)]
    for j in range(4):
        mj = u_mono(j)
        for i, coef in enumerate(mj):
            P3[i] += c[j] * coef
    R = poly_mul(base_poly(w, a, b), P3)
    av = family(D, s, R)
    assert av is not None and parity(D, av) == 1
    exact = sum(F(av[k] * av[k], comb(N, k)) for k in range(N + 1))
    print(f"  norme EXACTE = {exact} = {float(exact):.6f}")
    print(f"  q3 candidat (x-poly) = {P3}")
    return exact, av, P3


def phase2(radius, node_cap=2_000_000):
    """Test de vide EXACT (rationnels dans le parcours) au rayon donne
    sur le reseau des certificats de d=32."""
    n, A = cert_lattice(D)
    r = D + 1
    pars = [parity_func(n, D, v) for v in A]
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

    print("  [gram + LLL exacte dim 33...]", flush=True)
    G = [[dot(gens[i], gens[j]) for j in range(r)] for i in range(r)]
    U = lll_gram(G)
    gr = [[sum(U[q][i] * gens[q][k] for q in range(r))
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
        ystar[i] = zv[i] - sum(L[k][i] * ystar[k]
                               for k in range(i + 1, r))
    v0v0 = c0 + sum(bv[i] * ystar[i] for i in range(r))
    E = radius - v0v0                     # budget d'exces, EXACT
    print(f"  [E exact = {float(E):.6f} ; parcours exact...]", flush=True)
    if E < 0:
        return None, 0, False
    best = [E, None]
    nodes = [0]
    y = [0] * r
    zc = [ystar[i] + sum(L[k][i] * ystar[k] for k in range(i + 1, r))
          for i in range(r)]

    def dfs(i, part):
        if nodes[0] > node_cap:
            return
        if i < 0:
            if part < best[0]:
                best[0], best[1] = part, y.copy()
            return
        s = sum(L[j][i] * y[j] for j in range(i + 1, r) if y[j])
        center = zc[i] - s
        if part > best[0]:
            return
        k0 = round(center)
        left, right = k0 - 1, k0 + 1
        kk = k0
        while True:
            nodes[0] += 1
            if nodes[0] > node_cap:
                return
            t = part + Dg[i] * (kk - center) ** 2
            if t > best[0]:
                break
            y[i] = kk
            dfs(i - 1, t)
            y[i] = 0
            if abs(left - center) <= abs(right - center):
                kk, left = left, left - 1
            else:
                kk, right = right, right + 1

    dfs(r - 1, F(0))
    capped = nodes[0] > node_cap
    if best[1] is None:
        return None, nodes[0], capped
    a = [v0[k] + sum(gr[i][k] * best[1][i] for i in range(r))
         for k in range(n + 1)]
    return a, nodes[0], capped


def main():
    exact, av, P3 = phase1()
    print()
    print("phase 2 : certification exacte au rayon du candidat")
    t0 = time.time()
    a2, nodes, capped = phase2(exact * (1 - F(1, 10 ** 9)))
    print(f"  ({nodes} noeuds, {'CAP' if capped else 'complet'}, "
          f"{time.time() - t0:.0f}s)")
    if capped:
        print("  NON CONCLU (cap) — le candidat reste une borne sup.")
    elif a2 is None:
        print("  VIDE sous le rayon : le candidat est OPTIMAL "
              "(mu_32 = sa norme, CERTIFIE).")
    else:
        val = sum(F(a2[k] * a2[k], comb(N, k)) for k in range(N + 1))
        print(f"  MEILLEUR trouve : {val} = {float(val):.6f}")
        lead = next(i for i in range(len(a2)) if a2[i] != 0)
        sgn = 1 if a2[lead] > 0 else -1
        A2 = [sgn * x for x in a2[lead:]]
        while A2 and A2[-1] == 0:
            A2.pop()
        Dv = [comb(D + 1, i) for i in range(D + 2)]
        Rr = poly_divide_exact(A2, Dv)
        if Rr is not None:
            from sympy import symbols, Poly, factor_list
            x = symbols("x")
            Ri = [int(c) for c in Rr]
            print("  R =", factor_list(Poly(list(reversed(Ri)),
                                             x).as_expr()))


if __name__ == "__main__":
    main()
