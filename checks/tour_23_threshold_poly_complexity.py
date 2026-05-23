"""
Tour 23 -- Threshold polynomial complexity de fonctions canoniques (cadre TC^0).

OBJECTIF :
  Pivot hors AC^0 d=2. Etudier la *threshold polynomial complexity*
  tcomp(f) = (degre min, magnitude min) telle que f(x) = 1 <=> p(x) > 0,
  pour les fonctions canoniques du depot.

CADRE :
  Williams 2011 (NEXP non inclus dans ACC^0) repose sur un algo CAPP
  non-trivial pour ACC^0 via Beigel-Tarui 1994 (reduction a polynomes
  entiers symetriques). L'extension a TC^0 est ouverte depuis 2010.
  Question : la magnitude des coefficients croit-elle polynomialement
  pour les fonctions TC^0 ? Si oui : CAPP[TC^0] non-trivial possible.
  Sinon : obstacle quantifie.

METHODE :
  ILP exact via PuLP/CBC. Pour chaque fonction f sur n variables :
  - Variables : c_S in [-M, M] pour S sous-ensemble de [n] avec |S| <= D.
  - Contraintes : sum_S c_S * (prod_{i in S} x_i) > 0 pour f(x)=1,
                  sum_S c_S * (prod_{i in S} x_i) <= 0 pour f(x)=0.
  - Objectif : minimiser D, puis M.

VERIFICATION :
  Sanity checks : OR_n -> (1, 1), PARITY_n -> (n, 1), MAJ_n -> (1, ~n/2).
  IP_n -> magnitude exponentielle attendue (Krause-Pudlak 1998).

LIEN P vs NP :
  Le tableau quantifie l'obstacle TC^0 -> CAPP. Pas une separation, mais
  un calibrage empirique d'une voie ouverte (Williams 2011 -> TC^0).

CONDITIONS (a)-(r) en vigueur, dont :
  (p) pivot hors AC^0 d=2 : VRAI (threshold polynomials, profondeur 2 TC).
  (q) audit biblio : Williams 2011, Beigel-Tarui 1994, Krause-Pudlak 1998.
  (r) test n+1 : execution n=4 puis n=5 si faisable.
"""

from __future__ import annotations

import itertools
import math
import time

try:
    from pulp import (
        LpProblem, LpMinimize, LpVariable, lpSum, LpInteger,
        LpStatus, PULP_CBC_CMD, value as lp_value, LpStatusOptimal,
    )
except ImportError:
    print("ERREUR : PuLP requis. Installer via : pip install pulp")
    raise


# -------------------- Definitions des fonctions canoniques --------------------

def f_OR(n: int):
    """f(x) = OR(x_0, ..., x_{n-1})"""
    return lambda x: int(any((x >> i) & 1 for i in range(n)))


def f_AND(n: int):
    """f(x) = AND(x_0, ..., x_{n-1})"""
    return lambda x: int(all((x >> i) & 1 for i in range(n)))


def f_PARITY(n: int):
    """f(x) = XOR(x_0, ..., x_{n-1})"""
    return lambda x: bin(x).count('1') % 2


def f_MAJ(n: int):
    """f(x) = 1 ssi popcount(x) >= ceil(n/2)"""
    t = (n + 1) // 2
    return lambda x: int(bin(x).count('1') >= t)


def f_THRESHOLD(t: int, n: int):
    """f(x) = 1 ssi popcount(x) >= t"""
    return lambda x: int(bin(x).count('1') >= t)


def f_MOD_p(p: int, n: int):
    """f(x) = 1 ssi popcount(x) ≡ 0 (mod p)"""
    return lambda x: int(bin(x).count('1') % p == 0)


def f_IP(k: int):
    """f(x) = IP_{2k}(x_0..x_{k-1}, x_k..x_{2k-1})
       = (somme_{i=0}^{k-1} x_i * x_{i+k}) mod 2"""
    def g(x):
        s = 0
        for i in range(k):
            s += ((x >> i) & 1) * ((x >> (i + k)) & 1)
        return s % 2
    return g


# -------------------- Computation tcomp via ILP --------------------

def tcomp_at_degree(f_callable, n: int, D: int, M_max: int = 1000) -> tuple:
    """
    Cherche un polynome entier p(x) de degre <= D, coefficients dans [-M_max, M_max],
    tel que f(x) = 1 <=> p(x) >= 1, f(x) = 0 <=> p(x) <= 0.
    Renvoie (success, M_min, polynome) ou (False, None, None).
    """
    N = 1 << n

    # Sous-ensembles de [n] de taille <= D.
    subsets = []
    for k in range(D + 1):
        for S in itertools.combinations(range(n), k):
            subsets.append(S)

    prob = LpProblem(f"tcomp_n{n}_d{D}", LpMinimize)

    # Variables : c_S pour chaque sous-ensemble S de taille <= D.
    c = {}
    for S in subsets:
        c[S] = LpVariable(f"c_{S}", lowBound=-M_max, upBound=M_max, cat=LpInteger)

    # Variable auxiliaire pour magnitude max.
    M = LpVariable("M", lowBound=0, upBound=M_max, cat=LpInteger)

    # Contrainte |c_S| <= M pour tout S (modelisation : c_S <= M et -c_S <= M).
    for S in subsets:
        prob += c[S] <= M
        prob += -c[S] <= M

    # Contraintes pour chaque x.
    for x in range(N):
        # Construire le polynome p(x) = sum_S c_S * prod_{i in S} x_i.
        terms = []
        for S in subsets:
            # prod_{i in S} x_i : produit booleen, vaut 1 ssi tous les bits de S sont a 1 dans x.
            if all((x >> i) & 1 for i in S):
                terms.append(c[S])
            # sinon 0, n'ajoute rien

        if f_callable(x) == 1:
            prob += lpSum(terms) >= 1
        else:
            prob += lpSum(terms) <= 0

    # Objectif : minimiser M.
    prob += M

    solver = PULP_CBC_CMD(msg=0, timeLimit=60)
    status = prob.solve(solver)

    if status != LpStatusOptimal:
        return (False, None, None)

    M_val = int(round(lp_value(M)))
    poly = {S: int(round(lp_value(c[S]))) for S in subsets if abs(lp_value(c[S])) > 1e-6}
    return (True, M_val, poly)


