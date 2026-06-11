"""
TACHE F-011, etape 26 -- THEOREME K' : la famille t = 2 * 3^k.

THEOREME K'. Soit k >= 0, t = 2 * 3^k, s = 3^k, n = 2t, et [n] = A ⊔ B
avec |A| = |B| = t. Alors
    V = e_t([n]) + e_s(A) * e_s(B)   (mod 3)
est une representation faible de THR_{t, n} sur Z_6 (purement mod 3) :
deg_6(THR_{t, 2t}) = t (la borne >= t est le Lemme 5 / Mobius).

PREUVE (3 lemmes de Lucas ; profil (a, b), w = a + b, V(a,b) =
C(w, t) + C(a, s) C(b, s) mod 3) :
 (L1) fenetre basse w in [t, t+s) VIVE : w = t + r, r < s = 3^k ; en
      base 3, t = (2, 0^k) et w = (2, digits(r)) dominent (2, 0^k) :
      C(w, t) = C(2,2) * prod C(r_i, 0) = 1 mod 3.
 (L2) fenetre haute w in [t+s, 2t] : a + b = w >= t + s et a, b <= t
      forcent a, b in [s, t] = [3^k, 2*3^k] ; le digit de position k de
      a vaut 1 ou 2 (>= 1), donc C(a, s) = C(digit, 1) in {1, 2} != 0 ;
      idem b : le produit est != 0 mod 3. Et C(w, t) = 0 (le digit de
      position k de w = 3^{k+1} + r, r <= 3^k, vaut 0 ou 1 < 2).
      Donc V = produit != 0.
 (L3) non-collision sur la fenetre basse : V = 1 + C(a,s)C(b,s) = 0
      exigerait le produit = 2, donc un facteur = 2 (digit 2 <=> a = t)
      et l'autre = 1 ; mais a = t et w < t + s donnent b = w - t < s,
      d'ou C(b, s) = 0 et produit 0 != 2. Donc V in {1, 2}.       QED

Avec le Theoreme K (t = 2^a) : DEUX familles infinies de points n = 2t
plats. Verification : t = 2, 6, 18, 54 -- les 3 lemmes + la couverture
complete par profils (+ rappel : t = 2, 6 deja verifies exhaustivement
point-par-point aux etapes 17/24-25b).
"""

from __future__ import annotations

from math import comb


def check_t(t):
    s = t // 3 if t % 3 == 0 else 1  # s = 3^k = t / 2... attention
    s = t // 2
    n = 2 * t
    ok_L1 = all((comb(t + r, t) % 3) == 1 for r in range(s))
    ok_L2 = all(
        (comb(a, s) * comb(b, s)) % 3 != 0 and comb(a + b, t) % 3 == 0
        for a in range(s, t + 1) for b in range(s, t + 1)
        if t + s <= a + b <= 2 * t)
    ok_L3 = True
    for a in range(t + 1):
        for b in range(t + 1):
            w = a + b
            if t <= w < t + s:
                V = (comb(w, t) + comb(a, s) * comb(b, s)) % 3
                if V == 0:
                    ok_L3 = False
    # couverture complete : tous profils
    ok_full = all(
        (((comb(a + b, t) + comb(a, s) * comb(b, s)) % 3) == 0)
        == (a + b < t)
        for a in range(t + 1) for b in range(t + 1))
    return ok_L1, ok_L2, ok_L3, ok_full


def main() -> None:
    print("TACHE F-011 e26 -- Theoreme K' : t = 2 * 3^k, V = e_t + e_s(A)e_s(B)")
    print("=" * 68)
    all_ok = True
    for k in range(4):
        t = 2 * 3 ** k
        l1, l2, l3, full = check_t(t)
        ok = l1 and l2 and l3 and full
        all_ok &= ok
        print(f"  k={k}, t={t:>3}, n={2*t:>3} : L1 {'OK' if l1 else 'KO'} ; "
              f"L2 {'OK' if l2 else 'KO'} ; L3 {'OK' if l3 else 'KO'} ; "
              f"couverture complete (profils) {'OK' if full else 'KO'}")
    print("=" * 68)
    if all_ok:
        print("THEOREME K' VERIFIE sur k = 0..3 (t = 2, 6, 18, 54).")
        print("deg_6(THR_{t,2t}) = t pour toute la famille t = 2*3^k --")
        print("2e famille infinie de points 2t plats (avec K : t = 2^a).")
        print("(t = 2, 6 deja verifies point-par-point, e17/e24/e25b.)")
    else:
        print("ECHEC -- voir ci-dessus.")


if __name__ == "__main__":
    main()
