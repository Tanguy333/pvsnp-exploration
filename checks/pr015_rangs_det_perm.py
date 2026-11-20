# -*- coding: utf-8 -*-
r"""PR-015 — Contre-vérification exécutable de la candidature n° 10 (entrée de
registre E-6 : « la voie algébrique par mesures de rang, VP vs VNP »).

Implémentation INDÉPENDANTE. Mesures (définies) :
  PD_k(f)      = dim span{ ∂^k f / ∂x^S : |S| = k }        (Nisan-Wigderson 1997)
  SPD_{k,l}(f) = dim span{ x^m · ∂^k f : |m| = l, |S| = k } (partielles décalées)
Dérivées multilinéaires (S ensemble de variables) ; décalages par TOUS les
monômes de degré l (avec répétition). Rang exact sur F_p, p = 2^31 - 1,
par python-flint (nmod_mat). det_n, perm_n en n^2 variables x_ij.
Contrôle (classique, Nisan-Wigderson) : PD_k(det_n) = PD_k(perm_n) = C(n,k)^2.
Usage : python -u checks/pr015_rangs_det_perm.py [--big]
"""
import argparse
import itertools
import time
from math import comb

P = 2**31 - 1


def det_perm(n, signe):
    """dict monome(tuple trié d'indices de variables) -> coeff ; var (i,j) -> i*n+j."""
    f = {}
    for sigma in itertools.permutations(range(n)):
        inv = sum(1 for a in range(n) for b in range(a + 1, n) if sigma[a] > sigma[b])
        c = (-1) ** inv if signe else 1
        mono = tuple(sorted(i * n + sigma[i] for i in range(n)))
        f[mono] = f.get(mono, 0) + c
    return f


def deriv(f, S):
    """∂^|S| f / ∂x^S (f multilinéaire : on garde les monômes contenant S)."""
    g = {}
    Sset = set(S)
    for mono, c in f.items():
        if Sset <= set(mono):
            rest = tuple(v for v in mono if v not in Sset)
            g[rest] = g.get(rest, 0) + c
    return {m: c for m, c in g.items() if c % P}


def rang(polys):
    polys = [p for p in polys if p]
    if not polys:
        return 0
    cols = {}
    for p in polys:
        for m in p:
            if m not in cols:
                cols[m] = len(cols)
    from flint import nmod_mat
    M = nmod_mat(len(polys), len(cols), P)
    for r, p in enumerate(polys):
        for m, c in p.items():
            M[r, cols[m]] = c % P
    return M.rank()


def pd(f, nv, k):
    return rang([deriv(f, S) for S in itertools.combinations(range(nv), k)])


def spd(f, nv, k, l):
    ders = [d for d in (deriv(f, S) for S in itertools.combinations(range(nv), k)) if d]
    # dédoublonnage (à scalaire près, signe)
    uniq = {}
    for d in ders:
        key = tuple(sorted(d.items()))
        neg = tuple(sorted((m, -c) for m, c in d.items()))
        if key not in uniq and neg not in uniq:
            uniq[key] = d
    ders = list(uniq.values())
    polys = []
    for m in itertools.combinations_with_replacement(range(nv), l):
        for d in ders:
            polys.append({tuple(sorted(mono + m)): c for mono, c in d.items()})
    return rang(polys)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--big", action="store_true", help="inclure (n,k,l) = (4,2,2)")
    a = ap.parse_args()
    print("=== PD_k (contrôle : C(n,k)^2) ===", flush=True)
    for n in (3, 4, 5):
        D, Pm = det_perm(n, True), det_perm(n, False)
        row = []
        for k in range(1, n):
            x, y = pd(D, n * n, k), pd(Pm, n * n, k)
            row.append(f"k={k}: det {x} perm {y} attendu {comb(n,k)**2}")
        print(f"n={n} | " + " ; ".join(row), flush=True)
    print("\n=== SPD_{k,l} det contre perm ===", flush=True)
    cas = [(3, 1, 1), (3, 1, 2), (3, 2, 1), (3, 2, 2), (4, 1, 1), (4, 2, 1), (4, 3, 1)]
    if a.big:
        cas.append((4, 2, 2))
    for (n, k, l) in cas:
        t0 = time.time()
        D, Pm = det_perm(n, True), det_perm(n, False)
        x, y = spd(D, n * n, k, l), spd(Pm, n * n, k, l)
        print(f"(n,k,l)=({n},{k},{l}) : det {x}  perm {y}  écart {y - x}  [{time.time()-t0:.1f} s]",
              flush=True)


if __name__ == "__main__":
    main()
