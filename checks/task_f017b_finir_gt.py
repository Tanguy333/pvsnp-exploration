"""
TACHE F-017 (reprise b) -- FINIR les 2 fenetres GT.

Ajouts vs task_f017 :
  - COUPES PROUVEES (theoreme de tranche F-013, W(GT2) = 7 exact) :
      OR  : masse(S in A) >= 7 et masse(S in B) >= 7
            (tranches z_B = 0 / z_A = 0, OR(g,0) = g) ;
      AND : masse(S in A u {4}) >= 7, A u {5}, B u {0}, B u {1}
            (tranches a g_B = 1 : AND(g_A, 1) = g_A ; temoins
            b* = e_4 (2 >= 1) et e_5 (1 >= 1)).
  - domaines reduits : a_S <= cap.
  - callback : imprime chaque nouvel incumbent (trace utilisable
    meme si le run est tue).
argv : [OR|AND] [tl]
"""

from __future__ import annotations

import itertools
import sys
import time

from ortools.sat.python import cp_model
from task_f017_fermer_gt import GTA, GTB, HINT_AND, fs

# incumbent 36 de F-017 (re-verifie) — le hint 37 violerait le plafond
HINT_OR36 = {fs(0): 1, fs(1): 1, fs(4): 1, fs(5): 1,
             fs(0, 2): 2, fs(1, 2): 2, fs(1, 3): 2, fs(4, 6): 2,
             fs(5, 6): 2, fs(5, 7): 2,
             fs(0, 1, 4): 1, fs(0, 1, 5): 1, fs(0, 4, 5): 1,
             fs(1, 4, 5): 1, fs(0, 1, 2, 3): 2, fs(0, 1, 4, 5): 3,
             fs(0, 2, 4, 6): 1, fs(0, 2, 5, 6): 1, fs(0, 2, 5, 7): 1,
             fs(1, 2, 4, 6): 1, fs(1, 2, 5, 6): 1, fs(1, 2, 5, 7): 1,
             fs(1, 3, 4, 6): 1, fs(1, 3, 5, 6): 1, fs(1, 3, 5, 7): 1,
             fs(4, 5, 6, 7): 2}


class Printer(cp_model.CpSolverSolutionCallback):
    def __init__(self, total):
        super().__init__()
        self.total = total
        self.t0 = time.time()

    def on_solution_callback(self):
        print(f"    incumbent {round(self.value(self.total))} "
              f"a {time.time()-self.t0:.0f}s", flush=True)


def main():
    which = sys.argv[1]
    tl = float(sys.argv[2]) if len(sys.argv) > 2 else 3000.0
    if which == "OR":
        f = lambda z: 1 if GTA(z) + GTB(z) >= 1 else 0
        cap, hint = 36, HINT_OR36
    else:
        f = lambda z: 1 if GTA(z) + GTB(z) >= 2 else 0
        cap, hint = 38, HINT_AND

    n = 8
    inputs = list(itertools.product((0, 1), repeat=n))
    ones = [z for z in inputs if f(z)]
    zeros = [z for z in inputs if not f(z)]
    monos = []
    for d in range(1, n + 1):
        monos.extend(frozenset(c)
                     for c in itertools.combinations(range(n), d))
    m = cp_model.CpModel()
    a = {S: m.new_int_var(0, cap, f"a{i}") for i, S in enumerate(monos)}
    pv = {}
    for z in inputs:
        supp = frozenset(j for j in range(n) if z[j])
        t = [a[S] for S in monos if S <= supp]
        v = m.new_int_var(0, cap * 4, f"q{z}")
        m.add(v == sum(t) if t else v == 0)
        pv[z] = v
    for z1 in ones:
        for z0 in zeros:
            m.add(pv[z1] != pv[z0])
    total = sum(a.values())
    m.add(total <= cap)
    A4 = frozenset([0, 1, 2, 3])
    B4 = frozenset([4, 5, 6, 7])
    massA = sum(a[S] for S in monos if S <= A4)
    massB = sum(a[S] for S in monos if S <= B4)
    m.add(massA <= massB)
    if which == "OR":
        m.add(massA >= 7)
        m.add(massB >= 7)
    else:
        for cut in [A4 | {4}, A4 | {5}, B4 | {0}, B4 | {1}]:
            m.add(sum(a[S] for S in monos if S <= cut) >= 7)
    m.minimize(total)
    for S in monos:
        m.add_hint(a[S], min(hint.get(S, 0), cap))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tl
    solver.parameters.num_workers = 8
    cb = Printer(total)
    t0 = time.time()
    st = solver.solve(m, cb)
    name = solver.status_name(st)
    inc = (round(solver.objective_value)
           if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None)
    lb = round(solver.best_objective_bound)
    ver = ""
    if inc is not None:
        sol = {S: solver.value(a[S]) for S in monos
               if solver.value(a[S]) > 0}
        ones_v, zeros_v = set(), set()
        for z in inputs:
            supp = frozenset(j for j in range(n) if z[j])
            p = sum(v for S, v in sol.items() if S <= supp)
            (ones_v if f(z) else zeros_v).add(p)
        ok = not (ones_v & zeros_v)
        ver = " [re-verif OK]" if ok else " [RE-VERIF ECHEC !]"
        print("    support : " + ", ".join(
            f"{sorted(S)}:{v}" for S, v in sorted(
                sol.items(), key=lambda kv: (len(kv[0]), sorted(kv[0])))))
    print(f"  {which}(GT2,GT2) : statut {name}, incumbent = {inc}, "
          f"borne inf = {lb}{ver}  ({time.time()-t0:.0f}s)", flush=True)


if __name__ == "__main__":
    main()
