"""MC-001 — REFUTATION : contre-verifications INDEPENDANTES (partie 1, sans solveur).

Tout est re-implemente a partir des ENONCES (pas des scripts des attaques) :
  T1  : Th.1 setcover — exhaustif n=3 : unilateral existe <=> monotone & f(0)=0 ;
        poids unilateral = # uns minimaux.
  T2  : Th.2 setcover — 12 instances Set Cover seedees, W(variante listee, B={0})
        par ENUMERATION brute vs OPT Set Cover par force brute.
  T3  : temoins de l'attaque inverse — masques 1776 / 748 (n=4) : W par enumeration
        (deux conventions de lecture du masque) + batterie d'invariants A MOI.
  T4  : THR2_4 : W = 4 (aucun separateur de poids <= 3, enumeration) vs couvert 6 ;
        MAJ_4 : W = 4 et temoin reel 1/2*somme(paires) de poids 3.
  T5  : proposition diophantienne (hil) : scan n <= 300, |E| <= 3000.
  T6  : Prop. 5 setcover (echafaudage) : n=2 et n=3 EXHAUSTIFS, ma propre
        implementation de f_g et de p.
  T7  : Th.3 setcover (rails doubles) : (i) 12 instances partielles n=2 ;
        (ii) les 14 g totales non constantes n=2 — free-* vs W_litteraux>=0.
  T8  : appartenance NP : temoin injectif n=3 (256/256) ; degenerescence du
        stratum {0,1} (verification directe n=3).
"""
from __future__ import annotations
import itertools, random, sys, time
from itertools import combinations, combinations_with_replacement, product

# ---------------------------------------------------------------- outils de base
def popcount(x): return bin(x).count("1")

def W_enum(f, n, wmax, points=None):
    """W exact par enumeration des multisets de monomes positifs non vides,
    poids croissant. points=None -> tous les 2^n points. Retourne (W, combo)
    ou (None, None) si > wmax. Convention : f dict/list indexee par entier x,
    monome S actif sur x ssi S & x == S."""
    N = 1 << n
    pts = list(range(N)) if points is None else points
    ones = [x for x in pts if f[x]]
    zeros = [x for x in pts if not f[x]]
    if not ones or not zeros:
        return 0, ()
    mons = list(range(1, N))
    act = {S: [x for x in pts if (x & S) == S] for S in mons}
    for w in range(1, wmax + 1):
        for combo in combinations_with_replacement(mons, w):
            val = dict.fromkeys(pts, 0)
            for S in combo:
                for x in act[S]:
                    val[x] += 1
            su = {val[x] for x in ones}
            if not (su & {val[x] for x in zeros}):
                return w, combo
    return None, None

def est_monotone(f, n):
    N = 1 << n
    for x in range(N):
        for i in range(n):
            if not (x >> i) & 1 and f[x] > f[x | (1 << i)]:
                return False
    return True

def uns_minimaux(f, n):
    N = 1 << n
    ones = [x for x in range(N) if f[x]]
    return [x for x in ones
            if not any(f[y] and y != x and (y & x) == y for y in ones)]

# ============================================================== T1 : Th.1 n=3
def t1():
    n, N = 3, 8
    err = 0
    for mask in range(1, 2 ** N - 1):          # non constantes
        f = [(mask >> x) & 1 for x in range(N)]
        zeros = [x for x in range(N) if not f[x]]
        ones = [x for x in range(N) if f[x]]
        legal = [S for S in range(1, N) if all((z & S) != S for z in zeros)]
        existe = all(any((x & S) == S for S in legal) for x in ones)
        attendu = est_monotone(f, n) and f[0] == 0
        if existe != attendu:
            err += 1; print(f"  T1 ECART existence mask={mask}")
            continue
        if existe:
            # poids unilateral minimal = plus petite couverture des uns par legal
            best = None
            for r in range(1, len(legal) + 1):
                for comb in combinations(legal, r):
                    if all(any((x & S) == S for S in comb) for x in ones):
                        best = r; break
                if best: break
            if best != len(uns_minimaux(f, n)):
                err += 1
                print(f"  T1 ECART poids mask={mask} : couvert={best} "
                      f"!= #uns_min={len(uns_minimaux(f, n))}")
    print(f"T1 (Th.1, n=3, 254 f non constantes) : {'OK — 0 ecart' if not err else f'{err} ECARTS'}")

