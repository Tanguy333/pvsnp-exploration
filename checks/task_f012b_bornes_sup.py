"""
TACHE F-012 (volet b) -- bornes superieures VERIFIEES pour les
instances que l'ILP ne resout pas (aucun incumbent CBC en 9 min,
U exonere par le diagnostic U=200).

Construction : encodage injectif par blocs. p = s_A + (max_A+1) * s_B
ou s_X est la somme ponderee du bloc X ; p determine (s_A, s_B), donc
(g_A, g_B), donc la porte symetrique peut calculer n'importe quelle
composition. Poids = somme des coefficients.

Verification par enumeration directe (256 points) : les ensembles de
valeurs {p : f=1} et {p : f=0} sont disjoints.
"""

from __future__ import annotations

import itertools


def check_separation(f, coeffs_mono, n):
    """coeffs_mono : liste (coefficient, tuple d'indices). Retourne
    (separe?, poids)."""
    ones_vals, zeros_vals = set(), set()
    for z in itertools.product((0, 1), repeat=n):
        p = sum(c for c, S in coeffs_mono if all(z[j] for j in S))
        (ones_vals if f(z) else zeros_vals).add(p)
    return not (ones_vals & zeros_vals), sum(c for c, _ in coeffs_mono)


def main():
    thr4a = lambda z: 1 if 4 * z[0] + 3 * z[1] + 2 * z[2] + z[3] >= 4 else 0
    thr4b = lambda z: 1 if z[4] + 2 * z[5] + 3 * z[6] + 4 * z[7] >= 4 else 0
    gta = lambda z: 1 if 2 * z[0] + z[1] - 2 * z[2] - z[3] >= 1 else 0
    gtb = lambda z: 1 if 2 * z[4] + z[5] - 2 * z[6] - z[7] >= 1 else 0

    # XOR/tout de (THR4, THR4) : s_A = 4z1+3z2+2z3+z4 (0..10),
    # p = s_A + 11 s_B -- injectif sur les paires de sommes de blocs.
    enc_thr = ([(4, (0,)), (3, (1,)), (2, (2,)), (1, (3,))] +
               [(11 * 1, (4,)), (11 * 2, (5,)), (11 * 3, (6,)),
                (11 * 4, (7,))])
    for name, f in [("XOR(THR4,THR4)",
                     lambda z: (thr4a(z) + thr4b(z)) % 2)]:
        ok, w = check_separation(f, enc_thr, 8)
        print(f"  {name} : encodage blocs, poids {w} -- "
              f"{'SEPARE (borne sup VERIFIEE)' if ok else 'ECHEC'}")

    # compositions de GT : les sommes de blocs ne determinent PAS GT
    # (GT depend du couple (2z1+z2, 2z3+z4)) -> encodage injectif
    # par bloc : u_A = (2z1+z2) + 4(2z3+z4) in 0..15, poids 15 ;
    # p = u_A + 16 u_B, poids 15 + 240 = 255.
    enc_gt = ([(2, (0,)), (1, (1,)), (8, (2,)), (4, (3,))] +
              [(32, (4,)), (16, (5,)), (128, (6,)), (64, (7,))])
    for name, f in [("XOR(GT2,GT2)", lambda z: (gta(z) + gtb(z)) % 2),
                    ("OR(GT2,GT2)",
                     lambda z: 1 if gta(z) + gtb(z) >= 1 else 0),
                    ("AND(GT2,GT2)",
                     lambda z: 1 if gta(z) + gtb(z) >= 2 else 0)]:
        ok, w = check_separation(f, enc_gt, 8)
        print(f"  {name} : encodage injectif, poids {w} -- "
              f"{'SEPARE (borne sup VERIFIEE)' if ok else 'ECHEC'}")


if __name__ == "__main__":
    main()
