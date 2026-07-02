"""
TACHE AS-038 -- le squelette asymptotique de la route theta :
determinant contre correction duale.

Au point x90 (AS-037), ln(1/Theta) = T_det + T_dual avec
  T_det  = -r ln(s) + (1/2) ln det(4Q)   (pur invariant du reseau),
  T_dual = -ln S_pm(s)                    (la serie signee, finie ici).
Volet 1 : mesurer les parts T_det / T_dual au x90 de chaque cellule —
si T_det domine et croit, le squelette de la route est un DETERMINANT.
Volet 2 : det(Qb) EXACT pour d = 1..3, n = 3..15 — factorisation et
chasse a la forme close (X^T B X est un determinant de Hankel binomial,
famille a formes closes classiques => prouvable si motif).
"""

from __future__ import annotations

import sys
import time
from fractions import Fraction as F
from math import exp, log, pi, sqrt

sys.path.insert(0, "checks")
from task_as035 import enum_vecs, inv_rat  # noqa: E402


def cell_decomp(n, d, Dval, x90):
    """SANS enumeration duale (3e recidive memoire evitee — lecon
    AS-036 appliquee) : ln(1/Theta) vient du PRIMAL en flux (AS-037),
    T_dual = ln(1/Theta) - T_det par soustraction."""
    from task_as006b import weight_form
    from task_as037 import theta_stream
    from sympy import Matrix, Rational
    t = (n + 1) // 2
    f = [1 if k >= t else 0 for k in range(n + 1)]
    C, Cm, Qb = weight_form(n, d)
    r = len(C)
    Cf = [F(sum(C[i][k] * f[k] for k in range(n + 1))) for i in range(r)]
    Qrat = [[F(int(Qb[i, j].p), int(Qb[i, j].q)) for j in range(r)]
            for i in range(r)]
    det4Q = float((Matrix([[Rational((4 * Qrat[i][j]).numerator,
                                     (4 * Qrat[i][j]).denominator)
                            for j in range(r)]
                           for i in range(r)])).det())
    fourD = 4.0 * float(Dval)
    s2 = fourD * x90
    R = F(fourD) * F(1 + 8 * x90)
    th, npts, capped = theta_stream(Qrat, Cf, s2, R)
    if capped or not (0 < th < 1):
        print(f"  (n={n:>2}, d={d}) : theta primal inutilisable "
              f"(cap={capped}, th={th:.3g})", flush=True)
        return
    ln_inv = log(1.0 / th)
    T_det = -0.5 * r * log(s2) + 0.5 * log(det4Q)
    T_dual = ln_inv - T_det
    bound = s2 / pi * ln_inv
    print(f"  (n={n:>2}, d={d}) : bound = {bound:9.3f} "
          f"({100*bound/fourD:5.1f}% de 4D) ; T_det = {T_det:8.3f} "
          f"({100*T_det/ln_inv:5.1f}%) ; T_dual = {T_dual:8.3f} "
          f"({100*T_dual/ln_inv:5.1f}%) ; {npts} pts primaux",
          flush=True)


def main():
    print("== Volet 1 : parts determinant / correction duale au x90 ==")
    cells = [
        (5, 2, F(5, 32), 0.3), (7, 2, F(7, 8), 0.3),
        (9, 2, 4.365, 0.2), (11, 2, 20.10, 0.12),
        (13, 2, 89.44, 0.08),
        (7, 3, F(1, 8), 0.3), (9, 3, F(387, 512), 0.3),
        (11, 3, F(63, 16), 0.2), (13, 3, F(9749, 512), 0.12),
        (15, 3, 89.3, 0.08),
    ]
    for n, d, D, x90 in cells:
        cell_decomp(n, d, D, x90)

    print("== Volet 2 : det(Qb) exact — chasse a la forme close ==")
    from task_as006b import weight_form
    from sympy import Matrix, Rational, factorint
    for d in (1, 2, 3):
        for n in range(2 * d + 1, 16, 2):
            C, Cm, Qb = weight_form(n, d)
            r = Qb.shape[0]
            det = Qb.det()
            num = int(det.p)
            den = int(det.q)
            fn = factorint(num) if num != 0 else {}
            fd = factorint(den)
            print(f"  d={d}, n={n:>2} (dim {r:>2}) : det(Qb) = "
                  f"{num}/{den} ; num = {dict(fn)} ; den = {dict(fd)}",
                  flush=True)


if __name__ == "__main__":
    main()
