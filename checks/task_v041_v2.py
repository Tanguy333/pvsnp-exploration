"""
TACHE V-041 v2 -- machine CMSV pour les ideales SYMETRIQUES de taille
paire n : selection de n/2+2 elements seulement (au lieu de n),
restreinte par la chaine de congruences (21) (diviseurs requis p1, p2
de C'_n), porte algebrique F_n (deux premiers de controle puis exact),
et COMPLETION des n/2-2 elements restants par algebre exacte (sympy).

n = 12 : p1, p2 = 31, 29 -- VALIDATION : doit trouver Kuosa a H >= 151.
n = 14 : p1, p2 = 37, 31 -- CIBLE : replication <= 900 puis TERRITOIRE
NEUF au-dela (plafond mondial actuel, Table 2 de CMSV).

Usage : python task_v041_v2.py <n> <H> [a1_lo a1_hi]
Banking par a1 dans checks/v041_v2_n<n>_H<H>/ (reprise automatique).
"""

from __future__ import annotations

import os
import sys
import time

import numpy as np
from numba import njit

from v041_fpoly import derive_F

G1 = 2147483647   # 2^31 - 1, premier
G2 = 2147483629   # premier


@njit(cache=True)
def _gate(vals, sides, ntot, nx, Fco, Fex, g):
    """Evalue F(x_1..x_nx) mod g ; x_k = sum_b v^2k - sum_a v^2k."""
    x = np.zeros(nx + 1, dtype=np.int64)
    for k in range(1, nx + 1):
        acc = 0
        for i in range(ntot):
            t = (vals[i] * vals[i]) % g
            pw = 1
            for _ in range(k):
                pw = (pw * t) % g
            if sides[i] == 1:
                acc = (acc + pw) % g
            else:
                acc = (acc - pw) % g
        x[k] = acc % g
    tot = 0
    for it in range(Fco.shape[0]):
        term = Fco[it] % g
        for k in range(1, nx + 1):
            e = Fex[it, k - 1]
            for _ in range(e):
                term = (term * x[k]) % g
        tot = (tot + term) % g
    return tot % g


