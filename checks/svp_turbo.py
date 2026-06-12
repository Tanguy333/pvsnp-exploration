"""
SVP_TURBO -- enumeration de Schnorr-Euchner COMPILEE EN CODE MACHINE
(Numba/LLVM), reponse a la question : "fait-on la recherche en C ?".

svp_fast (V-036) avait remplace les Fractions exactes par des flottants
(x8-25) mais restait du bytecode Python interprete (~100-200 ns/noeud).
Ici le coeur de l'enumeration est compile par LLVM : ~2-5 ns/noeud,
soit la vitesse d'un programme C, sans chaine de compilation MSVC.

Architecture (meme garantie d'exactitude que V-036) :
 1. Gram-Schmidt flottant (numpy, hors boucle chaude) ;
 2. coeur njit : zigzag de Schnorr-Euchner, rayon retrecissant en
    flottant avec marge 2e-6, TOUS les candidats sous rayon final
    collectes dans un tampon (compactage in situ si plein) ;
 3. verification EXACTE en entiers Python de chaque candidat ;
    le minimum et les minimaux retournes sont exacts.

API : turbo_shortest(G, borne_init=None) -> (min_exact, [minimaux])
      strictement compatible avec fast_shortest / exact_shortest.
"""

from __future__ import annotations

import numpy as np
from numba import njit

MARGE = 1e-6


@njit(cache=True)
def _enum(mu, c, R2_init, buf, nlbuf, shrink):
    """Coeur compile. shrink=1 : rayon retrecissant (recherche du
    minimum) ; shrink=0 : rayon fixe (TOUS les vecteurs <= R2_init,
    pour voir les objets au-dessus du minimum). Retourne le nombre de
    candidats, ou -1 si le tampon est plein apres compactage."""
    m = c.shape[0]
    x = np.zeros(m, dtype=np.int64)
    sigma = np.zeros((m + 1, m))
    l = np.zeros(m + 1)
    ctr = np.zeros(m)
    step = np.zeros(m, dtype=np.int64)
    R2 = R2_init
    cnt = 0
    cap = buf.shape[0]

    k = m - 1
    going = True
    while going:
        diff = x[k] - ctr[k]
        nl = l[k + 1] + diff * diff * c[k]
        if nl <= R2:
            if k == 0:
                if nl > 0.5:  # ecarte le vecteur nul (norme exacte >= 1)
                    if cnt == cap:
                        w = 0
                        for i in range(cnt):
                            if nlbuf[i] <= R2:
                                if w != i:
                                    for j in range(m):
                                        buf[w, j] = buf[i, j]
                                    nlbuf[w] = nlbuf[i]
                                w += 1
                        cnt = w
                        if cnt == cap:
                            return -1
                    for j in range(m):
                        buf[cnt, j] = x[j]
                    nlbuf[cnt] = nl
                    cnt += 1
                    if shrink == 1 and nl * (1.0 + MARGE) + 1e-9 < R2:
                        R2 = nl * (1.0 + MARGE) + 1e-9
                # zigzag au niveau 0
                step[0] += 1
                d0 = (step[0] + 1) // 2 * (1 if step[0] % 2 == 1 else -1)
                base0 = int(round(ctr[0]))
                if ctr[0] - base0 <= 0:
                    x[0] = base0 + d0
                else:
                    x[0] = base0 - d0
                continue
            # descendre
            l[k] = nl
            for j in range(k):
                sigma[k, j] = sigma[k + 1, j] + x[k] * mu[k, j]
            k -= 1
            ctr[k] = -sigma[k + 1, k]
            x[k] = int(round(ctr[k]))
            step[k] = 0
            continue
        # nl > R2 : zigzag au niveau k ; si les deux branches sont
        # mortes (deux pas consecutifs hors rayon), remonter
        step[k] += 1
        d = (step[k] + 1) // 2 * (1 if step[k] % 2 == 1 else -1)
        base = int(round(ctr[k]))
        if ctr[k] - base <= 0:
            cand = base + d
        else:
            cand = base - d
        diff2 = cand - ctr[k]
        if diff2 * diff2 * c[k] + l[k + 1] > R2:
            d2 = (step[k] + 2) // 2 * (1 if (step[k] + 1) % 2 == 1 else -1)
            if ctr[k] - base <= 0:
                cand2 = base + d2
            else:
                cand2 = base - d2
            diff3 = cand2 - ctr[k]
            if diff3 * diff3 * c[k] + l[k + 1] > R2:
                k += 1
                if k == m:
                    going = False
                    continue
                step[k] += 1
                dd = (step[k] + 1) // 2 * (1 if step[k] % 2 == 1 else -1)
                bb = int(round(ctr[k]))
                if ctr[k] - bb <= 0:
                    x[k] = bb + dd
                else:
                    x[k] = bb - dd
                continue
        x[k] = cand
    return cnt


