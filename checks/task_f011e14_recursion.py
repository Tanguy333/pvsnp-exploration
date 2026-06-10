"""
TACHE F-011, etape 14 -- La borne recursive CAND2 vs la table exacte.

STRUCTURE DU 2e ETAGE (raffinement prouvable de l'etape 13) :
  pour P = 3^b avec t <= P et P <= deg < 2P, G = g(.+P) - g verifie :
    - deg(G) <= deg - P < P  =>  G est P-periodique ;
    - G est NON-NULLE sur tout [0, t)  (G(j) = g(j+P), j+P >= t) ;
    - G est NULLE sur [t, n-2P]        (paires interdites, 3 etages) ;
    - G libre sur (n-2P, n-P].
  Obstructions du 2e etage (chacune PROUVEE) :
    (i)  interpolation (etape 7, decalee) : deg(G) >= n-2P-t+1 ;
    (ii) temoins de multiples : pour toute puissance Q = 3^c, s'il existe
         z1 in [0, t) et z2 in [t, n-2P] avec Q | (z2 - z1), alors G ne
         peut etre Q-periodique => deg(G) >= Q.
  Contribution a la borne : deg ∉ [P, P + X_P) avec
  X_P = max((i), (ii)) => avec D-gen (deg >= P) : deg >= min(2P, P + X_P).

CAND2(t, n) = max( t, blocage_mono(t,n),
                   max sur P in [t, n-t+1] (3-puissances, n >= 2P + t) de
                       min(2P, P + X_P) ,
                   max sur P <= n-t+1 de P  [D-gen] )

Limite connue (cas (2,24)) : la loi exacte exige la structure {1,2} fine
des valeurs de G (pas seulement nulle/non-nulle) -- CAND2 est une borne,
pas la loi. Ce script mesure l'ecart.

  [A] table exacte deg_3^sym(THR_{t,n}) (DP, t = 1..10, n = t..t+26) ;
  [B] CAND2 vs exact : couverture, distribution des ecarts.
"""

from __future__ import annotations

from math import comb


def dp_feasible(t, n, d):
    W = d + 2
    coeffs = [((-1) ** (d + 1 - k)) * comb(d + 1, k) % 3 for k in range(W)]
    states = {tuple()}
    for w in range(0, n + 1):
        allowed = (0,) if w < t else (1, 2)
        new = set()
        for st in states:
            for val in allowed:
                seq = st + (val,)
                if len(seq) == W:
                    if sum(c * v for c, v in zip(coeffs, seq)) % 3 != 0:
                        continue
                    seq = seq[1:]
                new.add(seq)
        states = new
        if not states:
            return False
    return True


def dp_deg(t, n, d_cap=18):
    for d in range(t, d_cap + 1):
        if d + 1 > n or dp_feasible(t, n, d):
            return d
    return None


def b_block(t, n, cap=40):
    d = t
    while d <= cap:
        if not any(all(comb(w, i) % 3 == 0 for i in range(t, d + 1))
                   for w in range(t, n + 1)):
            return d
        d += 1
    return cap


def cand2(t, n):
    lb = max(t, b_block(t, n))
    P = 1
    while P <= n - t + 1:
        lb = max(lb, P)  # D-gen
        if P >= t and n >= 2 * P + t:
            zlo, zhi = t, n - 2 * P            # zone nulle de G
            X = zhi - zlo + 1                  # (i) interpolation
            Q = 1
            while Q <= zhi:                    # (ii) temoins de multiples
                found = any((z2 - z1) % Q == 0
                            for z1 in range(0, t)
                            for z2 in range(zlo, zhi + 1))
                if found:
                    X = max(X, Q)
                Q *= 3
            lb = max(lb, min(2 * P, P + X))
        P *= 3
    return lb


def main() -> None:
    print("TACHE F-011 etape 14 -- borne recursive CAND2 vs table exacte")
    print("=" * 70)

    print("\n[A] Table exacte deg_3^sym (lignes t, colonnes L = n-t+1) :")
    table = {}
    header = "  t\\L " + "".join(f"{L:>4}" for L in range(1, 28))
    print(header)
    for t in range(1, 11):
        row = []
        for L in range(1, 28):
            n = t + L - 1
            v = dp_deg(t, n)
            table[(t, n)] = v
            row.append(f"{v if v is not None else '·':>4}")
        print(f"{t:>5} " + "".join(row), flush=True)

    print("\n[B] CAND2 vs exact :")
    okc, gaps = 0, {}
    viol = []
    for (t, n), v in table.items():
        if v is None:
            continue
        c = cand2(t, n)
        if c > v:
            viol.append((t, n, c, v))
        elif c == v:
            okc += 1
        else:
            gaps.setdefault(v - c, []).append((t, n))
    total = okc + sum(len(g) for g in gaps.values())
    print(f"    exactes : {okc}/{total} ; VIOLATIONS (borne > vrai, "
          f"grave) : {len(viol)}")
    for delta in sorted(gaps):
        cells = gaps[delta]
        print(f"    ecart +{delta} : {len(cells)} cellules "
              f"(ex. {cells[:5]})")
    if viol:
        for v in viol[:10]:
            print(f"    *** VIOLATION : {v}")

    print("\n" + "=" * 70)
    print("CAND2 est une borne inferieure PROUVABLE (chaque ingredient est")
    print("un theoreme du fil). L'ecart residuel mesure ce que la structure")
    print("{1,2} fine ajoute -- la loi exacte reste l'automate (Lemme 2).")


if __name__ == "__main__":
    main()
