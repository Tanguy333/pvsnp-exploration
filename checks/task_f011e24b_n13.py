"""
TACHE F-011, etape 24b -- deg_6(MAJ_13) = 7 ? par ansatz biparti S_6 x S_7.

Suite immediate du succes n = 12 (ansatz S_6 x S_6 : solution purement
mod 3, v_k = (1,1,1,2,1,1,1), en 0 s la ou le SAT brut a echoue 4 h).
Ici : A = {0..5} (6 elements), B = {6..12} (7 elements) ; monomes =
7-sous-ensembles, orbite k = |T inter A| in [0, 6] ; contraintes par
(a, b) = (|S inter A|, |S inter B|), a + b >= 7.
Enumeration exacte 2^7 x 3^7 = 280k. Verification exhaustive 8192 points.
"""

from __future__ import annotations

import itertools
import time
from math import comb

import numpy as np

N, T = 13, 7
A = set(range(6))          # |A| = 6, |B| = 7


def main() -> None:
    print("TACHE F-011 e24b -- n = 13 par ansatz S_6 x S_7")
    print("=" * 58)
    t0 = time.time()
    pairs = [(a, b) for a in range(7) for b in range(8) if a + b >= T]
    Nk = np.array([[comb(a, k) * comb(b, T - k) for k in range(7)]
                   for (a, b) in pairs], dtype=np.int64)
    U_all = np.array(list(itertools.product(range(2), repeat=7)),
                     dtype=np.int64)
    V_all = np.array(list(itertools.product(range(3), repeat=7)),
                     dtype=np.int64)
    u_cov = (U_all @ Nk.T) % 2
    v_nz = ((V_all @ Nk.T) % 3) != 0
    sol = None
    for r in range(u_cov.shape[0]):
        W0 = np.where(u_cov[r] == 0)[0]
        good = (np.arange(V_all.shape[0]) if len(W0) == 0
                else np.where(np.all(v_nz[:, W0], axis=1))[0])
        if len(good):
            sol = (U_all[r], V_all[good[0]])
            break
    if sol is None:
        print(f"    aucun invariant S_6 x S_7 ({time.time()-t0:.0f}s) --")
        print("    cellule toujours ouverte (autres bipartitions/sous-")
        print("    groupes en reserve : S_5 x S_8, C_13...)")
        return
    uk, vk = sol
    print(f"    SOLUTION ({time.time()-t0:.0f}s) : u_k = {list(map(int, uk))}, "
          f"v_k = {list(map(int, vk))}")
    monos = list(itertools.combinations(range(N), T))
    uu = [int(uk[len(set(Tm) & A)]) for Tm in monos]
    vv = [int(vk[len(set(Tm) & A)]) for Tm in monos]
    Tsets = [frozenset(Tm) for Tm in monos]
    ok = True
    for x in range(1 << N):
        S = frozenset(i for i in range(N) if (x >> i) & 1)
        w = len(S)
        U = sum(c for Ts, c in zip(Tsets, uu) if Ts <= S) % 2
        V = sum(c for Ts, c in zip(Tsets, vv) if Ts <= S) % 3
        if (w < T and (U or V)) or (w >= T and not (U or V)):
            ok = False
            break
    print(f"    verification exhaustive 8192 points : "
          f"{'OK' if ok else '*** ECHEC ***'}")
    if ok:
        print("\n=> deg_6(MAJ_13) = 7 : PLATE CONFIRMEE, cellule fermee.")


if __name__ == "__main__":
    main()
