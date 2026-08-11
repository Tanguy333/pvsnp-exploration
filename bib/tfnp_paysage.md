# Audit A-022 — Le paysage TFNP (audit fondateur de la ligne 20)

Tâche : A-022 (2026-08-10 ; déclarée le 09). Type A (audit fondateur,
multi-pièces). Rattachement : création de la ligne 20 (condition posée
par PR-004). Audit par agent (règles du dépôt), consigné et relu par
la session. **14 textes lus in extenso** (extractions versionnées
`bib/pdf/tfnp/`), 6 pièces au niveau abstract verbatim (pages
officielles eprint/ECCC), 3 blocages d'accès documentés (ScienceDirect,
ACM, eprint-PDF — contournements légitimes : miroirs d'auteurs, .ps
converti, abstracts officiels). Révisions contrôlées à l'ouverture ET
à la clôture — aucune pièce n'a bougé.

Pièces intégrales : Megiddo-Papadimitriou TCS 1991 (copie d'auteur,
scan) ; Papadimitriou JCSS 1994 (miroir Matoušek) ; BCEIP JCSS 1998
(.ps Pitassi) ; DGP SICOMP 2009 ; Chen-Deng-Teng JACM 2009 (arXiv
v1) ; FGHS JACM 2022 (arXiv v4) ; GHJMPRT « Further Collapses » CCC
2022 (arXiv v2) ; Göös et al. « Separations in Proof Complexity and
TFNP » JACM 2024 (arXiv v3) ; BPR FOCS 2015 (ECCC TR15-001) ; Korten
FOCS 2021 (arXiv v3) ; KKMP ITCS 2021 (DROPS) ; GLS-D STOC 2026 (ECCC
TR25-210, 0 révision) ; Fleming-Imrek-Marciot CCC 2025 (DROPS) ; FISV
(arXiv:quant-ph/0505185). Abstracts : CHKPRR STOC 2019 (eprint
2019/549), JKKZ STOC 2021 (eprint 2020/980), BCHKLPR TCC 2022 (eprint
2022/1272), KLV (eprint 2022/1409 — venue NON VÉRIFIÉE), RSS (eprint
2016/375).

## 1. Fondations (verbatims)

**V1.1** (MP91, déf.) : « We call R total if, for every x ∈ Σ*, there
is always a y ∈ Σ* such that (x, y) ∈ R. We let TFNP (for total
functions from NP) be the class FNP restricted to total relations R. »
« Notice that TFNP coincides with F(NP ∩ coNP). »

**V1.2 — LA FLÈCHE, correction d'attribution.** « Si P = NP alors
TFNP = FP » n'est PAS un théorème numéroté de MP91. Le texte courant
(p. 318) : « The subset of FNP that ca[n be] solved in polynomial time
is called FP. At present it is not known whether FP = F[NP]; this
question is equivalent to the P = NP question. » (crochets = scan
rogné). La flèche = TFNP ⊆ FNP (déf.) + cette équivalence, dont la
preuve (recherche-vers-décision préfixe par préfixe) est standard et
non écrite dans MP91. **Attribution pour la ligne 20 : « MP91 p. 318
(équivalence, déclarée connue) + dérivation standard » — pas de
numéro fantôme.**

**V1.3** (MP91, Theorem 2.1 — LE verrou anti-NP-dureté) : « There is
an FNP-complete problem in TFNP if and only if NP = coNP. »

**V1.5** (pas de TFNP-complet attendu) : « As with other classes
(such as NP∩coNP, R, BPP, etc.) whose machine-based definition is
semantic instead of syntactic […] we do not expect such problems to
exist. »

