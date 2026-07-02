"""
TACHE AS-024 -- certificats duaux de transfert pour b_d : mesurer
mu_d = min ||w||^2_B sur les certificats admissibles, d = 1..16.

Cadre (reformulation parite-polynome d'AS-023) : a n = 2d+1,
b_d = dist^2_B(proj(f/2), Lambda) dans W = parite x poly(<=d),
Lambda = proj_W(Z^{n+1}). Certificat de transfert : w = (-1)^k q(k),
deg q <= d, tel que
  (i)  a_k := C(n,k) q(k) entier pour tout k   (<e_k, w>_B entier),
  (ii) somme_{k>=d+1} (-1)^k a_k IMPAIRE       (<f/2, w>_B demi-entier).
Alors b_d >= (1/2)^2 / ||w||^2_B, avec ||w||^2_B = somme a_k^2 / C(n,k).

mu_d := min ||w||^2 sous (i)+(ii). Donne b_d >= 1/(4 mu_d). Si mu_d
est BORNE en d (et la famille optimale a une forme close), la borne
uniforme b_d >= c > 0 devient un enonce d'algebre verifiable — l'etage
manquant sous le theoreme AS-022.

Structure : (i) definit un reseau A de rang d+1 dans Z^{n+1} (vecteurs
entiers du span des colonnes M[k][j] = C(n,j) C(n-j,k-j) — saturation) ;
(ii) est une classe de parite. Minimisation = CVP exact en dimension
d+1 (LLL exacte + enumeration, machinerie AS-023).

Validations obligatoires :
- d=1 : mu_1 = 8/3 (calcul manuel independant).
- coherence : 1/(4 mu_d) <= b_d pour toutes les valeurs exactes connues
  (une violation refuterait le code, la transference etant un theoreme).
"""

from __future__ import annotations

import sys
import time
from fractions import Fraction as F
from math import comb

sys.path.insert(0, "checks")
from task_as006b import kernel_basis  # noqa: E402
from task_as023 import lll_gram  # noqa: E402


def cert_lattice(d):
    """Base saturee de A = Z^{n+1} inter span_Q(M), M[k][j] =
    C(n,j) C(n-j,k-j) (n = 2d+1). Rang d+1."""
    n = 2 * d + 1
    M = [[comb(n, j) * comb(n - j, k - j) if k >= j else 0
          for j in range(d + 1)] for k in range(n + 1)]
    # noyau gauche entier de M : lignes K avec K M = 0
    Mt = [[M[k][j] for k in range(n + 1)] for j in range(d + 1)]
    K = kernel_basis(Mt)                 # (n-d) x (n+1), sature
    # A = noyau entier sature de K
    A = kernel_basis(K)                  # (d+1) x (n+1), sature
    return n, A


def parity_func(n, d, a):
    return sum(a[k] for k in range(d + 1, n + 1)) % 2


