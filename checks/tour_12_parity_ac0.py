"""
Tour 12 -- Mini-theoreme : PARITY_n n'est pas calculable par un AC^0 profondeur 2
            de taille < 2^(n-1).

Cible prescrite par le Refuteur apres deux propositions ecartees.

ENONCE FORMEL
  Soit parity_n : {0,1}^n -> {0,1}, parity_n(x) = x_0 XOR x_1 XOR ... XOR x_{n-1}.
  Soit "AC^0 profondeur 2" = DNF = OR de ANDs, sans contrainte de fan-in.
  Theoreme : la taille minimale (nombre de ANDs) d'un DNF calculant parity_n est
             exactement 2^(n-1).

PREUVE (structurelle, valable pour tout n) :
  (a) Tout implicant premier de parity_n a taille exactement n.
      Soit M un AND de k < n litteraux. M ne fixe pas une variable, disons x_i.
      Pour toute affectation y satisfaisant M, l'affectation y' obtenue en
      flippant x_i satisfait aussi M. Or parity_n(y) != parity_n(y'). Donc
      l'ensemble {x : M(x) = 1} contient des x avec parity(x)=0 et parity(x)=1.
      Donc M n'implique pas parity_n. Contradiction.
  (b) Les implicants premiers de taille n sont les mintermes complets
      correspondant aux affectations x avec parity(x)=1. Il y en a 2^(n-1).
  (c) Aucun n'est redondant : chaque minterm complet M_x est satisfait par
      l'unique affectation x, donc pour calculer parity sur toute la classe
      d'entrees impaires, tous les 2^(n-1) mintermes doivent figurer dans le DNF.
  CONCLUSION : la taille DNF minimale = 2^(n-1).

VERIFICATION EXHAUSTIVE a n=4 :
  - Enumerer les 3^4 = 81 ANDs sur 4 variables (chaque variable : absente,
    positive, ou negative).
  - Identifier les implicants de parity_4 (M tel que M(x)=1 implique parity(x)=1).
  - Verifier qu'aucun n'a taille < 4.
  - Exhiber les 2^3 = 8 implicants premiers.
  - Confirmer la borne 2^(n-1) = 8 pour parity_4.

LIEN A P vs NP (condition (k)) :
  PARITY n'est pas dans AC^0 (Furst-Saxe-Sipser 1981, Hastad 1986) est le
  premier theoreme non-trivial de borne inferieure de circuit. Il a ouvert la
  voie a Razborov-Smolensky 1987 (ACC^0[p]), puis Williams 2011 (NEXP ⊄ ACC^0)
  -- seul resultat ayant franchi les trois barrieres (relativisation,
  algebrisation, preuves naturelles). Tout chemin vers P vs NP qui passe par
  des bornes inferieures de circuit doit, a minima, etre capable de reproduire
  PARITY ∉ AC^0 a profondeur 2.

  Le mini-theoreme ici prouve une version restreinte (profondeur 2 fixe) par
  calcul exhaustif, etablissant la "premiere brique" du programme.
"""

from __future__ import annotations

import itertools


def parity_n(x: tuple[int, ...]) -> int:
    return sum(x) & 1


def all_ands(n: int):
    """Tous les ANDs : chaque variable est absente (0), positive (1) ou negative (-1).
       Total : 3^n monomes (y compris le vide qui est la constante 1)."""
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


def and_implies_parity(signs: tuple[int, ...], n: int) -> bool:
    """ True ssi pour tout x avec AND(x)=1, parity(x)=1. """
    for x in itertools.product([0, 1], repeat=n):
        if and_satisfies(signs, x):
            if parity_n(x) != 1:
                return False
    return True


def and_is_implicant_of_parity(signs: tuple[int, ...], n: int) -> bool:
    """ Implicant : (i) il existe au moins un x satisfaisant le AND
        (sinon vacuously implicant, exclu), (ii) AND => parity. """
    # Verifier qu'au moins un x satisfait le AND.
    has_satisfier = False
    for x in itertools.product([0, 1], repeat=n):
        if and_satisfies(signs, x):
            has_satisfier = True
            break
    if not has_satisfier:
        return False
    return and_implies_parity(signs, n)


