"""
TACHE V-002 (a) -- Le duel symetrique vs general sur le tore, n = 5 et 6.

V-001 a montre l'egalite exacte eps*(sym) = eps*(general) a n = 3, 4.
Si elle persiste a n = 5, 6, c'est une donnee empirique notable pour la
question ouverte de BHLR (la symetrisation WLOG sur le tore n'est pas
prouvee ; le cas general de leur conjecture reste ouvert).
MAJ_5 et MAJ_6 : t = 3.
"""

from __future__ import annotations

import time

from task_v001_torus import torus_sym_eps, torus_gen_eps


def main() -> None:
    print("TACHE V-002 (a) -- tore : sym vs general, n = 5, 6")
    print("=" * 64)
    all_eq = True
    for n in (5, 6):
        for d in range(1, n + 1):
            t0 = time.time()
            es, cs = torus_sym_eps(n, d)
            eg, cg = torus_gen_eps(n, d)
            gain = (es is not None and eg is not None and eg < es - 1e-6)
            all_eq &= not gain
            print(f"    n={n}, d={d} : sym = {es:.4f}{'~' if cs else ''} ; "
                  f"general = {eg:.4f}{'~' if cg else ''}   "
                  f"[{'GAIN ASYM' if gain else '='}]   "
                  f"({time.time()-t0:.0f}s)", flush=True)
            if es is not None and es < 1e-9 and eg is not None and eg < 1e-9:
                break
    print("\nVerdict :", "egalite sym = general partout (n <= 6)"
          if all_eq else "L'ASYMETRIE GAGNE quelque part -- voir ci-dessus")


if __name__ == "__main__":
    main()
