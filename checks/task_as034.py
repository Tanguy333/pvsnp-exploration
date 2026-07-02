"""
TACHE AS-034 -- NOUVELLE ROUTE : la transference de Banaszczyk (serie
theta gaussienne) au lieu des certificats uniques.

Principe (sans perte, sans jauge) : pour le CVP min_z val(z),
val(z) = (b + 2z)^T Q (b + 2z),

  Theta_t(s) = somme_z exp(-pi val(z)/s^2) >= exp(-pi minval/s^2)
  => minval >= (s^2/pi) ln(1/Theta_t(s)),  pour tout s.

Et par POISSON, Theta_t se reecrit sur le reseau dual avec des phases
e^{2 pi i m.b/2} — chez nous des SIGNES DE LUCAS (AS-024). C13 devient
une estimee d'ANNULATION d'une serie theta a signes de Lucas — un objet
analytique unique. AS-029 a montre que le certificat unique perd 40% ;
la question ici : la masse gaussienne complete est-elle serree ?

Mesures :
1. cellules diagonales b_d (d = 2..6, dims 3..7, valeurs certifiees) :
   borne de Banaszczyk optimisee en s vs b_d vrai — ratio de serrage.
2. verification de Poisson (primal = dual) a une cellule.
3. la cellule d'AS-029 ((3,2), h1 : le certificat unique donnait 60%) :
   Banaszczyk fait-il mieux ?
"""

from __future__ import annotations

import itertools
import sys
import time
from fractions import Fraction as F
from math import comb, exp, log, pi, sqrt

import numpy as np

sys.path.insert(0, "checks")
from task_as024 import cert_lattice, parity_func  # noqa: E402
from task_as030 import full_space_form  # noqa: E402


def enum_vals(Qrat, b_rat, radius):
    """TOUTES les valeurs val(z) = (b+2z)^T Q (b+2z) <= radius, par
    parcours exact dans la base LLL-reduite (valeurs exactes, liste
    de Fractions). Q, b rationnels ; radius Fraction."""
    from task_as023 import lll_gram
    r = len(b_rat)
    M = [[4 * Qrat[i][j] for j in range(r)] for i in range(r)]
    U = lll_gram(M)                       # M := U^T (4Q) U exact
    # LDL de M
    L = [[F(1) if i == j else F(0) for j in range(r)] for i in range(r)]
    Dg = [F(0)] * r
    for i in range(r):
        Dg[i] = M[i][i] - sum(L[i][j] ** 2 * Dg[j] for j in range(i))
        for k in range(i + 1, r):
            L[k][i] = (M[k][i] - sum(L[k][j] * L[i][j] * Dg[j]
                                     for j in range(i))) / Dg[i]
    # offset : val = (b + 2Uy)^T Q (b + 2Uy) ; centre reel y* :
    # 2Uy = -b => y* = -(U^{-1} b)/2 — passer par la resolution LDL :
    bv = [2 * sum(U[k][i] * sum(Qrat[k2][k] * b_rat[k2]
                                for k2 in range(r)) for k in range(r))
          for i in range(r)]
    c0 = sum(b_rat[i] * Qrat[i][j] * b_rat[j]
             for i in range(r) for j in range(r))
    wv = [F(0)] * r
    for i in range(r):
        wv[i] = -bv[i] - sum(L[i][j] * wv[j] for j in range(i))
    zv = [wv[i] / Dg[i] for i in range(r)]
    ystar = [F(0)] * r
    for i in range(r - 1, -1, -1):
        ystar[i] = zv[i] - sum(L[k][i] * ystar[k]
                               for k in range(i + 1, r))
    v0 = c0 + sum(bv[i] * ystar[i] for i in range(r))
    E = radius - v0
    vals = []
    if E < 0:
        return vals
    y = [0] * r
    zc = [ystar[i] + sum(L[k][i] * ystar[k] for k in range(i + 1, r))
          for i in range(r)]

    def dfs(i, part):
        if i < 0:
            vals.append(v0 + part)
            return
        s = sum(L[j][i] * y[j] for j in range(i + 1, r) if y[j])
        center = zc[i] - s
        k0 = round(center)
        left, right = k0 - 1, k0 + 1
        kk = k0
        while True:
            t = part + Dg[i] * (kk - center) ** 2
            if t > E:
                break
            y[i] = kk
            dfs(i - 1, t)
            y[i] = 0
            if abs(left - center) <= abs(right - center):
                kk, left = left, left - 1
            else:
                kk, right = right, right + 1

    dfs(r - 1, F(0))
    return vals


