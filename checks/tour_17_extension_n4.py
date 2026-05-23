"""
Tour 17 -- Extension du test de la conjecture (3^n - 1)/2 a n=4.

Le Proposeur a verifie DNF_min(IP_{2n}) = (3^n - 1)/2 a n=1, 2, 3
(valeurs 1, 4, 13). La conjecture predit a n=4 : (3^4 - 1)/2 = 40.

Le set cover exhaustif du script du Proposeur explose a n=4 (potentiellement
C(|primes|, 40) combinations). On utilise PuLP pour resoudre exactement
le set cover via ILP.

VARIABLES : x_i in {0, 1} pour chaque implicant premier i.
OBJECTIF : minimize sum(x_i).
CONTRAINTES : pour chaque affectation a in IP^{-1}(1),
              sum_{i : implicant_i covers a} x_i >= 1.

ILP exact via CBC (solveur par defaut de PuLP).
"""

from __future__ import annotations

import itertools
import sys
import time
from pathlib import Path

import pulp

sys.path.insert(0, str(Path(__file__).parent))
from tour_17_inner_product_dnf import (
    ip_value,
    all_ands,
    and_size,
    and_satisfies,
    and_implies_ip,
    is_strictly_more_constrained,
    and_to_string,
)


def compute_dnf_min_ip_ilp(n: int, verbose: bool = True) -> int:
    """ Renvoie DNF_min(IP_{2n}) en utilisant ILP exact pour le set cover. """
    num_vars = 2 * n
    truth_set = set()
    for x in itertools.product([0, 1], repeat=num_vars):
        if ip_value(x, n) == 1:
            truth_set.add(x)

    if verbose:
        print(f"  IP_{num_vars} sur {num_vars} variables")
        print(f"  |IP^{{-1}}(1)| = {len(truth_set)}")

    # Enumerer les implicants.
    t0 = time.time()
    ands = list(all_ands(num_vars))
    if verbose:
        print(f"  Total ANDs : {len(ands)} = 3^{num_vars}")
    implicants = [a for a in ands if and_implies_ip(a, n)]
    if verbose:
        print(f"  Implicants de IP_{num_vars} : {len(implicants)}  ({time.time()-t0:.1f}s)")

    # Identifier implicants premiers.
    t0 = time.time()
    primes = []
    for a in implicants:
        is_prime = True
        for b in implicants:
            if b != a and is_strictly_more_constrained(a, b):
                is_prime = False
                break
        if is_prime:
            primes.append(a)
    if verbose:
        print(f"  Implicants premiers : {len(primes)}  ({time.time()-t0:.1f}s)")
        sizes = {}
        for a in primes:
            s = and_size(a)
            sizes[s] = sizes.get(s, 0) + 1
        print(f"  Distribution par taille : {dict(sorted(sizes.items()))}")
        print()

    # Coverage matrix : pour chaque implicant premier i, quelles affectations couvre-t-il ?
    coverage = []
    for a in primes:
        covered = set()
        for x in truth_set:
            if and_satisfies(a, x):
                covered.add(x)
        coverage.append(covered)

    # ILP set cover.
    if verbose:
        print(f"  Resolution ILP set cover ({len(primes)} variables, {len(truth_set)} contraintes)...")
    t0 = time.time()

    prob = pulp.LpProblem("set_cover", pulp.LpMinimize)
    x_vars = [pulp.LpVariable(f"x{i}", cat="Binary") for i in range(len(primes))]
    prob += pulp.lpSum(x_vars)
    truth_list = list(truth_set)
    for a in truth_list:
        covering = [x_vars[i] for i in range(len(primes)) if a in coverage[i]]
        if not covering:
            if verbose:
                print(f"  ECHEC : affectation {a} non couverte par aucun implicant !")
            return -1
        prob += pulp.lpSum(covering) >= 1

    solver = pulp.PULP_CBC_CMD(msg=False, timeLimit=600)
    status = prob.solve(solver)
    dnf_min = int(pulp.value(prob.objective))

    if verbose:
        print(f"  ILP resolu en {time.time()-t0:.1f}s")
        print(f"  Statut : {pulp.LpStatus[status]}")
        print(f"  DNF_min(IP_{num_vars}) = {dnf_min}")
    return dnf_min


def main() -> None:
    print("Tour 17 -- Test de la conjecture (3^n - 1)/2 a n=4")
    print("=" * 78)
    print()

    # Vérification des cas connus n=2, 3 avec ILP (cross-check).
    print("### Cross-check avec ILP (n=2, 3) ###")
    print()
    for n in (2, 3):
        print(f"--- n={n} ---")
        v = compute_dnf_min_ip_ilp(n, verbose=True)
        expected = (3**n - 1) // 2
        print(f"  Conjecture (3^{n}-1)/2 = {expected}")
        match = "OK" if v == expected else "MISMATCH"
        print(f"  Verdict : {match}")
        print()

    # Test n=4 (cas decisif).
    print("=" * 78)
    print("### TEST DECISIF : n=4 ###")
    print()
    n = 4
    dnf_min_4 = compute_dnf_min_ip_ilp(n, verbose=True)
    expected_4 = (3**n - 1) // 2  # = 40
    print()
    print("=" * 78)
    print(f"VERDICT FINAL")
    print(f"  Conjecture predit : DNF_min(IP_8) = (3^4 - 1)/2 = {expected_4}")
    print(f"  Calcul exact ILP   : DNF_min(IP_8) = {dnf_min_4}")
    if dnf_min_4 == expected_4:
        print(f"  -> CONJECTURE CONFIRMEE a n=4. Tour 17 ETABLI a n=1,2,3,4.")
    else:
        print(f"  -> CONJECTURE REFUTEE a n=4. ECART = {dnf_min_4 - expected_4}.")


if __name__ == "__main__":
    main()
