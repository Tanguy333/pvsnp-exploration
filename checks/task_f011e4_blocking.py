"""
TACHE F-011, etape 4 -- Le critere de blocage est-il EXACT ?

CONJECTURE C-F011d (unifiante) : pour m in {2, 3, 6},
    deg_m^sym(THR_{t,n}) = B_m(t, n)
      := min{ d >= t : aucun w in [t, n] n'est m-bloque sur [t, d] },
ou "w est m-bloque sur [t,d]" signifie C(w,i) = 0 (mod p) pour tout
i in [t,d] et tout premier p | m.

- Sens >= (borne inferieure) : DEJA PROUVE (T-F011b, et sa version
  mono-premier identique).
- Sens <= (des qu'aucun poids unique ne bloque, une combinaison du noyau
  couvre) : C'EST la conjecture, testee ici massivement.

Si C-F011d tient : toute la loi (mod 2, 3 ET 6, toute la famille THR) se
reduit a un critere LUCAS PUR calculable en O(n^2), et il ne reste qu'un
theoreme a prouver (le sens <=).

Test : grille t = 1..10, n = t..30, m in {2, 3, 6} -- critere B_m
(combinatoire pure) vs solveur exact (noyaux + couverture).
"""

from __future__ import annotations

import itertools
from math import comb

import numpy as np

KER_CAP = 2_000_000


# ------------------------------------------------ critere de blocage (Lucas pur)

def blocked(w: int, t: int, d: int, m: int) -> bool:
    primes = [2, 3] if m == 6 else [m]
    for i in range(t, d + 1):
        c = comb(w, i)
        if not all(c % p == 0 for p in primes):
            return False
    return True


def B_criterion(t: int, n: int, m: int, d_cap: int = 40):
    for d in range(t, d_cap + 1):
        if not any(blocked(w, t, d, m) for w in range(t, n + 1)):
            return d
    return None


# ------------------------------------------------ solveur exact (etapes 1-3)

def binom_rows(n, d, p, ws):
    return np.array([[comb(w, i) % p for i in range(d + 1)] for w in ws],
                    dtype=np.int64)


def kernel_matrix(n, t, d, p):
    """ Par Lemme 1 : base = {e_i : t <= i <= d} directement. """
    idxs = list(range(t, d + 1))
    dim = len(idxs)
    if p ** dim > KER_CAP:
        return None, idxs
    coeffs = np.array(list(itertools.product(range(p), repeat=dim)),
                      dtype=np.int64)
    return coeffs, idxs


def feasible(n, t, d, m):
    highs = list(range(t, n + 1))
    if m in (2, 3):
        K, idxs = kernel_matrix(n, t, d, m)
        if K is None:
            return None
        H = np.array([[comb(w, i) % m for i in idxs] for w in highs],
                     dtype=np.int64)
        vals = (K @ H.T) % m
        return bool(np.all(vals != 0, axis=1).any())
    # m = 6 : CRT
    K2, idxs = kernel_matrix(n, t, d, 2)
    K3, _ = kernel_matrix(n, t, d, 3)
    if K2 is None or K3 is None:
        return None
    H2 = np.array([[comb(w, i) % 2 for i in idxs] for w in highs],
                  dtype=np.int64)
    H3 = np.array([[comb(w, i) % 3 for i in idxs] for w in highs],
                  dtype=np.int64)
    v2 = (K2 @ H2.T) % 2
    if bool(np.all(v2 != 0, axis=1).any()):
        return True
    nz3 = ((K3 @ H3.T) % 3) != 0
    order = np.argsort((v2 == 0).sum(axis=1))
    for r in order:
        W0 = np.where(v2[r] == 0)[0]
        if bool(np.all(nz3[:, W0], axis=1).any()):
            return True
    return False


def solver_deg(t, n, m, d_cap=30):
    for d in range(t, d_cap + 1):
        r = feasible(n, t, d, m)
        if r is None:
            return None
        if r:
            return d
    return None


# ------------------------------------------------ test massif

def main() -> None:
    print("TACHE F-011 etape 4 -- le critere de blocage est-il exact ?")
    print("=" * 68)
    stats = {m: {"ok": 0, "diff": [], "cap": 0} for m in (2, 3, 6)}
    for m in (2, 3, 6):
        for t in range(1, 11):
            for n in range(t, 31):
                B = B_criterion(t, n, m)
                S = solver_deg(t, n, m)
                if S is None or B is None:
                    stats[m]["cap"] += 1
                    continue
                if B == S:
                    stats[m]["ok"] += 1
                else:
                    stats[m]["diff"].append((t, n, B, S))
        d = stats[m]
        print(f"\nmod {m} : {d['ok']} coincidences, {len(d['diff'])} ecarts, "
              f"{d['cap']} non conclus (cap)")
        for (t, n, B, S) in d["diff"][:10]:
            print(f"    ECART : t={t}, n={n} : critere={B}, solveur={S}")

    total_ok = sum(s["ok"] for s in stats.values())
    total_diff = sum(len(s["diff"]) for s in stats.values())
    print("\n" + "=" * 68)
    if total_diff == 0:
        print(f"C-F011d : EXACTE sur les {total_ok} cellules conclues "
              f"(t <= 10, n <= 30, m = 2, 3, 6).")
        print("Borne inf : prouvee (T-F011b). Borne sup : conjecture, "
              "desormais massivement etayee.")
    else:
        print(f"C-F011d REFUTEE : {total_diff} contre-exemples "
              f"(sur {total_ok + total_diff} cellules).")


if __name__ == "__main__":
    main()
