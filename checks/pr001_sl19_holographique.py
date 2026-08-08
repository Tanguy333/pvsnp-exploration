"""
PR-001 / SL-19 -- Realisabilite holographique SIMULTANEE au niveau parite.

Cadre (convention Holant(G | R), Cai-Lu) : une transformation holographique
de base T ∈ GL_2 envoie les generateurs (variables, vecteurs lignes) sur
G·T⊗ et les recognisseurs (clauses, vecteurs colonnes) sur (T^{-1})⊗·R.
Pour que la reduction vers PerfMatch planaire (FKT) existe, chaque
signature transformee doit etre une signature de matchgate ; la CONDITION
DE PARITE (les composantes d'une seule parite de poids sont non nulles)
est NECESSAIRE (les identites de matchgate completes, non incluses ici,
ne peuvent que restreindre davantage -- donc une INFAISABILITE au niveau
parite est concluante, une faisabilite ne l'est pas encore).

Signatures symetriques transformees (T = [[a,b],[c,d]], adj(T) = (d,-b,-c,a),
l'echelle est libre car les conditions sont homogenes) :
  generateur =_k : g_w = a^{k-w} b^w + c^{k-w} d^w              (w = 0..k)
  recognisseur OR_3 (via adjugate (alpha,beta,gamma,delta)=(d,-b,-c,a)) :
    r_w = (alpha+beta)^{3-w} (gamma+delta)^w - alpha^{3-w} gamma^w

Parite : type pair -> composantes de poids impair nulles ;
         type impair -> composantes de poids pair nulles.
4 combinaisons (generateur x recognisseur) par paire de signatures.

Paires testees :
  A = {OR_3, =_2}  -- le cadre lu-deux-fois de Valiant (#_7 Pl-Rtw-Mon-3CNF) ;
                      calibration attendue : FAISABLE sur F_7, infaisable sur C.
  B = {OR_3, =_3}  -- le coeur du cas general (fanout 3).

Methodes :
  - Sur C : bases de Groebner exactes (sympy, corps Q) sur l'ideal
    {equations} + {t*det(T) - 1} (Rabinowitsch) ; GB = [1] <=> AUCUNE
    solution complexe avec det != 0 (Nullstellensatz).
  - Sur F_7 : enumeration exhaustive des 7^4 = 2401 matrices, det != 0
    (|GL_2(F_7)| = 2016) ; rigoureux, et exhibe les bases temoins.
"""

from __future__ import annotations

import itertools
import time

import sympy as sp

a, b, c, d, t = sp.symbols('a b c d t')
ALPHA, BETA, GAMMA, DELTA = d, -b, -c, a          # adjugate de T
DET = a * d - b * c


def gen_eq_sig(k: int):
    """ Signature transformee du generateur =_k : liste par poids w. """
    return [a ** (k - w) * b ** w + c ** (k - w) * d ** w
            for w in range(k + 1)]


def rec_or3_sig():
    """ Signature transformee du recognisseur OR_3 (via adjugate). """
    s, u = ALPHA + BETA, GAMMA + DELTA
    return [sp.expand(s ** (3 - w) * u ** w - ALPHA ** (3 - w) * GAMMA ** w)
            for w in range(4)]


def parity_eqs(sig: list, ptype: str) -> list:
    """ ptype 'even' : composantes de poids impair nulles ; 'odd' : pairs. """
    keep = 1 if ptype == "even" else 0
    return [sig[w] for w in range(len(sig)) if w % 2 == keep]


def solve_C(pair_label: str, gen_sig: list) -> None:
    rec = rec_or3_sig()
    print(f"  --- paire {pair_label} sur C (Groebner exact) ---", flush=True)
    for pg in ("even", "odd"):
        for pr in ("even", "odd"):
            eqs = ([sp.expand(e) for e in parity_eqs(gen_sig, pg)]
                   + [sp.expand(e) for e in parity_eqs(rec, pr)]
                   + [sp.expand(t * DET - 1)])
            t0 = time.time()
            gb = sp.groebner(eqs, a, b, c, d, t, order='grevlex')
            infeas = list(gb.exprs) == [sp.Integer(1)]
            dt = time.time() - t0
            verdict = ("INFAISABLE (1 dans l'ideal)" if infeas
                       else f"FAISABLE sur C -- GB = {list(gb.exprs)[:3]}...")
            print(f"    gen={pg:<5} rec={pr:<5} : {verdict}  ({dt:.1f}s)",
                  flush=True)


def solve_F7(pair_label: str, k_gen: int) -> None:
    p = 7
    print(f"  --- paire {pair_label} sur F_7 (enumeration GL_2, 2016 bases) ---",
          flush=True)
    sols = {("even", "even"): [], ("even", "odd"): [],
            ("odd", "even"): [], ("odd", "odd"): []}
    for av, bv, cv, dv in itertools.product(range(p), repeat=4):
        det = (av * dv - bv * cv) % p
        if det == 0:
            continue
        al, be, ga, de = dv % p, (-bv) % p, (-cv) % p, av % p
        gsig = [(pow(av, k_gen - w, p) * pow(bv, w, p)
                 + pow(cv, k_gen - w, p) * pow(dv, w, p)) % p
                for w in range(k_gen + 1)]
        s, u = (al + be) % p, (ga + de) % p
        rsig = [(pow(s, 3 - w, p) * pow(u, w, p)
                 - pow(al, 3 - w, p) * pow(ga, w, p)) % p
                for w in range(4)]
        for pg in ("even", "odd"):
            kg = 1 if pg == "even" else 0
            if any(gsig[w] for w in range(k_gen + 1) if w % 2 == kg):
                continue
            if all(v == 0 for v in gsig):        # signature nulle : inutile
                continue
            for pr in ("even", "odd"):
                kr = 1 if pr == "even" else 0
                if any(rsig[w] for w in range(4) if w % 2 == kr):
                    continue
                if all(v == 0 for v in rsig):
                    continue
                sols[(pg, pr)].append(((av, bv, cv, dv), gsig, rsig))
    for combo, lst in sols.items():
        if lst:
            (T0, gs, rs) = lst[0]
            print(f"    gen={combo[0]:<5} rec={combo[1]:<5} : FAISABLE, "
                  f"{len(lst)} bases ; temoin T={T0}, "
                  f"sig_gen={gs}, sig_rec={rs}", flush=True)
        else:
            print(f"    gen={combo[0]:<5} rec={combo[1]:<5} : infaisable",
                  flush=True)


def main():
    print("PR-001 / SL-19 -- realisabilite simultanee (niveau parite)")
    print("=" * 74)
    print("Paire A = {OR_3 recognisseur, =_2 generateur}  (cadre Valiant)")
    solve_C("A", gen_eq_sig(2))
    solve_F7("A", 2)
    print()
    print("Paire B = {OR_3 recognisseur, =_3 generateur}  (coeur du general)")
    solve_C("B", gen_eq_sig(3))
    solve_F7("B", 3)
    print()
    print("Rappel de lecture : INFAISABLE au niveau parite => infaisable")
    print("tout court (la parite est necessaire). FAISABLE au niveau parite")
    print("=> a confronter aux identites de matchgate completes (arite >= 4 ;")
    print("pour l'arite <= 3, references Cai-Lu a verifier sur texte).")


if __name__ == "__main__":
    main()
