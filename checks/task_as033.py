"""
TACHE AS-033 -- vers l'accumulation des deficits : LA LOI LOCALE.

Commande : prouver que les deficits mod 4 s'accumulent a taux ~3^d le
long de la recursion des tables RM (le mur complet de C13). Attaque par
le premier sous-enonce prouvable, avec critere d'arret declare :

A. LA LOI DU DEFICIT au niveau mesure (RM(1,4), 2048 cosets, AS-032) :
   - le deficit est-il constant sur les orbites S_4 ? (equivariance)
   - est-il determine par le couple de syndromes grossiers
     (sigma_Sig, sigma_Del) — ou les 4 bits mod-4 comptent-ils ?
   - caracterisation de l'ensemble a deficit nul (294 cosets) :
     combien d'orbites ? representants de poids minimal ?
   Si l'ensemble nul est propre : LEMME LOCAL (deficit >= 1/4 hors E)
   prouvable par verification finie exhaustive a ce niveau.

B. ACCUMULATION SUR DEUX NIVEAUX : le decouple double (tables n=3
   appliquees deux fois) vs la verite D(5,2,3) = 5/32 — le facteur
   d'accumulation, qui doit recouper la DP d'AS-017.
"""

from __future__ import annotations

import itertools
import sys
import time
from collections import Counter, defaultdict
from fractions import Fraction as F
from math import comb

sys.path.insert(0, "checks")
from task_as030 import full_space_form, class_min  # noqa: E402
from task_as031 import perms_action  # noqa: E402


def build_all():
    """Refait la mesure AS-032 en gardant TOUTES les donnees par coset."""
    wt4 = [bin(x).count("1") for x in range(16)]
    dl4 = [-1 if w == 2 else 0 for w in wt4]
    C4, Q4 = full_space_form(4, 1)
    r4 = len(C4)
    Ct4 = [sum(F(C4[i][k] * dl4[k], 2) for k in range(16))
           for i in range(r4)]
    wt3 = [bin(x).count("1") for x in range(8)]
    dl0 = [-1 if w == 2 else 0 for w in wt3]
    dl1 = [-1 if w == 1 else 0 for w in wt3]
    ts3 = [a + b for a, b in zip(dl0, dl1)]
    td3 = [b - a for a, b in zip(dl0, dl1)]
    tabs = {}
    for (dd, tnum, name) in [(1, ts3, "S"), (0, td3, "D")]:
        C, Q = full_space_form(3, dd)
        r = len(C)
        Ct = [sum(F(C[i][k] * tnum[k], 2) for k in range(8))
              for i in range(r)]
        table = {}
        for pi_int in range(256):
            pi = [(pi_int >> k) & 1 for k in range(8)]
            syn = tuple(sum(C[i][k] * pi[k] for k in range(8)) % 2
                        for i in range(r))
            if syn not in table:
                b = [F(sum(C[i][k] * pi[k] for k in range(8))) + Ct[i]
                     for i in range(r)]
                table[syn] = class_min(C, Q, b)
        tabs[name] = (table, C)
    tS, CS = tabs["S"]
    tD, CD = tabs["D"]
    rS, rD = len(CS), len(CD)
    data = {}
    reps = {}
    for pi_int in range(1 << 16):
        pi = [(pi_int >> k) & 1 for k in range(16)]
        syn = tuple(sum(C4[i][k] * pi[k] for k in range(16)) % 2
                    for i in range(r4))
        if syn in data:
            continue
        b = [F(sum(C4[i][k] * pi[k] for k in range(16))) + Ct4[i]
             for i in range(r4)]
        h4 = class_min(C4, Q4, b)
        pi0, pi1 = pi[:8], pi[8:]
        pip = [(a + c) % 2 for a, c in zip(pi0, pi1)]
        sS = tuple(sum(CS[i][k] * pip[k] for k in range(8)) % 2
                   for i in range(rS))
        sD = tuple(sum(CD[i][k] * pip[k] for k in range(8)) % 2
                   for i in range(rD))
        dec = F(1, 2) * tS[sS] + F(1, 2) * tD[sD]
        data[syn] = (h4 - dec, sS, sD, tS[sS], tD[sD])
        reps[syn] = pi
    return data, reps, C4, tS, tD


