# -*- coding: utf-8 -*-
r"""PR-017 — Contre-vérification exécutable de la candidature n° 11 (entrée de
registre E-7 : « la classification algébrique des CSP »).

Implémentation INDÉPENDANTE : recherche SAT (pysat / CaDiCaL 1.9.5) d'un
polymorphisme f : A^m -> B satisfaisant une condition de mineur.
  Sig(Γ)    : s : A^4 -> A, polymorphisme de toutes les relations de Γ,
              s(a,r,e,a) = s(r,a,r,e) pour tous a, r, e  (Siggers 4-aire).
  Ols(A, B) : o : A^6 -> B, polymorphisme de (A, B) (arête -> arête),
              o(x,x,y,y,y,x) = o(x,y,x,y,x,y) = o(y,x,x,x,y,y)  (Olšák).
Encodage one-hot de f ; polymorphisme : pour chaque m-uplet de tuples de
R, l'image n'est pas un tuple hors de R (une clause par tuple interdit) ;
identités : égalité des vecteurs one-hot. Témoin re-vérifié par
simulation indépendante quand SAT.
Antériorité : Schaefer 1978, Hell-Nešetřil 1990 (contrôle), Siggers
2010, Kearnes-Marković-McKenzie 2014, Olšák 2017, BBKO 2021.
Usage : python -u checks/pr017_polymorphismes.py
"""
import itertools
import time

from pysat.solvers import Solver


def neq(k):
    return {(i, j) for i in range(k) for j in range(k) if i != j}


def boolrel(pred, ar):
    return {t for t in itertools.product((0, 1), repeat=ar) if pred(t)}


def clauses_rel(signs):
    """relation d'une clause booléenne : signs[i] = 1 pour x_i, 0 pour ¬x_i."""
    return boolrel(lambda t: any(t[i] == signs[i] for i in range(len(signs))), len(signs))


GABARITS = {
    "2-SAT": (2, [clauses_rel(s) for s in itertools.product((0, 1), repeat=2)]),
    "Horn-3": (2, [boolrel(lambda t: t[0] == 1, 1), boolrel(lambda t: t[0] == 0, 1),
                   clauses_rel((0, 0, 1)), clauses_rel((0, 0, 0))]),
    "XOR-3": (2, [boolrel(lambda t: sum(t) % 2 == 0, 3), boolrel(lambda t: sum(t) % 2 == 1, 3)]),
    "Z3-lin": (3, [{t for t in itertools.product(range(3), repeat=3) if sum(t) % 3 == c} for c in range(3)]),
    "K2": (2, [neq(2)]),
    "1-in-3": (2, [boolrel(lambda t: sum(t) == 1, 3)]),
    "NAE-3": (2, [boolrel(lambda t: 0 < sum(t) < 3, 3)]),
    "3-SAT": (2, [clauses_rel(s) for s in itertools.product((0, 1), repeat=3)]),
    "K3": (3, [neq(3)]),
}
ATTENDU = {"2-SAT": True, "Horn-3": True, "XOR-3": True, "Z3-lin": True, "K2": True,
           "1-in-3": False, "NAE-3": False, "3-SAT": False, "K3": False}


class Poly:
    def __init__(self, nA, nB, m):
        self.nA, self.nB, self.m = nA, nB, m
        self.pts = list(itertools.product(range(nA), repeat=m))
        self.idx = {p: i for i, p in enumerate(self.pts)}
        self.cl = []
        for p in self.pts:                      # exactement une valeur
            vs = [self.v(p, b) for b in range(nB)]
            self.cl.append(vs)
            self.cl += [[-a, -c] for a, c in itertools.combinations(vs, 2)]

    def v(self, p, b):
        return 1 + self.idx[p] * self.nB + b

    def polymorphe(self, RA, RB):
        RA = list(RA)
        ar = len(RA[0])
        hors = [t for t in itertools.product(range(self.nB), repeat=ar) if t not in RB]
        for cols in itertools.product(RA, repeat=self.m):
            # cols : m tuples de RA ; ligne i = (cols[0][i], ..., cols[m-1][i])
            lignes = [tuple(c[i] for c in cols) for i in range(ar)]
            for t in hors:
                self.cl.append([-self.v(lignes[i], t[i]) for i in range(ar)])

    def egal(self, p, q):
        if p == q:
            return
        for b in range(self.nB):
            self.cl.append([-self.v(p, b), self.v(q, b)])
            self.cl.append([self.v(p, b), -self.v(q, b)])

    def resoudre(self):
        with Solver(name="cadical195", bootstrap_with=self.cl) as S:
            if not S.solve():
                return None
            mod = set(x for x in S.get_model() if x > 0)
        return {p: next(b for b in range(self.nB) if self.v(p, b) in mod) for p in self.pts}


def verifie(f, m, RA, RB):
    ar = len(next(iter(RA)))
    for cols in itertools.product(list(RA), repeat=m):
        img = tuple(f[tuple(c[i] for c in cols)] for i in range(ar))
        if img not in RB:
            return False
    return True


def siggers(n, rels):
    P = Poly(n, n, 4)
    for R in rels:
        P.polymorphe(R, R)
    for a, r, e in itertools.product(range(n), repeat=3):
        P.egal((a, r, e, a), (r, a, r, e))
    f = P.resoudre()
    if f is not None:
        assert all(verifie(f, 4, R, R) for R in rels)
        assert all(f[(a, r, e, a)] == f[(r, a, r, e)] for a, r, e in itertools.product(range(n), repeat=3))
    return f is not None, len(P.cl)


def olsak(c):
    P = Poly(3, c, 6)
    P.polymorphe(neq(3), neq(c))
    for x, y in itertools.product(range(3), repeat=2):
        a, b, d = (x, x, y, y, y, x), (x, y, x, y, x, y), (y, x, x, x, y, y)
        P.egal(a, b)
        P.egal(b, d)
    f = P.resoudre()
    if f is not None:
        assert verifie(f, 6, neq(3), neq(c))
    return f is not None, 729 * c, len(P.cl)


def main():
    print("=== Siggers (contrôle : Schaefer, Hell-Nešetřil) ===", flush=True)
    ok = 0
    for nom, (n, rels) in GABARITS.items():
        t0 = time.time()
        r, ncl = siggers(n, rels)
        conf = (r == ATTENDU[nom])
        ok += conf
        print(f"  {nom:>7} : Sig = {'OUI' if r else 'NON'}  attendu {'OUI' if ATTENDU[nom] else 'NON'}"
              f"  {'conforme' if conf else 'ÉCART'}  [{ncl} clauses, {time.time()-t0:.2f} s]", flush=True)
    print(f"  {ok}/9 conformes", flush=True)
    print("\n=== Olšák K3^6 -> K_c ===", flush=True)
    for c in range(3, 8):
        t0 = time.time()
        r, nv, ncl = olsak(c)
        print(f"  c = {c} : Ols = {'OUI' if r else 'NON'}  [{nv} vars, {ncl} clauses, {time.time()-t0:.1f} s]",
              flush=True)


if __name__ == "__main__":
    main()
