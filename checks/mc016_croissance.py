# -*- coding: utf-8 -*-
r"""MC-016 — La loi de croissance du déficit de partage (le verrou
requalifié par MC-015).

Objet : h(x, y) = [y = c_x], base t bits (k = 2^t fibres), fibre s bits
PARTAGÉE, supports c_x distincts. Déficit g := W(h) − Σ_x G(c_x), avec
G(c) = s − |c| + 1 (c ≠ 0), s (c = 0) — la loi prouvée.

Question : |g| suit-il t (bits de base), k (nombre de fibres), s
(largeur de fibre), ou Σ (le poids total) ? MC-015 a mesuré g ≥ −3 à
(t, s) = (2, 4), antichaînes concentrées à g = −2 = t.

Échelles neuves : (2, 5) ν = 7, (2, 6) ν = 8, (3, 5) ν = 8 (k = 8,
antichaîne pleine de paires de [5]), (3, 4) ν = 7 (k = 8,
QUASI-antichaîne : Sperner borne l'antichaîne max de 2^[4] à C(4,2) = 6
< 8 — 6 comparabilités inévitables, consignées comme telles).

Familles structurées suivies à travers les échelles :
- paires en antichaîne (la famille de MC-015) ;
- singletons {0},{1},{2},{3} (antichaîne bon marché, Σ G = 4s) ;
- le tuple de MC-015 PLONGÉ avec bits oisifs (l'effet du s pur) ;
- contrôles : chaîne (affectation alignée et pire), aléatoires.

Cap de recherche : cap = Σ G + 4 (re-solve à 2×(Σ G + 4) si
INFEASIBLE, sinon NON CONCLU) — le minimum trouvé sous cap est le
minimum vrai dès qu'il est ≤ cap. OPTIMAL exigé, témoin re-vérifié.

Modes (jobs courts, chaînables) : base, t2s5, var, t2s6, sing, t3.
"""
import random
import sys
import time

from ortools.sat.python import cp_model


def W_cpsat(uns, nvars, cap, tl=1500):
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
        return None, solver.StatusName(st)
    temoin = {S: solver.Value(a[S]) for S in monomes if solver.Value(a[S])}
    su = set(uns)
    v1, v0 = set(), set()
    for x in range(N):
        p = sum(c for S, c in temoin.items() if S & x == S)
        (v1 if x in su else v0).add(p)
    assert not (v1 & v0) and sum(temoin.values()) == solver.Value(tot)
    return solver.Value(tot), "OPTIMAL"


def loi_G(c, s):
    k = bin(c).count("1")
    return s if k == 0 else s - k + 1


def h_fibres(cs, t, s):
    return sorted({x | (cs[x] << t) for x in range(1 << t)})


def W_cpsat_intervalle(uns, nvars, cap, tl):
    """Comme W_cpsat, mais sur timeout FEASIBLE rend l'intervalle
    [borne inférieure prouvée, meilleur réalisable trouvé]."""
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
    nom_st = solver.StatusName(st)
    if st == cp_model.OPTIMAL:
        temoin = {S: solver.Value(a[S]) for S in monomes if solver.Value(a[S])}
        su = set(uns)
        v1, v0 = set(), set()
        for x in range(N):
            p = sum(c for S, c in temoin.items() if S & x == S)
            (v1 if x in su else v0).add(p)
        assert not (v1 & v0) and sum(temoin.values()) == solver.Value(tot)
        return solver.Value(tot), solver.Value(tot), "OPTIMAL"
    if st == cp_model.FEASIBLE:
        return (int(solver.BestObjectiveBound()),
                int(solver.ObjectiveValue()), nom_st)
    return None, None, nom_st


def mesure(nom, cs, t, s, tl=1500):
    somme = sum(loi_G(c, s) for c in cs)
    cap = somme + 4
    t0 = time.time()
    lo, hi, st = W_cpsat_intervalle(h_fibres(cs, t, s), t + s, cap, tl)
    if st == "INFEASIBLE":
        cap *= 2
        lo, hi, st = W_cpsat_intervalle(h_fibres(cs, t, s), t + s, cap, tl)
    dt = time.time() - t0
    bits = [bin(c)[2:].zfill(s) for c in cs]
    if st == "OPTIMAL":
        print(f"  {nom:28} (t={t},s={s},k={1 << t}) SommeG={somme:3} "
              f"W={lo:3} g={lo - somme:+d}  [{dt:.0f}s]  c={bits}")
    elif st == "FEASIBLE":
        print(f"  {nom:28} (t={t},s={s},k={1 << t}) SommeG={somme:3} "
              f"W dans [{lo}, {hi}] donc g dans [{lo - somme:+d}, "
              f"{hi - somme:+d}] : NON CONCLU (timeout, intervalle prouvé) "
              f"[{dt:.0f}s]  c={bits}")
    else:
        print(f"  {nom:28} (t={t},s={s}) c={bits} : NON CONCLU ({st}) "
              f"[{dt:.0f}s]")


P = lambda i, j: (1 << i) | (1 << j)


def mode_base():
    print("=== BASE — replays (2,4) ν = 6 : cohérence avec MC-015 ===")
    mesure("replay antichaine paires", [P(0, 1), P(0, 2), P(1, 2), P(0, 3)],
           2, 4)
    mesure("singletons s=4", [1, 2, 4, 8], 2, 4)


