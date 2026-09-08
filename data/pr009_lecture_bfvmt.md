# PR-009 — Lecture exécutable de BFvMT (arXiv math/9807185) : les deux lemmes de lecture de la candidature n° 6, tranchés sur le texte

Date : 2026-09-08. Instrument : `checks/pr009_lecture_bfvmt.py`
(téléchargement du PDF arXiv, extraction pypdf, motifs tolérants aux
espaces intra-mots et aux « / » devant les chiffres — typographie Type 1
de 1998 : « T uring », « Theorem /4/./1 »). Texte : 77 779 caractères,
25 pages ; extraction et fenêtres dans le scratchpad de session
(`bfvmt_arxiv.txt`, `pr009_lecture.log`) — non versionnées (l'audit
fondateur, s'il est ordonné, versionnera sous `bib/pdf/`).

Version : arXiv **v1 seule** (1er juillet 1998) ; référence journal
SICOMP 29(5), 2000, non ouverte. Le texte arXiv est la version
CORRIGÉE ; la version erronée est la version de conférence [6]
(FOCS 1995). Auteurs : Buhrman, Fortnow, van Melkebeek, Torenvliet.

## Lemme de lecture (i) — la Figure 7 contient-elle une case P ≠ NP ? NON

Verbatim (p. 21-22) : « *Theorem 5.1 In Figure 7, a positive answer to
a question from the first column, implies the separation in the second
column, and a negative answer, the separation in the third column.* »

| Question (colonne 1) | oui (colonne 2) | non (colonne 3) |
|---|---|---|
| Are all ≤ᵖ_T-complete sets for EXPSPACE autoreducible? | NL ≠ NP | PH ≠ PSPACE |
| Are all ≤ᵖ_T-complete sets for EEXP autoreducible? | NL ≠ NP, P ≠ PSPACE | PH ≠ EXP |
| Are all ≤ᵖ_tt-complete sets for PSPACE ≤ᵖ_tt-autoreducible? | NL ≠ NP | PH ≠ PSPACE |
| Are all ≤ᵖ_tt-complete sets for EXP ≤ᵖ_tt-autoreducible? | NL ≠ NP, P ≠ PSPACE | PH ≠ EXP |
| Are all ≤ᵖ_tt-complete sets for EXPSPACE probabilistically ≤ᵖ_tt-autoreducible? | NL ≠ NP | P ≠ PSPACE |

Preuve du Théorème 5.1 (verbatim) : « *The NL ≠ NP implications in the
"yes"-column of Figure 7 immediately follow from Theorems 5.3 and 5.4
by contraposition. By Theorem 3.1, a positive answer to the 2nd question
in Figure 7 would yield EEXP ≠ EEXPSPACE, and by Theorem 3.3, a positive
answer to the 4th question would imply EXP ≠ EXPSPACE. By padding, both
translate down to P ≠ PSPACE. Similarly, by Theorem 4.3, a negative
answer to the 2nd question would imply EXPH ≠ EEXP, which pads down to
PH ≠ EXP. A negative answer to the 4th question would yield PH ≠ EXP
directly by Theorem 4.4. By the same token, a negative answer to the 1st
question results in EXPH ≠ EXPSPACE and PH ≠ PSPACE, and a negative
answer to the 3rd question in PH ≠ PSPACE. By Theorem 4.6, a negative
answer to the last question implies EXP ≠ EXPSPACE and P ≠ PSPACE.* »

**Correction à la candidature** : à la ligne 5, « P ≠ PSPACE » est dans
la colonne NON (Théorème 4.6), pas dans la colonne oui — la candidature
écrivait « P ≠ PSPACE aux lignes 2, 4, 5 » côté oui. Sans conséquence
sur la thèse : **aucune case ne contient P ≠ NP**. La seule occurrence
de « P = NP » dans tout le texte est dans la preuve du Lemme 5.2, comme
CONSÉQUENCE de NP = NL.

Renforcement (verbatim, p. 23) : « *we can replace "NL ≠ NP" in Figure 7
by "coNP ⊄ NP ∩ NSPACE[log^{O(1)} n]." This is because that condition
suffices for Theorems 5.3 and 5.4, since we can strengthen Lemma 5.2 as
follows: Lemma 5.5 If coNP ⊆ NP ∩ NSPACE[log^{O(1)} n], we can decide the
validity of QBF-formulae of size t and with [α] alternations on a
deterministic Turing machine M1 in time t^{O(c)} and on a
nondeterministic Turing machine M2 in space O(d log^d t), for some
constants c and d.* »

## Le levier d'effondrement — pourquoi P = NP n'entre pas dans le tableau

Lemme 5.2 (verbatim) : « *If NP = NL, we can decide the validity of
QBF-formulae of size t and with [α] alternations on a deterministic
Turing machine M1 in time t^{O(c)} and on a nondeterministic Turing
machine M2 in space O(c log t), for some constant c.* » Preuve : « *Since
coNP = NP, by Cook's Theorem we can transform in polynomial time a
Σ₁-formula with free variables into an equivalent Π₁-formula […] Since
NP = P, we can decide the validity of Σ₁-formulae in polynomial-time.
[…] Moreover, since P = NL, a padding argument shows that DTIME[…] ⊆
NSPACE[log …] for any time constructible function. Therefore the result
holds.* » Théorème 5.3 : « *If NP = NL, there is a ≤ᵖ_{2-T}-complete set
for EXPSPACE that is not probabilistically autoreducible. The same holds
for EEXP instead of EXPSPACE. Proof: Combine Lemma 5.2 with the
probabilistic extension of Lemma 3.4 used in the proof of Theorem 3.2.* »

Lecture (argumentée — l'attribution machine par machine est une
inférence, à confirmer sur la preuve du Lemme 3.4 à l'audit) : la
partie TEMPS du levier (M1) n'utilise que coNP = NP et NP = P — deux
conséquences de P = NP aussi ; c'est la partie ESPACE (M2, via P = NL et
le padding DTIME ⊆ NSPACE[log]) qui fait descendre la diagonalisation de
Lemme 3.4 dans EXPSPACE/EEXP. L'hypothèse minimale du Lemme 5.5 le
confirme : « coNP ⊆ NP ∩ NSPACE[log^{O(1)} n] » — une économie
d'ESPACE que P = NP ne fournit pas. **L'absence de P ≠ NP dans la
Figure 7 n'est pas un accident du tableau : le mécanisme de transfert
exige un effondrement qui économise de l'espace, et P = NP n'en est
pas un.** Toutes les conclusions du tableau opposent des ressources de
natures différentes (temps/espace, hiérarchie/exponentielle) ; P vs NP
oppose deux classes de même ressource.

## Lemme de lecture (ii) — les théorèmes positifs ne valent-ils que pour k constant ? OUI, avec une nuance

- Introduction (verbatim) : « *All Turing-complete sets for Δ^{EXP}_k are
  autoreducible for any constant k* ».
- Note sur la version antérieure (p. 3-4, verbatim) : « *A previous
  version of this paper [6] erroneously claimed proofs showing all
  Turing complete sets for EXPSPACE are autoreducible and all
  truth-table complete sets for PSPACE are nonadaptively autoreducible.
  Combined with the additional results in this version, we would have a
  separation of NL and NP (see Section 5). However the proofs in the
  earlier version failed to account for the growth of the running time
  when recursively computing previous players' moves. We use the proof
  technique in Section 3 though unfortunately we get considerably
  weaker theorems. The original results claimed in the previous version
  remain important open questions as resolving them either way will
  yield new separation results.* » — [6] = la version de conférence
  (FOCS 1995) ; le texte arXiv EST la version corrigée (la candidature
  inversait les rôles des versions, sans conséquence sur le lemme).
- p. 13 (verbatim) : « *The number of rounds k being constant, seems
  crucial for keeping the complexity under control. The conference
  version of this paper [6] erroneously claimed the proof works for
  EXPSPACE, which can be thought of as alternating exponential time
  with an exponential number of alternations. Establishing Theorem 4.3
  for EXPSPACE would actually separate NL from NP, as we will see in
  Section 5.* »
- Théorème 4.4 (verbatim) : « *For any integer k > 0, every
  ≤ᵖ_tt-complete set for Δ^P_{k+1} is nonadaptively autoreducible.
  Parallel to the adaptive case, an earlier version of this paper [6]
  stated Theorem 4.4 for unbounded k, i.e., for PSPACE. However, we
  only get the proof to work for constant k.* »
- **Nuance manquée par la candidature** (Conclusion, verbatim) :
  « *Theorem 4.3 goes through for k(n) ∈ O(log n). Perhaps one can
  exploit this leeway in the coding of Lemma 3.4 and narrow the gap
  between the positive and negative results.* » — le plafond du moteur
  positif est à O(log n) alternances, pas à une constante ; la bande
  va de O(log n) à exponentiellement beaucoup (EXPSPACE).

## Les autres pièces verbatim

- Post's Program (p. 2) : « *In what we now call "Post's Program" (see
  [11, 15]), Post tried to show these classes differ by finding a
  property that holds for all sets in the first class but not for some
  set in the second. We would like to resurrect Post's Program for
  separating classes in complexity theory. […] While we do not separate
  any classes not already separable by known diagonalization
  techniques, we feel that refinements to our techniques may yield some
  new separation results.* » Conclusion : « *Finally, one may want to
  look at other properties than autoreducibility to realize Post's
  Program in complexity theory.* »
