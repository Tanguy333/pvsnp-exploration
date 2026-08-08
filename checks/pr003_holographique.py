# -*- coding: utf-8 -*-
r"""PR-003 — Contre-vérification exécutable de la candidature
holographique (SL-19 et extensions).

Convention (celle de la candidature) : base T = [[a, b], [c, d]],
det = ad − bc ≠ 0 ; côté reconnaisseur G = T⊗k · f ; côté générateur
H = adj(T)ᵀ⊗k · f (l'adjugate remplace (T⁻¹)ᵀ — les signatures sont
projectives, le facteur det^(−k) est sans effet sur la réalisabilité).
Robustesse : échanger les rôles reconnaisseur/générateur revient à
remplacer T par (Tᵀ)⁻¹, une bijection de GL₂ — la réalisabilité de la
PAIRE est indépendante de ce choix.

Signatures symétriques d'arité 3 : [f₀, f₁, f₂, f₃] (valeur par poids
de Hamming). OR₃ = [0,1,1,1] ; =₃ = [1,0,0,1] ; =₂ = [1,0,1].

Composantes transformées (dérivées à la main, RE-DÉRIVÉES ici par
calcul symbolique générique — le script ne fait confiance à aucune
formule manuscrite) :
- CONDITION DE PARITÉ (nécessaire pour toute signature matchgate,
  Kasteleyn/Cai-Lu) : la classe de poids impair OU la classe de poids
  pair s'annule. Les identités de matchgate au-delà de la parité pour
  l'arité 3 sont [À TRANCHER SUR TEXTE Cai-Lu] — le test ci-dessous
  implémente la parité SEULE : l'INFAISABILITÉ sous parité seule est
  donc un verdict SÛR (la parité est nécessaire) ; une FAISABILITÉ
  n'est qu'une candidature de base (à confirmer par construction).

Volets :
A. Vérification du pré-calcul du Proposeur (T = [[1, −2], [1, 0]] :
   OR₃ transformé est de parité paire).
B. SL-19 char 0 : pour {OR₃, =₃}, les 4 combinaisons de parités,
   système + saturation det ≠ 0 (variable e, e·det = 1), base de
   Gröbner sur ℚ — « 1 ∈ idéal » = infaisable sur TOUT corps de
   caractéristique 0 (ℚ(i) compris : verdict plus fort que demandé).
C. SL-19 char p : force brute EXHAUSTIVE sur GL₂(F_p),
   p ∈ {3, 5, 7, 11, 13} — {OR₃, =₃} ET la paire de contrôle
   {OR₃, =₂} (la lecture-deux-fois du miracle de Valiant 2004) ;
   témoins exhibés et re-vérifiés.
"""
import itertools
import sys
import time

import sympy as sp


def sym_to_tensor(f, k):
    """Signature symétrique [f_0..f_k] -> tenseur indexé par y
    (entier de k bits)."""
    return {y: f[bin(y).count("1")] for y in range(1 << k)}


def transforme(M, f, k):
    """(M⊗k · f)(y) = somme_x f(x) prod_i M[y_i, x_i]."""
    t = sym_to_tensor(f, k)
    g = {}
    for y in range(1 << k):
        s = 0
        for x, fx in t.items():
            if fx == 0:
                continue
            p = fx
            for i in range(k):
                p *= M[(y >> i) & 1][(x >> i) & 1]
            s += p
        g[y] = sp.expand(s)
    return g


def classes_parite(g, k):
    imp = [g[y] for y in range(1 << k) if bin(y).count("1") % 2 == 1]
    pai = [g[y] for y in range(1 << k) if bin(y).count("1") % 2 == 0]
    return {"impair=0": imp, "pair=0": pai}


def volet_A():
    print("=== A — pré-calcul du Proposeur (OR3 seul, T = [[1,-2],[1,0]]) ===")
    T = [[1, -2], [1, 0]]
    g = transforme(T, [0, 1, 1, 1], 3)
    imp = [g[y] for y in range(8) if bin(y).count('1') % 2 == 1]
    print(f"  composantes impaires : {imp} ; paires : "
          f"{[g[y] for y in range(8) if bin(y).count('1') % 2 == 0]}")
    print(f"  VERDICT : {'CONFORME (parite paire)' if all(v == 0 for v in imp) else 'NON CONFORME'}")


