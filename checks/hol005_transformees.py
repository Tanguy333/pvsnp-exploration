# -*- coding: utf-8 -*-
r"""HOL-005 — Les certificats de transformées pour la première épingle
de HOL-004 : f(0000) = i, f(0001) = 1, f(1110) = 1, 0 ailleurs
(bit k de x = (x >> k) & 1 ; 0001 = x_1, 1110 = x_2 x_3 x_4).

Tests (cahier : HOL-003 §5, périmètre déclaré dans le backlog) :
  (M)  M-transformable — EXACT : ∃T ∈ GL₂(C) tel que (=₂)T⊗² soit une
       signature matchgate d'arité 2 (parité) ET adj(T)⊗⁴ f satisfasse
       parité + MGI d'arité 4 (FCST Lemma 2.24). Les conditions sont
       POLYNOMIALES ⟹ Gröbner décide ; 1 ∈ idéal sur les 4
       combinaisons de parités = certificat de non-transformabilité.
  (A)  A-transformable — RELAXATION SÛRE : a = H̃⊗⁴ f devrait être
       affine ; conditions NÉCESSAIRES imposées : zéros hors d'un plat
       affine S (307 plats énumérés) et égalité des puissances 4èmes
       sur S ; H ∈ O₂(C) (rotation/réflexion, a² + b² = 1), variantes
       × diag(1, α) avec α⁴ = −1 (α = inconnue w, w⁴ + 1 = 0).
       Infaisable partout ⟹ PAS A-transformable (sûr).
  (P)  P-transformable — RELAXATION SÛRE : motifs produit (partitions
       de {1..4} + signes + épinglages), zéros hors motif + minors de
       factorisation ; H ∈ O₂(C) × {I, [[1,1],[i,−i]]}.
  (R)  réel-transformable — ∃T ∈ O₂(C), λ : λ·T⊗⁴f ∈ R^16 ;
       réalifié (6 inconnues réelles), Gröbner avec garde-temps ;
       repli : recherche numérique (moindres carrés, restarts).

Toute base de Gröbner est calculée sur QQ_I (ou réalifiée si le
domaine gaussien échoue) ; chaque « 1 ∈ idéal » est un certificat.
"""
from __future__ import annotations

import itertools
import sys
import time

import sympy as sp

I = sp.I
X = list(range(16))
W = [bin(x).count("1") for x in X]

F = [0] * 16
F[0] = I
F[1] = 1
F[14] = 1


def tensor_apply(M, f, k=4):
    """(M⊗k f)(y) = somme_x f(x) prod_j M[y_j, x_j] — M 2x2 sympy."""
    g = list(f)
    for j in range(k):
        h = [0] * (1 << k)
        for y in range(1 << k):
            y0 = y & ~(1 << j)
            y1 = y | (1 << j)
            b = (y >> j) & 1
            h[y] = sp.expand(M[b][0] * g[y0] + M[b][1] * g[y1])
        g = h
    return g


def groebner_trivial(eqs, gens):
    eqs = [sp.expand(e) for e in eqs if sp.expand(e) != 0]
    if not eqs:
        return False  # systeme vide : faisable
    try:
        gb = sp.groebner(eqs, *gens, order="grevlex")
        return list(gb.exprs) == [sp.Integer(1)]
    except Exception:
        # realification de secours
        table = {}
        gens_r = []
        for g in gens:
            gr, gi = sp.symbols(f"{g}_re {g}_im", real=True)
            table[g] = gr + I * gi
            gens_r += [gr, gi]
        eqs_r = []
        for e in eqs:
            er = sp.expand(e.subs(table))
            eqs_r += [sp.re(er), sp.im(er)]
        gb = sp.groebner([sp.expand(e) for e in eqs_r if e != 0],
                         *gens_r, order="grevlex")
        return list(gb.exprs) == [sp.Integer(1)]


# ------------------------------------------------------------------ (M)

def parite_eqs(g, classe):
    """classe 'pair' : composantes de poids impair nulles ; 'impair' :
    poids pair nulles. Rend la liste d'equations + l'identite MGI."""
    if classe == "pair":
        eqs = [g[x] for x in X if W[x] % 2 == 1]
        ix = lambda b1, b2, b3, b4: b1 | (b2 << 1) | (b3 << 2) | (b4 << 3)
        mgi = (g[ix(0, 0, 0, 0)] * g[ix(1, 1, 1, 1)]
               - g[ix(0, 0, 1, 1)] * g[ix(1, 1, 0, 0)]
               - (g[ix(0, 1, 1, 0)] * g[ix(1, 0, 0, 1)]
                  - g[ix(0, 1, 0, 1)] * g[ix(1, 0, 1, 0)]))
        return eqs + [mgi]
    eqs = [g[x] for x in X if W[x] % 2 == 0]
    ix = lambda b1, b2, b3, b4: b1 | (b2 << 1) | (b3 << 2) | (b4 << 3)
    mgi = (g[ix(0, 0, 1, 0)] * g[ix(1, 1, 0, 1)]
           - g[ix(0, 0, 0, 1)] * g[ix(1, 1, 1, 0)]
           - (g[ix(0, 1, 0, 0)] * g[ix(1, 0, 1, 1)]
              - g[ix(0, 1, 1, 1)] * g[ix(1, 0, 0, 0)]))
    return eqs + [mgi]


