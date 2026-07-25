"""
A-013, volet mesure — LE COUT DE LA CONVENTION.

Rattachement : Atlas ligne 7. La cellule porte un [NON TROUVE] : les portes AND
du format SYM-AND lisent-elles des LITTERAUX ou seulement des VARIABLES ? Le
volet lecture cherche la reponse dans les textes. Ce volet-ci mesure ce que la
question COUTE, quelle que soit sa reponse.

Deux modeles, meme definition du poids (somme des coefficients d'un p a
coefficients entiers >= 0, tel que {p : f=1} et {p : f=0} soient disjoints —
la porte symetrique lit p et decide) :
  * MODELE POSITIF (celui du depot, 18 taches) : les termes sont les 2^n - 1
    monomes positifs non vides.
  * MODELE LITTERAUX (le format de Beigel-Tarui si les negations sont
    admises) : les termes sont les 3^n - 1 monomes sur litteraux non vides,
    c'est-a-dire prod_{i dans S} (x_i ou 1 - x_i) pour S non vide.
Le modele positif est une SOUS-CLASSE stricte du modele litteraux (tout monome
positif est un monome sur litteraux). Donc W_lit <= W_pos toujours ; la
question est de combien.

Ce que la mesure donne, et qui vaut dans les deux cas :
  - si l'ecart est BORNE et petit, la convention est un detail de cadrage ;
  - s'il est GRAND ou croissant, alors les bornes INFERIEURES du modele positif
    ne disent rien du format a litteraux, et 18 taches du depot ont mesure un
    autre objet que celui qu'elles visaient.

Protocole (lecon F-016) : chaque optimum SAT est RE-VERIFIE par enumeration
complete et independante avant d'etre imprime.
"""

from __future__ import annotations

import itertools
import sys
import time

from ortools.sat.python import cp_model


def termes_positifs(n):
    """(nom, vecteur d'indicateurs sur les 2^n entrees)."""
    out = []
    for S in range(1, 1 << n):
        vec = [1 if (z & S) == S else 0 for z in range(1 << n)]
        out.append((f"+{S:0{n}b}", vec))
    return out


def termes_litteraux(n):
    out = []
    for S in range(1, 1 << n):
        idx = [i for i in range(n) if S >> i & 1]
        for pol in itertools.product((0, 1), repeat=len(idx)):
            vec = []
            for z in range(1 << n):
                ok = all(((z >> i) & 1) == p for i, p in zip(idx, pol))
                vec.append(1 if ok else 0)
            nom = "".join(("x" if p else "!") + str(i)
                          for i, p in zip(idx, pol))
            out.append((nom, vec))
    return out


def poids_min(f, termes, n, cap_max=40, tl=120.0):
    """min somme des coefficients ; canal de valeurs, sans cassage de
    symetrie (les deux modeles n'ont pas le meme groupe)."""
    N = 1 << n
    for cap in range(1, cap_max + 1):
        model = cp_model.CpModel()
        a = [model.NewIntVar(0, cap, "") for _ in termes]
        model.Add(sum(a) <= cap)
        z = [model.NewBoolVar("") for _ in range(cap + 1)]
        for e in range(N):
            expr = [a[t] for t, (_, vec) in enumerate(termes) if vec[e]]
            v = model.NewIntVar(0, cap, "")
            model.Add(v == (sum(expr) if expr else 0))
            model.AddElement(v, z, 1 if f[e] else 0)
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = tl
        solver.parameters.num_search_workers = 8
        st = solver.Solve(model)
        if st in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            sol = [solver.Value(x) for x in a]
            if not reverifie(f, termes, sol, n):
                return None, "ECHEC DE RE-VERIFICATION"
            return cap, sol
        if st != cp_model.INFEASIBLE:
            return None, f"UNKNOWN a cap={cap}"
    return None, f"> {cap_max}"


def reverifie(f, termes, sol, n):
    """Enumeration complete INDEPENDANTE du solveur."""
    uns, zeros = set(), set()
    for e in range(1 << n):
        val = sum(c for c, (_, vec) in zip(sol, termes) if vec[e])
        (uns if f[e] else zeros).add(val)
    return not (uns & zeros)


