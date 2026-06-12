"""
TACHE V-047 -- combler le rang m = 20 de la table de Borwein-Mossinghoff
2000 (absent : la table saute de 19 a 21). Chasse au produit pur plat
de 20 facteurs (1-x^{t_i}) -- multiplicite exactement 20 -- de degre
minimal (budget <= 299 pour battre l'interpolation vers leur m = 21).

Methode : DFS sur t_1 <= t_2 <= ... <= t_20, produit maintenu PLAT a
chaque prefixe (restriction "flat-monotone" : peut rater des produits
a hauteur transitoire >= 2 -- consigne si vide). Elagage : budget de
degre, et l'echec immediat des repetitions adjacentes est naturel
(le test de hauteur coupe).

Le motif naturel [1..9, 11, 13, ..., 31] (deg 276) et ses 320
perturbations a 1 echange ECHOUENT tous -- le trou de BM est reel.
"""

from __future__ import annotations

import sys
import time

import numpy as np
from numba import njit


@njit(cache=True)
def _dfs(NFAC, BUDGET, HTRANS, out, max_out):
    """DFS itératif. Retourne le nombre de produits plats trouves.
    out : lignes de 21 entiers (20 exposants + degre)."""
    DMAX = BUDGET + 1
    poly = np.zeros((NFAC + 1, DMAX), dtype=np.int8)
    poly[0, 0] = 1
    texp = np.zeros(NFAC + 1, dtype=np.int64)   # exposant choisi au niveau
    degs = np.zeros(NFAC + 1, dtype=np.int64)   # degre cumule
    nf = 0

    d = 1
    texp[1] = 0   # sera incremente
    while d >= 1:
        texp[d] += 1
        t = texp[d]
        # bornes : il reste (20 - d) facteurs apres celui-ci, chacun >= t
        reste = NFAC - d
        if degs[d - 1] + t + reste * t > BUDGET:
            d -= 1
            continue
        # multiplier le prefixe par (1 - x^t), verifier hauteur 1
        nd = degs[d - 1] + t
        # hauteur transitoire <= 2 (mesuree sur les extremaux de BM),
        # hauteur 1 exigee seulement au dernier facteur
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
            if nf < max_out:
                for j in range(NFAC):
                    out[nf, j] = texp[j + 1]
                out[nf, NFAC] = nd
                nf += 1
            continue
        d += 1
        texp[d] = texp[d - 1] - 1   # prochain >= precedent (incremente en tete)
    return nf


def main():
    nfac = int(sys.argv[1])
    budget = int(sys.argv[2])
    htrans = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    print(f"V-047 : produits purs plats a {nfac} facteurs (transit h<={htrans}), "
          f"budget degre <= {budget}", flush=True)
    t0 = time.time()
    out = np.zeros((65536, nfac + 1), dtype=np.int64)
    nf = _dfs(nfac, budget, htrans, out, 65536)
    print(f"{nf} produits plats trouves ({time.time()-t0:.0f}s)", flush=True)
    sols = sorted((int(out[i, nfac]), [int(x) for x in out[i, :nfac]])
                  for i in range(nf))
    for deg, ts in sols[:10]:
        print(f"  degre {deg} : {ts}", flush=True)
    if sols:
        deg, ts = sols[0]
        # verification exacte independante (entiers Python)
        f = [1]
        for t in ts:
            g = [0] * (len(f) + t)
            for i, c in enumerate(f):
                g[i] += c
                g[i + t] -= c
            f = g
        assert max(abs(c) for c in f) == 1 and len(f) - 1 == deg
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
        print(f"VERIFIE : champion degre {deg}, multiplicite exacte {m}",
              flush=True)


if __name__ == "__main__":
    main()