# ============================================================== T2 : Th.2
def t2():
    rng = random.Random(424242)                 # seed DIFFERENTE de la leur
    nb_ok = nb = 0
    for _ in range(12):
        k = rng.randint(3, 4)
        m = rng.randint(4, 6)
        while True:
            sets = [frozenset(x for x in range(m) if rng.random() < 0.45)
                    for _ in range(k)]
            if all(any(j in C for C in sets) for j in range(m)):
                break
        # OPT set cover, force brute
        opt = None
        for r in range(1, k + 1):
            for comb in combinations(range(k), r):
                if all(any(j in sets[i] for i in comb) for j in range(m)):
                    opt = r; break
            if opt: break
        # variante listee : points a_j sur k variables, B = {0}
        pts_A = []
        for j in range(m):
            a = 0
            for i in range(k):
                if j in sets[i]:
                    a |= 1 << i
            pts_A.append(a)
        f = {}
        for a in pts_A: f[a] = 1
        f[0] = 0
        W, _ = W_enum(f, k, wmax=m, points=sorted(set(pts_A)) + [0])
        nb += 1
        if W == opt:
            nb_ok += 1
        else:
            print(f"  T2 ECART : OPT={opt}, W={W}, sets={sets}")
    print(f"T2 (Th.2, 12 instances seedees independantes) : {nb_ok}/{nb} egalites W = OPT")

# ============================================================== T3 : masques 1776/748
def invariants(f, n):
    N = 1 << n
    inv = {}
    inv["nb_uns"] = sum(f)
    # ANF (Moebius GF2)
    anf = list(f)
    for i in range(n):
        for x in range(N):
            if (x >> i) & 1:
                anf[x] ^= anf[x ^ (1 << i)]
    inv["anf_sparsite"] = sum(anf)
    inv["deg_gf2"] = max((popcount(x) for x in range(N) if anf[x]), default=0)
    # Moebius sur Z (polynome reel multiligne)
    moe = [int(v) for v in f]
    for i in range(n):
        for x in range(N):
            if (x >> i) & 1:
                moe[x] -= moe[x ^ (1 << i)]
    inv["moebius_sparsite"] = sum(1 for v in moe if v)
    inv["moebius_L1"] = sum(abs(v) for v in moe)
    inv["deg_reel"] = max((popcount(x) for x in range(N) if moe[x]), default=0)
    # sensibilite max
    inv["sensibilite"] = max(sum(1 for i in range(n) if f[x] != f[x ^ (1 << i)])
                             for x in range(N))
    # alternance (DP sur chaines maximales, valeur en 1^n)
    A = [0] * N
    for x in range(1, N):
        A[x] = max(A[x ^ (1 << i)] + (1 if f[x ^ (1 << i)] != f[x] else 0)
                   for i in range(n) if (x >> i) & 1)
    inv["alternance"] = A[N - 1]
    inv["uns_minimaux"] = len(uns_minimaux(f, n))
    # implicants premiers (litteraux) et DNF minimale
    termes = []
    for idx in range(1, N):
        iset = [i for i in range(n) if (idx >> i) & 1]
        for pol in product((0, 1), repeat=len(iset)):
            cover = [x for x in range(N)
                     if all(((x >> i) & 1) == p for i, p in zip(iset, pol))]
            if all(f[x] for x in cover):
                termes.append((idx, pol, frozenset(cover)))
    # premiers = aucun sur-terme (moins de litteraux) implicant ne le contient
    prem = []
    for idx, pol, cov in termes:
        strict = False
        for idx2, pol2, cov2 in termes:
            if cov2 > cov:
                strict = True; break
        if not strict:
            prem.append((idx, pol, cov))
    inv["implicants_premiers"] = len(prem)
    ones = {x for x in range(N) if f[x]}
    dnf = 0
    if ones:
        dnf = None
        for r in range(1, len(prem) + 1):
            for comb in combinations(prem, r):
                if set().union(*(c for _, _, c in comb)) >= ones:
                    dnf = r; break
            if dnf: break
    inv["dnf_min"] = dnf
    # matrice f(x & y) : rangs et lignes distinctes
    M = [[f[x & y] for y in range(N)] for x in range(N)]
    inv["lignes_distinctes"] = len({tuple(r) for r in M})
    inv["rang_gf2"] = rang_gf2(M)
    try:
        import numpy as np
        inv["rang_reel"] = int(np.linalg.matrix_rank(np.array(M, dtype=float)))
    except ImportError:
        inv["rang_reel"] = "numpy absent"
    # couverts unilateraux (les deux orientations) : inf = None
    for nom, g in (("couv_zeros0", f), ("couv_uns0", [1 - v for v in f])):
        zeros = [x for x in range(N) if not g[x]]
        onesg = [x for x in range(N) if g[x]]
        legal = [S for S in range(1, N) if all((z & S) != S for z in zeros)]
        best = None
        if onesg and all(any((x & S) == S for S in legal) for x in onesg):
            for r in range(1, len(legal) + 1):
                trouve = False
                for comb in combinations(legal, r):
                    if all(any((x & S) == S for S in comb) for x in onesg):
                        best = r; trouve = True; break
                if trouve: break
        inv[nom] = best
    return inv

