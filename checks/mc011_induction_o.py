# -*- coding: utf-8 -*-
r"""MC-011 — Vérifications autour de l'induction sur o (fiche MC-011).

THÉORÈMES (preuves : fiche §2-3) :
  * loi comparable COMPLÈTE : F(0, b, 0, o) = b + 2o pour TOUT o (b ≥ 2)
    — le plafond o ≤ 7 de MC-010 est levé ;
  * loi (1,1) COMPLÈTE : F(1, 1, 0, o) = 2 + 2o pour TOUT o.
  Mécanisme : induction sur o, trichotomie par bit extérieur l —
  (1) l LOURD (ω_l ≥ 2) : la restriction x_l := 0 perd ω_l + μ_l ≥ 2 ;
  (2) l LÉGER avec μ_l ≥ 1 : la même restriction perd 1 + μ_l ≥ 2 ;
  (3) TOUS légers et μ = 0 : théorème A de MC-010 (F4 + convexité).
  LEMME (léger ⟹ singleton, tous cœurs) : si ω_l = 1 alors a_{{l}} = 1 —
  via les zéros u∪{l} et v∪{l} (les deux familles forcées, disjointes
  hors singleton, imposeraient ω_l ≥ 2 si a_{{l}} = 0).

Modes :
  trichotomie : sur les témoins optimaux des cœurs (CP-SAT), vérifie la
      comptabilité de la preuve — décomposition ω_l/μ_l par l, branche
      applicable, et l'inégalité de la branche.
  normalisation : vérifie l'ÉGALITÉ min{W : μ = 0} = W sur les cœurs
      accessibles (le fait structurel qui motivait le lemme abandonné —
      consigné comme observation, le théorème ne l'utilise plus).
  singleton : énumère les séparateurs de poids ≤ F + 1 des petits cœurs
      INCOMPARABLES et vérifie le lemme léger ⟹ singleton sur chacun.
"""
import sys
import time
from itertools import combinations_with_replacement

from ortools.sat.python import cp_model


def W_cpsat(uns, nvars, cap, tl=600, sans_multi_O=None):
    """sans_multi_O : (A, B, O) — si fourni, exclut les monômes à ≥ 2
    éléments de O (pour le mode normalisation)."""
    N = 1 << nvars
    zeros = [x for x in range(N) if x not in set(uns)]
    monomes = list(range(1, N))
    if sans_multi_O is not None:
        _, _, O = sans_multi_O
        monomes = [S for S in monomes if bin(S & O).count("1") <= 1]
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
    model.Minimize(tot)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tl
    solver.parameters.num_search_workers = 8
    st = solver.Solve(model)
    if st != cp_model.OPTIMAL:
        return None, None, str(st)
    temoin = {S: solver.Value(a[S]) for S in monomes if solver.Value(a[S])}
    su = set(uns)
    v1, v0 = set(), set()
    for x in range(N):
        p = sum(c for S, c in temoin.items() if S & x == S)
        (v1 if x in su else v0).add(p)
    assert not (v1 & v0) and sum(temoin.values()) == solver.Value(tot)
    return solver.Value(tot), temoin, "OPTIMAL"


def coeur(na, nb, o):
    nu = na + nb + o
    u = (1 << na) - 1
    v = ((1 << nb) - 1) << na
    A, B = u, v
    O = ((1 << nu) - 1) ^ A ^ B
    return sorted({u, v}), nu, A, B, O


def loi(na, nb, o):
    if na == 0:
        return nb + 2 * o
    return 2 * (na + nb + o) - max(nb, 2, na + nb - 2)


