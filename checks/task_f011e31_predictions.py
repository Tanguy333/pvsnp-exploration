"""
TACHE F-011, etape 31 -- test des predictions de la loi bipartite
" 3-lisses U {5} " sur t = 21..27.

Predictions (loi v2, e30) :
  t = 21 = 3*7   -> INSOLUBLE
  t = 22 = 2*11  -> INSOLUBLE
  t = 23 premier -> INSOLUBLE
  t = 24 = 2^3*3 -> soluble
  t = 25 = 5^2   -> INSOLUBLE (l'exception t = 5 ne se propage pas)
  t = 26 = 2*13  -> INSOLUBLE
  t = 27 = 3^3   -> soluble (et |A| = 1 attendu : puissance pure)
"""

from __future__ import annotations

import time

from task_f011e25_ansatz_machine import try_partition


def smooth3(t):
    while t % 2 == 0:
        t //= 2
    while t % 3 == 0:
        t //= 3
    return t == 1


def main() -> None:
    print("TACHE F-011 e31 -- predictions de la loi bipartite, t = 21..27")
    print("=" * 64)
    all_ok = True
    for t in range(21, 28):
        n = 2 * t
        pred = smooth3(t) or t == 5
        t0 = time.time()
        good = []
        for sa in range(1, t + 1):
            r = try_partition(n, t, (sa, n - sa))
            if r is not None and r != "ECHEC-VERIF":
                good.append(sa)
                if not pred:
                    break  # un seul suffit a refuter
        obs = bool(good)
        ok = (obs == pred)
        all_ok &= ok
        print(f"  t = {t:>2} : prediction {'soluble' if pred else 'insoluble'}"
              f" ; observe {'soluble |A|=' + str(good[:5]) if obs else 'insoluble'}"
              f"   [{'CONFORME' if ok else '*** CONTRE-EXEMPLE ***'}]"
              f"   ({time.time()-t0:.0f}s)", flush=True)
    print("=" * 64)
    print("LOI v2 (3-lisses U {5}) :",
          "26/26 points -- tient" if all_ok else "REFUTEE -- voir ci-dessus")


if __name__ == "__main__":
    main()
