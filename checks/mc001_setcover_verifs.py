"""
MC-001, strategie B (set cover / classe unilaterale F-021) — VERIFICATIONS.

Objets. Modele du depot (SYM+ de Williams, A-013) : p = somme a_S m_S,
a_S entiers >= 0, m_S = monomes POSITIFS non vides ; p separe f si
{p(x): f(x)=1} et {p(x): f(x)=0} sont disjoints ; W(f) = min somme a_S.

Ce script verifie par calcul CHAQUE pas calculable des enonces livres :

V1 (Th.1, effondrement monotone) : pour f NON CONSTANTE, un separateur
   unilateral (zeros -> {0}) existe SSI f est monotone et f(0)=0 ; et pour
   f monotone, tout monome legal contenu dans un un minimal EST son support
   (donc poids unilateral = # uns minimaux). Exhaustif n=3 et n=4.

V2 (Th.2, variante a points listes) : l'instance (A = vecteurs d'incidence
   des elements, B = {0}) a un poids EXACTEMENT egal a l'optimum de SET
   COVER. Verifie par ENUMERATION COMPLETE independante (pas le raccourci
   couverture : le test est la disjonction des ensembles de valeurs).

V3a (Th.3i, rails doubles, version prescrite-unilaterale) : le nombre
   minimal de monomes positifs legaux couvrant les uns de F_g (rails
   doubles de g partielle) = dnf-size(g) (Min-DNF(*)). Instances n=3.

V3b (Th.3ii, rails doubles, version libre) : le poids libre de F_g
   contraint aux seuls points diagonaux = W_litteraux>=0(g) pour g TOTALE.
   Exhaustif n=2, echantillon n=3. (CP-SAT + re-verification independante.)

V4 (Lemme 4, borne d'empaquetage) : pour toute paire-famille {(u_i,v_i)},
   v_i strictement sous u_i, f(u_i) != f(v_i), aux ensembles-differences
   D_i = {S non vide : S dans u_i, S pas dans v_i} deux a deux disjoints :
   W >= r. Verifie exhaustivement a n=3 : max-packing <= W pour les 254
   fonctions non constantes ; et alternance (F-020, DP poly) <= packing.

V5 (Prop. 5, echafaudage total) : la construction totale rails-doubles a
   penalites (alpha = r+1, beta = alpha(n+1)) SEPARE f_g pour toute g
   totale (exhaustif n=2 et n=3) avec poids 2n*alpha + n*beta + r —
   ce qui prouve W(f_g) <= (r+1)(n^2+3n) + r, borne superieure AFFINE en
   r = dnf-size(g) ; a n<=3 elle est PIRE que le temoin injectif 4^n - 1
   (constat d'obstruction, consigne comme tel).
"""

from __future__ import annotations

import itertools
import random
import sys
import time

from ortools.sat.python import cp_model

random.seed(20260802)


# ---------------------------------------------------------------- outillage

def popcount(x):
    return bin(x).count("1")


def poids_min_terms(activite, fvals, cap_max=30, tl=60.0):
    """min somme des coefficients (entiers >= 0) sur des 'termes' donnes par
    leur vecteur d'activite sur une liste de points ; contrainte : ensembles
    de valeurs des points f=1 / f=0 disjoints. CP-SAT, cap croissant, puis
    RE-VERIFICATION independante. Retourne (poids, sol) ou (None, msg)."""
    npts = len(fvals)
    for cap in range(0, cap_max + 1):
        model = cp_model.CpModel()
        a = [model.NewIntVar(0, cap, "") for _ in activite]
        model.Add(sum(a) <= cap)
        z = [model.NewBoolVar("") for _ in range(cap + 1)]
        for e in range(npts):
            expr = [a[t] for t, vec in enumerate(activite) if vec[e]]
            v = model.NewIntVar(0, cap, "")
            model.Add(v == (sum(expr) if expr else 0))
            model.AddElement(v, z, 1 if fvals[e] else 0)
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = tl
        solver.parameters.num_search_workers = 8
        st = solver.Solve(model)
        if st in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            sol = [solver.Value(x) for x in a]
            uns, zeros = set(), set()
            for e in range(npts):
                val = sum(c for c, vec in zip(sol, activite) if vec[e])
                (uns if fvals[e] else zeros).add(val)
            if uns & zeros:
                return None, "ECHEC RE-VERIFICATION"
            return sum(sol), sol
        if st != cp_model.INFEASIBLE:
            return None, f"UNKNOWN cap={cap}"
    return None, f">{cap_max}"


