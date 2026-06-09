"""
TACHE F-004 -- Structure des PTF L1-optimales d'IP : vers la preuve d'O-F002.

O-F002 (confirmee a 4 points par F-001/F-002) :
    min_D W_L1(IP_{2k}, D) = (3^k - 1)/2 = DNF_min(IP_{2k}).

HYPOTHESE STRUCTURELLE A TESTER (borne superieure) :
  Le polynome multilineaire EXACT de IP_{2k},
      p*(x, y) = (1 - prod_{i=1}^k (1 - 2 x_i y_i)) / 2,
  (qui vaut exactement IP sur {0,1}^{2k}, donc est une PTF a fortiori)
  a pour coefficients, sur le monome m_S = prod_{i in S} x_i y_i
  (S non vide) :  c_S = (-1)^{|S|+1} 2^{|S|-1},
  d'ou  L1(p*) = sum_{s=1}^k C(k,s) 2^{s-1} = (3^k - 1)/2.

  Si cela se verifie : la moitie "<=" d'O-F002 est PROUVEE structurellement
  (pour tout k), et seul le sens ">=" (borne inferieure) reste ouvert.

PARTIE 2 : extraire les solutions L1-optimales de l'ILP a k=2, 3 et
comparer leur support/signes a p*.
"""

from __future__ import annotations

import csv
import itertools

import pulp


def inner_product(x: tuple[int, ...]) -> int:
    n = len(x)
    half = n // 2
    return sum(a * b for a, b in zip(x[:half], x[half:])) % 2


# ------------------------------------------------------------------ Partie 1

def exact_multilinear_ip(k: int) -> dict[tuple[int, ...], int]:
    """
    Coefficients du polynome multilineaire exact de IP_{2k} dans la base
    des monomes 0/1 sur les variables (x_1..x_k, y_1..y_k), obtenus par
    expansion de (1 - prod (1 - 2 x_i y_i)) / 2.
    Variables indexees 0..k-1 (x) et k..2k-1 (y).
    Retourne {tuple_indices_du_monome: coefficient}.
    """
    coeffs: dict[tuple[int, ...], int] = {}
    for s in range(1, k + 1):
        for S in itertools.combinations(range(k), s):
            mono = tuple(sorted([i for i in S] + [i + k for i in S]))
            coeffs[mono] = (-1) ** (s + 1) * 2 ** (s - 1)
    return coeffs


def eval_poly(coeffs: dict, x: tuple[int, ...]) -> int:
    total = 0
    for mono, c in coeffs.items():
        p = 1
        for i in mono:
            p *= x[i]
        total += c * p
    return total


def verify_exact(k: int) -> tuple[bool, int]:
    coeffs = exact_multilinear_ip(k)
    n = 2 * k
    ok = all(eval_poly(coeffs, x) == inner_product(x)
             for x in itertools.product([0, 1], repeat=n))
    l1 = sum(abs(c) for c in coeffs.values())
    return ok, l1


# ------------------------------------------------------------------ Partie 2

def monomials_up_to(n: int, max_deg: int):
    out = []
    for d in range(max_deg + 1):
        out.extend(itertools.combinations(range(n), d))
    return out


def ilp_optimal(k: int):
    """ Resout min L1 a degre plein pour IP_{2k} et retourne la solution. """
    n = 2 * k
    monos = monomials_up_to(n, n)
    prob = pulp.LpProblem("f004", pulp.LpMinimize)
    c = [pulp.LpVariable(f"c{i}", lowBound=-1000, upBound=1000, cat="Integer")
         for i in range(len(monos))]
    a = [pulp.LpVariable(f"a{i}", lowBound=0) for i in range(len(monos))]
    for i in range(len(monos)):
        prob += a[i] >= c[i]
        prob += a[i] >= -c[i]
    prob += pulp.lpSum(a)
    for x in itertools.product([0, 1], repeat=n):
        s = pulp.lpSum(c[i] * (1 if all(x[j] for j in monos[i]) else 0)
                       for i in range(len(monos)))
        if inner_product(x) == 1:
            prob += s >= 1
        else:
            prob += s <= 0
    solver = pulp.PULP_CBC_CMD(msg=False, timeLimit=300)
    prob.solve(solver)
    sol = {}
    for i, mono in enumerate(monos):
        v = round(c[i].value())
        if v != 0:
            sol[mono] = v
    return sol, round(pulp.value(prob.objective))


def describe(sol: dict, k: int) -> str:
    """ Decrit le support : chaque monome est-il 'apparie' (de la forme
        prod_{i in S} x_i y_i) ? """
    paired = 0
    other = 0
    for mono in sol:
        xs = set(i for i in mono if i < k)
        ys = set(i - k for i in mono if i >= k)
        if xs == ys and xs:
            paired += 1
        else:
            other += 1
    return f"{len(sol)} monomes ({paired} apparies prod x_i y_i, {other} autres)"


def main() -> None:
    print("TACHE F-004 -- structure des PTF L1-optimales d'IP")
    print("=" * 72)

    # Partie 1 : le polynome exact realise-t-il (3^k-1)/2 ?
    print("\nPartie 1 : polynome multilineaire exact p* (borne superieure)")
    print("-" * 72)
    for k in range(1, 6):
        ok, l1 = verify_exact(k)
        target = (3 ** k - 1) // 2
        mark = "OK" if (ok and l1 == target) else "ECHEC"
        print(f"  k={k} : p* = IP partout ? {ok} ; L1(p*) = {l1} ; "
              f"(3^k-1)/2 = {target}  [{mark}]")

    # Partie 2 : optima ILP et comparaison
    print("\nPartie 2 : solutions L1-optimales de l'ILP (k=2, 3)")
    print("-" * 72)
    rows = []
    for k in [2, 3]:
        sol, l1 = ilp_optimal(k)
        exact = exact_multilinear_ip(k)
        same = (sol == exact)
        print(f"  k={k} : L1 = {l1} ; support ILP : {describe(sol, k)} ; "
              f"identique a p* ? {same}")
        if not same:
            print(f"         p*  : {describe(exact, k)}")
            print(f"         ILP : {sorted(sol.items())[:8]}{' ...' if len(sol) > 8 else ''}")
        for mono, c in sorted(sol.items()):
            rows.append({"k": k, "source": "ILP", "monome": str(mono), "coef": c})
        for mono, c in sorted(exact.items()):
            rows.append({"k": k, "source": "exact", "monome": str(mono), "coef": c})

    with open("data/optimal_ptf_structure.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["k", "source", "monome", "coef"])
        w.writeheader()
        w.writerows(rows)
    print("\nCSV : data/optimal_ptf_structure.csv")


if __name__ == "__main__":
    main()