def theta_bound(Qrat, b_rat, true_min, tag, cut_mult=8):
    """Borne de Banaszczyk mesuree : theta par enumeration exacte
    limitee au rayon vrai + cut_mult*s^2 (queue e^{-pi*cut} par point),
    convergence controlee EN RAYON (R vs 1.5R)."""
    tm = F(true_min)
    best = (0.0, None, 0)
    for sx in (F(1, 4), F(1, 2), F(3, 4), F(1), F(3, 2), F(2)):
        s2 = tm * sx
        R = tm + cut_mult * s2
        vals = enum_vals(Qrat, b_rat, R)
        vals2 = enum_vals(Qrat, b_rat, R + R // 2)
        tot = sum(exp(-pi * float(v / s2)) for v in vals)
        tot2 = sum(exp(-pi * float(v / s2)) for v in vals2)
        if tot2 - tot > 1e-9 * max(tot2, 1e-300):
            continue                       # queue non convergee
        if tot2 < 1.0 and tot2 > 0:
            bound = float(s2) / pi * log(1.0 / tot2)
            if bound > best[0]:
                best = (bound, float(s2), len(vals2))
    bound, s2, npts = best
    ratio = bound / true_min if true_min > 0 else float("nan")
    ok = "" if bound <= true_min * (1 + 1e-9) else "  ** INCOHERENT **"
    print(f"  {tag} : vrai = {true_min:.6f} ; Banaszczyk = {bound:.6f} "
          f"(s^2 = {s2:.4f}, {npts} pts) ; serrage = {100*ratio:.1f}%"
          f"{ok}", flush=True)
    return bound


def main():
    print("== 1. cellules diagonales b_d (reseau des certificats du "
          "primal poids-espace) ==")
    # le CVP de b_d : (Cf + 2z)^T Qb (Cf + 2z) / 4 — on borne la forme
    # val = u^T Qb u (4 b_d) et on compare a 4 b_d.
    from task_as006b import weight_form
    known = {2: F(5, 32), 3: F(1, 8), 4: F(93, 512), 5: F(59, 128),
             6: F(13, 32)}
    for d, bd in known.items():
        n = 2 * d + 1
        w = d + 1
        f = [1 if k >= w else 0 for k in range(n + 1)]
        C, Cm, Qb = weight_form(n, d)
        r = len(C)
        Cf = [F(sum(C[i][k] * f[k] for k in range(n + 1)))
              for i in range(r)]
        Qrat = [[F(int(Qb[i, j].p), int(Qb[i, j].q)) for j in range(r)]
                for i in range(r)]
        theta_bound(Qrat, Cf, float(4 * bd), f"4*b_{d} (dim {r})")

    print("== 2. verification de Poisson (d=3, dim 4) ==")
    d = 3
    n = 2 * d + 1
    from task_as006b import weight_form
    f = [1 if k >= d + 1 else 0 for k in range(n + 1)]
    C, Cm, Qb = weight_form(n, d)
    r = len(C)
    Cf = np.array([float(sum(C[i][k] * f[k] for k in range(n + 1)))
                   for i in range(r)])
    Qf = np.array([[float(Qb[i, j]) for j in range(r)]
                   for i in range(r)])
    s = 1.0
    tot = 0.0
    ctr = np.round(-Cf / 2.0)
    for z in itertools.product(range(-8, 9), repeat=r):
        v = Cf + 2.0 * (np.array(z) + ctr)
        tot += exp(-pi * float(v @ Qf @ v) / (s * s))
    # Poisson : somme_z f(z + Cf/2), f(y) = exp(-4pi y^T Qf y /s^2)
    # => (det(4Qf/s^2))^{-1/2} somme_m exp(-pi s^2 m^T (4Qf)^{-1} m)
    #    * exp(2 pi i m . Cf/2)
    G = 4.0 * Qf / (s * s)
    Gi = np.linalg.inv(4.0 * Qf)
    pref = 1.0 / sqrt(np.linalg.det(G))
    tot2 = 0.0
    for m in itertools.product(range(-8, 9), repeat=r):
        ma = np.array(m, dtype=float)
        ph = np.cos(pi * float(ma @ Cf))
        tot2 += pref * exp(-pi * s * s * float(ma @ Gi @ ma)) * ph
    print(f"  primal = {tot:.10f} ; dual (Poisson, phases cos(pi m.Cf))"
          f" = {tot2:.10f} ; ecart = {abs(tot-tot2):.2e}")

    print("== 3. la cellule d'AS-029 : h1 a (3,2), cible g/2 ==")
    # single certificat : 60%. Banaszczyk ?
    wt = [bin(x).count("1") for x in range(8)]
    g = [(1 if w >= 2 else 0) + (1 if w >= 1 else 0) for w in wt]
    C, Q = full_space_form(3, 2)
    r = len(C)
    # pi = 0 : b = C g / 2
    b = [sum(F(C[i][k] * g[k], 2) for k in range(8)) for i in range(r)]
    # vrai h1(0) : 1/32 (AS-030, table constante)
    theta_bound(Q, b, 1.0 / 32.0, "h1[g](pi=0) (dim 1)")


if __name__ == "__main__":
    main()
