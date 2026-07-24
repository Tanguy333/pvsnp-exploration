"""
T26-S4, volet PREUVE : le cas des MINIMA EGAUX, forme close et
mecanisme zero-sum.

DERIVATION (a verifier ici par un chemin de code INDEPENDANT de
task_t26s4_relaxation_singleton.py — lecon F-016).

Si tous les minima valent m, les sommes de minima sur c blocs valent
c*m. Pour un ensemble C de r blocs au SOMMET et A de a blocs au
minimum (a <= t-1-r), l'etat0 a le compte r+a < t et la somme
somme_C M + a*m ; l'etat1 a le compte c >= t et la somme c*m.
L'union sur a des valeurs interdites (c-a)*m, c dans [t,k],
a dans [0, t-1-r], donne exactement la FENETRE

    somme_{i dans C} M_i  hors de  m * {r+1, r+2, ..., k}
    pour tout C de taille r <= t-1.

(L'autre sens, |B| < t <= r+a, ne donne que des valeurs <= (r-1)m,
non contraignantes car somme_C M >= 2rm.)

CONSEQUENCE ARITHMETIQUE (le mecanisme). Ecrire M_i = j_i*m + rho_i,
0 <= rho_i < m. La contrainte de taille r est active seulement si
somme_C M <= k*m ; elle dit alors : somme_{i dans C} rho_i non
congru a 0 modulo m. Donc les rho_i forment une famille SANS
SOUS-SOMME NULLE de taille <= t-1 dans Z/m — structure de type
Davenport / Erdos-Ginzburg-Ziv : si m <= t-1, un argument de sommes
prefixes fournit TOUJOURS un bloc consecutif de taille <= m de somme
nulle, donc la contrainte force somme_C M > k*m pour ce bloc, donc
un M_i > k*m/m = k. C'est la branche DENSE. La branche DEGENEREE
(m grand) est immediate : M_i >= 2m donne W >= 2km >= k(k+1) des
que m >= (k+1)/2.

Ce script verifie :
  (1) la forme close ci-dessus contre la relaxation generale
      (deux implementations independantes doivent coincider) ;
  (2) que min W sous la forme close vaut k(k+1) sur une grille
      (k, m), et affiche les optima (structure des solutions).
"""

from __future__ import annotations

import itertools
import sys

from ortools.sat.python import cp_model


def closed_form_min(k, t, m, target):
    """Chemin INDEPENDANT : enumeration explicite des sous-ensembles,
    fenetre m*{r+1..k}, aucune DP ni masque binaire."""
    model = cp_model.CpModel()
    UB = max(target + 2 * k, (k + 2) * m)
    M = [model.NewIntVar(2 * m, UB, f"M{i}") for i in range(k)]
    for i in range(k - 1):
        model.Add(M[i] <= M[i + 1])   # blocs interchangeables
    for r in range(1, t):
        window = [c * m for c in range(r + 1, k + 1)]
        for C in itertools.combinations(range(k), r):
            expr = sum(M[i] for i in C)
            for v in window:
                model.Add(expr != v)
    model.Minimize(sum(M))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 120.0
    solver.parameters.num_search_workers = 8
    st = solver.Solve(model)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return (int(solver.ObjectiveValue()),
                [solver.Value(v) for v in M],
                st == cp_model.OPTIMAL)
    return None, None, False


def main():
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    sys.path.insert(0, "checks")
    from task_t26s4_relaxation_singleton import multitop_min

    all_ok = True
    for k in range(3, kmax + 1):
        t = (k + 1) // 2
        target = k * (k + 1)
        print(f"k={k} (t={t}, cible {target})", flush=True)
        for m in range(1, k + 2):
            cf, Mcf, opt1 = closed_form_min(k, t, m, target)
            gen, Mgen, opt2 = multitop_min((m,) * k, k, t, target)
            same = (cf == gen)
            ok = same and cf is not None and cf >= target
            all_ok &= ok
            trivial = " (branche degeneree 2km>=k(k+1))" if \
                2 * k * m >= target else ""
            print(f"  m={m} : forme close = {cf}, relaxation "
                  f"generale = {gen} "
                  f"[{'CONCORDE' if same else 'DIVERGENCE !!'}] ; "
                  f"vs cible {target} : "
                  f"{'OK' if cf is not None and cf >= target else 'SOUS'}"
                  f"{trivial}", flush=True)
            if cf is not None and cf < target + 3:
                print(f"        optimum : M = {Mcf}", flush=True)
    print("VOLET MINIMA EGAUX :",
          "forme close VALIDEE et bornes >= k(k+1)" if all_ok
          else "ECHEC — divergence ou borne sous la cible")


if __name__ == "__main__":
    main()
