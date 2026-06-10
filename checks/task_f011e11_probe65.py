"""
TACHE F-011, etape 11 -- C-F011 en territoire non teste : le sondage n = 65.

DECOUVERTE (preparation) : le mecanisme du Theoreme J ne s'etend PAS au
regime t = 33..40 (n = 65..80, q2 = 64, q3 = 81) :
  tout w in [64, 80] a digit_27(w) = 2, donc 54 = (2,0,0,0)_3 est un
  sous-ensemble de Lucas de w : C(w, 54) != 0 mod 3, et 54 in [t, 63].
  => aucun temoin Lucas-mort pour d >= 54 ; et a n = 65, 66 les temoins
  ne couvrent que d <= 35 (36 est sous-ensemble de 64, 65 et 66).
Or C-F011 predit deg_6^sym(MAJ_65) = L1(33) = 64 : la borne inferieure
au-dela de d = 35 n'a AUCUNE preuve, et la loi n'a jamais ete testee ici
(donnees etape 1 : n <= 44). C-F011 est donc en danger a n = 65.

Ce script :
  [A] verifie l'analyse des temoins par degre (t = 33, n = 65) :
      pour chaque d, liste les w in [64, 65] Lucas-morts sur [33, d] ;
  [B] teste la faisabilite mod 6 a n = 65, t = 33, d = 33..42
      (enumeration CRT vectorisee : noyau mod 2 (dim d-32) x noyau mod 3) ;
      - si FAISABLE a un d <= 42 : C-F011 REFUTEE (valeur < 64) ;
      - sinon : la loi survit au sondage ; d in [43, 63] reste indecidable
        avec nos outils (noyaux trop grands), documente honnetement.
"""

from __future__ import annotations

import itertools
import time
from math import comb

import numpy as np

T, N = 33, 65
KER_CAP = 80_000_000  # paires u x v


def lucas_dead_witnesses(t, n, q2):
    """ [A] pour chaque d, les w in [q2, n] avec w-q2 < t et
        C(w,i) = 0 mod 3 pour tout i in [t, d]. """
    out = {}
    for d in range(t, q2):
        ws = [w for w in range(q2, n + 1)
              if w - q2 < t and all(comb(w, i) % 3 == 0 for i in range(t, d + 1))]
        out[d] = ws
    return out


def feasible_mod6(n, t, d):
    """ Enumeration CRT complete (Lemme 1 : noyaux = degres [t, d]). """
    idxs = list(range(t, d + 1))
    dim = len(idxs)
    if (2 ** dim) * (3 ** dim) > KER_CAP * 64:
        return None
    highs = list(range(t, n + 1))
    H2 = np.array([[comb(w, i) % 2 for i in idxs] for w in highs],
                  dtype=np.int64)
    H3 = np.array([[comb(w, i) % 3 for i in idxs] for w in highs],
                  dtype=np.int64)
    U = np.array(list(itertools.product(range(2), repeat=dim)), dtype=np.int64)
    V = np.array(list(itertools.product(range(3), repeat=dim)), dtype=np.int64)
    v2 = (U @ H2.T) % 2          # |U| x W
    nz3 = ((V @ H3.T) % 3) != 0  # |V| x W
    # tri des u par nombre de zeros croissant
    order = np.argsort((v2 == 0).sum(axis=1))
    for r in order:
        W0 = np.where(v2[r] == 0)[0]
        if len(W0) == 0:
            return True
        if bool(np.all(nz3[:, W0], axis=1).any()):
            return True
    return False


def main() -> None:
    print(f"TACHE F-011 etape 11 -- sondage de C-F011 a n = {N} (t = {T})")
    print("=" * 68)
    q2 = 64

    print(f"\n[A] Temoins Lucas-morts par degre (w in [{q2}, {N}]) :")
    dead = lucas_dead_witnesses(T, N, q2)
    last_d_with = max((d for d, ws in dead.items() if ws), default=None)
    for d in sorted(dead):
        if d <= 38 or dead[d]:
            print(f"    d = {d} : {dead[d] if dead[d] else 'AUCUN'}")
    print(f"    Dernier d avec temoin : {last_d_with} "
          f"(=> borne inf par J limitee a deg >= {last_d_with + 1 if last_d_with else '?'})")

    print(f"\n[B] Faisabilite mod 6 a n = {N}, t = {T} (CRT complet) :")
    verdict = None
    for d in range(T, 43):
        t0 = time.time()
        r = feasible_mod6(N, T, d)
        lab = ('FAISABLE' if r else ('>cap' if r is None else 'infaisable'))
        print(f"    d = {d} : {lab}   ({time.time()-t0:.0f}s)", flush=True)
        if r:
            verdict = d
            break

    print("\n" + "=" * 68)
    if verdict is not None:
        print(f"*** C-F011 REFUTEE : deg_6^sym(MAJ_65) <= {verdict} < 64 ***")
        print("La loi etait un artefact du domaine n <= 44.")
    else:
        print("C-F011 survit au sondage (infaisable jusqu'a d = 42).")
        print("Region d in [43, 63] : INDECIDABLE avec nos outils (noyaux")
        print("3^31 max) et SANS preuve de borne inf -- statut honnete :")
        print("la loi est non testee et non prouvee dans cette region.")


if __name__ == "__main__":
    main()
