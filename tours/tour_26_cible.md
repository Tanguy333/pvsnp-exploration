# TOUR 26 — Dossier de cible pour le Proposeur (ouvert le 2026-07-23)

> Première réouverture de la boucle adverse depuis le Tour 25
> (conditions CLAUDE.md §8 satisfaites : la cible est née d'une
> cellule de l'Atlas — ligne 7, via le fil F-012..022 — elle est
> précise, et vérifiable par calcul). Ce dossier est AUTONOME : à
> donner tel quel au Proposeur. Le Réfuteur (Claude) attend la
> proposition collée par l'utilisateur.

## 1. LA CIBLE (unique, non négociable)

**Prouver une borne inférieure super-additive pour le poids SYM∘AND
d'une composition à porte de comptage :**

> Exhiber une famille explicite de blocs monotones g (NON-AND, sur
> b ≥ 2 variables) et prouver que
> **W(MAJ_k(g, …, g)) ≥ ω(k) quand k → ∞**, idéalement ≥ c·k·W(g)
> avec c > 1, ou toute croissance strictement super-linéaire en k.

OU BIEN (tout aussi recevable) :

> **Réfuter** : construire une famille de séparateurs prouvant
> W(MAJ_k(g^k)) = O(k) pour tout bloc monotone g fixé — ce qui
> tuerait l'écho jouet du mur TC⁰ et serait une découverte.

## 2. LE MODÈLE (définition complète — aucune variante n'est acceptée)

Pour f : {0,1}ⁿ → {0,1} : W(f) = min Σ_S a_S sur les polynômes
p(z) = Σ_S a_S·m_S(z), coefficients ENTIERS a_S ≥ 0 sur les monômes
positifs non vides (m_S = ∧_{i∈S} z_i), tels que les ensembles de
valeurs {p(z) : f(z)=1} et {p(z) : f(z)=0} soient DISJOINTS.
MAJ_k(g^k) = [au moins ⌈k/2⌉ des k blocs disjoints satisfont g].

## 3. CE QUI EST DÉJÀ PROUVÉ (ne pas relabourer — réfutation immédiate sinon)

- **T1 (tranche)** : W(f) ≥ W(g_A) + W(g_B) si f(z_A,0) = g_A,
  f(0,z_B) = g_B. Donne seulement O(k)·W(g) par tranches — INSUFFISANT
  pour la cible.
- **T2 (comptage)** : un p positif {0,1}-valué est un monôme unique —
  seul AND a un indicateur exact (c'est POURQUOI g doit être non-AND).
- **T3 (alternance)** : W(f) ≥ alt(f) (= decrease de Markov 1957).
  alt = 1 pour f monotone — INUTILE ici, ne pas le proposer.
- **T4 (fenêtre ANF)** : sparsité ANF des seuils escalier = 2^{k−1}−1.
- **Couvert unilatéral** : W(f) ≤ #uns minimaux (toujours) ; ÉGALITÉ
  mesurée sur MAJ₃(OR2³) = 12, AND(OR2²) = 4, OR(THR4²) = 6.
- **LP de couverture** : donne 3 sur MAJ₃(OR2³) = 12 — facteur ×4
  perdu ; l'argument devra faire STRICTEMENT mieux.

## 4. CE QUI EST DÉJÀ RÉFUTÉ (proposer une variante = faille immédiate)

- « W = couvert unilatéral pour toute composition monotone » : FAUX,
  3 contre-exemples — MAJ₅ (blocs singletons, comptage symétrique),
  MAJ₅(AND2⁵) ≤ 5 < 10 (indicateurs AND), et **AND2(MAJ3²) = 6 < 9**
  (mécanisme HYBRIDE : q = C(s,2), séparateur unilatéral à valeurs
  IMPAIRES {1,3} — la somme de deux impairs est paire).
- « Un invariant unique caractérise W » : FAUX — W = min d'un zoo ≥ 4
  mécanismes (couvert, parité/ANF, positionnel, comptage
  d'indicateurs, hybrides parité×positivité). **Tout argument de borne
  inf doit dominer TOUS les mécanismes à la fois** — c'est la
  difficulté exacte, démontrée, de la cible.

## 5. DONNÉES EXACTES DISPONIBLES (points d'appui et tests)

Blocs seuls : W(OR2) = 2, W(MAJ3) = 3, W(THR4) = 3, W(GT2) = 7.
Compositions : W(MAJ₃(OR2³)) = 12 (optimal certifié ; optimum = les
12 paires croisées, coefficient 1, unilatéral) ; W(AND2(MAJ3²)) = 6 ;
W(MAJ₃(MAJ3³)) ∈ [4, 27].
Le premier point NON TRIVIAL à prédire pour valider un argument :
**W(MAJ₅(OR2⁵))** — un argument super-additif correct doit produire
une borne > 5·2 = 10 vérifiable (l'instrument CP-SAT du dépôt pourra
la confronter, peut-être pas la fermer à n = 10).

## 6. CONDITIONS DE RECEVABILITÉ (anti-esquive, gelées)

1. **Citer cette cellule** (ligne 7 de l'Atlas / fil F-012..022) et ce
   dossier — aucune autre cible n'est ouverte ce tour.
2. **Livrer le calcul AVANT soumission** : toute affirmation
   vérifiable (petite instance, contre-exemple, valeur) doit venir
   avec son script/calcul exécuté et ses résultats. Une proposition
   sans calcul livré est rejetée sans examen (leçon des Tours 24-25 :
   5 à 20 minutes de calcul du Réfuteur les ont coulés).
3. **Le saut logique unique** : identifier explicitement le pas non
   prouvé de l'argument (s'il y en a plus d'un, les lister tous).
4. Pas de pivot : si l'attaque échoue, le dire (« échec honnête »
   recevable) — ne pas remplacer la cible par un problème voisin.
5. Barrières classiques : sans objet direct (modèle fini,
   combinatoire) — mais l'HONNÊTETÉ épistémique standard s'applique
   (distinguer prouvé/conjecturé/mesuré).

## 7. Ce que le Réfuteur fera de la proposition

Reformulation en une phrase ; attaque du saut logique ; recherche de
contre-exemple EXÉCUTÉE (CP-SAT/énumération, instances n ≤ 9) ;
confrontation aux mécanismes du zoo (§4) ; verdict FAILLE FATALE /
LACUNE RÉPARABLE / SURVIT avec le sous-lemme prioritaire.
