# AUDIT A-023 — Le transfert « algorithme ⟹ borne inférieure » instancié pour THR∘THR, et la frontière 2014-2026

Tâche : A-023 (audit fondateur du fil ALG — le manque n° 1 de la
candidature PR-005). Date : 2026-08-11. Type A (audit sur textes).
Tous les verbatims proviennent de PDF **ouverts, téléchargés et
extraits localement** — extractions texte versionnées dans
`bib/pdf/thrthr/` (16 fichiers `.txt` ; les PDF restent locaux,
non versionnés par `.gitignore`) —, sauf deux entrées marquées
**[TEXTE NON OUVERT]** (KL01, CLW20).

> **Ce que l'audit tranche** (résumé, détail aux sections) :
> 1. L'énoncé visé par PR-005 (« CAPP ou SAT non trivial pour
>    THR∘THR poly-taille ⟹ NEXP ⊄ THR∘THR ») est **VRAI et
>    numéroté** — mais ce n'est un théorème **ni** de Williams
>    2010/2011 **ni** de Murray-Williams 2018 (leurs clôtures ne
>    tiennent pas pour THR∘THR) : c'est **Chen-Williams CCC 2019,
>    Theorem 8**. L'attribution de la candidature est à corriger.
> 2. L'obstacle de clôture (OR de THR∘THR ∉ THR∘THR), nommé par
>    Williams lui-même en 2014 (note 6), a été **contourné en 2019**
>    par le PCPP à 2 requêtes + la ⊕₂-clôture folklore (XOR de deux
>    THR∘THR = THR∘THR poly-plus-grand, CW19 Lemma 50).
> 3. La frontière algorithmique est **partielle, bornée en portes** :
>    #SAT jusqu'à n^{2−δ} portes (ACW16), CAPP (⊕₂∘THR∘THR)
>    jusqu'à n^{2.5−ε} portes (CTW26, mars 2026, déterministe) —
>    d'où E^NP ⊄ THR∘THR[n^{2.5−ε}]. **La taille polynomiale
>    générale reste OUVERTE.**
> 4. Le transfert **ne consomme aucun paramètre de poids** — son
>    unique hypothèse est le temps du CAPP. Et côté bornes, toute
>    victoire à poids restreints est **subsumée depuis les années
>    1990** (Nisan ; Forster et al.).

## (i) Identifications et révisions (vérifiées à l'ouverture ET à la clôture, 2026-08-11)

| Sigle | Référence | Source ouverte utilisée | Révisions |
|---|---|---|---|
| **W10** | R. Williams, « Improving Exhaustive Search Implies Superpolynomial Lower Bounds », STOC 2010 (SICOMP 42(3) 2013) | `people.csail.mit.edu/rrw/improved-algs-lbs2.pdf` — version auteur datée « May 4, 2010 » (28 p.) | version site auteur, pas de versionnage |
| **JACM14** | R. Williams, « Nonuniform ACC Circuit Lower Bounds », JACM 61(1), 2014 | `people.csail.mit.edu/rrw/acc-lbs-journal-final.pdf` (31 p., version finale auteur ; en-têtes JACM en gabarit) | id. |
| **W14thr** | R. Williams, « New algorithms and lower bounds for circuits with linear threshold gates », STOC 2014 ; journal : Theory of Computing 14(1):1-25, 2018 | arXiv:1401.2444 (PDF v1) | **v1 seule** (10 janv. 2014) — reconfirmé à la clôture |
| **BV14** | E. Ben-Sasson, E. Viola, « Short PCPs with projection queries », ICALP 2014 ; ECCC TR14-017 | `ccs.neu.edu/home/viola/papers/AC0PCP.pdf` (24 p.) | version auteur |
| **KW16** | D. Kane, R. Williams, « Super-Linear Gate and Super-Quadratic Wire Lower Bounds for Depth-Two and Depth-Three Threshold Circuits », STOC 2016 | arXiv:1511.07860 (v1) | **v1 seule** (24 nov. 2015) — reconfirmé |
| **Tam16** | S. Tamaki, « A Satisfiability Algorithm for Depth Two Circuits with a Sub-Quadratic Number of Symmetric and Threshold Gates », **ECCC TR16-100** (2016) | `eccc.weizmann.ac.il/report/2016/100/download` (16 p.) | rapport 2016 ; réédité en volume Springer (chap. 978-981-96-0668-9_20) |
| **ACW16** | J. Alman, T. Chan, R. Williams, « Polynomial Representations of Threshold Functions and Algorithmic Applications », FOCS 2016 | arXiv:1608.04355 (v1, 30 p.) | **v1 seule** (15 août 2016) — reconfirmé |
| **CSS16** | R. Chen, R. Santhanam, S. Srinivasan, « Average-Case Lower Bounds and Satisfiability Algorithms for Small Threshold Circuits », CCC 2016 ; ToC 14(9) 2018 | ECCC TR15-191 download (29 p.) | TR déposé 27 nov. 2015 |
| **MW18** | C. Murray, R. Williams, « Circuit Lower Bounds for Nondeterministic Quasi-Polytime: An Easy Witness Lemma for NP and NQP », STOC 2018 | `people.csail.mit.edu/rrw/easy-witness-nqp.pdf` (21 p.) ; page ECCC TR17-188 consultée | TR17-188 : soumis 22 déc. 2017, publié 23 déc. 2017 ; aucune révision listée par la page (ouverture et clôture) |
| **Chen18** | Lijie Chen, « Toward Super-Polynomial Size Lower Bounds for Depth-Two Threshold Circuits », arXiv:1805.10698 | page abs (abstract verbatim) | **v1 seule** (27 mai 2018) |
| **Wil18/wccc18** | R. Williams, « Limits on Representing Boolean Functions by Linear Combinations of Simple Functions… », CCC 2018 | arXiv:1802.09121 (PDF, 23 p.) | non re-versionné à la clôture (pièce de contexte) |
| **CW19** | Lijie Chen, R. Williams, « Stronger Connections Between Circuit Analysis and Circuit Lower Bounds, via PCPs of Proximity », CCC 2019, LIPIcs 137, 19:1-19:43 | DROPS PDF officiel (43 p.) | version publiée |
| **VW20** | N. Vyas, R. Williams, « Lower Bounds Against Sparse Symmetric Functions of ACC Circuits… », STACS 2020, LIPIcs 154, 59 ; ToCS 2023 | DROPS PDF officiel (17 p.) | version publiée |
| **CR20** | Lijie Chen, Hanlin Ren, « Strong Average-Case Circuit Lower Bounds from Non-trivial Derandomization », STOC 2020 ; SICOMP | page **ECCC TR20-010** | publié 12 févr. 2020, **révision n° 1 : 3 sept. 2020** |
| **BW24** | G. Bathie, R. R. Williams, « Towards Stronger Depth Lower Bounds », ITCS 2024, LIPIcs 287, 10:1-10:24 | **ECCC TR23-184** download (30 p.) | version complète ECCC |
| **CTW26** | Lijie Chen, Avishay Tal, Yichuan Wang, « Super-quadratic Lower Bounds for Depth-2 Linear Threshold Circuits », **STOC 2026** (doi 10.1145/3798129.3800802) | **ECCC TR26-039** download (32 p.) | soumis 14 mars 2026, publié 15 mars 2026 ; aucune révision listée (ouverture et clôture) |
| **NR04** | M. Naor, O. Reingold, « Number-Theoretic Constructions of Efficient Pseudo-Random Functions », FOCS 1997 ; JACM 51(2), 2004 | miroir PDF de la version JACM (aminer, 32 p.) | version journal |
| **KS06** | A. Klivans, A. Sherstov, « Cryptographic Hardness for Learning Intersections of Halfspaces », FOCS 2006 ; JCSS 75(1) 2009 | `cs.utexas.edu/~klivans/crypto-hs.pdf` (21 p.) | version auteur |
| **KL01** | M. Krause, S. Lucks, « On the Minimal Hardware Complexity of Pseudorandom Function Generators » STACS 2001 ; « Pseudorandom functions in TC⁰… », comput. complexity 10(4):297-313, 2001 | **[TEXTE NON OUVERT]** — Springer paywalled, dépôt MADOC sans abstract ni PDF | — |
| IPS13 | Impagliazzo, Paturi, Schneider, « A Satisfiability Algorithm for Sparse Depth Two Threshold Circuits », FOCS 2013 | arXiv:1212.4548, abstract verbatim (page abs) | v1 19 déc. 2012, **v2 17 avr. 2013** |

