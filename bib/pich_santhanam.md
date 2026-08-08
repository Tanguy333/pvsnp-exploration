# Audit A-018 — Pich & Santhanam, « Towards P ≠ NP from Extended Frege lower bounds »

Tâche : A-018 (2026-08-08). Type A (audit sur texte). Rattachement :
Atlas ligne 15 (complexité des preuves), convergence ligne 13
(méta-complexité). Audit mené par agent avec les règles du dépôt ;
consigné et relu par la session.

**Documents OUVERTS (textes intégraux lus)** : ECCC TR23-199 (35 p.,
PDF officiel, extraction versionnée `bib/pdf/eccc_tr23199_texte.txt`) ;
version auteur Oxford datée septembre 2023 (29 p.,
`bib/pdf/pich_eopt_oxford_texte.txt`) ; AKPS ICALP 2024 (Dagstuhl,
`bib/pdf/akps_icalp2024_texte.txt`). Abstract arXiv v1 via l'API.
**NON OUVERT** : la version de référence J. ACM 2026 (mur ACM) — voir
Réserves.

**Convention de transcription** : verbatims issus des extractions
pypdf ; seuls les indices/exposants et ligatures aplatis par
l'extraction sont restaurés (`S1 2` → S¹₂, `wk n(f)` → w^k_n(f)) ;
aucun autre mot modifié.

## 1. Identification

| Version | Référence | Date | État |
|---|---|---|---|
| ECCC TR23-199 | https://eccc.weizmann.ac.il/report/2023/199/ | 2023-12-09 | 35 p. — **aucune révision** (« No revisions listed », vérifié à l'ouverture ET à la clôture, 2026-08-08). Mots-clés ECCC : « self-provability, witnessing ». |
| arXiv 2312.08163 | https://arxiv.org/abs/2312.08163 | 2023-12-13 | **v1 unique** (vérifié ouverture + clôture) ; note admin : « text overlap with arXiv:2111.10626 » (leur papier automatability). |
| PDF auteur (Oxford) | https://users.ox.ac.uk/~coml0742/papers/eopt.pdf | sept. 2023 | 29 p. ; porte : « A version of the paper with a less technical introduction appeared on ECCC. » |
| **J. ACM (référence)** | J. ACM 73(2), art. 12, p. 12:1-12:27, avril 2026, DOI 10.1145/3801091 | 2026 | **NON OUVERT** (403 + mur anti-bot ACM, aucune version OA) ; référence confirmée par dblp (journals/jacm/PichS26) et la page Oxford de Pich (« Accepted to JACM »). |

Les deux expositions 2023 diffèrent d'habillage et de **numérotation**
(ECCC : Th. 1-6 informels, 8-12 formels + logarithme discret ;
arXiv/Sept : Th. 1-5 informels, 7-9 formels), pas de substance visible
sur les énoncés comparés. Numérotation ECCC ci-dessous.

## 2. L'énoncé-titre (abstract arXiv v1, verbatim)

> « We prove that if conditions I-II (below) hold and there is a
> sequence of Boolean functions f_n hard to approximate by p-size
> circuits such that p-size circuit lower bounds for f_n do not have
> p-size proofs in Extended Frege system EF, then P ≠ NP.
> I. S¹₂ proves that a concrete function in E is hard to approximate by
> subexponential-size circuits.
> II. [Learning from ¬∃ OWF.] S¹₂ proves that a p-time reduction
> transforms circuits breaking one-way functions to p-size circuits
> learning p-size circuits over the uniform distribution, with
> membership queries.
> Here, S¹₂ is Buss's theory of bounded arithmetic formalizing p-time
> reasoning. Further, we show that any of the following assumptions
> implies that P ≠ NP, if EF is not p-bounded:
> 1. [Feasible anticheckers.] S¹₂ proves that a p-time function
> generates anticheckers for SAT.
> 2. [Witnessing NP ⊄ P/poly.] S¹₂ proves that a p-time function
> witnesses an error of each p-size circuit which fails to solve SAT.
> 3. [OWF from NP ⊄ P/poly & hardness of E.] Condition I holds and S¹₂
> proves that a p-time reduction transforms circuits breaking one-way
> functions to p-size circuits computing SAT.
> The results generalize to stronger theories and proof systems. »

**Précision structurante pour la cellule 15** : dans la route principale
(conditions I-II), la « borne EF » requise porte sur les **formules de
tables de vérité** tt(g_n, n^t) (taille exponentielle en n) — pas sur
des tautologies quelconques ; dans les variantes 1-3, « EF is not
p-bounded » (une tautologie dure quelconque) suffit.

