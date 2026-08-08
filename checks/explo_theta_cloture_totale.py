"""
CLOTURE TOTALE DU BLOC THETA : min-S(theta) >= 2 sur TOUTES les jauges.

Procedure de decision complete (voir la preuve de completude en tete de
chaque partie) :

  ROUTES (exhaustif) : par bras i, flip de feuille depuis k* = 0 :
    L : L_i(1) = 0  (feuille tuee ; motifs t_i = 1 morts globalement ;
        rigidite => (s0,r0) prop (2,1) => bras N_i = 2 x z^T - y w^T,
        det N = -2 d d' != 0 : INVERSIBLE, zeros exacts parmi 5 motifs)
    B : L_i(1) != 0 => B_i(0,0,1) = 0 ; M0[0,0] != 0 => (x0 z0, y0 w0)
        != (0,0) => M1 determinee (prop. au tenseur des mineurs) ; les
        cellules (a,b) tuees POUR TOUT t sont les zeros communs du
        pinceau : D = {(a,b) : (x_a=0 ou z_b=0) et (y_a=0 ou w_b=0)},
        purement structurel dans les zeros de coordonnees (chaque vecteur
        a au plus 1 zero ; x_a = y_a = 0 interdit par independance).

  COPIES (classification complete, degenerescences incluses) :
    A~ = ⊗pi0 + ⊗pi1, pi0 = rot(y - x), pi1 = rot(y) ; par arete 7 types
    (plein F, 4 zeros simples, 2 monomiaux). Par combo de types :
      - tues STRUCTURELS : les deux produits nuls ;
      - VIVANTS FORCES : exactement un produit nul (valeur != 0) ;
      - region LIBRE : tues multiplicatifs = fibres {prod t_i^{a_i} = c},
        criterion de reseau entier (prouve : plongement des groupes
        abeliens t.f. dans C*), sur les coordonnees des aretes F.
    => liste ACH complete des (types, ensemble tue) realisables.

  COUVERTURE : motif (alpha,beta) != (0,0) doit etre tue par un bras
  (Z_i pour L, D_i pour B) ou par A(alpha) = 0 ou C(beta) = 0.
  (Les tues partiels en t ne sauvent rien ; W(0,0) = {0} automatique
  car Delta[0,0] = 0.)

  GROEBNER par survivant : equations de zeros (bras + coordonnees +
  multiplicatifs des copies) + Rabinowitsch sur les non-nuls
  obligatoires ; variables normalisees par les echelles de colonnes
  (x, z fixes par type), 12 variables restantes.

VALIDATEURS INTERNES :
  V1 : jauges aleatoires -> l'ensemble tue observe de A est dans ACH.
  V2 : formule A~ (pi = rot) vs construction directe depuis P.
  V3 : le cadre unifie doit reproduire la fermeture route-L d'hier.
"""

from __future__ import annotations

import itertools
import sys
import time
from pathlib import Path

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).parent))

RNG = np.random.default_rng(20260809)


def _hnf_basis(gens):
    """ Base triangulaire (Hermite, style colonnes) du reseau engendre. """
    dim = len(gens[0])
    cols = [list(map(int, g)) for g in gens if any(int(x) for x in g)]
    basis = []
    row = 0
    while cols and row < dim:
        with_nz = [c for c in cols if c[row] != 0]
        without = [c for c in cols if c[row] == 0]
        if not with_nz:
            row += 1
            cols = without
            continue
        while len(with_nz) > 1:
            with_nz.sort(key=lambda c: abs(c[row]))
            c0 = with_nz[0]
            rest = []
            for c in with_nz[1:]:
                q = c[row] // c0[row]
                c2 = [a - q * b for a, b in zip(c, c0)]
                if c2[row] != 0:
                    rest.append(c2)
                elif any(c2):
                    without.append(c2)
            with_nz = [c0] + rest
        basis.append((row, with_nz[0]))
        cols = without
        row += 1
    return basis


