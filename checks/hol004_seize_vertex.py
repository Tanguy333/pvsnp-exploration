# -*- coding: utf-8 -*-
r"""HOL-004 — La grille seize-vertex : classement exécutable du coin
ouvert de l'arité 4 (cahier des charges : HOL-003 / bib/holant_arites_paires.md).

Objet : f : {0,1}^4 -> valeurs (ici 0/1 puis 0/±1), 16 composantes,
bit i de x = (x >> i) & 1. Chaque f est classée contre :
  (Z1) réductible (un produit tensoriel sur une bipartition) — cas FERMÉ
       (ramené aux arités <= 3, MWXZ Th. 1) ;
  (Z2) symétrique — FERMÉ (CGW) ;
  (Z3) zone huit-vertex : supp(K^-1 f) ⊆ poids pairs — FERMÉE
       (Cai-Fu 2023 / FCST 2026) ;
  (Z4) zone #EO/HW : supp(K^-1 f) ⊆ HW>= ou HW<= ou single-weighted —
       FERMÉE (MWXZ Cor. 30 / Th. 31) ; strict => VANISHING (Lemma 42) ;
  (T1) A directe (support affine + valeurs i^Q, Q quadratique à termes
       croisés pairs — Shao-Cai Def. 2.18) ;
  (T2) P directe (produit d'unaires, =2, !=2 — Def. 2.17) ;
  (T3) M directe (parité + MGI d'arité 4, FCST Lemma 2.24) ;
  (T4) L directe (pour chaque sigma du support, le shift diag(1,alpha)
       envoie f dans A — CLX SODA 2018 Def. 3.1) ;
  COIN sinon : « hors de toute classe DÉCIDÉE ICI ».

AVERTISSEMENT DE PÉRIMÈTRE (consigné aussi dans data/) : les
transformées (A-/P-/L-/M-transformable, réel-transformable) ne sont
PAS testées ici (balayage O2(C)/GL2 par Gröbner = HOL-005 candidat).
Le COIN de ce scan signifie « hors de A/P/M/L directes et des zones
fermées » — c'est une SURESTIMATION du vrai coin, jamais une
sous-estimation des zones fermées. Aucune #P-dureté n'est décidée.

Arithmétique EXACTE : entiers de Gauss (complex à parties entières) ;
K~^-1 = [[1,-i],[1,i]] sans normalisation (les tests sont des tests de
support/annulation, insensibles à l'échelle). Pour L : exposants
d'alpha = e^{i pi/4} tenus en entiers mod 8.
"""
from __future__ import annotations

import itertools
import sys
import time

W = [bin(x).count("1") for x in range(16)]
PAIRES_BIP = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]
UN_TROIS = [(0,), (1,), (2,), (3,)]


def bits(x):
    return [(x >> i) & 1 for i in range(4)]


# ------------------------------------------------------ Z1 réductibilité

def rang_le_1(M):
    """M = liste de lignes (valeurs complexes entières) ; rang <= 1 ?"""
    lignes = [l for l in M if any(v != 0 for v in l)]
    if len(lignes) <= 1:
        return True
    l0 = lignes[0]
    for l in lignes[1:]:
        # l proportionnelle a l0 : minors 2x2 nuls
        for a in range(len(l0)):
            for b in range(a + 1, len(l0)):
                if l0[a] * l[b] - l0[b] * l[a] != 0:
                    return False
    return True


def reductible(f):
    for (g1, g2) in PAIRES_BIP:
        M = [[f[sum(((ab >> k) & 1) << g1[k] for k in range(2))
               | sum(((cd >> k) & 1) << g2[k] for k in range(2))]
              for cd in range(4)] for ab in range(4)]
        if rang_le_1(M):
            return True
    for (i,) in UN_TROIS:
        reste = [j for j in range(4) if j != i]
        M = [[f[(a << i)
               | sum(((b >> k) & 1) << reste[k] for k in range(3))]
              for b in range(8)] for a in range(2)]
        if rang_le_1(M):
            return True
    return False


# ------------------------------------------------------------- Z2 symétrie

def symetrique(f):
    par_poids = {}
    for x in range(16):
        par_poids.setdefault(W[x], set()).add(f[x])
    return all(len(s) == 1 for s in par_poids.values())


# ------------------------------------------------- K-transformée (exacte)

