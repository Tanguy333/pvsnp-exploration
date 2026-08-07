# -*- coding: utf-8 -*-
"""MC-007 — La carte du partage en géométrie de FIBRE PARTAGÉE.

Le verrou requalifié par MC-006 : une totalisation polynomiale exige des
fibres à coordonnées PARTAGÉES (un bloc Y commun), géométrie où les classes
de charge de MC-006 se recouvrent. Question : quand le coût W se
partage-t-il entre fibres ?

Objet : h(x, y) = φ_x(y) — base x (t bits, ici t = 1 sauf mention), fibre
y (s bits) partagée. C'est EXACTEMENT une fonction arbitraire sur 1 + s
variables lue par tranches : l'espace est donc EXHAUSTIVEMENT mesurable.
Écart : g(h) := W(h) − [W(φ₀) + W(φ₁)].

Faits d'encadrement (prouvés en une ligne, vérifiés ici) :
  * φ répétée (φ₀ = φ₁ = φ) : W(h) = W(φ) — partage TOTAL, g = −W(φ)
    (≤ : séparateur pur-Y ; ≥ : restriction B2).
  * B2 : W(h) ≥ max(W(φ₀), W(φ₁)) toujours — le partage est borné :
    g ≥ −min(W₀, W₁).

Campagnes :
  s2  : exhaustif s = 2 — les 256 h sur 3 variables (W par force brute),
        carte complète de g par catégorie (répétée / complémentaire /
        distinctes non constantes / avec tranche constante).
  s3  : exhaustif s = 3 — les 65 536 h sur 4 variables (W par CP-SAT sur
        les 3 984 classes de S₄ seul — compte corrigé par VER-MC-1 : le
        « 1 992 » initial était le compte S₄×complément d'A-013, recopié à
        tort — propagé par orbites), même carte.
  struct : cas structurés — marqueur bon marché (φ, [y = 1^s]) pour toute
        φ ; points épars à la HOS18 ([y = c₀] vs [y = c₁], c₀ ≠ c₁) ;
        up-cubes disjoints vs emboîtés.
  t2  : base 2 bits (4 fibres, 6 variables) — échantillon CP-SAT de
        quadruplets de fibres distinctes : W(h) vs Σ des quatre.

Conventions : bit 0 = base x ; bits 1..s = fibre y. φ₀ = tranche x = 0,
φ₁ = tranche x = 1. Graine : 20260807. Aucune extrapolation (q.12).
"""
import random
import sys
import time
from itertools import combinations_with_replacement, permutations

from ortools.sat.python import cp_model


# ------------------------------------------------------------------ W exact
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
                return s
    return None


def W_cpsat(uns, nvars, cap, tl=300):
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
    if st != cp_model.OPTIMAL:
        return None, str(st)
    temoin = {S: solver.Value(a[S]) for S in monomes if solver.Value(a[S])}
    su = set(uns)
    v1, v0 = set(), set()
    for x in range(N):
        p = sum(c for S, c in temoin.items() if S & x == S)
        (v1 if x in su else v0).add(p)
    assert not (v1 & v0) and sum(temoin.values()) == solver.Value(tot)
    return solver.Value(tot), "OPTIMAL"


def uns_de(masque, n):
    return [x for x in range(1 << n) if masque >> x & 1]


