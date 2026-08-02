"""
MC-001, strategie C (mc001-inverse) — PRESUMER MinSYM+ FACILE et chercher
l'algorithme.

W(f) = min somme(a_S), a_S entiers >= 0 sur les monomes positifs non vides,
tel que {p(x): f(x)=1} et {p(x): f(x)=0} soient disjoints (format SYM+ du
depot, A-013).

Sous-commandes :
  exact       : tables exhaustives de W pour n=2,3,4 (enumeration SANS
                solveur, branch-and-bound), sauvegarde .npy
  valide      : validation croisee vs D-005 (stats publiees) + CP-SAT du depot
  invariants  : batterie d'invariants poly(N)-calculables ; test de
                DETERMINATION (un invariant, ou le n-uplet complet,
                determine-t-il W ?) sur n=3 (254 f) et n=4 (65534 f)
  strata      : W vs mecanisme couverture unilaterale (les deux orientations) ;
                fraction ou l'arithmetique bat / est le seul mecanisme
  sym         : fonctions symetriques — l'optimum est-il symetrique a n<=4 ?
  lp          : (i) vacuite de la relaxation LP naturelle (numerique),
                (ii) gap LP/ILP de la couverture unilaterale (n=3 exhaustif,
                n=4 classes), (iii) relaxation aux coefficients REELS W_R
                (MILP HiGHS : a_S continus, orientations binaires) sur la
                batterie du depot, y compris MAJ3(OR2^3) et AND2(MAJ3^2) a n=6
"""

from __future__ import annotations

import itertools
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


# ----------------------------------------------------------------------
# outils communs
# ----------------------------------------------------------------------

def popcount(x: int) -> int:
    return bin(x).count("1")


def fvec_of_mask(mask: int, n: int):
    return [(mask >> e) & 1 for e in range(1 << n)]


def up_masks(n: int):
    """UP[S] = bitmask (sur les 2^n entrees) des x avec S subset x."""
    N = 1 << n
    UP = [0] * N
    for S in range(N):
        m = 0
        for x in range(N):
            if x & S == S:
                m |= 1 << x
        UP[S] = m
    return UP


# ----------------------------------------------------------------------
# calcul exact de W : enumeration branch-and-bound SANS solveur
# (meme principe que checks/task_a013_refutation_facteur_n.py :
#  masques en ordre croissant => p(S) definitif des que a_S pose)
# ----------------------------------------------------------------------

def w_exact(fvec, n: int, budget_max=None):
    """W(f) exact par approfondissement iteratif. Retourne (W, temoin)."""
    N = 1 << n
    if all(fvec) or not any(fvec):
        return 0, {}
    if budget_max is None:
        budget_max = N - 1          # borne universelle (temoin injectif)
    masks = list(range(1, N))
    SUP = [[X for X in range(N) if X & S == S] for S in range(N)]
    # singletons forces : f(e_i) != f(0) => a_{i} >= 1
    forced = [1 if (popcount(S) == 1 and fvec[S] != fvec[0]) else 0
              for S in range(N)]
    # forced_after[idx] = somme des forces d'indice >= idx (elagage)
    forced_after = [0] * (N + 1)
    for i in range(N - 2, -1, -1):
        forced_after[i] = forced_after[i + 1] + forced[masks[i]]

    for budget in range(0, budget_max + 1):
        pv = [0] * N
        uns, zeros = set(), set()
        (uns if fvec[0] else zeros).add(0)
        witness = {}
        found = [False]

        def dfs(idx, weight):
            if found[0]:
                return
            if weight + forced_after[idx] > budget:
                return
            if idx == N - 1:
                found[0] = True
                return
            S = masks[idx]
            base = pv[S]
            mine, other = (uns, zeros) if fvec[S] else (zeros, uns)
            for c in range(forced[S], budget - weight + 1):
                v = base + c
                if v in other:
                    continue
                added = v not in mine
                if added:
                    mine.add(v)
                if c:
                    witness[S] = c
                    for X in SUP[S]:
                        pv[X] += c
                dfs(idx + 1, weight + c)
                if c:
                    del witness[S]
                    for X in SUP[S]:
                        pv[X] -= c
                if added:
                    mine.discard(v)
                if found[0]:
                    # restaure le temoin au vol
                    if c:
                        witness[S] = c
                    return

        dfs(0, 0)
        if found[0]:
            return budget, dict(witness)
    return None, None