@njit(cache=True)
def _gso(Zb, mu, c):
    """GSO flottant recalcule depuis les lignes entieres courantes."""
    m, ncols = Zb.shape
    Bs = np.zeros((m, ncols))
    for i in range(m):
        for t in range(ncols):
            Bs[i, t] = Zb[i, t]
        for j in range(i):
            dot = 0.0
            for t in range(ncols):
                dot += Zb[i, t] * Bs[j, t]
            mu[i, j] = dot / c[j]
            for t in range(ncols):
                Bs[i, t] -= mu[i, j] * Bs[j, t]
        s = 0.0
        for t in range(ncols):
            s += Bs[i, t] * Bs[i, t]
        c[i] = s


@njit(cache=True)
def _lll(Zb, delta):
    """LLL avec mises a jour incrementales (Cohen 2.6.3) MAIS GSO
    rafraichi depuis les lignes exactes toutes les 4m permutations,
    et sortie CERTIFIEE par une verification finale sur GSO frais
    (la version purement incrementale derivait de 8 ordres de
    grandeur -- base degeneree, enumeration explosive).
    Operations de lignes entieres => reseau exactement preserve.
    Retourne 0 si certifie, 1 si echec (l'appelant retombe en exact)."""
    m, ncols = Zb.shape
    mu = np.zeros((m, m))
    c = np.zeros(m)
    fenetre = 4 * m if m > 25 else 100
    for _outer in range(400):
        _gso(Zb, mu, c)
        k = 1
        swaps = 0
        while k < m and swaps <= fenetre:
            # size-reduction de la ligne k
            for j in range(k - 1, -1, -1):
                q = int(round(mu[k, j]))
                if q != 0:
                    for t in range(ncols):
                        Zb[k, t] -= q * Zb[j, t]
                    mu[k, j] -= q
                    for i2 in range(j):
                        mu[k, i2] -= q * mu[j, i2]
            if c[k] >= (delta - mu[k, k - 1] * mu[k, k - 1]) * c[k - 1]:
                k += 1
            else:
                swaps += 1
                for t in range(ncols):
                    tmp = Zb[k, t]
                    Zb[k, t] = Zb[k - 1, t]
                    Zb[k - 1, t] = tmp
                mu_ = mu[k, k - 1]
                Bnew = c[k] + mu_ * mu_ * c[k - 1]
                mu[k, k - 1] = mu_ * c[k - 1] / Bnew
                c[k] = c[k - 1] * c[k] / Bnew
                c[k - 1] = Bnew
                for j in range(k - 1):
                    tmp2 = mu[k, j]
                    mu[k, j] = mu[k - 1, j]
                    mu[k - 1, j] = tmp2
                for i2 in range(k + 1, m):
                    t1 = mu[i2, k]
                    mu[i2, k] = mu[i2, k - 1] - mu_ * t1
                    mu[i2, k - 1] = t1 + mu[k, k - 1] * mu[i2, k]
                k = max(k - 1, 1)
        if k < m:
            continue  # fenetre epuisee : GSO frais et on reprend
        # passe terminee : certification sur GSO recalcule, avec
        # hysteresis (delta - 0.002) pour interdire l'oscillation
        _gso(Zb, mu, c)
        good = True
        for kk in range(1, m):
            if c[kk] < (delta - 0.002 - mu[kk, kk - 1] * mu[kk, kk - 1]) \
                    * c[kk - 1]:
                good = False
                break
            for j in range(kk):
                if abs(mu[kk, j]) > 0.5005:
                    good = False
                    break
            if not good:
                break
        if good:
            return 0
    return 1


