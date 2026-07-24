"""
T27-S2 — L'ESPACE ENTIER : borne inferieure sur le VRAI W(MAJ_5(OR2^5))
par echelle de caps CP-SAT.

Generalisation du moteur v4 de T27-S1 (canal de valeurs + lex-leader)
a l'espace COMPLET des monomes : les 1023 sous-ensembles non vides des
10 variables, coefficients entiers >= 0. Plus aucune restriction de
classe : chaque cap UNSAT est une borne inferieure NEUVE sur le vrai
W(MAJ_5(OR2^5)) — etat de l'art : >= 20 (Tour 26, restriction L26.5 +
certificat THR_2(OR2^4) = 20 optimal). Une echelle complete jusqu'a
29 fermerait « decomposable => global » a k = 5 (fenetre [20, 30]).

Modele :
  - 1023 variables c_S in [0, cap], somme <= cap ;
  - 1024 entrees z in {0,1}^10 ; monome S actif ssi S est un
    sous-masque de z ; val(z) = somme des c_S actifs, dans [0, cap] ;
  - canal de valeurs : booleen z_v par valeur, element
    z[val(z)] = [m(z) >= 3] ou m(z) = # blocs avec OR2 = 1 ;
  - lex-leader sur les 9 involutions generatrices de
    G = S_5 x S_2^5 agissant sur les 1023 coordonnees (sound :
    representant lex-minimal d'orbite).
Triangulation (lecon F-016) : cap 30 SAT attendu (decomposable
(1,1,4)^5 en hint, re-verifie par enumeration) ; cap 19 UNSAT attendu
(theoreme du Tour 26 = etalon d'infaisabilite pleine-generalite).

Usage : python tour_27_s2_espace_entier_cpsat.py [cap budget]...
  sans argument : sonde (30 sanity, 19 etalon, 20 premier barreau neuf)
  avec paires cap/budget : barreaux a la demande (echelle continuee).
"""

from __future__ import annotations

import sys
import time

from ortools.sat.python import cp_model

K, T, NV = 5, 3, 10  # variables : bit 2i = x_i, bit 2i+1 = y_i
MONOS = list(range(1, 1 << NV))          # 1023 masques non vides
MIDX = {m: n for n, m in enumerate(MONOS)}
INPUTS = list(range(1 << NV))            # 1024 entrees


def set_k(k):
    """Reparametre le module pour MAJ_k(OR2^k) (t = ceil(k/2)).
    k = 5 (defaut) = l'instance de T27-S2 : chemin inchange."""
    global K, T, NV, MONOS, MIDX, INPUTS
    K, T, NV = k, (k + 1) // 2, 2 * k
    MONOS = list(range(1, 1 << NV))
    MIDX = {m: n for n, m in enumerate(MONOS)}
    INPUTS = list(range(1 << NV))


def nblocs(z):
    return sum(1 for i in range(K) if (z >> (2 * i)) & 3)


def value(z, coefs):
    v, s = 0, z
    while s:
        v += coefs[MIDX[s]]
        s = (s - 1) & z
    return v


def verify(coefs, cap):
    """Re-verification INDEPENDANTE par enumeration complete."""
    if sum(coefs) > cap or any(c < 0 for c in coefs):
        return False
    ones, zeros = set(), set()
    for z in INPUTS:
        (ones if nblocs(z) >= T else zeros).add(value(z, coefs))
    return not (ones & zeros)


# ---- involutions generatrices de G sur les masques de monomes ----

def generators():
    gens = []
    ident = tuple(range(K))
    for i in range(K):
        gens.append((ident, tuple(1 if a == i else 0 for a in range(K))))
    for i in range(K - 1):
        p = list(range(K))
        p[i], p[i + 1] = p[i + 1], p[i]
        gens.append((tuple(p), (0,) * K))
    return gens


def act_mask(perm, swaps, mask):
    out = 0
    for i in range(K):
        for v in (0, 1):
            if mask & (1 << (2 * i + v)):
                out |= 1 << (2 * perm[i] + (v ^ swaps[i]))
    return out


def add_lex_leader(model, cvars, perm, swaps):
    pairs = [(t, MIDX[act_mask(perm, swaps, m)])
             for t, m in enumerate(MONOS)
             if MIDX[act_mask(perm, swaps, m)] != t]
    prev = None
    for idx, (t, u) in enumerate(pairs):
        a, b = cvars[t], cvars[u]
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


