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

## 0. TEXTE PRIMAIRE LU — mise à jour A-002b (2026-08-02)

> **La limitation de sourçage ci-dessus est levée.** Le texte intégral a été
> obtenu par l'utilisateur (OCR, déposé en
> [pdf/beigel_tarui_1994_on_acc_ocr.txt](pdf/beigel_tarui_1994_on_acc_ocr.txt),
> 17 pages, artefacts OCR : barres de négation, ligatures et symboles de
> relation perdus — sens toujours reconstituable par le contexte). **Deux
> lectures indépendantes concordantes** ([A-002b](../tasks/done/A-002b.md)).
> Les numéros de ligne ci-dessous renvoient au fichier OCR.
>
> **Même jour** : la source (b) est désormais elle aussi conservée au dépôt —
> [pdf/buss_2017_uniformACC.pdf](pdf/buss_2017_uniformACC.pdf) (+ texte
> extrait, 32 pages), fournie par l'utilisateur. Le verbatim du Théorème 2
> cité au §2 ci-dessous a été **re-vérifié mot pour mot** sur ce texte
> (l. 78-85 de l'extraction) : les citations de juin sont exactes et
> re-vérifiables.

Ce que le texte primaire établit, et qui corrige ou précise les sections
suivantes (rédigées en juin sur Buss + abstract) :

1. **La définition OFFICIELLE de SYM+ est POLYNOMIALE, pas circuit**
   (l. 67-73) : familles de polynômes **sur ℤ** de degré log^{O(1)} n et de
   norme 2^{log^{O(1)} n}, avec h_n : ℤ → {0,1}. La **norme** est définie
   l. 64-65 : « *the sum of the absolute values of the coefficients* » — L1,
   **coefficients signés admis nativement**. La forme circuit du §2 ci-dessous
   (Buss Thm 2) n'est chez Beigel-Tarui qu'une équivalence « *by standard
   techniques of Beigel et al. (1994)* » (l. 76-79). Et les auteurs tranchent
   la bonne vue (l. 96-99) : « *it seems more useful to think of SYM+ in terms
   of low-degree polynomials as opposed to depth-two circuits (hence our
   definition of SYM+ above)* ».
2. **La forme circuit admet les littéraux NIÉS** — trois passages :
   l. 79-82 « *A NOT gate can appear in a circuit as a negated input literal
   x̄ᵢ* » (parenthèse attachée à la caractérisation profondeur 2) ; l. 141-142
   (tête de §2) « *we assume without loss of generality that NOT gates in a
   circuit only appear as negated input literals* » ; l. 335-336 (Lemme 2.5,
   niveau du bas) « *using (1 − xᵢ) for each negative literal* ».
   **Conséquence pour la ligne 7 et le fil SYM∘AND (A-013)** : la convention
   d'origine de Beigel-Tarui est littéraux + signés ; la variante « variables
   seules, multiplicités ≥ 0 » mesurée par le dépôt est celle de **Williams**
   (J. ACM 2014, p. 2:6 et 2:15) — les deux coexistent (note 3 de Williams),
   inter-convertibles à taille quasi-polynomiale, PAS à nombre de portes
   (écart exponentiel mesuré, A-013).
3. **Uniformité — le §3.3 ci-dessous est à nuancer** : le papier primaire
   revendique lui-même une version uniforme (l. 100-102, méthode
   Valiant-Vazirani via Toda), la preuve auto-contenue étant la version non
   uniforme (l. 102-107). L'apport de Buss 2017 est la preuve uniforme
   *unifiée*, pas la première revendication d'uniformité.
4. **TC⁰ — le §5.2 ci-dessous est INCOMPLET** : la **Remarque 2.11**
   (l. 542-550) pose explicitement la question d'extension avec une condition
   suffisante chiffrée : Théorème 1.1 tient encore pour m = log^{O(1)} n à
   O(1) facteurs premiers distincts ; et « *if we allow O(log n/log log n)
   distinct prime moduli of magnitude O(log n), any symmetric Boolean function
   on n variables can be computed by a circuit of the form: an OR at the root,
   at most n ANDs of fan-in O(log n) at the next level, and
   O(log² n/log log n) MODs at the bottom. Thus if a similar result holds in
   this case, then TC0 [...] is contained in SYM+* ». La question d'extension
   du verrou de la ligne 7 est donc posée **dans le texte primaire de 1994**.
   S'y ajoute la **Proposition 1.2** (l. 112-115) : porte symétrique admise au
   sommet du circuit d'ENTRÉE (pas seulement MOD_m).
5. **Modulus-amplifying — les degrés exacts manquants au §« Limitations »**
   (l. 127-137, 402) : Toda degré Θ(k²), Yao degré Θ(k^{log₂ 3}),
   Beigel-Tarui **2k−1, optimal** (par inversion de série formelle + restes
   chinois dans ℤ[x]).
6. **Exposants explicites** (Remarque 2.9, l. 514-531) : pour un circuit de
   profondeur d, le degré final est log^β n avec β = 2^{d+1}−2
   (Razborov-Smolensky non constructif) ou β = 2^{d+2}−3 (Valiant-Vazirani).
   Et la **Remarque 2.10** (l. 532-541) donne la forme de h_n : seuil de
   modulos emboîtés, améliorable en « Mid-Bit » (Green et al. 1992).

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

- ~~Source primaire illisible (PS bitmap 1995)~~ — **LEVÉE le 2026-08-02**
  (§0 ci-dessus) : texte intégral lu via l'OCR fourni par l'utilisateur, deux
  lectures indépendantes concordantes. Réserve résiduelle : artefacts OCR
  (barres de négation, exposants, symboles de relation) — les verbatims cités
  au §0 sont reconstitués par contexte et le fichier source est conservé pour
  re-vérification.
- ~~Les détails des modulus-amplifying polynomials ne sont pas extraits~~ —
  **LEVÉE** : degrés exacts au §0 point 5 (2k−1, optimal).
