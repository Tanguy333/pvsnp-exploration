# MC-016 — Mesures : la loi de croissance du déficit de partage

Tâche : MC-016. Script : `checks/mc016_croissance.py`. Date : 2026-08-08.
Instrument : CP-SAT, formulation canal-de-valeurs, OPTIMAL exigé, témoin
re-vérifié par assertion. **Cap de recherche** : cap = Σ G + 4 (re-solve
à 2×(Σ G + 4) si INFEASIBLE) — le minimum trouvé sous cap est le vrai
minimum dès qu'il est ≤ cap.

Objet : h(x, y) = [y = c_x], base t bits (k = 2^t fibres), fibre s bits
partagée ; déficit g := W(h) − Σ_x G(c_x). MC-015 (baseline (2,4)) :
antichaînes concentrées à g = −2, minimum global −3.

## Mode base — replays (2, 4), cohérence avec MC-015

| instance | Σ G | W | g |
|---|---|---|---|
| antichaîne de paires {01},{02},{12},{03} (affectation croissante) | 12 | 11 | **−1** (= MC-015 : reproduit) |
| singletons {0},{1},{2},{3}, s = 4 | 16 | 13 | **−3** |

## Mode t2s5 — la croissance en s à t = 2 (ν = 7)

| instance | Σ G | W | g | durée |
|---|---|---|---|---|
| a1 = tuple MC-015 plongé (1 bit oisif) | 16 | 14 | **−2** | 10 s |
| a2 mixte {01},{23},{04},{12} | 16 | 15 | −1 | 19 s |
| a3 étalé {01},{23},{14},{24} | 16 | 15 | −1 | 19 s |
| a4 étoile {01},{02},{03},{04} | 16 | 13 | **−3** | 3 s |
| a5 chemin {01},{12},{23},{34} | 16 | 15 | −1 | 26 s |
| a6 antichaîne aléatoire | 16 | 14 | −2 | 10 s |

Le plongement a1 : (2,4) → (2,5) fait passer g de −1 à −2 (Σ G croît de
4, W de 3 seulement) — **le bit oisif creuse le déficit**.

## Mode var — variance d'affectation + contrôles (ν = 7, s = 5)

| instance | Σ G | W | g |
|---|---|---|---|
| a1, permutation inverse | 16 | 14 | −2 |
| a1, permutation (1,{2,4},3) | 16 | 13 | −3 |
| a1, permutation croisée | 16 | 13 | −3 |
| chaîne alignée (rangs 1234) | 14 | 14 | **0** — l'additivité alignée TIENT à s = 5 |
| chaîne pire (rangs 4231) | 14 | 10 | **−4** — plus profond que le −3 de s = 4 |
| aléatoire 1 (avec emboîtements) | 12 | 9 | −3 |
| aléatoire 2 | 17 | 14 | −3 |

## Mode sing — LA FAMILLE RÉVÉLATRICE : singletons à travers s

| s | Σ G = 4s | W | g | durée |
|---|---|---|---|---|
| 4 | 16 | 13 | **−3** | 0 s |
| 5 | 20 | 16 | **−4** | 2 s |
| 6 | 24 | 19 | **−5** | 11 s |

**W = 3s + 1 et g = −(s − 1), conformes aux TROIS points mesurés**
(étiquette honnête : loi MESURÉE à 3 points, pas prouvée — précédent
q.12). Le déficit de cette famille est **linéaire en s — une fraction
constante de Σ G = 4s**. Ce n'est PAS un O(t).

## Mode t2s6 — le plafond ν = 8 à t = 2 (paires)

| instance | Σ G | W | g | durée |
|---|---|---|---|---|
| b1 partition + croisée {01},{23},{45},{12} | 20 | 20 | **0** — premier tuple multi-bits NON négatif | 1 014 s |
| b2 = tuple MC-015 plongé (2 bits oisifs) | 20 | 16 | **−4** | 37 s |
| b3 étalé {05},{14},{23},{24} | 20 | 19 | −1 | 435 s |

