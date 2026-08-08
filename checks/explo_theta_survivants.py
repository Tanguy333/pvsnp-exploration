"""
ETAPE FINALE ROUTE-L : faisabilite algebrique des 2 survivants
combinatoires (bras diagonaux + A tue les paires / C tue les impairs,
et le miroir u<->v).

REDUCTION (gauge-fixing par echelles de colonnes, licite car le motif de
zeros est invariant) : par arete u : p00 = p01 = 1, variable a_i = p10,
p11 = t*a_i (structure << A tue exactement les paires >> : ratio commun t,
t hors {0, +1, -1}, t^2 * prod a_i = -1). Par arete v : r00 = r01 = 1,
b_i = r10, r11 = -b_i (<< C tue exactement les impairs >> : t' = -1,
prod b_i = 1). Zeros de bras N_i = 2 x z^T - y w^T (route L) :
  N[0,1] = 0  <=>  2(t a_i - 1)(1 - b_i) + t a_i b_i = 0        (E1)
  N[1,0] = 0  <=>  2(1 - a_i)(1 + b_i) + a_i b_i = 0            (E2)
Non-nuls requis : N[0,0], N[1,1], a_i, b_i, t(t-1)(t+1), (2 - a_i).

Ce script : (0) VALIDE la reduction numeriquement (echantillon E1&E2 =>
motif diagonal effectif dans le reseau complet) ; (1) Groebner exact sur
le systeme ; (2) si solutions : construction du temoin et verification
support_cplx de bout en bout ; si 1 dans l'ideal : ROUTE-L NON-DEGENEREE
FERMEE => min-S(theta) >= 2 dans ce regime.
"""

from __future__ import annotations

import itertools
import sys
import time
from pathlib import Path

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).parent))
from explo_test_theta import support_cplx, ZX, E, EDGES


# ---------------- (0) validation numerique de la reduction ----------------

def build_full_gauges(a_vals, b_vals, t_val):
    """ Construit les 9 jauges completes depuis (a_i, b_i, t) :
        P_i = [[1, 1], [a_i, t a_i]], R_i = [[1, 1], [b_i, -b_i]],
        feuilles : route L (colonne 1 de Q de somme nulle),
        Q = [[1, 1], [1, -1]] (Hadamard, tue k=1, dual (1,1)/2). """
    HADQ = np.array([[1.0, 1.0], [1.0, -1.0]], dtype=complex)
    P = {}
    for i in range(3):
        Pu = np.array([[1, 1], [a_vals[i], t_val * a_vals[i]]], dtype=complex)
        Rv = np.array([[1, 1], [b_vals[i], -b_vals[i]]], dtype=complex)
        # ordre des aretes (build sur theta) : par clause i :
        # (u=0, c_i), (v=1, c_i), (feuille, c_i)
        P[3 * i] = Pu
        P[3 * i + 1] = Rv
        P[3 * i + 2] = HADQ
    return [P[e] for e in range(9)]


def numeric_validation():
    """ E1 & E2 pour un a generique => zeros N[0,1], N[1,0] dans le
        RESEAU COMPLET (support de la tranche t=0 sans les motifs 01/10
        de chaque bras). Validation indirecte : support et somme. """
    t = sp.Symbol('t')
    a = sp.Symbol('a')
    # depuis E1 et E2 : b = 2(a-1)/(2-a) et t = (4-3a)/(a(3-2a))
    a0 = sp.Rational(1, 3)
    b0 = 2 * (a0 - 1) / (2 - a0)
    t0 = (4 - 3 * a0) / (a0 * (3 - 2 * a0))
    G = build_full_gauges([complex(a0)] * 3, [complex(b0)] * 3, complex(t0))
    S, tot = support_cplx(G)
    print(f"  validation (a=b=meme racine, sans contrainte produit) :")
    print(f"    a = {a0}, b = {b0}, t = {t0}")
    print(f"    S = {S}, somme = {tot.real:.4f} (Z = {ZX:.0f}) "
          f"[la somme DOIT etre 25 : jauges valides]")
    return abs(tot - ZX) < 1e-6


# ---------------- (1) systeme exact et Groebner ----------------

