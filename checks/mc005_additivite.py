# -*- coding: utf-8 -*-
"""MC-005 — L'additivité de W sous combinaison à variables disjointes :
formalisation et mesure.

La question unique sur laquelle MC-004 a fait converger le front MC : la
totalisation à la HOS18-Th.16 pour SYM+ exige que le coût de structures
disjointes s'ADDITIONNE (pas de partage). On mesure W(f ⋄ g) contre
W(f) + W(g) pour quatre combineurs sur variables disjointes :

  ∧, ∨, ⊕   : h(x, y) = f(x) ⋄ g(y)                (n_f + n_g variables)
  MUX       : h(z, x, y) = f(x) si z = 1, g(y) si z = 0   (1 + n_f + n_g)
              — la forme « sélecteur » du schéma Th.16.

Deux bornes GÉNÉRIQUES prouvées (fiche MC-005 §1), vérifiées ici :
  (B1) appariement : pour tout combineur par classes sur variables
       disjointes, W(h) ≤ W(f) + (V_f + 1)·W(g), V_f = valeur max d'un
       séparateur optimal de f (≤ W(f)) — le témoin p_f + (V_f+1)·p_g rend
       la paire de classes lisible dans la valeur.
  (B2) restriction : si une tranche y := y₀ de h réalise f, alors
       W(h) ≥ W(f) — la restriction d'un séparateur est un séparateur à
       décalage constant près (le décalage = poids des monômes purs-y
       actifs en y₀, sans effet sur la disjonction).

Protocole : W exact par force brute (approfondissement itératif, ≤ 4 vars)
et par CP-SAT canal de valeurs (5-6 vars, OPTIMAL exigé, témoin re-vérifié
par évaluation indépendante). Exhaustif sur les paires de fonctions non
constantes à 2+2 variables ; famille NOR à 2+2 et 3+3 (re-vérification des
points F_m d'A-013) ; aucune extrapolation (q.12).
"""
import sys
import time
from itertools import combinations_with_replacement

try:
    from ortools.sat.python import cp_model
except ImportError:
    cp_model = None


# ------------------------------------------------------------ W par force brute
def W_brute(uns, nvars, cap):
    N = 1 << nvars
    su = set(uns)
    monomes = list(range(1, N))
    for s in range(0, cap + 1):
        for combo in combinations_with_replacement(monomes, s):
            coeffs = {}
            for S in combo:
                coeffs[S] = coeffs.get(S, 0) + 1
            v1, v0 = set(), set()
            ok = True
            for x in range(N):
                p = sum(c for S, c in coeffs.items() if S & x == S)
                if x in su:
                    if p in v0:
                        ok = False
                        break
                    v1.add(p)
                else:
                    if p in v1:
                        ok = False
                        break
                    v0.add(p)
            if ok:
                return s, coeffs
    return None, None


# ------------------------------------------------------------ W par CP-SAT
def W_cpsat(uns, nvars, cap, tl=180):
    N = 1 << nvars
    zeros = [x for x in range(N) if x not in set(uns)]
    monomes = list(range(1, N))
    model = cp_model.CpModel()
    a = {S: model.NewIntVar(0, cap, f"a{S}") for S in monomes}
    tot = model.NewIntVar(0, cap, "tot")
    model.Add(tot == sum(a.values()))
    val = {}
    for x in range(N):
        val[x] = model.NewIntVar(0, cap, f"v{x}")
        actifs = [a[S] for S in monomes if S & x == S]
        model.Add(val[x] == (sum(actifs) if actifs else 0))
    for u in uns:
        for v in zeros:
            model.Add(val[u] != val[v])
    model.Minimize(tot)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tl
    solver.parameters.num_search_workers = 8
    st = solver.Solve(model)
    if st == cp_model.OPTIMAL:
        temoin = {S: solver.Value(a[S]) for S in monomes if solver.Value(a[S])}
        # re-vérification indépendante du témoin
        su = set(uns)
        v1, v0 = set(), set()
        for x in range(N):
            p = sum(c for S, c in temoin.items() if S & x == S)
            (v1 if x in su else v0).add(p)
        assert not (v1 & v0) and sum(temoin.values()) == solver.Value(tot)
        return solver.Value(tot), "OPTIMAL"
    return (solver.Value(tot) if st == cp_model.FEASIBLE else None), str(st)