def reverifie(fvec, witness, n):
    """Re-verification INDEPENDANTE d'un temoin (enumeration complete)."""
    uns, zeros = set(), set()
    for x in range(1 << n):
        v = sum(c for S, c in witness.items() if x & S == S)
        (uns if fvec[x] else zeros).add(v)
    return not (uns & zeros)


# ----------------------------------------------------------------------
# classes canoniques (S_n x complementation de f) — vectorise numpy
# ----------------------------------------------------------------------

def canonical_map(n: int):
    """array c[mask] = representant canonique, pour tous les 2^(2^n) masques."""
    N = 1 << n
    M = 1 << N
    masks = np.arange(M, dtype=np.int64)
    bits = ((masks[:, None] >> np.arange(N)[None, :]) & 1).astype(np.int64)
    pow2 = (1 << np.arange(N)).astype(np.int64)
    best = np.full(M, M, dtype=np.int64)
    for perm in itertools.permutations(range(n)):
        # entree x -> entree image pi(x)
        pi = np.zeros(N, dtype=np.int64)
        for x in range(N):
            img = 0
            for i in range(n):
                if (x >> i) & 1:
                    img |= 1 << perm[i]
            pi[x] = img
        # bit x du nouveau masque = bit de l'entree dont l'image est x
        inv = np.argsort(pi)
        packed = bits[:, inv] @ pow2
        best = np.minimum(best, packed)
        best = np.minimum(best, (M - 1) - packed)
    return best


def compute_exact(n: int):
    N = 1 << n
    M = 1 << N
    t0 = time.time()
    canon = canonical_map(n)
    reps, inv_idx, counts = np.unique(canon, return_inverse=True,
                                      return_counts=True)
    print(f"n={n} : {M} fonctions -> {len(reps)} classes "
          f"({time.time()-t0:.0f}s)", flush=True)
    Wrep = np.zeros(len(reps), dtype=np.int64)
    t0 = time.time()
    for k, rep in enumerate(reps):
        f = fvec_of_mask(int(rep), n)
        w, wit = w_exact(f, n)
        assert w is not None
        if w > 0:
            assert reverifie(f, wit, n), f"temoin faux pour {rep}"
        Wrep[k] = w
        if k % 200 == 0:
            print(f"  classe {k}/{len(reps)} ({time.time()-t0:.0f}s)",
                  flush=True)
    Wall = Wrep[inv_idx]
    np.save(os.path.join(HERE, f"mc001_W_n{n}.npy"), Wall)
    print(f"n={n} : W calcule pour les {M} fonctions "
          f"({time.time()-t0:.0f}s), sauve.", flush=True)
    # distribution
    vals, cnts = np.unique(Wall, return_counts=True)
    print(f"  distribution W -> effectif : "
          f"{dict(zip(vals.tolist(), cnts.tolist()))}", flush=True)
    return Wall


# ----------------------------------------------------------------------
# invariants poly(N)
# ----------------------------------------------------------------------

def anf_stats(mask, n):
    """(sparsite ANF sur monomes non vides, degre GF2)."""
    N = 1 << n
    a = [(mask >> x) & 1 for x in range(N)]
    for i in range(n):
        b = 1 << i
        for x in range(N):
            if x & b:
                a[x] ^= a[x ^ b]
    nz = [S for S in range(1, N) if a[S]]
    deg = max((popcount(S) for S in range(N) if a[S]), default=0)
    return len(nz), deg


def mobius_stats(mask, n):
    """Mobius sur Z : (nb de coefs non nuls S!=vide, L1, degre reel)."""
    N = 1 << n
    c = [(mask >> x) & 1 for x in range(N)]
    for i in range(n):
        b = 1 << i
        for x in range(N):
            if x & b:
                c[x] -= c[x ^ b]
    nz = [S for S in range(1, N) if c[S]]
    L1 = sum(abs(c[S]) for S in nz)
    deg = max((popcount(S) for S in range(N) if c[S]), default=0)
    return len(nz), L1, deg


