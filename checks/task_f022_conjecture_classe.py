"""
TACHE F-022 -- la conjecture de classe : refuter d'abord, prouver
ensuite (ordre du Refuteur).

(0) L'enonce litteral est FAUX : MAJ_5 sur blocs singletons est une
    composition monotone a blocs disjoints, W = 5 < 10 = couvert.
    -> la classe doit exiger des blocs NON TRIVIAUX (>= 2 variables).
(1) Chasse au contre-exemple sur blocs non triviaux : grille h o g,
    h externe in {OR2, AND2, MAJ3}, g bloc in {OR2, AND2, MAJ3, THR3},
    n <= 8 (+ temoins n = 9 en tl court). Pour chaque cellule :
      - W exact (CP-SAT, statut honnete),
      - couvert unilateral exact (set cover ILP : min # de
        monomes-uns couvrant les uns minimaux),
      - verdict : EGAL (pro-conjecture) / W < couvert (CONTRE-EXEMPLE).
"""

from __future__ import annotations

import itertools
import sys
import time

import pulp
from ortools.sat.python import cp_model


def cover_number(f, n, tl=60):
    """Couvert unilateral exact : min # monomes S avec f(1_S) = 1
    couvrant tous les uns minimaux (ILP)."""
    inputs = list(itertools.product((0, 1), repeat=n))
    ones = [z for z in inputs if f(z)]
    min_ones = [z for z in ones
                if all(not f(tuple(b if j != i else 0
                                   for j, b in enumerate(z)))
                       for i in range(n) if z[i])]
    one_monos = []
    for d in range(1, n + 1):
        for c in itertools.combinations(range(n), d):
            S = frozenset(c)
            zS = tuple(1 if j in S else 0 for j in range(n))
            if f(zS):
                one_monos.append(S)
    prob = pulp.LpProblem("cover", pulp.LpMinimize)
    x = {S: pulp.LpVariable(f"x{i}", cat="Binary")
         for i, S in enumerate(one_monos)}
    prob += pulp.lpSum(x.values())
    for z in min_ones:
        supp = frozenset(j for j in range(n) if z[j])
        prob += pulp.lpSum(x[S] for S in one_monos if S <= supp) >= 1
    prob.solve(pulp.PULP_CBC_CMD(msg=False, timeLimit=tl))
    return round(pulp.value(prob.objective)), len(min_ones)


def w_exact(f, n, cap, tl=180):
    inputs = list(itertools.product((0, 1), repeat=n))
    ones = [z for z in inputs if f(z)]
    zeros = [z for z in inputs if not f(z)]
    monos = []
    for d in range(1, n + 1):
        monos.extend(frozenset(c)
                     for c in itertools.combinations(range(n), d))
    m = cp_model.CpModel()
    a = {S: m.new_int_var(0, cap, str(i)) for i, S in enumerate(monos)}
    pv = {}
    for z in inputs:
        supp = frozenset(j for j in range(n) if z[j])
        t = [a[S] for S in monos if S <= supp]
        v = m.new_int_var(0, cap * 4, "q" + str(z))
        m.add(v == sum(t) if t else v == 0)
        pv[z] = v
    for z1 in ones:
        for z0 in zeros:
            m.add(pv[z1] != pv[z0])
    m.add(sum(a.values()) <= cap)
    m.minimize(sum(a.values()))
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = tl
    s.parameters.num_workers = 8
    st = s.solve(m)
    inc = (round(s.objective_value)
           if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None)
    ok = None
    if inc is not None:
        sol = {S: s.value(a[S]) for S in monos if s.value(a[S]) > 0}
        ov, zv = set(), set()
        for z in inputs:
            supp = frozenset(j for j in range(n) if z[j])
            p = sum(v for S, v in sol.items() if S <= supp)
            (ov if f(z) else zv).add(p)
        ok = not (ov & zv)
    return s.status_name(st), inc, round(s.best_objective_bound), ok


def main():
    tl = float(sys.argv[1]) if len(sys.argv) > 1 else 180.0
    blocks = {
        "OR2": (2, lambda z: 1 if z[0] + z[1] >= 1 else 0),
        "AND2": (2, lambda z: z[0] * z[1]),
        "MAJ3": (3, lambda z: 1 if sum(z[:3]) >= 2 else 0),
        "THR3": (3, lambda z: 1 if 3 * z[0] + 2 * z[1] + z[2] >= 3
                 else 0),
    }
    outers = {
        "OR2o": (2, lambda v: 1 if sum(v) >= 1 else 0),
        "AND2o": (2, lambda v: 1 if sum(v) >= 2 else 0),
        "MAJ3o": (3, lambda v: 1 if sum(v) >= 2 else 0),
    }
    print("h(g^k) : W exact | couvert | verdict")
    for ho, (k, h) in outers.items():
        for go, (kb, g) in blocks.items():
            n = k * kb
            if n > 8:
                continue

            def f(z, k=k, kb=kb, h=h, g=g):
                vals = [g(z[i * kb:(i + 1) * kb]) for i in range(k)]
                return h(vals)
            cov, nmin = cover_number(f, n)
            st, W, lb, ok = w_exact(f, n, cap=cov, tl=tl)
            if st == "OPTIMAL":
                verdict = ("EGAL (pro-conjecture)" if W == cov else
                           f"CONTRE-EXEMPLE ! W = {W} < couvert = {cov}")
            else:
                verdict = f"indecis (lb {lb}, ub {W})"
            ver = {True: "", False: " [RE-VERIF ECHEC]",
                   None: ""}[ok]
            print(f"  {ho[:-1]}({go}^{k})  n={n} : W = {W} [{st}] | "
                  f"couvert = {cov} ({nmin} uns min) | {verdict}{ver}",
                  flush=True)


if __name__ == "__main__":
    main()