def W_exact(uns, nvars, cap=None, tl=180):
    """Force brute jusqu'à 4 variables, CP-SAT au-delà."""
    if cap is None:
        cap = (1 << nvars) - 1
    if nvars <= 4:
        w, _ = W_brute(uns, nvars, cap)
        return w, "BRUTE"
    return W_cpsat(uns, nvars, cap, tl)


# ------------------------------------------------------------ combineurs
def uns_de(masque, n):
    return [x for x in range(1 << n) if masque >> x & 1]


def combi(mf, nf, mg, ng, op):
    """Table de h = f ⋄ g sur nf + ng variables (x = bits bas, y = bits hauts)."""
    uns = []
    for y in range(1 << ng):
        gv = mg >> y & 1
        for x in range(1 << nf):
            fv = mf >> x & 1
            h = {"and": fv & gv, "or": fv | gv, "xor": fv ^ gv}[op]
            if h:
                uns.append(x | (y << nf))
    return uns


def mux(mf, nf, mg, ng):
    """h(z, x, y) = f(x) si z = 1, g(y) si z = 0 — z = bit de poids fort."""
    nv = 1 + nf + ng
    uns = []
    for z in (0, 1):
        for y in range(1 << ng):
            for x in range(1 << nf):
                v = (mf >> x & 1) if z else (mg >> y & 1)
                if v:
                    uns.append(x | (y << nf) | (z << (nf + ng)))
    return uns


def V_max_optimal(uns, nvars):
    """Valeur maximale d'un séparateur optimal (pour la borne B1) : on
    reprend le témoin de la force brute (4 vars max)."""
    w, coeffs = W_brute(uns, nvars, (1 << nvars) - 1)
    vmax = max(sum(c for S, c in coeffs.items() if S & x == S)
               for x in range(1 << nvars))
    return w, vmax


# ------------------------------------------------------------ campagnes
def campagne_2p2():
    """Exhaustif : toutes les paires (f, g) non constantes sur 2+2 variables."""
    fs = [m for m in range(1, 15)]  # 14 non constantes sur 2 vars
    W2 = {}
    for m in fs:
        W2[m], _ = W_brute(uns_de(m, 2), 2, 15)
    stats = {op: {"sub": 0, "egal": 0, "super": 0, "pire_sub": None,
                  "pire_super": None} for op in ("and", "or", "xor", "mux")}
    t0 = time.time()
    paires = [(a, b) for i, a in enumerate(fs) for b in fs[i:]]
    for k, (mf, mg) in enumerate(paires):
        somme = W2[mf] + W2[mg]
        for op in ("and", "or", "xor"):
            uns = combi(mf, 2, mg, 2, op)
            if not uns or len(uns) == 16:   # h constante : W = 0, hors sujet
                continue
            w, st = W_exact(uns, 4)
            d = w - somme
            cle = "sub" if d < 0 else ("egal" if d == 0 else "super")
            stats[op][cle] += 1
            if d < 0 and (stats[op]["pire_sub"] is None or d < stats[op]["pire_sub"][0]):
                stats[op]["pire_sub"] = (d, mf, mg, w, somme)
            if d > 0 and (stats[op]["pire_super"] is None or d > stats[op]["pire_super"][0]):
                stats[op]["pire_super"] = (d, mf, mg, w, somme)
        # MUX (5 variables, CP-SAT)
        uns = mux(mf, 2, mg, 2)
        w, st = W_exact(uns, 5)
        if st not in ("OPTIMAL", "BRUTE"):
            print(f"  MUX({mf},{mg}) NON CONCLU ({st})")
            continue
        d = w - somme
        cle = "sub" if d < 0 else ("egal" if d == 0 else "super")
        stats["mux"][cle] += 1
        if d < 0 and (stats["mux"]["pire_sub"] is None or d < stats["mux"]["pire_sub"][0]):
            stats["mux"]["pire_sub"] = (d, mf, mg, w, somme)
        if d > 0 and (stats["mux"]["pire_super"] is None or d > stats["mux"]["pire_super"][0]):
            stats["mux"]["pire_super"] = (d, mf, mg, w, somme)
        if (k + 1) % 21 == 0:
            print(f"  … {k+1}/{len(paires)} paires [{time.time()-t0:.0f}s]")
    print(f"\n=== EXHAUSTIF 2+2 ({len(paires)} paires non ordonnées) ===")
    for op in ("and", "or", "xor", "mux"):
        s = stats[op]
        tot = s["sub"] + s["egal"] + s["super"]
        print(f"{op.upper():4} : sous-additif {s['sub']}/{tot}, égal {s['egal']}/{tot}, "
              f"super {s['super']}/{tot}")
        if s["pire_sub"]:
            d, mf, mg, w, so = s["pire_sub"]
            print(f"       pire sous-additivité : f={mf}, g={mg} → W(h)={w} vs somme={so} (écart {d})")
        if s["pire_super"]:
            d, mf, mg, w, so = s["pire_super"]
            print(f"       pire super-additivité : f={mf}, g={mg} → W(h)={w} vs somme={so} (écart +{d})")
    return stats


