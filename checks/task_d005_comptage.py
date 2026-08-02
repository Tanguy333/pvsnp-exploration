"""
D-005, volet comptage — deux verifications :
  1. le motif max(W) = 2^{n-1}+1 au point n = 2 (exhaustif, 16 fonctions) ;
  2. l'argument de comptage de largeness : le nombre de fonctions separables
     a poids <= s est majore par
         C(s + 2^n - 1, 2^n - 1) * 2^{s+1}
     (choix du vecteur de coefficients a somme <= s, puis choix de la
     partition des <= s+1 valeurs distinctes possibles en valeurs-1 /
     valeurs-0). Quand cette borne est < 2^{2^n}/2, la MEDIANE de W depasse
     s — c'est l'argument « presque toutes les fonctions sont dures » de la
     largeness, a confronter aux medianes MESUREES (3 a n=3, 6 a n=4).
"""

from __future__ import annotations

import math
import sys

sys.path.insert(0, "checks")
from task_a013_cout_convention import termes_positifs, poids_min  # noqa: E402


def motif_n2():
    n, N = 2, 4
    tp = termes_positifs(n)
    dist = {}
    for m in range(1 << N):
        f = [(m >> e) & 1 for e in range(N)]
        if all(f) or not any(f):
            dist[0] = dist.get(0, 0) + 1
            continue
        w, _ = poids_min(f, tp, n, cap_max=10)
        dist[w] = dist.get(w, 0) + 1
    print("n=2 : distribution exacte :", dict(sorted(dist.items())))
    print(f"  max = {max(dist)} ; motif 2^(n-1)+1 = {2 ** (n - 1) + 1} "
          f"-> {'CONFORME' if max(dist) == 2 ** (n - 1) + 1 else 'CASSE'}")


def comptage():
    print("\nborne de comptage : #f avec W <= s "
          "<= C(s+2^n-1, 2^n-1) * 2^(s+1)")
    mesures = {3: 3, 4: 6}
    for n in (3, 4, 5, 6, 8, 10, 12):
        total = 2 ** (2 ** n)          # arithmetique entiere exacte
        smax = 0
        s = 1
        while True:
            borne = math.comb(s + 2 ** n - 1, 2 ** n - 1) * 2 ** (s + 1)
            if 2 * borne < total:
                smax = s
                s += 1
            else:
                break
        info = f" (mediane MESUREE : {mesures[n]})" if n in mesures else ""
        print(f"  n={n:2d} : mediane W > {smax} garanti par comptage{info}")


if __name__ == "__main__":
    motif_n2()
    comptage()
