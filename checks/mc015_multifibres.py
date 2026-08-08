# -*- coding: utf-8 -*-
r"""MC-015 — Le multi-fibres conditionnel : la brique que la totalisation
exige réellement.

Objet : h(x, y) = [y = c_x] — base x ∈ {0,1}^t (t = 2 : QUATRE fibres),
fibre y ∈ {0,1}^s PARTAGÉE, chaque fibre est un POINT c_x. Condition
candidate (MC-007/008) : les supports {c_x} deux à deux NON EMBOÎTÉS
(antichaîne). Écart : g(h) := W(h) − Σ_x G(c_x) où G est la loi prouvée
W([y = c]) = s − |c| + 1 (c ≠ 0), s (c = 0).

Volet A (corollaire 2-fibres, base 1 bit, s = 3) : la carte des signes
recalculée DEPUIS LES LOIS F désormais prouvées, en séparant les cases
THÉORÈME (familles comparable/(1,1)/linéaire prouvées) des cases
CERTIFIÉ-SOLVEUR (couronne : a, b ≥ 2), et re-vérifiée contre le solveur.

Volet B (la campagne neuve, t = 2, s = 4, ν = 6) : toutes les antichaînes
de 4 supports parmi les paires de [4] (C(6,4) = 15 affectations non
ordonnées, la symétrie de base rendant l'ordre indifférent) + antichaînes
mixtes (1 singleton + 3 paires l'évitant) ; W(h) exact par CP-SAT
(OPTIMAL exigé, témoin re-vérifié) ; CONTRÔLES : tuples avec emboîtements
(chaînes) et tuples aléatoires.
"""
import random
import sys
import time
from itertools import combinations

from ortools.sat.python import cp_model


def W_cpsat(uns, nvars, cap, tl=900):
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


def loi_G(c, s):
    k = bin(c).count("1")
    return s if k == 0 else s - k + 1


def lois_F(a, b, m, o, nu):
    """C-MC009 avec statut : (valeur, 'THEOREME'|'CERTIFIE')."""
    if a == 0 and b == 1:
        return (nu - m - (1 if m == 0 else 0), "THEOREME")   # recouvrement
    if a == 0:
        return (2 * nu - b - 2 * m + (1 if m >= 1 else 0), "THEOREME")
    if a == 1 and b == 1:
        return (2 * (nu - m) - 2, "THEOREME")
    if a == 1:
        return (2 * (nu - m) - max(2, b), "THEOREME")        # linéaire
    return (2 * (nu - m) - max(b, 2, a + b - 2), "CERTIFIE")  # couronne


def volet_A():
    print("=== VOLET A — le corollaire 2-fibres depuis les lois F "
          "(base 1 bit, s = 3) : théorème vs certifié ===")
    s = 3
    nu = 1 + s
    stats = {"THEOREME": {}, "CERTIFIE": {}}
    for c0 in range(1 << s):
        for c1 in range(1 << s):
            if c0 == c1:
                continue
            u, v = c0 << 1, (c1 << 1) | 1
            aa = bin(u & ~v).count("1")
            bb = bin(v & ~u).count("1")
            mm = bin(u & v).count("1")
            a2, b2 = min(aa, bb), max(aa, bb)
            F, statut = lois_F(a2, b2, mm, nu - a2 - b2 - mm, nu)
            g = F - loi_G(c0, s) - loi_G(c1, s)
            stats[statut][g] = stats[statut].get(g, 0) + 1
            # re-vérification solveur
            w, st = W_cpsat(sorted({u, v}), nu, (1 << nu) - 1)
            assert st == "OPTIMAL" and w == F, f"écart loi/solveur en ({c0},{c1})"
    for statut, d in stats.items():
        print(f"  cases {statut} : g = {dict(sorted(d.items()))}")
    print("  (toutes les valeurs re-vérifiées au solveur : 0 écart)")


def h_fibres(cs, t, s):
    """h(x, y) = [y = c_x] ; base = bits bas (t), fibre = bits hauts (s)."""
    uns = []
    for x in range(1 << t):
        uns.append(x | (cs[x] << t))
    return sorted(set(uns))


def incomparables(c1, c2):
    return (c1 & ~c2) != 0 and (c2 & ~c1) != 0