---

## (ii) LE TRANSFERT EXACT, théorème par théorème, et son instanciation THR∘THR

### 1. Les théorèmes généraux de W10 (le socle)

> **Theorem 1.1** (W10) : « Suppose there is a superpolynomial function s(n) such that CIRCUIT SAT on circuits with n variables and n^k gates can be solved in 2^n · poly(n^k)/s(n) time by a (co-non)deterministic algorithm, for all k. Then NEXP ⊄ P/poly. »

> **Theorem 1.3** (W10, CAPP) : « If there is an O(2^n · poly(n^c)/s(n)) nondeterministic algorithm for CAPP (for any superpolynomial s(n)), then NEXP ⊄ P/poly. » — et la remarque gap : « The proof of Theorem 1.3 holds even if we replace CAPP with the problem of distinguishing between circuits which are unsatisfiable and circuits with at least 2^{n−1} satisfying assignments. »

Pour les classes restreintes, la condition de clôture est écrite en toutes lettres :

> (W10, §3.1) : « let C be any non-uniform class of circuits that **contains AC0 and is closed under composition of circuits**. […] (Note that all well-studied classes of circuits have this property.) **Theorem 3.5** : If satisfiability of C-circuits on n variables and n^c gates can be solved in 2^{n/3}·poly(n^c)/s(n) time, then E^NP does not have polynomial size C-circuits. »

Mécanisme (Thm 3.2 + Lemma 3.2 « Folklore ») : témoin universel deviné → circuit E composé de « **three copies of the witness circuit** » + circuiterie AC⁰, UNSAT testé, contradiction avec la hiérarchie non-déterministe.

**Instanciation C = THR∘THR : ÉCHEC des hypothèses.** ✗ « contains AC⁰ » : non connu (THR∘THR poly ⊉ AC⁰ profondeur d quelconque). ✗ « closed under composition » : faux tel quel (composer deux profondeur-2 donne profondeur 4).

### 2. JACM14 — le métathéorème et ses propres exemples

> « Let C be a class of circuit families that is **closed under composition** (the composition of two circuit families from C is also a family in C) and **contains AC0**. Possible C include **constant-depth threshold circuits**, Boolean formulas, and unrestricted Boolean circuits. […] **THEOREM 1.3.** There is a k > 0 such that, if satisfiability of C-circuits with n variables and n^c size can be solved in O(2^n/n^k) time for every c, then NTIME[2^n] doesn't have non-uniform polysize C-circuits. »

