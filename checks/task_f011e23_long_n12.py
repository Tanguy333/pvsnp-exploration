"""
TACHE F-011, etape 23 -- run LONG (4 h) sur n = 12 seul, CMS + cassage
de symetrie. La cellule decisive : premier point 2t hors Theoreme K
(t = 6 non puissance de 2). SAT -> plate confirmee ; UNSAT -> plate
refutee au poids d'anomalie ; INDECIS -> probleme ouvert executable.
"""

from __future__ import annotations

import time

import task_f011e22_symbreak as sb

sb.MAXTIME = 14400  # 4 h


def main() -> None:
    n, t = 12, 6
    print("TACHE F-011 e23 -- n = 12, CMS + sym-break, maxtime 4 h")
    print("=" * 60)
    t0 = time.time()
    e, monos, u, v1, v2 = sb.build_sym(n)
    path = f"cms_sym_long_n{n}.cnf"
    sb.write_dimacs(e, path)
    print(f"n = {n} : {e.nv} vars, {len(e.cnf)} CNF + {len(e.xors)} XOR "
          f"({time.time()-t0:.0f}s)", flush=True)
    t0 = time.time()
    res, model = sb.solve(path)
    dt = time.time() - t0
    if res is True:
        ok = sb.verify(n, model, monos, u, v1, v2)
        print(f"SAT ({dt:.0f}s) ; verification 2^{n} : "
              f"{'OK' if ok else '*** ECHEC ***'}")
        print(f"=> deg_6(MAJ_12) = {t} : plate CONFIRMEE.")
    elif res is False:
        print(f"UNSAT ({dt:.0f}s)")
        print(f"=> deg_6(MAJ_12) >= {t+1} : PLATE REFUTEE au poids d'anomalie.")
    else:
        print(f"INDECIS apres {dt:.0f}s (4 h) -- probleme ouvert executable.")


if __name__ == "__main__":
    main()
