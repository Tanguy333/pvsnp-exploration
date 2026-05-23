"""
Tour 22 -- REFUTATION de L20.5 a n=5 (defaut > n(n-2)).

CONTEXTE :
  L20.5 (Tour 20) : pour n >= 3, les SEULES fonctions a defaut maximal n(n-2)
                    sont les antipodales (k=2, d_H = n). Verifie n=3, 4
                    exhaustivement, conjecturee pour n >= 5.

RESULTAT INITIAL VISE :
  Cloture de L21.D (k >= 3) par cas degenere/non-degenere, transformerait
  Tour 21 en ✅ ÉTABLI complet.

RESULTAT EFFECTIF (apres execution) :
  *** CONTRE-EXEMPLE A L20.5 DETECTE A n=5 ***
  Pour k = 5, il existe 320 fonctions a defaut 17 > 15 = n(n-2). Temoin
  canonique : f^{-1}(0) = {00000, 00011, 00101, 11001, 11110}, avec
  |primes| = 25, DNF_min = 8, defaut = 17.

  Verifie INDEPENDAMMENT par algorithme Tour 19 (enumeration directe des
  3^n=243 ANDs) : concordance parfaite. Donc bug exclu, L20.5 reellement
  fausse a n=5.

CONSEQUENCES :
  - L20.5 (Tour 20, conjecturee) : REFUTEE.
  - Borne defaut(f) <= n(n-2) (Tour 21, conjecturee) : FAUSSE.
  - Tour 20 (i)-(iv) reste valide (les antipodales ont bien defaut n(n-2)),
    mais elles ne sont PAS les uniques au defaut max pour n >= 5.

CADRE :
  primes(f) = minimal hitting sets de {C(z) : z ∈ f^{-1}(0)}.
  Cela donne une enumeration directe en n^k.

CONDITIONS (a)-(p) :
  (j) verification empirique : ce script + cross-check Tour 19.
  (l) honnetete factuelle : signaler le contre-exemple clairement.
"""

from __future__ import annotations

import itertools
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


# -------------------- Outils combinatoires elementaires --------------------

def hamming_distance(a: int, b: int) -> int:
    return bin(a ^ b).count('1')


def is_antipodal(zero_set: tuple, n: int) -> bool:
    """ Z antipodal ssi |Z| = 2 et d_H = n. """
    if len(zero_set) != 2:
        return False
    a, b = zero_set
    return hamming_distance(a, b) == n


def is_coord_degenerate(zero_set: tuple, n: int) -> tuple:
    """ Z degenere ssi il existe coord j sur laquelle tous z ∈ Z agreent.
        Renvoie (degenere?, coord_j, valeur_commune). """
    if not zero_set:
        return (True, 0, 0)
    for j in range(n):
        bits = [(z >> j) & 1 for z in zero_set]
        if all(b == bits[0] for b in bits):
            return (True, j, bits[0])
    return (False, -1, -1)


# -------------------- Primes par HS minimaux --------------------

def conflict_lits_mask(z: int, n: int) -> int:
    """ C(z) encode en bitmask sur 2n litteraux.
        Litteral positif x_i -> bit 2i ; litteral negatif -x_i -> bit 2i+1.
        x_i est dans C(z) ssi z_i = 0 ; -x_i est dans C(z) ssi z_i = 1. """
    m = 0
    for i in range(n):
        if (z >> i) & 1:
            m |= 1 << (2 * i + 1)
        else:
            m |= 1 << (2 * i)
    return m


def primes_via_hitting_sets(zero_set: tuple, n: int) -> list:
    """ primes(f) = minimal hitting sets de {C(z) : z ∈ zero_set}.
        Retourne liste de tuples (s_0, ..., s_{n-1}) avec s_i ∈ {-1, 0, 1}. """
    if not zero_set:
        # f constante 1 -> unique prime = AND vide.
        return [tuple([0] * n)]

    Cz_list = [conflict_lits_mask(z, n) for z in zero_set]
    primes = []

    for size in range(1, n + 1):
        for positions in itertools.combinations(range(n), size):
            for signs in itertools.product([0, 1], repeat=size):
                lit_mask = 0
                for pos, sg in zip(positions, signs):
                    lit_mask |= 1 << (2 * pos + sg)
                # Test HS : chaque C(z) doit intersecter lit_mask.
                if any((Cz & lit_mask) == 0 for Cz in Cz_list):
                    continue
                # Test minimalite : retirer chaque litteral doit casser le HS.
                minimal = True
                for pos, sg in zip(positions, signs):
                    bit = 1 << (2 * pos + sg)
                    reduced = lit_mask ^ bit
                    if all((Cz & reduced) for Cz in Cz_list):
                        minimal = False
                        break
                if minimal:
                    signs_tuple = [0] * n
                    for pos, sg in zip(positions, signs):
                        signs_tuple[pos] = 1 if sg == 0 else -1
                    primes.append(tuple(signs_tuple))
    return primes


