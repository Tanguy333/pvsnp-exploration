"""
TACHE AS-042 -- l'analyse multi-echelle de l'annulation de Lucas
(execution honnete de la commande : mesure des lois d'echelle, critere
d'arret declare — si aucune loi propre, echec consigne).

(A) MULTI-ECHELLE EN ESPACE (F2^r des classes eps) :
    A^(k) = somme sur les cosets de V_k = <e_{j1}..e_{jk}> de
    |sous-somme signee| ; A^(0) = S_+, A^(r) = |S_pm|.
    Facteurs par direction g_k = A^(k)/A^(k-1) : loi geometrique ?
    PREDICTION ENREGISTREE : le saut 25x -> 2264x sur Delta r = 2
    (AS-041) donne gamma ~ 9.5 par direction si la loi est geometrique.
    Robustesse de jauge : deux ordres de directions (Cf-impaires
    d'abord / en dernier).

(B) MULTI-ECHELLE EN s : rho(x) sur une echelle dyadique de
    x = s^2/(4D) — la loi d'echelle de l'annulation en sa variable
    naturelle.

Tout se calcule depuis les tables de masses (M_eps, signe_eps) —
streaming AS-041, aucune nouvelle machinerie.
"""

from __future__ import annotations

import sys
import time
from fractions import Fraction as F
from math import comb, log

sys.path.insert(0, "checks")
from task_as041 import masses_stream  # noqa: E402
from task_as035 import inv_rat  # noqa: E402


def cell_table(n, d, x):
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
    from task_as021 import construct, exact_polish, eval_exact
    # 4D de reference : valeurs certifiees connues
    known = {(9, 3): F(387, 512), (11, 3): F(63, 16)}
    Dv = known[(n, d)]
    fourD = 4.0 * float(Dv)
    s2 = fourD * x
    Rd = F(8) / F(s2)
    mass, ndual = masses_stream(Gi, Cf, s2, Rd)
    sgn = {eps: (-1) ** (sum(e * c for e, c in zip(eps, Cf)) % 2)
           for eps in mass}
    return mass, sgn, r, Cf


def hierarchy(mass, sgn, r, order):
    """A^(k) pour k = 0..r le long d'un ordre de directions."""
    # etat : dictionnaire classe-quotient -> somme signee
    cur = {eps: sgn[eps] * m for eps, m in mass.items()}
    A = [sum(abs(v) for v in cur.values())]
    for j in order:
        nxt = {}
        for eps, v in cur.items():
            key = tuple(e for i, e in enumerate(eps) if i != j)
            # quotient par la direction j : fusionner eps et eps^e_j
            nxt[key] = nxt.get(key, 0.0) + v
        # reindexer : les cles perdent la coordonnee j — pour iterer
        # proprement, on reconstruit des tuples pleins avec 0 en j
        cur = {}
        for key, v in nxt.items():
            full = list(key[:j]) + [0] + list(key[j:])
            cur[tuple(full)] = v
        A.append(sum(abs(v) for v in cur.values()))
    return A


def main():
    print("== (A) hierarchie par directions ==")
    for (n, d, x) in [(9, 3, 0.3), (11, 3, 0.2)]:
        t0 = time.time()
        mass, sgn, r, Cf = cell_table(n, d, x)
        odd = [j for j in range(r) if Cf[j] % 2 == 1]
        even = [j for j in range(r) if Cf[j] % 2 == 0]
        for name, order in [("impaires d'abord", odd + even),
                            ("impaires en dernier", even + odd)]:
            A = hierarchy(mass, sgn, r, order)
            gs = [A[k + 1] / A[k] if A[k] > 0 else float("nan")
                  for k in range(r)]
            print(f"  (n={n}, d={d}) r={r}, ordre {name} :")
            print(f"    A(k)   = " +
                  " ".join(f"{a:.3e}" for a in A))
            print(f"    g_k    = " +
                  " ".join(f"{g:.3f}" for g in gs), flush=True)
        print(f"    ({time.time()-t0:.0f}s)", flush=True)

    print("== (B) spectre en s : rho(x) sur echelle dyadique ==")
    for (n, d, xs) in [(9, 3, (1.2, 0.6, 0.3, 0.15)),
                       (11, 3, (1.6, 0.8, 0.4, 0.2))]:
        vals = []
        for x in xs:
            mass, sgn, r, Cf = cell_table(n, d, x)
            Sp = sum(mass.values())
            Ss = sum(sgn[e] * m for e, m in mass.items())
            rho = abs(Ss) / Sp if Sp > 0 else float("nan")
            vals.append((x, rho))
        print(f"  (n={n}, d={d}) : " +
              " ; ".join(f"x={x}: rho={rho:.2e}" for x, rho in vals),
              flush=True)


if __name__ == "__main__":
    main()
