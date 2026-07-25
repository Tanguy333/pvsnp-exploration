# Atlas des impasses — matrice barrières × approches pour P vs NP

> **Livrable central du dépôt** (tâche ATLAS-001, assemblée le 2026-06-09 ;
> en-tête recâblé le 2026-07-25, tâche ATLAS-007). Pièces du dépôt au
> 2026-07-25, comptées : **27 tours adverses** (30 fichiers,
> [`../tours/`](../tours/) — démarrage 2026-05-23), **22 fiches dans
> [`../bib/`](../bib/)** — pour la plupart des audits sur textes, mais le
> dossier contient aussi une veille, un pointeur d'antériorité, une réponse
> d'auteur et un statut bibliographique : ce ne sont donc pas 22 audits de
> texte —, **4 cellules barrières** ([`../barriers/`](../barriers/)),
> **169 fiches de tâches** ([`../tasks/done/`](../tasks/done/)),
> **188 scripts** ([`../checks/`](../checks/)) et **12 jeux de mesures**
> ([`../data/`](../data/)).
>
> **Ce que les cellules citent — et ce qu'elles ne citent pas.** Chaque cellule
> renvoie à ses pièces *écrites* (audit `bib/`, cellule `barriers/`, fiche
> `tasks/done/`, archive de tour), et plusieurs de ces fiches sont des fiches
> de mesure (lignes 7 et 14). Ce qu'aucune cellule ne fait, c'est renvoyer au
> **code** : sur les 15 lignes, **une seule** cite un fichier de `data/` — la
> ligne 11, vers [`../data/weight_tc0_d2.csv`](../data/weight_tc0_d2.csv) — et
> **aucune** ne nomme un script exécutable de [`../checks/`](../checks/) ni ne
> donne sa commande (compté le 2026-07-25). L'ancienne mention « chaque cellule
> renvoie à sa pièce » était fausse pour le code et a été retirée. Le chaînage
> *cellule → script → commande → sortie attendue* est désormais porté à part,
> par [`temoins.md`](temoins.md) (tâche ATLAS-010, 2026-07-25 : 17 scripts sur
> 188, 18 lignes) — pas encore par les cellules elles-mêmes.
>
> **Portée des mesures de ce dépôt.** Les chiffres cités dans les cellules sont
> exacts et certifiés *dans leur régime* — mais ce régime est petit (solveur
> exact à ~10 variables, réseaux exacts à n ≤ 8), alors que les phénomènes visés
> commencent deux à dix ordres de grandeur plus haut (ligne 14 : premier contenu
> de la borne symétrique à n = 41, croisement prouvé sym/asym à n ≈ 4050 ;
> ligne 7 : seuil quasi-polynomial 2^{polylog n}). Une mesure hors régime est
> *vraie et hors sujet*, et rien dans sa forme ne le signale. Lire
> [`echelle_instrument.md`](echelle_instrument.md) — deux témoins chiffrés et le
> contrôle positif qui en découle — **avant** d'utiliser un chiffre de cette
> matrice comme argument de portée.
>
> **Incohérence interne connue, à corriger dans le même commit.** Les comptes
> ci-dessus font foi au 2026-07-25 ; deux passages plus bas dans ce fichier
> sont restés à l'état du 2026-06-09 et les contredisent : « Inventaire des
> pièces » (« Archives des **25** tours », « **~30** scripts `checks/` »,
> 2 mesures exécutables, 12 fichiers `bib/` listés) et « Les trois lectures »
> §3 (« Les **25** tours du dépôt se classent sans reste », dont l'énumération
> **omet les Tours 26 et 27**, à rattacher à la ligne 7).
>
> **Lecture** : ✖ = l'approche est tuée par cette barrière (témoin connu) ;
> ✓ = barrière franchie ou évitée (avec le mécanisme) ; ◌ = sans objet
> structurel ; ⚠ = exposée/présumée ; — = non analysé. La colonne
> « Verrou réel » donne ce qui bloque *effectivement* l'approche aujourd'hui.

## La matrice