# -------------------- DNF_min par set cover branch-and-bound --------------------

def and_satisfies(signs: tuple, x: int) -> bool:
    for i, s in enumerate(signs):
        bit = (x >> i) & 1
        if s == 1 and bit != 1:
            return False
        if s == -1 and bit != 0:
            return False
    return True


def dnf_min_setcover(primes: list, truth_set: list) -> int:
    if not primes:
        return 0
    if not truth_set:
        return 0
    coverage = [frozenset(x for x in truth_set if and_satisfies(p, x)) for p in primes]
    target = frozenset(truth_set)
    order = sorted(range(len(primes)), key=lambda i: -len(coverage[i]))
    best = [len(primes)]

    def search(remaining, idx_pos, used):
        if not remaining:
            if used < best[0]:
                best[0] = used
            return
        if used + 1 >= best[0]:
            return
        for k in range(idx_pos, len(primes)):
            i = order[k]
            cov_inter = coverage[i] & remaining
            if cov_inter:
                search(remaining - coverage[i], k + 1, used + 1)

    search(set(truth_set), 0, 0)
    return best[0]


def defect_of_zeroset(zero_set: tuple, n: int) -> tuple:
    """ Renvoie (|primes|, DNF_min, defaut). """
    N = 1 << n
    if not zero_set:
        return (1, 1, 0)
    if len(zero_set) == N:
        return (0, 0, 0)
    truth_set = [x for x in range(N) if x not in set(zero_set)]
    primes = primes_via_hitting_sets(zero_set, n)
    dnf_min = dnf_min_setcover(primes, truth_set)
    return (len(primes), dnf_min, len(primes) - dnf_min)


# -------------------- Enumerations --------------------

def enumerate_n4_exhaustive() -> dict:
    n = 4
    N = 1 << n  # 16
    expected = n * (n - 2)
    print(f"### n={n} : enumeration exhaustive par k = |f^-1(0)| ###")
    print(f"  Defaut attendu n(n-2) = {expected}")
    print()
    print(f"  {'k':>3} | {'#zerosets':>10} | {'defmax':>6} | {'antipodales/total au max':>26}")
    print(f"  {'-'*3} | {'-'*10} | {'-'*6} | {'-'*26}")

    t0 = time.time()
    results = {}
    for k in range(1, N):
        max_def = 0
        atts: list = []
        for zs in itertools.combinations(range(N), k):
            _, _, d = defect_of_zeroset(zs, n)
            if d > max_def:
                max_def = d
                atts = [zs]
            elif d == max_def and d > 0:
                atts.append(zs)
        n_zs = math.comb(N, k)
        antip = sum(1 for zs in atts if is_antipodal(zs, n))
        results[k] = (n_zs, max_def, antip, len(atts))
        mark = ""
        if max_def == expected:
            if k == 2 and antip == len(atts):
                mark = "  (= n(n-2), tous antipodaux)"
            else:
                mark = "  *** CONTRE-EXEMPLE ***"
        print(f"  {k:>3} | {n_zs:>10} | {max_def:>6} | {antip:>11}/{len(atts):<13}{mark}")
    elapsed = time.time() - t0
    print(f"  Temps total : {elapsed:.1f}s")
    print()
    return results


