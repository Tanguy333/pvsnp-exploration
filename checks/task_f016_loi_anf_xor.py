"""
TACHE F-016 -- la loi ANF du XOR.

CANDIDAT pour c(g) (F-015) : la sparsite ANF.
  Construction parite (borne sup, PROUVEE ici par verification) :
  prendre a_S = ANF_S(g) in {0,1} pour chaque bloc ; alors
  p(z) mod 2 = g(z), donc p_A + p_B mod 2 = g_A xor g_B : la porte
  symetrique lit la parite. Poids = |ANF(g_A)| + |ANF(g_B)|.
  (Terme constant : nos blocs s'annulent en 0, ANF_vide = 0.)

  LOI CONJECTUREE (egalite) : W(XOR(g_A,g_B)) = |ANF(g_A)|+|ANF(g_B)|.
  Deja verifiee par les optima fermes si |ANF(THR4)| = 7 et
  |ANF(GT2)| = 8 (supports observes) ; IP_2k = XOR de k AND_2
  (sparsite 1) redonne la loi k de F-003.

Protocole : (1) calculer les ANF (Mobius sur F2) ; (2) verifier la
construction parite par enumeration ; (3) PREDIRE 4 instances neuves
puis les fermer par CP-SAT (hint = construction parite, plafond =
prediction [licite : la construction realise ce poids], cassage de
symetrie si blocs isomorphes).
"""

from __future__ import annotations

import itertools
import sys
import time

from ortools.sat.python import cp_model


def anf(g, n):
    """Coefficients ANF (Mobius sur F2). Retourne set de frozensets."""
    coeffs = {}
    for S in itertools.chain.from_iterable(
            itertools.combinations(range(n), d) for d in range(n + 1)):
        S = frozenset(S)
        v = 0
        for T in itertools.chain.from_iterable(
                itertools.combinations(sorted(S), d)
                for d in range(len(S) + 1)):
            z = tuple(1 if j in T else 0 for j in range(n))
            v ^= g(z)
        if v:
            coeffs[S] = 1
    return set(coeffs)


def verify_parity_construction(f, n, support):
    """p = somme des monomes ANF ; verifier que la parite de p separe."""
    ones_v, zeros_v = set(), set()
    for z in itertools.product((0, 1), repeat=n):
        supp = frozenset(j for j in range(n) if z[j])
        p = sum(1 for S in support if S <= supp)
        (ones_v if f(z) else zeros_v).add(p)
    return not (ones_v & zeros_v)


def cpsat_close(f, n, cap, hint_support, symbreak_blocks=None, tl=300):
    inputs = list(itertools.product((0, 1), repeat=n))
    ones = [z for z in inputs if f(z) == 1]
    zeros = [z for z in inputs if f(z) == 0]
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
    m.minimize(total)
    for S in monos:
        m.add_hint(a[S], 1 if S in hint_support else 0)
    if symbreak_blocks:
        A, B = symbreak_blocks
        massA = sum(a[S] for S in monos if S <= frozenset(A))
        massB = sum(a[S] for S in monos if S <= frozenset(B))
        m.add(massA <= massB)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tl
    solver.parameters.num_workers = 8
    st = solver.solve(m)
    inc = (round(solver.objective_value)
           if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None)
    return solver.status_name(st), inc, round(solver.best_objective_bound)


def main():
    tl = float(sys.argv[1]) if len(sys.argv) > 1 else 300.0
    # blocs
    thr4 = lambda z: 1 if 4 * z[0] + 3 * z[1] + 2 * z[2] + z[3] >= 4 else 0
    gt2 = lambda z: 1 if 2 * z[0] + z[1] - 2 * z[2] - z[3] >= 1 else 0
    or2 = lambda z: 1 if z[0] + z[1] >= 1 else 0
    maj3 = lambda z: 1 if z[0] + z[1] + z[2] >= 2 else 0
    and2 = lambda z: z[0] * z[1]

    print("== (1) sparsites ANF des blocs ==")
    spars = {}
    for name, g, k in [("AND2", and2, 2), ("OR2", or2, 2),
                       ("MAJ3", maj3, 3), ("THR4", thr4, 4),
                       ("GT2", gt2, 4)]:
        A = anf(g, k)
        spars[name] = (A, k)
        print(f"  |ANF({name})| = {len(A)} : " +
              ", ".join(str(sorted(S)) for S in
                        sorted(A, key=lambda S: (len(S), sorted(S)))),
              flush=True)
    print("  controle post-hoc : optima fermes 14 = 7+7 et 16 = 8+8 "
          "ssi |ANF(THR4)| = 7 et |ANF(GT2)| = 8")

    print("\n== (2)+(3) predictions et fermetures CP-SAT ==")
    def make_xor(gA, kA, gB, kB):
        def f(z):
            return gA(z[:kA]) ^ gB(z[kA:kA + kB])
        return f, kA + kB

    tests = [("XOR(OR2,OR2)", "OR2", "OR2", True),
             ("XOR(MAJ3,MAJ3)", "MAJ3", "MAJ3", True),
             ("XOR(AND2,THR4)", "AND2", "THR4", False),
             ("XOR(THR4,GT2)", "THR4", "GT2", False)]
    for label, nA, nB, sym in tests:
        (AA, kA), (AB, kB) = spars[nA], spars[nB]
        gA, gB = {"AND2": and2, "OR2": or2, "MAJ3": maj3,
                  "THR4": thr4, "GT2": gt2}[nA], \
                 {"AND2": and2, "OR2": or2, "MAJ3": maj3,
                  "THR4": thr4, "GT2": gt2}[nB]
        f, n = make_xor(gA, kA, gB, kB)
        pred = len(AA) + len(AB)
        support = set(AA) | {frozenset(j + kA for j in S) for S in AB}
        okc = verify_parity_construction(f, n, support)
        sb = ((list(range(kA)), list(range(kA, n)))
              if sym and kA == kB else None)
        t0 = time.time()
        st, inc, lb = cpsat_close(f, n, pred, support, sb, tl)
        verdict = ("LOI CONFIRMEE (optimum = prediction)"
                   if st == "OPTIMAL" and inc == pred else
                   f"LOI REFUTEE ? optimum {inc} < {pred}"
                   if st == "OPTIMAL" else f"indecis (lb {lb})")
        print(f"  {label:<18} : prediction {pred} "
              f"(constr. parite {'OK' if okc else 'ECHEC'}) ; "
              f"CP-SAT {st}, opt = {inc}, lb = {lb} -> {verdict}  "
              f"({time.time()-t0:.0f}s)", flush=True)


if __name__ == "__main__":
    main()
