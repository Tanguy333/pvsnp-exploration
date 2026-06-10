# TÂCHE F-011, étape 18 : Théorème K (anomalie-tueur) + MAJ_9 — ✅ l'hypothèse plate tient

- **Type** : F (théorème + sonde constructive)
- **Exécutée le** : 2026-06-10
- **Script** : [`checks/task_f011e18_flat_law.py`](../../checks/task_f011e18_flat_law.py)

## Lemme 5 (Möbius — le Lemme 1 du modèle général)

> Un polynôme multilinéaire sur Z_m s'annule sur tous les points de poids
> < t **ssi** ses coefficients sur les monômes de degré < t sont nuls
> (inversion triangulaire sur le treillis des parties).
> **Corollaire : deg₆(THR_{t,n}) ≥ t, toujours.**

## Théorème K (l'anomalie-tueur)

> Pour t = 2^a : `deg₆(THR_{t,2t}) = t`, réalisé par
> `c_T = 3` pour tout t-sous-ensemble T ≠ T₀ et `c_{T₀} = 1`
> (u ≡ 1 mod 2 partout + un seul monôme mod 3).

**Preuve.** Support en degré t → zéros sous t (Lemme 5). Pour
w ∈ [t, 2t−1] : P(S) = 3·C(w,t) − 2·[T₀ ⊆ S] ∈ {1, 3} mod 6 (C(w,t)
impair par Lucas sur [2^a, 2^{a+1})). Pour w = 2t : P = 3·C(2t,t) − 2 ≡ 4
(C(2t,t) pair par Kummer). ∎
**Vérifié** : exhaustif t = 2, 4, 8 (jusqu'à 65 536 points) ; forme close
t = 16.

> Les trois anomalies prouvées du modèle symétrique s'effondrent :
> deg₆(MAJ_4) = 2, deg₆(MAJ_16) = 8, deg₆(MAJ_32) = 16.

## La sonde MAJ_9 (premier test hors-anomalie non trivial)

W_fail = {6, 8, 9} (où C(w,5) est pair), 126 coefficients mod 3 :
**certificat trouvé** par recuit simulé (9 s), 76/126 coefficients non
nuls, **vérifié exhaustivement sur les 512 points** →
`deg₆(MAJ_9) = 5 = t` (contre 8 en symétrique).

## Hypothèse plate (étayée : tous les points testés)

> **`deg₆(MAJ_n) = ⌈n/2⌉`** — le degré faible général de MAJ mod 6 colle
> à la borne triviale de Möbius. Points établis : n = 4..9 (exhaustif ou
> certificat), 16, 32 (Théorème K) ; loi symétrique riche = artefact.

## Portée pour l'Atlas (zone 2) — le recadrage honnête

Si l'hypothèse plate est vraie en général, alors **le modèle des
représentations faibles mod 6 ne peut pas séparer MAJ des fonctions
triviales** (toute fonction ≥-monotone de seuil t y coûte exactement t).
La richesse que nous avons cartographiée (15 étapes) vit *uniquement*
dans la restriction symétrique. C'est un éclairage net sur le mur de
1987 : l'analogue composite du « Pas 1 » ne peut pas être le modèle
faible nu — il faudra des mesures plus contraintes (représentations
fortes, approximations probabilistes, ou le passage aux circuits).

## Garde-fous et suites

- « Hypothèse plate » = conjecture (étiquetée) ; points prouvés listés.
- Folklore-check requis : « weak degree of MAJ mod 6 = trivial bound »
  est peut-être connu (la construction du Théorème K est simple une fois
  vue) — à vérifier avant toute diffusion. [À ajouter au lot Göös/SE.]
- e19 candidates : (a) tester la plate à n = 10..13 (recuit) ; (b) le
  modèle FORT mod 6 (P(x) = valeurs prescrites) — là où la vraie
  difficulté composite devrait vivre ; (c) mise à jour de la note.
