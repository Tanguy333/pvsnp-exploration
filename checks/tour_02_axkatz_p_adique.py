"""
Tour 02 -- Verification empirique de la faille << signature p-adique d'Ax-Katz >>.

Objectifs du script (tous demontres par enumeration exacte sur petites tailles) :

1. **Lemme 1 du Proposeur est faux pour l'arithmetisation EXACTE.**
   L'arithmetisation produit-naive d'un 3-CNF a k clauses est de degre 3k, donc
   poly(m) -- pas polylog. Razborov-Smolensky donne du polylog mais en
   APPROXIMATION probabiliste, ce qui rend Ax-Katz inapplicable.

2. **Lemme 2 (Ax-Katz) s'ecroule des qu'on impose la contrainte booleenne.**
   En ajoutant les m equations w_i^2 - w_i = 0 (degre 2 chacune) au systeme, le
   minorant d'Ax-Katz mu >= ceil((m - sum d_i) / max d_i) devient <= 0.

3. **v_p(N_alg) ne predit pas N_bool.**
   On exhibe des instances 3-CNF concretes ou le nombre de zeros algebriques sur
   F_p^m et la valuation p-adique correspondante n'ont aucun lien avec le
   nombre de temoins booleens.

Implementation : evaluation directe en int mod p (pas de sympy.subs, trop lent
pour le volume d'enumeration).
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Types et evaluation directe d'un 3-CNF arithmetise sur F_p
# ---------------------------------------------------------------------------

Literal = tuple[int, int]            # (indice var, signe +1 ou -1)
Clause = tuple[Literal, Literal, Literal]


def clause_arith_eval(clause: Clause, w_vals: tuple[int, ...], p: int) -> int:
    """ Evalue c~(w) = 1 - prod_i (1 - lit_i(w)) mod p.
        lit_i positif -> w_i ; negatif -> 1 - w_i (mod p).
    """
    prod = 1
    for (i, sign) in clause:
        if sign == 1:
            lit = w_vals[i] % p
        else:
            lit = (1 - w_vals[i]) % p
        prod = (prod * ((1 - lit) % p)) % p
    return (1 - prod) % p


def cnf_arith_eval(clauses: list[Clause], w_vals: tuple[int, ...], p: int) -> int:
    """ V(w) = prod_j c~_j(w) mod p. """
    v = 1
    for c in clauses:
        v = (v * clause_arith_eval(c, w_vals, p)) % p
    return v


def evaluate_cnf_bool(clauses: list[Clause], a: tuple[int, ...]) -> bool:
    return all(
        any(
            (a[i] == 1 and sign == 1) or (a[i] == 0 and sign == -1)
            for (i, sign) in c
        )
        for c in clauses
    )


# ---------------------------------------------------------------------------
# Comptages exacts
# ---------------------------------------------------------------------------

def n_bool_witnesses(clauses: list[Clause], m: int) -> int:
    return sum(
        1 for a in itertools.product((0, 1), repeat=m) if evaluate_cnf_bool(clauses, a)
    )


def n_algebraic_zeros(clauses: list[Clause], m: int, p: int) -> int:
    """ |{ w in F_p^m : V(w) ≡ 1 (mod p) }| par enumeration. """
    count = 0
    for vals in itertools.product(range(p), repeat=m):
        if cnf_arith_eval(clauses, vals, p) == 1 % p:
            count += 1
    return count


def v_p(n: int, p: int) -> int | float:
    if n == 0:
        return math.inf
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


# ---------------------------------------------------------------------------
# Borne d'Ax-Katz
# ---------------------------------------------------------------------------

def ax_katz_lower_mu(n_vars: int, degrees: list[int]) -> int:
    """ Pour r polynomes en n_vars vars sur F_q, degres d_i :
            q^mu | N,   mu >= ceil((n_vars - sum d_i) / max d_i)
        (triviale, i.e. >= 0, quand le numerateur est <= 0).
    """
    if not degrees:
        return n_vars
    num = n_vars - sum(degrees)
    den = max(degrees)
    return max(0, math.ceil(num / den))


# ---------------------------------------------------------------------------
# Instances de test (6 variables)
# ---------------------------------------------------------------------------

@dataclass
class Instance:
    name: str
    m: int
    clauses: list[Clause]
    expected_n_bool: int | None = None


def make_instances() -> list[Instance]:
    # (A) UNSAT : toutes les 8 clauses (+/-x_0 v +/-x_1 v +/-x_2). Pour chaque
    #     affectation (a_0,a_1,a_2), exactement une clause est non satisfaite
    #     (celle dont tous les signes sont contraires) -> UNSAT.
    unsat: list[Clause] = []
    for s0 in (-1, 1):
        for s1 in (-1, 1):
            for s2 in (-1, 1):
                unsat.append(((0, s0), (1, s1), (2, s2)))

    # (B) SAT a temoin unique (1,1,1,1,1,1). Pour chaque i, on ajoute 4 clauses
    #     (x_i v +/-x_j v +/-x_k) avec j=i+1, k=i+2 (mod 6). Le AND des 4
    #     pour les 4 combinaisons de signes implique x_i = 1.
    sat1: list[Clause] = []
    m_b = 6
    for i in range(m_b):
        j = (i + 1) % m_b
        k = (i + 2) % m_b
        for sj in (-1, 1):
            for sk in (-1, 1):
                sat1.append(((i, 1), (j, sj), (k, sk)))

    # (C) SAT a peu de clauses (multiples temoins).
    sat_many: list[Clause] = [
        ((0, 1), (1, 1), (2, 1)),
        ((3, 1), (4, 1), (5, 1)),
        ((0, -1), (3, -1), (5, 1)),
        ((1, -1), (2, 1), (4, -1)),
    ]

    return [
        Instance("(A) UNSAT toutes +/-x_0+/-x_1+/-x_2", 6, unsat, expected_n_bool=0),
        Instance("(B) SAT temoin unique (1,...,1)",      6, sat1,  expected_n_bool=1),
        Instance("(C) SAT 4 clauses, multiples temoins", 6, sat_many),
    ]


# ---------------------------------------------------------------------------
# Pipeline d'analyse
# ---------------------------------------------------------------------------

def analyse(instance: Instance, primes: list[int]) -> None:
    print(f"\n{'=' * 78}")
    print(f"Instance : {instance.name}")
    print(f"  m = {instance.m}, k = {len(instance.clauses)} clauses")

    deg_V = 3 * len(instance.clauses)  # degre exact du produit des c~_j
    print(f"  Degre d'arithmetisation exacte (produit des c~_j) : {deg_V} = 3*k")
    print(f"  -> Faille n.1 : poly(m), PAS polylog (le Lemme 1 du Proposeur invoque")
    print(f"     Razborov-Smolensky, qui est une APPROXIMATION probabiliste, pas une")
    print(f"     arithmetisation exacte. Ax-Katz exige l'egalite exacte.)")

    N_bool = n_bool_witnesses(instance.clauses, instance.m)
    line = f"  N_bool = |{{w in {{0,1}}^m : phi(w)=1}}| = {N_bool}"
    if instance.expected_n_bool is not None:
        ok = "OK" if N_bool == instance.expected_n_bool else "MISMATCH"
        line += f"   [attendu : {instance.expected_n_bool} -- {ok}]"
    print(line)

    for p in primes:
        N_alg = n_algebraic_zeros(instance.clauses, instance.m, p)
        mu_alg = ax_katz_lower_mu(instance.m, [deg_V])              # sans contrainte
        mu_bool = ax_katz_lower_mu(                                  # avec contrainte
            instance.m, [deg_V] + [2] * instance.m
        )
        vp_Nalg = v_p(N_alg, p)
        vp_Nbool = v_p(N_bool, p)
        print(
            f"  p={p}: N_alg(F_p^m)={N_alg:>8}, v_p(N_alg)={vp_Nalg}, "
            f"v_p(N_bool)={vp_Nbool}  | Ax-Katz mu >= {mu_alg} (libre), "
            f">= {mu_bool} (contrainte booleenne)"
        )


def main() -> None:
    print("Tour 02 -- Verification de l'invariant p-adique d'Ax-Katz pour NP_{AC^0}")
    print("=" * 78)

    primes = [3, 5, 7]
    for inst in make_instances():
        analyse(inst, primes)

    print("\n" + "=" * 78)
    print("BILAN")
    print(
        "1. Le degre exact d'arithmetisation est 3k = poly(m), pas polylog.\n"
        "   Le Lemme 1 confond approximation probabiliste (Razborov-Smolensky)\n"
        "   et arithmetisation exacte. Ax-Katz exige l'egalite exacte.\n"
        "\n"
        "2. Ajouter la contrainte booleenne (m equations w_i^2 - w_i = 0) fait\n"
        "   chuter la borne d'Ax-Katz a 0 dans TOUS les cas testes (numerateur\n"
        "   m - 3k - 2m = -m - 3k < 0). L'invariant p-adique sur {0,1}^m est\n"
        "   donc trivialement borne par 1 -- aucune contrainte geometrique.\n"
        "\n"
        "3. v_p(N_alg) et v_p(N_bool) sont decorrelles. Une instance avec un\n"
        "   unique temoin booleen (v_p(N_bool)=0) coexiste avec un N_alg de\n"
        "   valuation arbitraire. L'invariant ne distingue rien d'utile pour SAT.\n"
        "\n"
        "Conclusion : l'idee compte des zeros algebriques sur F_p, qui n'ont aucun\n"
        "rapport direct avec l'existence d'un temoin booleen, tandis qu'Ax-Katz\n"
        "est desamorce des qu'on ajoute la contrainte w_i^2 = w_i. -> FAILLE FATALE\n"
        "sur le pont algebrique<->booleen."
    )


if __name__ == "__main__":
    main()
