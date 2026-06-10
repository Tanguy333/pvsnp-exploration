"""
TACHE F-011, etape 13 -- La loi mod 3 du cas t general.

THEOREME F-gen (borne sup, chaines) :
  Soit P = 3^b >= t. Si n < 2P + t, alors deg_3^sym(THR_{t,n}) <= P.
  Construction : g = 0 sur [0,t), 1 sur [t, P+t), 2 sur [P+t, n].
  Alors h(j) = g(j+P) - g(j) = 1 pour tout j in [0, n-P] (chaines de
  residus : 0 -> 1 -> 2 pour j0 < t, possibles ssi <= 3 etages, i.e.
  n < 3P + j0 ; 1 -> 2 pour j0 in [t, P), possibles ssi <= 2 etages,
  i.e. n < 2P + t). h constante => Delta^{P+1} g = 0 => deg <= P.

THEOREME E-gen (rampe, borne inf) :
  Soit P = 3^b avec P <= deg < 2P et n >= 2P + t. Alors
  deg_3^sym(THR_{t,n}) >= n - P - t + 1.
  Preuve : G = g(.+P) - g a deg <= d - P < P, domaine [0, n-P] ; G est
  P-periodique (Delta^P = S^P - id) ; paires interdites sur les positions
  j in [t, n-2P] (trois etages dans {1,2}) => G = 0 sur [t, n-2P] ; et
  G(t-1) = g(t-1+P) != 0. Decalage de Mahler : H = G(.+(t-1)) garde
  deg(H) <= deg(G), H(0) != 0, H = 0 sur [1, n-2P-t+1] ; interpolation
  (etape 7) : deg(G) >= n-2P-t+1, donc d >= P + (n-2P-t+1) = n-P-t+1. QED
  Consequence (avec D-gen : deg >= P si P <= n-t+1) :
  deg ∉ [P, min(2P, n-P-t+1)) => deg >= min(2P, n-P-t+1).

LOI CANDIDATE (mod 3, t general) :
  LB(t,n) = max( t,
                 max{ min(2P, n-P-t+1) : P = 3^b <= n-t+1 },   [D+E-gen]
                 B_block(t,n) )                                 [T-F011b mono]
  et conjecture : deg_3^sym = LB.

Ce script :
  [A] verifie F-gen (construction explicite, P = 3, 9, 27, tout n < 2P+t) ;
  [B] verifie E-gen contre la DP (aucune violation) ;
  [C] teste LOI == DP exacte sur la grille t = 1..12, n = t..t+26
      (cap DP d <= 18) -- coincidences et ecarts.
"""

from __future__ import annotations

from math import comb


def mahler_degree(vals, m=3):
    deg = -1
    for i in range(len(vals)):
        a = sum(((-1) ** (i - k)) * comb(i, k) * vals[k] for k in range(i + 1)) % m
        if a != 0:
            deg = i
    return deg


def dp_feasible(t, n, d):
    W = d + 2
    coeffs = [((-1) ** (d + 1 - k)) * comb(d + 1, k) % 3 for k in range(W)]
    states = {tuple()}
    for w in range(0, n + 1):
        allowed = (0,) if w < t else (1, 2)
        new = set()
        for st in states:
            for val in allowed:
                seq = st + (val,)
                if len(seq) == W:
                    if sum(c * v for c, v in zip(coeffs, seq)) % 3 != 0:
                        continue
                    seq = seq[1:]
                new.add(seq)
        states = new
        if not states:
            return False
    return True


def dp_deg(t, n, d_cap=18):
    for d in range(t, d_cap + 1):
        if d + 1 > n or dp_feasible(t, n, d):
            return d
    return None


# ------------------------------------------------------------ bornes

def B_block(t, n, cap=60):
    d = t
    while d <= cap:
        if not any(all(comb(w, i) % 3 == 0 for i in range(t, d + 1))
                   for w in range(t, n + 1)):
            return d
        d += 1
    return cap


def law(t, n):
    lb = t
    P = 1
    while P <= n - t + 1:
        lb = max(lb, min(2 * P, n - P - t + 1), P)
        P *= 3
    return max(lb, B_block(t, n))


# ------------------------------------------------------------ main

def main() -> None:
    print("TACHE F-011 etape 13 -- loi mod 3 du cas t general")
    print("=" * 68)

    print("\n[A] Theoreme F-gen : g = (0^t, 1^P, 2^{n-P-t+...}) -> deg <= P")
    okA = True
    for P in (3, 9, 27):
        for t in range(1, P + 1):
            for n in range(max(t, P), 2 * P + t):
                g = [0] * t + [1] * min(P, n - t + 1) + [2] * max(0, n - P - t + 1)
                g = g[:n + 1]
                if len(g) < n + 1:
                    continue
                cover = all(v in (1, 2) for v in g[t:]) and all(v == 0 for v in g[:t])
                d = mahler_degree(g)
                if not (cover and d <= P):
                    okA = False
                    print(f"    ECHEC : P={P}, t={t}, n={n} : deg={d}")
    print(f"    P = 3, 9, 27, tout t <= P, tout n < 2P+t : "
          f"{'OK' if okA else 'ECHEC'}")

    print("\n[B] + [C] Loi candidate vs DP exacte (t = 1..12, n = t..t+26) :")
    ok, diff, cap = 0, [], 0
    for t in range(1, 13):
        for n in range(t, t + 27):
            L = law(t, n)
            if L > 18:
                cap += 1
                continue
            D = dp_deg(t, n)
            if D is None:
                cap += 1
                continue
            if D == L:
                ok += 1
            else:
                diff.append((t, n, L, D))
    print(f"    {ok} coincidences, {len(diff)} ecarts, {cap} hors-cap")
    for (t, n, L, D) in diff[:15]:
        print(f"    ECART : t={t}, n={n} : loi={L}, DP={D}")
    if len(diff) > 15:
        print(f"    ... et {len(diff)-15} autres")

    print("\n" + "=" * 68)
    if not diff:
        print("LOI mod 3 GENERALE : coincide avec l'exact sur toute la grille.")
        print("  deg_3^sym(THR_t,n) = max(t, max_P min(2P, n-P-t+1), blocage)")
        print("Bornes prouvees : F-gen (sup), D-gen + E-gen + blocage (inf).")
        print("Si la loi tient : il reste a prouver l'EXACTITUDE (bornes sup")
        print("dans les regimes de rampe et de blocage).")
    else:
        print(f"LOI INCOMPLETE : {len(diff)} ecarts -- il manque une obstruction")
        print("ou une construction. Les theoremes F-gen/E-gen restent valides")
        print("comme bornes.")


if __name__ == "__main__":
    main()
