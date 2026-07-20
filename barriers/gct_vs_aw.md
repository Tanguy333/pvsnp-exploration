# D-002 : GCT (Geometric Complexity Theory) × Algébrisation (AW)

> Tâche type D. Exécutée le 2026-06-09. Sources : audit A-008 (AW 2008,
> texte intégral), abstract Bürgisser-Ikenmeyer-Panova
> ([arXiv:1604.06431](https://arxiv.org/abs/1604.06431), J. AMS 2019,
> récupéré verbatim), cahier §7.4.

## 1. La barrière

AW 2008 (A-008) : toute technique dont la validité survit à l'accès aux
extensions bas-degré Ã des oracles ne peut séparer P de NP — témoin :
A PSPACE-complet, Ã multilinéaire, `NP^Ã = P^A`.

## 2. Comment GCT est censée la franchir

GCT (Mulmuley-Sohoni 2001) attaque permanent vs déterminant — équivalent à
VP_ws vs VNP (verbatim BIP) :

> « The permanent versus determinant conjecture is a major problem in
> complexity theory that is equivalent to the separation of the complexity
> classes VP_ws and VNP. »

Stratégie : comparer les **fermetures d'orbites** de det_n et du permanent
paddé sous GL_{n²}, et chercher des *obstructions de représentation*
(multiplicités dans les anneaux de coordonnées) distinguant les deux
variétés.

## 3. Verdict : **SANS OBJET STRUCTUREL pour AW (présumé), mais la voie principale est morte pour une raison INTERNE**

### 3a. Vis-à-vis d'AW : hors cadre, non démontré

GCT n'opère pas avec des oracles : elle exploite la **caractérisation par
symétries** du permanent et du déterminant (ces fonctions sont déterminées
par leurs groupes de stabilisateurs — propriété *spécifique*, le contraire
d'un argument boîte-noire). Un argument fondé sur les multiplicités de
représentations de l'orbit closure d'une fonction *explicite* n'a pas de
version « pour tout oracle Ã » : la barrière AW ne s'applique pas
mécaniquement.

**Mais** : ce non-assujettissement est *structurel/présumé*, pas démontré au
sens où Williams l'est (pas d'énoncé du type « il existe un oracle algébrique
contredisant la cible de GCT » publié — et pour cause, la cible VP vs VNP
n'est pas une classe booléenne à oracle). De plus, GCT vise permanent vs
déterminant, dont le lien à P vs NP passe par des ponts supplémentaires
(non-uniformité, GRH dans certaines versions) — franchir AW « pour VP vs
VNP » n'est pas franchir AW pour P vs NP.

### 3b. La vraie barrière de GCT est interne — BIP 2019, verbatim

> « [Les auteurs établissent que] l'approche proposée par Mulmuley et Sohoni
> (2001) utilisant les "occurrence obstructions" pour séparer les fermetures
> d'orbites du déterminant et du permanent paddé s'avère impossible. »

Avec la nuance exacte :

> « we do not rule out the general approach to the permanent versus
> determinant problem via multiplicity obstructions as proposed by Mulmuley
> and Sohoni. »

Donc : les obstructions par **occurrences** (multiplicité nulle d'un côté,
non-nulle de l'autre) n'existent pas ; les obstructions par **multiplicités**
(comparaison quantitative) restent formellement possibles mais aucune
technique pour les exhiber n'est connue — programme au point mort depuis
(cahier §4 q.5).

## 4. Ligne Atlas

| Cellule | Verdict |
|---|---|
| GCT × relativisation | sans objet structurel (pas d'oracle) — présumé franchi |
| GCT × RR | présumé franchi (les propriétés de représentation ne sont ni constructives au sens table-de-vérité ni larges) — non démontré |
| GCT × algébrisation | sans objet structurel — présumé franchi, non démontré |
| GCT × **barrière interne (BIP 2019)** | **FERMÉE pour les occurrence obstructions** ; multiplicity obstructions ouvertes sans technique connue |

Leçon de la ligne : échapper aux 3 barrières classiques ne suffit pas — GCT
les évite *par construction* et bute sur une impossibilité qui lui est
propre. Toute proposition future invoquant GCT doit se positionner par
rapport à BIP 2019, pas par rapport aux 3 barrières.

## Références de la cellule

A-008 (`bib/aaronson_wigderson_2008.md`), BIP 2019 (arXiv:1604.06431,
J. AMS 32(1):163-193), cahier §7.4, Tour 2 (algébrisation active).

> **Mise à jour 2026-07-20 (A-011)** : audit complet sur textes livré —
> voir `bib/gct.md` (Mulmuley §18 verbatim sur relativisation/RR, BIP
> texte intégral avec le mécanisme du padding, état 2019→2026 des
> multiplicity obstructions). Cette cellule reste valable pour l'axe AW
> spécifiquement ; les cellules relativisation et RR de la ligne 8 sont
> désormais documentées, plus seulement présumées.
