"""
TACHE F-015 -- trancher XOR(THR4,THR4) in [13, 117].

Trois modes (argv[1]) :
  opt      : minimiser sum(a), hint COMPLET (les 255 valeurs -- le
             hint partiel de F-014 n'avait pas pris), plafond
             sum(a) <= 117, cassage de symetrie bloc-miroir
             (pi : 0<->7, 1<->6, 2<->5, 3<->4 laisse f invariante ;
             on impose masse(A) <= masse(B)).
  dec W    : DECISION pure -- existe-t-il une solution sum(a) <= W ?
             INFEASIBLE prouve => borne inf = W+1.
argv[2] = time limit (s).
"""

from __future__ import annotations

import itertools
import sys
import time

from ortools.sat.python import cp_model

THR4A = lambda z: 1 if 4 * z[0] + 3 * z[1] + 2 * z[2] + z[3] >= 4 else 0
THR4B = lambda z: 1 if z[4] + 2 * z[5] + 3 * z[6] + 4 * z[7] >= 4 else 0
F = lambda z: (THR4A(z) + THR4B(z)) % 2

HINT117 = {frozenset([0]): 1, frozenset([4]): 11, frozenset([5]): 22,
           frozenset([6]): 33, frozenset([7]): 44,
           frozenset([1, 2]): 1, frozenset([1, 3]): 1,
           frozenset([6, 7]): 2, frozenset([4, 5, 7]): 2}


def build(mode, W=None, symbreak=True, ub=127):
    n = 8
    inputs = list(itertools.product((0, 1), repeat=n))
    ones = [z for z in inputs if F(z) == 1]
    zeros = [z for z in inputs if F(z) == 0]
    monos = []
    for d in range(1, n + 1):
        monos.extend(frozenset(c)
                     for c in itertools.combinations(range(n), d))
    m = cp_model.CpModel()
    a = {S: m.new_int_var(0, ub, f"a{i}") for i, S in enumerate(monos)}
    pvals = {}
    for z in inputs:
        supp = frozenset(j for j in range(n) if z[j])
        terms = [a[S] for S in monos if S <= supp]
        v = m.new_int_var(0, ub * len(monos), f"q{z}")
        m.add(v == sum(terms) if terms else v == 0)
        pvals[z] = v
    for z1 in ones:
        for z0 in zeros:
            m.add(pvals[z1] != pvals[z0])

    total = sum(a.values())
    if mode == "opt":
        m.add(total <= 117)
        m.minimize(total)
        # hint COMPLET (255 valeurs, 0 hors support)
        for S in monos:
            m.add_hint(a[S], HINT117.get(S, 0))
        if symbreak:
            # pi : bloc-miroir ; imposer masse(S dans A) <= masse(S dans B)
            massA = sum(a[S] for S in monos
                        if S <= frozenset([0, 1, 2, 3]))
            massB = sum(a[S] for S in monos
                        if S <= frozenset([4, 5, 6, 7]))
            m.add(massA <= massB)
    else:
        m.add(total <= W)
    return m, a, monos


def verify(sol):
    ones_v, zeros_v = set(), set()
    for z in itertools.product((0, 1), repeat=8):
        supp = frozenset(j for j in range(8) if z[j])
        p = sum(v for S, v in sol.items() if S <= supp)
        (ones_v if F(z) else zeros_v).add(p)
    return not (ones_v & zeros_v)


def main():
    mode = sys.argv[1]
    if mode == "dec":
        W = int(sys.argv[2])
        tl = float(sys.argv[3]) if len(sys.argv) > 3 else 540.0
    else:
        W = None
        tl = float(sys.argv[2]) if len(sys.argv) > 2 else 540.0

    m, a, monos = build(mode, W)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tl
    solver.parameters.num_workers = 8
    t0 = time.time()
    st = solver.solve(m)
    name = solver.status_name(st)
    dt = time.time() - t0

    if mode == "opt":
        inc = (round(solver.objective_value)
               if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None)
        lb = round(solver.best_objective_bound)
        ver = ""
        if inc is not None:
            sol = {S: solver.value(a[S]) for S in monos
                   if solver.value(a[S]) > 0}
            ver = " [re-verif OK]" if verify(sol) else " [ECHEC!]"
            if st == cp_model.OPTIMAL or inc < 117:
                print(f"    support : " + ", ".join(
                    f"{sorted(S)}:{v}" for S, v in sorted(
                        sol.items(), key=lambda kv: (len(kv[0]),
                                                     sorted(kv[0])))))
        print(f"  OPT : statut {name}, incumbent = {inc}, "
              f"borne inf = {lb}{ver}  ({dt:.0f}s)")
    else:
        verdict = {"INFEASIBLE": f"AUCUNE solution <= {W} : "
                                 f"BORNE INF PROUVEE = {W + 1}",
                   "FEASIBLE": f"solution <= {W} TROUVEE",
                   "OPTIMAL": f"solution <= {W} TROUVEE",
                   "UNKNOWN": f"indecis a W = {W}"}[name]
        ver = ""
        if name in ("FEASIBLE", "OPTIMAL"):
            sol = {S: solver.value(a[S]) for S in monos
                   if solver.value(a[S]) > 0}
            w = sum(sol.values())
            ver = (f" poids {w}" +
                   (" [re-verif OK]" if verify(sol) else " [ECHEC!]"))
            print(f"    support : " + ", ".join(
                f"{sorted(S)}:{v}" for S, v in sorted(
                    sol.items(), key=lambda kv: (len(kv[0]),
                                                 sorted(kv[0])))))
        print(f"  DEC({W}) : statut {name} -- {verdict}{ver}  ({dt:.0f}s)")


if __name__ == "__main__":
    main()
