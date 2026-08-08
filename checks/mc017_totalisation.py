# -*- coding: utf-8 -*-
r"""MC-017 — La brique de totalisation minimale (le premier pas du
chaînon compression).

Contexte : MC-016 a établi que l'additivité de W n'existe qu'en blocs
DISJOINTS (sélecteur MC-006) — à l'échelle de compression (ν = O(log n))
le schéma n'a droit qu'à O(log) gadgets-fibres : il lui faut un
mécanisme GLOBAL. Le candidat minimal, la forme du Th.16 de HOS18
réduite à l'os : UN bit de sélection y, h(1, x) = f₀(x) (la complétion
∗→0), h(0, x) = 𝟙_∗(x) (l'indicatrice des don't-cares).

Objets, pour une instance partielle (U, B = {0}) sur s bits
(le format Th.2 de MC-001 : points listés) :
- W_partiel : min Σ a_S sous les seules contraintes val[u] ≠ val[b],
  u ∈ U, b ∈ B (les ∗ libres) — LA mesure que la NP-dureté partielle
  contrôle ;
- complétions : f₀ (∗→0), f₁ (∗→1), et le min sur TOUTES les
  complétions (exhaustif si |∗| ≤ 6, sinon échantillon) ;
- la totalisation MUX : h sur s+1 bits ci-dessus — W(h) contre le
  plancher MC-006 (W(f₀) + W(𝟙_∗) + 1) et la lecture de W_partiel.

Questions : Q0 — W_partiel = min-complétions ? (sinon, l'écart des
deux mesures est le premier obstacle du chaînon) ; Q1 — surcoût des
complétions canoniques ; Q2 — l'écart de couplage
δ = W(h) − (W(f₀) + W(𝟙_∗) + 1).
"""
import sys
import time
from itertools import combinations

from ortools.sat.python import cp_model


def W_solve(uns, zeros, nvars, tl=600):
    """W exact avec contraintes uns × zeros SEULES (partiel si
    uns ∪ zeros ne couvre pas le cube). OPTIMAL exigé, témoin vérifié."""
    N = 1 << nvars
    cap = N - 1
    monomes = list(range(1, N))
    model = cp_model.CpModel()
    a = {S: model.NewIntVar(0, cap, f"a{S}") for S in monomes}
    tot = model.NewIntVar(0, cap, "tot")
    model.Add(tot == sum(a.values()))
    val = {}
    for x in set(uns) | set(zeros):
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
        return None, solver.StatusName(st)
    temoin = {S: solver.Value(a[S]) for S in monomes if solver.Value(a[S])}
    pv = lambda x: sum(c for S, c in temoin.items() if S & x == S)
    v1 = {pv(u) for u in uns}
    v0 = {pv(z) for z in zeros}
    assert not (v1 & v0) and sum(temoin.values()) == solver.Value(tot)
    return solver.Value(tot), "OPTIMAL"


def W_total(uns, nvars, tl=600):
    N = 1 << nvars
    su = set(uns)
    return W_solve(sorted(su), [x for x in range(N) if x not in su],
                   nvars, tl)


def instance(nom, s, U):
    N = 1 << s
    U = sorted(set(U))
    stars = [x for x in range(1, N) if x not in set(U)]
    t0 = time.time()
    wp, st1 = W_solve(U, [0], s)
    wf0, st2 = W_total(U, s)
    wf1, st3 = W_total(U + stars, s)
    wind, st4 = W_total(stars, s)
    assert "OPTIMAL" == st1 == st2 == st3 == st4
    # Q0 : min sur les complétions (S1 = les étoiles envoyées sur 1)
    borne = f">= {wp} (= W_partiel, trivial)"
    if len(stars) <= 6:
        meilleurs = []
        for r in range(len(stars) + 1):
            for S1 in combinations(stars, r):
                w, st = W_total(U + list(S1), s)
                assert st == "OPTIMAL"
                meilleurs.append(w)
        mc = min(meilleurs)
        borne = (f"= {mc} EXHAUSTIF ({len(meilleurs)} complétions ; "
                 f"atteint {meilleurs.count(mc)} fois)")
    # Q2 : la totalisation MUX — y = bit haut ; y=1 : f0, y=0 : indicatrice
    y = 1 << s
    uns_h = [u | y for u in U] + stars
    wh, st5 = W_total(uns_h, s + 1)
    assert st5 == "OPTIMAL"
    plancher = wf0 + wind + 1
    # NB : somme+1 n'est un PLANCHER (MC-006) que pour des bras sur blocs
    # DISJOINTS — ici les deux bras PARTAGENT x : simple référence.
    print(f"  {nom:14} s={s} |U|={len(U)} |*|={len(stars)} : "
          f"W_partiel={wp}, W(f0)={wf0}, W(f1)={wf1}, W(ind*)={wind} ; "
          f"min-completions {borne} ; "
          f"W(MUX)={wh} vs ref somme+1={plancher} (pas un plancher : "
          f"espace partage) : delta={wh - plancher:+d}"
          f"  [{time.time() - t0:.0f}s]")


if __name__ == "__main__":
    quel = sys.argv[1] if len(sys.argv) > 1 else "tout"
    if quel in ("tout", "s3"):
        print("=== S3 — Q0 exhaustif (|*| <= 6) ===")
        instance("I0a paires", 3, [0b011, 0b101])
        instance("I0b sing+paire", 3, [0b001, 0b110])
        instance("I0c triangle", 3, [0b011, 0b101, 0b110])
    if quel in ("tout", "s4"):
        print("=== S4 — instances Th.2 (points listés) ===")
        instance("I1 triangle", 4, [0b0011, 0b0101, 0b0110])
        instance("I2 singletons", 4, [0b0001, 0b0010, 0b0100, 0b1000])
        instance("I3 mixte", 4, [0b0011, 0b1100, 0b0101])
        instance("I4 triples", 4, [0b0111, 0b1011, 0b1101, 0b1110])
    if quel in ("tout", "s5"):
        print("=== S5 — contrôles d'échelle ===")
        instance("I5 etoile", 5, [0b00011, 0b00101, 0b01001, 0b10001])
        instance("I6 mixte", 5, [0b00111, 0b11001, 0b10110])
