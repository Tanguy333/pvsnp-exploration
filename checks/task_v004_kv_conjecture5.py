"""
TACHE V-004 -- Test direct de la Conjecture 5 de Krishan-Vishwanathan
(ECCC TR24-074).

LE RESEAU : B est la matrice (n+1) x (n-d) avec
    B[i, k] = (-1)^{i-k} C(d+1, i-k)   (0 si i-k hors [0, d+1]),
colonnes = gabarits de differences finies Delta^{d+1} decales (base,
triangulaire inferieure, de null(M) = les vecteurs entiers orthogonaux
aux polynomes de degre <= d sur {0..n}). C'est l'objet de notre Lemme 2
(F-011), version reseau entier.

CONJECTURE 5 (KV) : « There exists a vector gamma in L(B) with the
smallest l2 norm such that gamma_n = 1. »
(gamma et -gamma etant toutes deux dans L(B), on teste |gamma_n| = 1.)

METHODE : LLL (maison, delta = 0.99) puis enumeration de Fincke-Pohst
EXACTE (rayon = plus court vecteur de la base reduite ; toutes les
solutions au minimum collectees ; normes verifiees en entiers).

Grille : n = 6..16, d = 1..min(8, n-3). On compare aussi au gabarit pur
(colonne seule, norme^2 = C(2d+2, d+1)) pour savoir si le plus court
vecteur est le gabarit lui-meme.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb

import numpy as np


def build_basis(n, d):
    """ Lignes = vecteurs de base (m x (n+1)), entiers. """
    m = n - d
    G = np.zeros((m, n + 1), dtype=object)
    for k in range(m):
        for j in range(d + 2):
            G[k, k + j] = (-1) ** j * comb(d + 1, j)
    return G


def lll_reduce(G, delta=0.99):
    """ LLL standard sur les lignes de G (entiers, GS en float). """
    B = [np.array(r, dtype=float) for r in G]
    Z = [np.array(r, dtype=object) for r in G]
    m = len(B)

    def gso():
        Bs, mu = [], [[0.0] * m for _ in range(m)]
        for i in range(m):
            v = B[i].copy()
            for j in range(i):
                mu[i][j] = float(B[i] @ Bs[j]) / float(Bs[j] @ Bs[j])
                v = v - mu[i][j] * Bs[j]
            Bs.append(v)
        return Bs, mu

    Bs, mu = gso()
    i = 1
    while i < m:
        for j in range(i - 1, -1, -1):
            q = round(mu[i][j])
            if q != 0:
                Z[i] = Z[i] - q * Z[j]
                B[i] = B[i] - q * np.array(Z[j], dtype=float) * 0 - q * B[j]
                Bs, mu = gso()
        if float(Bs[i] @ Bs[i]) >= (delta - mu[i][i - 1] ** 2) * float(
                Bs[i - 1] @ Bs[i - 1]):
            i += 1
        else:
            Z[i], Z[i - 1] = Z[i - 1], Z[i]
            B[i], B[i - 1] = B[i - 1], B[i]
            Bs, mu = gso()
            i = max(i - 1, 1)
    return [np.array(z, dtype=object) for z in Z]


def norm2_exact(v):
    return sum(int(x) * int(x) for x in v)


def shortest_vectors(G):
    """ Fincke-Pohst exact : toutes les solutions a la norme minimale. """
    m = len(G)
    Bf = np.array([[float(x) for x in r] for r in G])
    # GS
    Bs = []
    mu = np.zeros((m, m))
    for i in range(m):
        v = Bf[i].copy()
        for j in range(i):
            mu[i, j] = (Bf[i] @ Bs[j]) / (Bs[j] @ Bs[j])
            v -= mu[i, j] * Bs[j]
        Bs.append(v)
    c = np.array([b @ b for b in Bs])
    R2 = min(norm2_exact(r) for r in G) + 1e-6
    best = [None]
    sols = []

    def rec(level, x, center_off):
        nonlocal R2
        if level < 0:
            if any(x):
                v = sum(int(x[i]) * G[i] for i in range(m))
                n2 = norm2_exact(v)
                if best[0] is None or n2 < best[0]:
                    best[0] = n2
                    sols.clear()
                    sols.append(v)
                elif n2 == best[0]:
                    sols.append(v)
            return
        # intervalle pour x_level
        rem = R2 - center_off
        if rem < 0:
            return
        center = -sum(mu[k, level] * x[k] for k in range(level + 1, m))
        half = (rem / c[level]) ** 0.5
        lo = int(np.ceil(center - half - 1e-9))
        hi = int(np.floor(center + half + 1e-9))
        for xv in range(lo, hi + 1):
            add = c[level] * (xv - center) ** 2
            x[level] = xv
            rec(level - 1, x, center_off + add)
        x[level] = 0

    rec(m - 1, [0] * m, 0.0)
    return best[0], sols


def main() -> None:
    print("TACHE V-004 -- test direct de la Conjecture 5 de KV (TR24-074)")
    print("=" * 72)
    print(f"{'n':>3} {'d':>2} {'m':>2} | {'norme^2 min':>11} "
          f"{'gabarit C(2d+2,d+1)':>19} | {'|gamma_n| des minima':>20} | verdict")
    print("-" * 72)
    all_ok = True
    for n in range(6, 17):
        for d in range(1, min(8, n - 3) + 1):
            G = build_basis(n, d)
            G = lll_reduce(G)
            n2, sols = shortest_vectors(G)
            lasts = sorted({abs(int(v[n])) for v in sols})
            stencil = comb(2 * d + 2, d + 1)
            ok = 1 in lasts
            all_ok &= ok
            print(f"{n:>3} {d:>2} {n - d:>2} | {n2:>11} {stencil:>19} | "
                  f"{str(lasts):>20} | "
                  f"{'OK (gamma_n = 1 existe)' if ok else '*** CONTRE-EXEMPLE ***'}",
                  flush=True)
    print("-" * 72)
    if all_ok:
        print("CONJECTURE 5 : CONFIRMEE sur toute la grille testee.")
    else:
        print("CONJECTURE 5 : CONTRE-EXEMPLE TROUVE -- voir ci-dessus.")


if __name__ == "__main__":
    main()
