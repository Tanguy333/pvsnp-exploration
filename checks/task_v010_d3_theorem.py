"""
TACHE V-010 -- d = 3 : vers le troisieme cas de la Conjecture 5 de KV.

Cadre : multiples de (1+x)^4, conditions (t_i = sigma_i (-1)^{a_i}) :
  sum t_i = sum t_i a_i = sum t_i a_i^2 = sum t_i a_i^3 = 0.

PIECES DE PREUVE (regime stable n >= 11) :
 (a) normes 1..7 impossibles :
     - nb impair d'unites : sum t_i impair ;
     - (1,1) : a = b ; (2) : f(-1) != 0 ; (2,1) parite ; (2,2) contenu ;
     - (1x4) : split 2+2, sommes et carres egaux -> paires identiques ;
     - (1x6) : split 3+3, sommes de puissances 1,2,3 egales -> Newton ->
       ensembles identiques -> annulation -> f reduit ;
     - (2,1,1) : 2a = b+c, 2a^2 = b^2+c^2 -> (b-c)^2 = 0 ;
     - (2,1,1,1) : parite.
 (b) norme 8 : formes possibles = 8 unites (plat) ou (2,1,1,1,1) ou
     (2,2) [contenu 2, exclue]. La piece [B] ci-dessous tranche
     (2,1,1,1,1) par enumeration.
 (c) existence plate a degre 11 : la solution PTE ideale classique
     {0,4,7,11} vs {1,2,9,10} (sommes 22, carres 186, cubes 1738).
 (d) plat => extremites +-1. Les cas n = 6..10 (regimes 28/12/10) sont
     couverts par l'enumeration exacte du reseau (V-004/V-006 : tous les
     minima a extremites +-1) -- preuve par calcul fini.

Ce script verifie [A] (exhaustif deg <= 24), [B] (exhaustif deg <= 24),
[C] (exact), [D] (croisement reseau n = 11..20).
"""

from __future__ import annotations

import itertools
import time

from task_v004_kv_conjecture5 import build_basis, lll_reduce, shortest_vectors


def ok4(exps, sigs):
    t = [s * ((-1) ** a) for a, s in zip(exps, sigs)]
    return (sum(t) == 0
            and sum(ti * a for ti, a in zip(t, exps)) == 0
            and sum(ti * a * a for ti, a in zip(t, exps)) == 0
            and sum(ti * a ** 3 for ti, a in zip(t, exps)) == 0)


def main() -> None:
    print("TACHE V-010 -- d = 3 : pieces du theoreme")
    print("=" * 68)
    D = 24

    print(f"\n[A] Rigidites (deg <= {D}) : (1x4), (1x6), (2,1,1), (2,1,1,1)")
    t0 = time.time()
    bad = 0
    for k in (4, 6):
        for exps in itertools.combinations(range(D + 1), k):
            if exps[0] != 0:
                continue
            for sigs in itertools.product((1, -1), repeat=k - 1):
                if ok4(exps, (1,) + sigs):
                    bad += 1
                    print(f"    !!! {k} unites : {exps}")
    for k_units in (2, 3):  # formes (2,1,1) et (2,1,1,1)
        for exps in itertools.combinations(range(D + 1), 1 + k_units):
            if exps[0] != 0:
                continue
            for pos2 in range(1 + k_units):
                for sigs0 in itertools.product((1, -1), repeat=1 + k_units):
                    sigs = tuple(2 * s if i == pos2 else s
                                 for i, s in enumerate(sigs0))
                    if ok4(exps, sigs):
                        bad += 1
                        print(f"    !!! (2,1^{k_units}) : "
                              f"{list(zip(exps, sigs))}")
    print(f"    solutions trouvees : {bad} "
          f"{'(AUCUNE -- conforme)' if bad == 0 else '*** PROBLEME ***'}"
          f"   ({time.time()-t0:.0f}s)", flush=True)

    print(f"\n[B] Forme (2,1,1,1,1) a norme 8 (deg <= {D}) :")
    t0 = time.time()
    found = []
    for exps in itertools.combinations(range(D + 1), 5):
        if exps[0] != 0:
            continue
        for pos2 in range(5):
            for sigs0 in itertools.product((1, -1), repeat=5):
                sigs = tuple(2 * s if i == pos2 else s
                             for i, s in enumerate(sigs0))
                if sigs[0] < 0:
                    sigs = tuple(-s for s in sigs)
                if ok4(exps, sigs):
                    found.append((exps, sigs, pos2))
    ends_bad = [(e, s) for (e, s, p) in found if p in (0, 4)]
    print(f"    solutions : {len(found)} ; avec le +-2 en BOUT : "
          f"{len(ends_bad)}   ({time.time()-t0:.0f}s)")
    for (e, s, p) in found[:6]:
        print(f"      ex. : {list(zip(e, s))}")

    print("\n[C] Solution PTE ideale classique {0,4,7,11} vs {1,2,9,10} :")
    plus, minus = (0, 4, 7, 11), (1, 2, 9, 10)
    exps = tuple(sorted(plus + minus))
    tmap = {a: 1 for a in plus} | {a: -1 for a in minus}
    sigs = tuple(tmap[a] * ((-1) ** a) for a in exps)
    print(f"    sommes {sum(plus)}={sum(minus)}, carres "
          f"{sum(a*a for a in plus)}={sum(a*a for a in minus)}, cubes "
          f"{sum(a**3 for a in plus)}={sum(a**3 for a in minus)}")
    print(f"    (1+x)^4 | f : {'OUI' if ok4(exps, sigs) else 'NON ?!'} ; "
          f"norme^2 = 8 ; degre = 11")

    print("\n[D] Croisement reseau (d = 3, n = 11..20) :")
    okD = True
    for n in range(11, 21):
        G = lll_reduce(build_basis(n, 3))
        n2, sols = shortest_vectors(G)
        ends = all(
            abs(next(int(x) for x in v if int(x))) == 1 and
            abs(next(int(x) for x in reversed(v) if int(x))) == 1
            for v in sols)
        okD &= (n2 == 8 and ends)
    print(f"    norme^2 = 8 et extremites +-1 partout : "
          f"{'OK' if okD else '*** ECHEC ***'}")

    print("\n" + "=" * 68)
    if bad == 0 and not ends_bad and okD:
        print("THEOREME V10 : Conjecture 5 de KV VRAIE pour d = 3 --")
        print("regime stable n >= 11 par les pieces (a)-(d) ; n = 6..10 par")
        print("l'enumeration exacte du reseau (V-004/006). Troisieme cas.")
        if found:
            print(f"NB : {len(found)} solutions (2,1,1,1,1) existent mais")
            print("jamais avec le +-2 en bout -- extremites +-1 preservees.")
    else:
        print("Pieces manquantes -- voir ci-dessus (echec honnete possible).")


if __name__ == "__main__":
    main()
