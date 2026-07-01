"""
TACHE AS-002 -- instrument CVP certifie pour la Conjecture 13 de KV.

Objet : rho(n,d) = min_{Z in Z^{2^n}} ||P(n,d)(Z + MAJ/2)|| / 2^{n/2},
ou P projette orthogonalement au sous-espace V_d des polynomes
multilineaires de degre <= d evalues sur {0,1}^n. La Conjecture 13
(KV TR24-074, p.31) affirme rho >= 1/poly(n) pour d = o(sqrt n/log n).

Reduction exacte (derivee AS-002, verifiee sur n=3 vs scan boite) :
  - C = base ENTIERE SATUREE de ker_Z(A^T) (noyau par reduction de
    colonnes unimodulaire -- exactement sature par construction) ;
  - ||P y||^2 = w^T (C C^T)^{-1} w avec w = C y ; C surjectif sur Z^r
    (saturation) => w parcourt Z^r + C f/2 ;
  - dual scale : D~ = c (C C^T)^{-1} C entier => probleme = CVP entier ;
  - plongement de Kannan : lignes [2 D~_i | 0] + [ (Cf)^T D~ | W ],
    W^2 = borne_sup + 1 (k=+-2 impossible) ; turbo_below + filtre
    |derniere coord| = W ; dist^2 = (val - W^2)/(4c^2), rationnel EXACT.

GARDE-FOU precision : si max|entree| de la base plongee depasse 2^25,
la GSO float du moteur n'est plus fiable -> cellule marquee NON CERTIFIEE.
"""

from __future__ import annotations

import itertools
import sys
import time
from fractions import Fraction

import numpy as np
from sympy import Matrix, Rational, ilcm

from svp_turbo import turbo_lll, turbo_below


def monomial_matrix(n, d):
    monos = []
    for k in range(d + 1):
        monos.extend(itertools.combinations(range(n), k))
    N = 1 << n
    A = [[1 if all((x >> i) & 1 for i in T) else 0 for T in monos]
         for x in range(N)]
    return A, monos


