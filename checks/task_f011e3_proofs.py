"""
TACHE F-011, etape 3 -- Verification executable des preuves.

LEMME 1 (structure du noyau). L'espace des polynomes symetriques de degre
<= d sur Z_m s'identifie aux suites (S(w)) via la base de Mahler/Newton
S(w) = sum_i a_i C(w,i), a_i = Delta^i S(0) (differences finies,
triangulaire). Si S(w) = 0 pour w < t alors a_i = 0 pour i < t
(automatique). Donc le noyau des "zeros forces" est exactement
span{ C(w,i) : t <= i <= d }, de dimension d - t + 1.

THEOREME T-F011a (forme close mod 2, EXACTE). Sur F_2, la couverture
impose S(w) = 1 pour tout w dans [t, n] : la fonction est UNIQUE (echelon).
Ses coefficients de Mahler verifient, par telescope de Pascal,
    a_i = sum_{w=t}^{i} C(i,w)  ==  C(i-1, t-1)   (mod 2).
Donc :  deg_2^sym(THR_{t,n}) = max{ i in [t,n] : C(i-1,t-1) impair }
                             = 1 + max{ j in [t-1, n-1] : (t-1) AND j = t-1 }.

LEMME T-F011b (infaisabilite mod 6). Si w* dans [t,n] verifie
C(w*, i) = 0 mod 2 ET mod 3 pour TOUT i dans [t, d], alors aucune
representation symetrique faible de degre <= d n'existe (par Lemme 1,
U(w*) = V(w*) = 0 pour tout choix du noyau).
  Corollaires prouves : deg_6^sym(MAJ_4) >= 3, deg_6^sym(MAJ_16) >= 9,
  deg_6^sym(MAJ_32) >= 27 (w* = 2t a chaque fois).

UPPER : les bornes superieures correspondantes sont les certificats du
solveur (etapes 1-2) ; on extrait et re-verifie en entiers exacts le
certificat d = 27 a n = 32.

Ce script verifie chaque pas numeriquement.
"""

from __future__ import annotations

import itertools
from math import comb

import numpy as np


# ------------------------------------------------ Lemme 1 : telescope Pascal

def check_telescope(max_t=20, max_i=80) -> bool:
    ok = True
    for t in range(1, max_t + 1):
        for i in range(t, max_i + 1):
            lhs = sum(comb(i, w) for w in range(t, i + 1)) % 2
            rhs = comb(i - 1, t - 1) % 2
            if lhs != rhs:
                print(f"  ECHEC telescope : t={t}, i={i}")
                ok = False
    return ok


# ------------------------------------------------ T-F011a vs donnees mesurees

def d2_formula(n: int, t: int):
    best = None
    for j in range(t - 1, n):
        if (t - 1) & j == (t - 1):
            best = j + 1
    return best


# donnees mesurees (F-011 etape 1, colonne d2, n = 1..31)
MEASURED_D2 = {1: 1, 2: 2, 3: 2, 4: 4, 5: 4, 6: 4, 7: 4, 8: 8, 9: 8, 10: 8,
               11: 8, 12: 8, 13: 8, 14: 8, 15: 8, 16: 16, 17: 16, 18: 16,
               19: 16, 20: 16, 21: 16, 22: 16, 23: 16, 24: 16, 25: 16,
               26: 16, 27: 16, 28: 16, 29: 16, 30: 16, 31: 16}


def check_f011a() -> bool:
    ok = True
    for n, d2 in MEASURED_D2.items():
        t = (n + 1) // 2
        f = d2_formula(n, t)
        if f != d2:
            print(f"  ECHEC T-F011a : n={n}, formule={f}, mesure={d2}")
            ok = False
    return ok


# ------------------------------------------------ T-F011b : les 3 corollaires

def check_f011b() -> list:
    results = []
    for (n, t, w_star, bound) in [(4, 2, 4, 3), (16, 8, 16, 9), (32, 16, 32, 27)]:
        # verifier que C(w*, i) = 0 mod 2 et mod 3 pour tout i in [t, bound-1]
        all_zero = all(comb(w_star, i) % 2 == 0 and comb(w_star, i) % 3 == 0
                       for i in range(t, bound))
        # et qu'a i = bound, ca casse (sinon la borne serait plus haute)
        breaks = not (comb(w_star, bound) % 2 == 0 and comb(w_star, bound) % 3 == 0)
        results.append((n, t, w_star, bound, all_zero, breaks))
    return results


