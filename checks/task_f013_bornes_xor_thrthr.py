"""
TACHE F-013 -- resserrer la fenetre XOR(THR4,THR4) in [?, 120].

Volet 1 (BORNE INF, prouvee) : THEOREME de tranche.
  Si p = sum a_S m_S separe f par valeurs et f(z_A, 0) = g_A(z_A),
  alors p(., 0) = sum_{S inclus dans A} a_S m_S separe g_A -- donc
  sum_{S in A} a_S >= W(g_A). Idem cote B. Les deux masses sont
  disjointes (S in A vs S in B), les monomes croises >= 0 :
      W(f) >= W(g_A) + W(g_B)
  pour tout combineur avec f(z_A,0) = g_A et f(0,z_B) = g_B --
  en particulier XOR et OR de blocs s'annulant en 0
  (THR4(0) = 0, GT2(0) = 0).
  W(THR4) et W(GT2) calcules EXACTEMENT a n = 4 (ILP, secondes).

Volet 2 (BORNE SUP, heuristique) : recuit simule sur les vecteurs de
coefficients (cout lexicographique : collisions puis poids). Toute
solution trouvee est RE-VERIFIEE par enumeration exacte.
"""

from __future__ import annotations

import itertools
import random
import time

import pulp


def min_symand_weight_exact(f, n, U=64, tl=120):
    """ILP exact (modele F-003/F-012) -- pour petits n."""
    inputs = list(itertools.product((0, 1), repeat=n))
    ones = [z for z in inputs if f(z) == 1]
    zeros = [z for z in inputs if f(z) == 0]
    monos = []
    for d in range(1, n + 1):
        monos.extend(itertools.combinations(range(n), d))
    M = U * len(monos) + 1
    prob = pulp.LpProblem("symand", pulp.LpMinimize)
    a = [pulp.LpVariable(f"a{i}", lowBound=0, upBound=U, cat="Integer")
         for i in range(len(monos))]
    prob += pulp.lpSum(a)
    def p_expr(z):
        return pulp.lpSum(a[i] for i in range(len(monos))
                          if all(z[j] for j in monos[i]))
    for i1, z1 in enumerate(ones):
        for i0, z0 in enumerate(zeros):
            b = pulp.LpVariable(f"b_{i1}_{i0}", cat="Binary")
            prob += p_expr(z1) - p_expr(z0) >= 1 - M * b
            prob += p_expr(z0) - p_expr(z1) >= 1 - M * (1 - b)
    status = prob.solve(pulp.PULP_CBC_CMD(msg=False, timeLimit=tl))
    return round(pulp.value(prob.objective)), pulp.LpStatus[status]


def collisions_and_weight(f, n, coef):
    """coef : dict S(frozenset) -> a >= 1. Retourne (collisions, poids)."""
    ones_vals, zeros_vals = {}, {}
    for z in itertools.product((0, 1), repeat=n):
        p = sum(a for S, a in coef.items() if all(z[j] for j in S))
        d = ones_vals if f(z) else zeros_vals
        d[p] = d.get(p, 0) + 1
    coll = sum(min(ones_vals.get(v, 0), zeros_vals.get(v, 0)) > 0
               for v in set(ones_vals) | set(zeros_vals))
    return coll, sum(coef.values())


def anneal(f, n, seed_coef, iters=150_000, T0=3.0, seed=0):
    """Recuit lexicographique : collisions d'abord, poids ensuite."""
    rng = random.Random(seed)
    monos = []
    for d in range(1, n + 1):
        monos.extend(frozenset(c)
                     for c in itertools.combinations(range(n), d))
    coef = dict(seed_coef)
    best = None

    def cost(c):
        coll, w = collisions_and_weight(f, n, c)
        return coll * 10_000 + w

    cur = cost(coef)
    for it in range(iters):
        T = T0 * (1 - it / iters) + 0.01
        S = rng.choice(monos)
        delta = rng.choice((-1, 1))
        new = dict(coef)
        v = new.get(S, 0) + delta
        if v < 0 or v > 127:
            continue
        if v == 0:
            new.pop(S, None)
        else:
            new[S] = v
        cn = cost(new)
        if cn <= cur or rng.random() < 2.7 ** (-(cn - cur) / T):
            coef, cur = new, cn
            if cur < 10_000 and (best is None or cur < best[0]):
                best = (cur, dict(coef))
    return best


def main():
    thr4 = lambda z: 1 if 4 * z[0] + 3 * z[1] + 2 * z[2] + z[3] >= 4 else 0
    gt2 = lambda z: 1 if 2 * z[0] + z[1] - 2 * z[2] - z[3] >= 1 else 0

    print("== Volet 1 : bornes inf par le theoreme de tranche ==")
    for name, g in [("THR4", thr4), ("GT2", gt2)]:
        w, st = min_symand_weight_exact(g, 4)
        print(f"  W({name}) = {w} [{st}]", flush=True)
        if st != "Optimal":
            print("    (non optimal -- borne inf de tranche NON valide)")
            continue
        print(f"  => W(XOR({name},{name})) >= {2*w} ; "
              f"W(OR({name},{name})) >= {2*w}  (theoreme de tranche)")

    print("\n== Volet 2 : chasse a la borne sup (recuit, 3 graines) ==")
    thr4b = lambda z: 1 if z[4] + 2 * z[5] + 3 * z[6] + 4 * z[7] >= 4 else 0
    fxor = lambda z: (thr4(z) + thr4b(z)) % 2
    # graine : l'encodage par blocs (120), que le recuit doit battre
    seed_coef = {frozenset([0]): 4, frozenset([1]): 3,
                 frozenset([2]): 2, frozenset([3]): 1,
                 frozenset([4]): 11, frozenset([5]): 22,
                 frozenset([6]): 33, frozenset([7]): 44}
    best_overall = (10_000 + 120, seed_coef)
    for sd in range(3):
        t0 = time.time()
        res = anneal(fxor, 8, seed_coef, seed=sd)
        if res and res[0] < best_overall[0]:
            best_overall = res
        print(f"  graine {sd} : meilleur cout {res[0] if res else 'aucun'}"
              f" ({time.time()-t0:.0f}s)", flush=True)

    coll, w = collisions_and_weight(fxor, 8, best_overall[1])
    print(f"\n  MEILLEURE solution re-verifiee : collisions = {coll}, "
          f"poids = {w}")
    if coll == 0:
        print(f"  => BORNE SUP VERIFIEE : W(XOR(THR4,THR4)) <= {w}")
        print(f"  support ({len(best_overall[1])} monomes) : " +
              ", ".join(f"{sorted(S)}:{a}" for S, a in
                        sorted(best_overall[1].items(),
                               key=lambda kv: (len(kv[0]),
                                               sorted(kv[0])))))


if __name__ == "__main__":
    main()
