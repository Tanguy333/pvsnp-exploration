"""
TACHE V-001 -- Polynomes toriques de MAJ aux petits n (BHLR 2019).

MODELE (BHLR, ITCS 2019, arXiv:1804.08176) : P : {0,1}^n -> R, degre d ;
P eps-approxime f sur le tore si pour tout x il existe un entier k_x tel
que |P(x) - f(x)/2 - k_x| <= eps. (0 -> proche de 0 mod 1 ; 1 -> proche
de 1/2 mod 1.) BHLR reduisent MAJ ∉ ACC0 a une borne inferieure de degre
torique pour MAJ, et prouvent le cas SYMETRIQUE ; le general est ouvert.

Ici, mesure EXACTE par MILP (HiGHS) :
  variables : eps, coefficients reels, k entiers (bornes [-50, 50],
  cap consigne ; WLOG k_0 = 0 en symetrique, absorbe par a_0) ;
  contraintes : -eps <= P(x) - t_x/2 - k_x <= eps ;
  objectif : minimiser eps.

  [A] SYMETRIQUE : P = sum a_i e_i -> par strate w : sum a_i C(w,i).
      Table eps*(n, d) pour n in {8, 12, 16, 20, 24}, d = 1..n ;
      courbe d*(n) pour eps <= 1/8 et eps <= 1/(2n) -- la croissance
      observee est la replication numerique du phenomene BHLR.
  [B] GENERAL : n = 3, 4 -- multilineaire complet, k_x par point.
      Question signature du depot : l'asymetrie aide-t-elle sur le tore ?
"""

from __future__ import annotations

import itertools
import time
from math import comb

import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

K_BOUND = 5          # les decalages optimaux sont petits a ces tailles
MILP_TIME = 20.0     # limite par MILP (s) ; incumbent accepte, marque ~
MILP_OPTS = {"time_limit": MILP_TIME, "mip_rel_gap": 1e-6}


def torus_sym_eps(n, d, t=None):
    """ eps minimal pour un polynome torique SYMETRIQUE de degre <= d
        approximant THR_t (defaut MAJ) sur {0,1}^n. MILP exact. """
    t = t if t is not None else (n + 1) // 2
    # variables : [eps, a_0..a_d, k_1..k_n]  (k_0 = 0 WLOG)
    nv = 1 + (d + 1) + n
    c = np.zeros(nv)
    c[0] = 1.0
    rows, lbs, ubs = [], [], []
    for w in range(0, n + 1):
        target = 0.5 if w >= t else 0.0
        row = np.zeros(nv)
        for i in range(d + 1):
            row[1 + i] = comb(w, i)
        if w >= 1:
            row[1 + d + 1 + (w - 1)] = -1.0
        # P(w) - k_w - eps <= target  et  P(w) - k_w + eps >= target
        r1 = row.copy()
        r1[0] = -1.0
        rows.append(r1)
        lbs.append(-np.inf)
        ubs.append(target)
        r2 = row.copy()
        r2[0] = 1.0
        rows.append(r2)
        lbs.append(target)
        ubs.append(np.inf)
    A = np.array(rows)
    integrality = np.zeros(nv)
    integrality[1 + d + 1:] = 1
    lb = np.full(nv, -np.inf)
    ub = np.full(nv, np.inf)
    lb[0] = 0.0
    ub[0] = 0.5
    lb[1 + d + 1:] = -K_BOUND
    ub[1 + d + 1:] = K_BOUND
    res = milp(c, constraints=LinearConstraint(A, lbs, ubs),
               integrality=integrality, bounds=Bounds(lb, ub),
               options=MILP_OPTS)
    if res.x is not None:
        return float(res.x[0]), (res.status != 0)  # (eps, limite atteinte ?)
    return None, False


