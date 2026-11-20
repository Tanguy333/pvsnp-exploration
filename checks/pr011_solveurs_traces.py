# -*- coding: utf-8 -*-
r"""PR-011 — Contre-vérification exécutable de la candidature n° 8 (entrée de
registre E-4 : « les solveurs comme recherche de preuves »).

Le mécanisme instruit : « la trace est une preuve » — sur toute entrée
insatisfiable, l'exécution d'un solveur complet est une réfutation dans un
système de preuves S fixé, donc temps >= taille de la plus courte
réfutation dans S (borne inférieure), et le solveur atteint les bornes
supérieures de S à branchement près (réciproque : BKS04, PD11, AFT11).

DOUBLE CALIBRATION (implémentation INDÉPENDANTE de la candidature) :
  - familles : PHP_n (n+1 pigeons, n trous — Haken 1985 : toute
    réfutation par résolution est de taille 2^{Omega(n)}) ; Peb(P_h)
    (contradiction de pebbling OR sur la pyramide de hauteur h, deux
    variables par sommet — BIW04 : résolution arborescente 2^{Omega(h)},
    résolution générale/régulière polynomiale) ;
  - solveurs : DPLL minimal SANS apprentissage (propagation unitaire,
    heuristique fixe = plus petite variable libre ; la trace est une
    réfutation ARBORESCENTE) ; CDCL = CaDiCaL 1.9.5 via pysat (la trace
    est une réfutation par résolution générale à extension près).
  - mesures (définies) : noeuds(F) = nombre de noeuds de branchement du
    DPLL jusqu'à UNSAT ; conflits(F) = nombre de conflits de CaDiCaL
    jusqu'à UNSAT (accum_stats()['conflicts']).
  - table 2x2 prédite par théorèmes : PHP/DPLL exp, PHP/CDCL exp,
    Peb/DPLL exp (contrôles) ; Peb/CDCL polynomial (la cellule qui teste
    le mécanisme dans son sens borne-supérieure).

ANTÉRIORITÉ DÉCLARÉE : BKS04 §5 (zChaff contre DPLL sur pebbling —
réplication vérifiante) ; Haken 1985 / BIW04 (théorèmes) ; table exacte
de conflits par n : [NON TROUVÉ] — mesure, pas découverte.

Usage : python -u checks/pr011_solveurs_traces.py [--php-max 11]
        [--peb-max 40] [--dpll-budget 3000000] [--conf-budget 20000000]
"""
from __future__ import annotations

import argparse
import math
import sys
import time


# ----------------------------------------------------------------------
# Générateurs
# ----------------------------------------------------------------------
def php(n):
    """PHP_n : n+1 pigeons, n trous. Variable p(i,j) = pigeon i dans trou j
    (i in 0..n, j in 0..n-1), numérotée 1 + i*n + j. Rend (nvars, clauses)."""
    def v(i, j):
        return 1 + i * n + j
    cl = []
    for i in range(n + 1):
        cl.append([v(i, j) for j in range(n)])            # chaque pigeon a un trou
    for j in range(n):
        for i1 in range(n + 1):
            for i2 in range(i1 + 1, n + 1):
                cl.append([-v(i1, j), -v(i2, j)])          # au plus un pigeon par trou
    return (n + 1) * n, cl


def peb_pyramide(h):
    """Contradiction de pebbling OR (BIW04) sur la pyramide de hauteur h :
    sommets (r, c), r = 0..h-1 (r = 0 : les h sources), c = 0..h-1-r ;
    (r, c) a pour prédécesseurs (r-1, c) et (r-1, c+1) ; puits (h-1, 0).
    Deux variables par sommet : x(v,1), x(v,2).
    Clauses : sources : x1 v x2 ; sommet interne v de prédécesseurs a, b :
    pour i, j in {1,2} : ~a_i v ~b_j v v_1 v v_2 ; puits : ~t_1, ~t_2."""
    idx = {}
    for r in range(h):
        for c in range(h - r):
            idx[(r, c)] = len(idx)

    def x(v, k):          # k in {1, 2}
        return 1 + 2 * idx[v] + (k - 1)
    cl = []
    for c in range(h):
        cl.append([x((0, c), 1), x((0, c), 2)])
    for r in range(1, h):
        for c in range(h - r):
            a, b, v = (r - 1, c), (r - 1, c + 1), (r, c)
            for i in (1, 2):
                for j in (1, 2):
                    cl.append([-x(a, i), -x(b, j), x(v, 1), x(v, 2)])
    t = (h - 1, 0)
    cl.append([-x(t, 1)])
    cl.append([-x(t, 2)])
    return 2 * len(idx), cl


