"""
TACHE F-011, etape 33 -- [A] la plate sur n = 25..31 (multipartitions) ;
[B] departage t = 36 = 4*9 (la famille {4*3^b} existe-t-elle ?).

[A] n = 25..31 couvre les t bipartite-insolubles 13, 14, 15 : la
    machine multipartite (e25) doit fermer ces cellules. Budget
    300 s/cellule. Verification par profils (invariance par
    construction).
[B] t = 36, n = 72 : 12 = 4*3 est soluble (sporadique ?) mais
    24 = 8*3 insoluble. Si 36 = 4*9 est soluble -> candidate famille
    {4*3^b} ; sinon -> 12 reste sporadique.
"""

from __future__ import annotations

import time

from task_f011e25_ansatz_machine import try_partition, partitions_catalog


def main() -> None:
    print("TACHE F-011 e33 -- plate n = 25..31 + departage t = 36")
    print("=" * 64)

    print("\n[A] Plate n = 25..31 (machine multipartite) :", flush=True)
    for n in range(25, 32):
        t = (n + 1) // 2
        t0 = time.time()
        won = None
        tried = 0
        for P in partitions_catalog(n):
            tried += 1
            r = try_partition(n, t, P)
            if r is not None and r != "ECHEC-VERIF":
                won = P
                break
            if time.time() - t0 > 300:
                break
        if won:
            print(f"  n={n} (t={t}) : FERME par {won} "
                  f"({tried} partitions, {time.time()-t0:.0f}s)", flush=True)
        else:
            print(f"  n={n} (t={t}) : OUVERT apres {tried} partitions "
                  f"({time.time()-t0:.0f}s)", flush=True)

    print("\n[B] Departage t = 36 = 4*9 (n = 72, bipartitions seules) :",
          flush=True)
    t0 = time.time()
    good = []
    for sa in range(1, 37):
        r = try_partition(72, 36, (sa, 72 - sa))
        if r is not None and r != "ECHEC-VERIF":
            good.append(sa)
    if good:
        print(f"  t = 36 : SOLUBLE |A| = {good[:8]}{'...' if len(good) > 8 else ''}"
              f" ({time.time()-t0:.0f}s) -> candidate famille {{4*3^b}}")
    else:
        print(f"  t = 36 : INSOLUBLE ({time.time()-t0:.0f}s) "
              f"-> 12 reste sporadique")


if __name__ == "__main__":
    main()
