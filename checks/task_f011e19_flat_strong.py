"""
TACHE F-011, etape 19 -- (a) hypothese plate a n = 10..13 ;
(b) le modele FORT mod 6 expedie en theoreme.

(a) HYPOTHESE PLATE : deg_6(MAJ_n) = t = ceil(n/2).
    Borne inf = t (Lemme 5, Mobius). Borne sup : u = 1 partout (mod 2)
    couvre {w : C(w,t) impair} ; il faut V (degre t, mod 3) avec
    V(S) != 0 pour tout S de taille dans W_fail = {w : C(w,t) pair}.
    Recherche par recuit simule (instances : 252..1716 coefficients).

(b) THEOREME L (modele fort -- bookkeeping, pas d'exploration) :
    le polynome multilineaire representant exactement une fonction
    booleenne sur Z_m est UNIQUE (Mobius) ; pour MAJ_n ses coefficients
    ne dependent que de k = |T| : mu_k = (-1)^{k-t} C(k-1, t-1) (telescope
    de l'etape 3, ici sur Z). Donc
        deg_m^fort(MAJ_n) = max{ k <= n : C(k-1, t-1) != 0 mod m }.
    Pour m = 6 : C(k-1,t-1) != 0 mod 6 ssi (t-1 sous-ensemble de k-1 en
    base 2, Lucas) ET (digits_3(t-1) <= digits_3(k-1), Lucas). Table.
"""

from __future__ import annotations

import itertools
import random
import time
from math import comb

import numpy as np

random.seed(2026)
np.random.seed(2026)


# --------------------------------------------------- (a) recuit plate

def probe_flat(n, tries=150_000, anneal_iters=2_000_000):
    t = (n + 1) // 2
    monos = list(itertools.combinations(range(n), t))
    wfail = [w for w in range(t, n + 1) if comb(w, t) % 2 == 0]
    fails = []
    for w in wfail:
        fails.extend(itertools.combinations(range(n), w))
    if not fails:
        return "trivial (W_fail vide)", None, None
    M = np.zeros((len(fails), len(monos)), dtype=np.int8)
    for r, S in enumerate(fails):
        Ss = set(S)
        for c, T in enumerate(monos):
            if set(T) <= Ss:
                M[r, c] = 1
    M64 = M.astype(np.int64)
    t0 = time.time()
    for trial in range(tries):
        v = np.random.randint(0, 3, len(monos))
        if np.all((M64 @ v) % 3 != 0):
            return f"aleatoire (essai {trial})", v, (monos, wfail)
    v = np.random.randint(0, 3, len(monos))
    vals = (M64 @ v) % 3
    cost = int((vals == 0).sum())
    for it in range(anneal_iters):
        c = random.randrange(len(monos))
        delta = random.choice((1, 2))
        dvals = (vals + delta * M64[:, c]) % 3
        ncost = int((dvals == 0).sum())
        if ncost <= cost or random.random() < 0.005:
            v[c] = (v[c] + delta) % 3
            vals = dvals
            cost = ncost
            if cost == 0:
                return (f"recuit (iter {it}, {time.time()-t0:.0f}s)", v,
                        (monos, wfail))
        if time.time() - t0 > 150:
            break
    return f"echec (cout {cost}, {time.time()-t0:.0f}s)", None, None


def verify_flat(n, v, monos):
    """ Verification exhaustive (n <= 13 : 8192 points). """
    t = (n + 1) // 2
    Tsets = [frozenset(T) for T in monos]
    vnz = [(Ts, int(c)) for Ts, c in zip(Tsets, v) if c]
    for x in range(1 << n):
        S = frozenset(i for i in range(n) if (x >> i) & 1)
        w = len(S)
        U = (comb(w, t) % 2) if w >= t else 0
        V = sum(c for Ts, c in vnz if Ts <= S) % 3
        if w < t and (U or V % 3):
            return False
        if w >= t and not (U or V % 3):
            return False
    return True


# --------------------------------------------------- (b) modele fort

def strong_degree(n, m):
    t = (n + 1) // 2
    best = None
    for k in range(t, n + 1):
        if comb(k - 1, t - 1) % m != 0:
            best = k
    return best


def lucas_ok(a, b, p):
    while a or b:
        if b % p > a % p:
            return False
        a //= p
        b //= p
    return True


def main() -> None:
    print("TACHE F-011 etape 19 -- plate n = 10..13 + modele fort")
    print("=" * 68)

    print("\n(a) Hypothese plate : deg_6(MAJ_n) = t ?")
    for n in (10, 11, 12, 13):
        t = (n + 1) // 2
        how, v, info = probe_flat(n)
        if v is not None:
            monos, wfail = info
            okv = verify_flat(n, v, monos)
            print(f"    n={n:>2} (t={t}, W_fail={wfail}, "
                  f"{len(monos)} coefs) : CERTIFICAT [{how}] ; "
                  f"verification 2^{n} points : {'OK' if okv else 'ECHEC'}",
                  flush=True)
        else:
            print(f"    n={n:>2} (t={t}) : {how} -- NON CONCLU "
                  f"(recherche incomplete)", flush=True)

    print("\n(b) Theoreme L -- degre FORT de MAJ_n mod m "
          "(= max k : C(k-1,t-1) != 0 mod m) :")
    print(f"    {'n':>3} {'t':>3} | {'mod 2':>5} {'mod 3':>5} {'mod 6':>5} | n ?")
    full = 0
    for n in range(2, 41):
        t = (n + 1) // 2
        d2, d3, d6 = (strong_degree(n, m) for m in (2, 3, 6))
        full += (d6 == n)
        if n <= 16 or d6 != n:
            print(f"    {n:>3} {t:>3} | {d2:>5} {d3:>5} {d6:>5} | "
                  f"{'= n' if d6 == n else 'CHUTE'}")
    print(f"    deg_6^fort = n (plein) pour {full}/39 valeurs de n <= 40.")
    # croisement Lucas/Kummer de la forme close :
    # C != 0 mod 6 ssi != 0 mod 2 OU != 0 mod 3 (et non ET -- corrige)
    ok = all((comb(k - 1, t - 1) % 6 != 0) ==
             (lucas_ok(k - 1, t - 1, 2) or lucas_ok(k - 1, t - 1, 3))
             for n in range(2, 41) for t in [(n + 1) // 2]
             for k in range(t, n + 1))
    print(f"    Forme close Lucas x Kummer verifiee : {'OK' if ok else 'ECHEC'}")
    print("\n    Lecture : le modele FORT reste plein ou presque (rigidite de")
    print("    l'unicite) ; le modele FAIBLE general est plat (e17-18) ; toute")
    print("    la structure composite interessante vit ENTRE les deux --")
    print("    representations a valeurs prescrites partielles, approximations.")


if __name__ == "__main__":
    main()
