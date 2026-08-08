# Audit HOL-003 — La poche « Holant booléen complexe toutes-arités-paires » (le dernier trou booléen)

Tâche : HOL-003 (2026-08-08, décision utilisateur). Type A (audit
ciblé). Rattachement : Atlas ligne 19 — préciser la poche. Audit par
agent (règles du dépôt), consigné et relu par la session. Révisions
contrôlées à l'ouverture ET à la clôture (aucun changement).

**Pièces lues** : MWXZ « From an odd arity signature to a Holant
dichotomy » arXiv:2502.05597 v1 (30 p., in extenso ; version canonique
CCC 2025, LIPIcs 339, non ouverte) ; MWX « The FP^NP versus #P
dichotomy for #EO » arXiv:2502.02012 v2 (STOC 2025) ; FCST
« ...Eight-Vertex Model » arXiv:2602.11292 v1 (STOC 2026, sections
1-3 + 2.5-2.6) ; extractions locales A-021 réutilisées (CGW, Backens,
Shao-Cai, CLX SODA 2018 — identifications corrigées dans la table de
l'agent). **Abstract seul** : GSS arXiv:2607.27961 v1 (30 juillet
2026 — 9 jours d'âge). Nouvelles extractions versionnées :
`bib/pdf/holant/mwxz_odd_arity.txt`, `mwx_eo_dichotomy.txt`,
`fcst_eight_vertex.txt`.

## 1. La dichotomie arité-impaire (MWXZ, CCC 2025)

**V1** (Théorème 2) : « Let F be a set of signatures that contains a
non-trivial signature of odd arity. Then one of the following holds.
1. Holant(F) is #P-hard; 2. Holant(F) is in FP^NP. »

**V2** (Théorème 33 — la condition (PC), 7 cas) : « Holant(F) is
#P-hard unless: 1. F̂ only contains HW≥ signatures (or HW≤ […]). All
signatures in F̂|EO are ∀3 signatures or all […] ∀3̄ […], and
F̂|EO ⊆ EOA or F̂|EO ⊆ EOP; 2. All signatures in F̂ are
single-weighted. […] 3. F ⊆ ⟨T⟩; 4. F̂ ⊆ ⟨M⟩ or F̂ ⊆ ⟨XM⟩; 5. F is
A-transformable; 6. F is P-transformable; 7. F is L-transformable; In
case 1, 2, Holant(F) is in FP^NP; in case 3-7, Holant(F) is polynomial
time computable. » (F̂ = K⁻¹F, K⁻¹ = (1/√2)[[1,−i],[1,i]].)

**V3** (Théorème 1/32, décomposition) : « 1. Holant(F,f,g) ≡_T
Holant(F, f⊗g); 2. Holant(F, f⊗g) is in FP^NP. »

**V4** (le mécanisme — Lemma 43) : auto-boucles ≠₂ sur l'arité
impaire → descente de 2 en 2 → **une unaire**, puis 4 cas (∆₀
transformable, ou les unaires (1, ±i) intransformables — « This
special case does not appear in the setting of real-valued
signatures » — c'est là qu'entrent HW≥/HW≤/single-weighted et FP^NP).

## 2. #EO — le socle (MWX, STOC 2025)

**V5** : EO signature = arité paire, nulle hors du demi-poids ;
« #EO(F) ≡_T Holant(≠₂ | F) » ; le six-vertex = « a #EO problem
defined by a single quaternary EO signature ».

**V6** (Theorem 26) : « #EO(F) is #P-hard, unless all signatures in F
are ∀3 signatures or all […] ∀3̄ […], and F ⊆ EOA or F ⊆ EOP, in which
cases it is in FP^NP. In particular, […] polynomial-time computable,
unless F is neither 0-rebalancing nor 1-rebalancing. » Généalogie :
Cai-Fu-Shao I&C 2020 (ARS seulement) → MWX 2024 (algorithmes) → MWX
STOC 2025 (général).

**V7** (∀3, critère de support) : f est ∃3↛ s'il existe α, β, γ ∈
supp(f) avec δ = α⊕β⊕γ ∈ HW=, δ ∉ supp(f) ; ∃3↑/∃3↓ si δ ∈ HW>/HW< ;
∀3 = ni ∃3↛ ni ∃3↑ (resp. ∀3̄).

**V8** (EOA/EOP) : « If for any perfect pairing P of Var(f),
f|EO_P ∈ A, then […] f is EOA » (resp. P).

## 3. Pourquoi FP^NP — et la pièce de juillet 2026

**V9** (MWXZ) : « the complexity class FP^NP is introduced due to the
dichotomy for #EO […] such dichotomy can separate the computational
complexity as well, unless the complexity class PH collapses at the
second level. […] if a traditional FP vs. #P dichotomy is later proved
for #EO, Theorem 2 will consequently become an FP vs. #P dichotomy as
well. »

**V10** (MWX — l'oracle = le « support identification problem ») :
décider si α_f ∈ supp(f) est « effective » dans une instance ;
« whether this problem can be computed in polynomial time or it is
NP-complete remains unsettled. Dozens of attempts have been made » ;
frontière : Feder-Ford (delta-matroïdes, SIDMA 2006).

**V11** (⚡ GSS arXiv:2607.27961, v1 du 2026-07-30, ABSTRACT SEUL) :
« we settle this question by giving a polynomial-time algorithm for
all cases on the FP^NP side. Consequently, we obtain a complete FP
versus #P dichotomy for counting weighted Eulerian orientations, and
further for complex-valued Holant problems with an odd-arity
signature. » — **préprint de 9 jours, non relu, non vérifié : ne
fonder AUCUNE cellule sur « FP vs #P » sans re-contrôle** (leçon
A-017/A-020 des rétractations).

## 4. Le trou, rendu exact

**V13** (MWXZ) : « it is now sufficient for future studies to focus on
the case when all signatures in F are of even arity. […] we may
further assume that these signatures are irreducible, and each
realized signature does not contain a factor of odd arity. »

**V14** : « the only remaining case is when all signatures in F are of
even arity and irreducible. Nevertheless, the analysis of this case
may present significant challenges, as was evidenced in the proof of
its sub-cases. »

**Lecture structurelle** (textuelle en creux, Table 2 : le nombre de
signatures d'arité impaire disponibles décroît « being infinite, 4, 2,
1 (and 0 in the last column) ») : les gadgets préservent la parité
d'arité — **en arités toutes paires, aucun pinning ∆₀/∆₁ n'est
réalisable** ; toute la machinerie d'entrée s'effondre.

**Le plus petit coin ouvert concret** (SYNTHÈSE D'AUDIT — l'assemblage
est de l'audit, chaque brique est textuelle ; aucun texte ne nomme de
« sixteen-vertex ») : Holant(f), UNE SEULE f : {0,1}⁴ → ℂ, avec
f̂ = K⁻¹f :
- supp(f̂) ⊆ poids pairs {0,2,4} : FERMÉ (huit-vertex, Cai-Fu I&C
  2023 ; planaire FCST STOC 2026) ;
- f̂ single-weighted, supp ⊆ HW≥ ou ⊆ HW≤ : FERMÉ (MWXZ Cor. 30/
  Th. 31 ; vanishing si strict) ;
- f symétrique : FERMÉ (CGW Th. 42) ; f réelle-transformable : FERMÉ
  (Shao-Cai) ; f réductible : ramenée aux arités ≤ 3 (V3) ;
- **RESTE : f d'arité 4 IRRÉDUCTIBLE, non symétrique, non
  réelle-transformable, à support K-MIXTE** (mélange de poids < 2 et
  > 2 sans être ⊆ {0,2,4}) — 16 composantes : l'échelle exacte de
  l'instrument.

## 5. Les classes tractables — critères décidables (cahier des charges HOL-004)

- **A (affine)** : f = λ·χ_{AX=0}·i^{Q(X)}, Q multilinéaire deg ≤ 2,
  termes croisés pairs (Shao-Cai Def. 2.18) — support affine + système
  linéaire mod 4.
- **P (produit)** : produit d'unaires, =₂, ≠₂ (Def. 2.17) ; nécessaire :
  |supp| puissance de 2 (FCST).
- **A-/P-transformable** (CGW Lemmas 51/57) : « F is A-transformable
  iff there exists an H ∈ O₂(C) such that F ⊆ HA or
  F ⊆ H[1 0; 0 α]A » (α = e^{iπ/4}) ; P : « F ⊆ HP or
  F ⊆ H[1 1; i −i]P » — balayage O₂(ℂ) = systèmes à 2 inconnues
  (a² + b² = 1), Gröbner.
- **Vanishing** : symétrique — critère vd/rd de CGW (Def. 17-21,
  récurrence (t¦t)i^t f_{k+t} + … = 0 ; f ∈ R⁺_{t+1} ⟺ f_k = i^k p(k),
  deg p ≤ t) ; **général — MWXZ Lemma 42 : f vanishing ⟺ supp(f̂) ⊆
  HW> ou ⊆ HW<** (le critère à 2 tests de support).
- **L (local affine — découverte CLX SODA 2018, PAS Backens)** :
  « A function f is in L, if and only if for each σ ∈ supp(f),
  (M_α^{s₁} ⊗ … ⊗ M_α^{sₙ})f is in A » (M_α = diag(1, e^{iπ/4})) ;
  « These interesting structures can only appear for general functions
  but not for symmetric ones » ; « The algorithm L contains a global
  step […] We have tried many purely local algorithms and failed. »
- **M à l'arité 4** (FCST Lemma 2.24, la MGI explicite) : « If f has
  arity 4, then f ∈ M iff f satisfies the Even Parity Condition […]
  and det M_Out(f) = det M_In(f); or f satisfies the Odd Parity
  Condition […] and f₀₀₁₀f₁₁₀₁ − f₀₀₀₁f₁₁₁₀ = f₀₁₀₀f₁₀₁₁ −
  f₀₁₁₁f₁₀₀₀. »
- **Aiguillage #EO** : ∀3/∀3̄ (V7, boucle sur triplets du support) +
  EOA/EOP (V8, 3 appariements parfaits à l'arité 4).
- **Huit-vertex** (Cai-Fu I&C 2023 via FCST Th. 2.33) : ax ≠ 0 ⟹
  #P-dur sauf P-/A-/L-transformable ; **planaire** (FCST Th. 3.1) :
  + M-transformable + le cas 5 neuf (« d = w = ±√(ax), b = y = −c =
  −z = i·tan(βπ/8)√(ax) » — « a previously unknown tractable type »,
  « provably not subsumed by holographic transformation plus FKT »).

## 6. Les difficultés déclarées

1. La perte du point d'entrée unaire (pas de pinning en arités paires).
2. Les sous-cas résolus furent des tours de force : les signatures de
   Bell de Shao-Cai (« These amazing signatures are wholly unexpected,
   and their existence presented a formidable obstacle to the
   induction proof » ; f8 = la « Queen of the Night », code linéaire
   de dim 4 dans Z₂⁸ — lien codes de Hadamard, Shao-Tang ITCS 2025) ;
   réductions NON constructives.
3. Le complexe casse les techniques réelles (Backens sur CLX :
   interpolation des unaires prouvée seulement en réel).
4. L est globale et non symétrique par nature.
5. L'oracle NP (V10) — poli seulement en juillet 2026 (GSS, v1 sous
   réserve).
6. Les vanishing complexes — « the only true obstacle to a converse of
   the Holant theorem » (Cai-Young ITCS 2026).

## 7. État 2025-2026

MWXZ → CCC 2025 ; #EO → STOC 2025 ; GSS v1 (2026-07-30) prétend
FP^NP → FP ; FCST → STOC 2026 (planaire arité 4, classe neuve hors
FKT) ; Cai-Young → ITCS 2026 (vanishing = seule obstruction à la
réciproque du théorème de Holant) ; **aucun préprint trouvé qui
attaque frontalement le cas toutes-arités-paires complexe** — le trou
est vivant, la communauté en polit les bords.

## 8. Réserves d'audit

1. GSS : abstract seul, v1 de 9 jours — citer « préprint non
   vérifié », aucune cellule fondée dessus.
2. Versions canoniques non ouvertes : MWXZ LIPIcs (lu arXiv v1,
   30 p.) ; MWX STOC (lu arXiv v2) ; Backens SICOMP (extraction locale
   = version courte ; Th. 15 ≡ Th. 59, énoncés coïncidents).
3. Cai-Fu I&C 2023 et six-vertex SODA 2021 relayés verbatim par FCST
   (co-auteur Cai), non ouverts directement.
4. La délimitation « plus petit coin = arité 4 irréductible à support
   K-mixte » est une SYNTHÈSE D'AUDIT, déclarée comme telle.
5. Extraction pypdf : indices reconstruits — revalider vd/rd et L sur
   PDF avant tout codage (consigne transmise à HOL-004).
6. FCST : sections 4-8 (preuves) non parcourues.
