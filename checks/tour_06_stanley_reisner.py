"""
Tour 06 -- Refutation des Lemmes 1 et 2 du Proposeur, par enumeration des
168 fonctions monotones sur n=4 variables (nombre de Dedekind M(4) = 168)
et calcul direct du contre-exemple C_4 que je decele a priori.

Lemmes attaques :

  L1 : << La taille minimale d'un circuit Sigma Pi monotone de fan-in k
        calculant f est exactement egale a la taille minimale d'un
        recouvrement du complexe Delta_f par des simplexes de dimension
        <= k-1. >>

  L2 : << Si b_i(Delta_f) > 0 pour un certain i, alors tout recouvrement
        par des simplexes de dimension < i necessite une redondance
        (nombre de simplexes strictement superieur au nombre de faces
        maximales de Delta_f). >>

Approche :

  Pour une fonction monotone f sur [n], on definit :
    - Delta_f = { S subset [n] : f(chi_S) = 0 } (complexe simplicial,
      complexe de Stanley-Reisner de l'ideal monomial squarefree engendre
      par les implicants premiers de f).
    - Implicants premiers de f = elements minimaux de { S : f(chi_S) = 1 }.
    - Taille du circuit Sigma Pi monotone fan-in k =
        si max |T_j| > k : non-realisable (taille = infty) ;
        sinon : nombre d'implicants premiers (representation canonique).

  Le contre-exemple cible : Delta_f = complexe de drapeau du 4-cycle C_4.
    - Sommets {1, 2, 3, 4}.
    - Aretes {1,2}, {2,3}, {3,4}, {1,4}.
    - Pas de 2-simplexes.
    - b_0 = 1 (connecte), b_1 = 1 (cycle non remplie).
  Implicants premiers de f = {1,3} et {2,4} (les diagonales manquantes
  comme non-faces minimales).
  Donc f(x_1, x_2, x_3, x_4) = (x_1 AND x_3) OR (x_2 AND x_4).
  Circuit Sigma Pi monotone fan-in 2 : taille = 2 (deux monomes).
  Faces maximales de Delta_f : les 4 aretes du cycle.
  Le Lemme 2 predirait : taille > 4. Or taille = 2 < 4. Contradiction.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass

import numpy as np


# ---------------------------------------------------------------------------
# Enumeration des fonctions monotones sur n variables.
# ---------------------------------------------------------------------------

def is_subset_mask(y: int, x: int) -> bool:
    """ y subset de x (vus comme masques de bits) ssi y AND x = y. """
    return (y & x) == y


def is_monotone(mask: int, n: int) -> bool:
    """ mask encode f : bit x est mis ssi f(chi_S(x)) = 1.
        f monotone : pour tout x ayant f(x)=1, tous les y >= x (super-ensembles)
        verifient f(y)=1.
    """
    N = 1 << n
    for x in range(N):
        if (mask >> x) & 1:
            for i in range(n):
                if not ((x >> i) & 1):
                    y = x | (1 << i)
                    if not ((mask >> y) & 1):
                        return False
    return True


def all_monotone_functions(n: int) -> list[int]:
    """ Renvoie la liste des masques codant les fonctions monotones sur n vars.
        Pour n=4, devrait renvoyer 168 fonctions (Dedekind M(4) = 168).
    """
    N = 1 << n
    return [m for m in range(1 << N) if is_monotone(m, n)]


# ---------------------------------------------------------------------------
# Complexe simplicial Delta_f et nombres de Betti.
# ---------------------------------------------------------------------------

def faces_of_delta(mask: int, n: int) -> list[frozenset[int]]:
    """ Delta_f = { S subset [n] : f(chi_S) = 0 } code par mask. """
    N = 1 << n
    return [
        frozenset(i for i in range(n) if (x >> i) & 1)
        for x in range(N)
        if not ((mask >> x) & 1)
    ]


def maximal_faces(faces: list[frozenset[int]]) -> list[frozenset[int]]:
    """ Faces maximales (pour l'inclusion). """
    fs = sorted(faces, key=lambda s: -len(s))
    maximal = []
    for f in fs:
        if not any(f < g for g in maximal):
            maximal.append(f)
    return maximal


def betti_numbers(faces: list[frozenset[int]], n: int) -> list[int]:
    """ Calcule b_0, b_1, ..., b_{n-1} sur Q via les matrices de bord. """
    by_dim: dict[int, list[frozenset[int]]] = {}
    for f in faces:
        d = len(f) - 1
        by_dim.setdefault(d, []).append(f)
    if not by_dim:
        return [0] * n
    max_dim = max(by_dim.keys())

    def boundary(d: int) -> np.ndarray:
        """ Matrice de partial_d : C_d -> C_{d-1}, indexee par les faces. """
        if d <= 0 or d not in by_dim or d - 1 not in by_dim:
            return np.zeros((0, 0))
        rows = by_dim[d - 1]
        cols = by_dim[d]
        idx = {f: i for i, f in enumerate(rows)}
        M = np.zeros((len(rows), len(cols)), dtype=np.int64)
        for j, sigma in enumerate(cols):
            sigma_list = sorted(sigma)
            for i_v, v in enumerate(sigma_list):
                tau = frozenset(sigma_list[:i_v] + sigma_list[i_v + 1 :])
                if tau in idx:
                    M[idx[tau], j] = (-1) ** i_v
        return M

    betti = []
    for k in range(n + 1):
        n_k = len(by_dim.get(k, []))
        if k == -1 or n_k == 0:
            betti.append(0)
            continue
        # ker(partial_k) : pour k = 0 on prend ker = tout (partial_0 = 0).
        if k == 0:
            null_k = n_k
        else:
            Mk = boundary(k)
            if Mk.size == 0:
                null_k = n_k
            else:
                rank_k = int(np.linalg.matrix_rank(Mk.astype(float)))
                null_k = n_k - rank_k
        # im(partial_{k+1}) :
        Mk1 = boundary(k + 1)
        if Mk1.size == 0:
            rank_k1 = 0
        else:
            rank_k1 = int(np.linalg.matrix_rank(Mk1.astype(float)))
        betti.append(null_k - rank_k1)
    # Tronquer aux dimensions effectivement presentes.
    while len(betti) > 1 and betti[-1] == 0:
        betti.pop()
    return betti


# ---------------------------------------------------------------------------
# Implicants premiers et taille de circuit Sigma Pi monotone.
# ---------------------------------------------------------------------------

def prime_implicants(mask: int, n: int) -> list[frozenset[int]]:
    """ Elements minimaux pour l'inclusion de T_f = {S : f(chi_S) = 1}. """
    N = 1 << n
    T = [x for x in range(N) if (mask >> x) & 1]
    pi: list[frozenset[int]] = []
    for x in T:
        is_min = True
        for y in T:
            if y != x and is_subset_mask(y, x):
                is_min = False
                break
        if is_min:
            pi.append(frozenset(i for i in range(n) if (x >> i) & 1))
    return pi


# ---------------------------------------------------------------------------
# Demonstration explicite du contre-exemple C_4
# ---------------------------------------------------------------------------

def demo_C4_counterexample(n: int = 4) -> None:
    print("=" * 78)
    print("Contre-exemple explicite : f = (x_0 AND x_2) OR (x_1 AND x_3)")
    print("Delta_f = complexe de drapeau du 4-cycle C_4")
    print("=" * 78)

    # Fonction f : f(chi_S) = 1 ssi {0,2} subset S ou {1,3} subset S.
    N = 1 << n
    mask = 0
    for x in range(N):
        S = frozenset(i for i in range(n) if (x >> i) & 1)
        if {0, 2} <= set(S) or {1, 3} <= set(S):
            mask |= 1 << x

    assert is_monotone(mask, n), "f doit etre monotone"

    delta = faces_of_delta(mask, n)
    print(f"  Faces de Delta_f ({len(delta)} au total) : ")
    by_size = {}
    for f in delta:
        by_size.setdefault(len(f), []).append(f)
    for d in sorted(by_size):
        items = ", ".join("{" + ",".join(map(str, sorted(s))) + "}" if s else "∅"
                          for s in sorted(by_size[d], key=lambda x: sorted(x)))
        print(f"    dim {d-1}: {items}")

    maxf = maximal_faces(delta)
    print(f"\n  Faces maximales (au sens de l'inclusion) : {len(maxf)}")
    for f in sorted(maxf, key=lambda x: sorted(x)):
        print(f"    {{{','.join(map(str, sorted(f)))}}}")

    pi = prime_implicants(mask, n)
    print(f"\n  Implicants premiers : {len(pi)}")
    for p in sorted(pi, key=lambda x: sorted(x)):
        print(f"    {{{','.join(map(str, sorted(p)))}}}")

    max_pi_size = max(len(p) for p in pi)
    print(f"\n  Max taille d'implicant premier (= fan-in necessaire) : {max_pi_size}")
    print(f"  Taille Sigma Pi monotone fan-in 2 : {len(pi)}")

    betti = betti_numbers(delta, n)
    print(f"\n  Nombres de Betti de Delta_f : {betti}")

    print()
    print(">>> Comparaison avec le Lemme 2 du Proposeur :")
    print(f"    b_1(Delta_f) = {betti[1] if len(betti) > 1 else 0}")
    print(f"    Faces maximales de Delta_f : {len(maxf)}")
    print(f"    Taille du circuit (= #implicants premiers) : {len(pi)}")
    print()
    if (len(betti) > 1 and betti[1] > 0) and len(pi) <= len(maxf):
        print("    Le Lemme 2 predit : taille > #faces maximales (= {}).".format(len(maxf)))
        print("    Realite           : taille = {} <= {} faces maximales.".format(len(pi), len(maxf)))
        print("    -> Lemme 2 REFUTE par contre-exemple direct.")
    else:
        print("    Le Lemme 2 est compatible avec ce cas.")


# ---------------------------------------------------------------------------
# Enumeration exhaustive : 168 fonctions monotones sur n=4
# ---------------------------------------------------------------------------

@dataclass
class Stats:
    mask: int
    betti: list[int]
    n_prime_implicants: int
    max_prime_size: int
    n_max_faces: int


def enumerate_n4() -> list[Stats]:
    n = 4
    monotone = all_monotone_functions(n)
    print(f"  Nombre de fonctions monotones sur n=4 : {len(monotone)} (attendu : 168)")
    stats = []
    for mask in monotone:
        delta = faces_of_delta(mask, n)
        b = betti_numbers(delta, n)
        pi = prime_implicants(mask, n)
        n_pi = len(pi)
        max_pi_size = max((len(p) for p in pi), default=0)
        n_mf = len(maximal_faces(delta))
        stats.append(Stats(mask, b, n_pi, max_pi_size, n_mf))
    return stats


def analyse_lemme_2(stats: list[Stats]) -> None:
    print()
    print("=" * 78)
    print("Verification massive du Lemme 2 sur les 168 fonctions monotones de n=4")
    print("=" * 78)
    n_violations = 0
    n_b1_positive = 0
    examples_violation = []
    for s in stats:
        b1 = s.betti[1] if len(s.betti) > 1 else 0
        if b1 > 0:
            n_b1_positive += 1
            if s.n_prime_implicants <= s.n_max_faces:
                n_violations += 1
                if len(examples_violation) < 5:
                    examples_violation.append(s)

    print(f"  Fonctions avec b_1(Delta_f) > 0     : {n_b1_positive}")
    print(f"  ...dont taille <= #faces maximales  : {n_violations}")
    print(f"  -> Lemme 2 viole {n_violations} fois (sur {n_b1_positive} cas ou il devrait s'appliquer).")
    print()
    if examples_violation:
        print(f"  Cinq premieres violations :")
        print(f"    {'b':>13} | {'#impl':>5} | {'#max-f':>6} | {'max_size':>8}")
        for s in examples_violation:
            print(f"    {str(s.betti):>13} | {s.n_prime_implicants:>5} | {s.n_max_faces:>6} | {s.max_prime_size:>8}")


def analyse_lemme_1(stats: list[Stats]) -> None:
    print()
    print("=" * 78)
    print("Note sur le Lemme 1 (taille de circuit = << recouvrement simplicial >>)")
    print("=" * 78)
    print(
        "  Pour f monotone, la taille minimale d'un circuit Sigma Pi monotone est\n"
        "  exactement le nombre d'implicants premiers de f. C'est un fait classique,\n"
        "  pas nouveau. L'identification avec un << recouvrement de Delta_f par des\n"
        "  simplexes de dimension <= k-1 >> est imprecise : les implicants premiers\n"
        "  sont les NON-FACES MINIMALES de Delta_f (= generateurs minimaux de l'ideal\n"
        "  de Stanley-Reisner I_{Delta_f}), pas des faces de Delta_f lui-meme.\n"
        "\n"
        "  L'enonce du Lemme 1 confond donc le complexe avec son << complement >>\n"
        "  (l'ideal monomial associe). Cela ne donne pas une borne inferieure\n"
        "  non-triviale, c'est juste une reformulation de la definition canonique.\n"
    )


def main() -> None:
    print("Tour 06 -- Stanley-Reisner et fan-in borne pour fonctions monotones")
    print()
    demo_C4_counterexample()
    print()
    stats = enumerate_n4()
    analyse_lemme_2(stats)
    analyse_lemme_1(stats)
    print()
    print("=" * 78)
    print("BILAN")
    print(
        "1. Le Lemme 2 est REFUTE par contre-exemple direct : la fonction\n"
        "   f = (x_0 AND x_2) OR (x_1 AND x_3) a b_1(Delta_f) = 1, mais sa\n"
        "   taille de circuit (2) est strictement INFERIEURE au nombre de\n"
        "   faces maximales (4) de Delta_f. L'enumeration n=4 montre que ce\n"
        "   contre-exemple n'est pas isole.\n"
        "\n"
        "2. Le Lemme 1 est imprecis : il melange le complexe simplicial Delta_f\n"
        "   et l'ideal monomial associe (dont les generateurs minimaux sont les\n"
        "   implicants premiers, NON les faces). Reformule correctement, il\n"
        "   devient une tautologie definitionnelle (taille de circuit = nombre\n"
        "   de generateurs minimaux de l'ideal de Stanley-Reisner).\n"
        "\n"
        "3. La condition (f) (contribution technique concrete) n'est pas\n"
        "   satisfaite : le Proposeur << s'engage >> a concevoir un script mais\n"
        "   ne fournit ni le script ni le micro-theoreme demande. Le calcul que\n"
        "   je viens d'effectuer (qu'il aurait du faire) refute precisement la\n"
        "   conjecture qu'il avancait sans la verifier.\n"
        "\n"
        "VERDICT : LACUNE REPARABLE.\n"
        "  Le programme est legitime (bornes inferieures topologiques pour\n"
        "  circuits monotones, lignee Razborov 1985 / Alon-Boppana / Karchmer-\n"
        "  Wigderson), mais l'enonce specifique du Proposeur (Lemmes 1 et 2)\n"
        "  est faux comme presente. Pour reparer, il faudrait :\n"
        "    - reformuler L1 en termes d'IDEAL de Stanley-Reisner (non Delta_f\n"
        "      lui-meme) ;\n"
        "    - remplacer L2 par un enonce topologique correct (peut-etre une\n"
        "      borne via la regularite de Castelnuovo-Mumford de l'ideal, ou\n"
        "      via la profondeur projective). Mais alors on quitte le territoire\n"
        "      << calcul exhaustif sur n=5 >> pour rejoindre l'algebre commutative\n"
        "      / la theorie de l'evasivite -- programme actif et difficile."
    )


if __name__ == "__main__":
    main()