def activite_monomes_positifs(points, n):
    """Vecteurs d'activite des 2^n - 1 monomes positifs sur les points."""
    return [[1 if (pt & S) == S else 0 for pt in points]
            for S in range(1, 1 << n)]


def activite_litteraux(points, n):
    """Vecteurs d'activite des 3^n - 1 monomes sur litteraux (A, B),
    A inter B = vide, (A,B) != (0,0) : actif sur x ssi A dans x, B dans ~x."""
    out = []
    for A in range(1 << n):
        for B in range(1 << n):
            if A & B or (A == 0 and B == 0):
                continue
            out.append([1 if (pt & A) == A and (pt & B) == 0 else 0
                        for pt in points])
    return out


def enum_poids_min(points, fvals, monomes, wmax):
    """ENUMERATION COMPLETE independante (aucun solveur, aucun raccourci) :
    plus petit w <= wmax tel qu'un multiensemble de monomes de taille w
    separe (disjonction des ensembles de valeurs). None sinon."""
    for w in range(0, wmax + 1):
        for combo in itertools.combinations_with_replacement(monomes, w):
            uns, zeros = set(), set()
            ok = True
            for pt, fv in zip(points, fvals):
                val = sum(1 for S in combo if (pt & S) == S)
                (uns if fv else zeros).add(val)
            if not (uns & zeros):
                return w
    return None


def min_couverture(univers, familles, kmax):
    """Set cover exact par force brute (sous-ensembles de taille croissante).
    univers: set, familles: liste de sets. None si aucun <= kmax."""
    for k in range(0, kmax + 1):
        for combo in itertools.combinations(range(len(familles)), k):
            u = set()
            for i in combo:
                u |= familles[i]
            if univers <= u:
                return k
    return None


# ------------------------------------------------------------------- V1

def v1_effondrement_monotone(n):
    N = 1 << n
    t0 = time.time()
    nb = {"equiv_ok": 0, "mono_testees": 0}
    for masque in range(1 << N):
        f = [(masque >> e) & 1 for e in range(N)]
        if all(f) or not any(f):
            continue
        mono = all(f[x] <= f[x | (1 << i)]
                   for x in range(N) for i in range(n))
        # monomes legaux : tout sur-ensemble est un un
        L = [S for S in range(1, N)
             if all(f[x] for x in range(N) if (x & S) == S)]
        # existence d'un separateur unilateral = couverture des uns par L
        existe = all(any((x & S) == S for S in L)
                     for x in range(N) if f[x])
        attendu = mono and f[0] == 0
        assert existe == attendu, (n, masque, existe, attendu)
        nb["equiv_ok"] += 1
        if attendu:
            nb["mono_testees"] += 1
            # uns minimaux ; verifie : legal S dans un minimal => S = support
            for x in range(N):
                if f[x] and not any(f[x & ~(1 << i)]
                                    for i in range(n) if (x >> i) & 1):
                    for S in L:
                        if (x & S) == S:
                            assert S == x, (masque, x, S)
    print(f"V1 n={n} : equivalence 'unilateral existe <=> monotone et "
          f"f(0)=0' verifiee sur {nb['equiv_ok']} fonctions non constantes ; "
          f"argument de comptage (S legal dans un un minimal => S = support) "
          f"verifie sur les {nb['mono_testees']} monotones "
          f"({time.time()-t0:.0f}s)", flush=True)


# ------------------------------------------------------------------- V2

def v2_liste_egale_setcover(nb_inst=12):
    t0 = time.time()
    for it in range(nb_inst):
        k = random.randint(3, 5)          # nombre d'ensembles = variables
        m = random.randint(3, 8)          # nombre d'elements = points
        # incidence aleatoire, chaque element couvert par >= 1 ensemble
        inc = []
        for _ in range(m):
            v = random.randint(1, (1 << k) - 1)
            inc.append(v)
        pts = [0] + inc                   # B = {0} puis A
        fv = [0] + [1] * m
        monomes = list(range(1, 1 << k))
        w = enum_poids_min(pts, fv, monomes, k)
        familles = [set(j for j in range(m) if (inc[j] >> i) & 1)
                    for i in range(k)]
        opt = min_couverture(set(range(m)), familles, k)
        assert w == opt, (it, k, m, inc, w, opt)
    print(f"V2 : {nb_inst} instances aleatoires de SET COVER (k<=5, m<=8) — "
          f"poids (enumeration complete du vrai critere, disjonction des "
          f"valeurs) = optimum SET COVER (force brute) dans {nb_inst}/"
          f"{nb_inst} cas ({time.time()-t0:.0f}s)", flush=True)


