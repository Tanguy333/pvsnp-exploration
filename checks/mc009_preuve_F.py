# -*- coding: utf-8 -*-
r"""MC-009 — Prouver C-MC008 : outillage de preuve.

La réduction M (fiche MC-009 §2, prouvée sur papier) réduit C-MC008 aux
CŒURS m = 0 :
  * cœur comparable   : paire {0-point, v},  |v| = b ≥ 2, o dehors ;
    loi visée F = b + 2o ;
  * cœur incomparable : paire {u, v} à supports disjoints, |u| = a ≥ 1,
    |v| = b ≥ a, o dehors ; loi visée F = 2(a+b+o) − max(2, b).

Modes :
  reduction : vérifie numériquement l'EXACTITUDE de la réduction M —
      F(a,b,m,o) = F(a,b,0,o) sur ν−m variables (a ≥ 1), et le saut +1 du
      comparable à la transition m = 1 → 0 — sur toute la table ν ≤ 5 et
      des points ν = 6.
  temoins : extrait les témoins OPTIMAUX des cœurs (CP-SAT) et les
      imprime en forme BLOC-SYMÉTRIQUE : coefficients groupés par
      signature (|S∩A|, |S∩B|, |S∩O|) — la donnée pour généraliser les
      constructions.
  constructions : vérifie les constructions générales de la fiche
      (majorants) par évaluation par blocs sur une grande grille.
  minorants : vérifie les arguments de minorant là où ils sont codables
      (forçage des singletons du cœur comparable, sauts d_j).

Conventions : A = bits 0..a−1 (support propre de u), B = bits a..a+b−1
(support propre de v), O = bits a+b..ν−1 (dehors). Points : u = A, v = B
(cœur incomparable) ; u = ∅, v = B (cœur comparable, a = 0).
"""
import sys
import time
from itertools import combinations_with_replacement

from ortools.sat.python import cp_model


def W_cpsat_temoin(uns, nvars, cap, tl=900):
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
    if st != cp_model.OPTIMAL:
        return None, None, str(st)
    temoin = {S: solver.Value(a[S]) for S in monomes if solver.Value(a[S])}
    su = set(uns)
    v1, v0 = set(), set()
    for x in range(N):
        p = sum(c for S, c in temoin.items() if S & x == S)
        (v1 if x in su else v0).add(p)
    assert not (v1 & v0) and sum(temoin.values()) == solver.Value(tot)
    return solver.Value(tot), temoin, "OPTIMAL"


def signature(S, na, nb):
    sa = bin(S & ((1 << na) - 1)).count("1")
    sb = bin((S >> na) & ((1 << nb) - 1)).count("1")
    so = bin(S >> (na + nb)).count("1")
    return (sa, sb, so)


def loi_coeur(na, nb, o):
    """ATTENTION (VER-MC-1) : ceci est l'ANCIENNE loi C-MC008, conservée
    À DESSEIN comme comparateur du mode temoins — c'est elle qui a détecté
    la réfutation ((3,3,0,0) : ECART). La loi corrigée est loi_corrigee."""
    nu = na + nb + o
    if na == 0:
        return nb + 2 * o
    return 2 * nu - max(2, nb, na)


def run_temoins():
    print("=== TÉMOINS OPTIMAUX DES CŒURS (forme bloc-symétrique) ===")
    plafond = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    configs = ([(0, b, o) for b in (2, 3, 4) for o in (0, 1, 2, 3)
                if b + o <= plafond]
               + [(a, b, o) for a in (1, 2, 3) for b in (1, 2, 3, 4)
                  for o in (0, 1, 2, 3) if a <= b and a + b + o <= plafond])
    for na, nb, o in configs:
        nu = na + nb + o
        u = (1 << na) - 1            # A
        v = ((1 << nb) - 1) << na    # B
        uns = sorted({u, v})
        if u == 0 and nb + o == 0:
            continue
        w, temoin, st = W_cpsat_temoin(uns, nu, (1 << nu) - 1)
        attendu = loi_coeur(na, nb, o)
        marque = "CONFORME" if w == attendu else f"!!! ECART (loi {attendu})"
        groupes = {}
        for S, c in temoin.items():
            groupes.setdefault(signature(S, na, nb), []).append(c)
        profil = {sig: sorted(cs) for sig, cs in sorted(groupes.items())}
        print(f"  (a={na}, b={nb}, o={o}, ν={nu}) : F = {w} [{st}] {marque}")
        print(f"      profil (|S∩A|,|S∩B|,|S∩O|) → coeffs : {profil}")


