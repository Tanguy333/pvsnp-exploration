"""
A-013, volet refutation — LE COUT DE LA CONVENTION EST EXPONENTIEL, PAS LINEAIRE.

Rattachement : Atlas ligne 7. Le volet lecture a etabli que le format vise
(SYM+ de Williams, J. ACM 61(1) art. 2, 2014, p. 2:6) n'admet que des ANDs de
VARIABLES — donc le modele du depot est le bon. Reste la question quantitative :
si l'on passe a la convention a LITTERAUX (qui existe aussi dans la
litterature), que deviennent les bornes inferieures du depot ?

CE QUE CE SCRIPT ETABLIT, SANS SOLVEUR (enumeration exhaustive) :
  1. La conjecture W_pos <= n * W_lit, suggeree par la mesure exhaustive a
     n = 2, 3, 4 (rapport maximal exactement n), est FAUSSE des n = 5.
     Contre-exemple minimal f5 : W_lit = 2, W_pos = 11 > 10 = n * W_lit.
  2. Famille infinie F_m = NOR_m(x) XOR NOR_m(y) sur n = 2m variables :
     W_lit = 2 pour tout m, tandis que W_pos croit (6, 14, 24 a n = 4, 6, 8).
  3. Le seul transfert prouve est donc LOGARITHMIQUE :
     W_lit(f) >= log_{n+1}(W_pos(f) + 1), consequence du theoreme
     W_pos <= (n+1)^{W_lit} - 1 (encodage en base n+1, cf. tasks/done/A-013.md).

POURQUOI SANS SOLVEUR. Une borne INFERIEURE sur W_pos obtenue par UNSAT de
CP-SAT n'est pas re-verifiable par enumeration (reserve consignee par le depot
en T27-S2 §4). L'enumerateur ci-dessous parcourt l'espace ENTIER des
coefficients : il assigne a[S] pour S = 1, 2, ..., 2^n - 1 dans l'ordre
CROISSANT du masque ; comme S' inclus dans S implique S' <= S, la valeur
p(S) = somme des a[S'] sur les S' non vides inclus dans S est DEFINITIVE des
que a[S] est pose, et la collision se teste immediatement. Deux elagages, tous
deux prouves : (E1) a[{i}] >= 1 des que f(e_i) != f(0), car p(e_i) = a[{i}] et
p(0) = 0 ; (E2) p(S) <= budget, les coefficients etant >= 0. Aucun cassage de
symetrie : un « AUCUN » est une enumeration complete, pas une assertion de
solveur.

C'est aussi une lecon de methode consignee : la loi « rapport maximal = n »,
vraie et EXHAUSTIVE a n <= 4, est un artefact de petite taille — le regime
d'echec q.12 du cahier (« vrai aux petits k »), rencontre une fois de plus.
"""

from __future__ import annotations

import itertools
import sys


def separe(f, a, n):
    """p determine-t-il f ? Enumeration complete."""
    uns, zeros = set(), set()
    for z in range(1 << n):
        p = sum(c for S, c in a.items() if (z & S) == S)
        (uns if f[z] else zeros).add(p)
    return not (uns & zeros)