- Accès à l'oracle (p. 2) : « *Issues of relativization do not apply to
  this work because of oracle access (see [8]): A polynomial-time
  autoreduction can not view as much of the oracle as an exponential or
  doubly exponential computation. To illustrate this point we show that
  there exists an oracle relative to which some complete set for
  exponential time is not autoreducible.* » — [8] = Fortnow, « The role
  of relativization in complexity theory », Bull. EATCS 52:229-244,
  1994.
- p. 12 : « *The local checkability property of computations used in
  the proof of Theorem 4.1 does not relativize, because the oracle
  computation steps depend on the entire query, i.e., on a number of
  bits that is only limited by the resource bounds of the base machine,
  in this case exponentially many. We next show that Theorem 4.1 itself
  also does not relativize. Theorem 4.2 Relative to some oracle, EXP
  has a ≤ᵖ_{2-T}-complete set that is not autoreducible.* » Et :
  « *Theorem 4.2 applies to any complexity class containing EXP that
  has Property 4.1, e.g., EXPSPACE, EEXP, EEXPSPACE, etc.* »
- Théorème 3.1 : « *There is a ≤ᵖ_{2-T}-complete set for EEXPSPACE that
  is not autoreducible. Most natural classes containing EEXPSPACE,
  e.g., EEEXPTIME and EEEXPSPACE, also have this property.* » ;
  Théorème 3.3 : « *There is a ≤ᵖ_{3-tt}-complete set for EXPSPACE that
  is not nonadaptively autoreducible.* »
