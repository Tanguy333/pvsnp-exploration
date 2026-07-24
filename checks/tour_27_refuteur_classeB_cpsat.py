"""
TOUR 27 — suite (T27-S1, Refuteur) : fermeture de la CLASSE B pour
MAJ_5(OR2^5), fenetre [20, 30]. VERSION 4 : CP-SAT canal de valeurs
+ cassage de symetrie lex-leader.

Historique. v1/v2 (DFS) : plafond C=1, W_intra=21 (480 s). v3
(CP-SAT, 97 308 desidentites par paires) : cap 30 SAT verifie en
15 s, mais AUCUNE UNSAT prouvable — meme cap 19 (infaisable par le
theoreme du Tour 26) reste UNKNOWN a 120 s.

v4, deux leviers :
  1. CANAL DE VALEURS : toute valeur est dans [0, cap] ; 30 booleens
     z_v (« v est une valeur-de-1 ») + 1024 contraintes element
     z[val(sigma)] == [m(sigma) >= 3] remplacent les 97 308
     desidentites.
  2. CASSAGE DE SYMETRIE lex-leader : pour chacune des 9 involutions
     generatrices de G = S_5 x S_2^5 (5 swaps x<->y, 4 transpositions
     de blocs adjacents), contrainte vec <=lex g(vec) sur le vecteur
     des 55 coefficients. SOUND : tout temoin a un representant
     lex-minimal d'orbite qui satisfait ces contraintes.
     CALIBRATION OBLIGATOIRE : cap 30 doit rester SAT (temoin
     re-verifie par enumeration) ET cap 19 doit sortir UNSAT
     (theoreme connu du Tour 26 = etalon de l'infaisabilite).

Echelle de caps 19 -> 22 -> 25 -> 27 -> 29 : chaque UNSAT
intermediaire est un theoreme partiel (classe B >= cap+1).
"""

from __future__ import annotations

import itertools
import sys
import time

from ortools.sat.python import cp_model

K, T = 5, 3

# monomes intra : (bloc i, kind) — kind 1 = x_i, 2 = y_i, 3 = x_i y_i
INTRA = [(i, kind) for i in range(K) for kind in (1, 2, 3)]
# monomes croises : (i, vi, j, vj), i < j, vi/vj in {0 (x), 1 (y)}
CROSS = [(i, vi, j, vj)
         for i, j in itertools.combinations(range(K), 2)
         for vi in (0, 1) for vj in (0, 1)]
COORDS = [("i", m) for m in INTRA] + [("c", m) for m in CROSS]
CIDX = {c: n for n, c in enumerate(COORDS)}

SIGMAS = list(itertools.product(range(4), repeat=K))  # 0=00,1=x,2=y,3=xy


def intra_active(kind, st):
    if kind == 1:
        return st in (1, 3)
    if kind == 2:
        return st in (2, 3)
    return st == 3


def cross_active(v, st):
    return (st in (1, 3)) if v == 0 else (st in (2, 3))


def value(sigma, coefs):
    v = 0
    for n, (tag, m) in enumerate(COORDS):
        if tag == "i":
            i, kind = m
            if intra_active(kind, sigma[i]):
                v += coefs[n]
        else:
            i, vi, j, vj = m
            if cross_active(vi, sigma[i]) and cross_active(vj, sigma[j]):
                v += coefs[n]
    return v


def verify(coefs, cap):
    """Re-verification INDEPENDANTE par enumeration complete."""
    if sum(coefs) > cap or any(c < 0 for c in coefs):
        return False
    ones, zeros = set(), set()
    for sigma in SIGMAS:
        m = sum(1 for s in sigma if s)
        (ones if m >= T else zeros).add(value(sigma, coefs))
    return not (ones & zeros)


# ---- involutions generatrices de G et leurs permutations de coords ----

def act_coord(perm, swaps, coord):
    tag, m = coord
    if tag == "i":
        i, kind = m
        nk = kind
        if swaps[i] and kind in (1, 2):
            nk = 3 - kind
        return ("i", (perm[i], nk))
    i, vi, j, vj = m
    ni, nvi = perm[i], vi ^ swaps[i]
    nj, nvj = perm[j], vj ^ swaps[j]
    if ni > nj:
        ni, nvi, nj, nvj = nj, nvj, ni, nvi
    return ("c", (ni, nvi, nj, nvj))


def generators():
    """9 involutions : 5 swaps x<->y, 4 transpositions de blocs."""
    gens = []
    ident = tuple(range(K))
    for i in range(K):
        sw = tuple(1 if a == i else 0 for a in range(K))
        gens.append((ident, sw))
    for i in range(K - 1):
        p = list(range(K))
        p[i], p[i + 1] = p[i + 1], p[i]
        gens.append((tuple(p), (0,) * K))
    return gens


