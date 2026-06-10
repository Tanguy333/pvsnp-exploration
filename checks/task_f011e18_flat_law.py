"""
TACHE F-011, etape 18 -- Le theoreme anomalie-tueur et la sonde MAJ_9.

LEMME 5 (Mobius, general -- analogue exact du Lemme 1) :
  un polynome multilineaire sur Z_m s'annule sur TOUS les points de poids
  < t ssi ses coefficients sur les monomes de degre < t sont nuls
  (inversion de Mobius triangulaire sur le treillis des parties).
  COROLLAIRE : deg_6(THR_{t,n}) >= t toujours.

THEOREME K (anomalie-tueur) : pour t = 2^a et n = 2t,
    deg_6(THR_{t,2t}) = t.
  Construction : c_T = 3 pour tout t-sous-ensemble T != T0, c_{T0} = 1
  (i.e. u = 1 mod 2 partout, v = x_{T0} mod 3).
  - w < t : 0 (support de degre t) ;
  - w in [t, 2t-1] : P(S) = 3 C(w,t) - 2 [T0 c S] = 3 ou 1 mod 6
    (C(w,t) impair pour w in [2^a, 2^{a+1}) par Lucas) : != 0 ;
  - w = 2t : P = 3 C(2t,t) - 2 = -2 = 4 mod 6 (C(2t,t) pair, Kummer) : != 0.
  TOUTES les anomalies symetriques (3, 9, 27 prouvees aux etapes 3-10)
  s'effondrent a t dans le modele general : deg_6(MAJ_4) = 2,
  deg_6(MAJ_16) = 8, deg_6(MAJ_32) = 16.

HYPOTHESE PLATE (a tester) : deg_6(MAJ_n) = ceil(n/2) pour tout n.
  Premier test non trivial : MAJ_9 (t = 5, sym = 8). Suffit de trouver
  une forme V de degre 5 mod 3 (126 coefficients) avec V(S) != 0 pour
  tout S de taille dans W_fail = {6, 8, 9} (la ou C(w,5) est pair --
  le mod 2 u = 1 couvre w = 5, 7).
  Recherche : aleatoire + recuit simule (3^126 hors enumeration).

Ce script :
  [A] verifie le Theoreme K exhaustivement pour t = 2, 4, 8 (tous les
      2^n points) et par forme close pour t = 16 ;
  [B] cherche le certificat MAJ_9 (random + recuit) ; si trouve, le
      verifie en exact et conclut deg_6(MAJ_9) = 5.
"""

from __future__ import annotations

import itertools
import random
import time
from math import comb

import numpy as np

random.seed(2026)
np.random.seed(2026)


# ------------------------------------------------------- [A] Theoreme K

def check_theorem_k(t):
    n = 2 * t
    T0 = frozenset(range(t))
    bad = []
    for x in range(1 << n):
        S = [i for i in range(n) if (x >> i) & 1]
        w = len(S)
        # P(S) = sum_{T c S, |T| = t} c_T avec c_{T0} = 1, autres = 3
        cnt = comb(w, t) if w >= t else 0
        inT0 = 1 if T0.issubset(S) else 0
        val = (3 * cnt - 2 * inT0) % 6
        if w < t and val != 0:
            bad.append(x)
        if w >= t and val == 0:
            bad.append(x)
    return not bad


def check_theorem_k_closed(t):
    n = 2 * t
    for w in range(0, n + 1):
        cnt = comb(w, t) if w >= t else 0
        for inT0 in ([0] if w < t else [0, 1] if w < n else [1]):
            val = (3 * cnt - 2 * inT0) % 6
            if w < t and val != 0:
                return False
            if w >= t and val == 0:
                # verifier que ce cas (w, inT0) est realisable
                if w >= t and not (inT0 == 0 and w == n):
                    return False
    return True


# ------------------------------------------------------- [B] sonde MAJ_9

