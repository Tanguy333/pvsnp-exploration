# -*- coding: utf-8 -*-
r"""MC-013 — L'argument des bandes : vérifications.

LEMME INTERNE (fiche §2) : un « séparateur-à-bandes » du cube {x₁}∪B —
séparateur du cœur (1, b, 0, 0) dont les zéros évitent les BANDES
[c − o, c] ∪ [P − o, P] (c = valeur du un {x₁}, P = valeur du un B) — a
un poids ≥ b + 2 + o.

THÉORÈME (fiche §3, avec MC-011 branches 1-2 et MC-012 base) :
F(1, b, 0, o) = b + 2 + 2o pour tous b ≥ 2, o — la LOI LINÉAIRE COMPLÈTE.

Modes :
  lemme : teste le lemme interne DIRECTEMENT au solveur — min poids d'un
      séparateur du cube (1+b variables) sous les contraintes de bandes
      (domaines interdits via AddLinearExpressionInDomain), pour
      b = 2..4, o = 0..4 ; la borne REQUISE est ≥ b + 2 + o (le minimum
      MESURÉ vaut b + 2 + 2o — correction VER-MC-2 du docstring initial
      qui annonçait « exactement b + 2 + o »).
  certificats : décision au cap = loi − 1 sur la grille (1, b, o) jusqu'à
      la frontière ν = 8 — INFEASIBLE attendu partout.
"""
import sys
import time

from ortools.sat.python import cp_model


def lemme_bandes(b, o, tl=600):
    """Min poids d'un séparateur-à-bandes du cube (1, b) avec largeur de
    bande o+1. Variables du cube seulement (ν' = 1 + b) — o n'apparaît
    que dans les bandes."""
    nu = 1 + b
    N = 1 << nu
    u = 1
    v = ((1 << b) - 1) << 1
    zeros = [x for x in range(N) if x not in (u, v)]
    monomes = list(range(1, N))
    cap = 4 * (b + o + 2)
    model = cp_model.CpModel()
    a = {S: model.NewIntVar(0, cap, f"a{S}") for S in monomes}
    tot = model.NewIntVar(0, cap, "tot")
    model.Add(tot == sum(a.values()))
    val = {}
    for x in range(N):
        val[x] = model.NewIntVar(0, cap, f"v{x}")
        actifs = [a[S] for S in monomes if S & x == S]
        model.Add(val[x] == (sum(actifs) if actifs else 0))
    # bandes : pour tout zéro w, val(w) − c ∉ [−o, 0] et val(w) − P ∉ [−o, 0]
    hors_bande = cp_model.Domain.FromIntervals([[-cap, -o - 1], [1, cap]])
    for w in zeros:
        model.AddLinearExpressionInDomain(val[w] - val[u], hors_bande)
        model.AddLinearExpressionInDomain(val[w] - val[v], hors_bande)
    model.Minimize(tot)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tl
    solver.parameters.num_search_workers = 8
    st = solver.Solve(model)
    if st != cp_model.OPTIMAL:
        return None, str(st)
    # re-vérification indépendante du témoin
    temoin = {S: solver.Value(a[S]) for S in monomes if solver.Value(a[S])}
    vals = {}
    for x in range(N):
        vals[x] = sum(c for S, c in temoin.items() if S & x == S)
    c, P = vals[u], vals[v]
    for w in zeros:
        assert not (c - o <= vals[w] <= c), f"bande c violée en {w}"
        assert not (P - o <= vals[w] <= P), f"bande P violée en {w}"
    assert sum(temoin.values()) == solver.Value(tot)
    return solver.Value(tot), "OPTIMAL"


def run_lemme():
    print("=== LEMME INTERNE — min poids des séparateurs-à-bandes "
          "(attendu : b + 2 + o) ===")
    for b in (2, 3, 4):
        for o in (0, 1, 2, 3, 4):
            w, st = lemme_bandes(b, o)
            if st != "OPTIMAL":
                print(f"  (b={b}, o={o}) : NON CONCLU ({st})")
                continue
            attendu = b + 2 + o
            marque = "CONFORME" if w == attendu else (
                "!!! SOUS la borne — le lemme serait FAUX" if w < attendu
                else f"au-dessus ({w} > {attendu} — la borne n'est pas serrée ici)")
            print(f"  (b={b}, o={o}) : min = {w} ; lemme ≥ {attendu} : {marque}")


def decision(uns, nvars, cap, tl=1800):
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
    model.Add(tot <= cap)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tl
    solver.parameters.num_search_workers = 8
    st = solver.Solve(model)
    return {cp_model.INFEASIBLE: "INFEASIBLE", cp_model.OPTIMAL: "FAISABLE",
            cp_model.FEASIBLE: "FAISABLE"}.get(st, str(st))


def run_certificats():
    print("\n=== CERTIFICATS — la loi linéaire sur la grille, jusqu'à ν = 8 ===")
    t0 = time.time()
    for b, o in [(2, 3), (2, 4), (3, 3), (2, 5), (3, 4), (4, 3), (5, 2),
                 (6, 1)]:
        nu = 1 + b + o
        if nu > 8:
            continue
        u = 1
        v = ((1 << b) - 1) << 1
        loi = b + 2 + 2 * o
        st = decision(sorted({u, v}), nu, loi - 1)
        print(f"  (1,{b},0,{o}) ν={nu} : cap {loi-1} → {st}"
              f"  [{time.time()-t0:.0f}s]")
        if st == "FAISABLE":
            print("    !!! LOI LINÉAIRE RÉFUTÉE ICI")


if __name__ == "__main__":
    quel = sys.argv[1] if len(sys.argv) > 1 else "tout"
    if quel in ("tout", "lemme"):
        run_lemme()
    if quel in ("tout", "certificats"):
        run_certificats()
