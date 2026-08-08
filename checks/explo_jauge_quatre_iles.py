"""
EXPLORATION -- la superstructure de jauge qui unifie les quatre iles.

Objet : la fonction de partition Z d'une formule 3-SAT (= verre de spins
3-corps dilue) vue comme contraction d'un reseau de tenseurs :
  - noeud variable i : tenseur copie (indices tous egaux) ;
  - noeud clause a  : tenseur f_a = 1 si clause satisfaite, w sinon
    (w = 0 : temperature nulle, Z = #SAT ; w > 0 : temperature finie).

STRUCTURE DE JAUGE : sur chaque arete e on insere I = P_e P_e^{-1}
(P_e inversible 2x2). Z est INVARIANTE (les 4 iles en sont des sections) :
  ile 2 (holographique)  = jauges lineaires globales ;
  ile 4 (BP/cavite)      = la jauge construite sur les messages BP ;
  ile 1 (transfert/DP)   = ordre de contraction exact (independant de jauge) ;
  ile 3 (zeros/analytic) = analyticite de l'invariant Z.

IDENTITES VERIFIEES ICI (Chertkov-Chernyak 2006 ; Alkabetz-Arad 2020 --
replication verifiante declaree) :
  (a) pour TOUTE jauge inversible : somme des 2^E termes d'excitation = Z ;
  (b) a la jauge BP (v0 = m_{a->i}, dual w0 = m_{i->a}/z_e) : tout terme
      ou un noeud porte EXACTEMENT UNE arete excitee est NUL ;
  (c) donc les corrections vivent sur les BOUCLES GENERALISEES (sous-
      graphes sans sommet de degre 1) ; sur un arbre : vide -> Z_BP = Z ;
  (d) le NOMBRE de termes non nuls (boucles generalisees) explose avec la
      taille -- c'est la mesure du mur : la jauge reorganise
      l'exponentielle, elle ne la comprime que sur les iles.
"""

from __future__ import annotations

import itertools
import numpy as np

RNG = np.random.default_rng(20260808)


# ------------------------------------------------------------ instances

def tree_instance():
    """ 2 clauses en arbre : (x1 v x2 v x3), (x3 v x4 v x5). """
    return 5, [((0, 1), (1, 1), (2, 1)), ((2, 1), (3, 1), (4, 1))]


def loopy_instance():
    """ 5 vars, 5 clauses, graphe de facteurs avec boucles (satisfiable :
        tout-vrai satisfait, litteraux positifs majoritaires). """
    return 5, [((0, 1), (1, 1), (2, 0)),
               ((1, 1), (2, 1), (3, 1)),
               ((2, 1), (3, 0), (4, 1)),
               ((0, 1), (3, 1), (4, 0)),
               ((0, 0), (1, 1), (4, 1))]


def bigger_instance():
    """ 6 vars, 7 clauses (plus de boucles). """
    return 6, [((0, 1), (1, 1), (2, 1)),
               ((1, 0), (2, 1), (3, 1)),
               ((2, 1), (3, 1), (4, 0)),
               ((3, 1), (4, 1), (5, 1)),
               ((0, 1), (4, 1), (5, 0)),
               ((0, 0), (2, 1), (5, 1)),
               ((1, 1), (3, 0), (5, 1))]


def clause_weight(clause, assign, w):
    sat = any(assign[v] == pol for (v, pol) in clause)
    return 1.0 if sat else w


def exact_Z(n, clauses, w):
    Z = 0.0
    for bits in itertools.product((0, 1), repeat=n):
        p = 1.0
        for cl in clauses:
            p *= clause_weight(cl, bits, w)
        Z += p
    return Z


# ------------------------------------------------------------------- BP

def run_bp(n, clauses, w, iters=5000, damp=0.5, tol=1e-13):
    """ Messages m_va[(i,a)] et m_av[(a,i)], normalises (somme 1). """
    edges = [(i, a) for a, cl in enumerate(clauses) for (i, _) in [lit for lit in cl]]
    # (i, a) peut apparaitre une fois par occurrence ; on suppose les
    # variables distinctes dans chaque clause (vrai dans nos instances).
    m_va = {(i, a): np.array([0.5, 0.5]) for (i, a) in edges}
    m_av = {(a, i): np.array([0.5, 0.5]) for (i, a) in edges}
    var_edges = {i: [a for (j, a) in edges if j == i] for i in range(n)}

    def clause_msg(a, i):
        cl = clauses[a]
        out = np.zeros(2)
        others = [(v, p) for (v, p) in cl if v != i]
        for si in (0, 1):
            tot = 0.0
            for vals in itertools.product((0, 1), repeat=len(others)):
                assign = {i: si}
                for (v, _), val in zip(others, vals):
                    assign[v] = val
                weight = clause_weight(cl, assign, w)
                prob = 1.0
                for (v, _), val in zip(others, vals):
                    prob *= m_va[(v, a)][val]
                tot += weight * prob
            out[si] = tot
        return out / out.sum()

    for _ in range(iters):
        delta = 0.0
        for (i, a) in edges:
            prod = np.ones(2)
            for b in var_edges[i]:
                if b != a:
                    prod = prod * m_av[(b, i)]
            new = prod / prod.sum()
            new = damp * m_va[(i, a)] + (1 - damp) * new
            delta = max(delta, np.abs(new - m_va[(i, a)]).max())
            m_va[(i, a)] = new
        for (i, a) in edges:
            new = clause_msg(a, i)
            new = damp * m_av[(a, i)] + (1 - damp) * new
            delta = max(delta, np.abs(new - m_av[(a, i)]).max())
            m_av[(a, i)] = new
        if delta < tol:
            break
    return m_va, m_av, edges, delta


# ---------------------------------------- somme d'excitations sous jauge

