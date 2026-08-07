# -*- coding: utf-8 -*-
"""MC-003 — Le test de la voie nommée par MC-001 : W(f_g) est-il contrôlé
par r = dnf-size(g) sur les instances rails-doubles ?

f_g(y, z) = 1  ssi  z = ȳ  et  g(y) = 1   (Prop. 5 de MC-001, 2n variables).

Pour toutes les g non constantes (représentants des classes sous S_n) à
n = 2 puis n = 3 :
  - r(g)      : dnf-size exacte (couverture minimale des uns par implicants
                premiers — force brute, n ≤ 3) ;
  - W(f_g)    : poids SYM+ minimal exact — CP-SAT canal de valeurs
                (minimisation, statut OPTIMAL exigé), témoin RE-VÉRIFIÉ par
                évaluation indépendante, et à n = 2 recoupé par une
                énumération force brute SANS solveur ;
  - invariants de contrôle : #uns(g), W(g), monotonie de g.

Questions posées aux données (aucune extrapolation au-delà — q.12) :
  Q1. W(f_g) est-il une FONCTION de r ?  (dispersion par valeur de r)
  Q2. W(f_g) est-il MONOTONE en r ?      (chevauchement des plages)
  Q3. le vrai contrôleur est-il plutôt #uns(g) (= #uns(f_g)) ?
  Q4. la borne packing (Lemme 4) atteint-elle W sur ces instances ?
      (échantillon : les cas extrêmes de chaque r à n = 3, tous à n = 2)

Faits structurels vérifiés au passage : f_g(0) = 0, f_g(1^{2n}) = 0, donc
AUCUN implicant positif (lemme d'obstruction de MC-001) — les instances
vivent entièrement dans le régime valeurs/zoo ; les uns de f_g forment une
ANTICHAÎNE (tous de poids de Hamming n), donc l'alternance (F-020) est ≤ 2 :
seul le packing peut fournir une borne inférieure combinatoire ici.
"""
import sys
import time
from itertools import combinations, combinations_with_replacement, permutations

try:
    from ortools.sat.python import cp_model
