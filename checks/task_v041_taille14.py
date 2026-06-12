"""
TACHE V-041 -- chasse a l'ideale symetrique de taille 14 via la
reduction classique : symetrique ideale de taille 2m (A = -A, B = -B
centrees) <=> ideale de taille m en CARRES PARFAITS. Pour 2m = 14 :
ideale taille 7 dont les 14 entiers sont des carres.

ANTERIORITE (Table 2 de CMSV 2023, bib/pte_cmsv_2023.md) : le secteur
symetrique de la taille 14 n'est fouille que jusqu'a HAUTEUR 900 (le
plafond le plus bas de toutes les tailles ouvertes). En dessous de 900 :
replication verifiante ; au-dela : TERRITOIRE NEUF.

Reduction (preuve elementaire) : A = {+-a_1..+-a_m} rend les k impairs
automatiques ; les k pairs 2j (j = 1..m-1) deviennent
sum (a_i^2)^j = sum (b_i^2)^j -- l'idealite de taille m sur les carres.

Machine : DFS compile, valeurs strictement decroissantes, signe = cote
(a ou b) avec equilibre m/m, signe du sommet fixe (cote a). Elagage par
sommes prefixes des puissances paires : 2j <= 4 en int64 EXACT,
2j >= 6 en float64 avec marges relatives 1e-9 ; tout candidat est
REVERIFIE EXACTEMENT en entiers Python, y compris le relevement a la
paire de taille 2m (degre exact 2m-1).

Validations en cascade (objets connus, formes centrees) :
  m=3 -> {5,6,11 | 1,9,10}    attendue a M = 11  (la taille-6 classique)
  m=4 -> {2,16,21,25 | 5,14,23,24} a M = 25      (Tarry)
  m=6 -> Kuosa                attendue a M = 151
Usage : python task_v041_taille14.py <m> <M_debut> <M_fin>
"""

from __future__ import annotations

import sys
import time

import numpy as np
from numba import njit


@njit(cache=True)
def _dfs14(m2, mside, M, preI, preF, nI, nF, out, max_out):
    val = np.zeros(m2, dtype=np.int64)
    sgn = np.zeros(m2, dtype=np.int64)        # 0 = cote a (+), 1 = cote b (-)
    PI = np.zeros((m2 + 1, nI), dtype=np.int64)
    PF = np.zeros((m2 + 1, nF))
    cp = np.zeros(m2 + 1, dtype=np.int64)
    cm = np.zeros(m2 + 1, dtype=np.int64)
    nf = 0

    val[0] = M
    sgn[0] = 0
    for k in range(nI):
        PI[1, k] = preI[k, M] - preI[k, M - 1]
    for k in range(nF):
        PF[1, k] = preF[k, M] - preF[k, M - 1]
    cp[1] = 1
    cm[1] = 0

    d = 1
    val[d] = M
    sgn[d] = 1            # premier avancement -> (M-1, cote a)
    while d >= 1:
        if sgn[d] == 0:
            sgn[d] = 1
        else:
            val[d] -= 1
            sgn[d] = 0
        v = val[d]
        rp = mside - cp[d]
        rm = mside - cm[d]
        r = m2 - d
        if v < r:
            d -= 1
            continue
        # capacite de signe du present etat
        if sgn[d] == 0 and rp == 0:
            continue
        if sgn[d] == 1 and rm == 0:
            continue
        # faisabilite (independante du signe courant) :
        # -S_p <= P <= S_m avec S_x = somme des r_x plus grandes
        # puissances <= v ; si viole, aucun v' < v ne convient -> remonte
        bad = False
        for k in range(nI):
            P = PI[d, k]
            Sp = preI[k, v] - preI[k, v - rp]
            Sm = preI[k, v] - preI[k, v - rm]
            if P > Sm or -P > Sp:
                bad = True
                break
        if not bad:
            for k in range(nF):
                P = PF[d, k]
                Sp = (preF[k, v] - preF[k, v - rp]) * (1.0 + 1e-9) + 1e-3
                Sm = (preF[k, v] - preF[k, v - rm]) * (1.0 + 1e-9) + 1e-3
                if P > Sm or -P > Sp:
                    bad = True
                    break
        if bad:
            d -= 1
            continue
        # inclure (v, cote) ; descendre ou tester la feuille
        s = 1 if sgn[d] == 0 else -1
        for k in range(nI):
            PI[d + 1, k] = PI[d, k] + s * (preI[k, v] - preI[k, v - 1])
        for k in range(nF):
            PF[d + 1, k] = PF[d, k] + s * (preF[k, v] - preF[k, v - 1])
        if s > 0:
            cp[d + 1] = cp[d] + 1
            cm[d + 1] = cm[d]
        else:
            cp[d + 1] = cp[d]
            cm[d + 1] = cm[d] + 1
        if d == m2 - 1:
            ok = cp[d + 1] == mside and cm[d + 1] == mside
            if ok:
                for k in range(nI):
                    if PI[d + 1, k] != 0:
                        ok = False
                        break
            if ok:
                for k in range(nF):
                    tol = preF[k, M] * 1e-12 * m2 + 0.5
                    p = PF[d + 1, k]
                    if p < 0.0:
                        p = -p
                    if p > tol:
                        ok = False
                        break
            if ok and nf < max_out:
                for i in range(m2):
                    out[nf, i] = -val[i] if sgn[i] == 1 else val[i]
                nf += 1
            continue
        d += 1
        val[d] = v
        sgn[d] = 1
    return nf