def volet_B():
    print("\n=== B — SL-19 char 0 : {OR3, =3}, Grobner sur Q, det != 0 ===")
    a, b, c, d, e = sp.symbols("a b c d e")
    T = [[a, b], [c, d]]
    adjT = [[d, -c], [-b, a]]  # adj(T)^T
    G = transforme(T, [0, 1, 1, 1], 3)
    H = transforme(adjT, [1, 0, 0, 1], 3)
    det = a * d - b * c
    tout_infaisable = True
    for nomG, eqG in classes_parite(G, 3).items():
        for nomH, eqH in classes_parite(H, 3).items():
            sys_eq = [sp.expand(q) for q in eqG + eqH] + [e * det - 1]
            t0 = time.time()
            gb = sp.groebner(sys_eq, a, b, c, d, e, order="grevlex")
            triv = (list(gb.exprs) == [sp.Integer(1)])
            print(f"  G {nomG} & H {nomH} : "
                  f"{'1 dans l ideal -> INFAISABLE (char 0, tout corps)' if triv else 'IDEAL NON TRIVIAL — A EXAMINER'}"
                  f"  [{time.time() - t0:.1f}s]")
            if not triv:
                tout_infaisable = False
                print(f"    base : {list(gb.exprs)[:6]} ...")
    print(f"  SL-19 cote char 0 : "
          f"{'INFAISABLE dans les 4 combinaisons — CONFORME a l attendu' if tout_infaisable else 'faisabilite candidate — INATTENDU, a re-verifier 3 fois'}")


def volet_C():
    print("\n=== C — force brute GL2(F_p) : {OR3,=3} et controle {OR3,=2} ===")
    for p in (3, 5, 7, 11, 13):
        t0 = time.time()
        res = {"=3": [], "=2": []}
        for a, b, c, d in itertools.product(range(p), repeat=4):
            det = (a * d - b * c) % p
            if det == 0:
                continue
            adjT = [[d, (-c) % p], [(-b) % p, a]]
            T = [[a, b], [c, d]]
            # OR3 transforme par T
            g = transforme_fp(T, [0, 1, 1, 1], 3, p)
            gi = [g[y] for y in range(8) if bin(y).count("1") % 2 == 1]
            gp = [g[y] for y in range(8) if bin(y).count("1") % 2 == 0]
            okG = ("imp" if all(v == 0 for v in gi) else None,
                   "pai" if all(v == 0 for v in gp) else None)
            if okG == (None, None):
                continue
            for nom, sig, k in (("=3", [1, 0, 0, 1], 3), ("=2", [1, 0, 1], 2)):
                h = transforme_fp(adjT, sig, k, p)
                hi = [h[y] for y in range(1 << k) if bin(y).count("1") % 2 == 1]
                hp = [h[y] for y in range(1 << k) if bin(y).count("1") % 2 == 0]
                if (any(ok for ok in okG) and
                        (all(v == 0 for v in hi) or all(v == 0 for v in hp))):
                    res[nom].append((a, b, c, d))
        n2, n3 = len(res["=2"]), len(res["=3"])
        tem3 = res["=3"][0] if n3 else None
        tem2 = res["=2"][0] if n2 else None
        print(f"  p = {p:2} : {{OR3,=3}} {'FAISABLE' if n3 else 'infaisable'}"
              f" ({n3} bases{', temoin T = ' + str(tem3) if tem3 else ''}) ; "
              f"{{OR3,=2}} {'FAISABLE' if n2 else 'infaisable'}"
              f" ({n2} bases{', temoin T = ' + str(tem2) if tem2 else ''})"
              f"  [{time.time() - t0:.0f}s]")


def transforme_fp(M, f, k, p):
    t = sym_to_tensor(f, k)
    g = {}
    for y in range(1 << k):
        s = 0
        for x, fx in t.items():
            if fx == 0:
                continue
            pr = fx
            for i in range(k):
                pr = (pr * M[(y >> i) & 1][(x >> i) & 1]) % p
            s = (s + pr) % p
        g[y] = s % p
    return g


if __name__ == "__main__":
    quel = sys.argv[1] if len(sys.argv) > 1 else "tout"
    if quel in ("tout", "A"):
        volet_A()
    if quel in ("tout", "B"):
        volet_B()
    if quel in ("tout", "C"):
        volet_C()