Noter : l'exemple donné est « constant-depth threshold circuits » = **TC⁰ entier**, PAS la sous-classe profondeur-2. Et Remark 3.5 : « We only need that the underlying circuit class C contains AC0 and is closed under composition of two circuit families. » Même échec pour THR∘THR. Détail utile : le gain requis est un **polynôme FIXE** (O(2ⁿ/n^k) pour un k issu de la preuve), pas ω(1) — raffinement déjà présent ici.

### 3. MW18 — NQP/NP, la définition « typical »

> Définition (MW18, Préliminaires) : « C is **evaluatable** if […] the sub-circuit C(a) can be determined in polynomial time. […] **closed under negation** if there is a poly(n)-time algorithm […] outputs a description of ¬C. C is **closed under conjunctions** if there is a poly(n)-time algorithm A such that, given the descriptions of n circuits C1,…,Cn, each on n inputs from C, algorithm A outputs a circuit C′(x1,…,xn) ≡ C1(x1,…,xn) ∧ ··· ∧ Cn(x1,…,xn). Any C satisfying all three properties is called **typical**. »

> **Theorem 1.1** (MW18) : « Let C be typical, and let ε ∈ (0,1). Suppose GAP C UNSAT on n-input, 2^{εn}-size circuits is solvable in nondeterministic O(2^{(1−ε)n}) time. Then there is a c ≥ 1 such that for all k, NTIME[n^{ck⁴/ε}] does not have n^k-size C-circuits. »
> **Theorem 1.2** (MW18) : « Let C be typical, and let ε ∈ (0,1). Suppose GAP C UNSAT on n-input, 2^{n^ε}-size circuits is in nondeterministic O(2^{n−n^ε}) time. Then for all k, there is a c ≥ 1 such that NTIME[2^{log^{ck⁴/ε} n}] does not have 2^{log^k n}-size C-circuits. »

(GAP C UNSAT = distinguer UNSAT de ≥ 2ⁿ/4 assignments satisfaisants, algorithme non-déterministe à trois sorties.) **Instanciation THR∘THR : ✗ clôture par conjonctions non connue** (AND de n circuits THR∘THR = intersection, pas un THR∘THR connu). MW18 s'applique en revanche verbatim à ACC⁰∘THR (le haut ACC absorbe le ∧) :

> **Theorem 1.3** (MW18) : « For every constant k, d, and m ≥ 2, there is an e ≥ 1 and a problem in NTIME[n^{log^e n}] which does not have depth-d n^{log^k n}-size AC[m] circuits, even with n^{log^k n} linear threshold gates at the bottom layer. » (= NQP ⊄ ACC⁰∘THR quasi-poly.)

### 4. L'obstacle de clôture, nommé par Williams lui-même dès 2014

> (W14thr, note 6) : « The current theorems connecting circuit evaluation algorithms to circuit lower bounds require that, from the OR of a collection of circuits, we can generate an equivalent circuit in the same class. **We do not know how to convert a large OR of THR∘THR circuits into an equivalent THR∘THR circuit**, even assuming NEXP has small THR∘THR circuits. (In the case of ACC, this is trivial, because an OR of ACC circuits is still an ACC circuit.) »

### 5. BV14 — la clôture réduite aux projections (route E^NP)

> (BV14, abstract) : « Our proof yields a tighter connection: C is an And-Or of circuits from C′. Along the way we show that the same lower bound follows if the satisfiability of the **And of any 3 circuits from C′** can be solved in time 2^n/n^{ω(1)}. »

Forme utilisée par Tamaki (Tam16, Theorem 5.1, citant BV14) : « Let Cn be **efficiently closed under projections**. If the satisfiability problem of the form f₁∧f₂∧f₃ for f₁,f₂,f₃ ∈ C_{n+O(lg n)} can be deterministically solved in time 2^{n−ω(lg n)}, then there exists a language L ∈ E^NP such that Ln ∉ Cn holds for infinitely many n. » Et l'instanciation 2016 : « The class of depth 2 circuits with m symmetric and linear threshold gates is clearly efficiently closed under projections. » (le facteur 3 du ∧₃ coûte ×3 sur le degré du polynôme final).

### 6. CW19 — LE théorème que PR-005 cherchait (CORRECTION D'ATTRIBUTION)

CW19 affaiblit « typical » à : « **closed under taking negations of the output, and variable projections** » — THR∘THR **satisfait** cette définition (négation = renverser la porte de tête ; projections triviales).

> **Theorem 5** (CW19) : « There is an absolute constant δ > 0, such that for any typical circuit class C, if one of the following holds: there is a non-trivial Gap-UNSAT algorithm with gap δ for poly(n)-size AND₃∘C circuits, or there is a non-trivial CAPP algorithm with error δ for poly(n)-size OR₂∘C, ⊕₂∘C, or AND₂∘C circuits, then NEXP ⊄ C. Moreover, in the second bullet, C does not need to be closed under negation. »

(« non-trivial » = « for all c, it runs in 2^n/n^{ω(1)} time for all circuits of size n^c ».) Et l'instanciation profondeur-2, écrite noir sur blanc (§1.3, « Potential Approaches to THR∘THR Circuit Lower Bounds ») :

