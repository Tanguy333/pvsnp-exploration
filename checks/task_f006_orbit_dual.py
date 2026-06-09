"""
TACHE F-006 -- LP dual reduit aux orbites : vers la forme close du certificat.

Le probleme (P) de F-005, reduit par la symetrie d'IP (permutation des k
paires + echange x_i <-> y_i dans chaque paire) :

  Orbites d'entrees : (a, b, c), a+b+c = k
    a = #paires 11, b = #paires mixtes (10 ou 01), c = #paires 00.
    Taille d'orbite : k!/(a!b!c!) * 2^b.   IP = a mod 2.
  Variables : u(a,b,c) >= 0 si a impair, v(a,b,c) >= 0 si a pair.

  Types de monomes : (p, q), p+q <= k
    p = #paires dont les DEUX coordonnees sont dans S,
    q = #paires dont UNE coordonnee est dans S (le reste libre).
  Moment symetrise :
    mu(p,q) = sum_{i=0..q} sum_{j+m+l=r} C(q,i) * r!/(j!m!l!) * 2^m
              * w(p+i+j, (q-i)+m, l)
    ou r = k-p-q et w(a,b,c) = u si a impair, -v si a pair.
    (i = #paires de type q completees en 11 ; sur les r paires libres :
     j paires 11, m mixtes ALIGNEES avec... ATTENTION : pour une paire
     libre, z peut etre 10 ou 01 -> 2 facons, d'ou le 2^m. Pour une paire
     de type q, la coordonnee specifiee est forcee a 1 : l'autre est 0
     (mixte, 1 facon -- l'orientation est fixee par S) ou 1 (11).)

  LP : max sum_{a impair} taille(a,b,c) * u(a,b,c)
       s.c. |mu(p,q)| <= 1 pour tout (p,q).

  Par dualite L1/L_infty et symetrisation, l'optimum doit etre (3^k-1)/2.

Etapes :
  1. Stage 1 : resoudre, verifier optimum = (3^k-1)/2 pour k = 2..7.
  2. Stage 2 (canonisation) : fixer la valeur optimale, minimiser la masse
     totale sum taille*(u+v) -> sommet de masse minimale.
  3. Rationaliser (limit_denominator), VERIFIER EN FRACTIONS EXACTES
     (faisabilite + valeur), afficher les tables pour inspection.
"""

from __future__ import annotations

import csv
import itertools
from fractions import Fraction
from math import factorial

import pulp


def orbits(k: int):
    out = []
    for a in range(k + 1):
        for b in range(k + 1 - a):
            out.append((a, b, k - a - b))
    return out


def orbit_size(o) -> int:
    a, b, c = o
    k = a + b + c
    return factorial(k) // (factorial(a) * factorial(b) * factorial(c)) * 2 ** b


def mono_types(k: int):
    out = []
    for p in range(k + 1):
        for q in range(k + 1 - p):
            out.append((p, q))
    return out


def moment_coeffs(k: int, p: int, q: int):
    """ Coefficients exacts du moment mu(p,q) sur chaque orbite (a,b,c) :
        dict {(a,b,c): coefficient entier}. """
    r = k - p - q
    coeffs: dict[tuple, int] = {}
    for i in range(q + 1):
        ci = factorial(q) // (factorial(i) * factorial(q - i))
        for j in range(r + 1):
            for m in range(r + 1 - j):
                l = r - j - m
                cr = factorial(r) // (factorial(j) * factorial(m) * factorial(l))
                cnt = ci * cr * (2 ** m)
                o = (p + i + j, (q - i) + m, l)
                coeffs[o] = coeffs.get(o, 0) + cnt
    return coeffs


