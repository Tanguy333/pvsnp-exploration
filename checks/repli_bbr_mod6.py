"""
TACHE B-005 -- Replication de la surprise Barrington-Beigel-Rudich (1994) :
OR_n admet des representations faibles de BAS degre modulo 6 (composite),
alors que modulo un premier le degre est essentiellement lineaire.

Notion (BBR, "weak representation") : P in Z_m[x_1..x_n], multilineaire,
  represente faiblement OR_n si  P(0^n) = 0  et  P(x) != 0 (mod m)
  pour tout x != 0.

Restriction de ce script : representations SYMETRIQUES
  P = sum_{i=1}^{d} a_i e_i  (e_i = polynome symetrique elementaire).
  Valeur sur une entree de poids w :  P = sum_i a_i C(w, i)  (mod m).
  Condition : sum_i a_i C(w,i) != 0 (mod m) pour tout w in [1, n].
  -> deg_m^sym(OR_n) = min d tel qu'un vecteur (a_1..a_d) existe.
  CAVEAT : deg_m^sym est une BORNE SUP de deg_m (cas general) ; mod un
  composite, la symetrisation ne preserve pas la representation (pas de
  division par n!), donc l'egalite n'est pas garantie.

Methode :
  - m premier (2, 3, 5) : recherche exhaustive a in Z_m^d (numpy).
  - m = 6 : CRT -- chercher u in Z_2^d et v in Z_3^d tels que pour tout
    w : u.c2(w) != 0 (mod 2)  OU  v.c3(w) != 0 (mod 3),
    ou c_p(w) = (C(w,1..d) mod p).

Contexte theorique (a confronter aux resultats) :
  - mod p premier : deg_p(OR_n) >= n/(p-1)  -- croissance lineaire ;
    pour la version faible, la structure de Lucas (digits en base p)
    fait apparaitre des sauts aux puissances de p.
  - mod 6 : BBR donnent O(sqrt(n)) ; borne inf Omega(log n)
    (Tardos-Barrington). L'ecart est OUVERT depuis 1994. Le mecanisme
    sqrt : un poids w divisible par 2^a ET 3^b avec 2^a, 3^b > d annule
    tous les C(w, i <= d) mod 6 (Lucas) ; le plus petit tel w est
    2^a * 3^b ~ d^2 -> des que n >= 2^a 3^b, il faut d plus grand.
"""

from __future__ import annotations

import itertools
from math import comb

import numpy as np


def binom_table(n_max: int, d: int, m: int) -> np.ndarray:
    """ T[w-1, i-1] = C(w, i) mod m, pour w in [1, n_max], i in [1, d]. """
    T = np.zeros((n_max, d), dtype=np.int64)
    for w in range(1, n_max + 1):
        for i in range(1, d + 1):
            T[w - 1, i - 1] = comb(w, i) % m
    return T


def feasible_prime(n: int, d: int, p: int) -> bool:
    """ Existe-t-il a in Z_p^d avec sum a_i C(w,i) != 0 mod p, w in [1,n] ? """
    T = binom_table(n, d, p)  # n x d
    # Enumerer tous les a (p^d) par blocs numpy.
    total = p ** d
    if total > 4_000_000:
        raise MemoryError(f"espace {p}^{d} trop grand")
    # construire la matrice de tous les vecteurs a : total x d
    A = np.array(list(itertools.product(range(p), repeat=d)), dtype=np.int64)
    vals = (A @ T.T) % p          # total x n
    good = np.all(vals != 0, axis=1)
    return bool(good.any())


def feasible_mod6(n: int, d: int) -> bool:
    """ CRT : u in Z_2^d, v in Z_3^d avec, pour tout w,
        u.c2(w) != 0 (2)  ou  v.c3(w) != 0 (3). """
    T2 = binom_table(n, d, 2)
    T3 = binom_table(n, d, 3)
    V = np.array(list(itertools.product(range(3), repeat=d)), dtype=np.int64)
    vals3 = (V @ T3.T) % 3        # 3^d x n  (precalcule une fois)
    for u in itertools.product(range(2), repeat=d):
        u_arr = np.array(u, dtype=np.int64)
        v2 = (T2 @ u_arr) % 2     # n
        W0 = np.where(v2 == 0)[0]  # poids non couverts par u
        if len(W0) == 0:
            return True
        # existe-t-il v couvrant tous les w de W0 ?
        ok = np.all(vals3[:, W0] != 0, axis=1)
        if ok.any():
            return True
    return False


def min_degree(n: int, m: int, d_cap: int) -> int | None:
    for d in range(1, d_cap + 1):
        try:
            if m == 6:
                if feasible_mod6(n, d):
                    return d
            else:
                if feasible_prime(n, d, m):
                    return d
        except MemoryError:
            return None
    return None


def main() -> None:
    print("TACHE B-005 -- degre minimal des representations faibles")
    print("SYMETRIQUES de OR_n modulo m (replication BBR 1994)")
    print("=" * 70)
    print(f"{'n':>4} | {'mod 2':>6} | {'mod 3':>6} | {'mod 5':>6} | {'mod 6':>6}")
    print("-" * 70)
    caps = {2: 18, 3: 11, 5: 8, 6: 9}
    ns = list(range(1, 25)) + [27, 30, 32, 36, 40, 48, 60, 72, 96, 144]
    results = []
    for n in ns:
        row = {"n": n}
        for m in (2, 3, 5, 6):
            d = min_degree(n, m, caps[m])
            row[m] = d
        results.append(row)
        fmt = lambda x: str(x) if x is not None else f">{'?'}"
        print(f"{n:>4} | {fmt(row[2]):>6} | {fmt(row[3]):>6} | "
              f"{fmt(row[5]):>6} | {fmt(row[6]):>6}")

    print("-" * 70)
    print("(valeur '>?' = depasse le cap de recherche -- rapporte tel quel)")
    print()
    print("Lecture attendue : mod p premier, sauts aux puissances de p")
    print("(croissance ~lineaire) ; mod 6, croissance bien plus lente")
    print("(~sqrt, mecanisme 2^a 3^b de Lucas).")


if __name__ == "__main__":
    main()
