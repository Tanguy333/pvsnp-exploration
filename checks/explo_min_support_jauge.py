"""
EXPLORATION -- min-support de jauge : le 624 est-il compressible ?

Question (suite de explo_jauge_quatre_iles.py) : sur l'instance loopy
n=5, m=5 (15 aretes), la jauge BP donne 625 termes non nuls (vide + 624
boucles generalisees). Quel est le MINIMUM de S(jauge) = #termes non nuls,
sur de meilleures jauges ?

FAITS STRUCTURELS (verifies ici) :
  - jauge IDENTITE : les tenseurs copie sont maximalement creux (support
    << tous k egaux >>), les clauses pleines -> S = #affectations a poids
    non nul = 2^n (w > 0) ou #SAT (w = 0). Ici : 32 et 16.
  - jauge ALIGNEE-CLAUSE (base {vecteur tout-1, indicatrice du litteral
    violant}) : les clauses deviennent support 2, mais les copies
    deviennent PLEINES -> S = 2^m = 32. Antagonisme des deux masters.
  - jauge BP : creuse en MAGNITUDE (vide = Z_Bethe), dense en SUPPORT.

RECHERCHE : dictionnaire de jauges par arete {I, C, H, BP, R1, R2} ;
  (1) exhaustif sur {I, C}^15 (32768 configurations) ;
  (2) recuit simule sur le dictionnaire complet.
Chaque S est calcule exactement (32768 termes, numpy), et le minimum
trouve est re-verifie : somme des termes = Z exact.
"""

from __future__ import annotations

import itertools
import time

import numpy as np

RNG = np.random.default_rng(20260808)

# ------------------------------------------------------------ instance

N = 5
CLAUSES = [((0, 1), (1, 1), (2, 0)),
           ((1, 1), (2, 1), (3, 1)),
           ((2, 1), (3, 0), (4, 1)),
           ((0, 1), (3, 1), (4, 0)),
           ((0, 0), (1, 1), (4, 1))]
EDGES = [(i, a) for a, cl in enumerate(CLAUSES) for (i, _) in cl]
E = len(EDGES)
VAR_E = {i: [e for e, (j, _) in enumerate(EDGES) if j == i] for i in range(N)}
CL_E = {a: [e for e, (_, b) in enumerate(EDGES) if b == a] for a in range(len(CLAUSES))}
LIT_POL = {}
for a, cl in enumerate(CLAUSES):
    for (i, p) in cl:
        for e in CL_E[a]:
            if EDGES[e][0] == i:
                LIT_POL[e] = p


def clause_weight(cl, assign, w):
    return 1.0 if any(assign[v] == p for (v, p) in cl) else w


def exact_Z(w):
    Z = 0.0
    for bits in itertools.product((0, 1), repeat=N):
        t = 1.0
        for cl in CLAUSES:
            t *= clause_weight(cl, bits, w)
        Z += t
    return Z


# --------------------------------------------------------- jauges de base

I2 = np.eye(2)
HAD = np.array([[1.0, 1.0], [1.0, -1.0]])


def clause_aligned(e):
    """ Base duale de {1_vec, delta_(valeur violante)} sur l'arete e. """
    viol = 1 - LIT_POL[e]
    delta = np.zeros(2)
    delta[viol] = 1.0
    Pinv = np.vstack([np.ones(2) - delta, delta])  # w0.1=1,w0.delta=0 ; w1
    # correction : w0 doit verifier <w0,1>=1, <w0,delta>=0 ;
    # <(1-delta),1> = 1, <(1-delta),delta> = 0  OK
    # w1 : <w1,1>=0, <w1,delta>=1 -> w1 = delta - (1-delta) ... verif :
    w1 = 2 * delta - np.ones(2)
    Pinv = np.vstack([np.ones(2) - delta, w1])
    return np.linalg.inv(Pinv)


def run_bp(w, iters=4000, damp=0.5):
    m_va = {(i, a): np.array([.5, .5]) for (i, a) in EDGES}
    m_av = {(a, i): np.array([.5, .5]) for (i, a) in EDGES}
    for _ in range(iters):
        for (i, a) in EDGES:
            prod = np.ones(2)
            for e in VAR_E[i]:
                b = EDGES[e][1]
                if b != a:
                    prod = prod * m_av[(b, i)]
            new = prod / prod.sum()
            m_va[(i, a)] = damp * m_va[(i, a)] + (1 - damp) * new
        for (i, a) in EDGES:
            cl = CLAUSES[a]
            others = [(v, p) for (v, p) in cl if v != i]
            out = np.zeros(2)
            for si in (0, 1):
                tot = 0.0
                for vals in itertools.product((0, 1), repeat=len(others)):
                    assign = {i: si}
                    prob = 1.0
                    for (v, _), val in zip(others, vals):
                        assign[v] = val
                        prob *= m_va[(v, a)][val]
                    tot += clause_weight(cl, assign, w) * prob
                out[si] = tot
            m_av[(a, i)] = damp * m_av[(a, i)] + (1 - damp) * out / out.sum()
    G = []
    for (i, a) in EDGES:
        v0 = m_av[(a, i)].copy()
        w0 = m_va[(i, a)].copy()
        w0 = w0 / (w0 @ v0)
        v1 = np.array([-w0[1], w0[0]])
        G.append(np.column_stack([v0, v1]))
    return G