def add_lex_leader(model, cvars, perm, swaps):
    """Contrainte vec <=lex g(vec) pour l'involution g (sound)."""
    pairs = []
    for t, coord in enumerate(COORDS):
        u = CIDX[act_coord(perm, swaps, coord)]
        if u != t:
            pairs.append((t, u))
    prev = None
    for idx, (t, u) in enumerate(pairs):
        a, b = cvars[t], cvars[u]
        if prev is None:
            model.Add(a <= b)
        else:
            model.Add(a <= b).OnlyEnforceIf(prev)
        if idx == len(pairs) - 1:
            break
        eq = model.NewBoolVar("")
        model.Add(a == b).OnlyEnforceIf(eq)
        model.Add(a != b).OnlyEnforceIf(eq.Not())
        if prev is None:
            prev = eq
        else:
            both = model.NewBoolVar("")
            model.AddBoolAnd([prev, eq]).OnlyEnforceIf(both)
            model.AddBoolOr([prev.Not(), eq.Not(), both])
            prev = both


def solve(cap, tl, hint=None, sym=True):
    model = cp_model.CpModel()
    cvars = [model.NewIntVar(0, cap, f"c{n}")
             for n in range(len(COORDS))]
    model.Add(sum(cvars) <= cap)

    z = [model.NewBoolVar(f"z{v}") for v in range(cap + 1)]
    for sigma in SIGMAS:
        terms = []
        for n, (tag, m) in enumerate(COORDS):
            if tag == "i":
                i, kind = m
                if intra_active(kind, sigma[i]):
                    terms.append(cvars[n])
            else:
                i, vi, j, vj = m
                if cross_active(vi, sigma[i]) \
                        and cross_active(vj, sigma[j]):
                    terms.append(cvars[n])
        v = model.NewIntVar(0, cap, "")
        model.Add(v == (sum(terms) if terms else 0))
        one = sum(1 for s in sigma if s) >= T
        model.AddElement(v, z, 1 if one else 0)

    if sym:
        for perm, swaps in generators():
            add_lex_leader(model, cvars, perm, swaps)

    if hint is not None:
        for var, h in zip(cvars, hint):
            model.AddHint(var, h)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tl
    solver.parameters.num_search_workers = 8
    t0 = time.time()
    st = solver.Solve(model)
    dt = time.time() - t0
    if st in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        return "SAT", [solver.Value(v) for v in cvars], dt
    if st == cp_model.INFEASIBLE:
        return "UNSAT", None, dt
    return "UNKNOWN", None, dt


def main():
    budgets = {19: 120.0, 22: 150.0, 25: 200.0, 27: 300.0, 29: 480.0}
    if len(sys.argv) > 1:  # cap unique, budget = argv[2]
        cap = int(sys.argv[1])
        budgets = {cap: float(sys.argv[2]) if len(sys.argv) > 2
                   else 480.0}

    # calibration positive : cap 30 SAT (decomposable (1,1,4)^5),
    # AVEC cassage de symetrie (il doit laisser passer ce temoin)
    hint = [1, 1, 4] * K + [0] * len(CROSS)
    st, sol, dt = solve(30, 60.0, hint=hint, sym=True)
    ok = st == "SAT" and verify(sol, 30)
    print(f"cap=30 : {st} ({dt:.0f}s), enumeration : "
          f"{'OK' if ok else 'ECHEC'}", flush=True)
    if not ok:
        print("MODELE OU SYMETRIE SUSPECT — arret.", flush=True)
        return

    for cap in sorted(budgets):
        st, sol, dt = solve(cap, budgets[cap], sym=True)
        if st == "SAT":
            ok = verify(sol, cap)
            print(f"cap={cap} : TEMOIN ({dt:.0f}s), enumeration : "
                  f"{'OK' if ok else 'ECHEC'}", flush=True)
            if ok:
                intra = [tuple(sol[3 * i:3 * i + 3]) for i in range(K)]
                cross = [(COORDS[n][1], v) for n, v in
                         enumerate(sol) if v and COORDS[n][0] == "c"]
                print(f"  intra : {intra}\n  croises : {cross}",
                      flush=True)
                if cap <= 19:
                    print("CONTREDIT LE TOUR 26 — MODELE SUSPECT.",
                          flush=True)
                return
        elif st == "UNSAT":
            note = " (etalon Tour 26 : attendu)" if cap <= 19 else \
                   f" — THEOREME PARTIEL : classe B >= {cap + 1}"
            print(f"cap={cap} : UNSAT ({dt:.0f}s){note}", flush=True)
        else:
            print(f"cap={cap} : UNKNOWN (budget {budgets[cap]:.0f}s) "
                  f"— echelle arretee ici.", flush=True)
            return


if __name__ == "__main__":
    main()
