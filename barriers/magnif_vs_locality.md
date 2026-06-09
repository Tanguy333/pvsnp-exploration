# D-004 : Hardness magnification × Barrière de localité (CHOPRS 2020)

> Tâche type D. Exécutée le 2026-06-09. Source : Chen-Hirahara-Oliveira-
> Pich-Rajgopal-Santhanam, *« Beyond Natural Proofs: Hardness Magnification
> and Locality »* (ITCS 2020, [arXiv:1911.08297](https://arxiv.org/abs/1911.08297),
> **52 pages greppées en texte intégral**). Citations « > » = ce texte.

## 1. L'approche

Hardness magnification (Oliveira-Pich-Santhanam 2019, cahier §7.6 ;
abstract CHOPRS verbatim) :

> « Hardness magnification reduces major complexity separations (such as
> EXP ⊄ NC¹) to proving lower bounds for some natural problem Q against
> weak circuit models. »

L'espoir : les bornes « faibles » requises (légèrement super-linéaires, sur
MCSP/MKtP en versions gap) semblent à portée des techniques connues, et la
magnification **contourne RR** :

> « The very existence of the natural proofs barrier provides a direction
> for proving strong circuit lower bounds: one can proceed by refuting the
> existence of natural properties. In other words, a way to avoid natural
> proofs is to prove that there are no natural proofs. »

(MCSP est précisément le problème « détecter une propriété naturelle » —
une borne sur MCSP n'est pas elle-même naturalisable au sens usuel.)

## 2. La barrière — définition exacte

> « This is captured by a **locality barrier**: existing magnification
> theorems unconditionally show that the problems Q considered above admit
> highly efficient circuits extended with **small fan-in oracle gates**,
> while lower bound techniques against weak circuit models quite often
> **easily extend to circuits containing such oracles**. This explains why
> direct adaptations of certain lower bounds are unlikely to yield strong
> complexity separations via hardness magnification. »

Mécanisme : la preuve du théorème de magnification elle-même construit,
inconditionnellement, des circuits très efficaces pour Q *avec des portes
oracle de petit fan-in* :

> « it unconditionally follows that MCSP[2^{n^{1/3}}, 2^{n^{2/3}}] can be
> computed by highly efficient Formula-XOR circuits containing oracle gates
> of small fan-in, for some oracle. »

Donc toute technique de borne inférieure qui « localise » (= reste valide
en présence d'oracles de petit fan-in, quelle que soit la fonction
calculée par ces oracles) **ne peut pas** prouver la borne requise pour Q —
elle contredirait le circuit-oracle qui existe inconditionnellement.

Et les auteurs vérifient que les techniques connues localisent :

> « [lower bounds] of the hardness magnification frontiers quite easily
> handle (in the respective models) the presence of oracles of small
> fan-in, regardless of the function computed by these oracles. […] we
> actually localize all proofs of the lower bounds from B3 and B4 we are
> aware of. »

Application concrète : la localisation **réfute l'Anti-Checker Hypothesis**
de OPS19 (et une famille de théorèmes de magnification potentiels).

## 3. Verdict : **ÉCHEC (conditionnel) des adaptations directes — barrière du même type que RR mais orthogonale**

- La magnification **évite RR** (point 1) — c'était sa raison d'être.
- Mais elle bute sur la localité : les bornes faibles requises doivent être
  prouvées par des techniques **non-localisantes**, et toutes les
  techniques connues contre les modèles faibles localisent (vérifié par
  CHOPRS pour les frontières A-E).
- Structure remarquable : comme RR, c'est une barrière de type « la
  technique prouve trop » — RR : la propriété casserait les PRG ; localité :
  la borne contredirait un circuit-oracle qui existe *inconditionnellement*.
  La localité est même plus dure en un sens : pas d'hypothèse crypto.

## 4. Ligne Atlas

| Cellule | Verdict |
|---|---|
| Magnification × RR | **franchie par construction** (MCSP = méta-problème ; refuter les propriétés naturelles EST la stratégie) |
| Magnification × relativisation/algébrisation | non traité ici (les théorèmes de magnification sont des réductions, généralement relativisantes ; la borne finale viserait du non-relativisant) |
| Magnification × **localité** | **FERMÉE pour les adaptations directes des techniques connues** (toutes localisent) ; ouverte pour une hypothétique technique non-localisante — aucune connue |

Leçon de la ligne (même pattern que GCT/D-002) : chaque programme
post-barrières développe sa **barrière interne propre**. Le paysage n'est
pas « 3 barrières + 1 », c'est : toute stratégie assez précise pour être
exécutable engendre l'analyse de sa propre impossibilité.

## Références de la cellule

CHOPRS 2020 (arXiv:1911.08297, ITCS 2020), OPS 2019 (cahier §7.6),
A-007 (`bib/razborov_rudich_1997.md`), Tour 4 (où la barrière avait été
mentionnée comme « barrières internes connues »).
