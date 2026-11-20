# PR-010 — Lecture exécutable du survey d'Agrawal, « The Isomorphism Conjecture for NP » (IITK, 19 déc. 2009 ; Computability in Context, 2011) : les numéros cités par la candidature n° 7, tranchés sur le texte

Date : 2026-09-10. Instrument : `checks/pr010_lecture_agrawal.py`
(téléchargement du PDF IITK, extraction pypdf — 23 pages, 65 215
caractères —, motifs tolérants). Texte et fenêtres dans le scratchpad
de session (`agrawal_survey.txt`, `pr010_lecture.log`), non versionnés.
Version : PDF IITK daté du 19 décembre 2009 ; la version Computability
in Context (2011) n'a pas été ouverte — numérotation à aligner si un
audit est ordonné.

## Les numéros cités par la candidature — tous présents, verbatim

- **Proposition 3.5** : « *If the Isomorphism Conjecture is true then
  P ≠ NP. Proof. If P = NP then all sets in P are NP-complete. However,
  P has both finite and infinite sets and there cannot exist an
  isomorphism between a finite and an infinite set. Hence the
  Isomorphism Conjecture is false.* » — et la phrase qui suit, décisive
  pour l'instruction : « *This suggests that proving the conjecture is
  hard because the problem of separating P from NP has resisted all
  efforts so far. A natural question, therefore, is: Can one prove the
  conjecture assuming a reasonable hypothesis such as P ≠ NP? We
  address this question later in the paper.* »
- **Encrypted Complete Set Conjecture** (définition) : « *There exists a
  1-1, size-increasing, one-way function f such that SAT and f(SAT) are
  not p-isomorphic to each other.* » — la fonction à sens unique est
  DANS l'énoncé. **Proposition 4.1** : « *If the Encrypted Complete Set
  Conjecture is true then P ≠ NP. Proof. If P = NP then every 1-1,
  size-increasing p-function is also p-invertible. Hence for every such
  function, SAT and f(SAT) are p-isomorphic.* » Puis : « *The Encrypted
  Complete Set conjecture fails if one-way functions do not exist. Can
  it be shown to follow from the existence of strong one-way functions
  […]? This is not clear. (In fact, later we argue the opposite.)* »
- §1 : « *disproving the conjecture using one-way functions, or proving
  it, remained very hard (either implies P ≠ NP)* ».
- **r-Complete Degree Conjecture** : « *r-Complete sets for NP are also
  complete under 1-1, size-increasing, r-reductions that are
  r_range-invertible.* » **Proposition 6.19** : « *The p-Complete Degree
  Conjecture is equivalent to the Isomorphism Conjecture. Proof.
  Follows from the observation that p_range = p […] and from Theorem
  3.2.* » **Theorem 6.20** : « *For r ∈ {1-L, 1-NL, 2-DFA, NC⁰, AC⁰}, the
  r-Complete Degree Conjecture is true.* » Et : « *These results provide
  evidence that r-Complete Degree Conjecture is true for all reasonable
  resource bounds; in fact, there is no known example of a reasonable
  reducibility for which the conjecture is false.* »
- **Theorem 6.3** (Agrawal, 1-L, réductions oublieuses) ; **Theorem
  6.4** : « *1-L-complete sets for NP are all 2-L-isomorphic to each
  other but not 1-L-isomorphic.* […] *the 1-L-Isomorphism Conjecture
  fails and a little more work shows that the 1-L-Encrypted Complete
  Set Conjecture is true! However, the failure of the Isomorphism
  Conjecture here is for a very different reason: it is because
  1-L-reductions are not powerful enough to carry out the isomorphism
  construction* » ; **Theorem 6.15** (Agrawal-Allender, NC⁰) ;
  **Theorem 6.16** (Agrawal-Allender-Rudich) : « *Non-uniform
  AC⁰-complete sets for NP are non-uniform AC⁰-isomorphic to each
  other. Further, these isomorphisms can be computed and inverted by
  depth three non-uniform AC⁰ circuits.* » (preuve : AC⁰-complet ⟹
  NC⁰-complet — le « gap »).
- **Theorem 7.1** (Agrawal-Watanabe) : « *If there exists a 1-1,
  2^{n^ε}-secure one-way function for some ε > 0, then all NP-complete
  sets are also complete under 1-1, and size-increasing,
  P/poly-reductions.* » — introduit par : « *Proving this, of course, is
  hard as it implies P ≠ NP (Proposition 3.5). Can we prove this under
  a reasonable assumption?* »
