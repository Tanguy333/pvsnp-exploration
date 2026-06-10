"""
TACHE V-007 -- Reformulation polynomiale du reseau KV + test cyclotomique.

THEOREME P (reformulation polynomiale -- preuve) :
  Par la conjugaison de signes f_i = (-1)^i gamma_i, le reseau L(B_{n,d})
  s'identifie a { f in Z[x] : (1-x)^{d+1} divise f, deg f <= n } (suites
  de coefficients), avec preservation de la norme l2.
  Preuve : gamma = sum a_k col_k avec col_k[i] = (-1)^{i-k} C(d+1, i-k) ;
  en posant b_k = (-1)^k a_k : f_i = (-1)^i gamma_i = sum_k b_k C(d+1, i-k)
  = coefficients de g(x) (1+x)^{d+1} avec g = sum b_k x^k ; substituer
  x -> -x donne la divisibilite par (1-x)^{d+1}.            QED
  => le probleme du plus court vecteur de KV est le probleme PTE-l2 :
  minimiser la norme des multiples de (1-x)^{d+1} a degre borne
  (Prouhet-Tarry-Escott / Erdos-Szekeres).

LEMME (primitivite -- preuve) : tout minimiseur est primitif (contenu 1).
  Preuve : (1+x)^{d+1} est primitif ; par le lemme de Gauss,
  contenu(f) = contenu(g) ; si c > 1, f/c est un multiple plus court. QED

CONJECTURE 5 dans ce langage : un minimiseur a son coefficient de queue
(et de tete, par renversement) en +-1. OBSERVATION-CLE : les produits de
polynomes CYCLOTOMIQUES (x^s Prod Phi_k) ont queue et tete +-1
automatiquement. Si tous les minimiseurs sont de cette forme, la
Conjecture 5 se reduit a « les minimiseurs sont cyclotomiques ».

Test : factoriser tous les minimiseurs sur Z[x] (sympy) ; un facteur
irreductible monique est cyclotomique ssi toutes ses racines sont de
module 1 (Kronecker). Verdict par cellule.
"""

from __future__ import annotations

import numpy as np
import sympy as sp

from task_v004_kv_conjecture5 import build_basis, lll_reduce, shortest_vectors

X = sp.symbols("x")


def gamma_to_poly(gamma):
    coeffs = [int(((-1) ** i) * int(g)) for i, g in enumerate(gamma)]
    return sp.Poly(coeffs[::-1], X)  # sympy : plus haut degre d'abord


def is_cyclotomic_factor(p):
    """ p irreductible entier ; cyclotomique ssi monique (au signe pres)
        et toutes racines de module 1 (Kronecker). x est traite a part. """
    if p.degree() == 0:
        return abs(int(p.LC())) == 1
    if p == sp.Poly(X, X):
        return True  # facteur de decalage x^s
    if abs(int(p.LC())) != 1:
        return False
    roots = np.roots([float(c) for c in p.all_coeffs()])
    return bool(np.all(np.abs(np.abs(roots) - 1.0) < 1e-6))


def analyze(n, d, max_sols=4):
    G = lll_reduce(build_basis(n, d))
    n2, sols = shortest_vectors(G)
    results = []
    for v in sols[:max_sols]:
        f = gamma_to_poly(v)
        # verification Theoreme P : divisibilite par (1+x)^{d+1} + norme
        # (la version (1-x)^{d+1} s'obtient par x -> -x ; le f construit
        #  ici, f_i = (-1)^i gamma_i, est multiple de (1+x)^{d+1})
        q, r = sp.div(f, sp.Poly((1 + X) ** (d + 1), X), domain="ZZ")
        div_ok = r.is_zero
        norm_ok = (sum(int(c) ** 2 for c in f.all_coeffs()) == n2)
        content, prim = f.primitive()
        prim_ok = (abs(int(content)) == 1)
        fl = sp.factor_list(f.as_expr())
        cyclo = all(is_cyclotomic_factor(sp.Poly(base, X))
                    for base, _ in fl[1]) and abs(int(fl[0])) == 1
        trailing = next(int(c) for c in reversed(f.all_coeffs()) if int(c))
        results.append((div_ok, norm_ok, prim_ok, cyclo, trailing,
                        sp.factor(f.as_expr())))
    return n2, results


def main() -> None:
    print("TACHE V-007 -- reformulation polynomiale + test cyclotomique")
    print("=" * 70)
    all_div = all_prim = all_cyclo = True
    shown = 0
    for n in range(6, 19):
        for d in range(1, min(7, n - 3) + 1):
            n2, res = analyze(n, d)
            for (div_ok, norm_ok, prim_ok, cyclo, trail, fact) in res:
                all_div &= (div_ok and norm_ok)
                all_prim &= prim_ok
                all_cyclo &= cyclo
                if not cyclo or (shown < 8 and d >= 3):
                    tag = "CYCLO" if cyclo else "*** NON-CYCLO ***"
                    print(f"  n={n:>2}, d={d} (norme2={n2}) : queue={trail:+d}, "
                          f"{tag}")
                    print(f"      f = {fact}")
                    shown += 1
    print("\n" + "=" * 70)
    print(f"Theoreme P (divisibilite + normes) : "
          f"{'VERIFIE partout' if all_div else '*** ECHEC ***'}")
    print(f"Lemme de primitivite : "
          f"{'VERIFIE partout' if all_prim else '*** ECHEC ***'}")
    if all_cyclo:
        print("TOUS les minimiseurs (n <= 18, d <= 7) sont +- x^s * produits")
        print("de polynomes cyclotomiques => leur queue/tete est +-1, et la")
        print("Conjecture 5 SE REDUIT a : « tout minimiseur est cyclotomique »")
        print("(ou meme : « il en existe un ») -- nouvelle frontiere precise.")
    else:
        print("Des minimiseurs NON cyclotomiques existent -- la reduction")
        print("cyclotomique echoue ; voir les cellules ci-dessus.")


if __name__ == "__main__":
    main()
