"""
TACHE F-011, etape 10 -- Theoremes H et I : la loi MAJ mod 6, deux tiers.

Notation : t = ceil(n/2) ; q2 = plus petite puissance de 2 >= t ;
q3 = plus petite puissance de 3 >= t ; L1 = min(q2, q3).

LEMME 4 (glouton triangulaire -- folklore) : pour tout premier p et toute
fenetre [t, D], il existe V = sum_{i=t}^{D} v_i e_i avec V(w) != 0 mod p
pour tout w in [t, D]. (Triangulaire : V(w) = v_w + sum_{i<w} v_i C(w,i) ;
on choisit v_w en montant -- une valeur interdite, p-1 disponibles.)

THEOREME H (borne superieure) : deg_6^sym(MAJ_n) <= L1(t), SAUF cas
d'anomalie (L1 = q2 = t, n = 2t, C(2t,t) = 0 mod 3) ou la borne est la
puissance suivante.
  Preuve (cas L1 = q2) : u = e_{q2} couvre [q2, min(n, 2q2-1)] mod 2
  (Lucas : bit q2 present) ; V = glouton mod 3 couvre [t, q2-1] (Lemme 4).
  Si n = 2q2 (seulement si t = q2) : w = 2q2 a C(2q2,q2) pair (Kummer) ;
  si C(2q2,q2) != 0 mod 3, on ajuste v_{q2} en dernier pas du glouton pour
  couvrir w = 2q2 mod 3 ; sinon (anomalie) : puissance suivante.
  Cas L1 = q3 : symetrique (V = e_{q3} couvre [q3, n] mod 3 -- jamais
  d'anomalie car C(2q3, q3) = C(2,1) = 2 != 0 mod 3 par Lucas ; u =
  glouton mod 2 couvre [t, q3-1]).

THEOREME I (borne inferieure, regime n >= max(q2, q3)) :
  si d < L1, alors U est q2-periodique (BBR) et s'annule sur [q2, n]
  (car w - q2 < t pour w <= n <= t + q2), et V est q3-periodique et
  s'annule sur [q3, n]. Tout w in [max(q2,q3), n] est doublement mort.
  DONC deg_6^sym >= L1 des que n >= max(q2, q3).

REGIME RESIDUEL (n < max(q2,q3), ex. t = 10, q3 = 27) : la borne inf
demande l'argument MIXTE : periodicite mod 2 (U morte sur [q2, n]) +
fenetre Lucas-morte mod 3 (ex. w = 18 = (2,0,0)_3 : C(18, i) = 0 mod 3
pour tout i in [10, 15]). Non prouve en general ici -- cartographie.

Ce script verifie :
  [A] Lemme 4 (glouton) sur de nombreuses fenetres, p = 2 et 3 ;
  [B] Theoreme H : la construction explicite donne un certificat VALIDE
      a la valeur C-F011 pour tout n = 2..40 (MAJ) ;
  [C] Theoreme I : couverture du regime (quels n sont entierement
      prouves : H pour <=, I pour >=) ;
  [D] regime residuel : pour chaque n non couvert par I, chercher le
      temoin mixte (w mod-3-mort dans [q2, n]) -- diagnostic.
"""

from __future__ import annotations

from math import comb


def t_of(n):
    return (n + 1) // 2


def q_pow(t, p):
    q = 1
    while q < t:
        q *= p
    return q


def L1_of(t):
    return min(q_pow(t, 2), q_pow(t, 3))


def cf011_value(n):
    """ Valeur predite par C-F011. """
    t = t_of(n)
    q2, q3 = q_pow(t, 2), q_pow(t, 3)
    L1 = min(q2, q3)
    if L1 == q2 and n >= 2 * q2 and comb(2 * q2, q2) % 3 == 0:
        # anomalie : puissance suivante
        cands = []
        q = 1
        while q <= 4 * L1:
            if q > L1:
                cands.append(q)
            q *= 2
        q = 1
        while q <= 4 * L1:
            if q > L1:
                cands.append(q)
            q *= 3
        return min(cands)
    return L1


# ----------------------------------------------------- Lemme 4 : glouton

def greedy_cover(t, D, p, extra_w=None, extra_deg=None):
    """ v_i (i = t..max(D, extra_deg)) avec V(w) != 0 mod p sur [t, D]
        (+ extra_w si fourni, ajuste via v_{extra_deg}). """
    deg_max = max(D, extra_deg or 0)
    v = {}
    for w in range(t, D + 1):
        s = sum(v.get(i, 0) * comb(w, i) for i in range(t, w)) % p
        # choisir v_w pour rendre V(w) = s + v_w != 0 (0 est permis !)
        v[w] = 0 if s % p != 0 else 1
    if extra_w is not None:
        # ajuster v_{extra_deg} (non utilise par la fenetre [t, D])
        s = sum(v.get(i, 0) * comb(extra_w, i) for i in range(t, D + 1)) % p
        cw = comb(extra_w, extra_deg) % p
        if s % p != 0:
            v[extra_deg] = 0
        elif cw != 0:
            v[extra_deg] = 1  # s + 1*cw != 0 puisque s = 0, cw != 0
        else:
            return None
    return v


