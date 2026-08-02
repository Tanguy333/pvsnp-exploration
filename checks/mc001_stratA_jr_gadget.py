"""MC-001, strategie A (adapter Hirahara-Ilango-Loff) — etape 1 : validation
du gadget de Jiang-Ravikumar reconstruit depuis la figure du PDF
(bib/pdf/hirahara_ilango_focs2025.pdf, page 2, rendue en PNG et lue).

Gadget pour l'arete e={u,v}, u<v (indices de colonnes gadget 1..5) :
  - lignes-sommets : (u,0)->1 en (e,1) ; (u,1)->1 en (e,2) ;
                     (v,1)->1 en (e,3) ; (v,0)->1 en (e,4).
  - lignes gadget  : (e,1)->{1,3,5} ; (e,2)->{1,4,5} ;
                     (e,3)->{2,3,5} ; (e,4)->{2,4,5}.
  - bloc haut-gauche : (i,b) -> 1 en colonne i, pour tout i,b.

VALIDATION : chi_1(f_G) doit valoir n + 4|E| + kappa(G) (HIL / JR Lemme 3.3).
chi_1 est calcule EXACTEMENT par CP-SAT (partition des uns en rectangles
1-monochromatiques, clot par paires — la cloture par paires suffit :
si toute paire d'une classe a ses deux croisements DANS la classe, la classe
est un rectangle complet), puis RE-VERIFIE par un verificateur independant.
"""

from __future__ import annotations

import itertools
import sys
import time

from ortools.sat.python import cp_model


# ---------------------------------------------------------------- construction
def build_fG(n, edges):
    """Matrice f_G de JR/HIL. Lignes : (i,0),(i,1) pour i=1..n puis
    (e,1..4) par arete ; colonnes : 1..n puis (e,1..5) par arete."""
    edges = [tuple(sorted(e)) for e in edges]
    R = 2 * n + 4 * len(edges)
    C = n + 5 * len(edges)
    M = [[0] * C for _ in range(R)]
    row_v = lambda i, b: 2 * (i - 1) + b            # sommet i in 1..n
    row_e = lambda k, r: 2 * n + 4 * k + (r - 1)     # arete k (0-based), r in 1..4
    col_v = lambda i: i - 1
    col_e = lambda k, c: n + 5 * k + (c - 1)         # c in 1..5
    for i in range(1, n + 1):
        M[row_v(i, 0)][col_v(i)] = 1
        M[row_v(i, 1)][col_v(i)] = 1
    for k, (u, v) in enumerate(edges):
        M[row_v(u, 0)][col_e(k, 1)] = 1
        M[row_v(u, 1)][col_e(k, 2)] = 1
        M[row_v(v, 1)][col_e(k, 3)] = 1
        M[row_v(v, 0)][col_e(k, 4)] = 1
        for r, cols in ((1, (1, 3, 5)), (2, (1, 4, 5)),
                        (3, (2, 3, 5)), (4, (2, 4, 5))):
            for c in cols:
                M[row_e(k, r)][col_e(k, c)] = 1
    return M


def kappa(n, edges):
    """Couverture de sommets minimale, force brute."""
    edges = [tuple(sorted(e)) for e in edges]
    for k in range(0, n + 1):
        for comb in itertools.combinations(range(1, n + 1), k):
            s = set(comb)
            if all(u in s or v in s for u, v in edges):
                return k
    return n


