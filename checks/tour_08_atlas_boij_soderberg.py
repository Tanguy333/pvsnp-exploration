"""
Tour 08 -- Refutation du Lemme 4 (resolution pure = OR_n ou AND_n uniquement)
et livraison de l'atlas partiel des 168 fonctions monotones sur n=4 que
le Proposeur a promis sans livrer.

LEMME 4 du Proposeur : pour tout n, OR_n et AND_n sont les SEULES fonctions
monotones dont la decomposition de Boij-Soderberg est triviale (r = 1, soit
une resolution pure au sens de Herzog-Kuhl).

CONTRE-EXEMPLES IMMEDIATS : toutes les fonctions THRESHOLD_k (1 <= k <= n)
ont des resolutions pures (par Eagon-Northcott / Veronese squarefree). Donc
OR_n = THRESHOLD_1, MAJ_n = THRESHOLD_{ceil(n/2)}, ..., AND_n = THRESHOLD_n
sont toutes pures.

Pour n = 4, cela donne 4 classes de threshold pure (au lieu des 2 prevues).
On enumere les 168 fonctions monotones n=4 pour comptabiliser TOUTES les
fonctions a resolution pure -- l'atlas partiel.

REUTILISATION : on importe les routines Hochster du tour 7.
"""

from __future__ import annotations

import itertools
import math
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

# Reutilise les fonctions du tour 7.
sys.path.insert(0, str(Path(__file__).parent))
from tour_07_resolutions_libres import (
    hochster_bettis_RI,
    betti_I_from_RI,
    pd_from_betti,
    reg_from_betti_I,
)


# ---------------------------------------------------------------------------
# Enumeration des fonctions monotones sur n=4
# ---------------------------------------------------------------------------

def is_monotone(mask: int, n: int) -> bool:
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
    return [m for m in range(1 << (1 << n)) if is_monotone(m, n)]


def prime_implicants(mask: int, n: int) -> list[frozenset[int]]:
    N = 1 << n
    T = [x for x in range(N) if (mask >> x) & 1]
    pi: list[frozenset[int]] = []
    for x in T:
        is_min = True
        for y in T:
            if y != x and (y & x) == y:
                is_min = False
                break
        if is_min:
            pi.append(frozenset(i for i in range(n) if (x >> i) & 1))
    return pi


# ---------------------------------------------------------------------------
# Tests sur les Betti tables
# ---------------------------------------------------------------------------

def betti_table_I(prime_imps: list[frozenset[int]], n: int) -> dict[tuple[int, int], int]:
    """ Renvoie {(i, j) : beta_{i,j}(I)} via Hochster. """
    bettis_RI = hochster_bettis_RI(prime_imps, n)
    return betti_I_from_RI(bettis_RI)


def is_pure_resolution(betti_table: dict[tuple[int, int], int]) -> bool:
    """ Resolution pure ssi pour chaque i homologique, il y a AU PLUS UN j
        avec beta_{i,j} > 0.
    """
    by_i: dict[int, set[int]] = {}
    for (i, j), v in betti_table.items():
        if v > 0:
            by_i.setdefault(i, set()).add(j)
    return all(len(js) <= 1 for js in by_i.values())


def shift_sequence(betti_table: dict[tuple[int, int], int]) -> tuple[int, ...]:
    """ Si pure, renvoie le n-uplet des shifts (j_0, j_1, ..., j_p)
        avec j_i = unique j tel que beta_{i, j} > 0. Sinon raise. """
    by_i: dict[int, int] = {}
    for (i, j), v in betti_table.items():
        if v > 0:
            if i in by_i and by_i[i] != j:
                raise ValueError("Not pure")
            by_i[i] = j
    return tuple(by_i[i] for i in sorted(by_i.keys()))


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

@dataclass
class FuncStats:
    mask: int
    prime_imps: list[frozenset[int]]
    betti_table: dict[tuple[int, int], int]
    pure: bool
    pd_I: int
    reg_I: int
    shifts: tuple[int, ...] | None
    threshold_k: int | None  # k si fonction threshold, None sinon


def identify_threshold(prime_imps: list[frozenset[int]], n: int) -> int | None:
    """ THRESHOLD_k a pour mintermes tous les sous-ensembles de taille k.
        Renvoie k si c'est le cas, None sinon. """
    if not prime_imps:
        return None
    sizes = {len(p) for p in prime_imps}
    if len(sizes) != 1:
        return None
    k = next(iter(sizes))
    expected = list(itertools.combinations(range(n), k))
    if len(prime_imps) != len(expected):
        return None
    expected_set = {frozenset(s) for s in expected}
    if set(prime_imps) != expected_set:
        return None
    return k


