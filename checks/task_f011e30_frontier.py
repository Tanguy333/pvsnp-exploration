"""
TACHE F-011, etape 30 -- donnees t = 14..20 : la frontiere de
solvabilite bipartite a n = 2t.

Acquis (e29) : solubles {2,3,4,5,6,8,9,12} / insolubles {7,10,11,13} --
la 3-lissite est refutee (t = 5). Sous-motif observe : puissances pures
(3, 4, 8, 9) -> |A| = 1 suffit ; mixtes (5, 6, 12) -> |A| grand.
Ici : t = 14..20 avec l'ENSEMBLE des tailles |A| qui marchent.
"""

from __future__ import annotations

import time

from task_f011e25_ansatz_machine import try_partition


def main() -> None:
    print("TACHE F-011 e30 -- frontiere bipartite, t = 14..20")
    print("=" * 62)
    table = {2: [1], 3: [1], 4: [1], 5: [5], 6: [4], 8: [1], 9: [1],
             12: [7]}  # premiers |A| connus (e29, premier trouve)
    for t in range(14, 21):
        n = 2 * t
        t0 = time.time()
        good = []
        for sa in range(1, t + 1):
            r = try_partition(n, t, (sa, n - sa))
            if r is not None and r != "ECHEC-VERIF":
                good.append(sa)
        table[t] = good
        print(f"  t = {t:>2} (n = {n}) : "
              f"{'solubles |A| = ' + str(good) if good else 'INSOLUBLE'}"
              f"   ({time.time()-t0:.0f}s)", flush=True)
    print("\nTable cumulee (t -> tailles |A| solubles, e29 = 1er trouve) :")
    for t in sorted(table):
        print(f"  {t:>2} : {table[t] if table[t] else '---'}")
    print("\nFacteurs premiers, pour la lecture :")
    for t in sorted(table):
        f = []
        x = t
        for p in (2, 3, 5, 7, 11, 13, 17, 19):
            while x % p == 0:
                f.append(p)
                x //= p
        print(f"  {t:>2} = {'*'.join(map(str, f))} : "
              f"{'soluble' if table[t] else 'insoluble'}")


if __name__ == "__main__":
    main()
