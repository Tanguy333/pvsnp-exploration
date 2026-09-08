# -*- coding: utf-8 -*-
r"""PR-007 — Contre-vérification exécutable de la candidature « 21e ligne »
(bornes inférieures de circuits généraux / élimination de portes).

Implémentation INDÉPENDANTE de checks/pr002_sre_parite.py (qui utilisait
CP-SAT et a produit XOR_3 = 8, XOR_4 ∈ [10, 12] en NOT-payant) : ici
synthèse exacte par SAT (pysat / CaDiCaL), encodage de type
Kojevnikov-Kulikov-Yaroslavtsev 2009 / Knuth 7.2.2.2 (sélection d'une
paire d'entrées par porte, 4 bits de fonction par porte, valeurs par
ligne de table), témoin RE-VÉRIFIÉ par simulation indépendante ;
UNSAT = borne inférieure certifiée par le solveur (sans DRAT — réserve
habituelle du dépôt ; les cassages de symétrie sont désactivables par
--nosym pour la contre-épreuve).

ANTÉRIORITÉ DÉCLARÉE AVANT CALCUL (directive permanente) :
  - U2 (toutes portes binaires sauf XOR/XNOR, négations absorbées) :
    C(XOR_n) = 3(n-1) — Schnorr 1974 (attribution consignée PR-002).
  - B2 (toutes portes binaires), n = 4 : max C(f) = 7 sur les 222 classes
    NPN — Knuth, TAOCP 7.1.2 — RÉPLICATION VÉRIFIANTE DÉCLARÉE.
  - NOT-payant ({AND, OR, NOT}, chaque porte coûte 1, entrées gratuites,
    convention PR-002) : Markov 1958 — nombre minimal de NOT =
    ceil(log2(d(f)+1)), d(f) = max de chutes 1->0 sur une chaîne
    croissante ; d(XOR_4) = 2 => >= 2 NOT. Tout circuit NOT-payant
    donne, en absorbant les NOT dans les portes voisines, un circuit U2
    de même nombre de portes binaires => >= 9 portes binaires (Schnorr).
    Donc C_NOT-payant(XOR_4) >= 11 PAR THÉORÈME (l'intervalle PR-002
    [10, 12] se resserre à [11, 12] avant tout solveur). Red'kin 1973
    (valeur exacte 4(n-1) dans cette base) : à confirmer sur texte.

Modes :
  markov      d(XOR_n) par force brute + borne de Markov (n <= 6)
  counting    seuil de comptage (Shannon) : premier n où une fonction
              NON explicite exige > 3n portes (borne grossière, exacte
              comme majorant du nombre de chaînes)
  xor         XOR_n, base U2 | NOTPAY, k croissant (ou --k fixé)
  b4_all      les 222 classes NPN de B4 sur B2 : coût exact de chacune,
              histogrammes (classes, fonctions), maximum
"""
from __future__ import annotations

import argparse
import itertools
import math
import os
import sys
import time

# ----------------------------------------------------------------------
# Bases
# ----------------------------------------------------------------------
# Une porte binaire est décrite par (f00, f01, f10, f11) = f(a, b).
DEGENERES = {(0, 0, 0, 0), (1, 1, 1, 1),   # constantes
             (0, 0, 1, 1), (1, 1, 0, 0),   # a, non a
             (0, 1, 0, 1), (1, 0, 1, 0)}   # b, non b
XOR_PAT, XNOR_PAT = (0, 1, 1, 0), (1, 0, 0, 1)
AND_PAT, OR_PAT = (0, 0, 0, 1), (0, 1, 1, 1)

NOMS = {(0, 0, 0, 1): "AND", (0, 1, 1, 1): "OR", (0, 1, 1, 0): "XOR",
        (1, 0, 0, 1): "XNOR", (0, 1, 0, 0): "~a&b", (0, 0, 1, 0): "a&~b",
        (1, 1, 1, 0): "NAND", (1, 0, 0, 0): "NOR", (1, 1, 0, 1): "~a|b",
        (1, 0, 1, 1): "a|~b"}


def patterns_interdits(base):
    if base == "B2":
        return set(DEGENERES)
    if base == "U2":
        return set(DEGENERES) | {XOR_PAT, XNOR_PAT}
    if base == "NOTPAY":   # portes binaires = AND, OR seulement
        tous = set(itertools.product((0, 1), repeat=4))
        return tous - {AND_PAT, OR_PAT}
    raise ValueError(base)


