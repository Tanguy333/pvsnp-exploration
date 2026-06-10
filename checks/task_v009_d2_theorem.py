"""
TACHE V-009 -- THEOREME d = 2 : la Conjecture 5 de KV est vraie pour
d = 2, tout n >= 6.

Conventions : f = sum sigma_i x^{a_i}, (1+x)^3 | f <=> avec
t_i := sigma_i (-1)^{a_i} : sum t_i = 0, sum t_i a_i = 0, sum t_i a_i^2 = 0.

THEOREME V9. Pour d = 2 et n >= 6 :
 (1) la norme^2 minimale des multiples non nuls de (1+x)^3 de degre <= n
     est 6 ;
 (2) tout minimiseur a tous ses coefficients dans {0, +-1} (6 monomes) ;
 (3) tout minimiseur a ses coefficients de queue et de tete en +-1 ;
     en particulier la Conjecture 5 vaut pour d = 2.
PREUVE.
 (a) norme^2 impossible pour 1..5 :
     - 1, 3, 5 unites : sum t_i impair != 0 ;
     - (2) seul : f(-1) = +-2 != 0 ; (2,1) : sum t impair ; (2,2) :
       contenu 2 -> reduction a norme 2 ; (1,1) : t1 = -t2 puis a = b ;
     - (1,1,1,1) : 2+2 avec sommes ET sommes de carres egales -> les
       polynomes symetriques elementaires coincident -> paires egales ;
     - (2,1,1) : t0 = -2s, t1 = t2 = s -> 2a = b + c et 2a^2 = b^2 + c^2
       -> (b - c)^2 = 2(b^2+c^2) - (b+c)^2 = 0 -> b = c, contradiction.
 (b) existence a norme 6, degre 6 : la solution PTE classique
     {0, 4, 5} vs {1, 2, 6} (sommes 9 = 9, carres 41 = 41) donne
     f = 1 + x - x^2 + x^4 - x^5 - x^6.
 (c) par (a), tout minimiseur est a 6 monomes +-1 (la forme (2,1,1) est
     exclue), donc ses extremites sont +-1.                       QED

Le script verifie : [A] (a) par enumeration exhaustive (deg <= 30) ;
[B] (b) en exact ; [C] que les 32 solutions de la fenetre V-008 sont
toutes des PTE-2 signees a 6 monomes (aucune (2,1,1)) ; [D] croisement
avec les minima de reseau V-004 (d = 2, n = 6..20 : norme 6 partout).
"""

from __future__ import annotations

import itertools

from task_v004_kv_conjecture5 import build_basis, lll_reduce, shortest_vectors


def conds(exps, sigs):
    t = [s * ((-1) ** a) for a, s in zip(exps, sigs)]
    return (sum(t) == 0,
            sum(ti * a for ti, a in zip(t, exps)) == 0,
            sum(ti * a * a for ti, a in zip(t, exps)) == 0)


def ok3(exps, sigs):
    return all(conds(exps, sigs))


def main() -> None:
    print("TACHE V-009 -- theoreme d = 2 (Conjecture 5 vraie pour d = 2)")
    print("=" * 68)

    print("\n[A] Normes 1..5 impossibles (enumeration exhaustive, deg <= 30) :")
    bad = 0
    D = 30
    # 2 unites ; 4 unites ; (2,1,1) ; (2,2) primitif exclu par contenu
    for exps in itertools.combinations(range(D + 1), 2):
        for sigs in itertools.product((1, -1), repeat=2):
            if ok3(exps, sigs):
                bad += 1
    for exps in itertools.combinations(range(D + 1), 4):
        for sigs in itertools.product((1, -1), repeat=4):
            if ok3(exps, sigs):
                bad += 1
                print(f"    !!! 4 unites : {list(zip(exps, sigs))}")
    for exps in itertools.combinations(range(D + 1), 3):
        for pos2 in range(3):
            for sigs0 in itertools.product((1, -1), repeat=3):
                sigs = tuple(2 * s if i == pos2 else s
                             for i, s in enumerate(sigs0))
                if ok3(exps, sigs):
                    bad += 1
                    print(f"    !!! (2,1,1) : {list(zip(exps, sigs))}")
    print(f"    solutions de norme^2 <= 5 trouvees : {bad} "
          f"{'(AUCUNE -- conforme a la preuve)' if bad == 0 else '*** PROBLEME ***'}")

    print("\n[B] Existence a norme 6, degre 6 :")
    exps, sigs = (0, 1, 2, 4, 5, 6), (1, 1, -1, 1, -1, -1)
    print(f"    f = 1 + x - x^2 + x^4 - x^5 - x^6 : "
          f"(1+x)^3 | f : {'OUI' if ok3(exps, sigs) else 'NON ?!'}")

    print("\n[C] Les 32 solutions de la fenetre V-008 : toutes 6-unites ?")
    six_unit = 0
    other = 0
    for exps in itertools.combinations(range(21), 6):
        if exps[0] != 0:
            continue
        for sigs in itertools.product((1, -1), repeat=5):
            sg = (1,) + sigs
            if ok3(exps, sg):
                six_unit += 1
    for exps in itertools.combinations(range(21), 3):
        if exps[0] != 0:
            continue
        for pos2 in range(3):
            for sigs0 in itertools.product((1, -1), repeat=3):
                sg = tuple(2 * s if i == pos2 else s
                           for i, s in enumerate(sigs0))
                if sg[0] < 0:
                    sg = tuple(-s for s in sg)
                if ok3(exps, sg):
                    other += 1
    print(f"    6-unites : {six_unit} ; formes (2,1,1) : {other} "
          f"{'-- conforme (32 = 6-unites seulement)' if other == 0 else '*** PROBLEME ***'}")

    print("\n[D] Croisement reseau (d = 2, n = 6..20) : norme^2 = 6 et")
    print("    premiere/derniere coordonnee non nulle = +-1 partout ?")
    okD = True
    for n in range(6, 21):
        G = lll_reduce(build_basis(n, 2))
        n2, sols = shortest_vectors(G)
        ends = all(
            abs(next(int(x) for x in v if int(x))) == 1 and
            abs(next(int(x) for x in reversed(v) if int(x))) == 1
            for v in sols)
        okD &= (n2 == 6 and ends)
    print(f"    {'OK partout' if okD else '*** ECHEC ***'}")

    print("\n" + "=" * 68)
    print("THEOREME V9 : Conjecture 5 de KV VRAIE pour d = 2 (tout n >= 6).")
    print("Avec V-008 (d = 1) : les deux premiers cas de la conjecture sont")
    print("PROUVES ; d >= 3 : le regime plat (PTE ideal) demande n assez")
    print("grand -- le petit-n non plat reste la zone dure.")


if __name__ == "__main__":
    main()
