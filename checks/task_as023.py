"""
TACHE AS-023 -- la loi de b_d = D(2d+1, d, d+1), base du theoreme
AS-022 (C13 pour d = O(log n)).

Mesure : b_d = 5/32, 1/8, 93/512, 59/128, 13/32, 1/8 pour d = 2..7 —
jamais < 1/8 des d >= 3, et = 1/8 pile aux Mersenne d = 3, 7 (ou l'on
sait b_d <= 1/8 pour tout Mersenne, AS-012). Conjecture a tester :
b_d >= 1/8 pour tout d >= 3, egalite ssi d Mersenne. Si prouvee, la
perte d'AS-022 tombe de 2^{3d/2} a ~2^d.

Phase 1 : TEST DE VIDE au rayon 1/8 pour d = 8..16. La valeur exacte de
b_d est inutile pour la conjecture (et plafonne : d=8 a 2e8 noeuds meme
avec enumeration rayonnee par la borne sup serree de la machine AS-021,
UB = 590035/131072 ~ 4.50 — consigne). Le test decisif est l'enumeration
sous 4*(1/8)(1+eps) : vide (non plafonne) => b_d > 1/8 CERTIFIE ; point
a 1/8 => egalite Mersenne certifiee (la borne inf manquante d'AS-012,
certifiee d <= 7 seulement) ; point < 1/8 => conjecture REFUTEE.

Phase 3 : residus optimaux EXACTS r* = y* - p* pour d = 2..8 (loi a
deviner pour la preuve duale — a la AS-012 ou le residu Mersenne etait
la parite (-1)^k/2^{d+2}).
"""

from __future__ import annotations

import sys
import time
from fractions import Fraction as F
from math import comb

import numpy as np

sys.path.insert(0, "checks")
from task_as006b import weight_form  # noqa: E402
from task_as003_cvp2 import cvp_enum  # noqa: E402
from task_as021 import construct, exact_polish, eval_exact  # noqa: E402
from sympy import Matrix, Rational  # noqa: E402


def exact_bd(d, node_cap=200_000_000, ub_frac=None):
    """b_d exact : UB serree (machine AS-021) puis enumeration rayonnee."""
    n = 2 * d + 1
    w = d + 1
    f = [1 if k >= w else 0 for k in range(n + 1)]
    if ub_frac is None:
        Z, fc, _ = construct(n, d, hops=4000, seed=1)
        Z = exact_polish(n, d, Z, fc)
        ub_frac = eval_exact(n, d, Z, fc)
    C, Cm, Qb = weight_form(n, d)
    r = len(C)
    Cf = np.array([sum(C[i][k] * f[k] for k in range(n + 1))
                   for i in range(r)], dtype=np.int64)
    Qf = np.array([[float(Qb[i, j]) for j in range(r)] for i in range(r)])
    Mch = np.linalg.cholesky(Qf).T
    rad = float(ub_frac) * 4.0 * (1 + 1e-9) + 1e-12
    best, best_u, nodes, capped = cvp_enum(Mch, Cf, r, rad, node_cap=node_cap)
    if best_u is None:
        return ub_frac, nodes, capped, False   # rien sous le rayon ?!
    uv = Matrix([int(round(x)) for x in best_u])
    val = (uv.T * Qb * uv)[0, 0]
    D = F(int(val.p), int(val.q)) / 4
    return min(D, ub_frac), nodes, capped, True


def lll_gram(M, delta=F(99, 100)):
    """LLL EXACTE sur matrice de Gram rationnelle (liste de listes de
    Fractions, modifiee en place), retourne U unimodulaire (colonnes,
    ints Python). Tout en rationnels : aucun souci de conditionnement."""
    r = len(M)
    U = [[1 if i == j else 0 for j in range(r)] for i in range(r)]

    def gso():
        mu = [[F(0)] * r for _ in range(r)]
        Bs = [F(0)] * r
        for i in range(r):
            Bs[i] = M[i][i] - sum(mu[i][j] ** 2 * Bs[j] for j in range(i))
            for k in range(i + 1, r):
                mu[k][i] = (M[k][i] - sum(mu[k][j] * mu[i][j] * Bs[j]
                                          for j in range(i))) / Bs[i]
        return mu, Bs

    def colop(k, j, q):                        # col_k -= q col_j (M et U)
        mkj, mjj = M[k][j], M[j][j]
        for i in range(r):
            if i != k:
                M[i][k] -= q * M[i][j]
                M[k][i] = M[i][k]
        M[k][k] = M[k][k] - 2 * q * mkj + q * q * mjj
        for i in range(r):
            U[i][k] -= q * U[i][j]

    def swap(k):                                # colonnes k-1 <-> k
        for i in range(r):
            M[i][k - 1], M[i][k] = M[i][k], M[i][k - 1]
        for j in range(r):
            M[k - 1][j], M[k][j] = M[k][j], M[k - 1][j]
        for i in range(r):
            U[i][k - 1], U[i][k] = U[i][k], U[i][k - 1]

    k = 1
    while k < r:
        mu, Bs = gso()
        for j in range(k - 1, -1, -1):
            q = round(mu[k][j])
            if q != 0:
                colop(k, j, q)
                mu, Bs = gso()
        if Bs[k] >= (delta - mu[k][k - 1] ** 2) * Bs[k - 1]:
            k += 1
        else:
            swap(k)
            k = max(k - 1, 1)
    return U


