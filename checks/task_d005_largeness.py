"""
D-005 — L'AUTO-TEST RAZBOROV-RUDICH, volet mesure : la LARGENESS de la
propriete « W(f) >= s ».

Rattachement : Barriere preuves naturelles — l'approche testee est le
programme de mesure SYM-AND du depot lui-meme (18 taches, fil F-012..T27-S3).

RR 1997 : une propriete est LARGE si elle contient au moins une fraction
2^{-O(n)} des fonctions a n variables. Une preuve de borne inferieure est
« naturelle » si la propriete qu'elle utilise est constructive ET large — et
alors elle casse les PRG exponentiellement surs, donc est barree sous crypto
standard (pour les classes qui contiennent de tels PRG).

CE SCRIPT MESURE, exhaustivement :
  * n = 3 : distribution de W_pos sur les 256 fonctions (directe) ;
  * n = 4 : distribution de W_pos sur les 65 536 fonctions, calculee sur les
    1992 classes canoniques (S_4 x complementation de f) ponderees par la
    TAILLE D'ORBITE — c'est la distribution exacte, pas un echantillon.
Sortie : pour chaque seuil s, la fraction des fonctions avec W >= s — la
largeness EMPIRIQUE de chaque coupe de la propriete. Plus : mediane, max, et
la fraction au seuil « maximal » (les fonctions les plus dures).

Protocole : chaque optimum SAT re-verifie par enumeration independante
(fonctions heritees de task_a013_cout_convention). La ponderation par orbite
est verifiee par la somme (doit valoir exactement 2^{2^n}).
"""

from __future__ import annotations

import itertools
import sys
import time

sys.path.insert(0, "checks")
from task_a013_cout_convention import termes_positifs, poids_min  # noqa: E402


def canonique(masque, n):
    """Representant canonique sous permutation des variables ET
    complementation de f (les deux preservent W_pos... ATTENTION :
    la complementation de f preserve-t-elle W_pos ? La separation des
    ensembles de valeurs est symetrique en f/non-f, donc OUI."""
    N = 1 << n
    best = None
    for perm in itertools.permutations(range(n)):
        m = 0
        for e in range(N):
            img = 0
            for i in range(n):
                if (e >> i) & 1:
                    img |= 1 << perm[i]
            if (masque >> e) & 1:
                m |= 1 << img
        for cand in (m, (~m) & ((1 << N) - 1)):
            if best is None or cand < best:
                best = cand
    return best


def distribution(n, tl=60.0):
    N = 1 << n
    tp = termes_positifs(n)
    t0 = time.time()
    # classes et tailles d'orbite
    canon = {}
    for m in range(1 << N):
        c = canonique(m, n)
        canon.setdefault(c, 0)
        canon[c] += 1
    assert sum(canon.values()) == 1 << N, "ponderation cassee"
    print(f"n={n} : {1 << N} fonctions -> {len(canon)} classes "
          f"({time.time()-t0:.0f}s)", flush=True)
    # W par classe
    dist = {}   # W -> nombre de fonctions (pondere)
    nonconclu = 0
    for rep, taille in sorted(canon.items()):
        f = [(rep >> e) & 1 for e in range(N)]
        if all(f) or not any(f):
            dist[0] = dist.get(0, 0) + taille
            continue
        w, _ = poids_min(f, tp, n, cap_max=40, tl=tl)
        if w is None:
            nonconclu += taille
            continue
        dist[w] = dist.get(w, 0) + taille
    total = 1 << N
    print(f"  non conclus : {nonconclu}", flush=True)
    print(f"  distribution exacte de W_pos (ponderee par orbite) :",
          flush=True)
    cumul = 0
    for w in sorted(dist, reverse=True):
        cumul += dist[w]
        print(f"    W >= {w:2d} : {cumul:6d} fonctions "
              f"({100.0*cumul/total:6.2f} %)"
              + (f"   [exactement {w} : {dist[w]}]"), flush=True)
    # mediane
    acc = 0
    for w in sorted(dist):
        acc += dist[w]
        if acc >= total / 2:
            print(f"  mediane de W_pos : {w}", flush=True)
            break
    wmax = max(dist)
    print(f"  maximum : W = {wmax}, atteint par {dist[wmax]} fonctions "
          f"({100.0*dist[wmax]/total:.2f} %)", flush=True)
    return dist


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    for n in range(3, nmax + 1):
        distribution(n)
        print(flush=True)


if __name__ == "__main__":
    main()
