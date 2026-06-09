# D-003 : Complexité descriptive (CFI / FPC / CPT) × Preuves naturelles (RR)

> Tâche type D. Exécutée le 2026-06-09. Sources : audits A-005 (CFI + ABD,
> textes DRR 2008 et ABD 2007) et A-007 (RR 1997, texte PS Razborov).

## 1. La barrière

RR 1997 (A-007) : pas de propriété constructive + large + utile contre une
classe à PRF, sous crypto standard. Le cadre porte sur des **prédicats de
tables de vérité** de fonctions booléennes et des **bornes de taille de
circuit**.

## 2. Comment l'approche descriptive serait censée la franchir

Les séparations descriptives (CFI : FPC ⊊ P) ne produisent pas de bornes de
circuits : elles bornent le **pouvoir définitionnel de logiques** sur des
structures non-ordonnées, via des paires de structures riches en
automorphismes indistinguables par jeux à galets.

## 3. Verdict : **SANS OBJET pour FPC (hors cadre RR) — mais l'immunité vient du fait que la séparation ne touche pas P vs NP**

### 3a. Pourquoi RR ne s'applique pas à CFI

La preuve CFI (A-005) n'exhibe aucun prédicat `f_n ∈? C*_n` décidable sur
des tables de vérité : l'objet est une paire de **structures relationnelles**
(G⁰, G¹) et l'argument est un jeu d'Ehrenfeucht-Fraïssé avec comptage. Ni
constructivité, ni largeness, ni usefulness (au sens « taille de circuit
super-polynomiale ») ne sont définies pour cet argument. RR est
structurellement muet.

### 3b. Le revers : cette immunité est exactement la mesure de la distance à P vs NP

FPC ⊊ P (CFI) sépare deux formalismes **dont les deux côtés sont dans P**
(A-005 §5.1). L'argument échappe à RR parce qu'il ne produit aucune borne
de calcul — seulement une borne de définissabilité. Pour transformer une
séparation descriptive en P ≠ NP, il faudrait :

1. une logique L capturant exactement P sur structures non-ordonnées
   (question de Gurevich — le candidat vivant est CPT, ouvert), ET
2. prouver qu'un problème NP n'est pas définissable dans L.

Au point (2), la preuve devrait borner le pouvoir d'un formalisme
équivalent à P entier — et c'est ici que le spectre de RR réapparaît : une
telle borne impliquerait des bornes de circuits pour P, et si la technique
produisait un prédicat constructif et large sur les tables de vérité, RR
s'appliquerait à plein. L'immunité de CFI **ne se transmet pas** au
programme complet.

### 3c. État de la ligne CPT (rappel A-005)

Dawar-Richerby-Rossman 2008 : **CPT distingue les graphes CFI** (sur graphes
de base ordonnés). Aucun témoin contre CPT n'est connu ; aucune technique de
borne inférieure pour CPT au-delà du rang borné n'existe. La ligne est
ouverte *en amont* de toute considération de barrière.

## 4. Ligne Atlas

| Cellule | Verdict |
|---|---|
| CFI/FPC × RR | sans objet (pas une borne de circuit) — mais séparation interne à P |
| CFI/FPC × relativisation | sans objet (combinatoire finie explicite) |
| CPT × toute barrière | prématuré : aucune technique candidate pour CPT ⊊ P n'existe ; les CFI ne témoignent pas contre CPT (DRR 2008) |
| Transposition à SAT | fermée pour les gadgets naïfs (Tour 25, q.15) ; le domaine du mécanisme = CSP affines (ABD 2007) |

## Références de la cellule

A-005 (`bib/cfi_abd.md`), A-007 (`bib/razborov_rudich_1997.md`),
Tour 5 (`tours/tour_05_cpt_jeux_pavage.md`), Tour 25
(`tours/tour_25_cfi_sat_refute.md`), cahier q.15-q.16.
