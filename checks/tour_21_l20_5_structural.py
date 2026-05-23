"""
Tour 21 -- Preuve structurelle de L20.5 par cas sur |f^{-1}(0)|.

CONJECTURE L20.5 :
  Pour n >= 3, les SEULES fonctions a defaut maximal n(n-2) sont les
  fonctions antipodales (|f^{-1}(0)| = 2 avec les 2 affectations
  complementaires).

STRATEGIE DE PREUVE :
  Decomposer par cas selon k = |f^{-1}(0)|, et montrer que defaut(f) < n(n-2)
  sauf si f est antipodale.

  Cas 1 : k = 0 (f = constante 1). #primes = 1, DNF_min = 1, defaut = 0.
  Cas 2 : k = 2^n (f = constante 0). Exclu (constante).
  Cas 3 : k = 1 (f = 1 sauf en un point). Defaut ?
  Cas 4 : k = 2 antipodal. Defaut = n(n-2) (Tour 20).
  Cas 5 : k = 2 non-antipodal. Defaut ?
  Cas 6 : k >= 3. Defaut ?

OBJECTIF DU SCRIPT :
  Verifier empiriquement les cas 3, 5, 6 sur n=4 pour identifier le defaut
  maximal dans chacun.

LIEN A P vs NP : preuve structurelle = transformation d'un objet ETABLI
empiriquement (Tour 20) en objet ETABLI structurellement, comme Tour 18 l'a
fait pour Tour 17.
"""

from __future__ import annotations

import itertools
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from tour_19_primes_eq_dnfmin import (
    all_ands, and_size, and_satisfies, and_implies_f,
    is_strictly_more_constrained, compute_primes_and_dnfmin,
)


def hamming_distance(x: int, y: int) -> int:
    return bin(x ^ y).count('1')


def f_zero_set(mask: int, n: int) -> list[int]:
    """ Affectations a f=0. """
    return [x for x in range(1 << n) if not ((mask >> x) & 1)]


def is_antipodal(zero_set: list[int], n: int) -> bool:
    """ Verifie que zero_set = {alpha, ~alpha} pour un alpha. """
    if len(zero_set) != 2:
        return False
    a, b = zero_set
    return hamming_distance(a, b) == n


def analyze_by_zero_set_size(n: int):
    """ Pour chaque taille k de f^{-1}(0), calculer le defaut max. """
    print(f"### Analyse par taille |f^{{-1}}(0)| sur n={n} ###")
    print()

    ands_cache = list(all_ands(n))
    num_fns = 1 << (1 << n)

    by_k: dict[int, list[tuple[int, int]]] = {}  # k -> list of (mask, defaut)

    t0 = time.time()
    for mask in range(num_fns):
        if mask == 0 or mask == num_fns - 1:
            continue
        n_zeros = bin(((1 << (1 << n)) - 1) ^ mask).count('1')
        primes_count, dnf_min = compute_primes_and_dnfmin(mask, n, ands_cache)
        defaut = primes_count - dnf_min
        by_k.setdefault(n_zeros, []).append((mask, defaut))
    elapsed = time.time() - t0

    print(f"  Total {num_fns - 2} fonctions non-constantes traitees en {elapsed:.1f}s")
    print()
    print(f"  {'k = |f^-1(0)|':>15} | {'#fonctions':>10} | {'defaut max':>10} | {'attendu':>8} | {'note'}")
    print(f"  {'-'*15} | {'-'*10} | {'-'*10} | {'-'*8} | {'-'*40}")

    expected_max = n * (n - 2)
    for k in sorted(by_k.keys()):
        funcs = by_k[k]
        n_fns = len(funcs)
        max_defaut = max(d for _, d in funcs)
        note = ""
        if k == 2:
            # Examiner les fonctions a defaut max et verifier antipodalite.
            antipodal_count = sum(
                1 for mask, d in funcs
                if d == max_defaut and is_antipodal(f_zero_set(mask, n), n)
            )
            total_at_max = sum(1 for _, d in funcs if d == max_defaut)
            note = f"{antipodal_count}/{total_at_max} antipodales au max"
        if max_defaut == expected_max:
            note += " *** ATTEINT n(n-2)"
        print(f"  {k:>15} | {n_fns:>10} | {max_defaut:>10} | {expected_max:>8} | {note}")
    print()

    return by_k


def main() -> None:
    print("Tour 21 -- Preuve structurelle de L20.5 par cas sur |f^{-1}(0)|")
    print("=" * 78)
    print()

    n = 4
    by_k = analyze_by_zero_set_size(n)

    print("=" * 78)
    print(f"OBSERVATIONS POUR LA PREUVE STRUCTURELLE :")
    print()
    print(f"  Le defaut maximal n(n-2) = {n * (n-2)} est-il atteint seulement par k=2 ?")
    print()
    print(f"  Si oui : L20.5 est confirmee a n={n}.")
    print(f"  Si non : il existe d'autres fonctions a defaut max (a investiguer).")

    # Verification finale L20.5 a n=4.
    max_defaut = max(d for funcs in by_k.values() for _, d in funcs)
    print()
    print(f"  Defaut maximal observe a n={n} : {max_defaut} = {n*(n-2) if max_defaut == n*(n-2) else 'autre'}")

    # Fonctions a defaut max.
    extreme_fns = [(mask, k, d) for k, funcs in by_k.items() for mask, d in funcs if d == max_defaut]
    print(f"  #fonctions a defaut max : {len(extreme_fns)}")
    print(f"  Tailles k = |f^-1(0)| de ces fonctions : {sorted(set(k for _, k, _ in extreme_fns))}")

    # Vérifier antipodalité.
    antipodal_fns = [mask for mask, k, d in extreme_fns
                     if k == 2 and is_antipodal(f_zero_set(mask, n), n)]
    print(f"  #fonctions antipodales (k=2) a defaut max : {len(antipodal_fns)}")
    non_antipodal_fns = [mask for mask, k, d in extreme_fns if mask not in antipodal_fns]
    if non_antipodal_fns:
        print(f"  CONTRE-EXEMPLES (fonctions non-antipodales a defaut max) : {len(non_antipodal_fns)}")
        for mask in non_antipodal_fns[:3]:
            zero = f_zero_set(mask, n)
            print(f"    mask=0x{mask:04x}, f^-1(0)={[format(x, f'0{n}b') for x in zero]}")
    else:
        print(f"  ✓ AUCUN contre-exemple : seules les antipodales atteignent le defaut max.")
        print(f"    L20.5 confirmee empiriquement a n={n}.")


if __name__ == "__main__":
    main()