def verif_bornes_2p2():
    """Vérifie B1 (appariement) et B2 (restriction) sur toutes les paires 2+2."""
    fs = [m for m in range(1, 15)]
    infos = {}
    for m in fs:
        infos[m] = V_max_optimal(uns_de(m, 2), 2)  # (W, Vmax)
    viol_b1, viol_b2, n_tests = 0, 0, 0
    for mf in fs:
        for mg in fs:
            wf, vf = infos[mf]
            wg, _ = infos[mg]
            borne_b1 = wf + (vf + 1) * wg
            for op in ("and", "or", "xor"):
                uns = combi(mf, 2, mg, 2, op)
                if not uns or len(uns) == 16:
                    continue
                w, _ = W_exact(uns, 4)
                n_tests += 1
                if w > borne_b1:
                    viol_b1 += 1
                    print(f"  VIOLATION B1 : {op}({mf},{mg}) W={w} > {borne_b1}")
                if w < max(wf, wg):
                    viol_b2 += 1
                    print(f"  VIOLATION B2 : {op}({mf},{mg}) W={w} < max({wf},{wg})")
    print(f"\n=== BORNES B1/B2 sur 2+2 : {n_tests} tests — "
          f"violations B1 : {viol_b1}, violations B2 : {viol_b2} ===")


def campagne_nor():
    """La famille NOR : re-vérification des points A-013 et extension."""
    print("\n=== FAMILLE NOR (points exacts) ===")
    for m in (2, 3):
        nor = 1  # masque du point 0^m
        w, st = W_exact(uns_de(nor, m), m)
        print(f"W(NOR_{m}) = {w} [{st}]")
    # F_m = NOR_m ⊕ NOR_m (2m variables)
    for m, attendu in ((2, 6), (3, 14)):
        uns = combi(1, m, 1, m, "xor")
        w, st = W_exact(uns, 2 * m, tl=600)
        ok = "CONFORME A-013" if w == attendu else f"ECART vs A-013 ({attendu})"
        print(f"W(NOR_{m} ⊕ NOR_{m}) = {w} [{st}] — {ok} ; somme = {2*m} → "
              f"écart {'+' if w-2*m>=0 else ''}{w-2*m}")
    # les trois autres combineurs à 2+2 sur NOR_2 (référence)
    for op in ("and", "or"):
        uns = combi(1, 2, 1, 2, op)
        w, st = W_exact(uns, 4)
        print(f"W(NOR_2 {op} NOR_2) = {w} [{st}] ; somme = 4")
    uns = mux(1, 2, 1, 2)
    w, st = W_exact(uns, 5)
    print(f"W(MUX(NOR_2, NOR_2)) = {w} [{st}] ; somme = 4")
    # MUX à 3+3 : le point de taille suivante pour le sélecteur
    uns = mux(1, 3, 1, 3)
    w, st = W_exact(uns, 7, tl=900)
    print(f"W(MUX(NOR_3, NOR_3)) = {w} [{st}] ; somme = 6")


if __name__ == "__main__":
    quel = sys.argv[1] if len(sys.argv) > 1 else "tout"
    if quel in ("tout", "2p2"):
        campagne_2p2()
    if quel in ("tout", "bornes"):
        verif_bornes_2p2()
    if quel in ("tout", "nor"):
        campagne_nor()
