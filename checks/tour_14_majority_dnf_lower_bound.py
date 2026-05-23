"""
Tour 14 -- Mini-theoreme : MAJ_n requiert DNF (AC^0 profondeur 2) de taille
exactement C(n, ceil(n/2)).

Consequence (separation entre classes) :
  - MAJ_n est calculable par un seul threshold gate (TC^0 profondeur 1).
  - MAJ_n n'est PAS calculable en AC^0 profondeur 2 polynomial : la taille
    DNF minimale est C(n, ceil(n/2)) ~ 2^n / sqrt(n), super-polynomiale.
  - Donc AC^0 profondeur 2 polynomial ⊊ TC^0 profondeur 1 polynomial.

C'est une separation entre deux classes de circuits, dans la lignee de
Tour 12 mais ouvrant la porte a TC^0 -- premiere apparition explicite de
TC^0 dans le depot.

PREUVE STRUCTURELLE (valable tout n, 4 pas combinatoires) :

  Soit t = ceil(n/2). MAJ_n(x) = 1 ssi sum(x) >= t.

  Pour un AND M, notons pos(M) = nombre de litteraux positifs, neg(M) =
  nombre de litteraux negatifs. Toute assignation satisfaisant M a au moins
  pos(M) variables a 1 et au moins neg(M) variables a 0 (les variables
  libres pouvant prendre toute valeur).

  L14.1 : M est implicant de MAJ_n ssi pos(M) >= t.
    (=>) Si pos(M) < t, en fixant les variables libres a 0, sum(x) =
         pos(M) < t, donc MAJ(x) = 0, donc M non-implicant.
    (<=) Si pos(M) >= t, toute extension a au moins pos(M) >= t 1s, donc
         sum >= t, donc MAJ = 1.

  L14.2 : Aucun implicant PREMIER de MAJ_n ne contient de litteral negatif.
    Soit M un implicant avec ~x_i. L'AND M' = M sans ~x_i a pos(M') =
    pos(M) >= t, donc M' est aussi implicant. M' est strictement moins
    contraint que M, donc M n'est pas premier.

  L14.3 : Les implicants PREMIERS de MAJ_n sont exactement les ANDs de
          exactement t litteraux positifs distincts. Il y en a C(n, t).
    Par L14.1 et L14.2, les implicants premiers sont les ANDs positifs
    de taille >= t. Pour la minimalite, retirer un litteral d'un AND de
    taille > t donne pos = (size-1) qui pourrait etre encore >= t, donc
    non-premier sauf si size = t exactement.

  L14.4 : Chaque implicant premier M_S (sur sous-ensemble S de taille t)
          est satisfait par TOUTES les assignations dont le support
          contient S. En particulier, l'assignation chi_S (uniquement les
          variables de S a 1) ne satisfait QUE M_S parmi les implicants
          premiers. Donc tous les C(n, t) implicants premiers sont
          REQUIS dans tout DNF calculant MAJ_n.

  CONCLUSION : DNF_min(MAJ_n) = C(n, ceil(n/2)) exactement.

VERIFICATION EXHAUSTIVE a n=4 :
  - 3^4 = 81 ANDs enumeres.
  - Identifier les implicants de MAJ_4 (threshold t = 2).
  - Verifier que les implicants premiers sont exactement les 6 = C(4,2)
    paires positives {x_i ∧ x_j : i < j}.
  - Verifier que le DNF canonique de taille 6 calcule MAJ_4.

LIEN A P vs NP (condition (k)) :

  - MAJ_n ∈ TC^0 profondeur 1 (une porte threshold).
  - Notre theoreme : MAJ_n ∉ AC^0 profondeur 2 polynomial.
  - Donc AC^0 profondeur 2 polynomial ⊊ TC^0 profondeur 1 polynomial.

  Cette separation est analogue a Tour 12 (PARITY ∉ AC^0 d=2 -> AC^0 d=2 ⊊ P)
  mais ajoute la classe TC^0 au paysage du depot. La lignee complete devient :
    AC^0 ⊊ AC^0[p] ⊊ ACC^0 ⊊ TC^0 (dans P/poly et conjecturalement dans P)
  ou les separations strictes pour profondeurs constantes sont :
    - AC^0 ⊊ AC^0[p] : Razborov 1987, Smolensky 1987 (PARITY ∉ AC^0[3] etc.)
    - ACC^0 ⊊ TC^0 : ouvert ! C'est la question centrale du programme Williams.

  Notre Tour 14 prouve la separation la plus simple de cette hierarchie a
  profondeur fixe : AC^0 d=2 polynomial ⊊ TC^0 d=1.
"""