def groebner_survivor():
    a1, a2, a3, b1, b2, b3, t, tau = sp.symbols('a1 a2 a3 b1 b2 b3 t tau')
    A = [a1, a2, a3]
    B = [b1, b2, b3]
    eqs = []
    nonzeros = [t, t - 1, t + 1]
    for ai, bi in zip(A, B):
        eqs.append(sp.expand(2 * (t * ai - 1) * (1 - bi) + t * ai * bi))  # E1
        eqs.append(sp.expand(2 * (1 - ai) * (1 + bi) + ai * bi))          # E2
        # non-nuls : N[0,0] et N[1,1] (formes reduites), a_i, b_i, 2-a_i
        N00 = sp.expand(-2 * (t * ai - 1) * (1 + bi) + t * ai * bi)
        N11 = sp.expand(2 * (1 - ai) * (1 - bi) - ai * bi)
        nonzeros += [ai, bi, 2 - ai, N00, N11]
    eqs.append(sp.expand(t ** 2 * a1 * a2 * a3 + 1))     # prod a = -1/t^2
    eqs.append(sp.expand(b1 * b2 * b3 - 1))              # prod b = 1
    prod_nz = sp.expand(sp.prod(nonzeros))
    eqs.append(sp.expand(tau * prod_nz - 1))             # Rabinowitsch

    t0 = time.time()
    gb = sp.groebner(eqs, a1, a2, a3, b1, b2, b3, t, tau, order='grevlex')
    infeasible = list(gb.exprs) == [sp.Integer(1)]
    dt = time.time() - t0
    print(f"  Groebner ({len(eqs)} equations, 8 variables) : "
          f"{'1 DANS L IDEAL -- INFAISABLE' if infeasible else 'FAISABLE (base non triviale)'}"
          f"  ({dt:.1f}s)")
    return infeasible, gb


def try_solve_witness():
    """ Si faisable : resoudre numeriquement et verifier le temoin. """
    a1, a2, a3, b1, b2, b3, t = sp.symbols('a1 a2 a3 b1 b2 b3 t')
    A = [a1, a2, a3]
    B = [b1, b2, b3]

    def bi_of(ai):
        return 2 * (ai - 1) / (2 - ai)

    # racines de 2t a^2 - 3(t+1) a + 4 = 0 par arme + contraintes globales
    # -> resolution par cas de signes (k racines '+', 3-k racines '-')
    q = lambda ai: 2 * t * ai ** 2 - 3 * (t + 1) * ai + 4
    sols_found = []
    for k in range(4):
        # a1..ak = racine 1, le reste racine 2 : impose q(ai) = 0 et
        # l'egalite/difference des racines via les contraintes globales.
        eqs = [q(ai) for ai in A]
        # pattern des racines : premiers k egaux, derniers 3-k egaux
        for i in range(1, k):
            eqs.append(A[i] - A[0])
        for i in range(k + 1, 3):
            eqs.append(A[i] - A[k] if k < 3 else 0)
        if 0 < k < 3:
            eqs.append((A[0] - A[k]))  # racines DIFFERENTES : traite apres
        eqs = [e for e in eqs if e != 0]
        eqs.append(t ** 2 * A[0] ** (0) * sp.prod(A) + 1)
        eqs.append(sp.prod([bi_of(ai) for ai in A]) - 1)
        try:
            sols = sp.solve(eqs, A + [t], dict=True)
        except Exception as exc:
            print(f"    cas k={k} : solve echoue ({exc})")
            continue
        for s in sols:
            tv = s.get(t)
            if tv is None or tv in (0, 1, -1):
                continue
            avals = [complex(sp.N(s.get(ai, s.get(A[0])))) for ai in A]
            bvals = [complex(sp.N(bi_of(ai).subs(s))) for ai in A]
            sols_found.append((avals, bvals, complex(sp.N(tv))))
    print(f"  solutions candidates : {len(sols_found)}")
    for (av, bv, tv) in sols_found[:6]:
        G = build_full_gauges(av, bv, tv)
        try:
            S, tot = support_cplx(G)
        except np.linalg.LinAlgError:
            print("    candidat degenere (jauge singuliere)")
            continue
        ok = abs(tot - ZX) < 1e-6
        print(f"    t = {tv:.4f} : S = {S}, somme = {tot.real:.4f} "
              f"({'valide' if ok else 'jauge invalide'})"
              + ("   *** TEMOIN SUPPORT 1 ***" if ok and S == 1 else ""))


def main():
    print("Survivants route-L : etape algebrique finale")
    print("=" * 70)
    print("(0) validation de la reduction :")
    ok = numeric_validation()
    print(f"    reduction {'VALIDEE' if ok else 'INVALIDE -- STOP'}")
    print()
    if not ok:
        return
    print("(1) faisabilite exacte (Groebner) :")
    infeasible, gb = groebner_survivor()
    print()
    if infeasible:
        print("CONCLUSION : le survivant (et son miroir u<->v, par symetrie")
        print("de la clause en u,v) est INFAISABLE. Combine a la fermeture")
        print("combinatoire (84 500 combinaisons, 2 survivants) :")
        print("  *** ROUTE-L NON-DEGENEREE FERMEE : support 1 impossible ***")
    else:
        print("(2) resolution et verification du temoin :")
        try_solve_witness()


if __name__ == "__main__":
    main()
