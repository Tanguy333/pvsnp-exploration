"""
TACHE F-020 -- l'outil de borne inferieure du cote COMPTAGE.

(1) THEOREME D'ALTERNANCE (prouve, 3 lignes) :
    p = sum a_S m_S avec a_S >= 0 est MONOTONE sur le cube. Le long
    d'une chaine croissante, p est non-decroissant, et a chaque
    alternance de f les valeurs doivent differer (separation) donc p
    croit strictement. D'ou max p >= alt(f), et W = sum a_S >= p(1^n)
    >= max p >= alt(f) :
        W(f) >= alt(f)  (nb max d'alternances sur une chaine).
    Ce script calcule alt(f) par programmation dynamique exacte sur
    le cube pour TOUTE la batterie fermee, et compare a W exact.

(2) BORNE DE COUVERTURE (monotone f) : tout un minimal z exige
    p(z) >= 1 -> LP de couverture fractionnaire (borne inf, faible).

(3) Le tableau explique/inexplique : ou l'outil manque.
"""

from __future__ import annotations

import itertools

import pulp


def alt_dp(f, n):
    """alt(f) = max nb d'alternances de f le long d'une chaine
    croissante. DP sur le cube par niveaux : A[z] = max alternances
    d'une chaine finissant en z."""
    order = sorted(range(1 << n), key=lambda x: bin(x).count("1"))
    A = {}
    fv = {}
    for x in order:
        z = tuple((x >> i) & 1 for i in range(n))
        fv[x] = f(z)
        best = 0
        for i in range(n):
            if x & (1 << i):
                y = x ^ (1 << i)
                cand = A[y] + (1 if fv[y] != fv[x] else 0)
                if cand > best:
                    best = cand
        A[x] = best
    return max(A.values())


def cover_lp(f, n):
    """LP de couverture : min sum a_S s.c. pour tout un MINIMAL z,
    sum_{S <= supp z} a_S >= 1 (a reels >= 0)."""
    inputs = list(itertools.product((0, 1), repeat=n))
    ones = [z for z in inputs if f(z)]
    min_ones = [z for z in ones
                if all(not f(tuple(b if j != i else 0
                                   for j, b in enumerate(z)))
                       for i in range(n) if z[i])]
    monos = []
    for d in range(1, n + 1):
        monos.extend(frozenset(c)
                     for c in itertools.combinations(range(n), d))
    prob = pulp.LpProblem("cover", pulp.LpMinimize)
    a = {S: pulp.LpVariable(f"a{i}", lowBound=0)
         for i, S in enumerate(monos)}
    prob += pulp.lpSum(a.values())
    for z in min_ones:
        supp = frozenset(j for j in range(n) if z[j])
        prob += pulp.lpSum(a[S] for S in monos if S <= supp) >= 1
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    return pulp.value(prob.objective), len(min_ones)


def main():
    thr4 = lambda z: 1 if 4 * z[0] + 3 * z[1] + 2 * z[2] + z[3] >= 4 else 0
    thr4b = lambda z: 1 if z[4] + 2 * z[5] + 3 * z[6] + 4 * z[7] >= 4 else 0
    gt2 = lambda z: 1 if 2 * z[0] + z[1] - 2 * z[2] - z[3] >= 1 else 0
    gt2b = lambda z: 1 if 2 * z[4] + z[5] - 2 * z[6] - z[7] >= 1 else 0
    or2 = lambda z: 1 if z[0] + z[1] >= 1 else 0
    maj3 = lambda z: 1 if sum(z[:3]) >= 2 else 0

    battery = [
        ("PARITY_4", 4, lambda z: sum(z) % 2, 4),
        ("IP_8", 8, lambda z: sum(z[i] * z[4 + i] for i in range(4)) % 2, 4),
        ("OR(THR4,THR4)", 8, lambda z: 1 if thr4(z) + thr4b(z) >= 1 else 0, 6),
        ("XOR(THR4,THR4)", 8, lambda z: (thr4(z) + thr4b(z)) % 2, 14),
        ("XOR(GT2,GT2)", 8, lambda z: (gt2(z) + gt2b(z)) % 2, 16),
        ("XOR(OR2,OR2)", 4, lambda z: or2(z[:2]) ^ or2(z[2:4]), 6),
        ("MAJ3(OR2^3)", 6,
         lambda z: 1 if (or2(z[0:2]) + or2(z[2:4]) + or2(z[4:6])) >= 2
         else 0, 12),
        ("XOR3(MAJ3^3)", 9,
         lambda z: maj3(z[0:3]) ^ maj3(z[3:6]) ^ maj3(z[6:9]), 9),
    ]
    print("fonction              W exact | alt(f) | LP couverture "
          "(monotone seulement)")
    for name, n, f, W in battery:
        a = alt_dp(f, n)
        mono = all(True for _ in [0])
        # test de monotonie
        is_mono = True
        for x in range(1 << n):
            z = tuple((x >> i) & 1 for i in range(n))
            for i in range(n):
                if not z[i]:
                    z2 = tuple(1 if j == i else b
                               for j, b in enumerate(z))
                    if f(z) > f(z2):
                        is_mono = False
        cl = ""
        if is_mono:
            v, nm = cover_lp(f, n)
            cl = f" | LP = {v:.2f} ({nm} uns minimaux)"
        tight = "SERRE" if a == W else f"ecart x{W / a:.1f}"
        print(f"  {name:<18} W = {W:3d} | alt = {a:3d} [{tight}]{cl}",
              flush=True)


if __name__ == "__main__":
    main()
