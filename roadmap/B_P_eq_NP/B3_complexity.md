# Étape B.3 — Borner le temps d'exécution par $|\phi|^k$

## Objectif formel

Démontrer que l'algorithme $A$ (validé en B.1, prouvé correct en B.2) a
un temps d'exécution borné par $|\phi|^k$ pour un $k$ fixé indépendant de
$\phi$.

C'est **la** condition critique de B (B.2 est routine pour DPLL ; B.3 est
ce qui rend P = NP).

## Statut actuel (2026)

* Toute analyse de complexité « polynomiale » pour SAT a été trouvée
  fausse jusqu'à présent (cf. registres des prétentions arXiv).
* Erreurs typiques :
  * Oublier des branches dans le pire cas.
  * Confondre temps moyen et temps pire.
  * Borner le nombre d'itérations par une fonction de $n$ qui n'a pas de
    base théorique (e.g. « après $n^2$ itérations on converge » sans
    preuve).
  * Utiliser une « heuristique » qui marche en pratique mais pas dans le
    pire cas.

## Prompt pour Claude (à coller en session neuve)

> Tu reçois `A` (validé B.1-B.2).
>
> Mission : prouver que `time_A(φ) ≤ |φ|^k` pour un `k` fixé explicite.
>
> Procédure :
>
> 1. **Identifier la structure de récursion / d'itération** de `A` :
>    - Si récursif : récurrence `T(n) = a T(n/b) + f(n)` ou variante.
>    - Si itératif : compter les itérations de la boucle externe.
>
> 2. **Borner le travail par itération** :
>    - Chaque itération doit faire `poly(|φ|)` opérations primitives.
>    - Identifier le coût de chaque opération primitive (e.g. lookup,
>      arithmétique).
>
> 3. **Borner le nombre d'itérations / la profondeur de récursion** :
>    - C'est là que tout se joue. Si la borne est `2^Ω(n)`, l'algo
>      est exponentiel.
>    - Si la borne est `poly(n)`, il faut une **preuve solide** que
>      *toute* trace possible reste polynomiale.
>
> 4. **Test adversarial sur famille pathologique** :
>    - Famille `φ_n` choisie pour maximiser `time_A(φ_n)`.
>    - Mesurer empiriquement `time_A(φ_n)` pour `n ∈ {10, 20, 30, 50, 100}`.
>    - Si la croissance dépasse `n^k` pour tout `k` testé jusqu'à 10,
>      l'algorithme est **probablement exponentiel** et l'analyse de
>      complexité B.3 est fausse.
>
> 5. **Réfutation honnête si l'analyse échoue** :
>    - Identifier exactement la famille `φ_n` qui casse la borne `n^k`.
>    - Identifier la branche de l'algorithme qui prend trop de temps.
>
> Livrable : preuve formelle de complexité polynomiale **avec** confirmation
> empirique sur 5+ tailles, ou réfutation honnête.

## Critères d'acceptation

* **Succès complet** : `time_A(φ) ≤ |φ|^k` prouvé, confirmé empiriquement.
  *Sans précédent.*
* **Succès partiel** : borne polynomiale sur sous-classe d'instances
  (e.g. SAT random, planaire) avec dépendance explicite sur structure.
* **Échec acceptable** : identification empirique de la famille
  pathologique + raison structurelle.

## Modes d'échec attendus

* « Branch-and-bound » avec borne sur profondeur de récursion par `n` —
  faux car SAT a $2^n$ états potentiels.
* « Propagation unitaire » itérée — converge mais le nombre de cas
  branchés explose.
* « Symétrie » qui réduit l'espace — réduction d'un facteur polynomial,
  pas exponentiel.
* Confusion entre temps « expected » sur distribution aléatoire et
  temps pire.

## Références à embarquer

* Cook 1971 (théorème original).
* Hopcroft-Karp 1973 (matching polynomial — exemple de bornage rigoureux).
* Khachiyan 1979, Karmarkar 1984 (LP polynomial — discipline rigoureuse).
* Impagliazzo-Paturi 1999 (ETH — pourquoi exp est probablement optimal).

## Conditions du cahier en vigueur

* `(h)` script + log temporel mesuré.
* `(j)` test empirique sur famille adversariale (pas instances faciles).
* `(r)` test à tailles successives `n_0, n_0+1, n_0+2, ...` jusqu'à
  l'infaisable.
* **Test SETH implicite** : si l'algorithme dépasse `O(1.99^n)` pour
  SAT, l'analyse est probablement fausse.
