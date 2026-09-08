# PR-007 — Synthèse exacte à trois bases : le sous-lemme de la candidature n° 21 exécuté (réplication vérifiante déclarée)

Date : 2026-09-08. Instrument : `checks/pr007_synthese_exacte.py`
(pysat 1.8 / CaDiCaL 1.9.5, encodage KKY 2009 / Knuth 7.2.2.2,
implémentation indépendante de `checks/pr002_sre_parite.py`). Machine :
24 cœurs, un processus par run (CaDiCaL mono-thread).
Convention NOT-payant = celle de PR-002 : {AND, OR, NOT} fan-in ≤ 2,
entrées gratuites, CHAQUE porte (NOT compris) coûte 1, sortie = dernière
porte (constantes inutiles dans un circuit minimal d'une fonction non
constante — absorbables). U₂ = toutes portes binaires non dégénérées sauf
XOR/XNOR (négations absorbées) ; B₂ = les 10 portes binaires non
dégénérées.

## 0. Antériorité (déclarée avant tout calcul)

| Objet | Valeur publiée | Source |
|---|---|---|
| C_{U₂}(XOR_n) | 3(n − 1) | Schnorr 1974 (consigné PR-002) |
| C_{∧,∨,¬}(XOR_n), NOT comptés | 4n − 4 | Red'kin 1970/73 — verbatim via Kombarov, Vestnik MGU 2011 (réf. [4]) |
| Nombre minimal de NOT pour f | ⌈log₂(d(f) + 1)⌉ | Markov 1958 |
| max C_{B₂}(f), n = 4 | 7 | Knuth TAOCP 7.1.2 (texte non ouvert ; mesuré ici) |
| max C_{B₂}(f), n = 5 | 12 (une seule classe NPN) | Knuth, via Goucher 2019 (secondaire) |

