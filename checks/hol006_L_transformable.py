# -*- coding: utf-8 -*-
r"""HOL-006 — Le certificat L : l'épingle est-elle L-transformable ?

Épingle (HOL-004/005) : f(0000) = i, f(0001) = 1, f(1110) = 1.
Définition (MWXZ Def. 24, auditée HOL-003) : F est L-transformable si
∃M ∈ GL₂(C) : (=₂)M ∈ L et M⁻¹F ⊆ L. L (« local affine », CLX SODA
2018) : g ∈ L ssi pour CHAQUE σ ∈ supp(g), D_σ g ∈ A, où
D_σ = ⊗_j diag(1, α)^{σ_j}, α = e^{iπ/4}.

RELAXATION SÛRE (conditions NÉCESSAIRES pour g = adj(M)⊗⁴ f ∈ L) :
  (n1) supp(g) est un plat affine S (les shifts diagonaux ne changent
       pas le support ; A exige un support affine) ;
  (n2) pour σ₀ ∈ S (il suffit d'UN σ₀ du support pour une condition
       nécessaire ; on énumère tous les σ₀ ∈ S en branches) :
       (−1)^{⟨σ₀,x⟩} g_x⁴ est CONSTANT sur x ∈ S — car
       (α^{⟨σ₀,x⟩} g_x)⁴ = α^{4⟨σ₀,x⟩} g_x⁴ = (−1)^{⟨σ₀,x⟩} g_x⁴
       et les valeurs d'une signature A ont des rapports dans {±1, ±i}
       (puissances 4èmes égales) ;
  (n3) compagnon : h = (=₂)M⊗² ∈ L — mêmes conditions (plat S₂ de
       GF(2)², σ₂ ∈ S₂, signes sur h_y⁴).
Infaisable sur TOUTES les branches ⟹ PAS L-transformable (certificat,
étage par étage : chaque étage n'ajoute que du nécessaire).
Une branche survivante à l'étage 3 ⟹ NON CONCLU (la relaxation ne
tranche pas — consigné tel quel).

Étages (élagage) : E1 = zéros hors S + e·det(M) − 1 ; E2 = E1 + (n2) ;
E3 = E2 + (n3). Gröbner exact (sympy), 5 inconnues m0..m3, e.
"""
from __future__ import annotations

import itertools
import sys
import time

import sympy as sp

I = sp.I
X = list(range(16))
F = [0] * 16
F[0] = I
F[1] = 1
F[14] = 1

m0, m1, m2, m3, e = sp.symbols("m0 m1 m2 m3 e")
ADJ = [[m3, -m1], [-m2, m0]]
DET = m0 * m3 - m1 * m2


def tensor_apply(M, f, k=4):
    g = list(f)
    for j in range(k):
        h = [0] * (1 << k)
        for y in range(1 << k):
            y0 = y & ~(1 << j)
            y1 = y | (1 << j)
            b = (y >> j) & 1
            h[y] = sp.expand(M[b][0] * g[y0] + M[b][1] * g[y1])
        g = h
    return g


G = tensor_apply(ADJ, F)  # adj(M)^{tensor 4} f — 16 polynomes deg 4

# binaire compagnon : h_y = sum_x (=2)_x M[x1,y1] M[x2,y2]
M_ = [[m0, m1], [m2, m3]]
H = {}
for y in range(4):
    y1, y2 = y & 1, (y >> 1) & 1
    H[y] = sp.expand(M_[0][y1] * M_[0][y2] + M_[1][y1] * M_[1][y2])


def groebner_trivial(eqs, gens=(m0, m1, m2, m3, e)):
    eqs = [sp.expand(q) for q in eqs]
    eqs = [q for q in eqs if q != 0]
    if not eqs:
        return False
    gb = sp.groebner(eqs, *gens, order="grevlex")
    return list(gb.exprs) == [sp.Integer(1)]


def plats_affines(n):
    plats = set()
    for r in range(n + 1):
        for gens in itertools.combinations(range(1, 1 << n), r):
            span = {0}
            for v in gens:
                span |= {s ^ v for s in span}
            for x0 in range(1 << n):
                plats.add(frozenset(x0 ^ s for s in span))
    return sorted(plats, key=lambda s: (len(s), sorted(s)))


def scal(a, b, n=4):
    return bin(a & b).count("1")


def main():
    t00 = time.time()
    plats4 = plats_affines(4)
    print(f"Épingle : f(0000) = i, f(0001) = 1, f(1110) = 1")
    print(f"É1 — zéros hors plat + det ≠ 0 : {len(plats4)} plats")
    surv1 = []
    t0 = time.time()
    for S in plats4:
        eqs = [G[x] for x in X if x not in S] + [e * DET - 1]
        if not groebner_trivial(eqs):
            surv1.append(S)
    print(f"  [{time.time() - t0:.0f}s] survivants É1 : {len(surv1)}")
    for S in surv1[:8]:
        print(f"    plat {sorted(S)}")

    print("É2 — + puissances 4èmes signées (σ0 ∈ S)")
    surv2 = []
    t0 = time.time()
    for S in surv1:
        supp = sorted(S)
        for s0 in supp:
            eqs = [G[x] for x in X if x not in S] + [e * DET - 1]
            g0 = sp.expand(((-1) ** scal(s0, supp[0])) * G[supp[0]] ** 4)
            for x in supp[1:]:
                eqs.append(sp.expand(((-1) ** scal(s0, x)) * G[x] ** 4 - g0))
            if not groebner_trivial(eqs):
                surv2.append((S, s0))
                if len(surv2) <= 8:
                    print(f"    branche vivante : plat {sorted(S)}, "
                          f"σ0 = {s0:04b}")
    print(f"  [{time.time() - t0:.0f}s] branches vivantes É2 : {len(surv2)}")

    print("É3 — + compagnon (=₂)M ∈ L (plats de GF(2)², σ2)")
    plats2 = plats_affines(2)
    surv3 = []
    t0 = time.time()
    for (S, s0) in surv2:
        supp = sorted(S)
        base = [G[x] for x in X if x not in S] + [e * DET - 1]
        g0 = sp.expand(((-1) ** scal(s0, supp[0])) * G[supp[0]] ** 4)
        for x in supp[1:]:
            base.append(sp.expand(((-1) ** scal(s0, x)) * G[x] ** 4 - g0))
        for S2 in plats2:
            supp2 = sorted(S2)
            eqs2 = base + [H[y] for y in range(4) if y not in S2]
            for s2 in supp2:
                eqs3 = list(eqs2)
                h0 = sp.expand(((-1) ** scal(s2, supp2[0], 2))
                               * H[supp2[0]] ** 4)
                for y in supp2[1:]:
                    eqs3.append(sp.expand(((-1) ** scal(s2, y, 2))
                                          * H[y] ** 4 - h0))
                if not groebner_trivial(eqs3):
                    surv3.append((S, s0, S2, s2))
                    if len(surv3) <= 8:
                        print(f"    branche vivante É3 : plat {sorted(S)}, "
                              f"σ0={s0:04b}, S2={sorted(S2)}, σ2={s2:02b}")
    print(f"  [{time.time() - t0:.0f}s] branches vivantes É3 : {len(surv3)}")

    print(f"\nVERDICT L ({time.time() - t00:.0f}s total) : "
          + ("PAS L-transformable (certificat — relaxation nécessaire "
             "infaisable sur toutes les branches)" if not surv3 else
             f"NON CONCLU ({len(surv3)} branches de relaxation vivantes "
             "— la relaxation ne tranche pas ; à examiner)"))


if __name__ == "__main__":
    main()