@njit(cache=True)
def _search(a1, H, sides, ntot, p1, p2, nx, tot_a, tot_b,
            Fco, Fex, out, max_out):
    """DFS sur les ntot selections, a1 fixe. Retourne nb de survivants
    (selections passant la chaine (21) + bornes + double porte F)."""
    val = np.zeros(ntot, dtype=np.int64)
    rep = np.zeros((ntot, 2), dtype=np.int64)   # restes des classes
    stp = np.zeros(ntot, dtype=np.int64)        # pas (p ou 1)
    ncl = np.zeros(ntot, dtype=np.int64)
    icl = np.zeros(ntot, dtype=np.int64)
    PI = np.zeros((ntot + 1, 2), dtype=np.int64)      # 2k = 2, 4
    PF = np.zeros((ntot + 1, nx - 2))                  # 2k = 6..2nx
    ca = np.zeros(ntot + 1, dtype=np.int64)
    cb = np.zeros(ntot + 1, dtype=np.int64)
    Sm = np.zeros(ntot + 1, dtype=np.int64)            # somme paires mod p2
    capI = np.zeros(2, dtype=np.int64)
    capI[0] = H * H
    capI[1] = H * H * H * H
    capF = np.zeros(nx - 2)
    for k in range(3, nx + 1):
        capF[k - 3] = float(H) ** (2 * k)
    nf = 0

    # niveau 0 : a1 fixe
    d = 0
    val[0] = a1
    PI[1, 0] = a1 * a1
    PI[1, 1] = PI[1, 0] * PI[1, 0]
    for k in range(3, nx + 1):
        PF[1, k - 3] = float(a1) ** (2 * k)
    ca[1] = 1
    cb[1] = 0
    Sm[1] = (a1 * a1) % p2

    # preparer le niveau 1
    d = 1
    fresh = True
    while d >= 1:
        if fresh:
            # initialiser les classes du niveau d
            if sides[d] == 1:
                # b_k : b ≡ ±a_k (mod p1), a_k = val[d-1]
                r = val[d - 1] % p1
                rep[d, 0] = r
                rep[d, 1] = (p1 - r) % p1
                ncl[d] = 1 if rep[d, 1] == rep[d, 0] else 2
                stp[d] = p1
            else:
                if Sm[d] % p2 != 0:
                    r = val[d - 1] % p2
                    rep[d, 0] = r
                    rep[d, 1] = (p2 - r) % p2
                    ncl[d] = 1 if rep[d, 1] == rep[d, 0] else 2
                    stp[d] = p2
                else:
                    rep[d, 0] = 1
                    ncl[d] = 1
                    stp[d] = 1
            icl[d] = 0
            v0 = rep[d, 0]
            val[d] = v0 if v0 >= 1 else stp[d]
            fresh = False
        else:
            val[d] += stp[d]
        # classe suivante / remontee
        if val[d] > H:
            icl[d] += 1
            if icl[d] >= ncl[d]:
                d -= 1
                continue
            v0 = rep[d, icl[d]]
            val[d] = v0 if v0 >= 1 else stp[d]
            if val[d] > H:
                d -= 1
                continue
        v = val[d]
        # distinct des precedents
        dup = False
        for i in range(d):
            if val[i] == v:
                dup = True
                break
        if dup:
            continue
        # mise a jour des moments
        v2 = v * v
        sgn = 1 if sides[d] == 0 else -1
        PI[d + 1, 0] = PI[d, 0] + sgn * v2
        PI[d + 1, 1] = PI[d, 1] + sgn * v2 * v2
        pf = float(v2) * float(v2) * float(v2)
        for k in range(3, nx + 1):
            PF[d + 1, k - 3] = PF[d, k - 3] + sgn * pf
            pf *= float(v2)
        if sides[d] == 0:
            ca[d + 1] = ca[d] + 1
            cb[d + 1] = cb[d]
            Sm[d + 1] = (Sm[d] + v2) % p2
        else:
            ca[d + 1] = ca[d]
            cb[d + 1] = cb[d] + 1
            Sm[d + 1] = (Sm[d] - v2) % p2
        # bornes de faisabilite (comptages restants, completion incluse)
        pl = tot_a - ca[d + 1]
        ml = tot_b - cb[d + 1]
        bad = False
        for k in range(2):
            P = PI[d + 1, k]
            if P > ml * capI[k] or -P > pl * capI[k]:
                bad = True
                break
        if not bad:
            for k in range(nx - 2):
                P = PF[d + 1, k]
                lim_m = ml * capF[k] * (1.0 + 1e-9) + 1.0
                lim_p = pl * capF[k] * (1.0 + 1e-9) + 1.0
                if P > lim_m or -P > lim_p:
                    bad = True
                    break
        if bad:
            # cote a : croissant en v, l'exces positif ne fera qu'empirer
            if sides[d] == 0 and PI[d + 1, 0] > ml * capI[0]:
                val[d] = H + 1  # epuise la classe courante
            # cote b : symetrique
            if sides[d] == 1 and -PI[d + 1, 0] > pl * capI[0]:
                val[d] = H + 1
            continue
        if d == ntot - 1:
            if _gate(val, sides, ntot, nx, Fco, Fex, G1) == 0:
                if _gate(val, sides, ntot, nx, Fco, Fex, G2) == 0:
                    if nf < max_out:
                        for i in range(ntot):
                            out[nf, i] = val[i]
                        nf += 1
            continue
        d += 1
        fresh = True
    return nf


def completer(sel_a, sel_b, n, H):
    """Complete une selection survivante : resout exactement les
    moments restants, exige racines = carres parfaits distincts."""
    import sympy as sp
    ns = n // 2
    rema = ns - len(sel_a)
    remb = ns - len(sel_b)
    nx = ns - 1
    xs = [sum(b ** (2 * k) for b in sel_b) - sum(a ** (2 * k) for a in sel_a)
          for k in range(1, nx + 1)]

    es = sp.symbols(f"e1:{rema + 1}")
    fs = sp.symbols(f"f1:{remb + 1}")

    def newton(sym, m, K):
        p = {0: sp.Integer(m)}
        e = list(sym) + [sp.Integer(0)] * K
        for k in range(1, K + 1):
            acc = sp.Integer(0)
            for i in range(1, k):
                acc += (-1) ** (i - 1) * e[i - 1] * p[k - i]
            acc += (-1) ** (k - 1) * sp.Integer(k) * e[k - 1] if k <= m \
                else (-1) ** (k - 1) * sp.Integer(k) * sp.Integer(0)
            p[k] = sp.expand(acc)
        return p

    pa = newton(es, rema, nx)
    pb = newton(fs, remb, nx)
    eqs = [sp.expand(pa[k] - pb[k] - xs[k - 1]) for k in range(1, nx + 1)]
    try:
        sols = sp.solve(eqs[:rema + remb], list(es) + list(fs), dict=True)
    except Exception:
        return []
    out = []
    for so in sols:
        if any(not v.is_rational for v in so.values()):
            continue
        if sp.simplify(eqs[-1].subs(so)) != 0:
            continue
        t = sp.symbols("t")
        polA = t ** rema
        for i in range(rema):
            polA += (-1) ** (i + 1) * so[es[i]] * t ** (rema - 1 - i)
        polB = t ** remb
        for i in range(remb):
            polB += (-1) ** (i + 1) * so[fs[i]] * t ** (remb - 1 - i)
        ra = sp.roots(sp.Poly(polA, t))
        rb = sp.roots(sp.Poly(polB, t))
        if sum(ra.values()) != rema or sum(rb.values()) != remb:
            continue
        if any(m > 1 for m in list(ra.values()) + list(rb.values())):
            continue
        va, vb = [], []
        ok = True
        for r in ra:
            q = sp.sqrt(r)
            if not (r.is_integer and r > 0 and q.is_integer and q <= H):
                ok = False
                break
            va.append(int(q))
        if ok:
            for r in rb:
                q = sp.sqrt(r)
                if not (r.is_integer and r > 0 and q.is_integer and q <= H):
                    ok = False
                    break
                vb.append(int(q))
        if not ok:
            continue
        A = sorted(sel_a + va)
        B = sorted(sel_b + vb)
        if len(set(A)) == len(A) and len(set(B)) == len(B) \
                and not set(A) & set(B):
            out.append((A, B))
    return out


