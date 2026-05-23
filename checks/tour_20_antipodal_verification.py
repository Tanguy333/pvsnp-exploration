"""
Tour 20 -- Verification de la conjecture L20 a n=5.

CONJECTURE L20 :
  Les fonctions extremes hors (α)/(β) sont les fonctions ANTIPODALES
  f_alpha(x) = 1 ssi x ∉ {α, ¬α}, pour α ∈ {0,1}^n.

  Pour ces fonctions, sur n >= 3 :
    - |f^{-1}(1)| = 2^n − 2
    - #primes = n(n−1)
    - DNF_min = n  (couverture cyclique des paires (i,j))
    - defaut = n(n−2)

  Verification empirique a n=3 (4 fct, defaut=3) et n=4 (8 fct, defaut=8) OK.
  Test n=5 : 16 fonctions antipodales, defaut attendu = 5·3 = 15.

CONDITIONS (j) : verification n=5 avant soumission.
"""

from __future__ import annotations

import itertools
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from tour_19_primes_eq_dnfmin import (
    all_ands, and_size, and_satisfies, and_implies_f,
    is_strictly_more_constrained,
)


def antipodal_mask(alpha: int, n: int) -> int:
    """ Renvoie le masque de f_alpha : f(x) = 1 sauf si x = alpha ou x = ¬alpha. """
    N = 1 << n
    not_alpha = ((1 << N) - 1) - 0  # tout
    # mask : bit x est 1 (f(x)=1) sauf si x = alpha ou x = (¬alpha) = (1<<n - 1) ^ alpha
    full = (1 << N) - 1
    return full ^ (1 << alpha) ^ (1 << ((N - 1) ^ alpha))


def compute_extreme_stats(mask: int, n: int, ands_cache: list, fast_set_cover: bool = False) -> tuple[int, int, int]:
    """ Renvoie (|f^{-1}(1)|, #primes, DNF_min). """
    truth_set = [x for x in range(1 << n) if (mask >> x) & 1]
    truth_count = len(truth_set)

    # Implicants.
    implicants = []
    for a in ands_cache:
        has_sat, implies = and_implies_f(a, mask, n)
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

    if not primes:
        return (truth_count, 0, 0)

    # Pour les fonctions antipodales avec n grand, le set cover par enumeration
    # combinatoire devient cher. Utiliser un set cover greedy comme borne sup,
    # puis valider via greedy + ILP si dispo.
    coverage = []
    for a in primes:
        cov = frozenset(x for x in truth_set if and_satisfies(a, x, n))
        coverage.append(cov)

    target = frozenset(truth_set)

    if fast_set_cover or len(primes) > 20:
        # Greedy : pas necessairement optimal mais borne sup.
        # Pour la conjecture, on a besoin de la valeur exacte. Essayons exact
        # avec depth-first branch and bound.
        best = [len(primes)]
        def search(remaining: set, idx: int, used: int):
            if not remaining:
                if used < best[0]:
                    best[0] = used
                return
            if used + 1 >= best[0]:
                return
            for i in range(idx, len(primes)):
                if coverage[i] & remaining:
                    search(remaining - coverage[i], i + 1, used + 1)
        search(set(truth_set), 0, 0)
        dnf_min = best[0]
    else:
        # Enumeration directe par taille croissante.
        dnf_min = len(primes)
        for k in range(1, len(primes) + 1):
            found = False
            for combo in itertools.combinations(range(len(primes)), k):
                total = set()
                for idx in combo:
                    total |= coverage[idx]
                if total == target:
                    dnf_min = k
                    found = True
                    break
            if found:
                break

    return (truth_count, len(primes), dnf_min)


def main() -> None:
    print("Tour 20 -- Verification empirique conjecture L20 sur fonctions antipodales")
    print("=" * 78)
    print()

    for n in [3, 4, 5]:
        print(f"### n = {n} ###")
        print(f"  Nombre attendu de fonctions antipodales : 2^(n-1) = {2**(n-1)}")
        print(f"  Defaut attendu n(n-2) = {n*(n-2)}")
        print()

        ands_cache = list(all_ands(n))

        # Energer les 2^(n-1) fonctions antipodales (alpha < ¬alpha).
        N = 1 << n
        antipodal_alphas = [a for a in range(N) if a < (N - 1) ^ a]
        # Plus simplement : alpha ∈ {0, ..., N/2 - 1} (le plus petit de chaque paire).
        antipodal_alphas = [a for a in range(N // 2)]

        print(f"  Fonctions antipodales (alpha, ¬alpha) :")
        print(f"  {'alpha':>6} | {'|f^-1(1)|':>10} | {'#primes':>8} | {'DNF_min':>8} | {'defaut':>6} | {'conforme':>8}")
        print(f"  {'-'*6} | {'-'*10} | {'-'*8} | {'-'*8} | {'-'*6} | {'-'*8}")
        all_conform = True
        t0 = time.time()
        for alpha in antipodal_alphas:
            mask = antipodal_mask(alpha, n)
            truth_count, n_primes, dnf_min = compute_extreme_stats(mask, n, ands_cache, fast_set_cover=(n >= 5))
            defaut = n_primes - dnf_min
            expected_defaut = n * (n - 2)
            expected_primes = n * (n - 1)
            expected_dnf = n
            conform = (n_primes == expected_primes) and (dnf_min == expected_dnf) and (defaut == expected_defaut)
            mark = "✓" if conform else "✗"
            all_conform = all_conform and conform
            alpha_bits = format(alpha, f'0{n}b')
            print(f"  {alpha_bits:>6} | {truth_count:>10} | {n_primes:>8} | {dnf_min:>8} | {defaut:>6} | {mark:>8}")
        elapsed = time.time() - t0
        print(f"  Temps : {elapsed:.1f}s")
        print(f"  Toutes conformes : {all_conform}")
        print()

    print("=" * 78)
    print("OBSERVATIONS :")
    print("  Si la conjecture L20 est verifiee pour n=3, 4, 5, alors :")
    print("    - Fonctions antipodales sont les cas extremes universellement.")
    print("    - Formule defaut = n(n-2) generalisable.")
    print("  A demontrer structurellement pour tout n.")


if __name__ == "__main__":
    main()