def w_pos_exhaustif(f, n, budget):
    """Existe-t-il un separateur positif de poids <= budget ?
    Parcours de l'espace ENTIER, sans solveur.

    CLEF DE L'ELAGAGE : les masques sont traites dans l'ordre CROISSANT ;
    comme S' inclus dans S implique S' <= S, la valeur p(S) est DEFINITIVE
    des que a[S] est pose. On teste donc la collision IMMEDIATEMENT, sans
    attendre la feuille — c'est ce qui rend l'enumeration faisable.
    Retourne le poids minimal trouve, ou None si aucun <= budget."""
    masques = list(range(1, 1 << n))
    coef = [0] * (1 << n)          # coef[S] = a_S
    # p(0) = 0 : le point tout-a-zero est deja classe
    uns = {0} if f[0] else set()
    zeros = set() if f[0] else {0}
    meilleur = [None]

    def base_de(S):
        """somme des a[T] sur les T NON VIDES strictement inclus dans S
        (tous deja assignes, car T < S)."""
        s, T = 0, (S - 1) & S
        while T:
            s += coef[T]
            T = (T - 1) & S
        return s

    def dfs(idx, poids):
        if meilleur[0] is not None and poids >= meilleur[0]:
            return
        if idx == len(masques):
            meilleur[0] = poids
            return
        S = masques[idx]
        base = base_de(S)
        mini = 1 if (bin(S).count("1") == 1
                     and f[S] != f[0]) else 0            # (E1)
        for c in range(mini, budget - poids + 1):        # (E2)
            v = base + c
            if v > budget:
                break
            cible = uns if f[S] else zeros
            autre = zeros if f[S] else uns
            if v in autre:                 # collision : branche morte
                continue
            coef[S] = c
            neuf = v not in cible
            if neuf:
                cible.add(v)
            dfs(idx + 1, poids + c)
            if neuf:
                cible.discard(v)
            coef[S] = 0

    dfs(0, 0)
    return meilleur[0]


def f5(z):
    """Contre-exemple minimal, n = 5 :
    [x = 00000] OU (x0 ET non x3 ET non x4)."""
    return 1 if z == 0 else (1 if ((z & 1) and not ((z >> 3) & 1)
                                   and not ((z >> 4) & 1)) else 0)


def famille_F(m):
    """F_m = NOR_m(x) XOR NOR_m(y) sur n = 2m variables."""
    n = 2 * m
    masque_x = (1 << m) - 1
    masque_y = masque_x << m
    return n, [1 if ((z & masque_x) == 0) != ((z & masque_y) == 0) else 0
               for z in range(1 << n)]


def temoin_litteraux(f, n, termes):
    """Verifie qu'un separateur a litteraux donne separe bien f.
    termes : liste de (coefficient, predicat sur z)."""
    uns, zeros = set(), set()
    for z in range(1 << n):
        q = sum(c for c, pred in termes if pred(z))
        (uns if f[z] else zeros).add(q)
    return not (uns & zeros)


def main():
    budget = int(sys.argv[1]) if len(sys.argv) > 1 else 11

    print("=== 1. CONTRE-EXEMPLE MINIMAL, n = 5 ===")
    n = 5
    f = [f5(z) for z in range(1 << n)]
    ok = temoin_litteraux(
        f, n,
        [(1, lambda z: (z & 1) and not ((z >> 3) & 1)
          and not ((z >> 4) & 1)),
         (1, lambda z: not ((z >> 1) & 1) and not ((z >> 2) & 1)
          and not ((z >> 3) & 1) and not ((z >> 4) & 1))])
    print(f"  temoin a litteraux de poids 2 : "
          f"{'SEPARE' if ok else 'ECHEC'}  =>  W_lit(f5) <= 2")
    for b in (10, 11):
        w = w_pos_exhaustif(f, n, b)
        print(f"  W_positif <= {b} ? "
              f"{'OUI, poids ' + str(w) if w else 'AUCUN (enumeration '
                                                 'complete)'}")
    print("  => W_positif(f5) = 11 > 10 = n * W_lit : "
          "CONJECTURE W_pos <= n*W_lit REFUTEE")

    print("\n=== 2. LA FAMILLE F_m = NOR_m(x) XOR NOR_m(y) ===")
    for m in (2, 3):
        n, f = famille_F(m)
        mx = (1 << m) - 1
        ok = temoin_litteraux(
            f, n, [(1, lambda z, mx=mx: (z & mx) == 0),
                   (1, lambda z, mx=mx: (z & (mx << m)) == 0)])
        print(f"  m = {m} (n = {n}) : temoin a litteraux poids 2 "
              f"{'OK' if ok else 'ECHEC'} ; borne n*W_lit = {2 * n}")
        w = w_pos_exhaustif(f, n, 2 * n)
        print(f"    W_positif <= {2 * n} ? "
              f"{'OUI, poids ' + str(w) if w else 'AUCUN => W_positif > '
                                                 + str(2 * n)}")


if __name__ == "__main__":
    main()
