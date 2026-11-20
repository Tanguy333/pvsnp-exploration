# -*- coding: utf-8 -*-
r"""PR-014 — Contre-vérification exécutable de la candidature n° 9 (entrée de
registre E-5 : « l'apprentissage de classes de circuits ⟹ bornes »).

Le mécanisme instruit : chaque apprenant consomme une approximabilité de
bas degré sur un corps — Fourier (concentration de bas degré, LMN 1993 /
Jackson 1997 pour les DNF), ou polynômes sur F_p (Razborov-Smolensky ;
CIKK 2016). DOUBLE CALIBRATION (implémentation INDÉPENDANTE) : trois îles
d'apprenants et une fonction (MOD6) sur aucune.

Mesures (définies) :
  deg_F(f)      = degré du polynôme multilinéaire UNIQUE sur F coïncidant
                  avec f sur {0,1}^n (transformée de Möbius : c_S =
                  somme_{T⊆S} (-1)^{|S|-|T|} f(T) mod p ; deg = max |S| :
                  c_S != 0). Contrôle EXACT.
  W^{<=d}(f)    = somme_{|S|<=d} fhat(S)^2, f envoyée dans {+1,-1} par
                  f01 -> (-1)^{f01} ; fhat(S) = 2^-n somme_x f(x)(-1)^{<S,x>}.
                  (Parseval : W^{<=n} = 1.)
  adeg_{F,eps} = degré minimal d'un polynôme sur F coïncidant avec f sur
                  >= (1-eps) 2^n points (CP-SAT exact). Le degré APPROCHÉ,
                  la vraie mesure d'apprenabilité (Razborov-Smolensky).

Convention : MOD_m(x) = [ (somme x_i) ≡ 0 (mod m) ] ; PARITY(x) =
(somme x_i) mod 2. DNF aléatoires : k termes de largeur w, littéraux
tirés (graine consignée).

ANTÉRIORITÉ DÉCLARÉE : Smolensky 1987 (degrés F_p), LMN 1993
(concentration de Fourier de AC⁰), Jackson 1997 (DNF) — RÉPLICATION
VÉRIFIANTE, régime de contrôle ; la table exacte à petit n est une mesure.

Usage : python -u checks/pr014_apprentissage_degres.py [--deg-n 12]
        [--adeg-n 8] [--eps 0.125] [--seed 20260912]
"""
from __future__ import annotations

import argparse
import itertools
import random


# ----------------------------------------------------------------------
# Fonctions cibles : table de vérité comme liste de 0/1 indexée par x
# (x = entier 0..2^n-1, bit i = variable i)
# ----------------------------------------------------------------------
def popcount(x):
    return bin(x).count("1")


def f_parity(n):
    return [popcount(x) & 1 for x in range(1 << n)]


def f_mod(n, m):
    return [1 if popcount(x) % m == 0 else 0 for x in range(1 << n)]


def f_dnf(n, k, w, rng):
    """k termes de largeur w ; littéral = (variable, signe). Un terme est
    satisfait si tous ses littéraux le sont ; f = OR des termes."""
    termes = []
    for _ in range(k):
        vs = rng.sample(range(n), w)
        termes.append([(v, rng.randint(0, 1)) for v in vs])
    tt = []
    for x in range(1 << n):
        val = 0
        for term in termes:
            ok = 1
            for (v, s) in term:
                bit = (x >> v) & 1
                if bit != s:
                    ok = 0
                    break
            if ok:
                val = 1
                break
        tt.append(val)
    return tt


# ----------------------------------------------------------------------
# deg exact sur F_p (Möbius) et masse de Fourier
# ----------------------------------------------------------------------
def deg_Fp(tt, n, p):
    """Degré du polynôme multilinéaire unique sur F_p. Möbius rapide
    (transformée zêta signée par sous-ensembles via convolution sur les
    bits)."""
    # coefficients c[S] par Möbius : c = zeta^{-1} f. Sur {0,1}^n, la
    # transformée de Möbius subset : pour chaque bit, c[S] -= c[S sans bit].
    c = [v % p for v in tt]
    for i in range(n):
        bit = 1 << i
        for S in range(1 << n):
            if S & bit:
                c[S] = (c[S] - c[S ^ bit]) % p
    deg = 0
    for S in range(1 << n):
        if c[S] % p != 0:
            d = popcount(S)
            if d > deg:
                deg = d
    return deg


def fourier_weight_le(tt, n, d):
    """W^{<=d}(f) pour f = (-1)^{tt}. Walsh-Hadamard O(n 2^n)."""
    N = 1 << n
    a = [1 - 2 * b for b in tt]           # 0->+1, 1->-1
    # transformée de Walsh-Hadamard
    h = 1
    while h < N:
        for i in range(0, N, h * 2):
            for j in range(i, i + h):
                x, y = a[j], a[j + h]
                a[j], a[j + h] = x + y, x - y
        h *= 2
    # fhat(S) = a[S]/N ; W^{<=d} = somme_{|S|<=d} fhat(S)^2
    W = 0.0
    for S in range(N):
        if popcount(S) <= d:
            W += (a[S] / N) ** 2
    return W


