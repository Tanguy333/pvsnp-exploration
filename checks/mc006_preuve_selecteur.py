# -*- coding: utf-8 -*-
"""MC-006 — Vérification adverse du théorème de super-additivité du sélecteur.

THÉORÈME (fiche tasks/done/MC-006.md) :
  (i)  [fibres à blocs disjoints] Si h, sur Z ⊔ X₁ ⊔ … ⊔ X_k (blocs
       disjoints), vérifie h(σᵢ, 0, …, xᵢ, …, 0) = fᵢ(xᵢ) pour des motifs
       σᵢ ∈ {0,1}^Z distincts (h ARBITRAIRE partout ailleurs), alors
       W(h) ≥ Σᵢ W(fᵢ).
  (ii) [strict, MUX 1 bit] h(1,x,y) = f(x), h(0,x,y) = g(y), f et g non
       constantes ⟹ W(h) ≥ W(f) + W(g) + 1.
  (iii)[serrage] +1 est atteint (21/105 paires à 2+2).

Ce script tente de FALSIFIER le théorème (rôle adverse) :
  T1 : le point 1+1 (MUX(id, id) sur 3 variables) — valeur exacte attendue 3.
  T2 : exhaustif 2+2 (105 paires) — assertion W ≥ somme + 1, comptage des
       écarts (doit reproduire la distribution MC-005), un témoin de +1.
  T3 : LE TEST DUR — (i) avec tranches-poubelle : sélecteur à 2 bits,
       h ALÉATOIRE partout sauf les deux tranches réalisantes
       (z=(1,1), y=0) → f et (z=(0,0), x=0) → g ; assertion W ≥ W(f)+W(g).
       Toute violation réfuterait le théorème (i).
  T4 : MUX 2+3 aléatoire — assertion W ≥ somme + 1 hors de l'espace 2+2.

W exact : force brute (≤ 4 vars) / CP-SAT canal de valeurs (5-6 vars,
OPTIMAL exigé, témoin re-vérifié). Graine fixée : 20260807.
"""
import random
import sys
import time
from itertools import combinations_with_replacement

from ortools.sat.python import cp_model


def W_brute(uns, nvars, cap):
    N = 1 << nvars
    su = set(uns)
    monomes = list(range(1, N))
    for s in range(0, cap + 1):
        for combo in combinations_with_replacement(monomes, s):
            coeffs = {}
            for S in combo:
                coeffs[S] = coeffs.get(S, 0) + 1
            v1, v0 = set(), set()
            ok = True
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
            if ok:
                return s
    return None


def W_cpsat(uns, nvars, cap, tl=300):
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
    model.Minimize(tot)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tl
    solver.parameters.num_search_workers = 8
    st = solver.Solve(model)
    if st != cp_model.OPTIMAL:
        return None, str(st)
    temoin = {S: solver.Value(a[S]) for S in monomes if solver.Value(a[S])}
    su = set(uns)
    v1, v0 = set(), set()
    for x in range(N):
        p = sum(c for S, c in temoin.items() if S & x == S)
        (v1 if x in su else v0).add(p)
    assert not (v1 & v0) and sum(temoin.values()) == solver.Value(tot)
    return solver.Value(tot), "OPTIMAL"


def W_exact(uns, nvars, tl=300):
    cap = (1 << nvars) - 1
    if nvars <= 4:
        return W_brute(uns, nvars, cap), "BRUTE"
    return W_cpsat(uns, nvars, cap, tl)


def uns_de(masque, n):
    return [x for x in range(1 << n) if masque >> x & 1]


def mux(mf, nf, mg, ng):
    uns = []
    for z in (0, 1):
        for y in range(1 << ng):
            for x in range(1 << nf):
                v = (mf >> x & 1) if z else (mg >> y & 1)
                if v:
                    uns.append(x | (y << nf) | (z << (nf + ng)))
    return uns


def t1():
    ident = 2  # sur 1 variable : f(0)=0, f(1)=1
    w, st = W_exact(mux(ident, 1, ident, 1), 3)
    print(f"T1 — W(MUX(id, id)) sur 3 variables = {w} [{st}] ; "
          f"somme + 1 = 3 ; {'CONFORME (borne stricte atteinte)' if w == 3 else 'A EXAMINER'}")
    assert w >= 3