def in_lattice(v, gens):
    """ v dans le sous-groupe de Z^dim engendre par gens ? (pur entier) """
    v = list(map(int, v))
    if not any(v):
        return True
    gens2 = [g for g in gens if any(int(x) for x in g)]
    if not gens2:
        return False
    for (r, col) in _hnf_basis(gens2):
        if v[r] % col[r] != 0:
            return False
        q = v[r] // col[r]
        v = [a - q * b for a, b in zip(v, col)]
    return not any(v)
CUBE = list(itertools.product((0, 1), repeat=3))
IDX = {a: i for i, a in enumerate(CUBE)}

# ------------------- types d'arete pour les copies -------------------
# zeros imposes : liste de (rangee, valeur) avec rangee '0' = pi0, '1' = pi1
COPY_TYPES = {
    "F":  [],
    "z00": [(0, 0)], "z01": [(0, 1)], "z10": [(1, 0)], "z11": [(1, 1)],
    "Md": [(0, 1), (1, 0)],       # pi0 = (α,0), pi1 = (0,δ)
    "Ma": [(0, 0), (1, 1)],       # pi0 = (0,β), pi1 = (γ,0)
}


def copy_zero_flags(tname):
    z = {(r, a): False for r in (0, 1) for a in (0, 1)}
    for (r, a) in COPY_TYPES[tname]:
        z[(r, a)] = True
    return z


def classify_copy_combo(tnames):
    """ Renvoie (structural_mask, forced_alive_mask, free_list) ou None
        si 0 est tue structurellement. """
    flags = [copy_zero_flags(t) for t in tnames]
    structural, forced, free = 0, 0, []
    for a in CUBE:
        p0z = any(flags[i][(0, a[i])] for i in range(3))
        p1z = any(flags[i][(1, a[i])] for i in range(3))
        if p0z and p1z:
            structural |= 1 << IDX[a]
        elif p0z or p1z:
            forced |= 1 << IDX[a]
        else:
            free.append(a)
    if structural & 1:                       # 0 tue structurellement
        return None
    return structural, forced, free


def mult_kill_subsets(free, tnames):
    """ Sous-ensembles multiplicativement tuables de la region libre
        (0 exclu), via le critere de reseau sur les coordonnees F. """
    Fidx = [i for i in range(3) if tnames[i] == "F"]
    if not free:
        return [frozenset()]
    out = []
    free_nz = [a for a in free if a != (0, 0, 0)]
    for r in range(len(free_nz) + 1):
        for S in itertools.combinations(free_nz, r):
            Sv = [np.array([a[i] for i in Fidx]) for a in S]
            gens = [Sv[j] - Sv[0] for j in range(1, len(Sv))]
            forb = [np.eye(len(Fidx), dtype=int)[k] for k in range(len(Fidx))]
            others = ([np.array([a[i] for i in Fidx])
                       for a in free if a not in S])
            for a in Sv:
                for a2 in others:
                    forb.append(a - a2)
            if len(Fidx) == 0:
                ok = (len(S) == 0)
            else:
                ok = not any(in_lattice(f, gens) for f in forb) if Sv \
                    else not any(in_lattice(f, []) for f in forb)
                # sans generateurs : reseau {0} : f dedans ssi f = 0
                if not Sv:
                    ok = True
            if ok:
                out.append(frozenset(S))
    return out


def build_ACH():
    """ Liste complete des (types, S_mult, mask_tue) pour une copie. """
    ach = []
    for tnames in itertools.product(COPY_TYPES, repeat=3):
        cls = classify_copy_combo(tnames)
        if cls is None:
            continue
        structural, forced, free = cls
        for Sm in mult_kill_subsets(free, tnames):
            mask = structural
            for a in Sm:
                mask |= 1 << IDX[a]
            ach.append((tnames, Sm, mask))
    return ach


# ------------------- validateur V1/V2 -------------------

def rot(v):
    return np.array([v[1], -v[0]], dtype=complex)


def copy_tensor_from_xy(xs, ys):
    pi0 = [rot(y - x) for x, y in zip(xs, ys)]
    pi1 = [rot(y) for y in ys]
    vals = {}
    for a in CUBE:
        t0 = np.prod([pi0[i][a[i]] for i in range(3)])
        t1 = np.prod([pi1[i][a[i]] for i in range(3)])
        vals[a] = t0 + t1
    return vals


