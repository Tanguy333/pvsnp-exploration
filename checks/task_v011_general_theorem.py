"""
TACHE V-011 -- THEOREME V11 : la borne uniforme et la caracterisation
des minimiseurs (subsume V8, V9, V10).

THEOREME V11. Pour tout d >= 1 et tout n :
 (i)  tout multiple entier non nul f de (1+x)^{d+1} de degre <= n
      verifie ||f||^2 >= 2(d+1) ;
 (ii) il y a egalite ssi f est PLAT (coefficients dans {0, +-1}, 2(d+1)
      monomes) et son partage par signe de t_i = sigma_i(-1)^{a_i} est
      une solution PTE IDEALE de taille d+1 (sommes de puissances 1..d
      egales) ;
 (iii) en consequence, si une solution PTE ideale de taille d+1 tient en
      degre <= n, la Conjecture 5 de KV vaut pour (d, n) -- soit, par
      les tables connues (tailles <= 10 et 12) : d <= 9 et d = 11, pour
      n au-dela du degre minimal de la solution.
PREUVE de (i)-(ii) (10 lignes) :
  Soit A (resp. B) le multiensemble des exposants a_i comptes avec
  multiplicite |c_i| pour t_i > 0 (resp. < 0). La condition j = 0 donne
  |A| = |B| =: m ; les conditions j = 1..d donnent l'egalite des sommes
  de puissances 1..d de A et B. Or ||f||^2 = somme c_i^2 >= somme |c_i|
  = 2m. Si ||f||^2 < 2(d+1), alors m <= d ; les sommes de puissances
  1..m (a fortiori 1..d) determinent un multiensemble de taille m
  (identites de Newton, caracteristique 0) : A = B. Mais chaque exposant
  porte UN monome, donc UN signe de t : il ne peut etre dans A et B a la
  fois -> A = B = vide -> f = 0, contradiction. Egalite : 2m = 2(d+1)
  et c_i^2 = |c_i| pour tout i -> plat, m = d+1, et le partage est une
  PTE ideale de taille d+1 (si A = B etait encore force on aurait f = 0 ;
  ici m = d+1 > d echappe a Newton).                              QED

Verifications executables :
 [1] (i) sur toute la grille (d = 1..9, n = 6..20) : min >= 2(d+1) ;
 [2] (ii) : ou min = 2(d+1), tous les minima sont plats et leur
     +-split est PTE ideale de taille d+1 (sommes de puissances 1..d) ;
 [3] (iii) : table des transitions n*(d) = premier n avec min = 2(d+1)
     -- compare aux degres minimaux des solutions PTE ideales (6, 11,
     18 attendus pour les tailles 3, 4, 5 ; taille 6 : 23, hors grille).
"""

from __future__ import annotations

from task_v004_kv_conjecture5 import build_basis, lll_reduce, shortest_vectors


def main() -> None:
    print("TACHE V-011 -- Theoreme V11 (borne uniforme + caracterisation)")
    print("=" * 70)

    print("\n[1]+[2] Grille d = 1..9, n = 6..20 :")
    ok_bound = True
    ok_char = True
    viol_shown = 0
    transitions = {}
    for d in range(1, 10):
        for n in range(max(6, d + 3), 21):
            G = lll_reduce(build_basis(n, d))
            n2, sols = shortest_vectors(G)
            T = 2 * (d + 1)
            if n2 < T:
                ok_bound = False
                print(f"    *** VIOLATION (i) : (n={n}, d={d}) : {n2} < {T}")
            if n2 == T:
                transitions.setdefault(d, n)
                for v in sols:
                    coefs = [int(x) for x in v]
                    flat = all(abs(c) <= 1 for c in coefs)
                    if not flat:
                        ok_char = False
                        print(f"    *** (ii) minimum non plat a (n={n}, d={d})")
                        continue
                    # +-split selon t_i : en coordonnees RESEAU, t_i = gamma_i
                    # directement (f_i = (-1)^i gamma_i et t_i = f_i (-1)^i,
                    # les deux signes s'annulent)
                    A = [a for a, c in enumerate(coefs) if c > 0]
                    B = [a for a, c in enumerate(coefs) if c < 0]
                    pte = (len(A) == len(B) == d + 1 and
                           all(sum(a ** j for a in A) == sum(b ** j for b in B)
                               for j in range(1, d + 1)))
                    if not pte:
                        ok_char = False
                        if viol_shown < 5:
                            print(f"    *** (ii) split non-PTE a (n={n}, d={d}) : "
                                  f"{coefs}")
                            viol_shown += 1
    print(f"    (i) min >= 2(d+1) : {'OK partout' if ok_bound else 'ECHEC'}")
    print(f"    (ii) egalite => plat + PTE ideale taille d+1 : "
          f"{'OK partout' if ok_char else 'ECHEC'}")

    print("\n[3] Transitions n*(d) (premier n de la grille avec min = 2(d+1)) :")
    expected = {1: 6, 2: 6, 3: 11, 4: 18}
    for d in sorted(transitions):
        note = ""
        if d in expected:
            note = (" = degre minimal PTE ideale connue"
                    if transitions[d] == expected[d] else
                    f" (attendu {expected[d]})")
        print(f"    d = {d} : n* = {transitions[d]}{note}")
    absents = [d for d in range(1, 10) if d not in transitions]
    print(f"    d sans transition dans la grille (n <= 20) : {absents}")
    print("    (d = 5 : la PTE ideale minimale de taille 6 a degre 23 > 20 ;")
    print("     d >= 6 : degres minimaux encore plus grands -- coherent.)")

    print("\n" + "=" * 70)
    if ok_bound and ok_char:
        print("THEOREME V11 verifie : il subsume V8/V9/V10 et donne la")
        print("Conjecture 5 pour tout (d, n) ou une PTE ideale de taille d+1")
        print("tient -- d <= 9 et d = 11 par les tables connues (regime")
        print("stable). Le petit-n (avant la transition) reste la zone ou")
        print("seule l'enumeration exacte conclut (faite pour n <= 20).")


if __name__ == "__main__":
    main()
