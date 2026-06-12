"""
TACHE V-042 -- recensement de symetrie des minima du reseau KV.

Fait elementaire : le renversement des coefficients f(x) -> x^n f(1/x)
est une isometrie de chaque cellule (d, n) qui preserve la multiplicite
en x = 1 ; l'ensemble des minima est donc stable par renversement et se
decompose en vecteurs AUTO-symetriques (palindromes : m pair ;
antipalindromes : m impair -- Lemme A de V-039) et en PAIRES
asymetriques {v, rev(v)}.

Observation a confirmer ou refuter (la "loi de symetrie des minima",
conjecture du depot, 39/39 jusqu'ici) : les minima du reseau KV sont
TOUJOURS auto-symetriques -- jamais de paire asymetrique.

Recensement : d = 2..11, ~120 cellules, classification de TOUS les
minima (plats ou non). Toute exception est imprimee avec son vecteur
et consignee. Sortie : checks/v042_census.csv (reprise par cellule).
"""

from __future__ import annotations

import os
import time

from task_v004_kv_conjecture5 import build_basis
from svp_turbo import turbo_lll, turbo_shortest

CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "v042_census.csv")

CELLES = []
for d, lo, hi, st in [(2, 4, 40, 2), (3, 5, 50, 3), (4, 6, 60, 3),
                      (5, 8, 70, 4), (6, 10, 90, 4), (7, 12, 100, 4),
                      (8, 14, 110, 6), (9, 20, 70, 10), (9, 75, 125, 5),
                      (10, 30, 100, 10), (10, 111, 141, 5),
                      (11, 20, 60, 10)]:
    for n in range(lo, hi + 1, st):
        if n > d + 1:
            CELLES.append((d, n))


def classifier(v):
    c = [int(t) for t in v]
    nz = [i for i, t in enumerate(c) if t]
    lo, hi = nz[0], nz[-1]
    pal = all(c[lo + i] == c[hi - i] for i in range(hi - lo + 1))
    apal = all(c[lo + i] == -c[hi - i] for i in range(hi - lo + 1))
    plat = max(abs(t) for t in c) == 1
    return pal, apal, plat


def main():
    fait = set()
    if os.path.exists(CSV):
        for ligne in open(CSV):
            p = ligne.split(",")
            if p[0] != "d":
                fait.add((int(p[0]), int(p[1])))
    else:
        with open(CSV, "w", encoding="utf-8") as f:
            f.write("d,n,min,nmin,pal,antipal,asym,plats,t\n")
    print(f"V-042 recensement : {len(CELLES)} cellules, "
          f"{len(fait)} deja faites", flush=True)
    t0 = time.time()
    nasym_tot = 0
    for (d, n) in CELLES:
        if (d, n) in fait:
            continue
        tC = time.time()
        G = turbo_lll(build_basis(n, d))
        n2, sols = turbo_shortest(G)
        npal = napal = nasym = nplats = 0
        asyms = []
        for v in sols:
            if next(t for t in v if t) < 0:
                continue  # un representant par signe
            pal, apal, plat = classifier(v)
            nplats += plat
            if pal:
                npal += 1
            elif apal:
                napal += 1
            else:
                nasym += 1
                asyms.append(v)
        dt = time.time() - tC
        with open(CSV, "a", encoding="utf-8") as f:
            f.write(f"{d},{n},{n2},{npal+napal+nasym},{npal},{napal},"
                    f"{nasym},{nplats},{dt:.1f}\n")
        tag = ""
        if nasym:
            nasym_tot += nasym
            tag = f"  <<<<< {nasym} MINIMUM(S) ASYMETRIQUE(S) !"
            print(f"(d={d}, n={n}) : min={n2}, {npal} pal + {napal} antipal"
                  f" + {nasym} ASYM{tag}", flush=True)
            for v in asyms[:3]:
                print(f"   asym : {[int(t) for t in v]}", flush=True)
        elif dt > 20 or n % 20 == 0:
            print(f"(d={d}, n={n}) : min={n2}, {npal} pal + {napal} antipal"
                  f", 0 asym   ({dt:.0f}s)", flush=True)
    print(f"RECENSEMENT TERMINE ({time.time()-t0:.0f}s) : "
          f"{nasym_tot} minima asymetriques au total.", flush=True)


if __name__ == "__main__":
    main()