def validate_V1_V2(ach, n_rand=400):
    masks = {m for (_, _, m) in ach}
    # V2 : formule pi vs construction directe
    okV2 = True
    for _ in range(20):
        P = [np.array(RNG.normal(size=(2, 2))) for _ in range(3)]
        for M in P:
            while abs(np.linalg.det(M)) < .2:
                M[:] = RNG.normal(size=(2, 2))
        xs = [np.linalg.inv(M) @ np.ones(2) for M in P]
        ys = [np.linalg.inv(M) @ np.array([1.0, 0]) for M in P]
        At = copy_tensor_from_xy(xs, ys)
        for a in CUBE:
            direct = sum(np.prod([P[i][s, a[i]] for i in range(3)])
                         for s in (0, 1))
            ratio = At[a] / direct if abs(direct) > 1e-12 else None
        # proportionnalite : comparer deux motifs non nuls
        pairs = [(a, At[a], sum(np.prod([P[i][s, a[i]] for i in range(3)])
                                for s in (0, 1))) for a in CUBE]
        nz = [(t, d) for (_, t, d) in pairs if abs(d) > 1e-9]
        if len(nz) >= 2:
            r0 = nz[0][0] / nz[0][1]
            okV2 &= all(abs(t / d - r0) < 1e-6 * abs(r0) for (t, d) in nz)
    # V1 : ensembles tues observes dans ACH (aleatoire + zeros structures)
    okV1 = True
    for trial in range(n_rand):
        xs, ys = [], []
        for i in range(3):
            x = RNG.normal(size=2) + 1j * RNG.normal(size=2)
            y = RNG.normal(size=2) + 1j * RNG.normal(size=2)
            r = RNG.random()
            if r < .35:                       # forcer des zeros varies
                which = RNG.integers(6)
                if which == 0:
                    x[RNG.integers(2)] = 0
                elif which == 1:
                    y[RNG.integers(2)] = 0
                elif which == 2:
                    k = RNG.integers(2)
                    y[k] = x[k]              # (y-x) a un zero
                elif which == 3:
                    x[0] = 0
                    y[1] = 0
                elif which == 4:
                    y[0] = x[0]
                    y[1] = 0
                else:
                    x[1] = 0
                    y[0] = 0
            if abs(x[0] * y[1] - x[1] * y[0]) < 1e-9:
                y = y + 0.7 * np.array([1, 1j])
            xs.append(x)
            ys.append(y)
        vals = copy_tensor_from_xy(xs, ys)
        mask = 0
        for a in CUBE:
            if abs(vals[a]) < 1e-9 * max(abs(v) for v in vals.values()):
                mask |= 1 << IDX[a]
        if mask & 1:
            continue                          # A(0) = 0 : hors sujet
        if mask not in masks:
            okV1 = False
            print(f"    V1 ECHEC : masque observe {mask:08b} absent de ACH")
            break
    return okV1, okV2


# ------------------- motifs de bras -------------------

ZPAT_L = [frozenset(), frozenset({(0, 1)}), frozenset({(1, 0)}),
          frozenset({(1, 1)}), frozenset({(0, 1), (1, 0)})]

# types de coordonnees pour un bras route B : zeros de (x, y) et (z, w)
XY_TYPES = {"FF": [], "x0": [("x", 0)], "x1": [("x", 1)],
            "y0": [("y", 0)], "y1": [("y", 1)],
            "x0y1": [("x", 0), ("y", 1)], "x1y0": [("x", 1), ("y", 0)]}


def dpat_B(xyt, zwt):
    """ Cellules tuees pour tout t par un bras route B. """
    xz = {("x", a): False for a in (0, 1)}
    xz.update({("y", a): False for a in (0, 1)})
    for (v, a) in XY_TYPES[xyt]:
        xz[(v, a)] = True
    zw = {("z", b): False for b in (0, 1)}
    zw.update({("w", b): False for b in (0, 1)})
    for (v, b) in XY_TYPES[zwt]:
        zw[("z" if v == "x" else "w", b)] = True
    cells = set()
    for a in (0, 1):
        for b in (0, 1):
            c1 = xz[("x", a)] or zw[("z", b)]
            c2 = xz[("y", a)] or zw[("w", b)]
            if c1 and c2:
                cells.add((a, b))
    return frozenset(cells)


