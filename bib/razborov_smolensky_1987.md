# A-004 : Audit — Razborov 1987 & Smolensky 1987 (méthode polynomiale modulaire)

> Tâche type A. Exécutée le 2026-06-09.
> **Sourçage** : les originaux (Razborov, Mat. Zametki 1987, en russe ;
> Smolensky, STOC 1987, paywall ACM) n'ont pas été lus directement. L'audit
> repose sur O. Goldreich, *« On teaching the approximation method for
> circuit lower bounds »* (15 mars 2023,
> [PDF Weizmann](https://www.wisdom.weizmann.ac.il/~oded/PDF/mod-mod.pdf),
> **21 pages greppées en texte intégral**) — exposition dédiée précisément à
> ces deux papiers, avec énoncés et preuves complètes. Citations « > » =
> Goldreich.

## 1. Références canoniques

- A. A. Razborov, *« Lower bounds on the size of bounded depth circuits over
  a complete basis with logical addition »* (en russe), Matematicheskie
  Zametki, vol. 41, no. 4, 1987, pp. 598-607. Traduction anglaise :
  Mathematical Notes of the Academy of Sciences of the USSR, 41(4):333-338,
  1987.
- R. Smolensky, *« Algebraic methods in the theory of lower bounds for
  Boolean circuit complexity »*, 19th STOC, 1987, pp. 77-82.
  [doi:10.1145/28395.28404](https://doi.org/10.1145/28395.28404).
- Division du travail (telle que décrite par Goldreich) : Razborov introduit
  la **méthode d'approximation** sur GF(p) et l'applique à MAJORITY avec
  portes MOD_2 ; Smolensky l'**applique/généralise** à MOD_q vs AC⁰[p] pour
  premiers p ≠ q.

## 2. Théorème principal — énoncé exact (forme Goldreich, Theorem 1)

> « For any prime p ≥ 2, the following holds.
> 1. Computing the majority of n bits by a depth d circuit with unbounded
> fan-in AND, OR, NOT, and MOD_p gates requires size exp(Ω(n^{1/2d})).
> 2. For any prime q different from p, computing the MOD_q of n bits by a
> depth d circuit with unbounded fan-in AND, OR, NOT, and MOD_p gates
> requires size exp(Ω(n^{1/2d})). »

> « In particular, Part 1 (with p = 2) implies that AC0[2] cannot compute
> Majority, whereas Part 2 (with p = 3 and q = 2) implies that AC0[3] (let
> alone AC0 itself) cannot compute Parity. »

## 3. Hypothèses non-triviales

1. **p premier** — c'est LA restriction structurante. La méthode repose sur
   le fait que GF(p) est un corps (les portes MOD_p s'arithmétisent
   exactement en caractéristique p, et l'argument de comptage de Smolensky
   utilise la structure de corps).
2. **q premier ≠ p** pour la partie 2 (cas q composé dérivable pour ses
   facteurs premiers).
3. Profondeur d constante (l'exposant n^{1/2d} se dégrade avec d).

## 4. Outils techniques — la méthode en 2 pas (verbatim)

> « Step 1: Proving that the computation of AC0[p] circuits can be well
> approximated by polynomials of low degree over the finite field of p
> elements […]
> Step 2: Proving that the target functions (i.e., n-wise Majority and
> n-wise MOD_q, for q ≠ p) cannot be well approximated by low degree
> polynomials over GF(p). »

Pas 1 = polynômes probabilistes bas degré (OR/AND approximés par produits
randomisés à la Razborov) ; Pas 2 = argument de comptage/dimension de
Smolensky (toute fonction de {0,1}^n s'exprime sur l'ensemble des points où
l'approximant de MOD_q est correct avec un degré trop bas — contradiction
dimensionnelle).

## 5. Ce que ces papiers NE PROUVENT PAS

1. **Rien pour les modules composés.** Verbatim Goldreich :
   > « In contrast, we do not know a proof of the equally intuitive
   > conjecture that AC0[6] cannot compute Majority. »
   MOD_6 = MOD_2 × MOD_3 brise la structure de corps. **C'est la frontière
   restée ouverte de 1987 à 2011** (Williams contourne en passant par
   l'algorithmique au lieu de l'approximation), et ACC⁰ vs MAJORITY reste
   ouvert en 2026.
2. **Rien pour TC⁰** : MAJORITY est précisément la fonction *dure* ici —
   dès qu'on l'ajoute comme porte, la méthode n'a plus de cible.
3. **Borne se dégradant en profondeur** : exp(n^{1/2d}) — pas de borne
   super-polynomiale uniforme en d croissant.
4. **(Contexte dépôt, à confirmer par A-007)** : la propriété « non
   approximable par polynômes bas degré sur F_p » est constructive et
   large — c'est l'exemple canonique de preuve *naturelle* au sens
   Razborov-Rudich 1997. La méthode est donc soumise à la barrière RR si
   on tente de la pousser vers des classes contenant des PRF.

## 6. Lien à la bibliographie §7 du cahier

Cité au §7.2 (lignée AC⁰ → ACC⁰). L'audit ajoute la référence Goldreich 2023
comme exposition de référence (à intégrer au §7.2 si souhaité), et précise la
division Razborov (méthode + MAJ/MOD_2) / Smolensky (MOD_q vs AC⁰[p]).

## 7. Lien aux tours et tâches du dépôt

- **Tour 16 (MOD_p, DNF profondeur 2)** : le cahier note correctement que
  Tour 16 traite « seulement le cas profondeur 2 par application
  combinatoire de L13 » — la vraie lignée Razborov-Smolensky (profondeur
  arbitraire) est ce qui est audité ici.
- **A-001/A-002** : la chaîne des représentations — Razborov-Smolensky
  (approximation probabiliste, p premier) → Beigel-Tarui (exacte,
  m composé, SYM+) → Williams (exploitation algorithmique). La forme
  « Theorem 1 » de Buss (A-002) est explicitement signalée comme équivalente
  à la caractérisation Razborov-Smolensky.
- **Cellule Atlas « méthode polynomiale modulaire × barrières »** :
  - vs composite/ACC⁰ : fermée par la limitation 1 (structure de corps
    requise) — témoin : AC⁰[6] vs MAJORITY ouvert depuis 1987.
  - vs RR : exposée (preuve naturelle canonique) — à finaliser avec A-007.
  - vs Tardos : sans objet (la méthode n'est pas monotone).

## Limitations de l'audit

- Originaux non lus (russe / paywall) ; Goldreich 2023 est une exposition
  complète et récente mais ses choix de présentation (paramètres exacts des
  lemmes 2-3) peuvent différer des constantes originales.
- Les preuves des lemmes 2 et 3 (approximation et comptage) n'ont pas été
  extraites en détail — disponibles dans le PDF source §2.2.
