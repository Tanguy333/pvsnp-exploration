"""
SVP_SYM -- enumeration restreinte aux secteurs SYMETRIQUES du reseau KV
(V-049b). Calcule lambda+ (palindromes) et lambda- (antipalindromes)
EXACTEMENT, en enumerant les sous-reseaux L+ / L- de rang r/2 chacun
(au lieu du plein rang r). Accelerateur de phi(m) -- PAS un certificat
inconditionnel (les vecteurs asymetriques sont hors L+ u L-).

Base de L+/L- = NOYAU ENTIER SATURE de (S -+ I) (S = sigma en coords de
L), construit exactement (sympy) -- jamais le systeme generateur naif.
"""

from __future__ import annotations

import numpy as np
from sympy import Matrix, eye, Rational, igcd, ilcm

from task_v004_kv_conjecture5 import build_basis, lll_reduce
from svp_turbo import turbo_lll, turbo_shortest


def _prim(v):
    d_ = 1
    for x in v:
        d_ = ilcm(d_, Rational(x).q)
    w = [int(x * d_) for x in v]
    g = 0
    for x in w:
        g = igcd(g, x)
    return [x // g for x in w] if g else w


def _sigma_matrix(Bz, n):
    r = len(Bz)
    B = Matrix(Bz)
    Brev = Matrix([[Bz[i][n - j] for j in range(n + 1)] for i in range(r)])
    S = Brev * B.T * (B * B.T).inv()
    assert all(x == int(x) for x in S), "S non entiere"
    S = Matrix([[int(x) for x in S.row(i)] for i in range(r)])
    assert (S * S) == eye(r), "S^2 != I"
    return S


def _sublattice_basis(Bz, n, sign):
    """Base ENTIERE (lignes, en coords absolues = polynomes) du
    sous-reseau L+ (sign=+1) ou L- (sign=-1)."""
    r = len(Bz)
    S = _sigma_matrix(Bz, n)
    ker = (S - sign * eye(r)).nullspace()        # coords dans la base L
    coords = [_prim(list(v)) for v in ker]        # base entiere primitive
    # remonter en coordonnees absolues : combinaison des lignes de Bz
    B = np.array(Bz, dtype=object)
    rows = []
    for c in coords:
        row = np.zeros(n + 1, dtype=object)
        for i, ci in enumerate(c):
            if ci:
                row = row + ci * B[i]
        rows.append([int(t) for t in row])
    return rows


def sym_shortest(d, n):
    """Retourne (lambda_plus, lambda_minus, vecteurs minimaux par secteur)."""
    Bz = [[int(t) for t in row] for row in build_basis(n, d)]
    out = {}
    for sign, nom in ((+1, "plus"), (-1, "minus")):
        rows = _sublattice_basis(Bz, n, sign)
        if not rows:
            out[nom] = (None, [])
            continue
        G = turbo_lll(rows)
        nrm, sols = turbo_shortest(G)
        out[nom] = (nrm, sols)
    lp = out["plus"][0]
    lm = out["minus"][0]
    return lp, lm, out
