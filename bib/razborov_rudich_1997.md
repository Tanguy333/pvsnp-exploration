# A-007 : Audit — Razborov & Rudich, « Natural Proofs » (1997)

> Tâche type A. Exécutée le 2026-06-09.
> **Sourçage** : version PostScript hébergée par Razborov
> ([files/int.ps](http://people.cs.uchicago.edu/~razborov/files/int.ps),
> datée du 11 septembre 1999, 26 pages — **texte extrait des chaînes PS et
> greppé**). Citations « > » = ce texte (orthographe TeX-kerning nettoyée).

## 1. Référence canonique

- A. A. Razborov, S. Rudich, *« Natural Proofs »*, Journal of Computer and
  System Sciences, vol. 55, no. 1, 1997, pp. 24-35 (STOC 1994).
  [doi:10.1006/jcss.1997.1494](https://doi.org/10.1006/jcss.1997.1494).
- Prix Gödel 2007.

## 2. Définitions exactes (le cœur du papier)

Une propriété combinatoire `C_n ⊆ F_n` (fonctions booléennes à n variables)
est **naturelle** si elle contient un sous-ensemble `C*_n` vérifiant :

> « **Constructivity**: The predicate f_n ∈? C*_n is in P. Thus, C*_n is
> computable in time which is polynomial in the truth table of f_n. »

(Donc temps `2^{O(n)}` en n — polynomial dans la taille `N = 2^n` de la
table de vérité.)

> « **Largeness**: |C*_n| ≥ 2^{−O(n)} · |F_n|. »

(Reformulé dans le texte : « f_n has a non-negligible chance of having
property C_n », fraction ≥ 1/N^k.)

Et elle est **utile contre P/poly** si :

> « **Usefulness**: The circuit size of any sequence of functions f_1, f_2,
> …, where f_n ∈ C_n, is super-polynomial. »

## 3. Théorème principal — énoncé exact

> « Our main theorem in Section 4 gives evidence that no proof strategy
> along these lines can ever succeed. We show that any large and
> constructive C_n that is useful against P/poly provides a statistical
> test that can be used to break any polynomial-time pseudo-random number
> generator. Specifically, it would violate the fairly widely believed
> conjecture that there exist pseudo-random generators of hardness 2^{n^ε},
> for some ε > 0. »

Version inconditionnelle (abstract) :

> « Without the hardness assumption, we are able to show that they can't
> prove exponential lower bounds (for general circuits) for the discrete
> logarithm problem. »

## 4. Portée revendiquée — toutes les preuves connues sont naturelles

> « We argue that all lower bound proofs known to date against non-monotone
> Boolean circuits are natural, or can be represented as natural. »

L'abstract précise même la version restreinte :

> « the weaker class of AC⁰-natural proofs which is sufficient to prove the
> parity lower bounds of Furst, Saxe, and Sipser » [est aussi limitée, sous
> des hypothèses de dureté plus fortes].

Donc : FSS/Håstad (AC⁰) et Razborov-Smolensky (AC⁰[p]) **naturalisent** —
confirme la note de l'audit A-004 §5.4.

## 5. Ce que le papier NE PROUVE PAS — et l'échappatoire explicite

1. **Conditionnel** : le théorème principal suppose l'existence de PRG de
   dureté `2^{n^ε}` (vrai si factorisation/log discret durs). Ce n'est pas
   une impossibilité inconditionnelle.
2. **Ne s'applique qu'aux classes assez fortes pour contenir des PRF.**
   Pour ACC⁰, verbatim Williams (audit A-001) : « there is little evidence
   that ACC contains pseudorandom functions, so natural proofs may not be a
   barrier for ACC after all. »
3. **Les arguments de comptage/diagonalisation échappent à la naturalité** —
   verbatim :
   > « a consequence of Theorem 4.1 is that if our pseudo-random generator
   > assumption is true then such C*_n cannot exist at all! Thus, a counting
   > argument is presumably not a natural argument. »
   C'est précisément l'échappatoire empruntée par Williams 2011
   (diagonalisation + complétude). La barrière elle-même désigne sa sortie.
4. **Rien sur les preuves monotones** : le papier vise les modèles
   non-monotones (les bornes monotones de Razborov 1985 ne tombent pas sous
   RR — elles tombent sous Tardos, cf. A-003).

## 6. Statut de barrière (lecture pour l'Atlas)

Barrière #2 du cahier (§1). Test opérationnel issu de l'audit :

> Si l'argument de borne inférieure repose sur une propriété de la table de
> vérité qui est (i) décidable en temps `2^{O(n)}` ET (ii) vraie pour une
> fraction ≥ 2^{−O(n)} des fonctions, ET (iii) la classe visée contient
> plausiblement des PRF (P/poly, TC⁰ — Naor-Reingold), alors l'argument
> casserait la crypto standard : il est presumé impossible.

Trois sorties documentées : (a) propriété non-large (fonction unique ou
famille petite — la plupart des tours 12-20 du dépôt), (b) propriété
non-constructive, (c) classe sans PRF (ACC⁰) ou argument par
diagonalisation/comptage (Williams).

## 7. Lien à la bibliographie §7 du cahier et aux tours du dépôt

- §7.1 deuxième entrée — l'audit ajoute les définitions et le théorème
  verbatim.
- **Tours 12-20** : le cahier note « RR : propriété pas large » pour chaque
  ÉTABLI — conforme à la sortie (a). Le « signal d'alarme » du Tour 19
  (propriété constructive et large à 36 % sur n=4) était le bon réflexe :
  c'est exactement le profil que RR interdit *si* on en tirait une borne
  générale.
- **Tour 6** (β_i Stanley-Reisner) : invariant constructif et large —
  l'alerte RR du cahier (§3, q.7) est validée par les définitions exactes.
- **A-004** : Razborov-Smolensky naturalise — la méthode polynomiale
  modulaire ne peut pas être poussée au-delà des classes sans PRF.
- Cellule Atlas « ligne RR » : test des 3 conditions + 3 sorties (a)/(b)/(c).

## Limitations de l'audit

- La version auditée est le PS de 1999 sur la page de Razborov, qui peut
  différer marginalement de la version JCSS 1997 (pagination, remarques).
- Le théorème 4.1 (construction du test statistique depuis C*_n) est cité
  par son énoncé ; la preuve (découpage du générateur, hybrides) n'est pas
  extraite en détail.
