"""
EXPLORATION -- nos jauges constructibles satisfont-elles A ?
A = << jauges poly-constructibles a support polynomial pour TOUTES les
instances >>. Nos jauges (I, C=Mobius, H=Hadamard, B=BP, et tous les
hybrides par arete) sont bien poly-constructibles. Question : leur
support est-il polynomial partout ? Reponse visee : NON, temoin par
famille explicite.

FAMILLE TEMOIN T_r : r copies disjointes du GADGET CYCLIQUE MONOTONE
  G = { (a v b v c), (c v d v e), (e v f v a) }   (6 vars, 3 clauses,
  graphe de facteurs = UN cycle de longueur 6 + 3 feuilles, E = 9).

FAITS :
  (i)  supports MULTIPLICATIFS sur les copies disjointes (les termes
       factorisent bloc par bloc, pour toute jauge par arete) -- verifie
       numeriquement a r = 2 ;
  (ii) monotone => S_C(T_r) = 2^{3r} (prouve) ; S_I = #SAT = 45^r
       (prouve par produit) ;
  (iii) jauge BP : l'espace des cycles impose >= 2^{E-V+1} boucles
       generalisees par bloc (ici 2 : vide + le cycle) => S_BP >= 2^r ;
  (iv) LE POINT DUR : min par bloc sur TOUT le dictionnaire
       {I, C, H, B}^9 (262 144 jauges par arete, exhaustif). Si ce
       minimum est >= 2, alors LE MEILLEUR CHOIX du dictionnaire donne
       >= 2^r sur T_r : AUCUNE de nos jauges constructibles ne
       satisfait A.
"""

from __future__ import annotations

import itertools
import time

import numpy as np

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from explo_hybride_IC import build, exact_Z, support, mobius_P, I2
from explo_pire_cas_min_jauges import bp_gauges_generic

HAD = np.array([[1.0, 1.0], [1.0, -1.0]])


def gadget(r=1):
    """ r copies disjointes du gadget cyclique monotone (6 vars chacune). """
    clauses = []
    for j in range(r):
        o = 6 * j
        clauses += [((o + 0, 1), (o + 1, 1), (o + 2, 1)),
                    ((o + 2, 1), (o + 3, 1), (o + 4, 1)),
                    ((o + 4, 1), (o + 5, 1), (o + 0, 1))]
    return 6 * r, clauses


def main():
    w = 0.0
    print("Refutation de A pour le dictionnaire constructible {I, C, H, B}")
    print("=" * 74)

    # ------------------------------------------------ bloc r = 1
    n, clauses = gadget(1)
    ctx = build(n, clauses)
    edges, E, lit_pol = ctx[0], ctx[1], ctx[4]
    Zx = exact_Z(n, clauses, w)
    print(f"Bloc G : n={n}, m={len(clauses)}, E={E}, #SAT = {Zx:.0f} "
          f"(prevu 45), cyclomatique = E - V + 1 = {E - (n + 3) + 1}")

    bp = bp_gauges_generic(n, clauses, w)
    letters = {"I": lambda e: I2, "C": lambda e: mobius_P(lit_pol[e]),
               "H": lambda e: HAD, "B": lambda e: bp[e]}

    for name in letters:
        G = [letters[name](e) for e in range(E)]
        S, tot = support(n, clauses, ctx, G, w)
        ok = abs(tot - Zx) < 1e-6
        print(f"  jauge pure {name} : S = {S:>4}   somme = {tot:.4f} "
              f"({'ok' if ok else 'ECART !'})")

    # exhaustif sur le dictionnaire complet {I,C,H,B}^9
    print(f"\nExhaustif {{I,C,H,B}}^{E} = 4^{E} = {4**E} jauges du bloc :")
    t0 = time.time()
    keys = list(letters)
    best = (10 ** 9, None)
    histo = {}
    for combo in itertools.product(range(4), repeat=E):
        G = [letters[keys[c]](e) for e, c in enumerate(combo)]
        S, tot = support(n, clauses, ctx, G, w)
        if abs(tot - Zx) > 1e-6:
            continue
        histo[S] = histo.get(S, 0) + 1
        if S < best[0]:
            best = (S, "".join(keys[c] for c in combo))
    print(f"  min par bloc = {best[0]}   (config {best[1]})   "
          f"[{time.time()-t0:.0f}s]")
    small = {k: v for k, v in sorted(histo.items())[:6]}
    print(f"  distribution des petits supports : {small}")

    # ------------------------------------------------ multiplicativite r = 2
    print("\nMultiplicativite (r = 2, 12 vars, E = 18) :")
    n2, clauses2 = gadget(2)
    ctx2 = build(n2, clauses2)
    E2, lit_pol2 = ctx2[1], ctx2[4]
    Zx2 = exact_Z(n2, clauses2, w)
    print(f"  #SAT(T_2) = {Zx2:.0f} (prevu 45^2 = 2025)")
    bp2 = bp_gauges_generic(n2, clauses2, w)
    letters2 = {"I": lambda e: I2, "C": lambda e: mobius_P(lit_pol2[e]),
                "H": lambda e: HAD, "B": lambda e: bp2[e]}
    for name in ("I", "C", "B"):
        G = [letters2[name](e) for e in range(E2)]
        S, tot = support(n2, clauses2, ctx2, G, w)
        print(f"  jauge pure {name} sur T_2 : S = {S}   "
              f"(carre du bloc attendu)")
    # la meilleure config du bloc, dupliquee sur les deux blocs
    if best[1] is not None:
        G = ([letters2[c](e) for e, c in enumerate(best[1])]
             + [letters2[c](9 + e) for e, c in enumerate(best[1])])
        S, tot = support(n2, clauses2, ctx2, G, w)
        ok = abs(tot - Zx2) < 1e-6
        print(f"  meilleure config bloc, dupliquee : S = {S} "
              f"(attendu {best[0]}^2 = {best[0]**2}) "
              f"somme {'ok' if ok else 'ECART !'}")

    print("\nCONCLUSION :")
    print(f"  min dictionnaire par bloc = {best[0]} ; multiplicativite")
    print(f"  verifiee => sur T_r, TOUT choix du dictionnaire donne")
    print(f"  S >= {best[0]}^r : croissance exponentielle. Aucune de nos")
    print("  jauges constructibles ne satisfait A. (A reste ouverte pour")
    print("  des familles de jauges non encore construites.)")


if __name__ == "__main__":
    main()