def rang_gf2(M):
    rows = [int("".join(map(str, r)), 2) for r in M]
    rang = 0
    for bit in range(len(M[0]) - 1, -1, -1):
        piv = None
        for i, r in enumerate(rows):
            if (r >> bit) & 1:
                piv = i; break
        if piv is None: continue
        pr = rows.pop(piv); rang += 1
        rows = [r ^ pr if (r >> bit) & 1 else r for r in rows]
    return rang

def t3():
    n, N = 4, 16
    for conv, lit in (("LSB (f[x]=(mask>>x)&1)", lambda m, x: (m >> x) & 1),
                      ("MSB (f[x]=(mask>>(15-x))&1)", lambda m, x: (m >> (15 - x)) & 1)):
        f1 = [lit(1776, x) for x in range(N)]
        f2 = [lit(748, x) for x in range(N)]
        t0 = time.time()
        W1, _ = W_enum(f1, n, wmax=7)
        W2, _ = W_enum(f2, n, wmax=7)
        print(f"T3 convention {conv} : W(1776)={W1}, W(748)={W2} "
              f"({time.time()-t0:.0f}s)")
        if {W1, W2} == {4, 6}:
            i1, i2 = invariants(f1, n), invariants(f2, n)
            diff = {k: (i1[k], i2[k]) for k in i1 if i1[k] != i2[k]}
            print(f"   invariants EGAUX : {sorted(k for k in i1 if i1[k] == i2[k])}")
            print(f"   invariants DIFFERENTS : {diff if diff else 'AUCUN'}")
            print(f"   valeurs communes : {sorted((k, i1[k]) for k in i1 if i1[k]==i2[k])}")

# ============================================================== T4 : THR2_4, MAJ_4
def t4():
    n, N = 4, 16
    thr2 = [1 if popcount(x) >= 2 else 0 for x in range(N)]
    maj4 = [1 if popcount(x) >= 3 else 0 for x in range(N)]
    W_thr2, c_thr2 = W_enum(thr2, n, wmax=4)
    W_maj4, c_maj4 = W_enum(maj4, n, wmax=4)
    print(f"T4 THR2_4 : W = {W_thr2} (temoin {c_thr2}) ; "
          f"#uns minimaux = {len(uns_minimaux(thr2, n))}")
    print(f"T4 MAJ_4  : W = {W_maj4} (temoin {c_maj4})")
    # temoin reel 1/2 * somme des paires pour MAJ_4
    paires = [S for S in range(N) if popcount(S) == 2]
    vals_uns, vals_zeros = set(), set()
    for x in range(N):
        v = sum(0.5 for S in paires if (x & S) == S)
        (vals_uns if maj4[x] else vals_zeros).add(v)
    ok = not (vals_uns & vals_zeros)
    print(f"T4 W_R(MAJ_4) <= 3 : temoin 1/2*paires — separation {'OK' if ok else 'ECHEC'} "
          f"(uns {sorted(vals_uns)}, zeros {sorted(vals_zeros)}, poids {6*0.5})")

# ============================================================== T5 : diophantien
def t5():
    viol = []
    p2 = {1 << k for k in range(40)}
    for n in range(1, 301):
        for E in range(1, 3001):
            if (2 * n + 4 * E) in p2 and (n + 5 * E) in p2:
                viol.append((n, E))
    print(f"T5 (dimensions JR jamais deux puissances de 2, n<=300, E<=3000) : "
          f"violations = {viol if viol else 'AUCUNE'}")

