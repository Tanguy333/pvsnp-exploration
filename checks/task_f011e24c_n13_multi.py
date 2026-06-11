"""
TACHE F-011, etape 24c -- n = 13 par ansatze MULTI-partites (mini-SAT).

Les 6 bipartitions echouent. On teste des partitions plus fines de
[13] : les orbites (compositions de 7 bornees par les parts) restent
< 50 -> instances SAT minuscules (CaDiCaL, instantane).

Encodage par partition P = (p1..pm) :
  orbites o = (k1..km), somme 7, ki <= pi ; variables u_o (bin),
  v_o (2 bits, interdit 11) ; pour chaque profil a = (a1..am), ai <= pi,
  somme >= 7 : N_o(a) = prod C(ai, ki) ;
  U(a) = XOR des u_o avec N_o(a) impair ;
  V(a) = somme des (N_o(a) mod 3) * v_o mod 3 (chaine d'etats) ;
  couverture (U ou V != 0). Si SAT : verification exhaustive 8192 pts.
"""

from __future__ import annotations

import itertools
import time
from math import comb

from pysat.solvers import Cadical153

N, T = 13, 7

PARTITIONS = [(4, 4, 5), (3, 4, 6), (3, 5, 5), (2, 5, 6), (1, 6, 6),
              (2, 4, 7), (3, 3, 7), (2, 3, 8), (3, 3, 3, 4), (2, 3, 4, 4),
              (1, 4, 4, 4), (2, 2, 4, 5), (1, 3, 4, 5), (2, 2, 2, 3, 4)]


class CNF:
    def __init__(self):
        self.nv = 0
        self.cl = []

    def new(self):
        self.nv += 1
        return self.nv

    def add(self, c):
        self.cl.append(c)


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


def try_partition(P):
    parts = []
    start = 0
    for p in P:
        parts.append(list(range(start, start + p)))
        start += p
    orbits = [k for k in itertools.product(*(range(min(p, T) + 1) for p in P))
              if sum(k) == T]
    e = CNF()
    u = {o: e.new() for o in orbits}
    v1 = {o: e.new() for o in orbits}
    v2 = {o: e.new() for o in orbits}
    for o in orbits:
        e.add([-v1[o], -v2[o]])
    const_true = e.new()
    e.add([const_true])
    zero1, zero2 = e.new(), e.new()
    e.add([-zero1]); e.add([-zero2])
    profils = [a for a in itertools.product(*(range(p + 1) for p in P))
               if sum(a) >= T]
    for a in profils:
        Ns = {o: 1 for o in orbits}
        for o in orbits:
            for ai, ki in zip(a, o):
                Ns[o] *= comb(ai, ki)
        odd = [u[o] for o in orbits if Ns[o] % 2 == 1]
        if odd:
            ux = odd[0]
            for x in odd[1:]:
                ux = xor_gate(e, ux, x)
        else:
            ux = None
        s1, s2 = zero1, zero2
        for o in orbits:
            m = Ns[o] % 3
            if m == 0:
                continue
            for _ in range(m):
                s1, s2 = mod3_add(e, s1, s2, v1[o], v2[o])
        cov = ([ux] if ux else []) + [s1, s2]
        e.add(cov)
    s = Cadical153(bootstrap_with=e.cl)
    res = s.solve()
    model = set(s.get_model()) if res else None
    s.delete()
    if not res:
        return None
    uk = {o: (1 if u[o] in model else 0) for o in orbits}
    vk = {o: (1 if v1[o] in model else 0) + (2 if v2[o] in model else 0)
          for o in orbits}
    return parts, orbits, uk, vk


def verify(parts, uk, vk):
    monos = list(itertools.combinations(range(N), T))
    def orb(Tm):
        s = set(Tm)
        return tuple(len(s & set(p)) for p in parts)
    uu = [uk[orb(Tm)] for Tm in monos]
    vv = [vk[orb(Tm)] for Tm in monos]
    Tsets = [frozenset(Tm) for Tm in monos]
    for x in range(1 << N):
        S = frozenset(i for i in range(N) if (x >> i) & 1)
        w = len(S)
        U = sum(c for Ts, c in zip(Tsets, uu) if Ts <= S) % 2
        V = sum(c for Ts, c in zip(Tsets, vv) if Ts <= S) % 3
        if (w < T and (U or V)) or (w >= T and not (U or V)):
            return False
    return True


def main() -> None:
    print("TACHE F-011 e24c -- n = 13, ansatze multipartites (mini-SAT)")
    print("=" * 62)
    for P in PARTITIONS:
        t0 = time.time()
        r = try_partition(P)
        if r is None:
            print(f"  {P} : aucune solution invariante "
                  f"({time.time()-t0:.0f}s)", flush=True)
            continue
        parts, orbits, uk, vk = r
        print(f"  {P} : SOLUTION ({time.time()-t0:.0f}s) -- verification...",
              flush=True)
        ok = verify(parts, uk, vk)
        print(f"    verification exhaustive 8192 points : "
              f"{'OK' if ok else '*** ECHEC ***'}")
        if ok:
            print(f"    u par orbite : { {o: uk[o] for o in orbits if uk[o]} }")
            print(f"    v par orbite : { {o: vk[o] for o in orbits if vk[o]} }")
            print("\n=> deg_6(MAJ_13) = 7 : PLATE CONFIRMEE, cellule fermee.")
            return
    print("\nToutes les partitions testees echouent -- n = 13 reste ouvert")
    print("(solution, si elle existe, de symetrie encore plus basse).")


if __name__ == "__main__":
    main()
