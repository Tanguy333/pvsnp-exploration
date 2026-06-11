"""
TACHE F-011, etape 25 -- la MACHINE A ANSATZE : plate jusqu'a n = 20 ?

Generalisation d'e24 : pour chaque n (t = ceil(n/2)), essayer des
partitions de [n] de la plus grossiere a la plus fine ; par partition,
mini-SAT (CaDiCaL) sur les variables d'orbite ; VERIFICATION EXACTE PAR
PROFILS (l'invariance est par construction, donc U(S)/V(S) ne dependent
que du profil (a_1..a_m) -- la verification sur tous les profils est
rigoureuse et minuscule).

Note prealable (consignee) : le K' naif V = C(w,t) + C(a,s)C(b,s) mod 3
est REFUTE avant usage -- echoue a t = 4 (profil (4,2) : 15+6 = 21 = 0
mod 3) et t = 10 (profil (10,2) : C(12,10) = 66 = 0). La question du
Theoreme K' est donc empirique : quelle structure gagne a chaque t ?
"""

from __future__ import annotations

import itertools
import time
from math import comb

from pysat.solvers import Cadical153


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


def try_partition(n, t, P):
    orbits = [k for k in itertools.product(*(range(min(p, t) + 1) for p in P))
              if sum(k) == t]
    profils = [a for a in itertools.product(*(range(p + 1) for p in P))
               if sum(a) >= t]
    e = CNF()
    u = {o: e.new() for o in orbits}
    v1 = {o: e.new() for o in orbits}
    v2 = {o: e.new() for o in orbits}
    for o in orbits:
        e.add([-v1[o], -v2[o]])
    z1, z2 = e.new(), e.new()
    e.add([-z1]); e.add([-z2])
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
        s1, s2 = z1, z2
        for o in orbits:
            m = Ns[o] % 3
            for _ in range(m):
                s1, s2 = mod3_add(e, s1, s2, v1[o], v2[o])
        e.add(([ux] if ux else []) + [s1, s2])
    s = Cadical153(bootstrap_with=e.cl)
    res = s.solve()
    model = set(s.get_model()) if res else None
    s.delete()
    if not res:
        return None
    uk = {o: (1 if u[o] in model else 0) for o in orbits}
    vk = {o: (1 if v1[o] in model else 0) + (2 if v2[o] in model else 0)
          for o in orbits}
    # VERIFICATION exacte par profils (tous, y compris < t)
    for a in itertools.product(*(range(p + 1) for p in P)):
        w = sum(a)
        U = V = 0
        for o in orbits:
            m = 1
            for ai, ki in zip(a, o):
                m *= comb(ai, ki)
            U += uk[o] * m
            V += vk[o] * m
        U %= 2
        V %= 3
        if w < t and (U or V):
            return "ECHEC-VERIF"
        if w >= t and not (U or V):
            return "ECHEC-VERIF"
    return (uk, vk)


def partitions_catalog(n):
    """ de la plus grossiere a la plus fine, tailles raisonnables. """
    cat = []
    for a in range(n // 2, 0, -1):
        cat.append((a, n - a))
    seen = set()
    for m in (3, 4, 5):
        for c in itertools.combinations_with_replacement(range(1, n), m):
            if sum(c) == n and c not in seen:
                seen.add(c)
                cat.append(c)
    # limiter : orbites <= 220
    out = []
    for P in cat:
        t = (n + 1) // 2
        no = sum(1 for k in itertools.product(
            *(range(min(p, t) + 1) for p in P)) if sum(k) == t)
        if no <= 220:
            out.append(P)
    return out


def main() -> None:
    print("TACHE F-011 e25 -- machine a ansatze, n = 14..20")
    print("=" * 64)
    results = {}
    for n in range(14, 21):
        t = (n + 1) // 2
        t0 = time.time()
        won = None
        tried = 0
        for P in partitions_catalog(n):
            tried += 1
            r = try_partition(n, t, P)
            if r == "ECHEC-VERIF":
                print(f"  n={n} : *** verification echouee sur {P} ***",
                      flush=True)
                continue
            if r is not None:
                won = (P, r)
                break
            if time.time() - t0 > 240:
                break
        if won:
            P, (uk, vk) = won
            u_nz = sum(1 for o in uk if uk[o])
            v_nz = sum(1 for o in vk if vk[o])
            results[n] = (P, u_nz, v_nz)
            print(f"  n={n:>2} (t={t}) : FERME par {P} "
                  f"({tried} partitions essayees, {time.time()-t0:.0f}s) ; "
                  f"|u|={u_nz}, |v|={v_nz} orbites non nulles "
                  f"{'[PUR MOD 3]' if u_nz == 0 else ''}", flush=True)
        else:
            results[n] = None
            print(f"  n={n:>2} (t={t}) : OUVERT apres {tried} partitions "
                  f"({time.time()-t0:.0f}s)", flush=True)
    print("\n" + "=" * 64)
    closed = [n for n, r in results.items() if r]
    print(f"Cellules fermees : {closed}")
    if all(results.values()):
        print("PLATE CONFIRMEE jusqu'a n = 20 (avec 4..13, 16, 32 deja acquis).")
    print("Patterns (donnees pour le Theoreme K') ci-dessus.")


if __name__ == "__main__":
    main()
