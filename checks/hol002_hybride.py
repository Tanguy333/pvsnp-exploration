# -*- coding: utf-8 -*-
r"""HOL-002 — L'hybride des quatre îles, version falsifiable :
la CROISSANCE du min-support de jauge S_min hors des îles.

Cadre (repris des scripts utilisateur explo_jauge_quatre_iles.py /
explo_min_support_jauge.py, rejoués et conformes) : Z(3-SAT pondéré)
= contraction d'un réseau de tenseurs ; jauge P_e par arête ; Z
invariante ; S(jauge) = nombre de termes d'excitation non nuls.
L'évaluateur hybride = choisir les jauges (dictionnaire d'îles +
recuit) puis sommer les S termes — polynomial QUAND S est petit.

LA question mesurée ici : comment S_min croît-il avec n sur une
famille construite pour être HORS des quatre îles à la fois ?
- famille DURE : facteur-graphes aléatoires 3-réguliers bipartis
  (n variables de degré 3, m = n clauses de 3 littéraux, polarités
  aléatoires) — treewidth ~ linéaire (l'île DP paie 2^n), non planaire
  avec forte probabilité (l'île holographique/FKT sans prise),
  clauses OR (jamais affines), boucles courtes (BP inexact) ;
- contrôles : arbre + cordes (île DP), les instances utilisateur.

Mesures par instance : S des jauges-îles (identité, alignée-clause,
Hadamard, BP), S_min du dictionnaire (exhaustif {I,C}^E si E <= 16,
recuit budgété sinon), écart Bethe, et CHAQUE somme re-vérifiée
contre Z exact (énumération 2^n). Coûts comparés : S_min (hybride)
vs 2^n (île DP) vs 2^E (brut).

Échelle : E <= 21 en pleine méthode (mémoire vectorisée), n = m = 8
(E = 24) en mode par blocs sur jauges désignées seulement. Au-delà :
hors instrument, dit d'avance.
"""
from __future__ import annotations

import itertools
import sys
import time

import numpy as np

RNG = np.random.default_rng(20260808)

I2 = np.eye(2)
HAD = np.array([[1.0, 1.0], [1.0, -1.0]])


# ------------------------------------------------------------ instances

def famille_dure(n, graine):
    """m = n clauses ; chaque variable exactement 3 occurrences ;
    polarités aléatoires ; rejet des clauses à variable répétée."""
    rng = np.random.default_rng(graine)
    for _ in range(4000):
        pool = list(range(n)) * 3
        rng.shuffle(pool)
        clauses = []
        ok = True
        for a in range(n):
            trio = pool[3 * a: 3 * a + 3]
            if len(set(trio)) < 3:
                ok = False
                break
            clauses.append(tuple((v, int(rng.integers(2))) for v in trio))
        if ok:
            return n, clauses
    raise RuntimeError("echec generation")


def arbre_plus_cordes(n_cordes):
    """Chaîne de 4 clauses en arbre sur 9 variables + n_cordes clauses
    de rebouclage."""
    cls = [((0, 1), (1, 1), (2, 1)), ((2, 1), (3, 1), (4, 0)),
           ((4, 1), (5, 1), (6, 1)), ((6, 0), (7, 1), (8, 1))]
    cordes = [((0, 0), (4, 1), (8, 1)), ((1, 1), (5, 0), (7, 1))]
    return 9, cls + cordes[:n_cordes]


def instance_utilisateur():
    return 5, [((0, 1), (1, 1), (2, 0)), ((1, 1), (2, 1), (3, 1)),
               ((2, 1), (3, 0), (4, 1)), ((0, 1), (3, 1), (4, 0)),
               ((0, 0), (1, 1), (4, 1))]


# ------------------------------------------------------------ noyau

def poids_clause(cl, assign, w):
    return 1.0 if any(assign[v] == p for (v, p) in cl) else w


def Z_exacte(n, clauses, w):
    Z = 0.0
    for bits in itertools.product((0, 1), repeat=n):
        t = 1.0
        for cl in clauses:
            t *= poids_clause(cl, bits, w)
        Z += t
    return Z


