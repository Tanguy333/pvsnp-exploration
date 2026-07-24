"""
TOUR 27 (Proposeur) -- piece 3 : fermeture de classes de monomes croises
a budget <= 29 pour MAJ_5(OR2^5) (CP-SAT, minimisation ; une borne inf
prouvee > 29 ferme la classe ; un incumbent <= 29 est un TEMOIN).

Classes (pools de monomes) :
  A : intra-bloc individuels (15) + faisceaux de paires s_i*s_j (10 vars,
      cout 4 l'unite) -- 25 variables.
  B : intra (15) + paires croisees INDIVIDUELLES u_i v_j (40) -- 55 vars.
  C : span <= 2 complet : B + monomes (2,1) x_iy_iu_j (40) + (2,2)
      x_iy_ix_jy_j (10) -- 105 vars.
  E : C + tous les monomes de span 3 (types (1,1,1): 80, (2,1,1): 120,
      (2,2,1): 60, (2,2,2): 10) -- 375 vars. Par le lemme de span, les
      monomes de span >= 3 sont invisibles cote 0 (actifs seulement si
      m >= 3) : E couvre exactement < les temoins sans monome de span
      >= 4 >.

Usage : python tour_27_proposeur_classes.py <classe> <tl_secondes>
"""

from __future__ import annotations

import itertools
import sys
import time

from ortools.sat.python import cp_model

K = 5
N = 10
T = 3


def f_maj5(z):
    return 1 if sum(1 for i in range(K) if z[2 * i] or z[2 * i + 1]) >= T else 0


def intra_monos():
    out = []
    for i in range(K):
        x, y = 2 * i, 2 * i + 1
        out += [frozenset([x]), frozenset([y]), frozenset([x, y])]
    return out


def crossed_pairs():
    out = []
    for i, j in itertools.combinations(range(K), 2):
        for u in (2 * i, 2 * i + 1):
            for v in (2 * j, 2 * j + 1):
                out.append(frozenset([u, v]))
    return out


def span2_heavy():
    out = []
    for i, j in itertools.permutations(range(K), 2):
        for v in (2 * j, 2 * j + 1):        # (2,1) : bloc i complet + 1 var
            out.append(frozenset([2 * i, 2 * i + 1, v]))
    for i, j in itertools.combinations(range(K), 2):   # (2,2)
        out.append(frozenset([2 * i, 2 * i + 1, 2 * j, 2 * j + 1]))
    return out


def span3_all():
    out = []
    for blocks in itertools.combinations(range(K), 3):
        # chaque bloc contribue 1 var (2 choix) ou 2 vars (1 choix)
        for contrib in itertools.product((0, 1, 2, 3), repeat=3):
            if any(c == 0 for c in contrib):
                continue
            S = set()
            for b, c in zip(blocks, contrib):
                if c & 1:
                    S.add(2 * b)
                if c & 2:
                    S.add(2 * b + 1)
            out.append(frozenset(S))
    return sorted(set(out), key=lambda s: (len(s), sorted(s)))


def pool_for(cls: str):
    if cls == "A":
        return intra_monos(), crossed_pairs()   # (individuels, en faisceaux)
    if cls == "B":
        return intra_monos() + crossed_pairs(), None
    if cls == "C":
        return intra_monos() + crossed_pairs() + span2_heavy(), None
    if cls == "E":
        return (intra_monos() + crossed_pairs() + span2_heavy()
                + span3_all()), None
    raise ValueError(cls)


def solve_class(cls: str, tl: float):
    inputs = list(itertools.product((0, 1), repeat=N))
    ones = [z for z in inputs if f_maj5(z)]
    zeros = [z for z in inputs if not f_maj5(z)]

    m = cp_model.CpModel()

    if cls == "A":
        intra, pairs = pool_for(cls)
        a = {S: m.new_int_var(0, 29, f"a{i}") for i, S in enumerate(intra)}
        # faisceaux : d_ij, chaque faisceau = 4 paires de cout 1 chacune
        bundles = list(itertools.combinations(range(K), 2))
        d = {ij: m.new_int_var(0, 7, f"d{ij}") for ij in bundles}
        weight = sum(a.values()) + 4 * sum(d.values())

        def val_terms(z):
            supp = frozenset(j for j in range(N) if z[j])
            terms = [a[S] for S in intra if S <= supp]
            s = [z[2 * i] + z[2 * i + 1] for i in range(K)]
            for (i, j) in bundles:
                if s[i] and s[j]:
                    terms.append(d[(i, j)] * (s[i] * s[j]))
            return terms
    else:
        monos, _ = pool_for(cls)
        a = {S: m.new_int_var(0, 29, f"a{i}") for i, S in enumerate(monos)}
        weight = sum(a.values())

        def val_terms(z):
            supp = frozenset(j for j in range(N) if z[j])
            return [a[S] for S in monos if S <= supp]

    pvals = {}
    for z in inputs:
        terms = val_terms(z)
        v = m.new_int_var(0, 29 * 40, f"p{z}")
        m.add(v == sum(terms) if terms else v == 0)
        pvals[z] = v
    for z1 in ones:
        for z0 in zeros:
            m.add(pvals[z1] != pvals[z0])

    m.add(weight <= 30)          # on cherche <= 29 ; 30 = temoin connu
    m.minimize(weight)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tl
    solver.parameters.num_workers = 8
    t0 = time.time()
    st = solver.solve(m)
    dt = time.time() - t0
    name = solver.status_name(st)
    inc = (round(solver.objective_value)
           if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None)
    lb = round(solver.best_objective_bound)
    nvars = len(a) + (len(d) if cls == "A" else 0)
    print(f"  classe {cls} ({nvars} vars) : statut={name} "
          f"incumbent={inc} borne_inf_prouvee={lb}  ({dt:.0f}s)", flush=True)
    if inc is not None and inc <= 29:
        print("  *** TEMOIN < 30 TROUVE -- extraire et re-verifier ! ***",
              flush=True)
        if cls == "A":
            sol_intra = {S: solver.value(a[S]) for S in a
                         if solver.value(a[S]) > 0}
            sol_d = {ij: solver.value(d[ij]) for ij in d
                     if solver.value(d[ij]) > 0}
            print(f"  intra : { {tuple(sorted(S)): v for S, v in sol_intra.items()} }",
                  flush=True)
            print(f"  faisceaux : {sol_d}", flush=True)
        else:
            sol = {S: solver.value(a[S]) for S in a if solver.value(a[S]) > 0}
            print(f"  support : { {tuple(sorted(S)): v for S, v in sol.items()} }",
                  flush=True)
    return name, inc, lb


def main():
    cls = sys.argv[1].upper() if len(sys.argv) > 1 else "A"
    tl = float(sys.argv[2]) if len(sys.argv) > 2 else 600.0
    print(f"TOUR 27 piece 3 -- fermeture classe {cls} (tl={tl:.0f}s)",
          flush=True)
    solve_class(cls, tl)
    print("FIN.", flush=True)


if __name__ == "__main__":
    main()