def k_transforme(f):
    """f^ = (K~^-1)^{tensor 4} f, K~^-1 = [[1,-i],[1,i]] (bit a bit)."""
    g = list(f)
    for i in range(4):
        h = [0] * 16
        for x in range(16):
            x0 = x & ~(1 << i)
            x1 = x | (1 << i)
            if (x >> i) & 1 == 0:
                h[x] = g[x0] + (-1j) * g[x1]
            else:
                h[x] = g[x0] + (1j) * g[x1]
        g = h
    return [complex(round(v.real), round(v.imag)) for v in g]


def zones_K(f):
    fh = k_transforme(f)
    supp = [x for x in range(16) if fh[x] != 0]
    if not supp:
        return "nulle"
    poids = {W[x] for x in supp}
    if poids <= {0, 2, 4}:
        return "huit-vertex"
    if all(w >= 2 for w in poids):
        return "vanishing" if all(w > 2 for w in poids) else "HW>="
    if all(w <= 2 for w in poids):
        return "vanishing" if all(w < 2 for w in poids) else "HW<="
    if len(poids) == 1:
        return "single-weighted"
    return "K-mixte"


# --------------------------------------------------------- T1 : A directe

def puissance_de_i(v):
    """v = i^k * r, r > 0 reel ? renvoie k mod 4 ou None (v entier
    de Gauss, on exige v dans {r, ri, -r, -ri})."""
    if v == 0:
        return None
    if v.imag == 0:
        return 0 if v.real > 0 else 2
    if v.real == 0:
        return 1 if v.imag > 0 else 3
    return None


def support_affine(supp):
    s = set(supp)
    if not s:
        return False
    for a in s:
        for b in s:
            for c in s:
                if a ^ b ^ c not in s:
                    return False
    return True


def base_affine(supp):
    """supp affine : renvoie (x0, [e1..ed]) tel que supp = x0 + <ei>."""
    x0 = supp[0]
    lin = sorted({x ^ x0 for x in supp})
    base = []
    engendre = {0}
    for v in lin:
        if v not in engendre:
            base.append(v)
            engendre |= {g ^ v for g in engendre}
    return x0, base


