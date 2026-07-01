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

## MISE À JOUR 2026-06-29 — SECTIONS MÉTHODE LUES (pages 1-8, lecture visuelle)

Lecture ciblée « comment ont-ils calculé » (question : de meilleurs moyens
d'explorer ?). Rendu pymupdf 150 dpi, pages 1, 2, 3, 4, 5, 7, 8.

### Leurs deux stratégies de recherche (§2, bornes SUP)

1. **§2.1 Réduction de réseau (LLL, Maple)** sur les multiples RÉCIPROQUES :
   base {f·g_k} avec g_k réciproques, vecteurs = demi-coefficients (dimension
   divisée par 2 par symétrie) — c'est notre moteur symétrique/svp, réinventé
   indépendamment (lignée confirmée). Plus un raffinement GLOUTON qu'on n'a
   pas : chercher des multiples de hauteur moyenne, puis des multiples de CES
   multiples (≤ 3 itérations). Hauteur 1 atteinte pour tout m ≤ 18 ainsi.
   Le meilleur m=15 N'EST PAS un produit pur : produit pur [1..7,7,8..19]
   (exposant 7 RÉPÉTÉ) × un polynôme NON-cyclotomique de degré 28.
2. **§2.2 Recherche de produits purs À GABARIT** : ∏_{a∈A}(x^a−1)·∏_{c∈C}(x^c−1)
   avec A = {1} ∪ {p premier ≤ m+1} FIXE et C ⊂ B, B = composites ≤ m+1 +
   impairs de [m+2, 3(m+1)/2]. PAS de DFS exhaustif. « Despite several
   variations... no examples were found for m = 20 or m > 21 » — le trou
   m=20 vient du GABARIT : notre exposant 50 (pair, > 3·21/2 ≈ 31,5) est
   hors de leur B. Cohérent avec la réponse de Mossinghoff (le saut 31→50).
   => Notre DFS-transit-B&B (V-047/V-054) domine strictement leur §2.2.

### Leur machinerie exacte (§3-4, bornes INF et d(m) exacts m ≤ 10)

- **Théorème 3** : hauteur 1, zéro d'ordre m en 1, p ≤ m premier,
  r = ⌊(m−1)/(p−1)⌋ ; si d ≤ p^{r+1} − p alors Φ_p | f.
- **Théorème 4** : si d ≤ 2^{⌊(m+3)/2⌋} − 2 alors Φ₄ | f.
- **Théorème 5** : table R(m) des Φ_n forcés à d ≤ d₀(m), m ≤ 12
  (ex. R(12) = {2,3,4,5,7,11,13}).
- **§4** : algorithme exact — écrire f = (x−1)^m · ∏_{n∈R(m)} Φ_n · g et
  énumérer le cofacteur g contraint (+ analyses aux racines de l'unité,
  vérifs Maple). C'est ainsi que d(m) est PROUVÉ pour m ≤ 10 (et 11-12
  symétriques seulement).
- Application à nos plages (calcul Théorèmes 3-4) : m=22, d ≤ 473 ⟹
  Φ₂,Φ₃,Φ₄,Φ₅,Φ₇,Φ₁₁ | f ; produit pur ⟹ exposants contiennent des
  multiples de 2,3,4,5,7,11 (champion 473 : ✓ tous). Idem m=24, d ≤ 640.

### Contexte théorique (p.1-2) — corrige notre discours

- **Bornes CONNUES : m² ≪ d(m) ≪ m² log m** (inf : Borwein-Erdélyi-Kós
  1997 ; sup : Bloch-Pólya 1932). Le minorant QUADRATIQUE existe — notre
  claim de session « seul le linéaire 2m−1 est prouvable » était FAUX
  (conversation seulement, aucun doc committé ne le disait).
- **Erdős-Szekeres 1959** : A(m) = min norme sup des produits purs à m
  facteurs ; conjecture A(m) ≫ m^c pour tout c (OUVERTE) ; Belov-Konyagin
  1996 : log A(m) ≪ log⁴ m. BM notent p.2 : hauteur 1 ⟹ ‖f‖_∞ ≤ deg+1,
  donc la conjecture ⟹ **les extrémaux ne peuvent plus être des produits
  purs pour m grand**. NOTRE mur des produits purs (m=24-30, V-054) est
  exactement ce phénomène — d_produit(m) ≥ A(m) − 1 ; nos bornes basses
  (640..760) sont des données EMPIRIQUES sur la croissance de A(m).
- **Maltby 1998** : les produits purs ne résolvent pas PTE idéal pour
  m ∈ {7,9,10,11} — antériorité de saveur « produits purs insuffisants ».

### Meilleurs moyens — RECADRÉ par l'inventaire du dépôt (Tanguy, 2026-06-29)

**Constat : sur 2 des 3 composants de BM, le dépôt a DÉJÀ fait mieux.**

| composant BM 2000 | notre contrepartie | verdict |
|---|---|---|
| §2.1 LLL Maple heuristique, multiples réciproques (m ≤ 18) | svp_turbo (LLL certifié + énumération EXACTE, ×4000) + moteur symétrique (leur astuce réciproque = notre loi V-042 prouvée d ≥ 8) + **carte de phase φ(m)** (V-046/V-048 : coïncidence m ∈ {3..11,13,14}, décollements {12,15,16,17}, seuil m* = 15) | **dépôt strictement meilleur** |
| §2.2 gabarit produits purs (a raté m=20) | DFS-transit-B&B (V-047/V-054) : m=20=307, m=22=473, m=23=439 certifiés | **dépôt strictement meilleur** |
| §3-4 divisibilités forcées + d(m) exacts m ≤ 10 | V11 (plancher), Lemmes A/B parité, barreaux interdits — complémentaires, pas équivalents | **la seule pièce à importer** |

**Pépite de l'inventaire : notre m* = 15 EXPLIQUE leur anomalie m = 15.**
BM notent (p.3, sans explication) que leur meilleur m=15 n'est PAS un
produit pur (produit pur × non-cyclotomique). Notre seuil de découplage
m* = 15 (V-046 §4quater : dès m=15, les super-empilements cyclotomiques
hauteur 2 à Φ_q répétés battent SYSTÉMATIQUEMENT les plats en L2 au degré
d(m)) est l'explication structurelle de leur anomalie, 25 ans après.
Candidat fort pour la réponse à Mossinghoff.

Moyens restants, re-classés (seul le 1 est vraiment neuf) :
1. **L'HYBRIDE** : leurs Théorèmes 3-5 × nos moteurs — (a) élagage du DFS
   produits purs (multiples forcés) ; (b) réseau-QUOTIENT
   f = (x−1)^m ∏Φ_n · g + turbo-LLL pour le d(m) GÉNÉRAL à m=22/23
   (teste produit-pur = général, notre caveat central). Ni eux ni nous ne
   l'avons fait ; nous apportons la moitié computationnelle forte.
2. d(11)-d(13) exacts (leur §4 + notre calcul + V11/parité) — convertir
   « plus petits connus » en minima PROUVÉS (antériorité à vérifier avant).
3. Cadre A(m)/Erdős-Szekeres pour nommer le mur (documenté ci-dessus).
4. Parallélisme (t1,t2) ; demander à Mossinghoff (gratuit).