def check_lemma4():
    ok = True
    for p in (2, 3):
        for t in range(1, 20):
            for D in range(t, t + 25):
                v = greedy_cover(t, D, p)
                if v is None:
                    ok = False
                    continue
                for w in range(t, D + 1):
                    s = sum(v.get(i, 0) * comb(w, i) for i in range(t, D + 1)) % p
                    if s == 0:
                        print(f"  ECHEC glouton p={p}, t={t}, D={D}, w={w}")
                        ok = False
    return ok


# ----------------------------------------------------- Theoreme H : certificat

def build_certificate(n):
    """ Construit (u, v) realisant cf011_value(n) selon le Theoreme H.
        Retourne (u_dict, v_dict, d) ou None. """
    t = t_of(n)
    q2, q3 = q_pow(t, 2), q_pow(t, 3)
    d = cf011_value(n)
    L1 = min(q2, q3)
    if d == L1 == q3:
        # V = e_{q3} couvre [q3, n] mod 3 ; u = glouton mod 2 sur [t, q3-1]
        v = {q3: 1}
        u = greedy_cover(t, min(q3 - 1, n), 2) if q3 - 1 >= t else {}
        return u or {}, v, d
    if d == L1 == q2 and not (n >= 2 * q2 and comb(2 * q2, q2) % 3 == 0):
        u = {q2: 1}
        if n >= 2 * q2:  # w = 2q2 dans la fenetre, pair par Kummer
            v = greedy_cover(t, min(q2 - 1, n), 3,
                             extra_w=2 * q2, extra_deg=q2)
        else:
            v = greedy_cover(t, min(q2 - 1, n), 3) if q2 - 1 >= t else {}
        return u, v or {}, d
    # anomalie : certificat non couvert par H (constructions ad hoc des
    # etapes 3/8 : e2+e3, e8+e9, e16+e18+e25+e27) -- signale
    return None


def verify_certificate(n, u, v, d):
    t = t_of(n)
    if any(i < t or i > d for i in list(u) + list(v)):
        return False
    for w in range(0, n + 1):
        U = sum(c * comb(w, i) for i, c in u.items()) % 2
        V = sum(c * comb(w, i) for i, c in v.items()) % 3
        if w < t and (U != 0 or V != 0):
            return False
        if w >= t and U == 0 and V == 0:
            return False
    return True


def main() -> None:
    print("TACHE F-011 etape 10 -- Theoremes H et I (loi MAJ mod 6)")
    print("=" * 68)

    print("\n[A] Lemme 4 (glouton triangulaire), p = 2, 3 ; ~950 fenetres :")
    print(f"    {'OK' if check_lemma4() else 'ECHEC'}")

    print("\n[B] Theoreme H : certificats explicites a la valeur C-F011 :")
    okH, anomalies, fails = 0, [], []
    for n in range(2, 41):
        res = build_certificate(n)
        if res is None:
            anomalies.append(n)
            continue
        u, v, d = res
        if verify_certificate(n, u, v, d):
            okH += 1
        else:
            fails.append(n)
    print(f"    {okH} certificats valides (n = 2..40) ; "
          f"anomalies hors-H (ad hoc etapes 3/8) : {anomalies} ; "
          f"ECHECS : {fails if fails else 'aucun'}")

    print("\n[C] Theoreme I (borne inf par double periodicite) -- regime :")
    proven, residual = [], []
    for n in range(2, 41):
        t = t_of(n)
        q2, q3 = q_pow(t, 2), q_pow(t, 3)
        (proven if n >= max(q2, q3) else residual).append(n)
    print(f"    n entierement prouves (H pour <=, I pour >=, hors anomalies)"
          f" : {proven}")
    print(f"    regime residuel (borne inf non prouvee ici) : {residual}")

    print("\n[D] Regime residuel -- THEOREME J (argument mixte) par cellule :")
    print("    (d < t : trivial, noyau vide ; d in [t, L1-1] : U morte par")
    print("     periodicite mod 2 sur [q2, n], temoin w Lucas-mort mod 3)")
    allJ = True
    for n in residual:
        t = t_of(n)
        q2 = q_pow(t, 2)
        L = cf011_value(n)
        if L <= t:
            print(f"    n={n:>2} : L1 = {L} <= t = {t} -- borne inf TRIVIALE "
                  f"(noyau vide sous t)")
            continue
        # verifier le temoin pour TOUS les d in [t, L-1] et la mort mod 2
        wit = None
        for w in range(max(t, q2), n + 1):
            if (w - q2 < t and
                    all(comb(w, i) % 3 == 0 for i in range(t, L))):
                wit = w
                break
        okJ = wit is not None
        allJ &= okJ
        print(f"    n={n:>2} (t={t}, q2={q2}, exclure d <= {L-1}) : temoin "
              f"w = {wit} (mort mod 2 : w-q2 = {wit - q2 if wit else '?'} < t ; "
              f"mort mod 3 : C(w,i) = 0, i in [{t},{L-1}])"
              if okJ else f"    n={n:>2} : AUCUN temoin -- trou reel")
    print(f"    Theoreme J etabli sur tout le regime residuel : "
          f"{'OUI' if allJ else 'NON'}")


if __name__ == "__main__":
    main()