def enumerate_n5_by_k(k_range) -> dict:
    n = 5
    N = 1 << n  # 32
    expected = n * (n - 2)
    print(f"### n={n} : enumeration partielle par k ∈ {list(k_range)} ###", flush=True)
    print(f"  Defaut attendu n(n-2) = {expected}", flush=True)
    print(flush=True)
    print(f"  {'k':>3} | {'#zerosets':>10} | {'defmax':>6} | {'antipodales/total au max':>26} | {'temps':>8}", flush=True)
    print(f"  {'-'*3} | {'-'*10} | {'-'*6} | {'-'*26} | {'-'*8}", flush=True)

    results = {}
    for k in k_range:
        max_def = 0
        atts: list = []
        n_zs = math.comb(N, k)
        t0 = time.time()
        for zs in itertools.combinations(range(N), k):
            _, _, d = defect_of_zeroset(zs, n)
            if d > max_def:
                max_def = d
                atts = [zs]
            elif d == max_def and d > 0:
                if len(atts) < 500:
                    atts.append(zs)
        elapsed = time.time() - t0
        antip = sum(1 for zs in atts if is_antipodal(zs, n))
        results[k] = (n_zs, max_def, antip, len(atts), elapsed)
        mark = ""
        if max_def == expected:
            if k == 2 and antip == len(atts):
                mark = "  (= n(n-2), tous antipodaux)"
            else:
                mark = "  *** CONTRE-EXEMPLE ***"
        print(f"  {k:>3} | {n_zs:>10} | {max_def:>6} | {antip:>11}/{len(atts):<13} | {elapsed:>7.1f}s{mark}", flush=True)
    print(flush=True)
    return results


# -------------------- Tests structurels --------------------

def test_l22a_degenere_recurrence(n: int = 4, samples: int = 100) -> None:
    """ L22.A (cas degenere) : si Z degenere sur coord j avec valeur v, alors
        un litteral est prime de taille 1, et f = ℓ ∨ g ou g vit sur n-1 vars
        avec |g^{-1}(0)| = |Z|. Empiriquement, defaut(f) <= (n-1)(n-3). """
    N = 1 << n
    expected_full = n * (n - 2)
    expected_recur = (n - 1) * (n - 3)
    print(f"### Test L22.A (n={n}) : cas degenere -> recurrence ###")
    print(f"  Defaut attendu n(n-2) = {expected_full}")
    print(f"  Borne recursive (n-1)(n-3) = {expected_recur}")
    print()

    import random
    rng = random.Random(42)

    max_d_observed = 0
    n_tested = 0
    for _ in range(samples):
        k = rng.randint(1, N - 1)
        zs = tuple(sorted(rng.sample(range(N), k)))
        deg, _, _ = is_coord_degenerate(zs, n)
        if not deg:
            continue
        n_tested += 1
        _, _, d = defect_of_zeroset(zs, n)
        if d > max_d_observed:
            max_d_observed = d
    print(f"  {n_tested}/{samples} echantillons degeneres testes.")
    print(f"  Defaut max observe (degenere) : {max_d_observed}")
    print(f"  Conforme borne (n-1)(n-3) = {expected_recur} ? {max_d_observed <= expected_recur}")
    print()


def test_l22a_full_n4() -> None:
    """ A n=4, enumerer tous les zero-sets degeneres et confirmer defect <=
        (n-1)(n-3) = 3. """
    n = 4
    N = 1 << n
    expected_recur = (n - 1) * (n - 3)
    print(f"### Test L22.A exhaustif n={n} : tous degeneres ###")
    max_d = 0
    counter = 0
    for k in range(1, N):
        for zs in itertools.combinations(range(N), k):
            deg, _, _ = is_coord_degenerate(zs, n)
            if not deg:
                continue
            counter += 1
            _, _, d = defect_of_zeroset(zs, n)
            if d > max_d:
                max_d = d
    print(f"  {counter} zero-sets degeneres trouves.")
    print(f"  Defaut max parmi degeneres : {max_d}")
    print(f"  Borne (n-1)(n-3) = {expected_recur} respectee ? {max_d <= expected_recur}")
    print()


# -------------------- Validation des outils sur cas connus --------------------