**V1.6** (P94, les classes par principe) : parité (« Any finite graph
has an even number of odd-degree nodes »), PLS (puits d'un DAG), PPA
(feuille non standard), PPAD (source/puits orienté non standard),
PPP (PIGEONHOLE CIRCUIT complet) ; Proposition 1 :
« FP ⊆ PPAD ⊆ PPA ⊆ FNP » ; Proposition 4 (Vavasis, Yannakakis) :
« PPAD ⊆ PPP » ; Proposition 3 : « If PPP = FP then one-way
permutations do not exist » ; Theorem 2 : la variante « LA feuille
appariée » saute à FPSPACE. PPADS : absent de P94 (problème ouvert
(5), avec l'erratum d'une version préliminaire) — le nom et la
séparation viennent de BCEIP.

**V1.7** (complétudes d'origine, P94) : « 3D SPERNER is
PPAD-complete » ; BROUWER, KAKUTANI, EXCHANGE ECONOMY PPAD-complets ;
« NASH is in PPAD » (appartenance seule en 1994).

**V1.8** (P94, ouvertures porteuses) : (3) « Is 2D-SPERNER
PPAD-complete? […] **1D-SPERNER represents FP (it embodies binary
search in an exponential domain)**, 3D-SPERNER represents PPAD » — la
calibration 1D du sous-lemme PR-004 est TEXTUELLE dans le papier
fondateur ; (7) le lien arithmétique bornée (S¹₂, Buss) dès 1994 ;
(8) « I suspect that all these classes can be separated in all
possible ways by oracles. »

**V1.9** (Nash) : DGP SICOMP 2009 Th. 5.1 (« Both 3-Nash and
3-graphical Nash are PPAD-complete ») ; Chen-Deng-Teng JACM 2009
Th. 1.1 (« Bimatrix is PPAD-complete »), Th. 1.2 (approximation
n^{−c} PPAD-complète), Th. 1.3 (pas de FPTAS sauf PPAD ⊆ P).

**V1.10** (FGHS, JACM 2022) : « Theorem 6.1 : CLS = PPAD ∩ PLS. » ;
Th. 5.1 : KKT, GD-Local-Search, GD-Fixpoint, General-Continuous-
Localopt PPAD∩PLS-complets sur [0,1]² ; « the first non-artificial
problem to be shown complete for this class » — INCONDITIONNEL
(égalité de classes, zéro crypto).

**V1.11** (GHJMPRT, CCC 2022) : « Theorem 1. EOPL = PLS ∩ PPAD.
Theorem 2. SOPL = PLS ∩ PPADS. » Et le témoignage méthodologique :
« we set out to prove this separation in the black-box model […] We
tried in vain for nine months. The upshot is that Theorems 1 and 2
now crush this possibility, as they hold even in the black-box
model. »

## 2. La route crypto (le mécanisme white-box, conditionnel)

**V2.1** (BPR FOCS 2015, l'origine) : « Suppose that there exist
sub-exponentially-hard injective one-way functions and
quasi-polynomially-hard indistinguishability obfuscation for P/poly.
Then, the END-OF-THE-LINE problem is hard for polynomial-time
algorithms. »

**V2.2** (CHKPRR STOC 2019, abstract eprint) : « solving the
End-of-Metered-Line problem is no easier than breaking the soundness
of the Fiat-Shamir transformation when applied to the sumcheck
protocol » ; instanciation : FHE quasi-optimale + #SAT dur sur
polylog variables ⟹ distribution dure dans CLS ⊆ PPAD.

**V2.3** (JKKZ STOC 2021, abstract eprint) : Fiat-Shamir instancié
pour sum-check/GKR « assuming the sub-exponential hardness of LWE » ⟹
« sub-exponential average-case hardness of PPAD ».

**V2.4** (état des hypothèses 2022-2026) : TCC 2022 : « PPAD is as
hard as learning with errors (LWE) and the iterated squaring (IS)
problem […] improves over prior hardness results that relied either
on (1) sub-exponential assumptions, or (2) “obfustopia” » (LWE
POLYNOMIAL + IS) ; KLV : « hard problems in PPAD, assuming the
sub-exponential hardness of DDH ». **« LWE polynomial SEUL » :
[NON TROUVÉ]** au 2026-08.

**V2.5** (la limite interne — RSS, J. Cryptology 2021) :
« Average-case PPAD hardness (and even SVL hardness) does not imply
any form of cryptographic hardness (not even one-way functions) » ;
les constructions depuis hypothèses standard produisent des instances
à nombre quasi-exponentiel de solutions — divergence structurelle
d'avec la voie obfuscation (solutions uniques).

## 3. Les deux frontières

**Ligne 15 (preuves).** Göös et al. JACM 2024 : « we characterise the
classes PPADS, PPAD, SOPL by unary-SA, unary-NS, and Reversible
Resolution » ; tableau des Θ : FP^dt ↔ TreeRes, PLS^dt ↔ Res,
PPA^dt ↔ NS-F₂, PPA_p^dt ↔ NS-F_p, PPAD^dt ↔ uNS, PPADS^dt ↔ uSA,
SOPL^dt ↔ RevRes, EOPL^dt ↔ RevResT ; PPP/UEOPL sans caractérisation
« élégante » (la note v3 signale [BFI22] : correspondance GÉNÉRIQUE
système-auto-prouvant ⟺ problème TFNP, couvrant PPP par un système
non naturel). **LE POINT CLÉ, textuel** : « We emphasise that unlike
the standard uniform setting of TFNP, we will be interested in
non-uniform variants […] defined by decision trees » ; « Clearly, any
unconditional separation is completely out of reach, since it would
immediately imply that P ≠ NP. However, it turns out that one can
indeed prove separations relative to oracles » — **le recouvrement
avec la ligne 15 est FORT mais strictement boîte-noire, déclaré par
les textes ; la question uniforme white-box reste distincte.**

**Ligne 16 (Avoid/APEPP).** KKMP ITCS 2021 : « PEPP is not obviously
in NP! […] An alternation of quantifiers appears to be at work! » ;
« TFNP is the first level of the hierarchy, and the class PEPP […] at
the second level, denoted TFΣ₂. » Fleming CCC 2025 : « any solution y
to Avoid can be checked by a coNP verifier […] Avoid belongs to the
class TFΣ₂. » GLS-D STOC 2026 : « Notice that Avoid is not in TFNP
unless P = NP. » **La distinction est un théorème relativisé** : monde
où TFNP = FP mais TFΣ₂ ≠ FP^NP (Buhrman-Fortnow-Koucký-Rogers-
Vereshchagin, Theory Comput. Syst. 2010, cité par KKMP). **Les ponts,
tous récents** : FNP ⊆ PEPP (KKMP Th. 1) ; Avoid → TFNP par réduction
RANDOMISÉE conditionnelle (GLS-D STOC 2026, sous PRG forts ; +
« BPP^Avoid ⊆ AM ∩ coAM ») ; hasard NÉCESSAIRE sous crypto (Chen-Li
STOC 2024 : Avoid ∉ SearchNP) ; le programme preuves↔classes soulevé
au niveau 2 (Fleming : PEPP^dt ⟺ Σ₂-Sherali-Adams).

## 4. Oracles et barrières

**V4.1** (BCEIP, le cadre — Theorem 1) : « Let Q₁, Q₂ ∈ TFNP². The
following are equivalent: (i) Q₁ is many-one reducible to Q₂; (ii)
For all oracles A, (C_{Q₁})^A ⊆ (C_{Q₂})^A; (iii) There exists a
generic oracle G […]. » — **le régime inconditionnel boîte-noire
relativise PAR CONSTRUCTION.** Séparations : PPA^G ⊄ PPP^G,
PPP^G ⊄ PPADS^G, PPADS^G ⊄ PPA^G ; Theorem 12 = déjà une borne de
degré Nullstellensatz (PHP, degré ≥ √(2N) − 1) en 1998 ; Theorem 17 :
la recherche totale n'est équivalente à AUCUNE décision (relativisé).
Complété par Morioka 2001, Buresh-Oppenheim-Morioka CCC 2004, et la
pièce JACM 2024 (« complete picture of the black-box relationships »).

**V4.2** (relativisation de la flèche) : « P^O = NP^O ⟹ TFNP^O =
FP^O » n'apparaît nulle part sous cette forme — dérivation standard
(l'argument préfixe relativise), portée en contraposée par BCEIP
(« absolute separations would imply that P ≠ NP »).

**V4.4** (barrières, grep systématique sur ~15 textes) :
« algebriz- » : **0 occurrence** ; Baker-Gill : 0 ; AW08 : 0 — le
corpus TAIT l'algébrisation (même profil que la ligne 19).
« relativiz- » : omniprésent comme MÉTHODE (jamais comme discussion de
la barrière nommée). « natural proofs » : UNE occurrence porteuse,
chez Korten — l'analogue RR pour la LIGNE 16 : « just as the Natural
Proofs barrier shows that a generic method of proving circuit lower
bounds via a “Natural Property” would require solving a hard
computational problem, hardness of Empty would show that we should
not expect to prove exponential lower bounds for E via an efficient
algorithm that finds an empty pigeonhole. »

## 5. Folklore-check du sous-lemme PR-004 (table Sperner)

- 1D : textuel dans P94 (« 1D-SPERNER represents FP (it embodies
  binary search) ») ; valeurs exactes 2, 3, 4 : [NON TROUVÉ],
  triviales.
- 2D : la référence serrée n'est PAS HPV mais **Crescenzi-Silvestri
  1998** (borne Ω(√n) déterministe, n = sommets) close par **FISV**
  (arXiv:quant-ph/0505185) : « This upper bound matches the Ω(√n)
  deterministic lower bound of Crescenzi and Silvestri. The tightness
  of this bound was not known before. » En côté de grille : **Θ(k),
  linéaire** — nos 3, 4, 6 (accroissements +1, +2) sont compatibles ;
  valeurs exactes à petit k : [NON TROUVÉ] = réplication + constantes.
- HPV 1989 (paywall, non ouvert) : l'antériorité de la famille
  « bornes d'oracle pour Brouwer » (via MP91/P94/DGP) — la déclaration
  de la candidature était juste d'esprit, la référence 2D à corriger.
- Compléments : 2D-SPERNER PPAD-complet (Chen-Deng ICALP 2006,
  identification — résout P94 (3)) ; FISV : randomisé Ω(n^{1/4}),
  quantique Ω(n^{1/8}).

## 6. État 2024-2026 (identifications)

TFNP quantique (Yamakawa-Zhandry JACM 2024 ; Göös-Gur-Jain
TR24-172 ; Aaronson-Buhrman-Kretschmer ITCS 2024) ; caractérisations
supplémentaires ([HKT24], [LPR24], Hubáček-Khaniki-Thapen ITCS 2024) ;
« Separations Above TFNP from Sherali-Adams Lower Bounds » (CCC
2026) ; complétudes (Pure-Circuit FOCS 2022 — inapproximabilité PPAD
serrée ; KKT quadratique 2024 ; PLC ITCS 2023) ; frontière ligne 16
vivante (Fleming CCC 2025, GLS-D STOC 2026, Chen-Li STOC 2024,
Korten BEATCS 2025). « Metric TFNP » : [NON TROUVÉ] ; les programmes
réels adjacents : métamathématique de TFNP (Kołodziejczyk-Thapen) et
TFNP quantique.

## 7. Réserves d'audit

1. CHKPRR/JKKZ/TCC22/KLV : abstracts officiels seuls (PDF bloqués) —
   hypothèses complètes mais sans théorèmes numérotés internes.
2. MP91/P94 : scans (OCR à défauts, restitutions entre crochets) ;
   BCEIP : PostScript converti.
3. « Best paper STOC 2021 » (FGHS), version SICOMP de GHJMPRT, venue
   de KLV : métadonnées non vérifiées sur texte.
4. Le balayage 2024-2026 est une identification, pas un audit.
5. La dérivation « TFΣ₂ ≠ FP^NP ⟹ P ≠ NP dans le monde BFKRV » est
   un raisonnement standard de l'audit, marqué comme tel.
6. Extractions versionnées `bib/pdf/tfnp/` (les .txt ; .pdf ignorés).