def alternance(mask, n):
    """alt(f) : nb max d'alternances de f le long d'une chaine croissante."""
    N = 1 << n
    A = [0] * N
    for x in range(1, N):
        best = 0
        fx = (mask >> x) & 1
        for i in range(n):
            if (x >> i) & 1:
                y = x ^ (1 << i)
                fy = (mask >> y) & 1
                cand = A[y] + (1 if fx != fy else 0)
                if cand > best:
                    best = cand
        A[x] = best
    return A[N - 1]


def sensibilite(mask, n):
    N = 1 << n
    s = 0
    for x in range(N):
        fx = (mask >> x) & 1
        c = sum(1 for i in range(n) if ((mask >> (x ^ (1 << i))) & 1) != fx)
        s = max(s, c)
    return s


def and_matrix_stats(mask, n):
    """M[x,y] = f(x AND y) : (rang reel, rang GF2, nb lignes distinctes)."""
    N = 1 << n
    AT = np.bitwise_and(np.arange(N)[:, None], np.arange(N)[None, :])
    fv = np.array(fvec_of_mask(mask, n))
    Mx = fv[AT]
    rr = int(np.linalg.matrix_rank(Mx))
    # rang GF2 : lignes en entiers
    rows = [int(sum((Mx[i, j] & 1) << j for j in range(N))) for i in range(N)]
    r2 = 0
    basis = []
    for r in rows:
        for b in basis:
            r = min(r, r ^ b)
        if r:
            basis.append(r)
            r2 += 1
    ndr = len(set(map(tuple, Mx.tolist())))
    return rr, r2, ndr


def min_ones(mask, n):
    """nb d'elements minimaux de f^-1(1) pour subset."""
    N = 1 << n
    has_below = [False] * N   # existe un 1 strictement en dessous
    cnt = 0
    for x in range(N):
        hb = False
        for i in range(n):
            if (x >> i) & 1:
                y = x ^ (1 << i)
                if ((mask >> y) & 1) or has_below[y]:
                    hb = True
                    break
        has_below[x] = hb
        if ((mask >> x) & 1) and not hb:
            cnt += 1
    return cnt


# --- implicants premiers et DNF minimale (exacts, petits n) ---

def _terms(n):
    """tous les termes a litteraux : (vars_mask, pattern) -> bitmask entrees."""
    out = []
    for vs in range(1 << n):
        idx = [i for i in range(n) if (vs >> i) & 1]
        for bits in range(1 << len(idx)):
            pat = 0
            for j, i in enumerate(idx):
                if (bits >> j) & 1:
                    pat |= 1 << i
            m = 0
            for x in range(1 << n):
                if (x & vs) == pat:
                    m |= 1 << x
            out.append((vs, pat, m))
    return out


_TERM_CACHE = {}


def dnf_min(mask, n):
    """(nb d'implicants premiers, taille DNF minimale) — exact."""
    N = 1 << n
    full = (1 << N) - 1
    if mask == 0:
        return 0, 0
    if mask == full:
        return 1, 1   # terme vide
    if n not in _TERM_CACHE:
        _TERM_CACHE[n] = _terms(n)
    terms = _TERM_CACHE[n]
    impl = [(vs, pat, m) for (vs, pat, m) in terms if m & ~mask == 0]
    impl_set = {(vs, pat) for (vs, pat, m) in impl}
    primes = []
    for vs, pat, m in impl:
        prime = True
        for i in range(n):
            if (vs >> i) & 1:
                if (vs ^ (1 << i), pat & ~(1 << i)) in impl_set:
                    prime = False
                    break
        if prime:
            primes.append(m)
    # couverture exacte minimale des uns par les primes (B&B)
    best = [len(primes) + 1]

    def bb(cover, used, cands):
        if used >= best[0]:
            return
        rest = mask & ~cover
        if rest == 0:
            best[0] = used
            return
        # element le moins couvrable
        x = (rest & -rest).bit_length() - 1
        for j, m in enumerate(cands):
            if m >> x & 1:
                bb(cover | m, used + 1, cands)

    bb(0, 0, primes)
    return len(primes), best[0]