# ---------------------------------------------------------------- chi_1 exact
def chi1_exact(M, kmax, tl=300.0):
    """Partition minimale des uns en rectangles 1-monochromatiques.
    Modele : couleur de chaque un ; cloture par paires. Retourne (chi1,
    classes) avec preuve d'optimalite exigee, ou (None, msg)."""
    R, C = len(M), len(M[0])
    ones = [(r, c) for r in range(R) for c in range(C) if M[r][c]]
    m = len(ones)
    idx = {o: i for i, o in enumerate(ones)}
    model = cp_model.CpModel()
    x = [[model.NewBoolVar(f"x{i}_{t}") for t in range(kmax)] for i in range(m)]
    for i in range(m):
        model.AddExactlyOne(x[i])
        for t in range(i + 1, kmax):     # precedence : le un i n'utilise que t <= i
            model.Add(x[i][t] == 0)
    for i, (r1, c1) in enumerate(ones):
        for j in range(i + 1, m):
            r2, c2 = ones[j]
            if r1 == r2 or c1 == c2:
                continue
            if M[r1][c2] == 0 or M[r2][c1] == 0:   # incompatibles
                for t in range(min(j + 1, kmax)):
                    model.AddBoolOr([x[i][t].Not(), x[j][t].Not()])
            else:                                   # cloture : les croisements suivent
                k1, k2 = idx[(r1, c2)], idx[(r2, c1)]
                for t in range(kmax):
                    if t <= j:
                        if t <= k1:
                            model.AddBoolOr([x[i][t].Not(), x[j][t].Not(), x[k1][t]])
                        if t <= k2:
                            model.AddBoolOr([x[i][t].Not(), x[j][t].Not(), x[k2][t]])
    used = [model.NewBoolVar(f"u{t}") for t in range(kmax)]
    for t in range(kmax):
        for i in range(m):
            model.AddImplication(x[i][t], used[t])
    for t in range(kmax - 1):
        model.AddImplication(used[t + 1], used[t])
    model.Minimize(sum(used))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tl
    solver.parameters.num_search_workers = 8
    st = solver.Solve(model)
    if st != cp_model.OPTIMAL:
        return None, f"statut={solver.StatusName(st)} (pas OPTIMAL)"
    classes = {}
    for i, o in enumerate(ones):
        for t in range(kmax):
            if solver.Value(x[i][t]):
                classes.setdefault(t, []).append(o)
    return int(solver.ObjectiveValue()), list(classes.values())


def verifie_partition(M, classes):
    """Verificateur independant : classes disjointes, couvrant tous les uns,
    chaque classe = rectangle COMPLET A x B tout-uns."""
    R, C = len(M), len(M[0])
    ones = {(r, c) for r in range(R) for c in range(C) if M[r][c]}
    vus = set()
    for cl in classes:
        A = sorted({r for r, _ in cl})
        B = sorted({c for _, c in cl})
        if set(cl) != {(r, c) for r in A for c in B}:
            return False, f"classe non rectangulaire : {cl}"
        for r in A:
            for c in B:
                if M[r][c] != 1:
                    return False, f"entree 0 dans un rectangle : {(r, c)}"
        if vus & set(cl):
            return False, "classes non disjointes"
        vus |= set(cl)
    if vus != ones:
        return False, f"uns non couverts : {ones - vus}"
    return True, "OK"


# ---------------------------------------------------------------------- main
GRAPHES = {
    "K2":      (2, [(1, 2)]),
    "P3":      (3, [(1, 2), (2, 3)]),
    "K3":      (3, [(1, 2), (1, 3), (2, 3)]),
    "2K2":     (4, [(1, 2), (3, 4)]),
}

def main():
    noms = sys.argv[1:] or ["K2", "P3"]
    for nom in noms:
        n, edges = GRAPHES[nom]
        M = build_fG(n, edges)
        k = kappa(n, edges)
        attendu = n + 4 * len(edges) + k
        R, C = len(M), len(M[0])
        uns = sum(map(sum, M))
        print(f"\n=== {nom} : n={n}, |E|={len(edges)}, kappa={k} — "
              f"matrice {R}x{C}, {uns} uns — chi_1 attendu = {attendu}", flush=True)
        t0 = time.time()
        chi1, classes = chi1_exact(M, kmax=attendu + 2, tl=600.0)
        if chi1 is None:
            print(f"  chi_1 NON CONCLU : {classes}", flush=True)
            continue
        ok, msg = verifie_partition(M, classes)
        verdict = "CONFORME" if chi1 == attendu else "ECART !"
        print(f"  chi_1 (CP-SAT optimal) = {chi1}  [{verdict}]  "
              f"re-verification independante : {msg}  ({time.time()-t0:.0f}s)",
              flush=True)


if __name__ == "__main__":
    main()
