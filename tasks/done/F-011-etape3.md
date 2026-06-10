# TÂCHE F-011, étape 3 : PREUVES — ✅ premiers théorèmes du dépôt sur le front composite

- **Type** : F (preuve, pipeline T-F006)
- **Exécutée le** : 2026-06-10
- **Script de vérification** : [`checks/task_f011e3_proofs.py`](../../checks/task_f011e3_proofs.py)
  (4 blocs, tous OK : télescope t=1..20/i≤80, forme close 31/31,
  3 corollaires, certificat exact)
- **Cadre** : représentations faibles **symétriques** de THR_t sur Z_m
  (`S(w) ≡ 0` pour w < t, `≢ 0` pour t ≤ w ≤ n). Modèle restreint —
  cadrage honnête maintenu : polynôme unique ≠ circuit AC⁰[6].

---

## Lemme 1 (structure du noyau)

> L'espace des polynômes symétriques de degré ≤ d sur Z_m s'annulant sur
> tous les poids w < t est exactement `span{ e_i : t ≤ i ≤ d }` (en valeurs :
> `span{ C(w,i) : t ≤ i ≤ d }`), de dimension d − t + 1.

**Preuve.** En base de Mahler/Newton, S(w) = Σ_i a_i C(w,i) avec
a_i = Δ^i S(0) (différences finies — système triangulaire : a_i ne dépend
que de S(0..i)). Si S ≡ 0 sur [0, t−1], alors a_i = 0 pour tout i < t.
Réciproquement, C(w, i) = 0 pour w < i, donc toute combinaison des e_i,
i ≥ t, s'annule sur [0, t−1]. ∎

*(Explique au passage les dimensions observées à l'étape 2 : dim = d−15 à
t = 16, des deux côtés.)*

## Théorème T-F011a (forme close exacte de deg₂^sym, toute la famille THR)

> Pour tous 1 ≤ t ≤ n :
> `deg₂^sym(THR_{t,n}) = max{ i ∈ [t, n] : C(i−1, t−1) impair }`
> `= 1 + max{ j ∈ [t−1, n−1] : (t−1) AND j = (t−1) }` (Lucas, bit à bit).

**Preuve.** (i) Sur F₂, « non nul » = « égal à 1 » : la couverture impose
S(w) = 1 pour tout w ∈ [t, n] — combinée aux zéros forcés, la fonction S
sur [0, n] est *unique* (l'échelon). (ii) Ses coefficients de Mahler sont
a_i = Σ_{w=t}^{i} C(i, w) mod 2 ; par la récurrence de Pascal,
Σ_{w=t}^{i} C(i,w) = C(i−1, t−1) + 2·Σ_{w=t}^{i−1} C(i−1,w), donc
**a_i ≡ C(i−1, t−1) (mod 2)** (télescope ; vérifié exécutablement sur
1 540 paires (t, i)). (iii) Le degré de l'unique candidat est donc
max{i ≤ n : C(i−1,t−1) impair}, atteint ssi d ≥ ce max ; ce max existe
(i = t donne C(t−1,t−1) = 1). (iv) La forme bit à bit est Lucas. ∎

**Vérification** : coïncide avec les 31 valeurs mesurées (n = 1..31). Le
corollaire « plus petite puissance de 2 ≥ t, doublant quand n atteint le
prochain surensemble bit à bit de t−1 » explique *prouvablement* toute la
colonne mod 2.

## Lemme T-F011b (infaisabilité mod 6)

> S'il existe w* ∈ [t, n] tel que `C(w*, i) ≡ 0 (mod 2)` **et**
> `(mod 3)` pour **tout** i ∈ [t, d], alors aucune représentation
> symétrique faible de degré ≤ d de THR_{t,n} n'existe sur Z₆.

**Preuve.** Par le Lemme 1, tout candidat s'écrit U = Σ_{i=t}^d u_i C(·,i)
mod 2 et V = Σ_{i=t}^d v_i C(·,i) mod 3. L'hypothèse force U(w*) = 0 et
V(w*) = 0 quel que soit le choix des coefficients — w* n'est jamais
couvert. ∎

### Corollaires prouvés (le mécanisme des anomalies, vérifié bloc [3])

Avec w* = 2t et Kummer (C(2t, t) toujours pair) + Lucas :

| n | t | w* | C(w*, i) ≡ 0 mod 6 pour i ∈ | borne prouvée |
|---|---|---|---|---|
| 4 | 2 | 4 | [2, 2] | **deg ≥ 3** |
| 16 | 8 | 16 | [8, 8] | **deg ≥ 9** |
| 32 | 16 | 32 | [16, 26] | **deg ≥ 27** |

## Théorème (valeur exacte) : `deg₆^sym(MAJ_32) = 27`

**Borne inférieure** : corollaire ci-dessus (≥ 27).
**Borne supérieure — certificat explicite, remarquablement simple** :

> `V = e₁₆ + e₁₈ + e₂₅ + e₂₇ (mod 3)`, u = 0 :
> V(w) = C(w,16) + C(w,18) + C(w,25) + C(w,27) ≢ 0 (mod 3) pour tout
> w ∈ [16, 32], et ≡ 0 pour w < 16 (automatique, i ≥ 16 > w).

Vérifié **en entiers exacts** sur les 33 poids w = 0..32 (bloc [4]). Le
certificat est purement mod 3 — donc en prime : `deg₃^sym(MAJ_32) ≤ 27`. ∎

---

## Ce qui est prouvé / ce qui reste conjecture

| Énoncé | Statut |
|---|---|
| Lemme 1 (noyau) | ✅ **prouvé** (toute la famille, tout m) |
| T-F011a : forme close de deg₂^sym(THR_{t,n}) | ✅ **prouvé** (exact, toute la famille) |
| T-F011b + anomalies (≥ 3, ≥ 9, ≥ 27) | ✅ **prouvé** |
| deg₆^sym(MAJ_32) = 27 | ✅ **prouvé** (inf + certificat) |
| Loi complète C-F011 (toute valeur de deg₆^sym(MAJ_n)) | ⚠ conjecture (47/47 + mécanisme partiellement prouvé) — il manque la loi mod 3 exacte et les constructions générales |

## Portée (cadrage P vs NP)

Ce sont les **premières bornes inférieures prouvées du dépôt sur le front
composite** (zone 2 de l'Atlas, mur de 1987) — dans le modèle polynomial
symétrique, qui est exactement le « Pas 1 » dont l'absence d'analogue
composite bloque la méthode de Razborov-Smolensky depuis 1987. Le lemme
T-F011b montre *pourquoi* en une ligne : sur Z₆, les binômes peuvent
s'annuler simultanément mod 2 et mod 3 sur des fenêtres entières
(C(32, i) ≡ 0 mod 6 pour i ∈ [16, 26] !), un phénomène impossible sur un
corps. Prochaine marche réaliste : la loi mod 3 exacte (les valeurs 2·3^b),
puis lever la restriction symétrique — chaque marche élargit le modèle vers
les circuits.
