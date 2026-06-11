"""
TACHE F-011, etape 32 -- THEOREME K'' (famille 3^b) + stratification
symetrique de la frontiere.

THEOREME K''. Pour t = 3^k, n = 2t : V = e_t (mod 3) est une
representation faible symetrique de THR_{t,2t} -- deg_6 = t.
PREUVE (une ligne de Lucas) : pour w in [t, 2t], le digit de position k
de w en base 3 vaut 1 ou 2 (w = 3^k + r ou 2*3^k, r < 3^k), donc
C(w, t) = C(digit, 1) in {1, 2}, jamais 0 mod 3.            QED

STRATIFICATION. A n = 2t, " symetrique-soluble " := il existe (c2, c3)
tels que c2 e_t mod 2 / c3 e_t mod 3 couvrent la fenetre, i.e. AUCUN
w in [t, 2t] avec C(w,t) = 0 mod 6. On calcule la strate pour
t = 2..27 et on la confronte a la table bipartite d'e30/e31 :
attendu : sym-soluble => bipartite-soluble (l'inverse est faux, ex. 5).
"""

from __future__ import annotations

from math import comb


def sym_soluble(t):
    """ aucune valeur w de la fenetre avec C(w,t) = 0 mod 2 ET mod 3 """
    return all(comb(w, t) % 2 != 0 or comb(w, t) % 3 != 0
               for w in range(t, 2 * t + 1))


def mod3_alone(t):
    return all(comb(w, t) % 3 != 0 for w in range(t, 2 * t + 1))


def mod2_alone(t):
    return all(comb(w, t) % 2 != 0 for w in range(t, 2 * t + 1))


BIP = {2, 3, 4, 5, 6, 8, 9, 12, 16, 18, 27}  # e29-e31


def main() -> None:
    print("TACHE F-011 e32 -- Theoreme K'' + stratification symetrique")
    print("=" * 66)

    print("\n[1] Theoreme K'' (t = 3^k : e_t pur mod 3 couvre [t, 2t]) :")
    for k in range(6):
        t = 3 ** k
        ok = mod3_alone(t)
        print(f"    k={k}, t={t:>3}, n={2*t:>3} : "
              f"{'OK' if ok else '*** ECHEC ***'}")

    print("\n[2] Stratification a n = 2t (t = 2..27) :")
    print(f"    {'t':>3} {'sym?':>5} {'mod2':>5} {'mod3':>5} "
          f"{'bipartite (e29-31)':>20}  coherence")
    coherent = True
    for t in range(2, 28):
        s = sym_soluble(t)
        b = t in BIP
        # sym-soluble doit impliquer bipartite-soluble
        ok = (not s) or b
        coherent &= ok
        print(f"    {t:>3} {'OUI' if s else '-':>5} "
              f"{'OUI' if mod2_alone(t) else '-':>5} "
              f"{'OUI' if mod3_alone(t) else '-':>5} "
              f"{'soluble' if b else 'insoluble':>20}  "
              f"{'OK' if ok else '*** INCOHERENT ***'}")
    print("\n    sym-soluble => bipartite-soluble :",
          "VERIFIE" if coherent else "VIOLE ?!")
    syms = [t for t in range(2, 28) if sym_soluble(t)]
    extra = sorted(BIP - set(syms))
    print(f"    strate symetrique : {syms}")
    print(f"    bipartites NON symetriques (le vrai mystere) : {extra}")


if __name__ == "__main__":
    main()