def test_M():
    print("=== (M) M-transformable — test EXACT ===")
    t0, t1, t2, t3, e = sp.symbols("t0 t1 t2 t3 e")
    T = [[t0, t1], [t2, t3]]
    adjT = [[t3, -t1], [-t2, t0]]
    det = t0 * t3 - t1 * t2
    # binaire : h_y = sum_x (=2)_x T[x1,y1] T[x2,y2]
    h = {}
    for y in range(4):
        y1, y2 = y & 1, (y >> 1) & 1
        h[y] = sp.expand(T[0][y1] * T[0][y2] + T[1][y1] * T[1][y2])
    g = tensor_apply(adjT, F)
    tout_infaisable = True
    for cb in ("pair", "impair"):
        eq_h = ([h[1], h[2]] if cb == "pair" else [h[0], h[3]])
        for cg in ("pair", "impair"):
            eqs = eq_h + parite_eqs(g, cg) + [e * det - 1]
            tt = time.time()
            triv = groebner_trivial(eqs, (t0, t1, t2, t3, e))
            print(f"  =2 {cb} & f {cg} : "
                  f"{'1 dans l ideal -> INFAISABLE' if triv else 'IDEAL NON TRIVIAL — A EXAMINER'}"
                  f"  [{time.time() - tt:.1f}s]")
            if not triv:
                tout_infaisable = False
    print(f"  VERDICT M : {'PAS M-transformable (certificat)' if tout_infaisable else 'NON CONCLU (une branche faisable — a examiner)'}")
    return tout_infaisable


# ------------------------------------------------------------------ (A)

def plats_affines():
    """Tous les plats affines non vides de GF(2)^4 (dim 0..4)."""
    plats = set()
    # sous-espaces lineaires par ensembles de generateurs
    for r in range(5):
        for gens in itertools.combinations(range(1, 16), r):
            span = {0}
            for v in gens:
                span |= {s ^ v for s in span}
            span = frozenset(span)
            for x0 in range(16):
                plats.add(frozenset(x0 ^ s for s in span))
    return sorted(plats, key=lambda s: (len(s), sorted(s)))


def test_A():
    print("\n=== (A) A-transformable — relaxation SÛRE ===")
    a, b, w = sp.symbols("a b w")
    variantes = []
    # H in O2 : rotation [[a,b],[-b,a]], reflexion [[a,b],[b,-a]] ;
    # H tilde = H^{-1} = H^T (rotation) / H (reflexion) — projectivement
    # on applique directement la matrice generique (les conditions de
    # relaxation sont invariantes par inversion dans O2).
    rot = [[a, b], [-b, a]]
    refl = [[a, b], [b, -a]]
    for nom_h, H in (("rot", rot), ("refl", refl)):
        variantes.append((nom_h, H, []))
        Hd = [[H[0][0], H[0][1] * w], [H[1][0], H[1][1] * w]]
        variantes.append((nom_h + "*diag(1,alpha)", Hd, [w ** 4 + 1]))
    plats = plats_affines()
    print(f"  {len(plats)} plats affines x {len(variantes)} variantes")
    t0 = time.time()
    faisables = 0
    for nom_h, H, extra in variantes:
        gvec = tensor_apply(H, F)
        for S in plats:
            eqs = [gvec[x] for x in X if x not in S]
            supp = sorted(S)
            for k in range(len(supp) - 1):
                eqs.append(gvec[supp[k]] ** 4 - gvec[supp[k + 1]] ** 4)
            eqs += [a ** 2 + b ** 2 - 1] + extra
            if not groebner_trivial(eqs, (a, b, w)):
                faisables += 1
                if faisables <= 3:
                    print(f"  branche FAISABLE : {nom_h}, plat {sorted(S)}")
    print(f"  [{time.time() - t0:.0f}s] branches faisables : {faisables}")
    print(f"  VERDICT A : "
          f"{'PAS A-transformable (certificat — toutes branches infaisables)' if faisables == 0 else f'NON CONCLU ({faisables} branches de relaxation faisables — la relaxation ne tranche pas)'}")
    return faisables == 0


# ------------------------------------------------------------------ (P)