# ----------------------------------------------------------------------
# Encodage SAT
# ----------------------------------------------------------------------
class Synthese:
    """Existe-t-il un circuit de k portes (base donnée) sur n entrées
    calculant target (liste de 2^n bits) ? Entrées gratuites ; pas de
    constantes (inutiles dans un circuit minimal d'une fonction non
    constante : une porte à entrée constante est une projection, une
    négation ou une constante, absorbable) ; sortie = dernière porte."""

    def __init__(self, n, k, target, base, sym=True, nb_not=None):
        self.n, self.k, self.target, self.base = n, k, target, base
        self.sym, self.nb_not = sym, nb_not
        self.nv = 0
        self.cl = []
        self.T = 1 << n
        self.construire()

    def var(self):
        self.nv += 1
        return self.nv

    def construire(self):
        n, k, T = self.n, self.k, self.T
        self.s = []      # s[i][(j,l)] : porte i lit (j, l), j < l
        self.f = []      # f[i] = [f00, f01, f10, f11]
        self.v = []      # v[i][t]
        self.u = []      # NOTPAY : u[i][j] : porte i = NOT(j)
        self.isnot = []
        interdits = patterns_interdits(self.base)
        for i in range(k):
            m = n + i   # nœuds disponibles : 0..m-1
            paires = {(j, l): self.var() for j in range(m) for l in range(j + 1, m)}
            self.s.append(paires)
            self.f.append([self.var() for _ in range(4)])
            self.v.append([self.var() for _ in range(T)])
            if self.base == "NOTPAY":
                self.u.append({j: self.var() for j in range(m)})
                self.isnot.append(self.var())
            # exactement une sélection
            sels = list(paires.values()) + (list(self.u[i].values()) if self.base == "NOTPAY" else [])
            self.cl.append(sels)
            for a, b in itertools.combinations(sels, 2):
                self.cl.append([-a, -b])
            # patterns de fonction interdits (portes binaires)
            for pat in interdits:
                self.cl.append([(-self.f[i][q] if pat[q] else self.f[i][q]) for q in range(4)])
            if self.base == "NOTPAY":
                # isnot <-> OR(u)
                for j, uj in self.u[i].items():
                    self.cl.append([-uj, self.isnot[i]])
                self.cl.append([-self.isnot[i]] + list(self.u[i].values()))
                # sémantique NOT : v[i][t] = non x_j(t)
                for j, uj in self.u[i].items():
                    for t in range(T):
                        xj = self.lit(j, t)
                        if xj is True:
                            self.cl.append([-uj, -self.v[i][t]])
                        elif xj is False:
                            self.cl.append([-uj, self.v[i][t]])
                        else:
                            self.cl.append([-uj, -xj, -self.v[i][t]])
                            self.cl.append([-uj, xj, self.v[i][t]])
                # pas de NOT d'un NOT (inutile dans un circuit minimal)
                for j in range(n, m):
                    self.cl.append([-self.u[i][j], -self.isnot[j - n]])
            # sémantique des portes binaires
            for (j, l), sv in paires.items():
                for t in range(T):
                    xj, xl = self.lit(j, t), self.lit(l, t)
                    for a in (0, 1):
                        if xj is True and a == 0 or xj is False and a == 1:
                            continue
                        for b in (0, 1):
                            if xl is True and b == 0 or xl is False and b == 1:
                                continue
                            ante = [-sv]
                            if xj not in (True, False):
                                ante.append(-xj if a else xj)
                            if xl not in (True, False):
                                ante.append(-xl if b else xl)
                            fab = self.f[i][2 * a + b]
                            self.cl.append(ante + [-self.v[i][t], fab])
                            self.cl.append(ante + [self.v[i][t], -fab])
        # sortie
        for t in range(T):
            self.cl.append([self.v[k - 1][t] if self.target[t] else -self.v[k - 1][t]])
        # nombre de NOT imposé (justifié par théorème seulement)
        if self.base == "NOTPAY" and self.nb_not is not None:
            from pysat.card import CardEnc, EncType
            cnf = CardEnc.equals(lits=self.isnot, bound=self.nb_not,
                                 top_id=self.nv, encoding=EncType.seqcounter)
            self.cl.extend(cnf.clauses)
            self.nv = max(self.nv, cnf.nv)
        if self.sym:
            self.symetries()

    def lit(self, node, t):
        """Valeur du nœud node sur la ligne t : True/False (entrée) ou
        littéral (porte)."""
        if node < self.n:
            return bool((t >> node) & 1)
        return self.v[node - self.n][t]

    def symetries(self):
        n, k = self.n, self.k
        # (1) toute porte non finale est lue par une porte ultérieure
        for i in range(k - 1):
            node = n + i
            lecteurs = []
            for i2 in range(i + 1, k):
                lecteurs += [sv for (j, l), sv in self.s[i2].items() if l == node or j == node]
                if self.base == "NOTPAY":
                    lecteurs.append(self.u[i2][node])
            self.cl.append(lecteurs)
        # (2) pas deux portes binaires identiques (même paire, même fonction)
        for i in range(k):
            for i2 in range(i + 1, k):
                for p, sv in self.s[i].items():
                    if p not in self.s[i2]:
                        continue
                    d = [self.var() for _ in range(4)]
                    for q in range(4):
                        a, b = self.f[i][q], self.f[i2][q]
                        # d_q -> (a xor b)
                        self.cl.append([-d[q], a, b])
                        self.cl.append([-d[q], -a, -b])
                    self.cl.append([-sv, -self.s[i2][p]] + d)
        # (3) ordre lexicographique des paires de portes consécutives
        #     indépendantes : si la porte i+1 ne lit pas la porte i,
        #     paire(i) <= paire(i+1)
        for i in range(k - 1):
            node = n + i
            for p, sv in self.s[i].items():
                for q, sv2 in self.s[i + 1].items():
                    if q[1] >= node or q[0] >= node:
                        continue          # lit la porte i : sans contrainte
                    if q < p:
                        self.cl.append([-sv, -sv2])

    def resoudre(self, solveur="cadical195", conflits=None):
        from pysat.solvers import Solver
        with Solver(name=solveur, bootstrap_with=self.cl) as S:
            if conflits is not None:
                S.conf_budget(conflits)
                res = S.solve_limited()
            else:
                res = S.solve()
            if res is None:
                return None, "NON CONCLU (budget)"
            if not res:
                return None, "UNSAT"
            modele = set(x for x in S.get_model() if x > 0)
        circ = []
        for i in range(self.k):
            if self.base == "NOTPAY" and self.isnot[i] in modele:
                j = next(j for j, uj in self.u[i].items() if uj in modele)
                circ.append(("NOT", j, j))
                continue
            (j, l) = next(p for p, sv in self.s[i].items() if sv in modele)
            pat = tuple(int(self.f[i][q] in modele) for q in range(4))
            circ.append((pat, j, l))
        return circ, "SAT"


