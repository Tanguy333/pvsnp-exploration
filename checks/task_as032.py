"""
TACHE AS-032 -- la carte de renormalisation des tables : l'identite de
classe a couplage mod 4, verifiee puis mesuree sur les orbites de n=4.

IDENTITE (derivee AS-015 etendue aux classes ; verifiee ici) : pour
S = (S0, S1), pi = (pi0, pi1), cible t = (t0, t1),

  h_d^{(n)}(pi; t) = min { 1/2 ||P_{d,n-1}(Sig + t0+t1)||^2
                         + 1/2 ||P_{d-1,n-1}(Del + t1-t0)||^2 :
        Sig == Del == pi0+pi1 (mod 2),  Sig - Del == 2 pi0 (mod 4) }.

Le lien mod 4 est LE couplage quart-entier de la tour AS-020, au niveau
des tables. Version decouplee (on oublie le mod 4) :
  h >= 1/2 h_d^{(n-1)}(pi'; .) + 1/2 h_{d-1}^{(n-1)}(pi'; .).

Phases :
0. VALIDATION de l'identite : n=3 -> n=2, 24 classes pi aleatoires,
   les deux membres calcules independamment (classe exacte vs
   enumeration couplee mod 4).
1. Tables n=3 aux cibles du decoupage de H1^{(4)}[dl/2] :
   h_1[(dl0+dl1)/2] et h_0[(dl1-dl0)/2].
2. DEFICIT DE COUPLAGE sur les 2048 cosets / 180 orbites de RM(1,4) :
   deficit(sigma) = H1^{(4)}(sigma) - decouple(sigma) >= 0 ;
   distribution, quantization, part des orbites a deficit nul.
"""

from __future__ import annotations

import itertools
import random
import sys
import time
from collections import Counter
from fractions import Fraction as F
from math import comb

import numpy as np

sys.path.insert(0, "checks")
from task_as030 import full_space_form, class_min  # noqa: E402


def proj_np(n, d):
    from task_as002_cvp import monomial_matrix
    A, monos = monomial_matrix(n, d)
    Am = np.array(A, dtype=float)
    return np.eye(1 << n) - Am @ np.linalg.solve(Am.T @ Am, Am.T)


def h_exact(n, d, pi, target_num, den):
    C, Q = full_space_form(n, d)
    r = len(C)
    N = 1 << n
    b = [F(sum(C[i][k] * pi[k] for k in range(N)))
         + sum(F(C[i][k] * target_num[k], den) for k in range(N))
         for i in range(r)]
    return class_min(C, Q, b)


