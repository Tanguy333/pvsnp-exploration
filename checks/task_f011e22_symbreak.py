"""
TACHE F-011, etape 22 -- n = 12, 13 avec CASSAGE DE SYMETRIE.

Les instances ont la symetrie S_n complete (permutation des variables
booleennes => permutation des t-sous-ensembles => permutation des
(u_T, v_T)) et la negation globale mod 3 (v -> 2v). Sans cassage, une
preuve UNSAT doit refuter chaque branche symetrique separement.

CASSAGE (partiel, sain : le representant lex-minimal de chaque orbite
survit) :
 - negation mod 3 : interdire v_{T0} = 2 pour T0 = premier monome ;
 - pour chaque transposition adjacente sigma_i = (i, i+1) :
   contrainte X <=_lex sigma(X), ou X = concatenation des bits
   (u_T, v1_T, v2_T) des monomes DEPLACES par sigma_i, dans l'ordre
   canonique. Encodage standard par variables de prefixe egal
   (implications seules -- relaxation saine).

Solveur : CryptoMiniSat (XOR natifs, elimination gaussienne),
--maxtime 2400 s par instance.
"""

from __future__ import annotations

import itertools
import subprocess
import time
from pathlib import Path

from task_f011e21c_cms import Enc, mod3_step, write_dimacs, verify

EXE = str(Path(__file__).resolve().parent.parent / "tools" / "cryptominisat5.exe")
MAXTIME = 2400


def build_sym(n):
    t = (n + 1) // 2
    monos = list(itertools.combinations(range(n), t))
    idx = {T: i for i, T in enumerate(monos)}
    e = Enc()
    u = [e.new() for _ in monos]
    v1 = [e.new() for _ in monos]
    v2 = [e.new() for _ in monos]
    for i in range(len(monos)):
        e.add([-v1[i], -v2[i]])
    # couverture (XOR natifs + chaines mod 3)
    for w in range(t, n + 1):
        for S in itertools.combinations(range(n), w):
            subs = [idx[T] for T in itertools.combinations(S, t)]
            US = e.new()
            e.add_xor([u[j] for j in subs] + [-US])
            s1, s2 = v1[subs[0]], v2[subs[0]]
            for j in subs[1:]:
                s1, s2 = mod3_step(e, s1, s2, v1[j], v2[j])
            e.add([US, s1, s2])
    # --- cassage 1 : negation mod 3 (v_{T0} != 2)
    e.add([-v2[0]])
    # --- cassage 2 : lex-leader pour les transpositions adjacentes
    def sigma_img(T, i):
        if (i in T) == (i + 1 in T):
            return None  # fixe
        s = set(T)
        if i in s:
            s.remove(i); s.add(i + 1)
        else:
            s.remove(i + 1); s.add(i)
        return tuple(sorted(s))
    for i in range(n - 1):
        moved = [(T, sigma_img(T, i)) for T in monos
                 if sigma_img(T, i) is not None]
        # paires de bits (x_k, y_k) dans l'ordre canonique des monomes
        bits = []
        for (T, Ti) in moved:
            a, b = idx[T], idx[Ti]
            bits.extend([(u[a], u[b]), (v1[a], v1[b]), (v2[a], v2[b])])
        # X <=lex Y : e_0 = vrai ; (e_{k-1} et x_k) -> y_k ;
        # e_k -> e_{k-1}, e_k -> (x_k <-> y_k)
        prev = None
        for k, (x, y) in enumerate(bits):
            if k == 0:
                e.add([-x, y])
                ek = e.new()
                e.add([-ek, -x, y])
                e.add([-ek, x, -y])
                prev = ek
            else:
                e.add([-prev, -x, y])
                if k < len(bits) - 1:
                    ek = e.new()
                    e.add([-ek, prev])
                    e.add([-ek, -x, y])
                    e.add([-ek, x, -y])
                    prev = ek
    return e, monos, u, v1, v2


def solve(path):
    r = subprocess.run([EXE, "--maxtime", str(MAXTIME), path],
                       capture_output=True, text=True)
    out = r.stdout
    if "s SATISFIABLE" in out:
        model = set()
        for line in out.splitlines():
            if line.startswith("v "):
                for tok in line[2:].split():
                    val = int(tok)
                    if val > 0:
                        model.add(val)
        return True, model
    if "s UNSATISFIABLE" in out:
        return False, None
    return None, None


def main() -> None:
    print("TACHE F-011 e22 -- n = 12, 13 avec cassage de symetrie (CMS)")
    print("=" * 64)
    for n in (12, 13):
        t = (n + 1) // 2
        t0 = time.time()
        e, monos, u, v1, v2 = build_sym(n)
        path = f"cms_sym_n{n}.cnf"
        write_dimacs(e, path)
        print(f"\nn = {n} : {e.nv} vars, {len(e.cnf)} CNF + {len(e.xors)} XOR "
              f"(avec lex-leader {n-1} generateurs) ({time.time()-t0:.0f}s)",
              flush=True)
        t0 = time.time()
        res, model = solve(path)
        dt = time.time() - t0
        if res is True:
            ok = verify(n, model, monos, u, v1, v2)
            print(f"  SAT ({dt:.0f}s) ; verification 2^{n} : "
                  f"{'OK' if ok else '*** ECHEC ***'}")
            print(f"  => deg_6(MAJ_{n}) = {t} : plate CONFIRMEE.", flush=True)
        elif res is False:
            print(f"  UNSAT ({dt:.0f}s)")
            print(f"  => deg_6(MAJ_{n}) >= {t+1} : PLATE REFUTEE a n = {n}.",
                  flush=True)
        else:
            print(f"  INDECIS apres {dt:.0f}s (maxtime {MAXTIME}s)", flush=True)


if __name__ == "__main__":
    main()
