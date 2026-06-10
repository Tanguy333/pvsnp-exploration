"""
TACHE V-006 -- Symetries du reseau de KV et REFORMULATION de la
Conjecture 5.

LEMME S (decalage). Si gamma in L(B_{n,d}) et gamma_i = 0 pour i < k,
alors le decale a gauche gamma' (gamma'_i = gamma_{i+k}) est dans L.
  Preuve : gamma = sum a_j col_j ; B triangulaire inferieure a diagonale
  C(d+1,0) = 1, donc a_j = 0 pour j < k ; gamma' = sum a_{j+k} col_j. QED

LEMME R (renversement). R(gamma)_i := gamma_{n-i} preserve L.
  Preuve : R(col_k) = (-1)^{d+1} col_{n-d-1-k} (le gabarit binomial
  alternant est (anti)symetrique). QED

THEOREME (reformulation). Les enonces suivants sont equivalents :
  (a) [Conjecture 5 de KV] il existe un plus court vecteur avec
      gamma_n = 1 ;
  (b) il existe un plus court vecteur dont la PREMIERE coordonnee non
      nulle vaut +-1 ;
  (c) il existe un plus court vecteur dont le premier coefficient de
      reseau non nul vaut +-1 (par triangularite, gamma_{k0} = a_{k0}).
  Preuve : (b) => (a) : decaler a gauche (Lemme S) pour amener la
  premiere coordonnee en position 0, renverser (Lemme R) -- elle devient
  gamma_n = +-1, negation si besoin. (a) => (b) : renverser. (b) <=> (c)
  par triangularite. QED

La Conjecture 5 devient un enonce sur le COEFFICIENT DOMINANT des plus
courts vecteurs -- prise potentielle pour une preuve (type reduction de
taille / LLL sur a_0).

Ce script :
  [1] verifie S et R numeriquement (vecteurs de reseau aleatoires) ;
  [2] teste la version FORTE sur la grille n = 6..20 : TOUS les minima
      ont-ils leur premiere coordonnee non nulle en +-1 ?
      (si oui : la conjecture suivrait de N'IMPORTE QUEL plus court
       vecteur -- prise maximale.)
"""

from __future__ import annotations

import random

import numpy as np

from task_v004_kv_conjecture5 import build_basis, lll_reduce, shortest_vectors

random.seed(2026)


def in_lattice(G, v):
    """ v dans L(lignes de G) ? Resolution triangulaire sur la base
        canonique (les gabarits build_basis, triangulaires). """
    v = [int(x) for x in v]
    m = len(G)
    a = []
    rest = list(v)
    for k in range(m):
        a_k = rest[k]  # diagonale = 1
        a.append(a_k)
        for i in range(len(rest)):
            rest[i] -= a_k * int(G[k][i])
    return all(x == 0 for x in rest)


def check_lemmas(trials=300):
    okS = okR = True
    for _ in range(trials):
        n = random.randint(6, 14)
        d = random.randint(1, min(6, n - 3))
        G0 = build_basis(n, d)
        m = len(G0)
        a = [random.randint(-3, 3) for _ in range(m)]
        gamma = [sum(a[k] * int(G0[k][i]) for k in range(m))
                 for i in range(n + 1)]
        # Lemme R
        rev = gamma[::-1]
        okR &= in_lattice(G0, rev)
        # Lemme S : forcer un prefixe nul
        k0 = random.randint(0, m - 1)
        for j in range(k0):
            a[j] = 0
        gamma = [sum(a[k] * int(G0[k][i]) for k in range(m))
                 for i in range(n + 1)]
        shifted = gamma[k0:] + [0] * k0
        okS &= in_lattice(G0, shifted)
    return okS, okR


def first_nonzero(v):
    for x in v:
        if int(x) != 0:
            return int(x)
    return 0


def main() -> None:
    print("TACHE V-006 -- symetries du reseau KV + reformulation Conj. 5")
    print("=" * 68)

    print("\n[1] Lemmes S (decalage) et R (renversement), 300 tests :")
    okS, okR = check_lemmas()
    print(f"    S : {'OK' if okS else 'ECHEC'} ; R : {'OK' if okR else 'ECHEC'}")

    print("\n[2] Version FORTE : tous les minima ont-ils |1re coord. != 0| = 1 ?")
    all_strong = True
    weak_cells = []
    for n in range(6, 21):
        for d in range(1, min(9, n - 3) + 1):
            G = lll_reduce(build_basis(n, d))
            n2, sols = shortest_vectors(G)
            firsts = sorted({abs(first_nonzero(v)) for v in sols})
            strong = firsts == [1]
            all_strong &= strong
            if not strong:
                weak_cells.append((n, d, firsts))
    if all_strong:
        print("    OUI -- sur TOUTE la grille (n = 6..20, d <= 9), chaque")
        print("    plus court vecteur a sa premiere coordonnee non nulle")
        print("    en +-1.")
        print("\n    => via le Theoreme de reformulation, la Conjecture 5")
        print("       suivrait de n'importe quel argument montrant qu'UN")
        print("       plus court vecteur a un coefficient dominant +-1 --")
        print("       et empiriquement, TOUS l'ont. Prise maximale.")
    else:
        print(f"    NON -- cellules faibles : {weak_cells[:10]}")
        print("    (la version (b) a existence reste verifiee via V-004/5)")


if __name__ == "__main__":
    main()
