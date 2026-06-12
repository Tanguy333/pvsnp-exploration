"""
MARCHE TURBO -- balayage sequentiel d'une ligne d du reseau KV avec le
moteur compile (svp_turbo, V-038), persistance par cellule et reprise.

Usage : python march_turbo.py <d> <n_debut> <n_fin> <outdir>

Pour chaque cellule (d, n) : min exact, bouts +-1 parmi les minimaux,
existence d'un minimum PLAT (tous coefficients +-1) ; si plat, le
temoin A/B est ecrit dans le fichier de la cellule. Une cellule deja
presente dans outdir est sautee (reprise apres interruption).
"""

from __future__ import annotations

import os
import sys
import time

from task_v004_kv_conjecture5 import build_basis
from svp_turbo import turbo_lll, turbo_shortest


def main() -> None:
    d = int(sys.argv[1])
    n0 = int(sys.argv[2])
    n1 = int(sys.argv[3])
    outdir = sys.argv[4]
    os.makedirs(outdir, exist_ok=True)
    print(f"MARCHE TURBO d = {d}, n = {n0}..{n1} -> {outdir}", flush=True)
    for n in range(n0, n1 + 1):
        path = os.path.join(outdir, f"res_{n}.txt")
        if os.path.exists(path):
            continue
        t0 = time.time()
        G = turbo_lll(build_basis(n, d))
        n2, sols = turbo_shortest(G)
        dt = time.time() - t0
        ends = False
        flat = None
        for v in sols:
            c = [int(t) for t in v]
            nz = [t for t in c if t]
            if abs(nz[0]) == 1 and abs(nz[-1]) == 1:
                ends = True
            if max(abs(t) for t in c) == 1:
                flat = c
        lines = [f"n={n} min={n2} minima={len(sols)//2} "
                 f"bouts={'OUI' if ends else 'NON'} "
                 f"plat={'OUI' if flat else 'non'} t={dt:.0f}s"]
        tag = ""
        if flat is not None:
            A = [i for i, t in enumerate(flat) if t > 0]
            B = [i for i, t in enumerate(flat) if t < 0]
            lines.append(f"A={A}")
            lines.append(f"B={B}")
            tag = f"  <<< PLAT (taille {n2 // 2})"
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"  (d={d}, n={n}) : min={n2}, bouts "
              f"{'OUI' if ends else 'NON'}{tag}   ({dt:.0f}s)", flush=True)
    print("Marche terminee.", flush=True)


if __name__ == "__main__":
    main()
