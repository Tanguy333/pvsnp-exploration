"""
TACHE V-016c v2 -- extension PARALLELE du certificat taille 11,
RELANCE après l'incident nocturne (mort silencieuse du run v1,
vraisemblablement OOM des rationnels exacts en dimension > 135).

Corrections de conception (post-mortem consigné) :
 1. PETITES CELLULES D'ABORD : le certificat est un préfixe consécutif
    -- chaque cellule finie est immédiatement acquise.
 2. PERSISTANCE PAR CELLULE : chaque worker écrit son verdict dans
    checks/v016c_out/res_<n>.txt dès la fin -- plus d'otages.
 3. REPRISE : les cellules déjà résolues (fichier présent) sont sautées.
 4. 12 workers (cœurs physiques) au lieu de 20 : pression mémoire
    réduite ; plafond n = 132 (les monstres 133+ attendront un
    Gram-Schmidt moins gourmand).
"""

from __future__ import annotations

import multiprocessing as mp
import os
import time

CELLS = list(range(111, 133))   # petites d'abord (ordre croissant)
WORKERS = 12
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "v016c_out")


def run_cell(n):
    path = os.path.join(OUTDIR, f"res_{n}.txt")
    if os.path.exists(path):
        return (n, "deja fait", 0.0)
    t0 = time.time()
    from task_v004_kv_conjecture5 import build_basis, lll_reduce
    from task_v017c_verif_exacte import exact_shortest
    G = lll_reduce(build_basis(n, 10))
    n2, sols = exact_shortest(G)

    def ends_unit(v):
        nz = [int(x) for x in v if int(x) != 0]
        return abs(nz[0]) == 1 and abs(nz[-1]) == 1

    exists = any(ends_unit(v) for v in sols)
    dt = time.time() - t0
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"n={n} min={n2} minima={len(sols)} "
                f"bouts={'OUI' if exists else 'NON'} t={dt:.0f}s\n")
    return (n, f"min={n2} bouts={'OUI' if exists else 'NON'}", dt)


def main() -> None:
    os.makedirs(OUTDIR, exist_ok=True)
    print(f"V-016c v2 -- n = 111..132, {WORKERS} workers, petites d'abord, "
          f"persistance par cellule", flush=True)
    with mp.Pool(WORKERS) as pool:
        for (n, msg, dt) in pool.imap_unordered(run_cell, CELLS):
            print(f"  n = {n} : {msg}   ({dt:.0f}s)", flush=True)
    print("Termine.", flush=True)


if __name__ == "__main__":
    main()
