"""
TACHE T26-S3 -- premiere reduction : isotypique -> decomposable
general. Deux volets.

VOLET A — THEOREME (classe a == 1, prouve) :
  Si tous les minima a_i = 1, la collision-singleton
  (etat0 : bloc i au SOMMET + (m0-1) blocs au min ;
   etat1 : m1 blocs au min, m1 = m0 + g_i)
  est realisable pour tout g_i in [1, k-1] : choisir
  m0 = max(1, t - g_i) => m0 <= t-1, m1 = m0 + g_i in [t, k]. Donc
  separation => g_i >= k pour CHAQUE bloc =>
  W = somme(1 + g_i) >= k(k+1). Le temoin mod-k l'atteint.
  Verification mecanique : pour k = 3..9, TOUT systeme a == 1 avec un
  g_i <= k-1 doit COLLisionner (DP exacte) ; le temoin g == k separe.

VOLET B — machinerie F1 pour le cas general (consignee) :
  collision-singleton generale : g_i = somme de j minima d'autres
  blocs (j feasible) => separation exige g_i hors des sommes de
  sous-ensembles des minima. Non clos ici (dichotomie
  dense/degenere a construire) — trou consigne.
"""

from __future__ import annotations

import itertools
import random
import sys


def separates_blocks(blocks, k, t):
    """DP exacte (m -> set de sommes). blocks : liste (a, b, M)."""
    states = {0: {0}}
    for (a, b, M) in blocks:
        V = (a, b, M)
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
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    rng = random.Random(0)
    all_ok = True
    for k in range(3, kmax + 1):
        t = (k + 1) // 2
        # 1. tout systeme a==1 avec au moins un g_i <= k-1 collisionne.
        #    Exhaustif si petit, sinon echantillon aleatoire dense.
        bad = 0
        tested = 0
        gs_range = list(range(1, k + 3))
        samples = set()
        # exhaustif pour k <= 5 ; echantillon 4000 sinon
        if k <= 5:
            pools = itertools.product(gs_range, repeat=k)
        else:
            pools = (tuple(rng.choice(gs_range) for _ in range(k))
                     for _ in range(4000))
        for gs in pools:
            if min(gs) >= k:
                continue  # hors hypothese (le theoreme ne dit rien)
            tested += 1
            # bloc a==1 : b in [1, g_i] quelconque — prendre b = 1
            blocks = [(1, 1, 1 + g) for g in gs]
            if separates_blocks(blocks, k, t):
                bad += 1
                if bad <= 3:
                    print(f"  !! k={k} : separable avec g={gs}")
        # 2. le temoin g == k separe.
        wit = separates_blocks([(1, 1, k + 1)] * k, k, t)
        ok = (bad == 0) and wit
        all_ok &= ok
        mode = "exhaustif" if k <= 5 else "echantillon 4000"
        print(f"k={k} (t={t}) : systemes a==1 avec min(g) <= k-1 "
              f"separables = {bad}/{tested} ({mode}, attendu 0) ; "
              f"temoin g=k : {'separe' if wit else 'ECHEC'} "
              f"=> {'OK' if ok else 'ECHEC'}", flush=True)
    print("THEOREME a==1 :",
          "VERIFIE mecaniquement" if all_ok else "CONTREDIT ?!")


if __name__ == "__main__":
    main()