# ------------------------------------------------------------------- V3a

def comp3(x, n):
    return ((1 << n) - 1) & ~x


def v3a_rails_doubles_prescrit(nb_inst=30, n=3):
    N = 1 << n
    t0 = time.time()
    for it in range(nb_inst):
        # g partielle : chaque point ON / OFF / DC ; >= 1 ON et >= 1 OFF
        while True:
            spec = [random.choice("01*") for _ in range(N)]
            if "0" in spec and "1" in spec:
                break
        on = [x for x in range(N) if spec[x] == "1"]
        off = [x for x in range(N) if spec[x] == "0"]
        # cote Min-DNF(*) : termes consistants non vides legaux
        termes = []
        for A in range(N):
            for B in range(N):
                if A & B or (A == 0 and B == 0):
                    continue
                if any((x & A) == A and (x & B) == 0 for x in off):
                    continue
                termes.append(set(x for x in on
                                  if (x & A) == A and (x & B) == 0))
        dnf = min_couverture(set(on), termes, len(on))
        # cote rails doubles : monomes positifs 6 vars legaux
        diag = {x: x | (comp3(x, n) << n) for x in range(N)}
        monolegaux = []
        for S in range(1, 1 << (2 * n)):
            if any((diag[x] & S) == S for x in off):
                continue
            c = set(x for x in on if (diag[x] & S) == S)
            monolegaux.append(c)
        pos = min_couverture(set(on), monolegaux, len(on))
        assert dnf == pos and dnf is not None, (it, spec, dnf, pos)
    print(f"V3a : {nb_inst} instances partielles aleatoires (n=3) — "
          f"couverture unilaterale rails-doubles (2n=6 vars) = dnf-size "
          f"Min-DNF(*) dans {nb_inst}/{nb_inst} cas "
          f"({time.time()-t0:.0f}s)", flush=True)


# ------------------------------------------------------------------- V3b

def v3b_rails_doubles_libre(n, gs):
    t0 = time.time()
    N = 1 << n
    pts = list(range(N))
    for g in gs:
        fv = [g[x] for x in pts]
        # modele a litteraux sur g (coefficients >= 0, def. A-013)
        wlit, s1 = poids_min_terms(activite_litteraux(pts, n), fv)
        # version libre de F_g : contraintes aux SEULS points diagonaux
        diag = [x | (comp3(x, n) << n) for x in pts]
        wfree, s2 = poids_min_terms(
            activite_monomes_positifs(diag, 2 * n), fv)
        assert wlit == wfree and wlit is not None, (g, wlit, s1, wfree, s2)
    print(f"V3b n={n} : {len(gs)} fonctions totales — poids libre de la "
          f"version * rails-doubles (contraintes diagonales) = "
          f"W_litteraux>=0(g) dans {len(gs)}/{len(gs)} cas "
          f"({time.time()-t0:.0f}s)", flush=True)


# ------------------------------------------------------------------- V4

def w_exact(f, n):
    N = 1 << n
    pts = list(range(N))
    w, _ = poids_min_terms(activite_monomes_positifs(pts, n),
                           [f[x] for x in pts])
    return w


def max_packing(f, n):
    """Plus grande famille de paires (u,v), v strictement sous u, f(u)!=f(v),
    aux ensembles-differences deux a deux disjoints. CP-SAT (exact)."""
    N = 1 << n
    paires = []
    for u in range(N):
        for v in range(N):
            if v != u and (v & u) == v and f[u] != f[v]:
                D = frozenset(S for S in range(1, N)
                              if (S & u) == S and (S & v) != S)
                paires.append(D)
    model = cp_model.CpModel()
    b = [model.NewBoolVar("") for _ in paires]
    for i in range(len(paires)):
        for j in range(i + 1, len(paires)):
            if paires[i] & paires[j]:
                model.Add(b[i] + b[j] <= 1)
    model.Maximize(sum(b))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 30
    st = solver.Solve(model)
    assert st == cp_model.OPTIMAL
    return int(solver.ObjectiveValue())


def alternance(f, n):
    """max alternances de f le long d'une chaine croissante depuis 0 —
    DP sur le treillis, temps O(N n) : POLYNOMIAL en N."""
    N = 1 << n
    A = [0] * N
    for x in range(1, N):
        best = 0
        for i in range(n):
            if (x >> i) & 1:
                y = x & ~(1 << i)
                best = max(best, A[y] + (1 if f[y] != f[x] else 0))
        A[x] = best
    return max(A)


