"""
TACHE F-011, etape 12 -- Mesure du territoire n = 45..80, loi corrigee.

Contexte : C-F011 refutee a n = 65 (vraie valeur 40 = (3^4-1)/2, repunit
base 3). On mesure tout le territoire jamais sonde :
  - t = 23..27 (n = 45..54) : region Theoreme I/H -- prediction 27 prouvee ;
  - t = 28..32 (n = 55..64) : region Theoreme J (temoin w = 54) --
    prediction 32, SAUF n = 64 : anomalie C(64,32) = 0 mod 3, ex-C-F011
    predisait 64 -- point suspect ;
  - t = 33..40 (n = 65..80) : region refutee -- chasse a la loi v2
    (repunits (3^k-1)/2 ? valeur constante 40 ?).

Methode : enumeration CRT complete (Lemme 1) avec ELAGAGE : les poids
qu'aucun v ne couvre doivent etre couverts par u (reduction du nombre de
candidats u). Cap : dim <= 12 (3^12 = 531k).
"""

from __future__ import annotations

import itertools
import time
from math import comb

import numpy as np

DIM_CAP = 12


def t_of(n):
    return (n + 1) // 2


def feasible_mod6(n, t, d):
    idxs = list(range(t, d + 1))
    dim = len(idxs)
    if dim > DIM_CAP:
        return None
    highs = list(range(t, n + 1))
    H2 = np.array([[comb(w, i) % 2 for i in idxs] for w in highs],
                  dtype=np.int64)
    H3 = np.array([[comb(w, i) % 3 for i in idxs] for w in highs],
                  dtype=np.int64)
    U = np.array(list(itertools.product(range(2), repeat=dim)), dtype=np.int64)
    V = np.array(list(itertools.product(range(3), repeat=dim)), dtype=np.int64)
    v2 = (U @ H2.T) % 2
    nz3 = ((V @ H3.T) % 3) != 0
    # elagage : poids jamais couverts par v -> u doit les couvrir
    cov3_any = nz3.any(axis=0)
    must_u = np.where(~cov3_any)[0]
    if len(must_u):
        keep = np.all(v2[:, must_u] != 0, axis=1)
        v2 = v2[keep]
        if v2.shape[0] == 0:
            return False
    order = np.argsort((v2 == 0).sum(axis=1))
    for r in order:
        W0 = np.where(v2[r] == 0)[0]
        if len(W0) == 0:
            return True
        if bool(np.all(nz3[:, W0], axis=1).any()):
            return True
    return False


def measure(n, d_max_extra=14):
    t = t_of(n)
    for d in range(t, t + d_max_extra + 1):
        r = feasible_mod6(n, t, d)
        if r is None:
            return None, d
        if r:
            return d, None
    return None, t + d_max_extra


def repunit_candidates(lim):
    """ valeurs de la forme (3^k - 1)/2 et puissances, pour annotation """
    vals = {}
    k = 1
    while (3 ** k - 1) // 2 <= lim:
        vals[(3 ** k - 1) // 2] = f"(3^{k}-1)/2"
        k += 1
    q = 1
    while q <= lim:
        vals.setdefault(q, f"2^{q.bit_length()-1}" if (q & (q - 1)) == 0 else "")
        q *= 2
    q = 1
    while q <= lim:
        vals.setdefault(q, f"3^?")
        q *= 3
    return vals


def main() -> None:
    print("TACHE F-011 etape 12 -- mesure n = 45..80, chasse a la loi v2")
    print("=" * 68)
    ann = repunit_candidates(200)
    results = {}
    print(f"{'n':>3} {'t':>3} | {'deg_6^sym':>9} | annotation | region")
    print("-" * 68)
    for n in range(45, 81):
        t = t_of(n)
        t0 = time.time()
        val, cap = measure(n)
        q2 = 1
        while q2 < t:
            q2 *= 2
        q3 = 1
        while q3 < t:
            q3 *= 3
        if n >= max(q2, q3):
            region = "I (prouvee)"
        elif t <= 32:
            region = "J (temoin 54)" if t >= 28 else "J/autre"
        else:
            region = "REFUTEE (v2 ?)"
        if val is not None:
            results[n] = val
            note = ann.get(val, "")
            print(f"{n:>3} {t:>3} | {val:>9} | {note:>10} | {region}"
                  f"   ({time.time()-t0:.0f}s)", flush=True)
        else:
            print(f"{n:>3} {t:>3} | >cap(d<={cap}) | {'':>10} | {region}"
                  f"   ({time.time()-t0:.0f}s)", flush=True)
    print("-" * 68)
    # structure de la zone v2
    v2zone = {n: v for n, v in results.items() if t_of(n) >= 33}
    if v2zone:
        print(f"\nZone v2 (t >= 33) : {v2zone}")
        vals = sorted(set(v2zone.values()))
        print(f"Valeurs distinctes : {vals}")


if __name__ == "__main__":
    main()
