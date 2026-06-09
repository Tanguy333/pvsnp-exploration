"""
TACHE F-007 -- Cartographie exhaustive W_L1 vs DNF_min a n = 3 et n = 4.

Question (suite de T-F006) : T-F006 prouve W_L1(IP_{2k}) = DNF_min(IP_{2k}).
Ilot ou continent ? Indices : PARITY_4 a W=40 > DNF_min=8 ; MAJ_4 a
W=5 < DNF_min=6 -- l'inegalite va dans les DEUX sens. La classe d'egalite
est donc un objet structure. On la cartographie exhaustivement.

Pour chaque fonction non-constante f sur n variables :
  - DNF_min(f) : implicants premiers (enumeration 3^n ANDs par masques)
    puis set cover exact (MILP HiGHS in-process).
  - W_L1(f)    : min sum |c_S| sur les polynomes REELS avec p >= 1 sur
    f^{-1}(1), p <= 0 sur f^{-1}(0) (LP HiGHS). Mesure de T-F006 (sur R).
  - n_primes(f), pour recouper avec la classe d'essentialite du Tour 19
    (DNF_min = n_primes).

Sorties : data/w_vs_dnfmin.csv + statistiques (3 classes W<D / W=D / W>D,
recoupement essentialite, exemples).
"""

from __future__ import annotations

import csv
import itertools
import time
from math import isclose

import numpy as np
from scipy.optimize import linprog, milp, LinearConstraint, Bounds


def build_static(n: int):
    """ Precalculs independants de f. """
    N = 1 << n
    inputs = list(itertools.product([0, 1], repeat=n))
    # ANDs : signs in {0,1,-1}^n ; masque des satisfaisants (entier N bits)
    ands = []
    for signs in itertools.product([0, 1, -1], repeat=n):
        m = 0
        for idx, z in enumerate(inputs):
            ok = True
            for i, s in enumerate(signs):
                if s == 1 and z[i] != 1:
                    ok = False
                    break
                if s == -1 and z[i] != 0:
                    ok = False
                    break
            if ok:
                m |= (1 << idx)
        ands.append((signs, m))
    # parents (retrait d'un litteral) pour le test de primalite
    index = {signs: j for j, (signs, _) in enumerate(ands)}
    parents = []
    for signs, _ in ands:
        ps = []
        for i, s in enumerate(signs):
            if s != 0:
                t = list(signs)
                t[i] = 0
                ps.append(index[tuple(t)])
        parents.append(ps)
    # monomes (positifs) pour W_L1 : matrice d'evaluation N x M
    monos = []
    for d in range(n + 1):
        monos.extend(itertools.combinations(range(n), d))
    E = np.zeros((N, len(monos)))
    for r, z in enumerate(inputs):
        for c, S in enumerate(monos):
            E[r, c] = 1.0 if all(z[j] for j in S) else 0.0
    return N, ands, parents, E


def primes_of(fmask: int, N: int, ands, parents):
    """ Masques des implicants premiers de f. """
    notf = ((1 << N) - 1) ^ fmask
    is_impl = [m != 0 and (m & notf) == 0 for (_, m) in ands]
    primes = []
    for j, (signs, m) in enumerate(ands):
        if not is_impl[j]:
            continue
        if any(is_impl[p] for p in parents[j]):
            continue
        primes.append(m)
    return primes


def dnf_min_of(fmask: int, N: int, primes) -> int:
    """ Set cover exact par MILP HiGHS. """
    one_bits = [i for i in range(N) if (fmask >> i) & 1]
    P = len(primes)
    A = np.zeros((len(one_bits), P))
    for c, m in enumerate(primes):
        for r, b in enumerate(one_bits):
            if (m >> b) & 1:
                A[r, c] = 1.0
    res = milp(c=np.ones(P),
               constraints=LinearConstraint(A, lb=1, ub=np.inf),
               bounds=Bounds(0, 1), integrality=np.ones(P))
    return round(res.fun)


