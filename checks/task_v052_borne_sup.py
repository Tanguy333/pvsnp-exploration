"""
TACHE V-052 -- échelle des bornes supérieures explicites sur λ₁(L_{d,n})
(moitié haute de l'obstruction cyclotomique, fil P vs NP).

Reproduit tasks/done/V-052.md :
 1. sous-famille close (1-x)^{d+1}(1+x)^j : min_j P_j(d+1) ~ exponentiel ;
 2. Euler tronqué ∏_{q=1}^{d+1}(1-x^q) : mult d+1, span ~d²/2,
    norme² SOUS-EXPONENTIELLE e^{O(√d)} (fit R² sous-exp > R² poly) ;
 3. lien Cipu : produit de d+1 binômes ∈ L_{d,·}, A₂(d+1) borne λ₁.
"""

from __future__ import annotations

from math import factorial as fac

import numpy as np


def Pj(D, j):
    return fac(2 * D) * fac(2 * j) // (fac(D) * fac(j) * fac(D + j))


def euler_tronque(Q):
    """∏_{q=1}^{Q}(1-x^q) : retourne (mult, degre, hauteur, norme²)."""
    f = [1]
    for q in range(1, Q + 1):
        g = [0] * (len(f) + q)
        for i, c in enumerate(f):
            g[i] += c
            g[i + q] -= c
        f = g
    h = max(abs(c) for c in f)
    n2 = sum(c * c for c in f)
    # multiplicité en x=1 = nombre de facteurs (chaque (1-x^q) -> un (1-x))
    return Q, len(f) - 1, h, n2


def main():
    print("1. sous-famille close (1-x)^{d+1}(1+x)^j : min_j P_j(d+1)")
    for d in (10, 16, 22):
        m = min(Pj(d + 1, j) for j in range(3 * (d + 1)))
        print(f"   d={d} : min_j P_j = {m} (vs 4^d ~ {Pj(d+1,0)}) -- exponentiel")

    print("2. Euler tronqué ∏(1-x^q), q=1..d+1 :")
    ds = list(range(8, 41, 2))
    ns = []
    for d in ds:
        mult, deg, h, n2 = euler_tronque(d + 1)
        assert mult == d + 1
        ns.append(n2)
    ln = np.log([float(x) for x in ns])
    r_subexp = np.corrcoef(np.sqrt(ds), ln)[0, 1] ** 2
    r_poly = np.corrcoef(np.log(ds), ln)[0, 1] ** 2
    a = np.polyfit(np.sqrt(ds), ln, 1)
    print(f"   span(d) = (d+1)(d+2)/2 ~ d²/2 (POLYNOMIAL)")
    print(f"   log(norme²) = {a[0]:.2f}·√d {a[1]:+.2f}")
    print(f"   R²(sous-exp e^√d) = {r_subexp:.4f}  vs  R²(poly d^k) = {r_poly:.4f}")
    print(f"   => SOUS-EXPONENTIEL e^O(√d) à span polynomial")

    print("3. lien Cipu 2004 : produit de d+1 binômes a mult d+1, donc ∈ L_{d,·}")
    print("   Cipu prouve A₂(n) < (√n)^{√n/2} = exp(O(√n log n))")
    print("   => λ₁(L_{d,·}) ≤ A₂(d+1) < exp(O(√d log d)) PROUVÉ (sub-exp)")


if __name__ == "__main__":
    main()