Tout ce qui suit est donc réplication vérifiante ; le seul chiffre que
le dépôt ne possédait pas — la fermeture de sa réserve PR-002 — était
fermable par citation (Red'kin) et, plus simplement, borné à ≥ 11 par
Markov + Schnorr sans solveur.

## 1. Calibrations (foreground, toutes < 1 s sauf mention)

```
python -u checks/pr007_synthese_exacte.py markov
python -u checks/pr007_synthese_exacte.py counting
python -u checks/pr007_synthese_exacte.py xor --n {2,3} --base {U2,NOTPAY,B2}
```

| Mesure | Attendu | Mesuré |
|---|---|---|
| d(XOR_n), n = 2..6 | ⌊n/2⌋ | 1, 1, 2, 2, 3 ✓ → NOT ≥ 1, 1, 2, 2, 2 ; + Schnorr : C_NOT-payant(XOR_n) ≥ 4, 7, **11**, 14, 17 |
| C_{U₂}(XOR₂), C_{U₂}(XOR₃) | 3, 6 | 3, 6 ✓ (témoins re-vérifiés) |
| C_{NOT-payant}(XOR₂), (XOR₃) | 4, 8 | 4, 8 ✓ (= PR-002 ; témoin XOR₃ à 2 NOT + 6 binaires) |
| C_{B₂}(XOR₃), C_{B₂}(XOR₄) | 2, 3 | 2, 3 ✓ |

## 2. Seuil de comptage (mode `counting`)

Nombre de chaînes de s portes sur n entrées ≤ ∏_{i<s} C(n+i, 2)·10 ;
si Σ_{s'≤s} < 2^{2ⁿ}, une fonction exige > s portes. Plus grand s ainsi
forcé, s*(n), contre 3n :

| n | 4 | 5 | 6 | 7 | **8** | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|
| 3n | 12 | 15 | 18 | 21 | 24 | 27 | 30 | 33 | 36 |
| s*(n) | 2 | 4 | 7 | 13 | **24** | 43 | 78 | 141 | 256 |

**Dès n = 8, une fonction (non explicite) exige > 3n portes par simple
comptage.** Le « phénomène » dont la candidature constate l'absence à
n ≤ 5 n'est pas celui de la ligne : la ligne porte sur l'EXPLICITÉ, qui
n'a d'avatar à aucun petit n.

## 3. XOR₄, base U₂ (Schnorr : 9)

```
python -u checks/pr007_synthese_exacte.py xor --n 4 --base U2 --kmax 9
```
k = 1..6 UNSAT (< 3 s) ; k = 7 UNSAT (94,3 s) ; **k = 8 UNSAT (1 098,8 s) ;
k = 9 SAT (10,7 s), témoin re-vérifié sur 16 lignes — C_{U₂}(XOR₄) = 9 =
3(n − 1)** (Schnorr répliqué). Témoin : trois blocs de 3 portes
(g0..g2 = XNOR(x1, x3) ; g3..g5 = ⊕ x0 ; g6..g8 = ⊕ x2) :
```
g0 = ~a&b(x1, x3)  g1 = a&~b(x1, x3)  g2 = NOR(g0, g1)
g3 = ~a|b(x0, g2)  g4 = ~a&b(x0, g2)  g5 = a&~b(g3, g4)
g6 = NOR(x2, g5)   g7 = AND(x2, g5)   g8 = NOR(g6, g7)
```

## 4. XOR₄, base NOT-payant (Red'kin : 12 ; PR-002 : ∈ [10, 12])

| Run | Résultat | Durée | Statut de certificat |
|---|---|---|---|
| k = 10, symétries | **UNSAT** | 603 s | réplication du théorème (Markov + Schnorr ⟹ ≥ 11) |
| k = 11, exactement 2 NOT, symétries | **UNSAT** | 304 s | la SEULE configuration possible à 11 (b ≥ 9 par Schnorr, u ≥ 2 par Markov, b + u = 11 ⟹ (9, 2)) — donc **C = 12** modulo la validité des cassages de symétrie |
| k = 11, exactement 2 NOT, SANS symétries | **UNSAT** | 308 s | certificat sans cassage de symétrie (817 vars, 58 740 clauses) — **C = 12 par théorème + solveur, sans hypothèse de symétrie** |
| k = 11, sans restriction, symétries | NON CONCLU — arrêté par l'utilisateur le 2026-09-08 | > 3 h | redondant avec la ligne « 2 NOT, symétries » |
| k = 11, sans restriction, SANS symétries | NON CONCLU — arrêté par l'utilisateur le 2026-09-08 | > 3 h | redondant avec la ligne « 2 NOT, SANS symétries », qui est le certificat |
| k = 12 | **SAT**, témoin re-vérifié sur 16 lignes | 194 s | borne supérieure de Red'kin réalisée |

Témoin à 12 (3 NOT, 9 binaires — la structure en n − 1 = 3 blocs de
Kombarov 2011) :
```
g0 = AND(x0, x3)   g1 = OR(x0, x3)   g2 = AND(x1, x2)   g3 = OR(x1, x2)
g4 = NOT(g1)       g5 = OR(g0, g4)   g6 = NOT(g2)       g7 = AND(g3, g6)
g8 = AND(g5, g7)   g9 = OR(g5, g7)   g10 = NOT(g9)      g11 = OR(g8, g10)
```

**Bilan** : la réserve PR-002 (XOR₄ ∈ [10, 12]) est fermée — **XOR₄ = 12
en NOT-payant** — par théorème (Red'kin ; Markov + Schnorr pour ≥ 11)
et par solveur (10 UNSAT ; 11 UNSAT dans l'unique configuration
restante ; 12 SAT). Ce n'est pas une contribution : c'est 1958-1974.

## 5. Les 222 classes NPN de B4 sur B₂ (Knuth : max 7)

```
python -u checks/pr007_synthese_exacte.py b4_all
```
Classes : 222 (assertion) ; Σ tailles = 65 536 (assertion) ; 3,8 s pour
la classification ; synthèse des 222 classes en 1 115 s, **0 classe non
conclue**.

| Coût C | 0 | 1 | 2 | 3 | 4 | 5 | 6 | **7** |
|---|---|---|---|---|---|---|---|---|
| classes NPN | 2 | 2 | 5 | 20 | 34 | 75 | 72 | **12** |
| fonctions (sur 65 536) | 10 | 60 | 456 | 2 474 | 10 624 | 24 184 | 25 008 | **2 720** |

**MAXIMUM = 7** (Knuth 7.1.2 : 7). Les 12 classes de coût 7 : 0x0116,
0x0117, 0x066b, 0x0779, 0x166a, 0x1681, 0x168b, 0x168e, 0x1698, 0x169b,
0x16ac, 0x179a (tailles 32 à 384). L'histogramme par fonctions coïncide
nombre pour nombre avec la table de Knuth (7.1.2) telle que le Réfuteur
la mémorise (10, 60, 456, 2 474, 10 624, 24 184, 25 008, 2 720) — texte
non ouvert : concordance à confirmer à l'audit ; mais la coïncidence de
huit entiers sommant à 65 536 vaut validation forte de l'instrument ET
des cassages de symétrie (aucun faux UNSAT possible sans casser au
moins un de ces comptes).

## 6. Réserves

- UNSAT solveur sans certificat DRAT (réserve habituelle du dépôt) ; les
  cassages de symétrie (porte non finale lue ; pas de doublon ; ordre
  lexicographique des portes consécutives indépendantes) sont validés
  empiriquement par la reproduction de toutes les valeurs connues (§1,
  §3, §4, §5) et contre-éprouvés par les runs `--nosym`.
- Le « 7 » de Knuth est mesuré, pas lu (texte non ouvert) ; le « 12 »
  à n = 5 est de seconde main (Goucher 2019).
- Red'kin : référence primaire et date exactes à fixer à l'audit
  (1970 selon Kombarov [4] ; 1973 pour « Proof of minimality… »).
