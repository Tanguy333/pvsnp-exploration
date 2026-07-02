"""
TACHE AS-012 -- le motif des temoins Mersenne : extraire z* exact en
coordonnees STENCIL pour d = 1, 3, 7 (dims 2, 4, 8), deviner le motif de
doublement, construire le candidat d = 15 (dim 16) et VERIFIER par
evaluation exacte (sans recherche).

Coordonnees stencil : m_i = <x^i(1-x)^{d+1}, y> = z_i + s_i/2 avec
s_i = ±C(d, w-1-i) (AS-010) -- a d Mersenne, TOUS les s_i sont impairs
(Lucas, binaire tout-uns) : frustration maximale, et D = 1/8 constant.
La forme : val(y) = m^T Q_st m, Q_st = Y^T M Y (Y = right-inverse du
stencil), exacte (sympy).
"""

from __future__ import annotations

import sys
import time
from fractions import Fraction as F
from math import comb

import numpy as np
from sympy import Matrix, Rational

from task_as003_cvp2 import cvp_enum


def stencil_form(n, d):
    """Forme quadratique exacte en coordonnees stencil + offsets s."""
    r = n - d
    # stencil : ligne i = coefficients de x^i (1-x)^{d+1}, i = 0..r-1
    St = [[0] * (n + 1) for _ in range(r)]
    for i in range(r):
        for j in range(d + 2):
            St[i][i + j] = (-1) ** j * comb(d + 1, j)
    X = [[comb(k, i) for i in range(d + 1)] for k in range(n + 1)]
    B = [comb(n, k) for k in range(n + 1)]
    Xm, Bm, Stm = Matrix(X), Matrix.diag(*B), Matrix(St)
    Mw = Bm - Bm * Xm * (Xm.T * Bm * Xm).inv() * Xm.T * Bm
    Y = Stm.T * (Stm * Stm.T).inv()
    Qst = Y.T * Mw * Y
    w = (n + 1) // 2
    f = [1 if k >= w else 0 for k in range(n + 1)]
    s = [sum(St[i][k] * f[k] for k in range(n + 1)) for i in range(r)]
    return Qst, s, r


def solve_stencil(n, d, cap=40_000_000):
    Qst, s, r = stencil_form(n, d)
    # verification AS-010 : s_i = ±C(d, w-1-i)
    w = (n + 1) // 2
    for i in range(r):
        assert abs(s[i]) == comb(d, w - 1 - i) if 0 <= w - 1 - i <= d else s[i] == 0, (i, s[i])
    Qf = np.array([[float(Qst[i, j]) for j in range(r)] for i in range(r)])
    Mch = np.linalg.cholesky(Qf).T
    Cf = np.array(s, dtype=np.int64)          # u = s + 2z
    u = np.zeros(r)
    for i in range(r - 1, -1, -1):
        ss = Mch[i, i + 1:] @ u[i + 1:]
        u[i] = Cf[i] + 2 * round((-ss / Mch[i, i] - Cf[i]) / 2.0)
    ubf = float(np.sum((Mch @ u) ** 2))
    best, bu, nodes, capped = cvp_enum(Mch, Cf, r, ubf * (1 + 1e-9) + 1e-9,
                                       node_cap=cap)
    if bu is None:
        bu = u
    uv = Matrix([int(round(x)) for x in bu])
    D = Rational((uv.T * Qst * uv)[0, 0], 4)
    z = [(int(round(bu[i])) - s[i]) // 2 for i in range(r)]
    m = [F(int(round(bu[i])), 2) for i in range(r)]       # m_i = u_i/2
    return D, s, z, m, capped


def eval_candidate(n, d, zc):
    """Evaluation EXACTE d'un candidat z (aucune recherche)."""
    Qst, s, r = stencil_form(n, d)
    assert len(zc) == r
    uv = Matrix([s[i] + 2 * zc[i] for i in range(r)])
    return Rational((uv.T * Qst * uv)[0, 0], 4)


def main():
    print("=== temoins Mersenne exacts (coordonnees stencil) ===")
    pats = {}
    for d in (1, 3, 7):
        n = 2 * d + 1
        t0 = time.time()
        D, s, z, m, capped = solve_stencil(n, d)
        pats[d] = (s, z, m)
        print(f"d={d} n={n} : D={D} {'CAP' if capped else '(exact)'} "
              f"({time.time()-t0:.0f}s)")
        print(f"   s (offsets)   = {s}")
        print(f"   z* (entiers)  = {z}")
        print(f"   m* = z+s/2    = {[str(x) for x in m]}", flush=True)

    print("=== candidats d=15 (evaluation exacte, sans recherche) ===")
    d, n = 15, 31
    Qst, s, r = stencil_form(n, d)
    print(f"offsets s (d=15) = {s}")
    # candidat A : meme regle de m que le motif detecte (a ajuster a la
    # lecture des motifs) -- on essaie m_i = -s_i/2 arrondi vers 0 :
    # z_i = -(s_i - sign(s_i))//2  =>  m_i = ±1/2
    candA = [-(s[i] - (1 if s[i] > 0 else -1)) // 2 for i in range(r)]
    # candidat B : m_i = ±1/2 avec signe alterne
    candB = [-(s[i] - (1 if i % 2 == 0 else -1)) // 2 for i in range(r)]
    # candidat C : signes par parite du popcount de i (Thue-Morse)
    candC = [-(s[i] - (1 if bin(i).count('1') % 2 == 0 else -1)) // 2
             for i in range(r)]
    for nom, zc in (("A: m=sign(s)/2", candA), ("B: m=(-1)^i/2", candB),
                    ("C: Thue-Morse", candC)):
        val = eval_candidate(n, d, zc)
        print(f"   {nom} : D = {val}  {'<<< 1/8 !' if val == Rational(1,8) else ''}",
              flush=True)


if __name__ == "__main__":
    main()
