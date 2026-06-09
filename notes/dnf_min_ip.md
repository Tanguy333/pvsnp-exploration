# Note (brouillon) — La taille DNF minimale de la fonction inner product est (3^n − 1)/2

> **Statut : BROUILLON interne** (tâche L18-NOTE, 2026-06-09). Version arXiv
> éventuelle à rédiger en anglais. Préalables avant toute soumission : relecture
> experte indépendante + vérification de la réserve « école russe » (§6).

## 1. Énoncé

**Théorème.** Soit `IP_{2n}(x, y) = Σ_{i=1}^{n} x_i y_i mod 2` la fonction
inner product sur 2n variables. La taille minimale d'un DNF (OR de ANDs de
littéraux, fan-in arbitraire) calculant `IP_{2n}` est exactement

```
DNF_min(IP_{2n}) = (3^n − 1)/2.
```

De plus, `IP_{2n}` possède exactement `(3^n − 1)/2` implicants premiers, et
**chacun est essentiel** (admet un témoin couvert par lui seul) — le DNF
minimal est donc unique et égal à la somme de tous les implicants premiers.
La quantité compagnon pour le complément est `|primes(¬IP_{2n})| = (3^n + 1)/2`.

En fonction du nombre total de variables N = 2n : `DNF_min = (3^{N/2} − 1)/2
≈ 2^{0.7925 N}` — strictement entre la borne générique `2^{N−1}` (PARITY_N)
et les tailles polynomiales.

## 2. Preuve (récurrence sur la bi-décomposition XOR disjointe — Tour 18 du dépôt)

Décomposition : `IP_{2(n+1)}(x, y, x_{n+1}, y_{n+1}) = IP_{2n}(x, y) ⊕ (x_{n+1} ∧ y_{n+1})`.

**(A) Classification des implicants premiers.** Tout implicant premier de
`IP_{2(n+1)}` appartient à exactement une des trois classes :
- **A1** : `x_{n+1} ∧ y_{n+1} ∧ M₀` où `M₀` est implicant premier de `¬IP_{2n}` ;
- **A2a** : `¬x_{n+1} ∧ M₀` où `M₀` est implicant premier de `IP_{2n}` ;
- **A2b** : `¬y_{n+1} ∧ M₀` où `M₀` est implicant premier de `IP_{2n}`.

Les autres formes sont impossibles (une paire `(x_{n+1}, y_{n+1})` libre
forcerait `IP_{2n} = ¬IP_{2n}`) ou non-premières (`¬x_{n+1} ∧ ¬y_{n+1} ∧ M₀`
se réduit à A2a ou A2b). [Audit complet : `tours/tour_18_ip_recurrence_etabli.md`.]

**(B) Récurrence et forme close.** Avec `a_n = |primes(IP_{2n})|` et
`b_n = |primes(¬IP_{2n})|` :

```
a_{n+1} = 2 a_n + b_n,    b_{n+1} = a_n + 2 b_n,    (a_1, b_1) = (1, 2)
```

d'où `a_n = (3^n − 1)/2` et `b_n = (3^n + 1)/2` par induction
(`a_n + b_n = 3^n`, `b_n − a_n = 1`).

**(C) Essentialité (borne inférieure).** Pour chaque implicant premier `M`,
construction explicite d'un témoin couvert uniquement par `M` :
- A2a : `(x₀, x_{n+1} = 0, y_{n+1} = 1)` où `x₀` est le témoin essentiel de
  `M₀` dans `IP_{2n}` (récurrence) ;
- A2b : `(x₀, x_{n+1} = 1, y_{n+1} = 0)` ;
- A1 : `(x₀, x_{n+1} = 1, y_{n+1} = 1)` où `x₀` est témoin de `M₀` dans `¬IP_{2n}`.

Les fixations de `(x_{n+1}, y_{n+1})` excluent les couvertures croisées entre
classes. Tout DNF doit donc contenir chaque implicant premier : `DNF_min = a_n`. ∎

**Vérification exécutable** : énumération exhaustive + ILP set-cover exact
(PuLP/CBC) confirment 1, 4, 13, 40 pour n = 1, 2, 3, 4
(`checks/tour_17_inner_product_dnf.py`, `checks/tour_17_extension_n4.py`),
**et 121 pour n = 5** (énumération des 3^10 ANDs par masques de bits +
set cover ILP, `checks/task_f005b_verification_k4_k5.py`, 2026-06-09) —
soit **5 points de vérification directe**.

## 3. Pourquoi ce n'est pas une conséquence directe des techniques standards

- **Borne par couverture** : `|IP^{-1}(1)| / (taille max d'un sous-cube ⊆ IP^{-1}(1))`
  donne ~`2^n − 1`, loin de `(3^n − 1)/2 ≈ 3^n/2`. L'essentialité de *tous*
  les premiers est nécessaire.
