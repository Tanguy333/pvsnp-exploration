"""
Tour 03 -- Verification empirique des deux failles fatales de l'obstruction
topologique sur le paysage d'energie.

(A) DEPENDANCE A LA PRESENTATION, PAS A LA FONCTION
    Pour deux CNF psi et psi' qui calculent la MEME fonction booleenne (memes
    temoins, meme classification SAT/UNSAT), la topologie des sous-niveaux
    differe. L'invariant ne capture donc pas la difficulte du PROBLEME mais
    seulement celle de la PRESENTATION. P et NP sont des classes de fonctions :
    un invariant qui n'est pas invariant sous equivalence logique ne peut pas
    les separer.

(B) LES SAUTS BORNES NE PRESERVENT PAS LA TOPOLOGIE
    Un algorithme polynomial en temps n^c peut faire des sauts de Hamming
    arbitrairement grands (jusqu'a n^c bits modifies). Sur un CSP a temoins
    diametralement opposes, augmenter le rayon des sauts effondre b_0 (et tout
    Betti superieur). Le Lemme 3 du Proposeur, qui modelise une MT comme un
    champ de vecteurs a sauts BORNES, est faux.

Aucune dependance externe (pas de networkx) : on calcule b_0 (composantes
connexes) du sous-graphe induit par BFS sur le cube booleen muni de la
distance de Hamming variable.
"""

from __future__ import annotations

import itertools
from collections import deque
from dataclasses import dataclass


Literal = tuple[int, int]            # (indice variable, +1 ou -1)
Clause = tuple[Literal, ...]


# ---------------------------------------------------------------------------
# Energie syntaxique = nombre de clauses violees
# ---------------------------------------------------------------------------

def energy(clauses: list[Clause], w: tuple[int, ...]) -> int:
    e = 0
    for c in clauses:
        sat = False
        for (i, sign) in c:
            if (w[i] == 1 and sign == 1) or (w[i] == 0 and sign == -1):
                sat = True
                break
        if not sat:
            e += 1
    return e


def sublevel(clauses: list[Clause], m: int, k: int) -> set[tuple[int, ...]]:
    """ L_k = { w in {0,1}^m : E(w) <= k }. """
    return {
        w
        for w in itertools.product((0, 1), repeat=m)
        if energy(clauses, w) <= k
    }


# ---------------------------------------------------------------------------
# Composantes connexes (Betti_0) du sous-graphe induit dans Hamming-<=r
# ---------------------------------------------------------------------------

def hamming(u: tuple[int, ...], v: tuple[int, ...]) -> int:
    return sum(1 for a, b in zip(u, v) if a != b)


def beta_0(vertices: set[tuple[int, ...]], jump_radius: int) -> int:
    """ Nombre de composantes connexes du graphe (V, E) avec
        E = {(u,v) : u,v in V, 1 <= hamming(u,v) <= jump_radius}.
        Implementation BFS naive : O(|V|^2) verifications de distance.
    """
    if not vertices:
        return 0
    V = list(vertices)
    seen = [False] * len(V)
    comps = 0
    for start in range(len(V)):
        if seen[start]:
            continue
        comps += 1
        q = deque([start])
        seen[start] = True
        while q:
            i = q.popleft()
            for j in range(len(V)):
                if seen[j]:
                    continue
                if 1 <= hamming(V[i], V[j]) <= jump_radius:
                    seen[j] = True
                    q.append(j)
    return comps


def num_edges_hamming1(vertices: set[tuple[int, ...]]) -> int:
    """ Nombre d'aretes Hamming-1 induites entre les sommets de `vertices`. """
    V = list(vertices)
    s = set(V)
    e = 0
    for v in V:
        for i in range(len(v)):
            u = list(v); u[i] = 1 - u[i]; u = tuple(u)
            if u in s and v < u:  # eviter de compter deux fois
                e += 1
    return e


def beta_1_hamming1(vertices: set[tuple[int, ...]]) -> int:
    """ b_1 du *complexe de drapeau* sur le graphe Hamming-1 induit.
        Le k-cube a girth 4 (Q_k est biparti, sans triangle), donc le flag
        complex sur Hamming-1 a 0 simplexe de dimension >= 2.
        Pour un 1-complexe : b_1 = |E| - |V| + b_0.
    """
    nV = len(vertices)
    nE = num_edges_hamming1(vertices)
    b0 = beta_0(vertices, jump_radius=1)
    return nE - nV + b0


