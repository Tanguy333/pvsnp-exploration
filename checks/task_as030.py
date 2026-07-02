"""
TACHE AS-030 -- l'objet dual SANS PERTE : les tables de cosets de
Reed-Muller.

Theoreme (consequence directe d'AS-019, verifie ici) : la valeur de
classe h(pi) = min_{S == pi (2)} ||P_d(S + t)||^2 est INVARIANTE par
pi -> pi xor c pour tout c in RM(d, n) (ajouter un polynome entier ne
change pas la distance). Donc h est une fonction sur les COSETS de
RM(d,n) — objet FINI et EXACT (2^{2^n - dim RM} valeurs).

Et RM(d-1,n) inclus dans RM(d,n) => le syndrome fin (cosets de RM(d-1))
determine le grossier : LA CASCADE DEVIENT EXACTEMENT

  D(n+1, d, t) = min_{sigma in F2^N / RM(d-1,n)}
                 [ 1/2 H_d(coarsen(sigma)) + 1/2 H_{d-1}(sigma) ],

min d'une somme de deux TABLES liees par le raffinement des codes RM.
C'est la renormalisation d'objets duaux sans perte demandee : la tour
dyadique est une recursion sur les tables de cosets RM.

Phases :
1. verification de l'invariance RM (exacte, translations aleatoires) ;
2. tables exactes : (3,2) [2 cosets], (3,1) [16], (4,3) [2], (4,2) [32] ;
3. reconstruction de D(4,2,2), D(4,2,3), D(4,3,3) depuis les tables —
   doit reproduire les valeurs de force brute (AS-029/KNOWN) ;
4. inspection : formes des tables (lien avec les distributions de poids
   des cosets RM — litterature classique, anteriorite a auditer).
"""

from __future__ import annotations

import itertools
import sys
import time
from fractions import Fraction as F
from math import comb

import numpy as np

sys.path.insert(0, "checks")
from task_as002_cvp import monomial_matrix, kernel_basis  # noqa: E402


def full_space_form(n, d):
    """C (base entiere saturee du complement des monomes <= d) et
    Q = (C C^T)^{-1} rationnelle : h(pi) = min_{z in Z^r}
    (b + 2z)^T Q (b + 2z), b = C pi + C t (t la cible)."""
    from sympy import Matrix
    A, monos = monomial_matrix(n, d)
    At = [[A[i][j] for i in range(1 << n)] for j in range(len(monos))]
    C = kernel_basis(At)
    r = len(C)
    G = Matrix([[sum(C[i][k] * C[j][k] for k in range(1 << n))
                 for j in range(r)] for i in range(r)])
    Gi = G.inv()
    Q = [[F(int(Gi[i, j].p), int(Gi[i, j].q)) for j in range(r)]
         for i in range(r)]
    return C, Q


def class_min(C, Q, b):
    """min_{z in Z^r} (b + 2z)^T Q (b + 2z), b rationnel — DFS exact
    (LDL de 4Q, Babai-first)."""
    r = len(Q)
    A = [[4 * Q[i][j] for j in range(r)] for i in range(r)]
    L = [[F(1) if i == j else F(0) for j in range(r)] for i in range(r)]
    Dg = [F(0)] * r
    for i in range(r):
        Dg[i] = A[i][i] - sum(L[i][j] ** 2 * Dg[j] for j in range(i))
        for k in range(i + 1, r):
            L[k][i] = (A[k][i] - sum(L[k][j] * L[i][j] * Dg[j]
                                     for j in range(i))) / Dg[i]
    bv = [2 * sum(Q[i][j] * b[j] for j in range(r)) for i in range(r)]
    c0 = sum(b[i] * Q[i][j] * b[j] for i in range(r) for j in range(r))
    wv = [F(0)] * r
    for i in range(r):
        wv[i] = -bv[i] - sum(L[i][j] * wv[j] for j in range(i))
    zv = [wv[i] / Dg[i] for i in range(r)]
    ystar = [F(0)] * r
    for i in range(r - 1, -1, -1):
        ystar[i] = zv[i] - sum(L[k][i] * ystar[k]
                               for k in range(i + 1, r))
    v0 = c0 + sum(bv[i] * ystar[i] for i in range(r))
    # incumbent z = 0
    best = [c0 - v0, None]
    y = [0] * r
    zc = [ystar[i] + sum(L[k][i] * ystar[k] for k in range(i + 1, r))
          for i in range(r)]

    def dfs(i, part):
        if i < 0:
            if part <= best[0]:
                best[0] = part
            return
        s = sum(L[j][i] * y[j] for j in range(i + 1, r) if y[j])
        center = zc[i] - s
        if part > best[0]:
            return
        k0 = round(center)
        left, right = k0 - 1, k0 + 1
        kk = k0
        while True:
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
    return v0 + best[0]


def rm_code(n, d):
    """Generateurs de RM(d,n) comme vecteurs 0/1 sur 2^n points."""
    A, monos = monomial_matrix(n, d)
    return [[A[i][j] % 2 for i in range(1 << n)] for j in range(len(A[0]))]


