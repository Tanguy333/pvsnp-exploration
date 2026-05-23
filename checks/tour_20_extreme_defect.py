"""
Tour 20 -- Caracterisation des fonctions extremes HORS (α)/(β) : defaut maximal.

OBSERVATION Tour 19 : sur n=4, distribution du defaut `|primes| − DNF_min` :
  - 23862 fonctions a defaut 0 (classe α/β).
  - 23408 fonctions a defaut 1.
  - 9856 fonctions a defaut 2.
  - 6112 fonctions a defaut 3.
  - 1496 fonctions a defaut 4.
  - 760 fonctions a defaut 5.
  - 32 fonctions a defaut 6.
  - 8 fonctions a defaut 8.

Aucun cas a defaut 7. Les 8 cas a defaut 8 sont les fonctions les plus
extremes pour la minimisation DNF a n=4.

OBJECTIF : identifier ces 8 fonctions, leur structure combinatoire, et
formuler une caracterisation conjecturale.

Hypothese intuitive : les fonctions extremes correspondent a des structures
hautement symetriques avec recouvrement maximal par les implicants premiers.

LIEN A P vs NP (condition (k)) :
  DNF-MIN est Σ₂^P-difficile (Umans 1999). La classe (α)/(β) du Tour 19 est
  precisement celle ou l'algorithme glouton resout DNF-MIN en P. Les cas
  extremes (defaut maximal) sont les plus durs pour l'algorithme glouton,
  donc des candidats naturels pour des bornes inferieures sur des
  heuristiques de minimisation. Lien indirect a P vs NP via la frontiere
  P-facile/Σ₂^P-difficile.
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


def truth_to_minterms(mask: int, n: int) -> list[tuple[int, ...]]:
    """ Renvoie liste des affectations IP=1 comme tuples de bits. """
    return [tuple((x >> i) & 1 for i in range(n))
            for x in range(1 << n) if (mask >> x) & 1]


def and_to_string(signs: tuple[int, ...], n: int) -> str:
    if all(s == 0 for s in signs):
        return "1"
    parts = []
    for i, s in enumerate(signs):
        if s == 1:
            parts.append(f"x_{i}")
        elif s == -1:
            parts.append(f"~x_{i}")
    return " ∧ ".join(parts)


def compute_primes_and_min_cover(truth_mask: int, n: int, ands_cache: list):
    """ Renvoie (primes, min_cover) en plus de leurs comptes. """
    # Identifier implicants.
    implicants = []
    for a in ands_cache:
        has_sat, implies = and_implies_f(a, truth_mask, n)
        if has_sat and implies:
            implicants.append(a)

    # Implicants premiers.
    primes = []
    for a in implicants:
        is_prime = True
        for b in implicants:
            if b is not a and is_strictly_more_constrained(a, b):
                is_prime = False
                break
        if is_prime:
            primes.append(a)

    truth_set = [x for x in range(1 << n) if (truth_mask >> x) & 1]
    coverage = []
    for a in primes:
        cov = frozenset(x for x in truth_set if and_satisfies(a, x, n))
        coverage.append(cov)
    target = frozenset(truth_set)

    # Set cover minimal.
    for k in range(1, len(primes) + 1):
        for combo in itertools.combinations(range(len(primes)), k):
            total = set()
            for idx in combo:
                total |= coverage[idx]
            if total == target:
                return primes, [primes[i] for i in combo]
    return primes, primes


def main() -> None:
    n = 4
    print(f"Tour 20 -- Cas extremes (defaut maximal) HORS classe (α)/(β), n={n}")
    print("=" * 78)
    print()

    ands_cache = list(all_ands(n))
    num_fns = 1 << (1 << n)
    extreme_threshold = 8  # defaut maximal observe Tour 19

    print(f"  Recherche des fonctions a defaut exactement {extreme_threshold}...")
    extreme_fns = []
    t0 = time.time()
    for mask in range(num_fns):
        if mask == 0 or mask == num_fns - 1:
            continue
        primes_count, dnf_min = compute_primes_and_dnfmin(mask, n, ands_cache)
        if primes_count - dnf_min == extreme_threshold:
            extreme_fns.append(mask)
    elapsed = time.time() - t0
    print(f"  Trouvees {len(extreme_fns)} fonctions a defaut {extreme_threshold} en {elapsed:.1f}s")
    print()

    # Analyser chaque fonction extreme.
    print(f"  Analyse detaillee des {len(extreme_fns)} fonctions extremes :")
    print("-" * 78)
    for k, mask in enumerate(extreme_fns):
        print(f"\n  ### Fonction #{k+1} (mask = 0x{mask:04x}, soit 0b{mask:0{1<<n}b}) ###")
        minterms = truth_to_minterms(mask, n)
        print(f"    f^{{-1}}(1) = {len(minterms)} affectations :")
        for m in minterms:
            bin_str = ''.join(str(b) for b in m)
            print(f"      ({bin_str})")

        primes, min_cover = compute_primes_and_min_cover(mask, n, ands_cache)
        print(f"    #primes = {len(primes)}, DNF_min = {len(min_cover)}, defaut = {len(primes) - len(min_cover)}")
        print(f"    Implicants premiers :")
        for a in primes[:12]:
            print(f"      {and_to_string(a, n)}")
        if len(primes) > 12:
            print(f"      ... et {len(primes) - 12} autres")
        print(f"    Min cover :")
        for a in min_cover:
            print(f"      {and_to_string(a, n)}")

    # Structure combinatoire commune ?
    print()
    print("=" * 78)
    print(f"OBSERVATIONS STRUCTURELLES :")

    # Tailles |f^{-1}(1)| des fonctions extremes.
    sizes = [bin(mask).count('1') for mask in extreme_fns]
    print(f"  Tailles |f^{{-1}}(1)| : {sorted(sizes)}")

    # Compter #primes par fonction.
    n_primes_list = []
    for mask in extreme_fns:
        primes, _ = compute_primes_and_min_cover(mask, n, ands_cache)
        n_primes_list.append(len(primes))
    print(f"  #primes : {sorted(n_primes_list)}")

    # DNF_min.
    dnf_min_list = []
    for mask in extreme_fns:
        primes_count, dnf_min = compute_primes_and_dnfmin(mask, n, ands_cache)
        dnf_min_list.append(dnf_min)
    print(f"  DNF_min : {sorted(dnf_min_list)}")


if __name__ == "__main__":
    main()
