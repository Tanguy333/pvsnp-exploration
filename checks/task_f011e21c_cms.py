"""
TACHE F-011, etape 21c -- n = 12, 13 via CryptoMiniSat 5.14.5 (binaire
officiel Windows, tools/cryptominisat5.exe) avec clauses XOR NATIVES :
toute la partie mod 2 part en elimination gaussienne, la ou CDCL pur
(CaDiCaL) thrash sur le raisonnement de parite.

Encodage : u_T binaires ; v_T en 2 bits (interdit 11) ; par ensemble S :
  ligne XOR native  " x u_{T1} ... u_{Tk} -U_S 0 "  (<=> U_S = XOR des u),
  chaine d'etats mod 3 (CNF, 18 clauses/pas),
  couverture (U_S ou s1 ou s2).
Budget : --maxtime 1200 s par instance. Verification exhaustive si SAT.
"""

from __future__ import annotations

import itertools
import subprocess
import time
from pathlib import Path

EXE = str(Path(__file__).resolve().parent.parent / "tools" / "cryptominisat5.exe")
MAXTIME = 1200


class Enc:
    def __init__(self):
        self.nv = 0
        self.cnf = []
        self.xors = []

    def new(self):
        self.nv += 1
        return self.nv

    def add(self, cl):
        self.cnf.append(cl)

    def add_xor(self, lits):
        self.xors.append(lits)


def mod3_step(e, s1, s2, w1, w2):
    t1, t2 = e.new(), e.new()
    bits = {0: (0, 0), 1: (1, 0), 2: (0, 1)}
    for s in range(3):
        for v in range(3):
            r = (s + v) % 3
            sb, vb, rb = bits[s], bits[v], bits[r]
            ante = [s1 if sb[0] else -s1, s2 if sb[1] else -s2,
                    w1 if vb[0] else -w1, w2 if vb[1] else -w2]
            e.add([-l for l in ante] + [t1 if rb[0] else -t1])
            e.add([-l for l in ante] + [t2 if rb[1] else -t2])
    return t1, t2


def build(n):
    t = (n + 1) // 2
    monos = list(itertools.combinations(range(n), t))
    idx = {T: i for i, T in enumerate(monos)}
    e = Enc()
    u = [e.new() for _ in monos]
    v1 = [e.new() for _ in monos]
    v2 = [e.new() for _ in monos]
    for i in range(len(monos)):
        e.add([-v1[i], -v2[i]])
    for w in range(t, n + 1):
        for S in itertools.combinations(range(n), w):
            subs = [idx[T] for T in itertools.combinations(S, t)]
            US = e.new()
            e.add_xor([u[j] for j in subs] + [-US])   # XOR natif
            s1, s2 = v1[subs[0]], v2[subs[0]]
            for j in subs[1:]:
                s1, s2 = mod3_step(e, s1, s2, v1[j], v2[j])
            e.add([US, s1, s2])
    return e, monos, u, v1, v2


def write_dimacs(e, path):
    with open(path, "w") as f:
        f.write(f"p cnf {e.nv} {len(e.cnf) + len(e.xors)}\n")
        for cl in e.cnf:
            f.write(" ".join(map(str, cl)) + " 0\n")
        for xl in e.xors:
            f.write("x " + " ".join(map(str, xl)) + " 0\n")


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


def verify(n, model, monos, u, v1, v2):
    t = (n + 1) // 2
    uu = [1 if u[i] in model else 0 for i in range(len(monos))]
    vv = [(1 if v1[i] in model else 0) + (2 if v2[i] in model else 0)
          for i in range(len(monos))]
    Tsets = [frozenset(T) for T in monos]
    for x in range(1 << n):
        S = frozenset(i for i in range(n) if (x >> i) & 1)
        w = len(S)
        U = sum(c for Ts, c in zip(Tsets, uu) if Ts <= S) % 2
        V = sum(c for Ts, c in zip(Tsets, vv) if Ts <= S) % 3
        if w < t and (U or V):
            return False
        if w >= t and not (U or V):
            return False
    return True


def main() -> None:
    print("TACHE F-011 e21c -- n = 12, 13 via CryptoMiniSat (XOR natifs)")
    print("=" * 62)
    for n in (12, 13):
        t = (n + 1) // 2
        t0 = time.time()
        e, monos, u, v1, v2 = build(n)
        path = f"cms_n{n}.cnf"
        write_dimacs(e, path)
        print(f"\nn = {n} : {e.nv} vars, {len(e.cnf)} clauses CNF + "
              f"{len(e.xors)} XOR natifs ({time.time()-t0:.0f}s)", flush=True)
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
            print(f"  => deg_6(MAJ_{n}) >= {t+1} : PLATE REFUTEE.", flush=True)
        else:
            print(f"  INDECIS apres {dt:.0f}s (maxtime {MAXTIME}s)",
                  flush=True)


if __name__ == "__main__":
    main()
