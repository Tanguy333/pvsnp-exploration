"""
TACHE AS-028 -- p4 tranche par l'optimum CERTIFIE de d = 64 (dim 65).

Verrou leve : LLL exacte INCREMENTALE (mises a jour GSO en O(r) par
operation, formules de Cohen) au lieu du recalcul O(r^3) — et le GSO
incremental EST la LDL (mu = L, Bs = Dg), une phase en moins.

Protocole :
0. VALIDATION : le pipeline rapide doit re-certifier mu_32 = 2.050283
   (AS-027) a l'identique.
1. Ansatz d=64 : structures (1-x)^w q1 q2 q3 x^8 p4(u), p4 octique
   monique — norme quadratique en 8 coefficients : min reel + boite
   entiere + filtre parite ; plus les 4 lois candidates AS-027.
2. Certification exacte au rayon du candidat (parcours en rationnels,
   cap 5e6 noeuds) ; factorisation du R optimal ; identification de p4
   contre les lois candidates.
"""

from __future__ import annotations

import sys
import time
from fractions import Fraction as F
from math import comb

import numpy as np

sys.path.insert(0, "checks")
from task_as024 import cert_lattice, parity_func  # noqa: E402
from task_as025 import poly_mul, family, parity  # noqa: E402
from task_as026 import poly_divide_exact  # noqa: E402

DELTA = F(99, 100)


def lll_gso_fast(M, U):
    """LLL exacte incrementale sur Gram M (Fractions, modifie en place)
    avec transformation U (ints, colonnes, modifie en place).
    Retourne (mu, Bs) = GSO final (== LDL : L = mu, Dg = Bs)."""
    r = len(M)
    mu = [[F(0)] * r for _ in range(r)]
    Bs = [F(0)] * r
    for i in range(r):
        Bs[i] = M[i][i] - sum(mu[i][j] ** 2 * Bs[j] for j in range(i))
        for k in range(i + 1, r):
            mu[k][i] = (M[k][i] - sum(mu[k][j] * mu[i][j] * Bs[j]
                                      for j in range(i))) / Bs[i]

    def colop(k, j, q):                      # col_k -= q col_j
        mkj, mjj = M[k][j], M[j][j]
        for i in range(r):
            if i != k:
                M[i][k] -= q * M[i][j]
                M[k][i] = M[i][k]
        M[k][k] = M[k][k] - 2 * q * mkj + q * q * mjj
        for i in range(r):
            U[i][k] -= q * U[i][j]
        for t in range(j):
            mu[k][t] -= q * mu[j][t]
        mu[k][j] -= q

    def swap(k):                              # colonnes k-1 <-> k
        for i in range(r):
            M[i][k - 1], M[i][k] = M[i][k], M[i][k - 1]
        for jj in range(r):
            M[k - 1][jj], M[k][jj] = M[k][jj], M[k - 1][jj]
        for i in range(r):
            U[i][k - 1], U[i][k] = U[i][k], U[i][k - 1]
        muo = mu[k][k - 1]
        Bp = Bs[k] + muo * muo * Bs[k - 1]
        mun = muo * Bs[k - 1] / Bp
        Bs[k] = Bs[k - 1] * Bs[k] / Bp
        Bs[k - 1] = Bp
        for i in range(k + 1, r):
            t = mu[i][k]
            mu[i][k] = mu[i][k - 1] - muo * t
            mu[i][k - 1] = t + mun * mu[i][k]
        for j in range(k - 1):
            mu[k - 1][j], mu[k][j] = mu[k][j], mu[k - 1][j]
        mu[k][k - 1] = mun

    k = 1
    while k < r:
        for j in range(k - 1, -1, -1):
            q = round(mu[k][j])
            if q != 0:
                colop(k, j, q)
        if Bs[k] >= (DELTA - mu[k][k - 1] ** 2) * Bs[k - 1]:
            k += 1
        else:
            swap(k)
            k = max(k - 1, 1)
    return mu, Bs