def t2():
    fs = list(range(1, 15))
    W2 = {m: W_brute(uns_de(m, 2), 2, 15) for m in fs}
    ecarts, temoin_plus1 = {}, None
    t0 = time.time()
    for i, mf in enumerate(fs):
        for mg in fs[i:]:
            somme = W2[mf] + W2[mg]
            w, st = W_exact(mux(mf, 2, mg, 2), 5)
            assert st == "OPTIMAL"
            assert w >= somme + 1, f"FALSIFIE (ii) : f={mf}, g={mg}, W={w} < {somme+1}"
            e = w - somme
            ecarts[e] = ecarts.get(e, 0) + 1
            if e == 1 and temoin_plus1 is None:
                temoin_plus1 = (mf, mg, w, somme)
    print(f"T2 — 105/105 paires 2+2 : W ≥ somme + 1 PARTOUT "
          f"[{time.time()-t0:.0f}s] ; distribution {dict(sorted(ecarts.items()))} ; "
          f"témoin du serrage +1 : f={temoin_plus1[0]}, g={temoin_plus1[1]} → "
          f"W = {temoin_plus1[2]} = {temoin_plus1[3]}+1")
    assert ecarts.get(1, 0) == 21, "distribution différente de MC-005"


def t3(n_instances=12):
    rng = random.Random(20260807)
    t0 = time.time()
    for k in range(n_instances):
        mf = rng.randrange(1, 15)   # f non constante sur 2 vars
        mg = rng.randrange(1, 15)
        wf, wg = W_brute(uns_de(mf, 2), 2, 15), W_brute(uns_de(mg, 2), 2, 15)
        # variables : x (bits 0-1), y (bits 2-3), z (bits 4-5)
        uns = set()
        for pt in range(64):
            x, y, z = pt & 3, (pt >> 2) & 3, (pt >> 4) & 3
            if z == 3 and y == 0:          # tranche (z=(1,1), y=0) -> f(x)
                v = mf >> x & 1
            elif z == 0 and x == 0:        # tranche (z=(0,0), x=0) -> g(y)
                v = mg >> y & 1
            else:                          # POUBELLE : aléatoire
                v = rng.randrange(2)
            if v:
                uns.add(pt)
        w, st = W_exact(sorted(uns), 6, tl=600)
        assert st == "OPTIMAL", f"instance {k} non conclue ({st})"
        assert w >= wf + wg, (f"FALSIFIE (i) : instance {k}, f={mf}, g={mg}, "
                              f"W={w} < {wf}+{wg}")
        print(f"  T3.{k} : f={mf} (W={wf}), g={mg} (W={wg}), tranches-poubelle "
              f"aléatoires → W(h) = {w} ≥ {wf+wg}  [{time.time()-t0:.0f}s]")
    print(f"T3 — {n_instances}/{n_instances} instances à tranches-poubelle : "
          f"W ≥ W(f) + W(g) PARTOUT — la borne (i) survit à la falsification")


def t4(n_paires=15):
    rng = random.Random(20260807)
    t0 = time.time()
    W3 = {}
    for k in range(n_paires):
        mf = rng.randrange(1, 15)
        mg = rng.randrange(1, 255)
        if mg in (0, 255):
            continue
        wf = W_brute(uns_de(mf, 2), 2, 15)
        if mg not in W3:
            W3[mg] = W_brute(uns_de(mg, 3), 3, 63)
        wg = W3[mg]
        w, st = W_exact(mux(mf, 2, mg, 3), 6, tl=600)
        assert st == "OPTIMAL"
        assert w >= wf + wg + 1, (f"FALSIFIE (ii) hors 2+2 : f={mf}, g={mg}, "
                                  f"W={w} < {wf+wg+1}")
        print(f"  T4.{k} : MUX 2+3, f={mf} (W={wf}), g={mg} (W={wg}) → "
              f"W = {w} ≥ {wf+wg+1}  [{time.time()-t0:.0f}s]")
    print(f"T4 — MUX 2+3 aléatoires : W ≥ somme + 1 PARTOUT")


if __name__ == "__main__":
    quel = sys.argv[1] if len(sys.argv) > 1 else "tout"
    if quel in ("tout", "t1"):
        t1()
    if quel in ("tout", "t2"):
        t2()
    if quel in ("tout", "t3"):
        t3()
    if quel in ("tout", "t4"):
        t4()
    print("\nAUCUNE FALSIFICATION : le théorème MC-006 survit à la batterie.")
