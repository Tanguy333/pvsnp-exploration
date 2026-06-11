# Audit A-011 — Borwein-Mossinghoff 2000 et la famille « produits purs / hauteur 1 »

- **Déclencheur** : règle anti-redécouverte, avant de prouver d'autres
  théorèmes sur min ‖(1−x)^{d+1}·g‖₂ (formes closes Catalan V-021,
  reformulation, transitions n*(d)).
- **Source principale** : P. Borwein, M. J. Mossinghoff, *« Polynomials
  with height 1 and prescribed vanishing at 1 »*, Experimental Math.
  9(3), 2000, 425-433
  ([Project Euclid](https://projecteuclid.org/euclid.em/1045604677)) —
  **texte intégral paywallé**, audit au niveau abstract/recensions.
- Adjacents : Erdős-Szekeres 1959 (produits purs, sup-norme) ; Maltby
  1997 (produits purs & PTE, norme ℓ₁ — déjà cité au cahier) ;
  Borwein-Erdélyi, Littlewood-type problems.

## Ce que BM 2000 prouve (d'après l'abstract)

d(m) := degré minimal d'un polynôme à coefficients **{−1, 0, 1}**
(« hauteur 1 ») ayant un zéro d'ordre m en x = 1 (⟺ divisible par
(x−1)^m). Ils déterminent **d(m) exactement pour m ≤ 10**, m = 11, 12
en symétrique, exemples jusqu'à m ≤ 21 ; les extrémaux sont des
produits purs. Méthode : annulation forcée aux racines de l'unité +
combinatoire.

## DÉLIMITATION (les trois objets sont distincts)

| Objet | coefficients | taille/termes | ce que nous savons |
|---|---|---|---|
| **BM 2000 : d(m)** | {−1,0,1} | LIBRE | leur table, m ≤ 10 (non consultée — paywall) |
| **Nos transitions n*(d)** | {−1,0,1} de fait | **EXACTEMENT 2(d+1) termes** (idéales) | mesurées d ≤ 7 ; d(d+1) ≤ n*(d) toujours |
| **Nos minima m(d, n) / Conjecture 5** | **Z entiers libres** | libre | formes closes, contre-exemple, carte |

- Le travail **Conjecture 5 / contre-exemple / Catalan** porte sur les
  multiples entiers NON restreints — hors du cadre hauteur-1 de BM :
  pas de recouvrement.
- Les **transitions idéales** n*(d) sont la variante « taille fixée »
  de d(m) : objets voisins mais distincts (d(m) ≤ n*(m−1) ; l'égalité
  n'est pas garantie). Nos énoncés « n*(6) ∈ (81,102] ouvert » et
  « Tarry minimal » concernent les idéales — pas contredits par d(m),
  mais la PROXIMITÉ exige : (i) lecture humaine de BM 2000 avant toute
  diffusion des claims de transitions ; (ii) cross-check possible par
  notre propre machinerie (calculer d(m) nous-mêmes — candidate).
- Nos « premiers certificats tailles ≥ 13 » : BM donnent des EXEMPLES
  (bornes sup de d(m), m ≤ 21, toute taille) — nos certificats sont
  des bornes INF inconditionnelles à taille idéale fixée :
  complémentaires, mais la formulation « premiers » doit être
  restreinte aux **certificats d'inexistence idéale** (corrigé ici).

## Verdict

Aucun recouvrement détecté avec le cœur (Conjecture 5, contre-exemple,
formes closes) ; proximité réelle sur les transitions idéales —
**lecture humaine de BM 2000 requise avant diffusion** des claims
n*(d)/minimalité, et cross-check d(m) par nos outils en candidate.
