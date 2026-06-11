"""
TACHE V-024 -- THEOREME (offset 2) : m(d, d+2) = 2 Catalan(d+1),
minimum unique +-(1-x)^{d+1}(1+x) -- la Conjecture 5 est PROUVEE sur
toute la colonne n = d+2.

THEOREME V24. Soit d >= 1, D = d+1. Dans la cellule (d, n = d+2), le
reseau est de rang 2, engendre par s0 = (1-x)^D et s1 = x(1-x)^D.
Alors le plus court vecteur est UNIQUE au signe pres :
    v = (1-x)^D (1+x),   ||v||^2 = 2 C(2D, D)/(D+1) = 2 Catalan(D).
En particulier son coefficient de tete vaut -+1 : la Conjecture 5 de
KV tient sur TOUTE la colonne offset 2 (famille infinie prouvee dans
la zone profonde).

PREUVE. Gram : <s0,s0> = <s1,s1> = A := C(2D,D) ;
<s0,s1> = -somme_j C(D,j) C(D,j-1) = -B, B := C(2D,D-1) = A.D/(D+1).
Donc Q(a,b) = ||a s0 + b s1||^2 = A(a^2+b^2) - 2B ab, et :
 (i)  Q = A(a-b)^2 + 2(A-B) ab,    avec A - B = A/(D+1) = Catalan(D) ;
 (ii) Q = A(a+b)^2 - 2(A+B) ab.
Cas ab >= 1 : par (i), Q >= 2(A-B), egalite ssi a = b et ab = 1,
  i.e. (a,b) = +-(1,1).  [a = b >= 2 donne Q >= 8(A-B).]
Cas ab = 0, (a,b) != 0 : Q >= A > 2(A-B) car 2B > A
  (<=> 2D/(D+1) > 1 <=> D > 1, vrai pour d >= 1).
Cas ab <= -1 : par (ii), Q >= 2(A+B) > 2(A-B).
Donc min Q = 2(A-B) = 2 Catalan(D), atteint exactement en +-(1,1),
c'est-a-dire v = +-(1-x)^D (1+x), de coefficient de tete -+1. QED.

VERIFICATIONS CI-DESSOUS :
 [1] identites de Gram (A, -B) pour d = 1..60 (exact) ;
 [2] A - B = Catalan(D) et 2B > A pour d = 1..60 ;
 [3] croisement avec le SVP exact (minimum ET unicite) pour un
     echantillon de d ;
 [4] balayage brut de Q sur (a,b) in [-10,10]^2 pour d = 1..30 :
     le minimum est bien en +-(1,1).
"""

from __future__ import annotations

from math import comb

from task_v004_kv_conjecture5 import build_basis, lll_reduce
from task_v017c_verif_exacte import exact_shortest


def main() -> None:
    print("TACHE V-024 -- Theoreme offset 2 : m(d,d+2) = 2 Catalan(d+1)")
    print("=" * 64)

    print("\n[1-2] Identites de la preuve (d = 1..60) :")
    ok = True
    for d in range(1, 61):
        D = d + 1
        A = comb(2 * D, D)
        B = comb(2 * D, D - 1)
        s0 = [(-1) ** j * comb(D, j) for j in range(D + 1)]
        g11 = sum(c * c for c in s0)
        g12 = sum(s0[j] * s0[j - 1] for j in range(1, D + 1))
        ok &= (g11 == A and g12 == -B)
        ok &= (A - B == A // (D + 1) and (A - B) * (D + 1) == A)  # Catalan
        ok &= (2 * B > A)
    print(f"    Gram = (A, -B), A - B = Catalan(D), 2B > A : "
          f"{'OK partout' if ok else 'ECHEC'}")

    print("\n[3] Croisement SVP exact (minimum + unicite) :")
    for d in (1, 4, 9, 17, 25, 40):
        G = lll_reduce(build_basis(d + 2, d))
        n2, sols = exact_shortest(G)
        D = d + 1
        pred = 2 * comb(2 * D, D) // (D + 1)
        v = [int(x) for x in sols[0]]
        attendu = [(-1) ** j * (comb(D, j) - (comb(D, j - 1) if j else 0))
                   for j in range(D + 2)]
        match_v = (v == attendu or v == [-c for c in attendu])
        print(f"    d={d:>2} : min = {n2} == {pred} : {n2 == pred} ; "
              f"{len(sols)} minima (unicite : {len(sols) == 2}) ; "
              f"v == +-(1-x)^D(1+x) : {match_v}")

    print("\n[4] Balayage brut Q(a,b), (a,b) in [-10,10]^2, d = 1..30 :")
    ok4 = True
    for d in range(1, 31):
        D = d + 1
        A, B = comb(2 * D, D), comb(2 * D, D - 1)
        best, arg = None, None
        for a in range(-10, 11):
            for b in range(-10, 11):
                if (a, b) == (0, 0):
                    continue
                q = A * (a * a + b * b) - 2 * B * a * b
                if best is None or q < best:
                    best, arg = q, {(a, b)}
                elif q == best:
                    arg.add((a, b))
        ok4 &= (best == 2 * (A - B) and arg == {(1, 1), (-1, -1)})
    print(f"    minimum en exactement +-(1,1) partout : "
          f"{'OK' if ok4 else 'ECHEC'}")

    print("\n" + "=" * 64)
    print("THEOREME V24 etabli : sur toute la colonne offset 2, le minimum")
    print("est unique (+-(1-x)^{d+1}(1+x)), vaut 2 Catalan(d+1), et a une")
    print("tete -+1 -- la Conjecture 5 y est PROUVEE pour tout d.")


if __name__ == "__main__":
    main()
