"""
TACHE V-056 -- L'HYBRIDE : diviseurs cyclotomiques FORCES (BM 2000,
Theoremes 3-4) x moteur turbo-LLL. Cherche des multiples PLATS (hauteur 1)
de (x-1)^m de degre < champions produits purs (473 pour m=22, 439 pour
m=23), produits purs OU NON -- teste le caveat central de V-054
(produit pur = d(m) general ?).

Principe (neuf : BM n'utilisaient que f=(x-1)^m ou (x-1)^m(x+1)) :
tout f plat de degre <= D divisible par (x-1)^m est AUSSI divisible par
les Phi_p forces (Thm 3 : p <= m premier, r = floor((m-1)/(p-1)),
d <= p^{r+1}-p => Phi_p | f ; Thm 4 : d <= 2^{floor((m+3)/2)}-2 =>
Phi_4 | f). On quotiente donc SANS PERTE : f = f0 * q avec
f0 = (x-1)^m * prod Phi_n, et on cherche q par reduction de reseau sur
la base reciproque de BM (h_k = f0*g_k), scan hauteur <= 1.

Usage : python task_v056_hybride.py m D [pairs=1]
"""
from __future__ import annotations

import sys

import numpy as np

sys.path.insert(0, '.')
from svp_turbo import turbo_lll, turbo_shortest, turbo_below


def cyclotomic(n):
    """Phi_n pour n premier (all-ones) ou n=4. Suffisant ici."""
    if n == 4:
        return np.array([1, 0, 1], dtype=np.int64)
    # n premier
    return np.ones(n, dtype=np.int64)


