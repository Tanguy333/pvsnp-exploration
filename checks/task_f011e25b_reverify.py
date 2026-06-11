"""
TACHE F-011, etape 25b -- RE-VERIFICATION INDEPENDANTE (demande
utilisateur) des certificats n = 12 et n = 13, + contre-verification
point-par-point de n = 14.

Chemins independants de ceux d'e24/e25 :
 [A] n = 12 : (i) identite de Vandermonde -- pour tous (a, b) :
     somme_k C(a,k) C(b,6-k) c_k avec c = (1,1,1,2,1,1,1) est EGALE a
     C(a+b,6) + C(a,3) C(b,3) ; (ii) couverture de la forme close sur
     tous les profils ; (iii) sur les 4096 points : l'evaluation
     monomiale brute (somme sur les 6-sous-ensembles) coincide avec la
     forme close ET satisfait la representation faible.
 [B] n = 13 : re-resolution fraiche de la partition (4,4,5) puis
     verification exhaustive des 8192 points par un evaluateur reecrit
     (masques de bits), independant de celui d'e24c.
 [C] n = 14 : la solution (2,5,7) d'e25 est re-derivee et verifiee
     point-par-point sur les 16384 points (e25 ne verifiait que par
     profils).
"""

from __future__ import annotations

import itertools
import time
from math import comb

from task_f011e24c_n13_multi import try_partition as try_p_n13


def eval_points(n, t, coef_u, coef_v, monos):
    """ Evaluateur par masques de bits, reecrit. Retourne True si la
        representation faible est valide sur les 2^n points. """
    masks = [sum(1 << i for i in Tm) for Tm in monos]
    for x in range(1 << n):
        w = bin(x).count("1")
        U = V = 0
        for m, cu, cv in zip(masks, coef_u, coef_v):
            if (x & m) == m:
                U += cu
                V += cv
        U %= 2
        V %= 3
        if w < t and (U or V):
            return False
        if w >= t and not (U or V):
            return False
    return True


def main() -> None:
    print("TACHE F-011 e25b -- re-verification independante n = 12, 13, 14")
    print("=" * 66)

    # ------------------------------------------------ [A] n = 12
    print("\n[A] n = 12 -- forme close V(S) = C(w,6) + C(a,3)C(b,3) mod 3 :")
    c = [1, 1, 1, 2, 1, 1, 1]
    okA1 = all(
        sum(comb(a, k) * comb(b, 6 - k) * c[k] for k in range(7)) % 3
        == (comb(a + b, 6) + comb(a, 3) * comb(b, 3)) % 3
        for a in range(7) for b in range(7))
    print(f"    (i) identite de Vandermonde (49 profils) : "
          f"{'OK' if okA1 else 'ECHEC'}")
    okA2 = all(
        ((comb(a + b, 6) + comb(a, 3) * comb(b, 3)) % 3 == 0) == (a + b < 6)
        for a in range(7) for b in range(7))
    print(f"    (ii) zeros sous t et couverture au-dessus (profils) : "
          f"{'OK' if okA2 else 'ECHEC'}")
    A = set(range(6))
    monos12 = list(itertools.combinations(range(12), 6))
    cu = [0] * len(monos12)
    cv = [c[len(set(Tm) & A)] for Tm in monos12]
    t0 = time.time()
    okA3 = eval_points(12, 6, cu, cv, monos12)
    # et coincidence forme close <-> somme monomiale sur tous les points
    okA4 = True
    masks = [sum(1 << i for i in Tm) for Tm in monos12]
    maskA = sum(1 << i for i in range(6))
    for x in range(1 << 12):
        a = bin(x & maskA).count("1")
        b = bin(x).count("1") - a
        direct = sum(cv[j] for j, m in enumerate(masks) if (x & m) == m) % 3
        closed = (comb(a + b, 6) + comb(a, 3) * comb(b, 3)) % 3
        if direct != closed:
            okA4 = False
            break
    print(f"    (iii) 4096 points : representation faible "
          f"{'OK' if okA3 else 'ECHEC'} ; forme close == somme monomiale "
          f"{'OK' if okA4 else 'ECHEC'}   ({time.time()-t0:.0f}s)")

    # ------------------------------------------------ [B] n = 13
    print("\n[B] n = 13 -- re-resolution (4,4,5) + evaluateur reecrit :")
    r = try_p_n13((4, 4, 5))
    if r is None or r == "ECHEC-VERIF":
        print("    *** la re-resolution echoue ?! ***")
    else:
        parts, orbits, uk, vk = r
        monos13 = list(itertools.combinations(range(13), 7))
        def orb(Tm):
            s = set(Tm)
            return tuple(len(s & set(p)) for p in parts)
        cu = [uk[orb(Tm)] for Tm in monos13]
        cv = [vk[orb(Tm)] for Tm in monos13]
        t0 = time.time()
        okB = eval_points(13, 7, cu, cv, monos13)
        print(f"    8192 points (evaluateur independant) : "
              f"{'OK' if okB else '*** ECHEC ***'}   ({time.time()-t0:.0f}s)")

    # ------------------------------------------------ [C] n = 14
    print("\n[C] n = 14 -- re-derivation (2,5,7) + verification 16384 points :")
    from task_f011e25_ansatz_machine import try_partition as try_p_gen
    r = try_p_gen(14, 7, (2, 5, 7))
    if r is None or r == "ECHEC-VERIF":
        print("    *** la re-resolution echoue ?! ***")
    else:
        uk, vk = r
        parts = [list(range(0, 2)), list(range(2, 7)), list(range(7, 14))]
        monos14 = list(itertools.combinations(range(14), 7))
        def orb14(Tm):
            s = set(Tm)
            return tuple(len(s & set(p)) for p in parts)
        cu = [uk[orb14(Tm)] for Tm in monos14]
        cv = [vk[orb14(Tm)] for Tm in monos14]
        t0 = time.time()
        okC = eval_points(14, 7, cu, cv, monos14)
        print(f"    16384 points : {'OK' if okC else '*** ECHEC ***'}   "
              f"({time.time()-t0:.0f}s)")

    print("\n" + "=" * 66)
    print("Re-verification terminee.")


if __name__ == "__main__":
    main()
