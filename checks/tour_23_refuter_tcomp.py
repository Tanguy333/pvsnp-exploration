"""
Tour 23 -- Refuteur : verification independante des chiffres tcomp du Proposeur.

Le Proposeur (Claude jouant le role) a annonce sans livrer de script :
  OR_4 = (1, 1), AND_4 = (1, 3), PARITY_4 = (4, 8), MAJ_4 = (1, 1),
  IP_4 = (2, 2), IP_6 = (3, 4), IP_8 = (4, 8),
  conjecture tcomp(IP_{2k}) = (k, 2^{k-1}).

Le chiffre IP_4 = (2, 2) parait SUSPECT vis-a-vis de la litterature :
  - Sherstov 2008 (sign-rank of IP_n = 2^{n/2}) borne la representation.
  - Krause-Pudlak 1998 etablissent un tradeoff degre-magnitude exponentiel.

Definition utilisee (proposition Tour 23) :
  tcomp(f) = (d_min, m_min) ou
    d_min = plus petit degre d'un polynome p in Z[x_1..x_n] tel que
            (f(x) = 1 <=> p(x) > 0)
    m_min = plus petit M tel que tous les |c_S| <= M (pour ce degre d_min).

Comme p est entier, p(x) > 0 <=> p(x) >= 1, et p(x) <= 0 reste <= 0.

Algorithme : ILP via PuLP/CBC.
  - Pour D = 0, 1, 2, ..., n : balayer.
  - Pour chaque D, par recherche dichotomique sur M = 1, 2, 4, ..., trouver
    le plus petit M tel que l'ILP soit faisable.
  - Renvoyer (D_min, M_min) avec D_min le plus petit D admettant une solution.

Fonctions testees :
  OR_n, AND_n, PARITY_n, MAJ_n (avec convention sum >= ceil(n/2)),
  IP_{2k} pour k = 2, 3, 4 (n = 4, 6, 8).
"""

from __future__ import annotations

import itertools
from collections.abc import Callable

import pulp


def or_n(x: tuple[int, ...]) -> int:
    return 1 if any(x) else 0


def and_n(x: tuple[int, ...]) -> int:
    return 1 if all(x) else 0


def parity_n(x: tuple[int, ...]) -> int:
    return sum(x) % 2


def majority_n(x: tuple[int, ...]) -> int:
    # MAJ_n : sum >= ceil(n/2)
    n = len(x)
    return 1 if sum(x) >= (n + 1) // 2 else 0


def threshold_t(t: int) -> Callable[[tuple[int, ...]], int]:
    def thr(x: tuple[int, ...]) -> int:
        return 1 if sum(x) >= t else 0
    return thr


def inner_product(x: tuple[int, ...]) -> int:
    """ IP_{2k}(x_1..x_k, y_1..y_k) = XOR_i (x_i AND y_i). """
    n = len(x)
    assert n % 2 == 0
    k = n // 2
    xs = x[:k]
    ys = x[k:]
    s = sum(a * b for a, b in zip(xs, ys))
    return s % 2


def mod_p_n(p: int) -> Callable[[tuple[int, ...]], int]:
    def f(x: tuple[int, ...]) -> int:
        return 1 if sum(x) % p == 0 else 0
    return f


def enumerate_monomials(n: int, max_deg: int) -> list[tuple[int, ...]]:
    """ Toutes les sous-ensembles S de [n] avec |S| <= max_deg (forme tuple trie). """
    result = []
    for d in range(max_deg + 1):
        for combo in itertools.combinations(range(n), d):
            result.append(combo)
    return result


def monomial_eval(S: tuple[int, ...], x: tuple[int, ...]) -> int:
    """ Evalue le monome ∏_{i in S} x_i sur l'affectation x. """
    if not S:
        return 1
    p = 1
    for i in S:
        p *= x[i]
    return p