def volet_B():
    print("\n=== VOLET B — multi-fibres t = 2, s = 4 (ν = 6) : antichaînes "
          "contre contrôles ===")
    t, s = 2, 4
    paires = [c for c in range(1 << s) if bin(c).count("1") == 2]  # 6 paires
    # antichaînes de 4 paires distinctes (toutes les paires sont 2 à 2
    # incomparables) : C(6,4) = 15
    resultats = []
    t0 = time.time()
    for combo in combinations(paires, 4):
        cs = list(combo)
        somme = sum(loi_G(c, s) for c in cs)
        w, st = W_cpsat(h_fibres(cs, t, s), t + s, (1 << (t + s)) - 1)
        if st != "OPTIMAL":
            print(f"  antichaîne {cs} : NON CONCLU ({st})")
            continue
        resultats.append(("antichaine-paires", cs, somme, w, w - somme))
    # antichaînes mixtes : 1 singleton {i} + 3 paires ne contenant pas i
    for i in range(s):
        sing = 1 << i
        autres = [c for c in paires if not (c & sing)]  # C(3,2) = 3 paires
        if len(autres) >= 3:
            cs = [sing] + autres[:3]
            somme = sum(loi_G(c, s) for c in cs)
            w, st = W_cpsat(h_fibres(cs, t, s), t + s, (1 << (t + s)) - 1)
            if st == "OPTIMAL":
                resultats.append(("antichaine-mixte", cs, somme, w, w - somme))
    # contrôles emboîtés : chaînes c ⊂ c' ⊂ c'' ⊂ c'''
    controles = [[0b0001, 0b0011, 0b0111, 0b1111],
                 [0b0010, 0b0011, 0b1011, 0b1111],
                 [0b1000, 0b1100, 0b1110, 0b1111]]
    for cs in controles:
        somme = sum(loi_G(c, s) for c in cs)
        w, st = W_cpsat(h_fibres(cs, t, s), t + s, (1 << (t + s)) - 1)
        if st == "OPTIMAL":
            resultats.append(("chaine", cs, somme, w, w - somme))
    # contrôles aléatoires (points distincts quelconques)
    rng = random.Random(20260808)
    for _ in range(6):
        cs = rng.sample(range(1 << s), 4)
        somme = sum(loi_G(c, s) for c in cs)
        w, st = W_cpsat(h_fibres(cs, t, s), t + s, (1 << (t + s)) - 1)
        if st == "OPTIMAL":
            resultats.append(("aleatoire", cs, somme, w, w - somme))
    # bilan
    par_type = {}
    for typ, cs, somme, w, g in resultats:
        par_type.setdefault(typ, []).append(g)
        print(f"  {typ:18} c = {[bin(c)[2:].zfill(s) for c in cs]} : "
              f"Σ G = {somme}, W(h) = {w}, g = {g:+d}")
    print(f"\n  BILAN par type (distribution de g)  [{time.time()-t0:.0f}s] :")
    for typ, gs in par_type.items():
        d = {}
        for g in gs:
            d[g] = d.get(g, 0) + 1
        n_sub = sum(v for g, v in d.items() if g < 0)
        print(f"    {typ:18} : {dict(sorted(d.items()))} — "
              f"{n_sub}/{len(gs)} sous-additifs")


def volet_C():
    """L'affectation compte-t-elle ? Le modèle n'est pas invariant par
    permutation des points de base (le point 00 est nu : son point de h
    porte le seul support c_x). On rejoue chaque tuple du volet B sous
    LES 24 affectations fibre → point de base."""
    print("\n=== VOLET C — dépendance à l'affectation : 24 permutations "
          "par tuple ===")
    from itertools import permutations
    t, s = 2, 4
    paires = [c for c in range(1 << s) if bin(c).count("1") == 2]
    tuples_ = [("antichaine-paires", list(cb)) for cb in combinations(paires, 4)]
    for i in range(s):
        sing = 1 << i
        autres = [c for c in paires if not (c & sing)]
        tuples_.append(("antichaine-mixte", [sing] + autres[:3]))
    tuples_ += [("chaine", cs) for cs in
                [[0b0001, 0b0011, 0b0111, 0b1111],
                 [0b0010, 0b0011, 0b1011, 0b1111],
                 [0b1000, 0b1100, 0b1110, 0b1111]]]
    t0 = time.time()
    for typ, base_cs in tuples_:
        somme = sum(loi_G(c, s) for c in base_cs)
        gs = {}
        for perm in permutations(base_cs):
            w, st = W_cpsat(h_fibres(list(perm), t, s), t + s,
                            (1 << (t + s)) - 1)
            if st != "OPTIMAL":
                print(f"  {typ} {base_cs} perm {perm} : NON CONCLU ({st})")
                continue
            g = w - somme
            gs[g] = gs.get(g, 0) + 1
        print(f"  {typ:18} c = {[bin(c)[2:].zfill(s) for c in base_cs]} : "
              f"g sur 24 affectations = {dict(sorted(gs.items()))}")
    print(f"  [{time.time()-t0:.0f}s]")


def volet_C2():
    """QUELLES affectations rendent une chaîne additive ? On imprime g
    par permutation pour la chaîne c1 ⊂ c2 ⊂ c3 ⊂ c4 = 0001 ⊂ 0011 ⊂
    0111 ⊂ 1111, en notant l'affectation x ↦ rang du support (1..4)
    pour les points de base x = 00, 01, 10, 11."""
    print("\n=== VOLET C2 — les affectations additives d'une chaîne ===")
    from itertools import permutations
    t, s = 2, 4
    chaine = [0b0001, 0b0011, 0b0111, 0b1111]
    rang = {c: i + 1 for i, c in enumerate(chaine)}
    somme = sum(loi_G(c, s) for c in chaine)
    t0 = time.time()
    for perm in permutations(chaine):
        w, st = W_cpsat(h_fibres(list(perm), t, s), t + s, (1 << (t + s)) - 1)
        g = (w - somme) if st == "OPTIMAL" else None
        aff = "".join(str(rang[c]) for c in perm)
        marque = "  <-- ADDITIVE" if g == 0 else ""
        print(f"  x=00,01,10,11 recoivent les rangs {aff} : g = {g:+d}{marque}")
    print(f"  [{time.time()-t0:.0f}s]")


if __name__ == "__main__":
    quel = sys.argv[1] if len(sys.argv) > 1 else "tout"
    if quel in ("tout", "A"):
        volet_A()
    if quel in ("tout", "B"):
        volet_B()
    if quel == "C":
        volet_C()
    if quel == "C2":
        volet_C2()
