"""
TACHE V-015 -- Conjecture 5 de KV a d = 7 : cloture TOTALE visee.

Perspective : la plus petite ideale de taille 8 connue est TARRY 1913,
support [0, 50] (" first known, smallest known ", Chen Shuwen). Si le
reseau (i) verifie les bouts +-1 sur tout n = 8..49 et (ii) trouve la
transition a n*(7) = 50 avec temoin plat verifie en exact, alors par
V11 : Conjecture 5 vraie pour d = 7 et TOUT n >= 8 -- SANS TROU
(contrairement a d = 6, temoin a 102).

Schema V13/V14 : SVP exact (LLL + Fincke-Pohst) par cellule ; a la
transition (norme2 = 2(d+1) = 16), extraire un minimum plat, verifier
la propriete PTE ideale de taille 8 en exact.
"""

from __future__ import annotations

import time

from task_v004_kv_conjecture5 import build_basis, lll_reduce, shortest_vectors

D = 7
TARGET = 2 * (D + 1)


def ends_unit(v):
    nz = [int(x) for x in v if int(x) != 0]
    return abs(nz[0]) == 1 and abs(nz[-1]) == 1


def main() -> None:
    print("TACHE V-015 -- Conjecture 5, d = 7 : vers la cloture totale")
    print("=" * 66)
    ok_all = True
    n_star = None
    for n in range(D + 1, 56):
        t0 = time.time()
        G = lll_reduce(build_basis(n, D))
        n2, sols = shortest_vectors(G)
        exists = any(ends_unit(v) for v in sols)
        ok_all &= exists
        print(f"  (d=7, n={n:>2}) : norme2={n2:>4}, {len(sols):>4} minima, "
              f"bouts +-1 : {'OUI' if exists else '*** NON ***'}   "
              f"({time.time()-t0:.0f}s)", flush=True)
        if n2 <= TARGET and n_star is None:
            n_star = n
            flat = None
            for v in sols:
                coefs = [int(x) for x in v]
                if all(abs(c) <= 1 for c in coefs) and ends_unit(v):
                    A = [a for a, c in enumerate(coefs) if c > 0]
                    B = [a for a, c in enumerate(coefs) if c < 0]
                    if (len(A) == len(B) == D + 1 and
                            all(sum(a ** j for a in A)
                                == sum(b ** j for b in B)
                                for j in range(1, D + 1))):
                        flat = (A, B)
                        break
            if flat:
                A, B = flat
                print(f"\n  TRANSITION n*(7) = {n} : temoin PTE ideal "
                      f"taille 8 (verifie en exact) :")
                print(f"      A = {A}")
                print(f"      B = {B}\n", flush=True)
            else:
                print(f"\n  norme {TARGET} a n = {n} sans minimum plat PTE "
                      f"?! -- A EXAMINER\n", flush=True)
                ok_all = False
            break
    print("=" * 66)
    if ok_all and n_star:
        print(f"THEOREME V15 : Conjecture 5 VRAIE pour d = 7, TOUT n >= 8 --")
        print(f"  * n < {n_star} : exhaustif ci-dessus ;")
        print(f"  * n >= {n_star} : V11 + temoin decale x^(n-n*).")
        print(f"AUCUN TROU. Transitions : 6, 6, 11, 18, 23, (81,102], "
              f"{n_star} (d = 1..7).")
    elif ok_all:
        print("Bouts +-1 partout mais transition non atteinte avant 56 --")
        print("n*(7) > 55 ?! (contredirait Tarry 1913 a 50 : VERIFIER)")
    else:
        print("ECHEC ou anomalie -- voir ci-dessus.")


if __name__ == "__main__":
    main()