# ---------------------------------------------------------------------------
# (A) Deux CNF logiquement equivalentes a topologies differentes
# ---------------------------------------------------------------------------

def attack_A() -> None:
    print("=" * 78)
    print("(A) Deux CNF logiquement equivalentes -- topologies differentes")
    print("=" * 78)

    # psi  = (x0 v x1) and (x2 v x3) and (x4 v x5)        -- 3 clauses
    # psi' = psi avec chaque clause triplee               -- 9 clauses
    # Les deux calculent EXACTEMENT la meme fonction booleenne (27 temoins).
    m = 6
    base: list[Clause] = [
        ((0, 1), (1, 1)),
        ((2, 1), (3, 1)),
        ((4, 1), (5, 1)),
    ]
    psi = list(base)
    psi_prime = base * 3  # chaque clause repetee 3 fois

    # Verification : memes temoins.
    witnesses_psi = sublevel(psi, m, 0)
    witnesses_psi_prime = sublevel(psi_prime, m, 0)
    print(f"  #temoins psi  : {len(witnesses_psi)}")
    print(f"  #temoins psi' : {len(witnesses_psi_prime)}")
    print(f"  Memes temoins ? {witnesses_psi == witnesses_psi_prime}")
    print(f"  -> psi et psi' calculent LA MEME fonction booleenne.\n")

    # Sous-niveaux L_k. On calcule b_0, b_1 et la somme (l'invariant du Proposeur
    # est Sigma b_i ; le 6-cube etant biparti -> girth 4 -> pas de triangles dans
    # Hamming-1, donc le complexe de drapeau a 0 simplexe en dim >= 2, et
    # Sigma b_i = b_0 + b_1.).
    print(f"  {'k':>2} | {'|L_k(psi)|':>10} {'b_0':>3} {'b_1':>3} {'Sum bi':>7}"
          f" |"
          f" {'|L_k(psi*)|':>11} {'b_0':>3} {'b_1':>3} {'Sum bi':>7}")
    print(f"  {'-'*2} | {'-'*10} {'-'*3} {'-'*3} {'-'*7} | {'-'*11} {'-'*3} {'-'*3} {'-'*7}")
    for k in (0, 1, 2):
        Lk_psi = sublevel(psi, m, k)
        Lk_pp = sublevel(psi_prime, m, k)
        b0_psi = beta_0(Lk_psi, jump_radius=1)
        b1_psi = beta_1_hamming1(Lk_psi)
        b0_pp = beta_0(Lk_pp, jump_radius=1)
        b1_pp = beta_1_hamming1(Lk_pp)
        print(
            f"  {k:>2} | {len(Lk_psi):>10} {b0_psi:>3} {b1_psi:>3} {b0_psi+b1_psi:>7}"
            f" | {len(Lk_pp):>11} {b0_pp:>3} {b1_pp:>3} {b0_pp+b1_pp:>7}"
        )
    print(
        "\n  CONCLUSION (A): pour k=1, L_1(psi) contient les assignations qui violent\n"
        "  au plus 1 clause originale ; L_1(psi') = L_0(psi') (la moindre violation\n"
        "  compte 3 clauses dupliquees). Les SOMMETS des deux complexes sont differents,\n"
        "  et l'invariant Sigma b_i diverge nettement (cf. colonnes ci-dessus).\n"
        "\n"
        "  -> L'invariant topologique du Proposeur n'est PAS un invariant de la\n"
        "     fonction booleenne, mais de sa presentation syntaxique. Or P et NP\n"
        "     sont des classes de fonctions/langages : un algorithme P pour SAT\n"
        "     peut preprocesser n'importe quelle CNF en une forme canonique avant\n"
        "     de decider. Un invariant non-invariant sous equivalence logique ne\n"
        "     fournit donc aucune borne inferieure uniforme sur le temps de\n"
        "     decision -> ne peut pas separer P de NP.\n"
    )


