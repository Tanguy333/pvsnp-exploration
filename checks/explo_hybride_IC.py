"""
EXPLORATION -- hybrides I/C : existe-t-il des instances ou un melange
strict des jauges identite (primale) et Mobius (duale) bat les deux pures ?

Rappel (explo_min_support_jauge.py) :
  S(identite) = #affectations de poids non nul (= #SAT a w=0) ;
  S(Mobius)   = #sous-ensembles compatibles de clauses (inclusion-exclusion).

PREDICTION (avant mesure) : sur une instance DECOMPOSABLE en bloc A
(Mobius-favorable : clauses mutuellement conflictuelles) + bloc B
(identite-favorable : nombreuses clauses sur un meme triplet), les
supports se MULTIPLIENT, donc l'hybride C@A + I@B doit donner
S_C(A) * S_I(B) < min(S_I(A) * S_I(B), S_C(A) * S_C(B)).
  Bloc A : 2 clauses antipodales sur {0,1,2} : S_I = 6, S_C = 3.
  Bloc B : 4 clauses sur {3,4,5} (patterns interdits distincts) :
           S_I = 4, S_C = 5.
  Predictions : pure I = 24, pure C = 15, hybride = 12.

Puis : la question ouverte -- des instances CONNEXES avec victoire
hybride stricte existent-elles ? Balayage aleatoire, exhaustif {I,C}^E.
"""

from __future__ import annotations

import itertools
import time

import numpy as np

RNG = np.random.default_rng(20260809)
I2 = np.eye(2)


def build(n, clauses):
    edges = [(i, a) for a, cl in enumerate(clauses) for (i, _) in cl]
    E = len(edges)
    var_e = {i: [e for e, (j, _) in enumerate(edges) if j == i]
             for i in range(n)}
    cl_e = {a: [e for e, (_, b) in enumerate(edges) if b == a]
            for a in range(len(clauses))}
    lit_pol = {}
    for a, cl in enumerate(clauses):
        for e in cl_e[a]:
            i = edges[e][0]
            lit_pol[e] = dict((v, p) for (v, p) in cl)[i]
    ks = np.arange(1 << E, dtype=np.int64)
    bits = ((ks[:, None] >> np.arange(E)) & 1).astype(np.int64)
    var_idx = {}
    for i in range(n):
        idx = np.zeros(1 << E, dtype=np.int64)
        for pos, e in enumerate(var_e[i]):
            idx |= bits[:, e] << pos
        var_idx[i] = idx
    cl_idx = {}
    for a in range(len(clauses)):
        idx = np.zeros(1 << E, dtype=np.int64)
        for pos, e in enumerate(cl_e[a]):
            idx |= bits[:, e] << pos
        cl_idx[a] = idx
    return edges, E, var_e, cl_e, lit_pol, var_idx, cl_idx


def cw(cl, assign, w):
    return 1.0 if any(assign[v] == p for (v, p) in cl) else w


def exact_Z(n, clauses, w):
    Z = 0.0
    for b in itertools.product((0, 1), repeat=n):
        t = 1.0
        for cl in clauses:
            t *= cw(cl, b, w)
        Z += t
    return Z


def mobius_P(pol):
    viol = 1 - pol
    delta = np.zeros(2)
    delta[viol] = 1.0
    w1 = 2 * delta - np.ones(2)
    Pinv = np.vstack([np.ones(2) - delta, w1])
    return np.linalg.inv(Pinv)


def support(n, clauses, ctx, gauges, w):
    edges, E, var_e, cl_e, lit_pol, var_idx, cl_idx = ctx
    Pinvs = [np.linalg.inv(P) for P in gauges]
    terms = np.ones(1 << E)
    for i in range(n):
        es = var_e[i]
        loc = np.zeros(1 << len(es))
        for kb in range(1 << len(es)):
            p0 = p1 = 1.0
            for pos, e in enumerate(es):
                kk = (kb >> pos) & 1
                p0 *= gauges[e][0, kk]
                p1 *= gauges[e][1, kk]
            loc[kb] = p0 + p1
        terms = terms * loc[var_idx[i]]
    for a, cl in enumerate(clauses):
        es = cl_e[a]
        loc = np.zeros(1 << len(es))
        for kb in range(1 << len(es)):
            tot = 0.0
            for vals in itertools.product((0, 1), repeat=len(cl)):
                assign = {v: val for (v, _), val in zip(cl, vals)}
                weight = cw(cl, assign, w)
                prob = 1.0
                for pos, e in enumerate(es):
                    prob *= Pinvs[e][(kb >> pos) & 1, vals[pos]]
                tot += weight * prob
            loc[kb] = tot
        terms = terms * loc[cl_idx[a]]
    nz = int((np.abs(terms) > 1e-9).sum())
    return nz, float(terms.sum())


def gauges_of(mask, E, lit_pol):
    return [mobius_P(lit_pol[e]) if (mask >> e) & 1 else I2
            for e in range(E)]


