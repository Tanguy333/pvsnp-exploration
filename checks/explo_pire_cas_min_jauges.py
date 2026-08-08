"""
VERIFICATION -- le min des deux jauges pures (identite, Mobius) est
exponentiel dans le pire cas : PREUVE par famille explicite + mesure.

PROPOSITION (prouvee, verifiee ici) :
  Famille chaine monotone C_m : n = 2m+1 variables
  {x_1..x_{m+1}, y_1..y_m}, m clauses c_j = (x_j v y_j v x_{j+1}),
  littéraux tous positifs. Alors, a w = 0 :
  (1) S_C(C_m) = 2^m EXACTEMENT. Preuve : chaque clause allumee force
      ses 3 variables a 0 ; toutes les contraintes forcent des 0, jamais
      de 1 -> aucun conflit possible -> tous les 2^m sous-ensembles de
      clauses sont compatibles.
  (2) S_I(C_m) = #SAT >= 2^m. Preuve : poser x_j := 1 pour tout j
      satisfait toutes les clauses ; les m variables y_j restent libres.
  (3) Donc min(S_I, S_C) >= 2^m = 2^{(n-1)/2} : EXPONENTIEL,
      inconditionnellement.

RAFFINEMENT (verifie aussi) : le graphe de facteurs de C_m est un ARBRE
(les clauses forment un chemin via les x_j, les y_j sont des feuilles).
Donc la jauge BP donne S = 1 : le min sur TOUTES les jauges s'effondre
a 1 sur cette famille. L'exponentialite du min des deux jauges PURES ne
dit rien du min de l'orbite complete ; pour celui-ci, l'exponentialite
pire-cas est exactement conditionnelle a #P != FP (un min-S polynomial
constructif donnerait #SAT en temps polynomial).

Verification numerique : m = 2..5 pour la chaine ; famille disjointe
D_t (t clauses disjointes, S_I = 7^t, S_C = 2^t) pour t = 1..3.
"""

from __future__ import annotations

import itertools

import numpy as np

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from explo_hybride_IC import build, exact_Z, support, gauges_of, mobius_P, I2


def chain_instance(m):
    """ C_m : vars x_j = 0..m, y_j = m+1..2m ; clause j = (x_j, y_j, x_{j+1}). """
    n = 2 * m + 1
    clauses = [((j, 1), (m + 1 + j, 1), (j + 1, 1)) for j in range(m)]
    return n, clauses


def disjoint_instance(t):
    n = 3 * t
    clauses = [((3 * j, 1), (3 * j + 1, 1), (3 * j + 2, 1)) for j in range(t)]
    return n, clauses


def bp_gauges_generic(n, clauses, w, iters=3000, damp=0.5):
    edges = [(i, a) for a, cl in enumerate(clauses) for (i, _) in cl]
    var_e = {i: [(a) for (j, a) in edges if j == i] for i in range(n)}
    m_va = {(i, a): np.array([.5, .5]) for (i, a) in edges}
    m_av = {(a, i): np.array([.5, .5]) for (i, a) in edges}

    def cw_(cl, assign):
        return 1.0 if any(assign[v] == p for (v, p) in cl) else w

    for _ in range(iters):
        for (i, a) in edges:
            prod = np.ones(2)
            for b in var_e[i]:
                if b != a:
                    prod = prod * m_av[(b, i)]
            m_va[(i, a)] = damp * m_va[(i, a)] + (1 - damp) * prod / prod.sum()
        for (i, a) in edges:
            cl = clauses[a]
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
                    tot += cw_(cl, assign) * prob
                out[si] = tot
            m_av[(a, i)] = damp * m_av[(a, i)] + (1 - damp) * out / out.sum()
    G = []
    for (i, a) in edges:
        v0 = m_av[(a, i)].copy()
        w0 = m_va[(i, a)].copy()
        w0 = w0 / (w0 @ v0)
        v1 = np.array([-w0[1], w0[0]])
        G.append(np.column_stack([v0, v1]))
    return G


def analyse_family(label, make, params, w=0.0, with_bp=True):
    print(f"### {label} ###")
    print(f"  {'param':>5} | {'n':>3} {'m':>3} {'E':>3} | {'#SAT':>6} | "
          f"{'S_I':>6} | {'S_C':>6} | {'min':>6} | {'2^m':>5} | {'S_BP':>5}")
    prev_min = None
    for p in params:
        n, clauses = make(p)
        ctx = build(n, clauses)
        E, lit_pol = ctx[1], ctx[4]
        Zx = exact_Z(n, clauses, w)
        S_I, tI = support(n, clauses, ctx, gauges_of(0, E, lit_pol), w)
        S_C, tC = support(n, clauses, ctx,
                          gauges_of((1 << E) - 1, E, lit_pol), w)
        assert abs(tI - Zx) < 1e-6 and abs(tC - Zx) < 1e-6
        sbp = "-"
        if with_bp:
            G = bp_gauges_generic(n, clauses, w)
            S_B, tB = support(n, clauses, ctx, G, w)
            assert abs(tB - Zx) < 1e-5, (tB, Zx)
            sbp = str(S_B)
        mn = min(S_I, S_C)
        ratio = f"  (x{mn/prev_min:.2f})" if prev_min else ""
        prev_min = mn
        m = len(clauses)
        print(f"  {p:>5} | {n:>3} {m:>3} {E:>3} | {Zx:>6.0f} | {S_I:>6} | "
              f"{S_C:>6} | {mn:>6} | {2**m:>5} | {sbp:>5}{ratio}")
    print()


def main():
    print("Le min des deux jauges pures est-il exponentiel au pire cas ?")
    print("=" * 74)
    analyse_family(
        "Chaine monotone C_m (connexe ; prevu : S_C = 2^m, S_I >= 2^m, "
        "S_BP = 1 [arbre])",
        chain_instance, [2, 3, 4, 5])
    analyse_family(
        "Clauses disjointes D_t (prevu : S_I = 7^t, S_C = 2^t, S_BP = 1)",
        disjoint_instance, [1, 2, 3])
    print("Lecture : min(S_I, S_C) double a chaque clause ajoutee sur C_m")
    print("(= 2^m, prouve), alors que le min sur TOUTES les jauges vaut 1")
    print("(jauge BP, structure d'arbre) : l'exponentialite pire-cas des")
    print("deux jauges pures est PROUVEE ; celle de l'orbite complete est")
    print("exactement la question #P vs FP (conditionnelle).")


if __name__ == "__main__":
    main()
