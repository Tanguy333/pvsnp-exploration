"""
TACHE F-011, etape 27 -- donnees pour la construction tripartite
generale : extension n = 21..24 + dissection des certificats.

[A] Machine a ansatze sur n = 21..24 (t = 11, 12 -- territoire neuf).
[B] Re-derivation et DUMP des tables d'orbites des certificats
    tripartites connus : (13, (4,4,5)), (19, (3,7,9)), (20, (4,7,9)).
[C] Observations : les coefficients v par orbite suivent-ils une forme
    produit (a la K') ?
"""

from __future__ import annotations

import itertools
import time

from task_f011e25_ansatz_machine import try_partition, partitions_catalog


def run_cell(n):
    t = (n + 1) // 2
    t0 = time.time()
    for P in partitions_catalog(n):
        r = try_partition(n, t, P)
        if r is not None and r != "ECHEC-VERIF":
            return P, r, time.time() - t0
        if time.time() - t0 > 300:
            break
    return None, None, time.time() - t0


def dump(n, P):
    t = (n + 1) // 2
    r = try_partition(n, t, P)
    if r is None or r == "ECHEC-VERIF":
        print(f"  ({n}, {P}) : re-derivation echouee ?!")
        return
    uk, vk = r
    print(f"\n  --- certificat (n={n}, t={t}, P={P}) ---")
    print(f"  u non nuls : {sorted(o for o in uk if uk[o])}")
    print(f"  v par orbite (non nuls) :")
    for o in sorted(vk):
        if vk[o]:
            print(f"      {o} -> {vk[o]}")


def main() -> None:
    print("TACHE F-011 e27 -- donnees tripartites + extension n = 21..24")
    print("=" * 66)

    print("\n[A] Extension n = 21..24 :", flush=True)
    for n in range(21, 25):
        P, r, dt = run_cell(n)
        t = (n + 1) // 2
        if P:
            uk, vk = r
            u_nz = sum(1 for o in uk if uk[o])
            v_nz = sum(1 for o in vk if vk[o])
            print(f"  n={n} (t={t}) : FERME par {P} ({dt:.0f}s) ; "
                  f"|u|={u_nz}, |v|={v_nz} "
                  f"{'[PUR MOD 3]' if u_nz == 0 else ''}", flush=True)
        else:
            print(f"  n={n} (t={t}) : OUVERT ({dt:.0f}s)", flush=True)

    print("\n[B] Dissection des certificats tripartites connus :", flush=True)
    for (n, P) in ((13, (4, 4, 5)), (19, (3, 7, 9)), (20, (4, 7, 9))):
        dump(n, P)

    print("\n[C] A inspecter : formes produit C(.,.) par blocs ? motifs")
    print("    de digits base 2/3 dans les orbites actives ?")


if __name__ == "__main__":
    main()