La série du plongement (b2) : g = −1, −2, −4 à s = 4, 5, 6 — les bits
oisifs creusent, sans loi ajustée (3 points, pas de fit). b1 : la
structure « 3 paires disjointes + 1 croisée » ne partage PAS —
l'îlot d'additivité est du côté de la DISJONCTION des supports (cohérent
avec MC-006 : blocs disjoints = le seul mécanisme prouvé), mais pas
propre (a2 à s = 5, structure analogue, donnait −1).

## Mode t3 — la croissance en k : 8 fibres

| instance | Σ G | W | g | durée |
|---|---|---|---|---|
| quasi-antichaîne s = 4 (6 paires + {0} + {123} ; 6 comparabilités inévitables — Sperner : antichaîne max = 6 < 8) | 24 | 15 | **−9** | 28 s |
| antichaîne PLEINE s = 5 (8 paires de [5], ν = 8) | 32 | **∈ [20, 25]** | **∈ [−12, −7]** | 3 600 s, NON CONCLU — intervalle PROUVÉ (borne inf. du solveur + réalisable trouvé) |

**Le déficit croît avec k** : à k = 4 le pire mesuré était −3 (hors
chaîne pire −4) ; à k = 8 : −9 exact (quasi) et ≤ −7 prouvé
(antichaîne pleine, sans aucun emboîtement). En proportion : W ≤ 25
contre Σ = 32 — au moins 22 % de rabais.

## Mode temoin_sing — le mécanisme du partage linéaire : LA VALEUR COMMUNE

Programmes optimaux extraits (s = 4 : W = 13 ; s = 5 : W = 16) :
**les quatre points de h reçoivent UNE VALEUR COMMUNE** (3 à s = 4,
2 à s = 5), les zéros occupant tout le reste du spectre. Le programme
ne paie pas quatre lois G indépendantes : il couvre les quatre fibres
à valeur exacte partagée — une seule classe de valeur à protéger dans
l'espace commun. C'est le mécanisme déjà vu par MC-003 sur les uns en
antichaîne (« couvert à valeur exacte, tête ETHR de fait »), qui
resurgit ici en géométrie de fibres : **possible précisément parce que
les points de h sont deux à deux incomparables** (l'antichaîne, qui
devait empêcher le partage, est ce qui le PERMET).

## Lecture finale

1. La question de MC-015 (« |g| = O(t) ou Θ(Σ) ? ») est **tranchée
   contre le schéma naïf, sur les DEUX axes** : en s (singletons :
   g = −(s−1) aux 3 points, Θ(Σ/4)) et en k (−9 exact à k = 8 en
   quasi-antichaîne ; ≤ −7 prouvé en antichaîne pleine sans aucun
   emboîtement). L'additivité à terme contrôlé près N'EXISTE PAS en
   espace partagé.
2. **Le mécanisme est nommé et témoigné : la valeur commune** — les
   fibres incomparables se laissent couvrir à valeur exacte partagée ;
   l'antichaîne, condition candidate de NON-partage à base 1 bit, est
   ce qui REND le partage possible à base multi-bits. Le renversement
   de MC-015 a son explication.
3. Le déficit n'est pas uniforme à Σ constant : g va de −1 (étalé) à
   −3 (étoile, bit commun) à s = 5 — la géométrie des supports module.
4. Les îlots d'additivité observés : la chaîne ALIGNÉE (g = 0 à s = 4
   et 5) et les paires quasi-disjointes b1 (g = 0 à s = 6, 17 min de
   preuve) — tous deux du côté opposé à l'antichaîne serrée ; cohérent
   avec le sélecteur (MC-006 : blocs disjoints), sans faire une loi
   (a2, analogue de b1 à s = 5, donne −1).
5. **Conséquence pour la route-but** : le schéma de totalisation ne
   peut PAS traiter les fibres en espace partagé comme additives à
   terme près — il doit payer les blocs disjoints (le sélecteur,
   MC-006), et la charge de la route passe DÉFINITIVEMENT au chaînon
   compression (cible suivante nommée : MC-017, la compression à tête
   symétrique).
