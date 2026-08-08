# -*- coding: utf-8 -*-
r"""PR-002 — Contre-vérification exécutable de la candidature SRE.

Le sous-lemme de la candidature : « aucun circuit sur base
{AND, OR, NOT}, fan-in <= 2, avec au plus 4 portes, ne calcule la
parité a XOR b XOR c XOR d » (la solution unique de leur spécification
S4). Convention de la candidature : entrées et constantes 0/1
gratuites ; CHAQUE porte (y compris NOT) coûte 1 ; la sortie est une
porte.

Ce script fait DEUX choses :
1. exécute le sous-lemme tel quel (k <= 4 : SAT ou UNSAT ?) ;
2. établit le MINIMUM RÉEL de portes pour XOR_4 (et XOR_3 en
   contrôle) sous cette convention exacte, par synthèse de circuits
   CP-SAT (k = 1, 2, 3, ... jusqu'au premier SAT), témoin extrait et
   RE-VÉRIFIÉ par simulation indépendante.

Contexte d'antériorité (consigné dans le dossier) : la complexité de
XOR_n sur la base U2 (toutes les portes binaires sauf XOR/XNOR) est
classiquement 3(n-1) portes binaires (attribution : Schnorr 1974) ;
la convention de la candidature (NOT payant) peut décaler la valeur —
d'où la mesure exacte ici.
"""
import sys
import time

from ortools.sat.python import cp_model


def synthese(target, n, k, tl=300):
    """Existe-t-il un circuit de k portes {AND2, OR2, NOT} calculant
    target : {0,1}^n -> {0,1} ? Entrées + constantes gratuites, sortie
    = derniere porte. Rend (temoin | None, statut)."""
    N = 1 << n
    model = cp_model.CpModel()
    # sources d'une porte i : n entrees, 2 constantes, puis portes < i
    def srcvals(i, t):
        vals = []
        for j in range(n):
            vals.append((t >> j) & 1)
        vals += [0, 1]
        vals += [val[j][t] for j in range(i)]
        return vals
    tA, tO, tN, in1, in2, val = [], [], [], [], [], []
    for i in range(k):
        a = model.NewBoolVar(f"tA{i}")
        o = model.NewBoolVar(f"tO{i}")
        m = model.NewBoolVar(f"tN{i}")
        model.AddExactlyOne([a, o, m])
        tA.append(a); tO.append(o); tN.append(m)
        ns = n + 2 + i
        in1.append(model.NewIntVar(0, ns - 1, f"i1_{i}"))
        in2.append(model.NewIntVar(0, ns - 1, f"i2_{i}"))
        val.append([model.NewBoolVar(f"v{i}_{t}") for t in range(N)])
    for i in range(k):
        for t in range(N):
            s = srcvals(i, t)
            a1 = model.NewBoolVar(f"a1_{i}_{t}")
            a2 = model.NewBoolVar(f"a2_{i}_{t}")
            model.AddElement(in1[i], s, a1)
            model.AddElement(in2[i], s, a2)
            v = val[i][t]
            # AND
            model.Add(v <= a1).OnlyEnforceIf(tA[i])
            model.Add(v <= a2).OnlyEnforceIf(tA[i])
            model.Add(v >= a1 + a2 - 1).OnlyEnforceIf(tA[i])
            # OR
            model.Add(v >= a1).OnlyEnforceIf(tO[i])
            model.Add(v >= a2).OnlyEnforceIf(tO[i])
            model.Add(v <= a1 + a2).OnlyEnforceIf(tO[i])
            # NOT (sur in1 ; in2 force = in1 pour casser la symetrie)
            model.Add(v == 1 - a1).OnlyEnforceIf(tN[i])
        model.Add(in2[i] == in1[i]).OnlyEnforceIf(tN[i])
        # symetrie AND/OR : in1 <= in2
        model.Add(in1[i] <= in2[i]).OnlyEnforceIf(tA[i])
        model.Add(in1[i] <= in2[i]).OnlyEnforceIf(tO[i])
    for t in range(N):
        model.Add(val[k - 1][t] == ((target >> t) & 1))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tl
    solver.parameters.num_search_workers = 8
    st = solver.Solve(model)
    if st == cp_model.INFEASIBLE:
        return None, "UNSAT"
    if st != cp_model.OPTIMAL and st != cp_model.FEASIBLE:
        return None, solver.StatusName(st)
    circ = []
    for i in range(k):
        typ = "AND" if solver.Value(tA[i]) else (
            "OR" if solver.Value(tO[i]) else "NOT")
        circ.append((typ, solver.Value(in1[i]), solver.Value(in2[i])))
    return circ, "SAT"


