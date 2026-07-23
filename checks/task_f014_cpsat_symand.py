"""
TACHE F-014 -- moteur CP-SAT pour le poids SYM o AND (leve le goulot
big-M de CBC identifie en F-012).

Modele : a_S in [0, 127] entiers sur les 255 monomes positifs ;
p(z) = sum_{S subset z} a_S ; contrainte NATIVE p(z1) != p(z0) pour
toute paire (f=1, f=0) ; minimiser sum a_S.
CP-SAT rapporte a la fois l'incumbent (borne sup) et la meilleure
borne inf PROUVEE, meme en timeout -- exactement ce que F-012 n'avait
pas. Graine : la meilleure solution connue (117 pour XOR(THR4,THR4),
recuit F-013) fournie en hint.

Calibrations integrees : IP_8 (= 4 attendu) et OR(THR4,THR4)
(= 6 attendu, F-012/F-013).
"""

from __future__ import annotations

import itertools
import sys
import time

from ortools.sat.python import cp_model


def battery():
    thr4a = lambda z: 1 if 4 * z[0] + 3 * z[1] + 2 * z[2] + z[3] >= 4 else 0
    thr4b = lambda z: 1 if z[4] + 2 * z[5] + 3 * z[6] + 4 * z[7] >= 4 else 0
    gta = lambda z: 1 if 2 * z[0] + z[1] - 2 * z[2] - z[3] >= 1 else 0
    gtb = lambda z: 1 if 2 * z[4] + z[5] - 2 * z[6] - z[7] >= 1 else 0
    return [
        ("IP_8 (calib=4)", lambda z: (z[0] * z[4] + z[1] * z[5]
                                      + z[2] * z[6] + z[3] * z[7]) % 2,
         None),
        ("OR(THR4,THR4) (calib=6)",
         lambda z: 1 if thr4a(z) + thr4b(z) >= 1 else 0, None),
        ("XOR(THR4,THR4)", lambda z: (thr4a(z) + thr4b(z)) % 2,
         {frozenset([0]): 1, frozenset([4]): 11, frozenset([5]): 22,
          frozenset([6]): 33, frozenset([7]): 44,
          frozenset([1, 2]): 1, frozenset([1, 3]): 1,
          frozenset([6, 7]): 2, frozenset([4, 5, 7]): 2}),
        ("XOR(GT2,GT2)", lambda z: (gta(z) + gtb(z)) % 2,
         {frozenset([0]): 2, frozenset([1]): 1, frozenset([2]): 8,
          frozenset([3]): 4, frozenset([4]): 32, frozenset([5]): 16,
          frozenset([6]): 128, frozenset([7]): 64}),
        ("OR(GT2,GT2)", lambda z: 1 if gta(z) + gtb(z) >= 1 else 0,
         {frozenset([0]): 2, frozenset([1]): 1, frozenset([2]): 8,
          frozenset([3]): 4, frozenset([4]): 32, frozenset([5]): 16,
          frozenset([6]): 128, frozenset([7]): 64}),
        ("AND(GT2,GT2)", lambda z: 1 if gta(z) + gtb(z) >= 2 else 0,
         {frozenset([0]): 2, frozenset([1]): 1, frozenset([2]): 8,
          frozenset([3]): 4, frozenset([4]): 32, frozenset([5]): 16,
          frozenset([6]): 128, frozenset([7]): 64}),
    ]


def solve(f, n=8, hint=None, tl=300.0, workers=8, ub=127):
    inputs = list(itertools.product((0, 1), repeat=n))
    ones = [z for z in inputs if f(z) == 1]
    zeros = [z for z in inputs if f(z) == 0]
    monos = []
    for d in range(1, n + 1):
        monos.extend(frozenset(c)
                     for c in itertools.combinations(range(n), d))

    m = cp_model.CpModel()
    a = {S: m.new_int_var(0, ub, f"a{i}")
         for i, S in enumerate(monos)}
    pvals = {}
    for z in inputs:
        supp = frozenset(j for j in range(n) if z[j])
        terms = [a[S] for S in monos if S <= supp]
        v = m.new_int_var(0, ub * len(monos), f"p{z}")
        m.add(v == sum(terms) if terms else v == 0)
        pvals[z] = v
    for z1 in ones:
        for z0 in zeros:
            m.add(pvals[z1] != pvals[z0])
    m.minimize(sum(a.values()))
    if hint:
        for S, val in hint.items():
            m.add_hint(a[S], val)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tl
    solver.parameters.num_workers = workers
    st = solver.solve(m)
    name = solver.status_name(st)
    inc = (round(solver.objective_value)
           if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None)
    lb = round(solver.best_objective_bound)
    sol = None
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        sol = {S: solver.value(a[S]) for S in monos
               if solver.value(a[S]) > 0}
    return name, inc, lb, sol


def verify(f, n, sol):
    """Re-verification independante par enumeration."""
    ones_v, zeros_v = set(), set()
    for z in itertools.product((0, 1), repeat=n):
        supp = frozenset(j for j in range(n) if z[j])
        p = sum(v for S, v in sol.items() if S <= supp)
        (ones_v if f(z) else zeros_v).add(p)
    return not (ones_v & zeros_v)


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    tl = float(sys.argv[2]) if len(sys.argv) > 2 else 300.0
    for label, f, hint in battery():
        if only and not label.startswith(only):
            continue
        t0 = time.time()
        name, inc, lb, sol = solve(f, hint=hint, tl=tl)
        dt = time.time() - t0
        ver = ""
        if sol is not None:
            ok = verify(f, 8, sol)
            ver = " [re-verif OK]" if ok else " [RE-VERIF ECHEC !]"
        print(f"  {label:<26} : statut {name}, "
              f"incumbent = {inc}, borne inf prouvee = {lb}"
              f"{ver}  ({dt:.0f}s)", flush=True)
        if sol is not None and name == "OPTIMAL":
            supp = ", ".join(
                f"{sorted(S)}:{v}" for S, v in
                sorted(sol.items(), key=lambda kv: (len(kv[0]),
                                                    sorted(kv[0]))))
            print(f"      support : {supp}", flush=True)


if __name__ == "__main__":
    main()