def excitation_sum(n, clauses, w, gauges, edges, verbose_label=""):
    """ Z = somme sur k in {0,1}^E des termes ; renvoie (somme, termes). """
    var_edges = {i: [] for i in range(n)}
    cl_edges = {a: [] for a in range(len(clauses))}
    for eidx, (i, a) in enumerate(edges):
        var_edges[i].append(eidx)
        cl_edges[a].append(eidx)

    E = len(edges)
    terms = {}
    for k in itertools.product((0, 1), repeat=E):
        t = 1.0
        # noeuds variables : copie -> somme_s prod_e v_{k_e}(s)
        for i in range(n):
            s0 = 1.0
            s1 = 1.0
            for eidx in var_edges[i]:
                P = gauges[eidx]
                s0 *= P[0, k[eidx]]
                s1 *= P[1, k[eidx]]
            t *= (s0 + s1)
            if t == 0.0:
                break
        if t == 0.0:
            terms[k] = 0.0
            continue
        # noeuds clauses : somme ponderee avec les duaux w_{k_e}
        for a, cl in enumerate(clauses):
            eidxs = cl_edges[a]
            Pinvs = [np.linalg.inv(gauges[eidx]) for eidx in eidxs]
            tot = 0.0
            for vals in itertools.product((0, 1), repeat=len(cl)):
                assign = {v: val for (v, _), val in zip(cl, vals)}
                weight = clause_weight(cl, assign, w)
                prob = 1.0
                for (Pinv, eidx, val) in zip(Pinvs, eidxs, vals):
                    prob *= Pinv[k[eidx], val]
                tot += weight * prob
            t *= tot
        terms[k] = t
    return sum(terms.values()), terms


def bp_gauges(m_va, m_av, edges):
    """ Jauge BP : colonnes v0 = m_av (vers la variable), v1 = perp du dual
        w0 = m_va / z_e. P^{-1} fournit les duaux exacts. """
    gauges = []
    for (i, a) in edges:
        v0 = m_av[(a, i)].astype(float)
        w0 = m_va[(i, a)].astype(float)
        z = float(w0 @ v0)
        w0 = w0 / z
        v1 = np.array([-w0[1], w0[0]])          # perp de w0
        P = np.column_stack([v0, v1])
        gauges.append(P)
    return gauges


def analyse(label, n, clauses, w):
    print(f"### {label}  (n={n}, m={len(clauses)}, w={w}) ###")
    Zx = exact_Z(n, clauses, w)
    print(f"  Z exacte (enumeration 2^{n}) = {Zx:.10f}"
          + ("  [= #SAT]" if w == 0 else ""))

    m_va, m_av, edges, delta = run_bp(n, clauses, w)
    E = len(edges)
    print(f"  BP : {E} aretes, residu final = {delta:.2e}")

    # (a) invariance de jauge : jauge ALEATOIRE -> somme = Z.
    rnd = [np.array(RNG.normal(size=(2, 2))) for _ in range(E)]
    for P in rnd:
        while abs(np.linalg.det(P)) < 0.3:
            P[:] = RNG.normal(size=(2, 2))
    Zr, _ = excitation_sum(n, clauses, w, rnd, edges)
    print(f"  (a) jauge aleatoire : somme des 2^{E} termes = {Zr:.10f}"
          f"   ecart = {abs(Zr - Zx):.2e}")

    # (b)(c)(d) jauge BP.
    G = bp_gauges(m_va, m_av, edges)
    Zbp_sum, terms = excitation_sum(n, clauses, w, G, edges)
    vacuum = terms[(0,) * E]
    # excitations simples : un noeud avec exactement 1 arete excitee.
    var_edges = {i: [] for i in range(n)}
    cl_edges = {a: [] for a in range(len(clauses))}
    for eidx, (i, a) in enumerate(edges):
        var_edges[i].append(eidx)
        cl_edges[a].append(eidx)

    def has_lone_node(k):
        for i in range(n):
            if sum(k[e] for e in var_edges[i]) == 1:
                return True

        for a in range(len(clauses)):
            if sum(k[e] for e in cl_edges[a]) == 1:
                return True
        return False

    lone_max = max((abs(v) for k, v in terms.items() if k != (0,) * E
                    and has_lone_node(k)), default=0.0)
    nonzero = [(k, v) for k, v in terms.items() if abs(v) > 1e-10]
    loops = [(k, v) for k, v in nonzero if k != (0,) * E]
    print(f"  (b) jauge BP : somme = {Zbp_sum:.10f}  ecart = "
          f"{abs(Zbp_sum - Zx):.2e}")
    print(f"      terme vide (Z_Bethe) = {vacuum:.10f}   "
          f"correction totale = {Zx - vacuum:+.3e}")
    print(f"      max |terme a noeud solitaire| = {lone_max:.2e}  "
          f"(attendu ~0 : excitations simples annulees)")
    print(f"  (c)(d) termes non nuls = {len(nonzero)} / 2^{E} = {2**E}"
          f"   (boucles generalisees = {len(loops)})")
    print()


def main():
    print("Superstructure de jauge : verification executable")
    print("=" * 72)
    n, cl = tree_instance()
    analyse("ARBRE (BP doit etre EXACT : zero boucle)", n, cl, w=0.3)
    analyse("ARBRE a temperature nulle (Z = #SAT)", n, cl, w=0.0)
    n, cl = loopy_instance()
    analyse("BOUCLES (n=5, m=5)", n, cl, w=0.3)
    analyse("BOUCLES a temperature nulle (Z = #SAT)", n, cl, w=0.0)
    n, cl = bigger_instance()
    analyse("PLUS GRAND (n=6, m=7)", n, cl, w=0.3)


if __name__ == "__main__":
    main()