# ------------------------------------------- evaluation vectorisee de S

KS = np.arange(1 << E, dtype=np.int64)
BITS = ((KS[:, None] >> np.arange(E)) & 1).astype(np.int8)   # (2^E, E)

VAR_IDX = {}
for i in range(N):
    es = VAR_E[i]
    idx = np.zeros(1 << E, dtype=np.int64)
    for pos, e in enumerate(es):
        idx |= (BITS[:, e].astype(np.int64) << pos)
    VAR_IDX[i] = idx
CL_IDX = {}
for a in range(len(CLAUSES)):
    es = CL_E[a]
    idx = np.zeros(1 << E, dtype=np.int64)
    for pos, e in enumerate(es):
        idx |= (BITS[:, e].astype(np.int64) << pos)
    CL_IDX[a] = idx


def support_and_sum(gauges, w):
    """ Renvoie (S, somme des termes). gauges = liste de 15 matrices 2x2. """
    Pinvs = [np.linalg.inv(P) for P in gauges]
    terms = np.ones(1 << E)
    for i in range(N):
        es = VAR_E[i]
        d = len(es)
        loc = np.zeros(1 << d)
        for kbits in range(1 << d):
            p0 = p1 = 1.0
            for pos, e in enumerate(es):
                kk = (kbits >> pos) & 1
                p0 *= gauges[e][0, kk]
                p1 *= gauges[e][1, kk]
            loc[kbits] = p0 + p1
        terms = terms * loc[VAR_IDX[i]]
    for a, cl in enumerate(CLAUSES):
        es = CL_E[a]
        loc = np.zeros(1 << len(es))
        for kbits in range(1 << len(es)):
            tot = 0.0
            for vals in itertools.product((0, 1), repeat=len(cl)):
                assign = {v: val for (v, _), val in zip(cl, vals)}
                weight = clause_weight(cl, assign, w)
                prob = 1.0
                for pos, e in enumerate(es):
                    kk = (kbits >> pos) & 1
                    prob *= Pinvs[e][kk, vals[pos]]
                tot += weight * prob
            loc[kbits] = tot
        terms = terms * loc[CL_IDX[a]]
    nz = np.abs(terms) > 1e-9
    return int(nz.sum()), float(terms.sum())


def main():
    for w in (0.0, 0.3):
        Zx = exact_Z(w)
        print(f"===== w = {w}   (Z exacte = {Zx:.6f}"
              + ("  = #SAT" if w == 0 else "") + ") =====")

        bp = run_bp(w)
        R1 = [np.array(RNG.normal(size=(2, 2))) for _ in range(E)]
        R2 = [np.array(RNG.normal(size=(2, 2))) for _ in range(E)]
        CA = [clause_aligned(e) for e in range(E)]

        base_gauges = {
            "identite": [I2] * E,
            "alignee-clause": CA,
            "Hadamard": [HAD] * E,
            "BP": bp,
            "aleatoire": R1,
        }
        for name, G in base_gauges.items():
            S, tot = support_and_sum(G, w)
            print(f"  jauge {name:<16} : S = {S:>6}   somme = {tot:.6f}"
                  f"   (ecart Z : {abs(tot - Zx):.1e})")

        # (1) exhaustif {I, C}^15
        t0 = time.time()
        best_ic = (10 ** 9, None)
        for mask in range(1 << E):
            G = [CA[e] if (mask >> e) & 1 else I2 for e in range(E)]
            S, tot = support_and_sum(G, w)
            if abs(tot - Zx) < 1e-6 and S < best_ic[0]:
                best_ic = (S, mask)
        print(f"  exhaustif {{I,C}}^15 : min S = {best_ic[0]} "
              f"(mask {best_ic[1]:015b})  [{time.time()-t0:.0f}s]")

        # (2) recuit sur le dictionnaire complet
        dico = ["I", "C", "H", "B", "R1", "R2"]

        def gauge_of(choice):
            out = []
            for e, ch in enumerate(choice):
                out.append({"I": I2, "C": CA[e], "H": HAD, "B": bp[e],
                            "R1": R1[e], "R2": R2[e]}[ch])
            return out

        best = (10 ** 9, None)
        t0 = time.time()
        for restart in range(12):
            choice = [dico[RNG.integers(len(dico))] for _ in range(E)]
            S, tot = support_and_sum(gauge_of(choice), w)
            if abs(tot - Zx) > 1e-6:
                S = 10 ** 9
            cur = S
            temp = 8.0
            for step in range(600):
                temp = max(.3, temp * .99)
                e = RNG.integers(E)
                old = choice[e]
                choice[e] = dico[RNG.integers(len(dico))]
                S2, tot2 = support_and_sum(gauge_of(choice), w)
                if abs(tot2 - Zx) > 1e-6:
                    S2 = 10 ** 9
                if S2 <= cur or RNG.random() < np.exp((cur - S2) / temp):
                    cur = S2
                else:
                    choice[e] = old
                if cur < best[0]:
                    best = (cur, list(choice))
        print(f"  recuit dictionnaire : min S = {best[0]}   "
              f"config = {best[1]}  [{time.time()-t0:.0f}s]")
        S, tot = support_and_sum(gauge_of(best[1]), w)
        print(f"  re-verification du minimum : S = {S}, somme = {tot:.6f} "
              f"(Z = {Zx:.6f})")
        print()


if __name__ == "__main__":
    main()
