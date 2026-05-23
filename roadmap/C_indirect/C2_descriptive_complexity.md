# Étape C.2 — Complexité descriptive : conjecture de Gurevich

## Objectif formel

Trouver une **logique** $\mathcal{L}$ telle que :

* $\mathcal{L}$ capture P (au sens : `L ∈ P ⟺ ∃ φ ∈ L. struct(L) ⊨ φ`).
* OU : prouver qu'aucune logique récursivement énumérable ne capture P.

Si on prouve qu'une formule de SAT n'est pas $\mathcal{L}$-définissable pour
une logique $\mathcal{L}$ capturant P, alors $P \neq NP$.

## Statut actuel (2026)

* **Théorème d'Immerman-Vardi 1982** : sur les structures *ordonnées*,
  $FO + LFP$ (Fixed-Point Logic) capture P.
* **Conjecture de Gurevich** : il existe une logique capturant P sur
  *toute* structure (sans ordre). Ouverte.
* **Théorème de Cai-Fürer-Immerman 1992** : les graphes CFI ne sont pas
  distingués par $C^k$ (Counting Logic à $k$ variables) pour tout $k$
  fixé — résultat négatif pour la complexité descriptive sans ordre.
* **CPT+C** (Choiceless Polynomial Time avec Counting) : candidat
  contemporain. La conjecture Blass-Gurevich-Shelah `CPT+C = P` est
  ouverte.
* Tour 5 du cahier a tenté CPT+C sur hypercubes colorés, FAILLE FATALE.

## Prompt pour Claude (à coller en session neuve)

> Tu es chercheur en complexité descriptive. Mission : avancer sur la
> conjecture de Gurevich.
>
> Procédure :
>
> 1. **Choisir un angle** :
>    - (a) Prouver que CPT+C ≠ P (résultat *négatif* fort).
>    - (b) Prouver que CPT+C = P (résultat *positif* fort).
>    - (c) Étudier une logique candidate alternative (rank logic,
>      IFP+ranks, polynomial-time interpretation, etc.).
>
> 2. **Pour (a)** : exhiber une famille de structures `S_n ∈ P` qui ne
>    sont pas CPT+C-équivalentes, mais qui devraient l'être par
>    définition de P. Le candidat naturel est une variante CFI où la
>    structure est invariante sous certaines permutations cachées.
>
> 3. **Pour (b)** : prouver qu'une fonction polynomiale arbitraire peut
>    être simulée par un programme CPT+C. Demande de comprendre le
>    fragment décidable de CPT+C.
>
> 4. **Pour (c)** : la logique de rang (Dawar-Holm) capture des
>    extensions de P, mais on conjecture qu'elle ne capture toujours pas
>    P. Vérifier l'état du programme Dawar-Holm 2010s.
>
> 5. **Pivot vers P vs NP** : si on prouve qu'une logique `L` capture P
>    et qu'aucune formule de `L` ne définit SAT, alors P ≠ NP.
>
> 6. **Test des barrières** :
>    - Relativisation : les jeux de pavage de CFI sont *combinatoires*,
>      pas relativisants (✓).
>    - RR : la classe des structures CFI est-elle large ?
>      *Non, c'est une famille spécifique* (✓).
>    - Algébrisation : pas d'arithmétisation utilisée (✓).
>
> Livrable : choix d'angle + avancée (même mineure) + identification du
> gap restant.

## Critères d'acceptation

* **Succès complet** : conjecture de Gurevich résolue (positive ou
  négative). *Sans précédent.*
* **Succès partiel** : avancée sur CPT+C / rank logic / autre candidat.
* **Échec acceptable** : audit complet du front Dawar / Grohe /
  Gurevich.

## Modes d'échec attendus

* Tour 5 répété (encodage SAT trivialement FO-définissable par
  surface).
* Confusion FO vs FO+C vs FO+LFP — les 3 ont des pouvoirs très différents.
* Invocation d'un « théorème de Dawar » qui n'existe pas (cf. Tour 5).

## Références à embarquer

* Immerman 1982, *« Relational queries computable in polynomial time »*.
* Vardi 1982.
* Cai-Fürer-Immerman 1992 (CFI).
* Blass-Gurevich-Shelah 1999 (CPT+C).
* Dawar-Holm 2010s (rank logic).
* Grohe 2017, *Descriptive Complexity, Canonisation, and Definable
  Graph Structure Theory*.
* Otto, *« Bounded Variable Logics and Counting »*.

## Conditions du cahier en vigueur

* `(g)` encodage non-trivialisant : interdit Tour 5 répété.
* `(q)`, `(r)` toutes en vigueur.
