"""
TACHE F-002 -- Test de l'observation conjecturale de F-001 au point suivant.

Observation (F-001, 3 points) : min_D W_L1(IP_{2k}, D) = (3^k - 1)/2
  k=2 (n=4)  : 4   = (3^2-1)/2
  k=3 (n=6)  : 13  = (3^3-1)/2
  k=4 (n=8)  : 40  = (3^4-1)/2
C'est exactement DNF_min(IP_{2k}) (Tours 17-18, L18).

CE TEST (condition r, 4e point) : k=5, n=10.
  Prediction : min_D W_L1(IP_10, D) = (3^5-1)/2 = 121.

Comme W(f, D) est non-croissante en D (ajouter des monomes ne peut
qu'aider), le minimum sur D est atteint a D = n. On calcule donc
W_L1(IP_10, 10) -- ILP a 1024 monomes (tous les sous-ensembles),
2048 variables (c_S + |c_S|), 1024 contraintes.

On calcule aussi D=8, 9 pour le profil (le min est-il deja atteint
avant le degre plein ?).

Honnetete : si CBC ne prouve pas l'optimalite dans le temps imparti,
rapporter le statut exact (incumbent + borne), ne pas conclure.
"""

from __future__ import annotations

import csv
import itertools
import time

import pulp

CAP = 100_000
TIME_LIMIT = 540  # secondes par solve


def inner_product(x: tuple[int, ...]) -> int:
    n = len(x)
    half = n // 2
    return sum(a * b for a, b in zip(x[:half], x[half:])) % 2


def monomials_up_to(n: int, max_deg: int):
    out = []
    for d in range(max_deg + 1):
        out.extend(itertools.combinations(range(n), d))
    return out


def mono_eval(S, x) -> int:
    p = 1
    for i in S:
        p *= x[i]
    return p


def min_l1(n: int, D: int):
    monos = monomials_up_to(n, D)
    prob = pulp.LpProblem("f002", pulp.LpMinimize)
    c = [pulp.LpVariable(f"c{i}", lowBound=-CAP, upBound=CAP, cat="Integer")
         for i in range(len(monos))]
    a = [pulp.LpVariable(f"a{i}", lowBound=0) for i in range(len(monos))]
    for i in range(len(monos)):
        prob += a[i] >= c[i]
        prob += a[i] >= -c[i]
    prob += pulp.lpSum(a)
    for x in itertools.product([0, 1], repeat=n):
        s = pulp.lpSum(c[i] * mono_eval(monos[i], x) for i in range(len(monos)))
        if inner_product(x) == 1:
            prob += s >= 1
        else:
            prob += s <= 0
    solver = pulp.PULP_CBC_CMD(msg=False, timeLimit=TIME_LIMIT)
    status = prob.solve(solver)
    name = pulp.LpStatus[status]
    obj = pulp.value(prob.objective)
    return name, (round(obj) if obj is not None else None), len(monos)


def main() -> None:
    n = 10
    print("TACHE F-002 -- min_D W_L1(IP_10, D), prediction 121 = (3^5-1)/2")
    print("=" * 72)
    rows = []
    for D in [10, 9, 8]:
        t0 = time.time()
        statut, l1, nmonos = min_l1(n, D)
        dt = time.time() - t0
        rows.append({"n": n, "degre": D, "L1": l1 if l1 is not None else "",
                     "statut": statut, "monomes": nmonos,
                     "temps_s": round(dt, 1)})
        print(f"  D={D} ({nmonos} monomes) : statut={statut}, L1={l1}   ({dt:.1f}s)")

    with open("data/weight_ip_k5.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["n", "degre", "L1", "statut",
                                           "monomes", "temps_s"])
        w.writeheader()
        w.writerows(rows)
    print("\nCSV : data/weight_ip_k5.csv")

    full = next(r for r in rows if r["degre"] == 10)
    print("\n" + "=" * 72)
    if full["statut"] == "Optimal":
        if full["L1"] == 121:
            print("VERDICT : prediction CONFIRMEE -- min_D W(IP_10) = 121 = (3^5-1)/2.")
            print("4 points consecutifs (4, 13, 40, 121). Reste une observation")
            print("(pas un theoreme) tant que la preuve structurelle manque.")
        else:
            print(f"VERDICT : prediction REFUTEE -- L1 = {full['L1']} != 121.")
            print("Le pattern (3^k-1)/2 casse au 4e point (cf. q.12 du cahier).")
    else:
        print(f"VERDICT : NON CONCLUSIF -- statut CBC = {full['statut']}.")
        print("Ne pas conclure ; rapporter tel quel (regle 5, honest failure).")


if __name__ == "__main__":
    main()
