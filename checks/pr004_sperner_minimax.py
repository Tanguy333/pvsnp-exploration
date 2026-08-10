# -*- coding: utf-8 -*-
r"""PR-004 — Contre-vérification exécutable de la candidature TFNP :
complexité de requête déterministe EXACTE de SPERNER (minimax).

Implémentation INDÉPENDANTE du Réfuteur (le sous-lemme de la
candidature est rejoué avec un instrument écrit séparément).

Jeu : le requêteur interroge un sommet non connu ; l'adversaire répond
une couleur du DOMAINE du sommet (bords contraints, intérieur libre —
toute affectation respectant les domaines est une entrée Sperner
valide, donc l'adversaire n'a aucune contrainte globale). Le requêteur
gagne quand un petit simplexe entièrement interrogé est trichrome
(2D) / un segment bicolore (1D). Valeur = minimax mémoïsé exact.

Calibration (a) : SPERNER-1D, chemin de N segments, v0 = 0, vN = 1,
internes ∈ {0,1} — attendu ⌈log₂ N⌉ (dichotomie optimale).
Résistance (b) : SPERNER-2D, triangle de côté k, coins 0/1/2, bords
bicolores, intérieur libre — attendu : strictement au-dessus de
log₂(k²) et croissance ~linéaire en k.
"""
from __future__ import annotations

import math
import sys
import time
from functools import lru_cache


def minimax_generique(domaines, gagnants):
    """domaines : liste des couleurs possibles par sommet (None-index
    = inconnu au depart, singleton = fixe/connu) ; gagnants : liste de
    tuples d'indices (le requeteur gagne si l'un est entierement connu
    et 'valide' au sens du predicat associe). Ici : gagnants = liste
    de (indices, ensemble_de_couleurs_exigees). Rend le nombre minimal
    de requetes garanties."""
    n = len(domaines)
    fixes = tuple(d[0] if len(d) == 1 else None for d in domaines)

    def gagne(etat):
        for (idx, cible) in gagnants:
            cols = [etat[i] for i in idx]
            if all(c is not None for c in cols) and set(cols) == cible:
                return True
        return False

    from functools import lru_cache

    @lru_cache(maxsize=None)
    def valeur(etat):
        if gagne(etat):
            return 0
        meilleurs = None
        inconnus = [i for i in range(n) if etat[i] is None]
        # heuristique d'ordre : sommets touchant le plus de gagnants
        # presque complets d'abord (aide l'elagage)
        def score(i):
            s = 0
            for (idx, _) in gagnants:
                if i in idx:
                    s += sum(1 for j in idx if etat[j] is not None)
            return -s
        inconnus.sort(key=score)
        for i in inconnus:
            pire = 0
            for c in domaines[i]:
                e2 = list(etat)
                e2[i] = c
                v = valeur(tuple(e2))
                if v > pire:
                    pire = v
                if meilleurs is not None and pire + 1 >= meilleurs:
                    break  # elagage : cette requete ne battra pas le mieux
            cand = 1 + pire
            if meilleurs is None or cand < meilleurs:
                meilleurs = cand
                if meilleurs == 1:
                    break
        return meilleurs

    etat0 = fixes
    v = valeur(etat0)
    valeur.cache_clear()
    return v


def sperner_1d(N):
    domaines = [[0]] + [[0, 1] for _ in range(N - 1)] + [[1]]
    gagnants = [((i, i + 1), {0, 1}) for i in range(N)]
    return minimax_generique(domaines, gagnants)


def sperner_2d(k):
    sommets = [(x, y) for x in range(k + 1) for y in range(k + 1 - x)]
    ix = {v: i for i, v in enumerate(sommets)}
    domaines = []
    for (x, y) in sommets:
        if (x, y) == (0, 0):
            domaines.append([0])
        elif (x, y) == (k, 0):
            domaines.append([1])
        elif (x, y) == (0, k):
            domaines.append([2])
        elif y == 0:
            domaines.append([0, 1])
        elif x == 0:
            domaines.append([0, 2])
        elif x + y == k:
            domaines.append([1, 2])
        else:
            domaines.append([0, 1, 2])
    gagnants = []
    for x in range(k):
        for y in range(k - x):
            gagnants.append(((ix[(x, y)], ix[(x + 1, y)], ix[(x, y + 1)]),
                             {0, 1, 2}))
    for x in range(k - 1):
        for y in range(k - 1 - x):
            gagnants.append(((ix[(x + 1, y)], ix[(x, y + 1)],
                              ix[(x + 1, y + 1)]), {0, 1, 2}))
    nb_tri = len(gagnants)
    nb_col = 1
    for d in domaines:
        nb_col *= len(d)
    return minimax_generique(domaines, gagnants), nb_tri, nb_col


if __name__ == "__main__":
    quel = sys.argv[1] if len(sys.argv) > 1 else "tout"
    if quel in ("tout", "1d"):
        print("=== CALIBRATION 1D (attendu : ceil(log2 N)) ===")
        for N in (4, 8, 16):
            t0 = time.time()
            v = sperner_1d(N)
            att = math.ceil(math.log2(N))
            print(f"  N = {N:2} : requetes exactes = {v}   "
                  f"(attendu {att} : {'CONFORME' if v == att else 'ECART'})"
                  f"  [{time.time() - t0:.0f}s]")
    if quel in ("tout", "2d"):
        print("=== RESISTANCE 2D (attendu : > log2(k^2), ~lineaire) ===")
        for k in (2, 3, 4):
            t0 = time.time()
            v, nb_tri, nb_col = sperner_2d(k)
            lg = math.log2(nb_tri)
            print(f"  k = {k} : requetes exactes = {v}   "
                  f"(#triangles = {nb_tri}, log2 = {lg:.2f} ; "
                  f"#colorations = {nb_col})"
                  f"  [{time.time() - t0:.0f}s]")
