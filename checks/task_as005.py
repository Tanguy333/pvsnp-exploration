"""
TACHE AS-005 -- profil THR_w complet a n=7 avec CERTIFICATION PAR SANDWICH.

Pour chaque cellule (7, d, w) :
 - borne INF rigoureuse = convolution (1,2,1) du profil n=5 (AS-004) :
   pred = D5(w-2) + 2 D5(w-1) + D5(w)   (hors bornes -> 0) ;
 - borne SUP = temoin Babai + descente locale, VERIFIE EXACT (sympy) ;
 - si sup == pred : CERTIFIE (sandwich, zero enumeration) ;
 - sinon : enumeration a rayon = sup ; si complete : certifie ; si cap :
   la cellule est rendue comme encadrement [pred, sup].

Enjeu : la recursion serree predit D(7,3,3) = 9/64 > 1/8 -- le plateau de
d=3 se BOMBE a n=7, et q(9,3) >= 34/32768 > 32/32768 = q(7,3) : la
famille plate (le danger pour la Conjecture 13) s'evapore. A trancher.
"""

from __future__ import annotations

import time
from fractions import Fraction as F

import numpy as np
from sympy import Matrix, Rational

from task_as003_cvp2 import cvp_enum
from task_as004 import prepare_thr, local_refine, babai_ub

# profil n=5 exact (AS-004), D5[d][w] = dist^2 ; hors 1..5 -> 0
D5 = {
    1: {1: F(13, 64), 2: F(19, 32), 3: F(19, 32), 4: F(19, 32), 5: F(13, 64)},
    2: {1: F(1, 8), 2: F(9, 32), 3: F(5, 32), 4: F(9, 32), 5: F(1, 8)},
    3: {1: F(3, 64), 2: F(1, 32), 3: F(1, 32), 4: F(1, 32), 5: F(3, 64)},
}


def pred_lb(d, w):
    g = lambda ww: D5[d].get(ww, F(0))
    return g(w - 2) + 2 * g(w - 1) + g(w)


def exact_val(C, u):
    Cm = Matrix(C)
    G = Cm * Cm.T
    uv = Matrix([int(round(x)) for x in u])
    val = (uv.T * G.LUsolve(uv))[0, 0]
    return F(int(Rational(val, 4).p), int(Rational(val, 4).q))


def cell(n, d, w, cap=60_000_000):
    C, Cf, M, r = prepare_thr(n, d, w)
    u0, _ = babai_ub(M, Cf, r)
    u1, ubf = local_refine(M, Cf, r, u0)
    # multi-depart : perturbations aleatoires reproductibles du temoin
    rng = np.random.default_rng(12345)
    for _ in range(6):
        up = u1.copy()
        idx = rng.choice(r, size=max(1, r // 8), replace=False)
        up[idx] += 2 * rng.integers(-1, 2, size=len(idx))
        up, vp = local_refine(M, Cf, r, up)
        if vp < ubf - 1e-12:
            u1, ubf = up, vp
    ub = exact_val(C, u1)
    lb = pred_lb(d, w)
    if ub == lb:
        return lb, "CERTIFIE (sandwich, 0 enum)", 0
    # RAYON EN UNITES u : val_u = 4 * dist^2 (bug d'unites corrige — la
    # violation de symetrie w <-> 8-w l'a revele, 28e auto-correction)
    best, best_u, nodes, capped = cvp_enum(M, Cf, r,
                                           4.0 * float(ub) * (1 + 1e-9) + 1e-9,
                                           node_cap=cap)
    if best_u is not None:
        ub2 = exact_val(C, best_u)
        if ub2 == lb:
            return lb, f"CERTIFIE (sandwich apres enum, {nodes} nds)", nodes
        if not capped:
            return ub2, f"CERTIFIE (enum complete, {nodes} nds)", nodes
        return (lb, ub2), f"ENCADRE [lb, ub] (cap {nodes})", nodes
    if not capped:
        return ub, f"CERTIFIE (enum complete vide -> temoin local opt, {nodes} nds)", nodes
    return (lb, ub), f"ENCADRE [lb, ub] (cap, aucun temoin sous ub)", nodes


def main():
    with open("as005_profile.txt", "a", encoding="utf-8") as fh:
        for d in (3, 2):
            for w in range(1, 8):
                t0 = time.time()
                try:
                    val, statut, nodes = cell(7, d, w)
                    if isinstance(val, tuple):
                        s = f"D in [{val[0]}, {val[1]}]"
                    else:
                        s = f"D = {val} (q = {val / (1 << 7)})"
                    line = (f"n=7 d={d} w={w} : {s} | pred_fibres = "
                            f"{pred_lb(d, w)} | {statut} ({time.time()-t0:.0f}s)")
                except Exception as e:
                    line = f"n=7 d={d} w={w} : ECHEC {type(e).__name__}: {e}"
                print(line, flush=True)
                fh.write(line + "\n")
                fh.flush()


if __name__ == "__main__":
    main()
