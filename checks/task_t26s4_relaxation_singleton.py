"""
TACHE T26-S4 — la DICHOTOMIE dense/degenere attaquee par la
RELAXATION SINGLETON.

Cadre (systemes decomposables de MAJ_k^t(OR2^k)). Bloc i = triple
(alpha_i, beta_i, gamma_i) >= 0 ; valeurs actives {alpha, beta,
M_i} avec M_i = alpha+beta+gamma ; POIDS W = somme des coefficients
= somme des M_i. Minimum du bloc : m_i = min(alpha_i, beta_i).
Separation : deux configurations de comptes de part et d'autre du
seuil t n'ont jamais la meme somme.

LEMME 0 (minima >= 1, prouve et verifie ici) : si un bloc a une
valeur active nulle, prendre t blocs actifs dont lui a la valeur 0 ;
retirer ce bloc donne t-1 blocs et LA MEME SOMME => collision. Donc
tout systeme separant a m_i >= 1 pour tout i. (t <= k requis.)

FAMILLE COLLISION-SINGLETON (necessaire) : etat0 = bloc i au SOMMET
M_i + un ensemble A de blocs (i hors de A) a leur MINIMUM ;
etat1 = un ensemble B de blocs a leur MINIMUM. Comptes |A|+1 et |B|
de part et d'autre de t, sommes egales => collision. Donc :

  M_i  n'appartient pas a  F_i = { S_B - S_A }  ou  A inclus dans
  [k]\{i}, B inclus dans [k], (|A|+1 < t <= |B|) ou (|B| < t <=
  |A|+1), S_X = somme des minima de X.

Avec M_i >= alpha_i + beta_i >= 2 m_i, on obtient la RELAXATION :

  LB(m_1..m_k) = somme_i  min { M >= 2 m_i : M hors de F_i }
              <=  W  pour tout separateur de vecteur de minima m.

QUESTION DE LA TACHE : min sur tous les vecteurs de minima de
LB(m) vaut-il k(k+1) ? Si OUI, la famille singleton SEULE force la
loi — la dichotomie devient un enonce arithmetique sur les sommes
de sous-ensembles, et le trou de la reduction 1 est refermable par
preuve. Si NON, on obtient les vecteurs EXACTS qui echappent (a
comparer aux verites terrain exhaustives k <= 9 de T26-S1).

Cas de controle : m == 1 (classe du theoreme S3) doit rendre
minfeasible = k+1 par bloc, donc LB = k(k+1).
"""

from __future__ import annotations

import sys
import time


def dp_counts(vals):
    """masks[c] = bitmask des sommes atteignables avec exactement c
    blocs pris a leur valeur (une par bloc), sur la liste vals."""
    masks = [0] * (len(vals) + 1)
    masks[0] = 1
    for v in vals:
        for c in range(len(vals) - 1, -1, -1):
            if masks[c]:
                masks[c + 1] |= masks[c] << v
    return masks


def bits(mask):
    out = []
    while mask:
        low = mask & -mask
        out.append(low.bit_length() - 1)
        mask ^= low
    return out


def forbidden(m, i, k, t):
    """F_i sous forme de bitmask (valeurs positives seulement)."""
    mA = dp_counts([m[j] for j in range(k) if j != i])   # A
    mB = dp_counts(list(m))                              # B
    # union des masques B par cote
    B_low = 0   # |B| < t
    B_high = 0  # |B| >= t
    for c, msk in enumerate(mB):
        if c < t:
            B_low |= msk
        else:
            B_high |= msk
    F = 0
    for cA, mskA in enumerate(mA):
        if not mskA:
            continue
        target = B_high if cA + 1 < t else B_low
        if not target:
            continue
        for sA in bits(mskA):
            F |= target >> sA   # valeurs S_B - S_A >= 0
    return F


def lower_bound(m, k, t):
    """LB(m) = somme des plus petits M_i admissibles."""
    total = 0
    per = []
    for i in range(k):
        F = forbidden(m, i, k, t)
        M = max(1, 2 * m[i])
        while (F >> M) & 1:
            M += 1
        per.append(M)
        total += M
    return total, per


def vectors(k, maxsum):
    """Vecteurs de minima tries 1 <= m_1 <= ... <= m_k, somme <= maxsum."""
    out = []

    def rec(pos, low, rest, cur):
        if pos == k:
            out.append(tuple(cur))
            return
        for v in range(low, rest - (k - pos - 1) + 1):
            cur.append(v)
            rec(pos + 1, v, rest - v, cur)
            cur.pop()

    rec(0, 1, maxsum, [])
    return out


