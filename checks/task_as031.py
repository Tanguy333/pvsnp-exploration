"""
TACHE AS-031 -- les tables de cosets RM a n = 4 : la recursion des
tables observee une premiere fois, et leur taille EFFECTIVE (orbites).

1. Tables exactes a n=4 (16 points) pour le seuil central t=3 :
   H_3[g/2] (2 cosets), H_2[g/2] et H_2[dl/2] (32 cosets),
   H_1[dl/2] (2048 cosets, CVP exact dim 11 chacun).
2. VALIDATION de bout en bout : reconstruction de D(5,2,3) et D(5,3,3)
   depuis les tables seules — doit redonner 5/32 et 1/32 (certifies).
3. Structure : h est S_4-invariante (la cible ne depend que du poids) —
   verification, puis comptage des ORBITES : la taille effective de
   l'objet sans perte (2048 cosets -> combien d'orbites ? combien de
   valeurs distinctes ?), et comparaison du spectre avec n=3
   ({1/8, 3/8, 5/8}) : la recursion des tables, vue une fois.
"""

from __future__ import annotations

import itertools
import sys
import time
from collections import Counter
from fractions import Fraction as F
from math import comb

sys.path.insert(0, "checks")
from task_as002_cvp import monomial_matrix, kernel_basis  # noqa: E402
from task_as030 import full_space_form, class_min  # noqa: E402


def perms_action(n):
    """Permutations des n variables agissant sur les 2^n points."""
    idx = list(range(1 << n))
    perms = []
    for p in itertools.permutations(range(n)):
        m = []
        for x in idx:
            y = 0
            for i in range(n):
                if (x >> i) & 1:
                    y |= 1 << p[i]
            m.append(y)
        perms.append(m)
    return perms


def tables_n4():
    n = 4
    N = 1 << n
    wt = [bin(x).count("1") for x in range(N)]
    t = 3
    ft = [1 if w >= t else 0 for w in wt]
    ft1 = [1 if w >= t - 1 else 0 for w in wt]
    g = [a + b for a, b in zip(ft, ft1)]
    dl = [a - b for a, b in zip(ft, ft1)]
    out = {}
    for (d, tgt, name) in [(3, g, "H3[g]"), (2, g, "H2[g]"),
                           (2, dl, "H2[dl]"), (1, dl, "H1[dl]")]:
        t0 = time.time()
        C, Q = full_space_form(n, d)
        r = len(C)
        Ct = [sum(F(C[i][k] * tgt[k], 2) for k in range(N))
              for i in range(r)]
        table = {}
        reps = {}
        for pi_int in range(1 << N):
            pi = [(pi_int >> k) & 1 for k in range(N)]
            syn = tuple(sum(C[i][k] * pi[k] for k in range(N)) % 2
                        for i in range(r))
            if syn in table:
                continue
            b = [F(sum(C[i][k] * pi[k] for k in range(N))) + Ct[i]
                 for i in range(r)]
            table[syn] = class_min(C, Q, b)
            reps[syn] = pi
            if len(table) == 1 << r:
                break
        vals = Counter(table.values())
        print(f"  {name} (d={d}) : {len(table)} cosets, "
              f"{len(vals)} valeurs : "
              f"{[(str(v), c) for v, c in sorted(vals.items())]} "
              f"({time.time() - t0:.0f}s)", flush=True)
        out[name] = (table, reps, C)
    return out, g, dl


def main():
    print("== Phase 1 : tables exactes a n=4 (t=3) ==")
    tabs, g, dl = tables_n4()

    print("== Phase 2 : reconstruction de D(5,d,3) ==")
    N = 16
    known = {(2, "H2[g]", "H1[dl]"): F(5, 32),
             (3, "H3[g]", "H2[dl]"): F(1, 32)}
    for (d, nameA, nameB), lhs in known.items():
        tA, _, CA = tabs[nameA]
        tB, _, CB = tabs[nameB]
        rA, rB = len(CA), len(CB)
        best = None
        for pi_int in range(1 << N):
            pi = [(pi_int >> k) & 1 for k in range(N)]
            sA = tuple(sum(CA[i][k] * pi[k] for k in range(N)) % 2
                       for i in range(rA))
            sB = tuple(sum(CB[i][k] * pi[k] for k in range(N)) % 2
                       for i in range(rB))
            v = F(1, 2) * tA[sA] + F(1, 2) * tB[sB]
            if best is None or v < best:
                best = v
        ok = best == lhs
        print(f"  D(5,{d},3) reconstruit = {best} vs connu {lhs} "
              f"[{'OK' if ok else 'ECART'}]", flush=True)

    print("== Phase 3 : invariance S_4 et taille effective (orbites) ==")
    perms = perms_action(4)
    tab, reps, C = tabs["H1[dl]"]
    r = len(C)
    orbit_of = {}
    norb = 0
    bad = 0
    for syn, pi in reps.items():
        if syn in orbit_of:
            continue
        norb += 1
        for m in perms:
            # action : pi2[m[x]] = pi[x]
            pi2 = [0] * 16
            for x in range(16):
                pi2[m[x]] = pi[x]
            syn2 = tuple(sum(C[i][k] * pi2[k] for k in range(16)) % 2
                         for i in range(r))
            if syn2 in orbit_of:
                if orbit_of[syn2] != norb and tab[syn2] != tab[syn]:
                    bad += 1
            orbit_of[syn2] = norb
            if tab.get(syn2) != tab[syn]:
                bad += 1
    print(f"  H1[dl] : 2048 cosets -> {norb} orbites S_4 ; "
          f"violations d'invariance : {bad}")
    print(f"  (spectre n=3 : {{1/8, 3/8, 5/8}} sur 16 cosets ; "
          f"spectre n=4 : voir phase 1 — la recursion des tables.)")


if __name__ == "__main__":
    main()
