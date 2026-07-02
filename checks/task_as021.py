"""
TACHE AS-021 (v2) -- constructions par POLYNOME ARRONDI : bornes
superieures sur q(n,d) DANS le regime de la Conjecture 13 (d ~ sqrt(n)).

v1 (minimisation alternee seule) ECHOUAIT la validation : 5-11x
au-dessus des optima connus a (7,3),(9,3),(13,3) — minima locaux.
v2 = descente par coordonnees (moves Z_k +/- 1,2) + saut de bassin
(perturbation aleatoire, redescente, garde si meilleur), departs
multiples (Z=0, minimisation alternee, perturbes). Objectif float =
residu des moindres carres B-ponderes via base orthonormee (QR), puis
verdict EXACT (Fraction) sur le meilleur temoin : q_UB RIGOUREUSE.

Protocole : VALIDATION d'abord sur les cellules exactes connues
((7,3)=1/8, (9,3)=387/512, (13,3)=9749/512), ensuite seulement les
cellules iso-diagonale d=sqrt(n), n=25..169.
"""

from __future__ import annotations

import sys
import time
from fractions import Fraction as F
from math import comb

import numpy as np


def eval_exact(n, d, Z, f):
    """dist_B^2(Z + f/2, V_d) exacte : moindres carres rationnels."""
    y = [F(2 * int(Z[k]) + int(f[k]), 2) for k in range(n + 1)]
    B = [comb(n, k) for k in range(n + 1)]
    X = [[comb(k, j) for j in range(d + 1)] for k in range(n + 1)]
    A = [[sum(F(B[k] * X[k][i] * X[k][j]) for k in range(n + 1))
          for j in range(d + 1)] for i in range(d + 1)]
    b = [sum(F(B[k] * X[k][i]) * y[k] for k in range(n + 1))
         for i in range(d + 1)]
    from sympy import Matrix, Rational
    beta = Matrix([[Rational(A[i][j].numerator, A[i][j].denominator)
                    for j in range(d + 1)] for i in range(d + 1)]).LUsolve(
        Matrix([Rational(x.numerator, x.denominator) for x in b]))
    val = F(0)
    for k in range(n + 1):
        pk = sum(F(int(beta[j].p), int(beta[j].q)) * X[k][j]
                 for j in range(d + 1))
        val += B[k] * (y[k] - pk) ** 2
    return val


def exact_polish(n, d, Z, f, max_sweeps=8):
    """Descente par coordonnees EXACTE (rationnels) : corrige les
    coordonnees de queue invisibles au float64 (poids binomial minuscule
    => variation sous le seuil relatif), qui autrement s'amplifient
    ~2^d par pas d'extrapolation. D(Z+de_k) = D + 2d.g_k + d^2.M_kk avec
    g_k = B_k(y_k - (Xw)_k), M_kk = B_k(1 - B_k x_k^T G x_k) : optimum
    entier = arrondi(-g_k/M_kk), accepte si amelioration exacte."""
    from sympy import Matrix, Rational
    Z = [int(z) for z in Z]
    B = [F(comb(n, k)) for k in range(n + 1)]
    X = [[F(comb(k, j)) for j in range(d + 1)] for k in range(n + 1)]
    A = [[sum(B[k] * X[k][i] * X[k][j] for k in range(n + 1))
          for j in range(d + 1)] for i in range(d + 1)]
    G = Matrix([[Rational(A[i][j].numerator, A[i][j].denominator)
                 for j in range(d + 1)] for i in range(d + 1)]).inv()
    G = [[F(int(G[i, j].p), int(G[i, j].q)) for j in range(d + 1)]
         for i in range(d + 1)]
    Mkk = [B[k] * (1 - B[k] * sum(X[k][i] * G[i][j] * X[k][j]
                                  for i in range(d + 1)
                                  for j in range(d + 1)))
           for k in range(n + 1)]
    y = [F(2 * Z[k] + int(f[k]), 2) for k in range(n + 1)]
    Xty = [sum(B[k] * X[k][i] * y[k] for k in range(n + 1))
           for i in range(d + 1)]
    for _ in range(max_sweeps):
        moved = False
        for k in range(n + 1):
            if Mkk[k] == 0:
                continue
            w = [sum(G[i][j] * Xty[j] for j in range(d + 1))
                 for i in range(d + 1)]
            gk = B[k] * (y[k] - sum(X[k][j] * w[j] for j in range(d + 1)))
            delta = round(-gk / Mkk[k])
            if delta != 0 and 2 * delta * gk + delta * delta * Mkk[k] < 0:
                Z[k] += delta
                y[k] += delta
                for i in range(d + 1):     # maj incrementale de X^T B y
                    Xty[i] += delta * B[k] * X[k][i]
                moved = True
        if not moved:
            break
    return Z


