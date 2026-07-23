"""
TACHE F-021 -- anatomie du comptage + cadre unilateral + predictions.

(1) Anatomie de l'optimum MAJ3(OR2^3) = 12 : extraction CP-SAT du
    support + re-verification. Resultat : les 12 paires croisees
    inter-blocs, coefficient 1 — separateur UNILATERAL (zeros -> {0}).
(2) THEOREME de classe : poids unilateral minimal = couvert minimal
    des uns minimaux par des monomes-uns ; pour MAJ3(OR2^3), chaque
    un minimal exige son monome -> 12, serre.
(3) Predictions du cadre : AND(OR2,OR2) = 4 (CONFIRMEE OPTIMALE) ;
    MAJ3(MAJ3^3) = 27 (incumbent re-verifie, optimalite ouverte).
"""

from __future__ import annotations

import itertools

from ortools.sat.python import cp_model


def solve(f, n, cap, hint=None, tl=240):
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
    if hint:
        for S in monos:
            m.add_hint(a[S], 1 if S in hint else 0)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = tl
    s.parameters.num_workers = 8
    st = s.solve(m)
    inc = (round(s.objective_value)
           if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None)
    sol = ({S: s.value(a[S]) for S in monos if s.value(a[S]) > 0}
           if inc is not None else None)
    ok = None
    if sol:
        ov, zv = set(), set()
        for z in inputs:
            supp = frozenset(j for j in range(n) if z[j])
            p = sum(v for S, v in sol.items() if S <= supp)
            (ov if f(z) else zv).add(p)
        ok = not (ov & zv)
    return s.status_name(st), inc, round(s.best_objective_bound), ok, sol


def main():
    or2 = lambda z: 1 if z[0] + z[1] >= 1 else 0
    maj3 = lambda z: 1 if sum(z[:3]) >= 2 else 0

    print("== (1) anatomie MAJ3(OR2^3) ==")
    f12 = lambda z: 1 if (or2(z[0:2]) + or2(z[2:4]) + or2(z[4:6])) >= 2 \
        else 0
    st, inc, lb, ok, sol = solve(f12, 6, 60, tl=60)
    cross = [S for S in sol if len({j // 2 for j in S}) > 1]
    print(f"  {st}, opt = {inc}, re-verif {ok} ; "
          f"croises {len(cross)}/{len(sol)}")
    print("  support : " + ", ".join(
        f"{sorted(S)}:{v}" for S, v in sorted(
            sol.items(), key=lambda kv: (len(kv[0]), sorted(kv[0])))))

    print("== (3) predictions du cadre unilateral ==")
    fand = lambda z: 1 if (or2(z[0:2]) + or2(z[2:4])) >= 2 else 0
    st, inc, lb, ok, _ = solve(fand, 4, 8, tl=60)
    print(f"  AND(OR2,OR2) : prediction 4 ; {st}, opt = {inc}, "
          f"lb = {lb}, re-verif {ok}")

    fmm = lambda z: 1 if (maj3(z[0:3]) + maj3(z[3:6])
                          + maj3(z[6:9])) >= 2 else 0
    hint = set()
    for bi, bj in [(0, 1), (0, 2), (1, 2)]:
        for pi in itertools.combinations(range(3), 2):
            for pj in itertools.combinations(range(3), 2):
                hint.add(frozenset([3 * bi + x for x in pi]
                                   + [3 * bj + y for y in pj]))
    st, inc, lb, ok, _ = solve(fmm, 9, 27, hint=hint, tl=240)
    print(f"  MAJ3(MAJ3^3) : prediction 27 ; {st}, opt = {inc}, "
          f"lb = {lb}, re-verif {ok}")


if __name__ == "__main__":
    main()
