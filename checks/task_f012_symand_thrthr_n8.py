"""
TACHE F-012 -- Chasse au mur THR o THR a n = 8 (prolonge F-003').

Modele identique a F-003/F-003' : p(z) = sum_S a_S m_S(z), a_S entiers
>= 0 sur monomes positifs ; f representable en SYM o AND ssi les
ensembles de valeurs {p : f=1} et {p : f=0} sont disjoints.
Poids = sum a_S. ILP a indicateurs de paires (big-M).

Nouveautes vs F-003' :
  1. NON-DEGENERESCENCE VERIFIEE PROGRAMMATIQUEMENT (lecon F-003') :
     chaque bloc interne doit dependre de TOUTES ses variables.
  2. Instances GT (comparaison, poids +-) : la classe exacte ou la
     transformation Beigel-Tarui echoue (poids non bornes, non
     monotones) -- le vrai objet-frontiere de la ligne 7.
  3. n = 8 : 256 points, ~16k paires -- timeLimit 600 s/instance,
     statut honnete (borne courante si non Optimal).

Reperes : f symetrique => poids <= n ; encodage injectif => <= 2^n - 1.
A n = 6 (F-003') : XOR(THR3,THR3) = 6 = n, OR = 4 -- lineaire.
La question de F-012 : a n = 8, ~n ou decollage ?
"""

from __future__ import annotations

import csv
import itertools
import time

import pulp


def depends_on_all(f, n):
    """La fonction depend-elle de chacune de ses n variables ?"""
    inputs = list(itertools.product([0, 1], repeat=n))
    for i in range(n):
        if all(f(z) == f(tuple(b if j != i else 1 - b
                               for j, (b) in enumerate(z)))
               for z in inputs):
            return False
    return True


def make_battery():
    """[(label, n, f)] -- tous verifies non-degeneres avant mesure."""
    battery = []

    # blocs monotones 4 vars : g(z) = [4z1+3z2+2z3+z4 >= 4]
    thr4a = lambda z: 1 if 4 * z[0] + 3 * z[1] + 2 * z[2] + z[3] >= 4 else 0
    thr4b = lambda z: 1 if z[4] + 2 * z[5] + 3 * z[6] + 4 * z[7] >= 4 else 0
    battery.append(("XOR(THR4,THR4)", 8,
                    lambda z: (thr4a(z) + thr4b(z)) % 2))
    battery.append(("OR(THR4,THR4)", 8,
                    lambda z: 1 if thr4a(z) + thr4b(z) >= 1 else 0))

    # blocs GT (comparaison 2 bits vs 2 bits, poids +-) :
    # g(x1x2, y1y2) = [2x1+x2 - 2y1-y2 >= 1]
    gta = lambda z: 1 if 2 * z[0] + z[1] - 2 * z[2] - z[3] >= 1 else 0
    gtb = lambda z: 1 if 2 * z[4] + z[5] - 2 * z[6] - z[7] >= 1 else 0
    battery.append(("XOR(GT2,GT2)", 8, lambda z: (gta(z) + gtb(z)) % 2))
    battery.append(("OR(GT2,GT2)", 8,
                    lambda z: 1 if gta(z) + gtb(z) >= 1 else 0))
    battery.append(("AND(GT2,GT2)", 8,
                    lambda z: 1 if gta(z) + gtb(z) >= 2 else 0))

    # calibration : IP_8 (= PARITY o AND_2, poids 4 attendu, F-003)
    battery.append(("IP_8 (calibration)", 8,
                    lambda z: (z[0] * z[4] + z[1] * z[5] + z[2] * z[6]
                               + z[3] * z[7]) % 2))
    return battery


def min_symand_weight(f, n, U=16, tl=90):
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


def main():
    import sys
    only = sys.argv[1] if len(sys.argv) > 1 else None
    tl = int(sys.argv[2]) if len(sys.argv) > 2 else 90
    U = int(sys.argv[3]) if len(sys.argv) > 3 else 16
    print("TACHE F-012 -- chasse au mur THR o THR a n = 8"
          + (f" [instance {only}, tl={tl}s]" if only else ""))
    print("=" * 70)
    # verification de non-degenerescence des blocs internes
    thr4 = lambda z: 1 if 4 * z[0] + 3 * z[1] + 2 * z[2] + z[3] >= 4 else 0
    gt2 = lambda z: 1 if 2 * z[0] + z[1] - 2 * z[2] - z[3] >= 1 else 0
    for name, g in [("THR4", thr4), ("GT2", gt2)]:
        ok = depends_on_all(g, 4)
        print(f"  bloc {name} : depend de ses 4 variables -- "
              f"{'OK' if ok else 'DEGENERE (ABANDON)'}")
        if not ok:
            return
    print()

    rows = []
    for label, n, f in make_battery():
        if only and not label.startswith(only):
            continue
        assert depends_on_all(f, n), f"{label} degeneree"
        ones = sum(1 for z in itertools.product([0, 1], repeat=n)
                   if f(z) == 1)
        t0 = time.time()
        w, st = min_symand_weight(f, n, U=U, tl=tl)
        dt = time.time() - t0
        note = ("" if st == "Optimal" else
                f" [statut {st} -- borne courante, PAS l'optimum]")
        print(f"  {label:<20} (n={n}, |f^-1(1)|={ones:>3}) : "
              f"poids = {w}{note}   ({dt:.0f}s)", flush=True)
        rows.append({"fonction": label, "n": n, "ones": ones,
                     "poids": w if w is not None else "", "statut": st,
                     "temps_s": round(dt)})

    suffix = ("_" + only.replace("(", "_").replace(")", "").replace(
        ",", "_") if only else "")
    with open(f"data/symand_thrthr_n8{suffix}.csv", "w", newline="",
              encoding="utf-8") as fh:
        wcsv = csv.DictWriter(fh, fieldnames=["fonction", "n", "ones",
                                              "poids", "statut",
                                              "temps_s"])
        wcsv.writeheader()
        wcsv.writerows(rows)
    print("\nCSV : data/symand_thrthr_n8.csv")
    print("Reperes : symetrique => <= n ; injectif => <= 2^n - 1 = 255.")


if __name__ == "__main__":
    main()
