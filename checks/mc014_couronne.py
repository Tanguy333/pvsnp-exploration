# -*- coding: utf-8 -*-
r"""MC-014 — La base couronne (a ≥ 2, o = 0) : instruments.

Cible : F(a, b, 0, 0) = a + b + 2 pour 2 ≤ a ≤ b (la loi C-MC009 s'unifie
ainsi sur a ≥ 2 : min(2a+b, a+b+2) = a+b+2).

OUTILS PROUVÉS (fiche §2) :
  (T1) tranche x_i := 1 (i ∈ A) : v disparaît, reste [w' = A∖{i}] — la
       loi G donne W ≥ b + 1 + a_{{i}} pour tout i ∈ A (symétrique en B).
  (T2) tranche pleine x_A := 1 : q(y) := p(A∪y) − P_A est le polynôme
       fusionné de poids exactement W_B + X, ses positions singletons
       sont les E_k := Σ{a_S : S∖A = {k}}, et ses zéros évitent
       {0, Δ := P_B − P_A} — d'où W_B + X ≥ b, et si Δ = 1 : E_k ≥ 2 ∀k.
       Symétrique : W_A + X ≥ a, r-zéros évitent {0, −Δ}.
  (*)  W ≤ a+b+1 force h_A + h_B + R ≤ π + 1 (h = poids hauts, R = mixte
       à deux côtés ≥ 2, π = paires).

Modes :
  temoins : structure des optima couronne — décomposition (W_A, W_B, X,
      σ, h, π, R), valeurs (P_A, P_B, Δ), audit T1/T2/E_k sur témoins.
  certificats : rappel + compléments INFEASIBLE au cap a+b+1 (la
      non-existence que la preuve doit établir), jusqu'à ν = 8.
"""
import sys
import time

from ortools.sat.python import cp_model


def W_cpsat(uns, nvars, cap, tl=1800, minimise=True, cap_dur=None):
    N = 1 << nvars
    zeros = [x for x in range(N) if x not in set(uns)]
    monomes = list(range(1, N))
    model = cp_model.CpModel()
    a = {S: model.NewIntVar(0, cap, f"a{S}") for S in monomes}
    tot = model.NewIntVar(0, cap, "tot")
    model.Add(tot == sum(a.values()))
    val = {}
    for x in range(N):
        val[x] = model.NewIntVar(0, cap, f"v{x}")
        actifs = [a[S] for S in monomes if S & x == S]
        model.Add(val[x] == (sum(actifs) if actifs else 0))
    for u in uns:
        for v in zeros:
            model.Add(val[u] != val[v])
    if cap_dur is not None:
        model.Add(tot <= cap_dur)
    if minimise:
        model.Minimize(tot)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tl
    solver.parameters.num_search_workers = 8
    st = solver.Solve(model)
    if st == cp_model.INFEASIBLE:
        return None, None, "INFEASIBLE"
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None, None, str(st)
    temoin = {S: solver.Value(a[S]) for S in monomes if solver.Value(a[S])}
    su = set(uns)
    v1, v0 = set(), set()
    for x in range(N):
        p = sum(c for S, c in temoin.items() if S & x == S)
        (v1 if x in su else v0).add(p)
    assert not (v1 & v0)
    return solver.Value(tot), temoin, ("OPTIMAL" if st == cp_model.OPTIMAL
                                       else "FEASIBLE")


def coeur(na, nb):
    nu = na + nb
    A = (1 << na) - 1
    B = ((1 << nb) - 1) << na
    return A, B, nu


def run_temoins():
    print("=== TÉMOINS COURONNE — structure et audit T1/T2 ===")
    for na, nb in [(2, 2), (2, 3), (3, 3), (2, 4), (3, 4), (2, 5)]:
        A, B, nu = coeur(na, nb)
        if nu > 7:
            continue
        w, temoin, st = W_cpsat(sorted({A, B}), nu, (1 << nu) - 1)
        assert st == "OPTIMAL" and w == na + nb + 2
        # décomposition
        WA = sum(c for S, c in temoin.items() if S & B == 0)
        WB = sum(c for S, c in temoin.items() if S & A == 0)
        X = w - WA - WB
        sigA = sum(c for S, c in temoin.items()
                   if S & B == 0 and bin(S).count("1") == 1)
        sigB = sum(c for S, c in temoin.items()
                   if S & A == 0 and bin(S).count("1") == 1)
        pi = sum(c for S, c in temoin.items()
                 if bin(S & A).count("1") == 1 and bin(S & B).count("1") == 1)
        R = sum(c for S, c in temoin.items()
                if bin(S & A).count("1") >= 2 and bin(S & B).count("1") >= 2)
        PA = sum(c for S, c in temoin.items() if S & A == S)
        PB = sum(c for S, c in temoin.items() if S & B == S)
        delta = PB - PA
        # E_k et T1
        Es = []
        for k in range(na, na + nb):
            bk = 1 << k
            Es.append(sum(c for S, c in temoin.items() if (S & B) == bk))
        ais = [temoin.get(1 << i, 0) for i in range(na)]
        ok_t1 = all(w >= nb + 1 + ai for ai in ais)
        ok_t2 = (WB + X >= nb) and (WA + X >= na)
        ok_ek = all(e >= 1 for e in Es) and (delta != 1 or all(e >= 2 for e in Es))
        print(f"  ({na},{nb}) : W = {w} ; W_A={WA} (σ={sigA}), W_B={WB} "
              f"(σ={sigB}), X={X} (π={pi}, R={R}) ; P_A={PA}, P_B={PB}, "
              f"Δ={delta} ; E = {Es} ; T1 {'✓' if ok_t1 else '✗'} "
              f"T2 {'✓' if ok_t2 else '✗'} E-règles {'✓' if ok_ek else '✗'}")
        assert ok_t1 and ok_t2 and ok_ek


def run_certificats():
    print("\n=== CERTIFICATS — aucun séparateur de poids ≤ a+b+1 (la "
          "non-existence que la preuve doit établir) ===")
    t0 = time.time()
    for na, nb in [(2, 2), (2, 3), (3, 3), (2, 4), (3, 4), (2, 5), (4, 4),
                   (3, 5), (2, 6)]:
        A, B, nu = coeur(na, nb)
        if nu > 8:
            continue
        _, _, st = W_cpsat(sorted({A, B}), nu, (1 << nu) - 1,
                           minimise=False, cap_dur=na + nb + 1)
        print(f"  ({na},{nb}) ν={nu} : cap {na+nb+1} → {st}"
              f"  [{time.time()-t0:.0f}s]")
        if st != "INFEASIBLE":
            print("    !!! séparateur sous la loi — la cible serait fausse")


if __name__ == "__main__":
    quel = sys.argv[1] if len(sys.argv) > 1 else "tout"
    if quel in ("tout", "temoins"):
        run_temoins()
    if quel in ("tout", "certificats"):
        run_certificats()
