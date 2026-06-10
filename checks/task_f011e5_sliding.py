"""
TACHE F-011, etape 5 -- L'obstruction collective mod 3 par fenetre glissante.

LEMME 2 (reformulation rigoureuse, base de Mahler standard) :
  une fonction g : [0, n] -> F_3 a un degre de Mahler <= d
  ssi  Delta^{d+1} g (j) = 0 (mod 3) pour tout j = 0 .. n-d-1,
  ou Delta^{d+1} g(j) = sum_{k=0}^{d+1} (-1)^{d+1-k} C(d+1,k) g(j+k).

Donc : deg_3^sym(THR_{t,n}) <= d  ssi  il existe une suite
g(0..n) avec g = 0 sur [0,t), g in {1,2} sur [t,n], satisfaisant la
contrainte de fenetre glissante de largeur d+2 ci-dessus.
=> decision par DP sur l'etat = (d+1) dernieres valeurs. La structure est
   un AUTOMATE FINI : pour d fixe, la faisabilite en n est reguliere.

Ce script :
  (a) implemente la DP ;
  (b) la CROISE avec le solveur exact (grille t <= 6, n <= 24) ;
  (c) calcule deg_3^sym(OR_n) pour n = 1..44 (DP cap d <= 18, complete
      par la borne de blocage PROUVEE pour n >= 27) ;
  (d) teste la loi candidate : deg_3(OR_n) = max(B_block(n), n - 3^floor(log3 n)).
"""

from __future__ import annotations

import itertools
from math import comb

import numpy as np

D_CAP = 18


# ------------------------------------------------------------ DP fenetre

def dp_feasible(t: int, n: int, d: int) -> bool:
    """ Existe-t-il g : 0 sur [0,t), {1,2} sur [t,n], avec
        Delta^{d+1} g = 0 mod 3 partout ? Etat = (d+1) dernieres valeurs. """
    W = d + 2  # largeur de fenetre
    coeffs = [((-1) ** (d + 1 - k)) * comb(d + 1, k) % 3 for k in range(W)]
    # valeurs permises par position
    def allowed(w):
        return (0,) if w < t else (1, 2)
    # etats : tuples des (W-1) dernieres valeurs
    states = {tuple()}
    for w in range(0, n + 1):
        new = set()
        for st in states:
            for val in allowed(w):
                seq = st + (val,)
                if len(seq) == W:
                    s = sum(c * v for c, v in zip(coeffs, seq)) % 3
                    if s != 0:
                        continue
                    seq = seq[1:]
                elif len(seq) > W:
                    raise RuntimeError
                new.add(seq)
        states = new
        if not states:
            return False
    return True


def dp_deg(t: int, n: int, d_cap: int = D_CAP):
    for d in range(t, d_cap + 1):
        if d + 1 > n:  # degre >= n : toujours faisable (aucune contrainte)
            return d
        if dp_feasible(t, n, d):
            return d
    return None


# ------------------------------------------------------------ solveur exact

def solver_deg(t, n, m=3, d_cap=D_CAP, ker_cap=2_000_000):
    highs = list(range(t, n + 1))
    for d in range(t, d_cap + 1):
        idxs = list(range(t, d + 1))
        dim = len(idxs)
        if 3 ** dim > ker_cap:
            return None
        K = np.array(list(itertools.product(range(3), repeat=dim)),
                     dtype=np.int64)
        H = np.array([[comb(w, i) % 3 for i in idxs] for w in highs],
                     dtype=np.int64)
        vals = (K @ H.T) % 3
        if bool(np.all(vals != 0, axis=1).any()):
            return d
    return None


# ------------------------------------------------------------ blocage prouve

def block_bound(t, n):
    """ Borne inferieure PROUVEE (T-F011b mono-premier, p=3). """
    d = t
    while True:
        if not any(all(comb(w, i) % 3 == 0 for i in range(t, d + 1))
                   for w in range(t, n + 1)):
            return d
        d += 1


def law(n):
    """ Loi candidate pour OR (t=1) : max(blocage, n - 3^floor(log3 n)). """
    p = 1
    while p * 3 <= n:
        p *= 3
    return max(block_bound(1, n), n - p)


def main() -> None:
    print("TACHE F-011 etape 5 -- fenetre glissante mod 3 (Lemme 2 + DP)")
    print("=" * 70)

    # (b) cross-validation DP vs solveur
    print("\n(b) Cross-validation DP vs solveur exact (t <= 6, n <= 24) :")
    mism = 0
    tested = 0
    for t in range(1, 7):
        for n in range(t, 25):
            a = dp_deg(t, n)
            b = solver_deg(t, n)
            if a is None or b is None:
                continue
            tested += 1
            if a != b:
                mism += 1
                print(f"    DESACCORD t={t}, n={n} : DP={a}, solveur={b}")
    print(f"    {tested} cellules conclues, {mism} desaccords "
          f"-> {'LEMME 2 VALIDE' if mism == 0 else 'PROBLEME'}")

    # (c)+(d) loi de OR mod 3
    print("\n(c) deg_3^sym(OR_n) par DP (cap 18) + borne de blocage prouvee :")
    print(f"  {'n':>3} | {'DP':>5} | {'blocage':>7} | {'loi max(B, n-3^b)':>17} | accord")
    ok_law = True
    for n in range(1, 45):
        dpv = dp_deg(1, n)
        bb = block_bound(1, n)
        lw = law(n)
        # valeur retenue : DP si conclu ; sinon >= blocage (prouve)
        val = dpv if dpv is not None else None
        if val is not None:
            agree = (val == lw)
            ok_law &= agree
            print(f"  {n:>3} | {val:>5} | {bb:>7} | {lw:>17} | "
                  f"{'OK' if agree else '*** ECART ***'}")
        else:
            note = "coherent (loi >= cap)" if lw > D_CAP else "*** loi <= cap mais DP cap ?! ***"
            print(f"  {n:>3} | >cap{D_CAP} | {bb:>7} | {lw:>17} | {note}")
    print(f"\n  Loi candidate sur les cellules conclues : "
          f"{'CONFIRMEE' if ok_law else 'REFUTEE'}")


if __name__ == "__main__":
    main()
