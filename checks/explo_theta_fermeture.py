"""
FERMETURE (partielle, rigoureuse) DU CAS NON-ALIGNE DU BLOC THETA
+ preuve de la chaine : min >= 2 par bloc => min >= 2^r => A_exist refutee.

=== THEOREME A (chaine d'implications, PROUVE) ===
Lemme A1 (multiplicativite) : pour N = N1 ⊔ N2 (union disjointe) et TOUTE
jauge par arete G : term_N(k1,k2) = term_{N1}(k1|G1) * term_{N2}(k2|G2)
(chaque noeud appartient a une seule composante ; son facteur local ne
depend que des bits de ses aretes). Donc S_N(G) = S_{N1}(G1)*S_{N2}(G2)
et min_G S_N = (min S_{N1})(min S_{N2}).
Corollaire A2 : min-S(theta) >= 2 => min-S(Theta_r) >= 2^r.
Corollaire A3 : Theta_r est une 3-CNF a n = 5r variables avec
min-S superpolynomial => A_exist (support polynomial pour toutes les
instances, MEME non constructif) est FAUSSE.
[Verification numerique de A1 sur theta ⊔ theta incluse.]

=== THEOREME B (theta : cas fermes) ===
Cadre : support 1 en k* = 0 (WLOG par relabel des colonnes). Variables
par bras i : x=P_i^{-1}1, y=P_i^{-1}d0 (u-cote), z,w (v-cote), s,r
(feuille). Facteurs : A(a) (copie u), C(b) (copie v), L_i(t) (feuille,
L(1)=0 <=> feuille tuee), B_i(a,b,t) = x_a z_b s_t - y_a w_b r_t.
Flip de la feuille i depuis k* : (dagger_i) L_i(1) = 0 OU B_i(0,0,1) = 0
-- dichotomie route L / route B par bras.

Lemme B1 (PROUVE symboliquement ici) : bras route L (feuille tuee) =>
(s0,r0) prop. (2,1) => matrice de bras N = 2 x z^T - y w^T avec
det N = -2 det[x|y] det[z|w] != 0 : TOUJOURS INVERSIBLE. Zeros exacts
possibles (avec N[0,0] != 0) : vide, {01}, {10}, {11}, {01,10}.

Lemme B2 (PROUVE symboliquement) : en regime non-degenere (aucune entree
nulle dans P), deux motifs tues par A a distance de Hamming 1 forcent
det P = 0 : identite p02[1]*K1 - p02[0]*K2 = -p11[1]*p13[0]*det(P2).

Lemme B3 (structure des tues de A, non-degenere) : A(a) = 0 <=>
prod_{i in supp(a)} t_i = c avec t_i = ratio(lignes de P_i) != 1, c != 1.
Donc l'ensemble tue S est realisable ssi le sous-groupe de Z^3 engendre
par les differences de S ne contient ni les e_i, ni aucun a - a''
(a in S, a'' hors S). CRITERE DE RESEAU ENTIER -- enumere ci-dessous.

FERMETURE ROUTE-L NON-DEGENEREE (machine, ce script) :
en route L totale, les motifs t != 0 sont morts (feuilles) ; la tranche
t = 0 exige : pour tout (a,b) dans supp(A) x supp(C) \ {(0,0)} :
un bras i avec (a_i,b_i) dans Z_i. On enumere TOUS les (Z_1,Z_2,Z_3)
(5^3) x TOUTES les paires (supp(A), supp(C)) realisables (lemme B3) et
on verifie la couverture. Si aucune combinaison ne passe, le cas est
FERME. Si certaines passent combinatoirement, elles sont listees pour
l'etape algebrique (Groebner joint).

RESIDUS NON FERMES ICI (nommes) : aretes u/v a entree nulle isolee
(types degeneres non-monomiaux -- le cas monomial = famille alignee,
fermee a >= 4 au tour precedent) ; bras route B. """

from __future__ import annotations

import itertools
import sys
import time
from pathlib import Path

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).parent))
from explo_hybride_IC import build, exact_Z, support


# ================= THEOREME A : verification numerique A1 =================