def solve(cap, tl, hint=None, sym=True):
    model = cp_model.CpModel()
    cvars = [model.NewIntVar(0, cap, f"c{n}")
             for n in range(len(MONOS))]
    model.Add(sum(cvars) <= cap)

    z = [model.NewBoolVar(f"z{v}") for v in range(cap + 1)]
    for zin in INPUTS:
        terms, s = [], zin
        while s:
            terms.append(cvars[MIDX[s]])
            s = (s - 1) & zin
        v = model.NewIntVar(0, cap, "")
        model.Add(v == (sum(terms) if terms else 0))
        model.AddElement(v, z, 1 if nblocs(zin) >= T else 0)

    if sym:
        for perm, swaps in generators():
            add_lex_leader(model, cvars, perm, swaps)

    if hint is not None:
        for var, h in zip(cvars, hint):
            model.AddHint(var, h)

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


def hint_dec114():
    h = [0] * len(MONOS)
    for i in range(K):
        h[MIDX[1 << (2 * i)]] = 1          # x_i
        h[MIDX[1 << (2 * i + 1)]] = 1      # y_i
        h[MIDX[3 << (2 * i)]] = 4          # x_i y_i
    return h


def report(cap, st, sol, dt):
    if st == "SAT":
        ok = verify(sol, cap)
        print(f"cap={cap} : SAT ({dt:.0f}s), enumeration : "
              f"{'OK' if ok else 'ECHEC'}", flush=True)
        if ok and cap <= 29:
            nz = [(bin(MONOS[n]), v) for n, v in enumerate(sol) if v]
            print(f"  TEMOIN < 30 (poids {sum(sol)}) ! monomes : {nz}",
                  flush=True)
        return ok
    if st == "UNSAT":
        extra = " (etalon Tour 26 : attendu)" if cap <= 19 else \
                f" — THEOREME NEUF : W(MAJ_5(OR2^5)) >= {cap + 1}"
        print(f"cap={cap} : UNSAT ({dt:.0f}s){extra}", flush=True)
        return True
    print(f"cap={cap} : UNKNOWN (budget {dt:.0f}s) — barreau non "
          f"conclu.", flush=True)
    return False


def calibration():
    """ETALONNAGE BOUT-EN-BOUT sur verite terrain (durcissement de
    T27-S2 : le lex-leader n'etant pas confirmable par un second
    reglage a k = 5, on teste le moteur COMPLET la ou la reponse est
    connue independamment).
      k = 3 : W = 12 (F-021, couvert unilateral + ILP set cover)
      k = 4 : W = 20 (Tour 26, egalite certifiee)
    Attendu : cap = W-1 UNSAT, cap = W SAT (temoin enumere).
    Puis regression a k = 5 : cap 19 doit rester UNSAT."""
    ok = True
    for k, w in ((3, 12), (4, 20)):
        set_k(k)
        st, _, dt = solve(w - 1, 600.0)
        good = st == "UNSAT"
        ok &= good
        print(f"k={k} cap={w-1} : {st} ({dt:.0f}s) — attendu UNSAT "
              f"{'OK' if good else 'ECHEC'}", flush=True)
        st, sol, dt = solve(w, 600.0)
        good = st == "SAT" and verify(sol, w)
        ok &= good
        print(f"k={k} cap={w} : {st} ({dt:.0f}s), enumeration : "
              f"{'OK' if good else 'ECHEC'} — attendu SAT", flush=True)
    set_k(5)
    st, _, dt = solve(19, 300.0)
    good = st == "UNSAT"
    ok &= good
    print(f"k=5 cap=19 (regression) : {st} ({dt:.0f}s) "
          f"{'OK' if good else 'ECHEC'}", flush=True)
    print("ETALONNAGE :", "MOTEUR VALIDE sur verite terrain" if ok
          else "ECHEC — le moteur ou le lex-leader est SUSPECT")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "calib":
        calibration()
        return
    if len(sys.argv) > 1:  # paires cap budget
        args = list(map(float, sys.argv[1:]))
        for cap, tl in zip(args[::2], args[1::2]):
            st, sol, dt = solve(int(cap), tl)
            if not report(int(cap), st, sol, dt):
                break
        return

    # sonde par defaut
    st, sol, dt = solve(30, 90.0, hint=hint_dec114())
    if not report(30, st, sol, dt):
        print("MODELE SUSPECT — arret.", flush=True)
        return
    st, sol, dt = solve(19, 180.0)
    if st != "UNSAT":
        report(19, st, sol, dt)
        print("Etalon non conclu — echelle neuve non lancee.",
              flush=True)
        return
    report(19, st, None, dt)
    st, sol, dt = solve(20, 240.0)
    report(20, st, sol, dt)


if __name__ == "__main__":
    main()
