"""
TACHE AS-036 -- la courbe du taux d'annulation de Lucas en (n, d).

Tout se calcule cote DUAL (Poisson certifie en AS-035) :
  Theta(s) = pref(s) * S_pm(s),  pref = s^r / sqrt(det 4Q),
  S_pm = somme_m cos(pi m.Cf) e^{-pi s^2 val*(m)},
  val*(m) = m^T (4Q)^{-1} m  (enumere par rayon exact, streaming leger),
et la borne minval >= (s^2/pi) ln(1/Theta) quand Theta < 1.

Mesures par cellule (d = 2, 3 ; n jusqu'a 15) :
- rho(s*) = |S_pm|/S_+ (le taux d'annulation pur) ;
- Theta(s*) et la borne au meilleur s de la grille s^2 = D * x ;
- la FRACTION DE LA VERITE conservee : borne / (4D) — sa tendance en n
  a d fixe est LA courbe dont l'extrapolation est C13.
Valeurs D : certifiees quand connues (fractions), sinon mesures des
courbes AS (marquees ~, hypothese symetrique).
"""

from __future__ import annotations

import sys
import time
from fractions import Fraction as F
from math import exp, log, pi, sqrt

sys.path.insert(0, "checks")
from task_as035 import enum_vecs, inv_rat  # noqa: E402


def cell_curve(n, d, Dval, certified):
    from task_as006b import weight_form
    t = (n + 1) // 2
    f = [1 if k >= t else 0 for k in range(n + 1)]
    C, Cm, Qb = weight_form(n, d)
    r = len(C)
    Cf = [F(sum(C[i][k] * f[k] for k in range(n + 1))) for i in range(r)]
    Qrat = [[F(int(Qb[i, j].p), int(Qb[i, j].q)) for j in range(r)]
            for i in range(r)]
    Q4 = [[4 * Qrat[i][j] for j in range(r)] for i in range(r)]
    Gi, det4Q = inv_rat(Q4)
    true_min = 4.0 * float(Dval)
    best = (0.0, None, None, None)
    for x in (0.125, 0.25, 0.5, 1.0):
        s2 = true_min * x
        Rd = F(10) / F(s2)
        dual = enum_vecs(Gi, Rd)
        if len(dual) > 2_000_000:
            continue
        Sp, Ss = 0.0, 0.0
        for v, z in dual:
            w = exp(-pi * s2 * float(v))
            Sp += w
            sg = 1 if sum(int(zz) * int(cf)
                          for zz, cf in zip(z, Cf)) % 2 == 0 else -1
            Ss += sg * w
        pref = s2 ** (r / 2.0) / sqrt(float(det4Q))
        th = pref * Ss
        rho = abs(Ss) / Sp if Sp > 0 else float("nan")
        if 0 < th < 1:
            bnd = s2 / pi * log(1 / th)
            if bnd > best[0]:
                best = (bnd, s2, rho, len(dual))
    bnd, s2, rho, npts = best
    frac = bnd / true_min if true_min > 0 else float("nan")
    mark = "" if certified else "~"
    print(f"  (n={n:>2}, d={d}) dim {r:>2} : 4D = {true_min:9.4f}{mark} ; "
          f"borne = {bnd:9.4f} ({100*frac:5.1f}%) ; "
          f"rho = {rho if rho is not None else float('nan'):.4f} ; "
          f"{npts} pts duaux", flush=True)
    return frac


def main():
    print("== la courbe du taux d'annulation (fraction conservee) ==")
    cells = [
        (5, 2, F(5, 32), True), (7, 2, F(7, 8), True),
        (9, 2, 4.365, False), (11, 2, 20.10, False),
        (13, 2, 89.44, False),
        (7, 3, F(1, 8), True), (9, 3, F(387, 512), True),
        (11, 3, F(63, 16), True), (13, 3, F(9749, 512), True),
        (15, 3, 89.3, False),
    ]
    fr = {}
    for n, d, D, cert in cells:
        t0 = time.time()
        try:
            fr[(n, d)] = cell_curve(n, d, D, cert)
        except Exception as e:
            print(f"  (n={n}, d={d}) : ECHEC {type(e).__name__}: {e}",
                  flush=True)
        if time.time() - t0 > 60:
            print(f"    [{time.time() - t0:.0f}s]", flush=True)
    print()
    for d in (2, 3):
        seq = [(n, fr[(n, d)]) for (n, dd) in sorted(fr) if dd == d
               for _ in [0]]
        seq = [(n, fr[(n, dd)]) for (n, dd) in sorted(fr) if dd == d]
        print(f"  d={d} : fractions conservees en n : " +
              ", ".join(f"{n}:{100*v:.1f}%" for n, v in seq))


if __name__ == "__main__":
    main()
