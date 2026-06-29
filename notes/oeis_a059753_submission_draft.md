# Brouillon — soumission OEIS A059753 (rang m = 20), suggérée par Mossinghoff

> À soumettre par Tanguy via l'interface OEIS (« Contribute / Edit »).
> A059753 = « Minimal degree of a height one multiple of (x-1)^n ».
> Termes actuels (m=1..14) : 1, 3, 6, 11, 15, 22, 30, 41, 48, 61, 69,
> 93, 112, 120. Au-delà (m≥15), seuls des PLUS PETITS DEGRÉS CONNUS
> (bornes sup) existent — donc à proposer en COMMENT/EXAMPLE, pas comme
> termes prouvés. Mossinghoff (co-auteur de la réf. BM 2000) a suggéré
> de consigner le rang m=20.

## COMMENT à ajouter

For n = 15..21, the values in the literature are smallest known degrees
(upper bounds), not proven minima. From Borwein & Mossinghoff (2000),
Table 1: a(15) <= 141, a(16) <= 159, a(17) <= 185, a(18) <= 207,
a(19) <= 245, a(21) <= 294. The entry for n = 20 was absent from that
table; a height-1 multiple of (x-1)^20 of degree 307 was found in 2026
(T. Le Mer), giving a(20) <= 307. Note the non-monotonicity 307 > 294.
The example for n = 20 requires a transient height 2 in the partial
products taken in increasing order of exponent (unlike the n <= 14
extremals, several of which stay within height 2 as well, but the large
gap 31 -> 50 in the exponent set is what a height-bounded ascending
search must reach).

## EXAMPLE à ajouter (n = 20)

a(20) <= 307, attained by the pure product
  Product_{t in S} (1 - x^t),  S = {1,2,3,4,5,7,8,9,11,12,13,15,17,19,
                                    21,23,27,29,31,50},
a polynomial with coefficients in {-1,0,1} and a zero of order exactly 20
at x = 1 (degree 307).

## REFERENCE / LINK

P. Borwein and M. J. Mossinghoff, Polynomials with height 1 and
prescribed vanishing at 1, Experiment. Math. 9 (2000), no. 3, 425-433.
[+ lien éventuel vers le dépôt / un court note si Tanguy en publie une]

## PROG (PARI/GP — vérification, optionnel)

\\ vérifie : height 1 et ordre d'annulation 20 en x=1
S = [1,2,3,4,5,7,8,9,11,12,13,15,17,19,21,23,27,29,31,50];
P = prod(i=1, #S, 1 - x^S[i]);
print(vecmax(abs(Vec(P))) == 1);          \\ height 1 -> 1 (true)
print(valuation(subst(P, x, x+1), x) == 20); \\ ordre 20 en x=1 -> 1

## NOTE pour Tanguy (hors soumission)

- Vérifié 3× exactement (V-047, V-049, et 2026-06-27) : 20 facteurs,
  degré 307, hauteur 1, multiplicité exactement 20.
- 307 = plus petit connu sous (transit <= 6, degré <= 330) ; un produit
  de degré 256..306 exigerait transit >= 7 (non exploré). À présenter
  comme borne sup, jamais comme minimum prouvé.
- Antériorité : Mossinghoff (auteur de la table) confirme la nouveauté
  du cas hauteur-1 mult-20. Cipu 2004 (LMS JCM) borne la norme L2/length,
  ses exemples mult-20 sont hauteur 2 (adjacent, ne préempte pas).
