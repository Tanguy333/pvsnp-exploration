"""
Tour 16 -- Diversification vers la famille MOD_p (lignee Razborov-Smolensky).

THEOREME L16 (extension de Tour 12 a la famille MOD_p) :
  Pour tout p >= 2 et tout n >= 1, MOD_p_n(x) = [sum(x) ≡ 0 (mod p)] verifie :
    f^{-1}(1) est un independent set du graphe Q_n.

  Consequence (via L13 du Tour 13) :
    DNF_min(MOD_p_n) = |MOD_p_n^{-1}(1)| = sum_{k ≡ 0 mod p, 0 <= k <= n} C(n, k).

  Pour p fixe et n grand, ce nombre est ~ 2^n / p, super-polynomial.
  Donc MOD_p_n ∉ AC^0 d=2 polynomial pour tout p >= 2.

CAS PARTICULIERS :
  - p = 2 : MOD_2 = PARITY (Tour 12 ; DNF_min = 2^(n-1)).
  - p = 3 : MOD_3, nouveau theoreme du Tour 16.
  - p = n+1 : reduit a AND_n + 1 trivial.

PREUVE DE L'INDEPENDENT SET (L16.1) :
  Soient x, y in {0,1}^n avec dist_H(x, y) = 1, i.e. y differe de x sur un
  unique bit. Alors sum(y) = sum(x) ± 1. Si sum(x) ≡ 0 (mod p) (donc x ∈
  MOD_p^{-1}(1)), alors sum(y) ≡ ±1 (mod p) qui n'est pas ≡ 0 sauf si p = 1
  (cas degenere exclu). Donc y ∉ MOD_p^{-1}(1).

  Par contraposition, deux affectations Hamming-voisines ne peuvent pas etre
  toutes deux dans MOD_p^{-1}(1). C'est exactement la definition d'un
  independent set du graphe du n-cube Q_n. ∎

VERIFICATION EXHAUSTIVE n=4 :
  Pour chaque p ∈ {2, 3, 4, 5} :
    - Calculer MOD_p^{-1}(1) directement.
    - Verifier qu'aucune paire dans MOD_p^{-1}(1) n'est a distance Hamming 1.
    - Verifier DNF_min(MOD_p_4) = |MOD_p^{-1}(1)| via Tour 12 / 13.
    - Comparer avec la formule sum_{k ≡ 0 mod p} C(4, k).

LIEN A P vs NP (condition (k)) :
  MOD_p_n ∈ P (calculable en O(n log p)). Pour p fixe, n grand :
    DNF_min(MOD_p_n) ~ 2^n / p, non-polynomial.
    Donc MOD_p_n ∉ AC^0 d=2 polynomial.

  Lignee Razborov-Smolensky 1987 : MOD_p ∉ AC^0[q] pour p ≠ q premiers
  (theoreme plus fort, sur profondeur constante). Notre Tour 16 etablit
  le cas profondeur 2 par calcul direct, comme premier maillon de la lignee
  RS pour le depot (les Tours 12-15 etaient la lignee FSS).

CONDITION (m) HONOREE : separation par temoin (MOD_p ∈ P \ AC^0 d=2 poly),
  pas d'affirmation sur des inclusions strictes entre classes.

NOTE METHODOLOGIQUE : ce tour applique directement L13 (Tour 13) a une
nouvelle famille de fonctions. C'est donc une consolidation/extension
plutot qu'un nouveau theoreme structurel. L'apport principal est
l'identification des MOD_p comme appartenant a la classe (a)/(b)/(c) de
L13, ce qui n'avait pas ete remarque dans Tours 13-15.
"""

from __future__ import annotations

import itertools
import math


def hamming_dist(x: int, y: int, n: int) -> int:
    return bin(x ^ y).count('1')


def is_independent_set_Qn(true_set: set[int], n: int) -> bool:
    """ Verifie qu'aucune paire de true_set n'est a distance Hamming 1. """
    for x in true_set:
        for i in range(n):
            y = x ^ (1 << i)
            if y in true_set:
                return False
    return True


def mod_p_truth_set(p: int, n: int) -> set[int]:
    """ {x in {0,1}^n : sum(x) ≡ 0 (mod p)} represente comme indices entiers. """
    result = set()
    for x in range(1 << n):
        if bin(x).count('1') % p == 0:
            result.add(x)
    return result


def expected_count(p: int, n: int) -> int:
    """ Σ_{k ≡ 0 mod p, 0 <= k <= n} C(n, k). """
    return sum(math.comb(n, k) for k in range(0, n + 1) if k % p == 0)


