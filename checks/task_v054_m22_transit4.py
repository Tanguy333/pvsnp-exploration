"""
TACHE V-054 -- d(22) : plus petit produit pur PLAT (height 1) de 22
facteurs (1-x^{t_i}), exposants NON-DECROISSANTS, transit transitoire <= 4.

Objectif : battre la borne TRIVIALE d(22) <= 473 (= champion m=21 de degre
294 multiplie par (1-x^179)), pour obtenir un vrai d(22) (~300-340 attendu).

Robustesse (verifie avant lancement) :
- MEMOIRE : pas de buffer de solutions. On suit le MINIMUM en scalaires
  (best_deg + best_exps de taille 22). poly = (23 x ubound) int8 ~ 11 Ko.
  Empreinte totale = runtime Numba ~0.11 Go, plate, quel que soit le transit.
  => aucun risque de debordement ni de troncature du champion.
- TEMPS : branch-and-bound. ubound = meilleure borne connue ; on elague
  toute branche dont le degre minimal atteignable (nd + reste*t, exposants
  non-decroissants donc chaque facteur restant >= t) est >= ubound. Chaque
  amelioration resserre l'arbre. Boucle externe sur t1 (premier facteur)
  avec coupe NFAC*t1 >= ubound, pour un progres affiche par t1.

Usage : python task_v054_m22_transit4.py [NFAC=22] [HTRANS=4] [INIT_UBOUND=474]
Ecrit le resultat dans checks/v054_result.txt a la fin.
"""
from __future__ import annotations

import sys
import time

import numpy as np
from numba import njit


@njit(cache=True)
def _search_t1(NFAC, HTRANS, t1, ubound):
    """Explore les produits a premier facteur = t1, exposants non-decroissants,
    degre < ubound, transit <= HTRANS. Branch-and-bound : best_deg resserre.
    Retourne (nodes, count_improv, best_deg, best_exps)."""
    DMAX = ubound + 1
    poly = np.zeros((NFAC + 1, DMAX), dtype=np.int8)
    poly[0, 0] = 1
    texp = np.zeros(NFAC + 1, dtype=np.int64)
    degs = np.zeros(NFAC + 1, dtype=np.int64)
    best_deg = ubound
    best_exps = np.zeros(NFAC, dtype=np.int64)
    nodes = 0
    count = 0

    d = 1
    texp[1] = t1 - 1          # sera incremente a t1
    while d >= 1:
        texp[d] += 1
        t = texp[d]
        nodes += 1
        if d == 1 and t > t1:        # niveau 1 fige a t1
            d -= 1
            continue
        reste = NFAC - d
        nd = degs[d - 1] + t
        # branch-and-bound : degre final >= nd + reste*t (facteurs restants >= t)
        if nd + reste * t >= best_deg:
            d -= 1
            continue
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
            count += 1
            best_deg = nd            # resserre la borne
            for j in range(NFAC):
                best_exps[j] = texp[j + 1]
            continue
        d += 1
        texp[d] = texp[d - 1] - 1
    return nodes, count, best_deg, best_exps


def verify_exact(exps):
    """Verification independante en entiers Python : height 1 + multiplicite."""
    f = [1]
    for t in exps:
        g = [0] * (len(f) + t)
        for i, c in enumerate(f):
            g[i] += c
            g[i + t] -= c
        f = g
    height = max(abs(c) for c in f)
    deg = len(f) - 1
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
    return height, deg, m


def main():
    NFAC = int(sys.argv[1]) if len(sys.argv) > 1 else 22
    HTRANS = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    init_ub = int(sys.argv[3]) if len(sys.argv) > 3 else 474
    t1_start = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    print(f"V-054 : d({NFAC}) -- transit <= {HTRANS}, borne initiale "
          f"ubound = {init_ub} (degre cible < {init_ub})"
          + (f"  [reprise a t1={t1_start}]" if t1_start > 1 else ""), flush=True)
    t0 = time.time()
    best = init_ub
    best_exps = None
    total_nodes = 0
    total_improv = 0
    t1 = t1_start - 1
    while True:
        t1 += 1
        if NFAC * t1 >= best:        # premier facteur t1 => degre >= NFAC*t1
            break
        nodes, improv, bdeg, bexps = _search_t1(NFAC, HTRANS, t1, best)
        total_nodes += nodes
        total_improv += improv
        msg = ""
        if bdeg < best:
            best = bdeg
            best_exps = [int(x) for x in bexps]
            msg = f"  <-- NOUVEAU champion degre {best}"
        print(f"  t1={t1:>3}: nodes={nodes:>13,d}  best={best}{msg}  "
              f"[{time.time()-t0:.0f}s cumule]", flush=True)

    dt = time.time() - t0
    print(f"\nTERMINE en {dt:.0f}s  ({total_nodes:,d} noeuds, "
          f"{total_improv} ameliorations)", flush=True)

    out_path = "v054_result.txt"
    with open(out_path, "w", encoding="utf-8") as fh:
        if best_exps is not None and best < init_ub:
            h, deg, mult = verify_exact(best_exps)
            ok = (h == 1 and mult == NFAC and deg == best)
            line = (f"d({NFAC}) <= {best}  (transit<={HTRANS})\n"
                    f"exposants = {best_exps}\n"
                    f"verif independante : height={h}, degre={deg}, "
                    f"multiplicite={mult}  -> {'OK' if ok else 'INCOHERENT'}\n"
                    f"noeuds={total_nodes}, temps={dt:.0f}s\n")
            print(line, flush=True)
            fh.write(line)
        else:
            line = (f"AUCUN produit plat {NFAC}-facteurs transit<={HTRANS} de "
                    f"degre < {init_ub}.\nLa borne triviale {init_ub-1} tient ; "
                    f"d({NFAC}) exige transit >= {HTRANS+1} ou degre >= {init_ub}.\n"
                    f"noeuds={total_nodes}, temps={dt:.0f}s\n")
            print(line, flush=True)
            fh.write(line)
    print(f"resultat ecrit dans checks/{out_path}", flush=True)


if __name__ == "__main__":
    main()