# ----------------------------------------------------------------------
# adeg approché par CP-SAT
# ----------------------------------------------------------------------
def adeg_cpsat(tt, n, q, eps, dmax, tl=120):
    """Rend (adeg, [(d, accord_max)]). adeg = min d avec accord_max >=
    (1-eps) 2^n ; None si aucun d <= dmax. q = |F| (2 ou 3)."""
    from ortools.sat.python import cp_model
    N = 1 << n
    seuil = N - int(eps * N)          # >= (1-eps) N points d'accord
    # sous-ensembles par degré croissant
    subsets_by_deg = {d: [] for d in range(dmax + 1)}
    for S in range(N):
        dS = popcount(S)
        if dS <= dmax:
            subsets_by_deg[dS].append(S)
    trace = []
    subsets = []
    for d in range(dmax + 1):
        subsets += subsets_by_deg[d]
        # monômes : pour chaque x, liste des S (dans subsets) avec S ⊆ x
        model = cp_model.CpModel()
        c = {S: model.NewIntVar(0, q - 1, f"c{S}") for S in subsets}
        b = []
        for x in range(N):
            termes = [c[S] for S in subsets if (x & S) == S]
            s = model.NewIntVar(0, (q - 1) * len(termes), f"s{x}")
            model.Add(s == sum(termes))
            r = model.NewIntVar(0, q - 1, f"r{x}")
            model.AddModuloEquality(r, s, q)
            bx = model.NewBoolVar(f"b{x}")
            model.Add(r == tt[x]).OnlyEnforceIf(bx)
            model.Add(r != tt[x]).OnlyEnforceIf(bx.Not())
            b.append(bx)
        model.Maximize(sum(b))
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = tl
        solver.parameters.num_search_workers = 8
        st = solver.Solve(model)
        acc = int(solver.ObjectiveValue()) if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else -1
        opt = (st == cp_model.OPTIMAL)
        trace.append((d, acc, opt))
        if opt and acc >= seuil:
            return d, trace
    return None, trace


def borne_symetrique(tt, n, q, d):
    """Meilleur accord d'un polynôme SYMÉTRIQUE de degré <= d sur F_q :
    p(x) = somme_{j<=d} a_j * C(w, j) mod q, w = popcount(x) (base des
    polynômes symétriques). Énumération exhaustive des q^{d+1} choix —
    borne INFÉRIEURE sur l'accord maximal (un polynôme non symétrique
    peut faire mieux)."""
    from math import comb
    N = 1 << n
    poids = [popcount(x) for x in range(N)]
    best = -1
    for coeffs in itertools.product(range(q), repeat=d + 1):
        acc = 0
        for x in range(N):
            w = poids[x]
            v = sum(coeffs[j] * comb(w, j) for j in range(d + 1)) % q
            if v == tt[x]:
                acc += 1
        best = max(best, acc)
    return best