def w_l1_of(fmask: int, N: int, E) -> float:
    """ LP : variables (c, a), min sum a, a >= +-c, contraintes d'entree. """
    M = E.shape[1]
    # variables x = [c (libres), a (>=0)] ; objectif sum a
    cobj = np.concatenate([np.zeros(M), np.ones(M)])
    A_ub = []
    b_ub = []
    I = np.eye(M)
    # c - a <= 0 ; -c - a <= 0
    A_ub.append(np.hstack([I, -I]))
    b_ub.append(np.zeros(M))
    A_ub.append(np.hstack([-I, -I]))
    b_ub.append(np.zeros(M))
    rows1 = [r for r in range(N) if (fmask >> r) & 1]
    rows0 = [r for r in range(N) if not (fmask >> r) & 1]
    # f=1 : -E c <= -1 ; f=0 : E c <= 0
    A_ub.append(np.hstack([-E[rows1], np.zeros((len(rows1), M))]))
    b_ub.append(-np.ones(len(rows1)))
    A_ub.append(np.hstack([E[rows0], np.zeros((len(rows0), M))]))
    b_ub.append(np.zeros(len(rows0)))
    res = linprog(cobj, A_ub=np.vstack(A_ub), b_ub=np.concatenate(b_ub),
                  bounds=[(None, None)] * M + [(0, None)] * M, method="highs")
    return res.fun


def run(n: int, writer) -> dict:
    N, ands, parents, E = build_static(n)
    stats = {"lt": 0, "eq": 0, "gt": 0, "eq_and_essential": 0,
             "essential": 0, "total": 0}
    t0 = time.time()
    for fmask in range(1, (1 << N) - 1):
        primes = primes_of(fmask, N, ands, parents)
        dm = dnf_min_of(fmask, N, primes)
        w = w_l1_of(fmask, N, E)
        ess = (dm == len(primes))
        stats["total"] += 1
        stats["essential"] += ess
        if isclose(w, dm, abs_tol=1e-6):
            cl = "eq"
            stats["eq_and_essential"] += ess
        elif w < dm:
            cl = "lt"
        else:
            cl = "gt"
        stats[cl] += 1
        writer.writerow({"n": n, "fmask": fmask,
                         "ones": bin(fmask).count("1"),
                         "n_primes": len(primes), "dnf_min": dm,
                         "w_l1": round(w, 6), "classe": cl,
                         "essentiel": int(ess)})
        if fmask % 8192 == 0:
            el = time.time() - t0
            print(f"  n={n} : {fmask}/{(1 << N) - 2}  ({el:.0f}s)", flush=True)
    return stats


def main() -> None:
    print("TACHE F-007 -- cartographie W_L1 (reels) vs DNF_min, n = 3 et 4")
    print("=" * 72)
    with open("data/w_vs_dnfmin.csv", "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["n", "fmask", "ones",
                                                "n_primes", "dnf_min",
                                                "w_l1", "classe", "essentiel"])
        writer.writeheader()
        for n in [3, 4]:
            t0 = time.time()
            s = run(n, writer)
            dt = time.time() - t0
            print(f"\nn={n} ({s['total']} fonctions, {dt:.0f}s) :")
            print(f"  W <  DNF_min : {s['lt']:>6}  ({100*s['lt']/s['total']:.1f} %)")
            print(f"  W == DNF_min : {s['eq']:>6}  ({100*s['eq']/s['total']:.1f} %)")
            print(f"  W >  DNF_min : {s['gt']:>6}  ({100*s['gt']/s['total']:.1f} %)")
            print(f"  classe essentialite (DNF_min = #primes, Tour 19) : "
                  f"{s['essential']}")
            print(f"  egalite ET essentielle : {s['eq_and_essential']} "
                  f"(egalite sans essentialite : {s['eq'] - s['eq_and_essential']})")
    print("\nCSV : data/w_vs_dnfmin.csv")


if __name__ == "__main__":
    main()
