"""
MC-001 (formalisation) — verifications executables.

V1. APPARTENANCE : la construction injective p(x) = sum_i 2^i x_i
    (monomes singletons, coefficients 2^i, poids total 2^n - 1 = N-1)
    separe TOUTE fonction f — donc W(f) <= N-1 pour tout f, et dans
    MinSYM+ on peut supposer s < N ; alors tout certificat (a_S) a
    sum a_S <= s < N, donc chaque a_S < N : certificat de taille
    O(N log N), verification en O(N^2) additions. Verifie exhaustivement
    a n = 3 (256 f) et n = 4 (65 536 f).

V2. PAYSAGE : a n = 3, exhaustivement (256 f) :
    - W_global(f) par enumeration complete des vecteurs de coefficients
      (cap = 7 >= max connu 5 du depot) ;
    - le regime UNILATERAL (zeros -> {0}) : les monomes legaux sont
      exactement les S dont le up-cube {x : x >= S} est tout-uns ;
      poids unilateral minimal = SET COVER minimal des uns par ces
      up-cubes (coefficients > 1 inutiles : ils ne font qu'alourdir) ;
    - comptages : combien de f n'ont AUCUN separateur unilateral ;
      combien ont W_global < W_unilateral (le zoo bat le couvert) ;
    - ancrage : max W a n=3 doit valoir 5 (valeur du depot, D-005).
"""

import itertools
from functools import lru_cache

def masques_actifs(n):
    """actifs[x] = liste des S (1..2^n-1) avec S subset de supp(x)."""
    N = 1 << n
    return [[S for S in range(1, N) if (x & S) == S] for x in range(N)]

def separe(f, coeffs, actifs, N):
    uns, zeros = set(), set()
    for x in range(N):
        v = sum(coeffs.get(S, 0) for S in actifs[x])
        (uns if f[x] else zeros).add(v)
    return not (uns & zeros)

# ---------- V1 : construction injective ----------
def verif_injective(n):
    N = 1 << n
    actifs = masques_actifs(n)
    # p(x) = somme des 2^i pour i dans supp(x) = x lui-meme
    coeffs = {1 << i: 1 << i for i in range(n)}
    poids = sum(coeffs.values())
    assert poids == N - 1, poids
    ok = 0
    for masque in range(1 << N):
        f = [(masque >> x) & 1 for x in range(N)]
        if separe(f, coeffs, actifs, N):
            ok += 1
    print(f"V1 n={n} : construction injective (poids {poids} = N-1) "
          f"separe {ok}/{1 << N} fonctions", flush=True)
    assert ok == 1 << N

# ---------- V2 : paysage a n = 3 ----------
def w_global(f, n, actifs, cap=7):
    N = 1 << n
    monos = list(range(1, N))
    if all(f) or not any(f):
        return 0
    for w in range(1, cap + 1):
        # compositions de w sur les 7 monomes (ordre : combinaisons avec rep.)
        for combo in itertools.combinations_with_replacement(monos, w):
            coeffs = {}
            for S in combo:
                coeffs[S] = coeffs.get(S, 0) + 1
            if separe(f, coeffs, actifs, N):
                return w
    return None

def paysage_n3():
    n, N = 3, 8
    actifs = masques_actifs(n)
    sans_unilateral = 0
    zoo_bat_couvert = 0
    egal = 0
    wmax = 0
    for masque in range(1, (1 << N) - 1):  # non constantes
        f = [(masque >> x) & 1 for x in range(N)]
        wg = w_global(f, n, actifs)
        assert wg is not None, masque
        wmax = max(wmax, wg)
        # monomes legaux du regime unilateral : up-cube tout-uns
        legaux = [S for S in range(1, N)
                  if all(f[x] for x in range(N) if (x & S) == S)]
        uns = [x for x in range(N) if f[x]]
        # couverture minimale des uns par les up-cubes legaux
        best = None
        for k in range(0, len(legaux) + 1):
            for sub in itertools.combinations(legaux, k):
                if all(any((x & S) == S for S in sub) for x in uns):
                    best = k
                    break
            if best is not None:
                break
        if best is None:
            sans_unilateral += 1
        elif wg < best:
            zoo_bat_couvert += 1
        else:
            assert wg == best or wg < best, (masque, wg, best)
            egal += 1 if wg == best else 0
            # wg > best impossible : un couvert unilateral est un separateur
            assert wg <= best, (masque, wg, best)
    print(f"V2 n=3 (254 f non constantes) : max W = {wmax} "
          f"(depot : 5)", flush=True)
    print(f"   sans separateur unilateral : {sans_unilateral}", flush=True)
    print(f"   W_global < couvert unilateral (le zoo gagne) : "
          f"{zoo_bat_couvert}", flush=True)
    print(f"   W_global = couvert unilateral : {egal}", flush=True)
    assert wmax == 5

if __name__ == "__main__":
    verif_injective(3)
    verif_injective(4)
    paysage_n3()
    print("TOUTES LES VERIFICATIONS PASSENT", flush=True)
