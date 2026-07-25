# L'écart entre l'instrument et le phénomène — note de dispositif

> **Statut, à lire avant le reste.** Ceci **n'est pas une barrière** au sens de
> Baker-Gill-Solovay, Razborov-Rudich ou Aaronson-Wigderson : cela ne dit rien
> sur ce qui est *démontrable*. C'est une contrainte de **dispositif** — cela
> dit ce qu'un atelier de vérification exécutable peut *observer*. Ce n'est pas
> non plus une lecture de la matrice : les trois lectures portent sur des
> familles d'approches, celle-ci porte sur l'atelier. Elle est consignée ici
> parce qu'elle explique et **prédit** le régime d'échec le plus coûteux du
> dépôt, et parce que le dépôt l'a rencontrée **deux fois, par deux chemins
> entièrement indépendants**, sans la reconnaître ni la première ni la seconde
> fois.
>
> **Antériorité : non recherchée.** Aucune revendication de nouveauté ou de
> primauté n'est faite ici. La littérature 2024-2026 sur les limites des
> assistants LLM en découverte mathématique et sur les échelles d'instrument
> SAT/ILP n'a pas été auditée. Gabarit du dépôt appliqué
> ([`../notes/symand_synthese.md`](../notes/symand_synthese.md) §7) : ce constat
> **semble** propre au dispositif, **sans garantie**.

## Énoncé

*Un dispositif de vérification exécutable ne peut départager que des phénomènes
dont l'échelle caractéristique est inférieure à son plafond. Les fronts vivants
de la complexité ont des échelles caractéristiques qui excèdent de deux à dix
ordres de grandeur le plafond d'un solveur exact sur ~10 variables. Sur ces
fronts, l'instrument ne produit ni témoin positif ni réfutation : il produit des
mesures exactes dans un régime où le phénomène visé est absent. Ces mesures sont
vraies, elles ne sont pas fausses — elles sont hors sujet, et rien dans leur
forme ne le signale.*

## Témoin 1 — la route torique (ligne 14), voie ATLAS-006, 2026-07-23

| Grandeur | Valeur |
|---|---|
| Phénomène visé | la séparation prouvée symétrique / asymétrique du degré torique (le gain Δ_w de Krishan-Vishwanathan) |
| Échelle du phénomène | borne symétrique **vide pour tout n ≤ 40** (pigeonhole n^{(d+1)²} < 2^{⌈n/2⌉+1}, leur Lemme 3.7) ; **premier contenu à n = 41** ; **croisement prouvé sym/asym à n ≈ 4050** |
| Plafond de l'instrument | MILP torique exact certifié à **n ≤ 7** (ATLAS-003) ; contrôle positif à **n ≤ 7** (ATLAS-005) ; CVP du fil AS à **n ≤ 8** |
| Écart | **~500× en n**. Le no man's land 8 ≤ n ≤ ~4000 n'est couvert **ni par la preuve ni par la mesure** |
| Coût payé avant de le savoir | **97 tâches** (54 fil V + 43 fil AS), 77 scripts. Le verdict a été obtenu en **une tâche de lecture, zéro calcul** |
| Signature diagnostique | **ATLAS-005, le contrôle positif** : le gain Δ_w *démontré* par KV est lui aussi **invisible à n ≤ 7**. Un instrument qui ne voit pas un effet prouvé ne prouve rien par ses négatifs — les égalités MAJ à n ≤ 7 ne discriminaient rien |

Pièces : [`../tasks/done/ATLAS-006.md`](../tasks/done/ATLAS-006.md),
[`../tasks/done/ATLAS-005.md`](../tasks/done/ATLAS-005.md),
[`../bib/kv_asym_extraction.md`](../bib/kv_asym_extraction.md),
`../checks/svp_turbo.py`.

## Témoin 2 — la route SYM∘AND (ligne 7), voie Tour 26 §5, 2026-07-24

| Grandeur | Valeur |
|---|---|
| Phénomène visé | le seuil de la transformation de Beigel-Tarui : ACC⁰ ⊆ SYM∘AND de taille **2^{(log S)^{O(1)}}**. Un témoin utile doit **dépasser** 2^{polylog n} |
| Échelle du phénomène à n = 100 | 2^{(log₂ 100)²} ≈ **1,9 × 10¹³** |
| Échelle de la famille mesurée | **W(SYM_k(g^k)) = O_g(k²)** (U26.1) — soit **n²/4 + n/2 = 2 550** à n = 100 |
| Écart | **~10 ordres de grandeur** à n = 100. La famille est plafonnée polynomialement **pour toujours** : aucune valeur exacte de W, à aucun k, ne peut témoigner du verrou |
| Plafond de l'instrument | W(MAJ₅(OR2⁵)) = 30 fermé sur l'espace entier à **n = 10**, en **3 h 20** de CP-SAT (11 barreaux UNSAT, 58 s → 3 517 s) ; le point k = 9 en sous-classe décomposable a demandé **15 884 s** |
| Coût payé avant de le savoir | **7 tâches, ~6 h de solveur, 4 commits, 0 cellule** — dépensés **après** que l'archive du Tour 26 §5 eut écrit elle-même : « toute réponse à la cible vit dans **[Ω(k), O(k²)]** » |

