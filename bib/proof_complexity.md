# A-012 : La ligne « complexité des preuves » (programme Cook-Reckhow) — sources et verbatims

> Tâche type A. Exécutée le 2026-07-23. Objectif : créer la ligne 15 de
> l'Atlas — la dernière grande famille d'approches absente de la
> matrice. Pièce centrale : Pich-Santhanam FOCS 2019, **texte intégral
> (20 p.) extrait et greppé** (PDF officiel des proceedings).

## 0. Sources

1. **Pich-Santhanam**, *Why are Proof Complexity Lower Bounds Hard?* —
   FOCS 2019, pp. 1305-1324, **20 p. greppées** (PDF conferences.computer.org).
2. **Pich-Santhanam**, *Towards P≠NP from Extended Frege lower bounds* —
   arXiv:2312.08163 (2023), abstract verbatim.
3. **Krajíček-Pudlák**, *Some consequences of cryptographic conjectures
   for S¹₂ and EF* — Information and Computation 140(1), 1998
   (identifié comme la source de la mort de l'interpolation pour EF ;
   cité via [32] de la source 1 — non lu en intégral).
4. Faits de frontière : sourcés verbatim depuis la source 1 (§I.B, avec
   ses références : Haken [23], Ajtai [3], exponentiel [9], Razborov
   [41][42], Beame-Pitassi [10]).

## 1. Le programme (définition verbatim, source 1)

> « Cook and Reckhow [18] show that NP = coNP iff there is a
> propositional proof system P that is polynomially bounded [...]
> **Cook-Reckhow Program: Separate NP and coNP by proving
> super-polynomial lower bounds on the proof size of tautologies in
> increasingly powerful proof systems P.** » (§I.B)

NP ≠ coNP impliquerait P ≠ NP. C'est le pendant preuve du programme
bornes-de-circuits — avec une différence structurelle profonde,
verbatim :

> « In this setting, counting arguments do not work to get
> non-constructive lower bounds, since the space of small proofs is
> comparable in size to the space of tautologies. » (§I.B)