def mode_t2s5():
    print("=== T2S5 — la croissance en s à t = 2 (ν = 7) ===")
    mesure("a1 plonge MC-015 (bit oisif)",
           [P(0, 1), P(0, 2), P(1, 2), P(0, 3)], 2, 5)
    mesure("a2 mixte", [P(0, 1), P(2, 3), P(0, 4), P(1, 2)], 2, 5)
    mesure("a3 etale", [P(0, 1), P(2, 3), P(1, 4), P(2, 4)], 2, 5)
    mesure("a4 etoile bit 0", [P(0, 1), P(0, 2), P(0, 3), P(0, 4)], 2, 5)
    mesure("a5 chemin", [P(0, 1), P(1, 2), P(2, 3), P(3, 4)], 2, 5)
    rng = random.Random(20260808)
    paires5 = [P(i, j) for i in range(5) for j in range(i + 1, 5)]
    mesure("a6 antichaine aleatoire", rng.sample(paires5, 4), 2, 5)


def mode_var():
    print("=== VAR — variance d'affectation + contrôles (ν = 7) ===")
    a1 = [P(0, 1), P(0, 2), P(1, 2), P(0, 3)]
    mesure("a1 perm inverse", a1[::-1], 2, 5)
    mesure("a1 perm (1,{2,4},3)", [a1[0], a1[1], a1[3], a1[2]], 2, 5)
    mesure("a1 perm croisee", [a1[2], a1[0], a1[3], a1[1]], 2, 5)
    ch = [0b00001, 0b00011, 0b00111, 0b01111]
    mesure("chaine alignee 1234", ch, 2, 5)
    mesure("chaine pire 4231", [ch[3], ch[1], ch[2], ch[0]], 2, 5)
    rng = random.Random(4231)
    mesure("aleatoire 1", rng.sample(range(1, 32), 4), 2, 5)
    mesure("aleatoire 2", rng.sample(range(1, 32), 4), 2, 5)


def mode_t2s6():
    print("=== T2S6 — la croissance en s à t = 2 (ν = 8, plafond) ===")
    mesure("b1 partition + croisee",
           [P(0, 1), P(2, 3), P(4, 5), P(1, 2)], 2, 6)
    mesure("b2 plonge MC-015 (2 bits oisifs)",
           [P(0, 1), P(0, 2), P(1, 2), P(0, 3)], 2, 6)
    mesure("b3 etale", [P(0, 5), P(1, 4), P(2, 3), P(2, 4)], 2, 6)


def mode_sing():
    print("=== SING — la famille singletons à travers s (Σ G = 4s) ===")
    mesure("singletons s=5", [1, 2, 4, 8], 2, 5)
    mesure("singletons s=6", [1, 2, 4, 8], 2, 6)


def mode_t3():
    print("=== T3 — la croissance en k : 8 fibres (t = 3) ===")
    # quasi-antichaîne à s = 4 (Sperner : antichaîne max = 6 < 8) :
    # 6 paires + {0} + {1,2,3} — 6 comparabilités inévitables
    quasi = [P(0, 1), P(0, 2), P(0, 3), P(1, 2), P(1, 3), P(2, 3),
             0b0001, 0b1110]
    mesure("quasi-antichaine s=4", quasi, 3, 4)
    # antichaîne PLEINE de paires de [5] (10 paires, on en retire 2)
    paires5 = [P(i, j) for i in range(5) for j in range(i + 1, 5)]
    huit = [c for c in paires5 if c not in (P(0, 1), P(2, 3))]
    mesure("antichaine pleine s=5", huit, 3, 5)


def mode_t3s5():
    """Reprise ciblée de l'antichaîne pleine (NON CONCLU à tl = 1500) :
    budget long + intervalle prouvé en sortie quoi qu'il arrive."""
    print("=== T3S5 — reprise : antichaîne pleine 8 fibres, tl = 3600 ===")
    paires5 = [P(i, j) for i in range(5) for j in range(i + 1, 5)]
    huit = [c for c in paires5 if c not in (P(0, 1), P(2, 3))]
    mesure("antichaine pleine s=5", huit, 3, 5, tl=3600)


def W_temoin(uns, nvars, cap, tl=1500):
    """Comme W_cpsat mais rend aussi le témoin optimal."""
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
        return None, None, solver.StatusName(st)
    temoin = {S: solver.Value(a[S]) for S in monomes if solver.Value(a[S])}
    return solver.Value(tot), temoin, "OPTIMAL"


def mode_temoin_sing():
    print("=== TEMOIN — programmes optimaux des singletons (mécanisme) ===")
    t = 2
    for s in (4, 5):
        cs = [1 << i for i in range(4)]
        somme = sum(loi_G(c, s) for c in cs)
        uns = h_fibres(cs, t, s)
        w, temoin, st = W_temoin(uns, t + s, somme + 4)
        if st != "OPTIMAL":
            print(f"  s={s} : NON CONCLU ({st})")
            continue
        print(f"  s={s} : W = {w} (Σ G = {somme}, g = {w - somme:+d}), "
              f"points de h = {[bin(u)[2:].zfill(t + s) for u in uns]}")
        for S in sorted(temoin, key=lambda S: (bin(S).count('1'), S)):
            print(f"    a[{bin(S)[2:].zfill(t + s)}] = {temoin[S]}")
        su = set(uns)
        vals_uns = {u: sum(c for S, c in temoin.items() if S & u == S)
                    for u in uns}
        vals_zeros = sorted({sum(c for S, c in temoin.items() if S & x == S)
                             for x in range(1 << (t + s)) if x not in su})
        print(f"    valeurs des uns : {vals_uns}")
        print(f"    valeurs atteintes par les zéros : {vals_zeros}")


if __name__ == "__main__":
    modes = {"base": mode_base, "t2s5": mode_t2s5, "var": mode_var,
             "t2s6": mode_t2s6, "sing": mode_sing, "t3": mode_t3,
             "t3s5": mode_t3s5, "temoin_sing": mode_temoin_sing}
    for quel in sys.argv[1:] or ["base"]:
        modes[quel]()