# ============================================================== T6 : Prop 5
def dnf_size(g, n):
    N = 1 << n
    ones = {x for x in range(N) if g[x]}
    if not ones: return 0
    termes = []
    for idx in range(1, N):
        iset = [i for i in range(n) if (idx >> i) & 1]
        for pol in product((0, 1), repeat=len(iset)):
            cov = frozenset(x for x in range(N)
                            if all(((x >> i) & 1) == p for i, p in zip(iset, pol)))
            if all(g[x] for x in cov):
                termes.append((iset, pol, cov))
    # ne garder que les maximaux (implicants premiers) pour la couverture
    prem = [t for t in termes if not any(t2[2] > t[2] for t2 in termes)]
    for r in range(1, len(prem) + 1):
        for comb in combinations(prem, r):
            if set().union(*(c for _, _, c in comb)) >= ones:
                return r
    return None

def dnf_cover(g, n):
    """une couverture optimale (liste de (iset,pol))"""
    N = 1 << n
    ones = {x for x in range(N) if g[x]}
    termes = []
    for idx in range(1, N):
        iset = [i for i in range(n) if (idx >> i) & 1]
        for pol in product((0, 1), repeat=len(iset)):
            cov = frozenset(x for x in range(N)
                            if all(((x >> i) & 1) == p for i, p in zip(iset, pol)))
            if all(g[x] for x in cov):
                termes.append((iset, pol, cov))
    prem = [t for t in termes if not any(t2[2] > t[2] for t2 in termes)]
    for r in range(1, len(prem) + 1):
        for comb in combinations(prem, r):
            if set().union(*(c for _, _, c in comb)) >= ones:
                return [(i, p) for i, p, _ in comb]
    return None

def t6():
    for n in (2, 3):
        N = 1 << n
        nb = ok = 0
        pire = 0
        for mask in range(1, 2 ** N - 1):
            g = [(mask >> x) & 1 for x in range(N)]
            cover = dnf_cover(g, n)
            if cover is None: continue
            r = len(cover)
            alpha, beta = r + 1, (r + 1) * (n + 1)
            # f_g sur 2n variables : y = bits 0..n-1, z = bits n..2n-1
            M = 1 << (2 * n)
            vals_uns, vals_zeros = set(), set()
            for p in range(M):
                y, z = p & (N - 1), p >> n
                v = alpha * (popcount(y) + popcount(z)) + beta * popcount(y & z)
                for iset, pol in cover:
                    if all(((y >> i) & 1) if pl else ((z >> i) & 1)
                           for i, pl in zip(iset, pol)):
                        v += 1
                est_un = (z == (~y) & (N - 1)) and g[y] == 1
                (vals_uns if est_un else vals_zeros).add(v)
            poids = 2 * n * alpha + n * beta + r
            attendu = (r + 1) * (n * n + 3 * n) + r
            nb += 1
            if not (vals_uns & vals_zeros) and poids == attendu:
                ok += 1
                pire = max(pire, poids)
            else:
                print(f"  T6 ECHEC mask={mask} n={n} : "
                      f"collision={sorted(vals_uns & vals_zeros)}, poids={poids}!={attendu}")
        print(f"T6 (Prop 5, n={n}) : {ok}/{nb} separations OK, poids max {pire} "
              f"(temoin injectif : {4 ** n - 1})")

