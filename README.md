# P vs NP — Atlas des impasses

> **Mission (depuis le 2026-08-07).** Explorer le problème **P vs NP** à
> travers différentes voies pour obtenir une avancée significative — dans
> l'objectif d'un début de preuve ou d'une preuve de P = NP ou de P ≠ NP.
> L'instrument central est un **atlas d'élimination** : explorer les voies,
> éliminer celles qui meurent (preuves, contre-exemples exécutables, audits
> sur textes — 27 tours de réfutation adverse archivés), pour faire émerger
> la bonne voie de résolution.
>
> **Cadrage honnête, inchangé.** Le problème est ouvert depuis 1971 ; ce
> dépôt ne prétend pas l'avoir résolu ni être près de le faire. Aucune
> avancée n'y est revendiquée sans vérification exécutable, folklore-check
> écrit et confrontation aux barrières — l'ambition est un cap, pas une
> revendication.

### Ce que ce dépôt a établi (bilan au 2026-07-25)

Une chose fermée : **la Conjecture 5 de Krishan-Vishwanathan est fausse** —
mécanisme de parité prouvé, énumération exhaustive par cellule, confirmée par
écrit par un des auteurs. Cela ferme **un ingrédient** d'une route vers
MAJ ∉ ACC, pas MAJ ∉ ACC. **Vingt-deux audits sur textes intégraux**, avec le
marqueur `[NON TROUVÉ]` là où la pièce manque — c'est le format où ce dépôt rend
le plus. **Quatre instruments exacts certifiés**, dont on publie le plafond :
n ≤ 7-8 pour le torique et le CVP, n = 10 pour le CP-SAT. Et **un négatif de
dispositif**, rencontré deux fois par deux chemins indépendants et chiffré :
l'écart entre ce que l'atelier mesure et l'échelle où le phénomène commence
(n ≤ 8 contre n ≈ 4050 ; O(n²) contre 2^{polylog n}) —
[`atlas/echelle_instrument.md`](atlas/echelle_instrument.md). Le reste — 169
tâches, 188 scripts, 27 tours — est du coût, et il est présenté comme tel.
**Au 2026-07-25, rien ici n'avait fait progresser une preuve de P ≠ NP** — ce
bilan est daté et reste exact ; depuis le 2026-08-07 la mission vise
explicitement l'avancée (voir l'en-tête), et ce bilan est la ligne de départ
que toute revendication future devra battre, pièces à l'appui. La table des
erreurs du dépôt (36 auto-corrections, dont une revendication asymptotique
fausse interceptée avant envoi à un auteur du domaine) fait partie du
livrable au même titre que les résultats.

## Le problème

Tout problème dont une solution candidate est vérifiable en temps polynomial
(classe NP) est-il aussi *résoluble* en temps polynomial (classe P) ? C'est
l'un des sept problèmes du prix du millénaire, ouvert depuis 1971. Aucune
preuve valide n'existe à ce jour — et ce dépôt documente, pièce par pièce,
pourquoi les grandes familles d'attaques connues ne peuvent pas la donner.

## Le livrable central : la matrice barrières × approches

**[`atlas/matrice_barrieres.md`](atlas/matrice_barrieres.md)** — 20 familles
d'approches (de la diagonalisation à GCT, de la méthode polynomiale modulaire
à la hardness magnification, la méta-complexité moderne, les polynômes
toriques, la complexité des preuves, le range avoidance, le lifting, la
méta-complexité des classes profondeur-2 — la ligne 18 —, les algorithmes
holographiques de Valiant-Cai — la ligne 19, première ligne en direction
P = NP — et la recherche totale structurée TFNP — la ligne 20, la chaîne
la plus courte de la matrice) croisées avec les 4 barrières connues
(relativisation, preuves naturelles, algébrisation, monotone) plus une
colonne « **verrou réel** » : ce qui bloque effectivement chaque approche
aujourd'hui. Les cellules renvoient à leur pièce justificative — audit `bib/`
ou fiche `tasks/done/` ; le câblage vers les scripts est en cours dans
[`atlas/temoins.md`](atlas/temoins.md).

**Portée des mesures** — [`atlas/echelle_instrument.md`](atlas/echelle_instrument.md).
Les instruments de ce dépôt ont un plafond chiffré (n ≤ 7-8 pour le torique et
le CVP, n = 10 pour le CP-SAT), et plusieurs fronts de la matrice ont une
échelle caractéristique très supérieure. Le dépôt a payé cet écart deux fois,
par deux chemins indépendants, avant de l'écrire.

Les trois enseignements de la matrice :

