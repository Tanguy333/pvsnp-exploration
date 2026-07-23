"""
TOUR 26 (Proposeur) -- mesures CP-SAT pour la cible super-additive.

Reutilise l'instrument F-014 (solve/verify). Modele W identique au dossier.

MESURES :
  A. Sanite : MAJ_3(OR2^3) exact n=6 (attendu 12, certifie dossier §5).
  B. Optima DECOMPOSABLES exacts (monomes intra-bloc seulement) pour
     MAJ_k(OR2^k), k = 3, 4, 5 -- teste si le schema mod-(k+1) [poids
     k(k+2)] est optimal dans la classe decomposable.
  C. Points exacts n=8 : THR2(OR2^4) (= MAJ_4(OR2^4), restriction
     bloc5:=1 de MAJ_5) et THR3(OR2^4) (restriction bloc5:=0).
     Toute borne inf PROUVEE ici est une borne inf de W(MAJ_5(OR2^5))
     par le lemme de restriction (L26.5).
  D. MAJ_5(OR2^5) n=10 direct : incumbent + borne inf prouvee (tl long).

Usage : python tour_26_proposeur_cpsat.py [étape] [tl_secondes]
        étapes : A B C D (defaut : toutes sauf D ; D = longue)
"""

from __future__ import annotations

import itertools
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from task_f014_cpsat_symand import verify
from ortools.sat.python import cp_model


# ----------------------------------------------------------- fonctions

def maj_or2(k: int, t: int = None):
    t = t if t is not None else (k + 1) // 2
    def f(z):
        m = sum(1 for i in range(k) if z[2 * i] or z[2 * i + 1])
        return 1 if m >= t else 0
    return f


def or2_mod_hint(k: int, M: int) -> dict:
    h = {}
    for i in range(k):
        x, y = 2 * i, 2 * i + 1
        h[frozenset([x])] = 1
        h[frozenset([y])] = 1
        h[frozenset([x, y])] = M - 1
    return h


def crossed_pairs_hint(k: int) -> dict:
    h = {}
    for i, j in itertools.combinations(range(k), 2):
        for u in (2 * i, 2 * i + 1):
            for v in (2 * j, 2 * j + 1):
                h[frozenset([u, v])] = 1
    return h


# ------------------------------------------------------ solveur generique

def solve_gen(f, n, monos, hint=None, tl=300.0, workers=8, ub=127):
    inputs = list(itertools.product((0, 1), repeat=n))
    ones = [z for z in inputs if f(z) == 1]
    zeros = [z for z in inputs if f(z) == 0]

    m = cp_model.CpModel()
    a = {S: m.new_int_var(0, ub, f"a{i}") for i, S in enumerate(monos)}
    pvals = {}
    for z in inputs:
        supp = frozenset(j for j in range(n) if z[j])
        terms = [a[S] for S in monos if S <= supp]
        v = m.new_int_var(0, ub * max(1, len(monos)), f"p{z}")
        m.add(v == sum(terms) if terms else v == 0)
        pvals[z] = v
    for z1 in ones:
        for z0 in zeros:
            m.add(pvals[z1] != pvals[z0])
    m.minimize(sum(a.values()))
    if hint:
        for S, val in hint.items():
            if S in a:
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
        sol = {S: solver.value(a[S]) for S in monos if solver.value(a[S]) > 0}
    return name, inc, lb, sol


def all_monos(n: int) -> list:
    monos = []
    for d in range(1, n + 1):
        monos.extend(frozenset(c) for c in itertools.combinations(range(n), d))
    return monos


def intra_block_monos(k: int) -> list:
    """ Monomes intra-bloc pour blocs OR2 : {x_i}, {y_i}, {x_i,y_i}. """
    monos = []
    for i in range(k):
        x, y = 2 * i, 2 * i + 1
        monos += [frozenset([x]), frozenset([y]), frozenset([x, y])]
    return monos


def report(label, f, n, name, inc, lb, sol):
    ver = ""
    if sol is not None:
        ver = " [re-verif OK]" if verify(f, n, sol) else " [RE-VERIF ECHEC !]"
    print(f"  {label:<38} statut={name:<10} incumbent={inc} "
          f"borne_inf_prouvee={lb}{ver}", flush=True)
    if sol is not None and name == "OPTIMAL" and len(sol) <= 40:
        supp = ", ".join(f"{sorted(S)}:{v}" for S, v in
                         sorted(sol.items(),
                                key=lambda kv: (len(kv[0]), sorted(kv[0]))))
        print(f"      support : {supp}", flush=True)


def main():
    args = sys.argv[1:]
    steps = set(a.upper() for a in args if a.upper() in "ABCD") or {"A", "B", "C"}
    tl = float(next((a for a in args if a.replace('.', '').isdigit()), 600))

    print("TOUR 26 (Proposeur) -- mesures CP-SAT", flush=True)
    print("=" * 74, flush=True)

    if "A" in steps:
        print("\n[A] Sanite : MAJ_3(OR2^3) exact, n=6 (attendu 12)", flush=True)
        f = maj_or2(3)
        t0 = time.time()
        res = solve_gen(f, 6, all_monos(6), hint=crossed_pairs_hint(3), tl=tl)
        report("MAJ_3(OR2^3) full", f, 6, *res)
        print(f"      ({time.time()-t0:.0f}s)", flush=True)

    if "B" in steps:
        print("\n[B] Optima DECOMPOSABLES exacts (monomes intra-bloc)", flush=True)
        for k in (3, 4, 5):
            f = maj_or2(k)
            n = 2 * k
            t0 = time.time()
            res = solve_gen(f, n, intra_block_monos(k),
                            hint=or2_mod_hint(k, k + 1), tl=tl)
            report(f"MAJ_{k}(OR2^{k}) DECOMPOSABLE  [mod={k*(k+2)}]",
                   f, n, *res)
            print(f"      ({time.time()-t0:.0f}s)", flush=True)

    if "C" in steps:
        print("\n[C] Points exacts n=8 (restrictions de MAJ_5)", flush=True)
        # THR2(OR2^4) = MAJ_4(OR2^4) (t = ceil(4/2) = 2) = restriction bloc5:=1.
        f2 = maj_or2(4, t=2)
        t0 = time.time()
        res = solve_gen(f2, 8, all_monos(8), hint=crossed_pairs_hint(4), tl=tl)
        report("THR2(OR2^4) = MAJ_4 full  [hint 24]", f2, 8, *res)
        print(f"      ({time.time()-t0:.0f}s)", flush=True)
        # THR3(OR2^4) = restriction bloc5:=0.
        f3 = maj_or2(4, t=3)
        t0 = time.time()
        res = solve_gen(f3, 8, all_monos(8), hint=or2_mod_hint(4, 5), tl=tl)
        report("THR3(OR2^4) full  [hint mod 24]", f3, 8, *res)
        print(f"      ({time.time()-t0:.0f}s)", flush=True)

    if "D" in steps:
        print("\n[D] MAJ_5(OR2^5) direct, n=10 (incumbent + borne inf)", flush=True)
        f = maj_or2(5)
        t0 = time.time()
        res = solve_gen(f, 10, all_monos(10), hint=or2_mod_hint(5, 6),
                        tl=tl, ub=63)
        report("MAJ_5(OR2^5) full  [hint mod 35]", f, 10, *res)
        print(f"      ({time.time()-t0:.0f}s)", flush=True)

    print("\nFIN.", flush=True)


if __name__ == "__main__":
    main()