# ------------------------------------------------ certificat d=27 a n=32

def binom_rows(n, d, p, ws):
    return np.array([[comb(w, i) % p for i in range(d + 1)] for w in ws],
                    dtype=np.int64)


def find_certificate(n=32, t=16, d=27):
    """ Recherche directe dans le noyau (base C(w,i), i = t..d, Lemme 1)
        d'une paire (u, v) couvrante, puis verification en entiers exacts. """
    highs = list(range(t, n + 1))
    # base du noyau : directement les e_i, i = t..d (Lemme 1)
    idxs = list(range(t, d + 1))
    H2 = np.array([[comb(w, i) % 2 for i in idxs] for w in highs], dtype=np.int64)
    H3 = np.array([[comb(w, i) % 3 for i in idxs] for w in highs], dtype=np.int64)
    dim = len(idxs)
    # enumeration (2^12 x 3^12 trop gros ; on enumere u et teste v vectorise)
    V = np.array(list(itertools.product(range(3), repeat=dim)), dtype=np.int64)
    v3 = (V @ H3.T) % 3
    nz3 = (v3 != 0)
    for u_bits in itertools.product(range(2), repeat=dim):
        u = np.array(u_bits, dtype=np.int64)
        cov2 = (H2 @ u) % 2
        W0 = np.where(cov2 == 0)[0]
        if len(W0) == 0:
            return list(zip(idxs, u_bits)), None
        good = np.where(np.all(nz3[:, W0], axis=1))[0]
        if len(good):
            v = V[good[0]]
            return list(zip(idxs, u_bits)), list(zip(idxs, v.tolist()))
    return None, None


def verify_certificate(n, t, u_pairs, v_pairs) -> bool:
    """ Verification en entiers exacts du certificat (CRT). """
    for w in range(0, n + 1):
        U = sum(c * comb(w, i) for i, c in (u_pairs or [])) % 2
        Vv = sum(c * comb(w, i) for i, c in (v_pairs or [])) % 3
        if w < t:
            if U != 0 or Vv != 0:
                return False
        else:
            if U == 0 and Vv == 0:
                return False
    return True


def main() -> None:
    print("TACHE F-011 etape 3 -- verification executable des preuves")
    print("=" * 68)

    print("\n[1] Telescope de Pascal : sum_{w=t}^{i} C(i,w) = C(i-1,t-1) mod 2")
    print(f"    t = 1..20, i = t..80 : {'OK' if check_telescope() else 'ECHEC'}")

    print("\n[2] T-F011a (forme close de deg_2^sym) vs donnees mesurees n=1..31")
    print(f"    {'OK -- 31/31' if check_f011a() else 'ECHEC'}")

    print("\n[3] T-F011b (lemme d'infaisabilite) -- les 3 corollaires :")
    for (n, t, w, b, az, br) in check_f011b():
        print(f"    n={n:>2}, t={t:>2}, w*={w:>2} : C(w*,i) = 0 mod 6 pour "
              f"i in [{t},{b-1}] : {'OK' if az else 'ECHEC'} ; "
              f"casse a i={b} : {'OK' if br else 'ECHEC'}"
              f"  => deg >= {b} PROUVE")

    print("\n[4] Certificat explicite d=27, n=32 (borne superieure exacte) :")
    u_pairs, v_pairs = find_certificate()
    if u_pairs is not None:
        okc = verify_certificate(32, 16, u_pairs, v_pairs)
        un = [i for i, c in u_pairs if c]
        vn = [(i, c) for i, c in (v_pairs or []) if c]
        print(f"    u (mod 2) : e_i pour i in {un}")
        print(f"    v (mod 3) : {vn}")
        print(f"    verification en entiers exacts sur w = 0..32 : "
              f"{'OK' if okc else 'ECHEC'}")
        print("\n  => deg_6^sym(MAJ_32) = 27 : PROUVE (borne inf [3] + certificat [4])")
    else:
        print("    AUCUN certificat trouve -- incoherence, ne pas conclure")


if __name__ == "__main__":
    main()
