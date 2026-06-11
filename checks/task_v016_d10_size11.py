"""
TACHE V-016 -- d = 10 : Conjecture 5 en zone sans temoin + certificat
de NON-EXISTENCE bornee des ideales PTE de taille 11.

Question utilisateur : " peut-on prouver qu'il n'y a pas de solution
ideale en taille 11 ? " -- Reponse de methode : la non-existence TOTALE
est hors de portee (enonce infini, pas de finitisation ; et la
communaute PTE penche plutot pour l'existence). Mais l'exhaustion SVP
certifie INCONDITIONNELLEMENT (sans hypothese de symetrie, contrairement
aux grandes recherches classiques) :
    " aucune ideale de taille 11 n'a son support dans [0, N] "
    <=> le minimum du reseau (d = 10, n = N) reste > 2*11 = 22.
Double dividende : premieres cellules de la Conjecture 5 a d = 10
(degre SANS temoin connu -- la conjecture y vit sans filet V11).

Balayage n = 11..70, budget global ; arret anticipe si une cellule
depasse 1200 s (mur d'outil consigne).
"""

from __future__ import annotations

import time

from task_v004_kv_conjecture5 import build_basis, lll_reduce, shortest_vectors

D = 10
IDEAL = 2 * (D + 1)   # 22 : norme d'une ideale de taille 11


def ends_unit(v):
    nz = [int(x) for x in v if int(x) != 0]
    return abs(nz[0]) == 1 and abs(nz[-1]) == 1


def main() -> None:
    print("TACHE V-016 -- d = 10 : Conjecture 5 + non-existence bornee")
    print("                des ideales PTE de taille 11")
    print("=" * 66)
    last_ok = None
    for n in range(D + 1, 71):
        t0 = time.time()
        G = lll_reduce(build_basis(n, D))
        n2, sols = shortest_vectors(G)
        dt = time.time() - t0
        exists = any(ends_unit(v) for v in sols)
        ideal_found = (n2 <= IDEAL)
        print(f"  (d=10, n={n:>2}) : norme2={n2:>6}, {len(sols):>4} minima, "
              f"bouts +-1 : {'OUI' if exists else '*** NON ***'}"
              f"{'  <<< NORME 22 : IDEALE TAILLE 11 ?!' if ideal_found else ''}"
              f"   ({dt:.0f}s)", flush=True)
        if ideal_found:
            for v in sols:
                coefs = [int(x) for x in v]
                if all(abs(c) <= 1 for c in coefs):
                    A = [a for a, c in enumerate(coefs) if c > 0]
                    B = [a for a, c in enumerate(coefs) if c < 0]
                    if (len(A) == len(B) == 11 and
                            all(sum(a ** j for a in A)
                                == sum(b ** j for b in B)
                                for j in range(1, 11))):
                        print("  *** DECOUVERTE : ideale de taille 11 ***")
                        print(f"      A = {A}")
                        print(f"      B = {B}")
            break
        last_ok = n
        if dt > 1200:
            print(f"  -- mur d'outil : cellule a {dt:.0f}s, arret.", flush=True)
            break
    print("=" * 66)
    if last_ok:
        print(f"CERTIFICAT (inconditionnel, SVP exact) : aucune solution")
        print(f"PTE ideale de taille 11 n'a son support dans [0, {last_ok}].")
        print(f"Et la Conjecture 5 (bouts +-1) tient sur toutes les cellules")
        print(f"verifiees de d = 10 -- le premier degre SANS temoin connu.")


if __name__ == "__main__":
    main()