def syndrome_table(n, d, target_num, target_den):
    """Table h par coset : syndrome = C pi mod 2 (C = base saturee).
    target = vecteur rationnel (num/den). Retourne dict syndrome->h."""
    C, Q = full_space_form(n, d)
    r = len(C)
    N = 1 << n
    tb = [F(target_num[k], target_den) for k in range(N)]
    Ct = [sum(F(C[i][k]) * tb[k] for k in range(N)) for i in range(r)]
    table = {}
    reps = {}
    for pi in itertools.product((0, 1), repeat=N):
        syn = tuple(sum(C[i][k] * pi[k] for k in range(N)) % 2
                    for i in range(r))
        if syn in table:
            continue
        b = [F(sum(C[i][k] * pi[k] for k in range(N))) + Ct[i]
             for i in range(r)]
        table[syn] = class_min(C, Q, b)
        reps[syn] = pi
    return table, reps, C


def main():
    N = 8
    wt = [bin(x).count("1") for x in range(N)]
    # cibles pour (n+1=4, t) : g = f_t + f_{t-1}, delta cible = g/2, dl/2
    def targets(t):
        ft = [1 if w >= t else 0 for w in wt]
        ft1 = [1 if w >= t - 1 else 0 for w in wt]
        g = [a + b for a, b in zip(ft, ft1)]
        dl = [a - b for a, b in zip(ft, ft1)]
        return g, dl

    print("== Phase 1 : invariance RM de h (exacte) ==")
    import random
    rng = random.Random(11)
    g, dl = targets(2)
    C2, Q2 = full_space_form(3, 2)
    rm2 = rm_code(3, 2)
    ok = True
    for _ in range(20):
        pi = [rng.randint(0, 1) for _ in range(N)]
        cw = [0] * N
        for gvec in rm2:
            if rng.randint(0, 1):
                cw = [(a + b) % 2 for a, b in zip(cw, gvec)]
        pi2 = [(a + b) % 2 for a, b in zip(pi, cw)]
        b1 = [F(sum(C2[i][k] * pi[k] for k in range(N)))
              + sum(F(C2[i][k] * g[k], 2) for k in range(N))
              for i in range(len(C2))]
        b2 = [F(sum(C2[i][k] * pi2[k] for k in range(N)))
              + sum(F(C2[i][k] * g[k], 2) for k in range(N))
              for i in range(len(C2))]
        # NB : le syndrome C pi mod 2 identifie mais b differe d'un pair
        h1 = class_min(C2, Q2, b1)
        h2 = class_min(C2, Q2, b2)
        ok &= h1 == h2
    print(f"  h(pi) = h(pi xor RM(2,3)) : {'OK (20 tirages)' if ok else 'ECHEC'}")

    print("== Phase 2 : tables de cosets exactes ==")
    tables = {}
    for (n, d, t, tgt) in [(3, 2, 2, "g"), (3, 1, 2, "dl"),
                           (3, 2, 3, "g"), (3, 1, 3, "dl"),
                           (3, 3, 3, "g"), (3, 2, 3, "dl")]:
        g, dl = targets(t)
        tv = g if tgt == "g" else dl
        t0 = time.time()
        tab, reps, C = syndrome_table(n, d, tv, 2)
        tables[(n, d, t, tgt)] = tab
        vals = sorted(set(tab.values()))
        print(f"  h[{tgt}] a (n={n}, d={d}, t={t}) : {len(tab)} cosets, "
              f"valeurs = {[str(v) for v in vals]} "
              f"({time.time() - t0:.0f}s)", flush=True)

    print("== Phase 3 : reconstruction de D(4,d,t) depuis les tables ==")
    known = {(2, 2): F(5, 64), (2, 3): F(5, 64), (3, 3): F(1, 64)}
    for (d, t), lhs in sorted(known.items()):
        g, dl = targets(t)
        # min sur pi de 1/2 h_d(pi; g/2) + 1/2 h_{d-1}(pi; dl/2)
        Cd, Qd = full_space_form(3, d)
        Cd1, Qd1 = full_space_form(3, d - 1)
        Ctg = [sum(F(Cd[i][k] * g[k], 2) for k in range(N))
               for i in range(len(Cd))]
        Ctd = [sum(F(Cd1[i][k] * dl[k], 2) for k in range(N))
               for i in range(len(Cd1))]
        cache_d, cache_d1 = {}, {}
        best = None
        for pi in itertools.product((0, 1), repeat=N):
            s1 = tuple(sum(Cd[i][k] * pi[k] for k in range(N)) % 2
                       for i in range(len(Cd)))
            s2 = tuple(sum(Cd1[i][k] * pi[k] for k in range(N)) % 2
                       for i in range(len(Cd1)))
            if s1 not in cache_d:
                b = [F(sum(Cd[i][k] * pi[k] for k in range(N))) + Ctg[i]
                     for i in range(len(Cd))]
                cache_d[s1] = class_min(Cd, Qd, b)
            if s2 not in cache_d1:
                b = [F(sum(Cd1[i][k] * pi[k] for k in range(N))) + Ctd[i]
                     for i in range(len(Cd1))]
                cache_d1[s2] = class_min(Cd1, Qd1, b)
            v = F(1, 2) * cache_d[s1] + F(1, 2) * cache_d1[s2]
            if best is None or v < best:
                best = v
        ok = best == lhs
        print(f"  D(4,{d},{t}) reconstruit = {best} vs connu {lhs} "
              f"[{'OK' if ok else 'ECART'}] "
              f"(|cosets| = {len(cache_d)} x {len(cache_d1)})", flush=True)


if __name__ == "__main__":
    main()
