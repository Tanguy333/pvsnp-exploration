"""
T27-S3 — Fermer les DEUX FENETRES restantes du Tour 26 avec le
moteur validé en T27-S2 (canal de valeurs + lex-leader), généralisé
a un bloc interne quelconque.

Cibles (Tour 26, tours/tour_26_indicateur_modulaire_survit.md) :
  * W(THR_3(OR2^4))  dans [18, 20] — 8 variables, 255 monomes ;
    la borne 20 est le separateur mod-4 (re-verifie) ; le 18 vient
    d'un run 900 s du Proposeur.
  * W(MAJ_3(MAJ3^3)) dans [4, 12] — 9 variables, 511 monomes ;
    le 12 est l'indicateur mod-3 (il bat le couvert 27 de F-021),
    le 4 est une borne inferieure faible.
Chaque cap UNSAT remonte la borne inferieure ; atteindre la borne
superieure ferme la fenetre et donne W exactement.

Moteur (identique a T27-S2, parametre) :
  - 2^(k*b) - 1 coefficients entiers >= 0, somme <= cap ;
  - canal de valeurs : cap+1 booleens z_v + une contrainte element
    par entree (au lieu des desidentites par paires) ;
  - lex-leader SOUND sur les involutions generatrices de
    G = S_k (blocs) x (S_b)^k (variables dans un bloc — licite car
    les fonctions de bloc OR et MAJ3 sont symetriques).
PROTOCOLE (lecon F-016) : pour chaque cible, CALIBRATION d'abord —
le cap egal a la borne superieure connue doit sortir SAT avec temoin
RE-VERIFIE par enumeration complete. Sans cela, on n'interprete
aucune UNSAT.
"""

from __future__ import annotations

import sys
import time

from ortools.sat.python import cp_model


class Instance:
    def __init__(self, name, k, b, gfun, t, lo, hi):
        self.name, self.k, self.b, self.t = name, k, b, t
        self.gfun, self.lo, self.hi = gfun, lo, hi
        self.nv = k * b
        self.monos = list(range(1, 1 << self.nv))
        self.midx = {m: n for n, m in enumerate(self.monos)}
        self.inputs = list(range(1 << self.nv))

    def block(self, z, i):
        return (z >> (self.b * i)) & ((1 << self.b) - 1)

    def label(self, z):
        return sum(1 for i in range(self.k)
                   if self.gfun(self.block(z, i))) >= self.t

    def value(self, z, coefs):
        v, s = 0, z
        while s:
            v += coefs[self.midx[s]]
            s = (s - 1) & z
        return v

    def verify(self, coefs, cap):
        """Re-verification INDEPENDANTE par enumeration complete."""
        if sum(coefs) > cap or any(c < 0 for c in coefs):
            return False
        ones, zeros = set(), set()
        for z in self.inputs:
            (ones if self.label(z) else zeros).add(self.value(z, coefs))
        return not (ones & zeros)

    def perms(self):
        """Involutions generatrices de S_k x (S_b)^k, en permutations
        de variables (indice var = b*bloc + position)."""
        out = []
        for i in range(self.k - 1):          # echange de deux blocs
            p = list(range(self.nv))
            for j in range(self.b):
                p[self.b * i + j] = self.b * (i + 1) + j
                p[self.b * (i + 1) + j] = self.b * i + j
            out.append(p)
        for i in range(self.k):              # transposition intra-bloc
            for j in range(self.b - 1):
                p = list(range(self.nv))
                a, c = self.b * i + j, self.b * i + j + 1
                p[a], p[c] = c, a
                out.append(p)
        return out

    def act(self, p, mask):
        out = 0
        for v in range(self.nv):
            if mask >> v & 1:
                out |= 1 << p[v]
        return out


