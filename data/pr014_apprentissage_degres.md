# PR-014 — Trois îles d'apprenants et MOD₆ hors de toutes : degrés exacts, masse de Fourier, degré approché (réplication vérifiante déclarée ; témoin exécutable de l'entrée E-5)

Date : 2026-09-12. Instrument : `checks/pr014_apprentissage_degres.py`
(implémentation INDÉPENDANTE de la candidature n° 9 : transformée de
Möbius pour le degré exact sur F₂/F₃, Walsh-Hadamard pour la masse de
Fourier, CP-SAT pour le degré approché ; mode `--focus-mod6` pour les
certificats d'optimalité). Graine 20260912. Machine : 24 cœurs.

Mesures définies : **deg_F(f)** = degré du polynôme multilinéaire unique
sur F coïncidant avec f sur {0,1}ⁿ ; **W^{≤d}(f)** = Σ_{|S|≤d} f̂(S)² pour
f envoyée dans {±1} ; **adeg_{F,ε}(f)** = degré minimal d'un polynôme sur
F coïncidant avec f sur ≥ (1−ε)·2ⁿ points. Convention : MOD_m(x) =
[Σxᵢ ≡ 0 (mod m)] ; PARITY(x) = Σxᵢ mod 2 ; DNF : n termes de largeur 3,
littéraux tirés.

## 0. Antériorité (déclarée avant tout calcul)

| Objet | Résultat publié | Source |
|---|---|---|
| deg_{F_p}(MOD_q), p ∤ q, et l'inapproximabilité en bas degré | Ω(n) exact ; approximation ⟹ degré Ω(√n) | Smolensky 1987 (Razborov 1987) |
| deg_{F₃}(MOD₃) = 2, deg_{F₂}(PARITY) = 1 | exact (petit Fermat ; linéarité) | folklore |
| Concentration de Fourier d'AC⁰ / des DNF | masse sur les degrés ≤ polylog / ≤ log(s/ε) | LMN 1993 ; Jackson 1997 ; Mansour 1995 |
| Tables exactes à n = 8, 12 | — | [NON TROUVÉ] — mesure, pas découverte |

## 1. Degrés exacts et masse de Fourier, n = 12 (run eps8 et eps16, identiques)

| fonction | deg_F₂ | deg_F₃ | W^{≤2} | W^{≤4} | W^{≤log n} |
|---|---|---|---|---|---|
| PARITY | **1** | 12 | 0,000 | 0,000 | 0,000 |
| MOD₃ | 11 | **2** | 0,111 | 0,115 | 0,111 |
| MOD₆ | 11 | 12 | 0,406 | 0,512 | 0,406 |
| DNF(12×3) | 11 | 11 | 0,727 | **0,938** | 0,863 |

Conforme à la candidature (son pré-calcul : PARITY 1/12/0,000 ; MOD₃
11/2/0,115 ; MOD₆ 11/12/0,512 ; DNF 11/12/0,934 — la DNF diffère par la
graine). **Les trois îles sont nettes** : PARITY est linéaire sur F₂ ;
MOD₃ est de degré 2 sur F₃ (1 − (Σxᵢ)²) ; la DNF met 94 % de sa masse de
Fourier en degré ≤ 4. **MOD₆ n'est sur aucune** : degré 11 sur F₂, 12 sur
F₃, masse de bas degré 0,51 — le mur des modules composés (Smolensky) lu à
n = 12.

## 2. Degré approché par CP-SAT, n = 8 — la cellule discriminante est MIS-SPÉCIFIÉE

### 2a. ε = 1/8 tel que spécifié (seuil 224/256) — run eps8, complet

| fonction | F₂ : adeg | trace (d : accord ; ? = non optimal) | F₃ : adeg | trace |
|---|---|---|---|---|
| PARITY | **1** | d0:128 d1:256 | > 4 | d0:128 d1:128 d2:166? d3:190? d4:227? |
| MOD₃ | > 4 | d0:171 d1:171 d2:199? d3:189? d4:219? | **2** | d0:171 d1:171 d2:256 |
| MOD₆ | **0** | **d0:227** | **0** | **d0:227** |
| DNF(8×3) | > 4 | d0:170 … d4:222? | > 4 | d0:170 … d4:220? |

Contrôles conformes (PARITY sur F₂ : 1 ; MOD₃ sur F₃ : 2, accord 256/256).
**Mais la cellule discriminante est vide** : MOD₆ = [Σ ≡ 0 mod 6] ne vaut
1 que sur 29 points sur 256 (poids 0 et 6), donc le polynôme CONSTANT 0
coïncide avec elle sur 227/256 = 88,7 % ≥ 7/8 : adeg_{F,1/8}(MOD₆) = 0
sur les deux corps. L'énoncé de la candidature (« adeg_{F₂}(MOD₆) et
adeg_{F₃}(MOD₆) tous deux ≥ 3 à n = 8 ») est FAUX tel qu'écrit — non
parce que MOD₆ serait facile, mais parce qu'un seuil d'accord ε = 1/8 est
vide pour une fonction à 11 % de uns : l'instrument ne mesure pas le
phénomène à cette échelle. (Les « ? » sur MOD₃/F₂, PARITY/F₃, DNF :
CP-SAT n'a pas certifié l'optimum en 120 s — ces cellules ne sont pas
conclues non plus, mais elles ne portaient pas la charge discriminante.)