1. **Une seule ligne franchit les 4 barrières** : la méthode algorithmique de
   Williams (NEXP ⊄ ACC⁰, 2011) — et son verrou d'extension est précis
   (aucun algorithme SAT non-trivial au-delà d'ACC⁰).
2. **Les barrières classiques ne sont plus le front** : chaque programme
   vivant a réglé son rapport aux 3 barrières *par construction*, et bute
   sur une **barrière interne propre** (modules composés depuis 1987,
   BIP 2019 pour GCT, localité 2020 pour la magnification…).
3. Toute stratégie assez précise pour être exécutable engendre l'analyse de
   sa propre impossibilité.

## Les pièces

```
.
├── README.md                  ← ce fichier
├── CLAUDE.md                  ← règles de l'agent (mode tâches + anti-esquive)
├── cahier_de_bord.md          ← journal : pistes, lemmes, questions, registre satellite (§2 ter)
├── atlas/
│   ├── matrice_barrieres.md   ← LE livrable : matrice barrières × approches (15 lignes)
│   ├── temoins.md             ← cellule → script → commande → sortie → durée
│   └── echelle_instrument.md  ← note de dispositif : le plafond de l'atelier
├── bib/                       ← 22 audits bibliographiques sur textes intégraux
│   ├── bgs_1975.md            ← relativisation (les 2 oracles, preuves)
│   ├── razborov_rudich_1997.md← preuves naturelles (définitions verbatim)
│   ├── aaronson_wigderson_2008.md ← algébrisation (définition asymétrique exacte)
│   ├── tardos_1988.md         ← barrière monotone (mécanisme θ̄ + GLS)
│   ├── razborov_smolensky_1987.md ← méthode polynomiale modulaire
│   ├── beigel_tarui_1994.md   ← transformation SYM+ (cœur de Williams)
│   ├── williams_2011.md       ← le seul franchissement des 3 barrières
│   ├── cfi_abd.md             ← CFI, FPC ⊊ P, CSP affines
│   └── l18_status.md          ← le seul objet non recensé du dépôt
├── barriers/                  ← 4 cellules détaillées (approche × barrière)
├── tours/                     ← archives des 27 tours adverses (idée + réfutation)
├── checks/                    ← 188 scripts de vérification exécutables
├── data/                      ← 12 jeux de mesures (weight L1 des PTF sur TC⁰ d=2…)
├── notes/                     ← synthèses et brouillons (dont satellites, cf. cahier §2 ter)
├── roadmap/                   ← ARCHIVE 2026-05-23, pas le programme du dépôt
└── tasks/                     ← backlog (169 faites), hors_cible/, failed/
```

*(Les chiffres ci-dessus sont des comptes réels au 2026-07-25, pas des
estimations — le README précédent en annonçait 12, 9, ~30 et 25.)*

## Comment ce dépôt a été construit

**Phase adverse (Tours 1-25).** Deux LLM en rôles adverses : un *Proposeur*
génère une idée, un *Réfuteur* la démolit — avec obligation de contre-exemple
exécutable quand c'est calculable. Résultat : 25 archives de réfutation, et
un diagnostic net de **4 régimes d'échec** des LLM sur ce problème
(spéculation tuée par les barrières, dérive hors-sujet, re-démonstration de
folklore, pivot d'esquive).

**Phase atlas (depuis 2026-06).** La boucle adverse est suspendue, remplacée
par des **tâches atomiques anti-esquive** (CLAUDE.md §8) : audits de papiers
sur texte intégral, mesures ILP, cellules de matrice — chaque tâche avec
output spécifié à l'avance, échec honnête autorisé, invention interdite.
Deux tours adverses ont été rouverts (26 et 27) sur une cible née de l'Atlas ;
le fil qui en est issu a été **clos le 2026-07-25**, et la boucle re-suspendue.

**Recentrage (2026-07-25).** Un audit interne a mesuré que **160 des 169
tâches livrées n'avaient jamais touché le livrable** : le travail était absorbé
par le journal, pas par l'Atlas. Diagnostic : les six règles anti-esquive
régulaient toutes la *forme* d'une tâche, **aucune ne régulait sa direction**.
Quatre règles ont été ajoutées (CLAUDE.md §8, règles 7 à 10) : rattachement
obligatoire à une cellule nommée et **relu à la clôture**, test de plafond
(« à quelle échelle le phénomène commence-t-il, est-elle sous mon plafond ? »),
bilan par fil défini par sa *cible*, et obligation que tout recadrage s'écrive
dans les règles elles-mêmes. Le régime d'échec n°5 est ainsi documenté :
**une dérive lente que la rigueur locale ne détecte pas** — chaque tâche
irréprochable, la trajectoire hors sujet.

## Acquis vérifiables (et leur statut honnête)

- **9 mini-théorèmes de combinatoire booléenne** (profondeur 2) prouvés et
  vérifiés par calcul — dont l'audit bibliographique a établi que 8 sont du
  folklore (Quine 1952 → Hellerstein-Kletenik 2011). Le 9e,
  `DNF_min(IP_{2n}) = (3^n−1)/2`, est **non recensé après deux campagnes de
  recherche** ([`bib/l18_status.md`](bib/l18_status.md)) et fait l'objet d'un
  brouillon de note ([`notes/dnf_min_ip.md`](notes/dnf_min_ip.md)).
- **Une mesure neuve** ([`tasks/done/F-001.md`](tasks/done/F-001.md)) : la
  weight L1 des représentations PTF sur TC⁰ d=2 — EXACT_k est poly-weight
  (O(n²), structurel), IP est exponentielle (20 → 119 → 640) ; la sous-classe
  poly-weight ne couvre pas TC⁰ d=2, quantification de l'obstacle à
  l'extension de Williams.
- **Une observation ouverte** : `min_D W(IP_{2k}) = (3^k−1)/2 = DNF_min(IP)`
  aux 3 points mesurés — la constante 3^{n/2} gouverne la profondeur 2 d'IP
  dans trois modèles distincts (DNF, 2-CNF, PTF).

## Réouverture de la boucle adverse

Un Tour 26+ ne peut être ouvert que sur un **sous-lemme vérifiable** de
l'une des 5 zones génératrices identifiées en fin d'Atlas (extension TC⁰,
modules composés, technique non-localisante, borne CPT, multiplicity
obstructions) — pas sur une « grande idée ». L'Atlas est le générateur de
cibles, pas l'imagination du modèle.

## Avertissement

Ce projet est un exercice de méthode : faire produire à des LLM de la
compréhension *vérifiable* sur un problème qui les dépasse (et qui dépasse
tout le monde depuis 1971). Les preuves internes ont été auditées par boucle
adverse et vérification exécutable, pas par des referees humains. Ne citez
aucun contenu de ce dépôt comme résultat établi sans vérification
indépendante — y compris l'Atlas, dont chaque cellule indique précisément
sur quoi elle repose.