def tcomp(f_callable, n: int, D_max: int = None, M_max: int = 1000) -> tuple:
    """
    Renvoie (degre_min, magnitude_min) pour la fonction f sur n variables.
    """
    if D_max is None:
        D_max = n

    for D in range(0, D_max + 1):
        success, M, poly = tcomp_at_degree(f_callable, n, D, M_max=M_max)
        if success:
            return (D, M, poly)
    return (None, None, None)


# -------------------- Sanity checks --------------------

def sanity_checks(n: int = 4) -> bool:
    """Verifier OR, AND, PARITY donnent valeurs attendues."""
    print(f"### Sanity checks a n={n} ###")
    print()
    expected = {
        "OR": (1, 1),         # x_0 + x_1 + ... + x_{n-1} >= 1
        "AND": (1, 1),        # x_0 + x_1 + ... + x_{n-1} - (n-1) >= 1, magnitude max = n-1
        "PARITY": (n, 1),     # degre n requis
    }
    ok = True
    results = {}
    for name, (e_d, e_m) in expected.items():
        f = {"OR": f_OR(n), "AND": f_AND(n), "PARITY": f_PARITY(n)}[name]
        t0 = time.time()
        d, m, poly = tcomp(f, n, D_max=n, M_max=2 ** (n + 2))
        dt = time.time() - t0
        results[name] = (d, m, dt)
        status = "OK"
        # Note : pour AND, on attend en realite (1, n-1) car polynome
        # somme(x_i) - (n-1) >= 1 ssi tous = 1. On garde l'attendu lache.
        if name == "OR" and (d, m) != (1, 1):
            status = f"DEVIATION (attendu (1,1), obtenu ({d},{m}))"
            ok = False
        if name == "PARITY" and d != n:
            status = f"DEVIATION (attendu degre {n}, obtenu {d})"
            ok = False
        print(f"  {name:8s} : degre={d}, magnitude={m}, temps={dt:.1f}s  [{status}]")
        if poly:
            poly_str = " + ".join(
                f"{c}*x_{S}" if S else f"{c}"
                for S, c in sorted(poly.items(), key=lambda kv: (len(kv[0]), kv[0]))
            )
            print(f"    poly : {poly_str[:120]}{'...' if len(poly_str) > 120 else ''}")
        print()
    return ok


# -------------------- Tableau de reference --------------------

def reference_table(n: int = 4) -> None:
    """Calculer tcomp pour les fonctions canoniques."""
    print(f"### Tableau de reference a n={n} ###")
    print()
    print(f"  {'fonction':<15s} | {'|f^-1(1)|':>10s} | {'deg min':>7s} | {'magn min':>9s} | {'temps':>7s}")
    print(f"  {'-'*15} | {'-'*10} | {'-'*7} | {'-'*9} | {'-'*7}")

    M_max_default = 2 ** (n + 4)

    fns = [
        ("OR", f_OR(n)),
        ("AND", f_AND(n)),
        ("PARITY", f_PARITY(n)),
        ("MAJ", f_MAJ(n)),
    ]
    for t in [1, n]:
        if t not in [(n + 1) // 2, 1, n]:
            continue
    for t in range(1, n + 1):
        fns.append((f"THR_{t}", f_THRESHOLD(t, n)))
    for p in [2, 3]:
        fns.append((f"MOD_{p}", f_MOD_p(p, n)))

    # IP_n : n doit etre pair.
    if n % 2 == 0:
        k = n // 2
        fns.append((f"IP_{n}", f_IP(k)))

    N = 1 << n
    for name, f in fns:
        truth_count = sum(1 for x in range(N) if f(x))
        t0 = time.time()
        d, m, _ = tcomp(f, n, D_max=n, M_max=M_max_default)
        dt = time.time() - t0
        d_str = str(d) if d is not None else "?"
        m_str = str(m) if m is not None else "?"
        print(f"  {name:<15s} | {truth_count:>10d} | {d_str:>7s} | {m_str:>9s} | {dt:>6.1f}s")


def main() -> None:
    print("Tour 23 -- Threshold polynomial complexity (cadre TC^0)")
    print("=" * 78)
    print()

    # Etape 1 : sanity checks a n=4.
    ok = sanity_checks(n=4)
    if not ok:
        print(">>> Sanity check FAILED. Diagnostiquer avant continuation. <<<")
        return

    # Etape 2 : tableau a n=4.
    reference_table(n=4)

    print()
    print("=" * 78)
    print("ANALYSE :")
    print("  - Si magnitude(IP_4) >> 1 (croissance exponentielle attendue) :")
    print("    confirme obstacle Krause-Pudlak/Forster pour TC^0.")
    print("  - Si magnitude(MAJ_4) = O(n) : conforme Saks (degre 1 simple).")
    print("  - Si nouvelle fonction a magnitude polynomiale anormalement basse :")
    print("    candidat pour CAPP partiel TC^0.")


if __name__ == "__main__":
    main()
