"""
TACHE F-005b -- Verification approfondie a k=4 et k=5 (demande utilisateur).

Trois choses a verifier independamment :

(A) DNF_min(IP_10) = 121 ?  -- JAMAIS verifie directement : le Tour 18 le
    predit par recurrence, le cahier le marque "non-verifiable par
    enumeration directe". C'est en fait faisable : 3^10 = 59049 ANDs,
    masques de verite de 1024 bits.
    Methode : enumerer tous les ANDs, identifier les implicants de IP_10,
    filtrer les premiers (retrait de chaque litteral), compter
    (prediction : 121 = a_5), puis set cover ILP exact (prediction : 121).
    Idem a k=4 (n=8) pour re-confirmer le 40 du Tour 17.

(B) W_L1(IP_8) = 40 et W_L1(IP_10) = 121 cote certificat :
    extraire les duaux du LP reel, symetriser par orbites, et verifier
    INDEPENDAMMENT (recalcul de tous les moments) que le dual symetrise
    est faisable et atteint la valeur cible. Pour k=5 cette verification
    n'avait pas encore ete faite (F-005 s'arretait a k=4).
"""

from __future__ import annotations

import itertools
import time
from collections import defaultdict

import pulp


# ---------------------------------------------------------------- outils IP

def ip_val(z: tuple[int, ...]) -> int:
    k = len(z) // 2
    return sum(z[i] * z[i + k] for i in range(k)) % 2


def truth_mask(n: int):
    """ Masque (entier de 2^n bits) de IP^{-1}(1) et liste des entrees. """
    inputs = list(itertools.product([0, 1], repeat=n))
    ones_mask = 0
    for idx, z in enumerate(inputs):
        if ip_val(z) == 1:
            ones_mask |= (1 << idx)
    return inputs, ones_mask


def literal_masks(n: int, inputs):
    """ pos[i] = masque des entrees avec z_i = 1 ; neg[i] = z_i = 0. """
    pos = [0] * n
    neg = [0] * n
    for idx, z in enumerate(inputs):
        for i in range(n):
            if z[i] == 1:
                pos[i] |= (1 << idx)
            else:
                neg[i] |= (1 << idx)
    return pos, neg


# ------------------------------------------- (A) primes + DNF_min directs

def primes_and_dnfmin(k: int):
    n = 2 * k
    inputs, ones_mask = truth_mask(n)
    full = (1 << len(inputs)) - 1
    zeros_mask = full ^ ones_mask
    pos, neg = literal_masks(n, inputs)

    t0 = time.time()
    # Enumeration des 3^n ANDs : signs in {0, +1, -1}^n
    primes = []
    for signs in itertools.product([0, 1, -1], repeat=n):
        m = full
        for i, s in enumerate(signs):
            if s == 1:
                m &= pos[i]
            elif s == -1:
                m &= neg[i]
        if m == 0:
            continue
        if m & zeros_mask:
            continue  # pas implicant
        # premier ? retirer chaque litteral doit casser l'implication
        is_prime = True
        lits = [i for i, s in enumerate(signs) if s != 0]
        for drop in lits:
            m2 = full
            for i, s in enumerate(signs):
                if i == drop or s == 0:
                    continue
                m2 &= pos[i] if s == 1 else neg[i]
            if not (m2 & zeros_mask):
                is_prime = False  # encore implicant sans ce litteral
                break
        if is_prime:
            primes.append(m)
    t_enum = time.time() - t0

    # Set cover ILP exact
    t0 = time.time()
    one_indices = [idx for idx in range(len(inputs)) if (ones_mask >> idx) & 1]
    prob = pulp.LpProblem("dnfmin", pulp.LpMinimize)
    x = [pulp.LpVariable(f"x{i}", cat="Binary") for i in range(len(primes))]
    prob += pulp.lpSum(x)
    for idx in one_indices:
        covering = [x[i] for i in range(len(primes)) if (primes[i] >> idx) & 1]
        prob += pulp.lpSum(covering) >= 1
    status = prob.solve(pulp.PULP_CBC_CMD(msg=False, timeLimit=600))
    dnf_min = round(pulp.value(prob.objective))
    t_ilp = time.time() - t0
    return len(primes), dnf_min, pulp.LpStatus[status], t_enum, t_ilp


# ------------------------------------------- (B) dual symetrise verifie