### 2b. ε = 1/16 (correction du Réfuteur : seuil 240/256 > 227) — run eps16, INCOMPLET

| fonction | F₂ : adeg | trace | F₃ : adeg | trace |
|---|---|---|---|---|
| PARITY | 1 | d0:128 d1:256 | > 4 | d0:128 d1:128 d2:182? d3:190? d4:210? |
| MOD₃ | > 4 | d0:171 d1:171 d2:219? d3:197? d4:219? | 2 | d0:171 d1:171 d2:256 |
| MOD₆ | > 4 ? | d0:227 d1:227 d2:227? d3:227? **d4:235?** | [non couru — run arrêté] | — |
| DNF(8×3) | > 4 ? | d0:170 d1:170 d2:192? d3:210? d4:228? | [non couru] | — |

Le constant ne suffit plus ; aucun polynôme de degré ≤ 4 trouvé n'atteint
240 sur F₂ (meilleur : 235 à d = 4) — mais **sans certificat
d'optimalité** (« ? » partout au-delà de d = 1) : « adeg > 4 » n'est pas
prouvé, c'est le meilleur trouvé en 120 s. Le run s'est arrêté avant MOD₆
et DNF sur F₃ (fin de session).

### 2c. Run ciblé (`--focus-mod6`, ε = 1/16, tl = 600 s, 16 workers, borne symétrique injectée)

Lecture du certificat : pour une maximisation, `borne_sup` est la borne
supérieure PROUVÉE par CP-SAT sur l'accord maximal ; si elle est
strictement inférieure au seuil 240, aucun polynôme de degré ≤ d
n'atteint le seuil — **adeg > d est certifié** sans qu'il faille le
statut OPTIMAL (le script étiquetait à tort « NON CONCLU » ; logique
corrigée le 2026-09-12 ; réserve habituelle : borne du solveur, sans
certificat DRAT).

| cible | corps | d | borne symétrique | meilleur accord trouvé | borne sup prouvée | verdict |
|---|---|---|---|---|---|---|
| MOD₆ (29 uns/256 ; constant = 227) | F₂ | 2 | 227 | 227 | **234** (600 s, 16 workers) | **adeg_{F₂,1/16}(MOD₆) > 2 CERTIFIÉ** — un polynôme de degré 2 sur F₂ gagne au plus 7 points sur le constant |
| MOD₆ | F₂ | 3 | [en cours] | | | |
| MOD₆ | F₃ | 2 | [en cours] | | | |
| MOD₆ | F₃ | 3 | [en cours] | | | |
| PARITY (contrôle dur) | F₃ | 3 | [en cours] | | | |

Première cellule discriminante ÉTABLIE au sens corrigé (ε = 1/16) : à
n = 8 sur F₂, le degré 2 ne fait presque rien contre MOD₆ (avantage ≤
7/256 sur le constant, prouvé). Les autres cellules seront reportées à
la chute du run.

## 3. Ce que le témoin établit — et ce qu'il n'établit pas

- **Établi (n = 12, exact)** : les trois îles (PARITY/F₂, MOD₃/F₃,
  DNF/Fourier) et MOD₆ hors de toutes, par degré exact et masse de
  Fourier — réplication de Smolensky et LMN à échelle finie, conforme.
- **Non établi** : la version « degré approché » du mur MOD₆ à n = 8 —
  d'abord parce que la spécification de la candidature (ε = 1/8) est
  vide par déséquilibre, ensuite parce que la correction (ε = 1/16) n'a
  pas obtenu de certificat d'optimalité dans les budgets. La leçon
  d'instrument : **un seuil d'accord ε n'a de sens que si ε est inférieur
  au biais de la fonction** (ici 29/256 ≈ 0,113 : ε = 1/8 = 0,125 le
  dépasse) ; la mesure honnête est l'avantage sur le meilleur constant,
  ou une fonction équilibrée.
- **Pour l'entrée E-5**, rien ne dépend de cette cellule : l'élimination
  est par théorèmes (OS17, CIKK, Williams 2016) ; le témoin sert de
  régime de contrôle, et il est conforme là où il est exact.

## 4. Réserves

- Réplication déclarée (Smolensky, LMN) ; les tables à n = 8 et 12 sont
  des mesures.
- Le degré approché est une mesure asymptotique (Ω(√n)) sans avatar
  propre à n = 8 pour une fonction à 11 % de uns — même leçon d'échelle
  que PR-005/PR-007.
- Budgets : 120 s par palier (runs eps8/eps16), 600 s (run ciblé).