def solve_orbit_lp(k: int):
    """ Stage 1 + Stage 2. Retourne (val1, u, v) rationalises. """
    obs = orbits(k)
    u_vars = {o: pulp.LpVariable(f"u_{o[0]}_{o[1]}_{o[2]}", lowBound=0)
              for o in obs if o[0] % 2 == 1}
    v_vars = {o: pulp.LpVariable(f"v_{o[0]}_{o[1]}_{o[2]}", lowBound=0)
              for o in obs if o[0] % 2 == 0}

    def build(prob):
        for (p, q) in mono_types(k):
            co = moment_coeffs(k, p, q)
            expr = pulp.lpSum(
                co[o] * (u_vars[o] if o[0] % 2 == 1 else -v_vars[o])
                for o in co)
            prob += expr <= 1, f"mom_up_{p}_{q}"
            prob += expr >= -1, f"mom_lo_{p}_{q}"

    obj = pulp.lpSum(orbit_size(o) * u_vars[o] for o in u_vars)

    # Stage 1
    prob1 = pulp.LpProblem("orbit_dual", pulp.LpMaximize)
    prob1 += obj
    build(prob1)
    prob1.solve(pulp.PULP_CBC_CMD(msg=False))
    val1 = pulp.value(prob1.objective)

    # Stage 2 : valeur fixee, masse minimale
    prob2 = pulp.LpProblem("orbit_dual_canon", pulp.LpMinimize)
    prob2 += pulp.lpSum(orbit_size(o) * u_vars[o] for o in u_vars) + \
             pulp.lpSum(orbit_size(o) * v_vars[o] for o in v_vars)
    build(prob2)
    prob2 += pulp.lpSum(orbit_size(o) * u_vars[o] for o in u_vars) >= val1 - 1e-9
    prob2.solve(pulp.PULP_CBC_CMD(msg=False))

    u = {o: Fraction(u_vars[o].value() or 0).limit_denominator(100000)
         for o in u_vars}
    v = {o: Fraction(v_vars[o].value() or 0).limit_denominator(100000)
         for o in v_vars}
    return val1, u, v


def verify_exact(k: int, u: dict, v: dict):
    """ Verification en arithmetique exacte : faisabilite et valeur. """
    target = Fraction(3 ** k - 1, 2)
    value = sum(Fraction(orbit_size(o)) * u[o] for o in u)
    ok = True
    tights = []
    for (p, q) in mono_types(k):
        co = moment_coeffs(k, p, q)
        mu = sum(Fraction(co[o]) * (u[o] if o[0] % 2 == 1 else -v[o])
                 for o in co)
        if abs(mu) > 1:
            ok = False
        if abs(mu) == 1:
            tights.append((p, q, '+' if mu == 1 else '-'))
    return ok, value == target, value, tights


def main() -> None:
    print("TACHE F-006 -- LP dual reduit aux orbites, forme close ?")
    print("=" * 76)
    rows = []
    for k in range(2, 8):
        target = Fraction(3 ** k - 1, 2)
        val1, u, v = solve_orbit_lp(k)
        ok_feas, ok_val, value, tights = verify_exact(k, u, v)
        print(f"\nk={k} : stage1 = {val1:.6f} (cible {float(target)}) ; "
              f"verif EXACTE du sommet canonique : faisable={ok_feas}, "
              f"valeur={value} (={ok_val})")
        print("  u(a,b,c) non nuls :")
        for o in sorted(u):
            if u[o] != 0:
                print(f"    u{o} = {u[o]}")
                rows.append({"k": k, "type": "u", "a": o[0], "b": o[1],
                             "c": o[2], "valeur": str(u[o])})
        print("  v(a,b,c) non nuls :")
        for o in sorted(v):
            if v[o] != 0:
                print(f"    v{o} = {v[o]}")
                rows.append({"k": k, "type": "v", "a": o[0], "b": o[1],
                             "c": o[2], "valeur": str(v[o])})
        print(f"  moments serres (|mu|=1) : {tights}")

    with open("data/orbit_dual.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["k", "type", "a", "b", "c", "valeur"])
        w.writeheader()
        w.writerows(rows)
    print("\nCSV : data/orbit_dual.csv")


if __name__ == "__main__":
    main()
