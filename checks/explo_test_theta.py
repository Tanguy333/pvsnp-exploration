"""
TEST THETA -- min sur toutes les jauges du support du bloc theta >= 2 ?

BLOC THETA : u, v partages par 3 clauses monotones c_i = (u v v v l_i)
(l_i feuilles). Graphe de facteurs = deux noeuds de degre 3 relies par
trois bras parallele : DEUX cycles independants (dim espace des cycles = 2).
n = 5, m = 3, E = 9, Z = #SAT = 25.

Structure reduite : Z = 8 * somme_{su,sv} prod_i G_i(su,sv), produit
ENTRYWISE (Hadamard) des bras -- c'est la difference structurelle avec le
cycle simple (produit matriciel), et la raison pour laquelle le tour de
la monodromie-compagnon ne s'applique pas tel quel.

LEMME DE RIGIDITE (prouve, verifie ici) : si l'arete-feuille est jaugee
a support 1 (tuer k=1 : colonne 1 de Q de somme nulle), alors la ligne 0
de Q^{-1} est proportionnelle a (1,1). Consequence : la matrice effective
du bras est lambda0*(2J - E00), entrees (1,2,2,2) -- AUCUN zero. L'ansatz
aligne + feuilles-1 a donc support exactement 4.

EXPERIENCE : baselines (I, C, H, BP, aligne), puis minimisation continue
du support sur TOUT l'espace de jauge complexe GL_2(C)^9 (recuit,
redemarrages, graines structurees). Toute valeur atteinte est une borne
SUP du min ; la borne inf reste ouverte (elimination des quantificateurs
non tentee).
"""

from __future__ import annotations

import itertools
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from explo_hybride_IC import build, exact_Z, mobius_P, I2
from explo_pire_cas_min_jauges import bp_gauges_generic

RNG = np.random.default_rng(20260810)
HAD = np.array([[1.0, 1.0], [1.0, -1.0]])

N = 5
CLAUSES = [((0, 1), (1, 1), (2, 1)),
           ((0, 1), (1, 1), (3, 1)),
           ((0, 1), (1, 1), (4, 1))]
CTX = build(N, CLAUSES)
EDGES, E = CTX[0], CTX[1]
LIT_POL = CTX[4]
W = 0.0
ZX = exact_Z(N, CLAUSES, W)

VAR_E = {i: [e for e, (j, _) in enumerate(EDGES) if j == i] for i in range(N)}
CL_E = {a: [e for e, (_, b) in enumerate(EDGES) if b == a]
        for a in range(len(CLAUSES))}


def cw(cl, assign):
    return 1.0 if any(assign[v] == p for (v, p) in cl) else W


def support_cplx(gauges, tol=1e-8):
    """ Support et somme pour jauges complexes (enumeration 2^E exacte). """
    Pinvs = [np.linalg.inv(P) for P in gauges]
    terms = np.ones(1 << E, dtype=np.complex128)
    for i in range(N):
        es = VAR_E[i]
        loc = np.zeros(1 << len(es), dtype=np.complex128)
        for kb in range(1 << len(es)):
            p0 = p1 = 1.0 + 0j
            for pos, e in enumerate(es):
                kk = (kb >> pos) & 1
                p0 *= gauges[e][0, kk]
                p1 *= gauges[e][1, kk]
            loc[kb] = p0 + p1
        terms = terms * loc[CTX[5][i]]
    for a, cl in enumerate(CLAUSES):
        es = CL_E[a]
        loc = np.zeros(1 << len(es), dtype=np.complex128)
        for kb in range(1 << len(es)):
            tot = 0.0 + 0j
            for vals in itertools.product((0, 1), repeat=len(cl)):
                assign = {v: val for (v, _), val in zip(cl, vals)}
                weight = cw(cl, assign)
                prob = 1.0 + 0j
                for pos, e in enumerate(es):
                    prob *= Pinvs[e][(kb >> pos) & 1, vals[pos]]
                tot += weight * prob
            loc[kb] = tot
        terms = terms * loc[CTX[6][a]]
    mx = np.abs(terms).max()
    S = int((np.abs(terms) > tol * max(mx, 1e-30)).sum())
    return S, complex(terms.sum())


def rigidity_check():
    """ Verifie le lemme : colonne-1 de Q de somme nulle => ligne 0 de
        Q^{-1} proportionnelle a (1,1). """
    ok = True
    for _ in range(200):
        a, b, c = RNG.normal(size=3)
        if abs(b) < .1 or abs(a + c) < .1:
            continue
        Q = np.array([[a, b], [c, -b]])          # colonne 1 : somme nulle
        w0 = np.linalg.inv(Q)[0]
        ok &= abs(w0[0] - w0[1]) < 1e-9 * max(1, abs(w0[0]))
    return ok


