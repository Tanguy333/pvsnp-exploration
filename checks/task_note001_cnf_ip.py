"""
TACHE NOTE-001 -- la version CNF de la note T-F006 (reserve §6.3).

THEOREME vise : CNF_min(IP_{2n}) = (3^n + 1)/2.
Par De Morgan, CNF_min(f) = DNF_min(-f) ; et -IP_{2(n+1)} =
-IP_{2n} XOR (x_{n+1} AND y_{n+1}) — la bi-decomposition de Tour 18
est invariante par complementation, donc la classification A1/A2a/A2b,
la recurrence b_{n+1} = a_n + 2 b_n et l'essentialite se transferent.

Verification directe n = 1..4 (3^{2n} termes, force brute) :
  1. |primes(-IP_{2n})| = (3^n + 1)/2  (= 2, 5, 14, 41) ;
  2. CHAQUE premier de -IP est essentiel (temoin prive) =>
     DNF_min(-IP) = b_n => CNF_min(IP) = b_n ;
  3. controle croise cote IP : |primes(IP)| = (3^n - 1)/2, tous
     essentiels (re-verification de la note §2).
"""

from __future__ import annotations

from itertools import product


def primes_and_essential(nvars, truth):
    """Implicants premiers de la fonction truth : {0,1}^nvars -> {0,1},
    et essentialite de chacun (temoin couvert par lui seul)."""
    # terme = tuple dans {0,1,None}^nvars (None = libre)
    def covers(term, x):
        return all(t is None or t == xi for t, xi in zip(term, x))

    def is_implicant(term):
        return all(truth[x] for x in product((0, 1), repeat=nvars)
                   if covers(term, x))

    # enumere tous les termes, garde les implicants non vides
    implicants = []
    for term in product((0, 1, None), repeat=nvars):
        if all(t is None for t in term):
            continue
        if is_implicant(term):
            implicants.append(term)
    if truth[tuple([0] * nvars)] and all(truth[x] for x in
                                         product((0, 1), repeat=nvars)):
        raise ValueError("fonction constante 1")

    def weaken(term, i):
        t = list(term)
        t[i] = None
        return tuple(t)

    imp_set = set(implicants)
    primes = [t for t in implicants
              if all(t[i] is None or weaken(t, i) not in imp_set
                     for i in range(nvars))]

    # essentialite : pour chaque premier, existe-t-il un point couvert
    # par lui et par aucun autre premier ?
    essential = []
    for p in primes:
        others = [q for q in primes if q != p]
        witness = None
        for x in product((0, 1), repeat=nvars):
            if truth[x] and covers(p, x) and \
                    not any(covers(q, x) for q in others):
                witness = x
                break
        essential.append(witness is not None)
    return primes, essential


def main():
    for n in range(1, 5):
        nvars = 2 * n
        ip = {}
        for x in product((0, 1), repeat=nvars):
            ip[x] = sum(x[i] * x[n + i] for i in range(n)) % 2
        nip = {x: 1 - v for x, v in ip.items()}

        pa, ea = primes_and_essential(nvars, ip)
        pb, eb = primes_and_essential(nvars, nip)
        an, bn = (3 ** n - 1) // 2, (3 ** n + 1) // 2
        print(f"n={n} (2n={nvars} vars) :")
        print(f"  |primes(IP)|  = {len(pa)}  (attendu {an}) "
              f"{'OK' if len(pa) == an else 'ECHEC'} ; "
              f"essentiels {sum(ea)}/{len(pa)} "
              f"{'OK' if all(ea) else 'ECHEC'}")
        print(f"  |primes(-IP)| = {len(pb)}  (attendu {bn}) "
              f"{'OK' if len(pb) == bn else 'ECHEC'} ; "
              f"essentiels {sum(eb)}/{len(pb)} "
              f"{'OK' if all(eb) else 'ECHEC'}")
        print(f"  => CNF_min(IP_{2*n}) = DNF_min(-IP) = {len(pb)} "
              f"= (3^{n}+1)/2 : "
            f"{'CONFIRME' if len(pb) == bn and all(eb) else 'ECHEC'}",
              flush=True)


if __name__ == "__main__":
    main()