> « As a direct corollary of Theorem 5 and the folklore result that an **XOR of two THR∘THR can be written as a polynomially-larger THR∘THR** [note 4 : « See e.g. Lemma 50 for a proof »], it follows that non-trivial CAPP algorithms for THR∘THR circuits with small constant error would imply NEXP ⊄ THR∘THR. […]
> **Theorem 8.** There is an absolute constant δ > 0, such that if δ-error CAPP for poly(n)-size THR∘THR circuits can be solved in 2^n/n^{ω(1)} time, then NEXP ⊄ THR∘THR. The same is true with SAT in place of CAPP.
> **Theorem 9.** [même énoncé pour LT_d, TC⁰ de profondeur d quelconque] »

Et le recalibrage stratégique :

> **Corollary 10** (CW19) : « There is an absolute constant δ > 0, such that if one of the following holds: 1. CAPP (or SAT) for poly(n)-size **THR∘MAJ** circuits with error δ is in 2^n/n^{ω(1)} time, or 2. CAPP for poly(n)-size **MAJ∘MAJ** circuits with **1/poly(n) error** is in 2^n/n^{ω(1)} time, then NEXP ⊄ THR∘THR. » — « Therefore NEXP ⊄ THR∘THR follows if we can "mine" the known 2^{Ω(n)} lower bounds for THR∘MAJ or MAJ∘MAJ, and design non-trivial circuit-analysis algorithms from them! »

Versions NP (plus rapides) : **Theorem 6** (CW19) : CAPP d'erreur constante pour ⊕₂∘C de taille 2^{δn} en temps 2^{n−δn} ⟹ NP ⊄ n^k-size C pour tout k (via l'easy witness lemma de MW18). L'ingrédient PCPP à 2 requêtes est **Lemma 25** (CW19) : « For any constant δ > 0 there [are] two constants 0 < s < c < 1, such that there is a PCP of proximity system for Circuit-Eval with proximity δ, soundness s, completeness c, number of random bits r = O(log n) and query complexity q = 2. »

### 7. BW24 → CTW26 — la forme ciblée-en-taille (E^NP), celle du front 2026

> (BW24, § « Generalization to Other Circuit Classes ») : « the connection proved between Gap-SAT algorithms and circuit lower bounds is rather general: any non-trivial Gap-SAT algorithm for a size-O(s(n)) circuit class C such that **(a) C can compute PARITY in size s(n), (b) C is closed under the OR of 3 copies of C, and (c) C is closed under negations of their outputs, and projections** […] implies size-s(n) lower bounds against C. »

> **Lemma 3.8** (CTW26, attribué « [BW24, Theorem 3.7, Section 3.3] ») : « Let α > 1. If the CAPP with error o(1) for O(n^α)-size ⊕₂∘THR∘THR circuit can be solved in 2^n/n^{ω(1)} time, then **E^NP does not have n^α-size THR∘THR circuits**. The same also holds if we replace THR∘THR by SYM∘THR. » Preuve (esquisse verbatim) : « Theorem 3.7 of [BW24] and its generalization in Section 3.3 require that (i) n^α-size THR∘THR can compute parity (which is true for α ≥ 1) and (ii) a CAPP algorithm for O(n^α)-size OR₃∘THR∘THR. The second requirement can be relaxed to ⊕₂∘THR∘THR by using the 2-query PCPP specified in [CW19, Lemma 25] instead of the 3-query PCPP used in [BW24]. »

### Bilan d'instanciation (les conditions, cochées une à une pour C = THR∘THR)

| Condition | THR∘THR ? |
|---|---|
| négation de la sortie | ✓ (renverser la porte de tête) |
| projections (0/1 et négations de variables) | ✓ |
| calcule PARITY en taille n^α, α ≥ 1 | ✓ (MAJ∘MAJ, O(n) portes — KW16 : « PARITY is well-known to have MAJ∘MAJ circuits of O(n) gates ») |
| ⊕₂-clôture (XOR de deux) | ✓ **folklore, CW19 Lemma 50** (agrandissement polynomial) |
| OR/AND-clôture (∨₃, ∧_n) | ✗ non connue — c'est l'obstacle historique (W14thr note 6) ; **contournée** par le PCPP à 2 requêtes |
| contient AC⁰ ; clôture par composition (W10/JACM14) | ✗ — ces théorèmes-là ne s'appliquent pas tels quels |