def torus_gen_eps(n, d):
    """ eps minimal, polynome torique GENERAL de degre <= d, MAJ_n. """
    t = (n + 1) // 2
    monos = []
    for k in range(d + 1):
        monos.extend(itertools.combinations(range(n), k))
    pts = list(range(1 << n))
    nv = 1 + len(monos) + len(pts)
    c = np.zeros(nv)
    c[0] = 1.0
    rows, lbs, ubs = [], [], []
    for j, x in enumerate(pts):
        w = bin(x).count("1")
        target = 0.5 if w >= t else 0.0
        row = np.zeros(nv)
        for ci, T in enumerate(monos):
            if all((x >> i) & 1 for i in T):
                row[1 + ci] = 1.0
        if j > 0:  # k du point 0 fixe a 0 (absorbe par la constante)
            row[1 + len(monos) + j] = -1.0
        r1 = row.copy()
        r1[0] = -1.0
        rows.append(r1)
        lbs.append(-np.inf)
        ubs.append(target)
        r2 = row.copy()
        r2[0] = 1.0
        rows.append(r2)
        lbs.append(target)
        ubs.append(np.inf)
    A = np.array(rows)
    integrality = np.zeros(nv)
    integrality[1 + len(monos):] = 1
    lb = np.full(nv, -np.inf)
    ub = np.full(nv, np.inf)
    lb[0] = 0.0
    ub[0] = 0.5
    lb[1 + len(monos):] = -K_BOUND
    ub[1 + len(monos):] = K_BOUND
    res = milp(c, constraints=LinearConstraint(A, lbs, ubs),
               integrality=integrality, bounds=Bounds(lb, ub),
               options=MILP_OPTS)
    if res.x is not None:
        return float(res.x[0]), (res.status != 0)
    return None, False


def main() -> None:
    print("TACHE V-001 -- degres toriques de MAJ (modele BHLR), MILP exact")
    print("=" * 70)

    print("\n[A] SYMETRIQUE : eps*(n, d) et degres requis", flush=True)
    for n in (8, 12, 16, 20):
        t0 = time.time()
        eps_by_d = {}
        d8 = d2n = None
        for d in range(1, n + 1):
            e, capped = torus_sym_eps(n, d)
            eps_by_d[d] = (e, capped)
            if e is not None:
                if d8 is None and e <= 0.125 + 1e-9:
                    d8 = d
                if d2n is None and e <= 1.0 / (2 * n) + 1e-9:
                    d2n = d
            if d2n is not None:
                break
        curve = ", ".join(f"d={d}:{e:.3f}{'~' if cp else ''}"
                          for d, (e, cp) in eps_by_d.items() if e is not None)
        print(f"    n={n:>2} : d*(eps<=1/8) = {d8}, d*(eps<=1/(2n)) = {d2n}"
              f"   ({time.time()-t0:.0f}s)")
        print(f"           courbe : {curve}", flush=True)

    print("\n[B] GENERAL vs SYMETRIQUE (n = 3, 4) :", flush=True)
    for n in (3, 4):
        for d in range(1, n + 1):
            es, cs = torus_sym_eps(n, d)
            eg, cg = torus_gen_eps(n, d)
            gain = ("GAIN ASYM" if (es is not None and eg is not None
                                    and eg < es - 1e-6) else "=")
            print(f"    n={n}, d={d} : sym eps* = {es:.4f}{'~' if cs else ''} ; "
                  f"general eps* = {eg:.4f}{'~' if cg else ''}   [{gain}]",
                  flush=True)

    print("\nLecture : la croissance de d*(n) en [A] est la replication")
    print("numerique du phenomene BHLR (borne symetrique) ; [B] teste si")
    print("l'asymetrie aide sur le tore (gabarit e17 du fil F-011).")
    print(f"Caps honnetes : k bornes a [-{K_BOUND}, {K_BOUND}] ; "
          f"{MILP_TIME:.0f}s par MILP (valeurs ~ = incumbent, non prouve).")


if __name__ == "__main__":
    main()