def support(signs: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(i for i, s in enumerate(signs) if s != 0)


def is_subimplicant(s1: tuple[int, ...], s2: tuple[int, ...]) -> bool:
    """ s1 est sous-implicant de s2 si supp(s1) ⊆ supp(s2) et signs match. """
    for i in range(len(s1)):
        if s1[i] != 0:
            if s2[i] != s1[i]:
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
    return " ∧ ".join(parts)


def main() -> None:
    n = 4
    print(f"Tour 12 -- PARITY_{n} ∉ AC^0 profondeur 2 (calcul exhaustif)")
    print("=" * 78)
    print()

    # Etape 1 : tableau de verite de parity_n.
    parity_truth = {x: parity_n(x) for x in itertools.product([0, 1], repeat=n)}
    n_odd = sum(1 for v in parity_truth.values() if v == 1)
    print(f"  parity_{n} sur {{0,1}}^{n} :")
    print(f"    #entrees totales : {2**n}")
    print(f"    #entrees impaires (parity=1) : {n_odd}  (attendu : 2^{n-1} = {2**(n-1)})")
    assert n_odd == 2 ** (n - 1)
    print()

    # Etape 2 : enumerer tous les ANDs et identifier les implicants.
    ands = list(all_ands(n))
    print(f"  Total ANDs sur {n} variables : {len(ands)}  (attendu : 3^{n} = {3**n})")
    assert len(ands) == 3 ** n

    implicants = [a for a in ands if and_is_implicant_of_parity(a, n)]
    print(f"  Implicants de parity_{n} (AND ⇒ parity_{n}) : {len(implicants)}")
    print()

    # Etape 3 : verifier qu'aucun implicant n'a taille < n.
    implicants_by_size: dict[int, list] = {}
    for a in implicants:
        s = and_size(a)
        implicants_by_size.setdefault(s, []).append(a)

    print(f"  Distribution des tailles d'implicants :")
    for s in sorted(implicants_by_size):
        print(f"    taille {s} : {len(implicants_by_size[s])} implicants")
    print()

    # Etape 4 : verifier la propriete clef.
    small_implicants = [a for a in implicants if and_size(a) < n]
    if small_implicants:
        print(f"  ECHEC : {len(small_implicants)} implicants de taille < {n}")
        for a in small_implicants[:5]:
            print(f"    {and_to_string(a)}")
        return
    print(f"  ✓ Aucun implicant de taille < {n}. Tout implicant a taille = {n}.")
    print()

    # Etape 5 : les implicants de taille n sont exactement les mintermes impairs.
    implicants_max = implicants_by_size[n]
    # Chaque tel implicant determine une affectation x : x_i = 1 si signe = 1, sinon 0.
    impl_assignments = set()
    for a in implicants_max:
        x = tuple(1 if s == 1 else 0 for s in a)
        impl_assignments.add(x)
    odd_assignments = {x for x, v in parity_truth.items() if v == 1}
    print(f"  Implicants premiers (taille = {n}) -> affectations correspondantes :")
    print(f"    nb affectations distinctes = {len(impl_assignments)}")
    print(f"    nb affectations impaires de parity = {len(odd_assignments)}")
    if impl_assignments == odd_assignments:
        print(f"  ✓ Bijection : implicants premiers ↔ affectations impaires.")
    else:
        diff1 = impl_assignments - odd_assignments
        diff2 = odd_assignments - impl_assignments
        print(f"  ECHEC : ensembles differents. Symetrique difference :")
        print(f"    impl - odd = {diff1}")
        print(f"    odd - impl = {diff2}")
        return
    print()

    # Etape 6 : aucun implicant premier n'est redondant.
    # Chaque affectation impaire x n'est satisfaite que par son propre implicant.
    print(f"  Verification de non-redondance :")
    for x in sorted(odd_assignments):
        satisfying_implicants = [a for a in implicants_max if and_satisfies(a, x)]
        if len(satisfying_implicants) != 1:
            print(f"    ECHEC : x={x} satisfait {len(satisfying_implicants)} implicants")
            return
    print(f"  ✓ Chaque affectation impaire est satisfaite par exactement 1 implicant premier.")
    print(f"  -> Tout DNF calculant parity_{n} doit inclure les {len(odd_assignments)} implicants.")
    print()

    # Etape 7 : aucune sous-DNF de taille < 2^(n-1) ne calcule parity_n.
    print(f"  Verification que la borne 2^({n-1}) = {2**(n-1)} est SERREE :")
    print(f"    DNF de taille {2**(n-1)} : OR des {2**(n-1)} mintermes impairs.")
    # Verifier que cette DNF calcule parity_n.
    def dnf_value(monomes, x):
        return 1 if any(and_satisfies(m, x) for m in monomes) else 0
    canonical_dnf = implicants_max
    correct = all(dnf_value(canonical_dnf, x) == parity_truth[x]
                  for x in itertools.product([0, 1], repeat=n))
    if correct:
        print(f"  ✓ DNF canonique de taille {len(canonical_dnf)} calcule parity_{n} exactement.")
    else:
        print(f"  ECHEC : DNF canonique ne calcule pas parity.")
        return
    print()

    print("=" * 78)
    print(f"THEOREME ETABLI (calcul exhaustif n={n}) :")
    print(f"  La taille minimale d'un DNF calculant parity_{n} est EXACTEMENT 2^{n-1} = {2**(n-1)}.")
    print(f"  -> parity_{n} ∉ AC^0 profondeur 2 de taille < {2**(n-1)}.")
    print()
    print(f"Argument structurel valable pour tout n :")
    print(f"  (a) Tout AND de < n litteraux ne fixe pas une variable, donc admet")
    print(f"      des satisfaisants de parite differente -> n'est pas implicant.")
    print(f"  (b) Donc tous les implicants ont taille n -> mintermes complets.")
    print(f"  (c) Il y a 2^(n-1) mintermes impairs, et chacun est satisfait par")
    print(f"      une unique affectation, donc tous sont necessaires.")
    print(f"  CONCLUSION : DNF minimal pour parity_n a taille = 2^(n-1).")
    print()
    print(f"Verifie empiriquement pour n={n}. Verifiable symboliquement pour tout n.")


if __name__ == "__main__":
    main()