def fonctions(n):
    """Batterie : les objets deja mesures par le depot, plus des temoins."""
    out = {}
    N = 1 << n
    bits = lambda z: bin(z).count("1")
    out["PARITY"] = [bits(z) % 2 for z in range(N)]
    out["MAJ"] = [1 if bits(z) > n // 2 else 0 for z in range(N)]
    out["AND"] = [1 if z == N - 1 else 0 for z in range(N)]
    out["OR"] = [1 if z else 0 for z in range(N)]
    out[f"THR_2"] = [1 if bits(z) >= 2 else 0 for z in range(N)]
    if n % 2 == 0:
        k = n // 2
        out["IP"] = [sum((z >> (2 * i)) & 1 & ((z >> (2 * i + 1)) & 1)
                         for i in range(k)) % 2 for z in range(N)]
        # composition a blocs disjoints : MAJ_k(OR2^k), l'objet du fil
        t = (k + 1) // 2
        out[f"THR{t}(OR2^{k})"] = [
            1 if sum(1 for i in range(k)
                     if (z >> (2 * i)) & 3) >= t else 0
            for z in range(N)]
    return out


def exhaustif(n, tl=30.0):
    """L'ecart entre les deux conventions est-il BORNE ? Balayage de TOUTES
    les fonctions booleennes a n variables (2^(2^n)), rapport max."""
    tp, tl_ = termes_positifs(n), termes_litteraux(n)
    N = 1 << n
    print(f"=== n = {n} : balayage EXHAUSTIF des {1 << N} fonctions ===",
          flush=True)
    pire, pire_f = 1.0, None
    ecarts = {}
    t0 = time.time()
    for masque in range(1 << N):
        f = [(masque >> e) & 1 for e in range(N)]
        if all(f) or not any(f):
            continue  # constantes : poids 0 des deux cotes
        wp, _ = poids_min(f, tp, n, tl=tl)
        wl, _ = poids_min(f, tl_, n, tl=tl)
        if wp is None or wl is None:
            print(f"  !! non conclu pour le masque {masque:0{N}b}",
                  flush=True)
            continue
        ecarts[(wp, wl)] = ecarts.get((wp, wl), 0) + 1
        r = wp / wl
        if r > pire:
            pire, pire_f = r, (masque, wp, wl)
    print(f"  rapport MAXIMAL W_positif / W_litteraux = {pire:.2f}",
          flush=True)
    if pire_f:
        m, wp, wl = pire_f
        print(f"  atteint par f = {m:0{N}b} (table de verite), "
              f"W_positif = {wp}, W_litteraux = {wl}", flush=True)
    print(f"  distribution (W_pos, W_lit) -> effectif : "
          f"{dict(sorted(ecarts.items()))}", flush=True)
    print(f"  ({time.time()-t0:.0f}s)", flush=True)


def canonique(masque, n):
    """Representant canonique de f sous les symetries qui preservent LES DEUX
    mesures : permutation des variables (les deux modeles sont invariants) et
    complementation de f (la disjonction des ensembles de valeurs est
    symetrique en f / non-f). PAS la complementation d'une variable : elle
    preserve W_litteraux mais PAS W_positif — c'est justement l'asymetrie
    qu'on mesure."""
    N = 1 << n
    best = None
    for perm in itertools.permutations(range(n)):
        m = 0
        for e in range(N):
            img = 0
            for i in range(n):
                if (e >> i) & 1:
                    img |= 1 << perm[i]
            if (masque >> e) & 1:
                m |= 1 << img
        for cand in (m, (~m) & ((1 << N) - 1)):
            if best is None or cand < best:
                best = cand
    return best


def exhaustif_quotient(n, tl=60.0):
    """n = 4 : 65 536 fonctions, quotientees par S_n x (complement de f)."""
    tp, tl_ = termes_positifs(n), termes_litteraux(n)
    N = 1 << n
    reps = sorted({canonique(m, n) for m in range(1 << N)})
    print(f"=== n = {n} : {1 << N} fonctions -> {len(reps)} classes "
          f"(S_{n} x complement de f) ===", flush=True)
    pire, pire_f, t0 = 1.0, None, time.time()
    nonconclu = 0
    for m in reps:
        f = [(m >> e) & 1 for e in range(N)]
        if all(f) or not any(f):
            continue
        wp, _ = poids_min(f, tp, n, tl=tl)
        wl, _ = poids_min(f, tl_, n, tl=tl)
        if wp is None or wl is None:
            nonconclu += 1
            continue
        if wp / wl > pire:
            pire, pire_f = wp / wl, (m, wp, wl)
    print(f"  rapport MAXIMAL = {pire:.2f}   (non conclus : {nonconclu})",
          flush=True)
    if pire_f:
        m, wp, wl = pire_f
        print(f"  atteint par f = {m:0{N}b}, W_positif = {wp}, "
              f"W_litteraux = {wl}", flush=True)
    print(f"  ({time.time()-t0:.0f}s)", flush=True)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "quotient":
        exhaustif_quotient(int(sys.argv[2]) if len(sys.argv) > 2 else 4)
        return
    if len(sys.argv) > 1 and sys.argv[1] == "exhaustif":
        exhaustif(int(sys.argv[2]) if len(sys.argv) > 2 else 3)
        return
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    for n in range(2, nmax + 1):
        tp, tl_ = termes_positifs(n), termes_litteraux(n)
        print(f"\n=== n = {n} : {len(tp)} monomes positifs, "
              f"{len(tl_)} monomes sur litteraux ===", flush=True)
        for nom, f in fonctions(n).items():
            t0 = time.time()
            wp, sp = poids_min(f, tp, n)
            wl, sl = poids_min(f, tl_, n)
            if wp is None or wl is None:
                print(f"  {nom:16s} : positif={wp or sp}  "
                      f"litteraux={wl or sl}", flush=True)
                continue
            ratio = wp / wl if wl else float("inf")
            print(f"  {nom:16s} : W_positif = {wp:3d}   "
                  f"W_litteraux = {wl:3d}   rapport = {ratio:.2f}   "
                  f"({time.time()-t0:.0f}s, les deux re-verifies)",
                  flush=True)


if __name__ == "__main__":
    main()
