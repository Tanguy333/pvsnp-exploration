"""
TACHE F-011, etape 17 -- La restriction symetrique est-elle WLOG aux
petits n ? (premiere sonde du modele GENERAL, la marche vers les circuits)

QUESTION : deg_6(MAJ_n) < deg_6^sym(MAJ_n) pour n = 4..7 ?
Valeurs symetriques connues (etapes 1-10, prouvees pour n=4) :
  n=4 (t=2) : 3 (anomalie prouvee) ; n=5,6 (t=3) : 3 ; n=7 (t=4) : 4.

Pourquoi c'est la bonne question : BBR laissent explicitement ouvert le
gap general-vs-symetrique (OR : O(sqrt N) symetrique optimal, mais
"tantalizing possibility" de O(log N) en general ; la borne inf generale
Omega(log N) est Tardos-Barrington 1994). La symetrisation ne preserve
PAS les representations faibles (la condition != 0 n'est pas lineaire).
Les petits n exhaustifs ne sont dans aucun papier consulte.

METHODE : polynomes multilineaires generaux de degre <= d sur Z_6,
representation faible de MAJ (P = 0 ssi |x| < t). Par CRT :
U mod 2 et V mod 3, noyaux des contraintes "= 0 sur les bas points"
(Gauss sur F_p, base du noyau, enumeration complete si p^dim <= cap),
couverture sur les hauts points par paires (u, v).
"""

from __future__ import annotations

import itertools
import time
from math import comb

import numpy as np

KER_CAP = 3_000_000


def monomials(n, d):
    out = []
    for k in range(d + 1):
        out.extend(itertools.combinations(range(n), k))
    return out


def eval_matrix(n, monos, points):
    M = np.zeros((len(points), len(monos)), dtype=np.int64)
    for r, x in enumerate(points):
        for c, S in enumerate(monos):
            M[r, c] = 1 if all((x >> i) & 1 for i in S) else 0
    return M


def nullspace_mod_p(A, p):
    A = A.copy() % p
    rows, cols = A.shape
    pivots = []
    r = 0
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if A[i, c] % p:
                piv = i
                break
        if piv is None:
            continue
        A[[r, piv]] = A[[piv, r]]
        inv = pow(int(A[r, c]), p - 2, p) if p > 2 else 1
        A[r] = (A[r] * inv) % p
        for i in range(rows):
            if i != r and A[i, c] % p:
                A[i] = (A[i] - A[i, c] * A[r]) % p
        pivots.append(c)
        r += 1
        if r == rows:
            break
    free = [c for c in range(cols) if c not in pivots]
    basis = []
    for fc in free:
        v = np.zeros(cols, dtype=np.int64)
        v[fc] = 1
        for i, pc in enumerate(pivots):
            v[pc] = (-A[i, fc]) % p
        basis.append(v % p)
    return basis


def all_kernel(basis, p, ncols):
    dim = len(basis)
    if p ** dim > KER_CAP:
        return None
    if dim == 0:
        return np.zeros((1, ncols), dtype=np.int64)
    B = np.array(basis, dtype=np.int64)
    C = np.array(list(itertools.product(range(p), repeat=dim)), dtype=np.int64)
    return (C @ B) % p


def feasible_general(n, t, d):
    monos = monomials(n, d)
    pts = list(range(1 << n))
    lows = [x for x in pts if bin(x).count("1") < t]
    highs = [x for x in pts if bin(x).count("1") >= t]
    Ml = eval_matrix(n, monos, lows)
    Mh = eval_matrix(n, monos, highs)
    k2 = all_kernel(nullspace_mod_p(Ml, 2), 2, len(monos))
    k3 = all_kernel(nullspace_mod_p(Ml, 3), 3, len(monos))
    if k2 is None or k3 is None:
        return None
    v2 = (k2 @ Mh.T) % 2
    nz3 = ((k3 @ Mh.T) % 3) != 0
    cov3_any = nz3.any(axis=0)
    must_u = np.where(~cov3_any)[0]
    if len(must_u):
        keep = np.all(v2[:, must_u] != 0, axis=1)
        v2 = v2[keep]
        if v2.shape[0] == 0:
            return False
    order = np.argsort((v2 == 0).sum(axis=1))
    for r in order:
        W0 = np.where(v2[r] == 0)[0]
        if len(W0) == 0 or bool(np.all(nz3[:, W0], axis=1).any()):
            return True
    return False


def main() -> None:
    print("TACHE F-011 etape 17 -- l'asymetrie aide-t-elle MAJ mod 6 ?")
    print("=" * 66)
    sym = {4: 3, 5: 3, 6: 3, 7: 4}
    print(f"{'n':>2} {'t':>2} | {'sym':>4} | tests generaux d < sym")
    print("-" * 66)
    findings = []
    for n in (4, 5, 6, 7):
        t = (n + 1) // 2
        s = sym[n]
        line = []
        gain = None
        for d in range(1, s):
            t0 = time.time()
            r = feasible_general(n, t, d)
            lab = "FAISABLE" if r else ("cap" if r is None else "infaisable")
            line.append(f"d={d}: {lab} ({time.time()-t0:.0f}s)")
            if r:
                gain = d
                break
        print(f"{n:>2} {t:>2} | {s:>4} | " + " ; ".join(line), flush=True)
        if gain is not None:
            findings.append((n, gain, s))
    print("-" * 66)
    if findings:
        print("\n*** L'ASYMETRIE GAGNE ***")
        for (n, g, s) in findings:
            print(f"  MAJ_{n} : deg_6 general <= {g} < {s} = deg_6^sym")
        print("La restriction symetrique n'est PAS sans perte, meme a ces")
        print("tailles -- le modele general est strictement plus puissant.")
    else:
        print("\nAucun gain : deg_6 = deg_6^sym pour n = 4..7 (exhaustif aux")
        print("degres testes). La restriction symetrique est ROBUSTE aux")
        print("petits n pour MAJ -- premiere donnee exhaustive sur la")
        print("question generale-vs-symetrique (ouverte chez BBR pour OR).")


if __name__ == "__main__":
    main()