def simule(circ, n, t):
    """Re-vérification INDÉPENDANTE du témoin."""
    s = [(t >> j) & 1 for j in range(n)] + [0, 1]
    for typ, i1, i2 in circ:
        a1, a2 = s[i1], s[i2]
        s.append(a1 & a2 if typ == "AND" else
                 (a1 | a2 if typ == "OR" else 1 - a1))
    return s[-1]


def minimum(nom, n):
    target = 0
    for t in range(1 << n):
        if bin(t).count("1") % 2 == 1:
            target |= (1 << t)
    print(f"--- {nom} (XOR_{n}, cible {target:#x}) ---")
    for k in range(1, 13):
        t0 = time.time()
        circ, st = synthese(target, n, k)
        print(f"  k = {k:2} : {st}  [{time.time() - t0:.0f}s]")
        if st == "SAT":
            for t in range(1 << n):
                assert simule(circ, n, t) == ((target >> t) & 1)
            print(f"  >>> MINIMUM = {k} portes ; temoin re-verifie sur "
                  f"les {1 << n} points :")
            noms = [f"x{j}" for j in range(n)] + ["0", "1"]
            for i, (typ, i1, i2) in enumerate(circ):
                noms.append(f"g{i}")
                print(f"      g{i} = {typ}({noms[i1]}, {noms[i2]})")
            return k
        if st not in ("SAT", "UNSAT"):
            print("  NON CONCLU — arret")
            return None


def borne12():
    """Majorant explicite : XOR_4 en 12 portes payantes (3 etages de
    4 : t1 = AND(a,b), t2 = NOT(t1), t3 = OR(a,b), out = AND(t2,t3)),
    verifie par simulation pure sur les 16 points."""
    def xor2(circ, a, b):
        circ.append(("AND", a, b)); t1 = len(circ) - 1 + 6
        circ.append(("NOT", t1, t1)); t2 = len(circ) - 1 + 6
        circ.append(("OR", a, b)); t3 = len(circ) - 1 + 6
        circ.append(("AND", t2, t3)); return len(circ) - 1 + 6
    circ = []
    u = xor2(circ, 0, 1)          # x0 xor x1
    u = xor2(circ, u, 2)          # ... xor x2
    u = xor2(circ, u, 3)          # ... xor x3
    assert len(circ) == 12
    for t in range(16):
        attendu = bin(t).count("1") % 2
        assert simule(circ, 4, t) == attendu, f"echec en {t}"
    print("BORNE SUPERIEURE : XOR_4 realise en 12 portes (3 etages de "
          "4, convention NOT payant) — verifie par simulation sur les "
          "16 points.")


if __name__ == "__main__":
    quel = sys.argv[1] if len(sys.argv) > 1 else "tout"
    if quel in ("tout", "x3"):
        minimum("controle", 3)
    if quel in ("tout", "x4"):
        k4 = minimum("le sous-lemme de la candidature", 4)
        if k4 is not None:
            print(f"\nSOUS-LEMME << aucun circuit <= 4 portes >> : "
                  f"{'VRAI (trivialement : minimum = ' + str(k4) + ')' if k4 > 4 else 'FAUX'}")
    if quel in ("tout", "borne12"):
        borne12()
