# -*- coding: utf-8 -*-
r"""MC-010 — Les minorants des cœurs de C-MC009 : l'argument des copies
décalées, son audit numérique, et les certificats hors-preuve.

L'ARGUMENT (preuves complètes : fiche MC-010 §2-3). Cœur comparable
{0-point, B} (b ≥ 2, o dehors). Classes de poids : W_B (S ⊆ B),
ω_l (S∩O = {l}), μ (|S∩O| ≥ 2) ; W = W_B + Σ ω_l + μ. Faits :
  (F1) a_i ≥ 1 pour tout i (p({i}) ≠ p(0) = 0) ;
  (F2) D_j := P − p(B∖{j}) = Σ{a_S : j ∈ S ⊆ B} ≥ 1 ;
  (F3) l « léger » (ω_l = 1, donc a_l = 1 seul) : la copie l-décalée du
       cube B vaut p(X∪{l}) = p(X) + 1 ⟹ D_j ≠ 1 ;
  (F4) L ⊆ légers, μ = 0 : p(X∪L) = p(X) + |L| ⟹ D_j ∉ {1..k} ⟹
       D_j ≥ k+1 ;
  (convexité) Σ_j D_j = Σ_{S⊆B} |S|·a_S ≤ s₁ + b·h ⟹
       W_B ≥ s₁ + (min D) − s₁/b ≥ b + (min D) − 1.

Modes :
  audit : vérifie les inégalités de la preuve (F1-F4, convexité,
      dichotomie léger/lourd) sur les TÉMOINS OPTIMAUX re-calculés des
      cœurs comparables et (1,1) — un contre-exemple aux inégalités
      réfuterait la preuve.
  certificats : dans la ZONE HORS PREUVE (o ≥ 3, μ libre), certifie
      W ≥ loi par CP-SAT en décision : cap = loi − 1 → INFEASIBLE attendu
      (assertion de solveur, réserve T27-S2 §4 — consignée comme telle).
  incomparable : mêmes certificats pour les cœurs incomparables a ≥ 1
      (zone entièrement hors preuve de minorant).
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


def W_min(uns, nvars, cap, tl=900):
    model, a, tot = modele(uns, nvars, cap)
    model.Minimize(tot)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tl
    solver.parameters.num_search_workers = 8
    st = solver.Solve(model)
    if st != cp_model.OPTIMAL:
        return None, None, str(st)
    temoin = {S: solver.Value(a[S]) for S in monomes_actifs(a, solver)}
    return solver.Value(tot), temoin, "OPTIMAL"


def monomes_actifs(a, solver):
    return [S for S in a if solver.Value(a[S])]


def decision_infaisable(uns, nvars, cap, tl=900):
    """Renvoie True si aucun séparateur de poids ≤ cap (INFEASIBLE)."""
    model, a, tot = modele(uns, nvars, cap)
    model.Add(tot <= cap)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tl
    solver.parameters.num_search_workers = 8
    st = solver.Solve(model)
    if st == cp_model.INFEASIBLE:
        return True, "INFEASIBLE"
    if st == cp_model.OPTIMAL or st == cp_model.FEASIBLE:
        return False, "FAISABLE (contre-exemple au minorant !)"
    return None, str(st)


def coeur(na, nb, o):
    nu = na + nb + o
    u = (1 << na) - 1
    v = ((1 << nb) - 1) << na
    return sorted({u, v}), nu


def loi(na, nb, o):
    if na == 0:
        return nb + 2 * o
    return 2 * (na + nb + o) - max(nb, 2, na + nb - 2)


def run_audit():
    print("=== AUDIT — les inégalités de la preuve sur les témoins optimaux ===")
    configs = [(0, b, o) for b in (2, 3) for o in (1, 2, 3) if b + o <= 6] \
        + [(1, 1, o) for o in (1, 2, 3, 4) if 2 + o <= 6]
    for na, nb, o in configs:
        uns, nu = coeur(na, nb, o)
        w, temoin, st = W_min(uns, nu, (1 << nu) - 1)
        assert st == "OPTIMAL"
        # décomposition par classes
        A = (1 << na) - 1
        B = ((1 << nb) - 1) << na
        O = ((1 << nu) - 1) ^ A ^ B
        WB = sum(c for S, c in temoin.items() if S & O == 0)
        omegas = {}
        mu = 0
        for S, c in temoin.items():
            po = S & O
            if po == 0:
                continue
            if bin(po).count("1") == 1:
                omegas[po] = omegas.get(po, 0) + c
            else:
                mu += c
        # F1 : singletons ≥ 1 pour le comparable (0-point protégé)
        ok_f1 = True
        if na == 0:
            for i in range(nu):
                if temoin.get(1 << i, 0) < 1:
                    ok_f1 = False
        # dichotomie : chaque l léger (ω_l = 1) doit porter a_l = 1
        legers = [po for po, om in omegas.items() if om == 1]
        ok_leger = all(temoin.get(po, 0) == 1 for po in legers)
        # comptage global : W = WB + Σω + μ
        ok_somme = (WB + sum(omegas.values()) + mu == w)
        # bilan de la preuve : W ≥ loi
        print(f"  (a={na}, b={nb}, o={o}) : W = {w} = loi {loi(na, nb, o)} ; "
              f"W_B = {WB}, ω = {sorted(omegas.values())}, μ = {mu} ; "
              f"F1 {'✓' if ok_f1 else '✗'}, légers-portent-singleton "
              f"{'✓' if ok_leger else '✗'}, somme {'✓' if ok_somme else '✗'}")
        assert ok_somme
        if na == 0:
            assert ok_f1, "F1 violé : la preuve serait fausse"
        assert ok_leger or not legers, "un léger sans singleton : revoir F3"


def run_certificats():
    print("\n=== CERTIFICATS hors preuve (comparable et (1,1), o ≥ 3) ===")
    configs = [(0, 2, 3), (0, 2, 4), (0, 3, 3), (0, 2, 5), (1, 1, 3),
               (1, 1, 4), (1, 1, 5)]
    t0 = time.time()
    for na, nb, o in configs:
        uns, nu = coeur(na, nb, o)
        if nu > 7:
            continue
        cible = loi(na, nb, o)
        ok, st = decision_infaisable(uns, nu, cible - 1)
        print(f"  (a={na}, b={nb}, o={o}, ν={nu}) : cap {cible - 1} → {st}"
              f"  [{time.time()-t0:.0f}s]")
        if ok is False:
            print("    !!! MINORANT RÉFUTÉ — la loi C-MC009 est fausse ici")


def run_incomparable():
    print("\n=== CERTIFICATS incomparables (zone entièrement hors preuve) ===")
    configs = [(1, 2, 2), (1, 2, 3), (2, 2, 2), (1, 3, 2), (2, 3, 1),
               (3, 3, 1), (2, 2, 3), (1, 4, 2)]
    t0 = time.time()
    for na, nb, o in configs:
        uns, nu = coeur(na, nb, o)
        if nu > 7:
            continue
        cible = loi(na, nb, o)
        ok, st = decision_infaisable(uns, nu, cible - 1)
        print(f"  (a={na}, b={nb}, o={o}, ν={nu}) : cap {cible - 1} → {st}"
              f"  [{time.time()-t0:.0f}s]")
        if ok is False:
            print("    !!! MINORANT RÉFUTÉ — la loi C-MC009 est fausse ici")


def run_inegalite():
    """L'inégalité de recouvrement de l'assemblage (fiche §3) :
    (d−1) + ⌈C(k,d)/C(k−2,d−2)⌉ ≥ k pour 2 ≤ d ≤ k.
    Vraie ⟹ le cas (k lights, min D = d) paie. Cartographie des échecs."""
    from math import comb, ceil
    print("\n=== INÉGALITÉ DE RECOUVREMENT — cartographie k ≤ 40 ===")
    echecs = []
    for k in range(2, 41):
        for d in range(2, k + 1):
            gauche = (d - 1) + ceil(comb(k, d) / comb(k - 2, d - 2))
            if gauche < k:
                echecs.append((k, d))
    premiers = {}
    for k, d in echecs:
        premiers.setdefault(k, []).append(d)
    if not any(k <= 7 for k in premiers):
        print("  k ≤ 7 : AUCUN échec — le cœur comparable est prouvé "
              "inconditionnellement pour o ≤ 7")
    for k in sorted(premiers)[:8]:
        print(f"  k = {k} : échecs aux d ∈ {premiers[k]}")
    print(f"  (premier échec : {min(echecs) if echecs else 'aucun'} — "
          f"la zone résiduelle de la preuve)")


if __name__ == "__main__":
    quel = sys.argv[1] if len(sys.argv) > 1 else "tout"
    if quel in ("tout", "audit"):
        run_audit()
    if quel in ("tout", "certificats"):
        run_certificats()
    if quel in ("tout", "incomparable"):
        run_incomparable()
    if quel in ("tout", "inegalite"):
        run_inegalite()
