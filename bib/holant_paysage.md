# Audit A-021 — Le paysage holographique et les dichotomies Holant (audit fondateur de la ligne 19)

Tâche : A-021 (2026-08-08). Type A (audit sur textes, multi-pièces).
Rattachement : création de la ligne 19 (condition posée par PR-003) +
carte des poches du fil HOL. Audit mené par agent (règles du dépôt),
consigné et relu par la session. **17 textes lus in extenso** (PDF →
texte, extractions versionnées `bib/pdf/holant/`), 32 pièces
identifiées, révisions contrôlées à l'ouverture ET à la clôture
(2026-08-08, aucun changement).

**Correction d'identification** (erreur de la candidature, reconduite
par la mission) : « Accidental Algorithms » = FOCS **2006** (le miracle
mod 7 y est) ; FOCS 2004 = « Holographic algorithms (extended
abstract) ». La ligne 19 cite « Valiant 2004/2006/2008 ».

## 1. Identifications (extrait — table complète dans le rapport d'agent, révisions contrôlées)

Pièces maîtresses ouvertes : Valiant FOCS 2006 (page auteur) ; Valiant
SICOMP 2008 (préversion auteur + ECCC TR05-099, sans révision) ;
Valiant CC 2018 ; Cai-Gorenstein ToC 2014 (open access) ; Cai-Lu JCSS
2011 ; Cai-Lu « Bases Collapse » CCC 2007 ; ECCC TR07-020 (sans
révision) ; S. Chen STOC 2016 (arXiv v1 seul) ; CLX SICOMP 2011 ; CLX
Holant* SODA 2011/ToCS 2020 ; CHL Algorithmica 2012 ; Huang-Lu CCC
2012 ; CGW SICOMP 2016 (arXiv v3) ; CLX Holant^c réel SODA 2018 ;
Backens ICALP 2018 + SICOMP 2021 ; Shao-Cai FOCS 2020 (arXiv v1 seul ;
dblp : PAS de version journal) ; GLV SICOMP 2013 ; GHLX STACS 2011 ;
Faben arXiv 2008 ; Cai-Chen JACM 2017 (arXiv v1) ; CLX domaine 3 SODA
2013 ; CLX capture planaire SICOMP 2017 (arXiv v1 seul) ; Cai-Fu
universalité STOC 2017 (arXiv v1 seul, 94 p.) ; CFGW FOCS 2015 (arXiv
v1 seul) ; fronts 2025-2026 en abstracts (Meng-Wang-Xia-Zheng
arXiv:2502.05597 ; Cai-Ihm ICALP 2025 ; Fan-Cai-Shao-Tang STOC 2026).
**NON OUVERTS** : Cai-Fu Inf. Comput. 2014 (source première du lemme
d'arité ≤ 3 — relayé verbatim par arXiv:1603.07046 Lemma 2.27) ;
Xia-Zhang-Zhao TCS 2007 (attribution #P relayée par Cai-Lu) ;
Lin-Wang SICOMP 2018 ; Cai-Fu-Shao ICALP 2020.

## 2. Les fondations (verbatims)

**V1.1** (Valiant FOCS 2006, abstract) : « We consider a minimalist
version of Cook's 3CNF problem, namely that of monotone planar 3CNF
formulae where each variable occurs twice. We show that counting the
number of solutions of these modulo 2 is ⊕P-complete (hence NP-hard)
but counting them modulo 7 is polynomial time computable. »

**V1.3** (ibid., Theorem 4.1) : « For F7, n = (1, 1, 2, 1) and
p = (2, 3, 6, 2) is such a common basis for generating [1, 0, 1] and
recognizing [0, 1, 1, 1]. » — base de taille 2 ; descente en taille 1
attribuée « Cai and Lu, personal communication, June 2006 » :
« n = (1, 6) and p = (2, 4) ». **La configuration exacte du miracle :
générateur =₂ = [1,0,1], reconnaisseur OR₃ = [0,1,1,1], base commune —
précisément le système mesuré par PR-003/PR-001.**

**V1.5** (ibid., Theorem 4.2 — la trace char 0) : « For C there are
common bases of size one for (i) generating [1, 0, 1] and recognizing
[0, 1, 1, −4/3] and for (ii) generating [1, 0, α] and recognizing
[0, 1, 1, 1] where α is a root of x² + 3x + 3 = 0. » (Sur ℂ, la paire
exacte n'existe pas ; ses voisines à un paramètre, oui. −4/3 ≡ 1 ⟺
p | 7 — lecture d'audit.)

**V1.6** (ibid.) : « Matchgates and bases for these symmetric
signatures were discovered over F7 using the computer algebra system
Singular » — le solveur formel est l'instrument historique de la
famille.

**V1.7** (ibid., Th. 5.2 + Open Problem 3) : « There is no elementary
matchgrid algorithm for 3CNF. » ; « Is there a matchgrid algorithm for
#3CNF. »

**V1.8** (Valiant SICOMP 2008, Theorem 4.1) : « For any matchgrid Ω
over any basis b if Ω has weighted graph G then
Holant(Ω) = PerfMatch(G). »

**V1.9** (ibid. — la thèse P vs NP de la famille) : « we suggest that
any proof of P ≠ NP may need to explain, and not only to imply, the
unsolvability of our polynomial systems. Furthermore explanations of
such unsolvabilities may then stand equally in the way of any proofs
of P ≠ P^#P, P ≠ BPP, P ≠ QBP, P ≠ NC2 and P = PSPACE. »

**V1.10** (ECCC TR05-099, abstract) : « holographic reductions provide
a method of translating a combinatorial problem to a family of finite
systems of polynomial equations with integer coefficients such that
the number of solutions of the combinatorial problem can be counted in
polynomial time if some system in the family has a solution over the
complex numbers. […] If the method is applied to a #P-complete problem
then a family of polynomial systems is obtained such that the
solvability of any one member would imply that #P can be computed
within NC2. »

**V1.11-V1.13** (Cai-Gorenstein ToC 2014) : les IDENTITÉS DE MATCHGATE
(Th. 2.1, forme Grassmann-Plücker Σᵢ (−1)ⁱ Γ_{α⊕e_{p_i}} Γ_{β⊕e_{p_i}}
= 0) ; « If a vector Γ obeys the MGI, then it also obeys the Parity
Condition » (Th. 2.2) ; **suffisance sur TOUT corps** (Th. 5.1) :
« Let F be any field. Any Γ ∈ (F²)^⊗k satisfying the Matchgate
Identities is the signature of a matchgate with k external nodes. The
matchgate has O(k⁴) nodes. »

**V1.14** (Cai-Fu arXiv:1603.07046, Lemma 2.27 — LA QUESTION D'ARITÉ
≤ 3 TRANCHÉE) : « If f has arity ≤ 3, then f ∈ M iff f satisfies the
Parity Condition. » (source première : Cai-Fu Inf. Comput. 2014,
Lemmas 2.3/2.4, paywallée) ; « Hence all constructible non-matchgate
signatures have arity ≥ 4. » **Conséquence : l'instrument parité-seule
du dépôt est EXACT (nécessaire ET suffisant) à l'arité ≤ 3 — les
verdicts « faisable » de PR-003/PR-001 sont des réalisabilités
PROUVÉES.** Le bord : l'arité 4, première MGI non triviale. L'agent a
en outre RE-DÉMONTRÉ V1.14 exécutablement (les 2+12+56 instances de
MGI à k ≤ 3 identiquement nulles sous parité, sympy sur ℤ — valable
sur tout anneau commutatif), indépendamment de la source paywallée.

**V1.15-V1.16** (Cai-Lu JCSS 2011) : caractérisation des symétriques
réalisables (récurrence du second ordre ax_k + bx_{k+1} + cx_{k+2} =
0) ; et **le Simultaneous Realizability Problem (SRP), problème NOMMÉ
et RÉSOLU** : « Theorem 4.1. This is a polynomial time algorithm for
SRP. » — l'instrument du dépôt est une instance du SRP : légitimité
totale, originalité nulle.

**V1.17-V1.18** (effondrement des bases) : « 2-dimensional bases are
universal for holographic algorithms » (TR07-020) ; taille 1 suffit
dès qu'un générateur non dégénéré existe (CCC 2007) ; tous domaines :
⌊log₂ k⌋ pour full rank + « The rank of the standard signature matrix
Γ is always a power of two » (Chen STOC 2016). [Le survey de Cai
(~2008) disant « still open » est PÉRIMÉ — ne jamais le citer là-dessus.]

## 3. Les dichotomies (verbatims — le verrou de la ligne)

- **Holant*** complexe symétrique (CLX SICOMP 2011, Th. 4.1 — « The
  dichotomy is still valid even if the inputs are restricted to planar
  graphs ») ; **non symétrique** : SODA 2011/ToCS 2020 (« The
  constraint functions need not be symmetric functions »).
- **Holant^c** : réel symétrique (CLX 2011) → complexe symétrique (CHL
  2012, Th. 6) → réel non symétrique (SODA 2018) → **complexe non
  symétrique (Backens, Th. 15, SICOMP 50(6) 2021)** — POCHE FERMÉE.
- **Holant tout court** : réel symétrique (Huang-Lu CCC 2012) ;
  **symétrique complexe COMPLET** (CGW SICOMP 2016 : tractable ⟺
  arité ≤ 2, transformable affine, transformable produit, vanishing,
  Fibonacci-vanishing) ; **réel non symétrique COMPLET** (Shao-Cai
  FOCS 2020, condition (T)) ; complexe à arité impaire présente :
  fermé en FP^NP vs #P (Meng-Wang-Xia-Zheng 2025) ; **complexe
  toutes-arités-paires : OUVERT — le dernier trou booléen** (« a
  challenge that remains unresolved »).
- **#CSP** : complexe, TOUS domaines finis (Cai-Chen JACM 2017).
- **Capture planaire** : #CSP booléen — « category (2) consists
  precisely of those problems that are holographically reducible to
  the FKT algorithm » (Cai-Fu STOC 2017, complexe non symétrique ;
  déjà CLX SICOMP 2017 en symétrique réel). **MAIS pour Pl-Holant,
  FKT N'EST PAS UNIVERSEL** (CFGW FOCS 2015 : « The planar tractable
  class includes both those solvable by holographic reductions to FKT
  and those newly discovered ») — et du neuf encore à STOC 2026
  (8-vertex : « beyond Kasteleyn's algorithm »).

## 4. Le paysage modulaire (P7)

**V3.2** (Cai-Lu JCSS 2011, Th. 5.1 — contient notre fait (i)) :
« There is a polynomial time algorithm for #_{2^k−1}Pl-Rtw-Mon-kCNF.
Furthermore, any modulus m for which the appropriate signatures exist
must be a divisor of 2^k − 1. » — « In the case of k = 3, this shows
why 7 is special. » Mécanisme : ω² = 2 ∧ ω^k = ±1 ⟹ 2^k − 1 = 0 ;
« for any odd prime p, any prime factor q of the Mersenne number
2^p − 1 has q ≡ ±1 mod 8, and therefore 2 is a quadratic residue ».

**V3.3** (ibid., §5.2 — contient notre fait (ii), SANS preuve
détaillée) : « one may wish to extend the previous two problems to
allow more than Read-twice […] This calls for a simultaneous
realizability of [1, 0, 0,…, 0, 1] and [0, 1, 1,…, 1]. **This can be
shown to result in an empty intersection on M.** »

**V3.4-V3.5** (Faben 2008 ; GHLX STACS 2011) : sans planarité, AUCUN
miracle mod k — affine sinon #_pP-dur (« The answer is almost always
no »).

**V3.6** (GLV SICOMP 2013) : ⊕Holant symétrique fermé (A, M, Fibonacci
+[0,1,0], O) — et « It leaves open the corresponding questions for NP,
#P, and #_kP for k ≠ 2 » : **#_kHolant k ≠ 2 OUVERT, déclaré tel** ;
aucun texte 2014-2026 trouvé qui le ferme.

**V3.7** (Valiant CC 2018) : nouveaux algorithmes ⊕P planaires hors
élémentarité (corps exponentiels, interpolation, bases à 3
composantes) — le front mod 2 continue.

## 5. Verdict par poche (la carte du fil HOL)

| Poche | Verdict | Bord exact |
|---|---|---|
| P1 domaines ≥ 3 | PARTIELLEMENT FERMÉE | #CSP : fermé tous domaines (JACM 2017) ; Holant dom. 3 symétrique réel : fermé (ICALP 2025) ; dom. ≥ 4 : OUVERT ; collapse ⌊log₂ k⌋ full-rank seulement |
| P2 asymétriques | PARTIELLEMENT FERMÉE, se referme vite | réel fermé (FOCS 2020) ; complexe arité impaire fermé (2025, FP^NP vs #P) ; **complexe toutes-arités-paires : LE dernier trou booléen** |
| P3 Holant^c | **FERMÉE** | Backens SICOMP 2021 (complexe non symétrique) |
| P4 identités arité ≤ 3 | **FERMÉE — POSITIVE** | parité ⟺ matchgate (Lemma 2.27 + re-démonstration exécutable) ; bord = arité 4 (première MGI non triviale) |
| P5 effondrement des bases | **FERMÉE (dom. 2)** | 2×2 universel (TR07-020), taille 1 sous générateur non dégénéré ; tous domaines : full-rank seulement (Chen 2016) |
| P6 multi-gadgets / planaire | #CSP : FERMÉE (FKT = LE mécanisme, STOC 2017) ; **Pl-Holant : OUVERTE ET VIVANTE** | FKT non universel (FOCS 2015) ; « beyond Kasteleyn » à STOC 2026 — les nouveaux tractables planaires (arité 4, 8 composantes) sont à l'échelle de l'instrument |
| P7 paysage mod k | PARTIELLEMENT FERMÉE | sans planarité : rien (2008/2011) ; module = diviseurs de 2^k − 1 (Th. 5.1) ; fanout > 2 vide (§5.2) ; **#_kHolant k ≠ 2 : OUVERT (GLV)** ; famille 2^k − c² + cibles Valiant 2018 = instrument SRP existant |

## 6. Folklore-check des faits mesurés du dépôt

1. **Fait (i)** ({OR₃,=₂} faisable uniquement à p = 7, infaisable
   char 0) : **CONNU — théorème publié** (Valiant Th. 4.1/Cor. 4.1 +
   Cai-Lu Th. 5.1 : m divise 2³−1 = 7 ; char 0 impliqué par le
   mécanisme et cohérent avec V1.5). Statut dépôt : **réplication
   vérifiante par deux instruments indépendants** — recevable comme
   telle, pas comme découverte. Le compte « 72 bases » n'est pas
   recensé ; lecture d'audit (non vérifiée, calculable) : 72 = 2
   orbites × 36 (|F₇*|²) du manifold M.
2. **Fait (ii)** (frontière fanout-2 : {OR₃,=₃} vide partout) :
   **ÉNONCÉ sans preuve détaillée** (V3.3 : « can be shown ») — les
   certificats du dépôt (1 ∈ idéal en char 0 ; exhaustif GL₂(F_p))
   sont la **première vérification exécutable avec certificats**
   rencontrée par l'audit pour (l, k) = (3, 3). Valeur = le
   certificat, pas l'énoncé.
3. **La méthode** : c'est le SRP (nommé, décidable en P, Cai-Lu
   Th. 4.1) ; la découverte historique s'est faite au solveur
   (Singular). Légitimité totale, originalité nulle.
4. **Bonus session agent** : re-démonstration exécutable de V1.14
   (MGI k ≤ 3 nulles sous parité, coefficients entiers).

## 7. Matière pour la ligne 19 (consignée dans la matrice)

Direction P = NP textuellement Valiant (V1.9, V1.10 — la solvabilité
d'UN système donnerait #P ⊆ NC²). Barrières : **le corpus TAIT les
trois** (0 occurrence de natural proofs / algebrization / BGS / AW /
RR sur 17 textes ; unique « relativization » : mention bibliographique
GLV). À la place, la **barrière interne positive** : les dichotomies —
tout périmètre dichotomisé est « tractable connu ou #P-dur
inconditionnel », donc tout futur accident y vaudrait l'effondrement
FP = #P entier ; les impossibilités internes (pas d'encodage
élémentaire de 3CNF ; collapse des bases) ; la capture planaire (#CSP :
FKT seul mécanisme ; Pl-Holant : non — l'unique endroit où du neuf
apparaît encore).

## 8. Réserves d'audit

1. Versions non canoniques pour 3 pièces (FOCS 2006 page auteur ;
   SICOMP 2008 préversion ; CGW arXiv v3) — paywalls non contournés.
2. Cai-Fu Inf. Comput. 2014 (source première d'arité ≤ 3) non ouvert —
   relayé par arXiv:1603.07046 + re-démonstration exécutable ; citer
   les deux.
3. Shao-Cai FOCS 2020 : pas de version journal recensée (dblp).
4. Backens arXiv v2 du 2025-08-07 non examinée — citer SICOMP 2021.
5. Pièces 2025-2026 : v1 arXiv récentes (front vivant) — re-vérifier
   avant toute cellule qui s'y appuierait comme verrou.
6. Deux lectures d'audit calculables non exécutées : « 72 = 2
   orbites » ; « −4/3 ≡ 1 mod 7 ».
