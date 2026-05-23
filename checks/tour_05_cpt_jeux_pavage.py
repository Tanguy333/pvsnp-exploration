"""
Tour 05 -- Refutation du Lemme 3 (Duplicateur gagne le jeu de pavage bijectif
entre H_SAT et H_UNSAT).

Le Proposeur veut construire deux fonctions booleennes f (UNSAT) et g (SAT)
telles que les hypercubes colores H_f = ({0,1}^n, ~, f) et H_g sont
CPT+C-equivalents (i.e. indistinguables par toute formule en Choiceless
Polynomial Time with Counting).

CONTRE-ARGUMENT (vue d'ensemble) :

  La formule du PREMIER ORDRE suivante distingue trivialement H_f de H_g :

      phi_SAT  :=  exists x . f(x) = 1

  Sur H_f (UNSAT)  : aucun sommet n'est colore 1 -> phi_SAT est FAUSSE.
  Sur H_g (SAT)    : au moins un sommet est colore 1 -> phi_SAT est VRAIE.

  Or FO subset FO+C subset CPT+C (chaine d'inclusions standard en complexite
  descriptive). Donc phi_SAT est CPT+C-definissable. Donc CPT+C distingue
  H_f et H_g. Donc le Lemme 3 (existence d'une strategie gagnante pour le
  Duplicateur) est IMPOSSIBLE pour tout couple SAT/UNSAT.

  Plus formellement encore, le compte des sommets colores en 1 est lui aussi
  definissable en FO+C (et a fortiori en CPT+C) : #{x : f(x)=1}. Ce compte
  diffère entre H_f (= 0) et H_g (> 0). Tout jeu de pavage BIJECTIF a 1 tour
  permet au Spoiler de gagner immediatement en marquant un sommet colore 1
  dans H_g — le Duplicateur ne peut pas repondre dans H_f.

VERIFICATION EMPIRIQUE :

  On instancie 3 paires (f UNSAT, g SAT) sur m = 6 variables, et on calcule
  les invariants elementaires :
    * Cardinal de chaque couleur dans l'hypercube : (#{x : f(x)=0}, #{x : f(x)=1}).
    * Existence d'un sommet colore 1 : exists x. f(x) = 1.
  Tous ces invariants sont FO ou FO+C-definissables, donc CPT+C-definissables.
  On observe qu'ils separent H_f de H_g pour les 3 paires testees.

CONSEQUENCE :

  Le Lemme 3 du Proposeur exige H_f ≡_{CPT+C} H_g pour des fonctions f et g
  avec un statut SAT/UNSAT different. C'est imediatement contradictoire :
  l'encodage choisi (la coloration du SAT/UNSAT comme predicat unaire sur
  l'hypercube) rend la propriete distinguante TRIVIALEMENT definissable en
  FO. Le programme est ne dans une impasse.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass


Literal = tuple[int, int]
Clause = tuple[Literal, ...]


def evaluate_cnf(clauses: list[Clause], a: tuple[int, ...]) -> bool:
    return all(
        any(
            (a[i] == 1 and sign == 1) or (a[i] == 0 and sign == -1)
            for (i, sign) in c
        )
        for c in clauses
    )


def witnesses(clauses: list[Clause], m: int) -> list[tuple[int, ...]]:
    return [a for a in itertools.product((0, 1), repeat=m) if evaluate_cnf(clauses, a)]


@dataclass
class Instance:
    name: str
    clauses: list[Clause]
    m: int


def make_pairs() -> list[tuple[Instance, Instance]]:
    """ 3 paires (f UNSAT, g SAT) sur m=6 variables. """
    m = 6

    # Paire 1 : UNSAT minimal vs SAT minimal
    f1_unsat: list[Clause] = [
        ((0, 1),),
        ((0, -1),),  # x_0 et ~x_0 -> UNSAT
    ]
    g1_sat: list[Clause] = [
        ((0, 1),),  # juste x_0 -> SAT (toute assignation avec x_0=1)
    ]

    # Paire 2 : UNSAT 3-CNF strict vs SAT 3-CNF
    f2_unsat: list[Clause] = []
    for s0 in (-1, 1):
        for s1 in (-1, 1):
            for s2 in (-1, 1):
                f2_unsat.append(((0, s0), (1, s1), (2, s2)))
    g2_sat: list[Clause] = [
        ((0, 1), (1, 1), (2, 1)),
        ((3, 1), (4, 1), (5, 1)),
    ]

    # Paire 3 : memes variables apparaissent dans les deux, paire mieux comparable
    f3_unsat: list[Clause] = [
        ((0, 1), (1, 1), (2, 1)),
        ((0, -1), (1, 1), (2, 1)),
        ((0, 1), (1, -1), (2, 1)),
        ((0, -1), (1, -1), (2, 1)),
        ((0, 1), (1, 1), (2, -1)),
        ((0, -1), (1, 1), (2, -1)),
        ((0, 1), (1, -1), (2, -1)),
        ((0, -1), (1, -1), (2, -1)),
    ]
    g3_sat: list[Clause] = [
        ((0, 1), (1, 1), (2, 1)),
    ]

    return [
        (Instance("(1) UNSAT minimal x_0 ∧ ¬x_0",   f1_unsat, m),
         Instance("(1) SAT x_0",                     g1_sat,   m)),
        (Instance("(2) UNSAT 3-CNF complet sur x_0..2", f2_unsat, m),
         Instance("(2) SAT (x_0∨x_1∨x_2)∧(x_3∨x_4∨x_5)", g2_sat, m)),
        (Instance("(3) UNSAT 3-CNF (huit clauses)",  f3_unsat, m),
         Instance("(3) SAT (x_0∨x_1∨x_2)",            g3_sat,   m)),
    ]


def color_signature(inst: Instance) -> tuple[int, int]:
    """ (#sommets coloriés 0, #sommets coloriés 1) dans H_{f}.
        Definissable en FO+C, donc en CPT+C. """
    w = witnesses(inst.clauses, inst.m)
    n_one = len(w)
    n_zero = (1 << inst.m) - n_one
    return n_zero, n_one


def exists_witness(inst: Instance) -> bool:
    """ Sentence FO : exists x . f(x) = 1. Definissable en FO, donc en CPT+C. """
    return len(witnesses(inst.clauses, inst.m)) > 0


def main() -> None:
    print("Tour 05 -- Refutation du Lemme 3 (CPT+C ne peut PAS confondre SAT et UNSAT)")
    print("=" * 78)
    print()
    print(
        "Le Proposeur veut construire H_f (UNSAT) et H_g (SAT) CPT+C-equivalents.\n"
        "On montre que les invariants ELEMENTAIRES (FO ou FO+C) les distinguent\n"
        "immediatement, donc CPT+C aussi puisque FO subset FO+C subset CPT+C."
    )
    print()
    print(f"  {'paire':>40} | {'(#col0, #col1)':>16} | exists_witness ?")
    print(f"  {'-'*40} | {'-'*16} | {'-'*15}")

    pairs = make_pairs()
    all_distinguishable = True
    for f, g in pairs:
        sig_f = color_signature(f)
        sig_g = color_signature(g)
        ew_f = exists_witness(f)
        ew_g = exists_witness(g)
        print(f"  {f.name:>40} | {str(sig_f):>16} | {ew_f}")
        print(f"  {g.name:>40} | {str(sig_g):>16} | {ew_g}")
        # Distinguabilite : un seul des deux invariants suffit a separer.
        if sig_f != sig_g or ew_f != ew_g:
            print(f"  {'-> CPT+C separe immediatement.':>40}")
        else:
            print(f"  {'-> non separes par ces invariants.':>40}")
            all_distinguishable = False
        print()

    print("=" * 78)
    print("BILAN")
    if all_distinguishable:
        print(
            "Pour chaque paire (UNSAT, SAT) testee, l'invariant FO `exists x. f(x)`\n"
            "(le simple fait d'avoir un sommet colore 1) suffit a distinguer H_f de\n"
            "H_g. Aucune strategie du Duplicateur ne peut empecher le Spoiler de\n"
            "gagner en 1 tour : il marque dans H_g un sommet colore 1 ; aucun\n"
            "sommet colore 1 n'existe dans H_f, donc le Duplicateur ne peut pas\n"
            "repondre.\n"
            "\n"
            "Plus generalement, le multiset des couleurs ((#col 0, #col 1)) diverge\n"
            "trivialement entre UNSAT (= (2^m, 0)) et SAT (= (2^m - N_bool, N_bool)\n"
            "avec N_bool >= 1). Cet invariant est FO+C-definissable, donc\n"
            "CPT+C-definissable.\n"
            "\n"
            "Le Lemme 3 du Proposeur (Duplicateur gagne) est IMPOSSIBLE pour\n"
            "l'encodage choisi de SAT comme coloration de l'hypercube. C'est une\n"
            "consequence directe du choix d'encodage : la propriete distinguante\n"
            "(SAT vs UNSAT) est encodee en surface (la coloration), donc\n"
            "trivialement definissable au premier ordre.\n"
            "\n"
            "-> Programme structurellement impossible dans cette formulation."
        )


if __name__ == "__main__":
    main()