# ----------------------------------------------------------------------
# DPLL minimal (sans apprentissage) — trace = réfutation arborescente
# ----------------------------------------------------------------------
class Budget(Exception):
    pass


def dpll(nvars, clauses, budget):
    """Rend (resultat, noeuds). resultat in {'UNSAT', 'SAT'} ; lève Budget
    si le nombre de noeuds de branchement dépasse budget."""
    assign = [0] * (nvars + 1)      # 0 libre, +1 vrai, -1 faux
    noeuds = [0]

    def propage(trail):
        """Propagation unitaire naïve ; rend False en cas de conflit."""
        changed = True
        while changed:
            changed = False
            for c in clauses:
                sat = False
                libres = []
                for lit in c:
                    a = assign[abs(lit)]
                    if a == 0:
                        libres.append(lit)
                    elif (a > 0) == (lit > 0):
                        sat = True
                        break
                if sat:
                    continue
                if not libres:
                    return False
                if len(libres) == 1:
                    lit = libres[0]
                    assign[abs(lit)] = 1 if lit > 0 else -1
                    trail.append(abs(lit))
                    changed = True
        return True

    def rec():
        trail = []
        ok = propage(trail)
        if not ok:
            for v in trail:
                assign[v] = 0
            return False
        # variable libre la plus petite (heuristique fixe)
        var = next((v for v in range(1, nvars + 1) if assign[v] == 0), None)
        if var is None:
            return True
        noeuds[0] += 1
        if noeuds[0] > budget:
            raise Budget()
        for val in (1, -1):
            assign[var] = val
            sub = [var]
            if rec():
                return True
            assign[var] = 0
        for v in trail:
            assign[v] = 0
        return False

    sys.setrecursionlimit(max(10000, 4 * nvars + 100))
    res = rec()
    return ("SAT" if res else "UNSAT"), noeuds[0]


# ----------------------------------------------------------------------
# CDCL = CaDiCaL via pysat — trace = réfutation par résolution (+ext.)
# ----------------------------------------------------------------------
def cdcl(clauses, conf_budget):
    from pysat.solvers import Solver
    with Solver(name="cadical195", bootstrap_with=clauses) as S:
        S.conf_budget(conf_budget)
        t0 = time.time()
        r = S.solve_limited()
        dt = time.time() - t0
        st = S.accum_stats()
        res = "NON CONCLU (budget)" if r is None else ("SAT" if r else "UNSAT")
        return res, st.get("conflicts"), st.get("decisions"), dt


# ----------------------------------------------------------------------
# Ajustements (log2 par pas ; pente log-log)
# ----------------------------------------------------------------------
def pente_log2(xs, ys):
    """pente moyenne de log2(y) par unité de x (ajustement des moindres
    carrés sur les points y > 0)."""
    pts = [(x, math.log2(y)) for x, y in zip(xs, ys) if y and y > 0]
    if len(pts) < 2:
        return None
    n = len(pts)
    mx = sum(p[0] for p in pts) / n
    my = sum(p[1] for p in pts) / n
    num = sum((p[0] - mx) * (p[1] - my) for p in pts)
    den = sum((p[0] - mx) ** 2 for p in pts)
    return num / den if den else None


