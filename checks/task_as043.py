"""
TACHE AS-043 -- la courbe c(n,d) aux ECHELLES MODEREES.

AS-042 : ln(1/rho) = pi/x - c(n,d) — toute C13 dans le scalaire c.
Ici : estimer c sur une grille de cellules SANS payer les petites
echelles, grace a la loi pi/x :
  - estimateur ponctuel  c(x) = pi/x - ln(1/rho(x)) a x fixe modere
    (biaise en x, mais le biais est systematique : comparaison entre
    cellules A MEME x = tendance en n et en d) ;
  - ajustement 2 points L(x) = a/x - c sur la derniere paire :
    a doit retomber sur pi (controle de la loi), c = l'estime.

Cellules : d=3 : (9,3) r6, (11,3) r8, (13,3) r10 ;
           d=2 : (9,2) r7, (11,2) r9, (13,2) r11.
Echelles : x in {1.6, 0.8, 0.4} partout ; x = 0.2 seulement si r <= 8.
D de reference aux nouvelles cellules : temoin exact AS-021
(construct + exact_polish + eval_exact — borne sup certifiee, crue
optimale d'apres la validation 3/3 d'AS-021 ; sert d'echelle 4D).
Garde de budget : ~520 s — toute mesure sautee est dite SKIP.
"""

from __future__ import annotations

import sys
import time
from fractions import Fraction as F
from math import log, pi

sys.path.insert(0, "checks")
from task_as041 import masses_stream  # noqa: E402
from task_as035 import inv_rat  # noqa: E402

T0 = time.time()
BUDGET = 520.0

KNOWN = {(9, 3): F(387, 512), (11, 3): F(63, 16)}


def cell_setup(n, d):
    from task_as006b import weight_form
    t = (n + 1) // 2
    f = [1 if k >= t else 0 for k in range(n + 1)]
    C, Cm, Qb = weight_form(n, d)
    r = len(C)
    Cf = [sum(C[i][k] * f[k] for k in range(n + 1)) for i in range(r)]
    Qrat = [[F(int(Qb[i, j].p), int(Qb[i, j].q)) for j in range(r)]
            for i in range(r)]
    Q4 = [[4 * Qrat[i][j] for j in range(r)] for i in range(r)]
    Gi, _ = inv_rat(Q4)
    if (n, d) in KNOWN:
        Dv = KNOWN[(n, d)]
    else:
        from task_as021 import construct, exact_polish, eval_exact
        Z, ff, _ = construct(n, d, hops=2500, seed=1)
        Z = exact_polish(n, d, Z, ff)
        Dv = eval_exact(n, d, Z, ff)
    return Gi, Cf, r, Dv


def rho_at(Gi, Cf, Dv, x):
    s2 = 4.0 * float(Dv) * x
    Rd = F(8) / F(s2)
    mass, ndual = masses_stream(Gi, Cf, s2, Rd)
    sgn = {eps: (-1) ** (sum(e * c for e, c in zip(eps, Cf)) % 2)
           for eps in mass}
    Sp = sum(mass.values())
    Ss = sum(sgn[e] * m for e, m in mass.items())
    return abs(Ss) / Sp, ndual


def main():
    cells = [(9, 3), (9, 2), (11, 3), (11, 2), (13, 3), (13, 2)]
    for (n, d) in cells:
        if time.time() - T0 > BUDGET:
            print(f"(n={n}, d={d}) : SKIP (budget)", flush=True)
            continue
        Gi, Cf, r, Dv = cell_setup(n, d)
        print(f"(n={n}, d={d}) r={r}, 4D = {4*float(Dv):.4f} "
              f"(D = {Dv})", flush=True)
        xs = [1.6, 0.8, 0.4] + ([0.2] if r <= 8 else [])
        pts = []
        for x in xs:
            if time.time() - T0 > BUDGET:
                print(f"   x={x}: SKIP (budget)", flush=True)
                continue
            t1 = time.time()
            rho, nd = rho_at(Gi, Cf, Dv, x)
            L = log(1.0 / rho) if rho > 0 else float("inf")
            cx = pi / x - L
            pts.append((x, L))
            print(f"   x={x}: rho={rho:.3e}  ln(1/rho)={L:.3f}  "
                  f"c(x)={cx:+.3f}  ({nd} pts, {time.time()-t1:.0f}s)",
                  flush=True)
        if len(pts) >= 2:
            (x1, L1), (x2, L2) = pts[-2], pts[-1]
            u1, u2 = 1.0 / x1, 1.0 / x2
            a = (L2 - L1) / (u2 - u1)
            cfit = a * u2 - L2
            print(f"   fit 2 pts ({x1},{x2}) : pente a = {a:.3f} "
                  f"(pi = {pi:.3f}), c = {cfit:+.3f}", flush=True)


if __name__ == "__main__":
    main()
