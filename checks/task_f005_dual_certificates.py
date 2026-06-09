"""
TACHE F-005 -- Certificats duaux de l'optimalite L1 (vers la borne inf d'O-F002).

Primal (LP, coefficients REELS -- si l'optimum LP = (3^k-1)/2, la borne
inferieure vaut sur R, plus fort que sur Z) :
    min sum_S a_S
    s.c.  a_S >= c_S, a_S >= -c_S                  (pour tout S <= [2k])
          sum_S c_S m_S(z) >= 1   si IP(z) = 1
          sum_S c_S m_S(z) <= 0   si IP(z) = 0

Dual (lecture) : poids u_z >= 0 sur IP^{-1}(1), v_z >= 0 sur IP^{-1}(0),
maximisant sum u_z, tels que pour TOUT monome S :
    | sum_{z superset S, IP=1} u_z  -  sum_{z superset S, IP=0} v_z | <= 1.

Symetrie d'IP : permutation des k paires + echange x_i <-> y_i dans chaque
paire. Orbites des entrees : (a, b, c) = (#paires 11, #paires mixtes 10/01,
#paires 00), a+b+c = k, IP(z) = a mod 2.

Ce script :
  1. Resout le LP (continu) pour k = 2, 3, 4 ; verifie valeur = (3^k-1)/2.
  2. Extrait les duaux des contraintes d'entree (attribut .pi de PuLP/CBC).
  3. Moyenne par orbite (le dual symetrise reste optimal par convexite).
  4. Verifie independamment la faisabilite du dual symetrise et sa valeur.
  5. Affiche les tables u(a,b,c) / v(a,b,c) pour inspection de forme close.
"""

from __future__ import annotations

import csv
import itertools
from collections import defaultdict
from fractions import Fraction

import pulp


def ip(z: tuple[int, ...]) -> int:
    k = len(z) // 2
    return sum(z[i] * z[i + k] for i in range(k)) % 2


def orbit(z: tuple[int, ...]) -> tuple[int, int, int]:
    k = len(z) // 2
    a = sum(1 for i in range(k) if z[i] == 1 and z[i + k] == 1)
    b = sum(1 for i in range(k) if z[i] != z[i + k])
    c = k - a - b
    return (a, b, c)


def monomials(n: int):
    out = []
    for d in range(n + 1):
        out.extend(itertools.combinations(range(n), d))
    return out


def solve_lp_and_duals(k: int):
    n = 2 * k
    monos = monomials(n)
    prob = pulp.LpProblem("f005", pulp.LpMinimize)
    c = [pulp.LpVariable(f"c{i}") for i in range(len(monos))]          # libres
    a = [pulp.LpVariable(f"a{i}", lowBound=0) for i in range(len(monos))]
    for i in range(len(monos)):
        prob += a[i] >= c[i]
        prob += a[i] >= -c[i]
    prob += pulp.lpSum(a)
    cons_names = {}
    for idx, z in enumerate(itertools.product([0, 1], repeat=n)):
        s = pulp.lpSum(c[i] for i in range(len(monos))
                       if all(z[j] for j in monos[i]))
        name = f"in_{idx}"
        if ip(z) == 1:
            prob += (s >= 1), name
        else:
            prob += (s <= 0), name
        cons_names[idx] = z
    solver = pulp.PULP_CBC_CMD(msg=False, timeLimit=300)
    prob.solve(solver)
    obj = pulp.value(prob.objective)
    duals = {}
    for idx, z in cons_names.items():
        pi = prob.constraints[f"in_{idx}"].pi
        duals[z] = pi if pi is not None else 0.0
    return obj, duals


def verify_symmetrized(k: int, u_orb: dict, v_orb: dict) -> tuple[bool, float]:
    """
    Verification independante : avec u_z = u_orb[orbit(z)] (IP=1) et
    v_z = v_orb[orbit(z)] (IP=0), verifier |mu(S)| <= 1 + eps pour tout S
    et calculer sum u_z.
    """
    n = 2 * k
    inputs = list(itertools.product([0, 1], repeat=n))
    u = {z: u_orb.get(orbit(z), 0.0) for z in inputs if ip(z) == 1}
    v = {z: v_orb.get(orbit(z), 0.0) for z in inputs if ip(z) == 0}
    total_u = sum(u.values())
    eps = 1e-6
    ok = True
    worst = 0.0
    for S in monomials(n):
        mu = 0.0
        for z in inputs:
            if all(z[j] for j in S):
                if ip(z) == 1:
                    mu += u.get(z, 0.0)
                else:
                    mu -= v.get(z, 0.0)
        worst = max(worst, abs(mu))
        if abs(mu) > 1 + eps:
            ok = False
    return ok, total_u, worst


def main() -> None:
    print("TACHE F-005 -- certificats duaux LP de l'optimalite (3^k-1)/2")
    print("=" * 76)
    rows = []
    for k in [2, 3, 4]:
        target = (3 ** k - 1) / 2
        obj, duals = solve_lp_and_duals(k)
        print(f"\nk={k} : optimum LP (reels) = {obj}  ;  (3^k-1)/2 = {target}"
              f"  [{'EGAL -- borne valide sur R' if abs(obj - target) < 1e-6 else 'DIFFERENT'}]")

        # Moyenne par orbite (separement IP=1 / IP=0)
        sums1, cnt1 = defaultdict(float), defaultdict(int)
        sums0, cnt0 = defaultdict(float), defaultdict(int)
        for z, pi in duals.items():
            o = orbit(z)
            if ip(z) == 1:
                sums1[o] += pi
                cnt1[o] += 1
            else:
                sums0[o] += pi
                cnt0[o] += 1
        u_orb = {o: sums1[o] / cnt1[o] for o in sums1}
        v_orb = {o: -sums0[o] / cnt0[o] for o in sums0}  # contrainte <=, dual negatif

        print(f"  Orbites IP=1 (a impair) -- u(a,b,c) [taille orbite] :")
        for o in sorted(u_orb):
            size = cnt1[o]
            val = u_orb[o]
            frac = Fraction(val).limit_denominator(10**6)
            print(f"    (a,b,c)=({o[0]},{o[1]},{o[2]}) : u = {val:.6f} ~ {frac}   [{size} entrees]")
            rows.append({"k": k, "type": "u", "a": o[0], "b": o[1], "c": o[2],
                         "valeur": round(val, 8), "taille_orbite": size})
        print(f"  Orbites IP=0 (a pair) -- v(a,b,c) [taille orbite] :")
        for o in sorted(v_orb):
            size = cnt0[o]
            val = v_orb[o]
            frac = Fraction(val).limit_denominator(10**6)
            print(f"    (a,b,c)=({o[0]},{o[1]},{o[2]}) : v = {val:.6f} ~ {frac}   [{size} entrees]")
            rows.append({"k": k, "type": "v", "a": o[0], "b": o[1], "c": o[2],
                         "valeur": round(val, 8), "taille_orbite": size})

        ok, total, worst = verify_symmetrized(k, u_orb, v_orb)
        print(f"  Verification du dual symetrise : faisable={ok} "
              f"(max |mu(S)| = {worst:.6f}), valeur = {total:.6f}")

    with open("data/dual_certificates.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["k", "type", "a", "b", "c",
                                           "valeur", "taille_orbite"])
        w.writeheader()
        w.writerows(rows)
    print("\nCSV : data/dual_certificates.csv")


if __name__ == "__main__":
    main()
