"""
V-041 -- derivation generale et exacte des polynomes de consistance
F_n de CMSV 2023 (sec. 4.2) pour n pair : F_n(x_1..x_{n/2-1}) s'annule
quand une selection de n/2+2 elements est completable en solution
ideale symetrique de taille n. Derive par noyau exact (1-dimensionnel),
valide : F12 reproduite a l'identique (et certifiee sur Kuosa).
Convention : x_k = somme des b_sel^{2k} - somme des a_sel^{2k}
           = p_k(alpha_restants) - p_k(beta_restants).
"""

from __future__ import annotations

import json
import os
import random


def _mul(d1, d2, nv):
    out = {}
    for e1, c1 in d1.items():
        for e2, c2 in d2.items():
            e = tuple(x + y for x, y in zip(e1, e2))
            out[e] = out.get(e, 0) + c1 * c2
    return {e: c for e, c in out.items() if c}


def derive_F(n):
    """Retourne [(coef, exps)] pour n pair (12 ou 14), avec cache."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        f"v041_F{n}.json")
    if os.path.exists(path):
        data = json.load(open(path))
        return [(int(c), tuple(e)) for c, e in data]

    ns = n // 2
    s = -(-n // 4) + 1            # ceil(n/4)+1 elements a selectionnes
    t = n // 4 + 1
    rema, remb = ns - s, ns - t   # restants (cote a, cote b)
    nx = ns - 1                   # moments k = 1..nx
    T = 3 * (n - 6) // 2          # somme des k*dk (poids CMSV / 2)
    nv = rema + remb

    def powersum_diff(k):
        d = {}
        for i in range(nv):
            e = [0] * nv
            e[i] = k
            d[tuple(e)] = 1 if i < rema else -1
        return d

    # monomes (d1..d_nx) avec sum k*dk = T
    monos = []

    def gen(k, rest, cur):
        if k == 0:
            if rest == 0:
                monos.append(tuple(cur))
            return
        for dk in range(rest // k + 1):
            gen(k - 1, rest - k * dk, [dk] + cur)

    gen(nx, T, [])

    polys = []
    for m in monos:
        out = {tuple([0] * nv): 1}
        for k, dk in enumerate(m, start=1):
            Ek = powersum_diff(k)
            for _ in range(dk):
                out = _mul(out, Ek, nv)
        polys.append(out)

    cols = sorted(set().union(*[set(p) for p in polys]))
    import sympy as sp
    rng = random.Random(7)
    sub = rng.sample(range(len(cols)), min(3 * len(monos), len(cols)))
    M = sp.Matrix([[polys[i].get(cols[j], 0) for j in sub]
                   for i in range(len(monos))])
    ker = M.T.nullspace()
    assert len(ker) == 1, f"noyau de dimension {len(ker)} != 1"
    v = ker[0]
    dens = [sp.fraction(sp.nsimplify(x))[1] for x in v]
    l = sp.ilcm(*[int(d) for d in dens])
    vi = [int(x * l) for x in v]
    g = 0
    for x in vi:
        g = sp.igcd(g, x)
    vi = [x // g for x in vi]
    # verification exhaustive de la relation
    for e in cols:
        assert sum(vi[i] * polys[i].get(e, 0)
                   for i in range(len(monos))) == 0
    terms = [(c, m) for c, m in zip(vi, monos) if c]
    json.dump([[c, list(m)] for c, m in terms], open(path, "w"))
    return terms