def empt_test(d, radius_frac, node_cap=300_000_000):
    """Test de vide LLL-reduit, algebre EXACTE (rationnels partout,
    float uniquement dans les bornes du parcours) : enumere la classe
    u = Cf + 2Uy sous radius (unites D, forme = 4D). Retourne
    (min exact ou None, noeuds, cap)."""
    import math
    n = 2 * d + 1
    w = d + 1
    f = [1 if k >= w else 0 for k in range(n + 1)]
    C, Cm, Qb = weight_form(n, d)
    r = len(C)
    Cf = [sum(C[i][k] * f[k] for k in range(n + 1)) for i in range(r)]
    Q = [[F(int(Qb[i, j].p), int(Qb[i, j].q)) for j in range(r)]
         for i in range(r)]
    M = [[4 * Q[i][j] for j in range(r)] for i in range(r)]   # Gram 2Z^r
    U = lll_gram(M)                       # M devient U^T (4Q) U, exact
    QCf = [sum(Q[i][k] * Cf[k] for k in range(r)) for i in range(r)]
    bv = [2 * sum(U[k][i] * QCf[k] for k in range(r)) for i in range(r)]
    c0 = sum(Cf[i] * QCf[i] for i in range(r))
    # LDL^T exact de M
    L = [[F(1) if i == j else F(0) for j in range(r)] for i in range(r)]
    Dg = [F(0)] * r
    for i in range(r):
        Dg[i] = M[i][i] - sum(L[i][j] ** 2 * Dg[j] for j in range(i))
        for k in range(i + 1, r):
            L[k][i] = (M[k][i] - sum(L[k][j] * L[i][j] * Dg[j]
                                     for j in range(i))) / Dg[i]
    # y* exact : L w = -b ; Dg z = w ; L^T y* = z
    wv = [F(0)] * r
    for i in range(r):
        wv[i] = -bv[i] - sum(L[i][j] * wv[j] for j in range(i))
    zv = [wv[i] / Dg[i] for i in range(r)]
    ystar = [F(0)] * r
    for i in range(r - 1, -1, -1):
        ystar[i] = zv[i] - sum(L[k][i] * ystar[k] for k in range(i + 1, r))
    v0 = c0 + sum(bv[i] * ystar[i] for i in range(r))
    rad2 = 4 * F(radius_frac)
    E_exact = rad2 - v0                   # budget d'exces, EXACT
    if E_exact < 0:
        return None, 0, False, None       # vide sans enumeration
    E = float(E_exact) * (1 + 1e-9) + 1e-12
    Lf = [[float(L[i][j]) for j in range(r)] for i in range(r)]
    Df = [float(x) for x in Dg]
    ysf = [float(x) for x in ystar]
    best = [None, None]                   # [exces float, y]
    nodes = [0]
    y = [0] * r

    def dfs(i, part):
        if nodes[0] > node_cap:
            return
        if i < 0:
            lim = E if best[0] is None else best[0]
            if part < lim:
                best[0], best[1] = part, y.copy()
            return
        # exces ligne i : Dg_i (y_i + sum_{j>i} L[j][i] y_j - z*_i)^2
        s = sum(Lf[j][i] * y[j] for j in range(i + 1, r))
        zi = ysf[i] + sum(Lf[j][i] * ysf[j] for j in range(i + 1, r))
        center = zi - s
        lim = E if best[0] is None else best[0]
        rem = lim - part
        if rem < 0:
            return
        dev = (rem / Df[i]) ** 0.5
        for kk in range(math.ceil(center - dev - 1e-12),
                        math.floor(center + dev + 1e-12) + 1):
            nodes[0] += 1
            if nodes[0] > node_cap:
                return
            t = part + Df[i] * (kk - center) ** 2
            lim = E if best[0] is None else best[0]
            if t <= lim + 1e-15:
                y[i] = kk
                dfs(i - 1, t)
                y[i] = 0

    dfs(r - 1, 0.0)
    capped = nodes[0] > node_cap
    if best[1] is None:
        return None, nodes[0], capped, None
    u = [Cf[i] + 2 * sum(U[i][j] * best[1][j] for j in range(r))
         for i in range(r)]
    val = sum(u[i] * Q[i][j] * u[j] for i in range(r) for j in range(r))
    return val / 4, nodes[0], capped, u


