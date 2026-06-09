"""
TACHE F-003' -- Poids SYM o AND minimal de fonctions a 2 etages de seuils.

Contexte (F-003) : les objets-frontiere de l'extension Williams -> TC^0
sont les compositions de seuils a poids (THR o THR et apparentes), pas IP
(trivial en SYM o AND). Ce script mesure le poids SYM o AND minimal d'une
batterie de telles compositions a n = 4 et n = 6.

Modele (identique a F-003) : p(z) = sum_S a_S m_S(z), a_S entiers >= 0,
monomes positifs ; f representable ssi les ensembles de valeurs
{p(z) : f=1} et {p(z) : f=0} sont disjoints. Poids = sum a_S.
ILP a indicateurs de paires (big-M), time limit honnete par instance.

ATTENTION D'INTERPRETATION : a n = 4..6 on ne voit PAS d'asymptotique --
c'est un premier point de donnees + un instrument, rien de plus.
Reperes : toute fonction SYMETRIQUE a poids <= n (p = somme z_i) ;
l'encodage binaire injectif donne poids <= 2^n - 1 pour n'importe quoi.
"""

from __future__ import annotations

import csv
import itertools
import time

import pulp


def thr(weights, t):
    def f(z):
        return 1 if sum(w * z[i] for i, w in enumerate(weights)) >= t else 0
    return f


def make_battery():
    """ Retourne [(label, n, fonction)] """
    battery = []

    # ---- n = 4 : blocs de 2 variables ----
    h1 = lambda z: 1 if 2 * z[0] + z[1] >= 2 else 0
    h2 = lambda z: 1 if z[2] + 2 * z[3] >= 2 else 0
    battery.append(("OR(THR,THR)", 4, lambda z: 1 if h1(z) + h2(z) >= 1 else 0))
    battery.append(("AND(THR,THR)", 4, lambda z: 1 if h1(z) + h2(z) >= 2 else 0))
    battery.append(("XOR(THR,THR)", 4, lambda z: (h1(z) + h2(z)) % 2))

    # ---- n = 6 : blocs de 3 variables, poids 3,2,1 ----
    g1 = lambda z: 1 if 3 * z[0] + 2 * z[1] + z[2] >= 3 else 0
    g2 = lambda z: 1 if z[3] + 2 * z[4] + 3 * z[5] >= 3 else 0
    battery.append(("OR(THR3,THR3)", 6, lambda z: 1 if g1(z) + g2(z) >= 1 else 0))
    battery.append(("XOR(THR3,THR3)", 6, lambda z: (g1(z) + g2(z)) % 2))

    # ---- n = 6 : MAJ de trois seuils sur blocs de 2 ----
    e1 = lambda z: 1 if 2 * z[0] + z[1] >= 2 else 0
    e2 = lambda z: 1 if 2 * z[2] + z[3] >= 2 else 0
    e3 = lambda z: 1 if 2 * z[4] + z[5] >= 2 else 0
    battery.append(("MAJ3(THR,THR,THR)", 6,
                    lambda z: 1 if e1(z) + e2(z) + e3(z) >= 2 else 0))

    # ---- calibration : IP_6 (= 3 attendu, F-003) ----
    battery.append(("IP_6 (calibration)", 6,
                    lambda z: (z[0] * z[3] + z[1] * z[4] + z[2] * z[5]) % 2))

    return battery


def min_symand_weight(f, n: int, U: int = 12, tl: int = 240):
    inputs = list(itertools.product([0, 1], repeat=n))
    ones = [z for z in inputs if f(z) == 1]
    zeros = [z for z in inputs if f(z) == 0]
    monos = []
    for d in range(1, n + 1):
        monos.extend(itertools.combinations(range(n), d))
    M = U * len(monos) + 1

    prob = pulp.LpProblem("symand", pulp.LpMinimize)
    a = [pulp.LpVariable(f"a{i}", lowBound=0, upBound=U, cat="Integer")
         for i in range(len(monos))]
    prob += pulp.lpSum(a)

    pcache = {}
    def p_expr(z):
        if z not in pcache:
            pcache[z] = pulp.lpSum(a[i] for i in range(len(monos))
                                   if all(z[j] for j in monos[i]))
        return pcache[z]

    for i1, z1 in enumerate(ones):
        for i0, z0 in enumerate(zeros):
            b = pulp.LpVariable(f"b_{i1}_{i0}", cat="Binary")
            prob += p_expr(z1) - p_expr(z0) >= 1 - M * b
            prob += p_expr(z0) - p_expr(z1) >= 1 - M * (1 - b)

    status = prob.solve(pulp.PULP_CBC_CMD(msg=False, timeLimit=tl))
    name = pulp.LpStatus[status]
    obj = pulp.value(prob.objective)
    return (round(obj) if obj is not None else None), name


def main() -> None:
    print("TACHE F-003' -- poids SYM o AND de compositions de seuils")
    print("=" * 70)
    rows = []
    for label, n, f in make_battery():
        ones = sum(1 for z in itertools.product([0, 1], repeat=n) if f(z) == 1)
        t0 = time.time()
        w, st = min_symand_weight(f, n)
        dt = time.time() - t0
        note = ""
        if st != "Optimal":
            note = f" [statut {st} -- valeur = borne courante, PAS l'optimum]"
        print(f"  {label:<22} (n={n}, |f^-1(1)|={ones:>2}) : "
              f"poids = {w}{note}   ({dt:.0f}s)")
        rows.append({"fonction": label, "n": n, "ones": ones,
                     "poids": w if w is not None else "", "statut": st,
                     "temps_s": round(dt)})

    with open("data/symand_thrthr.csv", "w", newline="", encoding="utf-8") as fh:
        wcsv = csv.DictWriter(fh, fieldnames=["fonction", "n", "ones",
                                              "poids", "statut", "temps_s"])
        wcsv.writeheader()
        wcsv.writerows(rows)
    print("\nCSV : data/symand_thrthr.csv")
    print("\nReperes : symetrique => poids <= n ; injectif => <= 2^n - 1.")
    print("n = 4..6 : premier point de donnees, AUCUNE asymptotique visible.")


if __name__ == "__main__":
    main()