def verify_multiplicativity():
    print("=== Theoreme A : multiplicativite (verification numerique) ===")
    theta1 = [((0, 1), (1, 1), (2, 1)),
              ((0, 1), (1, 1), (3, 1)),
              ((0, 1), (1, 1), (4, 1))]
    theta2 = [tuple((v + 5, p) for (v, p) in cl) for cl in theta1]
    union = theta1 + theta2
    ctx1 = build(5, theta1)
    ctxU = build(10, union)
    E1, EU = ctx1[1], ctxU[1]
    rng = np.random.default_rng(3)
    ok = True
    for trial in range(3):
        G1 = [np.array(rng.normal(size=(2, 2))) for _ in range(E1)]
        G2 = [np.array(rng.normal(size=(2, 2))) for _ in range(E1)]
        for G in (G1, G2):
            for M in G:
                while abs(np.linalg.det(M)) < .3:
                    M[:] = rng.normal(size=(2, 2))
        S1, t1 = support(5, theta1, ctx1, G1, 0.0)
        S2, t2 = support(5, theta1, ctx1, G2, 0.0)
        SU, tU = support(10, union, ctxU, G1 + G2, 0.0)
        ok &= (SU == S1 * S2) and abs(tU - t1 * t2) < 1e-6 * abs(t1 * t2)
        print(f"  essai {trial}: S1={S1} S2={S2} S_union={SU} "
              f"(= produit ? {SU == S1*S2}) ; somme_union = {tU:.1f} "
              f"= {t1:.1f}*{t2:.1f}")
    print(f"  multiplicativite : {'VERIFIEE' if ok else 'ECHEC'}")
    print()


# ================= Lemmes B1, B2 : preuves symboliques =================

def lemma_B1():
    x0, x1, y0, y1, z0, z1, w0, w1 = sp.symbols('x0 x1 y0 y1 z0 z1 w0 w1')
    N = sp.Matrix([[2 * x0 * z0 - y0 * w0, 2 * x0 * z1 - y0 * w1],
                   [2 * x1 * z0 - y1 * w0, 2 * x1 * z1 - y1 * w1]])
    det_N = sp.expand(N.det())
    target = sp.expand(-2 * (x0 * y1 - x1 * y0) * (z0 * w1 - z1 * w0))
    ok = sp.simplify(det_N - target) == 0
    print(f"=== Lemme B1 : det(2xz^T - yw^T) = -2 det[x|y] det[z|w] : "
          f"{'PROUVE' if ok else 'ECHEC'} ===")
    return ok


def lemma_B2():
    p = {(e, s, a): sp.Symbol(f'p{e}{s}{a}') for e in (1, 2, 3)
         for s in (0, 1) for a in (0, 1)}
    K1 = (p[(1, 0, 1)] * p[(2, 0, 0)] * p[(3, 0, 0)]
          + p[(1, 1, 1)] * p[(2, 1, 0)] * p[(3, 1, 0)])   # A(100) = 0
    K2 = (p[(1, 0, 1)] * p[(2, 0, 1)] * p[(3, 0, 0)]
          + p[(1, 1, 1)] * p[(2, 1, 1)] * p[(3, 1, 0)])   # A(110) = 0
    combo = sp.expand(p[(2, 0, 1)] * K1 - p[(2, 0, 0)] * K2)
    detP2 = p[(2, 0, 0)] * p[(2, 1, 1)] - p[(2, 0, 1)] * p[(2, 1, 0)]
    target = sp.expand(-p[(1, 1, 1)] * p[(3, 1, 0)] * detP2)
    ok = sp.simplify(combo - target) == 0
    print(f"=== Lemme B2 : p201*K1 - p200*K2 = -p111*p310*det(P2) : "
          f"{'PROUVE' if ok else 'ECHEC'} ===")
    print("    (=> deux tues a distance 1 forcent une entree nulle ou "
          "det P = 0 : exclu en regime non-degenere)")
    return ok


# ============== Lemme B3 : ensembles tues realisables (reseau) ==============

CUBE = [np.array(v) for v in itertools.product((0, 1), repeat=3)]


def _invariant_factors(cols):
    """ Facteurs invariants (diagonale de Smith, valeurs absolues non
        nulles triees) du reseau engendre par les colonnes. """
    from sympy.matrices.normalforms import smith_normal_form
    from sympy import ZZ
    A = sp.Matrix([[int(g[j]) for g in cols] for j in range(3)])
    if A.rank() == 0:
        return (0, [])
    D = smith_normal_form(A, domain=ZZ)
    diag = [abs(D[i, i]) for i in range(min(D.shape)) if D[i, i] != 0]
    return (A.rank(), sorted(diag))


