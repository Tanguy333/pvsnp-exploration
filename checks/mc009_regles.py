# -*- coding: utf-8 -*-
"""MC-009 — Les trois constructions générales (majorants de C-MC009),
en règles bloc-symétriques : signature (|S∩A|, |S∩B|, |S∩O|) → coefficient
(chaque monôme de la signature reçoit ce coefficient).

Preuves de séparation dans la fiche MC-009 §4. Vérifiées par
`mc009_preuve_F.py constructions` (évaluation par comptages de blocs).
"""


def REGLES_COMPARABLE(b, o):
    """Cœur comparable {0-point, B} : p = Σ_{i∈B∪O} y_i + o·m_B.
    Poids b + 2o. Uns : 0 et b+o ; zéros : jamais 0 ni b+o."""
    regles = {(0, 1, 0): 1}
    if o:
        regles[(0, 0, 1)] = 1
        regles[(0, b, 0)] = o
    return regles


def REGLES_INCOMPARABLE(a, b, o):
    """Cœur incomparable {A, B}, 1 ≤ a ≤ b.
    (1,1) (ajout VER-MC-1, construction du vérificateur V2) :
        p = y₁ + y₂ + Σ_l (m_{1l} + m_{2l}) — poids 2 + 2o ;
        uns {1}, zéros {0} ∪ [2, ∞).
    a = 1, b ≥ 2 (branche linéaire) : p = y_A + m_B + Σ_j m_{A∪{j}}
        + Σ_l (m_{A∪{l}} + m_{B∪{l}}) — poids 2 + b + 2o.
    a ≥ 2 (branche couronne) : p = m_A + m_B + Σ_j m_{A∪{j}}
        + Σ_i m_{B∪{i}} + Σ_l (m_{A∪{l}} + m_{B∪{l}}) — poids a + b + 2 + 2o.
    Uns : tous à 1 ; zéros : 0 ou ≥ 2."""
    if a == b == 1:
        regles = {(1, 0, 0): 1, (0, 1, 0): 1}
        if o:
            regles[(1, 0, 1)] = 1
            regles[(0, 1, 1)] = 1
        return regles
    if a == 1:
        regles = {(1, 0, 0): 1, (0, b, 0): 1, (1, 1, 0): 1}
        if o:
            regles[(1, 0, 1)] = 1
            regles[(0, b, 1)] = 1
        return regles
    regles = {(a, 0, 0): 1, (0, b, 0): 1, (a, 1, 0): 1, (1, b, 0): 1}
    if o:
        regles[(a, 0, 1)] = 1
        regles[(0, b, 1)] = 1
    return regles