def main() -> None:
    n = 4
    print("Tour 08 -- Atlas partiel des fonctions monotones n=4 + refutation Lemme 4")
    print("=" * 78)

    print()
    print("(A) Refutation directe du Lemme 4 : K_3 (= MAJ_3) sur n=3")
    print("-" * 78)
    # MAJ_3 sur n=3 : I = (xy, xz, yz).
    maj3_imps = [frozenset({0, 1}), frozenset({0, 2}), frozenset({1, 2})]
    maj3_betti = betti_table_I(maj3_imps, 3)
    print(f"  MAJ_3 = (x_0∧x_1) ∨ (x_0∧x_2) ∨ (x_1∧x_2)")
    print(f"  Mintermes : {[set(p) for p in maj3_imps]}")
    print(f"  Betti(I) = { {ij: v for ij, v in sorted(maj3_betti.items()) if v > 0} }")
    print(f"  Pure resolution ? {is_pure_resolution(maj3_betti)}")
    if is_pure_resolution(maj3_betti):
        print(f"  Shifts : {shift_sequence(maj3_betti)}")
    print()
    print(f"  -> MAJ_3 a une resolution PURE (r=1) mais n'est ni OR_3 ni AND_3.")
    print(f"     Le Lemme 4 du Proposeur est REFUTE des n=3.")

    print()
    print("(B) Enumeration des 168 fonctions monotones sur n=4")
    print("-" * 78)
    monotone = all_monotone_functions(n)
    print(f"  Nombre de fonctions monotones (Dedekind M(4)) : {len(monotone)}")

    stats: list[FuncStats] = []
    for mask in monotone:
        pi = prime_implicants(mask, n)
        if not pi:
            # Fonction constante 0 : I = (1) (idéal unite, exclu de l'analyse)
            continue
        # Skip if mintermes is empty (constant 0).
        bt = betti_table_I(pi, n)
        pure = is_pure_resolution(bt)
        shifts = shift_sequence(bt) if pure else None
        bt_for_I = bt  # bt is already Betti(I)
        bettis_RI = hochster_bettis_RI(pi, n)
        pd_I = pd_from_betti(bettis_RI) - 1
        reg_I = reg_from_betti_I(bt_for_I)
        thr_k = identify_threshold(pi, n)
        stats.append(FuncStats(mask, pi, bt, pure, pd_I, reg_I, shifts, thr_k))

    print(f"  Fonctions non-constantes analysees : {len(stats)}")

    pure_stats = [s for s in stats if s.pure]
    non_pure_stats = [s for s in stats if not s.pure]
    print(f"  Fonctions a resolution PURE  : {len(pure_stats)}")
    print(f"  Fonctions a resolution NON-pure : {len(non_pure_stats)}")

    print()
    print("(C) Liste des fonctions a resolution PURE (avec mintermes et shifts)")
    print("-" * 78)
    # Trier par taille max d'implicant, puis nombre d'implicants.
    pure_stats.sort(key=lambda s: (max(len(p) for p in s.prime_imps), len(s.prime_imps)))
    for k, s in enumerate(pure_stats):
        thr_str = f" THRESHOLD_{s.threshold_k}" if s.threshold_k is not None else ""
        imps_str = ", ".join(
            "{" + ",".join(map(str, sorted(p))) + "}" for p in sorted(s.prime_imps, key=lambda x: (len(x), sorted(x)))
        )
        print(f"  #{k+1:>2} : {imps_str}{thr_str}")
        print(f"        shifts = {s.shifts}, pd = {s.pd_I}, reg = {s.reg_I}")

    print()
    print("(D) Sommaire par classe d'implicants")
    print("-" * 78)
    by_class: dict[tuple[int, int], list[FuncStats]] = {}
    for s in pure_stats:
        key = (len(s.prime_imps), max(len(p) for p in s.prime_imps))
        by_class.setdefault(key, []).append(s)
    print(f"  {'#imp':>4} | {'max_size':>8} | {'cnt':>3} | exemples")
    for (n_imp, max_sz), ss in sorted(by_class.items()):
        thr_k_list = [s.threshold_k for s in ss if s.threshold_k is not None]
        ex = "THRESHOLD" if thr_k_list else "autres"
        print(f"  {n_imp:>4} | {max_sz:>8} | {len(ss):>3} | {ex}")

    print()
    print("=" * 78)
    print("BILAN")
    print(
        f"1. Le Lemme 4 du Proposeur (OR_n, AND_n = seules a r=1) est REFUTE :\n"
        f"   - MAJ_3 (= I(K_3)) a une resolution pure : refutation immediate des n=3.\n"
        f"   - Sur n=4, {len(pure_stats)} fonctions sur les {len(stats)} non-constantes\n"
        f"     ont une resolution pure (pas seulement OR_4 et AND_4).\n"
        f"\n"
        f"2. Au minimum, les 4 fonctions THRESHOLD (k = 1, 2, 3, 4 sur n=4) ont\n"
        f"   toutes des resolutions pures, par Eagon-Northcott / Veronese\n"
        f"   squarefree. C'est un fait classique d'algebre commutative.\n"
        f"\n"
        f"3. Le Proposeur revendiquait le Lemme 4 comme 'prouvable inconditionnellement\n"
        f"   pour tout n', soulignant que c'etait son seul resultat mathematiquement\n"
        f"   solide. Or il est faux des n=3, et faux pour {len(pure_stats)} fonctions\n"
        f"   sur n=4.\n"
        f"\n"
        f"4. L'atlas partiel ci-dessus (point C) est un objet vrai et utile :\n"
        f"   classification des {len(pure_stats)} fonctions monotones a resolution\n"
        f"   pure sur n=4, avec leurs mintermes et leurs shift sequences. C'est\n"
        f"   le 'vrai objet' que le Proposeur promettait sans livrer.\n"
        f"\n"
        f"VERDICT : LACUNE REPARABLE (suite).\n"
        f"  Le Lemme 4 est faux comme enonce. La direction generale (catalogage\n"
        f"  Boij-Soderberg des fonctions monotones n=4) reste valide et l'atlas\n"
        f"  ci-dessus en est un debut. Pour reparer, il faudrait :\n"
        f"  - Reformuler L4 : 'I_f a une resolution pure ssi I_f est un ideal\n"
        f"    de Veronese squarefree' (c'est-a-dire ssi f est une fonction\n"
        f"    threshold), conjecture qui demande encore verification.\n"
        f"  - Implementer la decomposition Boij-Soderberg complete (algorithme\n"
        f"    de Eisenbud-Schreyer) pour les fonctions non-pures, et calculer\n"
        f"    leurs invariants (r, H_BS, Delta).\n"
        f"  - Comparer ces invariants avec D_m, L_m, C_m (a recuperer/recalculer)."
    )


if __name__ == "__main__":
    main()