# --- couverture unilaterale (zeros -> {0}) ---

def w_unilateral(mask, n, UP):
    """min couverture des uns par monomes legaux (up-cube subset uns),
    None si infaisable. = poids minimal du stratum unilateral (F-021)."""
    N = 1 << n
    ones_mask = mask
    legal = [S for S in range(1, N) if UP[S] & ~ones_mask == 0]
    if not legal:
        return None
    cover_of = {S: UP[S] for S in legal}
    # chaque un doit etre couvert
    for x in range(N):
        if (mask >> x) & 1:
            if not any(x & S == S for S in legal):
                return None
    best = [len(legal) + 1]

    def bb(cov, used):
        if used >= best[0]:
            return
        rest = ones_mask & ~cov
        if rest == 0:
            best[0] = used
            return
        x = (rest & -rest).bit_length() - 1
        for S in legal:
            if x & S == S:
                bb(cov | cover_of[S], used + 1)

    bb(0, 0)
    return best[0] if best[0] <= len(legal) else None


def compute_invariants(n):
    N = 1 << n
    M = 1 << N
    W = np.load(os.path.join(HERE, f"mc001_W_n{n}.npy"))
    UP = up_masks(n)
    t0 = time.time()
    rows = {}
    keys = ("anf", "deg2", "mobnnz", "mobL1", "degR", "alt", "sens",
            "rankR", "rank2", "ndr", "minones", "npi", "dnfmin",
            "wuni", "nones")
    data = {k: np.zeros(M, dtype=np.int64) for k in keys}
    for mask in range(M):
        anf, d2 = anf_stats(mask, n)
        mn, L1, dR = mobius_stats(mask, n)
        rr, r2, ndr = and_matrix_stats(mask, n)
        npi, dm = dnf_min(mask, n)
        wu = w_unilateral(mask, n, UP)
        data["anf"][mask] = anf
        data["deg2"][mask] = d2
        data["mobnnz"][mask] = mn
        data["mobL1"][mask] = L1
        data["degR"][mask] = dR
        data["alt"][mask] = alternance(mask, n)
        data["sens"][mask] = sensibilite(mask, n)
        data["rankR"][mask] = rr
        data["rank2"][mask] = r2
        data["ndr"][mask] = ndr
        data["minones"][mask] = min_ones(mask, n)
        data["npi"][mask] = npi
        data["dnfmin"][mask] = dm
        data["wuni"][mask] = -1 if wu is None else wu
        data["nones"][mask] = popcount(mask)
        if mask % 8192 == 0 and mask:
            print(f"  {mask}/{M} ({time.time()-t0:.0f}s)", flush=True)
    np.savez(os.path.join(HERE, f"mc001_inv_n{n}.npz"), W=W, **data)
    print(f"invariants n={n} : OK ({time.time()-t0:.0f}s)", flush=True)


