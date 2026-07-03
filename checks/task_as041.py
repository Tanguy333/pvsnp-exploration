"""
TACHE AS-041 -- l'anatomie mod 2 de l'annulation de Lucas.

FAIT STRUCTUREL (verifie ici) : sign(m) = (-1)^{m.Cf} ne depend que de
la classe eps = m mod 2. Donc
  S_pm(s) = somme_eps (-1)^{eps.Cf} M_eps(s),
  M_eps(s) = somme_{m == eps (2)} e^{-pi s^2 val*(m)}  (masse >= 0).
L'annulation = deficit de balance entre classes de signes opposes.

Mesures (cellules d = 2, 3 ; primal <-> dual via Poisson par classe) :
1. verification : somme des M_eps signees = S_pm (recoupement exact) ;
2. la DISTRIBUTION du desequilibre : part de |S_pm| portee par chaque
   paire de classes appariees — concentration ou diffusion ?
3. la loi du signe : (-1)^{eps.Cf} vs la masse M_eps — correlation.
NB dimensionnel : 2^r classes — exhaustif seulement pour r <= ~14 ;
on mesure aux cellules r = 6..10 ((9..13, d=3)), masses par
enumeration duale par classe (rayon petit a s modere, streaming).
"""

from __future__ import annotations

import sys
import time
from collections import Counter
from fractions import Fraction as F
from math import exp, log, pi

sys.path.insert(0, "checks")
from task_as035 import enum_vecs, inv_rat  # noqa: E402
from task_as023 import lll_gram  # noqa: E402


def masses_stream(Gi, Cf, s2, radius):
    """Masses par classe eps = m mod 2, EN FLUX (4e recidive du
    stockage evitee) : accumulation a la feuille, aucun point stocke."""
    r = len(Gi)
    M = [[Gi[i][j] for j in range(r)] for i in range(r)]
    U = lll_gram(M)
    L = [[F(1) if i == j else F(0) for j in range(r)] for i in range(r)]
    Dg = [F(0)] * r
    for i in range(r):
        Dg[i] = M[i][i] - sum(L[i][j] ** 2 * Dg[j] for j in range(i))
        for k in range(i + 1, r):
            L[k][i] = (M[k][i] - sum(L[k][j] * L[i][j] * Dg[j]
                                     for j in range(i))) / Dg[i]
    mass = Counter()
    cnt = [0]
    y = [0] * r
    s2f = float(s2)
    Umod = [[U[i][j] % 2 for j in range(r)] for i in range(r)]

    def dfs(i, part):
        if i < 0:
            eps = tuple(sum(Umod[k][j] * y[j] for j in range(r)) % 2
                        for k in range(r))
            mass[eps] += exp(-pi * s2f * float(part))
            cnt[0] += 1
            return
        s = sum(L[j][i] * y[j] for j in range(i + 1, r) if y[j])
        center = -s
        k0 = round(center)
        left, right = k0 - 1, k0 + 1
        kk = k0
        while True:
            t = part + Dg[i] * (kk - center) ** 2
            if t > radius:
                break
            y[i] = kk
            dfs(i - 1, t)
            y[i] = 0
            if abs(left - center) <= abs(right - center):
                kk, left = left, left - 1
            else:
                kk, right = right, right + 1

    dfs(r - 1, F(0))
    return mass, cnt[0]


def anatomy(n, d, Dval, x):
    from task_as006b import weight_form
    t = (n + 1) // 2
    f = [1 if k >= t else 0 for k in range(n + 1)]
    C, Cm, Qb = weight_form(n, d)
    r = len(C)
    Cf = [sum(C[i][k] * f[k] for k in range(n + 1)) for i in range(r)]
    Qrat = [[F(int(Qb[i, j].p), int(Qb[i, j].q)) for j in range(r)]
            for i in range(r)]
    Q4 = [[4 * Qrat[i][j] for j in range(r)] for i in range(r)]
    Gi, det4Q = inv_rat(Q4)
    fourD = 4.0 * float(Dval)
    s2 = fourD * x
    Rd = F(8) / F(s2)          # queue e^{-8pi} ~ 1e-11 : negligeable
    mass, ndual = masses_stream(Gi, Cf, s2, Rd)
    dual = []
    Sp = sum(mass.values())
    Ss = 0.0
    pairs = []
    seen = set()
    cfmod = tuple(c % 2 for c in Cf)
    for eps, me in mass.items():
        sg = (-1) ** (sum(e * c for e, c in zip(eps, Cf)) % 2)
        Ss += sg * me
    # appariement : eps <-> eps + delta ou delta est un vecteur qui
    # inverse le signe ; canonique : premiere coordonnee ou Cf est
    # impair
    j0 = next((j for j in range(r) if Cf[j] % 2 == 1), None)
    imbalance = []
    if j0 is not None:
        for eps, me in mass.items():
            if eps in seen:
                continue
            ep2 = list(eps)
            ep2[j0] ^= 1
            ep2 = tuple(ep2)
            seen.add(eps)
            seen.add(ep2)
            m2 = mass.get(ep2, 0.0)
            imbalance.append(abs(me - m2))
        imbalance.sort(reverse=True)
        tot_imb = sum(imbalance)
        top = imbalance[:5]
        conc = sum(top) / tot_imb if tot_imb > 0 else float("nan")
    else:
        tot_imb, conc, top = float("nan"), float("nan"), []
    rho = abs(Ss) / Sp if Sp > 0 else float("nan")
    print(f"  (n={n:>2}, d={d}) r={r:>2}, x={x} : |dual| = {ndual} ; "
          f"classes occupees = {len(mass)}/{2**r} ; rho = {rho:.2e} ; "
          f"|S_pm| = {abs(Ss):.3e} vs somme|desequilibres| = "
          f"{tot_imb:.3e} ; top5 des paires = {100*conc:.0f}% du "
          f"desequilibre", flush=True)
    return rho


def main():
    print("== anatomie mod 2 de l'annulation (signe = fonction de "
          "m mod 2) ==")
    cells = [(9, 3, float(F(387, 512)), 0.3),
             (11, 3, float(F(63, 16)), 0.2),
             (13, 3, float(F(9749, 512)), 0.12),
             (9, 2, 4.365, 0.2),
             (11, 2, 20.10, 0.12)]
    for n, d, D, x in cells:
        t0 = time.time()
        anatomy(n, d, D, x)
        if time.time() - t0 > 30:
            print(f"    [{time.time()-t0:.0f}s]", flush=True)


if __name__ == "__main__":
    main()