def simuler(circ, n, t):
    """Re-vérification INDÉPENDANTE du témoin sur la ligne t."""
    vals = [(t >> j) & 1 for j in range(n)]
    for op, j, l in circ:
        if op == "NOT":
            vals.append(1 - vals[j])
        else:
            vals.append(op[2 * vals[j] + vals[l]])
    return vals[-1]


def verifier(circ, n, target):
    for t in range(1 << n):
        if simuler(circ, n, t) != target[t]:
            return False
    return True


def afficher(circ, n):
    noms = [f"x{j}" for j in range(n)]
    for i, (op, j, l) in enumerate(circ):
        noms.append(f"g{i}")
        if op == "NOT":
            print(f"      g{i} = NOT({noms[j]})")
        else:
            print(f"      g{i} = {NOMS.get(op, op)}({noms[j]}, {noms[l]})")


def cout_zero(target, n):
    T = 1 << n
    if all(target) or not any(target):
        return "constante"
    for j in range(n):
        proj = [(t >> j) & 1 for t in range(T)]
        if target == proj:
            return f"x{j}"
        if target == [1 - b for b in proj]:
            return f"non x{j}"
    return None


def minimum(target, n, base, kmin=1, kmax=13, sym=True, nb_not=None,
            solveur="cadical195", conflits=None, verbose=True):
    z = cout_zero(target, n)
    if z is not None:
        if verbose:
            print(f"  coût 0 ({z})")
        return 0, []
    for k in range(kmin, kmax + 1):
        t0 = time.time()
        syn = Synthese(n, k, target, base, sym=sym, nb_not=nb_not)
        circ, st = syn.resoudre(solveur, conflits)
        dt = time.time() - t0
        if verbose:
            print(f"  k = {k:2} : {st:18} [{dt:8.1f} s ; {syn.nv} vars, {len(syn.cl)} clauses]",
                  flush=True)
        if st == "SAT":
            assert verifier(circ, n, target), "TÉMOIN FAUX — instrument en défaut"
            if verbose:
                print(f"  >>> MINIMUM = {k} ; témoin re-vérifié sur {1 << n} lignes :")
                afficher(circ, n)
            return k, circ
        if st != "UNSAT":
            return None, st
    return None, f"> {kmax}"