def determination(n):
    """Chaque invariant (symetrise par complementation) determine-t-il W ?"""
    N = 1 << n
    M = 1 << N
    z = np.load(os.path.join(HERE, f"mc001_inv_n{n}.npz"))
    W = z["W"]
    full = M - 1
    nonconst = [m for m in range(M) if m != 0 and m != full]
    names = [k for k in z.files if k != "W"]

    def sym_key(arr, m):
        a, b = int(arr[m]), int(arr[full ^ m])
        return (a, b) if a <= b else (b, a)

    print(f"\n=== n={n} : test de determination "
          f"({len(nonconst)} fonctions non constantes) ===")
    results = []
    for name in names:
        arr = z[name]
        groups = {}
        for m in nonconst:
            groups.setdefault(sym_key(arr, m), set()).add(int(W[m]))
        bad = {k: v for k, v in groups.items() if len(v) > 1}
        # temoin
        wit = ""
        if bad:
            k0 = next(iter(bad))
            ex = [m for m in nonconst if sym_key(arr, m) == k0][:6]
            wit = (f"ex cle {k0} : masques {ex[:2]} "
                   f"avec W {sorted(bad[k0])}")
        results.append((name, len(groups), len(bad), wit))
        print(f"  {name:8s} : {len(groups):5d} classes de valeur, "
              f"{len(bad):5d} AMBIGUES "
              f"{'<-- determine W' if not bad else ''}")
    # n-uplet complet
    groups = {}
    for m in nonconst:
        key = tuple(sym_key(z[name], m) for name in names)
        groups.setdefault(key, set()).add(int(W[m]))
    bad = {k: v for k, v in groups.items() if len(v) > 1}
    print(f"  N-UPLET COMPLET ({len(names)} invariants) : "
          f"{len(groups)} classes, {len(bad)} AMBIGUES "
          f"{'<-- determine W' if not bad else '<-- NE determine PAS W'}")
    if bad:
        k0 = next(iter(bad))
        ex = [m for m in nonconst
              if tuple(sym_key(z[name], m) for name in names) == k0]
        print(f"    temoin : masques {ex[:4]}, W = "
              f"{[int(W[m]) for m in ex[:4]]}")
        for m in ex[:2]:
            print(f"    f={m:0{N}b} W={int(W[m])} "
                  + " ".join(f"{nm}={int(z[nm][m])}" for nm in names))
    # egalites exactes
    print(f"  -- egalites exactes (fraction des non constantes) --")
    for name in names:
        arr = z[name]
        eq = sum(1 for m in nonconst if int(arr[m]) == int(W[m]))
        eqs = sum(1 for m in nonconst
                  if min(int(arr[m]) if int(arr[m]) >= 0 else 10**9,
                         int(arr[full ^ m]) if int(arr[full ^ m]) >= 0
                         else 10**9) == int(W[m]))
        print(f"    W == {name:8s}: {eq:6d} ({100.0*eq/len(nonconst):5.1f}%)"
              f"   W == min(sym): {eqs:6d} ({100.0*eqs/len(nonconst):5.1f}%)")
    # theoreme W >= alt : verification
    alt = z["alt"]
    viol = [m for m in nonconst if int(W[m]) < int(alt[m])]
    print(f"  verification du theoreme W >= alt : "
          f"{'OK, 0 violation' if not viol else f'VIOLE : {viol[:5]}'}")
    ratios = [int(W[m]) / int(alt[m]) for m in nonconst if int(alt[m]) > 0]
    print(f"  ratio W/alt : max = {max(ratios):.1f}, "
          f"mediane = {sorted(ratios)[len(ratios)//2]:.2f}")


# ----------------------------------------------------------------------
# strata : la part de l'arithmetique
# ----------------------------------------------------------------------

def strata(n):
    N = 1 << n
    M = 1 << N
    full = M - 1
    z = np.load(os.path.join(HERE, f"mc001_inv_n{n}.npz"))
    W, wuni = z["W"], z["wuni"]
    nonconst = [m for m in range(M) if m != 0 and m != full]
    stats = {"aucun_stratum": 0, "W_egal_couvert": 0,
             "W_strict_meilleur": 0, "W_pire": 0}
    temoins = []
    for m in nonconst:
        wu_f = int(wuni[m])
        wu_c = int(wuni[full ^ m])
        cands = [w for w in (wu_f, wu_c) if w >= 0]
        w = int(W[m])
        if not cands:
            stats["aucun_stratum"] += 1
        else:
            best = min(cands)
            if w == best:
                stats["W_egal_couvert"] += 1
            elif w < best:
                stats["W_strict_meilleur"] += 1
                if len(temoins) < 5:
                    temoins.append((m, w, best))
            else:
                stats["W_pire"] += 1   # impossible (couvert = separateur)
    print(f"\n=== n={n} : strata ({len(nonconst)} fonctions) ===")
    tot = len(nonconst)
    for k, v in stats.items():
        print(f"  {k:18s}: {v:6d} ({100.0*v/tot:5.1f}%)")
    if temoins:
        print(f"  temoins W < couvert : {temoins}")
    if stats["W_pire"]:
        print("  !! INCOHERENCE : couvert < W — bug quelque part")


# ----------------------------------------------------------------------
# fonctions symetriques : l'optimum est-il symetrique ?
# ----------------------------------------------------------------------