def mu_d(d, node_cap=50_000_000):
    """min sum a_k^2/C(n,k) sur A avec parite impaire. CVP exact."""
    import math
    n, A = cert_lattice(d)
    r = d + 1
    # base reorganisee : v0 impair, autres pairs
    pars = [parity_func(n, d, v) for v in A]
    if not any(pars):
        return None, None, "aucun certificat impair (parite nulle sur A)"
    i0 = pars.index(1)
    v0 = A[i0]
    basis = []
    for i, v in enumerate(A):
        if i == i0:
            continue
        if pars[i]:
            v = [v[k] - v0[k] for k in range(n + 1)]
        basis.append(v)
    gens = [[2 * x for x in v0]] + basis          # coset v0 + <gens>
    # metrique diag(1/C(n,k))
    wgt = [F(1, comb(n, k)) for k in range(n + 1)]

    def dot(u, v):
        return sum(wgt[k] * u[k] * v[k] for k in range(n + 1))

    G = [[dot(gens[i], gens[j]) for j in range(r)] for i in range(r)]
    U = lll_gram(G)                                # G devient U^T G U
    gr = [[sum(U[a][i] * gens[a][k] for a in range(r))
           for k in range(n + 1)] for i in range(r)]
    bv = [dot(gr[i], v0) for i in range(r)]
    c0 = dot(v0, v0)
    # LDL^T exact
    L = [[F(1) if i == j else F(0) for j in range(r)] for i in range(r)]
    Dg = [F(0)] * r
    for i in range(r):
        Dg[i] = G[i][i] - sum(L[i][j] ** 2 * Dg[j] for j in range(i))
        for k in range(i + 1, r):
            L[k][i] = (G[k][i] - sum(L[k][j] * L[i][j] * Dg[j]
                                     for j in range(i))) / Dg[i]
    wv = [F(0)] * r
    for i in range(r):
        wv[i] = -bv[i] - sum(L[i][j] * wv[j] for j in range(i))
    zv = [wv[i] / Dg[i] for i in range(r)]
    ystar = [F(0)] * r
    for i in range(r - 1, -1, -1):
        ystar[i] = zv[i] - sum(L[k][i] * ystar[k] for k in range(i + 1, r))
    v0v0 = c0 + sum(bv[i] * ystar[i] for i in range(r))  # min reel
    Lf = [[float(L[i][j]) for j in range(r)] for i in range(r)]
    Df = [float(x) for x in Dg]
    ysf = [float(x) for x in ystar]
    E0 = float(c0 - v0v0)          # exces de y=0 (le point v0 lui-meme)
    best = [E0 * (1 + 1e-9) + 1e-12, [0] * r]
    nodes = [0]
    y = [0] * r

    def dfs(i, part):
        if nodes[0] > node_cap:
            return
        if i < 0:
            if part < best[0]:
                best[0], best[1] = part, y.copy()
            return
        s = sum(Lf[j][i] * y[j] for j in range(i + 1, r))
        zi = ysf[i] + sum(Lf[j][i] * ysf[j] for j in range(i + 1, r))
        center = zi - s
        if part > best[0]:
            return
        # Schnorr-Euchner PARESSEUX : zigzag depuis round(center), sans
        # materialiser la plage (le rayon initial peut etre enorme) ;
        # ordre = distance croissante => 1re feuille = point de Babai,
        # et l'arret sur depassement est correct.
        k0 = round(center)
        left, right = k0 - 1, k0 + 1
        kk = k0
        while True:
            nodes[0] += 1
            if nodes[0] > node_cap:
                return
            t = part + Df[i] * (kk - center) ** 2
            if t > best[0] + 1e-15:
                break
            y[i] = kk
            dfs(i - 1, t)
            y[i] = 0
            if abs(left - center) <= abs(right - center):
                kk, left = left, left - 1
            else:
                kk, right = right, right + 1

    dfs(r - 1, 0.0)
    capped = nodes[0] > node_cap
    a = [v0[k] + sum(gr[i][k] * best[1][i] for i in range(r))
         for k in range(n + 1)]
    val = dot(a, a)
    assert parity_func(n, d, a) == 1, "parite perdue !"
    return val, a, ("CAP" if capped else f"{nodes[0]} noeuds")


def main():
    known = {1: F(1, 8), 2: F(5, 32), 3: F(1, 8), 4: F(93, 512),
             5: F(59, 128), 6: F(13, 32), 7: F(1, 8)}
    print("== mu_d et borne de transfert b_d >= 1/(4 mu_d), d = 1..16 ==")
    for d in range(1, 17):
        t0 = time.time()
        val, a, info = mu_d(d)
        if val is None:
            print(f"  d={d:>2} : {info}", flush=True)
            continue
        bound = 1 / (4 * val)
        chk = ""
        if d == 1:
            chk = " [VALIDATION mu_1 = 8/3 : " + \
                  ("OK]" if val == F(8, 3) else f"ECHEC, {val}]")
        if d in known:
            ok = bound <= known[d]
            chk += f" (<= b_d={known[d]} : {'OK' if ok else 'VIOLATION!'})"
        print(f"  d={d:>2} : mu = {val} = {float(val):.4f} ; "
              f"b_d >= {bound} = {float(bound):.5f}{chk} "
              f"({time.time() - t0:.0f}s, {info})", flush=True)
        n = 2 * d + 1
        print(f"        a = {a}", flush=True)


if __name__ == "__main__":
    main()
