"""
Tour 17 -- DNF_min(IP_{2n}) : Inner Product mod 2, fonction NON-MONOTONE
           non-symetrique, premiere fonction du depot hors de la classe L13.

IP_{2n}(x, y) := x_0 * y_0 + x_1 * y_1 + ... + x_{n-1} * y_{n-1}  (mod 2),
ou x, y ∈ {0,1}^n.

CONTEXTE METHODOLOGIQUE :
  Tours 12-16 ont catalogue 5 familles dans la classe L13 (PARITY, MAJ,
  THRESHOLD_t, MOD_p, et leurs caracterisations). Toutes sont DANS la classe
  des fonctions a `f^{-1}(1)` independent set du n-cube. Le Tour 17 propose
  d'examiner UNE PREMIERE fonction HORS de cette classe.

VERIFICATION HORS-CLASSE :
  IP_4(1,0,1,0) = 1*1 + 0*0 = 1. IP_4(1,1,1,0) = 1*1 + 1*0 = 1.
  Ces deux affectations sont a distance Hamming 1 (different sur x_1).
  Donc IP_4^{-1}(1) n'est PAS un independent set de Q_4.
  Par L13, DNF_min(IP_4) < |IP_4^{-1}(1)| strictement.

OBJECTIFS :
  1. Calculer DNF_min(IP_4) (= IP a n=2, 2n=4 variables) par enumeration.
  2. Calculer DNF_min(IP_6) (n=3, 2n=6) pour cross-validation.
  3. Identifier une formule analytique pour DNF_min(IP_{2n}).
  4. Comparer avec |IP^{-1}(1)| = 2^{2n-1} (= moitie des affectations).

LIEN A P vs NP (condition (k)) :
  IP est la fonction canonique de complexite de communication maximale
  (Chor-Goldreich 1988 : complexite communication = Theta(n)). Or :
  - IP ∈ TC^0 d=2 (Hajnal-Maass-Pudlak-Szegedy 1993, XOR de ANDs avec
    portes threshold).
  - IP ∉ AC^0 a toute profondeur (Razborov-Smolensky 1987 : IP est dans
    AC^0[2], donc PARITY de produits, mais MOD_2 ∉ AC^0[3] etc.).
  - DNF_min(IP_{2n}) borne la taille AC^0 d=2 polynomial.

  Le calcul exhaustif a 2n=4, 6 donne une borne explicite que l'on peut
  comparer aux bornes asymptotiques connues (Razborov-Smolensky pour
  profondeurs superieures).

CONDITION (n) HONOREE : ce theoreme n'est PAS une application de L13 ;
  IP_{2n} n'est pas dans la classe L13 (voisins Hamming-1 dans f^{-1}(1)).
  Donc nouvelle methode de calcul de DNF_min, pas reproduction.

CONDITION (m) HONOREE : separation par TEMOIN (IP ∈ TC^0 d=2 \\ AC^0 d=2 poly
  si DNF_min super-polynomial).
"""

from __future__ import annotations

import itertools
import math


def ip_value(x: tuple[int, ...], n: int) -> int:
    """ IP_{2n}(x) = sum_{i=0..n-1} x_i * x_{n+i} mod 2.
        Convention : les premieres n coordonnees forment x, les n suivantes y."""
    return sum(x[i] * x[n + i] for i in range(n)) % 2


def all_ands(num_vars: int):
    for signs in itertools.product([0, 1, -1], repeat=num_vars):
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


def and_implies_ip(signs: tuple[int, ...], n: int) -> bool:
    """ Verifier que toute affectation satisfaisant le AND a IP = 1. """
    num_vars = 2 * n
    has_sat = False
    for x in itertools.product([0, 1], repeat=num_vars):
        if and_satisfies(signs, x):
            has_sat = True
            if ip_value(x, n) != 1:
                return False
    return has_sat


def is_strictly_more_constrained(small: tuple[int, ...], big: tuple[int, ...]) -> bool:
    """ small a TOUS les litteraux de big plus au moins un autre. """
    for i in range(len(small)):
        if big[i] != 0:
            if small[i] != big[i]:
                return False
    if and_size(small) <= and_size(big):
        return False
    return True


def and_to_string(signs: tuple[int, ...], n: int) -> str:
    if all(s == 0 for s in signs):
        return "1"
    parts = []
    for i, s in enumerate(signs):
        if s == 0:
            continue
        if i < n:
            var = f"x_{i}"
        else:
            var = f"y_{i - n}"
        parts.append(var if s == 1 else f"~{var}")
    return " ∧ ".join(parts)


