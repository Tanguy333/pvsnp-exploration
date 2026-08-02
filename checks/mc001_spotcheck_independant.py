# -*- coding: utf-8 -*-
"""Contre-verification independante (3e passe, F-016) de deux faits decisifs de MC-001.

Fait 1 : W(THR2_4) = 4 < 6 = couvert unilateral (zoo sur fonction MONOTONE des n=4).
Fait 2 : les masques 1776 et 748 (n=4, convention LSB) ont W = 4 et W = 6.

Methode : force brute pure (aucun solveur) — enumeration des vecteurs de
coefficients de poids total <= s sur les 15 monomes positifs non vides,
critere exact : disjonction des ensembles de valeurs.
"""
from itertools import combinations_with_replacement

n = 4
N = 1 << n
MONOMES = [S for S in range(1, N)]  # masque S = monome AND_{i in S} x_i

def valeurs(f_uns, coeffs):
    """coeffs : dict S -> a_S. Renvoie (set vals uns, set vals zeros)."""
    v1, v0 = set(), set()
    for x in range(N):
        p = 0
        for S, a in coeffs.items():
            if S & x == S:
                p += a
        (v1 if x in f_uns else v0).add(p)
    return v1, v0

def W_brute(f_uns, cap):
    """Plus petit poids total <= cap admettant une separation, sinon None."""
    for s in range(0, cap + 1):
        # multiensembles de s monomes (a_S = multiplicite) : C(15+s-1, s)
        for combo in combinations_with_replacement(MONOMES, s):
            coeffs = {}
            for S in combo:
                coeffs[S] = coeffs.get(S, 0) + 1
            v1, v0 = valeurs(f_uns, coeffs)
            if not (v1 & v0):
                return s, coeffs
    return None, None

# --- Fait 1 : THR2_4 (au moins 2 bits a 1) ---
thr2 = {x for x in range(N) if bin(x).count("1") >= 2}
uns_minimaux = [x for x in thr2 if not any((y in thr2) for y in
                [x & ~(1 << i) for i in range(n) if x >> i & 1])]
print(f"THR2_4 : {len(thr2)} uns, {len(uns_minimaux)} uns minimaux (couvert attendu 6)")
w, temoin = W_brute(thr2, 4)
print(f"W(THR2_4) = {w} (temoin {temoin})")
assert w == 4 and len(uns_minimaux) == 6

# --- Fait 2 : masques 1776 (W=4) et 748 (W=6), convention LSB ---
for masque, attendu in [(1776, 4), (748, 6)]:
    uns = {x for x in range(N) if masque >> x & 1}
    w, temoin = W_brute(uns, attendu)
    # verifier aussi qu'aucun poids < attendu ne separe (W_brute le garantit
    # par balayage croissant : le premier s qui separe est le minimum)
    print(f"masque {masque} : {len(uns)} uns, W = {w} (attendu {attendu})")
    assert w == attendu

print("SPOT-CHECK : TOUT CONFORME (3e passe independante, force brute pure)")
