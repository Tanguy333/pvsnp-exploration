"""
TACHE F-011, etape 9 -- THEOREME G et cloture de la loi OR mod 3.

THEOREME G (borne superieure de la rampe) :
  Pour P = 3^b et 2P < n < 3P, posons r = n - 2P et
      h(w) := c * (-1)^r * C(w-1, r) mod 3   (c in {1,2}),
  l'unique fonction de degre <= r avec h(0) = c et h(1..r) = 0.
  CLES :
   (i) toute fonction de degre <= r < P est 3^c'-periodique pour le plus
       petit 3^c' > r (Delta^{3^c'} = S^{3^c'} - id), et 3^c' | P, donc
       h(j+P) = h(j) pour tout j -- en particulier h est P-periodique ;
  (ii) les contraintes de compatibilite de g (g(j+P) = g(j) + h(j),
       valeurs dans {1,2}, chaines de longueur <= 3) se reduisent a
       "h(j) = 0 pour j in [1, n-2P]" (paires interdites) et
       "h(0) != 0" -- exactement les proprietes de h ;
  (iii) un prefixe compatible existe : g(j) := 1 si h(j) in {0,1} sinon 2
        pour les positions libres, et la propagation reste dans {1,2}.
  DONC deg_3^sym(OR_n) <= P + r = n - P.

THEOREME (LOI COMPLETE, avec D + E + F + G) :
      deg_3^sym(OR_n) = max( 3^floor(log3 n), n - 3^floor(log3 n) )
  EXACTEMENT, pour tout n >= 1.

Ce script :
  [A] construit explicitement g pour TOUT n des deux regimes (P = 3, 9)
      et verifie : couverture + degre de Mahler <= valeur de la loi ;
  [B] croise avec la DP exacte : construction-degre == DP-degre == loi,
      pour n = 1..26.
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


def P_of(n):
    P = 1
    while P * 3 <= n:
        P *= 3
    return P


def law(n):
    P = P_of(n)
    return max(P, n - P)


# ------------------------------------------------- construction explicite

def build_g(n):
    """ Construction des Theoremes F (regime 1) et G (rampe). """
    P = P_of(n)
    if n <= 2 * P:
        # Theoreme F : 0, 1^P, 2^{n-P}
        return [0] + [1] * P + [2] * (n - P)
    # Theoreme G : rampe
    r = n - 2 * P
    c = 1
    h = [(c * ((-1) ** r) * comb(w - 1, r)) % 3 if w >= 1
         else c % 3 for w in range(0, n - P + 1)]
    # h(0) = c (C(-1, r) = (-1)^r donne c) -- fixe directement :
    h[0] = c
    g = [0] * (n + 1)
    # prefixe libre [1, P-1] : choisir selon h pour compatibilite
    for j in range(1, P):
        if j <= n - P:
            g[j] = 1 if h[j] in (0, 1) else 2
        else:
            g[j] = 1
    # propagation : g(j+P) = g(j) + h(j)
    for j in range(0, n - P + 1):
        g[j + P] = (g[j] + h[j]) % 3
    return g


def main() -> None:
    print("TACHE F-011 etape 9 -- Theoreme G et loi complete OR mod 3")
    print("=" * 68)

    print("\n[A] Constructions explicites (Theoremes F et G), n = 1..26 :")
    ok = True
    for n in range(1, 27):
        g = build_g(n)
        cover = g[0] == 0 and all(v in (1, 2) for v in g[1:])
        d = mahler_degree(g)
        L = law(n)
        good = cover and d <= L
        ok &= good
        tag = "OK" if good else "*** ECHEC ***"
        print(f"    n={n:>2} : loi={L:>2}, deg(construction)={d:>2}, "
              f"couverture={'oui' if cover else 'NON'}  [{tag}]")
    print(f"\n    Bornes superieures constructives : "
          f"{'TOUTES VALIDES' if ok else 'ECHEC'}")

    # [B] croisement avec DP (borne inf deja prouvee par D+E ; ici on
    # verifie l'EGALITE complete)
    print("\n[B] Egalite complete loi == construction == DP :")
    from itertools import product as _

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

    all_eq = True
    for n in range(1, 27):
        L = law(n)
        feas_at_L = dp_feasible(1, n, L) if L + 1 <= n else True
        infeas_below = (not dp_feasible(1, n, L - 1)) if L - 1 >= 1 and L <= n else True
        eq = feas_at_L and infeas_below
        all_eq &= eq
        if not eq:
            print(f"    n={n} : PROBLEME (faisable a {L} : {feas_at_L}, "
                  f"infaisable a {L-1} : {infeas_below})")
    print(f"    n = 1..26 : {'EGALITE PARTOUT' if all_eq else 'ECHEC'}")

    print("\n" + "=" * 68)
    if ok and all_eq:
        print("LOI COMPLETE PROUVEE ET VERIFIEE :")
        print("  deg_3^sym(OR_n) = max(3^b, n - 3^b),  b = floor(log3 n)")
        print("  (borne inf : Theoremes D + E ; borne sup : Theoremes F + G)")


if __name__ == "__main__":
    main()