def main() -> None:
    n = 4
    print(f"Tour 16 -- DNF_min(MOD_p_n) pour la famille MOD_p (n={n})")
    print("=" * 78)
    print()

    print(f"  Pour chaque p ∈ {{2, 3, 4, 5}} :")
    print(f"    1. Calculer MOD_p^{{-1}}(1).")
    print(f"    2. Verifier que c'est un independent set de Q_{n}.")
    print(f"    3. Verifier DNF_min = |MOD_p^{{-1}}(1)| (par L13).")
    print(f"    4. Comparer avec la formule Σ_{{k ≡ 0 mod p}} C({n}, k).")
    print()

    print(f"  {'p':>3} | {'|MOD_p^{-1}(1)|':>16} | {'attendu':>8} | {'indep.':>7} | {'DNF_min':>8}")
    print(f"  {'-'*3} | {'-'*16} | {'-'*8} | {'-'*7} | {'-'*8}")

    all_ok = True
    for p in [2, 3, 4, 5]:
        true_set = mod_p_truth_set(p, n)
        size = len(true_set)
        exp = expected_count(p, n)
        is_indep = is_independent_set_Qn(true_set, n)
        dnf_min = size if is_indep else "?"
        size_ok = "✓" if size == exp else "✗"
        indep_ok = "✓" if is_indep else "✗"
        all_ok = all_ok and (size == exp) and is_indep
        print(f"  {p:>3} | {size:>16} | {exp:>8} {size_ok} | {indep_ok:>7} | {dnf_min:>8}")

    print()

    if not all_ok:
        print("  ECHEC : au moins un cas a echoue.")
        return

    print(f"  ✓ Pour tout p ∈ {{2, 3, 4, 5}}, MOD_p^{{-1}}(1) est independent dans Q_{n}.")
    print(f"  ✓ DNF_min(MOD_p_{n}) = sum_{{k ≡ 0 mod p}} C({n}, k) exactement.")
    print()

    # Detail des affectations pour p = 3 (cas non couvert par Tours 12-15).
    print(f"  Detail p=3 : MOD_3_{n}^{{-1}}(1) :")
    true_3 = sorted(mod_p_truth_set(3, n))
    for x in true_3:
        binary = format(x, f'0{n}b')
        s = bin(x).count('1')
        print(f"    x = {binary}  (sum = {s}, sum mod 3 = {s % 3})")
    print()

    # Verification des distances Hamming dans MOD_3_4^{-1}(1).
    print(f"  Verification : aucune paire dans MOD_3_{n}^{{-1}}(1) n'a distance Hamming 1.")
    print(f"  Distances minimales entre paires :")
    dists = []
    true_3_list = list(true_3)
    for i, x in enumerate(true_3_list):
        for y in true_3_list[i+1:]:
            dists.append(hamming_dist(x, y, n))
    print(f"    Min distance = {min(dists)} (attendu : >= 2)")
    print(f"    Max distance = {max(dists)}")
    print()

    # Synthese.
    print("=" * 78)
    print(f"THEOREME L16 ETABLI (calcul exhaustif n={n}) :")
    print(f"  Pour tout p ∈ {{2, 3, 4, 5}}, MOD_p_{n}^{{-1}}(1) est un independent set")
    print(f"  de Q_{n}, donc par L13 (Tour 13), DNF_min(MOD_p_{n}) = |MOD_p^{{-1}}(1)|.")
    print()
    print(f"  Comptes verifies :")
    for p in [2, 3, 4, 5]:
        c = len(mod_p_truth_set(p, n))
        print(f"    MOD_{p}_{n} : DNF_min = {c}")
    print()
    print(f"PREUVE GENERALE (valable tout n, tout p >= 2) :")
    print(f"  Soient x, y ∈ {{0,1}}^n a distance Hamming 1.")
    print(f"  Alors sum(y) = sum(x) ± 1, donc sum(y) ≢ sum(x) (mod p) pour p >= 2.")
    print(f"  Donc x ∈ MOD_p^{{-1}}(1) implique y ∉ MOD_p^{{-1}}(1).")
    print(f"  Donc MOD_p^{{-1}}(1) est un independent set de Q_n.")
    print(f"  Par L13 du Tour 13 : DNF_min(MOD_p_n) = |MOD_p^{{-1}}(1)|.")
    print()
    print(f"COROLLAIRE pour P vs NP :")
    print(f"  Pour p fixe et n grand : |MOD_p^{{-1}}(1)| ~ 2^n / p, non-polynomial.")
    print(f"  Donc MOD_p_n ∉ AC^0 d=2 polynomial pour tout p >= 2.")
    print()
    print(f"  Lignee : Razborov-Smolensky 1987 prouve MOD_p ∉ AC^0[q] pour p ≠ q")
    print(f"  premiers (theoreme plus fort en profondeur arbitraire). Notre Tour 16")
    print(f"  etablit le cas profondeur 2 par calcul exhaustif + L13.")
    print()
    print(f"CONDITION (m) : separation par TEMOIN (MOD_p ∈ P \\ AC^0 d=2 poly),")
    print(f"  pas d'affirmation sur des inclusions strictes.")


if __name__ == "__main__":
    main()
