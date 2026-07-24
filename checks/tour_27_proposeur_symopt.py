"""
TOUR 27 (Proposeur) -- piece 1 : optimum G-SYMETRIQUE exact de MAJ_5(OR2^5)
et candidats croises a la main.

Cible : dossier tours/tour_27_cible.md (trou unique decomposable => global,
fenetre W(MAJ_5(OR2^5)) in [20, 30]).

IDEE : sous le groupe G = S_5 x| (S_2)^5 (permutation des blocs x swap
intra-bloc), les monomes se partitionnent en ORBITES typees (t2, t1) :
t2 blocs contribuant leurs DEUX variables, t1 blocs contribuant UNE
variable. Un separateur G-symetrique a un coefficient par orbite, et sa
valeur ne depend que du TYPE de configuration (a, b) = (blocs satisfaits
par une seule variable, blocs satisfaits par les deux). Le probleme
symetrique est donc un petit programme entier : 20 orbites, 21 types,
~90 contraintes de non-collision -- resoluble EXACTEMENT en secondes.

  - Si optimum symetrique < 30 : TEMOIN de refutation immediat.
  - Si = 30 : CERTIFICAT que toute refutation est asymetrique (et que le
    run symetrise de 25 min du dossier ne pouvait structurellement rien
    trouver).

Piece 2 (même script) : candidats croises asymetriques a la main, testes
par enumeration exhaustive des 1024 points (mod-4 + faisceau s1*s2 a
poids 29, variantes mod-3 + faisceaux, etc.).

Lemme de span (utilise partout, prouve dans la proposition) : dans un
bloc OR2 toute variable a 1 satisfait le bloc ; donc un monome couvrant
r blocs n'est actif que sur les configurations a m >= r blocs satisfaits.
"""

from __future__ import annotations

import itertools
from math import comb

K = 5
T = 3
N = 10


# ------------------------------------------------------------ enumeration

def block_states(z: tuple):
    """ Etat par bloc : 0 = vide, 1 = x seul, 2 = y seul, 3 = les deux. """
    return tuple((z[2 * i] | (z[2 * i + 1] << 1)) for i in range(K))


def sat_count(z: tuple) -> int:
    return sum(1 for i in range(K) if z[2 * i] or z[2 * i + 1])


def f_maj5(z: tuple) -> int:
    return 1 if sat_count(z) >= T else 0


ALL_INPUTS = list(itertools.product((0, 1), repeat=N))


def eval_poly(sol: dict, z: tuple) -> int:
    supp = frozenset(j for j in range(N) if z[j])
    return sum(v for S, v in sol.items() if S <= supp)


def check(sol: dict, verbose: bool = True, label: str = "") -> bool:
    ones, zeros = set(), set()
    for z in ALL_INPUTS:
        (ones if f_maj5(z) else zeros).add(eval_poly(sol, z))
    inter = ones & zeros
    w = sum(sol.values())
    if verbose:
        st = "DISJOINT OK  << TEMOIN !" if not inter else \
             f"collision sur {sorted(inter)[:6]}"
        print(f"  {label:<44} poids={w:<3} {st}")
    return not inter


# --------------------------------------------- piece 1 : optimum symetrique

def orbit_types():
    """ Types (t2, t1) : t2 blocs a 2 variables, t1 blocs a 1 variable. """
    out = []
    for t2 in range(K + 1):
        for t1 in range(K - t2 + 1):
            if t2 + t1 >= 1:
                out.append((t2, t1))
    return out


def orbit_size(t2: int, t1: int) -> int:
    return comb(K, t2) * comb(K - t2, t1) * (2 ** t1)


def active_count(t2: int, t1: int, a: int, b: int) -> int:
    """ Nombre de monomes de l'orbite (t2,t1) actifs sur une configuration
        de type (a, b) : a blocs mono-satisfaits, b blocs bi-satisfaits. """
    if t2 > b:
        return 0
    total = 0
    for j in range(t1 + 1):          # j blocs '1 variable' pris chez les mono
        if j <= a and (t1 - j) <= (b - t2):
            total += comb(a, j) * comb(b - t2, t1 - j) * (2 ** (t1 - j))
    return comb(b, t2) * total


def config_types():
    return [(a, b) for a in range(K + 1) for b in range(K + 1 - a)]