# ----------------------------------------------------------------------
# Fonctions cibles et classes NPN
# ----------------------------------------------------------------------
def xor_table(n):
    return [bin(t).count("1") & 1 for t in range(1 << n)]


def classes_npn(n=4):
    """Classes NPN de toutes les fonctions à n variables (numpy).
    Rend {canonique: taille}."""
    import numpy as np
    T = 1 << n
    NF = 1 << T
    fs = np.arange(NF, dtype=np.int64)
    F = ((fs[:, None] >> np.arange(T, dtype=np.int64)[None, :]) & 1).astype(np.int8)
    poids = (np.int64(1) << np.arange(T, dtype=np.int64))
    canon = fs.copy()
    for perm in itertools.permutations(range(n)):
        for masque in range(T):
            idx = np.empty(T, dtype=np.int64)
            for t in range(T):
                # T(t) : permuter les bits puis xor masque
                bits = [(t >> j) & 1 for j in range(n)]
                t2 = 0
                for j in range(n):
                    t2 |= bits[perm[j]] << j
                idx[t] = t2 ^ masque
            G = F[:, idx]
            g1 = (G.astype(np.int64) * poids[None, :]).sum(axis=1)
            g0 = ((1 - G).astype(np.int64) * poids[None, :]).sum(axis=1)
            canon = np.minimum(canon, np.minimum(g1, g0))
    reps, tailles = np.unique(canon, return_counts=True)
    return {int(r): int(c) for r, c in zip(reps, tailles)}


# ----------------------------------------------------------------------
# Markov et comptage
# ----------------------------------------------------------------------
def markov_d(target, n):
    """d(f) = max de chutes 1->0 le long d'une chaîne croissante."""
    T = 1 << n
    D = [0] * T
    for t in range(1, T):
        best = 0
        for j in range(n):
            if (t >> j) & 1:
                p = t ^ (1 << j)
                best = max(best, D[p] + (1 if target[p] == 1 and target[t] == 0 else 0))
        D[t] = best
    return max(D)


def mode_markov(args):
    print("Théorème de Markov (1958) : nombre minimal de NOT = ceil(log2(d(f)+1)).")
    for n in range(2, 7):
        d = markov_d(xor_table(n), n)
        print(f"  XOR_{n} : d = {d} (attendu floor(n/2) = {n // 2}) -> "
              f"NOT >= {math.ceil(math.log2(d + 1))} ; "
              f"+ Schnorr 3(n-1) = {3 * (n - 1)} portes binaires -> "
              f"C_NOT-payant >= {3 * (n - 1) + math.ceil(math.log2(d + 1))}")


def mode_counting(args):
    print("Comptage (Shannon) : nombre de chaînes de s portes sur n entrées "
          "<= prod_{i<s} C(n+i,2)*10 ; si sum_{s'<=s} < 2^(2^n), une fonction "
          "exige > s portes.")
    print(f"  {'n':>3} {'3n':>4} {'s*(n)':>6}  (s* = plus grand s tel que toutes "
          f"les fonctions ne tiennent pas en <= s portes ; > 3n ?)")
    for n in range(4, 13):
        log_total = None      # log2 de la somme, en domaine logarithmique
        s = 0
        while True:
            s += 1
            log_chaines = sum(math.log2(math.comb(n + i, 2) * 10) for i in range(s))
            if log_total is None:
                log_total = log_chaines
            else:
                m = max(log_total, log_chaines)
                log_total = m + math.log2(2 ** (log_total - m) + 2 ** (log_chaines - m))
            if log_total >= (1 << n):
                break
        sstar = s - 1
        print(f"  {n:>3} {3 * n:>4} {sstar:>6}  {'OUI' if sstar >= 3 * n else 'non'}")


