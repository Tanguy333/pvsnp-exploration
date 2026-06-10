"""
TACHE F-011, etape 20 -- Decision exacte : deg_6(MAJ_10) = 5 ?

L'etape 19 n'avait pas conclu (recuit sous ansatz u = 1, restrictif).
Ici, deux attaques completes :
  (1) recuit JOINT : u in F_2^252 et v in F_3^252 varient ensemble,
      cout = nombre d'ensembles S (|S| in [5,10], 638 au total) avec
      U(S) = 0 ET V(S) = 0 ;
  (2) ILP exact (PuLP/CBC) : pour chaque S,
      sum_{T c S} u_T = 2 k_S + U_S  (U_S binaire),
      sum_{T c S} v_T = 3 m_S + V_S  (V_S in {0,1,2}),
      U_S + V_S >= 1. Faisabilite => certificat ; infaisabilite prouvee
      => deg_6(MAJ_10) >= 6 et l'HYPOTHESE PLATE EST REFUTEE.

(Lemme 5 : a degre 5, le support est exactement les monomes de taille 5 ;
 les zeros sous le seuil sont automatiques.)
"""

from __future__ import annotations

import itertools
import random
import time
from math import comb

import numpy as np

random.seed(2026)
np.random.seed(2026)

N, T = 10, 5
MONOS = list(itertools.combinations(range(N), T))      # 252
SETS = []
for w in range(T, N + 1):
    SETS.extend(itertools.combinations(range(N), w))    # 638


def incidence():
    M = np.zeros((len(SETS), len(MONOS)), dtype=np.int64)
    for r, S in enumerate(SETS):
        Ss = set(S)
        for c, Tm in enumerate(MONOS):
            if set(Tm) <= Ss:
                M[r, c] = 1
    return M


def joint_anneal(M, budget_s=240):
    u = np.random.randint(0, 2, len(MONOS))
    v = np.random.randint(0, 3, len(MONOS))
    Uv = (M @ u) % 2
    Vv = (M @ v) % 3
    cost = int(((Uv == 0) & (Vv == 0)).sum())
    t0 = time.time()
    it = 0
    while time.time() - t0 < budget_s and cost > 0:
        it += 1
        if random.random() < 0.5:
            c = random.randrange(len(MONOS))
            nU = (Uv + M[:, c]) % 2
            ncost = int(((nU == 0) & (Vv == 0)).sum())
            if ncost <= cost or random.random() < 0.01:
                u[c] ^= 1
                Uv = nU
                cost = ncost
        else:
            c = random.randrange(len(MONOS))
            delta = random.choice((1, 2))
            nV = (Vv + delta * M[:, c]) % 3
            ncost = int(((Uv == 0) & (nV == 0)).sum())
            if ncost <= cost or random.random() < 0.01:
                v[c] = (v[c] + delta) % 3
                Vv = nV
                cost = ncost
    return (u, v) if cost == 0 else None, cost, it


def ilp_decide(time_limit=420):
    import pulp
    prob = pulp.LpProblem("maj10_deg5", pulp.LpMinimize)
    u = [pulp.LpVariable(f"u{i}", cat="Binary") for i in range(len(MONOS))]
    v = [pulp.LpVariable(f"v{i}", 0, 2, cat="Integer") for i in range(len(MONOS))]
    prob += 0
    for r, S in enumerate(SETS):
        Ss = set(S)
        cols = [c for c, Tm in enumerate(MONOS) if set(Tm) <= Ss]
        Us = pulp.LpVariable(f"U{r}", cat="Binary")
        Vs = pulp.LpVariable(f"V{r}", 0, 2, cat="Integer")
        k = pulp.LpVariable(f"k{r}", 0, len(cols), cat="Integer")
        m = pulp.LpVariable(f"m{r}", 0, len(cols), cat="Integer")
        prob += pulp.lpSum(u[c] for c in cols) == 2 * k + Us
        prob += pulp.lpSum(v[c] for c in cols) == 3 * m + Vs
        prob += Us + Vs >= 1
    status = prob.solve(pulp.PULP_CBC_CMD(msg=0, timeLimit=time_limit))
    name = pulp.LpStatus[status]
    if name == "Optimal":
        uu = np.array([int(pulp.value(x)) for x in u])
        vv = np.array([int(round(pulp.value(x))) for x in v])
        return "feasible", uu, vv
    if name == "Infeasible":
        return "infeasible", None, None
    return f"timeout/{name}", None, None


def verify(u, v):
    Tsets = [frozenset(Tm) for Tm in MONOS]
    for x in range(1 << N):
        S = frozenset(i for i in range(N) if (x >> i) & 1)
        w = len(S)
        U = sum(int(a) for Ts, a in zip(Tsets, u) if Ts <= S) % 2
        V = sum(int(a) for Ts, a in zip(Tsets, v) if Ts <= S) % 3
        if w < T and (U or V):
            return False
        if w >= T and not (U or V):
            return False
    return True


def main() -> None:
    print("TACHE F-011 etape 20 -- decision : deg_6(MAJ_10) = 5 ?")
    print("=" * 66)
    M = incidence()

    print("\n[1] Recuit JOINT (u, v), budget 240 s :", flush=True)
    sol, cost, iters = joint_anneal(M)
    if sol is not None:
        u, v = sol
        ok = verify(u, v)
        print(f"    CERTIFICAT trouve ({iters} iterations) ; verification"
              f" exhaustive 1024 points : {'OK' if ok else 'ECHEC'}")
        if ok:
            print("\n    => deg_6(MAJ_10) = 5 : l'hypothese plate TIENT a n=10.")
            return
    else:
        print(f"    echec (cout final {cost} apres {iters} iterations)",
              flush=True)

    print("\n[2] ILP exact (CBC, timeout 420 s) :", flush=True)
    t0 = time.time()
    res, u, v = ilp_decide()
    print(f"    statut : {res}   ({time.time()-t0:.0f}s)")
    if res == "feasible":
        ok = verify(u, v)
        print(f"    verification exhaustive : {'OK' if ok else 'ECHEC'}")
        if ok:
            print("\n    => deg_6(MAJ_10) = 5 : l'hypothese plate TIENT a n=10.")
    elif res == "infeasible":
        print("\n    => deg_6(MAJ_10) >= 6 : l'HYPOTHESE PLATE EST REFUTEE.")
        print("       (5e conjecture du fil ; la platitude etait propre aux")
        print("        points speciaux.)")
    else:
        print("\n    => NON CONCLU (recuit + ILP sous timeout). Le statut de")
        print("       la plate a n = 10 reste ouvert -- honnete.")


if __name__ == "__main__":
    main()
