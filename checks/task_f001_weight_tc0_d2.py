"""
TACHE F-001 -- Weight L1 des PTF pour fonctions TC^0 d=2 \\ TC^0 d=1.

Origine : prescription Tour 24 du cahier (jamais honoree, 2 esquives) + q.13
(distinction magnitude L_infty / weight L1 -- c'est la weight L1 qui apparait
dans Krause-Pudlak 1998 et dans la methode algorithmique Beigel-Tarui -> Williams).

QUESTION CIBLE : existe-t-il une fonction f in TC^0 d=2 \\ TC^0 d=1 dont la
weight L1 de PTF est polynomiale en n ?

Definitions :
  - PTF entiere de f : p in Z[x_1..x_n] (base monomiale 0/1) tel que
      f(x) = 1 <=> p(x) >= 1   et   f(x) = 0 <=> p(x) <= 0.
  - W(f, D) = min { sum_S |c_S| : p PTF de f, deg(p) <= D }  (weight L1)
  - L_infty rapporte = max_S |c_S| de la solution L1-optimale trouvee.

Fonctions cibles (TC^0 d=2 \\ d=1) :
  - EXACT_k(x) = 1 ssi sum(x) = k.
      * in TC^0 d=2 : AND([sum >= k], [sum <= k]) -- AND est un seuil, depth 2.
      * not in TC^0 d=1 : l'infaisabilite de l'ILP a D=1 en est la preuve
        executable (degre-1 PTF entiere = threshold gate).
      Points (condition r, 3 points) : (n=4,k=2), (n=5,k=2), (n=6,k=3).
  - IP_{2k} : in TC^0 d=2 (Hajnal-Maass-Pudlak-Szegedy 1993), temoin attendu de
    weight exponentielle (Bruck-Smolensky 1992 : norme spectrale 2^{n/2}).
      Points (condition r, 3 points) : n=4, 6, 8.

Sanity checks : MAJ_4 (d=1, weight petite), PARITY_4 (degre 4).

Algorithme : ILP PuLP/CBC.
  - Variables c_S entieres dans [-CAP, CAP] pour |S| <= D.
  - Variables a_S >= 0 avec a_S >= c_S et a_S >= -c_S (linearisation de |c_S|).
  - Contraintes : sum_S c_S prod_{i in S} x_i >= 1 si f(x)=1, <= 0 sinon.
  - Objectif : min sum_S a_S.
  - Balayage D = 0..n ; lignes infaisables rapportees INFEASIBLE.

Output : data/weight_tc0_d2.csv
  colonnes : fonction, n, degre, L1_min, Linf_solution, statut.
"""

from __future__ import annotations

import csv
import itertools
import time

import pulp

CAP = 100_000
TIME_LIMIT = 180  # secondes par solve


# ---------------------------------------------------------------- fonctions

def exact_k(k: int):
    def f(x: tuple[int, ...]) -> int:
        return 1 if sum(x) == k else 0
    return f


def inner_product(x: tuple[int, ...]) -> int:
    n = len(x)
    assert n % 2 == 0
    half = n // 2
    return sum(a * b for a, b in zip(x[:half], x[half:])) % 2


def majority(x: tuple[int, ...]) -> int:
    return 1 if sum(x) >= (len(x) + 1) // 2 else 0


def parity(x: tuple[int, ...]) -> int:
    return sum(x) % 2


# ---------------------------------------------------------------- ILP

def monomials_up_to(n: int, max_deg: int) -> list[tuple[int, ...]]:
    out = []
    for d in range(max_deg + 1):
        out.extend(itertools.combinations(range(n), d))
    return out


def mono_eval(S: tuple[int, ...], x: tuple[int, ...]) -> int:
    p = 1
    for i in S:
        p *= x[i]
    return p


def min_l1_weight(f, n: int, D: int) -> tuple[str, int | None, int | None]:
    """ Retourne (statut, L1_min, Linf_solution) pour degre <= D. """
    monos = monomials_up_to(n, D)
    prob = pulp.LpProblem("f001_weight", pulp.LpMinimize)
    c = [pulp.LpVariable(f"c{i}", lowBound=-CAP, upBound=CAP, cat="Integer")
         for i in range(len(monos))]
    a = [pulp.LpVariable(f"a{i}", lowBound=0) for i in range(len(monos))]
    for i in range(len(monos)):
        prob += a[i] >= c[i]
        prob += a[i] >= -c[i]
    prob += pulp.lpSum(a)
    for x in itertools.product([0, 1], repeat=n):
        s = pulp.lpSum(c[i] * mono_eval(monos[i], x) for i in range(len(monos)))
        if f(x) == 1:
            prob += s >= 1
        else:
            prob += s <= 0
    solver = pulp.PULP_CBC_CMD(msg=False, timeLimit=TIME_LIMIT)
    status = prob.solve(solver)
    name = pulp.LpStatus[status]
    if name == "Optimal":
        l1 = round(pulp.value(prob.objective))
        linf = max(abs(round(v.value())) for v in c)
        return ("OK", l1, linf)
    if name == "Infeasible":
        return ("INFEASIBLE", None, None)
    return (name.upper(), None, None)


# ---------------------------------------------------------------- main

def main() -> None:
    cases = [
        # (label, n, f, degres a tester)
        ("MAJ", 4, majority, range(0, 5)),
        ("PARITY", 4, parity, range(0, 5)),
        ("EXACT_2", 4, exact_k(2), range(0, 5)),
        ("EXACT_2", 5, exact_k(2), range(0, 6)),
        ("EXACT_3", 6, exact_k(3), range(0, 7)),
        ("IP", 4, inner_product, range(0, 5)),
        ("IP", 6, inner_product, range(0, 7)),
        ("IP", 8, inner_product, range(0, 9)),
    ]

    rows = []
    print("TACHE F-001 -- weight L1 des PTF, TC^0 d=2 \\ d=1")
    print("=" * 76)
    for label, n, f, degs in cases:
        print(f"\n{label}_{n} :")
        for D in degs:
            t0 = time.time()
            statut, l1, linf = min_l1_weight(f, n, D)
            dt = time.time() - t0
            rows.append({"fonction": label, "n": n, "degre": D,
                         "L1_min": l1 if l1 is not None else "",
                         "Linf_solution": linf if linf is not None else "",
                         "statut": statut})
            extra = f"L1={l1}, Linf={linf}" if statut == "OK" else statut
            print(f"  D={D} : {extra}   ({dt:.1f}s)")

    with open("data/weight_tc0_d2.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["fonction", "n", "degre", "L1_min",
                                           "Linf_solution", "statut"])
        w.writeheader()
        w.writerows(rows)
    print("\nCSV ecrit : data/weight_tc0_d2.csv")

    # Synthese sur la question cible
    print("\n" + "=" * 76)
    print("SYNTHESE")
    def first_ok(label, n):
        for r in rows:
            if r["fonction"] == label and r["n"] == n and r["statut"] == "OK":
                return r
        return None
    for label, ns in [("EXACT_2", [4, 5]), ("EXACT_3", [6]), ("IP", [4, 6, 8])]:
        for n in ns:
            r = first_ok(label, n)
            if r:
                print(f"  {label}_{n} : degre min = {r['degre']}, "
                      f"L1 au degre min = {r['L1_min']}")


if __name__ == "__main__":
    main()