def verifier(A, B, n):
    M = max(A + B)
    AA = sorted([M + x for x in A] + [M - x for x in A])
    BB = sorted([M + x for x in B] + [M - x for x in B])
    deg = 0
    for k in range(1, 2 * n):
        if sum(t ** k for t in AA) == sum(t ** k for t in BB):
            deg = k
        else:
            break
    return deg


def main():
    n = int(sys.argv[1])
    H = int(sys.argv[2])
    a1_lo = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    a1_hi = int(sys.argv[4]) if len(sys.argv) > 4 else H
    p1, p2 = {12: (31, 29), 14: (37, 31)}[n]
    ns = n // 2
    s = -(-n // 4) + 1
    t = n // 4 + 1
    ntot = s + t
    sides_l = []
    na = nb = 0
    while na + nb < ntot:
        if na <= nb and na < s:
            sides_l.append(0)
            na += 1
        else:
            sides_l.append(1)
            nb += 1
    sides = np.array(sides_l, dtype=np.int64)
    nx = ns - 1

    terms = derive_F(n)
    Fco = np.array([c for c, _ in terms], dtype=np.int64)
    Fex = np.array([list(e) for _, e in terms], dtype=np.int64)

    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          f"v041_v2_n{n}_H{H}")
    os.makedirs(outdir, exist_ok=True)
    print(f"V-041 v2 : n = {n}, H = {H}, (p1,p2) = ({p1},{p2}), "
          f"selections = {ntot} ({s}a + {t}b), F a {len(terms)} termes, "
          f"a1 = {a1_lo}..{a1_hi}", flush=True)

    out = np.zeros((4096, ntot), dtype=np.int64)
    vus = set()
    t0 = time.time()
    for a1 in range(a1_lo, a1_hi + 1):
        path = os.path.join(outdir, f"a1_{a1}.txt")
        if os.path.exists(path):
            continue
        tA = time.time()
        nf = _search(a1, H, sides, ntot, p1, p2, nx, ns, ns,
                     Fco, Fex, out, 4096)
        lignes = [f"a1={a1} survivants={nf} t={time.time()-tA:.1f}s"]
        for i in range(nf):
            vals = [int(x) for x in out[i]]
            sel_a = [vals[j] for j in range(ntot) if sides_l[j] == 0]
            sel_b = [vals[j] for j in range(ntot) if sides_l[j] == 1]
            # porte exacte (les deux portes modulaires ont deja filtre)
            xs = [sum(x ** (2 * k) for x in sel_b)
                  - sum(x ** (2 * k) for x in sel_a)
                  for k in range(1, nx + 1)]
            tot = 0
            for c, e in derive_F(n):
                tm = c
                for k in range(nx):
                    tm *= xs[k] ** e[k]
                tot += tm
            if tot != 0:
                continue
            for (A, B) in completer(sel_a, sel_b, n, H):
                key = (tuple(A), tuple(B)) if A < B else (tuple(B), tuple(A))
                if key in vus:
                    continue
                vus.add(key)
                deg = verifier(A, B, n)
                msg = (f"  *** SOLUTION n={n} hauteur {max(A+B)} : "
                       f"a={A} b={B} degre={deg}")
                print(msg, flush=True)
                lignes.append(msg)
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lignes) + "\n")
        if a1 % 10 == 0 or time.time() - tA > 30:
            print(f"  .. a1 = {a1} fait en {time.time()-tA:.1f}s "
                  f"(total {time.time()-t0:.0f}s)", flush=True)
    print(f"Termine ({time.time()-t0:.0f}s).", flush=True)


if __name__ == "__main__":
    main()
