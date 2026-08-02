"""MC-001 — REFUTATION, partie 2 (CP-SAT, encodages INDEPENDANTS des attaques).

  A : f_G(K2) reconstruit PAR MOI depuis la figure (lue sur PNG, page 2 HIL) ;
      indexation binaire naturelle (lignes = 3 bits hauts, colonnes = 3 bits bas,
      colonne 7 = bourrage 0). Verifs : f(0)=1, f(1^6)=0, 20 uns,
      0 implicant positif. Puis W : mon modele = disequations PAR PAIRES
      (880 contraintes v[un] != v[zero]), PAS le canal AddElement des attaques.
      Test 1 : faisable a poids <= 19 (temoin re-verifie sans solveur).
      Test 2 : INFAISABLE a poids <= 18 (assertion de solveur, consignee comme telle).
  B : chi_1(f_G(K2)) par COUVERTURE EXACTE sur la liste ENUMEREE des rectangles
      1-monochromatiques (autre modele que l'affectation+cloture des attaques).
      Test : optimum = 7 = n + 4|E| + kappa (JR Lemme 3.3), partition re-verifiee.
  C : (spot) permutation seed 3 des attaques : W = 16 ? (faisable 16 / infaisable 15)
"""
from __future__ import annotations
import itertools, random, sys, time
from ortools.sat.python import cp_model

# ------------------------------------------------- f_G depuis la figure (relue)
def build_fG_moi(n, edges):
    edges = [tuple(sorted(e)) for e in edges]
    R, C = 2 * n + 4 * len(edges), n + 5 * len(edges)
    M = [[0] * C for _ in range(R)]
    for i in range(1, n + 1):                     # bloc haut-gauche
        M[2 * (i - 1)][i - 1] = 1                 # (i,0) -> col i
        M[2 * (i - 1) + 1][i - 1] = 1             # (i,1) -> col i
    for k, (u, v) in enumerate(edges):
        cg = lambda c: n + 5 * k + (c - 1)
        rg = lambda r: 2 * n + 4 * k + (r - 1)
        M[2 * (u - 1)][cg(1)] = 1                 # (u,0) -> col gadget 1
        M[2 * (u - 1) + 1][cg(2)] = 1             # (u,1) -> col 2
        M[2 * (v - 1) + 1][cg(3)] = 1             # (v,1) -> col 3
        M[2 * (v - 1)][cg(4)] = 1                 # (v,0) -> col 4
        for r, cols in ((1, (1, 3, 5)), (2, (1, 4, 5)),
                        (3, (2, 3, 5)), (4, (2, 4, 5))):
            for c in cols:
                M[rg(r)][cg(c)] = 1
    return M

def encode(M, perm_r=None, perm_c=None):
    R, C = len(M), len(M[0])
    rb = max(1, (R - 1).bit_length())
    cb = max(1, (C - 1).bit_length())
    perm_r = perm_r or list(range(R))
    perm_c = perm_c or list(range(C))
    m = rb + cb
    f = [0] * (1 << m)
    for r in range(R):
        for c in range(C):
            if M[r][c]:
                f[(perm_r[r] << cb) | perm_c[c]] = 1
    return f, m

def implicants_positifs(f, m):
    N = 1 << m
    out = []
    for S in range(1, N):
        if all(f[x] for x in range(N) if (x & S) == S):
            out.append(S)
    return out

# ------------------------------------------------- W : modele par disequations
def W_faisable(f, m, budget, tl=600.0):
    """Existe-t-il un separateur de poids total <= budget ?
    Modele : a[S] entiers >= 0, somme <= budget, v[x] = somme des a actifs,
    v[un] != v[zero] PAR PAIRES. Retourne (statut, sol)."""
    N = 1 << m
    model = cp_model.CpModel()
    a = {S: model.NewIntVar(0, budget, f"a{S}") for S in range(1, N)}
    model.Add(sum(a.values()) <= budget)
    v = []
    for x in range(N):
        vx = model.NewIntVar(0, budget, f"v{x}")
        expr = [a[S] for S in range(1, N) if (x & S) == S]
        model.Add(vx == sum(expr) if expr else vx == 0)
        v.append(vx)
    ones = [x for x in range(N) if f[x]]
    zeros = [x for x in range(N) if not f[x]]
    for o in ones:
        for z in zeros:
            model.Add(v[o] != v[z])
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tl
    solver.parameters.num_search_workers = 8
    st = solver.Solve(model)
    nom = solver.StatusName(st)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        sol = {S: solver.Value(a[S]) for S in range(1, N) if solver.Value(a[S])}
        # re-verification SANS solveur
        vu, vz = set(), set()
        for x in range(N):
            val = sum(c for S, c in sol.items() if (x & S) == S)
            (vu if f[x] else vz).add(val)
        assert not (vu & vz), "ECHEC re-verification !"
        return nom, (sol, sorted(vu), sorted(vz))
    return nom, None