def focus_mod6(n, eps, tl, workers, degres):
    """Mode ciblé : MOD6 (et PARITY sur F3 en contrôle dur) à n variables,
    seuil (1-eps)2^n, degrés donnés, longue limite de temps, en cherchant
    un certificat d'OPTIMALITÉ (accord max < seuil => adeg > d prouvé)."""
    from ortools.sat.python import cp_model
    N = 1 << n
    seuil = N - int(eps * N)
    print(f"=== mode ciblé : n = {n}, eps = {eps} (seuil {seuil}/{N}), "
          f"tl = {tl} s, workers = {workers} ===", flush=True)
    cibles = [("MOD6", f_mod(n, 6), (2, 3)), ("PARITY", f_parity(n), (3,))]
    for nom, tt, corps in cibles:
        ones = sum(tt)
        print(f"\n-- {nom} : {ones} uns / {N} ; meilleur constant = {max(ones, N - ones)}",
              flush=True)
        for q in corps:
            for d in degres:
                bs = borne_symetrique(tt, n, q, d)
                subsets = [S for S in range(N) if popcount(S) <= d]
                model = cp_model.CpModel()
                c = {S: model.NewIntVar(0, q - 1, f"c{S}") for S in subsets}
                b = []
                for x in range(N):
                    termes = [c[S] for S in subsets if (x & S) == S]
                    s = model.NewIntVar(0, (q - 1) * len(termes), f"s{x}")
                    model.Add(s == sum(termes))
                    r = model.NewIntVar(0, q - 1, f"r{x}")
                    model.AddModuloEquality(r, s, q)
                    bx = model.NewBoolVar(f"b{x}")
                    model.Add(r == tt[x]).OnlyEnforceIf(bx)
                    model.Add(r != tt[x]).OnlyEnforceIf(bx.Not())
                    b.append(bx)
                model.Add(sum(b) >= bs)          # la borne symétrique est atteignable
                model.Maximize(sum(b))
                solver = cp_model.CpSolver()
                solver.parameters.max_time_in_seconds = tl
                solver.parameters.num_search_workers = workers
                st = solver.Solve(model)
                acc = int(solver.ObjectiveValue()) if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else -1
                bound = int(solver.BestObjectiveBound()) if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else -1
                statut = solver.StatusName(st)
                # Un certificat n'exige pas OPTIMAL : si la borne SUPÉRIEURE
                # prouvée par le solveur est < seuil, aucun polynôme de degré
                # <= d n'atteint le seuil — adeg > d est certifié (réserve
                # habituelle : la borne est celle du solveur, sans DRAT).
                if acc >= seuil:
                    verdict = "adeg <= %d (atteint)" % d
                elif 0 <= bound < seuil:
                    verdict = ("adeg > %d CERTIFIÉ (borne sup %d < seuil %d ; "
                               "avantage max sur le constant <= %d)"
                               % (d, bound, seuil, bound - max(ones, N - ones)))
                else:
                    verdict = "NON CONCLU"
                print(f"  F{q} d={d} : sym={bs} accord={acc} borne_sup={bound} "
                      f"[{statut}, {solver.WallTime():.0f} s] -> {verdict}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--deg-n", type=int, default=12)
    ap.add_argument("--adeg-n", type=int, default=8)
    ap.add_argument("--eps", type=float, default=0.125)
    ap.add_argument("--dmax", type=int, default=4)
    ap.add_argument("--seed", type=int, default=20260912)
    ap.add_argument("--tl", type=int, default=120)
    ap.add_argument("--focus-mod6", action="store_true",
                    help="mode ciblé MOD6/PARITY, certificats d'optimalité")
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--degres", type=str, default="2,3")
    args = ap.parse_args()
    rng = random.Random(args.seed)
    if args.focus_mod6:
        focus_mod6(args.adeg_n, args.eps, args.tl, args.workers,
                   tuple(int(d) for d in args.degres.split(",")))
        return

    print(f"PR-014 — degrés exacts / masse de Fourier / adeg approché ; "
          f"graine {args.seed}", flush=True)

    # ---- deg exact + Fourier, n = deg-n ----
    n = args.deg_n
    fams = [("PARITY", f_parity(n)),
            ("MOD3", f_mod(n, 3)),
            ("MOD6", f_mod(n, 6)),
            (f"DNF({n}x3)", f_dnf(n, n, 3, rng))]
    print(f"\n=== deg exact (Möbius) et masse de Fourier, n = {n} ===", flush=True)
    print(f"{'fonction':>12} | {'deg_F2':>6} {'deg_F3':>6} | "
          f"{'W<=2':>7} {'W<=4':>7} {'W<=logn':>8}", flush=True)
    import math
    dlog = max(1, int(math.log2(n)))
    for nom, tt in fams:
        d2 = deg_Fp(tt, n, 2)
        d3 = deg_Fp(tt, n, 3)
        w2 = fourier_weight_le(tt, n, 2)
        w4 = fourier_weight_le(tt, n, 4)
        wl = fourier_weight_le(tt, n, dlog)
        print(f"{nom:>12} | {d2:>6} {d3:>6} | {w2:>7.3f} {w4:>7.3f} "
              f"{wl:>8.3f}", flush=True)

    # ---- adeg approché, n = adeg-n ----
    n = args.adeg_n
    fams = [("PARITY", f_parity(n)),
            ("MOD3", f_mod(n, 3)),
            ("MOD6", f_mod(n, 6)),
            (f"DNF({n}x3)", f_dnf(n, n, 3, rng))]
    seuil = (1 << n) - int(args.eps * (1 << n))
    print(f"\n=== adeg approché par CP-SAT, n = {n}, eps = {args.eps} "
          f"(seuil accord >= {seuil}/{1 << n}), dmax = {args.dmax} ===", flush=True)
    for q in (2, 3):
        print(f"\n-- corps F{q} --", flush=True)
        for nom, tt in fams:
            adeg, trace = adeg_cpsat(tt, n, q, args.eps, args.dmax, args.tl)
            détail = " ".join(
                f"d{d}:{acc}{'' if opt else '?'}" for d, acc, opt in trace)
            verdict = f"adeg={adeg}" if adeg is not None else f"adeg>{args.dmax}"
            print(f"  {nom:>12} : {verdict:>9}  [{détail}]", flush=True)


if __name__ == "__main__":
    main()
