"""
TACHE F-011, etape 15 -- Hypothese H-v2 : les plateaux mod 6 de la zone
t = 33..40 sont gouvernes par le sous-probleme mod 3 "a trou".

MECANISME (prouve, Theoreme J etendu) : pour d < q2 = 64, U est
64-periodique donc MORTE sur [64, n] (w - 64 < t). La couverture de
[64, n] repose sur V seule.

HYPOTHESE H-v2 : deg_6^sym(MAJ_n) = m3gap(t, n) :=
    min{ d : exists v in F_3^{[t,d]} avec V(w) != 0 mod 3
             pour tout w in [64, n] }
(la couverture de [t, 63] par U mod 2 + V est supposee non-bloquante).

Test : m3gap vs valeurs mesurees (etape 12) -- 40, 40, 40, 44, 46 pour
t = 33..37 ; et tentative t = 38..40 (etape 12 : > 50, cap).
Le m3gap est cheap : la couverture ne porte que sur <= 17 poids, on
enumere le noyau (dim <= 14 -> 3^14 = 4.8M, vectorise par blocs).
"""

from __future__ import annotations

import itertools
import time
from math import comb

import numpy as np

Q2 = 64
DIM_CAP = 14
BLOCK = 200_000


def m3gap(t, n, d_cap_extra=20):
    targets = list(range(Q2, n + 1))
    for d in range(t, t + d_cap_extra + 1):
        idxs = list(range(t, d + 1))
        dim = len(idxs)
        if dim > DIM_CAP:
            return None, d
        H = np.array([[comb(w, i) % 3 for i in idxs] for w in targets],
                     dtype=np.int64)
        # enumeration par blocs
        found = False
        it = itertools.product(range(3), repeat=dim)
        while True:
            block = list(itertools.islice(it, BLOCK))
            if not block:
                break
            V = np.array(block, dtype=np.int64)
            vals = (V @ H.T) % 3
            if bool(np.all(vals != 0, axis=1).any()):
                found = True
                break
        if found:
            return d, None
    return None, t + d_cap_extra


def main() -> None:
    print("TACHE F-011 etape 15 -- hypothese H-v2 (sous-probleme a trou)")
    print("=" * 66)
    measured = {65: 40, 66: 40, 67: 40, 68: 40, 69: 40, 70: 40,
                71: 44, 72: 44, 73: 46, 74: 46}
    print(f"{'n':>3} {'t':>3} | {'m3gap':>6} | {'deg_6 mesure':>12} | verdict")
    print("-" * 66)
    agree = 0
    tested = 0
    for n in range(65, 81):
        t = (n + 1) // 2
        t0 = time.time()
        val, cap = m3gap(t, n)
        meas = measured.get(n)
        if val is None:
            print(f"{n:>3} {t:>3} | >cap({cap}) | {str(meas or '>50'):>12} | "
                  f"non conclu   ({time.time()-t0:.0f}s)", flush=True)
            continue
        if meas is not None:
            tested += 1
            ok = (val == meas)
            agree += ok
            print(f"{n:>3} {t:>3} | {val:>6} | {meas:>12} | "
                  f"{'MATCH' if ok else '*** ECART ***'}   "
                  f"({time.time()-t0:.0f}s)", flush=True)
        else:
            print(f"{n:>3} {t:>3} | {val:>6} | {'>50 (cap e12)':>12} | "
                  f"prediction H-v2   ({time.time()-t0:.0f}s)", flush=True)
    print("-" * 66)
    print(f"\nAccord H-v2 sur les cellules mesurees : {agree}/{tested}")
    if agree == tested and tested > 0:
        print("H-v2 CONFIRMEE sur le domaine mesure : les plateaux v2 sont le")
        print("sous-probleme mod 3 a trou. Les valeurs t = 38..40 ci-dessus")
        print("sont des PREDICTIONS falsifiables (a tester avec plus de cap).")
    else:
        print("H-v2 incomplete ou fausse -- la couverture de [t, 63] joue.")


if __name__ == "__main__":
    main()