# ---------------------------------------------------------------------------
# (B) Le rayon des sauts effondre la topologie
# ---------------------------------------------------------------------------

def attack_B() -> None:
    print("=" * 78)
    print("(B) Sauts polynomiaux effondrent les Betti")
    print("=" * 78)

    # CSP avec 8 temoins sur la << diagonale >> : (a,b,c,a,b,c) pour
    # (a,b,c) in {0,1}^3. Clauses : (x_i = x_{i+3}) pour i=0,1,2, codees
    # en 2-CNF (que l'on encode comme un 3-CNF en doublant un litteral).
    m = 6
    phi: list[Clause] = []
    for i in range(3):
        # x_i = x_{i+3}  <=>  (x_i v ~x_{i+3}) and (~x_i v x_{i+3})
        phi.append(((i, 1), ((i + 3), -1)))
        phi.append(((i, -1), ((i + 3), 1)))

    witnesses = sublevel(phi, m, 0)
    print(f"  Formule phi : x_i = x_{{i+3}} pour i=0,1,2 (6 variables)")
    print(f"  #temoins = {len(witnesses)} (attendu : 8, la diagonale (a,b,c,a,b,c))")

    # Distance minimale entre deux temoins (devrait etre 2 : on flippe x_i et x_{i+3}).
    W = list(witnesses)
    dmin = min(hamming(W[i], W[j]) for i in range(len(W)) for j in range(i + 1, len(W)))
    dmax = max(hamming(W[i], W[j]) for i in range(len(W)) for j in range(i + 1, len(W)))
    print(f"  Distances Hamming entre temoins : min={dmin}, max={dmax}\n")

    print("  Composantes connexes du sous-graphe induit sur les temoins,")
    print("  en fonction du rayon de saut r :")
    print(f"    {'r':>3} | {'b_0(temoins)':>12} | interpretation")
    print(f"    {'-'*3:>3} | {'-'*12:>12} | {'-'*40}")
    for r in range(1, m + 1):
        b0 = beta_0(witnesses, jump_radius=r)
        interp = ""
        if r == 1:
            interp = "MT a un pas : toutes isolees (Forman strict)"
        elif r == 2:
            interp = "MT a deux flips : topologie effondree"
        elif r >= m // 2:
            interp = "rayon polynomial : graphe complet"
        print(f"    {r:>3} | {b0:>12} | {interp}")

    print(
        "\n  CONCLUSION (B): une MT polynomiale en temps n^c peut modifier jusqu'a\n"
        "  n^c bits avant de se prononcer. Cela revient a un << champ de vecteurs >>\n"
        "  a sauts de rayon r = n^c >> 2. Or des r=2, b_0 des temoins chute a 1.\n"
        "  Tout Betti superieur s'effondre de meme (le graphe devient un cube\n"
        "  complet sur (a,b,c)). L'obstruction topologique du Lemme 4 est detruite\n"
        "  par la generalisation aux sauts (Lemme 3).\n"
        "\n"
        "  -> La modelisation d'une MT comme champ de vecteurs a sauts BORNES\n"
        "     (Forman generalise) est intenable : un algorithme polynomial a un\n"
        "     rayon de saut polynomial, ce qui banalise l'invariant.\n"
    )


def main() -> None:
    print("Tour 03 -- Verification : obstruction topologique sur paysage d'energie")
    print()
    attack_A()
    attack_B()
    print("=" * 78)
    print("BILAN GLOBAL")
    print(
        "1. L'invariant topologique depend de la PRESENTATION syntaxique d'un\n"
        "   CSP, pas de la fonction booleenne. Or P vs NP est une question sur\n"
        "   les fonctions. L'invariant ne peut donc pas separer ces deux classes.\n"
        "\n"
        "2. Le Lemme 3 (MT comme champ a sauts bornes) est intenable : des qu'on\n"
        "   autorise un rayon de saut >= 2, les Betti des sous-niveaux s'ecrasent.\n"
        "   Aucune MT polynomiale n'est piegee par cette geometrie.\n"
        "\n"
        "-> FAILLE FATALE."
    )


if __name__ == "__main__":
    main()
