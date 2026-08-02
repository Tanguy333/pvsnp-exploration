"""MC-001 strategie C — complement :
(1) W_R (coefficients reels, gap >= 1, orientations binaires exactes) sur les
    1992 classes canoniques n=4 : la relaxation continue est-elle tight ?
(2) fonctions MONOTONES n<=4 : W vs couvert (#uns minimaux) — le zoo
    apparait-il avant n=6 ?
"""
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mc001_inverse_algorithmes import (w_real_milp, fvec_of_mask,
                                       canonical_map, min_ones, popcount)


def wr_classes(n=4):
    W = np.load(os.path.join(HERE, f"mc001_W_n{n}.npy"))
    canon = canonical_map(n)
    reps = np.unique(canon)
    t0 = time.time()
    gaps = {}
    worst = (1.0, None)
    echecs = 0
    for k, rep in enumerate(reps):
        m = int(rep)
        M = 1 << (1 << n)
        if m == 0 or m == M - 1:
            continue
        w = int(W[m])
        f = fvec_of_mask(m, n)
        res = w_real_milp(f, n, UB=w, integers=False, tl=60.0)
        if not res.success:
            echecs += 1
            continue
        wr = res.fun
        ratio = w / wr if wr > 1e-9 else float("inf")
        key = round(ratio, 3)
        gaps[key] = gaps.get(key, 0) + 1
        if ratio > worst[0] + 1e-9:
            worst = (ratio, (m, w, round(wr, 4)))
        if k % 200 == 0:
            print(f"  {k}/{len(reps)} ({time.time()-t0:.0f}s)", flush=True)
    print(f"n={n} : ratios W/W_R sur les classes (effectifs de classes) :",
          flush=True)
    for r in sorted(gaps):
        print(f"    ratio {r} : {gaps[r]} classes", flush=True)
    print(f"  pire ratio = {worst[0]:.4f} atteint par {worst[1]}", flush=True)
    print(f"  echecs MILP : {echecs}", flush=True)


def monotone(nmax=4):
    for n in (3, nmax):
        N = 1 << n
        W = np.load(os.path.join(HERE, f"mc001_W_n{n}.npy"))
        # enumere les fonctions monotones
        monos = []
        for m in range(1 << N):
            ok = True
            for x in range(N):
                if (m >> x) & 1:
                    continue
                # f(x)=0 : tout y < x doit etre 0 ? non : monotone =
                # x <= y => f(x) <= f(y)
            for x in range(N):
                for i in range(n):
                    if not (x >> i) & 1:
                        y = x | (1 << i)
                        if ((m >> x) & 1) > ((m >> y) & 1):
                            ok = False
                            break
                if not ok:
                    break
            if ok:
                monos.append(m)
        print(f"n={n} : {len(monos)} fonctions monotones", flush=True)
        diff = []
        for m in monos:
            if m == 0 or m == (1 << N) - 1:
                continue
            mo = min_ones(m, n)
            w = int(W[m])
            if w != mo:
                diff.append((m, w, mo))
        print(f"  W != #uns_minimaux pour {len(diff)} d'entre elles", flush=True)
        for m, w, mo in diff[:10]:
            print(f"    f={m:0{N}b} W={w} couvert={mo}", flush=True)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "mono":
        monotone()
    else:
        wr_classes()
