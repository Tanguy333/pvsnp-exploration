"""
TACHE V-049 -- peut-on battre 307 pour d(20) ?
Recherche EXHAUSTIVE des produits purs plats a 20 facteurs distincts
(1-x^{t_i}), t_1 < t_2 < ... < t_20, de degre dans [256, 306], en
autorisant une hauteur de transit >= 4 (le regime que les recherches
transit <= 3 de V-047 ne couvraient pas).

Escalade : transit <= 4, puis 5, puis 6. Pour chaque niveau, le degre
minimal d'un produit plat <= 306 est rapporte. Si rien <= 306, 307
(V-047) reste la plus petite valeur connue dans (transit <= niveau).

Verification finale : tout champion est re-verifie en entiers Python
(hauteur 1) et multiplicite 20 par division symbolique.
"""

from __future__ import annotations

import sys
import time

import numpy as np
from numba import njit


@njit(cache=True)
def _dfs(NFAC, LO, HI, HTRANS, out, max_out):
    """Exposants STRICTEMENT croissants. poly = produit courant.
    Hauteur de transit <= HTRANS aux prefixes, == 1 au produit complet.
    Garde les produits plats de degre dans [LO, HI]."""
    DMAX = HI + 1
    poly = np.zeros((NFAC + 1, DMAX), dtype=np.int16)
    poly[0, 0] = 1
    texp = np.zeros(NFAC + 1, dtype=np.int64)
    degs = np.zeros(NFAC + 1, dtype=np.int64)
    nf = 0

    d = 1
    texp[1] = 0            # premier += 1 -> 1
    while d >= 1:
        texp[d] += 1
        t = texp[d]
        reste = NFAC - d   # facteurs restants, chacun STRICTEMENT > t
        # degre minimal pour finir : t + (t+1) + ... + (t+reste)
        dmin = degs[d - 1] + t + reste * t + reste * (reste + 1) // 2
        if dmin > HI:
            d -= 1
            continue
        nd = degs[d - 1] + t
        hmax = 1 if d == NFAC else HTRANS
        ok = True
        for i in range(nd + 1):
            v = poly[d - 1, i] if i <= degs[d - 1] else 0
            w = poly[d - 1, i - t] if i >= t else 0
            c = v - w
            if c > hmax or c < -hmax:
                ok = False
                break
            poly[d, i] = c
        if not ok:
            continue
        degs[d] = nd
        if d == NFAC:
            if LO <= nd <= HI and nf < max_out:
                for j in range(NFAC):
                    out[nf, j] = texp[j + 1]
                out[nf, NFAC] = nd
                nf += 1
            continue
        d += 1
        texp[d] = t        # prochain += 1 -> t+1 (strictement croissant)
    return nf


def verifie(ts):
    f = [1]
    for t in ts:
        g = [0] * (len(f) + t)
        for i, c in enumerate(f):
            g[i] += c
            g[i + t] -= c
        f = g
    h = max(abs(c) for c in f)
    import sympy as sp
    x = sp.symbols("x")
    p = sp.Poly(list(reversed(f)), x)
    m = 0
    q = p
    while True:
        quo, rem = sp.div(q, sp.Poly([-1, 1], x))
        if not rem.is_zero:
            break
        q = quo
        m += 1
    return h, m, len(f) - 1


def main():
    LO, HI = 256, 306
    for htrans in (4, 5, 6):
        print(f"=== transit <= {htrans}, degre dans [{LO},{HI}] ===", flush=True)
        t0 = time.time()
        out = np.zeros((200000, 21), dtype=np.int64)
        nf = _dfs(20, LO, HI, htrans, out, 200000)
        sols = sorted((int(out[i, 20]), [int(x) for x in out[i, :20]])
                      for i in range(nf))
        print(f"  {nf} produits plats de degre <= {HI} "
              f"({time.time()-t0:.0f}s)", flush=True)
        for deg, ts in sols[:5]:
            h, m, dd = verifie(ts)
            tag = "OK" if (h == 1 and m == 20) else f"INVALIDE h={h} m={m}"
            print(f"  degre {deg} : {ts}  [{tag}]", flush=True)
        if sols:
            print(f"  >>> 307 BATTU : plus petit degre = {sols[0][0]} "
                  f"a transit <= {htrans}", flush=True)
        else:
            print(f"  aucun produit plat dans [256,306] a transit <= {htrans}"
                  f" -- 307 tient", flush=True)
    print("Termine.", flush=True)


if __name__ == "__main__":
    main()
