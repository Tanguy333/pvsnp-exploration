"""
TOUR 26 (Proposeur) -- Mecanisme #5 : INDICATEUR MODULAIRE.

Cible : dossier tours/tour_26_cible.md (Atlas ligne 7, fil F-012..022).
Modele W : poids SYM o AND (monomes positifs non vides, coefficients
entiers >= 0, ensembles de valeurs {p : f=1} et {p : f=0} DISJOINTS).

CONSTRUCTION (Theoreme U26.1) :
  Pour g monotone non-constante d'expansion multilineaire (Mobius)
  g(z) = sum_S ghat_S m_S(z) (entiers relatifs, ghat_vide = 0 car g(0)=0),
  et M = k+1, poser q_M = sum_S (ghat_S mod M) m_S : coefficients dans
  [0, M-1], et q_M(z) === g(z) (mod M) pour tout z (difference = multiple
  de M par monome).
  Alors p = sum_{i=1..k} q_M(bloc_i) === m (mod k+1), ou m = #blocs
  satisfaits, m in [0, k] : le residu determine m EXACTEMENT.
  => les ensembles de valeurs de p sur {m >= t} et {m <= t-1} sont
  disjoints pour TOUT seuil t, et meme pour TOUTE fonction externe
  symetrique de m.

  Poids : W(SYM_k(g^k)) <= k * sum_S (ghat_S mod (k+1)).
  Pour OR2 (ghat = +1,+1,-1)  : k*(1+1+k) = k(k+2).
  Pour MAJ3 (ghat = 1,1,1,-2) : k*(3+(k-1)) = k(k+2).

CE SCRIPT verifie par enumeration exhaustive :
  1. MAJ_k(OR2^k), k = 3, 5, 7  (n = 6, 10, 14)     -- poids 15, 35, 63
  2. MAJ_3(MAJ3^3)              (n = 9)              -- poids 15 (< 27 !)
  3. MAJ_3(g^3), g = x or (y and z) (n = 9)          -- poids 15
  4. XOR_5(OR2^5) avec le MEME p (generalite SYM)    -- poids 35
  5. Sanite : l'optimum connu 12 de MAJ_3(OR2^3) (12 paires croisees)
  6. Temoin negatif : l'astuce parite seule ({1,3} par bloc, mod 2)
     ECHOUE a k=5 -- collision exhibee (pourquoi M > k est necessaire).
"""

from __future__ import annotations

import itertools


# ---------------------------------------------------------------- outils

def eval_poly(sol: dict, z: tuple) -> int:
    supp = frozenset(j for j in range(len(z)) if z[j])
    return sum(v for S, v in sol.items() if S <= supp)


def check_disjoint(f, n: int, sol: dict) -> tuple:
    ones, zeros = set(), set()
    for z in itertools.product((0, 1), repeat=n):
        (ones if f(z) else zeros).add(eval_poly(sol, z))
    inter = ones & zeros
    return (not inter, sorted(ones), sorted(zeros), sorted(inter))


def weight(sol: dict) -> int:
    return sum(sol.values())


# ------------------------------------------------- constructions mod-M

def or2_block_modM(i: int, M: int) -> dict:
    """ OR2 sur bloc i (vars 2i, 2i+1) : x + y + (M-1)xy  === OR2 mod M. """
    x, y = 2 * i, 2 * i + 1
    return {frozenset([x]): 1, frozenset([y]): 1,
            frozenset([x, y]): M - 1}


def maj3_block_modM(i: int, M: int) -> dict:
    """ MAJ3 sur bloc i (vars 3i..3i+2) : xy+xz+yz+(M-2)xyz === MAJ3 mod M. """
    x, y, z = 3 * i, 3 * i + 1, 3 * i + 2
    return {frozenset([x, y]): 1, frozenset([x, z]): 1,
            frozenset([y, z]): 1, frozenset([x, y, z]): M - 2}


def g_xoryz_block_modM(i: int, M: int) -> dict:
    """ g = x or (y and z) = x + yz - xyz : mod M -> x + yz + (M-1)xyz. """
    x, y, z = 3 * i, 3 * i + 1, 3 * i + 2
    return {frozenset([x]): 1, frozenset([y, z]): 1,
            frozenset([x, y, z]): M - 1}


def merge(blocks: list) -> dict:
    sol = {}
    for b in blocks:
        for S, v in b.items():
            sol[S] = sol.get(S, 0) + v
    return sol


# ------------------------------------------------------------ fonctions

def make_maj_or2(k: int, t: int = None):
    t = t if t is not None else (k + 1) // 2
    def f(z):
        m = sum(1 for i in range(k) if z[2 * i] or z[2 * i + 1])
        return 1 if m >= t else 0
    return f, 2 * k


def make_xor_or2(k: int):
    def f(z):
        m = sum(1 for i in range(k) if z[2 * i] or z[2 * i + 1])
        return m % 2
    return f, 2 * k


