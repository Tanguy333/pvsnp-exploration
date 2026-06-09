# P vs NP — Atlas des impasses

> **Cadrage honnête.** Ce dépôt n'est **pas** une prétention à résoudre P vs NP.
> C'est une exploration assistée par IA dont le livrable est un **atlas
> documenté de pourquoi chaque famille d'approches échoue** — adossé à des
> audits sur textes, des contre-exemples exécutables, et 25 tours de
> réfutation adverse archivés. La valeur recherchée est la compréhension
> accumulée et vérifiable, pas une preuve.

## Le problème

Tout problème dont une solution candidate est vérifiable en temps polynomial
(classe NP) est-il aussi *résoluble* en temps polynomial (classe P) ? C'est
l'un des sept problèmes du prix du millénaire, ouvert depuis 1971. Aucune
preuve valide n'existe à ce jour — et ce dépôt documente, pièce par pièce,
pourquoi les grandes familles d'attaques connues ne peuvent pas la donner.

## Le livrable central : la matrice barrières × approches

**[`atlas/matrice_barrieres.md`](atlas/matrice_barrieres.md)** — 12 familles
d'approches (de la diagonalisation à GCT, de la méthode polynomiale modulaire
à la hardness magnification) croisées avec les 4 barrières connues
(relativisation, preuves naturelles, algébrisation, monotone) plus une
colonne « **verrou réel** » : ce qui bloque effectivement chaque approche
aujourd'hui. Chaque cellule renvoie à sa pièce justificative dans le dépôt.

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
├── cahier_de_bord.md          ← journal central : 25 pistes, lemmes, 16 questions, bibliographie
├── atlas/
│   └── matrice_barrieres.md   ← LE livrable : matrice barrières × approches
├── bib/                       ← 9 audits bibliographiques sur textes intégraux
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
├── tours/                     ← archives des 25 tours adverses (idée + réfutation)
├── checks/                    ← ~30 scripts de vérification exécutables
├── data/                      ← mesures (weight L1 des PTF sur TC⁰ d=2…)
├── notes/                     ← brouillon de note (DNF_min(IP) = (3^n−1)/2)
└── tasks/                     ← backlog, tâches faites/échouées
```

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