- Théorème 4.1 : « *Every ≤ᵖ_T-complete set for EXP is autoreducible.* » ;
  Théorème 4.3 : « *For any integer k > 0, every ≤ᵖ_T-complete set for
  Δ^{EXP}_{k+1} is autoreducible.* » ; Théorème 4.9 : « *All
  ≤ᵖ_tt-complete sets for NP are probabilistically nonadaptively
  autoreducible.* » (Valiant-Vazirani).
- Limites déclarées (introduction) : « *For the restricted reducibility
  where we are only allowed to ask two nonadaptive queries, all
  complete sets for EXP, EXPSPACE, EEXP, EEXPSPACE, etc., are
  autoreducible. We also argue that uniformity is crucial* » ; et, sur
  le versant probabiliste : « *Low end complexity classes turn out to
  have the property that their complete sets are autoreducible, whereas
  high end complexity classes do not.* »

## État de la littérature 2016-2026 (recherche web, non exhaustive)

- Trouvé : Zhang, Quweider, Lei, Khan, « Weak mitoticity of bounded
  disjunctive and conjunctive truth-table autoreducible sets »,
  Theoretical Computer Science 822 (2020) — un ensemble creux de EXP
  2-tt-autoréductible mais pas faiblement T-mitotique ; les ensembles
  bdtt/bctt-autoréductibles sont faiblement mitotiques pour tt à
  log requêtes. La « dormance 2020-2026 » de la candidature est donc à
  nuancer (2020) ; aucune pièce trouvée ne remplit une case de la
  Figure 7 [NON TROUVÉ — recherche non exhaustive].