| # | Famille d'approches | Relativisation (BGS 1975) | Preuves naturelles (RR 1997) | Algébrisation (AW 2008) | Monotone (Tardos 1988) | **Verrou réel** |
|---|---|---|---|---|---|---|
| 1 | **Diagonalisation / simulation pures** | ✖ oracles A, B contradictoires ([bib/bgs_1975.md](../bib/bgs_1975.md)) | ◌ (pas une propriété — [A-007 §5.3](../bib/razborov_rudich_1997.md)) | ✖ a fortiori (AW généralise BGS) | ◌ | BGS : la technique est boîte-noire par essence |
| 2 | **Méta-complexité naïve (Kt, compressibilité)** | ✖ Kt relativise — Tour 1 ([tours/tour_01](../tours/tour_01_kolmogorov.md)) | — | ✖ | ◌ | Circularité conditionnel/inconditionnel + BGS |
| 3 | **Arithmétisation pure (sumcheck, IP=PSPACE)** | ✓ ne relativise pas | ◌ | ✖ tout ce qui arithmétise algébrise — témoin NP^Ã = P^A ([bib/aaronson_wigderson_2008.md](../bib/aaronson_wigderson_2008.md)) | ◌ | AW : il faut exploiter la structure au-delà du bas degré |
| 4 | **Méthode polynomiale modulaire (Razborov-Smolensky)** | ✓ combinatoire | ⚠ naturalise (exemple canonique RR — [bib/razborov_rudich_1997.md §4](../bib/razborov_rudich_1997.md)) | ◌ | ◌ | **Modules composés** : « AC⁰[6] vs Majority » ouvert depuis 1987 — verbatim Goldreich 2023 : « *In contrast, we do not know a proof of the equally intuitive conjecture that AC0[6] cannot compute Majority* » ([bib/razborov_smolensky_1987.md §5](../bib/razborov_smolensky_1987.md)) ; motif structurel : le **Pas 1** de la méthode approxime les circuits par des polynômes de bas degré **sur le corps GF(p)** — Z₆ n'est pas un corps. **Contenu mesuré du dépôt sur cette cellule** : fil F-011, **33 fiches** (F-009, F-010 et 31 fiches `F-011-etape*` — les étapes 16 et 23 n'en ont pas ; le compteur du backlog dit « 33 étapes », les deux 33 coïncident par accident) et **39 scripts** `checks/`, synthèse [notes/front_composite.md](../notes/front_composite.md) — le tout dans le modèle-jouet « **représentation faible mod 6** » (zéros forcés + couverture), analogue composite du Pas 1 **réduit à UN polynôme**. ▸ **RÉPLIQUÉ** (à distinguer explicitement du neuf ; requalifications faites par audit) : l'effondrement composite de OR (n = 18 : mod 2 → 18, mod 3 → 9, **mod 6 → 3** ; degré 9 encore à n = 144 — [B-005](../tasks/done/B-005.md)) est **BBR 1994, Thms 2.1-2.2** ; le « Théorème D » du fil (périodicité, deg₃^sym ≥ 3^b) **est** l'argument de **BBR Thm 2.2** spécialisé à m = 3, requalifié réplication ([bib/bbr_1994.md](../bib/bbr_1994.md)) ; la croissance linéaire de MAJ mod 6 symétrique mesurée en [F-009](../tasks/done/F-009.md) relève du **Thm 4.9 de BGL 2003**, lu verbatim : « *Every symmetric polynomial weakly representing the threshold function T_k over Z_pq has degree Ω(max(k, √n)) for k ≤ n/2* » ([bib/bgl_2003_sun_2020.md](../bib/bgl_2003_sun_2020.md)) ; Lemmes 1-2 du fil (noyau de Mahler, fenêtre glissante) = **folklore** ; le modèle **fort** est un domaine actif (Sun et al. ICALP 2020 : deg₆ ≥ 2n/7 symétrique) — le « Théorème L » du dépôt n'y est qu'un calcul d'instance. ▸ **PROUVÉ par le dépôt** (preuve écrite + vérification exécutable indépendante ; **aucune relecture externe**, et « non trouvé » ≠ « nouveau » — folklore-check dédié requis avant toute diffusion : [§9bis](../notes/front_composite.md) pour le modèle symétrique, et surtout **[§10bis](../notes/front_composite.md) pour le modèle GÉNÉRAL**, dont l'antériorité est explicitement NON auditée — thèse de Gopalan 2006 et « The Degree of Threshold mod 6 and Diophantine Equations », cf. [bib/bgl_2003_sun_2020.md §3](../bib/bgl_2003_sun_2020.md), « ce qui reste à auditer AVANT toute revendication sur le modèle général ») : loi exacte `deg₃^sym(OR_n) = max(3^b, n − 3^b)` avec b = ⌊log₃ n⌋, **prouvée des deux côtés** pour tout n (descente → périodicité → paires interdites → interpolation de Mahler) ; forme close exacte de `deg₂^sym(THR_{t,n})` pour toute la famille (probablement dérivable de la littérature ANF, Canteaut-Videau 2005) ; `deg₆^sym(MAJ_32) = 27`, certificat `e₁₆+e₁₈+e₂₅+e₂₇ mod 3` ; et dans le modèle **général** (restriction symétrique levée) **trois familles infinies** `deg₆(THR_{t,2t}) = t` — **K** (t = 2^a), **K′** (t = 2·3^k), **K″** (t = 3^k) — plus la classification complète de la frontière bipartite t ≤ 27 (solubles = {2,3,4,5,6,8,9,12,16,18,27}). ▸ **MESURÉ** : `deg₆^sym(MAJ_65) = 40 = (3⁴−1)/2` par énumération exhaustive des deux côtés — ce qui **réfute** la loi conjecturée du fil (artefact du domaine d'ajustement n ≤ 44) ; plateaux mesurés autour de la zone v2, que la note fixe à t = 33..40 : t = 28..31 → 32, t = 32 → 36, t = 33..35 → 40 = (3⁴−1)/2, t = 36 → 44, t = 37 → 46, et **t ≥ 38 → > 50, cap de l'outil** ; l'avantage composite meurt **dès t = 2** (d₆ saute de 3 à 8-9 : falaise, pas pente — [F-010](../tasks/done/F-010.md)) ; et **la plate `deg₆(MAJ_n) = ⌈n/2⌉`**, soit exactement la borne triviale de Möbius, **confirmée n = 4..25, 29, 31, 32** (les 4 trous n = 26-28, 30 sont une **frontière d'outil**, pas un verdict ; la plate au-delà reste **CONJECTURE**). ▸ **CAVEAT, déjà écrit dans la note §1 et dans [F-009](../tasks/done/F-009.md) : « polynôme unique ≠ circuit AC⁰[6] »** — ces mesures sondent la portée de la méthode polynomiale mod 6 sur MAJ, **pas** la conjecture de circuits. ▸ **VERROU RÉEL, INCHANGÉ DEPUIS 1987 — OUVERT.** *Pourquoi le fil s'arrête — le motif porteur est le CAVEAT ci-dessus, et lui seul est inconditionnel* : le Pas 1 de Razborov-Smolensky est une **approximation PROBABILISTE** de circuits, tandis que tout ce fil mesure des **représentations EXACTES** par un polynôme unique ; aucune valeur exacte de degré, à aucun n, ne borne donc un circuit AC⁰[6]. Cet argument ne dépend d'aucune mesure. *Motif d'appoint, étiqueté pour ce qu'il est* : la plate MESURÉE (n ≤ 32, 4 trous) et les trois familles PROUVÉES K/K′/K″ **indiquent** que le modèle faible mod 6 général n'offre aucun gain composite sur MAJ — indication convergente, **non théorème** : hors K ∪ K′ ∪ K″ et au-delà de n = 32 la plate reste CONJECTURE, les t insolubles (7, 10, 11, 13, 14, 15, 17, 19…) n'ont de certificats que jusqu'à n = 24, et rien n'est établi pour THR_{t,n} avec n ≠ 2t. Ce qui manque est un analogue composite de l'**approximation** — ou un modèle plus contraint (fort, probabiliste, circuits) — que ce fil ne fournit pas ; à noter que [notes/front_composite.md §8.4](../notes/front_composite.md) porte encore la thèse inverse (« lever la restriction symétrique … chaque étage rapproche du vrai mur de 1987 »), abandonnée par la présente clôture (ATLAS-011) |
| 5 | **Bornes monotones / tropicales / min-plus** | ✓ | ◌ (RR vise le non-monotone) | ◌ | ✖ **témoin θ̄-perturbée ∈ P à complexité monotone exp(n^{1/6})** ([bib/tardos_1988.md](../bib/tardos_1988.md)) ; tropical = monotone arith. (Jerrum-Snir, [Tour 24](../tours/tour_24_tropical_refutee.md)) | Tardos : le gap est intrinsèque au modèle, pas à la dureté |
| 6 | **Combinatoire profondeur 2 / DNF-MIN (Tours 12-22)** | ✓ | ✓ propriétés non-larges (fonctions uniques) | ◌ | ◌ | **Sans portée** : AC⁰ d=2 ⊊ P connu depuis FSS 1981 ; 8/9 objets folklore ([cahier §3 audit](../cahier_de_bord.md)) ; seul L18 non recensé ([bib/l18_status.md](../bib/l18_status.md)) |
| 7 | **Méthode algorithmique (Williams 2011)** | ✓ **démontré** — oracle NEXP^A ⊂ ACC^A ([bib/williams_2011.md §6](../bib/williams_2011.md)) | ✓ double sortie ([barriers/williams_vs_rr.md](../barriers/williams_vs_rr.md)) | ✓ **démontré** (même oracle, version algébrique) | ◌ | **Extension — verrou RÉÉCRIT le 2026-07-25 (VEILLE-2026-2), l'ancienne rédaction « aucun algorithme SAT non-trivial au-delà d'ACC⁰ » était FAUSSE depuis 2014** : la frontière des algorithmes SAT/#SAT non triviaux a dépassé ACC⁰ dès 2014 et bouge encore — ACC∘THR et ACC∘SYM, #SAT en 2^{n−n^ε}, d'où NEXP ⊄ quasi-poly ACC∘THR (Williams, STOC 2014, p. 194-202 ; arXiv:1401.2444) ; ACC⁰∘3-PTF par rang probabiliste (Limaye-Srinivasan-Srinivasan, MFCS 2025, LIPIcs 345, 67:1-67:18) ; THR∘THR de taille n^{2.5−ε} pour une fonction de E^NP (Chen-Tal-Wang, ECCC TR26-039, 2026-03-14 ; antérieurement sous-quadratique : Tamaki ECCC TR16-100, Alman-Chan-Williams FOCS 2016). Le verrou réel n'est donc pas « aucun algorithme » mais **le régime des bornes obtenues** : classes uniformes énormes (NEXP, E^NP), profondeur 2 ou une seule couche de seuils, et taille encore polynomiale (n^{2.5−ε}) là où TC⁰ de profondeur ≥ 3 reste entièrement hors d'atteinte ([bib/veille_2026_07.md](../bib/veille_2026_07.md) §1). Précision (F-003) : la transformation Beigel-Tarui manquante pour TC⁰ concerne les portes **THR à poids non bornés** (objets-frontière : THR∘THR) — IP est *trivial* en SYM∘AND (= PARITY∘AND₂, poids k, prouvé optimal) ; ce dont IP témoigne est la weight **PTF** exponentielle : 20→119→640, et exactement (3^k−1)/2 par T-F006 ([tasks/done/F-001.md](../tasks/done/F-001.md), [F-006](../tasks/done/F-006.md), [F-003](../tasks/done/F-003.md)). — **Sonde exécutable du dépôt sur ce verrou : le fil SYM∘AND (18 tâches — F-012..022, T26-S1..S4, T27-S1..S3), CLOS le 2026-07-25 sur un résultat NÉGATIF quant à la mesure.** *Ce qu'il laisse* : **U26.1** (PROUVÉ — [Tour 26 §1-2 pour la formule, §5 pour la borne O(k²)](../tours/tour_26_indicateur_modulaire_survit.md)) : l'indicateur modulaire donne W(SYM_k(g^k)) ≤ k·Σ_S (ĝ_S mod k), soit **O_g(k²)** à bloc monotone g fixé ; et des **valeurs exactes** : W_dec(MAJ_k(OR2^k)) = k(k+1) pour **k = 3..9** dans la classe décomposable (MESURÉ, exhaustif sans solveur mais **sous le plafond consigné w_bloc ≤ cible − 2(k−1)** — [T26-S1 §2](../tasks/done/T26-S1.md), le point k = 9 en 15 884 s), **W(MAJ₅(OR2⁵)) = 30 sur l'ESPACE ENTIER des 1023 monômes** (MESURÉ, certifié-solveur : 11 barreaux UNSAT, ~3 h 20 de CP-SAT, moteur étalonné des deux côtés sur les vérités terrain k = 3 et k = 4 — mais un UNSAT de CP-SAT **n'est pas re-vérifiable par énumération**, il est obtenu **sous cassage de symétrie lex-leader dont l'échelle dépend entièrement**, et **sans certificat DRAT**, jamais tenté : statut consigné en [T27-S2 §4](../tasks/done/T27-S2.md)), **W(THR₃(OR2⁴)) = 20** et **W(MAJ₃(MAJ3³)) = 12** (même moteur, mêmes réserves de solveur, étalonné sur MAJ₃(OR2³) = 12 — [T27-S3](../tasks/done/T27-S3.md)), **IP_8 = 4** ([notes/symand_synthese.md](../notes/symand_synthese.md) §2) ; plus trois bornes ∀k en sous-classes (isotypique ; minima ≡ 1 ; minima égaux à seuil ≥ majorité), avec le mécanisme **nommé** — somme nulle modulo le minimum, constante de Davenport / EGZ ([T26-S2](../tasks/done/T26-S2.md), [T26-S3](../tasks/done/T26-S3.md), [T26-S4](../tasks/done/T26-S4.md)). *Portée exacte de ces valeurs* : sur l'espace entier des monômes, la loi k(k+1) n'est certifiée qu'à k = 3, 4, 5 ; hors classe décomposable et au-delà, elle reste une CONJECTURE. **Et voici le point qui décide de la cellule, sans le sur-vendre : aucune de ces valeurs ne peut témoigner du verrou.** Le verrou est le seuil **quasi-polynomial** de Beigel-Tarui, 2^{(log S)^{O(1)}} — soit **≈ 1,9 × 10¹³ à n = 100**, chiffre qui résulte d'une **instanciation choisie par le rédacteur** (O(1) := 2 et S := n, d'où 2^{(log₂ 100)²}) et non du théorème, et qui est minorant puisque S ≥ n ; la famille mesurée est plafonnée **polynomialement** par U26.1 (n²/4 + n/2 = 2 550 à n = 100) — **~10 ordres de grandeur d'écart, et cela pour tout k**. C'est un résultat NÉGATIF sur l'instrument, pas sur l'approche : le verrou énoncé plus haut est inchangé, et aucune valeur exacte de W ne le déplacera. **Réserve de portée, à ne pas escamoter : DEUX divergences de convention entre le modèle mesuré et le format visé, relevées toutes deux dans le même audit [bib/beigel_tarui_1994.md](../bib/beigel_tarui_1994.md) §2.** *(1) Littéraux* : le modèle mesuré n'admet que des monômes **positifs**, et la question « le format Beigel-Tarui autorise-t-il les ∧ sur littéraux ? » est **[NON TROUVÉ]** — l'énoncé dont le dépôt dispose est le **Théorème 2 de Buss 2017** (re-preuve uniforme ; le texte primaire de Beigel-Tarui n'a pas été lu, source PS 1995 en polices bitmap non extractible), verbatim « ∧ gates of fanin (log S)^{O(1)} », tandis qu'une source secondaire consultée le 2026-07-25 paraphrase au contraire « ANDs **of variables** », ce qui validerait le modèle du dépôt : la question reste **OUVERTE dans les deux sens**. Si les ∧ sur littéraux étaient admis, Σᵢ (¬xᵢ ∧ ¬yᵢ) sépare au poids k (énumération exhaustive, k = 3..8), soit un facteur ≥ 6 dès k = 5. *(2) Signes* : le même audit relève, dans l'abstract Springer, des polynômes **sur ℤ** — donc à coefficients **SIGNÉS** — là où le modèle du dépôt impose des coefficients entiers **≥ 0**. Conséquence commune aux deux : les bornes **SUPÉRIEURES** du modèle transfèrent au format visé, ses bornes **INFÉRIEURES** ne bornent rien hors modèle tant que ces questions restent ouvertes. Chiffres et témoin : [`echelle_instrument.md`](echelle_instrument.md), témoin 2 |
| 8 | **GCT (permanent vs déterminant)** | ◌ documenté (A-011) : revendiqué 2× au conditionnel par Mulmuley (« *should be nonrelativizable* », §18 de 0709.0748 — pas de réduction Turing, constructions explicites) ; aucun théorème ([bib/gct.md](../bib/gct.md)) | ⚠ documenté (A-011) : violation revendiquée des DEUX conditions RR (§18.2-18.3) — largeness prouvée sur F_p SEULEMENT (« *We cannot prove this formally over C* », dépend de Deligne) ; constructivité circulaire avouée (« *a lower bound statement in itself* ») | ◌ présumé — aucune discussion AW dans les textes de Mulmuley audités ([NON TROUVÉ], seul l'argument structurel D-002 : [barriers/gct_vs_aw.md](../barriers/gct_vs_aw.md)) | ◌ | **Barrière interne BIP 2019 (texte intégral, A-011)** : Théorème 1.4 (n ≥ m²⁵) tue les occurrence obstructions par un mécanisme de plomberie — « *only the padding [...] is relevant* », aucune propriété du permanent utilisée ; même les power sums (Waring) inséparables par occurrences (note Wigderson). Multiplicités : réalisées UNIQUEMENT en cadres jouets (Chow vs Waring, DIP 2020 ; power sum vs produit, IK STOC 2020) — jamais det vs perm ; et les coefficients requis (Kronecker/plethysmes) sont eux-mêmes durs (positivité des caractères PH-dure, Panova 2023) : le paradoxe auto-référentiel du flip se reproduit un étage plus bas |
| 9 | **Complexité descriptive (CFI / FPC / CPT)** | ◌ | ◌ pour FPC — mais l'immunité = distance à P vs NP ([barriers/cfi_vs_rr.md](../barriers/cfi_vs_rr.md)) | ◌ | ◌ | **Aucune technique pour CPT ⊊ P** (les CFI ne témoignent pas contre CPT — DRR 2008, [bib/cfi_abd.md](../bib/cfi_abd.md)) ; transposition à SAT fermée ([Tour 25](../tours/tour_25_cfi_sat_refute.md), q.15) |
| 10 | **Hardness magnification (MCSP/MKtP)** | — (réductions relativisantes) | ✓ par construction (refuter les propriétés naturelles EST la stratégie) | — | ◌ | **Barrière de localité** : toutes les techniques connues localisent ([barriers/magnif_vs_locality.md](../barriers/magnif_vs_locality.md), CHOPRS 2020) |
| 11 | **PTF / threshold polynomials (Tours 23, F-001)** | ✓ ILP fini | ✓ fonctions individuelles | ◌ | ◌ | Instrument de mesure, pas une approche de séparation ; poly-weight ⊊ TC⁰ d=2 strictement (EXACT_k vs IP, [data/weight_tc0_d2.csv](../data/weight_tc0_d2.csv)) |
| 12 | **Invariants topologiques/homologiques sémantiques (Tours 3, 6, 7)** | ✓ | ✖ invariants constructifs et larges (Tour 6, q.7) | ◌ | ✖ pour les variantes monotones (Tour 7, test OR_n q.8) | Non-invariance sous équivalence logique + effondrement sous sauts polynomiaux (q.1, q.2) |
| 13 | **Programme méta-complexité moderne (Hirahara : MCSP, worst-case ↔ average-case non-boîte-noire)** | ✓ par construction — contournement *démontré* de la barrière boîte-noire Bogdanov-Trevisan (FOCS 2018) ; nuance : certains résultats sous oracle aléatoire seulement ([bib/meta_complexite.md](../bib/meta_complexite.md)) | ⚠ structurellement adjacent — MCSP *est* le problème au cœur de RR ; le programme en fait son objet (Kabanets-Cai) | — non analysé dans les sources | ◌ | **NP-complétude de MCSP exact ouverte depuis Levin (1971)** ; portée indirecte par essence : un succès complet exclut Heuristica et fonde les OWF sur P ≠ NP — restructure les mondes d'Impagliazzo **sans séparer P de NP** |
| 14 | **Polynômes toriques (BHLR 2019 → KV 2024) : MAJ ∉ ACC via degré torique** | — non discuté dans BHLR (vérifié : 0 occurrence ; machinerie héritée de Yao/Toda/Beigel-Tarui, cf. ligne 7 — [bib/bhlr_2019.md](../bib/bhlr_2019.md)) | ✓ selon les auteurs (§1.5 verbatim : prémisse d'inutilité — « *PRGs are not believed to be contained in* [ACC⁰] », même esquive que la ligne 7) ; **constructivité de la propriété OUVERTE** (leur Problem 1.9) | — non discuté dans BHLR (vérifié : 0 occurrence) | ◌ | **Voie symétrique-SV FERMÉE PAR CE DÉPÔT** : la Conjecture 5 de KV (∃ plus court vecteur avec γ_n = 1) est **fausse** — dans la bande d ≥ 17, tout vecteur minimal a bouts ±2 (cœur cyclotomique 2Φ₃+x, parité prouvée, énumération exhaustive par cellule, [V-053](../tasks/done/V-053.md)/[V-055](../tasks/done/V-055.md)) ; fermeture **confirmée par V. Krishan** (« *it rules out the shortest vector approach as stated in our paper* »). Reste la voie asymétrique (Conj. 3 BHLR, degré Ω(√n/log n)) : l'asymétrie aide prouvément pour Δ_w (KV) mais pas pour MAJ aux petits n (MILP exacts, [V-002](../tasks/done/V-002.md)) ([bib/krishan_2024.md](../bib/krishan_2024.md)). — **La voie asymétrique a un dossier : le fil AS (43 tâches, AS-001..043), jamais porté dans cette cellule avant le 2026-07-25.** Sa cible est la **Conjecture 13 de KV** — min_{Z ∈ ℤ^{2ⁿ}} ‖P(n,d)·(Z + MAJ_n/2)‖ ≥ 2^{n/2}/n^{O(1)} pour d = o(√n/log n) —, énoncé relevé **verbatim p. 31 dans [AS-001 §1](../tasks/done/AS-001.md)**, la voie asymétrique étant identifiée en [bib/kv_asym_extraction.md §4](../bib/kv_asym_extraction.md). Trois acquis. **(i) [AS-022](../tasks/done/AS-022.md) — PROUVÉ, inconditionnel** : C13 est vraie sur toute la tranche **d = O(log n)** (d ≤ K·log₂ n, toute constante K), par assemblage de deux briques prouvées **du dépôt** (AS-011, seuils duaux de sous-cube ; AS-004, padding (1,2,1) itéré) ; la perte 2^{3d/2} situe **précisément** la mort de la route padding à d ~ log n. C'est la première borne **du dépôt** à degré croissant — ses théorèmes antérieurs plafonnaient à d ≤ 3 constant —, et **aucune revendication de primauté n'est faite** : AS-022 §4 consigne noir sur blanc que « la réserve *folklore* reste à poser à Krishan » et que seul le §7 de KV (tranche Z = 0) a été balayé ; le folklore-check n'est donc **pas fait**, il est en attente d'un courrier resté sans réponse. **(ii) [AS-039](../tasks/done/AS-039.md) — THÉORÈME D'OBSTRUCTION, barrière interne AU DÉPÔT** — à distinguer des barrières internes de la lecture 2 (BIP 2019, CHOPRS 2020…), qui sont des résultats de la littérature : AS-039 §4 porte en toutes lettres la marque « [antériorité à auditer] ». Contenu : le coset nul (f = 0) vit dans le **même** réseau que le coset MAJ (mêmes λ₁, det, rang) et a Θ ≥ 1 à toute échelle, donc **aucune estimée n'utilisant que la géométrie du réseau ne peut prouver Θ < 1 pour le coset MAJ** — c'est l'énoncé exact d'AS-039 §1 ; Banaszczyk, comptage, lissage sont hors jeu seuls, et toute preuve doit passer par l'arithmétique du coset (les signes de Lucas). *Maillon à étiqueter* : le passage de là à « … ne peut prouver C13 » emprunte la reformulation « **C13 ⟺ le coset MAJ est un trou profond** » d'AS-039 §3, qui n'est **ni PROUVÉE ni MESURÉE** et n'est pas étiquetée dans la fiche. Géométrie MESURÉE à l'appui : λ₁(4Q) ≈ 3,0 → 3,96 (réseau dense, packing quasi constant, conjecturé → 4) alors que 4D croît comme 2ⁿ/poly. **(iii) [AS-042](../tasks/done/AS-042.md) + [AS-043](../tasks/done/AS-043.md) — MESURÉ** : loi d'échelle ln(1/ρ) = π/x − c(n,d), découverte sur les **deux** cellules d'AS-042 ((9,3) et (11,3)) puis **confirmée 6/6 par AS-043** (pentes ajustées 3,16-3,34 pour π = 3,142), d'où la reformulation **C13 ⟺ c(n,d) = O(polylog n)** : toute la conjecture réduite à un **scalaire par cellule**, mesuré dans la bande **[0,70 ; 1,49] sur 6 cellules** (r = 6..11, 4D de 3,0 à 357,6 — [AS-043 §2-3](../tasks/done/AS-043.md)), sans croissance détectable — mais AS-043 §4 note qu'une croissance lente en log n resterait **indétectable sur 3 valeurs de n**, et c'est précisément la bornitude asymptotique qui est l'estimée manquante, hors boucle. Au passage, la prédiction « facteur géométrique γ ≈ 9,5 par direction » est RÉFUTÉE (annulation éparse, portée par 2-3 directions et dépendante de la jauge de base). Synthèse envoyée à V. Krishan (2026-07-20) ; aucune réponse consignée à ce jour. **Ce que le fil AS ne fait pas — et le verrou de cette cellule est inchangé** : C13 reste **OUVERTE** (il faut passer de log n à √n/log n, c'est-à-dire récupérer 4^d par les couplages de parité), et le dossier AS est un résultat sur l'**instrument**, pas sur l'approche : son régime vit à n ~ milliers, hors de portée ([`echelle_instrument.md`](echelle_instrument.md), témoin 1) |

| 15 | **Complexité des preuves (programme Cook-Reckhow : NP ≠ coNP via bornes sur systèmes de preuves)** | ◌ sans objet structurel (pas de modèle oracle) — le programme est né comme repli finitiste post-BGS (« *attention shifted to a more finitistic setting* », [bib/proof_complexity.md](../bib/proof_complexity.md)) | ✓/✖ **la seule ligne dont la barrière-analogue est un THÉORÈME inconditionnel** : pas de transfert mécanique de RR (le comptage échoue — l'espace des petites preuves ~ l'espace des tautologies), trou ouvert 20 ans (Beame-Pitassi), comblé par **Pich-Santhanam FOCS 2019** : la conjecture de Rudich n'admet pas de preuves propositionnelles faisables (inconditionnel, non-constructif) + dichotomie EF (soit le programme circuits est infaisable dans EF, soit le programme Cook-Reckhow a des obstacles inhérents) — la barrière est auto-référentielle par essence (A-012) | — [NON TROUVÉ DANS LES SOURCES] | ✓ exploitée aux systèmes faibles (interpolation faisable = LA méthode de transfert monotone : Résolution, Cutting Planes) ; ✖ morte pour Frege/EF sous crypto (Krajíček-Pudlák 1998, RSA) | **AC⁰[p]-Frege ouvert** — l'analogue circuits est prouvé depuis 1987 (ligne 4, A-004) et la version preuve n'a AUCUNE borne (« *without any success. Thus the Cook-Reckhow program is also stalled* ») ; PV1 ⊬ bornes EF (inconditionnel) ; voie moderne : EF → P ≠ NP sous conditions S¹₂ (Pich-Santhanam 2023) — convergence avec la ligne 13 (OWF, anticheckers, apprentissage) |

## Les trois lectures de la matrice

### 1. Une seule ligne franchit les 4 colonnes : la ligne 7 (Williams)

Et son franchissement de relativisation + algébrisation est *démontré*
(oracle d'Aaronson), pas seulement argumenté. La raison structurelle, citée
du texte ([A-001](../bib/williams_2011.md)) : *« improvements over
exhaustive search necessarily exploit structure in instances that black-box
methods cannot see »*. Le coût : la borne ne descend pas sous NEXP, et
l'extension à TC⁰ exige un ingrédient algorithmique que personne n'a
(quantifié empiriquement par F-001 : la représentation à la Beigel-Tarui
n'existe pas pour TC⁰ d=2, IP en témoin).

### 2. Les barrières classiques ne sont plus le front

Les programmes vivants (lignes 7-10) ont tous, par construction, réglé leur
rapport aux 3 barrières classiques. Ce qui les bloque est **chaque fois une
barrière interne propre** : modules composés (ligne 4), algorithme SAT
manquant (ligne 7), BIP 2019 (ligne 8), absence de technique CPT (ligne 9),
localité (ligne 10). La méta-leçon : *toute stratégie assez précise pour
être exécutable engendre l'analyse de sa propre impossibilité*. Demander
« franchissez-vous les 3 barrières ? » est nécessaire mais très loin d'être
suffisant.

### 3. Les patterns d'échec du dépôt sont tous dans la matrice

Les 25 tours du dépôt se classent sans reste : Tours 1-2 (lignes 2-3),
Tour 3/6/7 (ligne 12), Tours 6-10 dérive (hors matrice — pas une approche
de P vs NP), Tours 12-22 (ligne 6), Tour 23 + F-001 (ligne 11), Tour 24
(ligne 5), Tour 25 (ligne 9). Aucun tour n'a travaillé les lignes 7, 8, 10
*avec une contribution technique* — ce sont les seules lignes où les
verrous réels sont des problèmes mathématiques ouverts identifiés plutôt
que des impossibilités démontrées.

**Mise à jour 2026-06 (fil V, hors-tours)** : la ligne 14 est la première
— et seule — cellule de la matrice dont le verrou a été **fermé par le
dépôt lui-même** (réfutation de la Conjecture 5 de KV, validée par un
auteur), et non documenté depuis la littérature. Coût observé : ~55 tâches
V, dont une longue dérive en théorie des nombres (V-040→V-050, consignée) ;
gain net pour P vs NP : une cellule fermée avec témoin exécutable, et la
25e-26e auto-corrections comme méthode (contrôle adverse avant diffusion).

## Zones génératrices de cibles (règle d'ouverture d'un Tour 26+, cf. CLAUDE.md §8)

Les seules cellules « ouvertes avec verrou identifié » — par ordre de
précision du verrou :

1. **Ligne 7, extension TC⁰** : trouver une représentation exacte
   évaluable-rapidement pour TC⁰ d=2 (le verrou est précis : F-001 + A-002
   montrent ce qui ne marche pas). Front de recherche mondial depuis 2011.
2. **Ligne 4, modules composés** : structure des polynômes mod 6 — front
   depuis 1987.
3. **Ligne 10, technique non-localisante** : une borne faible pour MCSP gap
   qui ne s'étende pas aux circuits-oracle small fan-in.
4. **Ligne 9, borne CPT** : au-delà du rang borné (DRR 2008).
5. **Ligne 8, multiplicity obstructions** : techniques de calcul de
   multiplicités au-delà de BIP 2019.
6. **Ligne 14, borne torique asymétrique (Conjecture 1.5 BHLR)** : la voie
   symétrique-SV est fermée (notre réfutation) ; le front est le degré
   asymétrique Ω(√n/log n) pour MAJ. Frontière mesurée ici : l'asymétrie
   n'aide pas MAJ à **n ≤ 7** (V-002 + ATLAS-003, MILP certifiés) — MAIS
   le contrôle positif ATLAS-005 montre que le gain asymétrique PROUVÉ
   pour Δ_w (KV) n'est **pas visible non plus à n ≤ 7**.
   **ZONE FERMÉE (ATLAS-006, 2026-07-23)** : la preuve de KV est
   EFFECTIVE (pigeonhole n^{(d+1)²} < 2^{⌈n/2⌉+1}, Lemme 3.7) et ses
   seuils sont calculés — la borne symétrique est **VIDE pour tout
   n ≤ 40** (ce qui explique structurellement ATLAS-005 : le théorème
   ne dit rien à n ≤ 7), premier contenu à n = 41, et le **croisement
   prouvé sym/asym n'apparaît qu'à n ≈ 4050** — trois ordres de
   grandeur au-delà de l'instrument (n ≤ 8). Le no-man's land
   8 ≤ n ≤ ~4000 n'est couvert ni par la preuve ni par la mesure ;
   « pointer l'instrument sur la séparation prouvée » est impossible.
   Détail : [bib/kv_asym_extraction.md](../bib/kv_asym_extraction.md).
   Leçons de méthode : certification obligatoire (un incumbent ne
   prouve rien) ; tout instrument doit passer un contrôle positif
   avant que ses négatifs aient valeur.

Aucune de ces cibles n'est à la portée d'un tour LLM + vérification
exécutable — ce sont des fronts de recherche. Le critère d'ouverture d'un
Tour 26+ doit donc être : *un sous-lemme vérifiable d'une de ces cinq
zones*, pas la zone elle-même.

## Inventaire des pièces

- **Audits sur textes** : `bib/bgs_1975.md`, `bib/razborov_rudich_1997.md`,
  `bib/aaronson_wigderson_2008.md`, `bib/tardos_1988.md`,
  `bib/razborov_smolensky_1987.md`, `bib/beigel_tarui_1994.md`,
  `bib/williams_2011.md`, `bib/cfi_abd.md`, `bib/l18_status.md`,
  `bib/krishan_2024.md` (ligne 14), `bib/gct.md` (ligne 8, A-011),
  `bib/proof_complexity.md` (ligne 15, A-012).
- **Fil V (ligne 14)** : réfutation Conjecture 5 + parité prouvée
  (`tasks/done/V-053.md`, relecture `V-055.md`), moteurs exacts
  (`checks/svp_turbo.py`, `checks/svp_sym.py`), mesures toriques MAJ
  (`tasks/done/V-002.md`) ; validation externe : V. Krishan (cahier,
  2026-06-12).
- **Cellules détaillées** : `barriers/williams_vs_rr.md`,
  `barriers/gct_vs_aw.md`, `barriers/cfi_vs_rr.md`,
  `barriers/magnif_vs_locality.md`.
- **Mesures exécutables** : `checks/task_f001_weight_tc0_d2.py` +
  `data/weight_tc0_d2.csv` (weight L1, TC⁰ d=2), ~30 scripts `checks/`
  des tours.
- **Archives des 25 tours** : `tours/tour_01_*.md` … `tours/tour_25_*.md`.
- **Journal complet** : `cahier_de_bord.md` (§2 pistes, §3 lemmes,
  §4 questions q.1-q.16, §7 bibliographie).