def w_sym_min(levels, n):
    """min poids d'un separateur SYMETRIQUE (b_j copies de chaque monome
    de taille j, poids b_j*C(n,j)) pour f symetrique donnee par levels."""
    from math import comb
    budget_max = (1 << n) - 1
    best = [None]
    cost = [comb(n, j) for j in range(1, n + 1)]

    def dfs(j, b, weight):
        if best[0] is not None and weight >= best[0]:
            return
        if j > n:
            vals = [sum(comb(k, jj) * b[jj - 1] for jj in range(1, n + 1))
                    for k in range(n + 1)]
            uns = {vals[k] for k in range(n + 1) if levels[k]}
            zer = {vals[k] for k in range(n + 1) if not levels[k]}
            if not (uns & zer):
                best[0] = weight
            return
        c = 0
        while weight + c * cost[j - 1] <= budget_max and (
                best[0] is None or weight + c * cost[j - 1] < best[0]):
            b.append(c)
            dfs(j + 1, b, weight + c * cost[j - 1])
            b.pop()
            c += 1

    dfs(1, [], 0)
    return best[0]


def sym_check(n):
    N = 1 << n
    W = np.load(os.path.join(HERE, f"mc001_W_n{n}.npy"))
    print(f"\n=== n={n} : fonctions symetriques ===")
    for lv in range(1 << (n + 1)):
        levels = [(lv >> k) & 1 for k in range(n + 1)]
        if all(levels) or not any(levels):
            continue
        mask = 0
        for x in range(N):
            if levels[popcount(x)]:
                mask |= 1 << x
        ws = w_sym_min(levels, n)
        w = int(W[mask])
        tag = "=" if ws == w else f"  OPTIMUM NON SYMETRIQUE (W={w} < {ws})"
        print(f"  niveaux {''.join(map(str,levels))} : W={w} Wsym={ws} {tag}")


# ----------------------------------------------------------------------
# LP / MILP
# ----------------------------------------------------------------------

def build_pairs(fvec, n):
    N = 1 << n
    ones = [x for x in range(N) if fvec[x]]
    zeros = [x for x in range(N) if not fvec[x]]
    return ones, zeros


def w_real_milp(fvec, n, UB, integers=False, relax_all=False, tl=180.0):
    """min somme a_S, a_S >= 0 (continus, ou entiers si integers),
    d_{xy} binaires d'orientation (ou relaxes [0,1] si relax_all),
    |p(x)-p(y)| >= 1 pour toute paire mixte. Big-M = UB+1, avec
    contrainte somme a <= UB (l'optimum entier UB est realisable)."""
    from scipy.optimize import milp, LinearConstraint, Bounds
    from scipy.sparse import lil_matrix
    N = 1 << n
    monos = list(range(1, N))
    nm = len(monos)
    ones, zeros = build_pairs(fvec, n)
    pairs = [(x, y) for x in ones for y in zeros]
    npair = len(pairs)
    nv = nm + npair
    Mbig = UB + 1
    # incidence : entree x -> indices de monomes actifs
    act = {x: [j for j, S in enumerate(monos) if x & S == S]
           for x in range(N)}
    A = lil_matrix((2 * npair + 1, nv))
    lb = np.zeros(2 * npair + 1)
    ub = np.full(2 * npair + 1, np.inf)
    for k, (x, y) in enumerate(pairs):
        # p(x) - p(y) + M d >= 1
        for j in act[x]:
            A[2 * k, j] += 1
        for j in act[y]:
            A[2 * k, j] -= 1
        A[2 * k, nm + k] = Mbig
        lb[2 * k] = 1
        # p(y) - p(x) + M (1-d) >= 1  <=>  p(y)-p(x) - M d >= 1 - M
        for j in act[y]:
            A[2 * k + 1, j] += 1
        for j in act[x]:
            A[2 * k + 1, j] -= 1
        A[2 * k + 1, nm + k] = -Mbig
        lb[2 * k + 1] = 1 - Mbig
    # somme a <= UB
    for j in range(nm):
        A[2 * npair, j] = 1
    lb[2 * npair] = 0
    ub[2 * npair] = UB
    c = np.concatenate([np.ones(nm), np.zeros(npair)])
    integrality = np.concatenate([
        np.full(nm, 1 if integers else 0),
        np.zeros(npair) if relax_all else np.ones(npair)])
    bounds = Bounds(np.zeros(nv),
                    np.concatenate([np.full(nm, np.inf), np.ones(npair)]))
    res = milp(c=c, constraints=LinearConstraint(A.tocsr(), lb, ub),
               integrality=integrality, bounds=bounds,
               options={"time_limit": tl})
    return res


