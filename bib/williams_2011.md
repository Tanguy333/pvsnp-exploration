# A-001 : Audit — Williams 2011, « Non-Uniform ACC Circuit Lower Bounds »

> Tâche type A. Exécutée le 2026-06-09. Texte intégral de la version CCC 2011
> (11 pages, [people.csail.mit.edu/rrw/acc-lbs-ccc.pdf](https://people.csail.mit.edu/rrw/acc-lbs-ccc.pdf))
> téléchargé et greppé. Citations textuelles marquées « > ». Les passages non
> trouvés dans cette version (qui renvoie à la « full version ») sont marqués.

## 1. Référence canonique

- R. Williams, *« Non-Uniform ACC Circuit Lower Bounds »*, IEEE Conference on
  Computational Complexity (CCC) 2011, pp. 115-125 — best paper award.
- Version journal : *« Nonuniform ACC Circuit Lower Bounds »*, Journal of the
  ACM, vol. 61, no. 1, article 2, 2014.
  [doi:10.1145/2559903](https://doi.org/10.1145/2559903).
- Affiliation à l'époque : IBM Almaden Research Center.

## 2. Théorèmes principaux — énoncés exacts

> **Theorem 1.1** : « NTIME[2ⁿ] does not have non-uniform ACC circuits of
> polynomial size. »

(La version conférence ajoute : « Stronger size lower bounds hold (e.g.
quasi-polynomial size); cf. the full version of the paper. »)

> **Theorem 1.2 (Exponential Size-Depth Tradeoff)** : « For every d and m,
> there is a δ > 0 and a language in E^NP that fails to have non-uniform ACC
> circuits of depth d and size 2^{n^δ} with MOD_m gates. »

Définition de la classe (abstract) : « The class ACC consists of circuit
families with constant depth over unbounded fan-in AND, OR, NOT, and MOD_m
gates, where m > 1 is an arbitrary constant. » — **m composite inclus** ;
avant ce papier, « it was not known whether EXP^NP had depth-3 polynomial
size circuits made out of only MOD_6 gates ».

## 3. Hypothèses non-triviales

1. **Non-uniformité totale** des circuits ACC (aucune condition de
   constructibilité sur la famille). La borne est inconditionnelle.
2. **Profondeur constante d et module m constants** : les constantes δ du
   Theorem 1.2 dépendent de (d, m). Pas de borne pour profondeur croissante.
3. La méthode passe par la **complétude forte de SUCCINCT 3SAT** pour NEXP
   (propriétés de complétude « paddables » spécifiques) et le **théorème de
   Gurevich-Shelah** (NTIME machines RAM vs multitape, Theorem 2.1 de la
   version conférence).

## 4. Outils techniques (la « méthode algorithmique »)

Structure en 2 moitiés, citée textuellement :

1. **Connexion algorithme → borne** (Theorem 3.1, [Wil10] renforcé en
   Theorem 3.2) :
   > « Let s(n) = ω(n^k) for every k. If ACC CIRCUIT SAT instances with n
   > variables and n^c size can be solved in O(2^{n/3}/s(n)) time for every
   > c, then E^NP does not have non-uniform ACC circuits of polynomial
   > size. »
   La version 2011 affaiblit le requis à `O(2ⁿ/n^k)` (gain super-polynomial
   seulement) :
   > « nontrivial satisfiability algorithms for size n^{log n} ACC circuits
   > with running time O(2ⁿ/n^k) imply exponential size ACC lower bounds for
   > E^NP (Theorem 3.2). »
   Le papier souligne : « this part of the proof does not use any specific
   properties of ACC, so it may be useful for proving stronger lower bounds
   in the future. »

2. **L'algorithme CAPP/SAT non-trivial pour ACC** (Theorem 4.1) via la
   transformation structurelle :
   > « Applying a powerful result of Yao, Beigel-Tarui, and Allender-Gore
   > (Lemma 4.1), C′ can be replaced by an equivalent depth-2 circuit C′′ of
   > 2^{n^δ·2^{O(d)}} size, which consists of an efficiently computable
   > symmetric function at the output gate and AND gates below it. »
   (SYM+ : taille `s^{O(log^c s)}`, fan-in des ANDs `poly(log s)` —
   Beigel-Tarui 1994 dérandomise la construction probabiliste de Yao 1985.)
   Puis évaluation rapide par programmation dynamique :
   > « C′′ can be evaluated on all of its possible assignments in
   > 2^{n−n^δ}·poly(n) time (Lemma 4.2). »

## 5. Ce que le papier NE PROUVE PAS

1. **Rien sur TC⁰** : la transformation Yao/Beigel-Tarui est spécifique aux
   portes MOD_m ; les portes majority/threshold n'admettent pas de SYM+
   quasi-polynomial connu. NEXP vs TC⁰ reste ouvert (toujours en 2026).
2. **Rien en-dessous de NEXP / E^NP** : pas de borne pour NP, P, ni même EXP
   sans oracle NP pour la version exponentielle. P ≠ NP n'est pas approché.
3. **Pas de borne pour P/poly ni NC¹** : seulement ACC (profondeur constante,
   MOD_m). L'extension à des classes plus puissantes exige de nouveaux
   algorithmes SAT non-triviaux — ce qui est précisément le programme ouvert
   depuis (cf. §7 q.7 du cahier).
4. **La borne quasi-polynomiale (pas pleinement exponentielle) pour NEXP** :
   l'exponentielle n'est obtenue que pour E^NP (Theorem 1.2), pas NTIME[2ⁿ].
5. **Uniformité** : le résultat précédent d'Allender-Gore (Permanent ∉ ACC
   uniforme) exigeait l'uniformité ; Williams retire l'uniformité mais au
   prix de monter à NEXP.

## 6. Position vis-à-vis des 3 barrières (verbatim — pièce maîtresse pour l'Atlas)

- **Preuves naturelles (RR)** :
  > « Intuitively, we circumvent the natural proofs barrier [RR97] because of
  > the use of diagonalization. More precisely, we rely heavily on strong
  > completeness properties of a specific NEXP language, namely SUCCINCT
  > 3SAT […] (Furthermore, there is little evidence that ACC contains
  > pseudorandom functions, so natural proofs may not be a barrier for ACC
  > after all.) »
  Donc : contournement par **diagonalisation + complétude**, et la largeness
  de RR est probablement sans objet pour ACC (pas de PRF candidates dans ACC).

- **Relativisation et algébrisation** :
  > « More conclusively, the approach of this work definitely avoids
  > relativization [BGS75] and algebrization [AW09] because there are oracles
  > A relative to which NEXP^A ⊂ ACC^A, and even NEXP^Ã ⊂ ACC^A (Scott
  > Aaronson, personal communication). The ACC SAT algorithm used in the
  > lower bounds relies on non-relativizing properties of ACC circuits. »
  Et la raison structurelle :
  > « all known improved SAT algorithms break down when oracles (or algebraic
  > extensions thereof) are added to the instance. That is, improvements over
  > exhaustive search necessarily exploit structure in instances that
  > black-box methods cannot see. »

  **C'est la formulation canonique du « pourquoi » la méthode algorithmique
  franchit les 3 barrières** : un algorithme SAT meilleur que la recherche
  exhaustive doit lire la structure interne du circuit — ce qu'aucun
  argument boîte-noire (oracle ou extension algébrique) ne peut faire.

## 7. Lien à la bibliographie §7 du cahier et aux tours du dépôt

- Déjà cité au cahier §7.2 (lignée AC⁰ → ACC⁰ → NEXP) comme « seul résultat
  ayant franchi les trois barrières » — l'audit confirme cette description,
  en la précisant : le franchissement de RR est *argumenté* (diagonalisation,
  absence probable de PRF dans ACC) tandis que le franchissement de
  relativisation/algébrisation est *démontré* (oracle d'Aaronson).
- **Tour 4** (tensor networks pour TC⁰) : invoquait la méthode Williams sans
  algorithme nouveau — l'audit confirme que sans CAPP/SAT non-trivial, il
  n'y a pas de méthode (le « programme actif depuis 2010 »).
- **Tour 23** (tcomp/PTF pour TC⁰) : le point (d) de la réfutation
  (« Beigel-Tarui utilise des polynômes exacts mod 2^ℓ / SYM+, pas des PTF
  entières ») est confirmé textuellement : Lemma 4.1 produit une **fonction
  symétrique de ANDs** (SYM+), pas une PTF à seuil.
- **Tâche F-001** : la conclusion (« pas d'analogue Beigel-Tarui pour TC⁰
  d=2, IP échappe à poly-weight ») est exactement l'obstacle qui borne
  l'extension de ce papier à TC⁰ — cellule de l'Atlas « méthode Williams ×
  extension TC⁰ » à remplir avec ces deux pièces.

## Limitations de l'audit

- Basé sur la **version conférence CCC 2011** (11 p.) ; la version JACM 2014
  (« full version ») contient les bornes quasi-polynomiales détaillées pour
  NTIME[2ⁿ] et les preuves complètes — non auditée ici.
- Les théorèmes 3.2/4.1/4.2 sont cités par leur rôle ; leurs énoncés complets
  avec quantificateurs exacts figurent dans le PDF source.