(Pas d'argument de comptage : en complexité des preuves, même la
non-constructivité gratuite des circuits n'existe pas.)

## 2. La frontière exacte (verbatim, source 1)

> « Haken [23] showed super-polynomial lower bounds [...] Pigeonhole
> Principle in the Resolution proof system. Ajtai [3] obtained a
> significant extension [...] also super-polynomially hard for
> Bounded-Depth Frege [...] strengthened to an exponential lower bound
> by [9]. » (§I.B)
> « There has been significant effort devoted to proving lower bounds
> for constant-depth Frege proofs with modular counting gates — the
> proof-theoretic analogue of constant-depth circuits with modular
> counting gates — but without any success. Thus the Cook-Reckhow
> program is also stalled. » (§I.B)

**Le verrou frontière est donc AC⁰[p]-Frege** : l'analogue circuits
(Razborov-Smolensky) est prouvé depuis 1987 (notre audit A-004), et la
version preuve est ouverte — le miroir exact de la ligne 4 de la
matrice, un étage plus haut. En amont, inconditionnel côté uniforme :

> « it is known unconditionally that Cook's theory PV1 cannot prove
> super-polynomial lower bounds on EF » (§I.E, refs [13][19][32])

## 3. L'analogue des preuves naturelles : un trou de 20 ans, comblé en 2019

Le trou, verbatim :

> « unlike the Circuit Lower Bounds program, we do not have a good
> explanation for why progress is stalled. There is no known analogue
> of the natural proofs barrier for proof complexity, and indeed this
> is one of the main open questions asked in the survey of Beame and
> Pitassi [10] from the late 90s. » (§I.B)

Le précédent partiel (Razborov, via interpolation) :

> « Razborov shows that under certain complexity assumptions, no proof
> system P with feasible interpolation can prove any super-polynomial
> circuit complexity lower bound. [...] The 'feasible interpolation'
> condition is a fairly restrictive one, and there is evidence that
> Frege and EF do not have feasible interpolation [12], [32]. » (§I.F)

([32] = Krajíček-Pudlák 1998 : sous conjectures cryptographiques (RSA),
EF n'a pas d'interpolation faisable — la méthode monotone du transfert
meurt aux systèmes forts.)

Le comblement (Pich-Santhanam 2019), abstract et Théorème 1 verbatim :

> « We establish the following unconditional result: Propositional
> proof systems cannot efficiently show that truth tables of random
> Boolean functions lack polynomial size non-uniform proofs of
> hardness. » (abstract)
> « **Theorem 1. Rudich's Conjecture does not admit feasible
> propositional proofs.** » (§I.C)
> « First, it is unconditional. Second, it rules out polynomial-size
> S-proofs in every propositional proof system S, even though S is
> allowed to depend on R. » (§I.C)
> « our proof of Theorem 1 [...] is non-constructive: we show
> unconditionally that a certain propositional proof system R with
> polynomial advice exists for which it is hard to show lower bounds,
> but we are unable to say what R is. » (§I.D)

Et la dichotomie EF, verbatim (abstract) :

> « For the specific case of the Extended Frege (EF) propositional
> proof system, we show that at least one of the following cases
> holds: (1) EF has no efficient proofs of superpolynomial circuit
> lower bound tautologies for any Boolean function or (2) There is an
> explicit family of tautologies [...] such that under reasonable
> hardness assumptions, most tautologies are hard but no propositional
> proof system can efficiently establish hardness [...]. Thus, under
> reasonable hardness assumptions, either the Circuit Lower Bounds
> program toward complexity separations cannot be implemented in EF,
> or there are inherent obstacles to implementing the Cook-Reckhow
> program for EF. »

La barrière est donc **auto-référentielle par essence** : les énoncés
de bornes inférieures de preuves sont eux-mêmes les tautologies dures.

## 4. La voie moderne : EF → P ≠ NP sous conditions (source 2, 2023)

Abstract verbatim (extraits) :

> « We prove that if conditions I-II (below) hold and there is a
> sequence of Boolean functions f_n hard to approximate by p-size
> circuits such that p-size circuit lower bounds for f_n do not have
> p-size proofs in Extended Frege system EF, then P ≠ NP. »
> (I : S¹₂ prouve qu'une fonction concrète de E est dure à approximer ;
> II : S¹₂ prouve une réduction casseur-de-OWF → apprentissage.)
> « Further, we show that any of the following assumptions implies
> that P ≠ NP, if EF is not p-bounded: 1. [Feasible anticheckers] [...]
> 2. [Witnessing NP ⊄ P/poly] [...] 3. [OWF from NP ⊄ P/poly &
> hardness of E]. »

Le programme se referme ainsi sur la méta-complexité (ligne 13 de la
matrice : OWF, apprentissage, anticheckers) — les deux programmes
convergent vers les mêmes hypothèses S¹₂.

## 5. Rapport aux barrières classiques (pour la ligne 15)

- **Relativisation** : sans objet structurel direct (un système de
  preuve propositionnel n'est pas une machine à oracle) ; le programme
  est historiquement NÉ comme repli finitiste post-BGS, verbatim :
  « After this barrier result, attention shifted to a more finitistic
  setting. » (§I.A)
- **Preuves naturelles** : pas de transfert mécanique de RR (le
  comptage même échoue, §1) ; l'analogue PROPRE est établi par P-S
  2019 (inconditionnel, non-constructif) — la seule famille de la
  matrice dont la barrière-analogue est un théorème sans hypothèse.
- **Algébrisation** : [NON TROUVÉ DANS LES SOURCES] — aucune
  discussion AW dans les textes audités.
- **Monotone/interpolation** : l'interpolation faisable est LA méthode
  de transfert monotone (succès : Résolution, Cutting Planes) ; morte
  pour Frege/EF sous crypto (Krajíček-Pudlák 1998).
