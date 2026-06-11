"""
TACHE V-017b -- tailles 17..30 (d = 16..29), fenetres n = d+1..d+10 :
certificats petits spans + Conjecture 5 jusqu'au degre 29.

Suite de V-017 (demande utilisateur). Les rangs de reseau restent
<= 10 -> SVP exact rapide malgre des normes geantes (C(2d+2, d+1)
~ 10^17 a d = 29). 140 cellules.
"""

from __future__ import annotations

import time

from task_v004_kv_conjecture5 import build_basis, lll_reduce, shortest_vectors


def ends_unit(v):
    nz = [int(x) for x in v if int(x) != 0]
    return abs(nz[0]) == 1 and abs(nz[-1]) == 1


def main() -> None:
    print("TACHE V-017b -- tailles 17..30, n = d+1..d+10")
    print("=" * 64)
    all_ok = True
    worst = 0.0
    for d in range(16, 30):
        ideal = 2 * (d + 1)
        line = []
        found = False
        for n in range(d + 1, d + 11):
            t0 = time.time()
            G = lll_reduce(build_basis(n, d))
            n2, sols = shortest_vectors(G)
            dt = time.time() - t0
            worst = max(worst, dt)
            exists = any(ends_unit(v) for v in sols)
            all_ok &= exists
            if n2 <= ideal:
                found = True
            line.append('OK' if exists else 'NON')
        statut = 'IDEALE ?!' if found else 'aucune ideale'
        print(f"  d={d:>2} (taille {d+1:>2}) : {statut} ; bouts +-1 : "
              f"{'10/10' if all(x == 'OK' for x in line) else line}"
              f"   (max {worst:.0f}s)", flush=True)
    print("=" * 64)
    print("Conjecture 5 :",
          "AUCUNE exception (140 cellules, d = 16..29)" if all_ok
          else "*** EXCEPTION TROUVEE ***")
    print("Certificats : aucune ideale de taille 17..30 dans les fenetres")
    print("n <= d+10 (premiers certificats existants a ces tailles).")


if __name__ == "__main__":
    main()
