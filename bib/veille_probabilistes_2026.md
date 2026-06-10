# Veille — méthodes probabilistes récentes et P vs NP (2026-06-11)

> Audit déclenché par la question utilisateur : « nouveaux algorithmes de
> probabilité conditionnelle et méthodes récentes — utilisables pour
> P vs NP ? ». Quatre fronts examinés ; verdict du Réfuteur par front.

## 1. Polynômes toriques (BHLR 2019 + Krishan 2024) — ★ LA PÉPITE

- **Sources** : [Bhrushundi-Hosseini-Lovett-Rao, ITCS 2019,
  arXiv:1804.08176](https://arxiv.org/abs/1804.08176) ;
  [Krishan, ECCC TR24-074 (2024)](https://eccc.weizmann.ac.il/report/2024/074/).
- **L'idée** : approximer les fonctions booléennes par des polynômes
  *réels modulo 1* (sur le tore) — modèle qui **généralise** les
  polynômes mod m. BHLR réduisent `MAJ ∉ ACC⁰` (le mur de 1987 !) à la
  non-existence de polynômes toriques de bas degré approximant MAJ.
- **État** : BHLR prouvent que MAJ n'est PAS approximable par des
  polynômes toriques **symétriques** de bas degré ; le cas **général est
  ouvert**. Krishan 2024 : réduction à la faisabilité d'une **famille
  infinie de programmes linéaires** + première borne asymétrique
  (AND exige degré Ω(log n) pour erreur 1/2n).
- **Verdict** : alignement frappant avec notre fil F-011 — (i) c'est
  exactement le « modèle intermédiaire » que notre conclusion d'étape 19
  appelait ; (ii) le motif *symétrique prouvé / général ouvert* est
  précisément celui de nos étapes 17-19 (et nous savons par expérience
  que l'asymétrie peut tuer les bornes symétriques — notre Théorème K) ;
  (iii) la formulation **LP** de 2024 est notre outillage natif (HiGHS,
  duaux exacts, petits n). **Barrières** : modèle concret (relativisation
  N/A) ; borne visant UNE fonction explicite (pas « naturelle » a
  priori) ; la motivation publiée du modèle est justement de contourner
  les barrières connues. → **Tâche exécutable : V-001** (mesurer les
  degrés toriques de MAJ aux petits n, symétrique vs général, LP exacts
  + certificats duaux ; répliquer la borne symétrique BHLR
  numériquement).

## 2. Méta-complexité (Hirahara, Ilango, Ren… 2018-2023) — programme majeur, ligne MANQUANTE de l'Atlas

- **Sources** : [Hirahara, Bulletin EATCS — « Meta-Computational
  Average-Case Complexity »](http://bulletin.eatcs.org/index.php/beatcs/article/view/688) ;
  [NP-Hardness of Approximating Meta-Complexity, STOC 2023](https://hanlin-ren.github.io/files/pdf/stoc23_NP-hardness-of-meta-complexity.pdf) ;
  [Capturing One-Way Functions via NP-Hardness of Meta-Complexity, STOC 2023](https://dl.acm.org/doi/10.1145/3564246.3585130) ;
  [Ilango-Ren-Santhanam, Robustness of Average-Case Meta-Complexity, STOC 2022](https://hanlin-ren.github.io/files/pdf/stoc22_robustness.pdf).
- **L'idée** : étudier la complexité des problèmes *sur* la complexité
  (MCSP, Kolmogorov borné en temps) ; réductions pire-cas ↔ cas-moyen
  **non-boîte-noire** pour NP (contournant les théorèmes d'impossibilité
  boîte-noire) ; caractérisation des fonctions à sens unique par la
  dureté de méta-complexité.
- **Verdict** : le programme probabiliste le plus actif vers
  l'exclusion de Heuristica (mondes d'Impagliazzo) — chemin *indirect*
  vers P ≠ NP mais structurant. Très lié aux preuves naturelles (MCSP est
  LE problème adjacent à Razborov-Rudich). **Pas directement exécutable
  petit-n**, mais c'est une **famille d'approches absente de notre
  Atlas** (aucune des 12 lignes). → **Tâche : A-009** (audit + nouvelle
  ligne Atlas « méta-complexité », barrières à documenter — le
  non-boîte-noire esquive certaines limites, statut vis-à-vis des
  3 barrières à instruire sur textes).

## 3. Méthode des probabilités conditionnelles & dérandomisation récente

- **Sources** : [méthode classique (Wikipedia, Erdős-Selfridge →
  Raghavan)](https://en.wikipedia.org/wiki/Method_of_conditional_probabilities) ;
  [dérandomisation parallèle pour coloriage, arXiv:2302.04378 (2024)](https://arxiv.org/pdf/2302.04378) ;
  [formalisation Isabelle/AFP (2024)](https://isa-afp.org/entries/Derandomization_Conditional_Expectations.html) ;
  [« Free Lunch Derandomization », CCC 2025](https://drops.dagstuhl.de/storage/00lipics/lipics-vol339-ccc2025/LIPIcs.CCC.2025.31/LIPIcs.CCC.2025.31.pdf).
- **L'idée** : convertir les preuves probabilistes en algorithmes
  déterministes (espérances conditionnelles, estimateurs pessimistes).
  Récent : versions parallèles/MPC (2024), « free lunch » (dérandomisation
  quasi sans surcoût sous hypothèses nécessaires/OWF, CCC 2025).
- **Verdict** : axe **BPP vs P**, pas NP vs P. Le lien profond
  (hardness vs randomness : des bornes de circuits ⟹ dérandomisation,
  Impagliazzo-Wigderson) fait de ce front un *consommateur* de bornes
  inférieures, pas un producteur. Aucune des nouveautés 2024-25 ne
  franchit ni n'attaque les trois barrières pour P vs NP. → **Pas de
  tâche** ; contexte consigné.

## 4. Overlap Gap Property (Gamarnik et al.)

- **Sources** : [perspective PNAS 2021](https://www.pnas.org/doi/10.1073/pnas.2108492118) ;
  [« Some easy optimization problems have the overlap-gap property », arXiv:2411.01836 (2024)](https://arxiv.org/pdf/2411.01836).
- **L'idée** : barrière *topologique* (déconnexion des solutions
  quasi-optimales) prouvant des bornes **inconditionnelles** — mais
  seulement contre des classes restreintes d'algorithmes (stables/
  Lipschitz, polynômes de bas degré) et sur des instances **aléatoires**.
- **Verdict** : cas-moyen ≠ pire-cas — la littérature elle-même note que
  la NP-dureté formelle manque ; et 2024 montre que des problèmes
  FACILES ont l'OGP (la propriété n'implique pas la dureté en général).
  Piège classique n° 2 de notre §2 (moyenne ≠ pire cas), désormais
  documenté. → **Pas de tâche** ; impasse consignée.

## Synthèse

| Front | P vs NP ? | Action dépôt |
|---|---|---|
| Polynômes toriques | chemin direct vers MAJ ∉ ACC⁰ (mur 1987), LP-isable | **V-001** (exécutable) |
| Méta-complexité | programme indirect majeur, ligne Atlas manquante | **A-009** (audit) |
| Probas conditionnelles / dérandomisation | axe BPP=P, pas NP | non |
| OGP | cas-moyen, classes restreintes | non (impasse documentée) |