def main():
    print("== A. la loi du deficit (RM(1,4)) ==")
    t0 = time.time()
    data, reps, C4, tS, tD = build_all()
    r4 = len(C4)
    print(f"  donnees reconstruites : {len(data)} cosets "
          f"({time.time() - t0:.0f}s)", flush=True)

    # A1. constance sur les orbites S_4
    perms = perms_action(4)
    orbit_of = {}
    norb = 0
    viol_orb = 0
    for syn, pi in reps.items():
        if syn in orbit_of:
            continue
        norb += 1
        for m in perms:
            pi2 = [0] * 16
            for x in range(16):
                pi2[m[x]] = pi[x]
            syn2 = tuple(sum(C4[i][k] * pi2[k] for k in range(16)) % 2
                         for i in range(r4))
            orbit_of[syn2] = norb
            if data[syn2][0] != data[syn][0]:
                viol_orb += 1
    print(f"  A1. deficit constant sur les {norb} orbites S_4 : "
          f"{'OUI' if viol_orb == 0 else f'NON ({viol_orb} violations)'}")

    # A2. le deficit est-il determine par (sigma_S, sigma_D) ?
    bypair = defaultdict(set)
    for syn, (df, sS, sD, hS, hD) in data.items():
        bypair[(sS, sD)].add(df)
    multi = {k: v for k, v in bypair.items() if len(v) > 1}
    print(f"  A2. paires (sigma_S, sigma_D) : {len(bypair)} ; paires a "
          f"deficit MULTIPLE : {len(multi)} "
          f"({'les 4 bits mod 4 comptent' if multi else 'deficit = f(paire)'})")
    if multi:
        spreads = Counter(tuple(sorted(str(x) for x in v))
                          for v in multi.values())
        print(f"      eventails dans les fibres : "
              f"{dict(list(spreads.items())[:6])}")

    # A3. l'ensemble a deficit nul
    zero_orbs = sorted({orbit_of[s] for s, d in data.items()
                        if d[0] == 0})
    all_zero_orbs = []
    for o in zero_orbs:
        members = [s for s in data if orbit_of[s] == o]
        if all(data[s][0] == 0 for s in members):
            all_zero_orbs.append(o)
    n0 = sum(1 for s in data if data[s][0] == 0)
    print(f"  A3. deficit nul : {n0} cosets, dans {len(zero_orbs)} "
          f"orbites (dont {len(all_zero_orbs)} orbites entierement "
          f"nulles sur {norb})")
    # representants de poids minimal des orbites nulles
    for o in zero_orbs[:8]:
        best = None
        for s in data:
            if orbit_of[s] != o or data[s][0] != 0:
                continue
            pi = reps[s]
            # chef de coset : poids min sur le coset (echantillon : rep)
            w = sum(pi)
            if best is None or w < best[0]:
                best = (w, pi, data[s][3], data[s][4])
        w, pi, hS, hD = best
        print(f"      orbite {o} : rep poids {w}, pi = "
              f"{''.join(map(str, pi))}, (hS, hD) = ({hS}, {hD})")

    print("== B. accumulation sur deux niveaux ==")
    # verite : D(5,2,3) = 5/32. decouple niveau 1 (tables n=4) :
    # 1/2 min H2[g] + 1/2 min H1[dl] — et decouple DOUBLE : on
    # redecoupe chaque table n=4 en tables n=3 decouplees.
    # min H2^{(4)}[g] >= 1/2 min h2^{(3)}[g0+g1] + 1/2 min h1^{(3)}[g1-g0]
    wt4 = [bin(x).count("1") for x in range(16)]
    g4 = [(1 if w >= 3 else 0) + (1 if w >= 2 else 0) for w in wt4]
    g0, g1 = g4[:8], g4[8:]
    cells = {
        "H2[g] via n=3": [(2, [a + b for a, b in zip(g0, g1)]),
                          (1, [b - a for a, b in zip(g0, g1)])],
        "H1[dl] via n=3": None,  # deja fait : tS, tD
    }
    mins = {}
    for name, spec in cells.items():
        if spec is None:
            v = F(1, 2) * min(tS.values()) + F(1, 2) * min(tD.values())
        else:
            v = F(0)
            for (dd, tnum) in spec:
                C, Q = full_space_form(3, dd)
                r = len(C)
                Ct = [sum(F(C[i][k] * tnum[k], 2) for k in range(8))
                      for i in range(r)]
                best = None
                seen = set()
                for pi_int in range(256):
                    pi = [(pi_int >> k) & 1 for k in range(8)]
                    syn = tuple(sum(C[i][k] * pi[k]
                                    for k in range(8)) % 2
                                for i in range(r))
                    if syn in seen:
                        continue
                    seen.add(syn)
                    b = [F(sum(C[i][k] * pi[k] for k in range(8)))
                         + Ct[i] for i in range(r)]
                    hv = class_min(C, Q, b)
                    if best is None or hv < best:
                        best = hv
                v += F(1, 2) * best
        mins[name] = v
        print(f"  {name} : borne decouplee = {v}")
    dec2 = F(1, 2) * mins["H2[g] via n=3"] + \
        F(1, 2) * mins["H1[dl] via n=3"]
    truth = F(5, 32)
    print(f"  D(5,2,3) : verite = {truth} ; decouple 2 niveaux = {dec2} "
          f"; facteur d'accumulation = {float(truth / dec2):.3f}")


if __name__ == "__main__":
    main()
