"""
TACHE T26-S1 (v2) -- explorer le SURVIT du Tour 26 : le sous-lemme
W_dec(MAJ_k(OR2^k)) >= k(k+1), par recherche exhaustive.

v1 (resultats acquis, runs du 2026-07-23) : k = 3, 4, 5 CONFIRMES
exhaustivement (12, 20, 30) — contre-validation des certificats
CP-SAT du Tour 26 par methode independante. k = 6 explosait.

v2 — trois accelerations :
  1. DP INCREMENTALE : l'etat (m -> ensemble de sommes) est maintenu
     le long du DFS (push/pop), plus de recalcul aux feuilles.
  2. ELAGAGE PARTIEL SAIN : si les j blocs deja choisis produisent
     une collision (somme d'un compte m >= t = somme d'un compte
     m' < t), la branche entiere est morte — car les k-j blocs
     restants peuvent rester non satisfaits (valeur 0, compte +0),
     donc toute collision partielle survit au systeme complet.
  3. APPROFONDISSEMENT ITERATIF sur le poids total : W = 2k, 2k+1,
     ..., k(k+1) ; le premier W realisable est l'OPTIMUM exact.

Classe : p_i = a x + b y + c xy, a, b >= 1, c >= 0 (a <= b par
symetrie du bloc), blocs echangeables (multiset, poids croissants).
"""

from __future__ import annotations

import sys
import time


def dfs_exact_weight(k, t, W_target, triples_by_w):
    """Existe-t-il un multiset de k triples de poids total exact
    W_target qui separe ? DP incrementale + elagage partiel."""
    # triples_by_w : liste (w, (a,b,c)) triee par w croissant
    n_tr = len(triples_by_w)

    # etat DP : liste de dicts m -> set de sommes ; pile pour pop
    state = {0: {0}}
    stack = [state]

    def push(tr):
        a, b, c = tr
        V = (a, b, a + b + c)
        cur = stack[-1]
        new = {}
        for m, sums in cur.items():
            new.setdefault(m, set()).update(sums)
            tgt = new.setdefault(m + 1, set())
            for s in sums:
                tgt.add(s + V[0])
                tgt.add(s + V[1])
                tgt.add(s + V[2])
        stack.append(new)

    def pop():
        stack.pop()

    def collision():
        cur = stack[-1]
        ones, zeros = set(), set()
        for m, sums in cur.items():
            (ones if m >= t else zeros).update(sums)
        return bool(ones & zeros)

    found = [None]

    def rec(j, idx, remaining):
        if j == k:
            if remaining == 0 and not collision():
                found[0] = True
                return True
            return False
        for i in range(idx, n_tr):
            w, tr = triples_by_w[i]
            # bornes : chaque bloc suivant pese >= w
            if w * (k - j) > remaining:
                break
            # atteignabilite : les k-j blocs a >= w chacun, total = remaining
            # (borne sup par bloc : remaining - (k-j-1)*w)
            push(tr)
            if collision():
                pop()
                continue
            if rec(j + 1, i, remaining - w):
                pop()
                return True
            pop()
        return False

    return rec(0, 0, W_target)


def optimum(k, verbose=True):
    t = (k + 1) // 2
    target = k * (k + 1)
    wmax = target - 2 * (k - 1)  # un bloc peut au plus porter le reste
    triples = []
    for w in range(2, wmax + 1):
        for a in range(1, w):
            for b in range(a, w - a + 1):
                c = w - a - b
                if c >= 0:
                    triples.append((w, (a, b, c)))
    triples.sort()
    t0 = time.time()
    for W in range(2 * k, target + 1):
        tw = time.time()
        ok = dfs_exact_weight(k, t, W, triples)
        if verbose:
            print(f"    k={k} W={W} : {'REALISABLE' if ok else 'vide'}"
                  f"  ({time.time()-tw:.0f}s)", flush=True)
        if ok:
            verdict = ("= k(k+1), LOI CONFIRMEE" if W == target
                       else f"< {target} : SOUS-LEMME MORT")
            print(f"k={k} : W_dec = {W} {verdict}  "
                  f"(total {time.time()-t0:.0f}s)", flush=True)
            return W
    print(f"k={k} : rien jusqu'a {target} ?! (bug probable — le "
          f"temoin mod-k devrait realiser {target})", flush=True)
    return None


def main():
    ks = [int(a) for a in sys.argv[1:]] or [6]
    for k in ks:
        optimum(k)


if __name__ == "__main__":
    main()