def residual(n, d, w, u=None):
    """Residu optimal exact r*_k. Si u (coordonnees noyau du temoin
    CERTIFIE par enumeration) est fourni, reconstruit le temoin par
    resolution entiere C x = u (les ajustements polynomiaux ne changent
    pas le residu) — sinon temoin heuristique (NON certifie)."""
    from task_as019 import integer_solve
    f = [1 if k >= w else 0 for k in range(n + 1)]
    if u is not None:
        C, Cm, Qb = weight_form(n, d)
        x = integer_solve([row[:] for row in C], list(u))
        y = [F(int(x[k]), 2) for k in range(n + 1)]
    else:
        Z, fc, _ = construct(n, d, hops=3000, seed=1)
        Z = exact_polish(n, d, Z, fc)
        y = [F(2 * Z[k] + f[k], 2) for k in range(n + 1)]
    B = [comb(n, k) for k in range(n + 1)]
    X = [[comb(k, j) for j in range(d + 1)] for k in range(n + 1)]
    A = [[sum(F(B[k] * X[k][i] * X[k][j]) for k in range(n + 1))
          for j in range(d + 1)] for i in range(d + 1)]
    b = [sum(F(B[k] * X[k][i]) * y[k] for k in range(n + 1))
         for i in range(d + 1)]
    beta = Matrix([[Rational(A[i][j].numerator, A[i][j].denominator)
                    for j in range(d + 1)] for i in range(d + 1)]).LUsolve(
        Matrix([Rational(x.numerator, x.denominator) for x in b]))
    rs = []
    for k in range(n + 1):
        pk = sum(F(int(beta[j].p), int(beta[j].q)) * X[k][j]
                 for j in range(d + 1))
        rs.append(y[k] - pk)
    return rs


def main():
    # TEST DE VIDE : pour la conjecture b_d >= 1/8, la VALEUR de b_d est
    # inutile — il suffit d'enumerer sous le rayon 4*(1/8)(1+eps) :
    # aucun point (non plafonne) => b_d > 1/8 CERTIFIE ; point a 1/8
    # => egalite (Mersenne) ; point < 1/8 => conjecture REFUTEE.
    # Le petit rayon effondre l'arbre (la valeur exacte de b_8, elle,
    # plafonne a 2e8 noeuds meme rayonnee — consigne tel quel).
    print("== Phase 0 : VALIDATION du test de vide LLL (d = 2..7) ==")
    expected = {2: None, 3: F(1, 8), 4: None, 5: None, 6: None, 7: F(1, 8)}
    ok = True
    for d in range(2, 8):
        D, nodes, capped, u = empt_test(d, F(1, 8))
        good = (not capped) and D == expected[d]
        ok &= good
        print(f"  d={d} : trouve={D} attendu={expected[d]} "
              f"[{'OK' if good else 'ECHEC'}] ({nodes} noeuds)", flush=True)
    print(f"  validation : {'OK' if ok else 'ECHEC — STOP'}")
    if not ok:
        return

    print("== Phase 1 : test de vide au rayon 1/8, d = 8..16 ==")
    for d in range(8, 17):
        t0 = time.time()
        D, nodes, capped, u = empt_test(d, F(1, 8))
        mers = " (Mersenne)" if d == 15 else ""
        if capped:
            tag = "NON CONCLU (cap)"
        elif D is None:
            tag = "b_d > 1/8 CERTIFIE"
        elif D == F(1, 8):
            tag = "b_d = 1/8 CERTIFIE"
        elif D < F(1, 8):
            tag = f"VIOLATION : b_d = {D} < 1/8"
        else:
            tag = f"point a {D} ?"
        print(f"  d={d:>2}{mers} : {tag} ({time.time() - t0:.0f}s, "
              f"{nodes} noeuds)", flush=True)

    print("== Phase 3 : residus optimaux CERTIFIES (loi a deviner) ==")
    # temoin certifie par enumeration au rayon b_d exact connu, puis
    # controle de norme OBLIGATOIRE (la v1 heuristique avait produit des
    # residus sous-optimaux a d=6,7 — attrape par ce controle)
    bd = {2: F(5, 32), 3: F(1, 8), 4: F(93, 512), 5: F(59, 128),
          6: F(13, 32), 7: F(1, 8)}
    for d in range(2, 8):
        n = 2 * d + 1
        Dv, nodes, capped, u = empt_test(d, bd[d])
        assert Dv == bd[d] and not capped, f"enum d={d} : {Dv} != {bd[d]}"
        rs = residual(n, d, d + 1, u=u)
        B = [comb(n, k) for k in range(n + 1)]
        norm = sum(B[k] * rs[k] ** 2 for k in range(n + 1))
        den = max(x.denominator for x in rs)
        num = [int(x * den) for x in rs]
        chk = "OK" if norm == bd[d] else f"NORME {norm} != {bd[d]} !"
        print(f"  d={d} (x 1/{den}) [{chk}] : {num}", flush=True)


if __name__ == "__main__":
    main()
