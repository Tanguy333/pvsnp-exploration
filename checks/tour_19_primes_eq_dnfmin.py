"""
Tour 19 -- Caracterisation des fonctions verifiant DNF_min(f) = |primes(f)|.

Observation accumulee Tours 12-18 : pour PARITY, MAJ, THRESHOLD_t, MOD_p, IP,
on a TOUJOURS DNF_min(f) = |primes(f)| (chaque implicant premier est requis).

Question : est-ce general ? Si non, quelle est la structure exacte ?

THEOREMES CLASSIQUES :
  - Quine 1952 : DNF_min(f) = taille minimum d'un set cover des affectations
    f^{-1}(1) par les implicants premiers.
  - DNF_min(f) ≤ |primes(f)| toujours.
  - L'inégalite stricte DNF_min(f) < |primes(f)| correspond a une redondance
    de couverture (un implicant peut etre "absorbe" par d'autres).

OBJECTIF TOUR 19 :
  Enumerer toutes les fonctions booleennes sur n=3 (256) et n=4 (65536),
  calculer #primes et DNF_min, et identifier la classe des fonctions a
  egalite.

CONDITIONS (a)-(n) : toutes a verifier. (n) honoree car ce n'est PAS une
application de L13 (qui caracterise une sous-classe ; on cherche ici une
classe potentiellement plus grande).
"""

from __future__ import annotations

import itertools
import math
import time
from collections import Counter


def all_ands(n: int):
    for signs in itertools.product([0, 1, -1], repeat=n):
        yield signs


def and_size(signs: tuple[int, ...]) -> int:
    return sum(1 for s in signs if s != 0)


def and_satisfies(signs: tuple[int, ...], x: int, n: int) -> bool:
    for i, s in enumerate(signs):
        bit = (x >> i) & 1
        if s == 1 and bit != 1:
            return False
        if s == -1 and bit != 0:
            return False
    return True


def and_implies_f(signs: tuple[int, ...], truth_mask: int, n: int) -> tuple[bool, bool]:
    """ Renvoie (has_sat, implies). has_sat : au moins une affectation satisfait ;
        implies : toutes les affectations satisfaisantes sont dans f^{-1}(1). """
    has_sat = False
    for x in range(1 << n):
        if and_satisfies(signs, x, n):
            has_sat = True
            if not ((truth_mask >> x) & 1):
                return (has_sat, False)
    return (has_sat, has_sat)


def is_strictly_more_constrained(small: tuple[int, ...], big: tuple[int, ...]) -> bool:
    for i in range(len(small)):
        if big[i] != 0:
            if small[i] != big[i]:
                return False
    if and_size(small) <= and_size(big):
        return False
    return True


def compute_primes_and_dnfmin(truth_mask: int, n: int, ands_cache: list) -> tuple[int, int]:
    """ Renvoie (#primes, DNF_min). Pour truth_mask=0 (fonction triviale 0)
        renvoie (0, 0). Pour truth_mask = 2^(2^n)-1 (constante 1) renvoie (1, 1)
        (le AND vide). """
    # Cas particulier : f constante 1.
    if truth_mask == (1 << (1 << n)) - 1:
        return (1, 1)
    # Cas particulier : f constante 0.
    if truth_mask == 0:
        return (0, 0)

    # Identifier les implicants.
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

    # DNF_min via set cover (par enumeration de taille croissante).
    truth_set = [x for x in range(1 << n) if (truth_mask >> x) & 1]
    coverage = []
    for a in primes:
        cov = frozenset(x for x in truth_set if and_satisfies(a, x, n))
        coverage.append(cov)

    target = frozenset(truth_set)
    dnf_min = len(primes)  # borne sup triviale
    # Recherche set cover de taille croissante.
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

    return (len(primes), dnf_min)


def main() -> None:
    print("Tour 19 -- Caracterisation de DNF_min(f) = |primes(f)| sur n=3, n=4")
    print("=" * 78)
    print()

    for n in [3, 4]:
        print(f"### Cas n = {n} ###")
        ands_cache = list(all_ands(n))
        num_fns = 1 << (1 << n)
        if n == 4:
            print(f"  Enumeration de {num_fns} fonctions sur n={n}...")
        t0 = time.time()

        # Statistiques.
        equal_count = 0
        strict_count = 0
        strict_examples = []  # liste de (truth_mask, #primes, dnf_min)
        diff_distribution = Counter()  # (#primes - dnf_min) -> count

        for mask in range(num_fns):
            if mask == 0 or mask == num_fns - 1:
                continue  # exclure les constantes
            primes_count, dnf_min = compute_primes_and_dnfmin(mask, n, ands_cache)
            if primes_count == dnf_min:
                equal_count += 1
            else:
                strict_count += 1
                if len(strict_examples) < 5:
                    strict_examples.append((mask, primes_count, dnf_min))
            diff_distribution[primes_count - dnf_min] += 1

        elapsed = time.time() - t0
        total = num_fns - 2  # exclure les 2 constantes
        print(f"  Fonctions non-constantes : {total}")
        print(f"  DNF_min = #primes : {equal_count} ({100*equal_count/total:.2f}%)")
        print(f"  DNF_min < #primes : {strict_count} ({100*strict_count/total:.2f}%)")
        print(f"  Distribution de #primes - DNF_min :")
        for diff in sorted(diff_distribution.keys()):
            print(f"    diff = {diff} : {diff_distribution[diff]} fonctions")
        print(f"  Temps : {elapsed:.1f}s")
        print()

        if strict_examples:
            print(f"  Exemples de fonctions avec DNF_min < #primes :")
            for mask, primes_count, dnf_min in strict_examples:
                # Afficher truth table.
                truth_str = ''.join('1' if (mask >> x) & 1 else '0' for x in range(1 << n))
                print(f"    mask=0b{mask:0{1 << n}b} truth=({truth_str}) #primes={primes_count} dnf_min={dnf_min}")
            print()

    print("=" * 78)
    print("Observations a synthetiser pour la proposition Tour 19...")


if __name__ == "__main__":
    main()
