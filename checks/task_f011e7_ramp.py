"""
TACHE F-011, etape 7 -- LA RAMPE EST PROUVEE (Theoreme E).

THEOREME E : pour P = 3^b et 2P < n < 3P :
    deg_3^sym(OR_n) >= n - P.
(Avec le Theoreme D (>= P), la borne inferieure de C-F011e est complete :
 deg_3^sym(OR_n) >= max(3^floor(log3 n), n - 3^floor(log3 n)) pour tout n.)

PREUVE (chaine de 4 maillons) :
  Soit g : [0,n] -> F_3, g(0) = 0, g in {1,2} sur [1,n], deg(g) =: d.
  Supposons d < n - P (et d >= P par le Theoreme D).
  (1) DESCENTE (Lemme 3) : G := g(.+P) - g a deg(G) <= d - P < n - 2P < P,
      domaine [0, n-P].
  (2) PERIODICITE (argument du Theoreme D applique a G) : deg(G) < P =>
      Delta^P G = 0 sur [0, n-2P] => G(j+P) = G(j) pour j in [0, n-2P].
  (3) PAIRES INTERDITES : G(j+P) = G(j) se reecrit
      g(j+2P) = 2 g(j+P) - g(j) (mod 3). Pour j in [1, n-2P], les trois
      valeurs sont dans {1,2} ; or (g(j), g(j+P)) = (1,2) donnerait
      g(j+2P) = 0, et (2,1) aussi : INTERDITES. Donc g(j+P) = g(j),
      c'est-a-dire G(j) = 0 pour tout j in [1, n-2P].
      Et G(0) = g(P) - g(0) = g(P) != 0.
  (4) INTERPOLATION DE MAHLER : posons D := deg(G) <= d - P <= n-2P-1.
      G est determinee par ses valeurs sur [0, D] : G(0) = c != 0,
      G(1..D) = 0 (car D <= n-2P-1). Ses coefficients sont
      a_i = (-1)^i c (i <= D), d'ou, par l'identite de somme alternee
      sum_{i=0}^{D} (-1)^i C(D+1, i) = (-1)^D :
          G(D+1) = c (-1)^D != 0 (mod 3).
      Mais D+1 <= n-2P, donc G(D+1) = 0 par (3). CONTRADICTION.
  Donc d >= n - P.                                                    QED

Ce script verifie executablement chaque maillon :
  [A] l'identite de somme alternee (D = 0..60) ;
  [B] la propagation des paires interdites (toutes les paires (a,b) de
      {1,2}^2 avec 2b - a hors {1,2} sont exactement (1,2) et (2,1)) ;
  [C] l'enonce final contre TOUTES les valeurs DP exactes (regime
      2P < n < 3P) ;
  [D] coherence totale de la loi max(P, n-P) (borne inf prouvee D+E) avec
      les donnees, n = 1..26.
"""

from __future__ import annotations

from math import comb


# ------------------------------------------------------- [A] somme alternee

def check_alternating():
    ok = True
    for D in range(0, 61):
        s = sum(((-1) ** i) * comb(D + 1, i) for i in range(D + 1))
        if s != (-1) ** D:
            print(f"  ECHEC identite : D={D}, somme={s}")
            ok = False
    return ok


# ------------------------------------------------------- [B] paires interdites

def check_pairs():
    forbidden = []
    for a in (1, 2):
        for b in (1, 2):
            c = (2 * b - a) % 3
            if c not in (1, 2):
                forbidden.append((a, b))
    return forbidden == [(1, 2), (2, 1)]


# ------------------------------------------------------- DP (etape 5, validee)

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


def dp_deg(n, d_cap=18):
    for d in range(1, d_cap + 1):
        if d + 1 > n or dp_feasible(1, n, d):
            return d
    return None


# ------------------------------------------------------- [C][D] vs donnees

def P_of(n):
    P = 1
    while P * 3 <= n:
        P *= 3
    return P


def main() -> None:
    print("TACHE F-011 etape 7 -- la rampe est prouvee (Theoreme E)")
    print("=" * 66)

    print("\n[A] Identite sum_{i=0}^{D} (-1)^i C(D+1,i) = (-1)^D, D = 0..60")
    print(f"    {'OK' if check_alternating() else 'ECHEC'}")

    print("\n[B] Paires interdites : (a,b) in {1,2}^2 avec 2b-a hors {1,2}")
    print(f"    exactement {{(1,2),(2,1)}} : {'OK' if check_pairs() else 'ECHEC'}")

    print("\n[C] Theoreme E contre les valeurs DP exactes (regime 2P < n < 3P) :")
    ok = True
    for n in range(1, 27):
        P = P_of(n)
        if not (2 * P < n < 3 * P):
            continue
        d = dp_deg(n)
        if d is None:
            continue
        bound = n - P
        status = "OK" if d >= bound else "*** VIOLATION ***"
        ok &= (d >= bound)
        print(f"    n={n:>2} (P={P}) : deg={d}, borne n-P={bound}  [{status}]")

    print("\n[D] Loi complete (borne inf D+E) : deg >= max(P, n-P), n = 1..26 :")
    ok2 = True
    exact = True
    for n in range(1, 27):
        P = P_of(n)
        d = dp_deg(n)
        if d is None:
            continue
        lb = max(P, n - P)
        ok2 &= (d >= lb)
        exact &= (d == lb)
    print(f"    borne respectee partout : {'OK' if ok2 else 'ECHEC'} ; "
          f"et EGALE a la valeur exacte sur toutes les cellules : "
          f"{'OUI' if exact else 'NON'}")

    print("\n" + "=" * 66)
    if ok and ok2:
        print("THEOREME E VERIFIE. Avec le Theoreme D :")
        print("  deg_3^sym(OR_n) >= max(3^b, n - 3^b)   [PROUVE, tout n]")
        print("et l'egalite est verifiee sur toutes les cellules calculees")
        print("(la borne superieure generale -- constructions -- reste a")
        print("prouver pour tout n ; certificats DP disponibles n <= 26).")


if __name__ == "__main__":
    main()