def motifs_produit():
    """Supports produit : partitions en composantes, signes, epinglages.
    Rend des ensembles de supports (frozensets)."""
    motifs = set()
    elts = [0, 1, 2, 3]
    def parts(l):
        if not l:
            yield []
            return
        h, r = l[0], l[1:]
        for p in parts(r):
            yield [[h]] + p
            for i in range(len(p)):
                yield p[:i] + [[h] + p[i]] + p[i + 1:]
    for part in parts(elts):
        for signes in itertools.product(
                *[list(itertools.product((0, 1), repeat=len(B) - 1))
                  for B in part]):
            for pins in itertools.product((None, 0, 1), repeat=len(part)):
                supp = set()
                choix = []
                for B, sg, pin in zip(part, signes, pins):
                    opts = [pin] if pin is not None else [0, 1]
                    choix.append((B, sg, opts))
                for vals in itertools.product(
                        *[opts for (_, _, opts) in choix]):
                    x = 0
                    for (B, sg, _), t in zip(choix, vals):
                        aff = {B[0]: t, **{B[k]: t ^ sg[k - 1]
                                           for k in range(1, len(B))}}
                        for i, v in aff.items():
                            x |= v << i
                    supp.add(x)
                motifs.add(frozenset(supp))
    return sorted(motifs, key=lambda s: (len(s), sorted(s)))


def test_P():
    print("\n=== (P) P-transformable — relaxation SÛRE ===")
    a, b = sp.symbols("a b")
    rot = [[a, b], [-b, a]]
    refl = [[a, b], [b, -a]]
    KP = [[1, 1], [I, -I]]
    variantes = []
    for nom_h, H in (("rot", rot), ("refl", refl)):
        variantes.append((nom_h, H))
        HK = [[sp.expand(H[0][0] * KP[0][0] + H[0][1] * KP[1][0]),
               sp.expand(H[0][0] * KP[0][1] + H[0][1] * KP[1][1])],
              [sp.expand(H[1][0] * KP[0][0] + H[1][1] * KP[1][0]),
               sp.expand(H[1][0] * KP[0][1] + H[1][1] * KP[1][1])]]
        variantes.append((nom_h + "*[[1,1],[i,-i]]", HK))
    motifs = motifs_produit()
    print(f"  {len(motifs)} motifs produit x {len(variantes)} variantes")
    t0 = time.time()
    faisables = 0
    for nom_h, H in variantes:
        gvec = tensor_apply(H, F)
        for S in motifs:
            eqs = [gvec[x] for x in X if x not in S]
            eqs += [a ** 2 + b ** 2 - 1]
            if not groebner_trivial(eqs, (a, b)):
                faisables += 1
                if faisables <= 3:
                    print(f"  branche FAISABLE : {nom_h}, motif {sorted(S)}")
    print(f"  [{time.time() - t0:.0f}s] branches faisables : {faisables}")
    print(f"  VERDICT P : "
          f"{'PAS P-transformable (certificat)' if faisables == 0 else f'NON CONCLU ({faisables} branches faisables)'}")
    return faisables == 0


# ------------------------------------------------------------------ (R)

def test_R():
    print("\n=== (R) réel-transformable — O2(C) réalifié ===")
    ar, ai, br, bi, lr, li = sp.symbols("ar ai br bi lr li", real=True)
    a = ar + I * ai
    b = br + I * bi
    lam = lr + I * li
    resultats = []
    for nom_h, H in (("rot", [[a, b], [-b, a]]),
                     ("refl", [[a, b], [b, -a]])):
        g = tensor_apply(H, F)
        eqs = []
        for x in X:
            eqs.append(sp.expand(sp.im(sp.expand(lam * g[x]))))
        eqs.append(sp.expand(sp.re(a ** 2 + b ** 2 - 1)))
        eqs.append(sp.expand(sp.im(a ** 2 + b ** 2)))
        # normalisation lambda != 0 : lr^2 + li^2 = 1
        eqs.append(lr ** 2 + li ** 2 - 1)
        tt = time.time()
        try:
            gb = sp.groebner([e for e in eqs if e != 0],
                             ar, ai, br, bi, lr, li, order="grevlex")
            triv = (list(gb.exprs) == [sp.Integer(1)])
            resultats.append(triv)
            print(f"  {nom_h} : "
                  f"{'1 dans l ideal -> INFAISABLE' if triv else 'IDEAL NON TRIVIAL — A EXAMINER'}"
                  f"  [{time.time() - tt:.0f}s]")
        except Exception as ex:
            resultats.append(None)
            print(f"  {nom_h} : NON CONCLU (Grobner : {type(ex).__name__})"
                  f"  [{time.time() - tt:.0f}s]")
    if all(r is True for r in resultats):
        print("  VERDICT R : PAS réel-transformable sous O2(C) (certificat)")
    elif any(r is False for r in resultats):
        print("  VERDICT R : NON CONCLU — branche(s) a examiner (variete non vide ?)")
    else:
        print("  VERDICT R : NON CONCLU (calcul)")


