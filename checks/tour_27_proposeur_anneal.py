"""
TOUR 27 (Proposeur) -- piece 4 : chasse au temoin < 30 par recuit simule
asymetrique (numpy), pool span <= 3.

Par L27.1 (optimum G-symetrique = 30, certifie), tout temoin est
asymetrique. Par le lemme de span, les monomes de span >= 4 ne touchent
que m >= 4 ; le pool span <= 3 couvre les temoins n'utilisant pas de
lifteur span >= 4 (et ceux-ci ne peuvent reparer que des collisions
impliquant m >= 4 -- inclus ici via les 270 monomes de span 3).

Representation : vecteur de coefficients c >= 0 sur le pool (375 monomes),
poids total <= 29. Objectif : nombre de valeurs en collision entre les
deux cotes (0 = TEMOIN). Mouvements : +/-1 sur un coefficient (rejet si
poids > 29), redemarrages multiples depuis bases mod-3/mod-4 perturbees
et aleatoires creuses.
"""

from __future__ import annotations

import itertools
import sys
import time

import numpy as np

K, N, T = 5, 10, 3
RNG = np.random.default_rng(20260724)


def build_pool():
    monos = []
    for i in range(K):                                   # intra
        x, y = 2 * i, 2 * i + 1
        monos += [frozenset([x]), frozenset([y]), frozenset([x, y])]
    for i, j in itertools.combinations(range(K), 2):     # paires croisees
        for u in (2 * i, 2 * i + 1):
            for v in (2 * j, 2 * j + 1):
                monos.append(frozenset([u, v]))
    for i, j in itertools.permutations(range(K), 2):     # (2,1)
        for v in (2 * j, 2 * j + 1):
            monos.append(frozenset([2 * i, 2 * i + 1, v]))
    for i, j in itertools.combinations(range(K), 2):     # (2,2)
        monos.append(frozenset([2 * i, 2 * i + 1, 2 * j, 2 * j + 1]))
    for blocks in itertools.combinations(range(K), 3):   # span 3
        for contrib in itertools.product((1, 2, 3), repeat=3):
            S = set()
            for b, c in zip(blocks, contrib):
                if c & 1:
                    S.add(2 * b)
                if c & 2:
                    S.add(2 * b + 1)
            monos.append(frozenset(S))
    monos = sorted(set(monos), key=lambda s: (len(s), sorted(s)))
    return monos


def main():
    budget = 29
    tl = float(sys.argv[1]) if len(sys.argv) > 1 else 300.0

    monos = build_pool()
    P = len(monos)
    inputs = list(itertools.product((0, 1), repeat=N))
    A = np.zeros((1024, P), dtype=np.int64)
    is_one = np.zeros(1024, dtype=bool)
    for r, z in enumerate(inputs):
        supp = frozenset(j for j in range(N) if z[j])
        is_one[r] = sum(1 for i in range(K)
                        if z[2 * i] or z[2 * i + 1]) >= T
        for cidx, S in enumerate(monos):
            if S <= supp:
                A[r, cidx] = 1
    ones_idx, zeros_idx = np.where(is_one)[0], np.where(~is_one)[0]
    print(f"pool = {P} monomes (span<=3), budget <= {budget}", flush=True)

    def n_collisions(c):
        """ Nombre d'ENTREES en collision (valeur presente de l'autre cote).
            Un polynome degenere score ~1000 ; un separateur score 0. """
        v = A @ c
        v1, v0 = v[ones_idx], v[zeros_idx]
        bad = np.intersect1d(v1, v0)
        if bad.size == 0:
            return 0
        return int(np.isin(v1, bad).sum() + np.isin(v0, bad).sum())

    idx_of = {S: i for i, S in enumerate(monos)}

    def base_mod(M):
        c = np.zeros(P, dtype=np.int64)
        for i in range(K):
            x, y = 2 * i, 2 * i + 1
            c[idx_of[frozenset([x])]] = 1
            c[idx_of[frozenset([y])]] = 1
            c[idx_of[frozenset([x, y])]] = M - 1
        return c

    best_overall = (10 ** 9, None)
    t0 = time.time()
    restarts = 0
    while time.time() - t0 < tl:
        restarts += 1
        r = RNG.random()
        if r < 0.45:
            c = base_mod(4)          # poids 25, 4 de marge
        elif r < 0.9:
            c = base_mod(3)          # poids 20, 9 de marge
        else:
            c = base_mod(RNG.integers(3, 6))
        # perturbation initiale : deplacer un peu de poids vers le croise
        for _ in range(RNG.integers(1, 8)):
            c[RNG.integers(P)] += 1
        while c.sum() > budget:
            nz = np.where(c > 0)[0]
            c[RNG.choice(nz)] -= 1

        cur = n_collisions(c)
        temp = 3.0
        for step in range(4000):
            if cur == 0:
                break
            temp = max(0.05, temp * 0.999)
            c2 = c.copy()
            if RNG.random() < 0.5 and c2.sum() < budget:
                c2[RNG.integers(P)] += 1
            else:
                nz = np.where(c2 > 0)[0]
                if nz.size == 0:
                    continue
                c2[RNG.choice(nz)] -= 1
            n2 = n_collisions(c2)
            if n2 <= cur or RNG.random() < np.exp((cur - n2) / temp):
                c, cur = c2, n2
        if cur < best_overall[0]:
            best_overall = (cur, c.copy())
            print(f"  [{time.time()-t0:5.0f}s] restart {restarts}: "
                  f"collisions = {cur}, poids = {c.sum()}", flush=True)
        if cur == 0:
            print("  *** TEMOIN TROUVE ***", flush=True)
            sol = {tuple(sorted(monos[i])): int(c[i])
                   for i in np.where(c > 0)[0]}
            print(f"  support : {sol}", flush=True)
            print(f"  poids : {c.sum()}", flush=True)
            return

    print(f"\nAucun temoin en {restarts} redemarrages / {tl:.0f}s.", flush=True)
    print(f"Meilleur atteint : {best_overall[0]} collisions "
          f"(poids {best_overall[1].sum() if best_overall[1] is not None else '-'})",
          flush=True)


if __name__ == "__main__":
    main()
