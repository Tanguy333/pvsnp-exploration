"""
TACHE V-041 (suite) -- DERIVATION INDEPENDANTE du polynome F14 de
CMSV 2023 (sec. 4.2) par algebre lineaire exacte, pour valider notre
transcription OCR et la methode avant de construire la machine v2.

Construction (CMSV) : pour n = 14, apres selection de s = 5 elements
de A et t = 4 de B, les 5 restants (2 cotes a, 3 cotes b) doivent
satisfaire (23). On substitue x_k -> E_k := p_k({alpha}) - p_k({beta})
(alpha = 2 carres restants cote a, beta = 3 cotes b, p_k = sommes de
puissances) dans les monomes de poids 24 (poids de x_k = 2k), et on
cherche la combinaison lineaire identiquement nulle. F14 est l'unique
relation (a un scalaire pres) ; F14(m'_2,...,m'_12) = 0 est alors la
condition necessaire de completabilite.

Methode : expansion exacte des monomes en polynomes de Z[a1,a2,b1,b2,b3]
(dictionnaires d'exposants), noyau gauche exact par sous-matrices
aleatoires (sympy, rationnels) puis verification contre la matrice
complete. Comparaison terme a terme avec l'OCR du papier.
"""

from __future__ import annotations

import itertools
import random
import time

from fractions import Fraction

NVAR = 5            # a1, a2, b1, b2, b3 (les carres restants)
KMAX = 6            # x_1..x_6, poids 2k, somme des poids = 24


def powersum_diff(k):
    """E_k = a1^k + a2^k - b1^k - b2^k - b3^k comme dict exposants->coef."""
    d = {}
    for i, s in [(0, 1), (1, 1), (2, -1), (3, -1), (4, -1)]:
        e = [0] * NVAR
        e[i] = k
        d[tuple(e)] = d.get(tuple(e), 0) + s
    return d


def mul(d1, d2):
    out = {}
    for e1, c1 in d1.items():
        for e2, c2 in d2.items():
            e = tuple(x + y for x, y in zip(e1, e2))
            out[e] = out.get(e, 0) + c1 * c2
    return {e: c for e, c in out.items() if c}


def monomial_poly(exps):
    """Expansion exacte de prod_k E_k^{d_k}."""
    out = {tuple([0] * NVAR): 1}
    for k, dk in enumerate(exps, start=1):
        Ek = powersum_diff(k)
        for _ in range(dk):
            out = mul(out, Ek)
    return out


def main():
    t0 = time.time()
    # monomes x1^d1..x6^d6 avec sum k*dk = 12 (poids 24)
    monos = []
    for d6 in range(3):
        for d5 in range(3):
            for d4 in range(4):
                for d3 in range(5):
                    for d2 in range(7):
                        r = 12 - 6 * d6 - 5 * d5 - 4 * d4 - 3 * d3 - 2 * d2
                        if r >= 0:
                            monos.append((r, d2, d3, d4, d5, d6))
    print(f"{len(monos)} monomes de poids 24", flush=True)

    # expansion exacte de chaque monome
    polys = [monomial_poly(m) for m in monos]
    cols = sorted(set().union(*[set(p) for p in polys]))
    colidx = {e: i for i, e in enumerate(cols)}
    print(f"{len(cols)} coefficients distincts ; expansion en "
          f"{time.time()-t0:.0f}s", flush=True)

    # noyau gauche exact : sous-ensembles aleatoires de colonnes via sympy
    import sympy as sp
    rng = random.Random(7)
    nm = len(monos)
    sub = rng.sample(range(len(cols)), min(3 * nm, len(cols)))
    Msub = sp.Matrix([[polys[i].get(cols[j], 0) for j in sub]
                      for i in range(nm)])
    ker = Msub.T.nullspace()
    print(f"noyau du sous-systeme : dimension {len(ker)} "
          f"({time.time()-t0:.0f}s)", flush=True)

    # verification exacte de chaque candidat contre TOUTES les colonnes
    valides = []
    for v in ker:
        # normaliser en entiers
        dens = [sp.fraction(sp.nsimplify(x))[1] for x in v]
        l = sp.ilcm(*[int(d) for d in dens]) if dens else 1
        vi = [int(x * l) for x in v]
        g = 0
        for x in vi:
            g = sp.igcd(g, x)
        if g:
            vi = [x // g for x in vi]
        ok = True
        for e in cols:
            s = sum(vi[i] * polys[i].get(e, 0) for i in range(nm))
            if s != 0:
                ok = False
                break
        if ok:
            valides.append(vi)
    print(f"relations exactes confirmees : {len(valides)}", flush=True)

    for vi in valides:
        print("F14 derive (termes non nuls) :")
        for c, m in sorted(zip(vi, monos), key=lambda t: -abs(t[0])):
            if c:
                term = " ".join(f"x{k+1}^{d}" if d > 1 else f"x{k+1}"
                                for k, d in enumerate(m) if d)
                print(f"  {c:+d} {term}")
    print(f"Total {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