## 3. Le plafond structurel — la « barrière Pich-Santhanam »

> « **Proposition 1.** Suppose that Q is a propositional proof system
> such that super-polynomial lower bounds on the Q-proof size for any
> sequence of tautologies implies that NP ⊄ P/poly. Then we have
> unconditionally that NEXP ⊄ P/poly. » (ECCC p. 3)

Preuve en cinq lignes via IKW (si Q p-borné : NP = coNP, et
NEXP ⊆ P/poly forcerait NEXP = MA = NP contre la hiérarchie
non-déterministe). **C'est ce qui rend les conditions non-optionnelles** :
une connexion inconditionnelle « bornes de preuves ⟹ NP ⊄ P/poly »
donnerait NEXP ⊄ P/poly d'office. La littérature aval (AKPS 2024)
l'appelle « the Pich-Santhanam barrier ».

## 4. Le mécanisme : témoignage et auto-prouvabilité

Formule de témoignage (ECCC §1.2, verbatim) :

> « w^k_n(f) := [SAT_n(x,y) → SAT_n(x,C(x))] ∨
> [SAT_n(f₁(C),f₂(C)) ∧ ¬SAT_n(f₁(C),C(f₁(C)))] »

— pour tout circuit C de taille n^k : ou bien C résout SAT-recherche,
ou bien la fonction p-time f exhibe un contre-exemple vérifiable.
Concept porteur : la **self-provability** — si SAT ∈ P/poly et que le
témoignage est disponible, cette facilité *se prouve elle-même*
efficacement ; toute borne inférieure de preuve la réfute donc.

## 5. Les théorèmes (verbatim, numérotation ECCC)

**Théorème 9** (= Th. 2 intro ECCC ; Th. 1 arXiv) — le cœur :

> « **Theorem 9** (Circuit complexity from proof complexity &
> witnessing of NP ⊄ P/poly). Let k ≥ 1 be a constant.
> 1. Suppose that there is a p-time function f such that for each big
> enough n, w^k_n(f) is a tautology. If EF + w^k(f) is not p-bounded,
> then SAT_n ∉ Circuit[n^{εk}] for infinitely many n.
> 2. Suppose that there is a p-time function f such that for some n₀,
> S¹₂ ⊢ W^k_{n₀}(f). If EF is not p-bounded, then
> SAT_n ∉ Circuit[n^{εk}] for infinitely many n.
> In Items 1 and 2, ε > 0 is a universal constant (independent of k). »

**Corollaire 1** — divergence de conclusion entre expositions (même
hypothèse « pour tout k, w^k_n(f_k) tautologies ») : ECCC conclut
« NEXP ⊄ P/poly » ; arXiv/Sept conclut « NP ⊄ SIZE[n^ℓ], for all
ℓ ∈ N » (cas p-borné ⟹ NP = coNP ⟹ Kannan). **Corollaire 3** (ECCC ;
Cor. 2 arXiv) — version uniforme (« witnessing of P ≠ NP ») : formules
w^{k,u}_n(f) pour algorithmes + conseil u(n), conclusion
« SAT ∉ Time[n^{Ω(k)}]/u(n) ».

**Théorème 10** (= Th. 4 informel ; Th. 7/3 arXiv) — anticheckers :

> « Let k ≥ 3 be a constant and assume that there is a p-time function
> f such that S¹₂ proves that for all integers n either f(1ⁿ) outputs a
> poly(n) circuit B solving SAT on inputs of length n, or f(1ⁿ) outputs
> an antichecker of SAT on inputs of length n with respect to size n^k,
> together with satisfying assignments for all YES instances of the
> antichecker. Then, EF is not p-bounded implies
> SAT_n ∉ Circuit[n^k] for infinitely many n. »

Version non-uniforme inconditionnelle, **Théorème 3** : « If there are
tautologies without p-size EF-derivations from substitutional instances
of tautologies α^{n^k}_n, then SAT_n ∉ Circuit[n^k] for infinitely many
n » — les α^{n^k}_n étant les tautologies-anticheckers garanties par
Lipton-Young 1994, non constructibles (EF + α^{n^k} est un système à
conseil, « in certain sense optimal »).

**Théorème 11** (= Th. 5 informel ; Th. 8/4 arXiv) — OWF depuis
NP ⊄ P/poly & E dure :

