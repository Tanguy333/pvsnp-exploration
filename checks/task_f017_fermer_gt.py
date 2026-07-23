"""
TACHE F-017 -- fermer les 2 dernieres fenetres de la batterie n = 8 :
OR(GT2,GT2) in [22, 37] et AND(GT2,GT2) in [19, 38].

Recette F-015 complete : plafond = incumbent connu (37/38), hint
COMPLET (les supports re-verifies de F-015b), cassage de symetrie
bloc-miroir (0<->4, 1<->5, 2<->6, 3<->7), re-verification independante
par enumeration (lecon F-016 : OBLIGATOIRE).
argv : [OR|AND] [tl]
"""

from __future__ import annotations

import itertools
import sys
import time

from ortools.sat.python import cp_model

GTA = lambda z: 1 if 2 * z[0] + z[1] - 2 * z[2] - z[3] >= 1 else 0
GTB = lambda z: 1 if 2 * z[4] + z[5] - 2 * z[6] - z[7] >= 1 else 0


def fs(*idx):
    return frozenset(idx)


HINT_OR = {fs(0): 1, fs(1): 1, fs(4): 1, fs(5): 1,
           fs(0, 2): 2, fs(1, 2): 2, fs(1, 3): 2, fs(4, 6): 2,
           fs(5, 6): 2, fs(5, 7): 2,
           fs(0, 1, 4): 1, fs(0, 1, 5): 1, fs(0, 4, 5): 1,
           fs(1, 4, 5): 1,
           fs(0, 1, 2, 4): 1, fs(0, 1, 2, 5): 1, fs(0, 1, 4, 5): 1,
           fs(0, 2, 4, 6): 1, fs(0, 2, 5, 6): 1, fs(0, 2, 5, 7): 1,
           fs(0, 4, 5, 6): 1, fs(1, 2, 4, 6): 1, fs(1, 2, 5, 6): 1,
           fs(1, 2, 5, 7): 1, fs(1, 3, 4, 6): 1, fs(1, 3, 5, 6): 1,
           fs(1, 3, 5, 7): 1, fs(1, 4, 5, 6): 1,
           fs(0, 1, 5, 6, 7): 1, fs(1, 2, 3, 4, 5): 1,
           fs(0, 1, 3, 4, 5, 7): 1}

HINT_AND = {fs(0, 4): 1, fs(0, 5): 1, fs(1, 4): 1, fs(1, 5): 1,
            fs(0, 2, 4): 2, fs(0, 2, 5): 2, fs(0, 4, 6): 2,
            fs(0, 5, 6): 2, fs(0, 5, 7): 2, fs(1, 2, 4): 2,
            fs(1, 2, 5): 2, fs(1, 3, 4): 2, fs(1, 3, 5): 2,
            fs(1, 4, 6): 2, fs(1, 5, 6): 2, fs(1, 5, 7): 2,
            fs(0, 1, 4, 6): 1, fs(0, 1, 5, 6): 1, fs(0, 1, 5, 7): 1,
            fs(0, 2, 4, 5): 1, fs(1, 2, 4, 5): 1, fs(1, 3, 4, 5): 1,
            fs(0, 1, 3, 4, 5): 1, fs(0, 1, 4, 5, 7): 1,
            fs(0, 1, 5, 6, 7): 1, fs(1, 2, 3, 4, 5): 1}


def main():
    which = sys.argv[1]
    tl = float(sys.argv[2]) if len(sys.argv) > 2 else 540.0
    if which == "OR":
        f = lambda z: 1 if GTA(z) + GTB(z) >= 1 else 0
        cap, hint = 37, HINT_OR
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
    a = {S: m.new_int_var(0, 127, f"a{i}") for i, S in enumerate(monos)}
    pvals = {}
    for z in inputs:
        supp = frozenset(j for j in range(n) if z[j])
        terms = [a[S] for S in monos if S <= supp]
        v = m.new_int_var(0, 127 * len(monos), f"q{z}")
        m.add(v == sum(terms) if terms else v == 0)
        pvals[z] = v
    for z1 in ones:
        for z0 in zeros:
            m.add(pvals[z1] != pvals[z0])
    total = sum(a.values())
    m.add(total <= cap)
    massA = sum(a[S] for S in monos if S <= frozenset([0, 1, 2, 3]))
    massB = sum(a[S] for S in monos if S <= frozenset([4, 5, 6, 7]))
    m.add(massA <= massB)
    m.minimize(total)
    for S in monos:
        m.add_hint(a[S], hint.get(S, 0))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tl
    solver.parameters.num_workers = 8
    t0 = time.time()
    st = solver.solve(m)
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
          f"borne inf = {lb}{ver}  ({time.time()-t0:.0f}s)")


if __name__ == "__main__":
    main()
