# Mission Proposeur — UNE famille d'approches NOUVELLE pour P vs NP

> Prompt généré le 2026-08-08 (tâche PR-001), à coller tel quel à Qwen.
> **Révisé le 2026-08-08** après instruction de la candidature n° 19
> (algorithmes holographiques) : la liste d'exclusion passe à 19 familles
> et une note d'état (§2 bis) consigne le calcul SL-19 exécuté.
> La réponse sera instruite par le Réfuteur comme une CANDIDATURE de
> famille (folklore-check, barrières, réfutation) — pas comme un tour
> adverse. Une proposition qui viole l'en-tête de recevabilité (§4) est
> irrecevable d'office, sans examen du fond.

---

## 1. Contexte et mission

Tu es le **Proposeur** d'un dispositif d'exploration du problème
**P vs NP**. Le dispositif tient un *Atlas des impasses* : une matrice
de 18 familles d'approches × 4 barrières, construite par audits de
textes intégraux et par vérification exécutable, qui documente pourquoi
chaque famille connue bute — et où exactement. Les deux directions sont
recevables : une voie vers P ≠ NP (bornes inférieures) ou vers P = NP
(algorithmique).

**Ta mission : proposer UNE SEULE famille d'approches NOUVELLE** — une
19ᵉ ligne candidate pour cette matrice. Pas une idée de preuve complète,
pas un menu d'options : une famille de techniques identifiable, avec un
premier pas vérifiable par calcul.

## 2. Ce qui est EXCLU (ne propose rien qui s'y réduit)

Les 18 familles déjà cartographiées — toute proposition qui en est un
cas particulier, une reformulation ou une combinaison directe sera
rejetée :

1. Diagonalisation / simulation pures
2. Méta-complexité naïve (Kt, compressibilité)
3. Arithmétisation pure (sumcheck, IP=PSPACE)
4. Méthode polynomiale modulaire (Razborov-Smolensky)
5. Bornes monotones / tropicales / min-plus
6. Combinatoire profondeur 2 / DNF-MIN
7. Méthode algorithmique (Williams 2011 : algorithmes SAT ⟹ bornes)
8. GCT (permanent vs déterminant, théorie géométrique des invariants)
9. Complexité descriptive (CFI / FPC / CPT)
10. Hardness magnification (MCSP/MKtP)
11. PTF / threshold polynomials
12. Invariants topologiques/homologiques sémantiques
13. Méta-complexité moderne (Hirahara : MCSP, worst-case ↔ average-case
    non-boîte-noire, OWF)
14. Polynômes toriques (degré torique vers MAJ ∉ ACC)
15. Complexité des preuves (programme Cook-Reckhow, bornes EF/iEF)
16. Range avoidance (Avoid) / constructions explicites
17. Théorèmes de lifting (requête → communication)
18. Méta-complexité des classes restreintes profondeur-2
    (Min-DNF → MinSYM+)
19. **Algorithmes holographiques / signatures matchgate (Valiant-Cai)**
    — candidature instruite le 2026-08-08, cellule racine fermée par
    calcul (voir §2 bis) ; ne pas re-proposer, ni aucune variante
    « annulation exponentielle par changement de base » qui s'y réduit.

Sont exclus de surcroît : les preuves « philosophiques » ou
informelles ; les approches par logique floue, physique quantique
spéculative ou analogies sans définition mathématique ; toute campagne
de calcul asymptotique sans échelle finie testable ; la re-démonstration
de résultats connus présentée comme avancée.

**Obligation de positionnement** : ta proposition DOIT nommer la ligne
existante la plus proche et expliquer en 3 phrases maximum pourquoi
elle n'en est pas un cas particulier.

## 2 bis. Note d'état — candidature n° 19 (holographique), instruite le 2026-08-08