> « Assume that there is h′ ∈ E such that for each sufficiently big n,
> each 2^{n/4}-size circuit fails to compute h′ on ≥ 1/2 − 1/2^{n/4}
> fraction of all inputs of length n. Further assume that there are
> p-time functions h and f such that S¹₂ proves that for each integer n
> and each fixed-polynomial size circuit C, f(C) either outputs a
> poly(n)-size circuit B solving SAT, or C fails to invert h with
> significant probability over a uniformly random input to h. Then, if
> EF + tt(h′, 2^{n/4}, 1/2 − 1/2^{n/4}) is not p-bounded, we have that
> SAT ∉ P/poly. »

Preuve via **Lemme 2** (« Formalized witnessing of NP ⊄ P/poly from
OWF & hardness of E »), formalisé dans S¹₂ + dWPHP(PV) (= APC₁ de
Jeřábek) : OWF + E dure ⟹ témoin d'erreur par générateur de
Nisan-Wigderson (formalisation de [Pich 2015, Müller-Pich 2019]).

**Théorème 12** (= Th. 6 informel ; Th. 9/5 arXiv) — apprentissage
depuis ¬∃OWF (la route de l'abstract) :

> « Let k ≥ 1 be an arbitrary constant. Assume that there is h′ ∈ E
> such that for each sufficiently big n, each 2^{n/4}-size circuit
> fails to compute h′ on ≥ 1/2 − 1/2^{n/4} fraction of all inputs of
> length n. Further assume that there are p-time functions h and f such
> that S¹₂ proves that for all integers n and fixed-polynomial size
> circuits C, either f(C) outputs an efficient circuit B that weakly
> learns Boolean circuits with membership queries over the uniform
> distribution, or C fails to invert h with significant probability.
> Then the existence of a function g_n : {0,1}ⁿ → {0,1} that is
> average-case hard for polynomial-size circuits and such that
> EF + tt(h′, 2^{n/4}, 1/2 − 1/2^{n/4}) does not have a poly-size proof
> of the hardness of g_n (represented by truth table formulas) implies
> that SAT_n ∉ Circuit[n^k]. »

Le formel (ECCC p. 30) précise : pas de preuves de taille **2^{an}** de
tt(g_n, n^t) — polynomial en la taille 2^{O(n)} de la formule. Sous la
condition I, EF + tt(h′,·,·) redevient EF : « if there is a p-time
function f′ and constant n₀ such that S¹₂ proves that for each n ≥ n₀,
f′(1^{2ⁿ}) outputs the truth-table of a function h′ with n inputs which
is hard on average for 2^{n/4}-size circuits, then EF and
EF + tt(h′, 2^{n/4}, 1/2 − 1/2^{n/4}) are p-equivalent. »

**Théorèmes 1 + 8, Corollaire 2 — logarithme discret (équivalence)** :
sous « f ∈ E requiring circuit size 2^{Ω(n)} on average », il existe un
système fort Q (simulant EF) et des familles F_{k,n} telles que « the
Discrete Logarithm problem for multiplicative groups Z×_q of integers
modulo a prime q ∈ (2^{n−1}, 2ⁿ] does not have polynomial size circuits
iff for each k ∈ N the sequence of (sets of) formulas {F_{k,n}}_n does
not have polynomial size Q-proofs » ; équivalence **inconditionnelle**
pour un système non-uniforme concret (Th. 1(2)). Mécanisme :
auto-réductibilité aléatoire du DL + dérandomisation NW. Réserve des
auteurs : « some formulas in sequences F_k are not tautologies […] this
seems unavoidable in the context of strong proof systems, since
formulas that we know to be tautologies also tend to have short proofs
in strong proof systems ».

**Affaiblissements (§1.3)** : S¹₂ remplaçable par toute T ⊇ S¹₂ ; la
*prouvabilité* S¹₂ des réductions affaiblissable en simple *validité*,
au prix d'axiomes ajoutés à EF : « the S¹₂-provability in the
assumptions of our theorems can be weakened just to the validity of the
respective statements, if we use stronger systems than EF in their
conclusions. It also shows that most of the technicalities in the
present paper stem from making the presented approach work for EF. »
Et la condition I est « for free » si le but final est P ≠ NP : « if
all functions in E can be approximated by subexponential-size circuits,
it is not hard to show that P ≠ NP. »

## 6. La chaîne (format DISTANCE, ≤ 4 flèches)

Route principale (Théorème 12 + condition I) :

[Cond. I : S¹₂ ⊢ « h′ ∈ E dure en moyenne pour circuits 2^{n/4} »] ∧
[Cond. II : S¹₂ ⊢ « réduction p-time : casseur d'OWF → apprenant
uniforme à requêtes d'appartenance »] ∧ [borne EF : ∃ g_n dure dont les
tt-formules n'ont pas de preuves EF de taille 2^{an}]
→ (Th. 12 + p-équivalence sous I) SAT_n ∉ Circuit[n^k] i.o., ∀k
→ NP ⊄ P/poly
→ P ≠ NP.

Trois flèches, toutes **prouvées dans le papier** ; les entrées sont
ouvertes. **Maillon le plus faible : la condition II** — sa simple
validité équivaut moralement à éliminer Pessiland (« Morally, the
existence of such a reduction would rule out Pessiland out of
Impagliazzo's worlds »), question ouverte majeure de la cryptographie
avec barrières boîte-noire connues ; l'échappatoire revendiquée : « the
reductions we consider are white-box, and we only require provability
of the reduction. » **Deuxième entrée ouverte, indépendante** : la
borne EF sur tt-formules — précisément l'objet que leur FOCS 2019
(audité par A-012) déclare auto-référentiellement difficile ; le front
des bornes de preuves reste à AC⁰[p]-Frege, plusieurs étages sous EF.
**Plafond au-dessus de tout affaiblissement : Proposition 1.**

## 7. Réserves des auteurs (verbatim)

1. Pourquoi des conditions : « Since the NEXP vs P/poly problem seems
   out of reach of current lower bound techniques, it seems unlikely
   that we will be able to prove an unconditional connection from
   super-polynomial lower bounds for a propositional proof system to
   strong circuit lower bounds any time soon. »
2. Statut de la condition I — le double tranchant : « If the
   tt-formulas expressing subexponential lower bounds for E are hard
   for EF, then S¹₂ cannot prove the lower bounds either. On the other
   hand, it is not known how to prove hardness of tt(h, 2^{n/4}), for
   all h, for Frege, under any standard complexity-theoretic hardness
   assumption. Moreover, all major circuit lower bounds for weak
   circuit classes and explicit Boolean functions are known to be
   provable in S¹₂ […] It is thus perfectly possible that
   subexponential average-case circuit lower bounds for E are provable
   in a theory such as S¹₂. » — note : « This has not been verified for
   lower bounds obtained via the algorithmic method of Williams [54]. »
3. Verrou technique anticheckers (quantificateurs vs fonction) : le
   MinMax efficace n'est pas connu formalisable dans APC₁, et le
   témoignage KPT bloque le remplacement de f par des ∃ : « given ∀n,
   SAT_n ∈ Circuit[n^k], we could not directly obtain p-size EF-proofs
   of tautologies stating that one of the functions f₁,…,f_c generates
   a circuit solving SAT_n. This is because B and A^{SAT_n,n^k}_n
   generated by f₂ depend on y₁. » D'où les Open Problems (arXiv §1.2) :
   construire f telle que les w^k_n(f) aient des preuves EF p-size
   (⟹ toute borne EF superpolynomiale séparerait P de NP), et
   remplacer les fonctions par des quantificateurs.
4. Lecture d'ensemble : « Showing that statements like P ≠ NP follow
   from proof complexity lower bounds for concrete proof systems is
   considered so challenging that there have not been practically any
   conscious attempts to approach it. Our results show that the
   significant efforts that have been made in order to address some of
   the central problems in cryptography and learning theory are, in
   fact, aiming to establish precisely that. This can be interpreted as
   an evidence for the hardness of resolving the relevant problems in
   cryptography and learning theory, but alternatively as a step toward
   realizing the Cook-Reckhow program successfully. »

## 8. La convergence ligne 13, telle que les auteurs l'écrivent

> « Recently, there have been various approaches proposed to rule out
> Heuristica and Pessiland (see, for example, [27, 52, 43]) by studying
> the complexity of problems about compression, such as the Minimum
> Circuit Size Problem (MCSP) and the problem of computing time-bounded
> Kolmogorov complexity. Our results have implications for the
> feasibility of such efforts - provable collapses of Impagliazzo's
> worlds would imply a new and surprising link between proof complexity
> and circuit complexity. »

([27] = Hirahara FOCS 2018 ; [52] = Santhanam ITCS 2020 ; [43] =
Liu-Pass CCC 2022 — bibliographie lue.) Pont automatisabilité (leur
ICALP 2022) : « [47, Lemma 4] shows that, assuming E is S¹₂-provably
hard as in Theorem 6, learning algorithms for small circuits can be
S¹₂-provably constructed from circuits automating EF on tt-formulas. »
La convergence annoncée par la cellule 15 est **textuellement fondée** :
OWF (Th. 11), anticheckers (Th. 10), apprentissage (Th. 12),
automatisabilité (via ICALP 2022).

## 9. État 2024-2026 (la voie est ACTIVE)

1. **Publication J. ACM 2026** (73(2), 12:1-12:27, DOI 10.1145/3801091).
2. **Arteche-Khaniki-Pich-Santhanam, ICALP 2024** (LIPIcs 297, 12:1-20,
   DOI 10.4230/LIPIcs.ICALP.2024.12 ; texte Dagstuhl LU) — Théorème 1 :
   « Suppose there is a Boolean function h ∈ NE ∩ coNE that is hard on
   average for subexponential-size circuits. If the Cook-Reckhow proof
   system iEF^tt(h) is not polynomially bounded, then #P ⊄ FP/poly. »
   Position déclarée : « Our result improves that of Pich and Santhanam
   by completely dropping their second assumption […] The price to pay
   […] 1. we need to replace EF by the seemingly stronger Implicit
   Extended Frege system (iEF) […] 2. we can conclude only #P ⊄ FP/poly
   from iEF lower bounds, instead of NP ⊄ P/poly. » Et : « one cannot
   make big improvements to this result without hitting the
   Pich-Santhanam barrier ». Mécanisme : robustesse du protocole
   **sum-check** (LFKN) formalisée dans iEF — de l'arithmétisation
   importée en complexité des preuves (croisement lignes 3/15).
3. **Khaniki-Pich-Sokolov, « Efficient Adversaries », CCC 2026**
   (LIPIcs, 8:1-8:32, DOI 10.4230/LIPIcs.CCC.2026.8 ; abstract Dagstuhl
   LU) : les bornes majeures connues « are constructive in the sense
   that they yield efficient algorithms computing winning strategies of
   adversaries » — et si (a) une borne EF *constructive* existe pour
   les formules de bornes succinctes de SAT et (b) EF prouve la
   correction d'anticheckers, alors la paire canonique d'EF se sépare :
   les conditions de PS23 retournées en test de constructivité
   (barrière interne).
4. Adjacents : Khaniki FOCS 2024 (« Jump Operators, Interactive Proofs
   and Proof Complexity Generators », DOI 10.1109/FOCS61266.2024.00044)
   [NON OUVERT — paywall IEEE, pas de version libre trouvée] ;
   Arteche-Atserias-de Rezende-Khaniki, « The Proof Analysis Problem »,
   FOCS 2025 (arXiv:2506.16956, abstract lu) : PAP pour EF NP-complet,
   « every proof system simulating EF is (weakly) automatable if and
   only if it is (weakly) automatable on formulas stating Resolution
   lower bounds ». Versions journal amont : Pich cc 33(2) 2024,
   cc 34(1) 2025.

## 10. Réserves d'audit

1. **J. ACM 2026 non ouvert** (403 + mur anti-bot, pas d'OA) : la
   coïncidence du texte de référence avec les versions 2023 n'est PAS
   certifiée ; identification par dblp + page auteur seulement. À la
   différence du cas TR24-074 (leçon A-017), la version *actuelle* de
   référence est précisément celle qui n'a pas pu être ouverte — toute
   citation doit viser TR23-199/arXiv v1 et le dire.
2. Khaniki FOCS 2024 et la colonne SIGACT (Oliveira) cités comme
   existants uniquement — aucun contenu ne leur est attribué.
3. La page Oxford de Pich étiquette l'automatability paper « JML'24 » ;
   dblp ne montre aucune version JML — discordance non résolue : ne
   citer que ICALP 2022.
4. Théorèmes formels ECCC 10-12 / arXiv 7-9 réputés identiques sur
   têtes d'énoncés comparées (Th. 8 arXiv ≡ Th. 11 ECCC vérifié ligne à
   ligne) ; collation mot à mot des 29+35 pages non faite.
5. Extraction pypdf : indices restaurés à la main dans les citations
   (convention déclarée en tête) ; formules longues vérifiables dans
   les `_texte.txt`.
6. Historique de révisions vérifié à l'ouverture ET à la clôture
   (2026-08-08) : ECCC sans révision, arXiv v1 unique.
