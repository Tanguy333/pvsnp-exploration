# -*- coding: utf-8 -*-
r"""ALG-001 — Le poids SYM+ sous restrictions : le mur de F-001
s'effondre-t-il quand on fixe des variables ?

Contexte (fil ALG, ligne 7, candidature PR-005) : W(f) = poids MinSYM+
minimal (monômes positifs, couvert à valeurs disjointes) — le prix
d'entrée de l'évaluation par lots à la Williams 2014. F-001 a mesuré :
EXACT_{n/2} polynomial (O(n²)), IP_n exponentiel (20/119/640 à
n = 4/6/8). LA QUESTION : sous une restriction aléatoire ρ (fixant
une fraction q des variables), la médiane de W(IP|ρ) s'effondre-t-elle
(voie « restrictions puis SYM+ » fondée) ou résiste-t-elle (mur
approfondi, quantifié) ?

Double calibration :
  - CONTRÔLE : EXACT_{n/2}|ρ reste dans la famille EXACT (translatée) —
    W doit suivre la loi polynomiale connue ; un écart = instrument
    faux.
  - STRUCTURE ATTENDUE POUR IP (validation croisée, pas prédiction de
    valeur) : si ρ fixe les deux moitiés proprement, IP|ρ devient une
    parité ⊕ constante (W ≤ #vars restantes + 1) ; le cas générique
    (paires partiellement tuées) est LA mesure.

Protocole : n ∈ {4, 6, 8} ; fractions q ∈ {1/4, 1/2} (arrondi) ;
20 restrictions aléatoires par cas (graine 20260811 consignée) ;
W EXACT au solveur certifié (canal de valeurs, OPTIMAL exigé, témoin
re-vérifié) ; médianes, extrêmes, et comparaison aux valeurs non
restreintes de F-001.
"""
from __future__ import annotations

import random
import statistics
import sys
import time

from ortools.sat.python import cp_model


def W_cpsat(uns, nvars, tl=600):
    N = 1 << nvars
    cap = max(2, N - 1)
    su = set(uns)
    if not su:
        return 0
    if len(su) == N:
        return 1  # constante 1 : un seul monome vide interdit -> m_x1&... ;
        # convention : couvert trivial, poids 1 (borne sup) — cas non
        # rencontre dans le protocole (IP et EXACT restreintes ne sont
        # jamais la constante 1 sur nos tailles ; garde-fou).
    zeros = [x for x in range(N) if x not in su]
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
    for u in su:
        for v in zeros:
            model.Add(val[u] != val[v])
    model.Minimize(tot)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tl
    solver.parameters.num_search_workers = 8
    st = solver.Solve(model)
    assert st == cp_model.OPTIMAL, f"non conclu ({solver.StatusName(st)})"
    temoin = {S: solver.Value(a[S]) for S in monomes if solver.Value(a[S])}
    pv = lambda x: sum(c for S, c in temoin.items() if S & x == S)
    v1 = {pv(u) for u in su}
    v0 = {pv(z) for z in zeros}
    assert not (v1 & v0) and sum(temoin.values()) == solver.Value(tot)
    return solver.Value(tot)


def ip(n, z):
    """IP_n : n pair, paires (i, i + n/2)."""
    k = n // 2
    acc = 0
    for i in range(k):
        acc ^= ((z >> i) & 1) & ((z >> (i + k)) & 1)
    return acc


def exact_moitie(n, z):
    return 1 if bin(z).count("1") == n // 2 else 0


def restreindre(f, n, fixes):
    """fixes : dict var -> bit. Rend (m, table des uns sur m vars)."""
    libres = [i for i in range(n) if i not in fixes]
    m = len(libres)
    uns = []
    for y in range(1 << m):
        z = 0
        for j, i in enumerate(libres):
            if (y >> j) & 1:
                z |= 1 << i
        for i, b in fixes.items():
            if b:
                z |= 1 << i
        if f(n, z):
            uns.append(y)
    return m, uns


def campagne(nom, f, n, q, nrest, rng, ref_pleine):
    nfix = max(1, round(n * q))
    ws = []
    t0 = time.time()
    for _ in range(nrest):
        vars_fixes = rng.sample(range(n), nfix)
        fixes = {i: rng.randint(0, 1) for i in vars_fixes}
        m, uns = restreindre(f, n, fixes)
        if not uns:
            ws.append(0)  # restreinte constante 0 : poids 0
            continue
        ws.append(W_cpsat(uns, m))
    med = statistics.median(ws)
    print(f"  {nom:10} n={n} fixe={nfix} (m={n - nfix}) : "
          f"W|rho sur {nrest} tirages — mediane={med:.1f}, "
          f"min={min(ws)}, max={max(ws)}   (W plein = {ref_pleine})"
          f"  [{time.time() - t0:.0f}s]")
    return ws


def main():
    rng = random.Random(20260811)
    refs_ip = {4: 20, 6: 119, 8: 640}       # F-001, non restreint
    print("=== ALG-001 — le poids SYM+ sous restrictions ===")
    print("(graine 20260811 ; 20 restrictions par cas ; W exact, "
          "OPTIMAL exige, temoins re-verifies)\n")
    for n in (4, 6, 8):
        ref_ex = W_cpsat([z for z in range(1 << n)
                          if exact_moitie(n, z)], n) if n <= 6 else "F-001:O(n^2)"
        print(f"--- n = {n} ---")
        for q in (0.25, 0.5):
            campagne("IP", ip, n, q, 20, rng, refs_ip[n])
            campagne("EXACT", exact_moitie, n, q, 20, rng, ref_ex)
        print()


if __name__ == "__main__":
    main()
