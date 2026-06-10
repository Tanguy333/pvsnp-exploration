# TÂCHE F-011, étape 2 : prédiction MAJ_32 = 27 — ✅ **CONFIRMÉE**

- **Type** : F (test de prédiction falsifiable)
- **Exécutée le** : 2026-06-10
- **Script** : [`checks/task_f011e2_maj32.py`](../../checks/task_f011e2_maj32.py)

## Le test et son verdict

C-F011 prédisait : t = 16 = 2⁴, `C(32,16) ≡ 0 (mod 3)` → la puissance 16
échoue dès que w = 32 entre dans la fenêtre, valeur = puissance suivante
= 27.

| Test | Prédiction | Résultat |
|---|---|---|
| n=31 (contrôle : w=32 hors fenêtre) | 16 | **16** ✓ (infaisable à 15) |
| **n=32, d = 16..26** | tous infaisables | **tous infaisables** ✓ (exhaustif, noyaux complets) |
| **n=32, d = 27** | faisable | **FAISABLE** ✓ |
| n=33..36 | 27 | **27, 27, 27, 27** ✓ |

**C-F011 tient désormais sur 47/47 points conclus** — y compris une
prédiction énoncée *avant* le calcul, sur le point le plus délicat
(l'anomalie de 3e génération t = 2⁴).

## Détail structurel révélé par le test

Aux degrés 16..25 (n=32), les noyaux sont **minuscules** (dim 1 de chaque
côté : 2 éléments mod 2, 3 mod 3) — les 16 lignes binomiales de contraintes
sont presque de rang plein, il n'y a *rien* à combiner : l'infaisabilité
est massive, pas marginale. À d=26 les dimensions montent à 11 (toujours
infaisable), à d=27 à 12 et la couverture apparaît. La borne inférieure de
l'étape 3 devra capturer exactement ce phénomène de rang : **c'est le rang
des matrices binomiales mod 2 et mod 3 sous le seuil qui commande tout** —
un objet Lucas-combinatoire propre, et prouvable.

## État du fil F-011

- Étape 1 ✅ : loi cernée, mécanisme 3/3.
- Étape 2 ✅ : prédiction falsifiable confirmée (47/47).
- **Étape 3 (la preuve)** : borne sup constructive + borne inf par rang
  des matrices binomiales sous le seuil. La cible est maintenant précise :
  > **T-F011 (à prouver)** : pour t ≤ q < d', le système {S(w) = 0, w < t ;
  > S(w) ≠ 0 mod 6, w ∈ [t, n]} est infaisable en degré d ssi … (condition
  > de rang Lucas) — avec pour corollaire la loi C-F011.

Statut : conjecture très fortement étayée, **pas un théorème** (q.12
respectée — mais c'est la première conjecture du dépôt avec une prédiction
confirmée *a priori* sur le front composite).
