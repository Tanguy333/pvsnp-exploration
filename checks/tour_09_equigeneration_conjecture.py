"""
Tour 09 -- Test empirique de la conjecture C9 (Proposeur) avant soumission.

CONJECTURE C9 :
  Pour f monotone non-constante, I_f a une resolution libre minimale PURE
  (au sens Boij-Soderberg, i.e. un seul shift par index homologique) si et
  seulement si tous les implicants premiers de f ont la MEME taille (i.e.
  I_f est equigenerated comme ideal monomial squarefree).

Application de la condition (j) : verification empirique a n=4 AVANT
soumission. Si la conjecture echoue ici, elle est retiree ; sinon, elle
est proposee avec les chiffres exacts.

Reutilise les routines Hochster du Tour 7 et l'enumeration du Tour 6/8.
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from tour_07_resolutions_libres import (
    hochster_bettis_RI,
    betti_I_from_RI,
)
from tour_08_atlas_boij_soderberg import (
    all_monotone_functions,
    prime_implicants,
    is_pure_resolution,
    betti_table_I,
)


def is_equigenerated(prime_imps: list[frozenset[int]]) -> bool:
    """ I_f equigenerated ssi tous les implicants premiers ont la meme taille. """
    if not prime_imps:
        return True  # ideal unite, trivialement
    sizes = {len(p) for p in prime_imps}
    return len(sizes) == 1


def main() -> None:
    n = 4
    print("Tour 09 -- Test empirique de la conjecture C9 sur n=4")
    print("=" * 78)
    print()
    print("  C9 : I_f pure (Boij-Soderberg) <=> implicants premiers de meme taille.")
    print()

    monotone = all_monotone_functions(n)
    print(f"  Fonctions monotones sur n=4 : {len(monotone)}")

    # Tableau de contingence : (pure?, equi?) -> count
    table = {
        (True, True): 0,
        (True, False): 0,
        (False, True): 0,
        (False, False): 0,
    }
    counter_examples_pure_not_equi: list[tuple[int, list[frozenset[int]]]] = []
    counter_examples_equi_not_pure: list[tuple[int, list[frozenset[int]]]] = []

    n_analyzed = 0
    for mask in monotone:
        pi = prime_implicants(mask, n)
        if not pi:
            # constante 0 : exclue de la conjecture (I_f = R)
            continue
        n_analyzed += 1
        bt = betti_table_I(pi, n)
        pure = is_pure_resolution(bt)
        equi = is_equigenerated(pi)
        table[(pure, equi)] += 1
        if pure and not equi:
            counter_examples_pure_not_equi.append((mask, pi))
        if equi and not pure:
            counter_examples_equi_not_pure.append((mask, pi))

    print(f"  Fonctions non-constantes analysees : {n_analyzed}")
    print()
    print("  Tableau de contingence (pure x equigenerated) :")
    print(f"  {'':>20} | {'equi=True':>11} | {'equi=False':>11}")
    print(f"  {'-'*20} | {'-'*11} | {'-'*11}")
    print(f"  {'pure=True':>20} | {table[(True, True)]:>11} | {table[(True, False)]:>11}")
    print(f"  {'pure=False':>20} | {table[(False, True)]:>11} | {table[(False, False)]:>11}")
    print()

    print(f"  Direction L9.1 (pure => equi) : {len(counter_examples_pure_not_equi)} contre-exemples.")
    print(f"  Direction L9.2 (equi => pure) : {len(counter_examples_equi_not_pure)} contre-exemples.")
    print()

    if counter_examples_pure_not_equi:
        print("  EXCEPTIONS pure-mais-non-equi (refute L9.1) :")
        for mask, pi in counter_examples_pure_not_equi[:5]:
            imps_str = ", ".join("{" + ",".join(map(str, sorted(p))) + "}" for p in pi)
            sizes = sorted(set(len(p) for p in pi))
            print(f"    mintermes={imps_str}  tailles={sizes}")

    if counter_examples_equi_not_pure:
        print("  EXCEPTIONS equi-mais-non-pure (refute L9.2) :")
        for mask, pi in counter_examples_equi_not_pure[:10]:
            imps_str = ", ".join("{" + ",".join(map(str, sorted(p))) + "}" for p in pi)
            sz = len(next(iter(pi)))
            print(f"    mintermes={imps_str}  taille uniforme={sz}")

    print()
    print("=" * 78)
    if not counter_examples_pure_not_equi and not counter_examples_equi_not_pure:
        print("VERDICT n=4 : CONJECTURE CONFIRMEE")
        print("  Les deux directions tiennent sur les 167 fonctions non-constantes.")
        print("  -> proposition C9 conforme a la condition (j), soumissible.")
    elif not counter_examples_pure_not_equi:
        print("VERDICT n=4 : L9.1 OK, L9.2 REFUTEE")
        print("  pure => equi tient ; mais equi =/=> pure (au moins un contre-exemple).")
        print("  -> Conjecture a affaiblir en implication unidirectionnelle.")
    elif not counter_examples_equi_not_pure:
        print("VERDICT n=4 : L9.2 OK, L9.1 REFUTEE")
        print("  equi => pure tient ; mais pure =/=> equi (au moins un contre-exemple).")
        print("  -> Conjecture a affaiblir en implication unidirectionnelle.")
    else:
        print("VERDICT n=4 : LES DEUX DIRECTIONS REFUTEES")
        print("  La conjecture C9 ne tient pas.")
        print("  -> Proposition retiree, alternative a trouver.")


if __name__ == "__main__":
    main()
