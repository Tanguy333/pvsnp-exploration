"""
TACHE B-006 (zone 1) -- Replication du MOTEUR de l'algorithme de Williams :
evaluation par lots d'un circuit SYM o AND sur TOUTES les entrees.

Contexte (audit A-001, Lemma 4.2) : le coeur algorithmique de
NEXP non-inclus-dans ACC^0 est l'evaluation d'un circuit profondeur 2
(fonction symetrique de portes AND) sur l'ensemble de ses 2^n entrees en
temps 2^n poly(n) -- QUASI-INDEPENDANT du nombre de portes t. La force
brute couterait t x 2^n. C'est ce gain ("improvements over exhaustive
search necessarily exploit structure in instances that black-box methods
cannot see") qui, via la connexion SAT -> bornes, franchit les barrieres.

Mecanisme replique : transformee zeta (somme sur les sous-ensembles, DP
classique en n 2^n additions) --
  count(z) = sum_{S subset de supp(z)} a_S,
ou a_S = multiplicite de la porte AND de support S. Puis g(count).

CADRAGE HONNETE :
  - On replique le moteur d'evaluation par lots, PAS l'algorithme complet
    (qui inclut la transformation Beigel-Tarui et la connexion diagonale).
  - La force brute est mesuree jusqu'a t = 30 000 portes puis EXTRAPOLEE
    lineairement (cout exactement t x 2^n) -- etiquete 'estime'. La faire
    tourner a t = 10^6 prendrait ~30 min : c'est precisement le point.
"""

from __future__ import annotations

import time

import numpy as np

rng = np.random.default_rng(2026)


def random_symand(n: int, t: int):
    gates = rng.integers(1, 1 << n, size=t, dtype=np.int64)
    theta = t // 3 + 1
    return gates, theta


def eval_brute(n: int, gates: np.ndarray, theta: int) -> np.ndarray:
    """ Force brute : t x 2^n. """
    N = 1 << n
    zs = np.arange(N, dtype=np.int64)
    count = np.zeros(N, dtype=np.int64)
    for g in gates:
        count += ((zs & g) == g)
    return (count >= theta).astype(np.int8)


def zeta_counts(n: int, gates: np.ndarray) -> np.ndarray:
    """ Transformee zeta : ~ (n+1) 2^n additions, independant de t. """
    N = 1 << n
    a = np.bincount(gates, minlength=N).astype(np.int64)
    zs = np.arange(N, dtype=np.int64)
    for i in range(n):
        bit = 1 << i
        has = (zs & bit).astype(bool)
        a[has] += a[zs[has] ^ bit]
    return a


def main() -> None:
    print("TACHE B-006 -- moteur de Williams : evaluation par lots SYM o AND",
          flush=True)
    print("=" * 72, flush=True)
    n = 20
    N = 1 << n
    print(f"n = {n} ({N} entrees)\n", flush=True)

    # Etalonnage du cout brute par porte (mesure a t = 10 000)
    gates_cal, theta_cal = random_symand(n, 10_000)
    t0 = time.time()
    out_b = eval_brute(n, gates_cal, theta_cal)
    cal = (time.time() - t0) / 10_000  # secondes par porte

    print(f"{'t (portes)':>12} | {'brute (s)':>12} | {'zeta (s)':>9} | "
          f"{'gain':>9} | egalite", flush=True)
    print("-" * 72, flush=True)
    for t in [1_000, 10_000, 30_000, 100_000, 1_000_000, 10_000_000]:
        gates, theta = random_symand(n, t)
        # zeta (toujours mesure)
        t0 = time.time()
        counts = zeta_counts(n, gates)
        out_z = (counts >= theta).astype(np.int8)
        tz = time.time() - t0
        # brute : mesure si t <= 30k, sinon extrapole
        if t <= 30_000:
            t0 = time.time()
            out_b = eval_brute(n, gates, theta)
            tb = time.time() - t0
            same = 'OK' if np.array_equal(out_b, out_z) else '*** ECHEC ***'
            tb_s = f"{tb:.2f}"
        else:
            tb = cal * t
            tb_s = f"~{tb:.0f} (est.)"
            # verification d'egalite par echantillon de 200 entrees
            idx = rng.integers(0, N, size=200)
            okc = all(int(((int(z) & gates) == gates).sum()) ==
                      int(counts[z]) for z in idx)
            same = 'OK (echantillon 200)' if okc else '*** ECHEC ***'
        print(f"{t:>12} | {tb_s:>12} | {tz:>9.3f} | {tb/tz:>8.0f}x | {same}",
              flush=True)

    # Application "SAT par lots"
    print("\nApplication : satisfiabilite d'un SYM o AND a 10M de portes",
          flush=True)
    t = 10_000_000
    gates, _ = random_symand(n, t)
    t0 = time.time()
    counts = zeta_counts(n, gates)
    theta_hi = int(counts.mean() + 6 * counts.std())  # seuil rare
    sat = np.where(counts >= theta_hi)[0]
    tz = time.time() - t0
    print(f"  seuil rare = {theta_hi} : {len(sat)} temoins en {tz:.2f} s "
          f"(brute estimee ~{cal * t / 60:.0f} min)", flush=True)
    if len(sat):
        z = int(sat[0])
        cnt = int(((z & gates) == gates).sum())
        print(f"  temoin z = {z:#07x} verifie independamment : "
              f"count = {cnt} >= {theta_hi} : "
              f"{'OK' if cnt >= theta_hi else 'ECHEC'}", flush=True)

    print(flush=True)
    print("Lecture : cout zeta plat en t ((n+1) 2^n additions) la ou la", flush=True)
    print("force brute paie t x 2^n. L'asymetrie 'la structure interne se", flush=True)
    print("lit plus vite que la boite noire' -- le moteur de la connexion", flush=True)
    print("SAT -> bornes de Williams (bib/williams_2011.md, section 6).", flush=True)


if __name__ == "__main__":
    main()