def forced_divisors(m, D):
    """Diviseurs forces par BM Thm 3 (p premier <= m) et Thm 4 (Phi_4)."""
    forced = []
    p = 2
    while p <= m:
        # primalite naive
        if all(p % q for q in range(2, int(p**0.5) + 1)):
            r = (m - 1) // (p - 1)
            if D <= p ** (r + 1) - p:
                forced.append(p)
        p += 1
    if m >= 2 and D <= 2 ** ((m + 3) // 2) - 2:
        forced.append(4)
    return sorted(forced)


def build_f0(m, forced):
    f = np.array([1], dtype=np.int64)
    for _ in range(m):                       # (x-1)^m ; signe global sans importance
        f = np.convolve(f, np.array([-1, 1], dtype=np.int64))
    for n in forced:
        f = np.convolve(f, cyclotomic(n))
    return f


def bm_basis(f0, n):
    """Base de BM : h_k = f0 * g_k, g_0 = x^{2n}+1, g_k = x^{2n}+x^{2n-k}+x^k+1,
    g_n = x^{2n}+x^n+1. Rang n+1, degre total = 2n + deg f0."""
    D = 2 * n + len(f0) - 1
    rows = []
    for k in range(n + 1):
        g = np.zeros(2 * n + 1, dtype=np.int64)
        g[0] = 1
        g[2 * n] += 1
        if 0 < k < n:
            g[k] += 1
            g[2 * n - k] += 1
        elif k == n:
            g[n] += 1
        h = np.convolve(f0, g)
        row = np.zeros(D + 1, dtype=np.int64)
        row[:len(h)] = h
        rows.append(row)
    return np.array(rows, dtype=np.int64)


def height_span(v):
    nz = np.nonzero(v)[0]
    if len(nz) == 0:
        return None, None, None
    return int(np.abs(v).max()), int(nz[-1] - nz[0]), int(np.abs(v).sum())


def mult_at_1(v):
    c = np.array(v, dtype=object)
    mm = 0
    while len(c) and sum(c) == 0:
        c = np.cumsum(c)[:-1]
        mm += 1
    return mm


def main():
    m = int(sys.argv[1])
    D = int(sys.argv[2])
    do_pairs = int(sys.argv[3]) if len(sys.argv) > 3 else 1

    noforce = len(sys.argv) > 5 and sys.argv[5] == "noforce"
    forced = [] if noforce else forced_divisors(m, D)
    f0 = build_f0(m, forced)
    degf0 = len(f0) - 1
    if (D - degf0) % 2:
        D -= 1                                # parite de la base BM
    n = (D - degf0) // 2
    print(f"V-056 hybride : m={m}, D={D}, forces Phi_{forced} "
          f"(deg f0 = {degf0}, max|f0| = {int(np.abs(f0).max())}), "
          f"rang reseau = {n+1}", flush=True)

    B = bm_basis(f0, n)
    import time
    t0 = time.time()
    R = turbo_lll([list(map(int, r)) for r in B])
    R = np.array(R, dtype=np.int64)
    print(f"LLL fait en {time.time()-t0:.0f}s", flush=True)

    best = []                                  # (hauteur, span, l1, index)
    for i, v in enumerate(R):
        h, s, l1 = height_span(v)
        if h is None:
            continue
        best.append((h, s, l1, i))
    best.sort()
    print("top 8 par hauteur (h, span, l1) :", [(h, s, l1) for h, s, l1, _ in best[:8]], flush=True)

    flats = [(h, s, l1, i) for h, s, l1, i in best if h == 1]
    if do_pairs and not flats:
        t0 = time.time()
        seen_best = 10 ** 9
        for i in range(len(R)):
            for j in range(i + 1, len(R)):
                for sg in (1, -1):
                    v = R[i] + sg * R[j]
                    h, s, l1 = height_span(v)
                    if h == 1:
                        flats.append((h, s, l1, (i, j, sg)))
                    elif h is not None and h < seen_best:
                        seen_best = h
        print(f"scan paires en {time.time()-t0:.0f}s ; "
              f"meilleure hauteur paire = {seen_best}", flush=True)

    # --- etape exacte : enumeration sous une borne (les plats ont L2^2 = l1) ---
    mode = sys.argv[4] if len(sys.argv) > 4 else ""
    if mode.startswith("below:") and not flats:
        borne = int(mode.split(":")[1])
        t0 = time.time()
        vecs = turbo_below([list(map(int, r)) for r in R], borne)
        print(f"turbo_below(borne={borne}) : {len(vecs)} vecteurs "
              f"en {time.time()-t0:.0f}s", flush=True)
        for nrm, v in vecs:
            v = np.array(v, dtype=np.int64)
            h, s, l1 = height_span(v)
            if h == 1:
                flats.append((h, s, l1, ("below", v)))
        if not flats and vecs:
            hs = sorted((height_span(np.array(v, dtype=np.int64))[0], int(nrm))
                        for nrm, v in vecs)
            print(f"   aucune hauteur 1 ; (hauteur, norme) presents : {hs[:10]}", flush=True)

    if flats:
        flats.sort(key=lambda t: t[1])         # plus petit span d'abord
        for h, s, l1, idx in flats[:5]:
            if isinstance(idx, tuple) and idx[0] == "below":
                v = idx[1]
            elif isinstance(idx, (int, np.integer)):
                v = R[idx]
            else:
                v = R[idx[0]] + idx[2] * R[idx[1]]
            nz = np.nonzero(v)[0]
            w = v[nz[0]:nz[-1] + 1]
            mm = mult_at_1(w)
            print(f"*** PLAT : span {s}, l1 {l1}, multiplicite {mm} "
                  f"{'>=' if mm >= m else '<'} m={m}", flush=True)
            champ = {22: 473, 23: 439}.get(m)
            if champ is not None and s < champ and mm >= m:
                print("    !!! BAT LE CHAMPION PRODUIT PUR !!!", flush=True)
            print("    coeffs:", list(map(int, w)), flush=True)
    else:
        print("aucun vecteur plat (hauteur 1) dans cette cellule", flush=True)


if __name__ == "__main__":
    main()