def multitop_min(m, k, t, target):
    """ETAGE 2 — famille MULTI-SOMMETS (necessaire, generalise F1) :
    etat0 = ensemble C de blocs au SOMMET + ensemble A (disjoint de
    C) au MINIMUM ; etat1 = ensemble B au MINIMUM. Contrainte, pour
    tout C non vide : somme_{i dans C} M_i hors de
      D_C = { S_B - S_A : A inclus dans [k]\\C, B inclus dans [k],
              (|C|+|A| < t <= |B|) ou (|B| < t <= |C|+|A|) }.
    Retourne min somme M_i sous ces contraintes (CP-SAT), avec
    M_i >= 2 m_i. C'est une BORNE INFERIEURE valide sur W."""
    from ortools.sat.python import cp_model

    model = cp_model.CpModel()
    UB = target + 2 * k
    M = [model.NewIntVar(2 * m[i], UB, f"M{i}") for i in range(k)]
    mB = dp_counts(list(m))
    B_low = B_high = 0
    for c, msk in enumerate(mB):
        if c < t:
            B_low |= msk
        else:
            B_high |= msk
    for Cmask in range(1, 1 << k):
        C = [i for i in range(k) if Cmask >> i & 1]
        mA = dp_counts([m[j] for j in range(k) if not (Cmask >> j & 1)])
        D = 0
        for cA, mskA in enumerate(mA):
            if not mskA:
                continue
            tgt = B_high if len(C) + cA < t else B_low
            if not tgt:
                continue
            for sA in bits(mskA):
                D |= tgt >> sA
        expr = sum(M[i] for i in C)
        for v in bits(D):
            if 0 < v <= UB * len(C):
                model.Add(expr != v)
    model.Minimize(sum(M))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 120.0
    solver.parameters.num_search_workers = 8
    st = solver.Solve(model)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return (int(solver.ObjectiveValue()),
                [solver.Value(v) for v in M],
                st == cp_model.OPTIMAL)
    return None, None, False


def main():
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    for k in range(3, kmax + 1):
        t = (k + 1) // 2
        target = k * (k + 1)
        # LB >= 2*somme(m) : au-dela, la borne est acquise d'office.
        maxsum = (target - 1) // 2
        t0 = time.time()
        vecs = vectors(k, maxsum)
        best, argmin = None, None
        control = None
        under = []
        for m in vecs:
            lb, per = lower_bound(m, k, t)
            if m == (1,) * k:
                control = (lb, per)
            if best is None or lb < best:
                best, argmin = lb, (m, per)
            if lb < target:
                under.append((lb, m, per))
        dt = time.time() - t0
        ctrl_ok = control is not None and control[0] == target
        # GARDE-FOU de validite : le temoin mod-k (m=1, M=k+1) satisfait
        # toutes les contraintes reelles, donc la relaxation F1+F2 sur
        # m=1 doit valoir EXACTEMENT k(k+1). Plus = famille invalide.
        mt1, Mv1, _ = multitop_min((1,) * k, k, t, target)
        gate = (mt1 == target)
        print(f"  garde-fou F1+F2 sur m=1 : {mt1} (attendu {target} "
              f"exactement) {'OK' if gate else 'FAMILLE INVALIDE'}",
              flush=True)
        if not gate:
            print("  ARRET : contraintes sur-contraignantes.", flush=True)
            return
        print(f"k={k} (t={t}, cible {target}) : {len(vecs)} vecteurs "
              f"de minima testes ({dt:.0f}s)", flush=True)
        print(f"  controle m=1 : LB = {control[0] if control else '?'} "
              f"(M_i = {control[1][0] if control else '?'}) "
              f"{'OK' if ctrl_ok else 'ECHEC'}", flush=True)
        print(f"  min LB = {best} au vecteur {argmin[0]} "
              f"-> M = {argmin[1]}", flush=True)
        if under:
            print(f"  !! {len(under)} vecteurs echappent a F1 "
                  f"(singleton) ; ETAGE 2 (multi-sommets) sur chacun :",
                  flush=True)
            worst = None
            for lb, m, per in sorted(under):
                mt, Mv, opt = multitop_min(m, k, t, target)
                flag = ("OK >= cible" if mt is not None and mt >= target
                        else "SOUS LA CIBLE")
                if worst is None or (mt is not None and mt < worst[0]):
                    worst = (mt, m, Mv)
                print(f"     m={m} : F1 donne {lb}, F1+F2 donne {mt} "
                      f"{'(optimal)' if opt else '(borne)'} "
                      f"M={Mv} -> {flag}", flush=True)
            if worst and worst[0] is not None and worst[0] >= target:
                print(f"  ==> ETAGE 2 RATTRAPE TOUT : min F1+F2 = "
                      f"{worst[0]} >= {target} sur les echappees.",
                      flush=True)
        else:
            print(f"  ==> AUCUN vecteur sous {target} : la famille "
                  f"SINGLETON SEULE force W >= k(k+1).", flush=True)


if __name__ == "__main__":
    main()
