"""
Tour 22 -- Verification independante du contre-exemple a L20.5 a n=5.

Le Proposeur a livre Z = {00000, 00011, 00101, 11001, 11110}
(= {0, 3, 5, 25, 30} en decimal) comme contre-exemple :
  |primes(f)| = 25, DNF_min(f) = 8, defaut = 17 > n(n-2) = 15.

Verification croisee independante par le Refuteur, utilisant la meme
methode Hochster+ILP que tour_17_extension_n4.py (donc completement
distincte de la methode du Proposeur).

Algorithme :
  1. Z = {0, 3, 5, 25, 30}, n = 5, donc 2n_size = 32 affectations.
  2. f(x) = 1 ssi x not in Z.
  3. Enumerer les 3^5 = 243 ANDs sur 5 variables.
  4. Identifier les implicants de f.
  5. Filtrer les implicants premiers.
  6. Set cover via PuLP (CBC) pour calculer DNF_min exact.

Si le triplet (|primes|, DNF_min, defaut) = (25, 8, 17), le contre-exemple
est CONFIRME. Sinon, le Proposeur a fait une erreur.
"""

from __future__ import annotations

import itertools

import pulp


def f(x_int: int, Z: set[int]) -> int:
    """ f(x) = 1 ssi x not in Z. """
    return 0 if x_int in Z else 1


def all_ands(n: int):
    """ Tous les 3^n ANDs : pour chaque variable, absent (0), positif (1), negatif (-1). """
    for signs in itertools.product([0, 1, -1], repeat=n):
        yield signs


def and_size(signs: tuple[int, ...]) -> int:
    return sum(1 for s in signs if s != 0)


def and_satisfies(signs: tuple[int, ...], x_int: int) -> bool:
    """ Le AND est-il satisfait par l'affectation x_int (codee comme entier) ? """
    for i, s in enumerate(signs):
        bit = (x_int >> i) & 1
        if s == 1 and bit != 1:
            return False
        if s == -1 and bit != 0:
            return False
    return True


def and_implies_f(signs: tuple[int, ...], n: int, Z: set[int]) -> bool:
    """ Tous les x satisfaisant le AND sont dans f^{-1}(1) = complementaire de Z. """
    has_sat = False
    for x in range(1 << n):
        if and_satisfies(signs, x):
            has_sat = True
            if f(x, Z) != 1:
                return False
    return has_sat


def is_strictly_more_constrained(small: tuple[int, ...], big: tuple[int, ...]) -> bool:
    """ small a tous les litteraux de big plus au moins un autre. """
    for i in range(len(small)):
        if big[i] != 0 and small[i] != big[i]:
            return False
    if and_size(small) <= and_size(big):
        return False
    return True


def and_to_string(signs: tuple[int, ...]) -> str:
    if all(s == 0 for s in signs):
        return "1"
    parts = []
    for i, s in enumerate(signs):
        if s == 1:
            parts.append(f"x_{i}")
        elif s == -1:
            parts.append(f"~x_{i}")
    return " AND ".join(parts)


def compute_primes_and_dnf_min(Z: set[int], n: int):
    """ Calcule |primes(f)|, DNF_min(f), defaut. """
    print(f"  n = {n}, |Z| = {len(Z)}, Z = {sorted(Z)} (bin : {[bin(z)[2:].zfill(n) for z in sorted(Z)]})")

    # Verification : f est non-constante
    f_one_count = sum(1 for x in range(1 << n) if f(x, Z) == 1)
    print(f"  |f^{{-1}}(1)| = {f_one_count} (attendu : 2^{n} - {len(Z)} = {(1 << n) - len(Z)})")

    # Identifier les implicants.
    ands = list(all_ands(n))
    implicants = [a for a in ands if and_implies_f(a, n, Z)]
    print(f"  Implicants (incl. non-premiers) : {len(implicants)}")

    # Filtrer les implicants premiers.
    primes = []
    for a in implicants:
        is_prime = True
        for b in implicants:
            if b != a and is_strictly_more_constrained(a, b):
                is_prime = False
                break
        if is_prime:
            primes.append(a)
    print(f"  Implicants premiers : {len(primes)}")

    # Distribution par taille.
    sizes = {}
    for a in primes:
        s = and_size(a)
        sizes[s] = sizes.get(s, 0) + 1
    print(f"  Distribution tailles : {dict(sorted(sizes.items()))}")

    # Set cover via ILP.
    truth_set = {x for x in range(1 << n) if f(x, Z) == 1}
    coverage = []
    for a in primes:
        covered = {x for x in truth_set if and_satisfies(a, x)}
        coverage.append((a, covered))

    prob = pulp.LpProblem("dnf_min", pulp.LpMinimize)
    x_vars = [pulp.LpVariable(f"x{i}", cat="Binary") for i in range(len(primes))]
    prob += pulp.lpSum(x_vars)
    for a in truth_set:
        covering = [x_vars[i] for i in range(len(primes)) if a in coverage[i][1]]
        if not covering:
            print(f"  ECHEC : affectation {a} non couverte !")
            return -1, -1, -1
        prob += pulp.lpSum(covering) >= 1

    solver = pulp.PULP_CBC_CMD(msg=False, timeLimit=300)
    status = prob.solve(solver)
    dnf_min = int(pulp.value(prob.objective))
    print(f"  DNF_min (par ILP CBC) : {dnf_min} (statut : {pulp.LpStatus[status]})")

    defect = len(primes) - dnf_min
    print(f"  Defaut = |primes| - DNF_min = {len(primes)} - {dnf_min} = {defect}")

    return len(primes), dnf_min, defect


def main() -> None:
    print("Tour 22 -- Verification independante du contre-exemple a L20.5 / L21.D")
    print("=" * 78)
    print()

    # Z = {0, 3, 5, 25, 30} sur n = 5.
    Z = {0, 3, 5, 25, 30}
    n = 5
    print("Test 1 : temoin canonique du Proposeur")
    print("-" * 78)
    pcount, dmin, defect = compute_primes_and_dnf_min(Z, n)

    print()
    print("=" * 78)
    print("VERIFICATION")
    print(f"  Proposeur annonce : |primes| = 25, DNF_min = 8, defaut = 17")
    print(f"  Refuteur calcule  : |primes| = {pcount}, DNF_min = {dmin}, defaut = {defect}")

    if pcount == 25 and dmin == 8 and defect == 17:
        print()
        print("  *** TRIPLET CONFIRME : (25, 8, 17). ***")
        print()
        print("  n(n-2) = 5 * 3 = 15. Defaut = 17 > 15.")
        print("  L20.5 EST REFUTEE par ce temoin.")
        print("  L21.D (defaut < n(n-2) pour k >= 3) EST REFUTEE par ce temoin.")
        print()
        print("  Z = {0, 3, 5, 25, 30} a 5 zeros, coord-non-degenere,")
        print("  aucune paire antipodale, mais defaut = 17 > 15 = n(n-2).")
    else:
        print()
        print("  *** DISCORDANCE : le Proposeur a fait une erreur. ***")
        print(f"  Triplet attendu : (25, 8, 17). Calcule : ({pcount}, {dmin}, {defect}).")


if __name__ == "__main__":
    main()