def run_reduction():
    print("=== LA RÉDUCTION M — vérification numérique de l'exactitude ===")
    # points de la table MC-008 (ν ≤ 5) reconstruits ici indépendamment
    def W_brute(uns, nvars, cap):
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
                    p = sum(c for T, c in coeffs.items() if T & x == T)
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

    ecarts = 0
    for nu in (3, 4, 5):
        for a in range(0, nu + 1):
            for b in range(max(a, 1), nu + 1):
                for m in range(1, nu - a - b + 1):
                    o = nu - a - b - m
                    # points : A puis B puis M puis O
                    u = ((1 << a) - 1) | (((1 << m) - 1) << (a + b))
                    v = (((1 << b) - 1) << a) | (((1 << m) - 1) << (a + b))
                    if u == v:
                        continue
                    Wm = (W_brute(sorted({u, v}), nu, (1 << nu) - 1)
                          if nu <= 4 else
                          W_cpsat_temoin(sorted({u, v}), nu, (1 << nu) - 1)[0])
                    u0 = (1 << a) - 1
                    v0m = ((1 << b) - 1) << a
                    nu0 = a + b + o
                    if u0 == 0 and v0m == 0:
                        continue
                    W0 = (W_brute(sorted({u0, v0m}), nu0, (1 << nu0) - 1)
                          if nu0 <= 4 else
                          W_cpsat_temoin(sorted({u0, v0m}), nu0,
                                         (1 << nu0) - 1)[0])
                    saut = 1 if (a == 0 and m >= 1) else 0
                    # réduction en chaîne : m étapes ; saut +1 seulement à la
                    # transition m=1 -> 0 du comparable (0-point créé)
                    attendu = W0 + saut
                    if Wm != attendu:
                        ecarts += 1
                        print(f"  ÉCART : (a={a},b={b},m={m},o={o},ν={nu}) : "
                              f"F = {Wm} ≠ F(m=0;ν−m) + saut = {W0}+{saut}")
    print(f"  {'RÉDUCTION M EXACTE sur toute la grille ν ≤ 5' if ecarts == 0 else f'{ecarts} écarts'}")


def evalue_par_blocs(regles, na, nb, o, uns_sig):
    """Évalue une construction bloc-symétrique par comptages.
    regles : dict signature (i, j, k) → coefficient (chaque monôme de cette
    signature reçoit ce coefficient). Renvoie (poids, séparant?)."""
    from math import comb
    poids = 0
    for (i, j, k), c in regles.items():
        poids += c * comb(na, i) * comb(nb, j) * comb(o, k)
    valeurs = {}
    for wa in range(na + 1):
        for wb in range(nb + 1):
            for wo in range(o + 1):
                val = 0
                for (i, j, k), c in regles.items():
                    if i <= wa and j <= wb and k <= wo:
                        val += c * comb(wa, i) * comb(wb, j) * comb(wo, k)
                valeurs.setdefault((wa, wb, wo), val)
    # ATTENTION : par bloc-symétrie, tous les points de même (wa, wb, wo)
    # ont la même valeur — il suffit de comparer les signatures.
    v1 = {valeurs[s] for s in uns_sig}
    v0 = {v for s, v in valeurs.items() if s not in uns_sig}
    return poids, not (v1 & v0)