- **Cadre Sasao-Butler (bi-décompositions, ASP-DAC 2001)** : leur méthode
  repose sur la distributivité du AND/OR ; la bi-décomposition **XOR**
  (le cas d'IP) est hors de leur cadre (vérifié sur le texte intégral).
- **Quine-McCluskey / essentialité (notre L19)** : IP est dans la classe
  « tous les premiers essentiels » (α)/(β) — la note rattache donc IP au
  théorème-cadre classique, mais le *comptage exact* `(3^n − 1)/2` demande
  la classification (A).

## 4. Théorème de correspondance (T-F006, prouvé le 2026-06-09) : weight PTF = DNF_min

> **Théorème.** Pour tout n ≥ 1, la weight L1 minimale d'une représentation
> à seuil de `IP_{2n}` par polynôme **réel** (base monômiale 0/1 ;
> p ≥ 1 sur IP⁻¹(1), p ≤ 0 sur IP⁻¹(0)) vaut exactement
> `(3^n − 1)/2 = DNF_min(IP_{2n})`.

**Borne sup** : le polynôme multilinéaire exact
`p* = (1 − Π(1−2x_iy_i))/2`, de coefficients `(−1)^{|S|+1}2^{|S|−1}` sur les
monômes appariés, a L1 = `Σ C(n,s)2^{s−1} = (3^n−1)/2`.

**Borne inf** : certificat dual **diagonal** — la mesure signée
`w(x,x) = (−1)^{|x|+1}2^{n−|x|}` (|x| ≥ 1), `w(0,0) = −(2^n−2)`, nulle hors
diagonale. Tous ses moments de sous-cube valent ±1 (calcul d'une ligne :
`(−1)^{s+1}2^{n−s−r}(2−1)^r` avec n−s−r = 0), sa masse positive vaut
`Σ_{a impair} C(n,a)2^{n−a} = (3^n−1)/2`, et la dualité faible conclut.
Détail : `tasks/done/F-006.md` ; vérification en arithmétique exacte
k = 1..14 + force brute k ≤ 4 : `checks/task_f006b_certificate_proof.py`.

**Esthétique** : le certificat vit sur la diagonale x = y, où IP se réduit
à PARITY.

### La constante 3^{n/2} transversale aux modèles de profondeur 2

| Modèle | Quantité | Valeur | Source |
|---|---|---|---|
| DNF pur | `DNF_min(IP_{2n})` | `(3^n − 1)/2` | cette note (Tours 17-18 ; vérifié directement n=1..5) |
| 2-CNF consistantes | max # affectations satisfaisantes d'une 2-CNF consistante avec IP | `3^n` (tight, optimum unique) | Frankl-Gryaznov-Talebanfard, ITCS 2022 ([arXiv:2111.09671](https://arxiv.org/abs/2111.09671)) |
| PTF réelle, degré libre | `min W_{L1}(IP_{2n})` | `(3^n − 1)/2` — **THÉORÈME T-F006** (plus une conjecture) | cette note §4 |

## 5. Travaux liés (recherche bibliographique, 2 campagnes, cf. `bib/l18_status.md`)

- **Profondeur 3 d'IP** (lignée active) : Golovnev-Kulikov-Williams ITCS'21 ;
  Frankl-Gryaznov-Talebanfard ITCS'22 ; Göös-Guan-Mosnoi MFCS'23 / I&C'24
  (Σ²₃ ∈ [2^{0.847n}, 2^{0.965n}]) ; Amano ISAAC'23 ; Gurumukhani et al. 2026.
  La profondeur 2 n'y est jamais formulée — cette note en serait le
  complément « cas de base exact ».
- **DNF de parités** : Cohen-Shinkar ITCS'16 (modèle DNF∘⊕, différent).
- **Compendiums** : Jukna 2012 (IP en communication / Σ⊕₃ / seuil, pas de
  DNF pur) ; Crama-Hammer 2011 ch. 3 (cadre implicants premiers, pas IP).
- **Théorie de la commutation** : Sasao-Butler 2001 (MSOP(EXOR_n) = 2^{n−1} ;
  bi-décomposition AND/OR « orthodox » ; XOR hors cadre) ; Butler-Sasao,
  tutoriel crypto DTIC (IP comme « disjoint quadratic bent function », angle
  ANF/non-linéarité, pas de taille SOP). **Les deux textes intégraux vérifiés
  le 2026-06-09 — formule absente.**

## 6. Réserves restantes avant soumission

1. **École russe (Yablonskii et coll., années 1960-70)** : la théorie des DNF
   minimales y est développée en profondeur, mal indexée. Un russophone
   devrait vérifier les surveys de l'école (Yablonskii, Vasil'ev, Glagolev,
   Korshunov — *Diskretnaya Matematika* / *Problemy Kibernetiki*).
2. **Relecture experte indépendante** de la preuve (A)-(C) — l'audit interne
   du dépôt (boucle adverse) ne remplace pas un referee.
3. La preuve devrait être étendue/vérifiée pour la version CNF
   (`CNF_min(IP_{2n}) = b_n = (3^n + 1)/2` ?) — non établie dans le dépôt,
   plausible par dualité mais NON prouvée (ne pas inclure sans preuve).

## 7. Distance à P vs NP

Nulle. C'est une note de combinatoire des fonctions booléennes (profondeur 2,
fonction unique). Son intérêt est (i) combler le cas de base exact de la
lignée depth-3 active, (ii) la constante 3^{n/2} transversale (§4). Aucune
barrière n'est concernée.