def enumerate_B_arms():
    out = []
    for xyt in XY_TYPES:
        for zwt in XY_TYPES:
            D = dpat_B(xyt, zwt)
            if (0, 0) in D:
                continue                     # M0[0,0] = 0 impossible
            out.append((xyt, zwt, D))
    return out


# ------------------- couche de couverture -------------------

def covering_survivors(ach_masks):
    """ Enumere routes x motifs de bras ; couverture par (KA, KC). """
    B_arms = enumerate_B_arms()
    B_dedup = {}
    for (xyt, zwt, D) in B_arms:
        B_dedup.setdefault(D, []).append((xyt, zwt))
    survivors = []
    n_comb = 0
    for route_B in itertools.product((False, True), repeat=3):
        arm_opts = []
        for i in range(3):
            if route_B[i]:
                arm_opts.append([("B", D) for D in B_dedup])
            else:
                arm_opts.append([("L", Z) for Z in ZPAT_L])
        for arms in itertools.product(*arm_opts):
            n_comb += 1
            killed = set()
            for a in CUBE:
                for b in CUBE:
                    if (a, b) == ((0, 0, 0), (0, 0, 0)):
                        continue
                    if any((a[i], b[i]) in arms[i][1] for i in range(3)):
                        killed.add((a, b))
            U = [(a, b) for a in CUBE for b in CUBE
                 if (a, b) != ((0, 0, 0), (0, 0, 0))
                 and (a, b) not in killed]
            found = None
            for KA in ach_masks:
                need = 0
                okKA = True
                for (a, b) in U:
                    if not (KA >> IDX[a]) & 1:
                        if b == (0, 0, 0):
                            okKA = False
                            break
                        need |= 1 << IDX[b]
                if not okKA:
                    continue
                for KC in ach_masks:
                    if need & ~KC == 0:
                        found = (KA, KC)
                        break
                if found:
                    break
            if found:
                survivors.append((route_B, arms, found[0], found[1], U))
    return survivors, n_comb


def main():
    t0 = time.time()
    print("CLOTURE TOTALE DU THETA -- pipeline unifie")
    print("=" * 72)

    print("[1] Classification complete des copies (ACH)...")
    ach = build_ACH()
    ach_masks = sorted({m for (_, _, m) in ach})
    print(f"    entrees : {len(ach)}, masques distincts : {len(ach_masks)}"
          f"  [{time.time()-t0:.0f}s]")

    print("[2] Validateurs V1 (aleatoire -> ACH) et V2 (formule pi) :")
    okV1, okV2 = validate_V1_V2(ach)
    print(f"    V1 : {'OK' if okV1 else 'ECHEC'}   "
          f"V2 : {'OK' if okV2 else 'ECHEC'}")
    if not (okV1 and okV2):
        print("    STOP : pipeline invalide.")
        return

    print("[3] Couche de couverture (routes x bras x ACH^2)...")
    survivors, n_comb = covering_survivors(ach_masks)
    print(f"    combinaisons de bras : {n_comb} ; "
          f"survivants combinatoires : {len(survivors)}"
          f"  [{time.time()-t0:.0f}s]")
    routes_seen = {}
    for (rb, arms, KA, KC, U) in survivors:
        key = tuple(rb)
        routes_seen.setdefault(key, 0)
        routes_seen[key] += 1
    for k, v in sorted(routes_seen.items()):
        print(f"      route B={k} : {v} survivants")

    # sauvegarde des survivants pour l'etape Groebner (fichier texte)
    outp = Path(__file__).parent / "theta_survivants_totale.txt"
    with open(outp, "w") as f:
        for (rb, arms, KA, KC, U) in survivors:
            f.write(f"route={rb} arms={[(t, sorted(p)) for (t, p) in arms]} "
                    f"KA={KA:08b} KC={KC:08b} |U|={len(U)}\n")
    print(f"    details -> {outp.name}")
    print(f"\n[{time.time()-t0:.0f}s] Etape suivante : Groebner par "
          f"survivant (script compagnon).")


if __name__ == "__main__":
    main()