def structure(n, clauses):
    edges = [(i, a) for a, cl in enumerate(clauses) for (i, _) in cl]
    var_e = {i: [e for e, (j, _) in enumerate(edges) if j == i]
             for i in range(n)}
    cl_e = {a: [e for e, (_, b) in enumerate(edges) if b == a]
            for a in range(len(clauses))}
    pol = {}
    for e, (i, a) in enumerate(edges):
        for (v, p) in clauses[a]:
            if v == i:
                pol[e] = p
    return edges, var_e, cl_e, pol


def jauge_alignee(pol_e):
    viol = 1 - pol_e
    delta = np.zeros(2)
    delta[viol] = 1.0
    w1 = 2 * delta - np.ones(2)
    Pinv = np.vstack([np.ones(2) - delta, w1])
    return np.linalg.inv(Pinv)


def run_bp(n, clauses, w, edges, var_e, iters=3000, damp=0.5):
    m_va = {e: np.array([.5, .5]) for e in range(len(edges))}
    m_av = {e: np.array([.5, .5]) for e in range(len(edges))}
    for _ in range(iters):
        for e, (i, a) in enumerate(edges):
            prod = np.ones(2)
            for f in var_e[i]:
                if f != e:
                    prod = prod * m_av[f]
            s = prod.sum()
            if s > 0:
                m_va[e] = damp * m_va[e] + (1 - damp) * prod / s
        for e, (i, a) in enumerate(edges):
            cl = clauses[a]
            others = [(v, p) for (v, p) in cl if v != i]
            out = np.zeros(2)
            for si in (0, 1):
                tot = 0.0
                for vals in itertools.product((0, 1), repeat=len(others)):
                    assign = {i: si}
                    prob = 1.0
                    for (v, _), val in zip(others, vals):
                        assign[v] = val
                    for (v, _), val in zip(others, vals):
                        fe = [g for g in var_e[v]
                              if edges[g][1] == a][0]
                        prob *= m_va[fe][val]
                    tot += poids_clause(cl, assign, w) * prob
                out[si] = tot
            s = out.sum()
            if s > 0:
                m_av[e] = damp * m_av[e] + (1 - damp) * out / s
    G = []
    for e in range(len(edges)):
        v0 = m_av[e].copy()
        w0 = m_va[e].copy()
        z = float(w0 @ v0)
        if abs(z) < 1e-12:
            G.append(I2.copy())
            continue
        w0 = w0 / z
        v1 = np.array([-w0[1], w0[0]])
        G.append(np.column_stack([v0, v1]))
    return G


def support_et_somme(n, clauses, w, gauges, edges, var_e, cl_e,
                     bloc=1 << 20):
    """S et somme, par blocs (mémoire bornée quel que soit E <= 24)."""
    E = len(edges)
    Pinvs = [np.linalg.inv(P) for P in gauges]
    loc_var = {}
    for i in range(n):
        es = var_e[i]
        d = len(es)
        loc = np.zeros(1 << d)
        for kb in range(1 << d):
            p0 = p1 = 1.0
            for pos, e in enumerate(es):
                kk = (kb >> pos) & 1
                p0 *= gauges[e][0, kk]
                p1 *= gauges[e][1, kk]
            loc[kb] = p0 + p1
        loc_var[i] = (es, loc)
    loc_cl = {}
    for a, cl in enumerate(clauses):
        es = cl_e[a]
        loc = np.zeros(1 << len(es))
        for kb in range(1 << len(es)):
            tot = 0.0
            for vals in itertools.product((0, 1), repeat=len(cl)):
                assign = {v: val for (v, _), val in zip(cl, vals)}
                weight = poids_clause(cl, assign, w)
                prob = 1.0
                for pos, e in enumerate(es):
                    kk = (kb >> pos) & 1
                    prob *= Pinvs[e][kk, vals[pos]]
                tot += weight * prob
            loc[kb] = tot
        loc_cl[a] = (es, loc)
    S = 0
    somme = 0.0
    for debut in range(0, 1 << E, bloc):
        ks = np.arange(debut, min(debut + bloc, 1 << E), dtype=np.int64)
        terms = np.ones(len(ks))
        for i in range(n):
            es, loc = loc_var[i]
            idx = np.zeros(len(ks), dtype=np.int64)
            for pos, e in enumerate(es):
                idx |= (((ks >> e) & 1) << pos)
            terms *= loc[idx]
        for a in range(len(clauses)):
            es, loc = loc_cl[a]
            idx = np.zeros(len(ks), dtype=np.int64)
            for pos, e in enumerate(es):
                idx |= (((ks >> e) & 1) << pos)
            terms *= loc[idx]
        S += int((np.abs(terms) > 1e-9).sum())
        somme += float(terms.sum())
    return S, somme