def chercher(mside, M):
    """Solutions avec max(a u b) = M exactement (cote du max = a)."""
    m2 = 2 * mside
    U = M
    powers = [2 * j for j in range(1, mside)]      # 2, 4, ..., 2m-2
    pI = [p for p in powers if p <= 4]
    pF = [p for p in powers if p > 4]
    preI = np.zeros((max(len(pI), 1), U + 1), dtype=np.int64)
    for idx, p in enumerate(pI):
        acc = 0
        for v in range(1, U + 1):
            acc += v ** p
            preI[idx, v] = acc
    preF = np.zeros((max(len(pF), 1), U + 1))
    for idx, p in enumerate(pF):
        acc = 0.0
        for v in range(1, U + 1):
            acc += float(v) ** p
            preF[idx, v] = acc
    out = np.zeros((64, m2), dtype=np.int64)
    nf = _dfs14(m2, mside, M, preI, preF, len(pI), len(pF), out, 64)
    sols = []
    for i in range(nf):
        X = [int(t) for t in out[i]]
        a = sorted(x for x in X if x > 0)
        b = sorted(-x for x in X if x < 0)
        # verification exacte des conditions en carres
        if all(sum(x ** (2 * j) for x in a) == sum(x ** (2 * j) for x in b)
               for j in range(1, mside)):
            sols.append((a, b))
    return sols


def verifier_taille_2m(a, b):
    """Releve en paire symetrique de taille 2m et verifie le degre exact."""
    M = max(a + b)
    A = sorted([M + x for x in a] + [M - x for x in a])
    B = sorted([M + x for x in b] + [M - x for x in b])
    deg = 0
    for k in range(1, 4 * len(a)):
        if sum(t ** k for t in A) == sum(t ** k for t in B):
            deg = k
        else:
            break
    return A, B, deg


def main():
    mside = int(sys.argv[1])
    M0 = int(sys.argv[2])
    M1 = int(sys.argv[3])
    print(f"V-041 : ideale taille {mside} en carres parfaits "
          f"(= symetrique taille {2*mside}), M = {M0}..{M1}", flush=True)
    t0 = time.time()
    for M in range(M0, M1 + 1):
        tM = time.time()
        for (a, b) in chercher(mside, M):
            A, B, deg = verifier_taille_2m(a, b)
            print(f"  M = {M} : SOLUTION  a = {a} | b = {b}", flush=True)
            print(f"    taille {2*mside} relevee : degre exact = {deg} "
                  f"(ideale ssi {2*mside - 1}), hauteur = {M}")
            print(f"    A = {A}")
            print(f"    B = {B}", flush=True)
        if M % 20 == 0 or time.time() - tM > 10:
            print(f"  .. M = {M} balaye en {time.time()-tM:.0f}s "
                  f"(total {time.time()-t0:.0f}s)", flush=True)
    print(f"Termine ({time.time()-t0:.0f}s).", flush=True)


if __name__ == "__main__":
    main()
