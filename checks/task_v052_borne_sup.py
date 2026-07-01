"""
TACHE V-052 (corrigée V-055) -- bornes supérieures explicites sur λ₁(L_{d,n}).

ERRATUM (25e auto-correction, relecture adverse Fable 5, 2026-06-27) :
la version initiale de ce script ne comparait que les modèles e^{c√d} et
d^k pour la norme² de l'Euler tronqué — JAMAIS l'exponentiel pur, qui
GAGNE largement (R² 0,9994). Conclusion corrigée : ∏(1-x^q) est
EXPONENTIEL e^{≈0,39d} (pentes locales croissantes → ≈0,389 ≈ 2·K_Sudler),
PAS sous-exponentiel. Et la borne A₂(n) < (√n)^{√n/2} est de MALTBY
(construction groupes de Weyl), citée dans Cipu 2004 — pas de Cipu.

Reproduit tasks/done/V-052.md (version corrigée) :
 1. sous-famille close (1-x)^{d+1}(1+x)^j : min_j P_j(d+1) ~ exponentiel ;
 2. Euler tronqué ∏_{q=1}^{d+1}(1-x^q) : multiplicité d+1 (VÉRIFIÉE par
    divisions), span ~d²/2, norme² EXPONENTIELLE (3 modèles + pentes) ;
 3. lien Maltby/Cipu : produit de d+1 binômes ∈ L_{d,·}, A₂(d+1) borne λ₁²
    (sous-exp, mais à span super-polynomial).
"""

from __future__ import annotations

from math import factorial as fac

import numpy as np


def Pj(D, j):
    return fac(2 * D) * fac(2 * j) // (fac(D) * fac(j) * fac(D + j))


def euler_tronque(Q):
    """∏_{q=1}^{Q}(1-x^q) : retourne (mult_verifiee, degre, hauteur, norme²)."""
    f = [1]
    for q in range(1, Q + 1):
        g = [0] * (len(f) + q)
        for i, c in enumerate(f):
            g[i] += c
            g[i + q] -= c
        f = g
    h = max(abs(c) for c in f)
    n2 = sum(c * c for c in f)
    # multiplicité en x=1 VÉRIFIÉE : divisions successives par (1-x).
    # p = (1-x)·q  <=>  q_i = somme partielle a_0+..+a_i ; reste = p(1).
    mult, p = 0, list(f)
    while sum(p) == 0 and any(p):
        acc, q_ = 0, []
        for c in p[:-1]:
            acc += c
            q_.append(acc)
        p = q_
        mult += 1
    return mult, len(f) - 1, h, n2


def main():
    print("1. sous-famille close (1-x)^{d+1}(1+x)^j : min_j P_j(d+1)")
    for d in (10, 16, 22):
        m = min(Pj(d + 1, j) for j in range(3 * (d + 1)))
        print(f"   d={d} : min_j P_j = {m} (vs 4^d ~ {Pj(d+1,0)}) -- exponentiel")

    print("2. Euler tronqué ∏(1-x^q), q=1..d+1 -- TROIS modèles :")
    ds = list(range(8, 65, 4))
    ns = []
    for d in ds:
        mult, deg, h, n2 = euler_tronque(d + 1)
        assert mult == d + 1, f"multiplicité {mult} != {d+1}"
        ns.append(n2)
    ln = np.log([float(x) for x in ns])
    print(f"   span(d) = (d+1)(d+2)/2 ~ d²/2 (POLYNOMIAL)")
    for name, xs in [("EXP e^{cd}", np.array(ds, float)),
                     ("SOUS-EXP e^{c√d}", np.sqrt(ds)),
                     ("POLY d^k", np.log(ds))]:
        a = np.polyfit(xs, ln, 1)
        res = ln - np.polyval(a, xs)
        print(f"   {name:>18} : pente={a[0]:.3f}  R²={1 - res.var() / ln.var():.5f}")
    pentes = [(ln[i] - ln[i - 1]) / (ds[i] - ds[i - 1]) for i in range(1, len(ds))]
    print(f"   pentes locales {pentes[0]:.3f} -> {pentes[-1]:.3f} : CROISSANTES"
          f" => EXPONENTIEL (2·K_Sudler ≈ 0,397)")

    print("3. lien Maltby (cité Cipu 2004) : produit de d+1 binômes ∈ L_{d,·}")
    print("   Maltby prouve A₂(n) < (√n)^{√n/2} = exp(O(√n log n))")
    print("   => λ₁(L_{d,·})² ≤ A₂(d+1) : sous-exp PROUVÉ, mais à span")
    print("      SUPER-polynomial. À span polynomial : rien de mieux que")
    print("      l'exponentiel (constante 0,39 vs 1,39 trivial) n'est prouvé.")


if __name__ == "__main__":
    main()
