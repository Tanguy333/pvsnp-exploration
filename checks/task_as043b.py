"""
TACHE AS-043 (phase 2) -- les 3 cellules manquantes, echelles
STRICTEMENT moderees x in {1.6, 0.8, 0.4} (la phase 1 a brule son
budget sur un x=0.2 deja connu d'AS-042 — coherence 3.036e-7 vs
3.04e-7, controle involontaire). Fit sur la paire (0.8, 0.4).
Cellules : (11,2) r9, (13,3) r10, (13,2) r11.
"""

from __future__ import annotations

import sys
import time
from math import log, pi

sys.path.insert(0, "checks")
from task_as043 import cell_setup, rho_at  # noqa: E402

T0 = time.time()
BUDGET = 540.0


def main():
    for (n, d) in [(11, 2), (13, 3), (13, 2)]:
        if time.time() - T0 > BUDGET:
            print(f"(n={n}, d={d}) : SKIP (budget)", flush=True)
            continue
        Gi, Cf, r, Dv = cell_setup(n, d)
        print(f"(n={n}, d={d}) r={r}, 4D = {4*float(Dv):.4f} "
              f"(D = {Dv})", flush=True)
        pts = []
        for x in [1.6, 0.8, 0.4]:
            if time.time() - T0 > BUDGET:
                print(f"   x={x}: SKIP (budget)", flush=True)
                continue
            t1 = time.time()
            rho, nd = rho_at(Gi, Cf, Dv, x)
            L = log(1.0 / rho) if rho > 0 else float("inf")
            print(f"   x={x}: rho={rho:.3e}  ln(1/rho)={L:.3f}  "
                  f"c(x)={pi/x - L:+.3f}  ({nd} pts, "
                  f"{time.time()-t1:.0f}s)", flush=True)
            pts.append((x, L))
        if len(pts) >= 2:
            (x1, L1), (x2, L2) = pts[-2], pts[-1]
            a = (L2 - L1) / (1 / x2 - 1 / x1)
            print(f"   fit 2 pts ({x1},{x2}) : pente a = {a:.3f} "
                  f"(pi = {pi:.3f}), c = {a / x2 - L2:+.3f}",
                  flush=True)


if __name__ == "__main__":
    main()
