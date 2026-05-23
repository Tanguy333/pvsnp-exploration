"""
Tour 24 -- Refuteur : verification de la construction CFI-rigidification de SAT.

Le Proposeur (numerotation Tour 25 = Tour 24 effectif) propose :

  L25.1 (construction) : pour chaque variable x_i de phi, introduire (x_i^0, x_i^1)
    avec contrainte XOR x_i^0 + x_i^1 = 1. Pour chaque clause C de phi, definir
    une "clause jumelee" C-tilde sur les variables jumelees.
  L25.2 (symetrie) : G = (Z/2)^n agit sur phi-tilde par swap (x_i^0, x_i^1) sur
    chaque variable independamment ; chaque element de G est automorphisme de
    phi-tilde et preserve la satisfiabilite.

ATTAQUE DU REFUTEUR :
  La construction n'a que deux lectures possibles pour C-tilde :

  (A) Avec orientation : choisir x_i^0 = "x_i vrai", x_i^1 = "x_i faux", puis
      traduire chaque litteral x_i (resp. ~x_i) par x_i^0 (resp. x_i^1) dans
      chaque clause.
      -> Lecture syntaxiquement naturelle.
      -> Mais BRISE la symetrie G : un swap sur x_i transforme la clause
         (x_i^0) en (x_i^1), donc le SAT-statut change.

  (B) Sans orientation : remplacer chaque litteral par une expression invariante
      sous swap, e.g. (x_i^0 OR x_i^1).
      -> Mais sous la contrainte XOR, (x_i^0 OR x_i^1) est toujours TRUE.
      -> Donc toutes les clauses jumelees sont tautologiques, et SAT(phi-tilde)
         est trivialement TRUE pour tout phi non-vide. Perte de SAT(phi).

Ce script construit explicitement phi-tilde sous lecture (A), enumere les
2^{2n} affectations, identifie celles qui satisfont phi-tilde, et VERIFIE que
G n'agit PAS comme groupe d'automorphismes sur l'ensemble des solutions.
"""

from __future__ import annotations

import itertools


def parse_clause(literals: list[int]) -> list[tuple[int, bool]]:
    """ Clause encodee comme liste d'entiers (positif = x_i, negatif = ~x_i, indices 1-based).
        Retourne liste de (i, polarite) 0-indexed. """
    return [(abs(L) - 1, L > 0) for L in literals]


def eval_clause(clause: list[tuple[int, bool]], x: tuple[int, ...]) -> bool:
    for (i, pol) in clause:
        if (x[i] == 1) == pol:
            return True
    return False


def is_sat(formula: list[list[tuple[int, bool]]], x: tuple[int, ...]) -> bool:
    return all(eval_clause(c, x) for c in formula)


def cfi_rigidify(phi: list[list[int]], n: int) -> list[list[tuple[int, bool]]]:
    """
    Construit phi-tilde sous lecture (A) avec orientation x_i^0 = "x_i vrai".
    Variables jumelees : x_i^0 a l'index 2i, x_i^1 a l'index 2i+1.

    phi-tilde = (XOR contraintes par i) AND (clauses jumelees).
    Contrainte XOR x_i^0 + x_i^1 = 1 encodee par 2 clauses CNF :
      (x_i^0 OR x_i^1) AND (~x_i^0 OR ~x_i^1)
    Chaque litteral L de phi (sur x_i) devient :
      si L = +x_i : x_i^0   (positif, indice 2i)
      si L = -x_i : x_i^1   (positif, indice 2i+1)
    (autre choix syntaxique aussi valide ; ne change pas le verdict)
    """
    phi_tilde = []
    # Contraintes XOR
    for i in range(n):
        phi_tilde.append(parse_clause([2 * i + 1, 2 * (i + 1) + 1 - 1]))  # (x_i^0 OR x_i^1) en CNF
        phi_tilde.append(parse_clause([-(2 * i + 1), -(2 * (i + 1) + 1 - 1)]))  # (~x_i^0 OR ~x_i^1)
    # Clauses jumelees
    for clause in phi:
        twin = []
        for L in clause:
            i = abs(L) - 1
            if L > 0:
                twin.append(2 * i + 1)       # x_i^0
            else:
                twin.append(2 * i + 2)       # x_i^1
        phi_tilde.append(parse_clause(twin))
    return phi_tilde


def solutions(formula: list[list[tuple[int, bool]]], num_vars: int) -> list[tuple[int, ...]]:
    sols = []
    for x in itertools.product([0, 1], repeat=num_vars):
        if is_sat(formula, x):
            sols.append(x)
    return sols


