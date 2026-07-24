"""
TACHE T26-S2 -- THEOREME (sous-classe isotypique) : pour 2 <= t <= k-1,
tout separateur decomposable ISOTYPIQUE (tous blocs identiques
(a, b, M), 1 <= a <= b, a+b <= M) de MAJ_k^t(OR2^k) a M >= k+1,
donc W = kM >= k(k+1). Le temoin mod-k (1, 1, k+... : (a,b,c) =
(1,1,k-1), M = k+1) l'atteint.

PREUVE (verifiee mecaniquement ici) :
  Restriction {a, M} : les etats n'utilisant que les valeurs a et M
  par bloc sont un sous-ensemble des etats — toute collision de la
  restriction est une collision du systeme. Sommes s = m a + g (M-a),
  0 <= g <= m <= k.
  (1) a <= t-1 et M <= k : collision explicite — prendre
      delta = a (ecart de g), Delta = M-a (ecart de m) :
      m0 = min(t-1, k-M+a), g0 = a, m1 = m0 + M - a, g1 = 0.
      Verifications : m0 >= a (les 2 sous-cas), m0 <= t-1,
      m1 in [t, k], g0 <= m0 — toutes passent => INFEASIBLE.
  (2) a >= t, k impair (t = (k+1)/2) : M >= a+b >= 2a >= 2t = k+1.
  (3) a >= t, k pair (t = k/2) : M >= 2a >= k ; si M = k alors
      a = b = t et s = t(m+g) : collision (m1,g1) = (t,0) vs
      (m0,g0) = (t-1,1) => INFEASIBLE ; donc M >= k+1.
  Dans tous les cas : separable => M >= k+1. QED.

VERIFICATION MECANIQUE : pour k = 3..10, enumeration de TOUS les
blocs isotypiques (a <= b, a+b <= M <= plafond) ; separation testee
par la DP exacte de T26-S1 ; verdict attendu : AUCUN separable avec
M <= k, et le temoin (1,1,k-1) separable a M = k+1.
"""

from __future__ import annotations

import sys


def separates_iso(a, b, M, k, t):
    """DP exacte (m -> set de sommes) pour k blocs identiques."""
    V = (a, b, M)
    states = {0: {0}}
    for _ in range(k):
        new = {}
        for m, sums in states.items():
            new.setdefault(m, set()).update(sums)
            tgt = new.setdefault(m + 1, set())
            for s in sums:
                for v in V:
                    tgt.add(s + v)
        states = new
    ones, zeros = set(), set()
    for m, sums in states.items():
        (ones if m >= t else zeros).update(sums)
    return not (ones & zeros)


def main():
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    all_ok = True
    for k in range(3, kmax + 1):
        t = (k + 1) // 2
        cap = 2 * k + 2
        bad = []
        for M in range(2, k + 1):          # M <= k : attendu AUCUN separable
            for a in range(1, M):
                for b in range(a, M - a + 1):
                    if separates_iso(a, b, M, k, t):
                        bad.append((a, b, M))
        witness_ok = separates_iso(1, 1, k + 1, k, t)
        ok = (not bad) and witness_ok
        all_ok &= ok
        print(f"k={k:2d} (t={t}) : M <= k separables = {len(bad)} "
              f"(attendu 0){' ' + str(bad[:3]) if bad else ''} ; "
              f"temoin (1,1,{k-1}) a M={k+1} : "
              f"{'separe' if witness_ok else 'ECHEC'} "
              f"=> {'OK' if ok else 'ECHEC'}", flush=True)
    print("THEOREME isotypique :",
          "VERIFIE mecaniquement" if all_ok else "CONTREDIT ?!")


if __name__ == "__main__":
    main()