**Second mécanisme, de nature différente : le modèle mesuré n'est pas
nécessairement le format visé.** Le modèle du dépôt n'admet que des monômes
**positifs** (`../checks/tour_27_s2_espace_entier_cpsat.py`,
`MONOS = list(range(1, 1 << NV))`). Sans cette restriction, la séparation est
quasi gratuite — vérifié par **énumération exhaustive sur {0,1}^{2k}, sans
solveur** :

> `p = Σᵢ (¬xᵢ ∧ ¬yᵢ)` compte les blocs nuls, vaut `k − s` où `s` est le nombre
> de blocs à 1 ; ses ensembles de valeurs sont `{0..k−t}` et `{k−t+1..k}`,
> disjoints par construction. **Séparation vérifiée pour tout k = 3..8 et tout
> seuil 2 ≤ t ≤ k−1, au poids exactement k.**

| k | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|
| W, modèle du dépôt (positif), certifié | 12 | 20 | **30** | 42 | 56 | 72 |
| W, monômes sur littéraux (borne sup) | 3 | 4 | **5** | 6 | 7 | 8 |

*Réserve de sourçage, à ne pas escamoter* : la question « le format
Beigel-Tarui autorise-t-il les ∧ sur littéraux ? » est
**[NON TROUVÉ DANS [`../bib/beigel_tarui_1994.md`](../bib/beigel_tarui_1994.md)]**
— le Théorème 2 verbatim ne dit que « ∧ gates of fanin (log S)^{O(1)} », et une
source secondaire consultée le 2026-07-25 paraphrase au contraire « ANDs **of
variables** », ce qui validerait le modèle du dépôt. **La question reste
ouverte** et devrait être tranchée sur le texte primaire avant toute
utilisation de ce paragraphe. Ce qui est affirmable sans elle, et qui suffit à
la clôture du fil : la quantité mesurée est une restriction du problème dont le
coût est un facteur ≥ 6 dès k = 5 ; et le motif de plafond ci-dessus est
indépendant de ce point.

Pièces : [`../tours/tour_26_indicateur_modulaire_survit.md`](../tours/tour_26_indicateur_modulaire_survit.md) §5,
[`../tasks/done/T27-S2.md`](../tasks/done/T27-S2.md),
[`../tasks/done/F-020.md`](../tasks/done/F-020.md).

## Ce que les deux témoins ont en commun

1. **L'échelle du phénomène était connue, et disponible sans calcul.** Dans les
   deux cas elle était écrite dans le texte de référence — le Lemme 3.7 de KV
   pour l'un, le théorème de Beigel-Tarui pour l'autre — ou dans le **premier
   livrable du fil lui-même** (Tour 26 §5). Aucun des deux fils ne l'a lue
   avant de lancer sa campagne.
2. **Le dépassement n'a produit aucun signal d'alarme.** Chaque tâche prise
   isolément est irréprochable : mesure certifiée, antériorité cherchée,
   auto-corrections consignées. **La rigueur locale n'informe pas sur la
   trajectoire.** Avec `tasks/failed/` vide et 169 tâches toutes ✅, aucun
   compteur du dépôt ne pouvait descendre.
3. **Une tâche de lecture a battu 43 tâches de calcul.** ATLAS-006 a établi en
   une session, sans solveur, le verdict de portée que la campagne AS n'avait
   pas atteint.
4. **La sortie du régime pertinent laisse une trace textuelle, mais elle n'est
   pas un critère.** Sur les 7 livrables du fil SYM∘AND aval, 5 ne mentionnent
   aucune classe de complexité ; sur les 43 du fil AS, 38. Mais le même test
   appliqué aux pièces phares du dépôt les classerait hors cible : `V-053`,
   `V-055` (la seule cellule fermée par le dépôt), `ATLAS-006`, `ATLAS-005`,
   `A-011`, `AS-022`, `AS-039`, `F-006`, `F-019` — **toutes à zéro occurrence**.
   Le signal est corrélé au *sujet*, pas à la *distance*. C'est pourquoi
   `CLAUDE.md` §8 règle 8 en fait une alerte et non une porte : c'est ATLAS-005
   appliqué à notre propre instrument de direction.

## Test opératoire dérivé — le contrôle positif généralisé

> Avant d'ouvrir une campagne de mesure : **exiger que l'instrument voie un
> effet DÉJÀ PROUVÉ de même nature, dans son domaine accessible.** S'il ne le
> voit pas, ses négatifs ne prouvent rien et ses positifs sont des artefacts de
> régime. ATLAS-005 est le cas d'école : le gain Δ_w prouvé par KV est
> invisible à n ≤ 7, donc les égalités MAJ à n ≤ 7 ne discriminaient rien — et
> il aura fallu 40 tâches de plus pour en tirer la conséquence.

C'est ce test qui adosse le **test de plafond** de `CLAUDE.md` §8 règle 7 et le
**bilan de fil** de la règle 9.

## Ce que cette note n'est pas

Elle ne dit pas que la vérification exécutable est inutile : les instruments
certifiés du dépôt ont fermé une cellule de la matrice (ligne 14) et produit des
théorèmes qui survivent hors modèle. Elle dit **où** elle est utile : sur des
objets **finis et complets** — un réseau de rang donné, un ILP de dualité, la
réplication d'un théorème connu — et non sur des **régimes asymptotiques** dont
le premier point non trivial vit à n = 41, n ≈ 4050, ou 2^{polylog n}. La
question à poser en premier n'est pas « puis-je calculer ceci ? » mais **« à
quelle échelle le phénomène commence-t-il, et est-elle sous mon plafond ? »**
