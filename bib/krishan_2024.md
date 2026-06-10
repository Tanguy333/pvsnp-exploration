# Audit — Krishan & Vishwanathan, « Towards ACC Lower Bounds using Torus Polynomials » (ECCC TR24-074)

- **Source** : [ECCC TR24-074](https://eccc.weizmann.ac.il/report/2024/074/),
  38 pages, texte intégral extrait le 2026-06-11 (pypdf).
- **Contexte dépôt** : suite de la veille probabiliste
  (`bib/veille_probabilistes_2026.md`) et des mesures V-001/V-002.

## La chaîne de réductions (verbatim)

1. **Yao 1990 (Conjecture 1)** : ACC ⊊ TC⁰.
   **Barrington 1989 (Conjecture 2)** : MAJ_n ∉ ACC.
2. **BHLR Théorème 1.1** : « Consider any function f ∈ ACC. Then, for any
   ε = 1/n^{O(1)}, there exists a torus polynomial of degree at most
   log(n)^{O(1)} that approximates f within an error of ε. »
3. **BHLR Théorème 1.2 (le mur symétrique)** : « Any symmetric torus
   polynomial approximating the majority function within an error of
   1/20n must have degree Ω(√n / log n). »
4. **BHLR Conjecture 5 (= Conjecture 3 du papier)** : la même borne pour
   les polynômes toriques **asymétriques** — « This conjecture, if true,
   proves Conjecture 2. Moreover [\[CLLO21\]] proved that it leads to an
   even stronger statement » : **sépare P de ACC**.

## La méthode (verbatim — et c'est notre outillage)

> « Write the conditions that P must satisfy as a **linear program** […]
> Use **duality** […] The dual is unbounded if and only if the original
> program is infeasible. Prove that the dual is indeed unbounded. »
> Pour le tore : « interpreting a torus polynomial as a real polynomial
> that can have arbitrary **integral parts**. This leads to a **family of
> linear programs, for each combination of integral parts** ».

Leur contribution : étendre la **méthode des polynômes duaux** (Bun-Thaler)
au tore, et réduire la conjecture à « a seemingly more manageable
conjecture regarding the **ℓ2 norm of specific vectors** ».

## Leurs résultats

- Borne inférieure pour les toriques **symétriques** approximant les
  fonctions Δ_w (sortie 1 ssi exactement w uns — inclut AND).
- **Conséquence prouvée** : « asymmetric torus polynomials are strictly
  more powerful than their symmetric counterparts » (pour les Δ_w).
- Première borne asymétrique : AND exige degré Ω(log n) pour erreur 1/2n.

## Confrontation avec nos mesures (V-001/V-002) — le raffinement

| Fonction | Asymétrie sur le tore | Source |
|---|---|---|
| Δ_w / AND | **aide prouvément** (séparation sym/asym) | KV 2024, théorème |
| **MAJ, n ≤ 6** | **n'aide pas** (ε\* identiques, MILP exacts, tous degrés) | nos V-001/V-002 |

Notre lecture V-001 (« le modèle torique est robuste à l'asymétrie ») était
**trop générale** — la robustesse est un phénomène *propre à MAJ* (au moins
aux petites tailles), pas au modèle. C'est précisément ce qui rend la
Conjecture 5 de BHLR à la fois plausible (nos données) et difficile (la
symétrisation WLOG est *fausse* en général sur le tore — KV le prouvent).
Nos mesures MAJ complètent leur séparation Δ_w : les deux ensemble
dessinent la frontière exacte de là où l'asymétrie mord.

## La conjecture exacte (extraite le 2026-06-11, V-003)

> « The main hurdle we encounter in proving this is that, while Lemma 3.9
> gives us an upper bound on the ℓ1 norm of the shortest vector, we are
> not able to argue about which position in the shortest vector must
> contain an odd entry. If we can prove that the last entry in the
> shortest vector is one, then by using an argument similar to Lemma 3.8,
> we can prove the lower bound for all ∆w functions. Hence, we conjecture
> that the last entry is indeed one.
> **Conjecture 5. Consider the basis B for any n, d. There exists a
> vector γ ∈ L(B) with the smallest ℓ2 norm such that γ_n = 1.** »

C'est un énoncé de **réseau euclidien** (plus court vecteur d'un réseau
binomial avec contrainte sur la dernière coordonnée) — directement
calculable aux petits (n, d) : candidat V-004.

## Ouverture exécutable (V-003 candidate)

Leur machinerie duale = nos certificats duaux (F-005/F-006). Sonder
numériquement : extraire les duaux de nos MILP toriques (à parties
entières fixées) pour MAJ aux petits n, et les comparer à la structure de
leurs vecteurs ℓ₂ — chercher empiriquement la forme du dual optimal que
leur conjecture postule.