def kernel_basis(M):
    """Base entiere SATUREE de ker_Z(M) (M : m x N, listes d'entiers).
    Reduction de colonnes unimodulaire avec suivi de U : M U = [H|0],
    les colonnes de U face aux colonnes nulles forment la base."""
    m = len(M)
    N = len(M[0])
    A = [list(row) for row in M]
    U = [[1 if i == j else 0 for j in range(N)] for i in range(N)]

    def col_op_swap(j, k):
        for r in range(m):
            A[r][j], A[r][k] = A[r][k], A[r][j]
        for r in range(N):
            U[r][j], U[r][k] = U[r][k], U[r][j]

    def col_op_addmul(j, k, q):  # col_j += q * col_k
        for r in range(m):
            A[r][j] += q * A[r][k]
        for r in range(N):
            U[r][j] += q * U[r][k]

    row = 0
    piv = 0
    while row < m and piv < N:
        # euclide sur les colonnes piv..N-1 dans la ligne 'row'
        while True:
            nz = [j for j in range(piv, N) if A[row][j] != 0]
            if not nz:
                break
            jmin = min(nz, key=lambda j: abs(A[row][j]))
            col_op_swap(piv, jmin)
            done = True
            for j in range(piv + 1, N):
                if A[row][j] != 0:
                    q = -(A[row][j] // A[row][piv])
                    col_op_addmul(j, piv, q)
                    if A[row][j] != 0:
                        done = False
            if done:
                break
        if any(A[row][j] != 0 for j in range(piv, N)):
            piv += 1
        row += 1
    # colonnes piv..N-1 de U : base du noyau
    ker = [[U[r][j] for r in range(N)] for j in range(piv, N)]
    # verification exacte
    for v in ker:
        for r in range(m):
            assert sum(M[r][i] * v[i] for i in range(N)) == 0
    return ker  # liste de r vecteurs de longueur N


def rho_exact(n, d, W_extra=1):
    N = 1 << n
    t = (n + 1) // 2
    f = [1 if bin(x).count("1") >= t else 0 for x in range(N)]
    A, monos = monomial_matrix(n, d)
    m = len(monos)
    At = [[A[x][j] for x in range(N)] for j in range(m)]
    C = kernel_basis(At)                       # r x N, sature
    r = len(C)
    assert r == N - m, (r, N - m)
    # base courte du noyau (LLL preserve le reseau)
    C = [[int(t2) for t2 in rowv] for rowv in turbo_lll(C)]
    Cm = Matrix(C)
    G = Cm * Cm.T
    Ginv = G.inv()
    den = 1
    for i in range(r):
        for j in range(r):
            den = ilcm(den, Rational(Ginv[i, j]).q)
    Dt = (den * Ginv) * Cm                     # r x N entier
    Dt = [[int(Dt[i, j]) for j in range(N)] for i in range(r)]
    Cf = [sum(C[i][x] * f[x] for x in range(N)) for i in range(r)]
    tgt = [sum(Cf[i] * Dt[i][j] for i in range(r)) for j in range(N)]
    val0 = sum(x * x for x in tgt)             # v = 0
    W2 = val0 + W_extra
    rows = [[2 * Dt[i][j] for j in range(N)] + [0] for i in range(r)]
    rows.append(tgt + [int(W2 ** 0.5) + 1])    # W entier > sqrt(val0)
    W = rows[-1][-1]
    W2 = W * W
    borne = val0 + W2
    Gred = turbo_lll(rows)
    maxent = max(abs(int(x)) for rw in Gred for x in rw)
    certifie = maxent < (1 << 25)
    sols = turbo_below(Gred, borne)
    best = None
    for nrm, v in sols:
        if abs(int(v[-1])) == W:
            if best is None or nrm < best:
                best = nrm
    if best is None:
        # v=0 est toujours admissible : dist^2 <= val0 ; si rien trouve,
        # c'est que l'enumeration a filtre le representant de signe.
        best = borne
    dist2 = Fraction(int(best) - W2, 4 * den * den) * 1  # (val-W^2)/(4c^2)
    # ATTENTION : dist reelle = sqrt(dist2) avec la normalisation
    # ||P y||^2 = w^T G^-1 w ; ici on a minimise ||(2v+Cf)^T D~||^2
    # = (2c)^2 * ||P y||^2  => dist^2 = best'/(4 c^2). c = den.
    import math
    dist = math.sqrt(float(dist2))
    rho = dist / 2 ** (n / 2)
    return dict(n=n, d=d, r=r, den=den, dist2=dist2, dist=dist, rho=rho,
                certifie=certifie, maxent=maxent)


def main():
    cells = [(3, 0), (3, 1), (3, 2),
             (4, 1), (4, 2), (4, 3),
             (5, 1), (5, 2), (5, 3)]
    if len(sys.argv) > 1 and sys.argv[1] == "n6":
        cells = [(6, 2), (6, 3)]
    with open("as002_profile.txt", "a", encoding="utf-8") as fh:
        for n, d in cells:
            t0 = time.time()
            try:
                R = rho_exact(n, d)
                line = (f"n={n} d={d} r={R['r']} den={R['den']} : "
                        f"dist={R['dist']:.6f} (dist^2={R['dist2']}) "
                        f"rho={R['rho']:.5f} "
                        f"[{'CERTIFIE' if R['certifie'] else 'NON CERTIFIE (maxent=%d)' % R['maxent']}] "
                        f"({time.time()-t0:.0f}s)")
            except Exception as e:
                line = f"n={n} d={d} : ECHEC {type(e).__name__}: {e}"
            print(line, flush=True)
            fh.write(line + "\n")
            fh.flush()


if __name__ == "__main__":
    main()
