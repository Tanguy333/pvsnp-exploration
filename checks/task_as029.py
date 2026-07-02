"""
TACHE AS-029 -- LE PONT : la cascade des certificats duaux.

Cote primal (AS-015, le mur de C13) :
  D(n+1,d,t) = min_pi [ 1/2 h1(pi) + 1/2 h2(pi) ],
  h1(pi) = min_{S == pi (2)} ||P_d(S + g/2)||^2,
  h2(pi) = min_{Z' == pi (2)} ||P_{d-1}(Z' + delta/2)||^2.
Le decouple (min separes) perd le facteur ~3^d : C13 <=> les couplages
de parite le recuperent (AS-017).

Cote dual : un certificat w in V_d^perp a coordonnees DEMI-ENTIERES
(appariements entiers avec 2Z^{2^n}) donne
  h1(pi) >= frac(<pi + g/2, w>)^2 / ||w||^2,
et la dependance en pi passe par les appariements <pi, w> in (1/2)Z.
LE PONT (teste ici au premier etage, exhaustivement) : existe-t-il des
PAIRES (w_A, w_B) dont les parties fractionnaires couvrent CONJOINTEMENT
toutes les classes pi —
  B_dual = max_{w_A, w_B} min_pi [ 1/2 frac_A(pi)^2/||w_A||^2
                                 + 1/2 frac_B(pi)^2/||w_B||^2 ]
recouvre-t-il D(n+1,d,t) (ou au moins le gain de couplage) ?

Verdicts possibles :
- B_dual ~ D_true : le pont EXISTE au premier etage — la tour dyadique
  devient une induction sur les certificats (l'idee manquante a une
  version duale finie).
- B_dual ~ B_dual_decouple << D_true : les certificats ne voient pas le
  couplage — pont mort au premier etage, consigne.

Cellules : (n+1,d,t) = (4,2,2), (4,2,3), (4,1,2) — exhaustif (256 pi,
candidats primaux 3^8, certificats en dim 1 et 4).
"""

from __future__ import annotations

import itertools
import sys
import time
from fractions import Fraction as F
from math import comb

import numpy as np

sys.path.insert(0, "checks")
from task_as002_cvp import monomial_matrix, kernel_basis  # noqa: E402


def orthobasis_int(n, d):
    """Base entiere saturee de V_d^perp dans R^{2^n} (euclidien)."""
    A, monos = monomial_matrix(n, d)
    # lignes de A^T = monomes ; noyau = orthocomplement
    At = [[A[i][j] for i in range(1 << n)] for j in range(len(monos))]
    K = kernel_basis(At)                    # r x 2^n, sature
    return K


def projector_np(n, d):
    A, monos = monomial_matrix(n, d)
    Am = np.array(A, dtype=float)
    P = np.eye(1 << n) - Am @ np.linalg.solve(Am.T @ Am, Am.T)
    return P


def h_values(n, d, target):
    """h(pi) exact-float pour chaque pi : min_{v == pi (2)} ||P(v+target)||^2,
    candidats v_k in {pi_k-2, pi_k, pi_k+2} (cible dans [-1,1])."""
    N = 1 << n
    P = projector_np(n, d)
    out = {}
    for pi in itertools.product((0, 1), repeat=N):
        best = None
        Vs = np.array(list(itertools.product(
            *[(p - 2.0, float(p), p + 2.0) for p in pi])))
        Y = (Vs + target) @ P.T
        vals = np.sum(Y * Y, axis=1)
        out[pi] = float(np.min(vals))
    return out


def frac_sq(x):
    """(distance de x a Z)^2, x float."""
    f = abs(x - round(x))
    return f * f


