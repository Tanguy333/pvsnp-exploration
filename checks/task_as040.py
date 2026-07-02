"""
TACHE AS-040 -- polissage d'instrument (pas un franchissement) :
(1) la forme close de det(Qb) ; (2) la courbe x90 deux crans plus loin.

VOLET 1 — THEOREME (formule de projection) :
  det(Qb) = prod_k C(n,k) / det(X^T B X),
car la base binomiale C(k,j) est une Z-base SATUREE du reseau des
polynomes a valeurs entieres, et les determinants de Gram sont
multiplicatifs (lemme classique, Smith + orthogonalite). det(X^T B X)
se calcule en forme close par d (Hankel binomial) :
  d=0 : 2^n ;  d=1 : n 4^{n-1} (verifie a la main).
Ici : formes closes symboliques d = 1..3 (sympy) + verification exacte
det(Qb) * det_d(n) = prod C(n,k) sur les 15 cellules d'AS-038.

VOLET 2 — x90 pour (15,2),(17,2),(17,3),(19,3) (dims 13..16).
PREDICTION ENREGISTREE (loi de Banaszczyk x90 ~ 1/r) : ~0.08 puis
~0.05-0.06. References D par la machine AS-021 (UB polie, marquees ~).
"""

from __future__ import annotations

import sys
import time
from fractions import Fraction as F
from math import comb, log, pi

sys.path.insert(0, "checks")


def volet1():
    from sympy import (Matrix, Symbol, binomial, factor, simplify,
                       summation)
    import sympy
    n = Symbol("n", positive=True, integer=True)
    print("== Volet 1 : formes closes de det(X^T B X) ==")
    forms = {}
    for d in (1, 2, 3):
        A = sympy.zeros(d + 1, d + 1)
        for i in range(d + 1):
            for j in range(d + 1):
                # A_ij = C(n,i) sum_t C(i, j-t) C(n-i, t) 2^{n-i-t}
                expr = 0
                for tt in range(0, j + 1):
                    expr += (binomial(i, j - tt) * binomial(n - i, tt)
                             * 2 ** (n - i - tt))
                A[i, j] = binomial(n, i) * expr
        det = factor(simplify(A.det()))
        forms[d] = det
        print(f"  d={d} : det(X^T B X) = {det}", flush=True)

    print("== verification exacte sur les cellules d'AS-038 ==")
    from task_as006b import weight_form
    ok_all = True
    for d in (1, 2, 3):
        for nn in range(2 * d + 1, 16, 2):
            C, Cm, Qb = weight_form(nn, d)
            detQ = Qb.det()
            detQ = F(int(detQ.p), int(detQ.q))
            prodC = 1
            for k in range(nn + 1):
                prodC *= comb(nn, k)
            H = int(forms[d].subs(n, nn))
            ok = detQ * H == prodC
            ok_all &= ok
            if not ok:
                print(f"  d={d}, n={nn} : ECART ! det*H = {detQ * H} "
                      f"vs prod = {prodC}", flush=True)
    print(f"  det(Qb) * det_d(n) = prod_k C(n,k) : "
          f"{'OK sur toutes les cellules' if ok_all else 'ECHEC'}",
          flush=True)


def volet2():
    from task_as021 import construct, exact_polish, eval_exact
    from task_as037 import theta_stream
    from task_as006b import weight_form
    print("== Volet 2 : x90 deux crans plus loin ==")
    print("  PREDICTION (x90 ~ 1/r) : ~0.08 puis ~0.05-0.06")
    for (nn, d) in [(15, 2), (17, 2), (17, 3), (19, 3)]:
        t0 = time.time()
        Z, f, _ = construct(nn, d, hops=2500, seed=1)
        Z = exact_polish(nn, d, Z, f)
        Dub = eval_exact(nn, d, Z, f)
        fourD = 4.0 * float(Dub)
        C, Cm, Qb = weight_form(nn, d)
        r = len(C)
        Cf = [F(sum(C[i][k] * f[k] for k in range(nn + 1)))
              for i in range(r)]
        Qrat = [[F(int(Qb[i, j].p), int(Qb[i, j].q)) for j in range(r)]
                for i in range(r)]
        x90 = None
        detail = []
        for x in (0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.12):
            s2 = fourD * x
            R = F(fourD) * F(1 + 8 * x)
            th, npts, capped = theta_stream(Qrat, Cf, s2, R,
                                            node_cap=30_000_000)
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
        print(f"  (n={nn:>2}, d={d}) dim {r:>2}~ : x90 = {x90} ; "
              f"1/r = {1.0/r:.3f} ; [{' '.join(detail)}] "
              f"({time.time()-t0:.0f}s)", flush=True)


def main():
    volet1()
    volet2()


if __name__ == "__main__":
    main()
