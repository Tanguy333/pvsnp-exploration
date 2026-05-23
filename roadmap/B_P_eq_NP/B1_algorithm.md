# Étape B.1 — Concevoir un algorithme polynomial pour SAT

## Objectif formel

Produire un algorithme déterministe $A$ tel que :
* $A$ prend en entrée une formule CNF $\phi$ sur $n$ variables, $m$ clauses.
* $A$ retourne $1$ si $\phi$ est satisfiable, $0$ sinon.
* Le temps d'exécution de $A$ est borné par $|\phi|^k$ pour un $k$ fixé.

## Statut actuel (2026)

* Tous les algorithmes connus pour SAT sont *exponentiels* dans le pire
  cas (DPLL, CDCL, WalkSAT, Survey Propagation).
* Meilleur algorithme déterministe pour 3-SAT : Schöning 1999,
  $O(1.334^n)$. Pour k-SAT général : Paturi-Pudlák-Saks-Zane 1998.
* Hypothèse ETH (Exponential Time Hypothesis) : pas d'algo en
  $2^{o(n)}$ pour 3-SAT.
* Hypothèse SETH (Strong ETH) : pas mieux que $2^{(1-\epsilon)n}$.
* La grande majorité des chercheurs conjecture P ≠ NP, donc cet algorithme
  *n'existe probablement pas*.

## Prompt pour Claude (à coller en session neuve)

> Tu es un chercheur en algorithmique combinatoire avec un mandat
> impossible : concevoir un algorithme polynomial pour SAT.
>
> Procédure (en mode honnête) :
>
> 1. **Choisir une approche structurelle** :
>    - réduction de SAT à un problème polynomial connu (LP, matching,
>      réseaux),
>    - exploitation de structure spécifique (2-SAT, Horn-SAT, XOR-SAT
>      sont déjà polynomiaux — la difficulté est 3-SAT général),
>    - méta-heuristique avec garantie polynomiale.
>
> 2. **Concevoir l'algorithme** :
>    - Pseudo-code complet, fan-in/fan-out de chaque opération.
>    - Modèle de calcul (RAM, MT) explicite.
>    - Borne polynomiale revendiquée.
>
> 3. **Test adversariel sur famille pathologique** :
>    - Construire une famille `φ_n` d'instances 3-SAT "dures" :
>      e.g. random k-SAT au seuil, pigeonhole, Tseitin sur expandeurs.
>    - Trace l'algorithme sur `φ_n` pour `n ∈ {10, 20, 30}` au moins.
>    - Mesurer si le temps reste polynomial ou explose.
>
> 4. **Auto-réfutation honnête si l'algorithme échoue** :
>    - Identifier précisément la famille `φ_n` qui le casse.
>    - Identifier la *raison structurelle* de l'échec (e.g. : algorithme
>      glouton qui ne backtrack pas, donc échoue sur instances avec
>      contradictions cachées).
>
> Livrable : algorithme + test adversariel + verdict honnête (polynomial
> ou exponentiel).

## Critères d'acceptation

* **Succès complet** : algorithme polynomial pour SAT prouvé correct.
  *Sans précédent depuis Cook 1971.*
* **Succès partiel** : algorithme polynomial pour une sous-classe
  non-triviale (e.g. SAT planaire, SAT avec contrainte structurelle).
* **Échec acceptable** : auto-identification de la famille pathologique
  + raison structurelle. **C'est l'issue probable.**

## Modes d'échec attendus

* Algorithme glouton ou local sans backtracking → casse sur Tseitin.
* Réduction à LP qui ignore l'intégralité → relaxation lâche.
* Algorithme exponentiel maquillé en polynomial (analyse fausse de la
  borne de complexité).
* Algorithme qui marche sur instances aléatoires mais pas adversariales
  (cas typique : SAT random au seuil 4.26 est dur).

## Références à embarquer

* Cook 1971.
* Schöning 1999, *« A probabilistic algorithm for k-SAT »*.
* Paturi-Pudlák-Saks-Zane 1998.
* Impagliazzo-Paturi 1999 (ETH).
* Williams 2010 (SETH consequences).

## Conditions du cahier en vigueur

* `(h)` script livré : algorithme exécutable, pas pseudo-code informel.
* `(j)` test empirique préalable : sur famille adversariale, pas
  instances jouet.
* `(k)` lien à P vs NP : direct par définition.
