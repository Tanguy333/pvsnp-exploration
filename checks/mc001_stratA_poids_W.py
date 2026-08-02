"""MC-001, strategie A — etape 2 : QUE VAUT W (poids SYM-AND du depot, convention
A-013 : monomes positifs non vides, coefficients entiers >= 0, ensembles de
valeurs disjoints) sur la matrice f_G de Jiang-Ravikumar indexee en binaire ?

Question posee par la strategie : W(f_G) = chi_1(f_G) ? (le couvert unilateral
gagne-t-il sur ces instances ?)

Trois mesures, chacune re-verifiee par enumeration independante :
  (1) W exact de f_G(K2) sous l'indexation binaire naturelle (lignes = bits
      hauts, colonnes = bits bas ; colonne 7 = bourrage, valeur 0) ;
  (2) enumeration des IMPLICANTS POSITIFS de f_G : un monome S est un implicant
      ssi TOUT y >= S (dans l'ordre des sous-ensembles sur {0,1}^m entier) est
      un un. S'il n'y en a AUCUN, les strata unilateral et {0,1} de W sont
      VIDES (aucun couvert, aucune partition par up-cubes n'existe) — le
      mecanisme analogue a chi_1 n'est pas disponible du tout ;
  (3) dependance a l'encodage : W recalcule sous 3 permutations aleatoires
      (seedees) des etiquettes de lignes/colonnes — chi_1 est invariant par
      permutation, W ne l'est a priori pas.
"""

from __future__ import annotations

import random
import sys
import time

from ortools.sat.python import cp_model

from mc001_stratA_jr_gadget import build_fG, kappa


# ------------------------------------------------------------------ encodage
def encode(M, perm_r=None, perm_c=None):
    """Table de verite f sur m = rb+cb bits ; ligne r -> bits hauts,
    colonne c -> bits bas ; hors matrice -> 0."""
    R, C = len(M), len(M[0])
    rb = max(1, (R - 1).bit_length())
    cb = max(1, (C - 1).bit_length())
    perm_r = perm_r or list(range(R))
    perm_c = perm_c or list(range(C))
    m = rb + cb
    f = [0] * (1 << m)
    for r in range(R):
        for c in range(C):
            if M[r][c]:
                f[(perm_r[r] << cb) | perm_c[c]] = 1
    return f, m, rb, cb


# ------------------------------------------------------------------- W exact
def W_exact(f, m, cap=None, tl=600.0):
    """min somme a_S (monomes positifs non vides, a_S >= 0 entiers,
    valeurs des uns et des zeros disjointes). Version minimisation directe ;
    exige OPTIMAL ; re-verifie par enumeration independante."""
    N = 1 << m
    if cap is None:
        cap = N - 1          # borne du temoin injectif (appartenance NP, acquise)
    model = cp_model.CpModel()
    a = [model.NewIntVar(0, cap, f"a{S}") for S in range(1, N)]
    tot = model.NewIntVar(0, cap, "tot")
    model.Add(tot == sum(a))
    z = [model.NewBoolVar(f"z{v}") for v in range(cap + 1)]
    for e in range(N):
        expr = [a[S - 1] for S in range(1, N) if (e & S) == S]
        v = model.NewIntVar(0, cap, f"v{e}")
        model.Add(v == (sum(expr) if expr else 0))
        model.AddElement(v, z, 1 if f[e] else 0)
    model.Minimize(tot)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tl
    solver.parameters.num_search_workers = 8
    st = solver.Solve(model)
    if st != cp_model.OPTIMAL:
        return None, f"statut={solver.StatusName(st)}", None
    sol = {S: solver.Value(a[S - 1]) for S in range(1, N) if solver.Value(a[S - 1])}
    # re-verification independante
    uns, zeros = set(), set()
    for e in range(N):
        val = sum(cS for S, cS in sol.items() if (e & S) == S)
        (uns if f[e] else zeros).add(val)
    if uns & zeros:
        return None, "ECHEC DE RE-VERIFICATION", None
    return int(solver.ObjectiveValue()), sol, (sorted(uns), sorted(zeros))


# -------------------------------------------------------- implicants positifs
def implicants_positifs(f, m):
    """Tous les S non vides tels que le up-cube {y : y >= S} est tout-uns."""
    N = 1 << m
    out = []
    for S in range(1, N):
        comp = (N - 1) ^ S
        ok = True
        T = comp
        while True:                      # enumere les sur-ensembles de S
            if not f[S | T]:
                ok = False
                break
            if T == 0:
                break
            T = (T - 1) & comp
        if ok:
            out.append(S)
    return out


# ---------------------------------------------------------------------- main
def main():
    n, edges = 2, [(1, 2)]
    M = build_fG(n, edges)
    k = kappa(n, edges)
    chi1_formule = n + 4 * len(edges) + k
    R, C = len(M), len(M[0])
    print(f"=== f_G(K2) : matrice {R}x{C}, chi_1 = {chi1_formule} (formule "
          f"JR validee par ailleurs) ===", flush=True)

    # (1) encodage naturel
    f, m, rb, cb = encode(M)
    uns = sum(f)
    print(f"\n(1) encodage naturel : m = {rb}+{cb} = {m} variables, "
          f"N = {1 << m}, {uns} uns, f(1^m) = {f[-1]}", flush=True)
    t0 = time.time()
    W, sol, valeurs = W_exact(f, m, tl=600.0)
    if W is None:
        print(f"    W NON CONCLU : {sol}", flush=True)
    else:
        print(f"    W(f_G) = {W}   (OPTIMAL, re-verifie ; {time.time()-t0:.0f}s)",
              flush=True)
        print(f"    chi_1  = {chi1_formule}   ->  W {'=' if W == chi1_formule else '!='} chi_1",
              flush=True)
        print(f"    solution : {{S (bits r|c) : coeff}} = "
              f"{{{', '.join(f'{S:0{m}b}:{c}' for S, c in sorted(sol.items()))}}}",
              flush=True)
        print(f"    valeurs des uns   : {valeurs[0]}", flush=True)
        print(f"    valeurs des zeros : {valeurs[1]}", flush=True)

    # (2) implicants positifs
    imps = implicants_positifs(f, m)
    print(f"\n(2) implicants positifs de f_G(K2) : {len(imps)} "
          f"{'-> strata unilateral et {0,1} VIDES' if not imps else imps}",
          flush=True)

    # (3) dependance a l'encodage
    print(f"\n(3) W sous permutations des etiquettes (chi_1 invariant = "
          f"{chi1_formule}) :", flush=True)
    for seed in (1, 2, 3):
        rng = random.Random(seed)
        pr = list(range(R)); rng.shuffle(pr)
        pc = list(range(C)); rng.shuffle(pc)
        fp, mp, _, _ = encode(M, pr, pc)
        t0 = time.time()
        Wp, solp, _ = W_exact(fp, mp, tl=600.0)
        ip = len(implicants_positifs(fp, mp))
        if Wp is None:
            print(f"    seed {seed} : NON CONCLU ({solp})", flush=True)
        else:
            print(f"    seed {seed} : W = {Wp}  (implicants : {ip} ; "
                  f"{time.time()-t0:.0f}s)", flush=True)


if __name__ == "__main__":
    main()