from __future__ import annotations

import itertools
import math


def maj_n(x: tuple[int, ...], threshold: int) -> int:
    return 1 if sum(x) >= threshold else 0


def all_ands(n: int):
    for signs in itertools.product([0, 1, -1], repeat=n):
        yield signs


def and_size(signs: tuple[int, ...]) -> int:
    return sum(1 for s in signs if s != 0)


def and_satisfies(signs: tuple[int, ...], x: tuple[int, ...]) -> bool:
    for i, s in enumerate(signs):
        if s == 1 and x[i] != 1:
            return False
        if s == -1 and x[i] != 0:
            return False
    return True


def and_implies_maj(signs: tuple[int, ...], n: int, threshold: int) -> bool:
    """L'AND implique MAJ_n : tout x satisfaisant le AND a sum(x) >= threshold."""
    for x in itertools.product([0, 1], repeat=n):
        if and_satisfies(signs, x):
            if sum(x) < threshold:
                return False
    return True


def and_has_satisfier(signs: tuple[int, ...], n: int) -> bool:
    for x in itertools.product([0, 1], repeat=n):
        if and_satisfies(signs, x):
            return True
    return False


def is_implicant(signs: tuple[int, ...], n: int, threshold: int) -> bool:
    return and_has_satisfier(signs, n) and and_implies_maj(signs, n, threshold)


def is_strictly_more_constrained(small: tuple[int, ...], big: tuple[int, ...]) -> bool:
    """small est strictement plus contraint que big : supp(big) ⊂ supp(small)
       et signs coincident sur supp(big)."""
    for i in range(len(small)):
        if big[i] != 0:
            if small[i] != big[i]:
                return False
    # Verifier que small a strictement plus de litteraux que big.
    if and_size(small) <= and_size(big):
        return False
    return True


def and_to_string(signs: tuple[int, ...]) -> str:
    if all(s == 0 for s in signs):
        return "1 (vide)"
    parts = []
    for i, s in enumerate(signs):
        if s == 1:
            parts.append(f"x_{i}")
        elif s == -1:
            parts.append(f"~x_{i}")
    return " ∧ ".join(parts)