def lp_unilateral(mask, n, UP):
    """LP de couverture du stratum unilateral. None si infaisable."""
    from scipy.optimize import linprog
    N = 1 << n
    legal = [S for S in range(1, N) if UP[S] & ~mask == 0]
    ones = [x for x in range(N) if (mask >> x) & 1]
    if not legal or not ones:
        return None
    rows = []
    for x in ones:
        row = [-1.0 if x & S == S else 0.0 for S in legal]
        if all(v == 0.0 for v in row):
            return None
        rows.append(row)
    res = linprog(c=[1.0] * len(legal), A_ub=rows, b_ub=[-1.0] * len(ones),
                  bounds=[(0, None)] * len(legal), method="highs")
    return res.fun if res.success else None


def lp_gap_unilateral(n):
    """gap LP/ILP de la couverture unilaterale sur les classes canoniques."""
    N = 1 << n
    M = 1 << N
    full = M - 1
    UP = up_masks(n)
    z = np.load(os.path.join(HERE, f"mc001_inv_n{n}.npz"))
    wuni = z["wuni"]
    canon = canonical_map(n)
    reps = np.unique(canon)
    worst = (1.0, None)
    feas = 0
    for rep in reps:
        for m in (int(rep), full ^ int(rep)):
            if int(wuni[m]) < 0:
                continue
            lpv = lp_unilateral(m, n, UP)
            if lpv is None:
                continue
            feas += 1
            gap = int(wuni[m]) / lpv if lpv > 1e-9 else float("inf")
            if gap > worst[0]:
                worst = (gap, (m, int(wuni[m]), lpv))
    print(f"n={n} : {feas} (classe, orientation) unilateralement faisables ; "
          f"gap LP/ILP maximal = {worst[0]:.3f}"
          + (f" atteint par {worst[1]}" if worst[1] else ""))


# --- batterie nommee ---