# ------------------------------------------- tables W exhaustives (n = 2, 3, 4)
def table_W(n, via="brute"):
    """W pour tous les masques sur n variables. n ≤ 3 : force brute directe.
    n = 4 : CP-SAT par classes S₄ + propagation par orbites."""
    N = 1 << n
    T = {}
    if n <= 3:
        for m in range(0, 1 << N):
            if m == 0 or m == (1 << N) - 1:
                T[m] = 0
                continue
            T[m] = W_brute(uns_de(m, n), n, N - 1)
        return T
    # n = 4 : classes sous permutation des variables
    def permute(m, perm):
        r = 0
        for x in range(N):
            if m >> x & 1:
                y = 0
                for i in range(n):
                    if x >> i & 1:
                        y |= 1 << perm[i]
                r |= 1 << y
        return r
    perms = list(permutations(range(n)))
    vus = {}
    t0 = time.time()
    fait = 0
    for m in range(0, 1 << N):
        if m in vus:
            continue
        orbite = {permute(m, p) for p in perms}
        if m == 0 or m == (1 << N) - 1:
            w = 0
        else:
            w, st = W_cpsat(uns_de(m, n), n, N - 1, tl=120)
            assert st == "OPTIMAL", f"masque {m} : {st}"
        for mm in orbite:
            vus[mm] = w
        fait += 1
        if fait % 200 == 0:
            print(f"    … {fait} classes [{time.time()-t0:.0f}s]")
    return vus


def tranches(h, s):
    """h : masque sur 1 + s variables (bit 0 = base). Renvoie (φ₀, φ₁)."""
    m0 = m1 = 0
    for y in range(1 << s):
        if h >> (y << 1) & 1:
            m0 |= 1 << y
        if h >> ((y << 1) | 1) & 1:
            m1 |= 1 << y
    return m0, m1


def carte(s, Wh_table, Wf_table):
    """La carte complète des écarts g(h) pour toutes les h sur 1+s vars."""
    N = 1 << s
    plein = (1 << N) - 1
    cats = {"repetee": {}, "complement": {}, "distinctes": {}, "constante": {}}
    pires, meilleurs = [], []
    for h in range(1 << (1 << (s + 1))):
        if h == 0 or h == (1 << (1 << (s + 1))) - 1:
            continue
        m0, m1 = tranches(h, s)
        w0, w1 = Wf_table[m0], Wf_table[m1]
        g = Wh_table[h] - (w0 + w1)
        if m0 in (0, plein) or m1 in (0, plein):
            cat = "constante"
        elif m0 == m1:
            cat = "repetee"
        elif m1 == plein ^ m0:
            cat = "complement"
        else:
            cat = "distinctes"
        cats[cat][g] = cats[cat].get(g, 0) + 1
        if cat == "distinctes":
            pires.append((g, h, m0, m1, Wh_table[h], w0, w1))
    pires.sort()
    return cats, pires[:6], pires[-3:]


def run_s(s):
    print(f"=== EXHAUSTIF s = {s} : les {1 << (1 << (s+1))} fonctions "
          f"sur {s+1} variables, lues par tranches ===")
    t0 = time.time()
    Wf = table_W(s)
    via = "CP-SAT par classes + orbites" if s + 1 == 4 else "force brute"
    Wh = table_W(s + 1)
    print(f"  tables W prêtes ({via}) [{time.time()-t0:.0f}s]")
    cats, pires, meilleurs = carte(s, Wh, Wf)
    for cat, dist in cats.items():
        if dist:
            print(f"  {cat:11} : g = {dict(sorted(dist.items()))}")
    # vérifications des faits d'encadrement
    rep = cats["repetee"]
    assert all(g < 0 for g in rep), "φ répétée : g devrait être −W(φ) < 0"
    tout = [g for d in cats.values() for g in d]
    print(f"  PIRES partages (distinctes) : "
          + " ; ".join(f"g={g} (h={h}, φ₀={m0} W={w0}, φ₁={m1} W={w1}, W(h)={wh})"
                       for g, h, m0, m1, wh, w0, w1 in pires))
    print(f"  MEILLEURS (distinctes) : "
          + " ; ".join(f"g={g} (h={h}, φ₀={m0}, φ₁={m1})"
                       for g, h, m0, m1, wh, w0, w1 in meilleurs))
    d = cats["distinctes"]
    n_tot = sum(d.values())
    n_sub = sum(v for g, v in d.items() if g < 0)
    n_super = sum(v for g, v in d.items() if g > 0)
    print(f"  BILAN distinctes non constantes : {n_sub}/{n_tot} sous-additives, "
          f"{d.get(0, 0)}/{n_tot} égales, {n_super}/{n_tot} super-additives")
    return Wf, Wh