def v4_packing(n=3):
    t0 = time.time()
    N = 1 << n
    egal_w = 0
    packing_bat_alt = 0
    total = 0
    for masque in range(1 << N):
        f = [(masque >> e) & 1 for e in range(N)]
        if all(f) or not any(f):
            continue
        total += 1
        W = w_exact(f, n)
        pk = max_packing(f, n)
        alt = alternance(f, n)
        assert pk <= W, (masque, pk, W)
        assert alt <= pk, (masque, alt, pk)
        if pk == W:
            egal_w += 1
        if pk > alt:
            packing_bat_alt += 1
    print(f"V4 n={n} : packing <= W et alternance <= packing verifies sur "
          f"les {total} fonctions non constantes ; packing = W dans "
          f"{egal_w}/{total} cas ; packing > alternance dans "
          f"{packing_bat_alt}/{total} cas ({time.time()-t0:.0f}s)",
          flush=True)


# ------------------------------------------------------------------- V5

def dnf_size_totale(g, n):
    N = 1 << n
    on = [x for x in range(N) if g[x]]
    off = [x for x in range(N) if not g[x]]
    termes, temoins = [], []
    for A in range(N):
        for B in range(N):
            if A & B or (A == 0 and B == 0):
                continue
            if any((x & A) == A and (x & B) == 0 for x in off):
                continue
            termes.append(set(x for x in on
                              if (x & A) == A and (x & B) == 0))
            temoins.append((A, B))
    for k in range(0, len(on) + 1):
        for combo in itertools.combinations(range(len(termes)), k):
            u = set()
            for i in combo:
                u |= termes[i]
            if set(on) <= u:
                return k, [temoins[i] for i in combo]
    return None, None


def v5_echafaudage(n):
    t0 = time.time()
    N = 1 << n
    pire_poids = 0
    total = 0
    for masque in range(1, (1 << N) - 1):     # non constantes
        g = [(masque >> e) & 1 for e in range(N)]
        r, cover = dnf_size_totale(g, n)
        alpha, beta = r + 1, (r + 1) * (n + 1)
        # monomes de l'echafaudage sur 2n variables (y = bas, z = haut)
        poly = []                              # (masque 2n bits, coeff)
        for i in range(n):
            poly.append((1 << i, alpha))               # y_i
            poly.append((1 << (n + i), alpha))         # z_i
            poly.append(((1 << i) | (1 << (n + i)), beta))  # y_i z_i
        for (A, B) in cover:
            poly.append((A | (B << n), 1))
        poids = sum(c for _, c in poly)
        assert poids == 2 * n * alpha + n * beta + r
        uns, zeros = set(), set()
        for w in range(1 << (2 * n)):
            val = sum(c for S, c in poly if (w & S) == S)
            y, z = w & (N - 1), w >> n
            estun = (z == comp3(y, n)) and g[y] == 1
            (uns if estun else zeros).add(val)
        assert not (uns & zeros), (masque, sorted(uns & zeros))
        pire_poids = max(pire_poids, poids)
        total += 1
    print(f"V5 n={n} : l'echafaudage (alpha=r+1, beta=alpha(n+1)) SEPARE "
          f"f_g pour les {total} g non constantes ; poids = "
          f"2n.alpha + n.beta + r, max observe {pire_poids} "
          f"(temoin injectif trivial : {(1 << (2 * n)) - 1}) "
          f"({time.time()-t0:.0f}s)", flush=True)


# ------------------------------------------------------------------- main

def main():
    quick = "quick" in sys.argv
    v1_effondrement_monotone(3)
    if not quick:
        v1_effondrement_monotone(4)
    v2_liste_egale_setcover()
    v3a_rails_doubles_prescrit()
    v3b_rails_doubles_libre(2, [[(m >> e) & 1 for e in range(4)]
                                for m in range(1, 15)])
    gs3 = []
    while len(gs3) < 25:
        m = random.randint(1, 254)
        g = [(m >> e) & 1 for e in range(8)]
        if any(g) and not all(g):
            gs3.append(g)
    v3b_rails_doubles_libre(3, gs3)
    v4_packing(3)
    v5_echafaudage(2)
    v5_echafaudage(3)
    print("TOUTES LES VERIFICATIONS PASSENT.")


if __name__ == "__main__":
    main()
