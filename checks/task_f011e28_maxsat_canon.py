"""
TACHE F-011, etape 28 -- CERTIFICATS MINIMAUX par MaxSAT (RC2).

Les solutions SAT brutes sont non canoniques (e27). Ici : memes
encodages d'ansatz, mais en WCNF -- clauses dures = couverture ;
clauses souples = une penalite par orbite active (soft -u_o ; pour v,
indicateur z_o avec v1_o -> z_o, v2_o -> z_o durs et soft -z_o).
RC2 minimise le nombre total d'orbites actives -> certificats CREUX,
la ou les formes closes (K'') se lisent. Verification par profils.
"""

from __future__ import annotations

import itertools
import time
from math import comb

from pysat.formula import WCNF
from pysat.examples.rc2 import RC2

CELLS = [(13, (4, 4, 5)), (14, (2, 5, 7)), (19, (3, 7, 9)),
         (20, (4, 7, 9)), (23, (8, 15)), (24, (7, 17))]


class Enc:
    def __init__(self):
        self.nv = 0
        self.hard = []

    def new(self):
        self.nv += 1
        return self.nv

    def add(self, c):
        self.hard.append(c)


def xor_gate(e, x, y):
    z = e.new()
    e.add([-x, -y, -z]); e.add([x, y, -z])
    e.add([x, -y, z]); e.add([-x, y, z])
    return z


def mod3_add(e, s1, s2, w1, w2):
    t1, t2 = e.new(), e.new()
    bits = {0: (0, 0), 1: (1, 0), 2: (0, 1)}
    for s in range(3):
        for v in range(3):
            r = (s + v) % 3
            sb, vb, rb = bits[s], bits[v], bits[r]
            ante = [s1 if sb[0] else -s1, s2 if sb[1] else -s2,
                    w1 if vb[0] else -w1, w2 if vb[1] else -w2]
            e.add([-l for l in ante] + [t1 if rb[0] else -t1])
            e.add([-l for l in ante] + [t2 if rb[1] else -t2])
    return t1, t2


def solve_min(n, P, budget_note=""):
    t = (n + 1) // 2
    orbits = [k for k in itertools.product(*(range(min(p, t) + 1) for p in P))
              if sum(k) == t]
    profils = [a for a in itertools.product(*(range(p + 1) for p in P))
               if sum(a) >= t]
    e = Enc()
    u = {o: e.new() for o in orbits}
    v1 = {o: e.new() for o in orbits}
    v2 = {o: e.new() for o in orbits}
    z = {o: e.new() for o in orbits}
    for o in orbits:
        e.add([-v1[o], -v2[o]])
        e.add([-v1[o], z[o]])
        e.add([-v2[o], z[o]])
    zz1, zz2 = e.new(), e.new()
    e.add([-zz1]); e.add([-zz2])
    for a in profils:
        Ns = {}
        for o in orbits:
            m = 1
            for ai, ki in zip(a, o):
                m *= comb(ai, ki)
            Ns[o] = m
        odd = [u[o] for o in orbits if Ns[o] % 2 == 1]
        ux = None
        if odd:
            ux = odd[0]
            for x in odd[1:]:
                ux = xor_gate(e, ux, x)
        s1, s2 = zz1, zz2
        for o in orbits:
            for _ in range(Ns[o] % 3):
                s1, s2 = mod3_add(e, s1, s2, v1[o], v2[o])
        e.add(([ux] if ux else []) + [s1, s2])
    w = WCNF()
    for c in e.hard:
        w.append(c)
    for o in orbits:
        w.append([-u[o]], weight=1)
        w.append([-z[o]], weight=1)
    with RC2(w) as rc2:
        model = rc2.compute()
        cost = rc2.cost
    if model is None:
        return None
    mset = set(model)
    uk = {o: (1 if u[o] in mset else 0) for o in orbits}
    vk = {o: (1 if v1[o] in mset else 0) + (2 if v2[o] in mset else 0)
          for o in orbits}
    # verification par profils (tous)
    for a in itertools.product(*(range(p + 1) for p in P)):
        wgt = sum(a)
        U = V = 0
        for o in orbits:
            m = 1
            for ai, ki in zip(a, o):
                m *= comb(ai, ki)
            U += uk[o] * m
            V += vk[o] * m
        U %= 2
        V %= 3
        if (wgt < t and (U or V)) or (wgt >= t and not (U or V)):
            return "ECHEC-VERIF"
    return uk, vk, cost


def main() -> None:
    print("TACHE F-011 e28 -- certificats minimaux (MaxSAT/RC2)")
    print("=" * 64)
    for (n, P) in CELLS:
        t = (n + 1) // 2
        t0 = time.time()
        r = solve_min(n, P)
        dt = time.time() - t0
        if r is None or r == "ECHEC-VERIF":
            print(f"\n(n={n}, P={P}) : {'INFAISABLE?!' if r is None else 'ECHEC-VERIF'} ({dt:.0f}s)",
                  flush=True)
            continue
        uk, vk, cost = r
        ua = sorted(o for o in uk if uk[o])
        va = sorted((o, vk[o]) for o in vk if vk[o])
        print(f"\n(n={n}, t={t}, P={P}) : MINIMUM = {cost} orbites actives "
              f"({dt:.0f}s)")
        print(f"  u ({len(ua)}) : {ua}")
        print(f"  v ({len(va)}) : {va}", flush=True)


if __name__ == "__main__":
    main()
