"""
TOUR 27 — suite (T27-S1, Refuteur) : fermeture de la CLASSE B pour
MAJ_5(OR2^5), fenetre [20, 30]. VERSION 2.

v1 : DFS naif — C = 1 depassait deja 480 s. v2 : architecture de la
classe A generalisee au niveau variable :
  1. enumerer les CONFIGURATIONS CROISEES canoniques : placements de
     C unites sur les 40 paires croisees, quotientes par le groupe
     G = S_5 (blocs) x S_2^5 (swaps intra) — canonicalisation par
     orbite brute (3840 elements) ;
  2. pour chaque configuration : recherche des triples intra par
     APPROFONDISSEMENT ITERATIF sur le poids intra exact (0 ..
     29 - C), DFS bloc par bloc, elagage partiel sain (blocs
     restants vides => croises inactifs, collisions partielles
     survivent), etats (m, valeur, etat exact des blocs).
Chaque niveau C ferme = theoreme partiel ; temoin => refutation.
"""

from __future__ import annotations

import itertools
import sys
import time

K, T, CAP = 5, 3, 29
# paires croisees : ((i, vi), (j, vj)) i < j, vi/vj in {0 (x), 1 (y)}
CROSS = []
for i, j in itertools.combinations(range(K), 2):
    for vi in (0, 1):
        for vj in (0, 1):
            CROSS.append((i, vi, j, vj))
CIDX = {c: n for n, c in enumerate(CROSS)}

# groupe G : permutations des blocs x swaps par bloc
GROUP = []
for perm in itertools.permutations(range(K)):
    for swaps in itertools.product((0, 1), repeat=K):
        GROUP.append((perm, swaps))


def act(gperm, gswap, cfg):
    """Action de g sur une config croisee (tuple de 40 coefs)."""
    out = [0] * len(CROSS)
    for n, (i, vi, j, vj) in enumerate(CROSS):
        if cfg[n] == 0:
            continue
        ni, nj = gperm[i], gperm[j]
        nvi = vi ^ gswap[i]
        nvj = vj ^ gswap[j]
        if ni > nj:
            ni, nj, nvi, nvj = nj, ni, nvj, nvi
        out[CIDX[(ni, nvi, nj, nvj)]] += cfg[n]
    return tuple(out)


def canonical(cfg):
    return min(act(p, s, cfg) for (p, s) in GROUP)


def gen_cross_configs(C):
    """Configurations canoniques de cout croise exact C."""
    seen = set()
    out = []

    def comp(rest, idx, cur):
        if idx == len(CROSS) - 1:
            cur.append(rest)
            c = canonical(tuple(cur))
            if c not in seen:
                seen.add(c)
                out.append(c)
            cur.pop()
            return
        for v in range(rest + 1):
            cur.append(v)
            comp(rest - v, idx + 1, cur)
            cur.pop()

    comp(C, 0, [])
    return out


def search_intra(cfg, intra_total, deadline):
    """Existe-t-il des triples intra de poids total EXACT intra_total
    separant, avec la config croisee cfg ? DFS + elagage partiel."""
    # croises par (bloc j, etat j, bloc i, etat i) precalcules :
    # cadd[j][stj][i][sti] = somme des coefs actifs
    def var_active(v, st):  # v : 0=x, 1=y ; st : 1=x, 2=y, 3=xy
        return (st in (1, 3)) if v == 0 else (st in (2, 3))
    cadd = [[[[0] * 4 for _ in range(K)] for _ in range(4)]
            for _ in range(K)]
    for n, (i, vi, j, vj) in enumerate(CROSS):
        c = cfg[n]
        if c == 0:
            continue
        for sti in (1, 2, 3):
            for stj in (1, 2, 3):
                if var_active(vi, sti) and var_active(vj, stj):
                    cadd[j][stj][i][sti] += c

    # dernier bloc touche par un croise (en canonique : les premiers)
    touched = [j for j in range(K)
               if any(cadd[j][st][i][si]
                      for st in (1, 2, 3) for i in range(K)
                      for si in (1, 2, 3))
               or any(cadd[l][st][j][si]
                      for l in range(K) for st in (1, 2, 3)
                      for si in (1, 2, 3))]
    last_touched = max(touched) if touched else -1

    def dfs(j, states, left, prev_free):
        """states : apres last_touched, ensembles de (m, val) dedupes ;
        avant, liste (m, val, sigma). prev_free : tuple (w,a,b,g) du
        dernier bloc libre (ordre multiset des blocs > last_touched)."""
        if time.time() > deadline:
            raise TimeoutError
        ones, zeros = set(), set()
        for s in states:
            m, val = s[0], s[1]
            (ones if m >= T else zeros).add(val)
        if ones & zeros:
            return False
        if j == K:
            return left == 0
        free = j > last_touched
        for w in range(0, left + 1):
            if j == K - 1 and w != left:
                continue
            for a in range(0, w + 1):
                for b in range(0, w - a + 1):
                    g = w - a - b
                    if free and prev_free is not None \
                            and (w, a, b, g) < prev_free:
                        continue  # ordre multiset des blocs libres
                    if free:
                        # etats dedupes (m, val) — plus de sigma
                        new = set()
                        for s in states:
                            m, val = s[0], s[1]
                            new.add((m, val))
                            for base in (a, b, a + b + g):
                                new.add((m + 1, val + base))
                    else:
                        new = []
                        for (m, val, sigma) in states:
                            new.append((m, val, sigma + (0,)))
                            for st, base in ((1, a), (2, b),
                                             (3, a + b + g)):
                                cr = 0
                                row = cadd[j][st]
                                for i in range(j):
                                    si = sigma[i]
                                    if si:
                                        cr += row[i][si]
                                new.append((m + 1, val + base + cr,
                                            sigma + (st,)))
                        if j == last_touched:
                            new = {(m, val) for (m, val, _) in new}
                    if dfs(j + 1, new, left - w,
                           (w, a, b, g) if free else None):
                        return True
        return False

    return dfs(0, [(0, 0, ())], intra_total, None)


def close_level(C, tl_level):
    t0 = time.time()
    deadline = t0 + tl_level
    cfgs = gen_cross_configs(C)
    print(f"  C={C} : {len(cfgs)} configurations canoniques "
          f"({time.time()-t0:.0f}s)", flush=True)
    for W_int in range(0, CAP - C + 1):
        for cfg in cfgs:
            try:
                if search_intra(cfg, W_int, deadline):
                    print(f"  C={C} : TEMOIN ! poids {C + W_int}, "
                          f"config {[(CROSS[n], v) for n, v in enumerate(cfg) if v]}")
                    return "TEMOIN"
            except TimeoutError:
                print(f"  C={C} : NON CLOS (budget {tl_level:.0f}s, "
                      f"atteint W_intra = {W_int})", flush=True)
                return "TIMEOUT"
    print(f"  C={C} : VIDE — aucun temoin <= {CAP} "
          f"({time.time()-t0:.0f}s)", flush=True)
    return "VIDE"


def main():
    tl_level = float(sys.argv[1]) if len(sys.argv) > 1 else 480.0
    cmax = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    closed = []
    for C in range(1, cmax + 1):
        r = close_level(C, tl_level)
        if r == "VIDE":
            closed.append(C)
        else:
            break
    if closed:
        print(f"CLASSE B fermee pour C in {{1..{closed[-1]}}} : "
              f"aucun separateur <= {CAP}.", flush=True)


if __name__ == "__main__":
    main()