def exhaustive_IC(n, clauses, w, verbose=True):
    ctx = build(n, clauses)
    edges, E = ctx[0], ctx[1]
    lit_pol = ctx[4]
    Zx = exact_Z(n, clauses, w)
    S_I, t_I = support(n, clauses, ctx, gauges_of(0, E, lit_pol), w)
    S_C, t_C = support(n, clauses, ctx, gauges_of((1 << E) - 1, E, lit_pol), w)
    best_hyb = (10 ** 9, None)
    for mask in range(1, (1 << E) - 1):        # strictement mixtes
        S, tot = support(n, clauses, ctx, gauges_of(mask, E, lit_pol), w)
        if abs(tot - Zx) < 1e-6 and S < best_hyb[0]:
            best_hyb = (S, mask)
    win = best_hyb[0] < min(S_I, S_C)
    if verbose:
        print(f"  S_I = {S_I}, S_C = {S_C}, meilleur hybride strict = "
              f"{best_hyb[0]} (mask {best_hyb[1]:b})"
              f"   victoire hybride stricte : {'OUI' if win else 'non'}")
    return S_I, S_C, best_hyb, win


def main():
    w = 0.0

    # ------------------------------------------------ temoin decomposable
    print("### 1. Temoin DECOMPOSABLE construit (predictions 24 / 15 / 12)")
    A = [((0, 1), (1, 1), (2, 1)), ((0, 0), (1, 0), (2, 0))]
    B = [((3, 1), (4, 1), (5, 1)), ((3, 0), (4, 0), (5, 0)),
         ((3, 1), (4, 1), (5, 0)), ((3, 1), (4, 0), (5, 1))]
    clauses = A + B
    n = 6
    ctx = build(n, clauses)
    edges, E, lit_pol = ctx[0], ctx[1], ctx[4]
    Zx = exact_Z(n, clauses, w)
    print(f"  n={n}, m={len(clauses)}, E={E}, #SAT = {Zx:.0f}")
    S_I, tI = support(n, clauses, ctx, gauges_of(0, E, lit_pol), w)
    S_C, tC = support(n, clauses, ctx, gauges_of((1 << E) - 1, E, lit_pol), w)
    maskA = 0
    for e in range(E):
        if edges[e][1] < 2:          # clauses du bloc A -> Mobius
            maskA |= (1 << e)
    S_H, tH = support(n, clauses, ctx, gauges_of(maskA, E, lit_pol), w)
    print(f"  pure I : S = {S_I} (predit 24)   somme = {tI:.1f}")
    print(f"  pure C : S = {S_C} (predit 15)   somme = {tC:.1f}")
    print(f"  hybride C@A + I@B : S = {S_H} (predit 12)   somme = {tH:.1f}")
    print()

    # --------------------------------------- balayage d'instances CONNEXES
    print("### 2. Balayage aleatoire d'instances CONNEXES n=4, m=4 (E=12),")
    print("###    exhaustif {I,C}^12, w = 0")
    wins = 0
    total = 0
    t0 = time.time()
    for trial in range(30):
        cls = []
        for _ in range(4):
            vs = sorted(RNG.choice(4, size=3, replace=False).tolist())
            pol = [int(RNG.integers(2)) for _ in range(3)]
            cls.append(tuple((v, p) for v, p in zip(vs, pol)))
        # connexite du graphe variable-clause (naif : union des supports)
        seen = {0}
        frontier = True
        while frontier:
            frontier = False
            for cl in cls:
                vs = {v for (v, _) in cl}
                if vs & seen and not vs <= seen:
                    seen |= vs
                    frontier = True
        if seen != set(range(4)):
            continue
        total += 1
        S_I, S_C, best_hyb, win = exhaustive_IC(4, cls, w, verbose=False)
        if win:
            wins += 1
            print(f"  VICTOIRE HYBRIDE sur {cls} :")
            print(f"    S_I={S_I} S_C={S_C} hybride={best_hyb[0]} "
                  f"(mask {best_hyb[1]:012b})")
    print(f"  {total} instances connexes testees, victoires hybrides "
          f"strictes : {wins}  [{time.time()-t0:.0f}s]")
    print()

    print("### 3. Balayage n=5, m=5 (E=15), 6 instances connexes, w = 0")
    t0 = time.time()
    wins5 = 0
    tot5 = 0
    for trial in range(12):
        cls = []
        for _ in range(5):
            vs = sorted(RNG.choice(5, size=3, replace=False).tolist())
            pol = [int(RNG.integers(2)) for _ in range(3)]
            cls.append(tuple((v, p) for v, p in zip(vs, pol)))
        seen = {0}
        frontier = True
        while frontier:
            frontier = False
            for cl in cls:
                vs = {v for (v, _) in cl}
                if vs & seen and not vs <= seen:
                    seen |= vs
                    frontier = True
        if seen != set(range(5)) or tot5 >= 6:
            continue
        tot5 += 1
        S_I, S_C, best_hyb, win = exhaustive_IC(5, cls, w, verbose=False)
        mark = "VICTOIRE HYBRIDE" if win else "non"
        print(f"  instance {tot5}: S_I={S_I} S_C={S_C} "
              f"hybride={best_hyb[0]} -> {mark}")
        if win:
            wins5 += 1
            print(f"    clauses = {cls}")
    print(f"  victoires : {wins5}/{tot5}  [{time.time()-t0:.0f}s]")


if __name__ == "__main__":
    main()