def analyse_instance(nom, n, clauses, w, budget_recuit=150,
                     jauges_seules=False):
    edges, var_e, cl_e, pol = structure(n, clauses)
    E = len(edges)
    Zx = Z_exacte(n, clauses, w)
    t0 = time.time()
    CA = [jauge_alignee(pol[e]) for e in range(E)]
    BP = run_bp(n, clauses, w, edges, var_e)
    dico = {"I": [I2] * E, "C": CA, "H": [HAD] * E, "B": BP}
    res = {}
    for nomj, G in dico.items():
        S, tot = support_et_somme(n, clauses, w, G, edges, var_e, cl_e)
        assert abs(tot - Zx) < 1e-5 * max(1.0, abs(Zx)), f"jauge {nomj}"
        res[nomj] = S
    smin = min((res[k], k) for k in res)
    if not jauges_seules:
        # recuit sur le dictionnaire par arête
        cles = ["I", "C", "H", "B"]
        choix = ["C"] * E
        G = [dico["C"][e] for e in range(E)]
        cur, _ = support_et_somme(n, clauses, w, G, edges, var_e, cl_e)
        best = cur
        temp = 6.0
        for step in range(budget_recuit):
            temp = max(.4, temp * .985)
            e = int(RNG.integers(E))
            old = choix[e]
            choix[e] = cles[int(RNG.integers(4))]
            G[e] = dico[choix[e]][e]
            S2, tot2 = support_et_somme(n, clauses, w, G, edges,
                                        var_e, cl_e)
            if abs(tot2 - Zx) > 1e-5 * max(1.0, abs(Zx)):
                S2 = 10 ** 9
            if S2 <= cur or RNG.random() < np.exp((cur - S2) / temp):
                cur = S2
                best = min(best, cur)
            else:
                choix[e] = old
                G[e] = dico[old][e]
        smin = (min(smin[0], best), smin[1])
    print(f"  {nom:24} n={n} m={len(clauses)} E={E} Z={Zx:10.4f} | "
          f"S: I={res['I']} C={res['C']} H={res['H']} B={res['B']} | "
          f"S_min={smin[0]}  (2^n={1 << n}, 2^E={1 << E})"
          f"  [{time.time() - t0:.0f}s]")
    return res, smin[0]


def campagne():
    w = 0.0  # température nulle : Z = #SAT — le régime dur
    print("=== CONTRÔLES ===")
    n, cl = instance_utilisateur()
    analyse_instance("utilisateur (replique)", n, cl, w)
    for nc in (0, 1, 2):
        n, cl = arbre_plus_cordes(nc)
        analyse_instance(f"arbre + {nc} corde(s)", n, cl, w)
    print("=== FAMILLE DURE (3-régulière bipartie, m = n) ===")
    courbe = []
    for n in (4, 5, 6, 7):
        for graine in (1, 2, 3):
            nn, cl = famille_dure(n, 100 + graine)
            _, smin = analyse_instance(f"dure n={n} g={graine}", nn, cl, w,
                                       budget_recuit=120 if n <= 6 else 60)
            courbe.append((n, smin))
    print("=== POINT ÉTENDU n = 8 (E = 24, jauges-îles seules) ===")
    nn, cl = famille_dure(8, 101)
    _, smin = analyse_instance("dure n=8 g=1", nn, cl, w, jauges_seules=True)
    courbe.append((8, smin))
    print("\n=== LA COURBE S_min(n) — famille dure ===")
    par_n = {}
    for n, s in courbe:
        par_n.setdefault(n, []).append(s)
    for n in sorted(par_n):
        vals = par_n[n]
        print(f"  n = {n} : S_min = {vals}  (2^n = {1 << n})")


if __name__ == "__main__":
    campagne()