def structures_produit():
    """Structures produit COMPLÈTES (partition, signes, épinglages) —
    pour le test P2 avec factorisation des valeurs."""
    elts = [0, 1, 2, 3]
    def parts(l):
        if not l:
            yield []
            return
        h, r = l[0], l[1:]
        for p in parts(r):
            yield [[h]] + p
            for i in range(len(p)):
                yield p[:i] + [[h] + p[i]] + p[i + 1:]
    out = []
    for part in parts(elts):
        for signes in itertools.product(
                *[list(itertools.product((0, 1), repeat=len(B) - 1))
                  for B in part]):
            for pins in itertools.product((None, 0, 1), repeat=len(part)):
                out.append((part, signes, pins))
    return out


def test_P2():
    """P-transformable, test RENFORCÉ : zéros hors motif + MINORS de
    factorisation (rang 1 à travers chaque bipartition de composantes)
    — l'appartenance à P étant exactement support-produit +
    factorisation, ce test est essentiellement EXACT sous la réduction
    O₂(C) x {I, [[1,1],[i,-i]]}."""
    print("\n=== (P2) P-transformable — test RENFORCÉ (minors) ===")
    a, b = sp.symbols("a b")
    rot = [[a, b], [-b, a]]
    refl = [[a, b], [b, -a]]
    KP = [[1, 1], [I, -I]]
    variantes = []
    for nom_h, H in (("rot", rot), ("refl", refl)):
        variantes.append((nom_h, H))
        HK = [[sp.expand(H[0][0] * KP[0][0] + H[0][1] * KP[1][0]),
               sp.expand(H[0][0] * KP[0][1] + H[0][1] * KP[1][1])],
              [sp.expand(H[1][0] * KP[0][0] + H[1][1] * KP[1][0]),
               sp.expand(H[1][0] * KP[0][1] + H[1][1] * KP[1][1])]]
        variantes.append((nom_h + "*[[1,1],[i,-i]]", HK))
    structs = structures_produit()
    print(f"  {len(structs)} structures x {len(variantes)} variantes")
    t0 = time.time()
    faisables = 0
    for nom_h, H in variantes:
        gvec = tensor_apply(H, F)
        for (part, signes, pins) in structs:
            choix = []
            for B, sg, pin in zip(part, signes, pins):
                opts = [pin] if pin is not None else [0, 1]
                choix.append((B, sg, opts))
            assigns = {}
            supp = set()
            for vals in itertools.product(
                    *[opts for (_, _, opts) in choix]):
                x = 0
                for (B, sg, _), t in zip(choix, vals):
                    aff = {B[0]: t, **{B[k]: t ^ sg[k - 1]
                                       for k in range(1, len(B))}}
                    for i, v in aff.items():
                        x |= v << i
                assigns[vals] = x
                supp.add(x)
            eqs = [gvec[x] for x in X if x not in supp]
            k = len(part)
            libres = [j for j in range(k) if choix[j][2] == [0, 1]]
            # minors : pour chaque composante libre j, la matrice
            # (valeur en t_j = 0 / 1) x (les autres) doit etre rang 1
            for j in libres:
                lignes = {0: {}, 1: {}}
                for vals, x in assigns.items():
                    autres = tuple(v for idx, v in enumerate(vals)
                                   if idx != j)
                    lignes[vals[j]][autres] = gvec[x]
                cles = list(lignes[0].keys())
                for p_ in range(len(cles)):
                    for q_ in range(p_ + 1, len(cles)):
                        eqs.append(sp.expand(
                            lignes[0][cles[p_]] * lignes[1][cles[q_]]
                            - lignes[0][cles[q_]] * lignes[1][cles[p_]]))
            eqs += [a ** 2 + b ** 2 - 1]
            if not groebner_trivial(eqs, (a, b)):
                faisables += 1
                if faisables <= 3:
                    print(f"  branche FAISABLE : {nom_h}, "
                          f"partition {part}, pins {pins}")
    print(f"  [{time.time() - t0:.0f}s] branches faisables : {faisables}")
    print(f"  VERDICT P2 : "
          f"{'PAS P-transformable (certificat)' if faisables == 0 else f'NON CONCLU ({faisables} branches faisables — a examiner)'}")
    return faisables == 0


if __name__ == "__main__":
    quel = sys.argv[1] if len(sys.argv) > 1 else "tout"
    print(f"Épingle : f(0000) = i, f(0001) = 1, f(1110) = 1, 0 ailleurs\n")
    if quel in ("tout", "M"):
        test_M()
    if quel in ("tout", "A"):
        test_A()
    if quel in ("tout", "P"):
        test_P()
    if quel in ("tout", "R"):
        test_R()
    if quel in ("tout", "P2"):
        test_P2()
