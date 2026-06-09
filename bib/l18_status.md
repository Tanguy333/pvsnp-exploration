# L18-STATUS : statut bibliographique de `DNF_min(IP_{2n}) = (3^n − 1)/2`

- **Tâche** : type A (audit bibliographique), Phase 1 du backlog.
- **Exécutée le** : 2026-06-09.
- **Objet audité** : L18 (Tours 17-18 du dépôt) — *la taille minimale d'un DNF
  calculant `IP_{2n}(x, y) = Σ x_i y_i mod 2` est exactement `(3^n − 1)/2`*,
  prouvé dans le dépôt par récurrence sur la classification des implicants
  premiers (A1/A2a/A2b), vérifié par ILP à n = 1..4.
- **Question** : ce résultat est-il déjà publié ?

## VERDICT : **NON RECENSÉ après recherche étendue** (avec réserves listées)

L'énoncé exact `DNF_min(IP_{2n}) = (3^n − 1)/2` n'a été trouvé dans **aucune**
des sources consultées ci-dessous. C'est le seul des 9 objets ÉTABLIS du dépôt
dont le statut reste « non recensé » après deux campagnes de recherche (audit
de mai 2026 + la présente). L18 est **candidat à une note courte** (arXiv
math.CO/cs.CC), sous les réserves de la section « Limites de la recherche ».

## Sources consultées (cette campagne)

### 1. Lignée moderne « depth-3 circuits for IP » (2021-2026) — formule absente

