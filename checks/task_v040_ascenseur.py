"""
TACHE V-040 -- l'ascenseur antipalindromique : machine de REPLICATION.

Reduction (V-039, Lemme A) : une ideale de taille n SYMETRIQUE
(B = -A centre ; pour n impair c'est le secteur antipalindromique)
existe ssi il existe n entiers non nuls de valeurs absolues distinctes
X = {e_i * u_i} avec  sum_{x in X} x^k = 0  pour k = 1, 3, ..., 2K-1
(K = ceil(n/2) conditions impaires) -- les conditions paires sont
automatiques (B = -A), et la multiplicite, impaire par le Lemme A,
saute chaque seuil pair gratuitement.

ANTERIORITE (bib/pte_cmsv_2023.md) : ce secteur est VIDE pour n = 11
jusqu'a hauteur 2000 (BLP 2002) puis 3500 (CMSV 2023). Ce script est
donc une REPLICATION verifiante (style B-001/B-002), pas une quete de
nouveaute sous 3500 :
  1. il doit RETROUVER Escott (n = 7, hauteur 51) ;
  2. trouver les ideales symetriques n = 9 connues ;
  3. repliquer une tranche du certificat CMSV (n = 11, vide <= plafond).

Implementation : DFS compile (numba), valeurs decroissantes strictes,
signe du sommet fixe (+), elagage par sommes prefixes des puissances
(k = 1..7 en int64 exact ; k = 9 en float64 avec marge relative 1e-6
et REVERIFICATION EXACTE en entiers Python de tout candidat).
"""

from __future__ import annotations

import sys
import time

import numpy as np
from numba import njit


@njit(cache=True)
def _dfs(nvals, M, preI, preF, kI, useF, out, max_out):
    """DFS : valeurs |u| strictement decroissantes depuis M, signes +-,
    signe du premier fixe a +. preI : (kI, U+1) sommes prefixes int64
    des puissances 1,3,5,7 ; preF : (U+1,) prefixes float64 de k=9.
    Retourne le nombre de solutions ecrites dans out (lignes signees)."""
    val = np.zeros(nvals, dtype=np.int64)
    sgn = np.zeros(nvals, dtype=np.int64)   # 0 = +, 1 = -
    PI = np.zeros((nvals + 1, kI), dtype=np.int64)
    PF = np.zeros(nvals + 1)
    nf = 0

    val[0] = M
    sgn[0] = 0
    for k in range(kI):
        PI[1, k] = preI[k, M] - preI[k, M - 1]
    PF[1] = preF[M] - preF[M - 1] if useF == 1 else 0.0

    d = 1
    val[d] = M  # sera decremente en entree de boucle
    sgn[d] = 1  # force le passage a (val-1, +) au premier tour
    while d >= 1:
        # avancer l'etat du niveau d : signe - apres +, sinon valeur-1
        if sgn[d] == 0:
            sgn[d] = 1
        else:
            val[d] -= 1
            sgn[d] = 0
        v = val[d]
        r = nvals - 1 - d  # restants APRES ce niveau
        if v < r + 1:
            # plus assez de valeurs distinctes : remonter
            d -= 1
            continue
        # elagage AVANT inclusion : capacite max des r+1 choix restants
        # (ce niveau inclus, valeurs <= v) contre |sommes partielles|
        dead = False
        cut = False
        for k in range(kI):
            cap = preI[k, v] - preI[k, v - r - 1]
            p = PI[d, k]
            if p < 0:
                p = -p
            if p > cap:
                cut = True
                break
        if not cut and useF == 1:
            capf = (preF[v] - preF[v - r - 1]) * (1.0 + 1e-6) + 1e-3
            pf = PF[d]
            if pf < 0.0:
                pf = -pf
            if pf > capf:
                cut = True
        if cut:
            # aucune valeur <= v ne peut suffire : remonter
            d -= 1
            continue
        # inclure (v, sgn) et descendre / tester la feuille
        s = -1 if sgn[d] == 1 else 1
        for k in range(kI):
            pw = preI[k, v] - preI[k, v - 1]
            PI[d + 1, k] = PI[d, k] + s * pw
        if useF == 1:
            PF[d + 1] = PF[d] + s * (preF[v] - preF[v - 1])
        else:
            PF[d + 1] = 0.0
        if d == nvals - 1:
            ok = True
            for k in range(kI):
                if PI[d + 1, k] != 0:
                    ok = False
                    break
            if ok and useF == 1:
                tol = (preF[M] - preF[M - 1]) * 1e-9 + 0.5
                pf = PF[d + 1]
                if pf < 0.0:
                    pf = -pf
                if pf > tol:
                    ok = False
            if ok and nf < max_out:
                for i in range(nvals):
                    out[nf, i] = -val[i] if sgn[i] == 1 else val[i]
                nf += 1
            # rester au meme niveau : la boucle avancera (v, sgn)
            continue
        d += 1
        val[d] = v  # sera decremente -> commence a v-1
        sgn[d] = 1
    return nf