# ------------------------------------------------- chi_1 : couverture exacte
def chi1_exact_cover(M, kmax, tl=600.0):
    R, C = len(M), len(M[0])
    ones = [(r, c) for r in range(R) for c in range(C) if M[r][c]]
    idx = {o: i for i, o in enumerate(ones)}
    # enumere TOUS les rectangles 1-monochromatiques (A x B, non vides)
    rects = set()
    lignes_uns = {r: frozenset(c for c in range(C) if M[r][c]) for r in range(R)}
    rows_nonvides = [r for r in range(R) if lignes_uns[r]]
    for k in range(1, len(rows_nonvides) + 1):
        for A in itertools.combinations(rows_nonvides, k):
            Bmax = frozenset.intersection(*(lignes_uns[r] for r in A))
            if not Bmax:
                continue
            for kb in range(1, len(Bmax) + 1):
                for B in itertools.combinations(sorted(Bmax), kb):
                    rects.add((A, B))
    rects = sorted(rects)
    model = cp_model.CpModel()
    x = [model.NewBoolVar(f"r{i}") for i in range(len(rects))]
    par_un = {i: [] for i in range(len(ones))}
    for j, (A, B) in enumerate(rects):
        for r in A:
            for c in B:
                par_un[idx[(r, c)]].append(x[j])
    for i in range(len(ones)):
        model.AddExactlyOne(par_un[i])            # PARTITION exacte
    model.Minimize(sum(x))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tl
    solver.parameters.num_search_workers = 8
    st = solver.Solve(model)
    if st != cp_model.OPTIMAL:
        return None, solver.StatusName(st), len(rects)
    chois = [rects[j] for j in range(len(rects)) if solver.Value(x[j])]
    # re-verification independante
    vus = set()
    for A, B in chois:
        for r in A:
            for c in B:
                assert M[r][c] == 1 and (r, c) not in vus
                vus.add((r, c))
    assert vus == set(ones)
    return int(solver.ObjectiveValue()), "OPTIMAL+re-verifie", len(rects)

# ---------------------------------------------------------------------- main
def main():
    quoi = sys.argv[1:] or ["A", "B"]
    n, edges = 2, [(1, 2)]
    M = build_fG_moi(n, edges)
    f, m = encode(M)
    if "A" in quoi:
        print(f"A : matrice {len(M)}x{len(M[0])}, m={m}, N={1 << m}, "
              f"uns={sum(f)}, f(0)={f[0]}, f(1^m)={f[-1]}, "
              f"implicants positifs={len(implicants_positifs(f, m))}", flush=True)
        t0 = time.time()
        st19, sol19 = W_faisable(f, m, 19, tl=600.0)
        print(f"   budget 19 : {st19} ({time.time()-t0:.0f}s)"
              + (f" — poids={sum(sol19[0].values())}, uns={sol19[1]}, zeros={sol19[2]}"
                 if sol19 else ""), flush=True)
        t0 = time.time()
        st18, _ = W_faisable(f, m, 18, tl=600.0)
        print(f"   budget 18 : {st18} ({time.time()-t0:.0f}s) "
              f"[INFEASIBLE attendu — assertion de solveur, consignee]", flush=True)
    if "B" in quoi:
        t0 = time.time()
        chi1, msg, nrect = chi1_exact_cover(M, kmax=9, tl=600.0)
        print(f"B : chi_1(f_G(K2)) = {chi1} [{msg}] — {nrect} rectangles enumeres, "
              f"attendu 7 = 2 + 4 + 1 ({time.time()-t0:.0f}s)", flush=True)
    if "C" in quoi:
        rng = random.Random(3)
        pr = list(range(len(M))); rng.shuffle(pr)
        pc = list(range(len(M[0]))); rng.shuffle(pc)
        fp, mp = encode(M, pr, pc)
        t0 = time.time()
        st16, sol16 = W_faisable(fp, mp, 16, tl=600.0)
        st15, _ = W_faisable(fp, mp, 15, tl=600.0)
        print(f"C : seed 3 — budget 16 : {st16}, budget 15 : {st15} "
              f"(attendu FEASIBLE/INFEASIBLE ; {time.time()-t0:.0f}s)", flush=True)

if __name__ == "__main__":
    main()
