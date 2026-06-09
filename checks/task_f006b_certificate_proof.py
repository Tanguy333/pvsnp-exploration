"""
TACHE F-006b -- VERIFICATION EXACTE du certificat diagonal (preuve de T-F006).

CERTIFICAT CANONIQUE (decouvert par le LP aux orbites a k=2,3,4) :
  Support = entrees diagonales z = (x, x), x in {0,1}^k. Poids :
    w(x) = (-1)^{|x|+1} * 2^{k-|x|}   si |x| >= 1
    w(0^k) = -(2^k - 2)
  (positif quand IP(z)=|x| mod 2 = 1 -> u ; negatif quand pair -> v ;
   tous les u, v >= 0 comme exige.)

PREUVE ANALYTIQUE (verifiee ci-dessous en arithmetique exacte) :
  1. Pour tout monome S touchant s = p+q >= 1 paires (r = k-s libres) :
     sur la diagonale, z superset S <=> x couvre les s paires touchees ;
     mu(S) = sum_{j=0}^{r} C(r,j) w_{s+j}
           = (-1)^{s+1} 2^{k-s-r} (2-1)^r = (-1)^{s+1}.       [k-s-r = 0]
  2. mu(vide) = w_0 + sum_{j>=1} C(k,j)(-1)^{j+1}2^{k-j}
              = -(2^k-2) + (2^k-1) = 1.
  3. Tous les moments dans {-1, +1} -> certificat faisable.
  4. Valeur = sum_{a impair} C(k,a) 2^{k-a} = (3^k-1)/2  [binome].
  5. Dualite faible : pour tout p reel avec p >= 1 sur IP^{-1}(1) et
     p <= 0 sur IP^{-1}(0) :
       (3^k-1)/2 <= sum_z w_z p(z) = sum_S c_S mu(S) <= sum_S |c_S|.
     Donc W_L1(IP_{2k}) >= (3^k-1)/2 sur R.   QED (avec T-F004 : egalite).

Ce script verifie en Fractions exactes :
  (A) niveau orbites, k = 1..14 : tous les moments mu(p,q) = (-1)^{p+q+1}
      (et mu(0,0) = 1), valeur = (3^k-1)/2 ;
  (B) force brute totale, k = 1..4 : tous les monomes S de [2k] un par un,
      toutes les entrees une par une (sans la reduction par orbites).
"""

from __future__ import annotations

import itertools
from fractions import Fraction
from math import comb


def w_diag(a: int, k: int) -> Fraction:
    if a == 0:
        return Fraction(-(2 ** k - 2))
    return Fraction((-1) ** (a + 1) * 2 ** (k - a))


# ------------------------------------------------- (A) niveau orbites

def verify_orbit_level(k: int) -> bool:
    ok = True
    # moments
    for s in range(0, k + 1):  # s = p+q = nombre de paires touchees
        r = k - s
        mu = sum(Fraction(comb(r, j)) * w_diag(s + j, k) for j in range(r + 1))
        expected = Fraction(1) if s == 0 else Fraction((-1) ** (s + 1))
        if mu != expected:
            print(f"    ECHEC moment : k={k}, s={s} : mu={mu}, attendu {expected}")
            ok = False
    # positivite
    for a in range(k + 1):
        wa = w_diag(a, k)
        if a % 2 == 1 and wa <= 0:
            ok = False
        if a % 2 == 0 and wa > 0:
            ok = False
    # valeur
    value = sum(Fraction(comb(k, a)) * w_diag(a, k)
                for a in range(1, k + 1, 2))
    target = Fraction(3 ** k - 1, 2)
    if value != target:
        print(f"    ECHEC valeur : k={k} : {value} != {target}")
        ok = False
    return ok


# ------------------------------------------------- (B) force brute

def ip_val(z) -> int:
    k = len(z) // 2
    return sum(z[i] * z[i + k] for i in range(k)) % 2


def verify_brute_force(k: int) -> bool:
    n = 2 * k
    inputs = list(itertools.product([0, 1], repeat=n))
    # poids par entree : nul hors diagonale
    w = {}
    for z in inputs:
        x, y = z[:k], z[k:]
        if x == y:
            w[z] = w_diag(sum(x), k)
        else:
            w[z] = Fraction(0)
    # positivite vs IP
    for z, wz in w.items():
        if wz > 0 and ip_val(z) != 1:
            return False
        if wz < 0 and ip_val(z) != 0:
            return False
    # tous les monomes
    for d in range(n + 1):
        for S in itertools.combinations(range(n), d):
            mu = sum(wz for z, wz in w.items() if all(z[j] for j in S))
            if abs(mu) > 1:
                print(f"    ECHEC brute force : k={k}, S={S} : mu={mu}")
                return False
    # valeur
    value = sum(wz for z, wz in w.items() if wz > 0)
    return value == Fraction(3 ** k - 1, 2)


def main() -> None:
    print("TACHE F-006b -- verification exacte du certificat diagonal")
    print("=" * 72)
    print("\n(A) Niveau orbites (Fractions exactes), k = 1..14 :")
    all_ok = True
    for k in range(1, 15):
        ok = verify_orbit_level(k)
        all_ok &= ok
        print(f"  k={k:2d} : moments = (-1)^(s+1) partout, mu(vide)=1, "
              f"poids signes OK, valeur = (3^k-1)/2 : {'OK' if ok else 'ECHEC'}")

    print("\n(B) Force brute integrale (tous monomes x toutes entrees), k = 1..4 :")
    for k in range(1, 5):
        ok = verify_brute_force(k)
        all_ok &= ok
        print(f"  k={k} : {'OK' if ok else 'ECHEC'}")

    print("\n" + "=" * 72)
    if all_ok:
        print("CERTIFICAT VALIDE EN ARITHMETIQUE EXACTE.")
        print("T-F006 : W_L1(IP_{2k}) = (3^k-1)/2 = DNF_min(IP_{2k}), sur R,")
        print("pour tout k -- borne sup par p* (T-F004), borne inf par le")
        print("certificat diagonal + dualite faible. O-F002 est un THEOREME.")
    else:
        print("ECHEC -- ne pas conclure.")


if __name__ == "__main__":
    main()
