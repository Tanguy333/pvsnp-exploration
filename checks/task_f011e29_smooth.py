"""
TACHE F-011, etape 29 -- formes closes t = 12 + CONJECTURE 3-LISSE.

[1] FORMES CLOSES (t = 12, etablies depuis les certificats MaxSAT e28) :
    n = 24, P = (7, 17) :
      U(a,b) = C(b,12) + a C(b,11)                  (mod 2)
      V(a,b) = 2 C(a+b,12) - C(b,12) - C(a,7) C(b,5) (mod 3)
    n = 23, P = (8, 15) :
      U(a,b) = somme_{k=1}^{8} C(a,k) C(b,12-k)
             = C(a+b,12) - C(b,12)                   (mod 2)
      V(a,b) = C(b,12) + C(a,3) C(b,9) + 2 C(a,8) C(b,4) (mod 3)
    Verification : identites de Vandermonde + couverture sur tous les
    profils (et zeros sous t automatiques par support).

[2] CONJECTURE 3-LISSE : a n = 2t, une solution bipartite-invariante
    existe ssi t = 2^a 3^b (3-lisse).
    Donnees actuelles : solubles {2, 4, 6, 8, 9, 12} (tous 3-lisses) ;
    insolubles {7, 10, 11} (aucun 3-lisse).
    PREDICTIONS A TESTER : t = 3 (lisse -> soluble), t = 5 (non lisse ->
    insoluble), t = 13 (non lisse -> insoluble). Balayage de TOUTES les
    bipartitions de [2t] par mini-SAT.
"""

from __future__ import annotations

import time
from math import comb

from task_f011e25_ansatz_machine import try_partition


def check_closed_forms():
    ok24 = True
    for a in range(8):
        for b in range(18):
            w = a + b
            U = (comb(b, 12) + a * comb(b, 11)) % 2
            V = (2 * comb(w, 12) - comb(b, 12)
                 - comb(a, 7) * comb(b, 5)) % 3
            # croisement avec la definition par orbites (Vandermonde)
            U2 = sum(c * comb(a, k) * comb(b, 12 - k)
                     for k, c in [(0, 1), (1, 1)]) % 2
            vks = {0: 1, 1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 1}
            V2 = sum(vks[k] * comb(a, k) * comb(b, 12 - k)
                     for k in range(8)) % 3
            if U != U2 or V != V2:
                return False, f"identite n=24 ({a},{b})"
            if (w < 12 and (U or V)) or (w >= 12 and not (U or V)):
                ok24 = False
                return False, f"couverture n=24 ({a},{b})"
    for a in range(9):
        for b in range(16):
            w = a + b
            U = (comb(w, 12) - comb(b, 12)) % 2
            U2 = sum(comb(a, k) * comb(b, 12 - k) for k in range(1, 9)) % 2
            V = (comb(b, 12) + comb(a, 3) * comb(b, 9)
                 + 2 * comb(a, 8) * comb(b, 4)) % 3
            if U != U2:
                return False, f"identite n=23 ({a},{b})"
            if (w < 12 and (U or V)) or (w >= 12 and not (U or V)):
                return False, f"couverture n=23 ({a},{b})"
    return True, "OK"


def bipartite_solvable(t):
    n = 2 * t
    for sa in range(1, t + 1):
        r = try_partition(n, t, (sa, n - sa))
        if r is not None and r != "ECHEC-VERIF":
            return sa
    return None


def smooth3(t):
    while t % 2 == 0:
        t //= 2
    while t % 3 == 0:
        t //= 3
    return t == 1


def main() -> None:
    print("TACHE F-011 e29 -- formes closes t = 12 + conjecture 3-lisse")
    print("=" * 66)

    print("\n[1] Formes closes des certificats t = 12 :")
    ok, msg = check_closed_forms()
    print(f"    n = 23 et 24 (identites + couverture, tous profils) : "
          f"{'OK' if ok else 'ECHEC : ' + msg}")

    print("\n[2] Conjecture 3-lisse (bipartite-soluble a n = 2t ssi "
          "t = 2^a 3^b) :")
    all_match = True
    for t in range(3, 14):
        t0 = time.time()
        sa = bipartite_solvable(t)
        pred = smooth3(t)
        obs = sa is not None
        match = (pred == obs)
        all_match &= match
        print(f"    t = {t:>2} ({'3-lisse' if pred else 'non-lisse'}) : "
              f"{'soluble (|A| = ' + str(sa) + ')' if obs else 'insoluble'}"
              f"   [{'CONFORME' if match else '*** CONTRE-EXEMPLE ***'}]"
              f"   ({time.time()-t0:.0f}s)", flush=True)
    print("\n" + "=" * 66)
    if all_match:
        print("CONJECTURE 3-LISSE : conforme sur tout t = 3..13.")
        print("Les familles K (2^a) et K' (2*3^k) sont les cas extremes ;")
        print("la conjecture predit des constructions bipartites pour TOUT")
        print("t 3-lisse -- et leur impossibilite sinon (tripartitions+).")
    else:
        print("CONTRE-EXEMPLE trouve -- la conjecture 3-lisse est fausse.")


if __name__ == "__main__":
    main()