def run_struct(Wf2, Wf3, Wh3, Wh4):
    print("\n=== CAS STRUCTURÉS (base 1 bit) — consultation des tables ===")
    for s, Wf, Wh in ((2, Wf2, Wh3), (3, Wf3, Wh4)):
        N = 1 << s
        marqueur = 1 << (N - 1)  # [y = 1^s] : monôme plein, W = 1
        gaps = {}
        for phi in range(1, (1 << N) - 1):
            h = 0
            for y in range(N):
                if phi >> y & 1:
                    h |= 1 << (y << 1)
                if marqueur >> y & 1:
                    h |= 1 << ((y << 1) | 1)
            g = Wh[h] - (Wf[phi] + 1)
            gaps[g] = gaps.get(g, 0) + 1
        print(f"  marqueur [y=1^{s}] (W=1) contre toute φ (s={s}) : "
              f"g = {dict(sorted(gaps.items()))}")
    # points épars à la HOS18 : [y = c₀] vs [y = c₁], c₀ ≠ c₁ (s = 3)
    res = {}
    for c0 in range(8):
        for c1 in range(8):
            if c0 == c1:
                continue
            phi0, phi1 = 1 << c0, 1 << c1
            h = 0
            for y in range(8):
                if phi0 >> y & 1:
                    h |= 1 << (y << 1)
                if phi1 >> y & 1:
                    h |= 1 << ((y << 1) | 1)
            g = Wh4[h] - (Wf3[phi0] + Wf3[phi1])
            res[g] = res.get(g, 0) + 1
    print(f"  points épars (s = 3, [y=c₀] vs [y=c₁], c₀ ≠ c₁) : "
          f"g = {dict(sorted(res.items()))} (56 paires ordonnées)")


def run_t2(n_ech=10):
    """CORRIGÉ (VER-MC-1, 2026-08-07) : la version initiale déclarait 6
    variables pour des points construits sur 4 bits (base 2 + fibre 2) —
    48 zéros fantômes gonflaient W et la conclusion consignée
    (« entièrement super-additif ») était un artefact d'encodage."""
    print("\n=== BASE 2 BITS (4 fibres partagées, s = 2, 4 variables) — échantillon ===")
    rng = random.Random(20260807)
    Wf = table_W(2)
    t0 = time.time()
    for k in range(n_ech):
        phis = [rng.randrange(1, 15) for _ in range(4)]
        h_uns = []
        for b in range(4):
            for y in range(4):
                if phis[b] >> y & 1:
                    h_uns.append(b | (y << 2))
        somme = sum(Wf[p] for p in phis)
        w, st = W_cpsat(h_uns, 4, 15, tl=600)
        if st != "OPTIMAL":
            print(f"  t2.{k} : NON CONCLU ({st})")
            continue
        print(f"  t2.{k} : φ = {phis} (Σ W = {somme}) → W(h) = {w}, "
              f"g = {w - somme}  [{time.time()-t0:.0f}s]")


if __name__ == "__main__":
    quel = sys.argv[1] if len(sys.argv) > 1 else "tout"
    Wf2 = Wf3 = Wh3 = Wh4 = None
    if quel in ("tout", "s2"):
        Wf2, Wh3 = run_s(2)
    if quel in ("tout", "s3"):
        Wf3, Wh4 = run_s(3)
    if quel in ("tout", "struct"):
        Wf2 = Wf2 or table_W(2)
        Wh3 = Wh3 or table_W(3)
        if Wf3 is None:
            Wf3 = table_W(3)
        if Wh4 is None:
            Wh4 = table_W(4)
        run_struct(Wf2, Wf3, Wh3, Wh4)
    if quel in ("tout", "t2"):
        run_t2()