def probe_maj9(tries=400_000, anneal_iters=300_000):
    n, t = 9, 5
    monos = list(itertools.combinations(range(n), t))   # 126
    fails = []
    for w in (6, 8, 9):
        fails.extend(itertools.combinations(range(n), w))
    # matrice d'incidence : ligne = ensemble S de W_fail, colonne = monome
    M = np.zeros((len(fails), len(monos)), dtype=np.int64)
    for r, S in enumerate(fails):
        Ss = set(S)
        for c, T in enumerate(monos):
            if set(T) <= Ss:
                M[r, c] = 1
    # 1) essais aleatoires
    t0 = time.time()
    for trial in range(tries):
        v = np.random.randint(0, 3, len(monos))
        if np.all((M @ v) % 3 != 0):
            return v, monos, f"aleatoire (essai {trial}, {time.time()-t0:.0f}s)"
    # 2) recuit : minimiser le nombre de S a somme nulle
    v = np.random.randint(0, 3, len(monos))
    vals = (M @ v) % 3
    cost = int((vals == 0).sum())
    best = cost
    for it in range(anneal_iters):
        c = random.randrange(len(monos))
        delta = random.choice((1, 2))
        nv = (v[c] + delta) % 3
        dvals = (vals + delta * M[:, c]) % 3
        ncost = int((dvals == 0).sum())
        if ncost <= cost or random.random() < 0.01:
            v[c] = nv
            vals = dvals
            cost = ncost
            best = min(best, cost)
            if cost == 0:
                return v, monos, f"recuit (iter {it}, {time.time()-t0:.0f}s)"
    return None, monos, f"echec (meilleur cout : {best} ensembles non couverts)"


def verify_maj9(v, monos):
    n, t = 9, 5
    T0sets = [set(T) for T in monos]
    for x in range(1 << n):
        S = {i for i in range(n) if (x >> i) & 1}
        w = len(S)
        U = (comb(w, t) % 2) if w >= t else 0          # u = 1 partout
        V = sum(int(c) for c, Ts in zip(v, T0sets) if Ts <= S) % 3
        ok = (U != 0) or (V != 0)
        if w < t and (U != 0 or V != 0):
            return False
        if w >= t and not ok:
            return False
    return True


def main() -> None:
    print("TACHE F-011 etape 18 -- theoreme anomalie-tueur + sonde MAJ_9")
    print("=" * 68)

    print("\n[A] Theoreme K : deg_6(THR_{t,2t}) = t pour t = 2^a")
    for t in (2, 4, 8):
        r = check_theorem_k(t)
        print(f"    t = {t:>2} (n = {2*t}, 2^{2*t} points, exhaustif) : "
              f"{'OK' if r else 'ECHEC'}", flush=True)
    print(f"    t = 16 (forme close sur les poids) : "
          f"{'OK' if check_theorem_k_closed(16) else 'ECHEC'}")
    print("    => deg_6(MAJ_4) = 2, deg_6(MAJ_16) = 8, deg_6(MAJ_32) = 16 :")
    print("       les anomalies symetriques (3, 9, 27) s'effondrent toutes.")

    print("\n[B] Sonde de l'hypothese plate : deg_6(MAJ_9) = 5 ?")
    print("    (sym = 8 ; W_fail = {6, 8, 9} ; 126 coefficients mod 3)")
    v, monos, how = probe_maj9()
    if v is not None:
        okv = verify_maj9(v, monos)
        nz = int((v != 0).sum())
        print(f"    CERTIFICAT TROUVE ({how}) : {nz}/126 coefficients non nuls")
        print(f"    verification exhaustive sur les 512 points : "
              f"{'OK' if okv else 'ECHEC'}")
        if okv:
            print("\n    => deg_6(MAJ_9) = 5 = t : l'hypothese plate tient ici,")
            print("       et le gain general vs symetrique est 5 vs 8.")
    else:
        print(f"    Pas de certificat ({how}) -- non conclu : la recherche")
        print("    est incomplete (3^126), l'hypothese plate reste ouverte a n=9.")


if __name__ == "__main__":
    main()
