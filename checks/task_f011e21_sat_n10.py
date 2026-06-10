"""
TACHE F-011, etape 21 -- Trancher deg_6(MAJ_10) = 5 ? par SAT (CaDiCaL).

L'instance ouverte de l'etape 20 (recuit cale a 27, ILP timeout).
Question : existe-t-il P sur Z_6, multilineaire, supporte sur les 252
monomes de taille 5 (Lemme 5), avec P(S) != 0 mod 6 pour tout |S| >= 5 ?

ENCODAGE :
 - u_T binaire (coefficient mod 2), v_T ternaire (mod 3) en 2 bits
   (v1, v2) avec interdit (1,1) : v = 0/1/2 = (00)/(10)/(01) ;
 - pour chaque S (638 ensembles, |S| = 5..10) :
   * U(S) = XOR des u_T (T sous-ensemble de S, |T| = 5) -- chaine de
     Tseitin (4 clauses par pas) ;
   * V(S) = somme des v_T mod 3 -- chaine d'etats 2 bits (transitions
     s' = s + v mod 3, 18 clauses par pas) ;
   * couverture : clause (U_S ou s1_S ou s2_S).
 - SAT -> certificat, verification exhaustive sur les 1024 points ;
   UNSAT -> deg_6(MAJ_10) >= 6 : l'hypothese plate est REFUTEE a n = 10.
"""

from __future__ import annotations

import itertools
import time

from pysat.solvers import Cadical153


class CNF:
    def __init__(self):
        self.nv = 0
        self.clauses = []

    def new(self):
        self.nv += 1
        return self.nv

    def add(self, cl):
        self.clauses.append(cl)


def xor_gate(cnf, x, y):
    z = cnf.new()
    cnf.add([-x, -y, -z])
    cnf.add([x, y, -z])
    cnf.add([x, -y, z])
    cnf.add([-x, y, z])
    return z


def mod3_step(cnf, s1, s2, v1, v2):
    """ (s1', s2') = etat s + valeur v mod 3, encodage 0=(00) 1=(10) 2=(01). """
    t1, t2 = cnf.new(), cnf.new()
    table = {}
    for s in range(3):
        for v in range(3):
            table[(s, v)] = (s + v) % 3
    bits = {0: (0, 0), 1: (1, 0), 2: (0, 1)}
    for (s, v), r in table.items():
        sb, vb, rb = bits[s], bits[v], bits[r]
        ante = []
        ante.append(s1 if sb[0] else -s1)
        ante.append(s2 if sb[1] else -s2)
        ante.append(v1 if vb[0] else -v1)
        ante.append(v2 if vb[1] else -v2)
        # ante -> t1 = rb[0], t2 = rb[1]
        cnf.add([-l for l in ante] + [t1 if rb[0] else -t1])
        cnf.add([-l for l in ante] + [t2 if rb[1] else -t2])
    return t1, t2


def build(n=10):
    t = (n + 1) // 2
    monos = list(itertools.combinations(range(n), t))
    idx = {T: i for i, T in enumerate(monos)}
    cnf = CNF()
    u = [cnf.new() for _ in monos]
    v1 = [cnf.new() for _ in monos]
    v2 = [cnf.new() for _ in monos]
    for i in range(len(monos)):
        cnf.add([-v1[i], -v2[i]])          # v != (1,1)
    for w in range(t, n + 1):
        for S in itertools.combinations(range(n), w):
            subs = [idx[T] for T in itertools.combinations(S, t)]
            # chaine XOR
            ux = u[subs[0]]
            for j in subs[1:]:
                ux = xor_gate(cnf, ux, u[j])
            # chaine mod 3
            s1, s2 = v1[subs[0]], v2[subs[0]]
            for j in subs[1:]:
                s1, s2 = mod3_step(cnf, s1, s2, v1[j], v2[j])
            cnf.add([ux, s1, s2])           # couverture
    return cnf, monos, u, v1, v2


def verify(model, monos, u, v1, v2, n=10):
    t = (n + 1) // 2
    mset = set(model)
    uu = [1 if u[i] in mset else 0 for i in range(len(monos))]
    vv = [(1 if v1[i] in mset else 0) + (2 if v2[i] in mset else 0)
          for i in range(len(monos))]
    Tsets = [frozenset(T) for T in monos]
    for x in range(1 << n):
        S = frozenset(i for i in range(n) if (x >> i) & 1)
        w = len(S)
        U = sum(c for Ts, c in zip(Tsets, uu) if Ts <= S) % 2
        V = sum(c for Ts, c in zip(Tsets, vv) if Ts <= S) % 3
        if w < t and (U or V):
            return False
        if w >= t and not (U or V):
            return False
    return True


def main() -> None:
    print("TACHE F-011 e21 -- deg_6(MAJ_n) = t ? par SAT (CaDiCaL), n = 10..13")
    print("=" * 64)
    for n in (10, 11, 12, 13):
        t = (n + 1) // 2
        t0 = time.time()
        cnf, monos, u, v1, v2 = build(n)
        print(f"\nn = {n} (t = {t}) : {cnf.nv} variables, "
              f"{len(cnf.clauses)} clauses ({time.time()-t0:.0f}s)",
              flush=True)
        solver = Cadical153(bootstrap_with=cnf.clauses)
        t0 = time.time()
        res = solver.solve()
        dt = time.time() - t0
        print(f"  resultat : {'SAT' if res else 'UNSAT'}   ({dt:.0f}s)",
              flush=True)
        if res:
            ok = verify(solver.get_model(), monos, u, v1, v2, n)
            print(f"  verification exhaustive (2^{n} points) : "
                  f"{'OK' if ok else '*** ECHEC ***'}", flush=True)
            if ok:
                print(f"  => deg_6(MAJ_{n}) = {t} : plate CONFIRMEE.")
        else:
            print(f"  => deg_6(MAJ_{n}) >= {t+1} : PLATE REFUTEE a n = {n}.")
        solver.delete()


if __name__ == "__main__":
    main()