def chercher(nvals, K, M):
    """Toutes les solutions signees avec max |u| = M exactement."""
    U = M
    ks = [1, 3, 5, 7, 9][:K]
    kI = min(K, 4)
    useF = 1 if K == 5 else 0
    preI = np.zeros((kI, U + 1), dtype=np.int64)
    for j in range(kI):
        k = ks[j]
        acc = 0
        for v in range(1, U + 1):
            acc += v ** k
            preI[j, v] = acc
    preF = np.zeros(U + 1)
    if useF:
        acc = 0.0
        for v in range(1, U + 1):
            acc += float(v) ** 9
            preF[v] = acc
    out = np.zeros((64, nvals), dtype=np.int64)
    nf = _dfs(nvals, M, preI, preF, kI, useF, out, 64)
    sols = []
    for i in range(nf):
        X = [int(t) for t in out[i]]
        # verification EXACTE en entiers Python (k impairs jusqu'a 2K-1)
        if all(sum(x ** k for x in X) == 0 for k in ks):
            sols.append(X)
    return sols


def verifier_pte(X):
    """Construit la paire PTE A = X + M, B = -X + M et verifie le degre
    exact en entiers Python. Retourne (A, B, degre, span)."""
    M = max(abs(x) for x in X)
    A = sorted(x + M for x in X)
    B = sorted(M - x for x in X)
    deg = 0
    for k in range(1, 2 * len(X)):
        if sum(a ** k for a in A) == sum(b ** k for b in B):
            deg = k
        else:
            break
    return A, B, deg, max(A + B) - min(A + B)


def main():
    nvals = int(sys.argv[1])
    M0 = int(sys.argv[2])
    M1 = int(sys.argv[3])
    # n impair : ideal = multiplicite n ; conditions impaires k = 1..n-2
    # (chaque seuil pair est franchi gratuitement, Lemme A V-039)
    K = (nvals - 1) // 2
    print(f"V-040 ascenseur : n = {nvals}, conditions impaires k = "
          f"{[1,3,5,7,9][:K]}, hauteurs M = {M0}..{M1}", flush=True)
    t0 = time.time()
    for M in range(M0, M1 + 1):
        sols = chercher(nvals, K, M)
        for X in sols:
            A, B, deg, span = verifier_pte(X)
            print(f"  M = {M} : SOLUTION  X = {sorted(X, key=abs)}",
                  flush=True)
            print(f"    A = {A}")
            print(f"    B = {B}")
            print(f"    degre exact = {deg} (ideale taille {nvals} ssi "
                  f"{nvals - 1}), span = {span}", flush=True)
        if M % 25 == 0:
            print(f"  .. M = {M} balaye ({time.time()-t0:.0f}s)",
                  flush=True)
    print(f"Termine ({time.time()-t0:.0f}s).", flush=True)


if __name__ == "__main__":
    main()