def named_functions():
    """(nom, n, fvec, W_connu_ou_None)"""
    out = []

    def add(name, n, pred, w=None):
        out.append((name, n, [1 if pred(z) else 0 for z in range(1 << n)], w))

    for n in (3, 4):
        add(f"PARITY_{n}", n, lambda z: popcount(z) % 2 == 1)
        add(f"MAJ_{n}", n, lambda z, n=n: popcount(z) > n // 2)
        add(f"AND_{n}", n, lambda z, n=n: z == (1 << n) - 1)
        add(f"OR_{n}", n, lambda z: z != 0)
        add(f"NOR_{n}", n, lambda z: z == 0)
        add(f"THR2_{n}", n, lambda z: popcount(z) >= 2)
    add("IP_4", 4, lambda z: (((z & 1) & ((z >> 1) & 1))
                              ^ (((z >> 2) & 1) & ((z >> 3) & 1))) == 1)
    add("AND(OR2^2)", 4, lambda z: (z & 3) != 0 and (z >> 2) != 0, 4)
    add("XOR(OR2^2)", 4, lambda z: ((z & 3) != 0) != ((z >> 2) != 0), 6)
    # n = 6
    def maj3or2(z):
        blocs = sum(1 for i in range(3) if (z >> (2 * i)) & 3)
        return blocs >= 2
    add("MAJ3(OR2^3)", 6, maj3or2, 12)

    def and2maj3(z):
        b1 = popcount(z & 7) >= 2
        b2 = popcount((z >> 3) & 7) >= 2
        return b1 and b2
    add("AND2(MAJ3^2)", 6, and2maj3, 6)
    return out


def lp_battery():
    UPc = {}
    for name, n, fvec, wk in named_functions():
        N = 1 << n
        mask = sum(b << x for x, b in enumerate(fvec))
        if n <= 4:
            W = int(np.load(os.path.join(HERE, f"mc001_W_n{n}.npy"))[mask])
            if wk is not None:
                assert W == wk, (name, W, wk)
        else:
            W = wk   # valeur du depot (F-021/F-022), re-verifiee la-bas
        if n not in UPc:
            UPc[n] = up_masks(n)
        t0 = time.time()
        res_r = w_real_milp(fvec, n, UB=W, integers=False)
        wr = res_r.fun if res_r.success else None
        res_lp = w_real_milp(fvec, n, UB=W, integers=False, relax_all=True)
        wlp = res_lp.fun if res_lp.success else None
        lpu = lp_unilateral(mask, n, UPc[n])
        lpu_c = lp_unilateral((1 << N) - 1 - mask, n, UPc[n])
        print(f"{name:14s} n={n} W={W:3d}  W_R(coef reels)="
              f"{wr if wr is None else round(wr,3)}  "
              f"LP totale relaxee={wlp if wlp is None else round(wlp,3)}  "
              f"LP_couv(f)={lpu if lpu is None else round(lpu,3)}  "
              f"LP_couv(non f)={lpu_c if lpu_c is None else round(lpu_c,3)}"
              f"  ({time.time()-t0:.0f}s)", flush=True)


# ----------------------------------------------------------------------
# validation croisee
# ----------------------------------------------------------------------

def valide():
    # stats publiees D-005
    for n, attendu in ((3, {"mediane": 3, "max": 5, "n_max": 12}),
                       (4, {"mediane": 6, "max": 9, "n_max": 675})):
        W = np.load(os.path.join(HERE, f"mc001_W_n{n}.npy"))
        med = int(np.median(W))
        mx = int(W.max())
        nmx = int((W == mx).sum())
        frac_med = float((W >= attendu["mediane"]).mean()) * 100
        print(f"n={n} : mediane={med} max={mx} #max={nmx} "
              f"fraction W>=mediane_D005={frac_med:.2f}%")
        print(f"   attendu D-005 : {attendu} "
              f"(n=3 : 70.31% W>=3, 4.69%*256=12 au max ; "
              f"n=4 : 67.60% W>=6, 1.03%*65536~675 au max)")
    # spot-check CP-SAT du depot sur classes n=4
    sys.path.insert(0, r"C:\Users\Tanguy Le Mer\Documents\ExplorationPsNP"
                    r"\checks")
    from task_a013_cout_convention import termes_positifs, poids_min
    rng = np.random.default_rng(20260802)
    W4 = np.load(os.path.join(HERE, "mc001_W_n4.npy"))
    tp = termes_positifs(4)
    picks = rng.integers(1, (1 << 16) - 1, size=12)
    ok = 0
    for mask in picks:
        f = fvec_of_mask(int(mask), 4)
        w_sat, _ = poids_min(f, tp, 4, tl=60.0)
        w_mine = int(W4[int(mask)])
        st = "OK" if w_sat == w_mine else "!!! DESACCORD"
        if w_sat == w_mine:
            ok += 1
        print(f"  masque {int(mask):5d} : enumeration={w_mine} "
              f"CP-SAT={w_sat} {st}", flush=True)
    print(f"spot-check CP-SAT : {ok}/{len(picks)} accords")


# ----------------------------------------------------------------------

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "exact"
    if cmd == "exact":
        for n in (2, 3, 4):
            compute_exact(n)
    elif cmd == "valide":
        valide()
    elif cmd == "invariants":
        for n in (3, 4):
            if not os.path.exists(os.path.join(HERE, f"mc001_inv_n{n}.npz")):
                compute_invariants(n)
            determination(n)
    elif cmd == "strata":
        for n in (3, 4):
            strata(n)
    elif cmd == "sym":
        for n in (3, 4):
            sym_check(n)
    elif cmd == "lp":
        lp_battery()
    elif cmd == "lpgap":
        for n in (3, 4):
            lp_gap_unilateral(n)
    else:
        print("sous-commande inconnue")


if __name__ == "__main__":
    main()
