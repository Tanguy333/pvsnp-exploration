"""
TACHE F-011, etape 24 -- deg_6(MAJ_12) = 6 ? par ANSATZE SYMETRIQUES.

Le SAT brut resiste (~4 h, 5 configurations). Si une solution existe,
elle a plausiblement une symetrie partielle (celle du Theoreme K etait
S_n-invariante mod 2). On teste des ansatze par sous-groupes :

 [1] S_6 x S_6 : u_T, v_T ne dependent que de k = |T inter A|
     (A = {0..5}) -> 7 variables binaires + 7 ternaires ; les
     contraintes ne dependent que de (a, b) = (|S inter A|, |S inter B|).
     ENUMERATION EXACTE (2^7 x 3^7 = 280k).
 [2] C_12 (rotation) : orbites de necklaces -> petit SAT (CaDiCaL).
 [3] u = 1 partout (mod 2 couvre w = 6, 7) + recuit mod 3 sur la
     couverture du trou w in [8, 12] (924 trits, 794 contraintes).

Tout succes => deg_6(MAJ_12) = 6 (plate confirmee), certificat verifie
exhaustivement sur les 4096 points. Echec des trois => consigne, sans
conclusion sur l'instance (les ansatze ne sont pas exhaustifs).
"""

from __future__ import annotations

import itertools
import random
import time
from math import comb

import numpy as np

random.seed(2026)
np.random.seed(2026)

N, T = 12, 6
A = set(range(6))


def verify_full(uu, vv, monos):
    """ uu, vv : dictionnaires T -> coefficient. Verification 2^12. """
    Tsets = [frozenset(Tm) for Tm in monos]
    uvals = [uu[Tm] for Tm in monos]
    vvals = [vv[Tm] for Tm in monos]
    for x in range(1 << N):
        S = frozenset(i for i in range(N) if (x >> i) & 1)
        w = len(S)
        U = sum(c for Ts, c in zip(Tsets, uvals) if Ts <= S) % 2
        V = sum(c for Ts, c in zip(Tsets, vvals) if Ts <= S) % 3
        if w < T and (U or V):
            return False
        if w >= T and not (U or V):
            return False
    return True


def ansatz_s6s6():
    pairs = [(a, b) for a in range(7) for b in range(7) if a + b >= T]
    Nk = np.array([[comb(a, k) * comb(b, T - k) for k in range(7)]
                   for (a, b) in pairs], dtype=np.int64)
    U_all = np.array(list(itertools.product(range(2), repeat=7)),
                     dtype=np.int64)
    V_all = np.array(list(itertools.product(range(3), repeat=7)),
                     dtype=np.int64)
    u_cov = (U_all @ Nk.T) % 2          # 128 x P
    v_nz = ((V_all @ Nk.T) % 3) != 0    # 2187 x P
    for r in range(u_cov.shape[0]):
        W0 = np.where(u_cov[r] == 0)[0]
        if len(W0) == 0:
            good = np.arange(V_all.shape[0])
        else:
            good = np.where(np.all(v_nz[:, W0], axis=1))[0]
        if len(good):
            return U_all[r], V_all[good[0]]
    return None, None


def ansatz_u1_anneal(budget_s=240):
    monos = list(itertools.combinations(range(N), T))
    fails = []
    for w in range(8, 13):
        fails.extend(itertools.combinations(range(N), w))
    M = np.zeros((len(fails), len(monos)), dtype=np.int8)
    for r, S in enumerate(fails):
        Ss = set(S)
        for c, Tm in enumerate(monos):
            if set(Tm) <= Ss:
                M[r, c] = 1
    M64 = M.astype(np.int64)
    v = np.random.randint(0, 3, len(monos))
    vals = (M64 @ v) % 3
    cost = int((vals == 0).sum())
    t0 = time.time()
    it = 0
    while time.time() - t0 < budget_s and cost > 0:
        it += 1
        c = random.randrange(len(monos))
        delta = random.choice((1, 2))
        nvals = (vals + delta * M64[:, c]) % 3
        ncost = int((nvals == 0).sum())
        if ncost <= cost or random.random() < 0.01:
            v[c] = (v[c] + delta) % 3
            vals = nvals
            cost = ncost
    return (v if cost == 0 else None), cost, it


def main() -> None:
    print("TACHE F-011 e24 -- n = 12 par ansatze symetriques")
    print("=" * 60)
    monos = list(itertools.combinations(range(N), T))

    print("\n[1] Ansatz S_6 x S_6 (7 orbites, enumeration exacte) :",
          flush=True)
    t0 = time.time()
    uk, vk = ansatz_s6s6()
    if uk is not None:
        print(f"    SOLUTION TROUVEE ({time.time()-t0:.0f}s) : "
              f"u_k = {list(uk)}, v_k = {list(vk)}")
        uu = {Tm: int(uk[len(set(Tm) & A)]) for Tm in monos}
        vv = {Tm: int(vk[len(set(Tm) & A)]) for Tm in monos}
        ok = verify_full(uu, vv, monos)
        print(f"    verification exhaustive 4096 points : "
              f"{'OK' if ok else '*** ECHEC ***'}")
        if ok:
            print("\n=> deg_6(MAJ_12) = 6 : PLATE CONFIRMEE, cellule fermee.")
            return
    else:
        print(f"    aucun invariant S_6 x S_6 ({time.time()-t0:.0f}s)",
              flush=True)

    print("\n[3] Ansatz u = 1 + recuit mod 3 sur le trou w in [8,12] :",
          flush=True)
    v, cost, it = ansatz_u1_anneal()
    if v is not None:
        vv = {Tm: int(v[i]) for i, Tm in enumerate(monos)}
        uu = {Tm: 1 for Tm in monos}
        ok = verify_full(uu, vv, monos)
        print(f"    SOLUTION ({it} iter) ; verification : "
              f"{'OK' if ok else '*** ECHEC ***'}")
        if ok:
            print("\n=> deg_6(MAJ_12) = 6 : PLATE CONFIRMEE, cellule fermee.")
            return
    else:
        print(f"    echec (cout final {cost}, {it} iterations)")

    print("\nAnsatze [1] et [3] sans succes -- la cellule reste ouverte")
    print("(les ansatze ne sont pas exhaustifs ; C_12 et autres sous-")
    print("groupes en reserve).")


if __name__ == "__main__":
    main()
