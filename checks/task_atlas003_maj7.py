"""
TACHE ATLAS-003 -- MAJ_7 sur le tore : l'asymetrie aide-t-elle ?

Etend V-001/V-002 (n <= 6) au point suivant de la frontiere : pour chaque
degre d, eps*(polynome torique SYMETRIQUE) vs eps*(GENERAL), MILP exacts.
Enjeu (ligne 14 de l'Atlas) : la borne prouvee de BHLR (Thm 1.2) n'est que
symetrique ; leur Conjecture 1.5 exige le cas general ; KV prouvent que
l'asymetrie AIDE pour Delta_w -- la symetrisation WLOG est fausse en
general. La question mesurable : aide-t-elle MAJ ?

Lecon de run (2026-06-27) : au budget solveur par defaut, les MILP
generaux d=2,3 rendent des INCUMBENTS non certifies (pires que l'optimum
symetrique, donc non informatifs) -- il FAUT etendre time_limit et exiger
la certification (status 0) avant tout verdict d'egalite.

Resultat : egalite CERTIFIEE a tous les degres (cf. tasks/done/ATLAS-003.md).
"""

from __future__ import annotations

import time

import task_v001_torus as T


def main() -> None:
    T.MILP_OPTS = dict(T.MILP_OPTS, time_limit=240)
    print("ATLAS-003 : MAJ_7 (t=4) -- eps*(sym) vs eps*(general), certifies")
    all_eq, all_cert = True, True
    for d in range(1, 8):
        t0 = time.time()
        es, cs = T.torus_sym_eps(7, d)
        eg, cg = T.torus_gen_eps(7, d)
        dt = time.time() - t0
        gain = es is not None and eg is not None and eg < es - 1e-6
        all_eq &= not gain
        all_cert &= not (cs or cg)
        print(f"  d={d} : sym={es:.6f}{'~' if cs else ''} | "
              f"gen={eg:.6f}{'~' if cg else ''}  "
              f"[{'GAIN ASYM !' if gain else '='}]  ({dt:.0f}s)", flush=True)
        if es is not None and es < 1e-9 and eg is not None and eg < 1e-9:
            break
    print("VERDICT n=7 :",
          ("egalite sym = general partout, CERTIFIEE" if all_cert else
           "egalite non refutee mais INCUMBENTS restants -- etendre time_limit")
          if all_eq else "L'ASYMETRIE GAGNE -- verifier et consigner")


if __name__ == "__main__":
    main()
