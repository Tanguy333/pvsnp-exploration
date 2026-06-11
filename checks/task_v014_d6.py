"""
TACHE V-014 -- Conjecture 5 de KV a d = 6 : zone sous-transition +
decouverte de la transition n*(6) par le reseau.

Schema du Theoreme V13, un cran plus haut :
 [1] balayer n = 7..34 en SVP EXACT (LLL + Fincke-Pohst, outillage
     V-004) : pour chaque cellule sous-transition, verifier qu'un
     minimum a ses bouts +-1 (reformulation de la Conjecture 5) ;
 [2] la transition n*(6) = premier n ou min = 2(d+1) = 14 : extraire
     un temoin plat, verifier EN EXACT la propriete PTE ideale de
     taille 7 (sommes de puissances 1..6 egales) et ses bouts +-1 ;
 [3] si [1] sans exception et [2] reussi : THEOREME V14 -- la
     Conjecture 5 vaut pour d = 6 et TOUT n >= 7 (V11 au-dela de la
     transition, exhaustif en-deca).

Cout : la dimension du reseau atteint ~35 ; Fincke-Pohst est exponentiel
en dimension -- budget par cellule affiche, echec honnete si timeout.
"""

from __future__ import annotations

import time

from task_v004_kv_conjecture5 import build_basis, lll_reduce, shortest_vectors

D = 6
TARGET = 2 * (D + 1)


def ends_unit(v):
    nz = [int(x) for x in v if int(x) != 0]
    return abs(nz[0]) == 1 and abs(nz[-1]) == 1


def main() -> None:
    print("TACHE V-014 -- Conjecture 5, d = 6 : sous-transition + n*(6)")
    print("=" * 66)
    ok_all = True
    n_star = None
    for n in range(D + 1, 35):
        t0 = time.time()
        G = lll_reduce(build_basis(n, D))
        n2, sols = shortest_vectors(G)
        exists = any(ends_unit(v) for v in sols)
        ok_all &= exists
        print(f"  (d=6, n={n:>2}) : norme2={n2:>3}, {len(sols):>4} minima, "
              f"bouts +-1 : {'OUI' if exists else '*** NON ***'}   "
              f"({time.time()-t0:.0f}s)", flush=True)
        if n2 == TARGET and n_star is None:
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
                print(f"\n  TRANSITION n*(6) = {n} : temoin PTE ideal "
                      f"taille 7 (verifie en exact) :")
                print(f"      A = {A}")
                print(f"      B = {B}\n", flush=True)
            else:
                print(f"\n  norme {TARGET} atteinte a n = {n} mais aucun "
                      f"minimum plat PTE ?! -- A EXAMINER\n", flush=True)
                ok_all = False
            break
    print("=" * 66)
    if ok_all and n_star:
        print(f"THEOREME V14 : Conjecture 5 VRAIE pour d = 6, tout n >= 7 --")
        print(f"  * n < {n_star} : exhaustif ci-dessus (bouts +-1 partout) ;")
        print(f"  * n >= {n_star} : Theoreme V11 + temoin decale x^(n-n*).")
        print(f"Transitions connues : n* = 6, 6, 11, 18, 23, {n_star} "
              f"(d = 1..6).")
    elif ok_all:
        print("Sous-transition OK jusqu'a n = 34 mais transition non")
        print("atteinte -- prolonger le balayage (n*(6) > 34 ?).")
    else:
        print("ECHEC ou anomalie -- voir ci-dessus.")


if __name__ == "__main__":
    main()
