"""
TACHE V-046 -- la courbe d(m) : span minimal d'un polynome hauteur 1
(coefficients -1,0,1) divisible par (1-x)^m, mesure par le reseau.

PRUDENCE DEFINITIONNELLE : nos cellules detectent les plats PARMI LES
MINIMA -- la valeur obtenue est une BORNE SUPERIEURE de d(m) (un plat
non minimal pourrait exister plus tot). Comparaison aux valeurs exactes
de Borwein-Mossinghoff 2000 (m <= 10) requise ; pour m = 11, 12 (BM :
symetrique seulement) nos bornes peuvent ameliorer l'etat de l'art.

Affinage : pour chaque m, scanner l'intervalle ouvert de la grille
V-042 jusqu'au premier n avec plat minimal. Sortie checks/v046_dm.csv.
"""

from __future__ import annotations

import os
import time

from task_v004_kv_conjecture5 import build_basis
from svp_turbo import turbo_lll, turbo_shortest

CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "v046_dm.csv")

# intervalles ouverts (d, n_sans_plat, n_avec_plat) d'apres V-042 + arbitrages
INTERVALLES = [
    (2, 4, 6), (3, 8, 11), (4, 12, 15), (5, 20, 24), (6, 26, 30),
    (7, 40, 44), (8, 44, 48), (9, 60, 70), (10, 60, 70),
    (11, 60, 136),
]


def cell(d, n):
    G = turbo_lll(build_basis(n, d))
    n2, sols = turbo_shortest(G)
    nf = sum(1 for v in sols
             if max(abs(int(t)) for t in v) == 1) // 2
    return n2, len(sols) // 2, nf


def main():
    fait = {}
    if os.path.exists(CSV):
        for ligne in open(CSV):
            p = ligne.strip().split(",")
            if p[0] != "d":
                fait[(int(p[0]), int(p[1]))] = int(p[3])
    else:
        with open(CSV, "w", encoding="utf-8") as f:
            f.write("d,n,min,plats,t\n")
    t0 = time.time()
    for (d, lo, hi) in INTERVALLES:
        premier = None
        for n in range(lo + 1, hi + 1):
            if (d, n) in fait:
                nf = fait[(d, n)]
            else:
                tC = time.time()
                n2, nm, nf = cell(d, n)
                with open(CSV, "a", encoding="utf-8") as f:
                    f.write(f"{d},{n},{n2},{nf},{time.time()-tC:.1f}\n")
                print(f"  (d={d}, n={n}) : min={n2}, plats={nf} "
                      f"({time.time()-tC:.0f}s)", flush=True)
            if nf > 0:
                premier = n
                break
        print(f"m = {d+1} : d({d+1}) <= {premier}  "
              f"(pas de plat minimal a n < {premier})", flush=True)
    print(f"Termine ({time.time()-t0:.0f}s).", flush=True)


if __name__ == "__main__":
    main()