def aligned_ansatz():
    """ Jauges diagonales partout + feuilles Hadamard. """
    G = []
    for e in range(E):
        i, a = EDGES[e]
        G.append(HAD if i >= 2 else np.diag([1.0, 1.0]))
    return [g.astype(np.complex128) for g in G]


def anneal(seed_gauges, steps=4000, temp0=2.0, sigma=0.35):
    G = [g.copy().astype(np.complex128) for g in seed_gauges]
    S, tot = support_cplx(G)
    if abs(tot - ZX) > 1e-6 * max(1, abs(ZX)):
        S = 10 ** 9
    best = S
    cur = S
    temp = temp0
    for step in range(steps):
        temp = max(0.02, temp * 0.9985)
        e = RNG.integers(E)
        old = G[e].copy()
        G[e] = G[e] + sigma * (RNG.normal(size=(2, 2))
                               + 1j * RNG.normal(size=(2, 2)))
        if abs(np.linalg.det(G[e])) < 1e-6:
            G[e] = old
            continue
        S2, tot2 = support_cplx(G)
        bad = abs(tot2 - ZX) > 1e-6 * max(1, abs(ZX))
        S2e = 10 ** 9 if bad else S2
        if S2e <= cur or RNG.random() < np.exp((cur - S2e) / temp):
            cur = S2e
            best = min(best, cur)
        else:
            G[e] = old
    return best, G


def main():
    print("TEST THETA : min du support sur toutes les jauges ?")
    print("=" * 70)
    print(f"instance : n={N}, m={len(CLAUSES)}, E={E}, Z = #SAT = {ZX:.0f}")
    print(f"lemme de rigidite (feuille-1 => dual (1,1)) : "
          f"{'VERIFIE' if rigidity_check() else 'ECHEC ?!'}")
    print()

    bp = bp_gauges_generic(N, CLAUSES, W)
    baselines = {
        "identite": [I2.astype(np.complex128)] * E,
        "Mobius": [mobius_P(LIT_POL[e]).astype(np.complex128)
                   for e in range(E)],
        "Hadamard": [HAD.astype(np.complex128)] * E,
        "BP": [g.astype(np.complex128) for g in bp],
        "aligne+feuilles-1": aligned_ansatz(),
    }
    for name, G in baselines.items():
        S, tot = support_cplx(G)
        print(f"  {name:<20} : S = {S:>4}   somme = {tot.real:.4f}")
    print()

    print("Minimisation continue (recuit complexe, 40 redemarrages) :")
    t0 = time.time()
    overall = 10 ** 9
    hist = {}
    for restart in range(40):
        r = RNG.random()
        if r < 0.25:
            seed = aligned_ansatz()
        elif r < 0.5:
            seed = [g.astype(np.complex128) for g in bp]
        elif r < 0.7:
            seed = [mobius_P(LIT_POL[e]).astype(np.complex128)
                    for e in range(E)]
        else:
            seed = [np.array(RNG.normal(size=(2, 2))
                             + 1j * RNG.normal(size=(2, 2)))
                    for _ in range(E)]
            seed = [g if abs(np.linalg.det(g)) > .2
                    else g + np.eye(2) for g in seed]
        best, G = anneal(seed)
        hist[best] = hist.get(best, 0) + 1
        if best < overall:
            overall = best
            S, tot = support_cplx(G)
            print(f"  [{time.time()-t0:5.0f}s] restart {restart}: "
                  f"S = {best} (somme = {tot.real:.4f})", flush=True)
            if best == 1:
                print("  *** SUPPORT 1 TROUVE : A survit sur le theta ***")
                break
    print(f"\n  distribution des minima atteints : {dict(sorted(hist.items()))}")
    print(f"  MIN GLOBAL TROUVE : {overall}   [{time.time()-t0:.0f}s]")
    print()
    print("LECTURE : toute valeur = borne SUP du vrai min (recherche).")
    print("Si le min trouve est 2 ou 3 malgre les graines structurees et")
    print("les redemarrages, c'est une evidence (pas une preuve) que le")
    print("theta resiste au support 1 -- la borne inf exacte demanderait")
    print("l'elimination des quantificateurs sur GL_2(C)^9.")


if __name__ == "__main__":
    main()
