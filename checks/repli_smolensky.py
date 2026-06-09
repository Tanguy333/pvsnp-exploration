"""
TACHE B-002 -- Replication de la methode Razborov-Smolensky (audit A-004),
en ses deux pas.

PAS 1 (cote construction) : approximation probabiliste de OR sur F_3.
  P_l(x) = 1 - prod_{t=1}^{l} (1 - L_t(x)^2),  L_t = sum_i r_{t,i} x_i mod 3,
  r aleatoires. Sur F_3, L^2 in {0, 1}, donc P_l(x) = 1 ssi au moins un
  L_t(x) != 0. Pour x = 0 : P = 0 toujours. Pour x != 0 :
  Pr[L_t(x) = 0] = 1/3, donc Pr[erreur en x] = (1/3)^l. Degre 2l.
  -> mesurer l'erreur empirique PIRE-CAS sur x et la comparer a (1/3)^l.

PAS 2 (cote borne inferieure) : PARITY est loin de tout polynome bas degre
  sur F_3. Borne de comptage de Smolensky : tout P de degre d sur F_3
  coincide avec PARITY_n sur au plus  sum_{i <= (n+d)/2} C(n, i)  entrees.
  -> calculer l'accord MAXIMAL EXACT par enumeration complete du code
     (evaluations de tous les polynomes de degre <= d, 3^M mots) pour
     (n, d) petits, et le comparer a la borne.
"""

from __future__ import annotations

import itertools
import random
from math import comb

import numpy as np

random.seed(2026)
rng = np.random.default_rng(2026)


# ----------------------------------------------------- PAS 1 : OR probabiliste

def step1(m: int, l_max: int, trials: int = 20000) -> None:
    print(f"\nPAS 1 -- OR_{m} ~ 1 - prod(1 - L_t^2) sur F_3, degre 2*l")
    print(f"  {'l':>2} | {'erreur pire-cas empirique':>26} | {'(1/3)^l':>10}")
    # jeu d'entrees de test : 0, tous les e_i, et 60 entrees aleatoires
    tests = [np.zeros(m, dtype=np.int64)]
    for i in range(m):
        e = np.zeros(m, dtype=np.int64)
        e[i] = 1
        tests.append(e)
    for _ in range(60):
        tests.append(rng.integers(0, 2, size=m))
    tests = np.array(tests)
    is_or = (tests.sum(axis=1) > 0).astype(np.int64)

    for l in range(1, l_max + 1):
        errs = np.zeros(len(tests))
        for _ in range(trials):
            R = rng.integers(0, 3, size=(l, m))
            L = (R @ tests.T) % 3                  # l x #tests
            P = (L != 0).any(axis=0).astype(np.int64)
            errs += (P != is_or)
        worst = errs.max() / trials
        print(f"  {l:>2} | {worst:>26.5f} | {(1/3)**l:>10.5f}")


# --------------------------------------------- PAS 2 : accord max avec PARITY

def step2(n: int, d: int) -> tuple[int, int, int]:
    """ Accord maximal exact d'un polynome F_3 de degre <= d avec PARITY_n
        (valeurs comparees dans F_3, PARITY in {0,1}). Enumeration du code.
        Retourne (accord_max, borne_smolensky, 2^n). """
    inputs = list(itertools.product([0, 1], repeat=n))
    N = len(inputs)
    parity = np.array([sum(z) % 2 for z in inputs], dtype=np.int64)
    monos = []
    for deg in range(d + 1):
        monos.extend(itertools.combinations(range(n), deg))
    M = len(monos)
    # matrice d'evaluation des monomes : N x M
    E = np.zeros((N, M), dtype=np.int64)
    for r, z in enumerate(inputs):
        for c, S in enumerate(monos):
            E[r, c] = 1 if all(z[j] for j in S) else 0
    # enumeration des 3^M vecteurs de coefficients par blocs
    total = 3 ** M
    best = 0
    block = 200_000
    coeff_iter = itertools.product(range(3), repeat=M)
    done = 0
    while done < total:
        rows = list(itertools.islice(coeff_iter, block))
        A = np.array(rows, dtype=np.int64)
        vals = (A @ E.T) % 3                      # |bloc| x N
        agree = (vals == parity[None, :]).sum(axis=1)
        best = max(best, int(agree.max()))
        done += len(rows)
    bound = sum(comb(n, i) for i in range(0, (n + d) // 2 + 1))
    return best, bound, N


def main() -> None:
    print("TACHE B-002 -- replication Razborov-Smolensky (F_3 vs MOD_2)")
    print("=" * 72)

    step1(m=16, l_max=6)
    step1(m=32, l_max=6, trials=10000)

    print("\nPAS 2 -- accord maximal exact degre-d / PARITY_n sur F_3")
    print(f"  {'(n,d)':>7} | {'accord max':>10} | {'borne Smolensky':>15} | "
          f"{'2^n':>5} | {'fraction':>9}")
    for (n, d) in [(3, 1), (4, 1), (5, 1), (6, 1), (4, 2), (5, 2)]:
        M = sum(comb(n, i) for i in range(d + 1))
        if 3 ** M > 50_000_000:
            print(f"  ({n},{d})  : espace 3^{M} trop grand -- saute (honnete)")
            continue
        best, bound, N = step2(n, d)
        ok = best <= bound
        print(f"  ({n},{d})  | {best:>10} | {bound:>15} | {N:>5} | "
              f"{best/N:>9.4f}   {'<= borne OK' if ok else '*** VIOLATION ***'}")

    print("\nLecture : pas 1 -> erreur en (1/3)^l avec degre seulement 2l")
    print("(c'est le moteur de l'approximation de tout AC^0[3]) ;")
    print("pas 2 -> l'accord avec PARITY plafonne bien sous la borne de")
    print("comptage : c'est la tension approximable/inapproximable qui")
    print("donne la borne exponentielle de Razborov-Smolensky.")


if __name__ == "__main__":
    main()
