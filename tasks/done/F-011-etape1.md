# TÂCHE F-011, étape 1 : la loi de deg₆^sym(MAJ_n) est cernée — ✅ conjecture C-F011 formulée

- **Type** : F (données → conjecture ; étapes 2-3 = preuve, à venir)
- **Exécutée le** : 2026-06-10
- **Script** : [`checks/task_f011_maj_law.py`](../../checks/task_f011_maj_law.py)
- **Objectif du fil** (recadrage P vs NP) : produire un **théorème sur le
  front composite** (zone 2) — une borne inférieure nouvelle, classe
  symétrique, honnêtement cadrée.

## Données (n = 1..44, t = ⌈n/2⌉)

La loi candidate `L1(t) = min{q ∈ {2^a, 3^b} : q ≥ t}` colle sur **40/42
points conclus**. Exactement deux anomalies : (n=4 : 3 vs 2) et
(n=16 : 9 vs 8).

## Le mécanisme des anomalies (vérifié 3/3)

Pour q = 2^a ≥ t, la stratégie mod 2 (digit de Lucas en position a) couvre
les poids w ∈ [q, 2q) mais **échoue toujours à w = 2q** (bit nul ; et
C(2q,q) est pair pour tout q ≥ 1, par Kummer). Si n ≥ 2q, le sauvetage ne
peut venir que du côté mod 3 — gouverné par **C(2q, q) mod 3** :

| t = q | C(2q, q) mod 3 | verdict | observé |
|---|---|---|---|
| 2 | C(4,2) = 6 ≡ 0 | échec → anomalie | ✓ (d₆ = 3) |
| 4 | C(8,4) = 70 ≡ 1 | sauvé | ✓ (d₆ = 4, pas d'anomalie) |
| 8 | C(16,8) = 12870 ≡ 0 | échec → anomalie | ✓ (d₆ = 9) |

## Conjecture C-F011

> `deg₆^sym(MAJ_n) = L1(t)`, **sauf** si `L1(t) = q = 2^a` avec `n ≥ 2q` et
> `C(2q, q) ≡ 0 (mod 3)`, auquel cas la valeur est la puissance suivante
> de {2^a, 3^b}.

**Prédiction falsifiable** : t = 16 = 2⁴ donne C(32,16) ≡ 0 (mod 3)
(Lucas : 32 = 1012₃, 16 = 0121₃, position 1 : C(1,2) = 0), donc
`deg₆^sym(MAJ_32) = 27`. Cohérent avec les données actuelles (caps >c24 à
n=32..36, et 27 observé directement dès n=37 où L1 = 27). À tester avec
des caps élargis (étape 2).

## Observations structurelles annexes

- `deg₂^sym(MAJ_n)` = plus petite puissance de 2 ≥ t — pur (1,2,4,8,16).
- `deg₃^sym(MAJ_n)` ∈ {1, 3, **6**, 9, **18**, 27} — mod 3 seul admet des
  valeurs 2·3^b : la structure fine n'est pas que des puissances.
- Toutes les valeurs mod 6 observées sont des puissances de 2 ou 3 — la
  conjecture « l'optimum est toujours réalisé au voisinage d'une stratégie
  mono-puissance » est implicite dans C-F011 et devra être prouvée (les
  stratégies de combinaison dans le noyau existent : c'est ainsi que d=3
  couvre n=4).

## Étapes suivantes (le chemin vers le théorème)

1. **Étape 2** : tester la prédiction MAJ_32 = 27 (caps élargis) +
   sonder t près d'autres puissances critiques.
2. **Étape 3** : preuve. Borne sup = constructions explicites (e_q +
   corrections dans le noyau — le cas n=4/d=3 montre le gabarit :
   a₂e₂ + a₃e₃). Borne inf = montrer qu'aucune combinaison du noyau à
   degré < valeur ne couvre — combinatoire de Lucas en dimension finie ;
   c'est la partie dure, pipeline T-F006 (chercher les certificats
   d'infaisabilité et leur structure).

Si l'étape 3 aboutit : **première borne inférieure prouvée du dépôt sur le
front composite** (classe symétrique — cadrage honnête maintenu : polynôme
unique ≠ circuit AC⁰[6] ; mais c'est précisément le Pas-1-analogue dont
l'absence bloque la méthode polynomiale mod 6 depuis 1987).