def in_lattice(v, gens):
    """ v dans le sous-groupe de Z^3 engendre par gens ?
        Critere : rang et facteurs invariants inchanges par adjonction
        de v (meme covolume => indice 1 => reseaux egaux). """
    if not any(int(x) != 0 for x in v):
        return True
    if not gens:
        return False
    rA, fA = _invariant_factors(gens)
    rB, fB = _invariant_factors(list(gens) + [v])
    return (rA == rB) and (fA == fB)


def achievable_kill_sets():
    """ S subseteq cube\\{0} realisable (regime non-degenere) ssi le
        reseau engendre par les differences de S evite e_i et a - a''
        (a in S, a'' hors S). Renvoie la liste des supports = cube\\S. """
    e = [np.array(v) for v in ((1, 0, 0), (0, 1, 0), (0, 0, 1))]
    ach = []
    nonzero_cube = [v for v in CUBE if v.any()]
    for r in range(len(nonzero_cube) + 1):
        for S in itertools.combinations(range(len(nonzero_cube)), r):
            Sv = [nonzero_cube[i] for i in S]
            gens = [Sv[j] - Sv[0] for j in range(1, len(Sv))]
            forb = list(e)
            others = [v for k, v in enumerate(nonzero_cube) if k not in S]
            others.append(np.zeros(3, dtype=int))
            for a in Sv:
                for a2 in others:
                    forb.append(a - a2)
            bad = any(in_lattice(f, gens) for f in forb)
            if not bad:
                supp = frozenset(tuple(v) for v in CUBE
                                 if not any((v == s).all() for s in Sv))
                ach.append((frozenset(tuple(s) for s in Sv), supp))
    return ach


# ============== Fermeture route-L non-degeneree (couverture) ==============

ZPATTERNS = [frozenset(), frozenset({(0, 1)}), frozenset({(1, 0)}),
             frozenset({(1, 1)}), frozenset({(0, 1), (1, 0)})]


def close_route_L(ach):
    """ Enumere (Z1,Z2,Z3) x (supp A, supp C) realisables ; verifie s'il
        existe une combinaison couvrant supp(A) x supp(C) \\ {(0,0)}. """
    supports = [supp for (_, supp) in ach]
    survivors = []
    checked = 0
    for Zs in itertools.product(ZPATTERNS, repeat=3):
        for SA in supports:
            for SB in supports:
                checked += 1
                okcover = True
                for a in SA:
                    for b in SB:
                        if a == (0, 0, 0) and b == (0, 0, 0):
                            continue
                        if not any((a[i], b[i]) in Zs[i] for i in range(3)):
                            okcover = False
                            break
                    if not okcover:
                        break
                if okcover:
                    survivors.append((Zs, SA, SB))
    return survivors, checked


def main():
    t0 = time.time()
    verify_multiplicativity()
    ok1 = lemma_B1()
    ok2 = lemma_B2()
    print()

    print("=== Lemme B3 : enumeration des ensembles tues realisables ===")
    ach = achievable_kill_sets()
    print(f"  familles (S_tue, support) realisables en regime "
          f"non-degenere : {len(ach)}")
    for S, supp in sorted(ach, key=lambda t: len(t[0]))[:12]:
        print(f"    tue = {sorted(S) if S else '{}'}  -> |supp| = {len(supp)}")
    if len(ach) > 12:
        print(f"    ... ({len(ach) - 12} autres)")
    print()

    print("=== Fermeture route-L non-degeneree : couverture de Kronecker ===")
    survivors, checked = close_route_L(ach)
    print(f"  combinaisons verifiees : {checked}")
    if not survivors:
        print("  AUCUNE combinaison (Z, supp A, supp C) ne couvre : le cas")
        print("  route-L non-degenere est FERME -- support 1 impossible.")
    else:
        print(f"  survivants combinatoires : {len(survivors)} -> etape")
        print("  algebrique requise (Groebner joint). Liste :")
        for (Zs, SA, SB) in survivors[:10]:
            print(f"    Z = {[sorted(z) for z in Zs]}")
            print(f"      supp A = {sorted(SA)}")
            print(f"      supp C = {sorted(SB)}")
    print(f"\n[{time.time()-t0:.0f}s]")


if __name__ == "__main__":
    main()