def make_maj_maj3(k: int):
    t = (k + 1) // 2
    def f(z):
        m = sum(1 for i in range(k)
                if z[3 * i] + z[3 * i + 1] + z[3 * i + 2] >= 2)
        return 1 if m >= t else 0
    return f, 3 * k


def make_maj_gxyz(k: int):
    t = (k + 1) // 2
    def f(z):
        m = sum(1 for i in range(k)
                if z[3 * i] or (z[3 * i + 1] and z[3 * i + 2]))
        return 1 if m >= t else 0
    return f, 3 * k


# ----------------------------------------------------------------- main

def run(label, f, n, sol, expect_w):
    ok, ones, zeros, inter = check_disjoint(f, n, sol)
    w = weight(sol)
    status = "DISJOINT OK" if ok else f"COLLISION {inter[:6]}"
    mark = "OK" if (ok and w == expect_w) else "!!"
    print(f"  [{mark}] {label:<34} poids={w:<4} (attendu {expect_w})  "
          f"{status}")
    print(f"        valeurs f=1 : {ones[:14]}{'...' if len(ones) > 14 else ''}")
    print(f"        valeurs f=0 : {zeros[:14]}{'...' if len(zeros) > 14 else ''}")
    return ok


def main():
    print("TOUR 26 (Proposeur) -- verification de l'indicateur modulaire")
    print("=" * 74)

    all_ok = True

    # 1. MAJ_k(OR2^k), k = 3, 5, 7.
    for k in (3, 5, 7):
        M = k + 1
        f, n = make_maj_or2(k)
        sol = merge([or2_block_modM(i, M) for i in range(k)])
        all_ok &= run(f"MAJ_{k}(OR2^{k})  mod {M}", f, n, sol, k * (k + 2))

    # 2. MAJ_3(MAJ3^3).
    f, n = make_maj_maj3(3)
    sol = merge([maj3_block_modM(i, 4) for i in range(3)])
    all_ok &= run("MAJ_3(MAJ3^3)  mod 4", f, n, sol, 15)

    # 3. MAJ_3(g^3), g = x or (y and z).
    f, n = make_maj_gxyz(3)
    sol = merge([g_xoryz_block_modM(i, 4) for i in range(3)])
    all_ok &= run("MAJ_3((x|yz)^3)  mod 4", f, n, sol, 15)

    # 4. Generalite SYM : XOR_5(OR2^5) avec le meme p (mod 6).
    f, n = make_xor_or2(5)
    sol = merge([or2_block_modM(i, 6) for i in range(5)])
    all_ok &= run("XOR_5(OR2^5)  meme p mod 6", f, n, sol, 35)

    # 5. Sanite : optimum connu 12 (paires croisees) pour MAJ_3(OR2^3).
    f, n = make_maj_or2(3)
    crossed = {}
    for i, j in itertools.combinations(range(3), 2):
        for u in (2 * i, 2 * i + 1):
            for v in (2 * j, 2 * j + 1):
                crossed[frozenset([u, v])] = 1
    all_ok &= run("MAJ_3(OR2^3)  12 paires croisees", f, n, crossed, 12)

    # 5bis. Variante amelioree mod-k (M = k) : par le lemme d'annulation,
    # q s'annule sur g^-1(0) ; l'unique paire de residus en collision
    # (m=0, m=k) est separee par magnitude (p=0 vs p>=k). Poids k(k+1).
    print("  --- variante mod-k (M = k), poids k(k+1) ---")
    for k in (3, 5, 7):
        f, n = make_maj_or2(k)
        sol = merge([or2_block_modM(i, k) for i in range(k)])
        all_ok &= run(f"MAJ_{k}(OR2^{k})  mod {k}", f, n, sol, k * (k + 1))
    for k in (3, 5):
        f, n = make_maj_maj3(k)
        sol = merge([maj3_block_modM(i, k) for i in range(k)])
        all_ok &= run(f"MAJ_{k}(MAJ3^{k})  mod {k}", f, n, sol, k * (k + 1))

    # 6. Temoin negatif : parite seule ({1,3}, i.e. gamma=1) echoue a k=5.
    f, n = make_maj_or2(5)
    parity_sol = merge([{frozenset([2 * i]): 1, frozenset([2 * i + 1]): 1,
                         frozenset([2 * i, 2 * i + 1]): 1}
                        for i in range(5)])
    ok, ones, zeros, inter = check_disjoint(f, n, parity_sol)
    print(f"  [{'OK' if not ok else '!!'}] parite seule (poids 15, mod 2) : "
          f"{'COLLISION attendue trouvee : ' + str(inter[:8]) if not ok else 'inattendu : disjoint ?!'}")

    print("=" * 74)
    print(f"BILAN : {'TOUTES verifications conformes' if all_ok else 'ECHEC quelque part'}")


if __name__ == "__main__":
    main()
