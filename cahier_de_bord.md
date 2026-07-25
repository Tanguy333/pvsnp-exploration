# Cahier de bord — Exploration P vs NP

> Document vivant. À joindre en contexte à **chaque** tour, pour le Proposeur comme pour le Réfuteur.
> Règle d'or : on ne réexplore jamais une impasse déjà documentée. On mesure le progrès par la compréhension accumulée, pas par « a-t-on la preuve ».

> **Recadrage (fin tour 9).** Le but du dépôt est **P vs NP**. Les Tours 8-9 ont
> dérivé vers de l'algèbre commutative pure (catalogage Boij-Söderberg,
> caractérisation des résolutions pures) — objets mathématiquement valables mais
> **sans lien démontré à P vs NP**. Les objets « ✅ Établis » du §3 sont conservés
> pour leur intérêt mathématique propre, mais **ne comptent pas comme progrès
> sur P vs NP**. Toute idée future doit avoir un lien explicite à la question
> originelle — voir conditions (i) corrigée et (k) ajoutée au §5.

## Dépôts satellites

- **[Tanguy333/pvsnp-LeanAC0Profondeur2](https://github.com/Tanguy333/pvsnp-LeanAC0Profondeur2)** *(privé)* —
  Formalisation Lean 4 des 8 théorèmes ✅ ÉTABLIS du présent dépôt (Tours 12-20,
  bornes inférieures combinatoires sur AC⁰ profondeur 2). Travaillé dans une
  **discussion séparée** par Claude en rôle de *Formaliseur Lean 4* (pas de boucle
  adverse). Ici, dans `pvsnp-exploration`, on conserve uniquement le rôle de
  **Réfuteur** ; les théorèmes établis sont l'*input* du dépôt Lean, jamais
  modifiés depuis le dépôt satellite.

  Cible à long terme : PR mathlib4 si la qualité le permet. Théorèmes ciblés :
  L12 (PARITY), L13 (IS(Q_n)), L14 (MAJ), L15 (THRESHOLD), L16 (MOD_p), L18 (IP),
  L19 (essentialité), L20 (antipodales).

---

## 0. Méta

- **Question** : tout problème dont une solution candidate est vérifiable en temps polynomial est-il aussi résoluble en temps polynomial ? (P vs NP)
- **Direction choisie** : séparation **P ≠ NP**, via une classe restreinte à structure algébrique/géométrique ; cadre principal = complexité descriptive, ouverture GCT ; outils encouragés = méta-complexité / Kolmogorov.
- **Démarré le** : 2026-05-23
- **Mise à jour intermédiaire** : 2026-06-11 après-midi (**journée des théorèmes** : ① **F-011 e24-e33** — le modèle faible **général** mod 6 dompté : hypothèse plate `deg₆(MAJ_n) = ⌈n/2⌉` confirmée sur n = 4..25, 29, 31, 32 (les cellules n = 12, 13 qui résistaient à 4,5 h de SAT tombent en 0 s par **ansätze d'orbites de sous-groupes** — leçon de méthode majeure) ; **trois familles infinies prouvées** : Théorème **K** (t = 2^a), **K′** (t = 2·3^k, e_t + correction équilibrée pure mod 3, 3 lemmes de Lucas), **K″** (t = 3^k, e_t pur mod 3, 1 ligne) ; **classification complète de la frontière bipartite** (t ≤ 27 ∪ {36} : solubles = les 3 familles + sporadiques isolés {5, 12} à formes closes — mosaïques de Lucas mixtes) ; 3 conjectures de plus réfutées le jour même (3-lisse, 3-lisse ∪ {5}, K′ naïf) ; MaxSAT/RC2 pour certificats canoniques. ② **Fil V : V-014 + V-015** — **Conjecture 5 de KV close pour d = 7, TOUT n, sans trou** (Théorème V15 ; le réseau redécouvre Tarry 1913 à n*(7) = 50 et **certifie sa minimalité**) ; d = 6 quasi clos (exhaustif n ≤ 81, témoin d'Escott 1910 vérifié exact ferme n ≥ 102, trou résiduel [82, 101]) ; suite des transitions non monotone certifiée. ③ **Audit A-010** (demande utilisateur) : BGL 2003 lu en texte complet par **lecture visuelle** (polices bitmap contournées) — notre cadre CRT/digits = leur lentille protocoles, borne linéaire symétrique MAJ mod 6 = leur Thm 4.9 ; nos lois exactes + tout le modèle général/bloc-symétrique = couche candidate délimitée (`bib/bgl_2003_sun_2020.md`). Synthèses à jour : [`notes/front_composite.md`](notes/front_composite.md) §10-10bis.)
- **Dernière mise à jour (soir)** : 2026-06-11 soir — **LE CONTRE-EXEMPLE** : la **Conjecture 5 de Krishan-Vishwanathan (2024) est RÉFUTÉE telle qu'énoncée** (V-017b/c, V-018) : à (d = 17, n = 30), l'unique plus court vecteur (au signe près) est un palindrome à γ₃₀ = ±2 — vérifié par TROIS chemins disjoints (SVP exact en rationnels purs avec témoins sains, division symbolique, sommes de puissances brutes) et une énumération contrainte indépendante. **Carte complète** (V-019a/b/c, ~930 cellules exactes) : bande réfutante née à d = 17 (îlot {13}), pleine [8, 20] dès d = 42, bord ~d/20 ; le régime utile à l'application ACC (d ≪ n) reste soutenu par nos ~290 cellules. **Mécanisme identifié** (V-021) : la bande commence exactement à la rupture d'optimalité des produits purs (1−x)^{d+1}(1+x)^{k−1} (coïncidence 7/7/8 à d = 30/40/45) ; **formes closes** : m(d, d+2) = 2·Catalan(d+1). **Loi de symétrie** (V-022, 10/10) : minima profonds uniques au signe près, palindromes ssi d+1 pair ; **éclaireur palindromique** (V-023, dimension /2, offset 40) : d = 17 fermé, bande d = 30 prolongée (têtes graduées jusqu'à 4). Plus : **V-015 (Théorème V15 : Conjecture 5 close pour d = 7, tout n — Tarry 1913 redécouvert et certifié minimal)** ; d = 6 quasi clos (Escott vérifié exact, trou [82, 101]) ; d = 10 vérifié n ≤ 107+ avec **certificat PTE inconditionnel taille 11** (support > 70-107, seul inconditionnel de la littérature — audits CMSV 2023 + survey Chen Shuwen 2025) ; **certificats du désert** tailles 13..50 (V-017/b, V-020) ; mur d = 10 / héritage 1851 consigné (kv_note §6bis-6quater, en anglais pour les auteurs). 8 étapes de plus au fil V (V-014..V-023), 3 auto-corrections honnêtes en route.
- **Dernière mise à jour (nuit)** : 2026-06-11 nuit — **LA THÉORIE DU BORD EST PROUVÉE ET FERMÉE** (V-024..V-033) : forme maîtresse P_j(D) = (2D)!(2j)!/(D!·j!·(D+j)!) (contient 2·Catalan(d+1) = Théorème V24, l'échelle V25) ; carrés parfaits sur le cercle (|Φ₃|² = (1+u)², |2Φ₃+x|² = (3+2u)²) → N_phi et N_cœur = combinaisons de P ; **Théorème de la loi des fenêtres (V-032)** : entrée cœur-bat-phi ⟺ D ≥ 5a+8 (une ligne), fenêtre cœur-bat-pur = intervalle entre les racines d'une quadratique explicite — la marche observée d ∈ [22,29] retrouvée à l'entier près ; **les ex æquo des bords = les racines ENTIÈRES des formes closes (V-033)** — aucun concurrent hors famille dans tout le paysage observé (des centaines de cellules), théorie complète. Plus : **cœurs universels** 2Φ₃+x / 2Φ₃²−x² (V-028, liste exhaustive tailles 17..50 V-029), théorème analytique colonnes 2-4 via Jacobi (V-026, seuil universel k = 5), Prouhet 1851 reconstruit et vérifié (V-031), **d(18) ∈ [97, 262143]**, lemme des cœurs (jamais de multiples hauteur-1), classes de symétrie PTE vérifiées sur Escott (miroir A↔B = antipalindrome) et Kuosa (auto-miroir = palindrome) = notre loi V-022. Emails : KV (contre-exemple) ENVOYÉ ; Chen Shuwen rédigé (adresse confirmée chen.shuwen@seekway.com). Run nocturne en cours : certificat taille 11 vers [0, 148] (20 workers parallèles, veille désactivée). Outillage : python-flint installé (LLL compilé ~1000×), calibration de prospection consignée (LLL pur aveugle au 24 de Kuosa — limite documentée).
- **Dernière mise à jour** : 2026-07-01 — **V-056 : l'hybride « diviseurs forcés × turbo-réseau », construit, validé, arrêté au mur exponentiel.** Lecture des sections MÉTHODE de BM 2000 (p.1-8, visuelle → bib) : leur §2.2 produits purs était un GABARIT (cœur premiers fixe, queue ≤ 3(m+1)/2 — le m=20 leur a échappé car 50 était hors gabarit) ⟹ notre DFS-transit domine strictement ; leur §2.1 = LLL Maple heuristique ⟹ nos moteurs certifiés dominent ; leur §3-4 (Φ forcés, d(m) exacts m≤10) = la seule pièce importée. **Pépite : notre seuil m*=15 (V-046) EXPLIQUE leur anomalie m=15** (meilleur exemple non-produit-pur, sans explication depuis 2000). Bornes m²≪d(m)≪m²log m CONNUES (BEK 1997 — corrige notre « seul le linéaire est prouvable »). **Mur des produits purs (V-054) = phénomène Erdős-Szekeres** (d_produit ≥ A(m)−1, conjecture 1959). Hybride V-056 : f=f₀·q, f₀=(x−1)^m·∏Φ_forcés (Thm 3-4), base réciproque BM + turbo-LLL + énumération exacte — VALIDÉ (retrouve d(18)=207/L=104 seul ; le LLL seul ne voit que hauteur ≥2, conforme m*=15). Acquis : m=23 D≤300 borne 160 = ZÉRO vecteur réciproque ; loi de coût ×2/+10 de rang ; heuristique gaussienne TROMPEUSE (réseaux structurés). Arrêt (décision Tanguy, critère vitesse) : mur exponentiel, GNR+BKZ = projet de jours pour un fil périphérique. Caveat produit-pur vs général (m≥22) reste ouvert, documenté. [tasks/done/V-056.md](tasks/done/V-056.md). **Addendum 2026-07-02** : toute la table BM m=11-21 CERTIFIÉE (B&B < valeur, transit ≤4, ~5 s, 0 amélioration) — upgrade de « plus petits connus » à **minima prouvés parmi les produits purs** ; certificats que BM n avaient pas (ils ne prouvent d(m) que pour m ≤ 10). V-054 §2bis + paragraphe ajouté à la réponse 4 Mossinghoff.
- **Mise à jour** : 2026-06-29 — **EXTENSION DE LA TABLE BORWEIN-MOSSINGHOFF (V-054)** : au-delà de la table BM (≤21), deux degrés minimaux de **produits purs** neufs — **m=22 = 473** (rang dur, = champion m=21 × (1−x^179), minimal transit ≤5, 71,4 G nœuds) et **m=23 = 439** (champion **compact non-trivial**, minimal transit ≤6) ; **non-monotonie prouvée 439 < 473** ; bornes inférieures m=24-30 (aucun champion ; tendance 0,67·m² inatteignable sur le domaine certifié : transit ≤7 pour m=26-30, ≤6 pour m=25, ≤5 pour m=24 — les runs manquants arrêtés volontairement (coût trop élevé / relance différée), non certifiés, pas de relance prévue) ; lois mesurées : **temps-degré ×5 par +40** (≈ ×10/57), croissance par transit ×53→×26→×10,7→×7,2→×3,6 (décroissante), **tassement** (coût ↓ quand m↑ à budget fixe) ; lien **PTE** vérifié (nos champions = solutions PTE **non-idéales** ; minimal-degré ⊥ minimal-taille — ne peut ni trouver ni réfuter une idéale). **Caveat** : produits purs = bornes sup. sur d(m) général (coïncident à m≤21, non vérifié au-delà). **Fil théorie des nombres, périphérique à P vs NP.** Suite : brouillon réponse 4 à Mossinghoff (`notes/mossinghoff_reply_4_draft.md`) + soumission OEIS (m=20 ferme ; 22/23 en bornes). Contexte : suit le recadrage V-051/V-052/V-053 (2026-06-27 ; filon réseau épuisé pour P vs NP, l'obstruction à KV = parité de γ_n, pas magnitude de λ₁). **Audit Fable 5 (2026-06-29, 27e auto-correction — E1/E2 de V-055 = 25e, faux-OOM = 26e)** : **τ(20) = 2, pas 3** (triple preuve ; V-047 §6) — la famille transit-3 = {15,16,17} seulement, la claim fausse a été envoyée 2× à Mossinghoff, correctif inséré dans la réponse 4 ; table des bornes m=24/25 recadrée (runs t6/t7 arrêtés volontairement, jamais terminés) ; croissance par transit corrigée (×53→×3,6 décroissante, pas « ×5-6 »).
- **Mise à jour** : 2026-06-12 — **JOURNÉE DES PALINDROMES & DU MOTEUR** (V-037..V-043) : ① **V-037** — chasse au barreau de d = 9 gagnée à la 1re cellule : taille 12, degré 9, **span 72** (palindrome, 4,2× plus compact que Kuosa) ; d = 9 : min ∈ {20, 22, 24} pour n ≥ 72, barreaux 20/24 couverts. ② **V-038** — moteur entièrement compilé LLVM : énumération ×173 + LLL certifié à fenêtres (l'incrémental pur dérivait de 8 ordres — 15e auto-correction, attrapée grâce à un arrêt utilisateur) : pipeline **×4000** ((9,72) : 44 s → 0,01 s) ; marches turbo : d = 9 jusqu'à n = 139, d = 10 jusqu'à n = 146 — **V-016c close** (objectif [0,132] dépassé), **fantôme exclu inconditionnellement span ≤ 146**, presque-fantôme et idéale-10 exclues ≤ 139. ③ **V-039** — Lemmes de symétrie A (palindrome ⟹ multiplicité paire ; antipalindrome ⟹ impaire) et B (tailles impaires jamais palindromes) ⟹ **toute presque-fantôme est asymétrique** ; barreaux 22 et 26 de d = 9 constatés VIDES (énumération à rayon fixe `turbo_below`) ; 37/37 minima antipalindromiques à (10,114). ④ **V-040** — ascenseur antipalindromique (idéale impaire symétrique ⟺ multigrade impair signé, 5 conditions au lieu de 10) : machine validée (Escott retrouvée à M = 51, la classique taille 9 à M = 99/span 198) ; antériorité actée AVANT recherche : secteur symétrique taille 11 **vide ≤ 3500** (BLP 2002 → CMSV 2023) — réplication vérifiante seulement. ⑤ **V-041** — taille 14 = idéale taille 7 en carrés parfaits : v1 valide (Tarry à M = 25 pile) puis mur exponentiel mesuré ; méthode CMSV n pair **décodée et re-dérivée** (F₁₂ certifiée = 0 sur Kuosa, F₁₄ re-dérivée par noyau exact — dim 1, 53 termes — pipeline auto-validé en reproduisant F₁₂) ; **v2 validée de bout en bout (Kuosa retrouvée : sélection 9 valeurs + congruences (21) + porte F + complétion algébrique)** puis **CLOS par la règle d'or** (décision Tanguy : on ne refait pas CMSV) ; Table 2 consignée (H = 3500/2000/900/1100/850 pour n = 11..16, PDF archivé localement). ⑥ **V-042** — recensement de symétrie : 162 cellules, **29 263 minima classés** — loi absolue RÉFUTÉE (8 284 asymétriques aux petits d) remplacée par trois lois : **seuil n_asym(d)** = 12/23/30/48/66/96 (d = 2..7), **zéro asymétrique à d ≥ 8** (= frontière de la littérature), Lemme A vérifié **100 %** ; DÉCOUVERTE du « palindrome caché » : **taille 14, degré 11, span 136** (témoin du barreau 28 de d = 11, 2,2× plus compact que Kuosa, bouts ±1). ⑦ **V-043 — THÉORÈME DES BARREAUX INTERDITS** (élémentaire, prouvé) : pour d impair, tout plat auto-symétrique de norme 2(d+2) est nécessairement l'idéale antipalindromique de taille d+2 ⟹ **les barreaux orphelins des réseaux impairs encodent exactement les problèmes ouverts des idéales impaires** (d = 9 ↔ taille 11, d = 11 ↔ 13, …) et rétro-valident les degrés fermés (3, 5, 7 ↔ tailles 5, 7, 9 existantes) ; les seuils n_asym = spans minimaux exacts des solutions non symétriques du barreau courant — **n_asym(7) = 96 = span minimal de l'idéale taille 8 non symétrique** (témoin explicite, certificat exhaustif sous 95). Cibles : 1er asymétrique de d = 8 à n > 198 (= 1re idéale taille 9 non symétrique, littérature ouverte), théorème du seuil, marches en pause reprenables. Outillage : `svp_turbo.py` (enum + LLL certifiés), `march_turbo.py`, machines V-040/V-041 réutilisables, `v042_census.csv`.
- **Mise à jour précédente** : 2026-06-11 matin (clôture F-011 e1-20 symétrique + fil V V-001..013 : Conjecture 5 close d ≤ 5, Théorème V11, 109/109, emails KV/Göös envoyés ; Atlas à 13 lignes)
- **Dernière mise à jour** : 2026-07-23 — **TROIS CAMPAGNES CLOSES.** ① **Fil AS (AS-001..043, 2026-07-01..20) — la Conjecture 13 de KV, dossier complet** : THÉORÈME inconditionnel C13 vraie pour d ≤ K·log₂ n (AS-022) ; loi b_d ≥ 1/8 certifiée d ≤ 16 (égalité ssi Mersenne, certificat neuf D(31,15) = 1/8) ; chaîne de réductions exactes cascade → tour dyadique → tables de cosets RM (carte mod 4 certifiée) → **série thêta à signes de Lucas** (Poisson certifié ; théorème d'obstruction : le coset MAJ = trou profond arithmétique de profondeur 2ⁿ/poly dans un réseau de packing constant λ₁ ≈ 4 — les méthodes géométriques ne peuvent rien) → **loi d'échelle ln(1/ρ) = π/x − c(n,d)** (AS-042, la MÊME constante π sur toutes les cellules : le trou profond SATURE sa thêta) → **C13 ⟺ c(n,d) = O(polylog n)** — toute la conjecture dans UN scalaire, mesuré plat ([0,70 ; 1,49], 6 cellules, 4D de 3 à 358, AS-043). Contre-exemple jugé improbable (témoins n ≤ 169). 5 routes réfutées avec témoins, 13 auto-corrections. **Synthèse envoyée à Krishan** (9 points, énoncé en tête, statut épistémique tracé) — réponse en attente, sans urgence. ② **Atlas complet : 15 lignes toutes documentées sur textes** — A-011 (ligne 8 GCT : Mulmuley §18 verbatim — « should be nonrelativizable » ×2, largeness prouvée sur F_p seulement, constructivité circulaire avouée ; BIP 2019 intégral — le mécanisme est le PADDING seul ; multiplicités 2019→2026 : cadres jouets uniquement, coefficients eux-mêmes durs) + A-012 (ligne 15 NEUVE, complexité des preuves Cook-Reckhow : frontière AC⁰[p]-Frege, la SEULE famille dont la barrière-analogue est un THÉORÈME inconditionnel — Pich-Santhanam 2019 ; voie moderne EF → P≠NP sous conditions S¹₂, convergence avec la ligne 13). ③ **NOTE-001 : la note T-F006 FINIE** (théorème CNF prouvé — CNF_min(IP_2n) = (3^n+1)/2, invariance sous complément ; version anglaise arXiv prête ; réserve unique restante : relecture experte). ④ **Fil F-012..022 (2026-07-23) — le barreau 1 (poids SYM∘AND, verrou TC⁰ ligne 7) DOSSIER COMPLET** : 10 valeurs exactes (IP_8 = 4, OR(THR4²) = 6 = 3+3, XOR(THR4²) = 14, XOR(GT2²) = 16, MAJ₃(OR2³) = 12…) ; 4 THÉORÈMES (tranche W ≥ W_A+W_B ; comptage — indicateur {0,1} positif = monôme unique = la ligne MOD/MAJ d'ACC/TC⁰ au niveau jouet ; alternance W ≥ alt(f), serré sur PARITY/IP ; **fenêtre ANF N(k,t) = 2^{k−1}−1 pour 2 ≤ t ≤ k+1** — induction de Shannon, d'où la route parité EXACTEMENT exponentielle en bloc = quantification démontrée du régime Beigel-Tarui) ; 2 lois de construction prouvées (parité/ANF, couvert unilatéral) chacune serrée dans son régime ; 3 réfutations mécanistiquement élucidées (injectivité ; additivité ANF — contre-exemple positionnel ; **invariant unique du comptage — tué 3× dont l'hybride positivité×parité q = C(s,2) de AND2(MAJ3²) = 6 < 9**) ; verdict : W = min d'un zoo ≥ 4 mécanismes, la dureté de l'outil comptage DÉMONTRÉE — l'écho jouet le plus fidèle du verrou TC⁰. Moteur neuf : OR-Tools CP-SAT (diségalités natives). Fenêtres résiduelles : OR(GT2²) ∈ [25, 32], AND(GT2²) ∈ [21, 38]. 2 incidents de protocole attrapés (dont 1 par l'utilisateur : re-vérification obligatoire).
- **Nombre de tours effectués** : 25 (boucle adverse suspendue ; réouverture conditionnée aux zones génératrices de l'Atlas — désormais 15 lignes, cf. CLAUDE.md §8 et `atlas/matrice_barrieres.md` dernière section)

> **Numérotation Tour 24.** Le Proposeur a titré sa proposition « Tour 23 » mais
> Tour 23 (threshold polynomial complexity / `tcomp`) est déjà existant et clos
> en ⚠️ LACUNE RÉPARABLE. La proposition « complexité tropicale » est donc
> archivée comme **Tour 24** ; voir [`tours/tour_24_tropical_refutee.md`](tours/tour_24_tropical_refutee.md).

> **Audit bibliographique (mai 2026).** Vérification croisée des 8 théorèmes
> ÉTABLIS (Tours 12-20) contre la littérature DNF-MIN. Verdict : les 7 résultats
> testés sont **folklore ou classiques** (Quine 1952, McCluskey 1956,
> Hammer-Kogan in Crama-Hammer 2011 ch.3, Hellerstein-Kletenik 2011). Seul L18
> (IP) reste **statut incertain** (non trouvé dans les sources consultées, peut
> être folklore obscur). Détail dans la note §3 « Audit bibliographique ». Les
> 8 théorèmes restent valides comme corpus vérifié, mais leur statut épistémique
> est désormais **« re-démonstration de classiques »**, pas « contribution
> nouvelle ». L'affirmation initiale « pas de littérature à ce sujet » est
> falsifiée.
>
> **Clôture du dépôt satellite Lean.** Le dépôt
> [`Tanguy333/pvsnp-LeanAC0Profondeur2`](https://github.com/Tanguy333/pvsnp-LeanAC0Profondeur2)
> est **fermé** post-audit (les théorèmes étant folklore, la valeur de leur
> formalisation Lean était limitée à un exercice d'ingénierie sans rapport
> avec P vs NP). Les architectures rédigées et `Basic.lean` prouvé restent
> accessibles localement, sans poursuite. Aucun nouveau tour de cette
> exploration P vs NP ne doit proposer de formalisation Lean.

---

## 1. Barrières connues (à garder sous les yeux en permanence)

| Barrière | En une ligne | Statut dans notre exploration |
|---|---|---|
| Relativisation (Baker–Gill–Solovay) | Une preuve qui « relativise » ne peut pas trancher P vs NP. | **ACTIVE** — a tué la piste 1. Tout outil relativisant (Kt, auto-réductibilité, recherche↔décision) est suspect. Exiger des techniques non-relativisantes (ex. arithmétisation à la Williams). |
| Preuves naturelles (Razborov–Rudich) | Les bornes inférieures « naturelles » échouent sous hypothèses cryptographiques standard. | Pertinente uniquement pour les arguments de type table de vérité / circuit. Ne s'applique pas aux arguments purement informationnels — donc « l'éviter » ne prouve rien en soi. |
| Algébrisation (Aaronson–Wigderson) | Généralise la relativisation aux techniques algébriques. | **ACTIVE** — a tué la piste 2. Toute technique mobilisant l'arithmétisation doit démontrer son caractère non-algébrisant (exhiber un oracle algébrique relativement auquel l'invariant proposé sépare P de NP). |
| **Barrière monotone (Razborov 1985 / Tardos 1988)** | Une borne inférieure exponentielle sur la complexité **monotone** (booléenne, arithmétique monotone, ou tropicale par Jerrum-Snir 1982) **n'implique pas** de borne sur la complexité non-monotone. Tardos 1988 exhibe une fonction *dans P* à complexité monotone $\exp(\Omega(n^{1/6-o(1)}))$. | **ACTIVE** — a tué la piste 24. Toute technique sur circuits monotones / arithmétique monotone / tropicaux / min-plus doit démontrer comment elle passe au cadre non-monotone, sous peine de récolter Tardos 1988 comme contre-exemple structurel. |

> Toute idée nouvelle DOIT dire laquelle de ces barrières elle prétend franchir, et comment. **Et explicitement traiter la relativisation.**

---

## 2. Pistes explorées

| # | Idée (résumé en 1 ligne) | Barrière visée | Verdict du Réfuteur | Statut |
|---|---|---|---|---|
| 1 | Incompressibilité (Kt) des témoins SAT : P comprimerait les témoins, contredisant leur incompressibilité | Preuves naturelles (revendiqué) | Équivoque K(w) vs K(w\|x) ; argument relativisant | ❌ **FAILLE FATALE** |
| 2 | Signature p-adique des témoins (Ax-Katz pour vérificateurs AC⁰) | Relativisation (revendiqué) | Arithmétisation exacte ≠ polylog ; Ax-Katz trivial sous contrainte booléenne ; technique algébrisante | ❌ **FAILLE FATALE** |
| 3 | Obstruction topologique sur paysage d'énergie CSP (Morse discrète + Lusternik-Schnirelmann) | Relativisation + algébrisation (revendiqué) | Invariant non-invariant sous équivalence logique ; sauts polynomiaux effondrent les Betti | ❌ **FAILLE FATALE** |
| 4 | Compilation TC⁰ → tensor network à bond polynomiale + Williams + Hardness Magnification | Les 3 (revendiqué) | Lemme 1 faux : IP_n ∈ TC⁰ a bond dimension exponentielle (rang 2ⁿ−1 sur ℝ) ; parade F₂ détruit l'outillage analytique ; ce qui reste = reformulation du programme Williams ouvert | ❌ **FAILLE FATALE** sur le mécanisme |
| 5 | Indistinguabilité CPT+C des hypercubes colorés `H_f` (jeux de pavage bijectifs + canonisation Dawar) | Les 3 + (d) + (e) (revendiqué) | Lemme 3 trivialement impossible : `∃ x. f(x)` est FO ⊂ CPT+C et distingue toute paire SAT/UNSAT ; Lemme 1 invoque un théorème de Dawar qui n'existe pas sous cette forme ; (f) non satisfaite (feuille de route admise) | ❌ **FAILLE FATALE** |
| 6 | Gap homologique sémantique pour circuits monotones Σ Π fan-in borné (Stanley-Reisner) | Les 7 (revendiqué) | Lemme 2 réfuté empiriquement (52/168 contre-exemples sur n=4) ; Lemme 1 confond complexe et idéal de Stanley-Reisner ; calcul promis non livré | ⚠️ **LACUNE RÉPARABLE** (direction légitime, mais réparation déplace hors cadre) |
| 7 | Obstruction homologique duale (résolutions libres + dualité d'Alexander) pour profondeur de formule monotone | Les 8 (revendiqué) | Chiffres C_4, K_4 corrects ; mais Lemme 2 (D_m ≥ Ω(pd)) réfuté par OR_n : pd(I_{OR_n}) = n−1 alors que D_m = 1 ; cadre limité aux formules (pas circuits) | ⚠️ **LACUNE RÉPARABLE** |
| 8 | Atlas de Boij-Söderberg des fonctions monotones n=4 (renoncement à P vs NP) | Inapplicables (objet fini) | Mouvement stratégique correct ; mais Lemme 4 (OR/AND = seuls à résolution pure) massivement faux (95/167 contre-exemples) ; atlas livré par le Réfuteur | ⚠️ **LACUNE RÉPARABLE** + objet positif livré |
| 8 bis | Révision du Proposeur : « résolution pure ssi threshold » | Inapplicables | Mini-théorème révisé encore faux (4 thresholds prédits sur n=4, mais 95 fonctions pures ; ex : f = x_0 et f = (x_0∧x_1)∨(x_0∧x_2) sont pures et non-threshold) ; **violation immédiate de (j)** que le Réfuteur venait d'ajouter | ⚠️ **LACUNE RÉPARABLE** |
| 9 | Conjecture C9 : pure ⟺ equigenerated (caractérisation des résolutions pures pour fonctions monotones) | Inapplicables | (h) et (j) honorées pour la première fois par le Proposeur. Conjecture vérifiée n=4 (167 fonctions, tableau parfait 95/0/0/72). **Réfutée n=5** : 215 contre-exemples sur 7579. Contre-exemple minimal : `(x₁x₂x₃)∨(x₁x₂x₄)∨(x₀x₃x₄)` (equigenerated, mais Betti(I) a 2 shifts à l'index 1) | ⚠️ **LACUNE RÉPARABLE** (épistémologie correcte) |
| 10 | (a) Conjecture C10 « intersections uniformes » testée préemptivement et **retirée par le Proposeur** (1068 contre-exemples) ; (b) pivot proposé vers formalisation Lean de Koszul de `m_n` | (a) C10 testée mais inapplicable car pas de prétention asymptotique ; (b) Koszul Lean : aucune | Bon réflexe épistémologique (test (j) honoré 2e fois consécutive). Mais pivot Lean cible un théorème **hors-sujet vis-à-vis de P vs NP** (admis par le Proposeur). Direction prescrite Tour 11 : `PARITY ∉ AC⁰ profondeur 2` | ⚠️ **LACUNE RÉPARABLE** + recadrage utilisateur |
| 11 | Borne `D_m(2COL) ≥ Ω(n log n)` via lifting (Raz-McKenzie/GPW) + Karchmer-Wigderson + Tseitin sur expandeurs (Ben-Sasson-Wigderson) | Trois barrières revendiquées (lifting+KW non-relativisant et non-algébrisant ; RR fragile admis) | Direction enfin correcte vis-à-vis P vs NP. Mais : (1) **erreur factuelle** : 2-COLORATION ∈ P, pas NP-complet ; (2) 2COL n'est pas naturellement monotone ; (3) chaîne L10.5 conjecturale (pattern récurrent que le Proposeur reconnaît) ; (4) (j) régressée (test n=4,6,8 promis mais non livré) ; (5) redondance possible avec Garg-Göös-Knop-Watson 2018 non vérifiée | ⚠️ **LACUNE RÉPARABLE — rejet maintenu par utilisateur** |
| 12 | Mini-théorème : `PARITY_n ∉ AC⁰ profondeur 2` de taille `< 2^(n-1)` (= DNF minimal exactement `2^(n-1)` monômes) | Toutes traitées explicitement (relativisation : preuve combinatoire sans oracle ; RR : propriété pas large car ne caractérise que PARITY et ¬PARITY ; algébrisation : pas d'arithmétisation) | Calcul exhaustif n=4 livré AVANT soumission (81 ANDs, 8 implicants, bijection vérifiée). Argument structurel L12.1–L12.4 valable pour tout n, prouvé combinatoirement. Reproduction indépendante par le Réfuteur OK. **Toutes les 12 conditions (a)–(l) honorées pour la première fois.** | ✅ **ÉTABLI POUR P vs NP** |
| 13 | Caractérisation : `DNF_min(f) = |f^{-1}(1)|` ⟺ `f^{-1}(1)` est independent set de `Q_n` ⟺ aucun AND de `< n` littéraux n'est implicant. PARITY est l'élément maximal d'une classe combinatoire de **743 fonctions à n=4**. | Toutes (relativisation combinatoire, RR : caractérise une classe pas une fonction, algébrisation : sans objet) | Calcul exhaustif n=4 livré : 743 fonctions identifiées, équivalence (b)⟺(c) vérifiée sur 200 échantillons sans incohérence, distribution exacte par taille, PARITY+¬PARITY uniquement à |f^{-1}(1)|=8. Preuves L13.1–L13.4 combinatoires audités OK. Erreur référentielle OEIS (A006506 cité à tort, mais 743 est correct par calcul direct) | ✅ **ÉTABLI POUR P vs NP** (2e objet) |
| 14 | Mini-théorème : `DNF_min(MAJ_n) = C(n, ⌈n/2⌉) ~ 2^n/√n`, donc `MAJ_n ∉ AC⁰ d=2 polynomial`. Première apparition de TC⁰ dans le dépôt. | Toutes (relativisation combinatoire ; RR : « f=MAJ_n » caractérise une fonction unique, non-large ; algébrisation : sans objet) | Calcul exhaustif n=4 livré : 81 ANDs, 33 implicants, **6 implicants premiers** (= C(4,2)), tous positifs taille 2, non-redondance vérifiée. L14.1 initial buggé, **bug détecté et corrigé par le Proposeur via (j)** avant soumission. Preuves L14.1–L14.4 auditées correctes. | ✅ **ÉTABLI POUR P vs NP** (3e objet) — avec **correction de formulation** : la séparation est `TC⁰ d=1 ⊄ AC⁰ d=2 poly` (par témoin), pas l'inclusion stricte `AC⁰ d=2 poly ⊊ TC⁰ d=1 poly` revendiquée. Les deux classes sont en fait incomparables (contre-exemple : DISJ_n ∈ AC⁰ d=2 poly \ TC⁰ d=1). |
| 15a | Proposeur P1 : profondeur logique de Bennett pour séparer P de NP par contradiction | Revendiquées non-rel/non-RR/non-alg (mais sans objet, voir Verdict) | **Auto-réfuté par le Proposeur** dans son Lemme 3 (*« l'argument est circulaire »*). Pattern Tour 1 (circularité conditionnel/inconditionnel) avec « Bennett » à la place de « Kt ». Le cahier §3 dit explicitement « à ne jamais réessayer ». (j) et (h) non honorées. Régression méthodologique après 3 ÉTABLIS consécutifs. | ❌ **FAILLE FATALE** — pattern Tour 1 explicitement interdit |
| 15b | Proposeur P2 : `DNF_min(THRESHOLD_{t,n}) = C(n, t)` pour tout `t ∈ [1, n]` + dichotomie polynomial/exponentiel | Toutes (relativisation combinatoire ; RR : famille de `n` fonctions parmi `2^{2^n}`, non-large ; algébrisation : sans objet) | Calcul exhaustif n=4 livré pour `t ∈ {1,2,3,4}` : `C(4, t) = 4, 6, 4, 1` confirmés. Tous implicants premiers positifs, non-redondance vérifiée. Preuves L15.1–L15.4 = généralisation directe de L14.1–L14.4. **Condition (m) honorée explicitement dès la première application** : séparation par témoin (`TC⁰ d=1 ⊄ AC⁰ d=2 poly`), pas inclusion stricte. Nuance technique honnête sur la frontière exacte (`O(log n)` vs `O(log n / log log n)`). | ✅ **ÉTABLI POUR P vs NP** (4e objet) |
| 16 | `DNF_min(MOD_p_n) = Σ_{k ≡ 0 mod p} C(n, k)`, application directe de L13 (Tour 13) à la famille `MOD_p`. Ouverture de la lignée Razborov-Smolensky. | Toutes (relativisation combinatoire ; RR : famille de `n` fonctions parmi `2^{2^n}`, non-large ; algébrisation : sans objet) | Calcul exhaustif n=4 livré pour `p ∈ {2,3,4,5}`. Comptes confirmés : 8, 5, 2, 1. L16.1 (MOD_p^{-1}(1) independent dans Q_n) prouvée combinatoirement : `sum(y) = sum(x) ± 1` à distance Hamming 1, donc `≢ (mod p)` pour `p ≥ 2`. L16.2 par application directe de L13. L16.3 asymptotique par roots of unity filter. Note terminologique mineure : MOD_2 = ¬PARITY (pas PARITY au sens strict), même DNF_min par symétrie de la bipartition. | ✅ **ÉTABLI POUR P vs NP** (5e objet) |
| 17 | Conjecture `DNF_min(IP_{2n}) = (3^n − 1)/2` pour INNER PRODUCT mod 2, **première fonction hors classe L13** (non-monotone, non-symétrique). Méthode ILP set cover (nouvelle pour le dépôt). | Toutes (relativisation combinatoire + ILP exact ; RR : fonction unique parmi 2^{2^{2n}}, non-large ; algébrisation : pas d'arithmétisation) | Vérification empirique à n=1, 2, 3 par le Proposeur (set cover exhaustif) ; **extension à n=4 par le Réfuteur via PuLP/CBC ILP** : 40 = (3^4 − 1)/2 confirmé. 4 points consécutifs sans exception. Observation structurelle : `|implicants premiers| = DNF_min` à chaque n testé. **Tour 18 fournit la preuve structurelle pour tout n** (cf. ci-dessous). | ✅ **ÉTABLI structurellement (via Tour 18)** (6e objet) |
| 18 | Preuve structurelle de L17 pour tout n : classification des implicants premiers en 3 classes (A1, A2a, A2b) selon `(x_n, y_n)`, récurrence `a_{n+1} = 2a_n + b_n`, `b_{n+1} = a_n + 2b_n`, close-form `a_n = (3^n − 1)/2`, non-redondance par construction explicite du témoin. | Toutes (relativisation combinatoire ; RR : fonction unique ; algébrisation : pas d'arithmétisation) | L18.A (classification) preuve par cas exhaustifs auditée OK. L18.B (récurrence + close-form) par induction triviale, auditée OK. L18.C (non-redondance) esquissée par le Proposeur, **détaillée par le Réfuteur** : construction explicite du témoin `(x_0, x_n=0, y_n=1)` pour A2a, etc. Vérification empirique n=1..4 cohérente avec la récurrence (1, 4, 13, 40). **Mise à jour 2026-06-09 (F-005b)** : la prédiction n=5 (121) est désormais **vérifiée directement** (énumération des 3^10 ANDs par masques de bits : \|primes\| = 121, DNF_min = 121 par set cover ILP Optimal — cf. `checks/task_f005b_verification_k4_k5.py`). L18 vérifié directement n=1..5 ; n=6 (364) reste prédiction. | ✅ **ÉTABLI STRUCTURELLEMENT** — promeut Tour 17 d'empirique à structurel |
| 19 | Théorème de caractérisation L19 : `DNF_min(f) = |primes(f)|` ⟺ chaque implicant premier admet un témoin essentiel. L13 ⊊ (α)/(β) strictement (témoin MAJ_3). | Toutes (relativisation combinatoire ; RR : *signal d'alarme* — propriété constructive et large à n=4 (36%), mais théorème ne dérive pas de borne inférieure générale, donc compatible ; algébrisation : sans objet) | L19.A et L19.B preuves combinatoires auditées (classiques Quine-McCluskey 1952-1956). Vérification empirique : 202/254 (n=3) et 23862/65534 (n=4) fonctions dans la classe. Unifie Tours 12-18 sous une caractérisation unique. Conjecture asymptotique « fraction → 0 » non démontrée (2 points). | ✅ **ÉTABLI** (7e objet) — théorème classique reformulé, unifie le paradigme |
| 20 | Théorème L20 : fonctions antipodales `f_α(x) = 1 ⟺ x ∉ {α, ¬α}` ont `|primes| = n(n−1)`, `DNF_min = n`, défaut maximal `n(n−2)`. **Pôle extrême opposé à L19**. | Toutes (relativisation combinatoire ; RR : famille petite `2^(n-1)`, non-large ; algébrisation : sans objet) | (i)-(iv) prouvées combinatoirement pour tout n ≥ 3 et auditées (audit du Réfuteur : impl. premier ⟺ 1 positif + 1 négatif ; couverture cyclique ; borne par vecteurs unitaires). Vérification empirique exhaustive n=3 (4 antipodales, défaut 3), n=4 (8, défaut 8), n=5 (16, défaut 15). L20.5 (unicité antipodales = seules à défaut max) conjecturée, vérifiée n=3, 4 par énumération exhaustive. **Note importante** : lien P vs NP plus faible que revendiqué — sur les antipodales, DNF-MIN est facile (calculable en O(n)), pas un témoin de Σ₂^P-difficulté. | ✅ **ÉTABLI** (8e objet) sur (i)-(iv) ; L20.5 conjecturée pour n ≥ 5 |
| 21 | Preuve partielle de L20.5 par cas sur k = \|f^{-1}(0)\|. L21.A (k=1) trivial, L21.B (k=2 antipodal) = Tour 20, L21.C (k=2 non-antipodal) prouvée rigoureusement (\|primes\|_max = d²−2d+n ≤ n²−3n+3 < n(n−2) pour n ≥ 4 ; n=3 direct), L21.D (k ≥ 3) reste **conjecturale**. | Toutes (combinatoire, non-large, pas d'arithmétisation) | L21.A, L21.B, L21.C prouvés rigoureusement (Réfuteur complète L21.C par calcul exact des implicants premiers). **L21.D RÉFUTÉ Tour 22** (contre-exemple à n=5, k=5). | ❌ **FAILLE FATALE (post-Tour 22)** — L21.D faux pour k ≥ 3 ; L20.5 réfutée ; L21.A/B/C maintenus |
| 22 | (a) Réfutation de L20.5 / L21.D par contre-exemple direct `Z = {0, 3, 5, 25, 30}` à n=5 : triplet (\|primes\|=25, DNF_min=8, défaut=17) > n(n−2)=15. (b) Acquis positif L22.A : si Z = f^{-1}(0) est coord-dégénéré sur position j, alors défaut(f) = défaut(g) ≤ (n−1)(n−3) < n(n−2). | Toutes (combinatoire ; pas de prétention à borne nouvelle pour P vs NP) | Triplet vérifié indépendamment par le Réfuteur (script distinct : énumération 3^5 ANDs + ILP PuLP/CBC). Distribution {2:2, 3:21, 4:2} — non-structure régulière. L22.A prouvée structurellement (audit des 7 sous-étapes a-g). Statistique Proposeur : 1280 contre-exemples à n=5 (0 coord-dégénérés, 0 antipodaux). | ✅ **TOUR RÉUSSI** par négation + acquis structurel L22.A. **Mais viole le recadrage §5 Tour 22** (reste en AC⁰ d=2 / DNF-MIN explicitement interdit). Apport méthodologique : 1er tour qui réfute un ÉTABLI partiel précédent. |
| 23 | Threshold polynomial complexity `tcomp(f) = (d_min, m_min)` mesurée par ILP sur OR, AND, PARITY, MAJ, THR_t, MOD_p, IP_{2k} (n=4..8). Conjecture T23.1 : `tcomp(IP_{2k}) = (k, 2^{k-1})` vérifiée à 3 points (k=2,3,4). Pivot revendiqué vers programme Williams 2011 → TC⁰. | Toutes (relativisation combinatoire ILP ; non-large ; pas d'arithmétisation) | **13 chiffres confirmés sans divergence** par script Réfuteur indépendant (1er tour avec auto-vérification parfaite). MAIS : (a) `tcomp` confond max-magnitude L∞ et L1-weight de la littérature PTF, (b) T23.1 = vérification de folklore (conjecture d'Anthony sur PTF degree, Bruck-Smolensky 1992 sur magnitude exponentielle d'IP), (c) cible TC⁰ d=2 \ TC⁰ d=1 non explorée (9/13 tests en TC⁰ d=1, seul IP en d=2), (d) pont à Williams CAPP non construit (Beigel-Tarui utilise polynômes exacts mod 2^ℓ, pas PTF). | ⚠️ **LACUNE RÉPARABLE** avec acquis méthodologique fort (instrument ILP réutilisable, 1er tour à toutes conditions (a)-(r) honorées) |
| 24 | Complexité tropicale de SAT : encoder 3-SAT comme polynôme tropical $P_\phi = \min_j \min(1, \sum_i \ell_{ji})$ et borner inférieurement $R(P_\phi) \geq 2^{n/2}$ régions linéaires pour $n \in \{4,5,6\}$ (Lemme L24.T) ; chaîne conjecturale tropical→boolean P vs NP | Les 3 (revendiquée), pas mentionnée Tardos | (1) **Encodage inversé** vérifié exécutable 0/16 cas (le Proposeur n'a pas calculé son propre encodage) ; (2) **Borne L24.T triviale** : un min de $m+1$ affines a $O(m^n)$ régions par Zaslavsky, donc $\geq 2^{n/2}$ atteint trivialement par n'importe quel polynôme tropical ; (3) **Violation explicite de (q)** : Jukna 2014 (arXiv:1406.3065) + Jerrum-Snir 1982 + Schnorr couvrent depuis 40 ans ; (4) **Barrière monotone Tardos 1988** non-mentionnée mais létale (tropical = monotone arith. par Jerrum-Snir) ; (5) chaîne tropical→boolean *purement conjecturale*, admise par le Proposeur ; (6) condition (k) violée (« années-lumière » de P vs NP) | ❌ **FAILLE FATALE** — barrière monotone létale + 5 failles indépendantes + (q) violée |
| 25 | CFI-rigidification de 3-SAT : pour chaque variable `x_i` de φ, jumelée `(x_i^0, x_i^1)` avec XOR `x_i^0 ⊕ x_i^1 = 1`, clauses jumelées en orientation arbitraire. Revendique G = (ℤ/2)^n automorphisme préservant SAT + borne inférieure exp pour circuits G-symétriques (L25.3) + pont à Gurevich 1988 / CPT (L25.4 + L25.5). | Toutes (combinatoire fini, non-large, sans arithmétisation) | (1) **L25.1 + L25.2 réfutés empiriquement à 100 %** sur 20 formules 3-SAT random à n=3 : la « jumelée » est équivalente à introduire `¬x_i` comme nouvelle variable, le « swap » est équivalent à flipper `x_i`, donc G ne préserve PAS SAT (testé à n=1 : 1 contre-exemple immédiat). (2) **L25.5 conflate FPC / CPT / symmetric P** : Anderson-Dawar 2017 caractérise FPC (⊊ P prouvé par CFI), pas P ; la vraie question est CPT (Blass-Gurevich-Shelah 1999), open. (3) **(q) violée** : Atserias-Bulatov-Dawar 2007 (CFI affine pour CSP) non cité, alors que c'est la VRAIE CFI moderne. (4) **(j) violée** : le Proposeur promet « calcul concret à n=3 » §5 aveu 5 mais NE LE LIVRE PAS — le Réfuteur l'a fait en 5 minutes, contre-exemples immédiats. | ❌ **FAILLE FATALE** sur L25.1 + L25.2 (construction incohérente) ; L25.3-L25.5 sans objet ; aveux honnêtes du Proposeur ne réparent pas la faille technique |
| 27 | **Quotient symétrique** : G = S_k ⋉ (S₂)^k réduit la classe symétrique à un programme d'orbites → **L27.1 : W_sym = k(k+1) certifié k ≤ 8** (toute réfutation est asymétrique) ; L27.2 (lemme de span) ; cartographie négative de [20, 30] ; sous-lemme classe A dessiné avec prédiction falsifiable | Sans objet (modèle fini) | Audit : L27.1 reproduit 6/6 + quotient validé ; L27.2 correct ; 1 erreur de portée attrapée (le run massé du dossier cherchait TOUTES les solutions, son évidence tient) ; **le Réfuteur EXÉCUTE la prédiction : classe A FERMÉE ≥ 30** (288 d-graphes canoniques, exhaustif 270 s). Cible non fermée (avoué, sans pivot) ; fenêtre [20, 30] structurellement rétrécie : témoin ⟹ asymétrique + hors classe A + span contraint | ⚖️ **ÉCHEC HONNÊTE sur la cible, ACQUIS VALIDÉS** ([archive](tours/tour_27_quotient_symetrique.md)) ; **post-tour T27-S1 : CLASSE B FERMÉE ≥ 30 elle aussi** (CP-SAT canal de valeurs + lex-leader, échelle 19..29 toute UNSAT, étalon = borne 20 du Tour 26 reproduite — subsume A et C=0) ; **post-tour T27-S2 : LA CIBLE EST FERMÉE À k = 5 — W(MAJ₅(OR2⁵)) = 30 = k(k+1) sur l'ESPACE ENTIER** (échelle de caps 19..29 toute UNSAT en ~3 h 20, borne sup décomposable énumérée : « décomposable ⇒ global » prouvé à k = 5, C26 certifiée k = 3, 4, 5) |
| 26 | **Indicateur modulaire** : q_M = Σ(ĝ_S mod M)·m_S est un indicateur exact mod M s'annulant sur g⁻¹(0) → W(SYM_k(g^k)) ≤ k·Σ(ĝ_S mod k) = O_g(k²) ; unification du zoo (parité = M=2, indicateurs AND = M=∞) ; borne inf par restriction W(MAJ₅(OR2⁵)) ≥ 20 = 2·k·W(g) ; conjecture C26 : k(k+1) | Sans objet (modèle fini) ; antériorité Toda/BT signalée | Audit complet du Réfuteur : preuves relues (toutes correctes), 13/13 constructions ré-exécutées, certificats reproduits (THR₂(OR2⁴) = 20 OPTIMAL, décomposables 12/20/30 optimaux), contre-attaque symétrisée sur C26 échouée (30 résiste, 25 min). 3 sauts avoués (décomposable⇒global k≥5 ; LB décomposable générale ; ω(k)). Cible asymptotique non fermée — mais O(k²) prouvé + premier point super-additif prouvé + fenêtres resserrées (MAJ₃(MAJ3³) ≤ 12) | ✅ **SURVIT** — 1er tour survivant en 26 tours ([archive](tours/tour_26_indicateur_modulaire_survit.md)) ; sous-lemme prioritaire : LB décomposable k(k+1) pour tout k |

### 2 bis. Fils de tâches atomiques (post-Tour 25, mode CLAUDE.md §8)

| Fil | Contenu | Acquis | Synthèse |
|---|---|---|---|
| **F-011** (33 étapes, 2026-06-10/11) | Le modèle polynomial faible mod 6 (zone 2 de l'Atlas — le mur composite de 1987) : symétrique (e1-16), puis **général/bloc-symétrique** (e17-33), plus le modèle fort | **Symétrique** : ~13 théorèmes (loi exacte complète `deg₃^sym(OR_n) = max(3^b, n−3^b)`, lois MAJ H/I/J, anomalies, récursion base 3) ; **Général** : hypothèse plate `deg₆(MAJ_n) = ⌈n/2⌉` confirmée n = 4..25, 29, 31, 32 ; **trois familles infinies prouvées** — Théorèmes **K** (2^a), **K′** (2·3^k), **K″** (3^k) ; **classification complète de la frontière bipartite** (3 familles + sporadiques isolés {5, 12} à formes closes) ; **Théorème L** (modèle fort) ; méthode : ansätze d'orbites (0 s là où 4,5 h de SAT échouent) + MaxSAT canonique. **7 conjectures réfutées le jour même**. Audits BBR 1994 + **BGL 2003/TR04-022** (A-010, lecture visuelle) : cadre = BGL, lois exactes + modèle général = couche candidate. | [`notes/front_composite.md`](notes/front_composite.md) §1-10bis |
| **V** (15 tâches, 2026-06-11) | Issu de la veille probabiliste (demande utilisateur) : polynômes toriques BHLR 2019 → **Conjecture 5 de Krishan-Vishwanathan 2024** (ECCC TR24-074, route vers MAJ ∉ ACC) | Conjecture 5 **reformulée** (⟺ coefficient dominant ±1 ⟺ queue du problème **PTE-ℓ₂**), testée 109/109, puis **CLOSE pour d ≤ 5 et d = 7 (tout n)** — Théorèmes V8-V11, **V13**, **V15** (le réseau redécouvre Tarry 1913 à n*(7) = 50 et certifie sa minimalité) ; **d = 6 quasi clos** (exhaustif n ≤ 81, Escott 1910 vérifié exact ferme n ≥ 102, trou [82, 101]) ; transitions du réseau = degrés PTE minimaux (suite non monotone certifiée : 6, 6, 11, 18, 23, (81,102], 50). Emails envoyés aux auteurs (×2). | [`notes/kv_note.md`](notes/kv_note.md) |
| VEILLE-P + A-009 (2026-06-11) | Méthodes probabilistes récentes (4 fronts) + audit méta-complexité | Toriques = cible exécutable (→ fil V) ; **ligne 13 de l'Atlas** (méta-complexité moderne : non-boîte-noire ✓, MCSP = l'objet de RR, verrou = NP-complétude ouverte depuis Levin) ; dérandomisation et OGP : hors-cible documenté | [`bib/veille_probabilistes_2026.md`](bib/veille_probabilistes_2026.md), [`bib/meta_complexite.md`](bib/meta_complexite.md) |
| **V (suite N.T.)** (V-037..V-054, 2026-06-12/29) | Fil théorie des nombres issu de la réfutation KV : palindromes, moteur turbo compilé, puis **extension de la table de Borwein-Mossinghoff** (degré minimal d'un produit pur plat ∏(1−x^{t_i}) divisible par (1−x)^m) par recherche transit-height (B&B + suivi-min, Numba/LLVM) | m=20 = 307 (confirmé **NOUVEAU** par Mossinghoff) ; **m=22 = 473** (rang dur, = champion m=21 × (1−x^179), minimal transit ≤5) et **m=23 = 439** (champion **compact non-trivial**, minimal transit ≤6) au-delà de la table BM (≤21) ; **non-monotonie prouvée** 439 < 473 ; bornes inf. m=24-30 (aucun champion ; inatteignable sur le certifié : t≤7 m=26-30, t≤6 m=25, t≤5 m=24) ; lois mesurées : temps-degré ×5/+40, croissance ×~5/transit, **tassement** (coût ↓ quand m↑ à budget fixe) ; lien PTE (nos champions = solutions PTE **non-idéales**, minimal-degré ⊥ minimal-taille). **Caveat** : produits purs = bornes sup. sur d(m) général. **Périphérique à P vs NP.** | [`tasks/done/V-054.md`](tasks/done/V-054.md) |
| **AS** (43 tâches, 2026-07-01..20) | La **Conjecture 13 de KV** (D(n,d) ≥ 2ⁿ/poly pour d = o(√n/log n) ⟹ MAJ ∉ ACC) : de « aucune donnée » au dossier complet | **THÉORÈME : C13 vraie pour d ≤ K·log₂ n** (inconditionnel) ; loi b_d certifiée d ≤ 16 (Mersenne ssi 1/8, certificat D(31,15) neuf) ; chaîne de réductions exactes → **série thêta à signes de Lucas** ; théorème d'obstruction (trou profond arithmétique, λ₁ ≈ 4) ; **loi π universelle : ln(1/ρ) = π/x − c(n,d)** ⟹ **C13 ⟺ c = O(polylog n)** — un scalaire, mesuré plat (6 cellules, 4D ∈ [3, 358]). 5 routes réfutées, 13 auto-corrections. **Synthèse envoyée à Krishan.** | [`tasks/done/AS-042.md`](tasks/done/AS-042.md), [`notes/krishan_synthese_c13_draft.md`](notes/krishan_synthese_c13_draft.md) |
| **A-011/A-012 + NOTE-001** (2026-07-20/23) | Atlas : lignes 8 (GCT) et 15 (complexité des preuves, NEUVE) documentées sur textes ; note T-F006 finie | Atlas **15 lignes toutes sur textes** ; GCT : les aveux de Mulmuley (§18 verbatim), BIP intégral (le padding seul), multiplicités = cadres jouets ; ligne 15 : AC⁰[p]-Frege frontière, barrière-analogue = THÉORÈME (Pich-Santhanam) ; **T-F006 : théorème CNF prouvé + version arXiv anglaise prête** (reste : relecture experte, main de Tanguy) | [`bib/gct.md`](bib/gct.md), [`bib/proof_complexity.md`](bib/proof_complexity.md), [`notes/dnf_min_ip_arxiv_en.md`](notes/dnf_min_ip_arxiv_en.md) |
| **F-012..022** (11 tâches, 2026-07-23) | **Le barreau 1** : poids SYM∘AND des compositions de seuils (le verrou TC⁰ de la ligne 7, échelle jouet) — mesure, puis ANALYSE | 10 valeurs exactes ; **4 théorèmes** (tranche, comptage, alternance — serré sur PARITY/IP, **fenêtre ANF N(k,t) = 2^{k−1}−1** ⟹ route parité exactement exponentielle en bloc = le régime Beigel-Tarui quantifié et démontré) ; 2 lois de construction serrées (parité ANF, couvert unilatéral) ; **3 réfutations élucidées** dont l'invariant unique du comptage (hybride positivité×parité) ⟹ **W = min d'un zoo ≥ 4 mécanismes : la dureté de l'outil comptage DÉMONTRÉE** — l'écho jouet du verrou TC⁰. Moteur CP-SAT. Fenêtres : OR(GT2²) ∈ [25,32], AND ∈ [21,38] | [`tasks/done/F-022.md`](tasks/done/F-022.md) (+ F-012..021) |

---

### 2 ter. Registre satellite (hors mission P vs NP) — créé le 2026-07-25

> Un item satellite peut être **terminé** — plusieurs sont à un cheveu de la
> publication et les abandonner serait du gâchis — mais il **ne consomme plus
> de créneau de tâche**, ne figure pas dans les acquis P vs NP, et passe en
> « main de Tanguy ». La décision manquante est prise ici : le dépôt avait déjà
> écrit trois fois que ce travail était « à part de P vs NP »
> (`atlas/matrice_barrieres.md`, `tasks/done/V-054.md`, `tasks/done/V-056.md`)
> sans en tirer la conséquence. Précédent interne appliqué : le recadrage
> Boij-Söderberg de la fin du Tour 9.

| Item | État | Note |
|---|---|---|
| Soumission OEIS n°1 — A397434, \|ANF(MAJ_n)\| (issue de F-018/F-019) | en revue | DATA étendues par un contributeur OEIS |
| Soumission OEIS n°2 — degré minimal d'un produit pur plat (issue de V-054) | non soumise | — |
| Note arXiv T-F006 (`notes/dnf_min_ip_arxiv_en.md`, `.tex`) | brouillon prêt, relecture experte requise | La note dit elle-même « Distance à P vs NP : nulle ». **Satellite = le canal de diffusion, jamais l'énoncé** : le théorème T-F006 reste cité par la ligne 7 et reste dans la mission |
| Correspondance Mossinghoff (m = 20 = 307 confirmé nouveau) et Chen Shuwen | brouillons rédigés | Travail mathématiquement réel, sur une autre question |
| Table BM / PTE, courbe d(m), phase du réseau (V-037..V-056) | clos | Rangs m = 22, 23 au-delà de la table publiée ; non-monotonie prouvée |

**La correspondance Krishan-Vishwanathan n'est PAS satellite** : elle porte la
ligne 14 de l'Atlas — la seule cellule que ce dépôt ait fermée par lui-même —
et reste pleinement dans la mission.

## 3. Lemmes et résultats

### ✅ Établis pour P vs NP (vérifiés / démontrés rigoureusement)

- **Mini-théorème** (Tour 12) : *`PARITY_n ∉ AC⁰ profondeur 2` de taille `< 2^(n-1)`*. Plus précisément : la taille minimale d'un DNF (OR de ANDs, fan-in arbitraire) calculant `parity_n(x) = x_0 ⊕ … ⊕ x_{n-1}` est **exactement `2^(n-1)`**. Cf. [`tours/tour_12_parity_ac0_etabli.md`](tours/tour_12_parity_ac0_etabli.md) et [`checks/tour_12_parity_ac0.py`](checks/tour_12_parity_ac0.py).

  **Preuve structurelle** (valable tout n, 4 pas combinatoires) :
  1. Tout AND de < n littéraux a une variable libre → admet satisfaisants de parités opposées → non-implicant.
  2. Donc implicants premiers = mintermes complets correspondant aux 2^(n-1) affectations impaires.
  3. Chaque minterm est satisfait par une unique affectation → tous requis dans tout DNF.
  4. Borne inférieure 2^(n-1) atteinte par DNF canonique. ∎

  **Vérification exhaustive n=4** : 81 ANDs énumérés, 8 implicants identifiés, bijection avec les 8 affectations impaires confirmée, DNF canonique de taille 8 calcule `parity_4`.

  **Lien à P vs NP** : `parity_n ∈ P` (calculable en `O(n)`), donc l'impossibilité d'un DNF de taille polynomiale (puisque `2^(n-1)` est exponentiel) montre que **`AC⁰ profondeur 2 ⊊ P`**. Premier maillon de la chaîne FSS 1981 → Håstad 1986 → Razborov-Smolensky 1987 → Williams 2011 (NEXP ⊄ ACC⁰, seul résultat ayant franchi les trois barrières).

  **Barrières** : non-relativisant (preuve combinatoire sans oracle), pas en tension avec RR (propriété trop spécifique pour être large : seules `parity` et `¬parity` la satisfont), non-algébrisant (pas d'arithmétisation).

  **Premier objet positif aligné sur P vs NP du dépôt** après 11 itérations.

- **Théorème de caractérisation** (Tour 13) : *Pour `f : {0,1}^n → {0,1}` non-constante, les trois conditions sont équivalentes :*
  - *(a) `DNF_min(f) = |f^{-1}(1)|`,*
  - *(b) aucun AND de `< n` littéraux n'est implicant de `f`,*
  - *(c) `f^{-1}(1)` est un independent set du graphe `Q_n` du n-cube.*

  Cf. [`tours/tour_13_independent_set_etabli.md`](tours/tour_13_independent_set_etabli.md) et [`checks/tour_13_independent_set_characterization.py`](checks/tour_13_independent_set_characterization.py).

  **Corollaire 1 (compte exact à n=4)** : la classe des fonctions vérifiant (a)/(b)/(c) sur n=4 contient exactement **743 fonctions** (= nombre d'independent sets de `Q_4`), distribuées par taille `|f^{-1}(1)|` selon `[1, 16, 88, 208, 228, 128, 56, 16, 2]`. La séquence des `|IS(Q_n)|` est `2, 3, 7, 35, 743, ...` (n=0,1,2,3,4,...).

  **Corollaire 2 (extrémalité PARITY)** : le maximum `|f^{-1}(1)| = 2^{n-1}` est atteint **exactement par PARITY et ¬PARITY** (les deux classes de la bipartition de `Q_n`). PARITY n'est plus un cas isolé du Tour 12 ; c'est l'élément maximal d'une classe combinatoire de 743 fonctions.

  **Preuves** : L13.1 (a)⟺(b) reprend Tour 12 généralisé. L13.2 (b)⟺(c) preuve directe par sous-cubes / arêtes de `Q_n`. L13.3 bijection triviale. L13.4 extrémalité par bipartition de `Q_n`.

  **Barrières** : non-relativisant (combinatoire sans oracle), RR non applicable (la propriété caractérise une classe, pas une fonction individuelle), non-algébrisant (pas d'arithmétisation).

  **Apport au dépôt** : *consolide et structure* le Tour 12. PARITY identifié comme élément maximal d'une classe identifiable (et non un cas isolé). Deuxième objet ÉTABLI.

  **Note (erreur référentielle mineure)** : le Proposeur cite OEIS A006506 pour le compte 743, mais A006506 = nombres de Dedekind (`2, 3, 6, 20, 168, 7581`). La séquence correcte est différente. Le chiffre 743 lui-même est correct par calcul exhaustif.

- **Théorème de la majorité** (Tour 14) : *`DNF_min(MAJ_n) = C(n, ⌈n/2⌉) ~ 2^n/√n`. Donc `MAJ_n ∉ AC⁰ d=2 polynomial`.*

  Cf. [`tours/tour_14_majority_etabli.md`](tours/tour_14_majority_etabli.md) et [`checks/tour_14_majority_dnf_lower_bound.py`](checks/tour_14_majority_dnf_lower_bound.py).

  **Preuves** :
  - L14.1 : `M` implicant de `MAJ_n` ⟺ `pos(M) ≥ ⌈n/2⌉` (force libres à 0 → sum minimal = pos(M)).
  - L14.2 : implicants premiers sans littéraux négatifs (suppression d'un `~x_i` préserve l'implication par L14.1).
  - L14.3 : implicants premiers = ANDs positifs de taille exactement `⌈n/2⌉`. Nombre = `C(n, ⌈n/2⌉)`.
  - L14.4 : pour chaque sous-ensemble `S` de taille `t = ⌈n/2⌉`, `χ_S` satisfait uniquement `M_S`. Donc tous les `C(n, t)` implicants premiers sont requis.

  **Vérification exhaustive n=4** : 81 ANDs, 33 implicants (incluant non-premiers), 6 implicants premiers (= C(4,2)) tous positifs taille 2, non-redondance vérifiée, DNF canonique de taille 6 calcule `MAJ_4`.

  **Note de bug corrigé** : la version initiale de L14.1 était erronée (« aucun implicant n'a de littéral négatif » — faux, 22 contre-exemples sur 81 ANDs). Le Proposeur a détecté le bug *via le calcul (j)* et corrigé en distinguant *implicant* / *implicant premier* avant soumission. Exemple parfait du rôle de la condition (j).

  **⚠️ Correction de formulation sur la séparation entre classes**. Le Proposeur a écrit comme conclusion : *« AC⁰ d=2 polynomial ⊊ TC⁰ d=1 polynomial »*. **Cette inclusion stricte est mal énoncée**. Ce que le théorème établit *réellement* est `MAJ_n ∈ TC⁰ d=1 \ AC⁰ d=2 polynomial`, donc **`TC⁰ d=1 ⊄ AC⁰ d=2 polynomial`** (séparation par témoin). L'inclusion réciproque `AC⁰ d=2 polynomial ⊆ TC⁰ d=1` est **fausse** : contre-exemple `DISJ_n(x, y) = ⋁_i (x_i ∧ ¬y_i)`, qui est dans AC⁰ d=2 polynomial mais pas dans TC⁰ d=1 (complexité communication non-triviale). Les deux classes sont **incomparables**. Erreur logique sur les classes (similaire à 2COL ∈ P du Tour 11) mais sans toucher le théorème central.

  **Barrières** : relativisation (preuve combinatoire sans oracle), RR (la propriété « f=MAJ_n » est unique parmi `2^{2^n}`, non-large), algébrisation (pas d'arithmétisation). ✓

  **Apport au dépôt** : *troisième objet ÉTABLI*, sur une fonction nouvelle (MAJ ≠ PARITY), avec borne sub-exponentielle `~ 2^n/√n` (pas exponentielle comme Tour 12). Première apparition de `TC⁰` dans la lignée FSS → Williams 2011. PARITY (Tour 12) et MAJ (Tour 14) constituent les deux fonctions canoniques séparant respectivement AC⁰ de classes plus puissantes.

- **Théorème de la famille seuil** (Tour 15-B) : *Pour tout `t ∈ [1, n]`, `DNF_min(THRESHOLD_{t, n}) = C(n, t)`. Par conséquent, `THRESHOLD_{t, n} ∉ AC⁰ d=2 polynomial` ssi `t = Θ(n)` (avec ratio strict).*

  Cf. [`tours/tour_15b_threshold_etabli.md`](tours/tour_15b_threshold_etabli.md) et [`checks/tour_15_threshold_dichotomy.py`](checks/tour_15_threshold_dichotomy.py).

  **Preuves** : L15.1–L15.4 sont la généralisation directe de L14.1–L14.4 (Tour 14) avec `t` quelconque en place de `⌈n/2⌉`. Tous les arguments restent valides.

  **Vérification exhaustive n=4** : pour `t ∈ {1, 2, 3, 4}`, comptes `C(4, t) = 4, 6, 4, 1` confirmés. Implicants premiers tous positifs, non-redondance vérifiée.

  **Dichotomie qualitative** : `C(n, t)` polynomial en `n` ssi `t` est constant ou (sub-)logarithmique (et symétriquement `n − t`). Pour `t = Θ(n)`, `C(n, t) ~ 2^n/√n` super-polynomial. Frontière exacte (nuance technique honnêtement notée par le Proposeur) : `t = O(log n / log log n)`, pas exactement `O(log n)`.

  **Cas particuliers unifiés** :
  - `t = 1` : `OR_n`, `C(n, 1) = n` polynomial → OR ∈ AC⁰ d=2 polynomial.
  - `t = ⌈n/2⌉` : `MAJ_n` (Tour 14), `C(n, ⌈n/2⌉) ~ 2^n/√n` non-polynomial.
  - `t = n` : `AND_n`, `C(n, n) = 1` trivial.

  **Condition (m) honorée explicitement** dès le premier tour suivant son ajout : séparation `TC⁰ d=1 ⊄ AC⁰ d=2 polynomial` par témoin (tout `THRESHOLD_{Θ(n)}`), pas inclusion stricte. Bon réflexe.

  **Barrières** : relativisation (preuve combinatoire), RR (famille de `n` fonctions parmi `2^{2^n}`, non-large), algébrisation (pas d'arithmétisation). ✓

  **Apport au dépôt** : *quatrième objet ÉTABLI*, première vraie **unification paramétrique**. Tours 12 (PARITY, `t = ?`), 14 (MAJ_n = THRESHOLD_{⌈n/2⌉}), 15 (THRESHOLD_t pour tout `t`) forment désormais une famille cohérente. La dichotomie polynomial/exponentiel comme fonction de `t` est un fait paramétrique nouveau pour le dépôt.

  **Risque noté** : 4 itérations dans la même veine (FSS profondeur 2). Le Tour 16 devrait diversifier (profondeur 3, ou Lean, ou autre famille de fonctions) pour ne pas saturer le paradigme.

- **Théorème de la famille MOD_p** (Tour 16) : *Pour tout `p ≥ 2` et tout `n`, `DNF_min(MOD_p_n) = |MOD_p^{-1}(1)| = Σ_{0 ≤ k ≤ n, k ≡ 0 (mod p)} C(n, k)`.*

  Cf. [`tours/tour_16_mod_p_etabli.md`](tours/tour_16_mod_p_etabli.md) et [`checks/tour_16_mod_p_dnf.py`](checks/tour_16_mod_p_dnf.py).

  **Preuves** :
  - L16.1 : `MOD_p^{-1}(1)` est independent set de `Q_n`. Argument : `dist_H(x, y) = 1` implique `sum(y) = sum(x) ± 1`, donc `sum(y) ≢ sum(x) (mod p)` pour `p ≥ 2`. Donc `x ∈ MOD_p^{-1}(1) ⇒ y ∉ MOD_p^{-1}(1)`.
  - L16.2 : application directe de L13 (Tour 13) — la condition « `f^{-1}(1)` independent dans `Q_n` » est satisfaite par L16.1, donc `DNF_min(f) = |f^{-1}(1)|`.
  - L16.3 : asymptotique par roots of unity filter — `|MOD_p^{-1}(1)| ~ 2^n/p`, super-polynomial pour `p` fixé.

  **Vérification exhaustive n=4** : pour `p ∈ {2,3,4,5}`, comptes `8, 5, 2, 1` confirmés. Independent set vérifié (distance Hamming minimale ≥ 2).

  **Diversification réussie** : sortie partielle du paradigme THRESHOLD. La famille `MOD_p` est **non-monotone** (flipper un bit change `sum mod p`), distincte de la famille THRESHOLD (monotone). Ouvre la lignée Razborov-Smolensky 1987 (qui prouve `MOD_p ∉ AC⁰[q]` à profondeur arbitraire pour `p ≠ q` premiers, par méthode polynomiale modulaire). Tour 16 traite seulement le cas profondeur 2 par application combinatoire de L13.

  **Apport au théorème L13** : Tour 13 n'avait été appliqué explicitement qu'à PARITY. Tour 16 utilise L13 comme **outil de production** pour identifier une nouvelle famille canonique. Le théorème de caractérisation gagne en valeur a posteriori.

  **Condition (m) honorée** : séparation par témoin (`MOD_p ∈ P \ AC⁰ d=2 poly`), pas d'affirmation d'inclusion stricte.

  **Note terminologique** : `MOD_2(x) = 1 ssi sum pair = ¬PARITY(x)` au sens strict (convention standard où `PARITY(x) = 1` ssi sum impair). `|MOD_2^{-1}(1)| = |¬PARITY^{-1}(1)| = 2^(n-1)` par symétrie de la bipartition de `Q_n`. Le résultat est cohérent avec Tour 12, mais l'identification « MOD_2 = PARITY » du Proposeur est imprécise.

  **Apport au dépôt** : *cinquième objet ÉTABLI*. Mais 5 itérations consécutives dans `AC⁰ d=2` — saturation persistante. Le Tour 17 doit *vraiment* diversifier.

- **Conjecture vérifiée à 4 points : INNER PRODUCT mod 2** (Tour 17) : *`DNF_min(IP_{2n}) = (3^n − 1)/2` pour `n ∈ {1, 2, 3, 4}`, conjecture pour tout `n ≥ 1`.*

  Cf. [`tours/tour_17_inner_product_etabli.md`](tours/tour_17_inner_product_etabli.md), [`checks/tour_17_inner_product_dnf.py`](checks/tour_17_inner_product_dnf.py) (Proposeur, n=1,2,3) et [`checks/tour_17_extension_n4.py`](checks/tour_17_extension_n4.py) (Réfuteur, n=4 via PuLP/CBC ILP).

  **IP est la première fonction HORS classe L13** du dépôt :
  - Non-monotone (flipper certains bits change `IP`).
  - Non-symétrique (`x` et `y` jouent des rôles distincts).
  - `IP^{-1}(1)` n'est PAS un independent set de `Q_{2n}` (vérifié : voisins Hamming-1 dans `IP^{-1}(1)`, ex. `(0,1,0,1) ↔ (1,1,0,1)`).

  **Validation à n=4 via ILP exact** : 6561 ANDs, 520 implicants, **40 implicants premiers** (32 de taille 5 + 8 de taille 7), set cover résolu par CBC en < 1s. DNF_min = 40 = (3^4 − 1)/2. ✓

  **Observation structurelle remarquable** : à chaque `n ∈ {2, 3, 4}`, `|implicants premiers(IP_{2n})| = DNF_min(IP_{2n})`. Cela signifie que **tous les implicants premiers sont nécessaires** dans le DNF minimal. Si on prouvait : (1) `|primes(IP_{2n})| = (3^n − 1)/2` pour tout `n`, et (2) non-redondance complète, alors le théorème serait acquis pour tout `n`.

  **Coefficient exponentiel `log_2 3 ≈ 1.585`** : strictement inférieur à `log_2 4 = 2` pour MAJ_{2n}. Première distinction quantitative entre deux fonctions super-polynomiales dans le dépôt.

  **Statut épistémique nouveau** : différent des Tours 12-16. Ces derniers étaient des théorèmes structurels prouvés pour tout `n` + vérifiés à n=4. Tour 17 était initialement une **conjecture vérifiée à 4 points consécutifs**, sans preuve générale. **Promotion au Tour 18** : la conjecture est désormais prouvée structurellement pour tout n.

  **Méthode ILP set cover** : nouveau dans le dépôt, réutilisable pour toute future fonction hors classe L13. Installation de PuLP/CBC pour cela.

  **Condition (n) honorée** : pas d'application de L13 ; nouvelle méthode (ILP). Diversification réelle.

- **Preuve structurelle de L17** (Tour 18) : *`DNF_min(IP_{2n}) = (3^n − 1)/2` prouvé pour tout n ≥ 1 par récurrence combinatoire.*

  Cf. [`tours/tour_18_ip_recurrence_etabli.md`](tours/tour_18_ip_recurrence_etabli.md) et [`checks/tour_18_ip_recurrence_proof.py`](checks/tour_18_ip_recurrence_proof.py).

  **Décomposition fondamentale** : `IP_{2(n+1)}(x_0..x_n, y_0..y_n) = x_n · y_n ⊕ IP_{2n}(x_0..x_{n-1}, y_0..y_{n-1})`. Cette décomposition permet la récurrence sur n.

  **L18.A (classification)** : par cas exhaustifs sur `(x_n, y_n)`, tout implicant premier de `IP_{2(n+1)}` appartient à exactement l'une des trois classes :
  - **A1** : `x_n ∧ y_n ∧ M_0` où M_0 est implicant premier de `¬IP_{2n}`.
  - **A2a** : `~x_n ∧ M_0` où M_0 est implicant premier de `IP_{2n}`.
  - **A2b** : `~y_n ∧ M_0` où M_0 est implicant premier de `IP_{2n}`.

  Tous les autres cas sont soit impossibles (paire libre forcerait IP_{2n} = ¬IP_{2n}), soit non-premiers (e.g. `~x_n ∧ ~y_n ∧ M_0` se simplifie en `~x_n ∧ M_0` ou `~y_n ∧ M_0`).

  **L18.B (récurrence + close-form)** : par L18.A, `a_{n+1} = 2a_n + b_n` et `b_{n+1} = a_n + 2b_n` (où `a_n = |primes(IP_{2n})|`, `b_n = |primes(¬IP_{2n})|`). Conditions initiales `a_1 = 1, b_1 = 2`. Close-form `a_n = (3^n − 1)/2, b_n = (3^n + 1)/2` par induction triviale.

  **L18.C (non-redondance)** : pour chaque implicant premier `M`, construction explicite du témoin unique :
  - A2a : `x = (x_0, x_n=0, y_n=1)` où x_0 est témoin unique de M_0 dans IP_{2n}^{-1}(1).
  - A2b : `x = (x_0, x_n=1, y_n=0)`.
  - A1 : `x = (x_0, x_n=1, y_n=1)` où x_0 est témoin unique de M_0 dans ¬IP_{2n}^{-1}(1).

  Vérification de couverture unique par cas (les autres classes ne couvrent pas le témoin à cause des fixations x_n/y_n). Par récurrence, tous les implicants premiers ont un témoin unique. ✓

  **Conclusion** : `DNF_min(IP_{2n}) = a_n = (3^n − 1)/2` pour tout n ≥ 1.

  **Vérification empirique** : récurrence et énumération directe coïncident pour n=1, 2, 3, 4. Prédiction récurrence pour n=5 (121), n=6 (364).

  **Apport méthodologique nouveau** : *premier tour qui consolide un tour précédent* en bouchant un trou dans sa preuve. Chaîne Tour 17 (empirique) → Tour 18 (structurel) illustre la suite « vérifier → identifier le pattern → prouver ». Pattern précieux pour d'autres conjectures potentielles.

  **Note** : L18.C esquissée par le Proposeur, détaillée par le Réfuteur. La construction explicite du témoin pour chaque classe + vérification de couverture unique complète rigoureusement la preuve.

  **Conséquence** : le 6e objet ÉTABLI du dépôt passe d'« empirique n=1..4 + conjecture pour n ≥ 5 » à « théorème prouvé pour tout n ≥ 1 ». Tous les 6 objets sont désormais structurels.

- **Théorème de caractérisation d'essentialité** (Tour 19) : *pour toute fonction booléenne non-constante `f`, `DNF_min(f) = |primes(f)|` ⟺ chaque implicant premier admet un témoin essentiel.*

  Cf. [`tours/tour_19_essentialite_etabli.md`](tours/tour_19_essentialite_etabli.md) et [`checks/tour_19_primes_eq_dnfmin.py`](checks/tour_19_primes_eq_dnfmin.py).

  **Définition** : *témoin essentiel* d'un implicant premier `M` = une affectation `x ∈ f^{-1}(1)` que `M` est l'unique implicant premier à satisfaire.

  **Preuve** :
  - L19.A : (α) ⇒ (β) par contrapositive (si M sans témoin essentiel, primes\{M} couvre f^{-1}(1), donc DNF_min < |primes|).
  - L19.B : (β) ⇒ (α) (chaque M force son inclusion dans tout DNF minimal via son témoin essentiel).
  - L19.D : L13 ⊊ (α)/(β) avec témoin MAJ_3 (dans (α)/(β) mais MAJ_3^{-1}(1) pas independent dans Q_3).

  **Vérification empirique** : à n=3, 202/254 (79.5%) fonctions dans la classe ; à n=4, 23862/65534 (36.4%). Distribution du défaut `|primes| − DNF_min` à n=4 : 23408 fonctions à diff=1, 9856 à diff=2, …, 8 à diff=8.

  **Unification des Tours 12-18** : tous les 6 théorèmes précédents deviennent des spécialisations de L19. Chaque famille (PARITY, MAJ, THRESHOLD_t, MOD_p, IP) est dans (α)/(β) et a `|primes|` calculé explicitement. L19 fournit le **théorème-cadre** qui caractérise pourquoi.

  **Risque RR** : la propriété (β) est constructive (poly en `2^n`) et large à n=4 (36%). Si on prétendait dériver une borne inférieure générale, RR s'appliquerait. Le théorème actuel ne le fait pas — il caractérise une classe sans en tirer de borne universelle. Compatible avec RR dans son usage actuel.

  **Conjecture asymptotique** : « la fraction `|(α)/(β)| / 2^{2^n}` tend vers 0 quand n → ∞ ». Suggérée par 79.5% (n=3) → 36.4% (n=4), mais non démontrée. Pas un théorème.

  **Lien à P vs NP** : L19 caractérise précisément les fonctions où DNF minimization est en P (algo glouton optimal). Hors classe, le problème est Σ₂^P-difficile (Umans 1999). Lien indirect via la hiérarchie polynomiale.

  **Apport au dépôt** : *unification conceptuelle*. Le paradigme « AC⁰ d=2 par essentialité » est désormais saturé : continuer à cataloguer des familles dans (α)/(β) ne donnerait rien de nouveau.

  **Apport mathématique** : zéro (théorème classique de Quine-McCluskey 1952-1956). Mais l'unification conceptuelle est un acquis réel pour le dépôt.

- **Théorème des fonctions antipodales** (Tour 20) : *pour `f_α(x) = 1 ⟺ x ∉ {α, ¬α}` (n ≥ 3) :*
  - *(i) `|f_α^{-1}(1)| = 2^n − 2`,*
  - *(ii) `|primes(f_α)| = n(n − 1)` (les `x_i ∧ ~x_j` pour i ≠ j),*
  - *(iii) `DNF_min(f_α) = n` (atteint par tout cycle dirigé),*
  - *(iv) défaut = `n(n − 2)`.*

  Cf. [`tours/tour_20_antipodales_etabli.md`](tours/tour_20_antipodales_etabli.md) et [`checks/tour_20_antipodal_verification.py`](checks/tour_20_antipodal_verification.py).

  **Preuves auditées** (WLOG α = 0...0) :
  - (ii) M implicant ⟺ M(0...0)=0 et M(1...1)=0 ⟺ M contient au moins un positif et un négatif. Premier ⟺ exactement 1 positif + 1 négatif. Comptage n·(n−1).
  - (iii) ≤ : cycle `{x_i ∧ ~x_{(i+1) mod n}}`. Toute x ∈ f^{-1}(1) a au moins une transition cyclique 1→0, satisfaite par un implicant du cycle. ≥ : pour chaque e_i (Hamming weight 1), l'unique implicant le couvrant a forme `x_i ∧ ~x_j`. Donc ≥ n implicants requis.

  **L20.5 (corollaire conjectural) — ❌ RÉFUTÉ Tour 22** : prétendait que seules les antipodales atteignent le défaut maximal n(n−2). Vérifié exhaustivement n=3 (4/4) et n=4 (8/8), mais **faux dès n=5** : contre-exemple `Z = {0, 3, 5, 25, 30}` non-antipodal, coord-non-dégénéré, avec triplet (|primes|, DNF_min, défaut) = (25, 8, 17), défaut > n(n−2) = 15. 1280 contre-exemples au total à n=5 selon statistique Proposeur. Voir §❌ Réfutés et `tours/tour_22_l20_5_refutee.md`. **L20 (i)-(iv) restent ÉTABLIS** ; seule l'extension conjecturale L20.5 tombe.

  **Vérification empirique** : n=3 → 4 antipodales (défaut 3 = 3·1), n=4 → 8 (défaut 8 = 4·2), n=5 → 16 (défaut 15 = 5·3). Tous conformes à la formule.

  **Lien P vs NP** : Tour 20 caractérise les fonctions à *défaut maximal* dans le paysage post-Tour 19. Pôle extrême opposé à la classe (α)/(β). **Note importante** : le lien à la Σ₂^P-difficulté de DNF-MIN (revendiqué par le Proposeur) est *plus faible que présenté*. Sur les antipodales, DNF-MIN est facile (`DNF_min = n` en O(n)) ; le défaut élevé concerne la redondance de l'algorithme glouton, pas la difficulté intrinsèque du problème. La Σ₂^P-difficulté d'Umans 1999 vient d'autres familles.

  **Apport au dépôt** : *cartographie bidirectionnelle* du paradigme AC⁰ d=2. L19 (pôle « facile ») + L20 (pôle « défaut maximal ») délimitent les deux extrêmes.

  **Risque (RR)** : famille petite (`2^{n-1}`), non-large. RR sans objet.

  **Saut qualitatif réel ?** Partiel. Tour 20 sort de (α)/(β) mais reste dans le paradigme AC⁰ d=2. Pas de profondeur 3, pas de Lean, pas de Razborov. **Le Tour 21 doit faire un saut qualitatif vrai** (cf. directions infra).

- **Théorème du cas dégénéré L22.A** (Tour 22) : *si `Z = f^{-1}(0)` est coord-dégénéré sur une position `j` (toutes les affectations de Z ont la même valeur `b ∈ {0,1}` sur `j`), alors `défaut(f) = défaut(g) ≤ (n−1)(n−3) < n(n−2)`, où `g` est la fonction à n−1 variables obtenue en éliminant `j`.*

  Cf. [`tours/tour_22_l20_5_refutee.md`](tours/tour_22_l20_5_refutee.md) et [`checks/tour_22_refuter_l20_5.py`](checks/tour_22_refuter_l20_5.py) (le check vérifie le contre-exemple à L20.5, pas L22.A elle-même).

  **Preuve auditée** (WLOG j = n−1, b = 0) :
  - (a) `ℓ = x_{n-1}` est implicant : pour tout x avec `x_{n-1} = 1`, `x ∉ Z`.
  - (b) `ℓ` est premier : taille 1, irréductible.
  - (c) Tout autre prime M ne contient ni `x_{n-1}` ni `~x_{n-1}` (les deux cas se réduisent ou rendent M non-premier).
  - (d) Bijection `primes(f) \ {x_{n-1}} ↔ primes(g)` par restriction à `x_{n-1} = 0`.
  - (e) `DNF_min(f) = 1 + DNF_min(g)` : `x_{n-1}` est nécessaire pour couvrir `(z', 1)` avec `z' ∈ Z_g`.
  - (f) défaut(f) = `(1 + |primes(g)|) − (1 + DNF_min(g))` = défaut(g).
  - (g) Par récurrence sur n : défaut(g) ≤ (n−1)(n−3). Or (n−1)(n−3) < n(n−2) pour `n ≥ 2`. ✓

  **Conséquence** : les contre-exemples non-triviaux à L20.5 (Tour 22) doivent être *non-dégénérés* sur chaque position. Statistique Proposeur : 0 / 1280 contre-exemples sont coord-dégénérés, cohérent avec L22.A.

  **Barrières** : combinatoire (non-relativisant), pas d'arithmétisation (non-algébrisant), RR sans objet (caractérise une réduction structurelle, pas une borne).

  **Apport au dépôt** : 9e objet ÉTABLI, mais *modeste* — caractérise un cas particulier facile (réduction à n−1) plutôt qu'une vraie borne. Pas de gain pour P vs NP.

  **Acquis méthodologique** : 1er tour qui **réfute un ÉTABLI partiel précédent** (L20.5 conjecturale au Tour 20). Confirme que l'extrapolation à partir de ≤ 2 points (n=3, n=4) est suspecte (déjà signalé §4 q.10, désormais formalisé en q.12).

### 📚 Audit bibliographique des 8 ÉTABLIS (mai 2026 — post-clôture Lean)

Vérification croisée systématique (Réfuteur, recherche web) des Tours 12-20
contre la littérature DNF-MIN. Statut individuel :

| Tour | Théorème | Verdict de l'audit | Référence(s) trouvées |
|---|---|---|---|
| 12 | `dnfMin(parity_n) = 2^(n−1)` | **Folklore** — exercice classique | UC Berkeley CS294-152 (Williams, Fall 2018) ; Stanford CS254 lecture 13 (Trevisan) ; Immerman *Lower Bounds* ch.13 |
| 13 | Caractérisation IS-`Q_n` ⟺ DNF-MIN = `|f^{-1}(1)|` | **Folklore probable** | Hammer & Kogan, *Prime implicants and minimal DNFs*, ch.3 in Crama-Hammer 2011 |
| 14 | `dnfMin(maj_n) = C(n, ⌈n/2⌉)` | **Folklore** — conséquence directe Sperner + monotonie | Boolean Zoo (Weizmann) ; ≥ années 1970, peut-être plus tôt |
| 15 | `dnfMin(thr_{t,n}) = C(n, t)` | **Folklore** par extension L14 | Idem L14 |
| 16 | `dnfMin(mod_{p,n}) = Σ_{k≡0 mod p} C(n,k)` | **Folklore** par extension L13 | Idem L13 |
| 17 | `dnfMin(IP_{2n}) = (3^n − 1)/2` (empirique n=1..4) | **NON RECENSÉ après recherche étendue** (2e campagne, 2026-06-09) | 10+ sources consultées dont Jukna 2012 (587 p. greppées), lignée depth-3 2021-2026 (GKW21, FGT22, GGM24, Amano23), Cohen-Shinkar 2016, Sasao-Butler 2001, Sergeev. Plus proche parent : FGT22 (« 2-CNF consistent with IP accepts ≤ 3^{n/2} assignments, tight » — côté CNF, pas DNF). Réserves : école russe Yablonskii non indexée + 2 sources Sasao-Butler inaccessibles. **Candidat note courte.** Détail : [`bib/l18_status.md`](bib/l18_status.md) |
| 18 | Preuve structurelle pour tout `n` de L17 | **NON RECENSÉ** (idem) | Idem L17 — la méthode (récurrence sur bi-décomposition EXOR disjointe) est dans l'esprit Sasao-Butler (MSOP de fonctions décomposables) mais la formule close pour IP n'a pas été trouvée |
| 19 | `dnfMin(f) = |primes(f)|` ⟺ tous premiers ont témoin essentiel | **Folklore quasi-certain (sous forme duale)** | Hellerstein & Kletenik, *On the gap between ess(f) and cnf_size(f)*, arXiv:1106.4247 (2011) / *Discrete Applied Mathematics* (2015) ; concept d'essential prime implicant remontant à Quine 1952 |
| 20 | Antipodales : `|primes| = n(n−1)`, `dnfMin = n`, défaut `n(n−2)` | **Probablement connu** comme exemple d'écart maximal | Non identifié précisément ; vraisemblablement dans Crama-Hammer 2011 ch.3 ou Hellerstein-Kletenik 2011 comme exemple |
| 22 | L22.A (cas dégénéré) : Z coord-dégénéré sur j ⇒ défaut(f) = défaut(g) ≤ (n−1)(n−3) | **Folklore probable** | Réduction triviale par élimination de variable libre (Quine-McCluskey) ; mécanisme standard de simplification booléenne. |

**Conséquences épistémiques** :

1. Les 8 théorèmes **restent valides** comme corpus vérifié (preuves
   combinatoires auditées, vérifications empiriques à n=4 OK).

2. Mais leur statut épistémique passe de *« théorèmes ÉTABLIS pour P vs NP »*
   à *« re-démonstration vérifiée de classiques DNF-MIN »*. La distinction est
   significative :
   - **Pas de novelty mathématique** sur 7/8 (L18 reste incertain).
   - **Apport réel** = boucle Proposeur/Réfuteur a re-prouvé proprement,
     pas découvert.

3. **Le lien à P vs NP** revendiqué pour ces 8 théorèmes est *factuellement
   correct mais marginal* : ils établissent `AC⁰ d=2 polynomial ⊊ P` (par
   exemples explicites) — ce qui est de toute façon connu depuis FSS 1981.
   Ils ne franchissent **aucune** des trois barrières (relativisation, RR,
   algébrisation) au-delà de ce qui est nécessaire pour profondeur 2.

4. **L'affirmation initiale** *« il n'y a pas de littérature scientifique à
   ce sujet à ma connaissance »* (à l'origine de la duplication vers le dépôt
   Lean) est **falsifiée**. La littérature existe mais était dispersée entre :
   - Logique booléenne classique (Quine 1952).
   - Théorie des fonctions monotones (Sperner, Korshunov).
   - Complexité moderne, forme duale CNF (Hellerstein-Kletenik 2011).

5. **Méthode d'audit à généraliser** : la condition `(q)` ajoutée au §5
   (« audit bibliographique préemptif ») est la formalisation de cet
   apprentissage. Le Tour 22 devra l'appliquer.

### ⚠️ Lacunes réparables récentes

- **Piste 23 — threshold polynomial complexity `tcomp` pour TC⁰** (cf. [`tours/tour_23_tcomp_tc0_lacune.md`](tours/tour_23_tcomp_tc0_lacune.md) et [`checks/tour_23_refuter_tcomp.py`](checks/tour_23_refuter_tcomp.py)).
  - Mesure empirique via ILP de `(deg_min, mag_min)` pour 13 fonctions à n=4..8. Conjecture T23.1 : `tcomp(IP_{2k}) = (k, 2^{k-1})` confirmée à 3 points.
  - **Acquis méthodologique** : 1er tour avec auto-vérification indépendante sans divergence (13/13 chiffres confirmés). 1er tour à honorer toutes les conditions (a)-(r). Instrument ILP réutilisable pour Tour 24+.
  - **Lacunes** : (a) `tcomp` confond max-magnitude L∞ et L1-weight standard (Krause-Pudlák utilise L1) ; (b) T23.1 = vérification de folklore (Bruck-Smolensky 1992, conjecture d'Anthony sur PTF degree) ; (c) cible TC⁰ d=2 \ TC⁰ d=1 non explorée (seul IP testé en d=2) ; (d) pont à Williams CAPP non démontré (Beigel-Tarui utilise polynômes exacts mod 2^ℓ, pas PTF entiers).
  - Réparations : reformuler `tcomp` avec weight L1, étendre à compositions MAJ ∘ MAJ ou THR ∘ THR, construire pont algorithmique explicite. Voir §5 Tour 24.

- **Piste 21 — preuve partielle de L20.5** (cf. [`tours/tour_21_l20_5_partiel.md`](tours/tour_21_l20_5_partiel.md) et [`checks/tour_21_l20_5_structural.py`](checks/tour_21_l20_5_structural.py)) : tentative de prouver L20.5 (unicité antipodale pour tout n) par décomposition selon `k = |f^{-1}(0)|`.
  - **L21.A** (k=1) : prouvé trivialement (défaut = 0, n littéraux conflictuels). ✅ Établi (intégré comme cas particulier de l'analyse résiduelle).
  - **L21.B** (k=2 antipodal) : = Tour 20, déjà ÉTABLI.
  - **L21.C** (k=2 non-antipodal) : **prouvé rigoureusement par le Réfuteur**. WLOG `α = 0^n`, `β = 1^d 0^{n-d}` avec `1 ≤ d ≤ n−1`. Implicants premiers : Cas 1 (taille 1, `n−d` éléments) et Cas 2 (taille 2 sur d positions, `d(d−1)` éléments). `|primes| = d² − 2d + n`, maximum à `d = n−1` : `n² − 3n + 3 < n(n−2)` pour `n ≥ 4`. Cas n=3 vérifié directement.
  - **L21.D** (k ≥ 3) : **❌ RÉFUTÉE Tour 22** par contre-exemple direct (k=5, n=5). Voir §❌ Réfutés.

  **Verdict révisé post-Tour 22** : L21 passe de ⚠️ LACUNE RÉPARABLE à ❌ FAILLE FATALE car son objectif initial (prouver L20.5 pour tout n) est désormais structurellement *impossible* — L20.5 elle-même étant réfutée. L21.A/B/C restent corrects comme sous-résultats indépendants, mais ils ne reconstituent pas un théorème.

### ❓ Conjecturaux pour P vs NP (plausibles mais non prouvés)
- *(aucun retenu pour l'instant)*

### 📚 Acquis hors-but principal (objets mathématiques sans lien démontré à P vs NP)

> **Note de recadrage (fin tour 9).** Les objets ci-dessous sont mathématiquement
> corrects et vérifiables, mais leur lien à P vs NP n'a pas été établi. Ils sont
> conservés pour leur intérêt mathématique propre (algèbre commutative
> computationnelle des fonctions monotones), mais ne comptent **pas** comme
> progrès sur la question du dépôt. Pour qu'ils en deviennent un, il faudrait
> exhiber un pont vers une borne de complexité — pont qui a échoué à chaque
> tentative (cf. Tour 7 : pd ne capture pas D_m via le contre-exemple OR_n).

- **Atlas des 95 fonctions monotones n=4 à résolution pure** (Tour 8, cf. [`checks/tour_08_atlas_boij_soderberg.py`](checks/tour_08_atlas_boij_soderberg.py)) — sur les 168 fonctions monotones non-constantes sur n=4 variables, exactement **95** ont un idéal de Stanley-Reisner à résolution libre minimale pure (au sens Boij-Söderberg : un seul shift par index homologique). La distribution par taille d'implicants + nombre d'implicants est tabulée dans le tour 8. *Lien à P vs NP : aucun démontré.*

- **Théorème L9.1** (Tour 9) : *pure ⇒ equigenerated*. Pour toute fonction monotone non-constante `f`, si `I_f` admet une résolution libre minimale pure alors tous ses implicants premiers ont la même taille. **Preuve triviale par contrapositive** : deux degrés différents `t_1 ≠ t_2` impliquent `β_{0,t_1}(I) > 0` et `β_{0,t_2}(I) > 0`, donc deux shifts à l'index 0, non-pure. Vérifié empiriquement sur n=4 (0 contre-exemple sur 167) et n=5 (0 contre-exemple sur 7579). *Lien à P vs NP : aucun démontré.*

- **Fait empirique** (Tour 9, cf. [`checks/tour_09_extension_n5.py`](checks/tour_09_extension_n5.py)) : la réciproque *equigenerated ⇒ pure* est **vraie sur n=4** (167 fonctions sans exception) mais **fausse sur n=5** (215 contre-exemples sur 7579). Contre-exemple minimal canonique : `f = (x₁∧x₂∧x₃) ∨ (x₁∧x₂∧x₄) ∨ (x₀∧x₃∧x₄)` ; tous mintermes de taille 3 (equigenerated), mais `β_{0,3}(I)=3, β_{1,4}(I)=1, β_{1,5}(I)=1` (deux shifts à l'index 1, donc non-pure). Causé par hétérogénéité des syzygies linéaires (deg 4) et quadratiques (deg 5) à l'intérieur du même idéal. *Lien à P vs NP : aucun démontré.*

- **Tableau de contingence n=5** :
  ```
                  | equi=True | equi=False
  pure=True       |      1894 |          0
  pure=False      |       215 |       5470
  ```

- **Fait empirique négatif sur la conjecture C10** (Tour 10, cf. [`checks/tour_10_intersection_uniform_conjecture.py`](checks/tour_10_intersection_uniform_conjecture.py)) : la caractérisation candidate *« pour `f` equigenerated, `I_f` pure ⟺ toutes les intersections non-vides entre paires de mintermes ont la même taille »* est **fausse dans les deux directions** sur n=5. Sur 2110 fonctions equigenerated non-constantes : **1068 contre-exemples** (893 cas pure-mais-non-uniform + 175 cas uniform-mais-non-pure). Cf. tableau :
  ```
                  | uniform=True | uniform=False
  pure=True       |         1002 |           893
  pure=False      |          175 |            40
  ```
  Le Proposeur a effectué ce test **avant** de soumettre la conjecture (condition (j) honorée pour la 2e fois consécutive) et a retiré C10 sans la proposer. *Lien à P vs NP : aucun démontré.*

### ⚠️ Lacunes réparables (direction légitime mais énoncé spécifique faux)

- **Piste 6 — « Gap homologique sémantique sur Stanley-Reisner ».** Première piste à ne PAS être en faille fatale. Direction correcte (topologie sémantique pour fonctions monotones, lignée Razborov 1985 / Knill-Forman / Björner-Wachs / Reiner-Welker), mais énoncé du Proposeur faux :
  - **Lemme 2 réfuté empiriquement** (cf. [`checks/tour_06_stanley_reisner.py`](checks/tour_06_stanley_reisner.py)) : sur les 168 fonctions monotones de `n = 4`, **52 ont `β_1(Δ_f) > 0`**, et **les 52 violent** la borne « taille > #faces maximales ». Contre-exemple canonique : `f = (x_0 ∧ x_2) ∨ (x_1 ∧ x_3)`, dont `Δ_f` est le complexe de drapeau du 4-cycle C_4 (β_1 = 1), mais taille de circuit = 2 < 4 = #faces maximales.
  - **Lemme 1 imprécis** : confond le complexe `Δ_f` avec l'**idéal** `I_{Δ_f}` (engendré par les non-faces minimales). Les implicants premiers sont les générateurs de l'idéal, *pas* des faces de Δ_f. Reformulé correctement, L1 devient une tautologie définitionnelle.
  - **(f) non satisfaite** : calcul promis (« je m'engage à concevoir un script SageMath ») non livré ; je l'ai effectué à la place, et il a réfuté la conjecture sous-jacente.
  - **Signe d'alarme RR** : l'invariant `β_i` est calculable en temps polynomial sur la table de vérité (constructif), et `β_1 > 0` est large (31 % à n=4). Si la borne marchait, elle serait *naturelle* au sens de Razborov-Rudich, donc condamnée par les preuves naturelles sous crypto standard.

  Pour réparer : reformuler en termes d'idéal de Stanley-Reisner et invoquer des invariants algébriques plus fins (régularité de Castelnuovo-Mumford, profondeur projective, Betti gradués / formule de Hochster). Mais alors la piste sort du cadre « calcul exhaustif sur n=5 » et entre dans l'algèbre commutative computationnelle — direction active mais bien plus difficile. La lacune est précise (énoncé à raffiner) mais sa réparation déplace hors du sous-but Tour 6.

- **Piste 7 — « Obstruction homologique duale (résolutions libres + dualité d'Alexander) ».** Le Proposeur a fait le pivot exact suggéré au Tour 6 : `Δ_f` → idéal `I_f`, avec résolutions libres minimales et dualité d'Alexander/Eagon-Reiner. Premier tour à honorer **(h)** : chiffres livrés (`Betti(I_{C_4}) = (4,4,1,0)`, `Betti(I_{K_4}) = (6,8,3,0)`, pd = 2 pour les deux), vérifiés indépendamment par implémentation de Hochster (cf. [`checks/tour_07_resolutions_libres.py`](checks/tour_07_resolutions_libres.py)). Mais **le Lemme 2 conjectural (D_m(f) ≥ Ω(pd(I_f))) est réfuté par contre-exemple OR_n** :
  - `I_{OR_n} = m = (x_1, …, x_n)`, résolution Koszul → pd(I) = n − 1.
  - `D_m(OR_n) = 1` (un OR de fan-in n) ou `log_2 n` (binaire).
  - Pour n = 3, 4, 5, 6 : pd(I) ∈ {2, 3, 4, 5}, D_m = 1 partout. Aucune constante c > 0 ne sauve L2.

  **Raison structurelle profonde** : toute fonction monotone non-constante admet une DNF de profondeur 2, donc `D_m(f) ≤ 2` sans contrainte de taille. Aucune inégalité `D_m ≥ f(pd)` non-bornée ne peut tenir, OR_n étant le cas extrême. Même MAJ_n viole L2 pour n ≥ 7 (D_m=2, pd=⌊n/2⌋−1).

  Le Proposeur lui-même admet (Aveu 1) que L2 est conjectural, et (Aveu 2) que le cadre se limite aux formules monotones — pas aux circuits, donc même un L2 valide ne donnerait pas P vs NP.

  **Verdict ⚠️ LACUNE RÉPARABLE** (meilleur tour à ce stade) : direction techniquement saine, chiffres corrects, (h) honorée. La lacune précise est l'**invariant algébrique manquant** : `pd` ne capture pas `D_m`. Toute proposition future doit passer le test OR_n (où pd explose mais D_m reste petit).

- **Piste 8 — « Atlas de Boij-Söderberg des fonctions monotones n=4 ».** Premier tour à abandonner explicitement la prétention à P vs NP (condition (i) honorée) au profit d'un objet de catalogage fini. Mouvement stratégique correct. Mais le Lemme 4 (« OR_n et AND_n sont les seules fonctions monotones à résolution pure, prouvable inconditionnellement pour tout n ») est **massivement faux** (cf. [`checks/tour_08_atlas_boij_soderberg.py`](checks/tour_08_atlas_boij_soderberg.py)) :
  - Faux dès n=3 : `MAJ_3 = I(K_3) = (x_0 x_1, x_0 x_2, x_1 x_2)` a Betti(I) = (3, 2) à shifts (2, 3) — résolution pure (r=1), pourtant ni OR_3 ni AND_3.
  - Sur n=4 : **95 fonctions monotones sur 167 non-constantes** ont des résolutions pures, pas 2. Erreur d'un facteur ~47. La 4-classe des fonctions threshold (OR_4, MAJ_4, THRESHOLD_3, AND_4) est pure (par Veronese squarefree), plus de nombreuses autres : OR de littéraux, paires d'arêtes disjointes (shifts non-consécutifs (2,4)), AND simples, etc.
  - Justification mathématique invoquée (Herzog-Kühl) mal interprétée : HK 1984 donne des contraintes sur Betti pour résolutions pures, pas une caractérisation binaire « linéaire ou principal ».
  - (h) toujours non honorée : aucun script livré, aucun CSV, aucun calcul. Le Réfuteur effectue le travail à sa place.

  **Atlas livré (sous-produit positif) :** classification des 95 fonctions monotones n=4 à résolution pure, avec mintermes et shift sequences. C'est le **premier objet mathématique positif** du dépôt, au-delà des réfutations. Reproductible via `checks/tour_08_atlas_boij_soderberg.py`.

  **Verdict ⚠️ LACUNE RÉPARABLE (3e consécutive)** : posture stratégique correcte, direction valide, atlas utile produit ; mais l'unique théorème revendiqué est faux. Pattern persistant sur 8 tours : le Proposeur corrige le défaut tour précédent mais introduit une nouvelle conjecture qui se révèle fausse à l'examen.

- **Piste 8 bis — Révision du Proposeur** (réponse au verdict ci-dessus). Admission honnête de l'erreur du Lemme 4, retrait, et révision en : *« I_f a résolution pure ssi f est une fonction threshold TH_t, à permutation près »*. **Encore faux** :
  - Prédit 4 fonctions threshold pures sur n=4. Réalité (mon atlas) : 95.
  - 4 contre-exemples concrets dans l'atlas même : `f = x_0` (1 minterme, pas threshold), `f = x_0 ∨ x_1` (2 mintermes, pas threshold), `f = (x_0∧x_1) ∨ (x_0∧x_2)` (2 mintermes de taille 2, mais TH_2 = MAJ_4 en a 6), `f = (x_0∧x_1∧x_2) ∨ (x_0∧x_1∧x_3)`.
  - Plus précisément : les sous-OR et sous-AND (fonctions dépendant de < n variables) ont toutes des résolutions pures et ne sont pas thresholds.
  - **Violation immédiate de (j)** : le Proposeur a soumis ce mini-théorème révisé sans avoir vérifié contre l'atlas n=4 que je venais de produire et publier. C'est exactement la condition (j) que (j) cherchait à empêcher, violée en temps réel.

  Pattern désormais établi sur 9 itérations (8 tours + 1 révision) : le Proposeur articule des théorèmes asymptotiques sans calcul empirique préalable, même quand la condition est explicitement énoncée. La boucle adverse (Réfuteur exécutant les calculs) est apparemment **nécessaire en permanence** pour catalyser une rigueur empirique que le Proposeur seul ne maintient pas.

- **Piste 9 — « Conjecture C9 : pure ⟺ equigenerated ».** Premier tour où le Proposeur honore vraiment (h) et (j) : il livre le script `checks/tour_09_equigeneration_conjecture.py` qui vérifie sa conjecture à n=4 (tableau parfait 95/0/0/72) avant soumission. Il anticipe explicitement le risque de réfutation à n=5 (Aveu 1). C'est un saut épistémologique réel.
  - **L9.1 (pure ⇒ equigen)** : triviale par contrapositive, confirmée. ✓ Établi.
  - **L9.2 (equigen ⇒ pure)** : vraie sur n=4 mais **fausse sur n=5**. J'ai écrit `tour_09_extension_n5.py` qui énumère les 7581 fonctions monotones n=5 via récursion de Dedekind, identifie 215 contre-exemples. Contre-exemple minimal : `(x₁x₂x₃) ∨ (x₁x₂x₄) ∨ (x₀x₃x₄)`, equigenerated mais avec deux shifts (4 et 5) à l'index 1 — due à coexistence de syzygies linéaires (deg 4, paires partageant 2 var) et quadratiques (deg 5, paires partageant 1 var).
  - **Verdict ⚠️ LACUNE RÉPARABLE (4e consécutive)** avec note positive : la conjecture est réfutée, mais l'**épistémologie est correcte**. Le Proposeur a posé une conjecture testable et falsifiable, anticipé le risque, et apporté un script vérifiable. C'est le meilleur tour à ce stade.

  La conjecture raffinée (à venir, problème ouvert) : *quelles conditions combinatoires distinguent les 1894 cas où equigen ⇒ pure tient des 215 cas où elle échoue ?* Question d'algèbre commutative intéressante en soi.

- **Piste 10 — Test préemptif de C10 + pivot Lean Koszul (rejeté).** Deux mouvements distincts :
  - **(a) Excellente épistémologie** : le Proposeur a testé sa conjecture candidate C10 (« intersections uniformes ») sur les 2110 fonctions equigenerated n=5 *avant* de la soumettre. 1068 contre-exemples identifiés. **Conjecture retirée par le Proposeur lui-même.** (j) honorée pour la 2e fois consécutive. Pattern « conjecture spéculative → réfutation » enfin brisé.
  - **(b) Pivot mal ciblé** : faute de C10, le Proposeur propose de formaliser en Lean la résolution de Koszul de `m_n = (x_1, …, x_n)`. **Bon mouvement stratégique** (sortir de la spéculation, viser certification mécanique) mais **mauvais théorème cible** : Koszul de `m_n` est hors-sujet vis-à-vis de P vs NP. Le Proposeur l'admet explicitement (*« Distance à P vs NP : maximale, assumée »*). Viole (i) corrigée et (k) ajoutée.

  **Recadrage utilisateur** : direction prescrite pour Tour 11 = **mini-théorème `PARITY ∉ AC⁰` profondeur 2 sur n=4 ou n=5**. Calcul exhaustif Python (énumérer les DNF/CNF de taille bornée, vérifier qu'aucun ne calcule `parity_n`) + perspective formalisation Lean. Lié à P vs NP via la lignée Furst-Saxe-Sipser 1981 → Razborov-Smolensky 1987 → Williams 2011.

  **Verdict ⚠️ LACUNE RÉPARABLE** : épistémologie excellente, mais direction à corriger.

- **Piste 11 — Lifting (Raz-McKenzie / GPW) + Karchmer-Wigderson + Tseitin sur expandeur → `D_m(2COL_G) ≥ Ω(n log n)`.** Première proposition recentrée sur P vs NP après le recadrage. Cadre théorique réel (Ben-Sasson-Wigderson 2001, Raz-McKenzie 1999, Göös-Pitassi-Watson 2018, Karchmer-Wigderson 1990). Conditions (i), (k), (l) honorées. **Mais** :
  - **Erreur factuelle décisive** : 2-COLORATION = test de bipartiteness, **dans P** (BFS/DFS linéaire), **pas NP-complet**. Toute la motivation revendiquée (« fonction monotone NP ») s'effondre. 3-COL est NP-complète, CLIQUE_k aussi ; 2COL ne l'est pas. Erreur de niveau cours de licence en complexité.
  - **Erreur de cadre** : 2COL n'est pas naturellement monotone (ni en coloration ni en arêtes). Karchmer-Wigderson exige une fonction monotone identifiée, ce qui n'est pas le cas.
  - **Chaîne L10.5 conjecturale** : la transposition « lifted Tseitin → 2COL via KW » est admise non prouvée par le Proposeur (Aveu 2). Pattern récurrent qui a tué les Tours 4, 7, 9.
  - **(j) régressée** : test empirique sur n=4, 6, 8 promis mais aucun script livré, aucun résultat numérique. Régression par rapport aux Tours 9 et 10 où (j) avait été honorée.
  - **Redondance possible** avec Garg-Göös-Knop-Watson 2018 non vérifiée bibliographiquement.

  Réparations possibles : remplacer 2COL par **CLIQUE_k** (monotone et NP-complète, exactement Razborov 1985), livrer le test empirique, vérifier GGKW 2018 et la chaîne L10.5. Mais ces réparations sont substantielles et le pattern conjecture-pont persiste.

  **Décision utilisateur (option 1)** : rejet maintenu, prescription Tour 12 = prescription Tour 11 du recadrage réaffirmée = **`PARITY_n ∉ AC⁰ profondeur 2` sur n=4 par calcul exhaustif Python**.

  **Note méthodologique** : c'est la 2e fois consécutive (Tours 10 et 11) que le Réfuteur doit *prescrire* la direction plutôt que réfuter une proposition cohérente. La boucle adverse à un Proposeur LLM, après 10 itérations, a épuisé l'espace des « grandes idées spéculatives » et doit se rabattre sur des cibles techniques précises et bornées.

- **Piste 12 — Mini-théorème `PARITY_n ∉ AC⁰ profondeur 2` de taille `< 2^(n-1)`.** Le Proposeur accepte intégralement la prescription du recadrage, exécute le calcul *avant* soumission, livre le script `tour_12_parity_ac0.py` et les chiffres exacts. **Toutes les 12 conditions (a)–(l) honorées pour la première fois.**
  - L'argument structurel L12.1–L12.4 est combinatoire élémentaire et valable pour tout n, prouvé.
  - Vérification exhaustive n=4 : 81 ANDs énumérés, 8 implicants tous de taille 4, bijection avec les 8 affectations impaires, DNF canonique de taille 8 calcule `parity_4`. Reproduit indépendamment par le Réfuteur.
  - Test des trois barrières confirmé : relativisation (preuve combinatoire sans oracle), preuves naturelles (propriété pas large : seules `parity` et `¬parity` ont implicants tous de taille n, donc `2/2^{2^n}` ≪ `2^{-O(n)}`), algébrisation (pas d'arithmétisation).
  - **Premier objet ✅ ÉTABLI POUR P vs NP du dépôt.** Après 11 itérations dont 5 FAILLE FATALE et 6 LACUNE RÉPARABLE / rejets, le dépôt a enfin un théorème prouvé et aligné sur la question.
  - *Novelty mathématique : zéro* (théorème de FSS 1981 profondeur 2, dans tout manuel). Mais *novelty épistémique pour le dépôt* : premier théorème réellement démontré et lié à P vs NP, ce qui n'avait jamais été fait dans les 11 tours précédents.

  Cf. [`tours/tour_12_parity_ac0_etabli.md`](tours/tour_12_parity_ac0_etabli.md).

### ❌ Réfutés (faux — et pourquoi, pour ne pas y revenir)
- **Piste 1 — « contradiction de compressibilité des témoins ».** Le sophisme central : la confrontation oppose un Kt **inconditionnel** (Lemme 1, incompressibilité Ω(n)) à un Kt qui n'est petit que **conditionnellement à x** (Lemme 2, vrai sous la forme K(w|x)=O(1), pas K(w)=O(log n) — la description doit embarquer x, de taille poly(n)). En unifiant les deux quantités, la contradiction disparaît : soit Lemme 2 redevient faux (inconditionnel), soit Lemme 1 redevient faux (conditionnel, car le témoin lex-premier est déterminé par x). Le fossé entre conditionnel et inconditionnel **est** P vs NP → circularité.
- **De plus : la piste 1 relativise** (Kt, auto-réductibilité, recherche↔décision relativisent tous). Par BGS, elle ne peut donc structurellement pas séparer P de NP, même réparée. À NE JAMAIS réessayer sous cette forme.

- **Piste 2 — « signature p-adique des témoins (Ax-Katz pour AC⁰) ».** Quatre failles convergentes, deux vérifiées par calcul (cf. [`checks/tour_02_axkatz_p_adique.py`](checks/tour_02_axkatz_p_adique.py)) :
  1. Le « Lemme 1 » revendique une arithmétisation AC⁰ → degré polylog. Faux pour l'arithmétisation **exacte** : la version polylog (Razborov-Smolensky) est une **approximation probabiliste**, et Ax-Katz exige des polynômes exacts. Empiriquement, l'arithmétisation exacte d'un 3-CNF à `k` clauses a un degré strictement égal à `3k = poly(m)`.
  2. Le « Lemme 2 » (Ax-Katz force `μ ≈ m/d` polynomial) **s'écroule sous la contrainte booléenne** `w_i² = w_i`. Les `m` équations ajoutées (degré 2 chacune) font passer le minorant à `⌈(m − d − 2m) / max⌉ ≤ 0` — **trivial dans tous les cas**. Ax-Katz ne dit absolument rien sur le nombre de témoins booléens. C'est précisément pour cela qu'on n'utilise pas Ax-Katz en complexité booléenne.
  3. La technique **algébrise** au sens d'Aaronson-Wigderson : l'invariant `v_p(N_x)` est une fonction d'une extension algébrique du vérificateur, donc relativise par rapport aux oracles algébriques relativement auxquels `P^Õ = NP^Õ`. L'argument anti-algébrisation du Proposeur (« `Õ` ne respecte pas le degré polylog ») est circulaire : la contrainte de degré polylog est sa propre invention, pas une propriété du cadre AW.
  4. « Lemme 3 » (arithmétisation de P) faux par le même mécanisme que (1) : un algorithme polynomial en temps `n^k` s'arithmétise à la Shamir en degré `n^{O(k)}` polynomial, pas polylog. La « contrainte géométrique » du Lemme 4 disparaît.

  À NE JAMAIS réessayer sous cette forme. **Nuance honnête** : le programme algébrique-géométrique en complexité existe (GCT, permanent vs déterminant), mais il n'utilise pas Ax-Katz pour les raisons ci-dessus. Confondre comptage algébrique (Ax-Katz) et existence booléenne (P vs NP) est l'erreur centrale.

- **Piste 3 — « obstruction topologique sur le paysage d'énergie d'un CSP ».** Deux failles fatales indépendantes, vérifiées par calcul (cf. [`checks/tour_03_topologie_morse.py`](checks/tour_03_topologie_morse.py)) :
  1. **L'invariant `Σ β_i(L_k(φ))` n'est pas une fonction de la fonction booléenne, mais de sa présentation syntaxique.** Le Proposeur l'admet (« deux formules équivalentes peuvent avoir des paysages différents ») sans en mesurer la conséquence. Démontré numériquement : pour ψ = (x_0∨x_1) ∧ (x_2∨x_3) ∧ (x_4∨x_5) et ψ' = ψ avec chaque clause triplée (mêmes 27 témoins, fonction booléenne identique), `Σ β_i(L_1)` vaut **92 pour ψ et 29 pour ψ'** (facteur 3) ; à `k=2`, **125 vs 29** (facteur 4). Conséquence : un algorithme P pour SAT peut préprocesser toute CNF en forme canonique en temps poly avant de décider — toute borne inférieure dérivée d'un invariant variant sous équivalence logique s'évanouit. `P` et `NP` étant des classes de fonctions/langages, un tel invariant ne peut structurellement pas les séparer. Ce n'est pas RR, c'est plus grave : on sort du cadre P vs NP.
  2. **Le Lemme 3 (MT modélisée comme champ de vecteurs à sauts bornés) est faux.** Une MT en temps `n^c` peut modifier `n^c` bits par étape ; le graphe pertinent est `G_{n^c}` = cube avec arêtes Hamming ≤ `n^c`. Dès `r = 2`, les Betti s'effondrent. Démontré sur CSP `x_i = x_{i+3}` (8 témoins sur la diagonale) : `β_0 = 8` à `r = 1`, mais `β_0 = 1` dès `r = 2`. La théorie de Morse discrète (Forman 1998) est strictement à 1-saut ; sa généralisation aux sauts polynomiaux trivialise l'obstruction. *Sans* Lemme 3, le Lemme 4 ne se prouve pas.

  À NE JAMAIS réessayer sous cette forme. **Nuance honnête** : le clustering topologique des CSP en phase RSB (Mézard-Parisi-Zecchina, Achlioptas et al.) borne effectivement les algorithmes **locaux** — pas P entier. Confondre « bornes pour algos locaux » et « bornes pour P » est l'erreur centrale.

- **Piste 4 — « compilation TC⁰ → tensor network à bond polynomiale + Williams + hardness magnification ».** Première piste à cocher formellement les 5 conditions du sous-but ; les attaques portent donc sur le contenu technique. Faille fatale principale, vérifiée par calcul (cf. [`checks/tour_04_tensor_network_TC0.py`](checks/tour_04_tensor_network_TC0.py)) :
  1. **Le Lemme 1 (« tout circuit TC⁰ de profondeur d et taille S compile en bond dimension χ = S^{O(d)} ») est faux.** Contre-exemple direct : `IP_n(x,y) = (x · y) mod 2`, calculable par un circuit TC⁰ de profondeur 2 et taille polynomiale (Hajnal-Maass-Pudlák-Szegedy 1993). Sa matrice de communication à la coupe `x|y` a un rang sur ℝ valant exactement `2ⁿ − 1` (essentiellement la matrice de Hadamard à un facteur près). Bond dimension = `2ⁿ − 1`, exponentielle, calculée pour `n ∈ [1, 8]`.
  2. **La parade « passer à F₂ »** (où le rang chute à `n`) **détruit l'outillage**. Le mécanisme proposé (SVD adaptative, décroissance des valeurs singulières, troncation analytique) est intrinsèquement analytique sur ℝ/ℂ — pas de SVD ni de norme L² sur F₂. De plus, un rang `n` sur F₂ représente `n × 2ⁿ` bits, sans gain sur la table de vérité.
  3. **Confusion structurelle :** le Proposeur conflate « TC⁰ est petit en circuit » et « TC⁰ a faible intrication ». Or TC⁰ peut calculer IP_n donc atteindre la complexité de communication maximale `Θ(n)`. Les techniques de rang/discrépance/communication, qui marchent pour AC⁰, **échouent toutes pour TC⁰** depuis 1993 — exactement la raison pour laquelle les bornes inférieures pour TC⁰ restent ouvertes.
  4. **Sans le Lemme 1**, l'idée se réduit à « trouver un algorithme CAPP non-trivial pour TC⁰ et appliquer Williams ». C'est le programme de recherche actif de la communauté depuis 2010 (Williams, Murray, Chen, Tamaki, Servedio, Tal...) — pas une contribution.
  5. **Bonus** : la hardness magnification (utilisée pour passer de NEXP à NP) a ses propres barrières internes connues (Chen-Hirahara-Oliveira-Pich-Rajgopal-Santhanam 2019, « Beyond Natural Proofs »).

  À NE JAMAIS réessayer sous cette forme spécifique. **Nuance honnête** : la *direction générale* (Williams pour TC⁰) reste la plus prometteuse aujourd'hui — mais sans algorithme nouveau, ce n'est pas une piste exploitable dans notre boucle adverse. Le Proposeur a entendu le feedback (cible adéquate, conditions formelles cochées) mais n'a apporté aucune contribution technique au-delà de la stratégie globale.

- **Piste 5 — « indistinguabilité CPT+C des hypercubes colorés `H_f` (jeux de pavage bijectifs + canonisation Dawar) ».** Pivot vers la complexité descriptive. Triple faille (cf. [`checks/tour_05_cpt_jeux_pavage.py`](checks/tour_05_cpt_jeux_pavage.py)) :
  1. **Lemme 3 trivialement impossible** : le Proposeur veut `H_f` (UNSAT) ≡_{CPT+C} `H_g` (SAT). Or la sentence FO `∃ x. f(x) = 1` distingue toute paire (UNSAT n'a aucun sommet colorié 1, SAT en a au moins un), et FO ⊂ FO+C ⊂ CPT+C. Le Spoiler gagne en 1 tour. Vérifié pour 3 paires explicites : multiset `(#col 0, #col 1)` toujours `(64, 0)` UNSAT vs `(<64, ≥1)` SAT.
  2. **Mauvais encodage** : la propriété distinguante (SAT vs UNSAT) est encodée *en surface* (la coloration), donc trivialement FO-définissable. Une vraie construction CFI doit cacher la propriété dans la structure relationnelle (graphe, relations entre sommets), pas dans une coloration directe.
  3. **Lemme 1 mal formulé** : le « théorème de Dawar » invoqué (« GI ∈ P ⇒ CPT+C capture NP sur les hypercubes ») n'existe pas. La conjecture Blass-Gurevich correcte (`CPT+C = P`) reste ouverte ; tout résultat est *conditionnel* à cette conjecture, donc jamais inconditionnel pour P vs NP.
  4. **Condition (f) non satisfaite** : aveu explicite *« feuille de route »*, pas de contribution.

  À NE JAMAIS réessayer sous cette forme. **Nuance honnête** : la complexité descriptive (Immerman, Vardi, Gurevich, Dawar, Grohe) est un programme actif et prometteur, avec des avancées récentes sur graphes structurés. Mais elle ne peut pas être empruntée par l'encodage trivial de SAT comme coloration de l'hypercube — il faut une structure relationnelle non-triviale.

- **Conjecture L20.5 — « les antipodales sont les seules à atteindre le défaut maximal `n(n−2)` ».** Vérifié empiriquement n=3 (4/4) et n=4 (8/8), extrapolé comme corollaire structurel au Tour 20. **Faux dès n=5** : 1280 contre-exemples sur les 201 376 zero-sets de taille 5, dont 320 à défaut 17 (= 15 + 2) et 960 à défaut 16. Témoin canonique double-vérifié : `Z = {0, 3, 5, 25, 30}` (en décimal sur n=5) donne `(|primes|, DNF_min, défaut) = (25, 8, 17)`. Vérification croisée par 2 algorithmes distincts (hitting sets côté Proposeur, énumération 3^5 ANDs + ILP PuLP/CBC côté Réfuteur) — bug d'implémentation exclu. **À NE JAMAIS réessayer sous cette forme** : non seulement L20.5 est fausse, mais les contre-exemples forment une *famille substantielle* (≥ 1280) « anti-antipodale » à n=5. Voir [`tours/tour_22_l20_5_refutee.md`](tours/tour_22_l20_5_refutee.md) et [`checks/tour_22_refuter_l20_5.py`](checks/tour_22_refuter_l20_5.py).

  **Cause structurelle de la chute** : la classe des contre-exemples est *coord-non-dégénérée* (cf. L22.A maintenu) et *anti-antipodale* (aucune paire `{z, ¬z}` dans Z). C'est une classe que ni le Tour 20 ni le Tour 21 n'avaient envisagée comme distincte.

- **Lemme L21.D — « pour k = |f^{-1}(0)| ≥ 3, défaut(f) < n(n−2) ».** Conjecturé Tour 21 sur la base d'une vérification empirique n=4 seulement. **Faux dès n=5, k=5** par le même contre-exemple `Z = {0, 3, 5, 25, 30}` qui réfute L20.5 (défaut 17 > 15). La preuve par hitting sets esquissée par le Proposeur ne pouvait pas être complétée — elle est fausse. **À NE JAMAIS réessayer sous cette forme**. La lacune n'est pas réparable : Tour 21 (programme « prouver L20.5 par cas sur k ») s'effondre puisque L20.5 elle-même est fausse.

  **Leçon transverse** : pattern « vraie à n=4, fausse à n=5 » réapparu au Tour 22 *malgré* l'avertissement explicite §4 q.10. La condition (q) audit bibliographique préemptif (introduite Tour 22 dans §5) ne suffit pas — il faut aussi la nouvelle condition (r) (voir §4 q.12 ci-dessous).

- **Piste 24 — « complexité tropicale de SAT » (encodage $P_\phi = \min_j \min(1, \sum_i \ell_{ji})$, borne $R(P_\phi) \geq 2^{n/2}$ régions linéaires).** Cinq failles indépendantes + une barrière non-mentionnée, chacune suffisante. Cf. [`tours/tour_24_tropical_refutee.md`](tours/tour_24_tropical_refutee.md).
  1. **L'encodage est INVERSÉ.** Le Proposeur affirme « $P_\phi(x) = 0$ ssi $x$ satisfait $\phi$ ». Vérifié exécutable (n=4, 5 clauses aléatoires, seed 42) : 0/16 cas honorent l'affirmation. La réalité : $T_j(x) = \min(1, \sum_i \ell_{ji}) = 1$ si $C_j$ satisfaite, $= 0$ sinon ; donc $P_\phi = \min_j T_j = 1$ ssi $\phi$ satisfaite. Erreur corrigeable mais signe que le Proposeur n'a pas calculé son propre encodage.
  2. **La borne $R(P_\phi) \geq 2^{n/2}$ est trivialement satisfaite.** Le nombre de cellules de l'arrangement de $k$ hyperplans en dim $n$ est borné par $O(k^n)$ (Zaslavsky). Pour $n=4, m \approx 17$ clauses, majorant $\binom{18}{5} = 8568 \gg 4 = 2^{n/2}$. Un polynôme tropical de complexité polynomiale dépasse trivialement la cible. Le Lemme L24.T ne dit donc *rien* sur la dureté de SAT.
  3. **Violation explicite de (q) audit bibliographique préemptif.** Le Proposeur écrit « personne n'a appliqué la géométrie tropicale à la complexité de circuit booléen ». FAUX : Jukna 2014 *Lower Bounds for Tropical Circuits and Dynamic Programs* (arXiv:1406.3065) est un papier entier sur le sujet. Jerrum-Snir 1982 ont prouvé que la complexité tropicale = complexité arithmétique monotone pour polynômes homogènes. Schnorr a des bornes pour CLIQUE. ~40 ans de littérature ignorée. Le Proposeur reconnaît son audit incomplet (« je n'ai pas identifié ») — admission de violation.
  4. **Barrière monotone Razborov-Tardos non-mentionnée mais LÉTALE.** Tropical = monotone arithmétique (Jerrum-Snir). Tardos 1988 exhibe une fonction *dans P* dont la complexité monotone est $\exp(\Omega(n^{1/6-o(1)}))$. Donc *même* une borne exponentielle sur $R(P_\phi)$ ou sur la complexité tropicale de $P_\phi$ ne dirait rien sur SAT ∉ P. La proposition était morte avant d'être écrite (mort depuis 1988).
  5. **Les 3 barrières classiques mal traitées.** Relativisation : un argument tropical *qui généraliserait* au booléen relativiserait au sens BGS ; s'il ne généralise pas, pas de P vs NP. Même dilemme que Razborov 1985 CLIQUE monotone. Preuves naturelles : $R \geq 2^{n/2}$ trivialement large, donc RR s'applique pleinement. Algébrisation : techniquement contournée mais sans valeur (barrière monotone domine).
  6. **Chaîne à P vs NP purement conjecturale.** Le Proposeur admet textuellement « cette chaîne est purement conjecturale », « cette piste est à des années-lumière de P vs NP ». Viole (k) au sens du fond (lien à P vs NP doit être substantif, pas verbal).

  **À NE JAMAIS réessayer sous cette forme.** Toute piste « tropical / monotone arithmétique / min-plus » pour P vs NP est aspirée par Tardos 1988 (cf. §1 4e ligne). **Nuance honnête** : le programme tropical de Jukna est mathématiquement vivace (bornes exponentielles pour PERMANENT, CLIQUE en monotone), mais ne donne *pas* P vs NP. Confondre « bornes tropicales / monotones » et « bornes booléennes non-monotones » est l'erreur centrale de Tour 24.

- **Piste 25 — « CFI-rigidification de 3-SAT » (gadget XOR-twist `(x_i^0, x_i^1)` avec `x_i^0 ⊕ x_i^1 = 1` + clauses jumelées + revendication d'automorphisme G = (ℤ/2)^n).** Cf. [`tours/tour_25_cfi_sat_refute.md`](tours/tour_25_cfi_sat_refute.md) et [`checks/tour_25_refuter_cfi_sat.py`](checks/tour_25_refuter_cfi_sat.py). **Faille fatale combinatoire vérifiée empiriquement à 100 %** sur 20 formules 3-SAT random à n=3.
  1. **L25.1 + L25.2 incohérents.** La « jumelée » avec contrainte XOR est *équivalente* à introduire `y_i = ¬x_i` comme nouvelle variable. Le « swap » `(x_i^0, x_i^1) ↔ (x_i^1, x_i^0)` est donc *équivalent à flipper x_i*, ce qui ne préserve pas SAT en général. Vérifié : à n=1 sur `φ = x_1`, l'unique solution de φ̃ est `(1, 0)` ; après swap, `(0, 1)`, qui n'est pas solution de φ̃. Le « groupe d'automorphismes » revendiqué n'existe pas.
  2. **Deux lectures syntaxiques possibles, aucune ne fonctionne** :
     - Lecture A (orientation `x_i^0 = "x_i vrai"`) : syntaxiquement naturelle, brise la symétrie (vérifié 100 % de contre-exemples).
     - Lecture B (clauses G-invariantes via `x_i^0 ∨ x_i^1`) : sous XOR, toujours TRUE, donc φ̃ devient tautologique et `SAT(φ) ⟺ SAT(φ̃)` échoue. Réduction triviale, perte du problème.
  3. **L25.5 conflate FPC / CPT / symmetric P.** Anderson-Dawar 2017 caractérise **FPC** (fixed-point + counting), pas P. FPC ⊊ P est *déjà prouvé* via les CFI graphs. La vraie question « logique pour P sur structures non-ordonnées » est **CPT** (Choiceless Polynomial Time, Blass-Gurevich-Shelah 1999), strictement plus puissant que FPC, encore ouvert. Le pont L25.4 → L25.5 saute le niveau CPT et ne reconstitue pas la question de Gurevich 1988.
  4. **(q) violée** : Atserias-Bulatov-Dawar 2007 (CFI affine pour CSP, encodage d'équations linéaires sur Z₂) non cité. C'est la *vraie* CFI moderne pour problèmes algébriques ; SAT n'étant pas naturellement affine sur Z₂, la transposition échoue précisément pour cette raison.
  5. **(j) violée** : le Proposeur promet « calcul concret à livrer à n=3 » en §5 aveu 5, mais ne le livre pas. Le Réfuteur l'a écrit en 5 minutes et a obtenu un contre-exemple immédiat à n=1.
  6. **Aveux honnêtes du Proposeur**, à valoriser : aveu 1 (« réduction entre deux problèmes ouverts ≠ progrès »), aveu 3 (audit biblio incomplet), aveu 5 (calcul non livré). La posture est correcte mais les aveux ne réparent pas la faille structurelle.

  **À NE JAMAIS réessayer sous cette forme.** Transposer naïvement la construction CFI (faite pour graphes ou CSP avec parité globale) à SAT (qui n'a pas d'invariant de parité naturel) ne fonctionne pas. Pour viser CPT depuis SAT, il faudrait d'abord encoder SAT dans une structure relationnelle non-triviale (e.g. graphe, hypergraphe avec relations soigneusement choisies) — ce que le Tour 5 du dépôt avait déjà tenté et échoué. **Nuance honnête** : la complexité descriptive (CPT, FPC + rank, IFPC) reste une direction autorisée §5, mais demande une construction techniquement correcte ; le saut « CFI pour graphes → CFI pour SAT » via la construction L25.1 est faux.

---

## 4. Questions ouvertes prioritaires

1. **Tout invariant proposé doit être explicitement invariant sous équivalence logique** des présentations du problème. *(Piste 3 a échoué là-dessus.)*
2. **Tout argument « tout algo P est contraint par X » doit démontrer que X survit aux sauts polynomiaux**, i.e. à l'extension `Hamming-1 → G_{n^c}`. *(Piste 3 a échoué là aussi.)*
3. **Tout argument « low-X pour TC⁰ » (low-rank, low-bond-dim, low-degree) doit d'abord exhiber un test positif sur IP_n**, où toutes ces quantités sont exponentielles. *(Piste 4 a échoué sur ce test.)*
4. **Toute piste doit apporter une contribution technique concrète**, pas seulement une stratégie globale ou un cadre à explorer. Pointer vers Williams 2011 ne suffit pas — il faut un sous-théorème prouvable, un calcul vérifiable, ou un ingrédient algorithmique nouveau. *(Pistes 4 et 5 ont échoué sur ce test.)*
5. **Tout argument « encoder un problème NP sous forme X et invoquer une obstruction sur X »** doit d'abord vérifier que la propriété d'intérêt n'est pas trivialement définissable dans le langage des outils utilisés. Sanity-check préalable au cadre. *(Piste 5 a échoué dessus : SAT comme coloration → trivialement FO-définissable.)*
6. **Toute conjecture topologique sur les circuits monotones doit être empiriquement testée sur les 168 fonctions monotones de `n = 4` avant publication**, faute de quoi des contre-exemples triviaux la réfutent. *(Piste 6 : 52 contre-exemples sur 168.)*
7. **L'invariant topologique « β_i(Δ_f) > 0 » est constructif et large** — il tombe sous Razborov-Rudich (preuves naturelles) si on prétendait en tirer une vraie borne inférieure. Tout invariant calculable en temps polynomial sur la table de vérité et vrai pour ≥ 2^{-n} des fonctions doit être traité comme suspect.
8. **Tout invariant algébrique conjecturé borner `D_m(f)` doit passer le test OR_n** : la fonction OR_n a `pd(I_{OR_n}) = n − 1`, `reg = 1`, Scarf défaut 0, mais `D_m = 1`. Tout invariant qui ne distingue pas ce cas extrême du cas générique est inutilement large.
9. **Le cadre formule monotone n'est pas suffisant pour P vs NP** : même un théorème inattaquable sur D_m (profondeur de formule monotone) ne donne pas de borne pour les **circuits** ou les **machines de Turing**, qui sont les objets de P vs NP. La sous-classe est trop restreinte.
10. **Tout théorème asymptotique revendiqué doit être vérifié empiriquement à n=4 ou n=5 avant soumission.** Le Lemme 4 du Tour 8 prétendait à un théorème *inconditionnel pour tout n*, et il aurait été réfuté en 30 secondes par énumération à n=3 ou n=4. *(Pattern persistant sur 8 tours.)*
11. **Question ouverte mathématique positive** : *quelle est la caractérisation exacte des fonctions monotones à résolution pure ?* Pas juste threshold (qui en est une sous-classe stricte), pas juste linéaire + principal (idée fausse), pas seulement « threshold à permutation près » (réfuté Tour 8 bis), mais quelque chose de structurel. Question intéressante en soi, indépendamment de P vs NP. **Donnée empirique acquise** : 95 fonctions sur 167 non-constantes monotones n=4 (cf. atlas tour 8). La caractérisation devra englober au minimum : OR_n, AND_n, MAJ_n, autres TH_t, sous-OR (fonctions linéaires sur k < n variables), sous-AND, paires d'arêtes disjointes (shifts non-consécutifs), et autres.

12. **Toute extrapolation d'un théorème asymptotique à partir de ≤ 2 points est suspecte.** Le pattern « vraie à n=4, fausse à n=5 » a tué la C9 (Tour 9) et est réapparu avec L20.5 / L21.D (Tour 22, contre-exemple à n=5 trouvé après extrapolation depuis n=3, n=4). La condition (q) « audit bibliographique préemptif » n'est pas suffisante pour bloquer ce pattern. Nouvelle règle implicite à appliquer : **exiger systématiquement le test au point suivant `n+1`** *avant* de promouvoir une conjecture vérifiée empiriquement au statut « ÉTABLI structurellement ». Si le test n+1 est infaisable par énumération directe, alors le théorème doit rester ⚠️ Conjectural, pas ✅ Établi. Le Tour 20 a violé cette règle sur L20.5 (extrapolation n=3, n=4 → tout n) ; le Réfuteur n'a pas insisté assez. La condition de catalogage est désormais à appliquer rétroactivement à tout futur ÉTABLI.

13. **Toute mesure de complexité polynomiale entière doit explicitement distinguer max-magnitude (L∞ = `max_S |c_S|`) et weight (L1 = `Σ_S |c_S|`).** Ces deux mesures peuvent diverger d'un facteur `O(n^d)` (nombre de monômes de degré ≤ d). C'est *weight* qui apparaît dans Krause-Pudlák 1998 et dans la méthode algorithmique de Williams 2011 (via Beigel-Tarui). Une fonction TC⁰ à magnitude polynomiale mais L1-weight exponentielle ne donne **pas** de CAPP non-trivial. Pattern apparu Tour 23 : le Proposeur utilise `mag = max |c_S|` sous le nom de « magnitude » et compare aux bornes de Krause-Pudlák qui portent sur *weight* — l'instrument reste valide pour ce qu'il mesure, mais l'interprétation revendiquée du résultat est erronée. Pour future utilisation de l'instrument `tcomp`, exiger deux colonnes (magnitude L∞, weight L1).

14. **Toute piste relevant des circuits monotones / arithmétiques monotones / tropicaux / min-plus / max-plus doit passer le test Tardos 1988** : exhiber une fonction *dans P* à complexité super-polynomiale dans le cadre étudié. La fonction de Tardos (basée sur la θ-fonction de Lovász) a complexité monotone $\exp(\Omega(n^{1/6-o(1)}))$ ET est calculable en temps polynomial non-monotone. Donc toute borne inférieure dans le cadre monotone est silencieuse sur P vs NP. *Pattern apparu Tour 24 : tropical complexity revendiquée comme contournement des 3 barrières, sans mention de la barrière monotone.* Tout futur Tour invoquant ces cadres doit expliquer comment il franchit Tardos, sous peine de FAILLE FATALE automatique.

15. **Avant d'invoquer la construction CFI (Cai-Fürer-Immerman 1992) ou tout autre gadget combinatoire connu pour les graphes / CSP / hypergraphes, vérifier explicitement que l'invariant central (parité globale XOR sur twists, comptage, isomorphisme structural) transporte au domaine cible.** La CFI repose sur une *parité globale* attachée à une famille de twists locaux ; cette parité distingue G_T (parité 0) de G_F (parité 1). Sur SAT, qui n'a pas d'invariant de parité naturel, la construction CFI ne se transpose pas (vérifié Tour 25 : la « jumelée » `(x_i^0, x_i^1)` avec contrainte XOR est triviale et le « swap » revient à flipper x_i, qui ne préserve pas SAT). Atserias-Bulatov-Dawar 2007 ont étendu CFI aux CSP *affines sur Z₂* (où l'invariant existe) ; SAT n'étant pas affine sur Z₂, l'extension naïve échoue. *Pattern apparu Tour 25 : usage du nom « CFI » sans vérifier que le mécanisme transporte.*

16. **Avant d'invoquer FPC / fixed-point logic + counting comme niveau de complexité, distinguer FPC / CPT / P.** Anderson-Dawar 2017 caractérisent les circuits booléens symétriques comme exactement FPC ; FPC ⊊ P est *déjà prouvé* via CFI graphs. La vraie question « logique pour PTIME sur structures non-ordonnées » (Gurevich 1988) est résolue (négativement) pour FPC. Elle reste ouverte pour **CPT** (Choiceless Polynomial Time, Blass-Gurevich-Shelah 1999), strictement plus puissant. Toute proposition qui revendique « réduire P vs NP à Gurevich 1988 » via une borne inférieure FPC ne fait pas avancer P vs NP, puisque FPC ⊊ P n'implique pas P ≠ NP. *Pattern apparu Tour 25 : confusion FPC / CPT dans L25.5.*
5. **Existe-t-il une obstruction non-locale et non-algébrique** qui survive aux sauts polynomiaux *et* à l'équivalence logique ? GCT (permanent vs déterminant) est la seule réponse sérieuse aujourd'hui, mais elle est au point mort depuis 2017 (Bürgisser-Ikenmeyer-Panova : pas d'obstruction par occurrences).
6. Côté complexité descriptive : la conjecture de Gurevich (logique capturant P) offre-t-elle un angle non-relativisant **et** non-algébrisant exploitable ?
7. Williams 2011 (NEXP ⊄ ACC⁰) reste l'unique précédent ayant franchi les trois barrières. La voie « algorithmic method + circuit lower bound » se généralise-t-elle à TC⁰ ? *(Question ouverte centrale de la complexité depuis 15 ans — invoquer cette voie n'est pas une piste, c'est rejoindre le front de la recherche.)*

---

## 5. Sous-but du tour courant

> Un seul objectif concret et, si possible, vérifiable.

---

### ⚠️ RECENTRAGE DU 2026-07-25 (décision utilisateur) — ce qui suit prime sur tout l'historique de cette section

**Le sous-but courant, en une phrase : recâbler le livrable sur ce que le dépôt
a réellement produit, puis le rendre rejouable par un tiers.** Rien de neuf
n'est à mesurer d'abord : les acquis existent, ils ne sont pas dans `atlas/`.

**L'aune (à appliquer avant d'ouvrir une tâche).** Une tâche est ON-TARGET si
elle fait progresser l'une de ces trois choses : **(a)** remplir une cellule de
l'Atlas avec témoin — documenter *pourquoi* une famille d'approches échoue ;
**(b)** tester une approche candidate contre les barrières (relativisation,
preuves naturelles, algébrisation, monotone) ; **(c)** construire un instrument
vérifiable **réutilisable** pour (a) ou (b). Elle est **hors cible** si elle
produit des mathématiques autonomes dont l'énoncé ne mentionne plus de classe
de complexité, si elle optimise un modèle jouet au-delà de ce que l'Atlas
exige, ou si elle re-démontre du folklore.

**L'état chiffré qui motive ce recentrage** (mesuré le 2026-07-25) :

| Grandeur | Valeur |
|---|---|
| Tâches livrées dans `tasks/done/` | 169 |
| Tâches ayant modifié `atlas/` | **9** (ATLAS-001..006, A-009, A-011, A-012) |
| Tâches déclarées en échec (`tasks/failed/`) | **0** depuis 2026-06-09 |
| Scripts `checks/` | 188 — dont **zéro** cité par une cellule du corps de la matrice |
| Dernière modification de `atlas/` | 2026-07-23 — **4 commits de résultats postérieurs n'y sont pas entrés** |
| Dernière modification de `CLAUDE.md` avant ce jour | 2026-06-09 — **aucun des 4 recadrages utilisateur ultérieurs n'y figurait** |
| `prompts/proposeur.md`, `prompts/refuteur.md` | inchangés depuis 2026-05-23, alors qu'ils sont collés à Qwen à chaque tour |

Avec `failed/` vide et 169 tâches toutes ✅, **le seul compteur du dépôt ne
peut que monter** : la dérive était structurellement invisible de l'intérieur.
Ce n'est pas la rigueur locale qui a manqué — 36 auto-corrections consignées,
une revendication asymptotique fausse interceptée avant envoi à un auteur du
domaine — c'est un dispositif qui mesure la distance à la question. Les règles
7 à 10 de `CLAUDE.md` §8 le fournissent : les six règles anti-esquive
existantes régulaient toutes la *forme* d'une tâche, **aucune ne régulait sa
direction**.

**Ce qui est clos** (phrases de clôture : §2 et §2 ter) : (1) SYM∘AND versant
borne inférieure (F-012..022, T26-S*, T27-S*) ; (2) fil AS — clos *après*
écriture de la ligne 14 ; (3) fil V phase théorie des nombres — registre
satellite §2 ter ; (4) fil F-011 — clos *après* câblage de la ligne 4, et
**inachevé tant que ce câblage n'est pas fait** ; (5) boucle adverse —
suspendue.

**Directions interdites ajoutées au 2026-07-25** (cumulatives avec celles des
Tours 22-25) :
9. **Toute nouvelle valeur exacte de W(MAJ_k(g^k)) ou variantes**, à quelque k
   que ce soit — y compris minima inégaux ∀k, petits seuils, « décomposable ⇒
   global » pour k ≥ 6, cible asymptotique k(k+1). Motif : famille plafonnée
   polynomialement, refusée par le test de plafond (règle 7).
10. **Toute campagne de mesure ouverte sans avoir écrit à quelle échelle le
    phénomène visé commence** — voir [`atlas/echelle_instrument.md`](atlas/echelle_instrument.md).
11. **Toute revendication de nouveauté ou de primauté sans folklore-check écrit.**
12. **Toute tâche satellite** (OEIS, note T-F006, correspondance
    Mossinghoff/Chen) : elle ne consomme plus de créneau. Registre §2 ter.

**Ce qui compterait comme progrès, maintenant** : une cellule de la matrice
enrichie ou fermée **avec témoin rejouable**. Rien d'autre. La leçon la plus
dure des 169 tâches est chiffrée : ATLAS-006, une **tâche de lecture, zéro
calcul**, a produit en une session le verdict de portée que **43 tâches de
calcul** du fil AS n'avaient pas atteint.

---

> **⚠️ Historique ci-dessous — section gelée depuis 2026-06-09.** La boucle adverse par tours est
> suspendue (4 régimes d'échec documentés sur 25 tours). Le mode opératoire
> courant est le **workflow par tâches atomiques** : `tasks/backlog.md` +
> règles CLAUDE.md §8. La prescription Tour 24 ci-dessous a été **soldée le
> 2026-06-09 par la tâche F-001** (`tasks/done/F-001.md`) : OUI, il existe
> f ∈ TC⁰ d=2 \ d=1 à weight L1 polynomiale (EXACT_k, O(n²) structurel,
> ILP-optimal aux 3 points testés), mais IP_{2k} a une weight exponentielle
> au degré minimal (20, 119, 640 pour n=4,6,8) → la sous-classe poly-weight
> ne couvre pas TC⁰ d=2, pas d'analogue Beigel-Tarui direct pour TC⁰.
> Un Tour 26 ne peut être rouvert que via une cellule vide de l'Atlas
> (`atlas/matrice_barrieres.md`, à construire — Phase 2 du backlog).

- **Tour 26** : ~~prescription Tour 24 toujours maintenue et non-honorée après 2 tentatives~~ (Tours 24 + 25) — **soldée par F-001**.

  ### 📋 Notes sur Tours 23, 24, 25

  **Tour 23** a effectué le pivot AC⁰ d=2 → TC⁰. Premier tour à honorer toutes
  les conditions (a)-(r). Chiffres tous vérifiés. Mais (a) `tcomp` confond
  L∞/L1, (b) TC⁰ d=2 \ d=1 non exploré, (c) pont à Williams CAPP non construit.
  ⚠️ LACUNE RÉPARABLE avec acquis méthodologique.

  **Tour 24** (Qwen Max session parallèle) a *violé* la prescription Tour 24
  en pivotant vers « complexité tropicale de SAT » — cadre disqualifié par
  barrière monotone Tardos 1988 (4e barrière ajoutée §1) + audit (q) violé
  (Jukna 2014). ❌ FAILLE FATALE. Voir [`tours/tour_24_tropical_refutee.md`](tours/tour_24_tropical_refutee.md).

  **Tour 25** (Claude auto-proposition) a *violé* la prescription en pivotant
  vers « CFI-rigidification de 3-SAT ». Construction L25.1 + L25.2 réfutée
  empiriquement à 100 % (le swap = flip de variable, qui ne préserve pas
  SAT). L25.5 conflate FPC / CPT / symmetric P. ❌ FAILLE FATALE. Aveux
  honnêtes du Proposeur en §5 mais (j) violée (calcul promis n=3 non livré ;
  Réfuteur l'a fait, contre-exemple immédiat à n=1). Voir
  [`tours/tour_25_cfi_sat_refute.md`](tours/tour_25_cfi_sat_refute.md).

  **Conséquence** : la prescription Tour 24 (TC⁰ d=2 \ d=1 avec weight L1)
  **reste valide et non-honorée après 2 tentatives qui ont pivoté ailleurs**.
  Tour 26 doit soit la reprendre, soit justifier explicitement pourquoi pivoter
  (et choisir un cadre qui ne tombe sur aucune des 4 barrières actives).

  ### 🎯 Sous-but Tour 26 (= prescription Tour 24 reprise, 3e tentative)

  **Réparer Tour 23 sur ses lacunes (a) et (b)** :

  1. Étendre `tcomp` pour rapporter *deux* mesures simultanément :
     - magnitude L∞ = `max_S |c_S|`
     - weight L1 = `Σ_S |c_S|` (la mesure de Krause-Pudlák)
     Et tabuler les deux pour les fonctions du Tour 23.

  2. Tester des fonctions **TC⁰ profondeur 2 \ TC⁰ profondeur 1** :
     - `MAJ_n ∘ XOR_n` (parity-of-majorities, ou inverse).
     - `THR_t ∘ THR_s` avec des seuils variés.
     - Compositions à deux étages avec poids non-uniformes.
     - Quelques fonctions sparse choisies aléatoirement dans TC⁰ d=2.

  3. **Question cible** : existe-t-il une fonction `f ∈ TC⁰ d=2 \ TC⁰ d=1`
     avec **weight polynomial** (pas seulement magnitude polynomiale) ?
     - Si oui : candidate pour CAPP non-trivial par méthode Williams.
     - Si non : confirmation empirique que `weight_TC⁰_d=2 = exp(Ω(n))` (la
       barrière Krause-Pudlák) — ce qui éclaire empiriquement pourquoi
       Williams 2011 n'a pas pu être étendu à TC⁰ depuis 15 ans.

  4. **Si la question 3 reste ouverte à n=5** : honnêteté empirique impose
     de le dire et de ne pas extrapoler (cf. q.12 §4).

  ### 🚫 Directions interdites pour le Tour 26

  Maintenues du recadrage cumulatif Tours 22-25 :

  1. **Retour à AC⁰ d=2 / DNF-MIN** sous quelque forme que ce soit.
  2. **Formalisation Lean.**
  3. **Algèbre commutative sans pont à P vs NP.**
  4. **Re-démonstration empirique d'un résultat déjà cité dans §7.** Si le
     Proposeur réplique numériquement Bruck-Smolensky ou Anthony, c'est de la
     pédagogie, pas du progrès. Toute proposition doit cibler une *zone non
     couverte* par la bibliographie §7.

  Nouvelles post-Tour 24 :

  5. **Tout cadre monotone / arithmétique monotone / tropical / min-plus /
     max-plus** comme passerelle vers P vs NP. La barrière #4 (Razborov 1985 /
     Tardos 1988) est désormais ACTIVE. Voir §4 q.14 (test Tardos obligatoire
     si proposition dans ces cadres).
  6. **Pivot non-aligné sur la prescription du tour courant** sans justification
     mathématique explicite. Si le Proposeur change de cible (comme aux Tours
     24 et 25), il doit dire *pourquoi* la cible prescrite est inappropriée —
     pas l'ignorer silencieusement.

  Nouvelles post-Tour 25 :

  7. **Transposition naïve de gadgets connus (CFI, twist, structures
     d'isomorphisme) au domaine cible sans vérifier l'invariant central**.
     Voir §4 q.15. La CFI nécessite une parité globale ; SAT n'en a pas. Pour
     viser CPT depuis NP, encoder SAT dans une structure relationnelle
     non-triviale (la condition (g) du cahier l'exige déjà depuis Tour 5).
  8. **Borne inférieure FPC présentée comme « réduction à Gurevich 1988 »**.
     FPC ⊊ P est *déjà prouvé* via CFI ; Gurevich 1988 portait initialement
     sur la *définissabilité de PTIME* sur structures non-ordonnées (=
     question CPT, ouverte). Voir §4 q.16. Confusion à éviter explicitement.

  ### ✅ Directions autorisées (générales, en cas de pivot Tour 24+)

  Si le sous-but TC⁰ d=2 \ d=1 ci-dessus s'avère trop difficile ou stérile,
  le Proposeur peut choisir un autre saut **qualitatif** parmi :

  - **Profondeur ≥ 3** : FSS 1981 → Håstad 1986 (Switching Lemma) →
    Razborov-Smolensky 1987. Toute borne de profondeur ≥ 3, même partielle ou
    sur classe restreinte (ACC⁰, monotone, sparse), compte.
  - **Circuits non-formules** : sortir du cadre formule monotone (Tour 7 a
    établi son insuffisance). Cibles : circuits booléens généraux,
    branching programs, communication complexity.
  - **Méta-méthode Williams** : « algorithmic method + circuit lower bound »
    (Williams 2011 NEXP ⊄ ACC⁰). Toute contribution algorithmique nouvelle
    (CAPP non-trivial, derandomization, etc.) qui pourrait alimenter cette
    méthode.
  - **Méthode polynomiale modulaire** : Razborov-Smolensky 1987, GCT
    (Mulmuley-Sohoni permanent vs déterminant) — sous réserve de ne pas
    réintroduire des objets relativisants/algébrisants déjà éliminés.
  - **Complexité descriptive non-triviale** : Gurevich, Dawar, Grohe — sous
    réserve qu'on ne tombe pas dans le piège du Tour 5 (encodage trivialement
    FO-définissable de SAT).
  - **Fine-grained complexity** ou **hardness magnification** — sous réserve
    de fournir un sous-théorème nouveau, pas un slogan.

  ### Conditions (a)-(r) en vigueur

  Toutes les conditions (a)-(p) restent actives. **Condition (q)** ajoutée
  Tour 22 :

  > **(q) Audit bibliographique préemptif.** Avant de soumettre une idée, le
  > Proposeur doit explicitement vérifier (recherche web minimale, citation
  > d'au moins une référence) que sa cible n'est pas un résultat classique
  > déjà publié sous une formulation équivalente.

  **Nouvelle condition (r) ajoutée post-Tour 22** :

  > **(r) Test au point suivant pour toute conjecture asymptotique.** Si une
  > conjecture asymptotique est vérifiée empiriquement à `n ∈ {n_0, n_0+1}`,
  > elle ne peut être proposée comme ÉTABLI structurellement que (i) si une
  > preuve structurelle pour tout n est fournie, OU (ii) si elle est vérifiée
  > à `n_0 + 2` au minimum. Le pattern « vraie à n=4, fausse à n=5 » a tué C9
  > (Tour 9) puis L20.5 / L21.D (Tour 22) ; la condition (r) bloque sa
  > troisième apparition.

  ### Conjectures internes écartées

  - **Compléter / réparer L20.5 ou L21.D** : impossible (L20.5 est fausse,
    pas seulement non-prouvée). Et reste en AC⁰ d=2, donc doublement
    **interdit**.
  - **Caractérisation des fonctions à défaut maximal n(n−2) à n=5** : reste
    en AC⁰ d=2, donc **interdit** (même si question ouverte légitime,
    possiblement Σ₂^P-difficile).
  - **Conjecture asymptotique de L19** (`|(α)/(β)| / 2^{2^n} → 0`) : écartée.

  ### Note méta-épistémique

  Après 23 tours dont 8 ÉTABLIS identifiés folklore + 2 acquis modestes
  (L22.A + instrument `tcomp` Tour 23) + 1 dérive algèbre commutative + 5
  FAILLE FATALE + plusieurs LACUNE RÉPARABLE, le dépôt n'a **pas encore
  franchi les trois barrières** (relativisation, preuves naturelles,
  algébrisation). Le précédent unique reste Williams 2011. Si le Proposeur
  ne peut pas se positionner par rapport à ces trois barrières *de manière
  vérifiable*, il doit le dire et abandonner sa piste avant soumission.

  **Tours 22-25 confirment** que (i) rester en AC⁰ d=2 mène à des
  réfutations de conjectures folkloriques (Tour 22), (ii) pivoter
  superficiellement vers TC⁰ via une instrumentation empirique livre du
  folklore re-vérifié + un outil utile mais pas une borne nouvelle (Tour
  23), (iii) pivoter vers tropical/monotone tombe sur la barrière #4
  Razborov-Tardos (Tour 24), (iv) pivoter vers CFI/descriptive sans
  vérifier que les gadgets transportent au domaine cible donne une
  construction incohérente (Tour 25). Pour Tour 26 : viser explicitement
  une **zone non couverte par bibliographie §7**, et **livrer le calcul
  AVANT soumission** (cf. (j)) — le Réfuteur a livré 5 minutes de calcul
  qui ont coulé le Tour 25, et 20 minutes qui ont coulé le Tour 24.

---

## 6. Prochaine action

> **Mode tâches atomiques en vigueur** (CLAUDE.md §8, `tasks/backlog.md`).
> L'ancienne boucle « Proposeur génère une idée » est suspendue.

> **⚠️ RECENTRAGE DU 2026-07-25.** Boucle adverse **suspendue** (§5). Ordre
> imposé : la gouvernance d'abord, sinon la première tâche re-dérive.
> **Aucune des tâches ci-dessous ne demande de solveur.**
>
> - [x] **GOUV-001 (fait ce jour)** — règles posées dans `CLAUDE.md` : arborescence
>   réelle (§4), test des barrières non désactivable seul (§5.4), règles 7 à 10
>   (rattachement + relecture à la clôture, test de distance non-grep, bilan de
>   fil par cible, recadrages écrits dans CLAUDE.md), règle 2 durcie (un commit =
>   une tâche, profondeur d'auto-génération ≤ 3), réouverture d'un Tour à 5
>   conditions dont la recopie verbatim de la cellule.
> - [x] **ATLAS-008 (fait ce jour)** — [`atlas/echelle_instrument.md`](atlas/echelle_instrument.md) :
>   la note de dispositif, deux témoins chiffrés (n ≤ 8 contre n ≈ 4050 ;
>   O(n²) contre 2^{polylog n}), et le test opératoire du contrôle positif.
> - [ ] **ATLAS-007** — porter dans le livrable les 4 commits postérieurs au
>   2026-07-23 et les 43 tâches du fil AS : lignes 7 et 14, chiffres d'en-tête.
> - [ ] **ATLAS-010** — `atlas/temoins.md` : cellule → script → commande →
>   sortie attendue → **durée** (le dépôt a un résultat à 3 h 20 et un à
>   15 884 s : c'est une information de reproductibilité).
> - [ ] **ATLAS-011** — écrire la ligne 4 avec le contenu mesuré de F-011, puis
>   clore le fil. **Sans cette tâche, F-011 est inachevé, pas clos.**
> - [ ] **PUB-001** — réécrire `README.md` : il annonce 12 familles (15),
>   9 audits (22), ~30 scripts (188), 25 tours (27).
> - [ ] **VEILLE-2026-2** — veille sur le modèle de `bib/veille_probabilistes_2026.md`,
>   le format le plus rentable du dépôt (il a produit le fil V → ligne 14, et
>   A-009 → ligne 13). **À exécuter AVANT toute tâche d'audit A-013+**, dont les
>   références n'existent nulle part dans le dépôt.

- [x] Phases 1-2 + SYNTH-001 + fils F-001..F-010, B-001..B-006 — complets (2026-06-09/10)
- [x] **Fil F-011** (33 étapes) — palier propre atteint : 3 familles infinies (K/K′/K″), classification bipartite complète, plate n ≤ 25 + 29, 31, 32, audits BBR + BGL — synthèse `notes/front_composite.md` §1-10bis (2026-06-11)
- [x] **Fil V** (15 tâches) — Conjecture 5 close d ≤ 5 et d = 7, d = 6 quasi clos ; puis réfutation de la Conjecture 5 (validée Krishan) et fil N.T. clos — synthèses `notes/kv_note.md`, `tasks/done/V-054.md` (2026-06)
- [x] **Fil AS** (43 tâches) — Conjecture 13 : dossier complet, C13 réduite au scalaire c(n,d), synthèse ENVOYÉE à Krishan (2026-07-20)
- [x] **Atlas 15 lignes toutes documentées sur textes** (A-011 GCT, A-012 complexité des preuves, 2026-07-20/23)
- [x] **Fil F-012..022** — le barreau 1 (SYM∘AND) : dossier complet, 4 théorèmes, zoo des mécanismes démontré (2026-07-23)
- [ ] **Attentes externes** : réponse de Krishan (synthèse C13, envoyée ~2026-07-20 — le brouillon du dépôt contient déjà la matière d'un complément : point 0, courbe c) ; Göös (mail 2026-06-09, sans réponse consignée — le silence ne vaut rien)
- [ ] **Main de Tanguy** : soumission note T-F006 (relecture experte → LaTeX → arXiv, `notes/dnf_min_ip_arxiv_en.md` prête) ; envois OEIS (m=20 ferme)
- [ ] **Fronts candidats** (au choix de l'utilisateur) : ATLAS-006 (zone 6 — localiser où le gain asymétrique Δ_w de KV devient visible, la tâche que la matrice a elle-même définie) ; note de synthèse du fil SYM∘AND + antériorité des théorèmes (fenêtre ANF, alternance — candidats note externe) ; veille 2025-26 des lignes vivantes (ITCS 2026 : AC⁰[p]-Frege, range avoidance ; Panova 2025) ; cellule bounded arithmetic ligne 15 (PV1 ⊬ EF à la source) ; B-007 réplication DIP (ligne 8) ; fenêtres GT ([25,32], [21,38], runs nocturnes)
- [ ] **Lecture humaine recommandée avant diffusion** : thèse Gopalan 2006 (PDF dans `bib/pdf/` + sources ECCC) — cf. table de requalification `bib/bgl_2003_sun_2020.md`
- [x] **TOUR 26 OUVERT** (2026-07-23, décision utilisateur — 1re réouverture de la boucle adverse depuis le Tour 25, conditions §8 satisfaites) : cible née de la ligne 7 via le fil F-012..022 — **borne inf super-additive W(MAJ_k(g^k)) ≥ ω(k) pour bloc monotone non-AND, ou sa réfutation constructive**. Dossier de cible autonome pour le Proposeur : [`tours/tour_26_cible.md`](tours/tour_26_cible.md). En attente : proposition de Qwen (collée par l'utilisateur) → réfutation.
- [x] **Tours 26-27 + sous-lemmes** (2026-07-23/24) : Tour 26 **SURVIT** (1er en 26 tours — indicateur modulaire, O(k²) universel, fenêtre MAJ₅ ∈ [20, 30]) ; T26-S1 (W_dec = k(k+1) exhaustif k ≤ 9 — le point k = 9 clos par run de fond 15 884 s : 85..89 vides, 90 réalisable), T26-S2 (théorème isotypique ∀k), T26-S3 (théorème minima ≡ 1 ∀k) ; Tour 27 échec honnête + acquis (L27.1 : classe symétrique = k(k+1) pour k ≤ 8 ; classe A ≥ 30 exécutée par le Réfuteur) ; **T27-S1 : classe B ≥ 30** (CP-SAT canal de valeurs + lex-leader, échelle complète UNSAT, étalon Tour 26 reproduit). **T27-S2 (le couronnement, 2026-07-24) : W(MAJ₅(OR2⁵)) = 30 = k(k+1) PROUVÉ SUR L'ESPACE ENTIER** — échelle de caps 19..29 toute UNSAT (11 barreaux, 58 s → 3517 s), borne sup décomposable énumérée ; « décomposable ⇒ global » fermé à k = 5, C26 certifiée k = 3, 4, 5 ; le CP-SAT d'avant plafonnait à lb 7, le canal de valeurs + lex-leader porte la frontière à 30. **T26-S4 (le même jour, front asymptotique) : LA DICHOTOMIE DENSE/DÉGÉNÉRÉ EST NOMMÉE** — la séparation se relaxe en une famille purement arithmétique (Lemme R : Σ_C M ∉ D_C), et le mécanisme dense est une **condition de somme nulle modulo le minimum** (constante de Davenport de ℤ/m, racine d'Erdős–Ginzburg–Ziv 1961 — outil classique). **Théorème S4 ∀k** : minima égaux quelconques (β_i libre), seuil ≥ majorité ⟹ W ≥ k(k+1) − r(k−2m), exact si m = 1 / m | k / m ≥ k/2, **toujours Ω(k²)** — 3ᵉ classe ∀k, strictement plus large que S3. Mesuré : la famille singleton de S3 casse dès k = 5, la famille multi-sommets a pour minimum global exactement k(k+1) (k = 3..8), et la relaxation suffit exactement au-dessus du seuil de majorité. **T27-S3 (le même jour) : LES DEUX DERNIÈRES FENÊTRES DU TOUR 26 SONT FERMÉES** — W(THR₃(OR2⁴)) = 20 et W(MAJ₃(MAJ3³)) = 12 (moteur générique étalonné sur la vérité terrain MAJ₃(OR2³) = 12). **Observation forte sur 5 instances : W = k(k+1) ne dépend ni du bloc g ni du seuil t, seulement du nombre de blocs k** (blocs AND exceptés, F-022) ; **corollaire : l'indicateur modulaire du Tour 26 est OPTIMAL sur tout ce qui est décidé** — le mod-3 de MAJ₃(MAJ3³) bat d'un facteur 2 le couvert unilatéral 27 de F-021, dont l'optimalité était ouverte. Antériorité : littérature SYM∘AND entièrement asymptotique, aucune valeur exacte recensée. Fronts suivants : minima INÉGAUX ∀k (désormais un énoncé de combinatoire additive posable à un spécialiste) ; petits seuils t < ⌈k/2⌉ (familles sommets+minima insuffisantes, il faut la valeur intermédiaire β_i).

---

## 7. Bibliographie sur P vs NP

> **But de cette section.** Centraliser les références qui *encadrent* l'exploration :
> les trois barrières, la lignée des bornes inférieures de circuit, les surveys, et
> les classiques de complexité booléenne sur lesquels les Tours 12-22 reposent.
> Toute idée future du Proposeur doit être positionnable par rapport à cette
> bibliographie (cf. condition (q) §5 — audit bibliographique préemptif).

### 7.1 Les trois barrières (à franchir simultanément pour séparer P de NP)

- **Relativisation** — T. Baker, J. Gill, R. Solovay, *« Relativizations of the
  P =? NP question »*, SIAM Journal on Computing, vol. 4, no. 4, 1975, pp.
  431-442. [doi:10.1137/0204037](https://doi.org/10.1137/0204037).
  Construit deux oracles `A`, `B` tels que `P^A = NP^A` et `P^B ≠ NP^B`. Toute
  preuve qui relativise (i.e. qui traite la machine comme une boîte noire) ne
  peut donc trancher P vs NP. Pertinent pour Tours 1, 2 du dépôt.

- **Preuves naturelles** — A. Razborov, S. Rudich, *« Natural proofs »*, Journal
  of Computer and System Sciences, vol. 55, no. 1, 1997, pp. 24-35 (version
  conférence STOC 1994). Prix Gödel 2007.
  [doi:10.1006/jcss.1997.1494](https://doi.org/10.1006/jcss.1997.1494).
  Sous l'hypothèse que les fonctions pseudo-aléatoires « one-way »
  existent, aucune *preuve naturelle* (i.e. constructive et large)
  ne peut donner de borne super-polynomiale sur la complexité de circuit.
  Pertinent pour Tours 6, 19 du dépôt (signaux d'alarme RR explicitement notés).

- **Algébrisation** — S. Aaronson, A. Wigderson, *« Algebrization: A new barrier
  in complexity theory »*, ACM Transactions on Computation Theory, vol. 1, no.
  1, 2009 (version conférence STOC 2008, pp. 731-740).
  [doi:10.1145/1490270.1490272](https://doi.org/10.1145/1490270.1490272).
  [PDF auteur](https://www.scottaaronson.com/papers/alg.pdf).
  Étend la relativisation aux extensions polynomiales basse-degré sur corps
  finis. Toute technique fondée sur l'arithmétisation à la Shamir/IP=PSPACE
  algébrise et ne peut donc séparer P de NP. Pertinent pour Tours 2, 4 du dépôt.

### 7.2 Lignée AC⁰ → ACC⁰ → NEXP (Williams 2011)

- **PARITY ∉ AC⁰** — M. Furst, J. B. Saxe, M. Sipser, *« Parity, circuits, and
  the polynomial-time hierarchy »*, Mathematical Systems Theory, vol. 17, 1984,
  pp. 13-27 (FOCS 1981).
  [doi:10.1007/BF01744431](https://doi.org/10.1007/BF01744431).
  Première borne super-polynomiale sur AC⁰. Résultat indépendamment prouvé par
  M. Ajtai, *« Σ₁¹-formulae on finite structures »*, Annals of Pure and Applied
  Logic, vol. 24, 1983, pp. 1-48. Pertinent pour Tour 12 (cas profondeur 2 de
  la borne FSS).

- **Switching Lemma de Håstad** — J. Håstad, *« Almost optimal lower bounds for
  small depth circuits »*, dans *Randomness and Computation*, Advances in
  Computing Research, vol. 5, JAI Press, 1989, pp. 143-170 (thèse MIT 1986).
  Améliore FSS à `2^Ω(n^(1/(d−1)))` pour profondeur `d`. Outil canonique des
  bornes inférieures AC⁰. Pertinent pour toute extension Tour 23 vers
  profondeur ≥ 3.

- **MOD_p ∉ AC⁰[MOD_q] (p ≠ q premiers)** — A. A. Razborov,
  *« Lower bounds on the size of bounded depth circuits over a complete basis
  with logical addition »* (en russe), Matematicheskie Zametki, vol. 41, no. 4,
  1987, pp. 598-607. R. Smolensky, *« Algebraic methods in the theory of lower
  bounds for Boolean circuit complexity »*, STOC 1987, pp. 77-82.
  [doi:10.1145/28395.28404](https://doi.org/10.1145/28395.28404).
  Méthode polynomiale modulaire : représenter AC⁰[MOD_p] par polynômes de bas
  degré sur F_p. Atteint la barrière entre AC⁰[p] et ACC⁰. Pertinent pour Tour
  16 et toute extension vers ACC⁰.

- **NEXP ⊄ ACC⁰** — R. Williams, *« Nonuniform ACC circuit lower bounds »*,
  Journal of the ACM, vol. 61, no. 1, 2014, art. 2 (CCC 2011).
  [doi:10.1145/2559903](https://doi.org/10.1145/2559903).
  [PDF auteur](https://people.csail.mit.edu/rrw/acc-lbs-ccc.pdf).
  *Seul résultat à ce jour ayant franchi les trois barrières.* Méthode
  « algorithmic method + circuit lower bound » : un algorithme CAPP
  non-trivial pour ACC⁰ implique NEXP ⊄ ACC⁰. **Pertinent pour Tours 4, 23 du
  dépôt** (toute piste prétendant à une borne non-relativisante et
  non-algébrisante doit se positionner par rapport à cette méthode).

### 7.3 Bornes inférieures monotones et Karchmer-Wigderson

- **CLIQUE_k requiert circuit monotone super-polynomial** — A. A. Razborov,
  *« Lower bounds on the monotone complexity of some Boolean functions »*,
  Doklady Akademii Nauk SSSR, vol. 281, no. 4, 1985, pp. 798-801.
  Méthode d'approximation par tournesols (Erdős-Rado). Premier exemple d'une
  borne super-polynomiale sur une fonction NP-complète, *mais en cadre
  monotone uniquement*.

- **Amélioration exponentielle** — N. Alon, R. B. Boppana, *« The monotone
  circuit complexity of Boolean functions »*, Combinatorica, vol. 7, no. 1,
  1987, pp. 1-22. [doi:10.1007/BF02579196](https://doi.org/10.1007/BF02579196).
  Renforce Razborov 1985 à `exp(Ω((n / log n)^{1/3}))` pour CLIQUE de taille
  `(1/4)(n / log n)^{2/3}`.

- **Equivalence profondeur ⟷ complexité de communication** — M. Karchmer, A.
  Wigderson, *« Monotone circuits for connectivity require super-logarithmic
  depth »*, SIAM J. Discrete Mathematics, vol. 3, no. 2, 1990, pp. 255-265.
  [doi:10.1137/0403021](https://doi.org/10.1137/0403021).
  Le jeu KW : Alice reçoit `x ∈ f^{-1}(1)`, Bob `y ∈ f^{-1}(0)`, ils
  cherchent un `i` tel que `x_i ≠ y_i`. La complexité de communication
  optimale = profondeur de formule en base de De Morgan. Outil-pivot pour
  bornes inférieures de profondeur. Pertinent pour Tour 11 du dépôt (piste
  rejetée car cible 2COL ∈ P, pas NP-complet).

- **Théorèmes de lifting (query → communication)** — M. Göös, T. Pitassi, T.
  Watson, *« Deterministic communication vs. partition number »*, SIAM J.
  Computing, vol. 47, no. 6, 2018, pp. 2435-2450.
  [doi:10.1137/16M1059369](https://doi.org/10.1137/16M1059369).
  Avec une composition « gadget » (souvent index `IND` ou inner product),
  toute borne sur la complexité d'arbre de décision se *lift* en borne sur
  la complexité de communication. Combiné à Karchmer-Wigderson, donne des
  bornes de profondeur. Pertinent pour Tour 11 du dépôt.

### 7.4 GCT (Geometric Complexity Theory)

- **Programme initial** — K. D. Mulmuley, M. Sohoni, *« Geometric complexity
  theory I: An approach to the P vs. NP and related problems »*, SIAM J.
  Computing, vol. 31, no. 2, 2001, pp. 496-526.
  [doi:10.1137/S009753970038715X](https://doi.org/10.1137/S009753970038715X).
  Approche algébro-géométrique : étudier l'orbit closure du permanent et du
  déterminant sous l'action de GL_N. Cible VP vs VNP (version algébrique de P
  vs NP) plutôt que P vs NP directement.

- **Obstacle aux obstructions par occurrences** — P. Bürgisser, C. Ikenmeyer, G.
  Panova, *« No occurrence obstructions in geometric complexity theory »*,
  Journal of the AMS, vol. 32, no. 1, 2019, pp. 163-193 (FOCS 2016).
  [doi:10.1090/jams/908](https://doi.org/10.1090/jams/908).
  Réfute le plan original de Mulmuley-Sohoni : aucune *occurrence obstruction*
  (multiplicité = 0 dans le coordinate ring du permanent vs ≥ 1 dans celui du
  déterminant) ne peut séparer ces variétés. GCT au point mort depuis. Cité en
  §4 q.5 du cahier.

### 7.5 DNF-MIN, implicants premiers, complexité Σ₂^P

- **Origine du concept d'implicant premier** — W. V. Quine, *« The problem of
  simplifying truth functions »*, American Mathematical Monthly, vol. 59, 1952,
  pp. 521-531. Algorithme dual : E. J. McCluskey, *« Minimization of Boolean
  functions »*, Bell System Technical Journal, vol. 35, 1956, pp. 1417-1444.
  Cadre canonique du Tour 19 (essentialité) et de l'audit bibliographique de
  mai 2026.

- **Σ₂^P-complétude de DNF-MIN** — C. Umans, *« The minimum equivalent DNF
  problem and shortest implicants »*, Journal of Computer and System Sciences,
  vol. 63, no. 4, 2001, pp. 597-611 (FOCS 1999).
  [doi:10.1006/jcss.2001.1775](https://doi.org/10.1006/jcss.2001.1775).
  Résout la conjecture de Stockmeyer 1976. Lien fondamental entre DNF-MIN et
  la hiérarchie polynomiale, cité au Tour 20 du dépôt.

- **Synthèse moderne** — Y. Crama, P. L. Hammer (eds.), *Boolean Functions:
  Theory, Algorithms, and Applications*, Encyclopedia of Mathematics and its
  Applications, vol. 142, Cambridge University Press, 2011.
  Chapitre 3, *« Prime implicants and minimal DNFs »* (par P. L. Hammer et A.
  Kogan), couvre la majeure partie du folklore re-démontré aux Tours 12-20
  (cf. audit bibliographique §3).

- **Gap essentialité / taille CNF** — L. Hellerstein, D. Kletenik, *« On the
  gap between ess(f) and cnf_size(f) »*, Discrete Applied Mathematics, vol.
  187, 2015, pp. 92-101 (arXiv 2011, [arXiv:1106.4247](https://arxiv.org/abs/1106.4247)).
  Référence directe pour le théorème de caractérisation Tour 19.

### 7.5bis Polynomial threshold functions (PTF) et complexité polynomiale entière

- **PTF degree d'IP via norme spectrale** — J. Bruck, R. Smolensky,
  *« Polynomial threshold functions, AC⁰ functions, and spectral norms »*,
  SIAM J. Computing, vol. 21, no. 1, 1992, pp. 33-42.
  [doi:10.1137/0221003](https://doi.org/10.1137/0221003).
  Caractérisation : une fonction `f` est PTF de magnitude polynomiale **ssi**
  sa norme spectrale `L1(f̂)` est polynomiale. Pour IP_n, `L1(f̂) = 2^n`
  (Hadamard parfait), donc la magnitude PTF est exponentielle. **Référence
  centrale pour Tour 23** : la conjecture T23.1 du Proposeur (`tcomp(IP_{2k})
  = (k, 2^{k-1})`) est une vérification empirique de cette borne sur 3 points.

- **PTF degree typique** — R. O'Donnell, R. A. Servedio, *« New degree bounds
  for polynomial threshold functions »*, Combinatorica, vol. 30, no. 3, 2010,
  pp. 327-358 (STOC 2003).
  [PDF auteur](http://www.cs.columbia.edu/~rocco/Public/stoc03-ptfdb.pdf).
  Borne supérieure `n/2 + O(√n log n)` sur le PTF degree de toute fonction
  booléenne, complétant la conjecture d'Anthony (PTF degree ≈ ⌈n/2⌉ pour la
  plupart des fonctions). Mon observation Tour 23 `deg(IP_{2k}) = k = n/2`
  est conforme à cette borne (et représente le cas extrême « degré minimum
  possible » selon Anthony-Alon).

- **Weight vs magnitude PTF** — K. A. Hansen, V. V. Podolskii, *« Polynomial
  threshold functions and Boolean threshold circuits »*, Information and
  Computation, vol. 240, 2015, pp. 56-73 (ECCC TR13-021).
  [PDF ECCC](https://eccc.weizmann.ac.il/report/2013/021/download/).
  Survey unifiant degré, weight (L1 = `Σ |c_S|`), magnitude (L∞ = `max |c_S|`).
  Référence pour la **distinction technique** soulignée Tour 23 §4 q.13 :
  c'est *weight* (L1), pas *magnitude* (L∞), qui apparaît dans Krause-Pudlák
  et dans la méthode algorithmique Beigel-Tarui → Williams.

- **Weight bounds tight pour IP** — A. A. Sherstov, *« Algebraic methods in
  the theory of lower bounds for Boolean circuit complexity »*, monographie /
  habilitation, 2009-2011 ; et **A. A. Razborov**, *« On small depth threshold
  circuits »*, Helsinki notes 1992.
  [PDF Razborov](https://people.cs.uchicago.edu/~razborov/files/helsinki.pdf).
  IP a `sign-rank = 2^{n/2}` (Forster 2002) ; tight `weight ≥ 2^n` pour toute
  PTF entière représentant IP_n. **Aucune représentation polynomiale dense
  pour IP n'évite la croissance exponentielle simultanément en degré et
  weight L1**, donc IP n'est pas une candidate à CAPP non-trivial via PTF.

### 7.5ter Complexité descriptive — CFI, FPC, CPT, circuits symétriques

- **Origine CFI** — J.-Y. Cai, M. Fürer, N. Immerman, *« An optimal lower
  bound on the number of variables for graph identification »*,
  Combinatorica 12(4), 1992, pp. 389-410.
  [doi:10.1007/BF01305232](https://doi.org/10.1007/BF01305232).
  Construction des graphes G_T (parité 0) et G_F (parité 1), indistinguables
  par `k`-Weisfeiler-Leman pour tout `k` fixé mais distinguables en temps
  polynomial. Repose sur une *parité globale* attachée à des gadgets locaux
  de twist sur les arêtes. Référence centrale pour Tour 5 et Tour 25 du
  dépôt.

- **Extension CFI aux CSP affines sur Z_2** — A. Atserias, A. Bulatov, A.
  Dawar, *« Affine systems of equations and counting infinitary logic »*,
  Theoretical Computer Science 410(18), 2009, pp. 1666-1683 (ICALP 2007).
  [PDF Dawar](https://www.cl.cam.ac.uk/~ad260/papers/abd-icalp07.pdf).
  Réinterprète CFI comme un encodage de systèmes d'équations linéaires sur
  Z_2 où chaque variable apparaît dans précisément deux équations. Établit
  que pour les CSP « affines », FPC échoue. **Note critique pour Tour 25** :
  SAT n'est pas naturellement affine sur Z_2, donc la transposition naïve
  de CFI échoue. La condition q.15 du cahier (test transport de
  l'invariant) cristallise cette leçon.

- **Choiceless Polynomial Time (CPT)** — A. Blass, Y. Gurevich, S. Shelah,
  *« Choiceless polynomial time »*, Annals of Pure and Applied Logic 100,
  1999, pp. 141-187. Et *« On polynomial time computation over unordered
  structures »*, J. Symbolic Logic 67(3), 2002, pp. 1093-1125.
  [PDF Shelah 533](https://shelah.logic.at/files/180379/533.pdf).
  Formalisation de la question de Gurevich 1988 (« logique pour PTIME sur
  structures non-ordonnées ») via un modèle de calcul *choiceless* :
  machines qui n'effectuent jamais de choix arbitraire mais peuvent
  exécuter en parallèle sur tous les choix. CPT capture beaucoup plus que
  FPC (par exemple les graphes CFI). **CPT = P sur structures
  non-ordonnées ?** Ouvert depuis 1999.

- **CPT et CFI** — A. Dawar, D. Richerby, B. Rossman, *« Choiceless polynomial
  time, counting and the Cai-Fürer-Immerman graphs »*, Annals of Pure and
  Applied Logic 152(1-3), 2008, pp. 31-50.
  [PDF Rossman](https://users.cs.duke.edu/~br148/CPT-CFI.pdf).
  CPT (avec compteurs) décide l'isomorphisme CFI, contrairement à FPC.
  Précise donc que la stratification *FPC ⊊ CPT ⊆ P* est stricte au moins
  sur la première inclusion.

- **Symmetric circuits = FPC** — M. Anderson, A. Dawar, *« On symmetric
  circuits and fixed-point logics »*, Theory of Computing Systems 60(3),
  2017, pp. 521-551 (STACS 2014).
  [arXiv:1401.1125](https://arxiv.org/abs/1401.1125).
  *« Les requêtes définissables par familles uniformes de circuits booléens
  symétriques (avec portes majority) sont exactement celles définissables
  en FPC. »* Implication pour Tour 25 : toute borne inférieure sur les
  circuits symétriques pour SAT ne sépare que FPC ⊊ P (déjà connu via CFI),
  pas P vs NP. La vraie cible serait une borne sur les circuits **CPT** —
  question ouverte.

### 7.6 Hardness magnification et méta-complexité (front actif 2018-)

- **Hardness magnification** — I. C. Oliveira, J. Pich, R. Santhanam,
  *« Hardness magnification near state-of-the-art lower bounds »*, CCC 2019.
  [doi:10.4230/LIPIcs.CCC.2019.27](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CCC.2019.27).
  Stratégie : montrer qu'une borne *faible* sur un problème *spécifique*
  (MCSP, MKtP) suffit à magnifier en NEXP ⊄ P/poly. Cité en §5 du cahier
  comme direction autorisée Tour 23.

- **Barrière interne à la magnification** — L. Chen, S. Hirahara, I. C.
  Oliveira, J. Pich, N. Rajgopal, R. Santhanam, *« Beyond natural proofs:
  Hardness magnification and locality »*, ITCS 2020.
  [doi:10.4230/LIPIcs.ITCS.2020.70](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITCS.2020.70).
  Les théorèmes de magnification eux-mêmes butent sur une variante de RR :
  une approche qui prouve une borne magnifiable doit éviter d'être *locale*.
  Cité au Tour 4 du dépôt comme barrière supplémentaire.

### 7.6bis Modèles polynomiaux composites, toriques et PTE (fils F-011 et V, 2026-06)

- **Représentations faibles mod m** — D. A. M. Barrington, R. Beigel,
  S. Rudich, *« Representing Boolean functions as polynomials modulo
  composite numbers »*, Comput. Complexity 4 (1994). **Lu en texte
  intégral** ([`bib/bbr_1994.md`](bib/bbr_1994.md)) : Thm 2.1 (OR mod m en
  O(N^{1/r})), Thm 2.2 (borne inf symétrique par périodicité — notre
  Théorème D requalifié réplication), base des symétriques par période.
- **Polynômes toriques** — A. Bhrushundi, K. Hosseini, S. Lovett,
  S. Rao, *« Torus polynomials: an algebraic approach to ACC lower
  bounds »*, ITCS 2019, [arXiv:1804.08176](https://arxiv.org/abs/1804.08176).
  MAJ ∉ ACC réduit aux bornes toriques ; cas symétrique prouvé, général
  ouvert (Conjecture 5 de leur papier = notre cible du fil V via KV).
- **Réduction réseau/LP** — V. Krishan, S. Vishwanathan, *« Towards ACC
  Lower Bounds using Torus Polynomials »*,
  [ECCC TR24-074 (2024)](https://eccc.weizmann.ac.il/report/2024/074/).
  **Lu en texte intégral** ([`bib/krishan_2024.md`](bib/krishan_2024.md)) :
  méthode des polynômes duaux étendue au tore, famille de LP par parties
  entières, Conjecture 5 (plus court vecteur à γ_n = 1) — **reformulée et
  prouvée en régime stable d ≤ 9, d = 11 par le fil V**
  ([`notes/kv_note.md`](notes/kv_note.md)).
- **Prouhet-Tarry-Escott / produits purs** — Erdős-Szekeres 1959 (voir
  [arXiv:1509.08411](https://arxiv.org/abs/1509.08411) pour l'historique) ;
  R. Maltby, *« Pure product polynomials and the Prouhet-Tarry-Escott
  problem »*, Math. Comp. 66 (1997). Le problème PTE-ℓ₂ = la forme
  polynomiale exacte du réseau de KV (Théorème P du fil V) ; les
  solutions PTE **idéales** (ouvertes depuis 1851 pour les grandes
  tailles, connues ≤ 10 et 12) sont les minimiseurs au seuil.
- **Polynômes symétriques sur Z_m / protocoles** — N. Bhatnagar,
  P. Gopalan, R. J. Lipton, *« Symmetric polynomials over Z_m and
  simultaneous communication protocols »*, FOCS 2003 / JCSS 2006,
  [ECCC TR03-047](https://eccc.weizmann.ac.il/report/2003/047/). **Lu en
  texte complet par lecture visuelle** (polices bitmap,
  [`bib/bgl_2003_sun_2020.md`](bib/bgl_2003_sun_2020.md)) : équivalence
  degré symétrique mod pq ⟺ protocoles simultanés sur digits (= notre
  cadre CRT/Lucas) ; **Thm 4.9 : Ω(max(k, √n))** faible symétrique pour
  T_k — la borne linéaire de MAJ mod 6 est à eux. Et N. Bhatnagar,
  P. Gopalan, *« The Degree of Threshold mod 6 and Diophantine
  Equations »*, [ECCC TR04-022](https://eccc.weizmann.ac.il/report/2004/022/)
  (seuils à k constant, Filaseta/abc). Nos lois exactes + modèle
  général/bloc-symétrique = couche candidate (table de requalification).
- **Degré modulaire fort** — X. Sun, Y. Sun, J. Wang, K. Wu, Z. Xia,
  Y. Zheng, *« On the Degree of Boolean Functions as Polynomials over
  Z_m »*, [ICALP 2020](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2020.100) :
  deg_m(f sym) ≥ n/(2 + 1/(p−1) + 1/(q−1)) (= 2n/7 pour m = 6) — le
  modèle fort est actif ; notre Théorème L à citer comme instance.
- **Tables PTE** — Chen Shuwen, *« The Prouhet-Tarry-Escott Problem »*,
  [eslpower.org/TarryPrb.htm](http://eslpower.org/TarryPrb.htm) :
  premières/plus petites idéales connues par taille — Escott 1910
  (taille 7, support [0, 102], vérifiée exacte par V-014c) ; Tarry 1913
  (taille 8, support [0, 50], **redécouverte ET certifiée minimale par
  notre réseau, V-015**).
- **Méta-complexité moderne** — S. Hirahara (FOCS 2018, réduction
  non-boîte-noire) ; Y. Huang, R. Ilango, H. Ren,
  *« NP-Hardness of Approximating Meta-Complexity »*, STOC 2023. **Lu en
  intégral** ([`bib/meta_complexite.md`](bib/meta_complexite.md)) —
  ligne 13 de l'Atlas.
- **Veille probabiliste 2026** —
  [`bib/veille_probabilistes_2026.md`](bib/veille_probabilistes_2026.md)
  (toriques ★, méta-complexité, dérandomisation/« free lunch » CCC 2025,
  OGP : hors-cible documenté).

### 7.7 Manuels et surveys (à consulter en priorité)

- **Manuel de référence** — S. Arora, B. Barak, *Computational Complexity: A
  Modern Approach*, Cambridge University Press, 2009.
  [Site officiel + PDF draft](https://theory.cs.princeton.edu/complexity/).
  Couvre tout le matériau de cadrage : barrières, AC⁰, communication, PCP,
  GCT. Référence-mère pour positionner toute idée nouvelle.

- **Bornes inférieures booléennes en détail** — S. Jukna, *Boolean Function
  Complexity: Advances and Frontiers*, Algorithms and Combinatorics, vol. 27,
  Springer, 2012.
  [Page auteur + draft](https://web.vu.lt/mif/s.jukna/boolean/index.html).
  Compendium détaillé des techniques de bornes inférieures, des années 1940 à
  ~2010. Inclut Razborov-Smolensky, Håstad, monotone, méthode probabiliste.

- **Survey P vs NP de Aaronson** — S. Aaronson, *« P =? NP »*, dans *Open
  Problems in Mathematics* (J. F. Nash Jr., M. T. Rassias, eds.), Springer,
  2016, pp. 1-122.
  [PDF auteur](https://www.scottaaronson.com/papers/pnp.pdf).
  Survey accessible et opinionné couvrant barrières, GCT, méta-complexité,
  derandomization. *« La vraie raison pour laquelle prouver P ≠ NP est dur,
  c'est qu'il existe d'innombrables façons remarquables d'éviter la recherche
  exhaustive »*. Lecture obligatoire avant toute nouvelle piste.

- **Indépendance formelle ?** — S. Aaronson, *« Is P versus NP formally
  independent? »*, Bulletin of the EATCS, vol. 81, 2003, pp. 109-136.
  [PDF auteur](https://www.scottaaronson.com/papers/indep.pdf).
  Examine l'hypothèse que P vs NP soit indépendant de ZFC ; conclut que peu
  probable mais pas exclu.

### 7.8 Outils annexes mobilisés dans le dépôt

- **Ax-Katz (théorie p-adique des solutions de polynômes)** — J. Ax, *« Zeroes
  of polynomials over finite fields »*, American Journal of Mathematics, vol.
  86, no. 2, 1964, pp. 255-261. N. M. Katz, *« On a theorem of Ax »*, American
  Journal of Mathematics, vol. 93, 1971, pp. 485-499.
  Cité au Tour 2 du dépôt (réfuté : ne survit pas à la contrainte booléenne
  `w_i² = w_i`).

- **Morse discrète** — R. Forman, *« Morse theory for cell complexes »*,
  Advances in Mathematics, vol. 134, no. 1, 1998, pp. 90-145.
  Cité au Tour 3 du dépôt (réfuté : effondrement des Betti sous sauts
  polynomiaux).

- **Stanley-Reisner et résolutions libres** — E. Miller, B. Sturmfels,
  *Combinatorial Commutative Algebra*, Graduate Texts in Mathematics, vol. 227,
  Springer, 2005.
  Référence-mère pour Tours 6, 7, 8, 9 (idéaux Stanley-Reisner, formule de
  Hochster, dualité d'Alexander, Boij-Söderberg).

- **Hardness amplification et méthode polynomiale** — A. R. Klivans, R. A.
  Servedio, *« Toward attribute efficient learning of decision lists and
  parities »*, Journal of Machine Learning Research, vol. 7, 2006, pp. 587-602.
  Cité indirectement au Tour 4 du dépôt comme exemple de méthode polynomiale
  appliquée à TC⁰.

### 7.9 Note méta-bibliographique

La condition (q) §5 (audit bibliographique préemptif, ajoutée Tour 22) impose
au Proposeur de vérifier que toute idée n'est pas déjà couverte par cette
bibliographie *avant* soumission. Pattern observé : sur les 8 ÉTABLIS Tours
12-20, **7 sont folklore** identifiables dans cette bibliographie ; seul L18
(IP, formule `(3^n − 1)/2`) reste de statut incertain. La condition (q)
formalise la leçon : *toute proposition aurait dû citer au moins une référence
de §7 ou justifier explicitement son absence*.

### Échange externe — Mika Göös (2026-06-12)
Réponse de Mika Göös à l'email (référence/antériorité) : « Sorry, I don't
know any reference off the top of my head. These days you could also ask
ChatGPT :) ». Lecture : accusé de réception courtois, non engagé (off-the-cuff)
— indication FAIBLE que la question n'est pas un classique immédiat dans son
aire, mais une seule réponse à froid, non creusée. Ne RIEN en conclure sur
l'ouverture/nouveauté. Bons interlocuteurs ciblés restent : auteurs KV
(Conjecture 5, déjà contactés) et Mossinghoff (fil d(m)/m=20, email prêt).

### Échange externe — Vaibhav Krishan (auteur KV), 2026-06-12 — VALIDATION
Réponse de V. Krishan (co-auteur de TR24-074) à l'email de réfutation de
la Conjecture 5 : « *It's indeed useful to know that the conjecture is false,
and it rules out the shortest vector approach as stated in our paper toward
proving an error-degree tradeoff for AND in the symmetric case. Would be happy
to hear back if you have more thoughts.* »
PORTÉE (confirmée par l'auteur) : notre contre-exemple (V-017b/c, V-018) +
la théorie quantitative (loi des fenêtres V-032, cœurs 2Phi3+x, carte de
phase V-046, seuil de découplage m*=15) FERME une voie de leur programme
(SV-approach pour le tradeoff erreur-degré de AND, cas symétrique). C'est
le résultat le plus fort du dépôt, désormais validé par un auteur. L'auteur
invite une suite — réponse substantielle en préparation (notes/kv_reply_2_draft.md).

### Échange externe — Chen Shuwen (référence mondiale PTE), 2026-06-12 — ANTÉRIORITÉ PRIMAIRE
Données autoritaires (bib/chen_shuwen_2024_reponse.md) : recherches exhaustives
d'idéales NON SYMÉTRIQUES — taille 8 jusqu'à 570 (trouvées, p.229) ; taille 9
jusqu'à 592 (AUCUNE) ; taille 10 jusqu'à 530 (AUCUNE) ; taille 11 jusqu'à 1600
(AUCUNE, p.52) ; taille 12 jusqu'à 500 (AUCUNE).
RECALIBRATION (22e auto-correction) : notre span-96 (idéale taille 8 non sym.)
= CONNU (Chen p.229) ; chasse d=8→idéale-9-non-sym FERMÉE (Chen ≤592) — cible
abandonnée. Distinction clé : nos minima asym. de RÉSEAU (V-042, d≤7, non idéaux)
≠ idéales non sym. de Chen. CORROBORATION : Chen confirme idéales symétriques
tailles 9-12 large plage = soutient notre loi V-042 (cas idéal). Notre apport
unique reste le certificat INCONDITIONNEL réseau (toutes formes, défectueux
compris, par span) pour KV — pas la découverte d'idéales (verrou de Chen).

### Échange externe — Michael Mossinghoff (auteur de la table BM 2000), 2026-06-12 — NOUVEAUTÉ CONFIRMÉE
Réponse de M. Mossinghoff à l'email V-047 (rang m=20) : « *That is a very nice
example, I do not believe another example with height 1 and multiplicity exactly
20 has appeared before.* » — NOUVEAUTÉ de notre produit pur plat (degré 307, h=1,
mult. exactement 20) CONFIRMÉE PAR L'AUTEUR de la table. Il valide aussi l'idée
de borner la hauteur de transit (« promising space ») et note que le saut 31→50
explique que leur méthode l'ait manqué. Pointeur d'antériorité fourni : Cipu 2004
(LMS JCM) — produits purs MAIS minimise L₂, ses mult-20 ont hauteur 2 : adjacent,
ne préempte pas (bib/cipu_2004_pointeur.md). « Please keep me posted. »
STATUT : 1er objet du dépôt à nouveauté validée par l'autorité du domaine. Réel
mais PÉRIPHÉRIQUE à P vs NP (théorie des nombres expérimentale). Soumission OEIS
A059753 (rang 20) désormais bien fondée.
