# A-002 : Audit — Beigel & Tarui, « On ACC » (1994)

> Tâche type A. Exécutée le 2026-06-09.
> **Particularité de sourçage** : le fichier original (`bt-acc-cc.PS.gz`,
> page de Beigel à Temple, dvips 1995) a été téléchargé mais est en polices
> bitmap Type 3 — texte non extractible. Les énoncés exacts ci-dessous
> proviennent de **deux sources vérifiées** : (a) l'abstract Springer
> ([doi:10.1007/BF01263423](https://doi.org/10.1007/BF01263423)) ;
> (b) S. Buss, *« Uniform Proofs of ACC Representations »* (Archive for
> Mathematical Logic, 2017 — [PDF UCSD](https://mathweb.ucsd.edu/~sbuss/ResearchWeb/uniformACC/uniformACC.pdf),
> **32 pages greppées en texte intégral**), qui re-démontre le théorème avec
> énoncés complets. Toute citation « > » ci-dessous vient de Buss sauf
> mention contraire.

## 1. Référence canonique

- R. Beigel, J. Tarui, *« On ACC »*, computational complexity, vol. 4, no. 4,
  1994, pp. 350-366. [doi:10.1007/BF01263423](https://doi.org/10.1007/BF01263423).
- Version conférence : FOCS 1991.
- Améliore Yao 1985 (version probabiliste) ; analyse et améliore les
  *modulus-amplifying polynomials* de Toda 1991 et Yao 1985 (abstract
  Springer).

## 2. Théorème principal — énoncé exact (forme Buss, Theorem 2)

> « Fix d and m ≥ 2. Suppose C is a depth d ACC circuit of size S which uses
> MOD m gates. Then there is an equivalent circuit C′ of size
> 2^{(log S)^{O(1)}} of depth two. The first level of C′ contains ∧ gates of
> fanin (log S)^{O(1)} and the output gate is a symmetric gate. The constants
> implicit in the O(1) terms in the bounds on size and fanin are independent
> of S, but do depend on d and m. Note that C′ is quasipolynomial size, not
> polynomial, size. »

Forme polynomiale équivalente (abstract Springer) : il existe des polynômes
`p_n` **sur ℤ** de degré `log^{O(1)} n` et **à coefficients de magnitude
`2^{log^{O(1)} n}`** tels que le circuit se réduit à une fonction symétrique
appliquée à `p_n`.

Forme intermédiaire (Buss, Theorem 1, m premier — équivalente à
Razborov-Smolensky) : profondeur 3 avec niveau ∧ polylog, niveau MOD_m,
sommet symétrique (approximate majority possible).

## 3. Hypothèses non-triviales

1. **m et d constants** : les exposants O(1) dépendent de (d, m). La
   transformation explose si d ou m croissent.
2. **Quasi-polynomial, pas polynomial** : `2^{(log S)^{O(1)}}` — c'est
   suffisant pour l'évaluation rapide de Williams mais pas anodin
   (Buss cite Barrington : « quasipolynomial size is more natural than
   polynomial size » pour ces classes).
3. **Uniformité** : la version originale est non-uniforme mais C′ est
   descriptible uniformément depuis C (« direct connection ») — c'est
   l'objet du papier de Buss 2017.

## 4. Outils techniques

- **Modulus-amplifying polynomials** (Toda 1991, Yao 1985, améliorés par
  Beigel-Tarui) : transforment un test mod m en un test à plus forte marge —
  c'est le cœur technique qui élimine les portes MOD_m au profit d'une
  unique fonction symétrique.
- Composition avec la dérandomisation de la construction probabiliste de
  Yao 1985.
- Chez Buss : forme relativisée du théorème de Toda + traductions
  Furst-Saxe-Sipser / Paris-Wilkie (preuve uniforme).

## 5. Ce que le papier NE PROUVE PAS

1. **Aucune borne inférieure** : c'est un théorème de *structure/simulation*
   (ACC ⊆ SYM+ quasi-poly), pas une borne. La borne vient 17 ans plus tard
   (Williams 2011) en *exploitant* cette structure algorithmiquement.
2. **Rien pour TC⁰** : la transformation repose sur l'arithmétique modulaire
   des portes MOD_m (modulus amplification). Les portes majority/threshold
   n'admettent **aucun analogue connu** — c'est exactement l'obstacle
   quantifié par notre tâche F-001 (IP ∈ TC⁰ d=2 a une weight PTF
   exponentielle ; et même en représentation exacte, pas de SYM+
   quasi-polynomial connu pour TC⁰).
3. **Les coefficients sont de magnitude quasi-polynomiale `2^{log^{O(1)} n}`**,
   pas polynomiale — la distinction L∞/L1/magnitude (cahier q.13) s'applique
   aussi ici : c'est la *combinaison* degré polylog × magnitude quasi-poly ×
   évaluation par fonction symétrique qui rend l'algorithme de Williams
   possible, pas une simple « petitesse » des coefficients.

## 6. Lien à la bibliographie §7 du cahier

Cité au §7.2 via l'audit Williams (A-001). À ajouter comme entrée propre si
souhaité. La chaîne exacte : Yao 1985 (probabiliste) → Beigel-Tarui 1994
(déterministe, m composite) → Allender-Gore 1994 (uniforme, application au
Permanent) → Williams 2011 (borne via algorithme) → Buss 2017 (preuve
uniforme unifiée).

## 7. Lien aux tours et tâches du dépôt

- **A-001 (Williams 2011)** : Lemma 4.1 de Williams = ce théorème (cité
  comme « a powerful result of Yao, Beigel-Tarui, and Allender-Gore »). C'est
  la moitié « algorithme » de la méthode.
- **Tour 23, point (d) de la réfutation** : confirmé une seconde fois — la
  représentation est une fonction **symétrique** de ANDs sur ℤ (exacte),
  pas une PTF à seuil. Les mesures `tcomp`/weight du Tour 23 et de F-001
  ne mesurent donc pas la « bonne » quantité pour reproduire Beigel-Tarui
  sur TC⁰ — il faudrait une représentation exacte symétrique, dont
  l'inexistence pour TC⁰ est l'obstacle du programme.
- **Cellule Atlas « méthode Williams × extension TC⁰ »** : 3 pièces
  désormais réunies — (i) Beigel-Tarui spécifique MOD_m (cet audit),
  (ii) F-001 (weight PTF exponentielle pour IP), (iii) Williams A-001
  (« this part of the proof does not use any specific properties of ACC »
  pour la moitié connexion — donc le manque est *entièrement* du côté
  algorithme/représentation).

## Limitations de l'audit

- Source primaire illisible (PS bitmap 1995) — énoncés pris de l'abstract
  Springer et de Buss 2017 (re-preuve rigoureuse). Les pages 350-366 de la
  version journal n'ont pas été lues directement.
- Les détails des modulus-amplifying polynomials (degrés exacts, constantes)
  ne sont pas extraits — disponibles dans Buss §3 si besoin.
