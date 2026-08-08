# MC-015 — Mesures : le multi-fibres conditionnel (fibres composées)

Tâche : MC-015. Script : `checks/mc015_multifibres.py`. Date : 2026-08-08.
Instrument : CP-SAT (ortools), formulation canal-de-valeurs robuste
(variables val[x] + `!=` par paires), **OPTIMAL exigé partout, témoin
re-vérifié par assertion** à chaque résolution. 636 résolutions au total
(56 + 28 + 528 + 24), **0 non-conclu**. Durées : volet A < 1 min (ν = 4),
volet B 17 s, volet C 559 s, volet C2 7 s.

Objet : h(x, y) = [y = c_x], base x ∈ {0,1}^t, fibre y ∈ {0,1}^s
**partagée**, fibres-points c_x. Écart g(h) := W(h) − Σ_x G(c_x), avec
G la loi prouvée (MC-008) : W([y = c]) = s − |c| + 1 (c ≠ 0), s (c = 0).

> Incident sans perte : le PC a redémarré (~14 h 55) après la fin du
> volet C — le processus avait terminé et écrit sa sortie complète
> (ligne finale `[559s]`) ; seule la notification de fin a été perdue.
> Données relues depuis le fichier de sortie intact.

## Volet A — le corollaire 2-fibres depuis les lois F (base 1 bit, s = 3, ν = 4)

Les 56 paires ordonnées (c₀, c₁), c₀ ≠ c₁ : g recalculé DEPUIS les lois
F (C-MC009), puis **re-vérifié au solveur : 0 écart sur 56**.

| statut des cases | distribution de g |
|---|---|
| THÉORÈME (recouvrement, comparable, (1,1), linéaire — prouvées MC-008..013) | {−1 : 9, 0 : 40, +1 : 4} — 53 cases |
| CERTIFIÉ-solveur (couronne, min(a,b) ≥ 2 après normalisation) | {+1 : 3} — 3 cases |

Les 3 cases encore certifiées (non prouvées) sont exactement les paires
« 2-ensemble contre singleton complémentaire » — c₀ = {i, j},
c₁ = {k}, {i, j, k} = [3] — toutes trois **super-additives** (g = +1).
Le corollaire 2-fibres à base 1 bit est donc un THÉORÈME sur 53/56 de
la carte à s = 3, certifié sur le reste (couverture couronne ν ≤ 8,
MC-014).

## Volet B — multi-fibres t = 2, s = 4 (ν = 6) : une affectation par tuple

4 fibres-points sur base 2 bits ; affectation de référence : combo trié
croissant → points de base 00, 01, 10, 11 dans l'ordre.

| type | tuples | distribution de g | sous-additifs |
|---|---|---|---|
| antichaîne-paires (les 15 = C(6,4)) | 15 | {−2 : 13, −1 : 2} | **15/15** |
| antichaîne-mixte (singleton + 3 paires l'évitant) | 4 | {−2 : 4} | **4/4** |
| chaîne c₁ ⊂ c₂ ⊂ c₃ ⊂ c₄ (affectation alignée) | 3 | {0 : 3} | 0/3 |
| aléatoires (graine 20260808) | 6 | {−3 : 1, −1 : 3, 0 : 2} | 4/6 |

Détail complet (Σ G, W(h), g par tuple) dans la sortie du script,
mode `B`. Les deux antichaînes-paires à g = −1 sous cette affectation :
{0011, 0101, 0110, 1001} et {0011, 0101, 0110, 1010} (le « triangle »
des paires internes à {0,1,2} plus une paire touchant le bit 3).

## Volet C — les 24 affectations par tuple (528 résolutions)

Le modèle n'est **pas** invariant par permutation des points de base
(le point 00 est nu : son point de h porte le seul support c_x) — le
volet B ne testait qu'une affectation. Ici : chaque tuple × les 24
affectations fibre → point de base.

| type | tuples | g sur 24 affectations (par tuple) |
|---|---|---|
| antichaîne-paires | 12 des 15 | {−2 : 20, −1 : 4} |
| antichaîne-paires (deux couples complémentaires) | 3 des 15 | {−2 : 24} |
| antichaîne-mixte | 4 | {−2 : 24} |
| chaîne | 3 | {−3 : 2, −2 : 4, −1 : 12, 0 : 6} |

- **Antichaînes : 456/456 affectations sous-additives** (19 tuples × 24),
  g ∈ {−2 (majoritaire), −1}, jamais 0, jamais positif.
- Les 3 antichaînes-paires uniformément à −2 sont exactement celles
  formées de **deux couples complémentaires** ({0011, 1100}, {0101, 1010},
  {0110, 1001} pris 2 à 2 : C(3,2) = 3) — observation, mécanisme non
  établi.
- **Chaînes : l'additivité du volet B était un artefact d'alignement** —
  6/24 affectations additives seulement, 18/24 sous-additives, minimum
  g = −3 (plus bas que les antichaînes).
- Les 3 chaînes testées ont des distributions IDENTIQUES (elles sont
  images l'une de l'autre par permutation des bits de fibre — symétrie
  du modèle, cohérence interne).

## Volet C2 — quelles affectations rendent une chaîne additive ?

Chaîne 0001 ⊂ 0011 ⊂ 0111 ⊂ 1111, notation : rangs (1..4) reçus par
x = 00, 01, 10, 11. Les 6 affectations additives :

```
1234, 1243, 1324, 1423, 3142, 3412
```

soit **3 classes × 2** (la paire venant de l'échange des deux bits de
base, vraie symétrie du modèle) :

| classe | 00 reçoit | {01, 10} reçoivent | 11 reçoit |
|---|---|---|---|
| alignée | rang 1 (minimum) | {2, 3} | rang 4 (maximum) |
| B | rang 1 | {2, 4} | rang 3 |
| C | rang 3 | {1, 4} | rang 2 |

La classe alignée contient les 2 seules affectations **monotones**
(x ⊆ x′ ⟹ c(x) ⊆ c(x′)) ; les classes B et C ne sont pas monotones —
aucun invariant simple ne couvre les 3 classes. Mécanisme : **OUVERT**.
Pire affectation : rangs {4231, 4321} (le maximum au point nu, le
minimum au point plein), g = −3.

## Lecture

1. **La condition d'antichaîne est RÉFUTÉE comme condition suffisante de
   non-partage dès la base 2 bits** : 456/456 affectations d'antichaînes
   sous-additives. (À base 1 bit elle reste un théorème — volet A.)
   L'image s'INVERSE en passant de 2 fibres à 4 : à base 1, seuls les
   emboîtements (recouvrement descendant) partageaient ; à base 2, les
   antichaînes partagent toujours et seules certaines affectations de
   chaînes sont additives.
2. **Aucune condition d'ordre sur les supports ne protège** : antichaînes
   toujours sous-additives, chaînes sous-additives sauf 6 affectations
   sur 24. Le partage en espace partagé est **générique** à base ≥ 2.
   Le seul mécanisme d'additivité prouvé du dépôt reste le sélecteur
   (MC-006, blocs DISJOINTS).
3. **Mais le déficit mesuré est petit et borné** : g ≥ −3 sur les 580
   résolutions à (t, s) = (2, 4) — antichaînes concentrées à g = −2 = t.
   La question utile n'est plus le SIGNE mais la **loi de croissance du
   déficit** avec (t, s, nombre de fibres) : si |g| = O(t) ou O(k), la
   totalisation par fibres partagées reste additive à terme contrôlé
   près (ce qui pourrait suffire au schéma) ; si |g| = Θ(Σ), elle meurt.
   C'est le verrou requalifié.
