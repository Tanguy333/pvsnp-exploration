"""
TACHE B-001 -- Replication empirique du Switching Lemma de Hastad (1986).

Enonce replique : pour toute k-DNF f et une restriction aleatoire rho ~ R_p
(chaque variable : libre avec probabilite p, sinon fixee a 0/1 uniforme),
    Pr[ DTdepth(f|rho) >= s ] <= (5 p k)^s.

Methode :
  - DNF testees : (a) k-DNF aleatoire (n=24, m=60 termes de largeur k),
    (b) TRIBES (termes disjoints, la famille classique ou le lemme est
    essentiellement serre en exposant).
  - Pour chaque echantillon : tirer rho, simplifier la DNF (litteral
    falsifie -> terme mort ; litteral satisfait -> retire ; terme vide ->
    fonction = 1), puis calculer la profondeur d'arbre de decision EXACTE
    de la fonction restreinte (recursion memoisee sur la table de verite
    des variables pertinentes).
  - Tabuler Pr_empirique[depth >= s] et comparer a (5pk)^s.

Configurations avec 5pk < 1 (sinon la borne est triviale).
"""

from __future__ import annotations

import random
from functools import lru_cache
from itertools import product

random.seed(2026)


# ------------------------------------------------------------ DNF + restriction

def random_kdnf(n: int, m: int, k: int):
    """ Liste de termes ; terme = liste de litteraux (var, signe). """
    terms = []
    for _ in range(m):
        vs = random.sample(range(n), k)
        terms.append([(v, random.choice([0, 1])) for v in vs])
    return terms


def tribes(n: int, k: int):
    """ n/k termes disjoints, tous positifs. """
    return [[(i, 1) for i in range(b * k, (b + 1) * k)]
            for b in range(n // k)]


def restrict(terms, n: int, p: float):
    """ Tire rho ~ R_p, retourne (termes simplifies, vars libres) ou
        ('const', valeur). """
    rho = {}
    for v in range(n):
        if random.random() < p:
            rho[v] = None  # libre
        else:
            rho[v] = random.choice([0, 1])
    new_terms = []
    for t in terms:
        nt = []
        dead = False
        for (v, sgn) in t:
            if rho[v] is None:
                nt.append((v, sgn))
            elif rho[v] == sgn:
                continue       # litteral satisfait
            else:
                dead = True    # litteral falsifie
                break
        if dead:
            continue
        if not nt:
            return ('const', 1)   # terme entierement satisfait
        new_terms.append(nt)
    if not new_terms:
        return ('const', 0)
    return ('dnf', new_terms)


# ------------------------------------------------------------ profondeur DT

def dt_depth_of_dnf(terms) -> int:
    """ Profondeur d'arbre de decision exacte de la DNF restreinte. """
    rel = sorted({v for t in terms for (v, _) in t})
    v = len(rel)
    if v == 0:
        return 0
    if v > 16:
        return 99  # trop gros pour le calcul exact -- compte comme >= s
    idx = {var: i for i, var in enumerate(rel)}
    # table de verite en bitmask
    table = 0
    for bits in range(1 << v):
        val = 0
        for t in terms:
            ok = True
            for (var, sgn) in t:
                if ((bits >> idx[var]) & 1) != sgn:
                    ok = False
                    break
            if ok:
                val = 1
                break
        if val:
            table |= (1 << bits)
    full = (1 << (1 << v)) - 1

    @lru_cache(maxsize=None)
    def depth(tbl: int, nv: int, mask: int) -> int:
        # mask = variables encore libres (bitmask sur nv positions)
        if tbl == 0:
            return 0
        # tbl restreint a l'espace courant ; tester constance
        # (on garde la table complete et on teste sur les points coherents)
        # Simplification : on reconstruit recursivement.
        # constant 1 ?
        # points de l'espace courant : tous bits, mais seules les vars de
        # mask varient ; pour la constance on teste les valeurs atteintes.
        vals = set()
        # echantillon complet de l'espace courant
        free = [i for i in range(nv) if (mask >> i) & 1]
        fixed_bits = 0  # les vars hors mask sont deja integrees via tbl filtre
        for assign in range(1 << len(free)):
            bits = 0
            for j, i in enumerate(free):
                if (assign >> j) & 1:
                    bits |= (1 << i)
            vals.add((tbl >> bits) & 1)
            if len(vals) == 2:
                break
        if len(vals) == 1:
            return 0
        best = 99
        for i in free:
            m2 = mask & ~(1 << i)
            # brancher x_i = 0 / 1 : filtrer la table
            d0 = depth(project(tbl, nv, i, 0), nv, m2)
            d1 = depth(project(tbl, nv, i, 1), nv, m2)
            best = min(best, 1 + max(d0, d1))
        return best

    @lru_cache(maxsize=None)
    def project(tbl: int, nv: int, i: int, val: int) -> int:
        """ Fixe x_i = val : recopie les entrees coherentes sur tout l'espace
            (les points avec x_i != val recoivent la valeur du point miroir,
            pour que la table reste definie sur le meme espace). """
        out = 0
        for bits in range(1 << nv):
            b2 = (bits & ~(1 << i)) | (val << i)
            if (tbl >> b2) & 1:
                out |= (1 << bits)
        return out

    return depth(table, v, (1 << v) - 1)


# ------------------------------------------------------------ experience

def run_config(label, terms, n, p, k, samples, s_max=5):
    counts = [0] * (s_max + 1)  # counts[s] = #{depth >= s}
    for _ in range(samples):
        kind, payload = restrict(terms, n, p)
        d = 0 if kind == 'const' else dt_depth_of_dnf(payload)
        for s in range(1, s_max + 1):
            if d >= s:
                counts[s] += 1
    bound = 5 * p * k
    print(f"\n  {label}  (n={n}, k={k}, p={p}, 5pk={bound:.3f}, "
          f"{samples} echantillons)")
    print(f"    {'s':>2} | {'Pr_emp[depth>=s]':>18} | {'(5pk)^s':>10} | borne respectee ?")
    ok_all = True
    for s in range(1, s_max + 1):
        emp = counts[s] / samples
        b = bound ** s
        ok = emp <= b
        ok_all &= ok
        print(f"    {s:>2} | {emp:>18.6f} | {b:>10.6f} | {'oui' if ok else '*** NON ***'}")
    return ok_all


def main() -> None:
    print("TACHE B-001 -- replication du Switching Lemma (Hastad 1986)")
    print("=" * 72)
    n = 24
    samples = 200_000
    all_ok = True

    all_ok &= run_config("k-DNF aleatoire (m=60)", random_kdnf(n, 60, 3),
                         n, 1 / 20, 3, samples)
    all_ok &= run_config("k-DNF aleatoire (m=60)", random_kdnf(n, 60, 2),
                         n, 1 / 20, 2, samples)
    all_ok &= run_config("TRIBES (8 blocs de 3)", tribes(n, 3),
                         n, 1 / 20, 3, samples)
    all_ok &= run_config("TRIBES (8 blocs de 3), p plus grand", tribes(n, 3),
                         n, 1 / 16, 3, samples)

    print("\n" + "=" * 72)
    print("VERDICT :", "borne (5pk)^s respectee sur toutes les configurations"
          if all_ok else "*** VIOLATION DETECTEE -- verifier le code ***")


if __name__ == "__main__":
    main()
