"""
TACHE AS-035 -- le portrait du taux d'annulation : que valent les
signes de Lucas dans la serie theta duale ?

Decomposition de la borne de Banaszczyk (AS-034) via Poisson :
  Theta_t(s) = pref(s) * S_pm(s),   pref = s^r / sqrt(det 4Q),
  S_pm(s) = somme_m cos(pi m.Cf) e^{-pi s^2 m^T (4Q)^{-1} m}.
- SANS les signes (S_+ : valeurs absolues) : borne de VOLUME generique,
  valable pour toute cible.
- AVEC les signes : le gain specifique a MAJ — l'annulation de Lucas.
C13 <=> ce gain croit assez vite. Ici : premiere mesure du gain.

Phases :
1. POISSON a haute precision : primal et dual enumeres par rayon exact
   (LLL, machinerie AS-034) — l'ecart doit tomber a ~1e-9 (le 1e-2
   d'AS-034 venait de la troncature en boites).
2. Portrait : cellules (5,2),(7,3),(9,3),(11,3),(13,3) — pour chaque s
   d'une grille : borne signee vs borne non-signee vs vrai. Le GAIN DES
   SIGNES = B_signe - B_non-signe ; tendance en n a d fixe.
"""

from __future__ import annotations

import sys
import time
from fractions import Fraction as F
from math import exp, log, pi, sqrt

import numpy as np

sys.path.insert(0, "checks")
from task_as023 import lll_gram  # noqa: E402


def enum_vecs(Qrat, radius, offset=None):
    """Enumere {(val, y)} avec val = (offset + 2Uy... ) — ici version
    GENERIQUE : points w = z (entiers) du reseau Z^r + offset reel,
    metrique Qrat : val = (offset + z)^T Qrat (offset + z) <= radius.
    Retourne liste (val exact, z original)."""
    r = len(Qrat)
    if offset is None:
        offset = [F(0)] * r
    M = [[Qrat[i][j] for j in range(r)] for i in range(r)]
    U = lll_gram(M)                       # M := U^T Q U
    L = [[F(1) if i == j else F(0) for j in range(r)] for i in range(r)]
    Dg = [F(0)] * r
    for i in range(r):
        Dg[i] = M[i][i] - sum(L[i][j] ** 2 * Dg[j] for j in range(i))
        for k in range(i + 1, r):
            L[k][i] = (M[k][i] - sum(L[k][j] * L[i][j] * Dg[j]
                                     for j in range(i))) / Dg[i]
    # centre reel : minimise (offset + Uy)^T Q (offset + Uy)
    # convention : val = c0 + 2 bv.y + y^T M y  =>  centre = -M^{-1} bv,
    # v0 = c0 + bv.ystar  (bv NON double — le doubler decale le centre
    # d'un facteur 2 : bug attrape par Poisson + 44 GB de RAM)
    bv = [sum(U[k][i] * sum(Qrat[k2][k] * offset[k2]
                            for k2 in range(r)) for k in range(r))
          for i in range(r)]
    c0 = sum(offset[i] * Qrat[i][j] * offset[j]
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
    out = []
    if E < 0:
        return out
    y = [0] * r
    zc = [ystar[i] + sum(L[k][i] * ystar[k] for k in range(i + 1, r))
          for i in range(r)]

    def dfs(i, part):
        if i < 0:
            z = [sum(U[k][j] * y[j] for j in range(r)) for k in range(r)]
            out.append((v0 + part, z))
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
    return out


def inv_rat(Qrat):
    from sympy import Matrix, Rational
    r = len(Qrat)
    M = Matrix([[Rational(Qrat[i][j].numerator, Qrat[i][j].denominator)
                 for j in range(r)] for i in range(r)])
    Mi = M.inv()
    det = M.det()
    return [[F(int(Mi[i, j].p), int(Mi[i, j].q)) for j in range(r)]
            for i in range(r)], F(int(det.p), int(det.q))


def portrait(n, d, true_D):
    from task_as006b import weight_form
    t = (n + 1) // 2
    f = [1 if k >= t else 0 for k in range(n + 1)]
    C, Cm, Qb = weight_form(n, d)
    r = len(C)
    Cf = [F(sum(C[i][k] * f[k] for k in range(n + 1))) for i in range(r)]
    Qrat = [[F(int(Qb[i, j].p), int(Qb[i, j].q)) for j in range(r)]
            for i in range(r)]
    true_min = float(4 * true_D)
    # dual : Gram Gi = (4Q)^{-1}, signes cos(pi m.Cf)
    Q4 = [[4 * Qrat[i][j] for j in range(r)] for i in range(r)]
    Gi, det4Q = inv_rat(Q4)
    best_s, best_u = (0.0, None), (0.0, None)
    for sx in (0.25, 0.5, 1.0, 2.0, 4.0):
        s2 = true_min * sx
        # primal (controle) : rayon vrai + 8 s^2
        Rp = F(true_min) + F(8) * F(s2)
        prim = enum_vecs(Q4, Rp, offset=[x / 2 for x in Cf])
        # attention : val = (Cf/2 + z)^T 4Q (Cf/2 + z) = (Cf+2z)^T Q (.)
        th_p = sum(exp(-pi * float(v) / s2) for v, z in prim)
        # dual : rayon tel que s^2 * val_dual <= ~ 8 => val <= 8/s^2
        Rd = F(8) / F(s2) if s2 > 0 else F(1)
        dual = enum_vecs(Gi, Rd)
        pref = s2 ** (r / 2.0) / sqrt(float(det4Q))
        th_s = pref * sum((1 if sum(int(zz) * int(cf) for zz, cf in
                                    zip(z, Cf)) % 2 == 0 else -1)
                          * exp(-pi * s2 * float(v)) for v, z in dual)
        th_u = pref * sum(exp(-pi * s2 * float(v)) for v, z in dual)
        # controle de Poisson
        if sx == 1.0:
            print(f"    Poisson (s^2={s2:.3f}) : primal = {th_p:.9f} ; "
                  f"dual signe = {th_s:.9f} ; ecart = "
                  f"{abs(th_p - th_s):.2e}", flush=True)
        for tot, best in ((th_s, best_s), (th_u, best_u)):
            pass
        if 0 < th_s < 1:
            bnd = s2 / pi * log(1 / th_s)
            if bnd > best_s[0]:
                best_s = (bnd, s2)
        if 0 < th_u < 1:
            bnd = s2 / pi * log(1 / th_u)
            if bnd > best_u[0]:
                best_u = (bnd, s2)
    bs, bu = best_s[0], best_u[0]
    print(f"  ({n},{d}) dim {r} : vrai = {true_min:.4f} ; "
          f"B_signe = {bs:.4f} ({100*bs/true_min:.0f}%) ; "
          f"B_volume = {bu:.4f} ({100*bu/true_min:.0f}%) ; "
          f"GAIN DES SIGNES = {bs - bu:.4f}", flush=True)


def main():
    print("== portrait du gain des signes de Lucas ==")
    cells = [(5, 2, F(5, 32)), (7, 3, F(1, 8)), (9, 3, F(387, 512)),
             (11, 3, F(63, 16)), (13, 3, F(9749, 512))]
    for n, d, D in cells:
        t0 = time.time()
        portrait(n, d, D)
        print(f"    ({time.time() - t0:.0f}s)", flush=True)


if __name__ == "__main__":
    main()
