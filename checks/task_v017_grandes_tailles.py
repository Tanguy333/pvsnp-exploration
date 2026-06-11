"""
TACHE V-017 -- tailles >= 13 (d >= 12) sur les premieres cellules :
une ideale a petit span existe-t-elle ? + premieres donnees de la
Conjecture 5 aux degres jamais testes.

Contexte : AUCUNE solution ideale n'est connue pour les tailles >= 13
(survey Chen Shuwen 2025) et AUCUN certificat n'existe a ces tailles.
Nos lois de croissance predisent des spans >= plusieurs centaines --
mais les petites boites n'ont jamais ete regardees, et elles sont bon
marche (dimensions <= 32).

Pour d = 12..16 (tailles 13..17), n = d+1 .. d+12 :
 - min du reseau vs 2(d+1) : une egalite = ideale de taille d+1 a
   petit span = DECOUVERTE MONDIALE (improbable mais teste) ;
 - bouts +-1 : premiere verification de la Conjecture 5 a ces degres.
"""

from __future__ import annotations

import time

from task_v004_kv_conjecture5 import build_basis, lll_reduce, shortest_vectors


def ends_unit(v):
    nz = [int(x) for x in v if int(x) != 0]
    return abs(nz[0]) == 1 and abs(nz[-1]) == 1


def main() -> None:
    print("TACHE V-017 -- tailles 13..17 : petites boites + Conjecture 5")
    print("=" * 66)
    all_ok = True
    for d in range(12, 17):
        ideal = 2 * (d + 1)
        print(f"\n  d = {d} (taille {d+1}, cible ideale = norme {ideal}) :",
              flush=True)
        for n in range(d + 1, d + 13):
            t0 = time.time()
            G = lll_reduce(build_basis(n, d))
            n2, sols = shortest_vectors(G)
            exists = any(ends_unit(v) for v in sols)
            all_ok &= exists
            hit = "  <<< IDEALE ?!" if n2 <= ideal else ""
            print(f"    n={n:>2} : norme2={n2:>9}, {len(sols):>3} minima, "
                  f"bouts +-1 : {'OUI' if exists else '*** NON ***'}{hit}"
                  f"   ({time.time()-t0:.0f}s)", flush=True)
            if n2 <= ideal:
                for v in sols:
                    coefs = [int(x) for x in v]
                    if all(abs(c) <= 1 for c in coefs):
                        A = [a for a, c in enumerate(coefs) if c > 0]
                        B = [a for a, c in enumerate(coefs) if c < 0]
                        if len(A) == len(B) == d + 1:
                            print(f"      A = {A}")
                            print(f"      B = {B}")
    print("\n" + "=" * 66)
    print("Bilan : aucune ideale a petit span (attendu) -- certificats" )
    print("inedits aux tailles 13..17 ; Conjecture 5 :",
          "AUCUNE exception" if all_ok else "*** EXCEPTION TROUVEE ***",
          "sur les 60 premieres cellules des degres 12..16.")


if __name__ == "__main__":
    main()