def add_lex_leader(model, cvars, inst, p):
    pairs = [(n, inst.midx[inst.act(p, m)])
             for n, m in enumerate(inst.monos)
             if inst.midx[inst.act(p, m)] != n]
    prev = None
    for idx, (a_i, b_i) in enumerate(pairs):
        a, b = cvars[a_i], cvars[b_i]
        if prev is None:
            model.Add(a <= b)
        else:
            model.Add(a <= b).OnlyEnforceIf(prev)
        if idx == len(pairs) - 1:
            break
        eq = model.NewBoolVar("")
        model.Add(a == b).OnlyEnforceIf(eq)
        model.Add(a != b).OnlyEnforceIf(eq.Not())
        if prev is None:
            prev = eq
        else:
            both = model.NewBoolVar("")
            model.AddBoolAnd([prev, eq]).OnlyEnforceIf(both)
            model.AddBoolOr([prev.Not(), eq.Not(), both])
            prev = both


def solve(inst, cap, tl, sym=True):
    model = cp_model.CpModel()
    cvars = [model.NewIntVar(0, cap, f"c{n}")
             for n in range(len(inst.monos))]
    model.Add(sum(cvars) <= cap)
    z = [model.NewBoolVar(f"z{v}") for v in range(cap + 1)]
    for zin in inst.inputs:
        terms, s = [], zin
        while s:
            terms.append(cvars[inst.midx[s]])
            s = (s - 1) & zin
        v = model.NewIntVar(0, cap, "")
        model.Add(v == (sum(terms) if terms else 0))
        model.AddElement(v, z, 1 if inst.label(zin) else 0)
    if sym:
        for p in inst.perms():
            add_lex_leader(model, cvars, inst, p)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tl
    solver.parameters.num_search_workers = 8
    t0 = time.time()
    st = solver.Solve(model)
    dt = time.time() - t0
    if st in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        return "SAT", [solver.Value(v) for v in cvars], dt
    if st == cp_model.INFEASIBLE:
        return "UNSAT", None, dt
    return "UNKNOWN", None, dt


def run(inst, tl):
    print(f"=== {inst.name} : fenetre [{inst.lo}, {inst.hi}], "
          f"{inst.nv} variables, {len(inst.monos)} monomes",
          flush=True)
    # CALIBRATION : la borne superieure connue doit etre SAT.
    st, sol, dt = solve(inst, inst.hi, tl)
    ok = st == "SAT" and inst.verify(sol, inst.hi)
    print(f"  calibration cap={inst.hi} : {st} ({dt:.0f}s), "
          f"enumeration : {'OK' if ok else 'ECHEC'}", flush=True)
    if not ok:
        print("  MODELE SUSPECT — aucune UNSAT ne sera interpretee.",
              flush=True)
        return
    lb = inst.lo
    for cap in range(inst.lo, inst.hi):
        st, sol, dt = solve(inst, cap, tl)
        if st == "UNSAT":
            lb = cap + 1
            print(f"  cap={cap} : UNSAT ({dt:.0f}s) -> W >= {lb}",
                  flush=True)
        elif st == "SAT":
            good = inst.verify(sol, cap)
            print(f"  cap={cap} : SAT ({dt:.0f}s), enumeration : "
                  f"{'OK' if good else 'ECHEC'} -> W <= {cap} "
                  f"(la borne superieure {inst.hi} TOMBE)", flush=True)
            if good:
                nz = [(bin(inst.monos[n]), v)
                      for n, v in enumerate(sol) if v]
                print(f"    temoin : {nz}", flush=True)
            return
        else:
            print(f"  cap={cap} : UNKNOWN (budget {dt:.0f}s) — "
                  f"echelle arretee, W dans [{lb}, {inst.hi}]",
                  flush=True)
            return
    print(f"  ==> FENETRE FERMEE : W({inst.name}) = {inst.hi}",
          flush=True)


def main():
    tl = float(sys.argv[1]) if len(sys.argv) > 1 else 300.0
    which = sys.argv[2] if len(sys.argv) > 2 else "both"
    insts = []
    if which in ("both", "thr"):
        insts.append(Instance("THR_3(OR2^4)", 4, 2,
                              lambda m: m != 0, 3, 18, 20))
    if which in ("both", "maj"):
        insts.append(Instance("MAJ_3(MAJ3^3)", 3, 3,
                              lambda m: bin(m).count("1") >= 2,
                              2, 4, 12))
    for inst in insts:
        run(inst, tl)


if __name__ == "__main__":
    main()
