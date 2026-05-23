"""
Tour 09 -- Extension de la conjecture C9 a n=5.

Le Proposeur a verifie C9 sur n=4 (167 fonctions non-constantes, tableau
95/0/0/72 parfaitement diagonal). Pour tester si la conjecture survit,
on l'etend a n=5 (7581 fonctions monotones).

DEFI : enumerer brute force les 2^32 = 4 milliards de masques de n=5 est
infaisable. On utilise la recursion de Dedekind :

    f monotone sur n vars
    <=> paire (f_0, f_1) de fonctions monotones sur n-1 vars avec f_0 <= f_1

    avec f(x_1, ..., x_n) = f_0(x_1, ..., x_{n-1}) si x_n = 0
                          = f_1(x_1, ..., x_{n-1}) si x_n = 1

Le mask f sur n vars = f_0 | (f_1 << 2^{n-1}).
On filtre les paires (f_0, f_1) par (f_0 & f_1) == f_0 (i.e. f_0 subseteq f_1).
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from tour_07_resolutions_libres import hochster_bettis_RI, betti_I_from_RI
from tour_09_equigeneration_conjecture import is_equigenerated

# is_pure_resolution et prime_implicants sont dans tour_08
from tour_08_atlas_boij_soderberg import is_pure_resolution, prime_implicants


# ---------------------------------------------------------------------------
# Generation efficace via Dedekind
# ---------------------------------------------------------------------------

def all_monotone_masks_dedekind(n: int, _cache: dict[int, list[int]] = {}) -> list[int]:
    """ Genere les masques bitfield des fonctions monotones sur n vars
        par recursion. Pour n=5, devrait renvoyer 7581 masques (Dedekind M(5)).
    """
    if n in _cache:
        return _cache[n]
    if n == 0:
        _cache[n] = [0, 1]
        return _cache[n]
    sub = all_monotone_masks_dedekind(n - 1)
    half_shift = 1 << (n - 1)
    result: list[int] = []
    for f0 in sub:
        for f1 in sub:
            if (f0 & f1) == f0:
                mask = f0 | (f1 << half_shift)
                result.append(mask)
    _cache[n] = result
    return result


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def main() -> None:
    n = 5
    print(f"Tour 09 -- Extension de C9 a n={n}")
    print("=" * 78)
    print()

    # Verification : n=4 doit donner 168
    print(f"  M(4) = {len(all_monotone_masks_dedekind(4))} (attendu : 168)")
    print(f"  Generation des fonctions monotones sur n={n} par recursion...")
    t0 = time.time()
    monotone = all_monotone_masks_dedekind(n)
    elapsed = time.time() - t0
    print(f"  M({n}) = {len(monotone)} (attendu : 7581 pour n=5)")
    print(f"  ({elapsed:.2f}s)")
    print()

    # Test de la conjecture C9
    print(f"  Calcul de (pure, equigen) pour chacune des {len(monotone)} fonctions...")
    table = {(True, True): 0, (True, False): 0, (False, True): 0, (False, False): 0}
    counter_pure_not_equi: list[tuple[int, list[frozenset[int]]]] = []
    counter_equi_not_pure: list[tuple[int, list[frozenset[int]], dict]] = []

    t0 = time.time()
    n_analyzed = 0
    n_excluded = 0
    for idx, mask in enumerate(monotone):
        pi = prime_implicants(mask, n)
        if not pi or pi == [frozenset()]:
            n_excluded += 1
            continue
        n_analyzed += 1

        bettis_RI = hochster_bettis_RI(pi, n)
        bettis_I = betti_I_from_RI(bettis_RI)
        pure = is_pure_resolution(bettis_I)
        equi = is_equigenerated(pi)
        table[(pure, equi)] += 1

        if pure and not equi:
            counter_pure_not_equi.append((mask, pi))
        if equi and not pure:
            counter_equi_not_pure.append((mask, pi, bettis_I))

        if (idx + 1) % 500 == 0:
            elapsed = time.time() - t0
            rate = (idx + 1) / elapsed
            eta = (len(monotone) - idx - 1) / rate
            print(f"    {idx+1} / {len(monotone)} traitees "
                  f"({elapsed:.1f}s, {rate:.0f}/s, ETA {eta:.0f}s)")

    elapsed = time.time() - t0
    print(f"  {n_analyzed} fonctions non-constantes analysees, {n_excluded} exclues ({elapsed:.1f}s)")

    print()
    print(f"  Tableau de contingence (pure x equigenerated) sur n={n} :")
    print(f"  {'':>20} | {'equi=True':>11} | {'equi=False':>11}")
    print(f"  {'-'*20} | {'-'*11} | {'-'*11}")
    print(f"  {'pure=True':>20} | {table[(True, True)]:>11} | {table[(True, False)]:>11}")
    print(f"  {'pure=False':>20} | {table[(False, True)]:>11} | {table[(False, False)]:>11}")
    print()

    n_violations_L91 = len(counter_pure_not_equi)
    n_violations_L92 = len(counter_equi_not_pure)
    print(f"  Direction L9.1 (pure => equi) : {n_violations_L91} contre-exemples.")
    print(f"  Direction L9.2 (equi => pure) : {n_violations_L92} contre-exemples.")
    print()

    if counter_pure_not_equi:
        print(f"  EXCEPTIONS pure-mais-non-equi (refute L9.1, surprenant) :")
        for mask, pi in counter_pure_not_equi[:5]:
            imps_str = ", ".join("{" + ",".join(map(str, sorted(p))) + "}" for p in pi)
            sizes = sorted(set(len(p) for p in pi))
            print(f"    mintermes={imps_str}  tailles={sizes}")

    if counter_equi_not_pure:
        print(f"  EXCEPTIONS equi-mais-non-pure (refute L9.2, vraie question) :")
        for mask, pi, bt in counter_equi_not_pure[:5]:
            imps_str = ", ".join("{" + ",".join(map(str, sorted(p))) + "}" for p in pi)
            sz = len(next(iter(pi)))
            non_zero = {ij: v for ij, v in sorted(bt.items()) if v > 0}
            print(f"    mintermes={imps_str}")
            print(f"      taille uniforme={sz}, Betti(I) (non nuls) = {non_zero}")

    print()
    print("=" * 78)
    if n_violations_L91 == 0 and n_violations_L92 == 0:
        print(f"VERDICT n={n} : CONJECTURE CONFIRMEE")
        print(f"  La conjecture C9 tient sur les {n_analyzed} fonctions monotones non-constantes")
        print(f"  de n={n}. Combinee avec n=4, cela renforce considerablement la conjecture.")
    elif n_violations_L91 == 0 and n_violations_L92 > 0:
        print(f"VERDICT n={n} : L9.1 OK, L9.2 REFUTEE ({n_violations_L92} cas)")
        print(f"  pure => equi tient ; mais il existe des fonctions equigenerated dont")
        print(f"  la resolution n'est PAS pure. La conjecture C9 est refutee a n={n}.")
        print(f"  Contre-exemples concrets identifies ci-dessus.")
    elif n_violations_L91 > 0 and n_violations_L92 == 0:
        print(f"VERDICT n={n} : L9.2 OK, L9.1 REFUTEE ({n_violations_L91} cas) -- TRES surprenant")
        print(f"  Cela contredirait la preuve par contrapositive triviale.")
        print(f"  Probable bug du code -- a investiguer.")
    else:
        print(f"VERDICT n={n} : LES DEUX DIRECTIONS REFUTEES")
        print(f"  La conjecture C9 ne tient pas a n={n}.")


if __name__ == "__main__":
    main()
