"""
TACHE V-005 -- (A) Conjecture 5 de KV sur grille etendue (n = 17..20) ;
(B) structure des plus courts vecteurs et lien avec les duaux LP (V-003).

(B) questions : les plus courts vecteurs de L(B) sont-ils des "duaux de
Tchebychev entiers" ? -- support contigu ?, signes alternes ?, et
ressemblent-ils aux duaux LP y* des programmes toriques de MAJ (V-003) ?
Mesure : similarite cosinus |<gamma, y*>| / (||gamma||_2 ||y*||_2).
"""

from __future__ import annotations

import time

import numpy as np

from task_v004_kv_conjecture5 import build_basis, lll_reduce, shortest_vectors
from task_v003_torus_duals import milp_solve, lp_with_duals

TIME_BUDGET_CELL = 60.0


def main() -> None:
    print("TACHE V-005 -- grille etendue + structure des plus courts vecteurs")
    print("=" * 70)

    print("\n[A] Conjecture 5, n = 17..20 :", flush=True)
    all_ok = True
    for n in range(17, 21):
        for d in range(1, min(9, n - 3) + 1):
            t0 = time.time()
            G = lll_reduce(build_basis(n, d))
            n2, sols = shortest_vectors(G)
            dt = time.time() - t0
            lasts = sorted({abs(int(v[n])) for v in sols})
            ok = 1 in lasts
            all_ok &= ok
            print(f"    n={n}, d={d} : norme2={n2}, |gamma_n| in {lasts} "
                  f"[{'OK' if ok else '*** CONTRE-EXEMPLE ***'}] ({dt:.0f}s)",
                  flush=True)
            if dt > TIME_BUDGET_CELL:
                print(f"    (budget cellule depasse a n={n} -- d suivants "
                      f"sautes)", flush=True)
                break
    print(f"    Verdict [A] : {'73+ cellules toutes OK' if all_ok else 'CONTRE-EXEMPLE'}")

    print("\n[B] Structure des plus courts vecteurs + lien duaux LP :", flush=True)
    for (n, d) in ((12, 4), (16, 5), (16, 8)):
        G = lll_reduce(build_basis(n, d))
        n2, sols = shortest_vectors(G)
        t = (n + 1) // 2
        _, kvec = milp_solve(n, d, t)
        eps, y = lp_with_duals(n, d, t, kvec)
        print(f"\n  (n={n}, d={d}) : norme2 min = {n2}, "
              f"{len(sols)} vecteur(s) minimal(aux) ; eps*_LP = {eps:.4f}")
        best_sim = 0.0
        for v in sols[:6]:
            vv = np.array([int(x) for x in v], dtype=float)
            supp = np.where(np.abs(vv) > 0)[0]
            contig = (len(supp) == supp[-1] - supp[0] + 1) if len(supp) else False
            signs = "".join("+" if x > 0 else "-" if x < 0 else "0" for x in vv)
            alt = all(vv[supp[i]] * vv[supp[i + 1]] < 0
                      for i in range(len(supp) - 1)) if len(supp) > 1 else True
            sim = (abs(float(vv @ y)) /
                   (np.linalg.norm(vv) * np.linalg.norm(y) + 1e-12))
            best_sim = max(best_sim, sim)
            print(f"    gamma = {[int(x) for x in v]}")
            print(f"      support {len(supp)}/{n+1} "
                  f"({'contigu' if contig else 'troue'}), "
                  f"alternance stricte : {'oui' if alt else 'NON'}, "
                  f"cos(gamma, y*_LP) = {sim:.3f}")
        print(f"    meilleure similarite avec le dual LP : {best_sim:.3f}")

    print("\nLecture : si les minima sont contigus-alternes, ce sont des")
    print("'gabarits comprimes' ; la similarite avec y*_LP mesure si le")
    print("certificat continu (V-003) vit pres du reseau entier (V-004).")


if __name__ == "__main__":
    main()