def main():
    print("== Phase 0 : identite de classe mod 4 (n=3 -> n=2) ==")
    n, d = 3, 2
    N = 1 << n
    M = 1 << (n - 1)
    wt = [bin(x).count("1") for x in range(N)]
    t_num = [-1 if w == 2 else 0 for w in wt]     # delta a n=3, t=2 :
    # delta = [w>=2]-[w>=1] = -[w=1] ... choisir cible generique :
    t_num = [1 if w >= 2 else 0 for w in wt]
    t_num = [a + b for a, b in zip(
        [1 if w >= 2 else 0 for w in wt],
        [1 if w >= 1 else 0 for w in wt])]        # g a t=2
    den = 2
    # decoupage : moitie x3=0 -> indices 0..3 ; x3=1 -> 4..7
    t0 = t_num[:M]
    t1 = t_num[M:]
    ts = [a + b for a, b in zip(t0, t1)]          # cible Sigma (num/den)
    td = [b - a for a, b in zip(t0, t1)]          # cible Delta
    Pd = proj_np(n - 1, d)
    Pd1 = proj_np(n - 1, d - 1)
    rng = random.Random(3)
    ok = True
    for _ in range(24):
        pi = [rng.randint(0, 1) for _ in range(N)]
        lhs = h_exact(n, d, pi, t_num, den)
        pi0, pi1 = pi[:M], pi[M:]
        pip = [(a + b) % 2 for a, b in zip(pi0, pi1)]
        # enumeration couplee : Sig = pip + 2a, Del = Sig - 2 pi0 - 4m
        best = None
        box = range(-2, 3)
        for a in itertools.product(box, repeat=M):
            Sig = np.array([pip[k] + 2 * a[k] for k in range(M)],
                           dtype=float)
            vs = Sig + np.array(ts, dtype=float) / den
            h1v = vs @ Pd
            h1 = float(h1v @ h1v)
            for m in itertools.product(box, repeat=M):
                Del = np.array([Sig[k] - 2 * pi0[k] - 4 * m[k]
                                for k in range(M)])
                vd = Del + np.array(td, dtype=float) / den
                h2v = vd @ Pd1
                v = 0.5 * h1 + 0.5 * float(h2v @ h2v)
                if best is None or v < best:
                    best = v
        ok &= abs(float(lhs) - best) < 1e-9
    print(f"  identite mod 4 : {'OK (24 classes)' if ok else 'ECHEC'}",
          flush=True)
    if not ok:
        return

    print("== Phase 1 : tables n=3 aux cibles du decoupage de "
          "H1[dl/2] (n=4) ==")
    # delta a n=4, t=3 : dl = -[w=2] sur 16 pts ; moities :
    # dl0 = -[w'=2], dl1 = -[w'=1]
    wt3 = [bin(x).count("1") for x in range(8)]
    dl0 = [-1 if w == 2 else 0 for w in wt3]
    dl1 = [-1 if w == 1 else 0 for w in wt3]
    ts3 = [a + b for a, b in zip(dl0, dl1)]       # /2 -> num, den=2
    td3 = [b - a for a, b in zip(dl0, dl1)]
    tabs = {}
    for (dd, tnum, name) in [(1, ts3, "h1[Sig]"), (0, td3, "h0[Del]")]:
        C, Q = full_space_form(3, dd)
        r = len(C)
        Ct = [sum(F(C[i][k] * tnum[k], 2) for k in range(8))
              for i in range(r)]
        table = {}
        for pi_int in range(256):
            pi = [(pi_int >> k) & 1 for k in range(8)]
            syn = tuple(sum(C[i][k] * pi[k] for k in range(8)) % 2
                        for i in range(r))
            if syn in table:
                continue
            b = [F(sum(C[i][k] * pi[k] for k in range(8))) + Ct[i]
                 for i in range(r)]
            table[syn] = class_min(C, Q, b)
        vals = Counter(table.values())
        print(f"  {name} (d={dd}) : {len(table)} cosets, valeurs "
              f"{[(str(v), c) for v, c in sorted(vals.items())]}",
              flush=True)
        tabs[name] = (table, C)

    print("== Phase 2 : deficit de couplage mod 4 sur RM(1,4) ==")
    t0c = time.time()
    # table exacte n=4 (recalculee, cf AS-031)
    C4, Q4 = full_space_form(4, 1)
    r4 = len(C4)
    wt4 = [bin(x).count("1") for x in range(16)]
    dl4 = [-1 if w == 2 else 0 for w in wt4]
    Ct4 = [sum(F(C4[i][k] * dl4[k], 2) for k in range(16))
           for i in range(r4)]
    tS, CS = tabs["h1[Sig]"]
    tD, CD = tabs["h0[Del]"]
    rS, rD = len(CS), len(CD)
    seen = {}
    defs = Counter()
    for pi_int in range(1 << 16):
        pi = [(pi_int >> k) & 1 for k in range(16)]
        syn = tuple(sum(C4[i][k] * pi[k] for k in range(16)) % 2
                    for i in range(r4))
        if syn in seen:
            continue
        b = [F(sum(C4[i][k] * pi[k] for k in range(16))) + Ct4[i]
             for i in range(r4)]
        h4 = class_min(C4, Q4, b)
        pi0, pi1 = pi[:8], pi[8:]
        pip = [(a + c) % 2 for a, c in zip(pi0, pi1)]
        sS = tuple(sum(CS[i][k] * pip[k] for k in range(8)) % 2
                   for i in range(rS))
        sD = tuple(sum(CD[i][k] * pip[k] for k in range(8)) % 2
                   for i in range(rD))
        dec = F(1, 2) * tS[sS] + F(1, 2) * tD[sD]
        seen[syn] = (h4, dec)
        defs[h4 - dec] += 1
    neg = sum(c for v, c in defs.items() if v < 0)
    zero = defs.get(F(0), 0)
    print(f"  {len(seen)} cosets ({time.time() - t0c:.0f}s) ; "
          f"deficits : {[(str(v), c) for v, c in sorted(defs.items())]}")
    print(f"  deficit < 0 : {neg} (DOIT etre 0) ; deficit nul : {zero} "
          f"/ {len(seen)} cosets", flush=True)


if __name__ == "__main__":
    main()
