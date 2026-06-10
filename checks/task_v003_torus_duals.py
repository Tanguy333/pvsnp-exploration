"""
TACHE V-003 -- Les certificats duaux des LP toriques de MAJ.

Methode KV (TR24-074) : pour des parties entieres fixees, l'approximation
torique est un LP de Tchebychev ; son DUAL optimal y* est une mesure
signee sur les poids w :
    (i)   orthogonalite : sum_w y*_w C(w, i) = 0 pour tout i <= d
          (y* "annule" les polynomes de degre <= d -- polynome dual) ;
    (ii)  normalisation : sum_w |y*_w| = 1 ;
    (iii) objectif : sum_w y*_w (t_w/2 + k*_w) = eps*.
KV etendent la methode des polynomes duaux au tore et reduisent la
Conjecture 5 de BHLR a une conjecture de norme l2 sur ces objets.

Ici : pour MAJ_n (n = 8, 12, 16) au degre critique (d*(1/8) et d*-1),
  [1] MILP -> k* optimaux ;
  [2] LP a k* fixe -> y* (marginaux HiGHS) ;
  [3] verification numerique de (i)-(iii) ;
  [4] structure de y* : signes, support, l2 -- croissance avec n.
"""

from __future__ import annotations

import time
from math import comb

import numpy as np
from scipy.optimize import linprog, milp, LinearConstraint, Bounds

K_BOUND = 5
MILP_OPTS = {"time_limit": 30.0, "mip_rel_gap": 1e-8}


def milp_solve(n, d, t):
    nv = 1 + (d + 1) + n
    c = np.zeros(nv)
    c[0] = 1.0
    rows, lbs, ubs = [], [], []
    for w in range(0, n + 1):
        target = 0.5 if w >= t else 0.0
        row = np.zeros(nv)
        for i in range(d + 1):
            row[1 + i] = comb(w, i)
        if w >= 1:
            row[1 + d + 1 + (w - 1)] = -1.0
        r1 = row.copy(); r1[0] = -1.0
        rows.append(r1); lbs.append(-np.inf); ubs.append(target)
        r2 = row.copy(); r2[0] = 1.0
        rows.append(r2); lbs.append(target); ubs.append(np.inf)
    integ = np.zeros(nv); integ[1 + d + 1:] = 1
    lb = np.full(nv, -np.inf); ub = np.full(nv, np.inf)
    lb[0] = 0.0; ub[0] = 0.5
    lb[1 + d + 1:] = -K_BOUND; ub[1 + d + 1:] = K_BOUND
    res = milp(c, constraints=LinearConstraint(np.array(rows), lbs, ubs),
               integrality=integ, bounds=Bounds(lb, ub), options=MILP_OPTS)
    if res.x is None:
        return None, None
    kvec = np.concatenate([[0.0], np.round(res.x[1 + d + 1:])])
    return float(res.x[0]), kvec


def lp_with_duals(n, d, t, kvec):
    """ LP a k fixe : min eps ; variables [eps, a_0..a_d]. Retourne
        eps*, y* (mesure signee sur les poids). """
    nv = 1 + (d + 1)
    c = np.zeros(nv); c[0] = 1.0
    A_ub, b_ub = [], []
    # P(w) - eps <= b_w   et   -P(w) - eps <= -b_w
    for w in range(0, n + 1):
        b = (0.5 if w >= t else 0.0) + kvec[w]
        row = np.zeros(nv)
        for i in range(d + 1):
            row[1 + i] = comb(w, i)
        r1 = row.copy(); r1[0] = -1.0
        A_ub.append(r1); b_ub.append(b)
        r2 = -row.copy(); r2[0] = -1.0
        A_ub.append(r2); b_ub.append(-b)
    res = linprog(c, A_ub=np.array(A_ub), b_ub=np.array(b_ub),
                  bounds=[(0, None)] + [(None, None)] * (d + 1),
                  method="highs")
    if not res.success:
        return None, None
    lam = -res.ineqlin.marginals          # >= 0 pour contraintes <=
    # convention : y_w = lam_bas - lam_haut, de sorte que <y, b> = +eps*
    y = np.array([lam[2 * w + 1] - lam[2 * w] for w in range(n + 1)])
    return float(res.fun), y


def main() -> None:
    print("TACHE V-003 -- certificats duaux des LP toriques de MAJ")
    print("=" * 70)
    for n in (8, 12, 16):
        t = (n + 1) // 2
        # degre critique : d*(1/8)
        dstar = None
        for d in range(1, n + 1):
            e, _ = milp_solve(n, d, t)
            if e is not None and e <= 0.125 + 1e-9:
                dstar = d
                break
        for d in (dstar - 1, dstar):
            e_milp, kvec = milp_solve(n, d, t)
            eps, y = lp_with_duals(n, d, t, kvec)
            if y is None:
                print(f"  n={n}, d={d} : LP en echec ?!")
                continue
            # verifications (i)-(iii)
            orth = max(abs(sum(y[w] * comb(w, i) for w in range(n + 1)))
                       for i in range(d + 1))
            norm1 = float(np.abs(y).sum())
            b = np.array([(0.5 if w >= t else 0.0) + kvec[w]
                          for w in range(n + 1)])
            obj = float(y @ b)
            ok = orth < 1e-6 and abs(norm1 - 1) < 1e-6 and abs(obj - eps) < 1e-6
            signs = "".join("+" if v > 1e-9 else "-" if v < -1e-9 else "0"
                            for v in y)
            l2 = float(np.linalg.norm(y))
            print(f"  n={n:>2}, d={d} (eps* = {eps:.4f}) : certificat dual "
                  f"{'VALIDE' if ok else '*** INVALIDE ***'}")
            print(f"      (i) orthogonalite max = {orth:.2e} ; "
                  f"(ii) ||y||_1 = {norm1:.6f} ; (iii) <y,b> - eps = "
                  f"{obj - eps:.2e}")
            print(f"      signes(y) sur w = 0..{n} : {signs}")
            print(f"      ||y||_2 = {l2:.4f} ; support = "
                  f"{int((np.abs(y) > 1e-9).sum())}/{n+1} poids", flush=True)
    print("\nLecture : y* est le 'polynome dual' au sens Bun-Thaler/KV --")
    print("l'objet dont KV conjecturent une propriete l2 (Conjecture 5,")
    print("plus court vecteur de reseau avec gamma_n = 1) pour conclure")
    print("MAJ hors ACC. ||y||_2 mesure la concentration du certificat.")


if __name__ == "__main__":
    main()