| Source | Ce qu'elle contient | DNF_min(IP) ? |
|---|---|---|
| Golovnev, Kulikov, Williams, *Circuit Depth Reductions* (ITCS 2021, [arXiv:1811.04828](https://arxiv.org/abs/1811.04828)) | A initié l'étude de la complexité Σ³ₖ de IP | Non |
| Frankl, Gryaznov, Talebanfard, *A Variant of the VC-dimension with Applications to Depth-3 Circuits* (ITCS 2022, [arXiv:2111.09671](https://arxiv.org/abs/2111.09671)) — **texte intégral greppé** | **Le plus proche parent trouvé** : « any 2-CNF consistent with the IP on n variables accepts at most 3^{n/2} assignments and this is tight » + unicité de la 2-CNF optimale. Le comptage 3^{n/2} y apparaît, côté *CNF-consistance* (ingrédient de borne Σ²₃), pas comme taille DNF minimale | Non |
| Göös, Guan, Mosnoi, *Depth-3 Circuits for Inner Product* (MFCS 2023 ; Information & Computation 2024) — **texte intégral greppé** | Σ²₃-complexité de IP : α ∈ [0.847, 0.965], LP de couverture | Non — la profondeur 2 n'y est pas formulée |
| Amano (ISAAC 2023) ; Gurumukhani et al., *Optimal Depth-Three Circuits for Inner Product* ([arXiv:2601.04446](https://arxiv.org/abs/2601.04446)) — **interrogé via fetch** | Bornes améliorées profondeur 3 | Non — « the paper contains no prior work specifically on DNF complexity for Inner Product » |

### 2. DNF de parités (modèle voisin, ≠ DNF pur)

- Cohen, Shinkar, *The Complexity of DNF of Parities* (ITCS 2016,
  [doi:10.1145/2840728.2840734](https://dl.acm.org/doi/10.1145/2840728.2840734)) :
  complexité DNF∘⊕ de IP ≈ 2^{n/2}. **Modèle différent** (les entrées des ANDs
  sont des parités, pas des littéraux). Ne couvre pas L18.

### 3. Compendiums — formule absente

- Jukna, *Boolean Function Complexity* (Springer 2012, draft V7, **587 pages
  greppées en texte intégral**) : IP apparaît 14+ fois (communication, signum
  rank, Σ⊕₃ top fan-in Ω(2^{m/2}), seuil profondeur 2-3, gip multipartite) —
  **jamais sa taille DNF pure**.
- Crama, Hammer (eds.), *Boolean Functions* (CUP 2011), ch. 3 Hammer-Kogan :
  déjà consulté à l'audit de mai 2026 — couvre L13/L19/L20, pas L18.

### 4. Théorie de la commutation (école Sasao-Butler) — méthode voisine, formule absente

- Sasao, Butler, *Worst and Best Irredundant Sum-of-Products Expressions*
  (IEEE Trans. Computers 50(9), 2001 — **texte intégral greppé** via
  [calhoun.nps.edu](https://calhoun.nps.edu/server/api/core/bitstreams/696fde2b-58bc-40dd-a268-4f6a737e9484/content)) :
  contient `MSOP(EXOR_n) = 2^{n-1}` (= notre L12, re-confirmé folklore),
  WSOP/MSOP, conjecture de Meo, contre-exemple de Yablonskii 1962. **Pas IP.**
- Sasao, Butler, *A Fast Method to Derive Minimum SOPs for Decomposable
  Functions* : MSOP par bi-décomposition AND + fonctions « orthodox ». La
  *méthode* (diviser pour régner sur bi-décompositions disjointes) est l'esprit
  exact de la récurrence du Tour 18 — mais le cas EXOR-bi-décomposition avec
  formule close pour IP n'a pas pu être consulté (accès ResearchGate refusé).
- Butler, Sasao, *Logic Functions for Cryptography — A Tutorial* (DTIC
  ADA548052) : la jonction bent/SOP existe comme sujet — **accès refusé (403)**,
  non vérifié.

### 5. Autres

- Sergeev, *DNF complexity of complete boolean functions*
  ([arXiv:1501.01331](https://arxiv.org/abs/1501.01331)) : fonctions complètes,
  pas IP.
- Recherches directes « prime implicants + bent function », « minimum SOP +
  bent + 3^{n/2} » : aucune occurrence de la formule.

## Observation transverse (pour l'Atlas)

La constante `3^{n/2}` gouverne la combinatoire profondeur-2 de IP dans **trois
modèles distincts** :
1. **DNF pur** : `DNF_min(IP_{2n}) = (3^n − 1)/2` (notre L18, non recensé).
2. **2-CNF consistantes** : max 3^{n/2} affectations satisfaisantes, tight,
   optimum unique (Frankl-Gryaznov-Talebanfard 2022).
3. **Weight L1 de PTF à degré libre** : `min_D W(IP_{2k}, D) = (3^k − 1)/2`
   aux 3 points mesurés (tâche F-001, observation conjecturale).

La coïncidence exacte entre (1) et (3) — la weight PTF minimale égale le nombre
de monômes du DNF minimal — est la tâche candidate F-002 du backlog.

## Limites de la recherche (réserves honnêtes)

1. **École russe (Yablonskii et coll., années 1960-70)** : la théorie des DNF
   minimales y a été développée en profondeur, en russe, mal indexée par les
   moteurs actuels. Le résultat pourrait y figurer. Non vérifiable d'ici.
2. **Sasao-Butler inaccessibles** : 2 sources pertinentes (Fast Method ;
   tutoriel cryptographie) n'ont pas pu être lues (403). La probabilité que la
   formule exacte y figure n'est pas nulle — la bi-décomposition EXOR de IP est
   exactement leur objet.
3. Absence de preuve d'absence : « non recensé » ≠ « nouveau ».

## Recommandation

1. **Mettre à jour le cahier §3 (audit bibliographique)** : L17/L18 passent de
   « statut incertain » à « **non recensé après recherche étendue
   (2 campagnes, 10+ sources, 2 livres greppés)** ».
2. **Si rédaction d'une note courte** : vérifier d'abord les 2 sources
   Sasao-Butler inaccessibles (bibliothèque, contact direct, ou autre miroir),
   et signaler la réserve école russe dans la note elle-même.
3. La note éventuelle gagnerait à inclure l'observation transverse 3^{n/2}
   (3 modèles) et le lien avec FGT22, ce qui la rattacherait à la littérature
   active depth-3.
