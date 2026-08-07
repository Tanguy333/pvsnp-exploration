# -*- coding: utf-8 -*-
r"""MC-008 — Les lois exactes des fonctions à 1 et 2 points.

Cible désignée par MC-007 : transformer la règle mesurée du non-partage
(antichaîne de supports) en théorème, via les lois exactes :

  G(u ; ν)   := W([w = u])            — LOI PROUVÉE (fiche §2) :
                ν − |u| + 1 si u ≠ 0, ν si u = 0.
                Majorant : p = m_u + Σ_{j∉u} m_{u∪{j}}.
                Minorant : packing (Lemme 4 de MC-001) — paires
                (u∪{j}, u), j ∉ u, D-ensembles disjoints, + la paire
                (u, v ⊊ u) si u ≠ 0.

  F(u, v ; ν) := W([w = u] ∨ [w = v]) — à TABLER : par symétrie S_ν,
                F ne dépend que de (a, b, m, ν) = (|u\v|, |v\u|, |u∩v|, ν),
                symétrique en (a, b).

Campagnes :
  g1 : vérification exhaustive de la loi G à ν = 2, 3, 4 (toutes les
       fonctions à un point, tables de force brute / CP-SAT par classes).
  f2 : table exhaustive de F à ν = 3 (28 paires) et ν = 4 (120 paires),
       groupée par (a, b, m) — vérifie au passage que F est bien constante
       sur chaque groupe (la symétrie l'exige : témoin d'implémentation).
  f5 : contrôles à ν = 5 par CP-SAT sur un échantillon de (a, b, m)
       représentatifs (garde q.12).
  cor : le corollaire fibre : pour les paires de points épars de MC-007
       (base 1 bit), recalcul de g = F − G − G en termes de (a, b, m) et
       vérification que la règle d'emboîtement directionnel est EXACTEMENT
       le signe prédit.

Graine : sans objet (tout est exhaustif ou énuméré). Aucune extrapolation.
"""
import sys
import time
from itertools import combinations, permutations, combinations_with_replacement

from ortools.sat.python import cp_model


# ------------------------------------------------------------------ W exact
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


def W_cpsat(uns, nvars, cap, tl=600):
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


def W_exact(uns, nvars, tl=600):
    if nvars <= 4:
        return W_brute(uns, nvars, (1 << nvars) - 1), "BRUTE"
    return W_cpsat(uns, nvars, (1 << nvars) - 1, tl)


def loi_G(k, nu):
    return nu if k == 0 else nu - k + 1


# ------------------------------------------------------------------ campagnes
def run_g1():
    print("=== G1 — la loi G vérifiée exhaustivement (ν = 2, 3, 4) ===")
    for nu in (2, 3, 4):
        N = 1 << nu
        ecarts = 0
        for u in range(N):
            w, _ = W_exact([u], nu)
            attendu = loi_G(bin(u).count("1"), nu)
            if w != attendu:
                ecarts += 1
                print(f"  ÉCART : ν={nu}, u={u:0{nu}b} : W={w} ≠ loi {attendu}")
        print(f"  ν = {nu} : {N} points, {ecarts} écart(s) à la loi "
              f"{'— LOI CONFIRMÉE' if ecarts == 0 else ''}")


def params(u, v):
    return (bin(u & ~v).count("1"), bin(v & ~u).count("1"),
            bin(u & v).count("1"))


def run_f2():
    print("\n=== F2 — la table de F (exhaustif ν = 3, 4) ===")
    tables = {}
    for nu in (3, 4):
        N = 1 << nu
        groupes = {}
        for u, v in combinations(range(N), 2):
            w, _ = W_exact(sorted({u, v}), nu)
            a, b, m = params(u, v)
            cle = (min(a, b), max(a, b), m)
            groupes.setdefault(cle, set()).add(w)
        # la symétrie exige une valeur unique par groupe
        table = {}
        for cle, vals in sorted(groupes.items()):
            assert len(vals) == 1, f"ν={nu}, groupe {cle} : valeurs {vals} !"
            table[cle] = vals.pop()
        tables[nu] = table
        print(f"  ν = {nu} : F par (a≤b, b, m) — {len(table)} groupes, "
              f"valeur unique par groupe (symétrie confirmée) :")
        for (a, b, m), w in sorted(table.items()):
            o = nu - a - b - m
            somme_G = loi_G(a + m, nu) + loi_G(b + m, nu)
            print(f"    (a={a}, b={b}, m={m}, o={o}) : F = {w}"
                  f"   [Σ G des deux points pris seuls = {somme_G}]")
    return tables


def run_f5(tables):
    print("\n=== F5 — contrôles ν = 5 (CP-SAT, échantillon de groupes) ===")
    nu = 5
    # un représentant par (a, b, m) atteignable avec a ≤ b, a+b+m ≤ 5, (a,b) ≠ (0,0)
    vus = set()
    t0 = time.time()
    for a in range(0, 4):
        for b in range(max(a, 1), 5):
            for m in range(0, 6 - a - b):
                if (a, b, m) in vus or a + b + m > nu:
                    continue
                vus.add((a, b, m))
                # construire u, v canoniques
                u = ((1 << a) - 1) << (b)          # a bits propres à u
                v = (1 << b) - 1                    # b bits propres à v
                commun = ((1 << m) - 1) << (a + b)
                u |= commun
                v |= commun
                w, st = W_exact(sorted({u, v}), nu, tl=900)
                if st != "OPTIMAL":
                    print(f"    (a={a}, b={b}, m={m}) : NON CONCLU ({st})")
                    continue
                print(f"    (a={a}, b={b}, m={m}, o={nu-a-b-m}) : F = {w}"
                      f"  [{time.time()-t0:.0f}s]")


def run_cor(tables):
    print("\n=== COROLLAIRE — les points épars de MC-007 en termes de (a, b, m) ===")
    # base 1 bit + fibre s = 3 : u = c0 (bit x absent), v = {x} ∪ c1 ; ν = 4
    T = tables[4]
    regle_ok = True
    res = {}
    for c0 in range(8):
        for c1 in range(8):
            if c0 == c1:
                continue
            u, v = c0 << 1, (c1 << 1) | 1
            a, b, m = params(u, v)
            F = T[(min(a, b), max(a, b), m)]
            g = F - loi_G(bin(c0).count("1"), 3) - loi_G(bin(c1).count("1"), 3)
            res[g] = res.get(g, 0) + 1
            emboite_dir = (c1 & ~c0) == 0 and c1 != 0 and c0 != c1
            if (g < 0) != emboite_dir:
                regle_ok = False
                print(f"    CONTRE-EXEMPLE à la règle : c0={c0:03b}, c1={c1:03b}, "
                      f"g={g}, emboîtement directionnel={emboite_dir}")
    print(f"  distribution de g (recalculée via F et G) : {dict(sorted(res.items()))}")
    print(f"  règle « g < 0 ⟺ supp(c1) ⊊ supp(c0), c1 ≠ 0 » : "
          f"{'EXACTE sur les 56 paires' if regle_ok else 'VIOLÉE'}")


if __name__ == "__main__":
    quel = sys.argv[1] if len(sys.argv) > 1 else "tout"
    tables = None
    if quel in ("tout", "g1"):
        run_g1()
    if quel in ("tout", "f2", "cor"):
        tables = run_f2()
    if quel in ("tout", "f5"):
        if tables is None:
            tables = run_f2()
        run_f5(tables)
    if quel in ("tout", "cor"):
        run_cor(tables)