def est_A(f):
    supp = [x for x in range(16) if f[x] != 0]
    if not support_affine(supp):
        return False
    exps = {}
    for x in supp:
        k = puissance_de_i(f[x] / f[supp[0]]) if f[supp[0]] != 0 else None
        # valeurs 0/±1/±i : ratio exact
        r = f[x] * (f[supp[0]].conjugate())
        k = puissance_de_i(r)
        if k is None:
            return False
        exps[x] = k
    x0, base = base_affine(supp)
    d = len(base)
    # Q(t) = sum c_i t_i + sum_{i<j} c_ij t_i t_j (mod 4), c_ij pair
    lins = list(itertools.product(range(4), repeat=d))
    croix = list(itertools.product((0, 2), repeat=d * (d - 1) // 2))
    pts = []
    for t in range(1 << d):
        x = x0
        for k in range(d):
            if (t >> k) & 1:
                x ^= base[k]
        pts.append((t, exps[x] - exps[x0]))
    for cl in lins:
        for cc in croix:
            ok = True
            for (t, e) in pts:
                q = 0
                for k in range(d):
                    if (t >> k) & 1:
                        q += cl[k]
                idx = 0
                for a in range(d):
                    for b in range(a + 1, d):
                        if (t >> a) & 1 and (t >> b) & 1:
                            q += cc[idx]
                        idx += 1
                if (q - e) % 4 != 0:
                    ok = False
                    break
            if ok:
                return True
    return False


# --------------------------------------------------------- T2 : P directe

def partitions_ensemble(elts):
    if not elts:
        yield []
        return
    tete, reste = elts[0], elts[1:]
    for p in partitions_ensemble(reste):
        yield [[tete]] + p
        for i in range(len(p)):
            yield p[:i] + [[tete] + p[i]] + p[i + 1:]


def est_P(f):
    supp = [x for x in range(16) if f[x] != 0]
    n = len(supp)
    if n == 0 or (n & (n - 1)) != 0:
        return False
    for part in partitions_ensemble([0, 1, 2, 3]):
        # dans chaque bloc : variables liees par egalites/inegalites en
        # chaine -> motifs de signes s (var j = t xor s_j), bloc libre
        # (2 valeurs) ; f doit se factoriser en produit de fonctions de
        # bloc (unaire sur le representant)
        for signes in itertools.product(
                *[[tuple(s) for s in itertools.product((0, 1),
                                                       repeat=len(B) - 1)]
                  for B in part]):
            def val_bloc(B, sg, t):
                # variables du bloc : B[0] = t ; B[k] = t xor sg[k-1]
                return {B[0]: t, **{B[k]: t ^ sg[k - 1]
                                    for k in range(1, len(B))}}
            # resoudre les fonctions de bloc par les valeurs de f
            ts = list(itertools.product((0, 1), repeat=len(part)))
            coh = True
            vals = {}
            for tt in ts:
                assign = {}
                for B, sg, t in zip(part, signes, tt):
                    assign.update(val_bloc(B, sg, t))
                x = sum(assign[i] << i for i in range(4))
                vals[tt] = f[x]
            # f(t1..tk) doit etre un produit u1(t1)...uk(tk) :
            # test par minors sur chaque paire de coordonnees
            for a in range(len(part)):
                for tfix in itertools.product((0, 1), repeat=len(part) - 1):
                    pass
            # test produit : pour toute paire tt, ss :
            # f(tt)*f(ss') ... plus simple : rang 1 iteratif
            def produit_ok(vals, k):
                if k == 0:
                    return True
                M = {}
                for tt, v in vals.items():
                    M.setdefault(tt[0], {})[tt[1:]] = v
                lignes = [M[a] for a in M if any(M[a].values())]
                if len(lignes) >= 2:
                    cles = list(lignes[0].keys())
                    l0 = lignes[0]
                    for l in lignes[1:]:
                        for i in range(len(cles)):
                            for j in range(i + 1, len(cles)):
                                if (l0[cles[i]] * l[cles[j]]
                                        - l0[cles[j]] * l[cles[i]]) != 0:
                                    return False
                if not lignes:
                    return True
                sous = lignes[0]
                return produit_ok({t: v for t, v in sous.items()}, k - 1)
            if produit_ok(vals, len(part)):
                coh = True
                return True
    return False


# --------------------------------------------------------- T3 : M directe

def est_M(f):
    supp = [x for x in range(16) if f[x] != 0]
    if not supp:
        return True
    pairs = all(W[x] % 2 == 0 for x in supp)
    impairs = all(W[x] % 2 == 1 for x in supp)
    ix = lambda b1, b2, b3, b4: b1 | (b2 << 1) | (b3 << 2) | (b4 << 3)
    if pairs:
        d_out = (f[ix(0, 0, 0, 0)] * f[ix(1, 1, 1, 1)]
                 - f[ix(0, 0, 1, 1)] * f[ix(1, 1, 0, 0)])
        d_in = (f[ix(0, 1, 1, 0)] * f[ix(1, 0, 0, 1)]
                - f[ix(0, 1, 0, 1)] * f[ix(1, 0, 1, 0)])
        return d_out == d_in
    if impairs:
        return (f[ix(0, 0, 1, 0)] * f[ix(1, 1, 0, 1)]
                - f[ix(0, 0, 0, 1)] * f[ix(1, 1, 1, 0)]
                == f[ix(0, 1, 0, 0)] * f[ix(1, 0, 1, 1)]
                - f[ix(0, 1, 1, 1)] * f[ix(1, 0, 0, 0)])
    return False


# --------------------------------------------------------- T4 : L directe
# (valeurs 0/±1/±i : les shifts diag(1, alpha) donnent des exposants
# d'alpha mod 8 ; f_sigma dans A exige des exposants pairs relatifs +
# forme Q — on teste : support affine (le meme pour tout sigma) et pour
# chaque sigma, exposants alpha^{<sigma,x>} * i^{k(x)} relatifs pairs et
# la forme Q sur les demi-exposants.)

def est_L(f):
    supp = [x for x in range(16) if f[x] != 0]
    if not support_affine(supp):
        return False
    for sigma in supp:
        exps = {}
        ok = True
        for x in supp:
            r = f[x] * (f[supp[0]].conjugate())
            k = puissance_de_i(r)
            if k is None:
                return False
            e8 = (2 * k + sum(bits(sigma)[i] * bits(x)[i]
                              for i in range(4))
                  - sum(bits(sigma)[i] * bits(supp[0])[i]
                        for i in range(4))) % 8
            if e8 % 2 != 0:
                ok = False
                break
            exps[x] = (e8 // 2) % 4
        if not ok:
            return False
        x0, base = base_affine(supp)
        d = len(base)
        lins = list(itertools.product(range(4), repeat=d))
        croix = list(itertools.product((0, 2), repeat=d * (d - 1) // 2))
        pts = []
        for t in range(1 << d):
            x = x0
            for k in range(d):
                if (t >> k) & 1:
                    x ^= base[k]
            pts.append((t, (exps[x] - exps[x0]) % 4))
        trouve = False
        for cl in lins:
            for cc in croix:
                bon = True
                for (t, e) in pts:
                    q = sum(cl[k] for k in range(d) if (t >> k) & 1)
                    idx = 0
                    for a in range(d):
                        for b in range(a + 1, d):
                            if (t >> a) & 1 and (t >> b) & 1:
                                q += cc[idx]
                            idx += 1
                    if (q - e) % 4 != 0:
                        bon = False
                        break
                if bon:
                    trouve = True
                    break
            if trouve:
                break
        if not trouve:
            return False
    return True


# ------------------------------------------------------------- le verdict

def classe(f):
    if all(v == 0 for v in f):
        return "nulle"
    if reductible(f):
        return "Z1-reductible"
    if symetrique(f):
        return "Z2-symetrique"
    # CORRECTION (prise du premier scan) : toute signature a valeurs
    # REELLES est couverte par la dichotomie de Shao-Cai FOCS 2020 —
    # elle est HORS de la poche ouverte, quel que soit son statut face
    # aux tests directs. La poche exige du complexe non reel.
    if all(complex(v).imag == 0 for v in f):
        return "Z-reel(Shao-Cai)"
    z = zones_K(f)
    if z in ("huit-vertex", "HW>=", "HW<=", "single-weighted", "vanishing"):
        return "Z-" + z
    if est_A(f):
        return "T1-A"
    if est_P(f):
        return "T2-P"
    if est_M(f):
        return "T3-M"
    if est_L(f):
        return "T4-L"
    return "COIN"


def calibration():
    print("=== CALIBRATION ===")
    eq4 = [0] * 16
    eq4[0] = 1
    eq4[15] = 1
    print(f"  EQ4 [1,0,0,0,1]           : {classe(eq4)} (attendu Z2-symetrique)")
    prod = [0] * 16
    for x in range(16):
        b = bits(x)
        prod[x] = (1 if b[0] == b[1] else 0) * (1 if b[2] != b[3] else 0)
    print(f"  (x1=x2)(x3!=x4)           : {classe(prod)} (attendu Z1-reductible)")
    van = [0] * 16  # f = K (support HW>) : vanishing par construction
    # on construit f^ a support {poids 3, 4} puis f = K~ f^ n'est pas
    # entier simple — on teste directement la zone via un f dont la
    # K-transformee est a support haut : prendre f^ voulu et verifier
    # zones_K(K~ f^) — hors scan ; a defaut : controle de detection
    # huit-vertex par un f de support K-pair connu : f = signature du
    # modele six-vertex [support poids 2 dans le monde !=2] transforme —
    # controle simplifie : verifier qu'EQ4 transforme est bien detecte.
    aff = [0] * 16
    for x in (0, 3, 5, 6):
        aff[x] = 1
    print(f"  support {{0,3,5,6}} (affine): {classe(aff)}")
    xor_odd = [1 if W[x] % 2 == 1 else 0 for x in range(16)]
    print(f"  indicatrice poids impairs : {classe(xor_odd)} (parite impaire, MGI ?)")


def scan_01():
    print("\n=== SCAN EXHAUSTIF : les 65 536 signatures 0/1 ===")
    t0 = time.time()
    comptes = {}
    coins = []
    for masque in range(1 << 16):
        f = [(masque >> x) & 1 for x in range(16)]
        c = classe(f)
        comptes[c] = comptes.get(c, 0) + 1
        if c == "COIN" and len(coins) < 12:
            coins.append(masque)
    print(f"  [{time.time() - t0:.0f}s]")
    for c in sorted(comptes, key=lambda k: -comptes[k]):
        print(f"  {c:18} : {comptes[c]:6}")
    print("\n  PREMIÈRES ÉPINGLES DU COIN (supports, valeurs = 1) :")
    for m in coins:
        supp = [x for x in range(16) if (m >> x) & 1]
        print(f"    masque {m:5} : supp = {[format(x, '04b') for x in supp]}")
    return comptes, coins


def echantillon_pm1(n_ech=4000):
    print(f"\n=== ÉCHANTILLON 0/±1 ({n_ech} signatures aléatoires) ===")
    import random
    rng = random.Random(20260808)
    t0 = time.time()
    comptes = {}
    coins = []
    for _ in range(n_ech):
        f = [rng.choice((0, 1, -1)) for _ in range(16)]
        c = classe(f)
        comptes[c] = comptes.get(c, 0) + 1
        if c == "COIN" and len(coins) < 5:
            coins.append(list(f))
    print(f"  [{time.time() - t0:.0f}s]")
    for c in sorted(comptes, key=lambda k: -comptes[k]):
        print(f"  {c:18} : {comptes[c]:6}")
    if coins:
        print("  exemples COIN (valeurs sur 0..15) :")
        for f in coins:
            print(f"    {f}")


def echantillon_complexe(n_ech=8000):
    """LA vraie chasse : valeurs dans {0, ±1, ±i} (complexes, entiers
    de Gauss exacts). COIN = candidat du coin — avec l'avertissement
    de perimetre (transformees et reel-transformabilite non testees)."""
    print(f"\n=== ÉCHANTILLON COMPLEXE 0/±1/±i ({n_ech} signatures) ===")
    import random
    rng = random.Random(20260808)
    t0 = time.time()
    comptes = {}
    coins = []
    vals = (0, 1, -1, 1j, -1j)
    for _ in range(n_ech):
        f = [rng.choice(vals) for _ in range(16)]
        c = classe(f)
        comptes[c] = comptes.get(c, 0) + 1
        if c == "COIN" and len(coins) < 6:
            coins.append(list(f))
    print(f"  [{time.time() - t0:.0f}s]")
    for c in sorted(comptes, key=lambda k: -comptes[k]):
        print(f"  {c:18} : {comptes[c]:6}")
    if coins:
        print("  ÉPINGLES COMPLEXES candidates (valeurs sur x = 0..15,")
        print("  i note j ; reserve : transformees non testees) :")
        for f in coins:
            print(f"    {f}")


def scan_supports_i():
    """Scan structure : support de taille 3-6 avec valeurs dans {1, i}
    — exhaustif sur un sous-espace cible (supports K-mixtes candidats),
    pour des epingles REPRODUCTIBLES plutot qu'aleatoires."""
    print("\n=== SCAN STRUCTURÉ : supports de taille 3, valeurs {1, i} ===")
    t0 = time.time()
    comptes = {}
    coins = []
    for supp in itertools.combinations(range(16), 3):
        for pat in range(1, 1 << 3):  # au moins un i (sinon reel)
            f = [0] * 16
            for k, x in enumerate(supp):
                f[x] = 1j if (pat >> k) & 1 else 1
            c = classe(f)
            comptes[c] = comptes.get(c, 0) + 1
            if c == "COIN" and len(coins) < 10:
                coins.append((supp, pat))
    print(f"  [{time.time() - t0:.0f}s]  ({sum(comptes.values())} signatures)")
    for c in sorted(comptes, key=lambda k: -comptes[k]):
        print(f"  {c:18} : {comptes[c]:6}")
    print("  ÉPINGLES structurées (support ; positions en i) :")
    for supp, pat in coins:
        marque = [f"{format(x, '04b')}{'*i' if (pat >> k) & 1 else ''}"
                  for k, x in enumerate(supp)]
        print(f"    {marque}")


if __name__ == "__main__":
    quel = sys.argv[1] if len(sys.argv) > 1 else "tout"
    if quel in ("tout", "cal"):
        calibration()
    if quel in ("tout", "scan"):
        scan_01()
    if quel in ("tout", "pm1"):
        echantillon_pm1()
    if quel in ("tout", "cplx"):
        echantillon_complexe()
    if quel in ("tout", "structi"):
        scan_supports_i()
