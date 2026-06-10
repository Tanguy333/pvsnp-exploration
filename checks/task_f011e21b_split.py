"""
TACHE F-011, etape 21b -- n = 13 (rapide attendu) puis n = 12 avec
garde-fou d'interruption (25 min) : SAT / UNSAT / INDECIS honnete.

Contexte : n = 10, 11 -> SAT en ~1 s (certificats verifies). n = 12
(cas pair, w = 2t avec C(12,6) = 924 = 0 mod 6 -- le poids de type
anomalie) resiste : 36+ min de CaDiCaL sans verdict. On scinde.
"""

from __future__ import annotations

import threading
import time

from pysat.solvers import Cadical153

from task_f011e21_sat_n10 import build, verify

N12_BUDGET_S = 1500.0   # 25 min


def run(n, budget=None):
    t = (n + 1) // 2
    t0 = time.time()
    cnf, monos, u, v1, v2 = build(n)
    print(f"\nn = {n} (t = {t}) : {cnf.nv} vars, {len(cnf.clauses)} clauses "
          f"({time.time()-t0:.0f}s)", flush=True)
    solver = Cadical153(bootstrap_with=cnf.clauses)
    timer = None
    if budget:
        timer = threading.Timer(budget, solver.interrupt)
        timer.start()
    t0 = time.time()
    res = solver.solve_limited(expect_interrupt=bool(budget)) \
        if budget else solver.solve()
    dt = time.time() - t0
    if timer:
        timer.cancel()
    if res is True:
        ok = verify(solver.get_model(), monos, u, v1, v2, n)
        print(f"  SAT ({dt:.0f}s) ; verification 2^{n} points : "
              f"{'OK' if ok else '*** ECHEC ***'}")
        print(f"  => deg_6(MAJ_{n}) = {t} : plate CONFIRMEE.", flush=True)
    elif res is False:
        print(f"  UNSAT ({dt:.0f}s)")
        print(f"  => deg_6(MAJ_{n}) >= {t+1} : PLATE REFUTEE a n = {n}.",
              flush=True)
    else:
        print(f"  INDECIS -- interrompu apres {dt:.0f}s (budget {budget:.0f}s)")
        print(f"  => statut de n = {n} OUVERT : l'instance resiste a CDCL")
        print("     (structure XOR-lourde ; pistes : CryptoMiniSat avec")
        print("     elimination gaussienne native, ou cassage de symetrie).",
              flush=True)
    solver.delete()


def main() -> None:
    print("TACHE F-011 e21b -- n = 12 et 13, garde-fou 20 min CHACUN")
    print("(correction : v1 n'avait de budget que sur n = 12 ; n = 13")
    print(" s'est revele dur aussi -- C(w,7) pair sur tout [8,13], le")
    print(" mod 3 porte toute la couverture)")
    print("=" * 62)
    run(12, budget=1200.0)
    run(13, budget=1200.0)


if __name__ == "__main__":
    main()
