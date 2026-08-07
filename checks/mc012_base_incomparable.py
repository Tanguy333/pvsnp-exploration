# -*- coding: utf-8 -*-
r"""MC-012 — La base incomparable : vérifications.

THÉORÈME (fiche §2) : F(1, b, 0, 0) = b + 2 pour b ≥ 2 — le forçage
d'égalité : si W ≤ b+1, alors c := a_{{x₁}} = 1, E_j := a_{{j}} +
a_{{x₁,j}} = 1 pour tout j, aucun monôme de B de taille ≥ 2 ; c = 1
interdit a_{{j}} = 1 (le point {j} est un zéro), donc a_{{x₁,j}} = 1
partout, donc σ_B = 0, donc P_B = p(B) = 0 = p(∅) — collision un/zéro. ∎

COROLLAIRE (avec les branches 1-2 de MC-011) :
b + 2 + o ≤ F(1, b, 0, o) ≤ b + 2 + 2o.

Modes :
  audit : sur les témoins optimaux (1, b, 0, 0), vérifie la comptabilité
      du forçage — au poids b+2, quelles inégalités sont serrées.
  certificats : décision au cap = loi − 1 sur les bases a = 1 (rappel)
      et surtout a ≥ 2 aux points JAMAIS ATTEINTS : ν = 8 — (4,4,0,0)
      [loi 10], (3,5,0,0) [loi 10], (2,6,0,0) [loi 10] — INFEASIBLE
      attendu ; puis faisabilité à la loi. NON CONCLU possible (ν = 8 est
      la frontière de l'instrument) — consigné honnêtement.
"""
import sys
import time

from ortools.sat.python import cp_model


def modele(uns, nvars, cap):
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
    return model, a, tot


def W_min(uns, nvars, cap, tl=1800):
    model, a, tot = modele(uns, nvars, cap)
    model.Minimize(tot)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tl
    solver.parameters.num_search_workers = 8
    st = solver.Solve(model)
    if st != cp_model.OPTIMAL:
        return None, None, str(st)
    temoin = {S: solver.Value(a[S]) for S in a if solver.Value(a[S])}
    su = set(uns)
    v1, v0 = set(), set()
    for x in range(1 << nvars):
        p = sum(c for S, c in temoin.items() if S & x == S)
        (v1 if x in su else v0).add(p)
    assert not (v1 & v0) and sum(temoin.values()) == solver.Value(tot)
    return solver.Value(tot), temoin, "OPTIMAL"


def decision(uns, nvars, cap, tl=1800):
    model, a, tot = modele(uns, nvars, cap)
    model.Add(tot <= cap)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tl
    solver.parameters.num_search_workers = 8
    st = solver.Solve(model)
    return {cp_model.INFEASIBLE: "INFEASIBLE",
            cp_model.OPTIMAL: "FAISABLE", cp_model.FEASIBLE: "FAISABLE",
            }.get(st, str(st))


def coeur(na, nb, o=0):
    nu = na + nb + o
    u = (1 << na) - 1
    v = ((1 << nb) - 1) << na
    return sorted({u, v}), nu


def loi(na, nb, o=0):
    if na == 0:
        return nb + 2 * o
    return 2 * (na + nb + o) - max(nb, 2, na + nb - 2)


def run_audit():
    print("=== AUDIT du forçage — témoins (1, b, 0, 0) ===")
    for b in (2, 3, 4, 5, 6):
        uns, nu = coeur(1, b)
        if nu > 7:
            continue
        w, temoin, st = W_min(uns, nu, (1 << nu) - 1)
        assert st == "OPTIMAL" and w == b + 2
        c = temoin.get(1, 0)
        sigma_B = sum(cc for S, cc in temoin.items()
                      if S & 1 == 0 and bin(S).count("1") == 1)
        paires = sum(cc for S, cc in temoin.items()
                     if S & 1 and bin(S).count("1") == 2)
        hauts_B = sum(cc for S, cc in temoin.items()
                      if S & 1 == 0 and bin(S).count("1") >= 2)
        autres = w - c - sigma_B - paires - hauts_B
        print(f"  (1,{b}) : W = {w} = b+2 ; c = {c}, σ_B = {sigma_B}, "
              f"paires = {paires}, hauts-B = {hauts_B}, autres mixtes = {autres}")


def run_certificats():
    print("\n=== CERTIFICATS — bases a ≥ 2, points jamais atteints (ν = 8) ===")
    t0 = time.time()
    for na, nb in [(4, 4), (3, 5), (2, 6)]:
        uns, nu = coeur(na, nb)
        cible = loi(na, nb)
        st_dec = decision(uns, nu, cible - 1)
        print(f"  ({na},{nb},0,0) ν={nu} : cap {cible-1} → {st_dec}"
              f"  [{time.time()-t0:.0f}s]")
        if st_dec == "FAISABLE":
            print("    !!! MINORANT RÉFUTÉ — C-MC009 fausse ici")
        st_fais = decision(uns, nu, cible)
        print(f"    faisabilité à {cible} → {st_fais}  [{time.time()-t0:.0f}s]")
    # rappel a = 1 (théorème neuf) : certificats aux tailles accessibles
    print("  rappel a = 1 (désormais THÉORÈME à o = 0) :")
    for nb, o in [(2, 0), (3, 0), (4, 0), (5, 0), (6, 0)]:
        uns, nu = coeur(1, nb, o)
        if nu > 7:
            continue
        cible = loi(1, nb, o)
        st_dec = decision(uns, nu, cible - 1, tl=600)
        print(f"  (1,{nb},0,{o}) ν={nu} : cap {cible-1} → {st_dec}"
              f"  [{time.time()-t0:.0f}s]")


if __name__ == "__main__":
    quel = sys.argv[1] if len(sys.argv) > 1 else "tout"
    if quel in ("tout", "audit"):
        run_audit()
    if quel in ("tout", "certificats"):
        run_certificats()