except ImportError:
    print("ortools indisponible", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------- outils g
def uns_de(masque, n):
    return [x for x in range(1 << n) if masque >> x & 1]


def dnf_size(masque, n):
    """dnf-size exacte de g : couverture minimale des uns par sous-cubes
    inclus dans les uns (implicants). Force brute sur les implicants
    premiers, n <= 3."""
    N = 1 << n
    uns = set(uns_de(masque, n))
    if not uns:
        return 0
    # sous-cubes : (fixe, valeurs) — représentés par (masque_libre, base)
    implicants = []  # ensembles de points couverts
    for libre in range(N):  # bits libres du cube
        fixes = (N - 1) ^ libre
        bases = set()
        for x in range(N):
            bases.add(x & fixes)
        for b in bases:
            pts = []
            ok = True
            sous = libre
            while True:
                p = b | sous
                if p not in uns:
                    ok = False
                    break
                pts.append(p)
                if sous == 0:
                    break
                sous = (sous - 1) & libre
            if ok:
                implicants.append(frozenset(pts))
    # premiers = maximaux pour l'inclusion
    implicants = list(set(implicants))
    premiers = [I for I in implicants
                if not any(I < J for J in implicants)]
    # couverture minimale (force brute croissante)
    for r in range(1, len(uns) + 1):
        for combo in combinations(premiers, r):
            couv = set().union(*combo)
            if uns <= couv:
                return r
    return len(uns)


def canonique_Sn(masque, n):
    """Représentant canonique de g sous S_n (permutation des variables)."""
    best = None
    for perm in permutations(range(n)):
        m2 = 0
        for x in range(1 << n):
            y = 0
            for i in range(n):
                if x >> i & 1:
                    y |= 1 << perm[i]
            if masque >> x & 1:
                m2 |= 1 << y
        if best is None or m2 < best:
            best = m2
    return best


def est_monotone(masque, n):
    for x in range(1 << n):
        if masque >> x & 1:
            continue
        for i in range(n):
            if x >> i & 1 and masque >> (x & ~(1 << i)) & 1:
                return False
    return True


# ------------------------------------------------------------- instance f_g
def table_fg(masque_g, n):
    """f_g sur 2n variables : x = (y | z<<n) ; f_g = [z = ȳ et g(y) = 1]."""
    plein = (1 << n) - 1
    uns = []
    for y in range(1 << n):
        if masque_g >> y & 1:
            z = (~y) & plein
            uns.append(y | (z << n))
    return uns


# ----------------------------------------------------- W exact (deux voies)
def W_cpsat(uns, nvars, cap, tl=120):
    """Poids minimal par CP-SAT (canal de valeurs). Renvoie
    (W, temoin, statut) ; statut 'OPTIMAL' exigé pour conclure."""
    N = 1 << nvars
    zeros = [x for x in range(N) if x not in set(uns)]
    monomes = list(range(1, N))
    model = cp_model.CpModel()
    a = {S: model.NewIntVar(0, cap, f"a{S}") for S in monomes}
    tot = model.NewIntVar(0, cap, "tot")
    model.Add(tot == sum(a.values()))
    val = {}
    for x in range(N):
        val[x] = model.NewIntVar(0, cap, f"v{x}")
        actifs = [a[S] for S in monomes if S & x == S]
        model.Add(val[x] == (sum(actifs) if actifs else 0))
    for u in uns:
        for v in zeros:
            model.Add(val[u] != val[v])
    model.Minimize(tot)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tl
    solver.parameters.num_search_workers = 8
    st = solver.Solve(model)
    if st == cp_model.OPTIMAL:
        temoin = {S: solver.Value(a[S]) for S in monomes if solver.Value(a[S])}
        return solver.Value(tot), temoin, "OPTIMAL"
    if st == cp_model.FEASIBLE:
        return solver.Value(tot), None, "FEASIBLE"
    return None, None, str(st)


def verifie_temoin(uns, nvars, temoin, W_annonce):
    """Évaluation indépendante du témoin (sans solveur)."""
    N = 1 << nvars
    su = set(uns)
    assert sum(temoin.values()) == W_annonce, "poids incohérent"
    v1, v0 = set(), set()
    for x in range(N):
        p = sum(c for S, c in temoin.items() if S & x == S)
        (v1 if x in su else v0).add(p)
    assert not (v1 & v0), "témoin non séparant"
    return True


def W_brute(uns, nvars, cap):
    """Force brute pure (sans solveur), poids croissant — pour n = 2
    (2n = 4, 15 monômes)."""
    N = 1 << nvars
    su = set(uns)
    monomes = list(range(1, N))
    for s in range(0, cap + 1):
        for combo in combinations_with_replacement(monomes, s):
            coeffs = {}
            for S in combo:
                coeffs[S] = coeffs.get(S, 0) + 1
            v1, v0 = set(), set()
            ok = True
            for x in range(N):
                p = sum(c for S, c in coeffs.items() if S & x == S)
                if x in su:
                    if p in v0:
                        ok = False
                        break
                    v1.add(p)
                else:
                    if p in v1:
                        ok = False
                        break
                    v0.add(p)
            if ok:
                return s
    return None


# --------------------------------------------------- packing (Lemme 4) exact
def packing_cpsat(uns, nvars, tl=60):
    """Borne d'empaquetage maximale (Lemme 4 de MC-001) : paires (u, v),
    supp(v) ⊊ supp(u), f(u) ≠ f(v), ensembles-différences D_i disjoints."""
    N = 1 << nvars
    su = set(uns)
    paires = []
    for u in range(N):
        v = (u - 1) & u
        # tous les v dont le support est strictement inclus dans celui de u
        sous = (u - 1) & u if u else 0
        v = sous
        while True:
            if (u in su) != (v in su):
                D = frozenset(S for S in range(1, N)
                              if S & u == S and not (S & v == S))
                paires.append((u, v, D))
            if v == 0:
                break
            v = (v - 1) & u
    model = cp_model.CpModel()
    b = [model.NewBoolVar(f"b{i}") for i in range(len(paires))]
    for i in range(len(paires)):
        for j in range(i + 1, len(paires)):
            if paires[i][2] & paires[j][2]:
                model.Add(b[i] + b[j] <= 1)
    model.Maximize(sum(b))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tl
    solver.parameters.num_search_workers = 8
    st = solver.Solve(model)
    if st == cp_model.OPTIMAL:
        return solver.Value(sum(b)), "OPTIMAL"
    if st == cp_model.FEASIBLE:
        return solver.Value(sum(b)), "FEASIBLE"
    return None, str(st)


# ------------------------------------------------------------------- run
def run_n(n, tl_w, faire_packing):
    N = 1 << n
    plein = (1 << (2 * n)) - 1
    vus, lignes = set(), []
    t0 = time.time()
    for masque in range(1, (1 << N) - 1):  # g non constantes
        can = canonique_Sn(masque, n)
        if can in vus:
            continue
        vus.add(can)
        g_uns = uns_de(can, n)
        r = dnf_size(can, n)
        uns_fg = table_fg(can, n)
        # faits structurels
        assert 0 not in uns_fg and plein not in uns_fg
        W, temoin, st = W_cpsat(uns_fg, 2 * n, cap=(1 << (2 * n)) - 1, tl=tl_w)
        if st != "OPTIMAL":
            lignes.append((can, r, len(g_uns), None, st, None))
            print(f"  g={can:>3} r={r} : NON CONCLU ({st})")
            continue
        verifie_temoin(uns_fg, 2 * n, temoin, W)
        if n == 2:  # recoupement sans solveur
            Wb = W_brute(uns_fg, 2 * n, cap=W + 1)
            assert Wb == W, f"désaccord brute/CP-SAT : {Wb} vs {W}"
        pk = None
        if faire_packing:
            pk, stp = packing_cpsat(uns_fg, 2 * n)
            if stp != "OPTIMAL":
                pk = f"{pk}?({stp})"
        lignes.append((can, r, len(g_uns), W, "OPTIMAL", pk))
        print(f"  g={can:>3} |uns|={len(g_uns)} r={r} : W(f_g)={W}"
              + (f"  packing={pk}" if pk is not None else "")
              + f"  [{time.time()-t0:.0f}s]")
    return lignes


def analyse(lignes, n):
    print(f"\n=== ANALYSE n={n} ===")
    ok = [l for l in lignes if l[3] is not None]
    nc = [l for l in lignes if l[3] is None]
    print(f"{len(ok)} classes conclues, {len(nc)} non conclues")
    # Q1/Q2 : dispersion et monotonie par r
    par_r = {}
    for can, r, ug, W, st, pk in ok:
        par_r.setdefault(r, []).append(W)
    print("r : [min W, max W]  (#classes)")
    for r in sorted(par_r):
        v = par_r[r]
        print(f"  r={r} : [{min(v)}, {max(v)}]  ({len(v)})"
              + ("  <-- DISPERSION" if min(v) != max(v) else ""))
    rs = sorted(par_r)
    print(f"Q1 fonction de r seul : "
          + ("OUI" if all(min(v) == max(v) for v in par_r.values()) else "NON"))
    # Q2 : trois niveaux — inversion / contact / gap strict, par frontière
    for i in range(len(rs) - 1):
        hi, lo = max(par_r[rs[i]]), min(par_r[rs[i + 1]])
        etat = ("GAP STRICT" if hi < lo else
                "CONTACT (valeur partagée — seuil ambigu)" if hi == lo else
                "INVERSION")
        print(f"Q2 frontière r={rs[i]}|{rs[i+1]} : max={hi} vs min={lo} → {etat}")
        if hi == lo:
            tem_bas = [l for l in ok if l[1] == rs[i] and l[3] == hi]
            tem_haut = [l for l in ok if l[1] == rs[i + 1] and l[3] == lo]
            print(f"    témoins : r={rs[i]} g∈{[l[0] for l in tem_bas]} ; "
                  f"r={rs[i+1]} g∈{[l[0] for l in tem_haut]}")
    # Q3 : contrôle par #uns, puis par le couple (r, #uns)
    par_u, par_ru = {}, {}
    for can, r, ug, W, st, pk in ok:
        par_u.setdefault(ug, []).append(W)
        par_ru.setdefault((r, ug), []).append(W)
    disp_u = sum(1 for v in par_u.values() if min(v) != max(v))
    disp_ru = {k: v for k, v in par_ru.items() if min(v) != max(v)}
    print(f"Q3 dispersion par #uns : {disp_u}/{len(par_u)} valeurs dispersées ; "
          f"par (r, #uns) : {len(disp_ru)}/{len(par_ru)} couples dispersés"
          + (f" — ex. {sorted(disp_ru)[:4]}" if disp_ru else ""))
    # Q4 : packing vs W
    avec_pk = [(can, r, W, pk) for can, r, ug, W, st, pk in ok
               if isinstance(pk, int)]
    if avec_pk:
        serres = sum(1 for _, _, W, pk in avec_pk if pk == W)
        print(f"Q4 packing = W : {serres}/{len(avec_pk)} ; "
              f"pire écart : {max(W - pk for _, _, W, pk in avec_pk)}")


if __name__ == "__main__":
    quel = sys.argv[1] if len(sys.argv) > 1 else "n2"
    if quel == "n2":
        print("=== n = 2 : toutes les g non constantes (classes S_2), "
              "f_g sur 4 variables — CP-SAT + recoupement force brute ===")
        lignes = run_n(2, tl_w=60, faire_packing=True)
        analyse(lignes, 2)
    elif quel == "n3":
        print("=== n = 3 : toutes les g non constantes (classes S_3), "
              "f_g sur 6 variables — CP-SAT (OPTIMAL exigé) ===")
        lignes = run_n(3, tl_w=180, faire_packing=False)
        analyse(lignes, 3)
        # packing sur les cas extrêmes par r
        print("\n=== packing (Lemme 4) sur les extrêmes de chaque r ===")
        ok = [l for l in lignes if l[3] is not None]
        par_r = {}
        for l in ok:
            par_r.setdefault(l[1], []).append(l)
        for r in sorted(par_r):
            v = sorted(par_r[r], key=lambda l: l[3])
            for l in {v[0][0]: v[0], v[-1][0]: v[-1]}.values():
                uns_fg = table_fg(l[0], 3)
                pk, stp = packing_cpsat(uns_fg, 6, tl=120)
                print(f"  r={r} g={l[0]} W={l[3]} : packing={pk} ({stp})")
    elif quel == "frontiere":
        # témoins des frontières en CONTACT à n = 3 : mêmes W, r différents
        print("=== témoins de frontière (n = 3) : structure des optima ===")
        for g in [234, 22, 235, 105]:
            r = dnf_size(g, 3)
            uns_fg = table_fg(g, 3)
            W, temoin, st = W_cpsat(uns_fg, 6, cap=63, tl=180)
            assert st == "OPTIMAL"
            verifie_temoin(uns_fg, 6, temoin, W)
            su = set(uns_fg)
            v1 = sorted({sum(c for S, c in temoin.items() if S & x == S)
                         for x in su})
            v0 = sorted({sum(c for S, c in temoin.items() if S & x == S)
                         for x in range(64) if x not in su})
            par_taille = {}
            for S, c in temoin.items():
                par_taille.setdefault(bin(S).count("1"), []).append(c)
            profil = {t: sorted(cs) for t, cs in sorted(par_taille.items())}
            print(f"g={g} (r={r}) : W={W}, {len(temoin)} monômes, "
                  f"profil taille→coeffs {profil}")
            print(f"    valeurs uns {v1} ; zéros {v0}")
    else:
        print("usage : mc003_rails_doubles.py [n2|n3|frontiere]")