def run_constructions():
    print("=== CONSTRUCTIONS GÉNÉRALES (majorants) — évaluation par blocs ===")
    from math import comb
    ok_tout = True
    # Cœur comparable (0, b, o), b >= 2 : cible b + 2o.
    # Construction C1 : singletons B à 1 ; singletons O à 2 ;
    #                   paires BB à ... — À REMPLIR d'après les témoins.
    # (les règles ci-dessous sont celles retenues dans la fiche §4 ;
    #  ce mode les vérifie sur la grille)
    try:
        from mc009_regles import REGLES_COMPARABLE, REGLES_INCOMPARABLE
    except ImportError:
        print("  (mc009_regles.py absent — mode constructions inactif tant que")
        print("   les témoins n'ont pas été généralisés ; voir la fiche)")
        return
    for b in range(2, 9):
        for o in range(0, 9):
            regles = REGLES_COMPARABLE(b, o)
            poids, sep = evalue_par_blocs(regles, 0, b, o,
                                          uns_sig={(0, 0, 0), (0, b, 0)})
            cible = b + 2 * o
            if not sep or poids != cible:
                ok_tout = False
                print(f"  comparable (b={b}, o={o}) : poids {poids} "
                      f"(cible {cible}), séparant : {sep}")
    for a in range(1, 9):
        for b in range(max(a, 1), 9):
            for o in range(0, 9):
                regles = REGLES_INCOMPARABLE(a, b, o)
                poids, sep = evalue_par_blocs(regles, a, b, o,
                                              uns_sig={(a, 0, 0), (0, b, 0)})
                cible = loi_corrigee(a, b, o)
                if not sep or poids != cible:
                    ok_tout = False
                    print(f"  incomparable (a={a}, b={b}, o={o}) : poids "
                          f"{poids} (cible {cible}), séparant : {sep}")
    print("  " + ("TOUTES LES CONSTRUCTIONS CONFORMES ET AU POIDS DE C-MC009 "
                  "(grille a,b ≤ 8, o ≤ 8 ; (1,1) inclus depuis VER-MC-1)"
                  if ok_tout else "des règles échouent — voir ci-dessus"))


def loi_corrigee(na, nb, o):
    """C-MC009 (post-réfutation de C-MC008 au point (3,3,0,0)) :
    cœur comparable (a=0) : b + 2o ; cœur incomparable (1 ≤ a ≤ b) :
    2(a+b+o) − max(b, 2, a+b−2)."""
    if na == 0:
        return nb + 2 * o
    return 2 * (na + nb + o) - max(nb, 2, na + nb - 2)


def run_confirme():
    print("=== C-MC009 — points de contrôle NEUFS (hors plage d'ajustement) ===")
    configs = [(1, 5, 0), (3, 3, 1), (3, 4, 0), (2, 5, 0), (1, 5, 1),
               (1, 6, 0), (2, 4, 1)]
    t0 = time.time()
    for na, nb, o in configs:
        nu = na + nb + o
        u = (1 << na) - 1
        v = ((1 << nb) - 1) << na
        w, temoin, st = W_cpsat_temoin(sorted({u, v}), nu, (1 << nu) - 1,
                                       tl=1800)
        pred = loi_corrigee(na, nb, o)
        if st != "OPTIMAL":
            print(f"  (a={na}, b={nb}, o={o}, ν={nu}) : NON CONCLU ({st})"
                  f"  [{time.time()-t0:.0f}s]")
            continue
        marque = "CONFORME" if w == pred else f"!!! REFUTE C-MC009 (prédit {pred})"
        print(f"  (a={na}, b={nb}, o={o}, ν={nu}) : F = {w} — {marque}"
              f"  [{time.time()-t0:.0f}s]")


if __name__ == "__main__":
    quel = sys.argv[1] if len(sys.argv) > 1 else "temoins"
    if quel in ("tout", "reduction"):
        run_reduction()
    if quel in ("tout", "temoins"):
        run_temoins()
    if quel in ("tout", "confirme"):
        run_confirme()
    if quel in ("tout", "constructions"):
        run_constructions()