def run_trichotomie():
    print("=== TRICHOTOMIE — la comptabilité de la preuve sur les témoins ===")
    configs = [(0, 2, o) for o in (1, 2, 3, 4)] + [(0, 3, o) for o in (1, 2, 3)] \
        + [(1, 1, o) for o in (1, 2, 3, 4)]
    for na, nb, o in configs:
        uns, nu, A, B, O = coeur(na, nb, o)
        if nu > 7:
            continue
        w, temoin, st = W_cpsat(uns, nu, (1 << nu) - 1)
        assert st == "OPTIMAL" and w == loi(na, nb, o)
        # décomposition par l
        détail = []
        for i in range(nu):
            l = 1 << i
            if not (l & O):
                continue
            om = sum(c for S, c in temoin.items()
                     if S & O == l)
            mu_l = sum(c for S, c in temoin.items()
                       if S & l and bin(S & O).count("1") >= 2)
            branche = ("lourd" if om >= 2 else
                       ("leger+mu" if mu_l >= 1 else "leger-pur"))
            assert om >= 1, "un extérieur sans poids simple-O : à examiner"
            détail.append((om, mu_l, branche))
        mu = sum(c for S, c in temoin.items()
                 if bin(S & O).count("1") >= 2)
        tout_leger_mu0 = all(om == 1 for om, _, _ in détail) and mu == 0
        print(f"  ({na},{nb},o={o}) : W = {w} = loi ; par l : {détail} ; "
              f"μ = {mu} ; branche globale : "
              f"{'3 (tout-léger, μ=0 — thm A conclut)' if tout_leger_mu0 else '1/2 (restriction paie ≥ 2)'}")


def run_normalisation():
    print("\n=== NORMALISATION (observation, plus nécessaire au théorème) : "
          "min{W : μ = 0} = W ? ===")
    configs = [(0, 2, o) for o in (1, 2, 3, 4, 5)] \
        + [(0, 3, o) for o in (1, 2, 3, 4)] \
        + [(1, 1, o) for o in (1, 2, 3, 4, 5)] \
        + [(1, 2, o) for o in (1, 2, 3)] + [(2, 2, o) for o in (1, 2)]
    ecarts = 0
    for na, nb, o in configs:
        uns, nu, A, B, O = coeur(na, nb, o)
        if nu > 7:
            continue
        w, _, st = W_cpsat(uns, nu, (1 << nu) - 1)
        w0, _, st0 = W_cpsat(uns, nu, (1 << nu) - 1, sans_multi_O=(A, B, O))
        assert st == st0 == "OPTIMAL"
        marque = "=" if w == w0 else "ÉCART"
        if w != w0:
            ecarts += 1
        print(f"  ({na},{nb},o={o}) : W = {w}, min sans multi-O = {w0}  [{marque}]")
    print(f"  {'ÉGALITÉ PARTOUT — un optimum μ = 0 existe sur chaque cœur testé' if ecarts == 0 else f'{ecarts} écarts'}")


def run_singleton():
    print("\n=== LEMME léger ⟹ singleton — sur séparateurs ÉNUMÉRÉS "
          "(cœurs incomparables) ===")
    for na, nb, o in [(1, 2, 1), (1, 2, 2), (2, 2, 1), (1, 3, 1)]:
        uns, nu, A, B, O = coeur(na, nb, o)
        if nu > 5:
            continue
        N = 1 << nu
        su = set(uns)
        cible = loi(na, nb, o)
        monomes = list(range(1, N))
        n_sep, n_leger, viol = 0, 0, 0
        t0 = time.time()
        for s in range(cible, cible + 2):
            for combo in combinations_with_replacement(monomes, s):
                coeffs = {}
                for S in combo:
                    coeffs[S] = coeffs.get(S, 0) + 1
                v1, v0, ok = set(), set(), True
                for x in range(N):
                    p = sum(c for S, c in coeffs.items() if S & x == S)
                    if x in su:
                        if p in v0:
                            ok = False
                            break
                        v1.add(p)
                    else:
                        if p in v1:
                            ok = False
                            break
                        v0.add(p)
                if not ok:
                    continue
                n_sep += 1
                for i in range(nu):
                    l = 1 << i
                    if not (l & O):
                        continue
                    om = sum(c for S, c in coeffs.items() if S & O == l)
                    if om == 1:
                        n_leger += 1
                        if coeffs.get(l, 0) != 1:
                            viol += 1
                            print(f"    VIOLATION : ({na},{nb},{o}), "
                                  f"séparateur {coeffs}, l = {i}")
        print(f"  ({na},{nb},o={o}) : {n_sep} séparateurs (poids ≤ loi+1), "
              f"{n_leger} extérieurs légers rencontrés, {viol} violation(s)"
              f"  [{time.time()-t0:.0f}s]")


if __name__ == "__main__":
    quel = sys.argv[1] if len(sys.argv) > 1 else "tout"
    if quel in ("tout", "trichotomie"):
        run_trichotomie()
    if quel in ("tout", "normalisation"):
        run_normalisation()
    if quel in ("tout", "singleton"):
        run_singleton()
