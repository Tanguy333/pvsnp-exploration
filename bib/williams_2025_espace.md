# Audit A-020 — Williams, « Simulating Time With Square-Root Space » (STOC 2025)

Tâche : A-020 (2026-08-08). Type A (audit sur texte). Rattachement :
Atlas ligne 1 (diagonalisation / simulation) — refonder sur pièce le
verrou réécrit par A-017 (qui s'appuyait sur la veille). Audit mené par
agent (règles du dépôt), consigné et relu par la session.

**Documents OUVERTS intégralement** : arXiv:2502.17779 v1 (PDF +
contrôle HTML ; extraction `bib/pdf/williams_2025_espace_arxiv_texte.txt`) ;
ECCC TR25-017 ; Cook-Mertz ECCC TR23-174
(`bib/pdf/cook_mertz_tr23174_texte.txt`) ; [HCC+93] copie auteur UMBC
(`bib/pdf/hcc93_relativization_texte.txt`). **NON OUVERTS** : PDF STOC
(ACM, 403) et J. ACM 73(3) 2026 (identification Crossref/dblp seule).

## 1. Identification et révisions

| Version | Identifiant | Date | Historique |
|---|---|---|---|
| ECCC | TR25-017, « Simulating Time **in** Square-Root Space » | 2025-02-24 | aucune révision |
| arXiv | 2502.17779, « Simulating Time **With** Square-Root Space » | v1 2025-02-25 | **v1 unique** — vérifié à l'ouverture ET à la clôture (2026-08-08) |
| STOC 2025 | DOI 10.1145/3717823.3718225, p. 13-23 | 2025-06-15 | [NON OUVERT] ; **Best Paper Award** (page SIGACT, sous le titre « Simulating Time in (Nearly) Square-Root Space » — 3e variante) |
| J. ACM | DOI 10.1145/3798104, 73(3), art. 16, 16:1-16:25 | 2026-06-16 | [identification seule] |

**Écart textuel consigné** : la parenthèse « (see for example
[HCC+93]) » du passage-barrière figure dans **arXiv v1** (ouvert,
citable) mais PAS dans ECCC TR25-017 — la note d'A-017 qui l'attribuait
à la seule page personnelle de l'auteur est corrigée : la citation
s'adosse à l'arXiv.

## 2. Théorème et modèle (verbatim, arXiv v1)

> « **Theorem 1.1.** For every function t(n) ≥ n,
> TIME[t(n)] ⊆ SPACE[√(t(n) log t(n))]. »

Modèle : machines de Turing **multiruban unidimensionnelles**
(« let TIME[t(n)] be the class of decision problems decided by
O(t(n))-time multitape Turing machines ») ; t(n) **sans hypothèse de
constructibilité** (essai incrémental t = n, n+1, …, astuce [HPV75]) ;
robustesse côté espace via l'« invariance thesis » [SvEB88, vEB90].
Preuve : blocs « block-respecting » [HPV75] (la preuve complète se
passe de la simulation oblivious de Hennie-Stearns, utilisée seulement
au warm-up Th. 3.1). Extension dimension d :

> « **Theorem 1.5.** Every decision problem solvable by a t(n)-time
> d-dimensional multitape Turing machine can be decided in
> O((t(n) log t(n))^{1−1/(d+1)}) space. »

**Remark 1.6** : pas d'extension connue aux RAM arbitraires
(« the indegree of the resulting computation graph … is so high ») ;
modèles à accès oblivious : oui, à facteur poly(log t) près.

## 3. L'ingrédient Cook-Mertz et son rôle

> « **Theorem 2.2 ([CM24], Theorem 7).** TREE EVALUATION on trees of
> bit-length b, maximum height h, and fan-in at most d, can be
> computed in O(d·b + h log(d·b)) space. »

Source ouverte : ECCC TR23-174 (Cook & Mertz, aucune révision ; le
résultat y est le Theorem 15, notation k = 2^b ; la numérotation
« Theorem 7 » est celle de la version STOC 2024, paywallée — cohérence
vérifiée, aucune contradiction). Branchement : la computation découpée
en blocs de b pas/bits → instance de Tree Evaluation implicite de
hauteur h = Θ(t/b), arité O(1), valeurs de b bits ; optimisation
verbatim : « setting d·b = h log(d·b) = Θ(t·log(d·b)/b) […] we find
b = Θ(√(t log t)) ». Contenu algébrique (Appendix A, suivant
l'exposition de Goldreich TR24-109) : extensions multilinéaires puis
bas-degré sur un corps de **caractéristique 2**, interpolation aux
puissances d'une racine de l'unité, registres réutilisés (stockage
« "catalytic" or "global" »).

**Avertissement de vocabulaire** : « height compression » n'apparaît
NULLE PART chez Williams (0 occurrence de « compress ») — c'est le
vocabulaire du préprint RETIRÉ de Nye (§7) ; ne pas l'employer.

## 4. Corollaires (verbatim)

- > « **Corollary 1.2.** For space constructible s(n) ≥ n, and all
  > ε > 0, SPACE[s(n)] ⊄ TIME[s(n)^{2−ε}]. »
  — par diagonalisation ; « the first generic polynomial separation of
  time and space in a robust computational model » (forme fine : des
  problèmes en espace O(n) exigent temps n²/log^c n).
- **Corollary 1.3** : le problème d'arrêt borné en espace k exige
  n^{2−ε} ; langages contextuels : « need essentially n² time ».
- **Corollary 1.4** : circuits taille s → branching programs
  2^{k√s·log^k s} — une SIMULATION (borne supérieure) ; **le papier
  n'énonce aucune borne inférieure de circuits**.
- **Corollary 3.6** (conditionnel) : « If TREE EVALUATION is in
  LOGSPACE, then TIME[t(n)] ⊆ SPACE[√(t(n))]. »

## 5. Relevé barrières (occurrence par occurrence)

**Relativisation** — le résultat est déclaré **non-relativisant par
l'auteur**, sourcé [HCC+93] :

> « While Theorem 1.1 and Theorem 3.1 are non-relativizing (see for
> example [HCC+93]), the simulations do permit a restricted form of
> relativization, as do all prior simulations of time in smaller
> space. »

Le monde-oracle est dans [HCC+93] (OUVERT) : « **Theorem 6.** There
exists an oracle A such that for all f(n),
TIME^A[f(n)] = SPACE^A[f(n)] » — avec « the theorem itself does not
relativize, so any proof of the theorem must use non-relativizing
techniques » (énoncé pour HPV75 ; relativement à cet A, l'inclusion de
Williams contredirait la hiérarchie espace — inférence d'audit,
consignée comme telle). **La relativisation RESTREINTE est un théorème
du papier** :

> « **Theorem 5.1.** For every oracle A and t(n) ≥ n,
> TIME-LENGTH^A[t(n), √(t(n) log t(n))] is contained in
> SPACE-LENGTH^A[√(t(n) log t(n)), √(t(n) log t(n))]. »

avec le mécanisme : « **the Cook-Mertz procedure treats the evaluation
functions as black boxes**. Thus each evaluation function F_{h,i} can
simply call the oracle A as needed. »

**PRÉCISION D'ATTRIBUTION (corrige le raccourci d'A-017)** : le texte
n'attribue PAS la non-relativisation à l'algèbre de Cook-Mertz — c'est
l'inverse : le caractère boîte-noire de Cook-Mertz PERMET la
relativisation restreinte ; la non-relativisation est une propriété du
théorème lui-même (« as do ALL prior simulations », HPV75 compris, qui
n'a aucune algèbre). Question-barrière posée par l'auteur :

> « Is there a barrier to improving such (restricted) relativizing
> results to obtain P ≠ PSPACE? This seems related to the fact that
> Cai and Watanabe [CW06] were unable to collapse PSPACE to P with
> "random access to advice" (length-restricted access to oracles). »

Baker-Gill-Solovay : **0 occurrence** (la non-relativisation est
sourcée à [HCC+93] seul).

**Algébrisation : [NON TROUVÉ]** — « algebriz- » 0, « arithmeti- » 0,
Aaronson-Wigderson absent de la bibliographie. Fait brut : la
machinerie interne EST de l'arithmétisation (extensions bas-degré,
interpolation) mais c'est une INCLUSION algorithmique, pas une borne
inférieure du type visé par AW08 — le texte n'en dit rien.

**Preuves naturelles : [NON TROUVÉ]** — « natural proof » 0, Rudich 0 ;
l'unique Razborov est [Raz91] (survey branching programs). Attendu
(résultat uniforme).

**Barrières internes discutées par le papier** : le pseudo-théorème
rétrospectif (« Unless the 50-year-old [HPV75] simulation
TIME[t] ⊆ SPACE[t/log t] can be improved, TREE EVALUATION instances
[…] cannot be solved in o(h·b/log(h·b)) space ») et la question NNJAG
(« NNJAG is fundamentally a node-pebbling model, and the Cook-Mertz
procedure definitely breaks space lower bounds for pebbling DAGs and
trees »).

## 6. Distance et problèmes ouverts (verbatim)

Le papier revendique « **a little progress on the P versus PSPACE
problem** » — **« NP » n'apparaît nulle part dans le corps du texte**
(aucun lien à P vs NP affirmé ; n'en fabriquer aucun). Pont
conditionnel : « if Theorem 1.1 could be extended to show for all
ε > 0 that every time-t(n) Turing machine can be simulated in
O(t(n)^ε) space, then P ≠ PSPACE would follow ». Le mur : la
**récursion bloquée** — « we cannot directly apply recursion to time
blocks, because in the Cook-Mertz procedure, the task at each function
evaluation is not just to simulate for b steps, but to compute a
low-degree extension of the function » (coût 2^Θ(b), lié à SETH via
les extensions multilinéaires de CNF). Six questions ouvertes en §5,
dont : « Can the simulation be applied recursively, to show that
TIME[t] ⊆ SPACE[t^ε] for all ε > 0? Note that a yes-answer would imply
P ≠ PSPACE. » et « Is there a barrier to further progress? »

## 7. État 2025-2026

- **Shalunov, CCC 2026** (arXiv:2504.20950 v2) : CIRCUIT EVALUATION en
  O(√(s log s)) (réduction directe circuit → TreeEval) ; en retour une
  simulation temps « slightly weakened » O(√t·log t).
- **Henzinger-Pyne-Ragavan** (arXiv:2602.14320 / ECCC TR26-022,
  2026-02) : TreeEval CATALYTIQUE en espace libre O(log n) ; « opens a
  new line of attack on putting TreeEval in logspace, and immediately
  implies an improved simulation of time by catalytic space, by the
  reduction of Williams (STOC 2025). »
- **DEUX PRÉPRINTS RETIRÉS — ne citer nulle part comme résultats** :
  Nye, arXiv:2508.14831 (« TIME[t] ⊆ SPACE[O(√t)] via Tree Height
  Compression », v4 retirée 2026-01-01 : « The proof of the main
  theorem is incorrect ») ; Asadi-Cleve, arXiv:2604.02606 (TreeEval
  catalytique quasi-log, v2 retirée 2026-04-07 : erreur de degré).
  **Au 2026-08-08 : ni le facteur √log t ni TreeEval ∈ L ne sont
  tombés ; O(√(t log t)) reste la meilleure borne publiée**, version
  J. ACM 73(3) juin 2026.
- Lignée catalytique très active (identifications dblp) : Bipartite
  Matching in Catalytic Logspace (FOCS 2025), Collapsing Catalytic
  Classes (FOCS 2025), Structure of Catalytic Space (STOC 2025), etc.
- Réponse à la question-barrière de Williams : **[NON TROUVÉ]** — la
  question reste ouverte.

## 8. Réserves d'audit

1. Versions ACM (STOC, J. ACM) non ouvertes — l'audit repose sur
   arXiv v1 + ECCC, intégraux et concordants (à la parenthèse
   [HCC+93] près, consignée §1).
2. Trois variantes de titre en circulation (« With » / « in » /
   « in (Nearly) ») — citer selon la version visée.
3. [CM24, Theorem 7] : numérotation STOC 2024 paywallée, vérifiée par
   TR23-174 (Theorem 15) + la restitution de Williams — cohérents.
4. Verbatims contre-vérifiés sur le HTML arXiv pour les phrases
   porteuses ; l'inférence « monde-oracle ⟹ l'inclusion de Williams y
   est fausse » est une inférence d'audit (via hiérarchie espace
   relativisante), [HCC+93] ne l'énonçant que pour HPV75.
5. Audit en lecture unique (agent + relecture de session).