def mode_xor(args):
    n, base = args.n, args.base
    target = xor_table(n)
    print(f"--- XOR_{n}, base {base}, sym={not args.nosym}, nb_not={args.nb_not}, "
          f"solveur {args.solver} (pid {os.getpid()}) ---")
    if args.k is not None:
        k = args.k
        t0 = time.time()
        syn = Synthese(n, k, target, base, sym=not args.nosym, nb_not=args.nb_not)
        print(f"  k = {k} : {syn.nv} vars, {len(syn.cl)} clauses — résolution...", flush=True)
        circ, st = syn.resoudre(args.solver, args.conflits)
        print(f"  k = {k} : {st} [{time.time() - t0:.1f} s]", flush=True)
        if st == "SAT":
            assert verifier(circ, n, target), "TÉMOIN FAUX"
            print("  témoin re-vérifié :")
            afficher(circ, n)
        return
    minimum(target, n, base, kmin=args.kmin, kmax=args.kmax, sym=not args.nosym,
            nb_not=args.nb_not, solveur=args.solver, conflits=args.conflits)


def mode_b4_all(args):
    n = 4
    t0 = time.time()
    cls = classes_npn(n)
    print(f"Classes NPN de B4 : {len(cls)} (attendu 222) ; "
          f"somme des tailles = {sum(cls.values())} (attendu 65536) "
          f"[{time.time() - t0:.1f} s]", flush=True)
    assert len(cls) == 222 and sum(cls.values()) == 65536
    couts = {}
    hist_cls, hist_fn = {}, {}
    t0 = time.time()
    for idx, (rep, taille) in enumerate(sorted(cls.items())):
        target = [(rep >> t) & 1 for t in range(1 << n)]
        k, circ = minimum(target, n, "B2", kmin=1, kmax=8, sym=not args.nosym,
                          solveur=args.solver, conflits=args.conflits, verbose=False)
        if k is None:
            print(f"  classe {rep:#06x} : NON CONCLU ({circ})", flush=True)
            continue
        couts[rep] = k
        hist_cls[k] = hist_cls.get(k, 0) + 1
        hist_fn[k] = hist_fn.get(k, 0) + taille
        if args.verbose or k >= 7:
            print(f"  [{idx + 1:3}/222] classe {rep:#06x} (taille {taille:5}) : C = {k}", flush=True)
    print(f"\nTemps total : {time.time() - t0:.0f} s")
    print("Histogramme par CLASSES NPN (coût : nombre de classes) :")
    for k in sorted(hist_cls):
        print(f"  C = {k} : {hist_cls[k]} classes")
    print("Histogramme par FONCTIONS (coût : nombre de fonctions sur 65536) :")
    for k in sorted(hist_fn):
        print(f"  C = {k} : {hist_fn[k]} fonctions")
    print(f"MAXIMUM sur B4 : C = {max(couts.values())} "
          f"(Knuth 7.1.2 : 7 attendu) ; classes non conclues : {222 - len(couts)}")
    print("Classes de coût maximal :")
    for rep, k in sorted(couts.items()):
        if k == max(couts.values()):
            print(f"  {rep:#06x} (taille {cls[rep]})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["markov", "counting", "xor", "b4_all"])
    ap.add_argument("--n", type=int, default=4)
    ap.add_argument("--base", default="U2", choices=["B2", "U2", "NOTPAY"])
    ap.add_argument("--k", type=int, default=None, help="palier unique")
    ap.add_argument("--kmin", type=int, default=1)
    ap.add_argument("--kmax", type=int, default=13)
    ap.add_argument("--nb-not", dest="nb_not", type=int, default=None,
                    help="NOTPAY : impose exactement ce nombre de NOT (justifier par théorème)")
    ap.add_argument("--nosym", action="store_true", help="désactive les cassages de symétrie")
    ap.add_argument("--solver", default="cadical195")
    ap.add_argument("--conflits", type=int, default=None, help="budget de conflits par palier")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()
    {"markov": mode_markov, "counting": mode_counting,
     "xor": mode_xor, "b4_all": mode_b4_all}[args.mode](args)


if __name__ == "__main__":
    main()