def main() -> None:
    n = 4
    threshold = (n + 1) // 2  # = ceil(n/2). Pour n=4 : t=2.

    print(f"Tour 14 -- MAJ_{n} ∉ AC^0 profondeur 2 polynomial (calcul exhaustif)")
    print("=" * 78)
    print()
    print(f"  MAJ_{n}(x) = 1 ssi sum(x) >= {threshold}.")
    print(f"  Attendu : DNF_min(MAJ_{n}) = C({n}, {threshold}) = {math.comb(n, threshold)}")
    print()

    # Etape 1 : truth table.
    truth = {x: maj_n(x, threshold) for x in itertools.product([0, 1], repeat=n)}
    n_ones = sum(truth.values())
    print(f"  Truth table : MAJ_{n}(x)=1 sur {n_ones} affectations sur {2**n}.")
    # Theoriquement : sum_{k >= t} C(n, k).
    expected = sum(math.comb(n, k) for k in range(threshold, n + 1))
    print(f"  Attendu : sum_{{k>={threshold}}} C({n}, k) = {expected}")
    assert n_ones == expected
    print()

    # Etape 2 : enumerer ANDs et identifier implicants.
    ands = list(all_ands(n))
    print(f"  Total ANDs : {len(ands)} (= 3^{n})")
    implicants = [a for a in ands if is_implicant(a, n, threshold)]
    print(f"  Implicants de MAJ_{n} : {len(implicants)}")
    print()

    # Etape 3 : verifier L14.1 (M implicant ssi pos(M) >= t).
    # Verifier l'equivalence sur tous les ANDs avec satisfacteur.
    failures_L141 = []
    for a in ands:
        if not and_has_satisfier(a, n):
            continue
        pos_a = sum(1 for s in a if s == 1)
        is_imp = is_implicant(a, n, threshold)
        predicted = (pos_a >= threshold)
        if is_imp != predicted:
            failures_L141.append((a, pos_a, is_imp, predicted))
    if failures_L141:
        print(f"  ECHEC L14.1 : {len(failures_L141)} discrepances entre is_implicant et pos>={threshold}")
        for a, pos_a, is_imp, pred in failures_L141[:3]:
            print(f"    {and_to_string(a)} : pos={pos_a}, implicant={is_imp}, predit={pred}")
        return
    print(f"  ✓ L14.1 : M implicant de MAJ_{n} <=> pos(M) >= {threshold}.")
    print(f"             Verifie sur {len(ands)} ANDs.")
    print()

    # Etape 5 : identifier les implicants premiers (minimaux).
    primes = []
    for a in implicants:
        is_prime = True
        for b in implicants:
            if b != a and is_strictly_more_constrained(a, b):
                # a est strictement plus contraint que b ; donc b ⊂ a, donc a non-minimal.
                is_prime = False
                break
        if is_prime:
            primes.append(a)
    expected_primes = math.comb(n, threshold)
    print(f"  Implicants premiers : {len(primes)} (attendu : C({n}, {threshold}) = {expected_primes})")
    if len(primes) != expected_primes:
        print(f"  ECHEC L14.3 : nombre incorrect")
        return
    # Verifier L14.2 et L14.3 : aucun implicant premier n'a de litteral negatif,
    # et tous ont taille = threshold.
    for a in primes:
        if any(s == -1 for s in a):
            print(f"  ECHEC L14.2 : implicant premier avec litteral negatif : {and_to_string(a)}")
            return
        if and_size(a) != threshold:
            print(f"  ECHEC L14.3 : implicant premier de taille {and_size(a)} != {threshold}")
            return
    print(f"  ✓ L14.2 + L14.3 : implicants premiers = {threshold}-subsets positifs distincts.")
    print()

    # Lister les implicants premiers.
    print(f"  Liste des {len(primes)} implicants premiers :")
    for a in sorted(primes, key=lambda x: tuple(i for i, s in enumerate(x) if s == 1)):
        print(f"    {and_to_string(a)}")
    print()

    # Etape 6 : non-redondance (L14.4).
    # Pour chaque assignation x avec sum(x) == threshold, le seul implicant
    # premier qui la satisfait est celui correspondant a support(x).
    print(f"  Verification de non-redondance L14.4 :")
    threshold_assignments = [x for x in itertools.product([0, 1], repeat=n)
                              if sum(x) == threshold]
    print(f"    Assignations a exactement {threshold} 1s : {len(threshold_assignments)}")
    for x in threshold_assignments:
        satisfying = [a for a in primes if and_satisfies(a, x)]
        if len(satisfying) != 1:
            print(f"    ECHEC : x={x} satisfait {len(satisfying)} implicants premiers")
            return
    print(f"  ✓ L14.4 : Chaque telle assignation satisfait EXACTEMENT 1 implicant premier.")
    print(f"  -> Tous les {len(primes)} implicants premiers sont REQUIS dans tout DNF.")
    print()

    # Etape 7 : DNF canonique calcule MAJ_n.
    def dnf_value(mons, x):
        return 1 if any(and_satisfies(m, x) for m in mons) else 0

    correct = all(dnf_value(primes, x) == truth[x] for x in itertools.product([0, 1], repeat=n))
    if not correct:
        print(f"  ECHEC : DNF canonique ne calcule pas MAJ_{n}")
        return
    print(f"  ✓ DNF canonique de taille {len(primes)} calcule MAJ_{n} exactement.")
    print()

    # Bilan.
    print("=" * 78)
    print(f"THEOREME ETABLI (calcul exhaustif n={n}) :")
    print(f"  DNF_min(MAJ_{n}) = C({n}, {threshold}) = {math.comb(n, threshold)}.")
    print()
    print(f"Argument structurel valable pour tout n :")
    print(f"  L14.1 : implicants n'ont que des litteraux positifs.")
    print(f"  L14.2 : ANDs positifs de taille >= ceil(n/2) sont implicants.")
    print(f"  L14.3 : implicants premiers = C(n, ceil(n/2)) ANDs positifs de taille")
    print(f"          exactement ceil(n/2).")
    print(f"  L14.4 : chaque assignation a exactement ceil(n/2) 1s force son")
    print(f"          implicant premier -> tous requis.")
    print(f"  CONCLUSION : DNF_min(MAJ_n) = C(n, ceil(n/2)) ~ 2^n / sqrt(n).")
    print()
    print(f"CONSEQUENCE pour la lignee FSS->Williams :")
    print(f"  - MAJ_n ∈ TC^0 profondeur 1 (une porte threshold sum >= ceil(n/2)).")
    print(f"  - MAJ_n ∉ AC^0 profondeur 2 polynomial.")
    print(f"  -> SEPARATION : AC^0 profondeur 2 polynomial ⊊ TC^0 profondeur 1 polynomial.")
    print()
    print(f"  Premiere apparition de TC^0 dans le depot.")


if __name__ == "__main__":
    main()