def setup(n, d):
    t = (n + 1) // 2
    f = np.array([1.0 if k >= t else 0.0 for k in range(n + 1)])
    ks = np.arange(n + 1, dtype=float)
    B = np.array([float(comb(n, k)) for k in range(n + 1)])
    W = np.sqrt(B)
    Xb = np.stack([((ks - t) / max(n, 1)) ** j for j in range(d + 1)], axis=1)
    Q, _ = np.linalg.qr(Xb * W[:, None])

    def obj(Z):
        wy = W * (Z + f / 2.0)
        r = wy - Q @ (Q.T @ wy)
        return float(r @ r)

    return f, Xb, W, obj


def descend(Z, obj):
    """Descente par coordonnees avec recherche lineaire a pas doublant :
    aux grands n les coordonnees optimales sont a des dizaines d'unites,
    les pas fixes +/-1,2 convergeraient en marchant — on double le pas
    tant que ca descend (1,2,4,8,...), puis on raffine."""
    val = obj(Z)
    improved = True
    while improved:
        improved = False
        for k in range(len(Z)):
            for sgn in (1, -1):
                step = sgn
                while True:
                    Z[k] += step
                    v = obj(Z)
                    if v < val * (1 - 1e-12) - 1e-300:
                        val = v
                        improved = True
                        step *= 2
                    else:
                        Z[k] -= step
                        break
    return Z, val


def alt_min(n, d, f, Xb, W, iters=60):
    Z = np.zeros(n + 1)
    for _ in range(iters):
        yv = Z + f / 2.0
        beta, *_ = np.linalg.lstsq(Xb * W[:, None], yv * W, rcond=None)
        Z2 = np.round(Xb @ beta - f / 2.0)
        if np.array_equal(Z2, Z):
            break
        Z = Z2
    return Z