**Verdict mission n° 1 — l'attribution de PR-005 est à corriger.** L'énoncé visé (« #SAT ou CAPP déterministe pour THR∘THR de taille polynomiale en 2ⁿ/n^{ω(1)} ⟹ NEXP ⊄ THR∘THR ») est **VRAI et numéroté**, mais il n'est un théorème ni de Williams 2011 ni de Murray-Williams 2018 : leurs hypothèses de clôture (composition + AC⁰ ; « typical » avec ∧_n) ne sont pas satisfaites par THR∘THR — Williams a nommé l'obstacle en 2014 (note 6). La flèche exacte est **Chen-Williams CCC 2019, Theorem 8** (CAPP à erreur constante OU SAT, poly-taille, 2ⁿ/n^{ω(1)}, conclusion NEXP) ; la forme ciblée en taille est **Bathie-Williams ITCS 2024 (Th. 3.7 + §3.3) via CTW26 Lemma 3.8** (CAPP o(1) de ⊕₂∘THR∘THR[n^α] ⟹ E^NP ⊄ THR∘THR[n^α]) ; MW18 fournit l'étage NQP/NP du cadre général (et sert dans CW19 Thm 6), mais pas l'instanciation profondeur-2. #SAT ⟹ SAT et CAPP(erreur 0), donc #SAT suffit a fortiori. Aucun numéro fantôme : tous les numéros ci-dessus vérifiés sur texte.

---

## (iii) LE GABARIT ALGORITHMIQUE (Williams STOC 2014, arXiv:1401.2444)

> **Theorem 1.1** : « Given a SYM∘ACC∘THR circuit with n inputs and 2^{n^{o(1)}} size, we can produce its outputs on all 2^n inputs in 2^n · poly(n) time. »
> **Theorem 1.2** : « For every integer m > 1 and d > 0, there is an ε > 0 such that counting satisfying assignments to ACC∘THR circuits of size 2^{n^ε}, depth d, and MODm gates can be done in 2^{n−n^ε} time. »
> **Theorem 1.3** : « NEXP does not have non-uniform ACC∘THR circuits of quasi-polynomial size. » (idem ACC∘SYM ; « Nontrivial size lower bounds were not known even for AND∘OR∘THR circuits », abstract.)

Le pipeline (les paramètres consommés, §2) : (1) **réduction de poids** — « we can assume that the weights of all threshold gates in C have absolute value at most 2^{bn log₂ n} [MTT61, Mur71] » + note 7 : représentation petite-pondération obtenue « by evaluating the large-weight representation at only n+1 points, then solving a linear system » [MTT61, Thm 16] ; (2) THR → AC⁰∘MAJ via **Maciel-Thérien** (Thm 2.1 : « Addition of n distinct n-bit numbers can be performed with polynomial-size AND∘OR∘SYM circuits ») ; (3) **Beigel-Tarui** (Thm 2.2 : « Every SYM∘ACC circuit of size s can be simulated by a SYM∘AND circuit of 2^{(log s)^{c′}} size […] the AND gates of the final circuit have only (log s)^{c′} fan-in ») ; (4) **évaluation par lots** via la multiplication rectangulaire de **Coppersmith** (« a rectangular matrix multiplication of Coppersmith [Cop82] can be applied […] the final matrix M is obtained in poly(n) time per entry »).

**Ce que le papier dit de THR∘THR** :

> **Theorem 1.5** : « Let k > 1. Given a depth-two 2^{n/24}-size linear threshold circuit C with integer weights in [−2^{n^k}, 2^{n^k}], we can evaluate C on all 2^n input assignments in 2^n · poly(n^k) time. » — « This is evidence that non-uniform lower bounds for THR∘THR are within reach » (abstract) — MAIS : « **we do not yet know how to turn Theorem 1.5 into depth-two linear threshold lower bounds** » (texte, renvoyant à la note 6 citée plus haut : l'OR-clôture manquante).

L'évaluation par lots existe donc pour THR∘THR à poids exponentiels depuis 2014 ; c'est la conversion évaluation → SAT/CAPP qui bloquait.

---

## (iv) LA FRONTIÈRE 2014-2026 (état exact de « SAT/#SAT/CAPP non trivial pour THR∘THR »)

**Réponse courte : PARTIEL, borné en nombre de portes ; la taille polynomiale générale reste OUVERTE.** CTW26 (mars 2026) : « despite much effort […] **prior to this work, we still do not have any non-trivial circuit-analysis algorithms for super-quadratic-size THR∘THR circuits (say, size n^{2.001}) for either SAT or CAPP**. »

| Année | Pièce | Algorithme (verbatim des paramètres) | Borne dérivée | Restrictions |
|---|---|---|---|---|
| 2013 | IPS13 (FOCS) | SAT « for cn-wire threshold circuits of depth two […] better than exhaustive search by a factor 2^{sn} where s = 1/c^{O(c²)} » (randomisé zéro-erreur) | — (motivation TC⁰ nommée) | **fils linéaires** cn |
| 2015-16 | CSS16 (CCC) | « **Theorem 2.** For each depth d ≥ 1, there is a constant ε_d > 0 such that the satisfiability of depth-d threshold circuits with n^{1+ε_d} wires can be solved in randomized time 2^{n−n^{ε_d}} poly(n) » | corrélation : Parity ≤ 1/n^{Ω(1)}, Generalized Andreev ≤ 1/2^{n^{Ω(1)}} (Theorem 1) | fils **n^{1+ε_d}**, ε_d = 1/2^{O(d)} |
| 2016 | KW16 (STOC) | pas d'algorithme — restrictions aléatoires + Littlewood-Offord | « Andreev's function cannot be computed on a (1/2+ε)-fraction […] by depth-two linear threshold circuits of o(ε³n^{3/2}/log³n) gates, nor […] o(ε³n^{5/2}/log^{7/2}n) wires » — fonction dans **P**, average-case | portes n^{1.5−o(1)} |
| 2016 | **Tam16** (ECCC TR16-100) | « **Theorem 1.1.** […] deterministic algorithm that, given a depth 2 circuit C with n variables and m gates, where each gate is either symmetric or linear threshold, runs in time 2^{n−Ω((n/(√m·poly(log n)))^c)} and **counts the number of satisfying assignments** » — superpoly ssi m = O(n²/log^b n) | « **Theorem 1.2.** There exist a language L ∈ E^NP […] any family of depth 2 circuits with O(n²/log^c n) gates, where each gate is either symmetric or linear threshold, cannot compute L » | portes **sous-quadratique** ; couvre SYM∘SYM |
| 2016 | **ACW16** (FOCS) | « **Theorem 1.8.** For every integer d > 0, m > 1, and δ > 0, there is an ε > 0 and an algorithm for satisfiability of AC0[d,m]∘LTF∘LTF[2^{n^ε}, 2^{n^ε}, n^{2−δ}] circuits that runs in **deterministic 2^{n−n^ε}** time » ; « trivially implies deterministic SAT algorithms for LTF∘LTF circuits of up to n^{2−o(1)} gates » | « **Corollary 1.1.** […] E^NP does not have non-uniform circuits in AC0[d,m]∘LTF∘LTF[2^{n^ε},2^{n^ε},n^{2−δ}] » — CTW26 précise : « with no restriction on the number of THR gates in the second layer » | fond **n^{2−δ}** portes LTF ; #SAT aussi (per CTW26) |
| 2018 | Chen18 (arXiv) | équivalences fine-grained : « An n²poly(d)/log^{ω(1)} n time algorithm for ℓ₂-Furthest-Pair […] implies NEXP has no polynomial size THR∘THR circuits. The same holds for Hopcroft's problem, Bichrom.-ℓ₂-Closest-Pair and Integer Max-IP » ; Boolean Max-IP d = n^ε idem ; approx-Closest-Pair ⟹ SYM∘THR | (conditionnel) | « **A major frontier is to prove that NEXP does not have poly-size THR∘THR circuit** » (verbatim) |
| 2018 | Wil18 (CCC) | Sum-Product algorithms (Subset-Sum-style) | « **Theorem 1.1.** For all k, there is an f_k ∈ NP without **SUM∘THR** circuits of n^k sparsity » (+ NTIME[n^{α(n)}]) ; idem SUM∘ReLU | combinaisons **linéaires exactes**, pas THR∘THR |
| 2018 | [Tel18] STOC 2018 (Tell) | dérandomisation **quantifiée** de circuits LTF (cité par CTW26 dans la liste des « non-trivial circuit-analysis algorithms […] for interesting subclasses of TC⁰ ») | — | promesse quantifiée, pas CAPP plein |
| 2019 | **CW19** (CCC) | équivalences : « **Theorem 1.** […] There is a non-trivial SAT algorithm for THR∘MAJ circuits of poly(n)-size **if and only if** there is such an algorithm for poly(n)-size THR∘THR circuits » ; CAPP : erreur δ (THR∘MAJ) → δ+1/n (THR∘THR) ; « **Theorem 3.** If SAT for poly(n)-size MAJ∘MAJ circuits is in 2^{(1−ε)n} time […] then SAT for poly(n)-size THR∘THR […] in 2^{(1−ε′)n} » ; CAPP 1/poly-erreur MAJ∘MAJ → THR∘THR ; Corollaries 2/4 : toute profondeur d | Theorems 8/9/Corollary 10 (cf. §ii) ; Theorems 12/13 : NP ⊄ Sum_ε∘THR (« depth-two neural networks with sign activation functions »), poly sparsity, tout ε < 1/2 | le verrou déplacé vers MAJ∘MAJ/THR∘MAJ |
| 2018-20 | MW18 ; CR20 ; CLW20 ; VW20 | (SAT ACC∘THR de W14thr réutilisé) | MW18 Thm 1.3 : NQP ⊄ ACC⁰∘THR quasi-poly ; CR20 (TR20-010, page ECCC) : « NQP = NTIME[n^{polylog(n)}] cannot be (1/2 + 2^{−log^a n})-approximated by 2^{log^a n}-size ACC⁰ of THR circuits » ; VW20 Corollary 4 : « For all constant depths d ≥ 2 and constant moduli m ≥ 2, Quasi-NP does not have polynomial-size **EMAJ∘AC⁰[m]∘THR** circuits » (« the first nontrivial lower bound against such a circuit class ») ; CLW20 = versions almost-everywhere [PDF 403, non ouvert — entrée d'après CR20/recherche] | tout ceci reste **au-dessus d'un top ACC⁰/EMAJ**, pas THR∘THR |
| 2020 | VW20, Conjecture 1 | « Non-trivial #SAT algorithms for circuit classes C imply size lower bounds against **SYM∘C** circuits » — « If Conjecture 1 is true, then existing #SAT algorithms would already imply super-polynomial lower bounds for SYM∘ACC⁰∘THR circuits, a class that contains depth-two symmetric circuits (**for which no lower bounds greater than n² are presently known**) » | (conjecture, ouverte) | — |
| **2026** | **CTW26** (STOC 2026, ECCC TR26-039) | « **Theorem 1.2.** For every constant ε ∈ (0,1), there is a **deterministic** algorithm for solving **CAPP for ⊕₂∘THR_{O(n^{2.5−ε})}∘THR with error o(1)** that runs in O(2^{n−n^{Ω(ε)}}) time. » — « We only obtain the weaker CAPP algorithm, which is sufficient nonetheless for the algorithmic method » (Tam16/ACW16 avaient le #SAT) | « **Theorem 1.1.** For every constant ε ∈ (0,1), there is a function f ∈ **E^NP** that cannot be computed by **n^{2.5−ε}-size THR∘THR** circuits. The same holds for SYM∘THR. » (ne s'étend PAS à SYM∘SYM, note 3) | portes n^{2.5−ε} ; méthode : restrictions aléatoires (portes non-constantes ≤ n^{2−ε/2} sur la plupart des colonnes) + « only quasi-polynomially many distinct "types" » de polynômes probabilistes |

**Y a-t-il déjà une borne NEXP/NQP ⊄ THR∘THR sous restriction de poids ? OUI — et bien plus fort, depuis les années 1990.** W14thr §1.1, verbatim : « Hajnal et al. [HMP+93] proved that every MAJ∘MAJ circuit requires 2^{Ω(n)} gates to compute IP2. […] Nisan [Nis94] extended the lower bound to MAJ∘THR circuits, and Forster et al. [FKL+01] extended the lower bound to THR∘MAJ circuits. » (KW16 précise que Nisan traite MAJ∘LTF « even if the weights of the LTFs on the hidden layer are arbitrary », et FKL+01 LTF∘MAJ.) IP2 est calculable en temps polynomial : **dès qu'une des deux couches a des poids polynomiaux, une borne exponentielle EXPLICITE (fonction dans P) est connue** — une « victoire » de PR-005 sous restriction de poids serait donc subsumée et sans valeur. La cible de PR-005 doit être formulée **poids libres aux deux étages** ; en revanche, côté ALGORITHME, la restriction de poids est gratuite (CW19 Thm 1/3 : équivalences).

**Recalibrage explicite demandé par la mission : oui, PR-005 doit être recalibrée** — (a) attribution de la flèche → CW19 Thm 8 (+ BW24/CTW26 pour E^NP ciblé) ; (b) l'état de l'art n'est plus « rien au-delà de n^{1.5} » mais **E^NP ⊄ THR∘THR[n^{2.5−ε}] (mars 2026)** avec CAPP déterministe pour ⊕₂∘THR∘THR jusqu'à n^{2.5−ε} portes ; (c) le premier jalon ouvert nommable est « CAPP non trivial pour THR∘THR de taille n^{2.5} et au-delà », le jalon majeur « poly-taille » (⟹ NEXP ⊄ THR∘THR, CW19 Thm 8). Bornes : SETH interdit 2^{(1−ε)n} même pour AND∘OR ⊆ THR∘THR (inclusion par définition — remarque du présent audit, pas un théorème sourcé) : le régime 2ⁿ/n^{ω(1)} est le bon.

---

## (v) BARRIÈRES pour cette variante

- **Relativisation / algébrisation.** W10 (verbatim, conclusion) : « The three primary barriers are relativization, natural proofs, and algebrization. We believe our work may provide a path that circumvents all three (provided the appropriate algorithms exist, of course!). […] all nontrivial SAT algorithms that we know do not relativize or algebrize. » JACM14 (version journal, concordante avec A-001) : « More conclusively, the approach of this work definitely avoids relativization [Baker et al. 1975] and algebrization [Aaronson and Wigderson 2009] because there are oracles A relative to which NEXP^A ⊂ ACC^A, and even NEXP^{Ã} ⊂ ACC^A (Scott Aaronson, personal communication). » **Pour les extensions THR (W14thr, ACW16, CW19, BW24, CTW26) : aucune discussion propre de relativisation/algébrisation — [NON TROUVÉ]** (greps exhaustifs ; seules des entrées bibliographiques). L'héritage est structurel (même machinerie PCP/easy-witness/hiérarchie + un algorithme qui lit le circuit), pas re-déclaré.
- **Preuves naturelles.** JACM14 : « we circumvent the natural proofs barrier [Razborov and Rudich 1997] because of the use of diagonalization […] there is little evidence that ACC contains pseudorandom functions ». W14thr note 1 : « NEXP ⊄ P/poly if and only if there is a "constructive" property of Boolean functions that is "useful" against P/poly » [Wil13b]. **Où vivent les PRF :** NR04 (verbatim) : « these functions have the advantage of being in TC0 » ; « if the GDH-Assumption holds against a subexponential-time adversary (and in particular if factoring is sufficiently hard), then there are no Natural Proofs for separating TC0 from P/poly » ; profondeur fine (NR04, §4.2, citant Siu et al.) : « multiple sum is in TC0₂, multiplication and division in TC0₃ and multiple product in **TC0₄** ». W14thr : « Plaku [Pla02] observed that the Naor-Reingold family of pseudorandom functions [NR04] can be implemented with quasi-polynomial size **OR∘THR∘AND** circuits; it follows that the natural proofs barrier already applies to this circuit class. It is an interesting open problem if ACC∘THR can efficiently simulate such depth-three circuits. » ACW16 : « It would not be surprising (to at least one author) if [MAJ∘AC⁰∘LTF∘AC⁰∘LTF] contained strong pseudorandom function candidates ». **Pour THR∘THR (profondeur 2)** : aucun candidat PRF revendiqué dans le corpus ouvert ; Krause-Lucks 2001 affirmeraient l'impossibilité pour TC⁰₂ et l'ouverture pour TC⁰₃ (« TC⁰₂ do not contain PRFGs », « NR […] consists of TC⁰₄-functions », « whether TC⁰₃-functions can form PRFGs remains an open problem ») — **[TEXTE NON OUVERT : résumés de moteur seulement, à re-sourcer avant toute citation]**. Pièce ouverte la plus proche : KS06, « **Theorem 1.3.** Assume that depth-2 polynomial-size circuits of majority gates are PAC learnable. Then there is a polynomial-time solution to Õ(n^{1.5})-uSVP and polynomial-time quantum solutions to Õ(n^{1.5})-SVP and Õ(n^{1.5})-SIVP » (+ remarque : Feldman et al. indépendamment via Ajtai-Dwork) — dureté d'apprentissage (plus faible qu'un PRF) dès la profondeur 2 à poids polynomiaux. Bilan cellule : la barrière RR n'est PAS établie pour THR∘THR, et la méthode algorithmique l'esquive de toute façon par constructivité/diagonalisation.
- **Monotone** : sans objet (seuils signés) — aucune occurrence dans le corpus, conforme.

---

## (vi) LE PARAMÈTRE POIDS + folklore-check (réponse à ALG-001/ALG-002)

Ce que la littérature fait du poids, pièce par pièce : (1) **borne de Muroga et réduction effective** (W14thr + MTT61 Thm 16, verbatim au §iii) : tout THR ⟺ poids de bit-complexité O(n log n), calculables par n+1 évaluations + système linéaire ; (2) **élimination structurelle du poids** : GHR92 (KW16, verbatim) : « every LTF∘LTF circuit can be efficiently simulated by a MAJ∘MAJ∘MAJ circuit » ; MT98 : THR → AC⁰∘MAJ ; Hansen-Podolskii 2010 (repris par CTW26, Lemma 3.4) : « ∧_{poly(n)}∘ETHR ⊆ ETHR ; THR ⊆ DOR∘ETHR ; ETHR ⊆ GapAND∘SYM » ; (3) **élimination algorithmique du poids** : CW19 Theorems 1/3 et Corollaries 2/4 — pour concevoir l'algorithme, on peut supposer les poids du bas polynomiaux (équivalence exacte), et ceux du haut aussi au prix d'une erreur 1/poly ; (4) **le poids que le gabarit consomme réellement** : pour ACC∘THR, c'est la taille/le fan-in de la représentation SYM∘AND de Beigel-Tarui (quasi-poly, fan-in polylog) + la table du SYM — pas un poids de PTF ; pour THR∘THR (CTW26), c'est le **degré** des polynômes probabilistes (Õ(√m) pour un SYM de m fils, ACW16/AW15, avec polylog bits d'aléa), l'**amplification de module** (BT91, degré 2k−1), et le **nombre de portes non-constantes sous restriction** ; (5) **restrictions** : KW16 (« The key is a new random restriction lemma for linear threshold functions. Our main analytical tool is the Littlewood-Offord Lemma ») ; forme reprise par CTW26 Lemma 4.1 : « for a random restriction ρ ∈ {0,1,∗}^n, which has exactly k many ∗-s, with probability ≥ 1 − O(k/√n), f|ρ is a constant function » ; CTW26 §4 s'intitule « Simplification of THR Gates Under Random Restrictions ».

**Folklore-check du sous-lemme (« poids PTF sous restrictions », ALG-002 candidate)** : l'objet publié le plus proche est l'anti-concentration de Littlewood-Offord sous restriction (contrôle de la probabilité de non-constantification par la structure des poids), et les corrélations sous fils bornés (CSS16). **Une « loi du poids (PTF ou SYM+) minimal sous restrictions aléatoires » comme objet d'étude nommé : [NON TROUVÉ]** dans les ~17 textes ouverts consultés — confirmation du pronostic de la mission, avec la réserve d'usage (corpus ouvert, pas exhaustif). MAIS deux mises en garde pour le fil : (a) le transfert lui-même ne consomme AUCUN paramètre de poids — son unique hypothèse est le temps du CAPP (CW19 Thm 8) ; (b) CW19 Cor 10 montre que le mur « poids exponentiels de IP » (F-001) ne barre pas la route CAPP en tant que telle : la cible algorithmique peut être prise à poids polynomiaux (MAJ∘MAJ, erreur 1/poly). Ce que F-001 documente reste pertinent pour la route « représentation exacte type SYM+ » (aucun analogue Beigel-Tarui pour la profondeur 2 — cohérent avec A-001 §5.1), qui est précisément celle que CTW26 remplace par du probabiliste (« list approximating F₂-probabilistic polynomials », « only quasi-polynomially many distinct types »).

## (vii) Réserves

1. **Krause-Lucks 2001** : paywalled partout (Springer, MADOC sans abstract) — les trois affirmations (pas de PRFG dans TC⁰₂ ; NR ∈ TC⁰₄ ; TC⁰₃ ouvert) proviennent de résumés de moteur, PAS d'un texte ouvert ; à re-sourcer avant citation dans la cellule. La profondeur TC⁰₄ de NR est corroborée indirectement par NR04 lui-même (multiple product ∈ TC⁰₄, verbatim ci-dessus).
2. **CLW20** (almost-everywhere) : PDF Berkeley en 403 ; entrée de table fondée sur la page ECCC de CR20 et les résultats de recherche — au niveau abstract seulement.
3. **BW24 Theorem 3.7** est énoncé pour les formules DeMorgan (O(n^{3+ε})) ; l'extension aux classes générales est le §3.3 (conditions (a)(b)(c) verbatimées) et c'est CTW26 Lemma 3.8 qui écrit l'instanciation THR∘THR — la chaîne est citée exactement ainsi, sans lui inventer un numéro unique.
4. Les versions NP/NQP pour THR∘THR (via CW19 Thm 6 + Lemma 50) sont dérivables mais **non écrites verbatim** dans CW19 (qui écrit NEXP aux Thms 8/9) — à étiqueter [DÉRIVABLE] si une candidature veut viser NQP.
5. `jacm14.pdf` = version finale auteur (en-têtes JACM en gabarit « Vol. 9, No. 4 ») ; `w10.pdf` = version auteur mai 2010 (le SICOMP 2013 non audité séparément) ; Tam16 audité sur le TR ECCC (la version Springer 2025 non comparée).
6. La liste CTW26 des algorithmes de sous-classes ([SSTT15, SSTT16, Tel18, KL18, HHTT21, BKK+22]) n'a été suivie qu'au niveau bibliographique — aucun de ces travaux ne revendique THR∘THR au-delà du sous-quadratique (c'est l'affirmation verbatim de CTW26, mars 2026, qui fait foi pour l'état de l'art).