def certify(d, radius, node_cap=5_000_000, verbose=True):
    """Parcours EXACT du reseau de certificats de d au rayon donne.
    Retourne (a optimal ou None si vide, noeuds, cap)."""
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

    t0 = time.time()
    if verbose:
        print(f"  [gram dim {r}...]", flush=True)
    M = [[dot(gens[i], gens[j]) for j in range(r)] for i in range(r)]
    U = [[1 if i == j else 0 for j in range(r)] for i in range(r)]
    if verbose:
        print(f"  [LLL incrementale... ({time.time() - t0:.0f}s)]",
              flush=True)
    L, Dg = lll_gso_fast(M, U)
    if verbose:
        print(f"  [LLL ok ({time.time() - t0:.0f}s) ; solve + parcours...]",
              flush=True)
    gr = [[sum(U[q][i] * gens[q][k] for q in range(r))
           for k in range(n + 1)] for i in range(r)]
    bv = [dot(gr[i], v0) for i in range(r)]
    c0 = dot(v0, v0)
    wv = [F(0)] * r
    for i in range(r):
        wv[i] = -bv[i] - sum(L[i][j] * wv[j] for j in range(i))
    zv = [wv[i] / Dg[i] for i in range(r)]
    ystar = [F(0)] * r
    for i in range(r - 1, -1, -1):
        ystar[i] = zv[i] - sum(L[k][i] * ystar[k]
                               for k in range(i + 1, r))
    v0v0 = c0 + sum(bv[i] * ystar[i] for i in range(r))
    E = radius - v0v0
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


def u_to_x(p, half):
    out = [0] * (2 * half + 1)
    for j, c in enumerate(p):
        if c == 0:
            continue
        for i in range(j + 1):
            out[half + j - 2 * i] += c * comb(j, i)
    return out


P1 = [-1, 1]
P2 = [3, -3, 1]
P3 = [10, -20, 16, -6, 1]


def ansatz64():
    d, n = 64, 129
    wgt = np.array([1.0 / comb(n, k) for k in range(n + 1)])
    base0 = poly_mul(poly_mul(u_to_x(P1, 1), u_to_x(P2, 2)),
                     u_to_x(P3, 4))
    best = None
    for w in range(28, 40):
        B = base0[:]
        for _ in range(w):
            B = poly_mul(B, [1, -1])
        # vecteurs : x^8 u^j fois B, j = 8 (fixe) puis 0..7
        vecs = []
        for j in [8, 0, 1, 2, 3, 4, 5, 6, 7]:
            mono = [0] * (j + 1)
            mono[j] = 1
            vecs.append(poly_mul(B, u_to_x(mono, 8)))
        for s in range(0, 3):
            avs = []
            ok = True
            for P in vecs:
                av = family(d, s, P)
                if av is None:
                    ok = False
                    break
                avs.append(np.array(av, dtype=float))
            if not ok:
                continue
            a0, A8 = avs[0], np.stack(avs[1:], axis=1)
            p0 = int(sum(int(round(t)) for t in a0[d + 1:]) % 2)
            pj = [int(sum(int(round(t)) for t in A8[d + 1:, j]) % 2)
                  for j in range(8)]
            Mq = A8.T @ (A8 * wgt[:, None])
            rhs = -(A8.T @ (a0 * wgt))
            try:
                creal = np.linalg.solve(Mq, rhs)
            except np.linalg.LinAlgError:
                continue
            c00 = np.round(creal).astype(int)
            # boite +/-1 autour du min reel (3^8 = 6561)
            from itertools import product
            for dc in product((-1, 0, 1), repeat=8):
                c = c00 + np.array(dc)
                par = (p0 + sum(int(c[j]) * pj[j] for j in range(8))) % 2
                if par != 1:
                    continue
                av = a0 + A8 @ c.astype(float)
                v = float(np.sum(av * av * wgt))
                if best is None or v < best[0]:
                    best = (v, w, s, c.tolist())
    v, w, s, c = best
    # reconstruire exactement
    p4 = list(c) + [1]
    B = base0[:]
    for _ in range(w):
        B = poly_mul(B, [1, -1])
    R = poly_mul(B, u_to_x(p4, 8))
    av = family(64, s, R)
    assert av is not None and parity(64, av) == 1
    exact = sum(F(av[k] * av[k], comb(129, k)) for k in range(130))
    return exact, av, p4, w, s