def construct(n, d, hops=80, seed=1, verbose=False):
    """Meilleur temoin entier : multi-departs + descente + saut de bassin."""
    f, Xb, W, obj = setup(n, d)
    rng = np.random.default_rng(seed)
    starts = [np.zeros(n + 1), alt_min(n, d, f, Xb, W)]
    best, bestZ = None, None
    for Z0 in starts:
        Z, val = descend(Z0.copy(), obj)
        if best is None or val < best:
            best, bestZ = val, Z.copy()
    if verbose:
        print(f"    [descentes initiales : q~{best / 2.0**n * 1024:.4f}]",
              flush=True)
    # saut de bassin depuis le meilleur ; les sauts POLYNOMIAUX
    # (Z += round(P), P reel de degre <= d) traversent les vallees :
    # ils deplacent loin en ne changeant l'objectif que par l'erreur
    # d'arrondi de P (les polynomes ENTIERS sont des symetries exactes).
    # L'amplitude des sauts est PROPORTIONNELLE aux coefficients du
    # polynome courant : l'echelle des bassins croit comme C(n/2, d-1)
    # avec n, une amplitude fixe devient invisible aux grands n.
    for h in range(hops):
        Z = bestZ.copy()
        if h % 3 == 0:
            idx = rng.choice(n + 1, size=max(1, (n + 1) // 8), replace=False)
            Z[idx] += rng.integers(-2, 3, size=len(idx))
        elif h % 3 == 1:
            s = rng.choice([1.0, 4.0, 16.0, 64.0])
            a = rng.normal(0, s, d + 1) * (2.0 ** np.arange(d + 1))
            Z += np.round(Xb @ a)
        else:
            yb = bestZ + f / 2.0
            beta, *_ = np.linalg.lstsq(Xb * W[:, None], yb * W, rcond=None)
            s = rng.choice([0.01, 0.03, 0.1, 0.3])
            a = rng.normal(0, 1, d + 1) * (s * np.abs(beta) + 2.0)
            Z += np.round(Xb @ a)
        Z, val = descend(Z, obj)
        if val < best * (1 - 1e-12):
            best, bestZ = val, Z.copy()
        if verbose and (h + 1) % max(10, hops // 6) == 0:
            print(f"    [saut {h + 1}/{hops} : q~{best / 2.0**n * 1024:.4f}]",
                  flush=True)
    return [int(z) for z in bestZ], [int(x) for x in f], best


def hop_once(Z, n, d, f, Xb, W, obj, rng, h):
    """Un saut de bassin (meme melange de mouvements que construct)."""
    Z = Z.copy()
    if h % 3 == 0:
        idx = rng.choice(n + 1, size=max(1, (n + 1) // 8), replace=False)
        Z[idx] += rng.integers(-2, 3, size=len(idx))
    elif h % 3 == 1:
        s = rng.choice([1.0, 4.0, 16.0, 64.0])
        a = rng.normal(0, s, d + 1) * (2.0 ** np.arange(d + 1))
        Z += np.round(Xb @ a)
    else:
        yb = Z + f / 2.0
        beta, *_ = np.linalg.lstsq(Xb * W[:, None], yb * W, rcond=None)
        s = rng.choice([0.01, 0.03, 0.1, 0.3])
        a = rng.normal(0, 1, d + 1) * (s * np.abs(beta) + 2.0)
        Z += np.round(Xb @ a)
    return descend(Z, obj)


def continuation(d, n1, hops_step=30, seed=1, verbose=True):
    """Continuation par ALIGNEMENT AU SEUIL : la plongee Q(m) est stable
    en la coordonnee m = t - k a travers n (structure AS-021), donc on
    resout la petite cellule a fond puis on marche n -> n+2 en copiant
    le temoin aligne au seuil (t' = t+1 : Znew[k'] = Z[k'-1]) et en
    extrapolant la queue basse par le polynome de plongee."""
    n0 = 2 * d + 1
    Z, f, approx = construct(n0, d, hops=3000, seed=seed)
    Z = np.array(Z, dtype=float)
    rng = np.random.default_rng(seed + 1000)
    n = n0
    while n < n1:
        n += 2
        # graine alignee au seuil
        Znew = np.empty(n + 1)
        Znew[1:n] = Z[0:n - 1]
        Znew[n] = Z[n - 2]          # haut : copie (zone plate 2Z+f=1)
        lo = np.polyfit(np.arange(d + 1, dtype=float), Z[0:d + 1],
                        min(d - 1, d))
        Znew[0] = np.round(np.polyval(lo, -1.0))   # bas : extrapolation
        f2, Xb, W, obj = setup(n, d)
        Znew, val = descend(Znew, obj)
        best, bestZ = val, Znew.copy()
        for h in range(hops_step):
            Zc, v = hop_once(bestZ, n, d, f2, Xb, W, obj, rng, h)
            if v < best * (1 - 1e-12):
                best, bestZ = v, Zc.copy()
        # polissage EXACT : repare les queues invisibles au float64
        bestZ = np.array(exact_polish(n, d, bestZ, f2), dtype=float)
        best = obj(bestZ)
        Z, f = bestZ, f2
        if verbose and (n % 8 == 1 or n == n1):
            print(f"    [cont d={d} : n={n}, q~{best / 2.0**n * 1024:.4f}]",
                  flush=True)
    return [int(z) for z in Z], [int(x) for x in f]


def run_cell(n, d, hops, verbose=False, seeds=(1,)):
    t0 = time.time()
    bestv, bestZ, bestf = None, None, None
    for seed in seeds:
        Z, f, approx = construct(n, d, hops=hops, seed=seed, verbose=verbose)
        if bestv is None or approx < bestv:
            bestv, bestZ, bestf = approx, Z, f
    val = eval_exact(n, d, bestZ, bestf)
    q = val / (F(2) ** n)
    return val, q, time.time() - t0


def main_cont():
    """Mode continuation : python task_as021.py cont <d> <n1>"""
    d, n1 = int(sys.argv[2]), int(sys.argv[3])
    t0 = time.time()
    Z, f = continuation(d, n1)
    val = eval_exact(n1, d, Z, f)
    q = val / (F(2) ** n1)
    print(f"  CONT (n={n1}, d={d}) : q_UB = {float(q * 1024):.4f}/1024 "
          f"(exact {val.numerator}/{val.denominator} / 2^{n1}) "
          f"({time.time()-t0:.0f}s)", flush=True)


def main():
    print("== VALIDATION (optima exacts connus, hypothese symetrique) ==")
    known = {(7, 3): F(1, 8), (9, 3): F(387, 512), (13, 3): F(9749, 512)}
    ok = 0
    for (n, d), opt in known.items():
        val, q, dt = run_cell(n, d, hops=200)
        tag = "OK exact" if val == opt else f"ratio {float(val / opt):.3f}"
        ok += val == opt
        print(f"  (n={n},d={d}) : construction={val} vs optimum={opt} "
              f"[{tag}] ({dt:.0f}s)", flush=True)
    print(f"  validation : {ok}/{len(known)} optima retrouves exactement")
    # non-regression : (25,5) doit atteindre <= 452689582665/8388608
    # (~1.647/1024, meilleur temoin connu, bat le cap 3.74 d'AS-014)
    ref = F(452689582665, 8388608)
    val, q, dt = run_cell(25, 5, hops=3000, seeds=(1, 2, 3, 4))
    tag = "OK" if val <= ref else f"REGRESSION x{float(val / ref):.2f}"
    print(f"  (n=25,d=5) : {float(q * 1024):.4f}/1024 vs ref 1.6469 [{tag}] "
          f"({dt:.0f}s)", flush=True)

    print("== ISO-DIAGONALE d = sqrt(n) : bornes sup RIGOUREUSES ==")
    # budgets calibres : ~5s/3000 sauts a n=25, ~0.6s/saut a n=169
    plan = [(49, 7, 3000, (1, 2, 3, 4)),
            (81, 9, 2000, (1, 2)), (121, 11, 1500, (1, 2)),
            (169, 13, 900, (1,))]
    for (n, d, hops, seeds) in plan:
        val, q, dt = run_cell(n, d, hops=hops, verbose=(n >= 121),
                              seeds=seeds)
        print(f"  (n={n:>3}, d={d:>2}) : q_UB = {float(q * 1024):.4f}/1024 "
              f"(exact {val.numerator}/{val.denominator} / 2^{n}) "
              f"({dt:.0f}s, {len(seeds)}x{hops} sauts)", flush=True)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "cont":
        main_cont()
    else:
        main()
