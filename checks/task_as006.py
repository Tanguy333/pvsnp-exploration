"""
TACHE AS-006 -- anatomie du supplement hors-centre : decomposition
fibre-par-fibre des temoins optimaux EXACTS de (7, 3, w), w = 2, 3, 4.

Pour chaque temoin optimal u (CVP certifie), on reconstruit le residu
exact R = C^T G^{-1} (u/2) in Q^128 (avec verifications : ||R||^2 = D et
R orthogonal a tous les monomes de degre <= d), puis pour CHAQUE paire de
variables (i,j) (21 choix) on partitionne les 128 points en 4 fibres
(x_i, x_j) et on compare les normes^2 de fibre aux optima libres D(5,3,.)
(benchmarks AS-004). Question : le temoin du CENTRE (w=4, serre) se
factorise-t-il fibre-optimalement ? Ou se loge l'exces hors centre ?
"""

from __future__ import annotations

import time
from fractions import Fraction as F

import numpy as np
from sympy import Matrix, Rational

from task_as003_cvp2 import cvp_enum
from task_as004 import prepare_thr, local_refine, babai_ub
from task_as005 import D5, pred_lb

N = 128
n, d = 7, 3


def solve_witness(w):
    C, Cf, M, r = prepare_thr(n, d, w)
    u0, _ = babai_ub(M, Cf, r)
    u1, ubf = local_refine(M, Cf, r, u0)
    best, best_u, nodes, capped = cvp_enum(M, Cf, r, ubf * (1 + 1e-9) + 1e-9,
                                           node_cap=80_000_000)
    assert not capped, f"cap atteint a w={w}"
    if best_u is None:
        best_u = u1
    return C, best_u


def exact_residual(C, u):
    Cm = Matrix(C)
    G = Cm * Cm.T
    uv = Matrix([int(round(x)) for x in u])
    sol = G.LUsolve(uv)
    R = (Cm.T * sol) / 2
    return [F(int(Rational(R[x]).p), int(Rational(R[x]).q)) for x in range(N)]


def verify_residual(R, w):
    import itertools
    total = sum(x * x for x in R)
    for k in range(d + 1):
        for T in itertools.combinations(range(n), k):
            s = sum(R[x] for x in range(N) if all((x >> i) & 1 for i in T))
            assert s == 0, f"orthogonalite violee T={T}"
    return total


def fibre_split(R, i, j, w):
    out = []
    for a in (0, 1):
        for b in (0, 1):
            pts = [x for x in range(N)
                   if ((x >> i) & 1) == a and ((x >> j) & 1) == b]
            nrm = sum(R[x] * R[x] for x in pts)
            bench = D5[d].get(w - a - b, F(0))
            out.append((a, b, nrm, bench))
    return out


def main():
    with open("as006_anatomie.txt", "a", encoding="utf-8") as fh:
        for w in (4, 3, 2):
            t0 = time.time()
            C, u = solve_witness(w)
            R = exact_residual(C, u)
            total = verify_residual(R, w)
            pred = pred_lb(d, w)
            head = (f"=== (7,3,w={w}) : D={total} (pred fibres {pred}, "
                    f"exces {total - pred}) [orthogonalite verifiee] "
                    f"({time.time()-t0:.0f}s)")
            print(head, flush=True)
            fh.write(head + "\n")
            # pour chaque paire : la fibre-decomposition ; on cherche la
            # paire au MOINDRE exces total et la structure de l'exces
            best_pairs = []
            for i in range(n):
                for j in range(i + 1, n):
                    fs = fibre_split(R, i, j, w)
                    exces = sum(nrm - bench for (_, _, nrm, bench) in fs)
                    tight = all(nrm == bench for (_, _, nrm, bench) in fs)
                    best_pairs.append((exces, (i, j), fs, tight))
            best_pairs.sort(key=lambda t: t[0])
            exces_min, pair, fs, tight = best_pairs[0]
            line = (f"  meilleure paire {pair} : exces={exces_min} "
                    f"{'FACTORISATION EXACTE (fibres = optima libres)' if tight else ''}")
            print(line, flush=True)
            fh.write(line + "\n")
            for (a, b, nrm, bench) in fs:
                l2 = f"    fibre ({a},{b}) -> THR_{w-a-b} : ||R||^2={nrm} vs optimum libre {bench} (delta {nrm-bench})"
                print(l2, flush=True)
                fh.write(l2 + "\n")
            uni = len({e for e, _, _, _ in best_pairs})
            l3 = (f"  exces identique sur les 21 paires ? "
                  f"{'OUI' if uni == 1 else f'NON ({uni} valeurs distinctes, min {best_pairs[0][0]}, max {best_pairs[-1][0]})'}")
            print(l3, flush=True)
            fh.write(l3 + "\n")
            fh.flush()


if __name__ == "__main__":
    main()
