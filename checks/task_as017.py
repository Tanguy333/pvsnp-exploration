"""
TACHE AS-017 -- LE DERNIER CALCUL : que vaut la cascade decouplee ?

DP exacte sur la cascade (AS-015/016) depuis MAJ_N au centre :
  V(m, e) = 1/2 V(m+1, e) + 1/2 V(m+1, e-1)
  bases : e < 0  -> norme pleine exacte de la classe (1/4 sum C(n_m, w)) ;
          n_m <= NBASE -> valeur exacte (solveur poids-espace).
Les classes S_m suivent la dynamique XOR exacte avec troncature de bord :
  S' = (S cap [0,n]) Delta ((S-1) cap [0,n])   (Pascal mod 2 tronque).

Deux variantes :
  LB_full : bases exactes aux petits n (le meilleur que la cascade + nos
            tables peuvent donner) ;
  LB_pure : base UNIQUEMENT e < 0 (ce que la cascade donne assymptotiquement
            sans oracle) -- c'est elle qui decide si la cascade peut, seule,
            atteindre la Conjecture 13.
Verdict par comparaison aux vraies valeurs D(N, d) connues.
"""

from __future__ import annotations

import sys
from fractions import Fraction as F
from functools import lru_cache
from math import comb

from task_as015 import solve_weight_target

NBASE = 6


def classes_cascade(N, t):
    """S_m pour m = 0..N-1 (classe au niveau m, domaine [0, N-m])."""
    S = frozenset(range(t, N + 1))
    out = [S]
    n = N
    while n > 1:
        n -= 1
        f0 = {w for w in S if w <= n}
        f1 = {w - 1 for w in S if 1 <= w and w - 1 <= n}
        S = frozenset(f0 ^ f1)
        out.append(S)
    return out


def full_norm(S, n):
    return F(sum(comb(n, w) for w in S), 4)


def lb_cascade(N, d, t, pure):
    Ss = classes_cascade(N, t)

    @lru_cache(maxsize=None)
    def V(m, e):
        n = N - m
        S = Ss[m]
        if not S:
            return F(0)
        if e < 0:
            return full_norm(S, n)
        if not pure and n <= NBASE:
            f = [1 if k in S else 0 for k in range(n + 1)]
            val, capped = solve_weight_target(n, d=e, f=f)
            return val
        if n == 1:
            return F(0)  # domaine trivial, borne triviale
        return F(1, 2) * V(m + 1, e) + F(1, 2) * V(m + 1, e - 1)

    return V(0, d)


def main():
    true_vals = {(5, 2): F(5, 32), (5, 3): F(1, 32), (7, 2): F(7, 8),
                 (7, 3): F(1, 8), (9, 3): F(387, 512), (11, 3): F(63, 16),
                 (13, 3): F(9749, 512)}
    print("cell | D vrai | LB_full (bases exactes n<=6) | LB_pure (cascade seule) | ratios")
    for (N, d), D in sorted(true_vals.items()):
        t = (N + 1) // 2
        lf = lb_cascade(N, d, t, pure=False)
        lp = lb_cascade(N, d, t, pure=True)
        print(f"(N={N:>2},d={d}) : D={str(D):>9} | LB_full={str(lf):>10} "
              f"({float(lf/D):.3f} de D) | LB_pure={str(lp):>10} "
              f"({float(lp/D):.4f} de D)", flush=True)
    # tendance asymptotique de LB_pure a d fixe, N croissant
    print("\ntendance LB_pure/2^N a d=3 (la quantite q que la cascade seule garantit) :")
    for N in range(7, 26, 2):
        lp = lb_cascade(N, 3, (N + 1) // 2, pure=True)
        print(f"  N={N:>2} : q_garanti = {float(lp / (1 << N)) * 1024:.5f}/1024", flush=True)


if __name__ == "__main__":
    main()
