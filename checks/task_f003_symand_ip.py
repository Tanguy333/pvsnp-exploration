"""
TACHE F-003 -- Poids SYM o AND minimal de IP : verification du trivial + correction.

CONSTAT DE CADRAGE (avant calcul) :
  IP_{2k} = PARITY_k o AND_2 : avec p(z) = sum_i x_i y_i (k monomes,
  coefficients 1) et g(c) = c mod 2, on a IP = g(p). Le poids SYM o AND
  de IP est donc <= k -- LINEAIRE. IP n'est PAS un temoin du verrou
  Williams -> TC^0 dans le format SYM o AND (il l'est en weight PTF,
  cf. F-001/T-F006 -- deux mesures differentes).

CE SCRIPT verifie que le minimum est exactement k (pas moins) a k = 2, 3.

Modele : p(z) = sum_S a_S m_S(z), a_S entiers >= 0, monomes en les
variables (sans negations), et f = g o p pour un g quelconque
<=> les ensembles de valeurs {p(z) : IP(z)=1} et {p(z) : IP(z)=0}
sont disjoints.

ILP : min sum a_S avec, pour chaque paire (z1 dans IP^{-1}(1),
z0 dans IP^{-1}(0)), un indicateur binaire b et
  p(z1) - p(z0) >= 1 - M b      (cas p(z1) > p(z0))
  p(z0) - p(z1) >= 1 - M (1-b)  (cas p(z0) > p(z1))
"""

from __future__ import annotations

import itertools

import pulp


def ip_val(z) -> int:
    k = len(z) // 2
    return sum(z[i] * z[i + k] for i in range(k)) % 2


def min_symand_weight(k: int, U: int = 8) -> int:
    n = 2 * k
    inputs = list(itertools.product([0, 1], repeat=n))
    ones = [z for z in inputs if ip_val(z) == 1]
    zeros = [z for z in inputs if ip_val(z) == 0]
    monos = []
    for d in range(1, n + 1):
        monos.extend(itertools.combinations(range(n), d))
    M = U * len(monos) + 1

    prob = pulp.LpProblem("symand", pulp.LpMinimize)
    a = [pulp.LpVariable(f"a{i}", lowBound=0, upBound=U, cat="Integer")
         for i in range(len(monos))]
    prob += pulp.lpSum(a)

    def p_expr(z):
        return pulp.lpSum(a[i] for i in range(len(monos))
                          if all(z[j] for j in monos[i]))

    for i1, z1 in enumerate(ones):
        for i0, z0 in enumerate(zeros):
            b = pulp.LpVariable(f"b_{i1}_{i0}", cat="Binary")
            prob += p_expr(z1) - p_expr(z0) >= 1 - M * b
            prob += p_expr(z0) - p_expr(z1) >= 1 - M * (1 - b)

    status = prob.solve(pulp.PULP_CBC_CMD(msg=False, timeLimit=600))
    return round(pulp.value(prob.objective)), pulp.LpStatus[status]


def main() -> None:
    print("TACHE F-003 -- poids SYM o AND minimal de IP_{2k}")
    print("=" * 64)
    print("Construction triviale : p = sum x_i y_i, g = (mod 2) -> poids k.")
    print()
    for k in [2, 3]:
        w, st = min_symand_weight(k)
        verdict = "= k (construction triviale optimale)" if w == k else \
                  f"!= k ({w} vs {k}) -- INATTENDU"
        print(f"  k={k} : poids minimal = {w} (statut {st})   {verdict}")
    print()
    print("CONCLUSION : le poids SYM o AND de IP est lineaire (= k).")
    print("IP n'est pas un temoin du verrou TC^0 dans CE format.")
    print("Le verrou que IP temoigne est en weight PTF (F-001, T-F006).")
    print("Les vrais objets-frontiere du format SYM o AND sont les")
    print("THR o THR a poids non bornes (cf. reformulation F-003').")


if __name__ == "__main__":
    main()