def apply_swap(sigma: tuple[int, ...], x: tuple[int, ...], n: int) -> tuple[int, ...]:
    """ sigma in {0,1}^n. Pour chaque i, si sigma[i] = 1, swap (x[2i], x[2i+1]). """
    y = list(x)
    for i in range(n):
        if sigma[i] == 1:
            y[2 * i], y[2 * i + 1] = y[2 * i + 1], y[2 * i]
    return tuple(y)


def main() -> None:
    print("Tour 24 -- Verification de L25.1 + L25.2 (CFI-rigidification de SAT)")
    print("=" * 78)
    print()

    # Test 1 : phi = x_1 (SAT trivial, 1 variable, 1 clause).
    print("Test 1 : phi = (x_1)")
    print("-" * 78)
    n = 1
    phi = [[1]]  # Clause : x_1 positif
    phi_tilde = cfi_rigidify(phi, n)
    sols = solutions(phi_tilde, 2 * n)
    print(f"  phi-tilde a {len(sols)} solutions : {sols}")
    print()

    # Verifier que chaque swap sigma in {0,1}^n preserve l'ensemble des solutions.
    print("  Test invariance sous G = (Z/2)^n :")
    for sigma in itertools.product([0, 1], repeat=n):
        if all(s == 0 for s in sigma):
            continue  # sigma = identite
        swapped = set(apply_swap(sigma, s, n) for s in sols)
        sol_set = set(sols)
        preserved = swapped == sol_set
        marker = "preserve" if preserved else "*** CASSE ***"
        print(f"    sigma = {sigma} : sols apres swap = {sorted(swapped)} -- {marker}")
    print()

    # Test 2 : phi = (x_1 OR x_2) AND (~x_1 OR x_2).
    print("Test 2 : phi = (x_1 OR x_2) AND (~x_1 OR x_2)")
    print("-" * 78)
    n = 2
    phi = [[1, 2], [-1, 2]]
    phi_tilde = cfi_rigidify(phi, n)
    sols = solutions(phi_tilde, 2 * n)
    print(f"  phi-tilde a {len(sols)} solutions : {sols}")
    print()
    print("  Test invariance sous G = (Z/2)^n :")
    for sigma in itertools.product([0, 1], repeat=n):
        if all(s == 0 for s in sigma):
            continue
        swapped = set(apply_swap(sigma, s, n) for s in sols)
        sol_set = set(sols)
        preserved = swapped == sol_set
        marker = "preserve" if preserved else "*** CASSE ***"
        print(f"    sigma = {sigma} : preserve ? {marker}")
    print()

    # Test 3 : phi UNSAT (verification que SAT-statut est bien preserve).
    print("Test 3 : phi UNSAT = x_1 AND ~x_1")
    print("-" * 78)
    n = 1
    phi = [[1], [-1]]
    phi_tilde = cfi_rigidify(phi, n)
    sols = solutions(phi_tilde, 2 * n)
    print(f"  phi-tilde a {len(sols)} solutions : {sols} (attendu : 0, car phi UNSAT)")
    print()

    # Test 4 : verification systematique sur petites formules 3-SAT.
    print("Test 4 : statistique sur formules 3-SAT random petites (n=3, m=2..4 clauses)")
    print("-" * 78)
    import random
    random.seed(42)
    n = 3
    counterexamples = 0
    total = 0
    for trial in range(20):
        m = random.randint(2, 4)
        phi = []
        for _ in range(m):
            clause_size = random.randint(2, 3)
            vars_in_clause = random.sample(range(1, n + 1), min(clause_size, n))
            phi.append([v if random.random() > 0.5 else -v for v in vars_in_clause])
        phi_tilde = cfi_rigidify(phi, n)
        sols = solutions(phi_tilde, 2 * n)
        sol_set = set(sols)
        all_preserved = True
        broken_sigma = None
        for sigma in itertools.product([0, 1], repeat=n):
            if all(s == 0 for s in sigma):
                continue
            swapped = set(apply_swap(sigma, s, n) for s in sols)
            if swapped != sol_set:
                all_preserved = False
                broken_sigma = sigma
                break
        total += 1
        if not all_preserved:
            counterexamples += 1
    print(f"  Sur {total} formules 3-SAT random : {counterexamples} ont G action *cassee*.")
    print(f"  Soit {100*counterexamples//total}% de contre-exemples a L25.2.")


if __name__ == "__main__":
    main()