def compute_dnf_min_ip(n: int, verbose: bool = True) -> tuple[int, list]:
    """ Renvoie (DNF_min, implicants_premiers). """
    num_vars = 2 * n
    truth_set = set()
    for x in itertools.product([0, 1], repeat=num_vars):
        if ip_value(x, n) == 1:
            truth_set.add(x)

    if verbose:
        print(f"  IP_{num_vars} = sum_i x_i*y_i mod 2 sur {num_vars} variables")
        print(f"  |IP^{{-1}}(1)| = {len(truth_set)} (attendu : 2^{2*n-1} = {2**(2*n-1)})")

    # Verifier que IP^{-1}(1) n'est PAS independent set de Q_{2n}.
    not_independent = False
    for x in list(truth_set)[:20]:  # echantillon
        for i in range(num_vars):
            y = list(x)
            y[i] = 1 - y[i]
            y = tuple(y)
            if y in truth_set:
                not_independent = True
                if verbose:
                    print(f"  Voisin Hamming-1 dans IP^{{-1}}(1) : {x} <-> {y}")
                break
        if not_independent:
            break
    if verbose:
        print(f"  IP^{{-1}}(1) n'est PAS independent set : {not_independent}")
        print(f"  -> Hors classe L13. Calcul DNF_min necessite enumeration directe.")
        print()

    # Enumerer implicants.
    ands = list(all_ands(num_vars))
    implicants = [a for a in ands if and_implies_ip(a, n)]
    if verbose:
        print(f"  Total ANDs : {len(ands)} = 3^{num_vars}")
        print(f"  Implicants de IP_{num_vars} : {len(implicants)}")

    # Identifier implicants premiers.
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
        print(f"  Implicants premiers : {len(primes)}")
        # Distribution par taille.
        sizes = {}
        for a in primes:
            s = and_size(a)
            sizes[s] = sizes.get(s, 0) + 1
        print(f"  Distribution par taille : {dict(sorted(sizes.items()))}")
        print()

    # DNF minimal : il faut couvrir toutes les affectations IP=1 avec un
    # sous-ensemble minimum d'implicants premiers (set cover).
    # Pour petite taille, enumerer.

    if verbose:
        print(f"  Recherche du DNF minimal couvrant les {len(truth_set)} affectations IP=1...")

    # Pour chaque implicant premier, l'ensemble d'affectations qu'il couvre.
    coverage = []
    for a in primes:
        covered = set()
        for x in truth_set:
            if and_satisfies(a, x):
                covered.add(x)
        coverage.append((a, covered))

    # Recherche par taille croissante.
    truth_set_frozen = frozenset(truth_set)
    dnf_min = None
    best_cover = None
    for k in range(1, len(primes) + 1):
        # Essayer toutes les combinaisons de k implicants.
        for combo in itertools.combinations(range(len(primes)), k):
            total = set()
            for idx in combo:
                total |= coverage[idx][1]
            if total == truth_set_frozen:
                dnf_min = k
                best_cover = [coverage[idx][0] for idx in combo]
                break
        if dnf_min is not None:
            break

    if verbose:
        print(f"  DNF_min(IP_{num_vars}) = {dnf_min}")
        print(f"  DNF canonique :")
        for a in best_cover:
            print(f"    {and_to_string(a, n)}")
        print()

    return dnf_min, primes


def main() -> None:
    print(f"Tour 17 -- DNF_min(IP_{{2n}}) pour n=2, 3")
    print("=" * 78)
    print()

    print(f"### Cas n=2 (2n=4 variables) ###")
    print()
    dnf_min_4, primes_4 = compute_dnf_min_ip(2, verbose=True)

    print()
    print(f"### Cas n=3 (2n=6 variables) ###")
    print()
    dnf_min_6, primes_6 = compute_dnf_min_ip(3, verbose=True)

    print()
    print("=" * 78)
    print(f"RESULTATS EXPERIMENTAUX :")
    print(f"  DNF_min(IP_4) = {dnf_min_4}")
    print(f"  DNF_min(IP_6) = {dnf_min_6}")
    print()

    # Conjectures testables.
    print(f"Comparaison avec formules candidates :")
    formulas = {
        "|IP^{-1}(1)| = 2^{2n-1}": lambda n: 2 ** (2*n - 1),
        "n * 2^{n-1}": lambda n: n * 2 ** (n - 1),
        "2^n": lambda n: 2 ** n,
        "C(2n, n) / 2": lambda n: math.comb(2*n, n) // 2,
        "n * 2^n / 2": lambda n: n * 2 ** (n - 1),  # idem
    }
    print(f"  {'formule':>30} | {'n=2':>5} | {'n=3':>5}")
    print(f"  {'-'*30} | {'-'*5} | {'-'*5}")
    for name, f in formulas.items():
        v2 = f(2)
        v3 = f(3)
        match2 = "✓" if v2 == dnf_min_4 else ""
        match3 = "✓" if v3 == dnf_min_6 else ""
        print(f"  {name:>30} | {v2:>5} {match2} | {v3:>5} {match3}")


if __name__ == "__main__":
    main()
