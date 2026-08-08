# HOL-004 — Mesures : la grille seize-vertex et les premières épingles complexes

Tâche : HOL-004. Script : `checks/hol004_seize_vertex.py`. Date :
2026-08-08. Arithmétique exacte (entiers de Gauss ; K̃⁻¹ sans
normalisation ; exposants d'α mod 8 pour L). Cahier des charges :
HOL-003 (`bib/holant_arites_paires.md` §5).

## 1. LA PRISE (correction en cours de tâche, marquée)

Le premier passage du scan 0/1 rendait 48 962 « COIN » (74,7 %) —
**faux comme lecture de poche** : toute signature à valeurs réelles est
couverte par la dichotomie de Shao-Cai (FOCS 2020), donc HORS de la
poche ouverte par théorème, quel que soit son statut face aux tests
directs. Le taux anormal était l'alarme. Correction : zone
« Z-réel(Shao-Cai) » ajoutée à la grille (avant les tests directs) ;
les scans réels deviennent des CONTRÔLES. Leçon : la condition « non
réelle-transformable » de la synthèse HOL-003 commence par « non
réelle » — le coin vit dans le complexe.

## 2. Calibration et contrôles (grille corrigée)

| test | résultat |
|---|---|
| EQ₄ | Z2-symétrique ✓ |
| (x₁=x₂)(x₃≠x₄) | Z1-réductible ✓ |
| support affine {0,3,5,6} | Z1-réductible ✓ (= [x₄=0]⊗[⊕₃=0], correct) |
| indicatrice poids impairs | Z2-symétrique ✓ |
| **scan exhaustif 0/1 (65 536)** | Z-réel 62 906 + réductible 2 601 + symétrique 28 + nulle 1 = 65 536 — **ZÉRO COIN ✓** (4 s) |
| échantillon 0/±1 (4 000) | Z-réel 3 984 + réductible 16 — zéro COIN ✓ |

## 3. La chasse complexe

**Échantillon aléatoire {0, ±1, ±i} (8 000)** : COIN 7 707, T2-P 292,
réductible 1. Lecture : le générique complexe est hors des classes
directes — attendu ; la masse COIN porte la réserve de périmètre
(transformées non testées).

**Scan STRUCTURÉ exhaustif** — supports de taille 3, valeurs {1, i},
au moins un i (3 920 signatures) : réductible 2 464, **COIN 1 456**.
Épingles reproductibles (les premières par ordre lexicographique) :

```
supp = {0000, 0001, 1110}, i sur {0000}            (la première épingle)
supp = {0000, 0001, 1110}, i sur {0001} / {0000,0001} / {1110} / ...
supp = {0000, 0001, 1111}, i sur {0000} / ...
```

Vérifications portées par la grille pour chaque épingle : non nulle,
irréductible (minors 2×2 des 7 bipartitions), non symétrique, NON
réelle, zone K-mixte (ni huit-vertex ni HW≥/HW≤/single-weighted ni
vanishing), hors A directe (support affine + i^Q), hors P (produit),
hors M (parité + MGI d'arité 4 de FCST Lemma 2.24), hors L (16 tests
A-shiftés).

## 4. Ce que les épingles SONT et NE SONT PAS

SONT : les premières signatures d'arité 4 explicites du dépôt situées
hors de TOUTE classe tractable directe décidée et hors de TOUTE zone
fermée par théorème décidable sans transformation — des candidates
concrètes du coin « seize-vertex » de la poche toutes-arités-paires.
NE SONT PAS : des instances certifiées ouvertes — il reste à tester
les classes TRANSFORMÉES (A-/P-/L-/M-transformable, et la
réel-transformabilité T⁻¹f réelle, T ∈ GL₂) par balayage
O₂(ℂ)/Gröbner : HOL-005 candidate, sur la PREMIÈRE épingle d'abord.
Aucune #P-dureté n'est décidée par ce scan.

## 5. Compléments d'observation

- T3-M a détecté 64 signatures 0/1 au premier passage (avant
  l'absorption Z-réel) — la MGI d'arité 4 fonctionne ; T4-L : 0
  détection sur tous les scans (cohérent avec la délicatesse déclarée
  de L — supports type codes correcteurs).
- Convention M_Out/M_In de la MGI implémentée telle que citée (FCST) ;
  réserve de convention consignée (une calibration sur matchgate
  explicite reste à faire si M devient discriminant).