def solve_symmetric(budget: int = 200):
    from ortools.sat.python import cp_model
    types = orbit_types()
    m = cp_model.CpModel()
    coef = {tau: m.new_int_var(0, budget, f"c{tau}") for tau in types}
    weight = sum(orbit_size(*tau) * coef[tau] for tau in types)
    vals = {}
    for (a, b) in config_types():
        v = m.new_int_var(0, budget * 400, f"v{a}_{b}")
        m.add(v == sum(active_count(*tau, a, b) * coef[tau] for tau in types))
        vals[(a, b)] = v
    for (a1, b1) in config_types():
        if a1 + b1 < T:
            continue
        for (a0, b0) in config_types():
            if a0 + b0 >= T:
                continue
            m.add(vals[(a1, b1)] != vals[(a0, b0)])
    m.minimize(weight)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 120.0
    st = solver.solve(m)
    name = solver.status_name(st)
    obj = round(solver.objective_value) if name in ("OPTIMAL", "FEASIBLE") else None
    lb = round(solver.best_objective_bound)
    sol = {tau: solver.value(coef[tau]) for tau in types
           if solver.value(coef[tau]) > 0} if obj is not None else None
    return name, obj, lb, sol


def symmetric_sol_to_monomials(sol_orbits: dict) -> dict:
    """ Deplie une solution par orbites en polynome concret pour re-verif. """
    poly = {}
    for (t2, t1), c in sol_orbits.items():
        for blocks2 in itertools.combinations(range(K), t2):
            rest = [i for i in range(K) if i not in blocks2]
            for blocks1 in itertools.combinations(rest, t1):
                for choice in itertools.product((0, 1), repeat=t1):
                    S = set()
                    for i in blocks2:
                        S |= {2 * i, 2 * i + 1}
                    for i, ch in zip(blocks1, choice):
                        S.add(2 * i + ch)
                    poly[frozenset(S)] = poly.get(frozenset(S), 0) + c
    return poly


# ------------------------------------------ piece 2 : candidats a la main

def dec_blocks(coeffs: list) -> dict:
    """ coeffs = liste de (alpha, beta, gamma) par bloc. """
    sol = {}
    for i, (al, be, ga) in enumerate(coeffs):
        x, y = 2 * i, 2 * i + 1
        if al:
            sol[frozenset([x])] = al
        if be:
            sol[frozenset([y])] = be
        if ga:
            sol[frozenset([x, y])] = ga
    return sol


def add_bundle(sol: dict, i: int, j: int, c: int) -> dict:
    """ Ajoute c * s_i * s_j = les 4 paires croisees entre blocs i et j. """
    out = dict(sol)
    for u in (2 * i, 2 * i + 1):
        for v in (2 * j, 2 * j + 1):
            out[frozenset([u, v])] = out.get(frozenset([u, v]), 0) + c
    return out


def add_mono(sol: dict, vars_: tuple, c: int) -> dict:
    out = dict(sol)
    out[frozenset(vars_)] = out.get(frozenset(vars_), 0) + c
    return out


def solve_symmetric_k(Kk: int, Tt: int, budget: int = 300):
    """ Version parametree en k du programme entier par orbites. """
    from ortools.sat.python import cp_model
    types_orb = [(t2, t1) for t2 in range(Kk + 1)
                 for t1 in range(Kk - t2 + 1) if t2 + t1 >= 1]
    types_cfg = [(a, b) for a in range(Kk + 1) for b in range(Kk + 1 - a)]

    def osize(t2, t1):
        return comb(Kk, t2) * comb(Kk - t2, t1) * (2 ** t1)

    def act(t2, t1, a, b):
        if t2 > b:
            return 0
        s = sum(comb(a, j) * comb(b - t2, t1 - j) * (2 ** (t1 - j))
                for j in range(t1 + 1) if j <= a and t1 - j <= b - t2)
        return comb(b, t2) * s

    m = cp_model.CpModel()
    coef = {tau: m.new_int_var(0, budget, f"c{tau}") for tau in types_orb}
    w = sum(osize(*tau) * coef[tau] for tau in types_orb)
    vals = {}
    for (a, b) in types_cfg:
        v = m.new_int_var(0, budget * 1000, f"v{a}_{b}")
        m.add(v == sum(act(*tau, a, b) * coef[tau] for tau in types_orb))
        vals[(a, b)] = v
    for c1 in types_cfg:
        if sum(c1) < Tt:
            continue
        for c0 in types_cfg:
            if sum(c0) >= Tt:
                continue
            m.add(vals[c1] != vals[c0])
    m.minimize(w)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = 120.0
    st = s.solve(m)
    return (s.status_name(st), round(s.objective_value),
            round(s.best_objective_bound),
            {tau: s.value(coef[tau]) for tau in types_orb
             if s.value(coef[tau]) > 0})


