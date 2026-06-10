"""
TACHE V-013 -- Cloture totale de la Conjecture 5 de KV pour d <= 5.

STRUCTURE DU THEOREME V13 :
  Pour chaque d <= 5, la droite des n se partage en :
  - regime stable n >= n*(d) : par le Theoreme V11, il suffit d'un temoin
    plat (PTE ideale de taille d+1) de degre n*(d), DECALE par x^{n-n*} :
    plus court vecteur a derniere coordonnee +-1 -> Conjecture 5 ;
  - zone sous-transition n < n*(d) : FINIE -- verification exhaustive
    par plus courts vecteurs exacts (LLL + Fincke-Pohst, V-004/005 pour
    6 <= n <= 20 ; les cellules restantes sont traitees ICI).

Ce script :
 [1] verifie les cellules sous-transition jamais couvertes :
     (d=1, n=2..5), (d=2, n=3..5), (d=3, n=4..5), (d=4, n=5),
     (d=5, n=21..22) -- bouts +-1 pour au moins un minimum (et rapport
     de la version forte) ;
 [2] fait decouvrir au RESEAU les temoins PTE ideaux de tailles 5 et 6 :
     cellules (18, 4) et (23, 5) -- on verifie min = 2(d+1), on extrait
     un minimum plat, on verifie en exact son +-split (sommes de
     puissances 1..d egales) et ses bouts +-1. Aucune dependance aux
     tables de la litterature.
 [3] verdict : Theoreme V13 -- la Conjecture 5 vaut pour TOUT d <= 5 et
     TOUT n (>= d+1).
"""

from __future__ import annotations

import time

from task_v004_kv_conjecture5 import build_basis, lll_reduce, shortest_vectors

TRANSITIONS = {1: 6, 2: 6, 3: 11, 4: 18, 5: 23}


def ends_unit(v):
    nz = [int(x) for x in v if int(x) != 0]
    return abs(nz[0]) == 1 and abs(nz[-1]) == 1


def first_unit_all(sols):
    return all(abs(next(int(x) for x in v if int(x))) == 1 for v in sols)


def main() -> None:
    print("TACHE V-013 -- cloture de la Conjecture 5 pour d <= 5, tout n")
    print("=" * 68)

    print("\n[1] Cellules sous-transition restantes :")
    cells = ([(1, n) for n in range(2, 6)] + [(2, n) for n in range(3, 6)]
             + [(3, n) for n in range(4, 6)] + [(4, 5)]
             + [(5, n) for n in (21, 22)])
    ok1 = True
    for (d, n) in cells:
        if n < d + 1:
            continue
        t0 = time.time()
        G = lll_reduce(build_basis(n, d))
        n2, sols = shortest_vectors(G)
        exists = any(ends_unit(v) for v in sols)
        strong = first_unit_all(sols)
        ok1 &= exists
        print(f"    (d={d}, n={n:>2}) : norme2={n2:>3}, {len(sols):>3} minima, "
              f"bouts +-1 : {'OUI' if exists else '*** NON ***'} "
              f"(forte : {'oui' if strong else 'non'})   "
              f"({time.time()-t0:.0f}s)", flush=True)

    print("\n[2] Temoins PTE ideaux decouverts par le reseau :")
    ok2 = True
    for (d, n_star) in ((4, 18), (5, 23)):
        t0 = time.time()
        G = lll_reduce(build_basis(n_star, d))
        n2, sols = shortest_vectors(G)
        target = 2 * (d + 1)
        flat_w = None
        for v in sols:
            coefs = [int(x) for x in v]
            if all(abs(c) <= 1 for c in coefs) and ends_unit(v):
                A = [a for a, c in enumerate(coefs) if c > 0]
                B = [a for a, c in enumerate(coefs) if c < 0]
                if (len(A) == len(B) == d + 1 and
                        all(sum(a ** j for a in A) == sum(b ** j for b in B)
                            for j in range(1, d + 1))):
                    flat_w = (A, B)
                    break
        good = (n2 == target and flat_w is not None)
        ok2 &= good
        if good:
            A, B = flat_w
            print(f"    (d={d}, n*={n_star}) : min = {n2} = 2(d+1) ; temoin "
                  f"plat PTE ideal taille {d+1} :")
            print(f"        A = {A}")
            print(f"        B = {B}")
            print(f"        sommes de puissances 1..{d} egales : verifie "
                  f"exactement   ({time.time()-t0:.0f}s)", flush=True)
        else:
            print(f"    (d={d}, n*={n_star}) : min = {n2} (attendu {target}) "
                  f"-- *** PROBLEME ***   ({time.time()-t0:.0f}s)", flush=True)

    print("\n" + "=" * 68)
    if ok1 and ok2:
        print("THEOREME V13 : la Conjecture 5 de KV est VRAIE pour tout")
        print("d <= 5 et tout n >= d+1 --")
        print("  * n >= n*(d) : Theoreme V11 + temoin PTE ideal (extrait du")
        print("    reseau, verifie en exact) decale par x^{n - n*} ;")
        print("  * n < n*(d) : verification exhaustive (V-004/005 pour")
        print("    6 <= n <= 20, cellules restantes ci-dessus).")
        print("Transitions utilisees : n* = 6, 6, 11, 18, 23 (d = 1..5).")
    else:
        print("Pieces manquantes -- voir ci-dessus.")


if __name__ == "__main__":
    main()