- **Easy Cylinder Conjecture** : « *All 1-1, size-increasing,
  P/poly-functions have an easy cylinder.* » **Corollary 7.5** : « *If
  there exists a 2^{n^ε}-secure one-way function and the Easy Cylinder
  Conjecture is true, then all sets complete for NP under
  P/poly-reductions are P/poly-isomorphic to each other.* » Objection :
  « *Goldreich [31] argued against the conjecture by defining a
  candidate one-way function of the form f^n where f is a candidate
  one-way function in NC⁰ based on expander graphs. He argued that it is
  not clear whether f^n has an easy cylinder, and conjectured that it
  does not.* »
- **§8 Future Directions** (les trois questions, verbatim) : « *Can one
  prove the r-Complete Degree Conjecture for other reducibilities, for
  example, AC⁰[2] […]?* » ; « *Does Goldreich's function have an easy
  cylinder? Can one prove it does not under a reasonable hypothesis?* » ;
  « *Even if the Easy Cylinder Conjecture is true and strong one-way
  functions exist, the Isomorphism Conjecture is true only for
  P/poly-reductions. Can one define alternative and plausible
  conjecture(s) from which the Isomorphism Conjecture for p-reductions
  follows?* »
- **Oracles** (§4) : Hartmanis-Hemachandra [33] — « *an oracle relative
  to which P = UP and the Isomorphism Conjecture is false. This shows
  that both the conjectures fail in a relativized world* » ; **Theorem
  4.4** (Kurtz-Mahaney-Royer) : « *Relative to a random oracle,
  scrambling functions exist. Therefore, relative to a random oracle,
  the Encrypted Complete Set Conjecture is true and the Isomorphism
  Conjecture is false* » ; **Theorem 4.5** (Fenner-Fortnow-Kurtz) :
  « *There exists an oracle relative to which Isomorphism [Conjecture
  holds]* ».

## Lemme de lecture (i) — « barreau r ⟹ NP ⊄ r » : l'argument est celui de la Prop. 3.5, et le survey l'écrit pour le barreau L

Forme générale : [NON TROUVÉE dans le survey]. Cas L, verbatim (§6) :
« *Weakening p-reductions to logspace-reductions […] does not yield
unconditional results as any such result will separate NP from L,
another long-standing open problem. So we need to weaken it further.* »
L'argument général est la Prop. 3.5 relativisée au barreau : si
NP ⊆ r, un ensemble fini non trivial est r-complet (x ↦ a si x ∈ SAT,
b sinon), et aucune réduction 1-1 croissante d'un ensemble infini ne
l'atteint — vérifié à la main. **Conséquence lue dans le survey
lui-même : l'échelle n'est prouvée que pour des réducibilités dont la
séparation d'avec NP est connue ou triviale (1-L, NC⁰, AC⁰), et elle
s'arrête là où il faudrait une séparation ouverte (L) — ou là où la
séparation est connue mais la structure manque (AC⁰[2]).**

## Lemme (ii) — un barreau au-dessus d'AC⁰ depuis 2011 : [NON TROUVÉ]

Dernier barreau : AC⁰ (Agrawal, JCSS 2011, version uniforme) ; la
question AC⁰[2] est posée au §8 (2009) ; recherche web du 2026-09-10 :
aucun résultat 2012-2026 sur le r-CDC pour AC⁰[2] ou TC⁰ [NON TROUVÉ,
recherche non exhaustive]. **TC⁰ : 0 occurrence dans le survey** — le
« barreau TC⁰ » et sa lecture RR sont une construction de la
candidature (sourcée chez Naor-Reingold et la cellule 7 du dépôt), pas
un énoncé d'Agrawal.

## Lemme (iii) — le cylindre facile de la fonction de Goldreich

Question ouverte du §8, sans réponse dans le survey ; ce n'est pas un
lemme de lecture mais une question de recherche. [OUVERT]

## Corrections et précisions à la candidature

- « Rogers, JCSS 54 (1997) » : **0 occurrence dans le survey** ; la
  pièce existe (J. Rogers, « The isomorphism conjecture holds and
  one-way functions exist relative to an oracle », JCSS 54(3):412-423,
  1997 — « *every paddable 1-li-degree collapses to an isomorphism
  type* », recherche du jour). Le survey donne trois mondes (HH : les
  deux conjectures fausses ; KMR : la rivale vraie ; FFK : IC vraie) ;
  la candidature en ajoute un quatrième (Rogers : IC vraie + OWF).
- « La rivale implique aussi P ≠ NP » : vrai — parce que l'ECSC affirme
  l'existence d'une fonction à sens unique ; la Prop. 4.1 est
  « OWF ⟹ P ≠ NP » habillée. La moitié « rivale » du « fait structurel
  rare » est triviale.
- Le mécanisme conjecturé du sommet (Cor. 7.5) n'atteint que
  l'isomorphisme P/poly, et le survey le dit (§8, troisième question).