def validate_against_tour20(n: int = 4) -> None:
    """ Verifier que notre code reproduit Tour 20 sur les antipodales. """
    N = 1 << n
    expected_defect = n * (n - 2)
    expected_primes = n * (n - 1)
    expected_dnf = n
    print(f"### Validation : fonctions antipodales n={n} ###")
    print(f"  Attendu : |primes|={expected_primes}, DNF_min={expected_dnf}, defaut={expected_defect}")
    ok = True
    for alpha in range(N // 2):
        beta = ((1 << n) - 1) ^ alpha
        zs = tuple(sorted([alpha, beta]))
        p, d, defect = defect_of_zeroset(zs, n)
        if (p, d, defect) != (expected_primes, expected_dnf, expected_defect):
            ok = False
            print(f"  alpha={alpha:0{n}b} : (p={p}, d={d}, def={defect}) ✗")
    print(f"  Toutes conformes : {ok}")
    print()


# -------------------- Main --------------------

def cross_check_counterexample(zs: tuple, n: int) -> tuple:
    """ Verification independante via algorithme Tour 19 (enum 3^n ANDs).
        Renvoie (tour22_result, tour19_result, concordance). """
    from tour_19_primes_eq_dnfmin import compute_primes_and_dnfmin, all_ands

    # Tour 22 algorithm.
    p22, d22, df22 = defect_of_zeroset(zs, n)

    # Tour 19 algorithm.
    N = 1 << n
    full = (1 << N) - 1
    zero_mask = sum(1 << z for z in zs)
    truth_mask = full ^ zero_mask
    ands_cache = list(all_ands(n))
    p19, d19 = compute_primes_and_dnfmin(truth_mask, n, ands_cache)
    df19 = p19 - d19

    return ((p22, d22, df22), (p19, d19, df19), (p22, d22, df22) == (p19, d19, df19))


def main() -> None:
    print("Tour 22 -- Verification empirique de L20.5 / L21.D")
    print("=" * 78)
    print()

    # Validation prealable des outils.
    validate_against_tour20(n=4)

    # Etape 1 : test L22.A sur n=4 exhaustif.
    test_l22a_full_n4()

    # Etape 2 : enumeration exhaustive n=4 par k.
    r4 = enumerate_n4_exhaustive()

    # Etape 3 : enumeration partielle n=5 par k = 1..5 (k=6 ~ 2h).
    r5 = enumerate_n5_by_k(range(1, 6))

    # Synthese.
    print("=" * 78)
    print("OBSERVATIONS L21.D :")
    print()
    n4_max_k_ge_3 = max((r4[k][1] for k in r4 if k >= 3), default=-1)
    expected_n4 = 4 * 2
    print(f"  n=4 (exhaustif) : defaut max pour k >= 3 = {n4_max_k_ge_3}")
    print(f"                    cible n(n-2) = {expected_n4} ; ecart = {expected_n4 - n4_max_k_ge_3}")
    n5_max_k_ge_3 = max((r5[k][1] for k in r5 if k >= 3), default=-1)
    expected_n5 = 5 * 3
    print(f"  n=5 (k<=5)      : defaut max pour k >= 3 = {n5_max_k_ge_3}")
    print(f"                    cible n(n-2) = {expected_n5} ; ecart = {expected_n5 - n5_max_k_ge_3}")
    print()

    if n5_max_k_ge_3 > expected_n5:
        print(f"  *** CONTRE-EXEMPLE A L20.5 DETECTE A n=5 ***")
        print(f"  Defaut > n(n-2) = {expected_n5} observe.")
        print()
        # Verifier croisement avec Tour 19 sur le temoin canonique.
        zs = (0, 3, 5, 25, 30)
        print(f"  Verification croisee Tour 19 sur f^-1(0) = {zs}")
        print(f"    (binaire : {[format(z, '05b') for z in zs]})")
        t22, t19, concorde = cross_check_counterexample(zs, 5)
        print(f"    Tour 22 algo (HS minimaux) : |primes|={t22[0]} DNF_min={t22[1]} defaut={t22[2]}")
        print(f"    Tour 19 algo (3^n ANDs)    : |primes|={t19[0]} DNF_min={t19[1]} defaut={t19[2]}")
        print(f"    Concordance : {concorde}")
        if concorde and t22[2] > expected_n5:
            print(f"    => L20.5 REFUTEE INDEPENDAMMENT.")
    else:
        print(f"  L21.D verifiee empiriquement a n=4 (toutes k) et a n=5 (k <= 5).")
        print(f"  Aucun contre-exemple : seules les antipodales atteignent n(n-2).")


if __name__ == "__main__":
    main()