def certificates(n, d, coef_box):
    """Liste de (w float array, ||w||^2) pour a = combo entier de la base
    saturee de V_d^perp, w = a/2, coefficients dans [-box..box]."""
    K = orthobasis_int(n, d)
    r = len(K)
    Kv = np.array(K, dtype=float)
    outs = []
    for cs in itertools.product(range(-coef_box, coef_box + 1), repeat=r):
        if all(c == 0 for c in cs):
            continue
        a = np.array(cs, dtype=float) @ Kv
        w = a / 2.0
        outs.append((w, float(np.sum(w * w))))
    return outs


def bridge_cell(n1, d, t, box_a=4, box_b=2):
    n = n1 - 1
    N = 1 << n
    wt = [bin(x).count("1") for x in range(N)]
    ft = np.array([1.0 if w >= t else 0.0 for w in wt])
    ft1 = np.array([1.0 if w >= t - 1 else 0.0 for w in wt])
    g2 = (ft + ft1) / 2.0
    dl2 = (ft - ft1) / 2.0
    print(f"== cellule (n+1={n1}, d={d}, t={t}) ==", flush=True)
    t0 = time.time()
    h1 = h_values(n, d, g2)
    h2 = h_values(n, d - 1, dl2)
    pis = list(h1.keys())
    D_true = min(0.5 * h1[p] + 0.5 * h2[p] for p in pis)
    D_dec = 0.5 * min(h1.values()) + 0.5 * min(h2.values())
    print(f"  D_true (couple)  = {D_true:.6f}")
    print(f"  D_decouple       = {D_dec:.6f}"
          f"   [gain de couplage = {D_true - D_dec:.6f}]")
    # certificats
    certA = certificates(n, d, box_a)
    certB = certificates(n, d - 1, box_b)
    print(f"  certificats : |A| = {len(certA)}, |B| = {len(certB)} "
          f"({time.time() - t0:.0f}s)", flush=True)
    # bornes duales DECOUPLEES (chaque cote separement)
    piA = np.array(pis, dtype=float)

    def best_single(certs, target):
        best = 0.0
        for w, nw in certs:
            fr = min(frac_sq(float(np.dot(p, w) + np.dot(target, w)))
                     for p in piA)
            v = fr / nw
            if v > best:
                best = v
        return best

    bA = best_single(certA, g2)
    bB = best_single(certB, dl2)
    dual_dec = 0.5 * bA + 0.5 * bB
    print(f"  dual DECOUPLE    = {dual_dec:.6f}")
    # borne duale COUPLEE : max sur paires du min sur pi
    t0 = time.time()
    # precalcul des fracs par certificat (vecteur sur les pi)
    def frac_vec(certs, target):
        out = []
        for w, nw in certs:
            dots = piA @ w + float(np.dot(target, w))
            fr = (dots - np.round(dots)) ** 2
            out.append((fr, nw))
        return out

    fA = frac_vec(certA, g2)
    fB = frac_vec(certB, dl2)
    best = (0.0, None, None)
    for ia, (fra, nwa) in enumerate(fA):
        va = 0.5 * fra / nwa
        # majorant rapide : min_pi va + max possible de vb
        for ib, (frb, nwb) in enumerate(fB):
            v = float(np.min(va + 0.5 * frb / nwb))
            if v > best[0]:
                best = (v, ia, ib)
    dual_cpl, ia, ib = best
    print(f"  dual COUPLE      = {dual_cpl:.6f}   "
          f"[recouvre {100 * dual_cpl / D_true:.1f}% de D_true ; "
          f"gain dual = {dual_cpl - dual_dec:.6f}]", flush=True)
    if ia is not None:
        wA = certA[ia][0] * 2
        wB = certB[ib][0] * 2
        print(f"  paire gagnante : 2w_A = {wA.astype(int).tolist()}, "
              f"2w_B = {wB.astype(int).tolist()} ({time.time() - t0:.0f}s)")
    return D_true, D_dec, dual_dec, dual_cpl


def main():
    for (n1, d, t) in [(4, 2, 2), (4, 2, 3), (4, 1, 2)]:
        bridge_cell(n1, d, t)
        print()


if __name__ == "__main__":
    main()
