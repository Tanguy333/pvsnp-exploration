"""
Tour 10 -- Test empirique de la conjecture C10 (Proposeur) avant soumission.

CONJECTURE C10 (raffinement de C9 a la lumiere des 215 contre-exemples n=5) :
  Pour f monotone non-constante, equigeneree en degre t, I_f a une resolution
  libre minimale PURE si et seulement si toutes les intersections NON-VIDES
  entre paires distinctes de mintermes ont la MEME taille.

  Formellement : posons S_inter(f) = { |M_i cap M_j| : i != j, M_i cap M_j != emptyset }.
                 C10 : I_f pure <=> |S_inter(f)| <= 1.

INTUITION : le contre-exemple minimal `(x1x2x3)v(x1x2x4)v(x0x3x4)` a S_inter
= {2, 1, 1} (deux paires partageant 1 var, une paire partageant 2 var). Le
mix de tailles d'intersection cree des syzygies de degres melanges (deg 4
entre paires partageant 2 var, deg 5 entre paires partageant 1 var), ce qui
oblige deux shifts a l'index 1, donc non-pure.

Application stricte de la condition (j) : verification sur les 2109 fonctions
equigenerated n=5 AVANT soumission. Si la conjecture echoue, elle est retiree
ou raffinee.
"""

from __future__ import annotations

import itertools
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from tour_07_resolutions_libres import hochster_bettis_RI, betti_I_from_RI
from tour_08_atlas_boij_soderberg import is_pure_resolution, prime_implicants, betti_table_I
from tour_09_equigeneration_conjecture import is_equigenerated
from tour_09_extension_n5 import all_monotone_masks_dedekind


# ---------------------------------------------------------------------------
# Predicat : intersections non-vides toutes de meme taille
# ---------------------------------------------------------------------------

def intersection_sizes(prime_imps: list[frozenset[int]]) -> set[int]:
    """ Renvoie l'ensemble des tailles |M_i cap M_j| pour i != j et intersection non-vide. """
    sizes = set()
    for i, j in itertools.combinations(range(len(prime_imps)), 2):
        inter = prime_imps[i] & prime_imps[j]
        if inter:
            sizes.add(len(inter))
    return sizes


def is_intersection_uniform(prime_imps: list[frozenset[int]]) -> bool:
    """ True si toutes les intersections non-vides ont la meme taille (ou vacuously). """
    return len(intersection_sizes(prime_imps)) <= 1


# ---------------------------------------------------------------------------
# Pipeline n=5 ciblant les equigenerated
# ---------------------------------------------------------------------------

def main() -> None:
    n = 5
    print(f"Tour 10 -- Test C10 (intersections non-vides uniformes) sur n={n}")
    print("=" * 78)
    print()
    print("  C10 : I_f equigenerated pure <=>")
    print("        toutes les intersections non-vides entre paires de mintermes")
    print("        ont la meme taille.")
    print()

    t0 = time.time()
    monotone = all_monotone_masks_dedekind(n)
    print(f"  Fonctions monotones sur n={n} : {len(monotone)} ({time.time()-t0:.1f}s)")

    # Filtrer les equigenerated non-constantes.
    equi_funcs = []
    for mask in monotone:
        pi = prime_implicants(mask, n)
        if not pi:
            continue
        if is_equigenerated(pi):
            equi_funcs.append((mask, pi))

    print(f"  Fonctions non-constantes equigenerated : {len(equi_funcs)}")
    print()

    # Pour chaque : calculer (pure, intersection-uniform).
    table = {(True, True): 0, (True, False): 0, (False, True): 0, (False, False): 0}
    counter_examples_pure_not_uniform: list[tuple[int, list[frozenset[int]]]] = []
    counter_examples_uniform_not_pure: list[tuple[int, list[frozenset[int]]]] = []

    t1 = time.time()
    progress_every = max(1, len(equi_funcs) // 20)
    for k, (mask, pi) in enumerate(equi_funcs):
        if k % progress_every == 0:
            elapsed = time.time() - t1
            print(f"    [{k}/{len(equi_funcs)}] {elapsed:.1f}s", flush=True)
        bt = betti_table_I(pi, n)
        pure = is_pure_resolution(bt)
        uniform = is_intersection_uniform(pi)
        table[(pure, uniform)] += 1
        if pure and not uniform:
            counter_examples_pure_not_uniform.append((mask, pi))
        if uniform and not pure:
            counter_examples_uniform_not_pure.append((mask, pi))
    print(f"    {len(equi_funcs)}/{len(equi_funcs)} {time.time()-t1:.1f}s done.")
    print()

    # Tableau de contingence.
    print("  Tableau (pure x intersection-uniforme) sur les fonctions equigenerated :")
    print(f"  {'':>15} | {'uniform=True':>12} | {'uniform=False':>13}")
    print(f"  {'-'*15} | {'-'*12} | {'-'*13}")
    print(f"  {'pure=True':>15} | {table[(True, True)]:>12} | {table[(True, False)]:>13}")
    print(f"  {'pure=False':>15} | {table[(False, True)]:>12} | {table[(False, False)]:>13}")
    print()

    print(f"  Direction pure => uniform : {len(counter_examples_pure_not_uniform)} contre-exemples.")
    print(f"  Direction uniform => pure : {len(counter_examples_uniform_not_pure)} contre-exemples.")
    print()

    def fmt_pi(pi: list[frozenset[int]]) -> str:
        return ", ".join("{" + ",".join(map(str, sorted(p))) + "}" for p in sorted(pi, key=sorted))

    if counter_examples_pure_not_uniform:
        print(f"  Exceptions pure-mais-non-uniform ({len(counter_examples_pure_not_uniform)}) :")
        for mask, pi in counter_examples_pure_not_uniform[:5]:
            print(f"    mintermes={fmt_pi(pi)}  S_inter={sorted(intersection_sizes(pi))}")
        if len(counter_examples_pure_not_uniform) > 5:
            print(f"    ...et {len(counter_examples_pure_not_uniform) - 5} autres.")

    if counter_examples_uniform_not_pure:
        print(f"  Exceptions uniform-mais-non-pure ({len(counter_examples_uniform_not_pure)}) :")
        for mask, pi in counter_examples_uniform_not_pure[:5]:
            print(f"    mintermes={fmt_pi(pi)}  S_inter={sorted(intersection_sizes(pi))}")
        if len(counter_examples_uniform_not_pure) > 5:
            print(f"    ...et {len(counter_examples_uniform_not_pure) - 5} autres.")

    print()
    print("=" * 78)
    if not counter_examples_pure_not_uniform and not counter_examples_uniform_not_pure:
        print("VERDICT n=5 (equigenerated only) : CONJECTURE C10 CONFIRMEE")
        print("  -> Proposition soumissible.")
    elif not counter_examples_pure_not_uniform:
        print("VERDICT n=5 : Direction pure => uniform OK ; uniform =/=> pure REFUTEE")
        print("  -> Conjecture a affaiblir en implication unidirectionnelle.")
    elif not counter_examples_uniform_not_pure:
        print("VERDICT n=5 : Direction uniform => pure OK ; pure =/=> uniform REFUTEE")
        print("  -> Conjecture a affaiblir en implication unidirectionnelle.")
    else:
        print("VERDICT n=5 : LES DEUX DIRECTIONS REFUTEES")
        print("  -> C10 n'est pas la bonne caracterisation. Affiner ou retirer.")


if __name__ == "__main__":
    main()
