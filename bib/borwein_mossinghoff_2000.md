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

## MISE À JOUR 2026-06-12 (V-046) — table lue, audit levé

PDF récupéré (archive CECM, `bib/pdf/BM_2000_P153.pdf`) et Table 1 lue
VISUELLEMENT (polices bitmap contournées, pymupdf 300 dpi, comme A-010).
Valeurs exactes : d(m) = 1, 3, 6, 11, 15, 22, 30, 41, 48, 61 (m = 1..10) ;
plus petits connus : 69 (m=11), 93 (12), 112 (13), 120 (14), 141 (15),
159 (16), 185 (17), 207 (18), 245 (19), ABSENT (20), 294 (21).
Réplication réseau (V-046) : identique m = 3..11 et 13 ; séparation à
m = 12 (frontière de phase 99 > existence 93). La « lecture humaine
requise » est faite ; le rang m = 20 manquant est une cible.

## Antériorité du rang m=20 — recherche du 2026-06-12 (avant email Mossinghoff)

Recherche web (WebSearch + WebFetch) : AUCUNE publication post-2000 d'une
valeur d(20) trouvée. Référence standard = BM 2000 (la table omet m=20
selon notre lecture visuelle ; descriptions web génériques « m <= 21 »).
Pistes vérifiées sans résultat : AMS Math.Comp. 2003 (S0025-5718-02-01460-6),
arXiv 1406.2560 (ordre d'annulation), DBLP Mossinghoff.
DEUX TROUS non comblables par l'agent :
  1. OEIS inaccessible (HTTP 403) — À VÉRIFIER MANUELLEMENT par Tanguy
     (coller : 1,3,6,11,15,22,30,41,48,61,69,93,112,120,141,159,185,207,245).
  2. Doute résiduel sur la lecture « ligne 20 absente » (rendu image) —
     reconfirmer sur copie propre avant toute revendication externe.
CONCLUSION : l'email à Mossinghoff (auteur de la table) EST le test
d'antériorité définitif ; formulé en question, pas en revendication.

### MAJ 2026-06-12 (copie propre relue)
Doute n°2 LEVÉ : la copie propre (bib/pdf/BM_2000_copie_propre.pdf) confirme
sans ambiguïté que la Table 1 passe de m=19 (d=245) directement à m=21 (d=294)
— la ligne m=20 est RÉELLEMENT absente du papier original (2000). Reste le
seul trou : antériorité post-2000 (OEIS à vérifier manuellement).

### MAJ 2026-06-12 (OEIS vérifié — capture utilisateur)
Recherche OEIS de la suite 1,3,6,11,15,22,30,41,48,61,69,93,112,120,141,159,185,207,245 :
match = A059753 « Minimal degree of a height one multiple of (x-1)^n » = notre d(m).
A059753 NE LISTE QUE jusqu'à d=120 (m=14) — donc PAS de valeur m=20 dans l'OEIS.
(le recouvrement affiché s'arrête à 120 ; si 141+ y étaient, ils apparaîtraient.)
=> Les DEUX trous d'antériorité sont LEVÉS : ni BM 2000 (table) ni OEIS A059753
   n'ont de rang m=20. Nuance : A059753 s'arrête à m=14 car au-delà BM ne donnent
   que des « smallest known » (bornes sup), pas des minima prouvés. Notre 307 est
   du même type (borne sup) — contribution naturelle, formulée comme telle dans l'email.
