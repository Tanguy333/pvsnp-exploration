"""
TOUR 27 (Refuteur) -- execution de la prediction falsifiable du
Proposeur : fermeture EXACTE de la classe A pour MAJ_5(OR2^5).

Classe A : monomes intra-bloc individuels (x_i : alpha_i, y_i : beta_i,
x_i y_i : gamma_i, entiers >= 0 — 0 AUTORISE, l'argument « valeur
satisfaite >= 1 » ne tient plus en presence de croises) + FAISCEAUX de
paires d_ij >= 0 (les 4 paires croisees du couple de blocs {i,j} au
meme coefficient ; cout 4 d_ij ; valeur d_ij s_i s_j ou s = # variables
actives du bloc).

Question : existe-t-il un separateur de classe A de poids total
<= 29 ? (d = 0 exclu : decomposable pur, clos a 30 par T26-S1.)
  - AUCUN => classe A >= 30 : la prediction du Proposeur est PROUVEE.
  - UN => temoin < 30 : refutation de la cible du Tour 27.

Methode : configurations = 4^5 = 1024 etats de blocs (vide, x, y, xy) ;
valeur = somme intra + somme d_ij s_i s_j ; separation = valeurs des
comptes >= 3 disjointes de celles des comptes <= 2. DFS : d-vecteurs
canonises a permutation des blocs pres (graphes ponderes sur 5 sommets,
somme <= 7), puis triples intra (alpha <= beta par swap local) en
approfondissement iteratif sur le poids TOTAL, elagage partiel sain
(blocs restants vides => croises avec eux nuls => toute collision
partielle survit).
"""

from __future__ import annotations

import itertools
import sys
import time

K, T = 5, 3
PAIRS = list(itertools.combinations(range(K), 2))


def canonical_d(d):
    """Representant canonique du d-vecteur a permutation des blocs pres."""
    best = None
    for perm in itertools.permutations(range(K)):
        key = tuple(sorted(
            (d[PAIRS.index((min(perm[i], perm[j]), max(perm[i], perm[j])))]
             for (i, j) in PAIRS)))
        # cle grossiere insuffisante — utiliser le multivecteur ordonne
        vec = tuple(d[PAIRS.index((min(perm[i], perm[j]),
                                   max(perm[i], perm[j])))]
                    for (i, j) in PAIRS)
        if best is None or vec < best:
            best = vec
    return best


def gen_d_vectors(dmax_total):
    """d-vecteurs canoniques avec 1 <= somme <= dmax_total."""
    seen = set()
    out = []
    for total in range(1, dmax_total + 1):
        # compositions de total sur 10 aretes
        def comp(rest, idx, cur):
            if idx == len(PAIRS) - 1:
                cur.append(rest)
                d = tuple(cur)
                c = canonical_d(d)
                if c not in seen:
                    seen.add(c)
                    out.append(c)
                cur.pop()
                return
            for v in range(rest + 1):
                cur.append(v)
                comp(rest - v, idx + 1, cur)
                cur.pop()
        comp(total, 0, [])
    return out


def search_d(d, budget_intra):
    """Pour d fixe : existe-t-il des triples intra de poids total
    <= budget_intra separant ? DFS bloc par bloc, elagage partiel."""
    dmat = [[0] * K for _ in range(K)]
    for (i, j), v in zip(PAIRS, d):
        dmat[i][j] = dmat[j][i] = v

    # etats de bloc : (s, poids_intra_contribue en fonction du triple)
    # on branche sur (alpha <= beta, gamma) du bloc courant.
    # Etat DP partiel : liste de configurations partielles
    # (m, valeur, s-profil des blocs deja choisis) — le s-profil est
    # necessaire pour les croises avec les blocs futurs.
    def dfs(j, budget_left, partial_states, weight_used):
        # partial_states : liste (m, val, s_tuple)
        # collision partielle ?
        ones, zeros = set(), set()
        for (m, val, _) in partial_states:
            (ones if m >= T else zeros).add(val)
        if ones & zeros:
            return None
        if j == K:
            return weight_used if not (ones & zeros) else None
        # brancher sur le triple du bloc j : poids w = a+b+g <= budget_left
        for w in range(0, budget_left + 1):
            for a in range(0, w + 1):
                for b in range(a, w - a + 1):
                    g = w - a - b
                    # etats du bloc j : vide (s=0, +0), x (s=1, +a),
                    # y (s=1, +b), xy (s=2, +a+b+g)
                    new_states = []
                    for (m, val, sprof) in partial_states:
                        cross1 = sum(dmat[i][j] * sprof[i]
                                     for i in range(j))
                        new_states.append((m, val, sprof + (0,)))
                        new_states.append((m + 1, val + a + cross1,
                                           sprof + (1,)))
                        new_states.append((m + 1, val + b + cross1,
                                           sprof + (1,)))
                        new_states.append((m + 1, val + a + b + g
                                           + 2 * cross1, sprof + (2,)))
                    r = dfs(j + 1, budget_left - w, new_states,
                            weight_used + w)
                    if r is not None:
                        return r
        return None

    return dfs(0, budget_intra, [(0, 0, ())], 0)


def main():
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 29
    t0 = time.time()
    dvecs = gen_d_vectors((cap - 0) // 4)
    print(f"d-vecteurs canoniques (somme <= {cap // 4}) : {len(dvecs)}",
          flush=True)
    found = None
    for idx, d in enumerate(dvecs):
        cost_d = 4 * sum(d)
        if cost_d > cap:
            continue
        r = search_d(d, cap - cost_d)
        if r is not None:
            found = (d, r + cost_d)
            print(f"  TEMOIN ! d={d}, poids total = {r + cost_d}")
            break
        if (idx + 1) % 25 == 0:
            print(f"  ... {idx + 1}/{len(dvecs)} d-vecteurs vides "
                  f"({time.time()-t0:.0f}s)", flush=True)
    if found is None:
        print(f"AUCUN separateur de classe A de poids <= {cap} : "
              f"CLASSE A >= 30 — PREDICTION DU PROPOSEUR PROUVEE "
              f"({time.time()-t0:.0f}s)", flush=True)
    else:
        print(f"REFUTATION : temoin de classe A a poids {found[1]} < 30")


if __name__ == "__main__":
    main()