def main():
    print("== Phase 0 : VALIDATION — re-certifier mu_32 (AS-027) ==")
    t0 = time.time()
    target = F(10339808642005567799296, 5043112220613321848175)
    a, nodes, capped = certify(32, target * (1 + F(1, 10 ** 9)))
    if a is None or capped:
        print(f"  ECHEC validation (vide={a is None}, cap={capped}) — STOP")
        return
    val = sum(F(a[k] * a[k], comb(65, k)) for k in range(66))
    ok = val == target
    print(f"  mu_32 retrouve = {float(val):.6f} "
          f"[{'OK' if ok else 'ECHEC'}] ({nodes} noeuds, "
          f"{time.time() - t0:.0f}s)", flush=True)
    if not ok:
        return

    print("== Phase 1 : ansatz d=64 (octique en u) ==")
    t0 = time.time()
    exact, av, p4, w, s = ansatz64()
    print(f"  candidat : norme exacte = {float(exact):.6f} "
          f"(w={w}, s={s}) ; p4 = {p4} ({time.time() - t0:.0f}s)",
          flush=True)

    print("== Phase 2 : certification exacte d=64 (dim 65) ==")
    t0 = time.time()
    a2, nodes, capped = certify(64, exact * (1 - F(1, 10 ** 9)))
    print(f"  ({nodes} noeuds, {'CAP' if capped else 'complet'}, "
          f"{time.time() - t0:.0f}s)", flush=True)
    if capped:
        print("  NON CONCLU — le candidat reste une borne sup.")
        return
    if a2 is None:
        print(f"  VIDE sous le rayon : mu_64 = {float(exact):.6f} "
              f"CERTIFIE, p4 = {p4}")
        final = av
    else:
        val = sum(F(a2[k] * a2[k], comb(129, k)) for k in range(130))
        print(f"  MEILLEUR : mu_64 = {val} = {float(val):.6f} CERTIFIE")
        final = a2
    lead = next(i for i in range(len(final)) if final[i] != 0)
    sgn = 1 if final[lead] > 0 else -1
    A2 = [sgn * x for x in final[lead:]]
    while A2 and A2[-1] == 0:
        A2.pop()
    Dv = [comb(65, i) for i in range(66)]
    Rr = poly_divide_exact(A2, Dv)
    if Rr is not None:
        from sympy import symbols, Poly, factor_list
        x = symbols("x")
        Ri = [int(c) for c in Rr]
        print("  R =", factor_list(Poly(list(reversed(Ri)), x).as_expr()))
    # comparaison aux lois candidates
    import numpy as _np
    def sq(p):
        return poly_mul(p, p)
    def add(a_, b_):
        m = [0] * max(len(a_), len(b_))
        for i, c in enumerate(a_):
            m[i] += c
        for i, c in enumerate(b_):
            m[i] += c
        return m
    laws = {
        "p3^2+p2^2": add(sq(P3), sq(P2)),
        "p3^2+p3+(u-2)": add(add(sq(P3), P3), [-2, 1]),
        "p3^2-(u-2)": add(sq(P3), [2, -1]),
        "p3^2+p2^2+p1^2": add(add(sq(P3), sq(P2)), sq(P1)),
    }
    for name, lp in laws.items():
        lp = lp + [0] * (9 - len(lp))
        print(f"  loi {name} : p4 = {lp} "
              f"{'<= MATCH' if lp == p4 else ''}")


if __name__ == "__main__":
    main()