def orbit(z: tuple[int, ...]) -> tuple[int, int, int]:
    k = len(z) // 2
    a = sum(1 for i in range(k) if z[i] == 1 and z[i + k] == 1)
    b = sum(1 for i in range(k) if z[i] != z[i + k])
    return (a, b, k - a - b)


def dual_certificate_check(k: int):
    n = 2 * k
    monos = []
    for d in range(n + 1):
        monos.extend(itertools.combinations(range(n), d))
    prob = pulp.LpProblem("lp", pulp.LpMinimize)
    c = [pulp.LpVariable(f"c{i}") for i in range(len(monos))]
    a = [pulp.LpVariable(f"a{i}", lowBound=0) for i in range(len(monos))]
    for i in range(len(monos)):
        prob += a[i] >= c[i]
        prob += a[i] >= -c[i]
    prob += pulp.lpSum(a)
    inputs = list(itertools.product([0, 1], repeat=n))
    for idx, z in enumerate(inputs):
        s = pulp.lpSum(c[i] for i in range(len(monos))
                       if all(z[j] for j in monos[i]))
        if ip_val(z) == 1:
            prob += (s >= 1), f"in_{idx}"
        else:
            prob += (s <= 0), f"in_{idx}"
    prob.solve(pulp.PULP_CBC_CMD(msg=False, timeLimit=600))
    lp_val = pulp.value(prob.objective)

    # symetrisation des duaux
    s1, c1 = defaultdict(float), defaultdict(int)
    s0, c0 = defaultdict(float), defaultdict(int)
    for idx, z in enumerate(inputs):
        pi = prob.constraints[f"in_{idx}"].pi or 0.0
        o = orbit(z)
        if ip_val(z) == 1:
            s1[o] += pi
            c1[o] += 1
        else:
            s0[o] += pi
            c0[o] += 1
    u = {o: s1[o] / c1[o] for o in s1}
    v = {o: -s0[o] / c0[o] for o in s0}

    # verification independante : tous les moments
    uz = {z: u.get(orbit(z), 0.0) for z in inputs if ip_val(z) == 1}
    vz = {z: v.get(orbit(z), 0.0) for z in inputs if ip_val(z) == 0}
    total_u = sum(uz.values())
    worst = 0.0
    neg_weight = min([0.0] + list(uz.values()) + list(vz.values()))
    for S in monos:
        mu = 0.0
        for z in inputs:
            if all(z[j] for j in S):
                mu += uz.get(z, 0.0) if ip_val(z) == 1 else -vz.get(z, 0.0)
        worst = max(worst, abs(mu))
    return lp_val, total_u, worst, neg_weight


def main() -> None:
    print("TACHE F-005b -- verifications approfondies k=4 et k=5")
    print("=" * 76)

    print("\n(A) Primes + DNF_min par enumeration directe (jamais fait a k=5)")
    print("-" * 76)
    for k in [4, 5]:
        target = (3 ** k - 1) // 2
        np_, dm, st, te, ti = primes_and_dnfmin(k)
        ok = (np_ == target and dm == target and st == "Optimal")
        print(f"  k={k} (n={2*k}, 3^{2*k} = {3**(2*k)} ANDs) :")
        print(f"    |primes(IP)| = {np_}   (prediction Tour 18 : {target})")
        print(f"    DNF_min      = {dm}   (statut {st})   (prediction : {target})")
        print(f"    [{'CONFIRME' if ok else '*** DISCORDANCE ***'}]"
              f"   (enum {te:.1f}s, ILP {ti:.1f}s)")

    print("\n(B) Certificat dual symetrise, verification independante")
    print("-" * 76)
    for k in [4, 5]:
        target = (3 ** k - 1) / 2
        lp_val, total_u, worst, negw = dual_certificate_check(k)
        ok = (abs(lp_val - target) < 1e-5 and abs(total_u - target) < 1e-5
              and worst <= 1 + 1e-6 and negw >= -1e-9)
        print(f"  k={k} : LP = {lp_val:.6f} ; valeur du dual symetrise = {total_u:.6f} ;")
        print(f"         max |mu(S)| = {worst:.8f} ; poids min = {negw:.2e}")
        print(f"         [{'CERTIFICAT VALIDE' if ok else '*** PROBLEME ***'}]   (cible {target})")


if __name__ == "__main__":
    main()
