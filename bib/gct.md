# A-011 : Audit GCT sur textes complets — le flip, les barrières selon Mulmuley, BIP 2019 en intégral, et l'état 2019→2026 des multiplicités

> Tâche type A. Exécutée le 2026-07-20. Objectif : faire passer la ligne 8
> de l'Atlas (GCT) de « présumé » à « documenté ». Règle no-invention :
> toute citation est verbatim des textes listés (ligatures PDF recollées).

## 0. Sources (textes obtenus et greppés)

1. **Mulmuley**, *On P vs. NP, Geometric Complexity Theory, and the Flip I:
   a high level view* — arXiv:0709.0748, **103 p. extraites et greppées**
   (la Section 18 « On relativization and P/poly-naturalization barriers »
   est la pièce centrale).
2. **Mulmuley**, *Explicit Proofs and The Flip* — arXiv:1009.0246
   (version du 31 oct. 2018), **32 p. extraites et greppées**.
3. **Bürgisser-Ikenmeyer-Panova**, *No occurrence obstructions in
   geometric complexity theory* — arXiv:1604.06431v3 (J. AMS 32(1),
   2019), **27 p. extraites et greppées** (D-002 n'avait lu que
   l'abstract).
4. **Dörfler-Ikenmeyer-Panova** — arXiv:1901.04576 (SIAM J. Appl.
   Algebra Geometry 4(2), 2020) — abstract verbatim.
5. **Ikenmeyer-Kandasamy** — arXiv:1911.03990 (STOC 2020) — abstract
   verbatim.
6. **Panova**, *Computational Complexity in Algebraic Combinatorics* —
   arXiv:2306.17511 (Current Developments in Mathematics 2023) +
   page recherche USC (état 2023-2025) — niveau abstract.

## 1. Le programme et le flip (définitions verbatim)

Le flip est LA stratégie définissante de GCT, et vise le paradoxe
auto-référentiel :

> « This article describes a formal strategy of geometric complexity
> theory (GCT) to resolve the self referential paradox in the P vs. NP
> and related problems. The strategy, called the flip, is to go for
> explicit proofs of these problems. By an explicit proof we mean a
> proof that constructs proof certificates of hardness that are easy to
> verify, construct and decode. » (1009.0246, abstract)

> « This paradox refers to the question that is often asked: namely,
> since the P vs. NP problem is a universal statement about mathematics
> that says that discovery is hard, why could it not preclude its own
> proof [...] ? » (1009.0246, §1)

Les obstructions sont des certificats de dureté courts, vérifiables et
constructibles en temps poly — le « hard » (borne inf) est réduit à des
« easy » (bornes sup : vérification, construction, décodage ∈ P).

## 2. GCT × relativisation — DOCUMENTÉ : revendiqué au conditionnel

Section 18 de 0709.0748, verbatim :

> « We already mentioned one reason for why the flip should be
> nonrelativizable: namely, the "reduction" from hard nonexistence to
> easy existence is not a formal Turing machine reduction. » (§18)
> « It is not a formal Turing machine reduction. If it were, it would
> be relativizable. » (§1)
> « the flip is to be implemented using explicit algebro-geometric and
> representation-theoretic constructions. This is why it should be
> nonrelativizable. » (§18)

Statut : **« should », deux fois** — un argument structurel de l'auteur
(pas de réduction Turing, constructions explicites), jamais un théorème
du type oracle (contrairement à Williams, A-001). Cohérent avec D-002
(pas d'objet oracle pour VP vs VNP) — mais désormais sourcé.

## 3. GCT × preuves naturelles — DOCUMENTÉ : violation revendiquée des DEUX conditions, avec aveux de non-preuve

C'est la découverte principale de l'audit. Mulmuley ne dit pas « GCT
échappe à RR » en passant : il y consacre §18.2-18.3, en visant la
violation des deux conditions à la fois :

> « we next formulate a property which is conjecturally useful and
> which should violate both the largeness and the constructivity
> constraints. This should be enough to cross the
> P/poly-naturalizability barrier. » (§18)

**Largeness (§18.2)** — prouvée sur corps finis, PAS sur ℂ :

> « We cannot prove this formally over C. But this can be proved
> formally over a finite field F_p or an algebraically closed field
> F̄_p of positive characteristic [GCT10]. In fact, it turns out that
> violation of the largeness constraint is far more severe than what is
> formally required. Namely, [...] |C_n|/|F_n| ≥ 1/2^{Ω(N)} » (§18.2)
> « The proof of violation of the largeness constraint over F̄_p does
> not carry over to C for technical reasons. Specifically, the key
> ingredient in this proof is the Riemann hypothesis over finite
> fields, or rather its extension as proved in [Deligne]. » (§18.2)

**Constructivité (§18.3)** — circularité avouée :

> « We cannot hope to show this formally, since this is a lower bound
> statement in itself. But rather we can give good evidence. » (§18.3)

(L'évidence : calculer le stabilisateur = résoudre un système
polynomial, NP-complet.) La violation de constructivité est donc
elle-même un énoncé de borne inf — la barrière se referme sur qui veut
prouver qu'il l'a franchie.

**L'auto-évaluation tardive (2018)** — la version finale du flip paper
va plus loin : la vraie contrainte n'est pas RR mais l'explicitation :

> « This form of rigidity is extremely severe in comparison to the mild
> rigidity constraint that the natural proof barrier [33] places on
> proof techniques [...] just mild rigidity which suffices to bypass
> the natural proof barrier may not be enough, and a proof may be
> forced to be extremely rigid » (1009.0246, avec la note de bas de
> page : « Ignoring the constructivity condition in [33] »)

Verdict cellule : ⚠ **franchissement argumenté par l'auteur, démontré
nulle part sur ℂ** — largeness : théorème sur F_p seulement ;
constructivité : espérée, avec circularité explicite.

## 4. La barrière interne — BIP 2019 sur texte intégral

**La cible exacte.** Ω_n = fermeture d'orbite GL_{n²}·det_n ;
Z_{n,m} = GL_{n²}·(X₁₁^{n−m}·perm_m) (permanent paddé). Définition
verbatim :

> « Schur's lemma implies that if λ occurs in C[Z_{n,m}], then it must
> also occur in C[Ω_n]. A partition λ violating this condition is
> called an occurrence obstruction. Its existence thus proves that
> Z_{n,m} ⊄ Ω_n and hence dc(per_m) > n. » (§1)

**La conjecture tuée et le théorème, verbatim :**

> « 1.3. Conjecture (Mulmuley and Sohoni 2001). For all c ∈ N≥1, for
> infinitely many m, there exists a partition λ occurring in
> C[Z_{m^c,m}] but not in C[Ω_{m^c}]. »
> « Unfortunately, this conjecture is false! This is the main result
> of this work. »
> « 1.4. Theorem. Let n, d, m be positive integers with n ≥ m^25 and
> λ ⊢ nd. If λ occurs in C[Z_{n,m}], then λ also occurs in C[Ω_n]. In
> particular, Conjecture 1.3 is false. »

**Le mécanisme (l'endroit exact de la mort)** — le padding, et rien
d'autre :

> « The only information we exploit about the orbit closure Z_{n,m} of
> the padded permanent is an insight due to Kadish and Landsberg [...]
> So no specific property of the permanent is used: only the padding
> (multiplication with a power of a linear form) is relevant. » (§2(a))

Le permanent paddé contient trop de sommes de puissances : toute λ qui
apparaît côté paddé apparaît déjà côté déterminant. Aggravation
(remerciements, note de Wigderson) :

> « our proof reveals that, using occurrence obstructions, one cannot
> prove significant lower bounds in the significantly weaker model of
> power sums. » (§1, acknowledgments ; développé en §2(d) : même pour
> le rang de Waring — où des bornes exponentielles sont PROUVABLES par
> d'autres moyens — les occurrences ne donnent rien.)

Complément (§1(b)) : Kumar, sous la conjecture d'Alon-Tarsi, montre
K_n(nλ) > 0 (positivité asymptotique des GCT-coefficients) — les zéros
requis n'existent tout simplement pas dans le régime paddé.

**La porte laissée ouverte, verbatim :**

> « While our main result, Theorem 1.4, rules out the possibility of
> proving the Conjecture 1.2 via occurrence obstructions, there still
> remains the possibility that one may succeed so by comparing
> multiplicities. » (§1(c))

## 5. L'état de la porte multiplicités, 2019 → 2026

- **DIP 2020** (abstract verbatim) : « This paper provides for the
  first time a setting where separating with multiplicities can be
  achieved, while the separation with occurrences is provably
  impossible. Our setting is surprisingly simple and natural: We study
  the variety of products of homogeneous linear forms (the so-called
  Chow variety) and the variety of polynomials of bounded border
  Waring rank. » — **cadre jouet** (Chow vs Waring), pas det vs perm.
- **Ikenmeyer-Kandasamy STOC 2020** (abstract verbatim) : « Our paper
  is the first implementation of the ambitious approach that was
  originally suggested in the first papers on geometric complexity
  theory » — séparation de la somme de puissances vs produit de
  variables par multiplicités issues des DEUX groupes de symétrie.
  Encore un cadre modèle, pas det vs perm.
- **Panova 2023-2025** (abstract/survey) : « the study of Kronecker and
  plethysm coefficients leads to the disproof of the wishful approach
  of Geometric Complexity Theory » ; « to make GCT work and establish
  computational complexity lower bounds, we need to understand
  representation theoretic multiplicities in further detail, possibly
  asymptotically. » Résultats durs associés : pas de formule
  combinatoire positive connue pour Kronecker (problème ouvert depuis
  ~85 ans) ; la positivité des caractères de S_n est aussi dure que PH
  (SODA 2023) — **les quantités que la voie multiplicités doit
  contrôler sont elles-mêmes computationnellement intraitables**, un
  écho direct du flip : il faudrait les rendre explicites pour
  franchir RR, et elles résistent.

Aucun résultat 2019-2026 trouvé qui réalise des multiplicity
obstructions pour det vs perm — le front est resté aux cadres modèles.

## 6. Verdict pour la ligne 8 de l'Atlas

| Cellule | Avant (D-002) | Après audit |
|---|---|---|
| GCT × relativisation | ◌ présumé | ◌ **documenté** : revendiqué 2× au conditionnel (« should be nonrelativizable », §18) — argument structurel, pas de théorème |
| GCT × RR | ⚠ présumé franchi | ⚠ **documenté** : violation revendiquée des DEUX conditions (§18.2-18.3) ; largeness prouvée sur F_p SEULEMENT (« cannot prove this formally over C ») ; constructivité circulaire (« a lower bound statement in itself ») |
| GCT × algébrisation | ◌ présumé | ◌ inchangé (aucune discussion AW dans les textes de Mulmuley audités — [NON TROUVÉ DANS LES PAPERS] ; l'argument structurel D-002 reste le seul) |
| Barrière interne | BIP abstract | **BIP texte intégral** : Théorème 1.4 (n ≥ m^25), mécanisme = le padding seul, extension Waring (Wigderson), Kumar/Alon-Tarsi ; multiplicités : réalisées UNIQUEMENT en cadres jouets (DIP, IK) ; les coefficients requis sont eux-mêmes durs (Panova) |

**Leçon consolidée** : GCT est l'approche dont l'évasion des barrières
classiques est la plus argumentée par son auteur ET la moins démontrée
formellement — et son programme concret est mort une première fois
(occurrences, BIP) d'un détail de plomberie (le padding), pas de
représentation-théorie profonde. La voie survivante (multiplicités)
exige de rendre explicites des quantités (Kronecker, plethysmes) dont
l'intraitabilité est elle-même en voie de formalisation. Le paradoxe
auto-référentiel que le flip voulait résoudre se reproduit un étage
plus bas.