def turbo_lll(G, delta=0.99):
    """LLL compile et certifie ; en cas d'echec de certification ou
    d'entrees approchant 2^40 (debordement int64), retombe sur le
    LLL Python exact de task_v004 (lent mais toujours correct)."""
    Zb = np.array([[int(t) for t in row] for row in G], dtype=np.int64)
    status = _lll(Zb, delta)
    if status == 0 and np.max(np.abs(Zb)) < (1 << 40):
        return [list(int(t) for t in row) for row in Zb]
    from task_v004_kv_conjecture5 import lll_reduce
    return lll_reduce(G)


def turbo_shortest(G, borne_init=None):
    m = len(G)
    ncols = len(G[0])
    Bz = [[int(t) for t in row] for row in G]
    B = np.array(Bz, dtype=np.float64)

    # Gram-Schmidt flottant (identique a svp_fast)
    Bs = np.zeros_like(B)
    mu = np.zeros((m, m))
    for i in range(m):
        v = B[i].copy()
        for j in range(i):
            mu[i, j] = float(B[i] @ Bs[j]) / float(Bs[j] @ Bs[j])
            v -= mu[i, j] * Bs[j]
        Bs[i] = v
    c = np.array([float(b @ b) for b in Bs])

    best = min(sum(t * t for t in row) for row in Bz)
    if borne_init is not None:
        best = min(best, borne_init)
    R2 = float(best) * (1.0 + MARGE) + 1e-9

    cap = 20000
    while True:
        buf = np.zeros((cap, m), dtype=np.int16)
        nlbuf = np.zeros(cap)
        cnt = _enum(mu, c, R2, buf, nlbuf, 1)
        if cnt >= 0:
            break
        cap *= 4

    # verification exacte des candidats
    def exact_vec(xrow):
        v = [0] * ncols
        for k in range(m):
            xk = int(xrow[k])
            if xk:
                rk = Bz[k]
                for t in range(ncols):
                    v[t] += xk * rk[t]
        return v

    sols = {}
    for i in range(cnt):
        v = exact_vec(buf[i])
        ne = sum(t * t for t in v)
        if 0 < ne <= best:
            if ne < best:
                best = ne
                sols = {}
            sols[tuple(v)] = True

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


def turbo_below(G, borne):
    """TOUS les vecteurs exacts de norme <= borne (rayon fixe, pas de
    retrecissement) -- rend visibles les objets AU-DESSUS du minimum,
    p. ex. les tailles impaires cachees derriere un plateau. Retourne
    la liste des (norme_exacte, vecteur), un representant par signe."""
    m = len(G)
    ncols = len(G[0])
    Bz = [[int(t) for t in row] for row in G]
    B = np.array(Bz, dtype=np.float64)

    Bs = np.zeros_like(B)
    mu = np.zeros((m, m))
    for i in range(m):
        v = B[i].copy()
        for j in range(i):
            mu[i, j] = float(B[i] @ Bs[j]) / float(Bs[j] @ Bs[j])
            v -= mu[i, j] * Bs[j]
        Bs[i] = v
    c = np.array([float(b @ b) for b in Bs])

    R2 = float(borne) * (1.0 + MARGE) + 1e-9
    cap = 20000
    while True:
        buf = np.zeros((cap, m), dtype=np.int16)
        nlbuf = np.zeros(cap)
        cnt = _enum(mu, c, R2, buf, nlbuf, 0)
        if cnt >= 0:
            break
        cap *= 4

    canon = {}
    for i in range(cnt):
        v = [0] * ncols
        for k in range(m):
            xk = int(buf[i, k])
            if xk:
                rk = Bz[k]
                for t in range(ncols):
                    v[t] += xk * rk[t]
        ne = sum(t * t for t in v)
        if 0 < ne <= borne:
            nz = next(t for t in v if t != 0)
            key = tuple(v) if nz > 0 else tuple(-t for t in v)
            canon[key] = ne
    return sorted((ne, list(v)) for v, ne in canon.items())
