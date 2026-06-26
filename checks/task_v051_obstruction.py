"""
TACHE V-051 -- vérification de l'obstruction cyclotomique (fil P vs NP).

Reproduit les chiffres de tasks/done/V-051.md :
 1. loi d'échelle min(d, 0.55(d+1)^2) pour d = 10..22 + fit log-log ;
 2. cellule (16,159) : min, hauteur, factorisation cyclotomique ;
 3. plateau d = 10 : min(10, n) = 28 stable sur n = 98..240.

Tout via le moteur symétrique svp_sym (min_sym = λ1 pour d >= 8, V-042).
"""

from __future__ import annotations

import numpy as np
import sympy as sp

from svp_sym import sym_shortest


def loi_echelle():
    print("1. loi d'échelle min(d, 0.55(d+1)^2) :")
    ds, mns = [], []
    for d in (10, 12, 14, 16, 18, 20, 22):
        n = round(0.55 * (d + 1) ** 2)
        lp, lm, _ = sym_shortest(d, n)
        ms = min(x for x in (lp, lm) if x is not None)
        ds.append(d)
        mns.append(ms)
        print(f"   d={d:>2} span={n:>3} floor={2*(d+1):>3} min={ms:>3} "
              f"ratio={ms/(2*(d+1)):.2f}")
    a = np.polyfit(np.log(ds), np.log(mns), 1)
    print(f"   fit : min ~ d^{a[0]:.2f} (polynomial, sous-quadratique)")


def cellule_16_159():
    print("2. cellule (16,159) :")
    x = sp.symbols("x")
    lp, lm, out = sym_shortest(16, 159)
    ms = min(lp, lm)
    sec = "plus" if lp == ms else "minus"
    v = [int(t) for t in out[sec][1][0]]
    nz = [i for i, c in enumerate(v) if c]
    lo, hi = nz[0], nz[-1]
    h = max(abs(c) for c in v)
    f = sp.factor(sp.Poly(list(reversed(v[lo:hi + 1])), x).as_expr())
    print(f"   min={ms}, hauteur={h}, span={hi-lo}")
    print(f"   {str(f)[:160]}...")


def plateau_d10():
    print("3. plateau d=10 (doit etre 28 stable) :")
    for n in (98, 120, 150, 200, 240):
        lp, lm, _ = sym_shortest(10, n)
        print(f"   (10,{n}) : min={min(lp, lm)}")


if __name__ == "__main__":
    loi_echelle()
    cellule_16_159()
    plateau_d10()
