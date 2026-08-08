"""
EXPLORATION -- jauge a support 1 sur le bloc cyclique, par TRIANGULARISATION
DE LA MONODROMIE. Renverse la presomption de la refutation-dictionnaire :
le bloc cyclique G ADMET une jauge constructible a support 1.

CONSTRUCTION (verifiee ici par enumeration exacte des 512 termes) :
  1. Feuilles (vars 1, 3, 5) : jauge Hadamard -> le tenseur feuille ne
     survit que sur k = 0 (somme des lignes = (2, 0)) ; la clause voit le
     dual (1/2)(1,1) : tenseur effectif F(su, sv) = 1 - (1/2)[su=sv=0],
     soit F = [[1/2, 1], [1, 1]].
  2. Cycle (6 aretes alternant variables 0,2,4 et clauses c1,c2,c3) :
     choisir les jauges pour transformer 5 des 6 matrices locales en
     l'IDENTITE et concentrer la monodromie M = F^3 sur le dernier lien,
     exprimee en BASE COMPAGNON B = [g0, M g0] :
         B^{-1} M B = [[0, -det M], [1, tr M]]  --  zero en [0,0].
     Les identites forcent k constant sur le cycle ; le zero du compagnon
     tue k = 0 ; seul survit k = 1, de valeur tr(M) != 0.
  3. Support total = 1 (feuilles x cycle), terme unique = 2^3 tr(F^3) = 45.

PROPRIETE REVELEE : construire cette jauge REVIENT a calculer Z
(le terme unique EST tr M = Z / 8). La jauge n'est pas un raccourci qui
evite le calcul : sa construction EST le calcul.
"""

from __future__ import annotations

import numpy as np

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from explo_hybride_IC import build, exact_Z, support
from explo_refutation_A_dictionnaire import gadget

HAD = np.array([[1.0, 1.0], [1.0, -1.0]])
F = np.array([[0.5, 1.0], [1.0, 1.0]])          # clause effective (feuille absorbee)


def inv_T(P):
    return np.linalg.inv(P).T


def cycle_gauges_for_block():
    """ Renvoie le dict {edge_local: P} pour un bloc (9 aretes locales).
        Ordre local des aretes (cf. build sur gadget(1)) :
          0:(v0,c1) 1:(v1,c1) 2:(v2,c1) 3:(v2,c2) 4:(v3,c2) 5:(v4,c2)
          6:(v4,c3) 7:(v5,c3) 8:(v0,c3)
        Cycle : e1=0, e2=2, e3=3, e4=5, e5=6, e6=8 ; feuilles : 1, 4, 7. """
    M = F @ F @ F                                 # monodromie
    g0 = np.array([1.0, 0.0])
    B = np.column_stack([g0, M @ g0])             # base compagnon

    P = {}
    P[0] = B                                      # e1
    P[2] = F.T @ inv_T(P[0])                      # c1 -> I
    P[3] = inv_T(P[2])                            # var2 -> I
    P[5] = F.T @ inv_T(P[3])                      # c2 -> I
    P[6] = inv_T(P[5])                            # var4 -> I
    P[8] = inv_T(P[0])                            # var0 -> I
    for leaf in (1, 4, 7):
        P[leaf] = HAD
    return P, M


def main():
    w = 0.0
    print("Jauge a support 1 sur le bloc cyclique (monodromie compagnon)")
    print("=" * 72)

    # ---------------------------------------------------------- bloc r=1
    n, clauses = gadget(1)
    ctx = build(n, clauses)
    E = ctx[1]
    Zx = exact_Z(n, clauses, w)
    Pmap, M = cycle_gauges_for_block()
    print(f"monodromie M = F^3 : tr = {np.trace(M):.4f} (Z/8 = {Zx/8:.4f}), "
          f"det = {np.linalg.det(M):.4f}")
    comp = np.linalg.inv(np.column_stack([np.array([1.0, 0]), M @ np.array([1.0, 0])])) \
        @ M @ np.column_stack([np.array([1.0, 0]), M @ np.array([1.0, 0])])
    print(f"forme compagnon B^-1 M B =\n{np.round(comp, 6)}")

    gauges = [Pmap[e] for e in range(E)]
    S, tot = support(n, clauses, ctx, gauges, w)
    print(f"\nBloc G : S = {S}   somme = {tot:.6f}   (Z = {Zx:.0f})"
          f"   {'*** SUPPORT 1 ***' if S == 1 else ''}")

    # ---------------------------------------------------------- T_2 (r=2)
    n2, clauses2 = gadget(2)
    ctx2 = build(n2, clauses2)
    E2 = ctx2[1]
    Zx2 = exact_Z(n2, clauses2, w)
    gauges2 = [Pmap[e % 9] for e in range(E2)]    # meme jauge par bloc
    S2, tot2 = support(n2, clauses2, ctx2, gauges2, w)
    print(f"T_2     : S = {S2}   somme = {tot2:.6f}   (Z = {Zx2:.0f})"
          f"   {'*** SUPPORT 1 ***' if S2 == 1 else ''}")

    print("\nLECTURE : la refutation-dictionnaire ne fermait que le")
    print("dictionnaire ; la jauge monodromie-compagnon est poly-")
    print("constructible et donne S=1 sur T_r -- mais sa construction")
    print("calcule tr(M) = Z/8 : la jauge EST le calcul.")


if __name__ == "__main__":
    main()
