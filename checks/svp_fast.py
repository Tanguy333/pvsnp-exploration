"""
SVP_FAST -- enumeration de Schnorr-Euchner en flottants avec
verification exacte des candidats (seance d'ingenierie V-036).

Domaine de validite : bases a entrees moderees (|entree| < ~2^20,
normes < ~2^45) -- le cas de nos reseaux a d <= ~25 apres LLL. Les
erreurs flottantes relatives par noeud (~1e-15) sont couvertes par une
marge de rayon relative 1e-6 : tout vecteur de norme entiere <= cible
a une evaluation flottante strictement sous rayon*(1+marge).

API : fast_shortest(G) -> (min_exact, [vecteurs minimaux exacts])
      compatible avec exact_shortest de task_v017c.
"""

from __future__ import annotations

MARGE = 1e-6


def fast_shortest(G, borne_init=None):
    import numpy as np
    m = len(G)
    ncols = len(G[0])
    B = np.array([[float(int(t)) for t in row] for row in G])
    Bz = [[int(t) for t in row] for row in G]

    # Gram-Schmidt flottant
    Bs = np.zeros_like(B)
    mu = np.zeros((m, m))
    for i in range(m):
        v = B[i].copy()
        for j in range(i):
            mu[i, j] = float(B[i] @ Bs[j]) / float(Bs[j] @ Bs[j])
            v -= mu[i, j] * Bs[j]
        Bs[i] = v
    c = np.array([float(b @ b) for b in Bs])

    # borne initiale : meilleur vecteur de base (exact)
    best = min(sum(t * t for t in row) for row in Bz)
    if borne_init is not None:
        best = min(best, borne_init)
    R2 = best * (1.0 + MARGE) + 1e-9

    sols = {}

    def exact_norm(x):
        v = [0] * ncols
        for k in range(m):
            xk = x[k]
            if xk:
                rk = Bz[k]
                for t in range(ncols):
                    v[t] += xk * rk[t]
        return sum(t * t for t in v), v

    # Schnorr-Euchner iteratif avec sigma incremental
    x = [0] * m
    sigma = np.zeros((m + 1, m))
    l = [0.0] * (m + 1)
    ctr = [0.0] * m
    dx = [0] * m
    step = [0] * m

    k = m - 1
    ctr[k] = 0.0
    x[k] = 0
    dx[k] = 0
    step[k] = 0
    going_down = True

    while True:
        diff = x[k] - ctr[k]
        nl = l[k + 1] + diff * diff * c[k]
        if nl <= R2:
            if k == 0:
                ne, v = exact_norm(x)
                if 0 < ne <= best:
                    if ne < best:
                        best = ne
                        R2 = best * (1.0 + MARGE) + 1e-9
                        sols = {}
                    sols[tuple(v)] = True
                # zigzag au niveau 0
                step[0] += 1
                d0 = (step[0] + 1) // 2 * (1 if step[0] % 2 == 1 else -1)
                base0 = int(round(ctr[0]))
                x[0] = base0 + (d0 if (ctr[0] - base0) <= 0 else -d0)
                continue
            # descendre
            l[k] = nl
            for j in range(k):
                sigma[k][j] = sigma[k + 1][j] + x[k] * mu[k][j]
            k -= 1
            ctr[k] = -sigma[k + 1][k]
            base = int(round(ctr[k]))
            x[k] = base
            step[k] = 0
            continue
        # nl > R2 : zigzag au niveau k ; si epuise, remonter
        # (on remonte si le pas courant depasse des DEUX cotes : le zigzag
        # garantit qu'apres un echec de chaque cote, plus rien sous R2)
        step[k] += 1
        d = (step[k] + 1) // 2 * (1 if step[k] % 2 == 1 else -1)
        base = int(round(ctr[k]))
        cand = base + (d if (ctr[k] - base) <= 0 else -d)
        # test : si l'ecart minimal possible du cote courant depasse deja,
        # et idem de l'autre, remonter. Critere simple et sur : si
        # |cand - ctr| > |x_prec - ctr| pour les deux derniers et nl>R2
        # deux fois consecutives -> les deux branches sont mortes.
        diff2 = cand - ctr[k]
        if diff2 * diff2 * c[k] + l[k + 1] > R2:
            d_next = (step[k] + 2) // 2 * (1 if (step[k] + 1) % 2 == 1 else -1)
            cand2 = base + (d_next if (ctr[k] - base) <= 0 else -d_next)
            diff3 = cand2 - ctr[k]
            if diff3 * diff3 * c[k] + l[k + 1] > R2:
                # remonter
                k += 1
                if k == m:
                    break
                step[k] += 1
                dd = (step[k] + 1) // 2 * (1 if step[k] % 2 == 1 else -1)
                bb = int(round(ctr[k]))
                x[k] = bb + (dd if (ctr[k] - bb) <= 0 else -dd)
                continue
        x[k] = cand

    # filtrer au minimum exact et canoniser au signe pres
    # (premier coefficient non nul > 0), puis restituer les deux signes
    canon = set()
    for v in sols:
        if sum(t * t for t in v) != best:
            continue
        nz = next(t for t in v if t != 0)
        canon.add(v if nz > 0 else tuple(-t for t in v))
    out = []
    for v in canon:
        out.append(list(v))
        out.append([-t for t in v])
    return best, out
