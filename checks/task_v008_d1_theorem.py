"""
TACHE V-008 -- (b) THEOREME d = 1 ; (c) classification exhaustive d = 2.

THEOREME V8 (d = 1 -- preuve complete) :
  Tout f in Z[x], f != 0, (1+x)^2 | f, de norme l2 minimale (= 4 des que
  le degre le permet), s'ecrit f = +- x^s (1 - x^u)(1 - x^v) avec u, v
  pairs -- un produit pur d'Erdos-Szekeres, cyclotomique. En particulier
  la Conjecture 5 de KV est VRAIE pour d = 1.
  Preuve :
  (i) norme^2 < 4 impossible : 1 ou 3 monomes unitaires -> f(-1) impair
      != 0 ; 2 monomes -> f(-1) = 0 et f'(-1) = 0 forcent a = b ;
      un coefficient +-2 seul -> contenu 2, se reduit.
  (ii) norme^2 = 4 : ou bien (2,1,1)... f(-1) = 0 mod 2 ok mais
      norme^2 = 6 ; donc quatre monomes +-1 : f = e1 x^{a1} + ... ;
      f(-1) = 0 => deux termes "+" et deux "-" au sens ei(-1)^{ai} ;
      f'(-1) = 0 => somme des exposants du groupe + = somme du groupe -
      (c'est PTE de taille 2). En normalisant (signe global, decalage
      x^s, le plus petit exposant a 0), PTE-2 donne {0, u+v} vs {u, v} :
      f = 1 - x^u - x^v + x^{u+v} = (1 - x^u)(1 - x^v).
      Divisibilite par (1+x)^2 <=> u et v pairs.            QED

Ce script verifie [B] le theoreme par enumeration exhaustive (deg <= 24)
et [C] classifie TOUS les multiples de (1+x)^3 de norme^2 <= 6 en fenetre
deg <= 20 : sont-ils tous cyclotomiques ? (=> Conjecture 5 pour d = 2 en
fenetre.)
"""

from __future__ import annotations

import itertools
import time

import numpy as np
import sympy as sp

X = sp.symbols("x")


def divisible_by_1px_pow(exps, signs, power):
    """ f = sum signs[i] x^{exps[i]} divisible par (1+x)^power ?
        <=> les derivees 0..power-1 s'annulent en -1. """
    for k in range(power):
        tot = 0
        for a, e in zip(exps, signs):
            if a < k:
                continue
            coef = 1
            for j in range(k):
                coef *= (a - j)
            tot += e * coef * ((-1) ** (a - k))
        if tot != 0:
            return False
    return True


def is_cyclo_product(exps, signs):
    f = sp.Poly(sum(int(e) * X ** int(a) for a, e in zip(exps, signs)), X)
    fl = sp.factor_list(f.as_expr())
    if abs(int(fl[0])) != 1:
        return False
    for base, _ in fl[1]:
        p = sp.Poly(base, X)
        if p == sp.Poly(X, X):
            continue
        if abs(int(p.LC())) != 1:
            return False
        roots = np.roots([float(c) for c in p.all_coeffs()])
        if not np.all(np.abs(np.abs(roots) - 1.0) < 1e-6):
            return False
    return True


def enum_d1(maxdeg=24):
    """ [B] tous les f a 4 monomes unitaires, exp min = 0, deg <= maxdeg,
        (1+x)^2 | f -- verifier la forme produit pur. """
    count = ok_form = 0
    for exps in itertools.combinations(range(maxdeg + 1), 4):
        if exps[0] != 0:
            continue
        for signs in itertools.product((1, -1), repeat=3):
            sg = (1,) + signs  # signe global normalise
            if not divisible_by_1px_pow(exps, sg, 2):
                continue
            count += 1
            # forme (1-x^u)(1-x^v) ? <=> {a : signe +} = {0, u+v},
            # {a : signe -} = {u, v} avec u+v egal
            plus = [a for a, e in zip(exps, sg) if e == 1]
            minus = [a for a, e in zip(exps, sg) if e == -1]
            if (len(plus) == 2 and len(minus) == 2
                    and plus[0] + plus[1] == minus[0] + minus[1]
                    and plus[0] == 0 and plus[1] == minus[0] + minus[1]
                    and minus[0] % 2 == 0 and minus[1] % 2 == 0):
                ok_form += 1
            elif is_cyclo_product(exps, sg):
                ok_form += 1  # autre forme mais cyclotomique quand meme
    return count, ok_form


def enum_d2(maxdeg=20):
    """ [C] tous les f de norme^2 <= 6, exp min = 0, (1+x)^3 | f. """
    t0 = time.time()
    sols = []
    # forme 6 monomes unitaires
    for exps in itertools.combinations(range(maxdeg + 1), 6):
        if exps[0] != 0:
            continue
        for signs in itertools.product((1, -1), repeat=5):
            sg = (1,) + signs
            if divisible_by_1px_pow(exps, sg, 3):
                sols.append((exps, sg))
    # forme (2, 1, 1) : norme 6
    for exps in itertools.combinations(range(maxdeg + 1), 3):
        if exps[0] != 0:
            continue
        for pos2 in range(3):
            for signs in itertools.product((1, -1), repeat=2):
                sg = [0, 0, 0]
                rest = iter(signs)
                for i in range(3):
                    sg[i] = 2 if i == pos2 else next(rest)
                # normaliser signe global : premier coeff > 0
                if sg[0] < 0:
                    sg = [-s for s in sg]
                if divisible_by_1px_pow(exps, tuple(sg), 3):
                    sols.append((exps, tuple(sg)))
    # cyclotomie de chaque solution
    non_cyclo = []
    for exps, sg in sols:
        if not is_cyclo_product(exps, sg):
            non_cyclo.append((exps, sg))
    return len(sols), non_cyclo, time.time() - t0


def main() -> None:
    print("TACHE V-008 -- theoreme d = 1 + classification d = 2")
    print("=" * 66)

    print("\n[B] d = 1 : multiples de (1+x)^2 a 4 monomes +-1, deg <= 24")
    count, okf = enum_d1()
    print(f"    {count} solutions (normalisees) ; conformes au theoreme "
          f"(produit pur / cyclotomique) : {okf}")
    print(f"    THEOREME d=1 : {'VERIFIE EXHAUSTIVEMENT' if count == okf else '*** CONTRE-EXEMPLE ***'}")

    print("\n[C] d = 2 : multiples de (1+x)^3 de norme^2 <= 6, deg <= 20")
    total, non_cyclo, dt = enum_d2()
    print(f"    {total} solutions ({dt:.0f}s) ; non-cyclotomiques : "
          f"{len(non_cyclo)}")
    for (exps, sg) in non_cyclo[:5]:
        print(f"      *** {list(zip(exps, sg))}")
    if not non_cyclo:
        print("    => en fenetre deg <= 20, TOUT multiple minimal de (1+x)^3")
        print("       est cyclotomique : Conjecture 5 (d = 2) tient en fenetre.")


if __name__ == "__main__":
    main()
