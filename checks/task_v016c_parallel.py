"""
TACHE V-016c -- extension PARALLELE du certificat taille 11 :
d = 10, n = 111..148, multiprocessing sur ~20 workers (24 coeurs).

Chaque cellule est independante : Pool dynamique, les grosses cellules
sont lancees en premier (tri decroissant) pour optimiser le makespan.
Verdict par cellule : norme min, nb minima, bouts +-1 (Conjecture 5),
alerte si norme <= 22 (ideale de taille 11 !).
"""

from __future__ import annotations

import multiprocessing as mp
import time

CELLS = list(range(148, 110, -1))   # grosses d'abord
WORKERS = 20


def run_cell(n):
    t0 = time.time()
    from task_v004_kv_conjecture5 import build_basis, lll_reduce
    from task_v017c_verif_exacte import exact_shortest
    G = lll_reduce(build_basis(n, 10))
    n2, sols = exact_shortest(G)
    def ends_unit(v):
        nz = [int(x) for x in v if int(x) != 0]
        return abs(nz[0]) == 1 and abs(nz[-1]) == 1
    exists = any(ends_unit(v) for v in sols)
    return (n, n2, len(sols), exists, time.time() - t0)


def main() -> None:
    print(f"TACHE V-016c (parallele) -- d = 10, n = 111..148, "
          f"{WORKERS} workers / 24 coeurs", flush=True)
    t0 = time.time()
    results = {}
    with mp.Pool(WORKERS) as pool:
        for (n, n2, nb, exists, dt) in pool.imap_unordered(run_cell, CELLS):
            results[n] = (n2, exists)
            alerte = "  <<< NORME <= 22 : IDEALE ?!" if n2 <= 22 else ""
            print(f"  (d=10, n={n}) : norme2={n2:>3}, {nb:>3} minima, "
                  f"bouts +-1 : {'OUI' if exists else '*** NON ***'}"
                  f"{alerte}   ({dt:.0f}s)", flush=True)
    ok = [n for n in sorted(results) if results[n][0] > 22]
    consecutif = 110
    for n in range(111, 149):
        if n in results and results[n][0] > 22:
            consecutif = n
        else:
            break
    print(f"\nTermine en {(time.time()-t0)/3600:.1f} h.", flush=True)
    print(f"CERTIFICAT etendu : aucune ideale de taille 11 a support "
          f"dans [0, {consecutif}].", flush=True)
    bad = [n for n in sorted(results) if not results[n][1]]
    print(f"Conjecture 5 (d=10) : "
          f"{'aucune exception' if not bad else 'EXCEPTIONS : ' + str(bad)}")


if __name__ == "__main__":
    main()
