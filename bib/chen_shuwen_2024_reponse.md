# Antériorité primaire — Chen Shuwen (réponse directe, 2026-06-12)

Source : email de Chen Shuwen à Tanguy (data primaire, autoritaire — Chen
est la référence mondiale des recherches PTE par ordinateur). À traiter
comme borne d'antériorité de plus haute fiabilité.

## Recherches exhaustives de solutions IDÉALES NON SYMÉTRIQUES (avant 2024)

| Problème | Taille | Recherche complète jusqu'à | Résultat |
|---|---|---|---|
| PTE7 | 8 | hauteur 570 | non-sym TROUVÉES (listées p.229 de son papier) |
| PTE8 | 9 | hauteur 592 | AUCUNE non-sym (2 sym connues seulement) |
| PTE9 | 10 | hauteur 530 | AUCUNE non-sym |
| PTE10 | **11** | hauteur **1600** | **AUCUNE non-sym** (p.52) |
| PTE11 | 12 | hauteur 500 | AUCUNE non-sym |

La méthode est exhaustive par conception (couvre sym ET non-sym). Plus :
thèses de 3 étudiants chinois (réfs [116], [34], [147], p.164) — recherches
exhaustives non-sym jusqu'à PTE11, toutes DANS les bornes de Chen.

## RECALIBRATION HONNÊTE de nos cadrages (≈22e auto-correction)

1. **Notre « idéale taille 8 non symétrique de span 96 » (V-043, n_asym(7))
   N'EST PAS neuve** : les non-sym de taille 8 sont listées p.229 de Chen,
   recherche complète jusqu'à 570 (notre span 96 ≪ 570). Notre flag de
   l'époque (« comparaison littérature à faire avant toute revendication »)
   est résolu : CONNU. Seul reste éventuellement nôtre l'angle « span
   minimal exact via réseau » — à ne PAS revendiquer sans vérifier p.229.

2. **La « chasse au 1er minimum asymétrique de d = 8 (= 1re idéale taille 9
   non sym.) » que nous envisagions est FERMÉE** : Chen prouve qu'AUCUNE
   idéale taille 9 non sym. n'existe ≤ 592. Cible abandonnée (gain : calcul
   épargné). NB : nos minima asymétriques de réseau à d ≤ 7 (V-042) sont des
   vecteurs courts NON idéaux — objet distinct de ceux de Chen ; pas de
   contradiction, mais ne pas confondre « minimum asym. de réseau » et
   « idéale non sym. ».

3. **Le fantôme taille 11 est encadré bien plus largement que par nous** :
   non-sym ≤ 1600 (Chen) + sym ≤ 3500 (CMSV). Notre certificat réseau
   (span ≤ 146) reste COMPLÉMENTAIRE mais sur un AUTRE objet (plus court
   vecteur du réseau KV, incluant les vecteurs DÉFECTUEUX type un seul ±2,
   que la recherche d'idéales de Chen ne couvre pas) et borné par SPAN, pas
   par hauteur. Pour la question « idéale taille 11 existe-t-elle », Chen +
   CMSV dominent ; pour la question KV/Conjecture 5 (minimum du réseau),
   notre objet est le bon.

## CORROBORATION (le côté positif)

Chen confirme indépendamment, par recherche exhaustive autoritaire, que les
idéales sont SYMÉTRIQUES pour les tailles 9-12 dans de larges plages — ce
qui soutient fortement notre loi de symétrie (V-042) DANS LE CAS IDÉAL.
La frontière « non-sym connues seulement taille ≤ 8 » = exactement notre
« zéro minimum asymétrique à d ≥ 8 » (régime idéal).

## Action

- Ne plus présenter le span-96 ni la chasse d=8→taille-9 comme du neuf.
- Notre contribution unique reste : certificat INCONDITIONNEL par réseau
  (toutes formes, vecteurs défectueux compris, par span) pour la question
  KV ; carte de phase ; cœurs ; seuil de découplage. PAS la découverte
  d'idéales (terrain de Chen, verrouillé).
