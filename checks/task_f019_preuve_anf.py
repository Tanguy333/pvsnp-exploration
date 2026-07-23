"""
TACHE F-019 -- ANALYSE : prouver |ANF(THRW_m)| = 2^{m-1}-1.

Reduction deja etablie (complementation mod 2, |A| >= 1) :
  a_A = parite de #{U inclus dans A : somme(U) < m}   (poids {1..m}).

Phase 1 (ce script) : la table 2D EXACTE N(k,t) = sparsite ANF de
[somme des poids {1..k} choisis >= t], pour tout t, k <= 12.
Hypothese des petits cas (k = 2, 3 a la main) : N(k,t) = 2^{j}-1 avec
j = j(k,t) un escalier en t. Objectif : la forme close de j, puis la
preuve par induction de Shannon (phase 2, a la main).
"""

from __future__ import annotations


def anf_sparsity_thr(k, t):
    """Sparsite ANF de g(U) = [somme(U) >= t], U dans {1..k}."""
    size = 1 << k
    v = bytearray(size)
    for x in range(size):
        s = 0
        for i in range(k):
            if x & (1 << i):
                s += i + 1
        v[x] = 1 if s >= t else 0
    for i in range(k):
        for x in range(size):
            if x & (1 << i):
                v[x] ^= v[x ^ (1 << i)]
    return sum(v)


def anf_set(k, t):
    """Ensemble des monomes ANF (masques) de [somme >= t] sur {1..k}."""
    size = 1 << k
    v = bytearray(size)
    for x in range(size):
        s = 0
        for i in range(k):
            if x & (1 << i):
                s += i + 1
        v[x] = 1 if s >= t else 0
    for i in range(k):
        for x in range(size):
            if x & (1 << i):
                v[x] ^= v[x ^ (1 << i)]
    return {x for x in range(size) if v[x]}


def main():
    import math
    print("N(k,t) et j = log2(N+1) (— si N+1 pas puissance de 2)")
    for k in range(2, 13):
        tmax = k * (k + 1) // 2
        row = []
        for t in range(1, tmax + 1):
            N = anf_sparsity_thr(k, t)
            j = math.log2(N + 1)
            row.append(str(int(j)) if j == int(j) else f"({N})")
        print(f"  k={k:2d} : j(t=1..{tmax}) = " + " ".join(row),
              flush=True)

    print("\n== verification mecanique du THEOREME et de sa preuve ==")
    ok_thm = ok_rec = ok_or = True
    for k in range(2, 13):
        for t in range(2, k + 2):
            if anf_sparsity_thr(k, t) != (1 << (k - 1)) - 1:
                ok_thm = False
        # cas 2 <= t <= k : S(k,t) = S(k-1,t) u z_k(S(k-1,t) u {vide})
        for t in range(2, k + 1):
            S = anf_set(k, t)
            S0 = anf_set(k - 1, t)
            top = 1 << (k - 1)
            pred = S0 | {x | top for x in (S0 | {0})}
            if S != pred:
                ok_rec = False
        # cas t = k+1 : g1 = OR_{k-1}, ANF = tous les non-vides
        t = k + 1
        S = anf_set(k, t)
        S0 = anf_set(k - 1, t)
        allne = set(range(1, 1 << (k - 1)))
        top = 1 << (k - 1)
        pred = S0 | {x | top for x in (allne - S0)}
        if S != pred:
            ok_or = False
    print(f"  N(k,t) = 2^(k-1)-1 sur 2 <= t <= k+1, k <= 12 : "
          f"{'OK' if ok_thm else 'ECHEC'}")
    print(f"  recurrence cas 2 <= t <= k (g1 = 1)      : "
          f"{'OK' if ok_rec else 'ECHEC'}")
    print(f"  recurrence cas t = k+1 (g1 = OR)          : "
          f"{'OK' if ok_or else 'ECHEC'}")


if __name__ == "__main__":
    main()
