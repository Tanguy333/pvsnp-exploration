"""
TACHE V-045 -- cartographie de la famille des PRESQUE-IDEALES de
taille 14 : les palindromes plats de norme 28 du reseau d = 11
(degre 11 = multiplicite 12 : a UNE condition de l'ideale taille 14).

But constructif (question de Tanguy : « construisons un palindrome qui
verifie toutes les conditions ») : suivre la methode de Letac (taille
12 : la famille porte une courbe elliptique) -- enumerer la famille
compacte COMPLETE par le reseau, projeter chaque membre en carres
(demi-valeurs u_i : projection = taille 7 de degre 5 en carres),
mesurer l'ecart de la 6e condition, chercher la structure algebrique.

Tout membre de multiplicite 14 serait l'ideale taille 14 elle-meme
(impossible ici : span <= ~300 => hauteur <= 150 < 900 = zone CMSV
vide -- la valeur est la STRUCTURE de la famille, pas le jackpot).

Sortie : checks/v045_famille.csv (un membre par ligne, reprise par n).
"""

from __future__ import annotations

import os
import sys
import time

from task_v004_kv_conjecture5 import build_basis
from svp_turbo import turbo_lll, turbo_shortest

CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "v045_famille.csv")


def membres(n):
    """Tous les palindromes plats de norme 28 parmi les minima de (11, n)."""
    G = turbo_lll(build_basis(n, 11))
    # le temoin span-136 garantit min <= 28 pour n >= 136 : borne initiale
    n2, sols = turbo_shortest(G, borne_init=28)
    out = []
    if n2 != 28:
        return n2, out
    for v in sols:
        c = [int(t) for t in v]
        if next(t for t in c if t) < 0:
            continue
        if max(abs(t) for t in c) != 1:
            continue
        nz = [i for i, t in enumerate(c) if t]
        lo, hi = nz[0], nz[-1]
        if not all(c[lo + i] == c[hi - i] for i in range(hi - lo + 1)):
            continue
        A = [i for i, t in enumerate(c) if t > 0]
        B = [i for i, t in enumerate(c) if t < 0]
        out.append((A, B))
    return n2, out


def analyser(A, B):
    """Projection en carres et ecart de la 6e condition."""
    S = max(A + B)
    # centre : S/2 ou (S+min)/2 -- on centre sur le support
    lo = min(A + B)
    if (S + lo) % 2 != 0:
        return None  # centre non entier : demi-valeurs non entieres
    c = (S + lo) // 2
    # chaque demi-valeur apparait exactement deux fois (paires miroir,
    # centre jamais occupe pour une taille paire) : on dedouble
    ua = sorted(abs(x - c) for x in A)[::2]
    ub = sorted(abs(x - c) for x in B)[::2]
    al = [u * u for u in ua]
    be = [u * u for u in ub]
    degre = 0
    for j in range(1, 8):
        if sum(x ** j for x in al) == sum(x ** j for x in be):
            degre = j
        else:
            break
    ecart = sum(x ** (degre + 1) for x in al) - sum(x ** (degre + 1) for x in be)
    return ua, ub, degre, ecart


def main():
    n0, n1 = int(sys.argv[1]), int(sys.argv[2])
    fait = set()
    if os.path.exists(CSV):
        for ligne in open(CSV):
            p = ligne.split(";")
            if p[0] != "n":
                fait.add(int(p[0]))
    else:
        with open(CSV, "w", encoding="utf-8") as f:
            f.write("n;min;ua;ub;degre_carres;ecart_j_suivant\n")
    t0 = time.time()
    vus = set()   # dedoublonnage des decalages du meme objet
    for n in range(n0, n1 + 1):
        if n in fait:
            continue
        tC = time.time()
        n2, mem = membres(n)
        lignes = []
        for (A, B) in mem:
            r = analyser(A, B)
            if r is None:
                lignes.append(f"{n};{n2};CENTRE_NON_ENTIER;{A};{B};")
                continue
            ua, ub, degre, ecart = r
            cle = (tuple(ua), tuple(ub))
            if cle in vus:
                continue
            vus.add(cle)
            lignes.append(f"{n};{n2};{ua};{ub};{degre};{ecart}")
            print(f"(11,{n}) NOUVEAU membre : u_a={ua} u_b={ub} "
                  f"degre_carres={degre} ecart={ecart}", flush=True)
        if not mem:
            lignes.append(f"{n};{n2};;;;")
        with open(CSV, "a", encoding="utf-8") as f:
            f.write("\n".join(lignes) + "\n")
        print(f"  .. n={n} : min={n2}, {len(mem)} membre(s) "
              f"({time.time()-tC:.0f}s, total {time.time()-t0:.0f}s)",
              flush=True)
    print(f"Termine ({time.time()-t0:.0f}s).", flush=True)


if __name__ == "__main__":
    main()
