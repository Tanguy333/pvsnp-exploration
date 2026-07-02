"""
TACHE AS-037 -- la courbe x90(n, d) : a quelle profondeur de s la borne
theta reste-t-elle serree ?

x90 = le plus grand x tel que s^2 = 4D x donne borne >= 90% de 4D,
calcule cote PRIMAL en flux (petit s = peu de points primaux — le
regime exactement complementaire du dual d'AS-036).
- x90 ~ constante en n : la fenetre ne se ferme pas — route VIVANTE ;
- x90 ~ 1/poly(n)     : difficulte analytique chiffree ;
- x90 -> 0 exponentiel : certificat de deces de la route theta.

Theta en STREAMING (lecon AS-035/036 : jamais de stockage de points) :
DFS exact (LLL + LDL rationnels, machinerie AS-034) qui ACCUMULE
somme e^{-pi val/s^2} ; rayon = 4D(1+8x) (queue <= e^{-8pi}/point) ;
plafond de noeuds 2e7 avec drapeau honnete.
"""

from __future__ import annotations

import sys
import time
from fractions import Fraction as F
from math import exp, log, pi

sys.path.insert(0, "checks")
from task_as023 import lll_gram  # noqa: E402


def theta_stream(Qrat, b_rat, s2, radius, node_cap=20_000_000):
    """Somme e^{-pi val/s2}, val = (b+2Uy)^T Q (b+2Uy) <= radius,
    accumulation en flux, arithmetique exacte pour l'elagage."""
    r = len(b_rat)
    M = [[4 * Qrat[i][j] for j in range(r)] for i in range(r)]
    U = lll_gram(M)
    L = [[F(1) if i == j else F(0) for j in range(r)] for i in range(r)]
    Dg = [F(0)] * r
    for i in range(r):
        Dg[i] = M[i][i] - sum(L[i][j] ** 2 * Dg[j] for j in range(i))
        for k in range(i + 1, r):
            L[k][i] = (M[k][i] - sum(L[k][j] * L[i][j] * Dg[j]
                                     for j in range(i))) / Dg[i]
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
    acc = [0.0, 0]                       # somme, noeuds-feuilles
    if E < 0:
        return 0.0, 0, False
    y = [0] * r
    zc = [ystar[i] + sum(L[k][i] * ystar[k] for k in range(i + 1, r))
          for i in range(r)]
    nodes = [0]
    s2f = float(s2)
    v0f = float(v0)

    def dfs(i, part):
        if nodes[0] > node_cap:
            return
        if i < 0:
            acc[0] += exp(-pi * (v0f + float(part)) / s2f)
            acc[1] += 1
            return
        s = sum(L[j][i] * y[j] for j in range(i + 1, r) if y[j])
        center = zc[i] - s
        k0 = round(center)
        left, right = k0 - 1, k0 + 1
        kk = k0
        while True:
            nodes[0] += 1
            if nodes[0] > node_cap:
                return
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
    return acc[0], acc[1], nodes[0] > node_cap


def cell_x90(n, d, Dval, certified):
    from task_as006b import weight_form
    t = (n + 1) // 2
    f = [1 if k >= t else 0 for k in range(n + 1)]
    C, Cm, Qb = weight_form(n, d)
    r = len(C)
    Cf = [F(sum(C[i][k] * f[k] for k in range(n + 1))) for i in range(r)]
    Qrat = [[F(int(Qb[i, j].p), int(Qb[i, j].q)) for j in range(r)]
            for i in range(r)]
    fourD = 4.0 * float(Dval)
    x90 = None
    detail = []
    for x in (0.03, 0.05, 0.08, 0.12, 0.2, 0.3, 0.5):
        s2 = fourD * x
        R = F(fourD) * F(1 + 8 * x)
        th, npts, capped = theta_stream(Qrat, Cf, s2, R)
        if capped:
            detail.append(f"x={x}:CAP")
            break
        if not (0 < th < 1):
            detail.append(f"x={x}:th>=1")
            continue
        frac = (s2 / pi) * log(1 / th) / fourD
        detail.append(f"x={x}:{100*frac:.1f}%({npts}p)")
        if frac >= 0.90:
            x90 = x
        elif x90 is not None:
            break
    mark = "" if certified else "~"
    print(f"  (n={n:>2}, d={d}) dim {r:>2}{mark} : x90 = {x90} ; "
          f"[{' '.join(detail)}]", flush=True)
    return x90


def main():
    print("== la courbe x90(n, d) — primal, flux ==")
    cells = [
        (5, 2, F(5, 32), True), (7, 2, F(7, 8), True),
        (9, 2, 4.365, False), (11, 2, 20.10, False),
        (13, 2, 89.44, False),
        (7, 3, F(1, 8), True), (9, 3, F(387, 512), True),
        (11, 3, F(63, 16), True), (13, 3, F(9749, 512), True),
        (15, 3, 89.3, False),
    ]
    res = {}
    for n, d, D, cert in cells:
        t0 = time.time()
        res[(n, d)] = cell_x90(n, d, D, cert)
        if time.time() - t0 > 30:
            print(f"    [{time.time() - t0:.0f}s]", flush=True)
    print()
    for d in (2, 3):
        seq = [(n, res[(n, dd)]) for (n, dd) in sorted(res) if dd == d]
        print(f"  d={d} : x90 en n : " +
              ", ".join(f"{n}:{v}" for n, v in seq))


if __name__ == "__main__":
    main()
