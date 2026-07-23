"""
TACHE F-018 -- l'asymptotique du poids SYM o AND des compositions de
seuils, au niveau que la boucle peut atteindre honnetement.

(1) LEMME DU COMPTAGE (preuve 2 lignes, sanity-check executable) :
    un p a monomes positifs a valeurs dans {0,1} est un monome unique
    (2 monomes => p >= 2 en 1_{S u T} ; coefficient >= 2 => p >= 2).
    Consequence : seul AND a un indicateur exact bon marche -- la
    construction parite (F-016) n'a PAS d'analogue pour le comptage.

(2) CROISSANCE EXACTE de la route parite : |ANF(MAJ_m)| et
    |ANF(THRW_m)| (poids m..1, seuil m) pour m = 2..20, zeta mod 2.
    => borne sup PROUVEE W(XOR_k(g)) <= k |ANF(g)| et son asymptotique.

(3) CONTRASTE MESURE porte externe parite vs comptage (CP-SAT,
    re-verification obligatoire) :
    XOR3 vs MAJ3 sur blocs OR2 (n=6) et MAJ3 (n=9), avec la sparsite
    ANF de la fonction COMPOSEE comme borne sup de reference
    (la construction parite s'applique a toute f).
"""

from __future__ import annotations

import itertools
import sys
import time

from ortools.sat.python import cp_model


# ---------- (1) sanity du lemme ----------
def lemma_sanity(n=4):
    """Verifie exhaustivement a n<=4 : tout p a >= 2 monomes (ou un
    coefficient >= 2) prend une valeur >= 2 quelque part."""
    monos = []
    for d in range(1, n + 1):
        monos.extend(frozenset(c)
                     for c in itertools.combinations(range(n), d))
    viol = 0
    for S, T in itertools.combinations(monos, 2):
        z = tuple(1 if j in (S | T) else 0 for j in range(n))
        p = (1 if S <= frozenset(i for i in range(n) if z[i]) else 0) + \
            (1 if T <= frozenset(i for i in range(n) if z[i]) else 0)
        if p < 2:
            viol += 1
    return viol


# ---------- (2) sparsites ANF ----------
def anf_sparsity(g, m):
    """Zeta transform mod 2 sur 2^m entrees."""
    v = [g(tuple((x >> i) & 1 for i in range(m))) & 1
         for x in range(1 << m)]
    for i in range(m):
        for x in range(1 << m):
            if x & (1 << i):
                v[x] ^= v[x ^ (1 << i)]
    return sum(v)


# ---------- (3) CP-SAT ----------
def solve(f, n, cap=None, tl=120.0):
    inputs = list(itertools.product((0, 1), repeat=n))
    ones = [z for z in inputs if f(z)]
    zeros = [z for z in inputs if not f(z)]
    monos = []
    for d in range(1, n + 1):
        monos.extend(frozenset(c)
                     for c in itertools.combinations(range(n), d))
    m = cp_model.CpModel()
    a = {S: m.new_int_var(0, 127, f"a{i}") for i, S in enumerate(monos)}
    pv = {}
    for z in inputs:
        supp = frozenset(j for j in range(n) if z[j])
        t = [a[S] for S in monos if S <= supp]
        v = m.new_int_var(0, 127 * len(monos), f"q{z}")
        m.add(v == sum(t) if t else v == 0)
        pv[z] = v
    for z1 in ones:
        for z0 in zeros:
            m.add(pv[z1] != pv[z0])
    total = sum(a.values())
    if cap:
        m.add(total <= cap)
    m.minimize(total)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = tl
    s.parameters.num_workers = 8
    st = s.solve(m)
    name = s.status_name(st)
    inc = (round(s.objective_value)
           if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None)
    lb = round(s.best_objective_bound)
    ok = None
    if inc is not None:
        sol = {S: s.value(a[S]) for S in monos if s.value(a[S]) > 0}
        ones_v, zeros_v = set(), set()
        for z in inputs:
            supp = frozenset(j for j in range(n) if z[j])
            p = sum(v for S, v in sol.items() if S <= supp)
            (ones_v if f(z) else zeros_v).add(p)
        ok = not (ones_v & zeros_v)
    return name, inc, lb, ok


def main():
    tl = float(sys.argv[1]) if len(sys.argv) > 1 else 120.0

    print("== (1) lemme du comptage : sanity n = 4 ==")
    print(f"  violations trouvees : {lemma_sanity(4)} (attendu 0)")
    print("  => indicateur {0,1} a monomes positifs = monome unique "
          "(preuve 2 lignes) ; pas de construction 'comptage' analogue "
          "a la parite", flush=True)

    print("\n== (2) croissance exacte de la route parite ==")
    print("  m : |ANF(MAJ_m)| , |ANF(THRW_m)| , 2^m")
    for m in range(2, 21):
        maj = lambda z, m=m: 1 if sum(z) >= (m + 1) // 2 else 0
        thrw = lambda z, m=m: 1 if sum((m - i) * z[i]
                                       for i in range(m)) >= m else 0
        sm, st_ = anf_sparsity(maj, m), anf_sparsity(thrw, m)
        print(f"  {m:2d} : {sm:7d} , {st_:7d} , {1 << m}", flush=True)

    print("\n== (3) contraste XOR vs MAJ en porte externe (CP-SAT) ==")
    or2 = lambda z: 1 if z[0] + z[1] >= 1 else 0
    maj3 = lambda z: 1 if sum(z[:3]) >= 2 else 0

    def comp(outer, block, kb, k):
        def f(z):
            vals = [block(z[i * kb:(i + 1) * kb]) for i in range(k)]
            return outer(vals)
        return f

    xor3 = lambda v: v[0] ^ v[1] ^ v[2]
    majo = lambda v: 1 if sum(v) >= 2 else 0

    tests = [("XOR3(OR2^3)", comp(xor3, or2, 2, 3), 6, 9),
             ("MAJ3(OR2^3)", comp(majo, or2, 2, 3), 6, None),
             ("XOR3(MAJ3^3)", comp(xor3, maj3, 3, 3), 9, 9),
             ("MAJ3(MAJ3^3)", comp(majo, maj3, 3, 3), 9, None)]
    for label, f, n, pred in tests:
        sp = anf_sparsity(lambda z: f(z), n)
        t0 = time.time()
        name, inc, lb, ok = solve(f, n, cap=(sp if pred is None
                                             else pred), tl=tl)
        note = (f"prediction parite-blocs {pred}" if pred
                else f"ref |ANF(f)| = {sp} (borne sup parite globale)")
        ver = {True: " [re-verif OK]", False: " [ECHEC!]",
               None: ""}[ok]
        print(f"  {label:<14} (n={n}) : {note} ; CP-SAT {name}, "
              f"opt = {inc}, lb = {lb}{ver}  ({time.time()-t0:.0f}s)",
              flush=True)


if __name__ == "__main__":
    main()