# ============================================================== T7 : Th.3 rails n=2
def t7():
    n, N = 2, 4
    diag = [x | (((~x) & (N - 1)) << n) for x in range(N)]   # d(x) sur 2n vars
    M2 = 1 << (2 * n)
    # (i) 12 instances partielles seedees
    rng = random.Random(777)
    nb = ok = 0
    for _ in range(12):
        spec = {}
        while True:
            spec = {x: rng.choice([0, 1, None]) for x in range(N)}
            vs = [v for v in spec.values() if v is not None]
            if 0 in vs and 1 in vs: break
        ones = [x for x in range(N) if spec[x] == 1]
        zeros = [x for x in range(N) if spec[x] == 0]
        # Min-DNF(*) : termes evitant les zeros, couvrant les uns
        termes = []
        for idx in range(1, N):
            iset = [i for i in range(n) if (idx >> i) & 1]
            for pol in product((0, 1), repeat=len(iset)):
                sat = lambda x: all(((x >> i) & 1) == p for i, p in zip(iset, pol))
                if not any(sat(z) for z in zeros):
                    termes.append(frozenset(x for x in range(N) if sat(x)))
        mindnf = None
        if all(any(x in T for T in termes) for x in ones):
            for r in range(1, len(termes) + 1):
                for comb in combinations(termes, r):
                    if all(any(x in T for T in comb) for x in ones):
                        mindnf = r; break
                if mindnf: break
        # rails : monomes sur 4 vars, legaux = inactifs sur d(zeros), couvrant d(uns)
        legal = [S for S in range(1, M2)
                 if all((diag[z] & S) != S for z in zeros)]
        rails = None
        if all(any((diag[o] & S) == S for S in legal) for o in ones):
            for r in range(1, len(legal) + 1):
                trouve = False
                for comb in combinations(legal, r):
                    if all(any((diag[o] & S) == S for S in comb) for o in ones):
                        rails = r; trouve = True; break
                if trouve: break
        nb += 1
        if mindnf == rails: ok += 1
        else: print(f"  T7i ECART spec={spec} : mindnf={mindnf} rails={rails}")
    print(f"T7 (i) (Th.3i, n=2, 12 instances partielles) : {ok}/{nb} egalites")
    # (ii) les 14 totales non constantes : free-* vs W_litteraux>=0
    lits = []
    for idx in range(1, N):
        iset = [i for i in range(n) if (idx >> i) & 1]
        for pol in product((0, 1), repeat=len(iset)):
            lits.append([1 if all(((x >> i) & 1) == p for i, p in zip(iset, pol))
                         else 0 for x in range(N)])
    nb = ok = 0
    for mask in range(1, 2 ** N - 1):
        g = [(mask >> x) & 1 for x in range(N)]
        # W_litteraux>=0(g) par enumeration
        wlit = None
        for w in range(1, 8):
            for combo in combinations_with_replacement(range(len(lits)), w):
                vals = [sum(1 for t in combo if lits[t][x]) for x in range(N)]
                su = {vals[x] for x in range(N) if g[x]}
                sz = {vals[x] for x in range(N) if not g[x]}
                if not (su & sz): wlit = w; break
            if wlit: break
        # free-* sur rails : contraintes aux seuls points diagonaux
        fstar = {}
        for x in range(N): fstar[diag[x]] = g[x]
        wstar, _ = W_enum(fstar, 2 * n, wmax=8, points=diag)
        nb += 1
        if wlit == wstar: ok += 1
        else: print(f"  T7ii ECART mask={mask} : W_lit={wlit} W*_libre={wstar}")
    print(f"T7 (ii) (Th.3ii, n=2, 14 totales) : {ok}/{nb} egalites")

# ============================================================== T8 : NP + {0,1}
def t8():
    n, N = 3, 8
    # temoin injectif
    inj_ok = all(len({sum((1 << i) for i in range(n) if (x >> i) & 1)
                      for x in range(N)}) == N for _ in (0,))
    poids = sum(1 << i for i in range(n))
    nb_ok = 0
    for mask in range(2 ** N):
        f = [(mask >> x) & 1 for x in range(N)]
        vals_u = {x for x in range(N) if f[x]}          # p(x) = x
        vals_z = {x for x in range(N) if not f[x]}
        if not (vals_u & vals_z): nb_ok += 1
    print(f"T8 temoin injectif n=3 : injectif={inj_ok}, poids={poids} (=N-1={N-1}), "
          f"separation {nb_ok}/256")
    # stratum {0,1} : support >= 2 monomes -> infaisable (verification directe n=3)
    viol = 0
    for S1 in range(1, N):
        for S2 in range(S1 + 1, N):
            if not (1 <= 1 + 1):
                pass
            # p = m_S1 + m_S2 : valeur au point S1|S2
            e = S1 | S2
            v = (1 if (e & S1) == S1 else 0) + (1 if (e & S2) == S2 else 0)
            if v < 2: viol += 1
    print(f"T8 stratum {{0,1}} : paires (S1,S2) avec p(S1|S2) < 2 : {viol} "
          f"(attendu 0 -> support d'au plus 1 monome, stratum degenere)")

if __name__ == "__main__":
    quoi = sys.argv[1:] or ["t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8"]
    for t in quoi:
        t0 = time.time()
        globals()[t]()
        print(f"   [{t} : {time.time()-t0:.0f}s]\n", flush=True)