def is_feasible(f: Callable[[tuple[int, ...]], int], n: int, D: int, M: int) -> bool:
    """
    Existe-t-il un polynome p sur Z[x_1..x_n] de degre <= D, coefs dans [-M, M],
    tel que f(x) = 1 <=> p(x) >= 1 et f(x) = 0 <=> p(x) <= 0 ?
    """
    monomials = enumerate_monomials(n, D)
    prob = pulp.LpProblem("tcomp_feasibility", pulp.LpMinimize)
    c = [pulp.LpVariable(f"c_{i}", lowBound=-M, upBound=M, cat="Integer")
         for i in range(len(monomials))]
    prob += 0  # objectif factice (faisabilite)
    for x in itertools.product([0, 1], repeat=n):
        s = pulp.lpSum(c[i] * monomial_eval(monomials[i], x) for i in range(len(monomials)))
        if f(x) == 1:
            prob += s >= 1
        else:
            prob += s <= 0
    solver = pulp.PULP_CBC_CMD(msg=False, timeLimit=60)
    status = prob.solve(solver)
    return status == pulp.LpStatusOptimal


def compute_tcomp(f: Callable[[tuple[int, ...]], int], n: int, M_cap: int = 4096) -> tuple[int, int]:
    """
    Calcule tcomp(f) = (D_min, M_min) :
      - D_min = plus petit degre admettant une representation
      - M_min = plus petite magnitude (puissance de 2) telle que (D_min, M_min) faisable
    """
    for D in range(n + 1):
        # Recherche du plus petit M par doublement.
        M = 1
        while M <= M_cap:
            if is_feasible(f, n, D, M):
                # Une fois trouve, raffiner M par recherche lineaire decroissante.
                # M est faisable. Tester M-1, M-2, ..., 1 pour trouver le plus petit.
                M_min = M
                for M_test in range(M - 1, 0, -1):
                    if is_feasible(f, n, D, M_test):
                        M_min = M_test
                    else:
                        break
                return (D, M_min)
            M *= 2
    raise RuntimeError(f"Pas de representation trouvee avec M <= {M_cap}")


def label(f_name: str, n: int) -> str:
    return f"{f_name}_{n}"


def main() -> None:
    print("Tour 23 -- Verification independante du tableau tcomp du Proposeur")
    print("=" * 78)
    print()

    test_cases = [
        ("OR", 4, or_n),
        ("AND", 4, and_n),
        ("PARITY", 4, parity_n),
        ("MAJ", 4, majority_n),
        ("THR_1", 4, threshold_t(1)),
        ("THR_2", 4, threshold_t(2)),
        ("THR_3", 4, threshold_t(3)),
        ("THR_4", 4, threshold_t(4)),
        ("MOD_2", 4, mod_p_n(2)),
        ("MOD_3", 4, mod_p_n(3)),
        ("IP", 4, inner_product),
        ("IP", 6, inner_product),
        ("IP", 8, inner_product),
    ]

    proposeur_claims = {
        "OR_4": (1, 1),
        "AND_4": (1, 3),
        "PARITY_4": (4, 8),
        "MAJ_4": (1, 1),
        "MOD_2_4": (4, 8),
        "MOD_3_4": (3, 3),
        "IP_4": (2, 2),
        "IP_6": (3, 4),
        "IP_8": (4, 8),
    }

    results = {}
    for name, n, f in test_cases:
        lbl = label(name, n)
        print(f"Test {lbl} (n = {n})...")
        d_min, m_min = compute_tcomp(f, n)
        results[lbl] = (d_min, m_min)
        claim = proposeur_claims.get(lbl)
        if claim is None:
            print(f"  -> calcule : (deg={d_min}, mag={m_min})  [pas de claim du Proposeur]")
        else:
            ok = (d_min, m_min) == claim
            marker = "OK" if ok else "DIVERGENCE"
            print(f"  -> calcule : (deg={d_min}, mag={m_min})  vs Proposeur : {claim}  [{marker}]")
        print()

    print("=" * 78)
    print("Resume des divergences :")
    divergences = []
    for lbl, claim in proposeur_claims.items():
        if lbl in results and results[lbl] != claim:
            divergences.append((lbl, claim, results[lbl]))
    if not divergences:
        print("  Aucune divergence -- les chiffres du Proposeur sont confirmes.")
    else:
        for lbl, claim, actual in divergences:
            print(f"  {lbl} : Proposeur annonce {claim}, Refuteur calcule {actual}")


if __name__ == "__main__":
    main()