def sweep_k():
    print("Balayage k = 3..8 : optimum G-symetrique vs k(k+1)")
    for Kk in (3, 4, 5, 6, 7, 8):
        Tt = (Kk + 1) // 2
        name, obj, lb, sol = solve_symmetric_k(Kk, Tt)
        print(f"  k={Kk} t={Tt} : statut={name} W_sym={obj} "
              f"borne_inf={lb}  k(k+1)={Kk*(Kk+1)}  orbites={sol}")


def main():
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] == "sweep":
        sweep_k()
        return
    print("TOUR 27 (Proposeur) -- piece 1 : optimum G-symetrique exact")
    print("=" * 74)
    name, obj, lb, sol = solve_symmetric()
    print(f"  statut={name}  optimum_symetrique={obj}  borne_inf={lb}")
    if sol:
        print(f"  orbites actives : {sol}")
        poly = symmetric_sol_to_monomials(sol)
        ok = check(poly, label=f"re-verif solution symetrique")
        print(f"  poids re-calcule = {sum(poly.values())}")
    print()

    print("piece 2 : candidats croises a la main (enumeration 1024 points)")
    print("=" * 74)

    mod4 = [(1, 1, 3)] * K          # 25
    mod3 = [(1, 1, 2)] * K          # 20
    mod5 = [(1, 1, 4)] * K          # 30 (temoin connu)

    check(dec_blocks(mod5), label="mod-5 pur (sanite, poids 30)")
    check(dec_blocks(mod4), label="mod-4 pur (collision attendue)")

    # mod-4 + un faisceau croise s1*s2 (25 + 4 = 29)
    check(add_bundle(dec_blocks(mod4), 0, 1, 1),
          label="mod-4 + s1*s2 (29)")
    # mod-4 + deux paires croisees seules (25 + 2 = 27)
    c = add_mono(add_mono(dec_blocks(mod4), (0, 2), 1), (1, 3), 1)
    check(c, label="mod-4 + x1x2 + y1y2 (27)")
    # mod-4 + 4 paires en cycle (25 + 4 = 29)
    c = dec_blocks(mod4)
    for (u, v) in [(0, 2), (2, 4), (4, 6), (6, 8)]:
        c = add_mono(c, (u, v), 1)
    check(c, label="mod-4 + chaine x_i x_{i+1} (29)")
    # mod-3 + faisceaux s1s2 + s3s4 (20 + 8 = 28)
    c = add_bundle(add_bundle(dec_blocks(mod3), 0, 1, 1), 2, 3, 1)
    check(c, label="mod-3 + s1s2 + s3s4 (28)")
    # mod-3 + faisceaux s1s2 + s3s4 + x5-terme (29)
    c2 = add_mono(c, (8, 4), 1)
    check(c2, label="mod-3 + s1s2 + s3s4 + x5x3 (29)")
    # mod-3 + trois faisceaux en triangle sur blocs 1-3 (20 + 12 = 32 > 29,
    # teste quand meme pour la structure)
    c = dec_blocks(mod3)
    for (i, j) in [(0, 1), (1, 2), (0, 2)]:
        c = add_bundle(c, i, j, 1)
    check(c, label="mod-3 + triangle s_is_j (32, hors budget)")
    # blocs asymetriques : 4 blocs mod-5 (1,1,4) + bloc 5 allege (1,1,2)
    # + paire croisee de reparation (28 + 1 = 29)
    base = [(1, 1, 4)] * 4 + [(1, 1, 2)]
    c = add_mono(dec_blocks(base), (8, 0), 1)
    check(c, label="4x(1,1,4) + (1,1,2) + x5x1 (29)")
    c = add_bundle(dec_blocks(base), 4, 0, 1)
    check(c, label="4x(1,1,4) + (1,1,2) + s5s1 (32, hors budget)")

    print()
    print("FIN piece 1+2.")


if __name__ == "__main__":
    main()