def pente_loglog(xs, ys):
    pts = [(math.log2(x), math.log2(y)) for x, y in zip(xs, ys) if x > 1 and y and y > 0]
    if len(pts) < 2:
        return None
    n = len(pts)
    mx = sum(p[0] for p in pts) / n
    my = sum(p[1] for p in pts) / n
    num = sum((p[0] - mx) * (p[1] - my) for p in pts)
    den = sum((p[0] - mx) ** 2 for p in pts)
    return num / den if den else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--php-min", type=int, default=4)
    ap.add_argument("--php-max", type=int, default=11)
    ap.add_argument("--peb-min", type=int, default=4)
    ap.add_argument("--peb-max", type=int, default=40)
    ap.add_argument("--dpll-budget", type=int, default=3_000_000)
    ap.add_argument("--dpll-peb-max", type=int, default=20)
    ap.add_argument("--conf-budget", type=int, default=20_000_000)
    args = ap.parse_args()

    print("PR-011 — solveurs certifiants sur PHP_n et Peb(P_h) ; mesures : "
          "noeuds DPLL (arborescent) / conflits CaDiCaL (résolution)", flush=True)

    # ---------------- PHP ----------------
    print("\n=== PHP_n (Haken : 2^{Omega(n)} pour la résolution) ===", flush=True)
    print(f"{'n':>3} {'vars':>5} {'cls':>6} | {'DPLL':>9} {'noeuds':>10} {'s':>7} | "
          f"{'CDCL':>9} {'conflits':>10} {'decis.':>10} {'s':>8}", flush=True)
    php_ns, php_dpll, php_cdcl = [], [], []
    dpll_actif = True
    for n in range(args.php_min, args.php_max + 1):
        nv, cl = php(n)
        # DPLL
        if dpll_actif:
            t0 = time.time()
            try:
                res_d, nd = dpll(nv, cl, args.dpll_budget)
                dt_d = time.time() - t0
                sd = f"{res_d:>9} {nd:>10} {dt_d:>7.1f}"
                php_dpll.append(nd if res_d == "UNSAT" else None)
            except Budget:
                dt_d = time.time() - t0
                sd = f"{'BUDGET':>9} {'>' + str(args.dpll_budget):>10} {dt_d:>7.1f}"
                php_dpll.append(None)
                dpll_actif = False
        else:
            sd = f"{'—':>9} {'—':>10} {'—':>7}"
            php_dpll.append(None)
        # CDCL
        res_c, conf, dec, dt_c = cdcl(cl, args.conf_budget)
        php_cdcl.append(conf if res_c == "UNSAT" else None)
        php_ns.append(n)
        print(f"{n:>3} {nv:>5} {len(cl):>6} | {sd} | {res_c:>9} {conf:>10} {dec:>10} {dt_c:>8.1f}",
              flush=True)
    p1 = pente_log2([n for n, y in zip(php_ns, php_dpll) if y], [y for y in php_dpll if y])
    p2 = pente_log2([n for n, y in zip(php_ns, php_cdcl) if y], [y for y in php_cdcl if y])
    print(f"  pente log2(noeuds DPLL)/n   = {p1 if p1 is None else round(p1, 2)}  "
          f"(facteur x{None if p1 is None else round(2 ** p1, 2)} par pigeon)")
    print(f"  pente log2(conflits CDCL)/n = {p2 if p2 is None else round(p2, 2)}  "
          f"(facteur x{None if p2 is None else round(2 ** p2, 2)} par pigeon)")

    # ---------------- Peb ----------------
    print("\n=== Peb(P_h), pyramide de hauteur h (BIW04 : arborescent 2^{Omega(h)}, "
          "général polynomial) ===", flush=True)
    print(f"{'h':>3} {'vars':>5} {'cls':>6} | {'DPLL':>9} {'noeuds':>10} {'s':>7} | "
          f"{'CDCL':>9} {'conflits':>10} {'decis.':>10} {'s':>8}", flush=True)
    peb_hs, peb_dpll, peb_cdcl = [], [], []
    dpll_actif = True
    for h in range(args.peb_min, args.peb_max + 1):
        nv, cl = peb_pyramide(h)
        if dpll_actif and h <= args.dpll_peb_max:
            t0 = time.time()
            try:
                res_d, nd = dpll(nv, cl, args.dpll_budget)
                dt_d = time.time() - t0
                sd = f"{res_d:>9} {nd:>10} {dt_d:>7.1f}"
                peb_dpll.append(nd if res_d == "UNSAT" else None)
            except Budget:
                dt_d = time.time() - t0
                sd = f"{'BUDGET':>9} {'>' + str(args.dpll_budget):>10} {dt_d:>7.1f}"
                peb_dpll.append(None)
                dpll_actif = False
        else:
            sd = f"{'—':>9} {'—':>10} {'—':>7}"
            peb_dpll.append(None)
        res_c, conf, dec, dt_c = cdcl(cl, args.conf_budget)
        peb_cdcl.append(conf if res_c == "UNSAT" else None)
        peb_hs.append(h)
        print(f"{h:>3} {nv:>5} {len(cl):>6} | {sd} | {res_c:>9} {conf:>10} {dec:>10} {dt_c:>8.1f}",
              flush=True)
    q1 = pente_log2([h for h, y in zip(peb_hs, peb_dpll) if y], [y for y in peb_dpll if y])
    q2 = pente_loglog([h for h, y in zip(peb_hs, peb_cdcl) if y], [y for y in peb_cdcl if y])
    q2e = pente_log2([h for h, y in zip(peb_hs, peb_cdcl) if y], [y for y in peb_cdcl if y])
    print(f"  pente log2(noeuds DPLL)/h        = {q1 if q1 is None else round(q1, 2)}  "
          f"(facteur x{None if q1 is None else round(2 ** q1, 2)} par niveau)")
    print(f"  pente log-log conflits CDCL vs h = {q2 if q2 is None else round(q2, 2)}  "
          f"(exposant polynomial apparent)")
    print(f"  pente log2(conflits CDCL)/h      = {q2e if q2e is None else round(q2e, 2)}  "
          f"(facteur x{None if q2e is None else round(2 ** q2e, 3)} par niveau — "
          f"~1 si polynomial)")


if __name__ == "__main__":
    main()
