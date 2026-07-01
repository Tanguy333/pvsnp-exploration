"""
TACHE ATLAS-005a -- CONTROLE POSITIF de l'instrument torique : Delta_w.

KV 2024 PROUVENT que les polynomes toriques asymetriques sont strictement
plus puissants que les symetriques pour les fonctions Delta_w (indicatrice
du poids de Hamming = w ; Delta_n = AND). Notre instrument MILP mesure
« pas de gain asymetrique pour MAJ, n <= 7 » (V-001/V-002/ATLAS-003).
Question de controle : le MEME instrument voit-il le gain PROUVE sur
Delta_w a ces tailles ?
 - S'il le voit : instrument valide + le contraste Delta_w/MAJ est reel.
 - S'il ne le voit pas : le gain KV n'apparait qu'asymptotiquement, et
   l'egalite MAJ aux petits n perd beaucoup de sa valeur probante.

Adaptation directe de task_v001_torus (memes conventions : K_BOUND,
cibles 0/0.5, certification exigee).
"""

from __future__ import annotations

import itertools
import time

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.special import comb

import task_v001_torus as T


def delta_sym_eps(n, d, w0):
    """eps minimal, polynome torique SYMETRIQUE degre <= d, Delta_{w0}."""
    nv = 1 + (d + 1) + n
    c = np.zeros(nv)
    c[0] = 1.0
    rows, lbs, ubs = [], [], []
    for w in range(0, n + 1):
        target = 0.5 if w == w0 else 0.0
        row = np.zeros(nv)
        for i in range(d + 1):
            row[1 + i] = comb(w, i)
        if w >= 1:
            row[1 + d + 1 + (w - 1)] = -1.0
        r1 = row.copy(); r1[0] = -1.0
        rows.append(r1); lbs.append(-np.inf); ubs.append(target)
        r2 = row.copy(); r2[0] = 1.0
        rows.append(r2); lbs.append(target); ubs.append(np.inf)
    A = np.array(rows)
    integrality = np.zeros(nv); integrality[1 + d + 1:] = 1
    lb = np.full(nv, -np.inf); ub = np.full(nv, np.inf)
    lb[0] = 0.0; ub[0] = 0.5
    lb[1 + d + 1:] = -T.K_BOUND; ub[1 + d + 1:] = T.K_BOUND
    res = milp(c, constraints=LinearConstraint(A, lbs, ubs),
               integrality=integrality, bounds=Bounds(lb, ub),
               options=T.MILP_OPTS)
    if res.x is not None:
        return float(res.x[0]), (res.status != 0)
    return None, False


def delta_gen_eps(n, d, w0):
    """eps minimal, polynome torique GENERAL degre <= d, Delta_{w0}."""
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
        target = 0.5 if w == w0 else 0.0
        row = np.zeros(nv)
        for ci, Tm in enumerate(monos):
            if all((x >> i) & 1 for i in Tm):
                row[1 + ci] = 1.0
        if j > 0:
            row[1 + len(monos) + j] = -1.0
        r1 = row.copy(); r1[0] = -1.0
        rows.append(r1); lbs.append(-np.inf); ubs.append(target)
        r2 = row.copy(); r2[0] = 1.0
        rows.append(r2); lbs.append(target); ubs.append(np.inf)
    A = np.array(rows)
    integrality = np.zeros(nv); integrality[1 + len(monos):] = 1
    lb = np.full(nv, -np.inf); ub = np.full(nv, np.inf)
    lb[0] = 0.0; ub[0] = 0.5
    lb[1 + len(monos):] = -T.K_BOUND; ub[1 + len(monos):] = T.K_BOUND
    res = milp(c, constraints=LinearConstraint(A, lbs, ubs),
               integrality=integrality, bounds=Bounds(lb, ub),
               options=T.MILP_OPTS)
    if res.x is not None:
        return float(res.x[0]), (res.status != 0)
    return None, False


def main() -> None:
    T.MILP_OPTS = dict(T.MILP_OPTS, time_limit=240)
    print("ATLAS-005a : controle positif Delta_w (gain asym PROUVE par KV)")
    gains = []
    for n in (5, 6):
        for w0 in (n, n - 1, n // 2):
            for d in range(1, n):
                t0 = time.time()
                es, cs = delta_sym_eps(n, d, w0)
                eg, cg = delta_gen_eps(n, d, w0)
                dt = time.time() - t0
                gain = (es is not None and eg is not None
                        and eg < es - 1e-6 and not cg)
                if gain:
                    gains.append((n, w0, d, es, eg))
                print(f"  n={n} w={w0} d={d} : sym={es:.6f}{'~' if cs else ''} "
                      f"| gen={eg:.6f}{'~' if cg else ''}  "
                      f"[{'GAIN ASYM' if gain else '='}]  ({dt:.0f}s)",
                      flush=True)
    print("BILAN gains asymetriques certifies :", gains if gains else "AUCUN")


if __name__ == "__main__":
    main()