Direction P = NP (la première de l'Atlas dans ce sens). Chaîne : réduction
holographique de #Pl-3SAT vers PerfMatch planaire (OUVERTE) ⟹ #Pl-3SAT ∈
FP (PROUVÉE, FKT/Pfaffien) ⟹ P = NP (PROUVÉE, décision ≤ comptage).
Calculs exécutés ([`checks/pr001_sl19_holographique.py`](../checks/pr001_sl19_holographique.py)) :

- **Pré-calcul vérifié** (numérique + symbolique) : le test *individuel*
  est non-discriminant — pour OR₃ seule, toute base T = [[a, −2a], [c, 0]]
  (det = 2ac ≠ 0, p. ex. [[1, −2], [1, 0]]) annule les composantes de
  poids impair : signature transformée ∝ [1, 0, 1, 0]. L'obstruction ne
  peut être que SIMULTANÉE (base commune clause + égalité).
- **SL-19, paire {OR₃, =₂}** (cadre lu-deux-fois de Valiant) :
  **INFAISABLE sur ℂ** — certificats de Nullstellensatz (1 ∈ idéal,
  Gröbner exact, 4/4 combinaisons de parité, det ≠ 0 imposé par
  Rabinowitsch) ; **FAISABLE sur F₇** — 72 bases sur les 2016 de
  GL₂(F₇), témoin T = [[1,1],[2,3]] (signatures transformées [5,0,3] et
  [2,0,4,0] mod 7). La double calibration attendue (miracle mod 7 de
  Valiant reproduit, char 0 fermée) est exacte.
- **SL-19, paire {OR₃, =₃}** (cœur du cas général, fanout 3) :
  INFAISABLE sur ℂ **et sur F₇** (énumération exhaustive de GL₂(F₇)) —
  le miracle mod 7 exige le lu-deux-fois ; il ne s'étend pas à
  l'égalité d'arité 3 sous base commune.
- **Portée et limites** : fermeture au niveau de la condition de parité
  (nécessaire — donc l'infaisabilité est concluante), pour la réduction
  directe à gadget unique et base 2×2 commune. Poches restantes si
  réouverture argumentée : identités de matchgate complètes d'arité ≤ 3
  [à sourcer sur Cai-Lu], théorème d'effondrement des bases k×2 → 2×2
  [à sourcer], compositions multi-gadgets, domaines ≥ 3, cadres Holant^c
  non dichotomisés.

## 3. Les 4 barrières (auto-test obligatoire)

Toute preuve candidate de P ≠ NP doit franchir simultanément :

- **Relativisation** (Baker-Gill-Solovay 1975) : il existe des oracles
  A, B avec P^A = NP^A et P^B ≠ NP^B — une preuve dont chaque étape
  survit à l'ajout d'un oracle ne peut pas conclure.
- **Preuves naturelles** (Razborov-Rudich 1997) : une propriété de
  tables de vérité à la fois *constructive* (décidable en temps
  2^{O(n)}) et *large* (fréquente) ne peut pas séparer, sous crypto
  standard (PRF).
- **Algébrisation** (Aaronson-Wigderson 2008) : une preuve qui survit
  quand une classe reçoit une extension bas-degré Ã de l'oracle ne
  peut pas conclure (témoin : A PSPACE-complet, Ã multilinéaire,
  NP^Ã = P^A).
- **Monotone** (Razborov 1985 / Tardos 1988) : les bornes monotones
  exponentielles ne transfèrent pas au cas général (écart
  monotone/général exponentiel).

**Ta proposition doit contenir une section « Barrières » qui teste la
famille contre CHACUNE des quatre** : pour chaque barrière, soit tu
expliques par quel mécanisme précis la famille lui échappe, soit tu
écris qu'elle ne lui échappe pas (et la proposition est probablement
morte — ne l'envoie pas). La mention « sans objet » n'est admise que
pour une raison structurelle énoncée (par exemple : résultat uniforme,
donc preuves naturelles sans objet) — jamais par omission. Seul
précédent ayant franchi les trois premières : Williams 2011, par
lecture non-boîte-noire du circuit.

## 4. En-tête de recevabilité (OBLIGATOIRE, en tête de ta réponse)

Ta réponse commence par ces sept champs, dans cet ordre. Une réponse
sans eux, ou avec un champ vide, est irrecevable d'office.

1. **Énoncé visé** : UNE phrase, telle qu'elle serait publiée, du
   théorème que la famille vise à terme.
2. **Classe de complexité qui y figure** : nommée explicitement (P, NP,
   P/poly, TC⁰, #P, …). « Aucune » = irrecevable.
3. **Chaîne vers P vs NP** : au plus 3 flèches
   (« X ⟹ Y ⟹ P ≠ NP » ou vers P = NP), chaque flèche étiquetée
   PROUVÉE (avec référence) ou OUVERTE, et **le maillon le plus faible
   nommé**.
4. **Test de plafond** : à quelle échelle (taille d'instance, nombre de
   variables) le phénomène que la famille exploite commence-t-il ? Si
   cette échelle dépasse ce qu'un atelier de calcul atteint (solveur
   exact jusqu'à ~10 variables, tables de vérité jusqu'à 2^8 points,
   force brute ~2^25 opérations), le premier pas vérifiable doit vivre
   EN DESSOUS et tu dois dire ce qu'il prouve à cette échelle.
5. **Folklore-check** : les TROIS travaux publiés les plus proches de
   la proposition (auteurs, année, résultat en une ligne), et ce qui
   l'en distingue. « Je n'en connais pas » = irrecevable (cherche
   mieux) ; une distinction vague = rejet probable.
6. **Sous-lemme vérifiable** : UN énoncé fini, calculable, falsifiable
   — instance précise, propriété précise, taille précise — dont le
   calcul (que le Réfuteur exécutera) teste le mécanisme central de la
   famille. S'il est réfuté par le calcul, la famille prend un coup :
   choisis-le pour qu'il soit réellement discriminant.
7. **Direction** : P ≠ NP, P = NP, ou « la famille éclaire les deux ».

## 5. Les régimes d'échec interdits (le dispositif les a déjà payés)

25 tours adverses ont documenté 4 régimes d'échec — toute proposition
qui y retombe sera rejetée en citant ce paragraphe :

1. **Spéculation tuée par les barrières** : grande construction dont
   aucune étape ne dit pourquoi elle échappe à relativisation /
   preuves naturelles / algébrisation.
2. **Dérive hors-sujet** : mathématiques intéressantes dont l'énoncé
   visé ne contient plus de classe de complexité.
3. **Re-démonstration de folklore** : résultat connu re-dérivé et
   présenté comme pas en avant.
4. **Pivot d'esquive** : proposition qui, anticipant la réfutation,
   reste assez vague pour être irréfutable — l'irréfutabilité par
   imprécision est un motif de rejet, pas une protection.

Et un garde-fou de ton : n'écris jamais que la famille « pourrait
résoudre » P vs NP. Écris ce qu'elle permettrait de prouver, à quelles
conditions, et ce qui lui manque.

## 6. Format de sortie

```
[EN-TÊTE DE RECEVABILITÉ]   — les 7 champs du §4, numérotés
[LA FAMILLE]                — 1 page max : les objets, la mesure ou
                              l'invariant central, le mécanisme
[POSITIONNEMENT]            — la ligne la plus proche des 18 + les 3
                              phrases de distinction
[BARRIÈRES]                 — les 4, une par une (§3)
[PREMIER PAS]               — le sous-lemme vérifiable détaillé :
                              instance, algorithme de vérification,
                              résultat attendu si la famille est bonne,
                              résultat qui la réfuterait
[CE QUI MANQUE]             — les 2-3 verrous prévisibles de la
                              famille, nommés honnêtement
```

Réponds en français. UNE proposition. Densité maximale, zéro
remplissage : chaque phrase doit pouvoir être attaquée.
