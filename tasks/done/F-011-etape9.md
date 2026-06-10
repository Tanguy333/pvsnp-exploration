# TÂCHE F-011, étape 9 : Théorème G — ✅ **LA LOI OR MOD 3 EST COMPLÈTE**

- **Type** : F (preuve — clôture de loi)
- **Exécutée le** : 2026-06-10
- **Script** : [`checks/task_f011e9_complete_law.py`](../../checks/task_f011e9_complete_law.py)

## Théorème G (borne supérieure de la rampe)

> Pour P = 3^b, 2P < n < 3P, r = n−2P :
> `deg₃^sym(OR_n) ≤ n − P`, réalisé par
> `h(w) = c·(−1)^r·C(w−1, r) mod 3` et un préfixe compatible.

**Preuve.** (i) *Périodicité automatique* : toute fonction de degré ≤ r < P
est 3^{c'}-périodique pour le plus petit 3^{c'} > r (Δ^{3^{c'}} =
S^{3^{c'}} − id), et 3^{c'} | P — donc h(j+P) = h(j) pour tout j.
(ii) Les contraintes de compatibilité de g (chaînes g(j) → g(j)+h(j) →
g(j)+2h(j) de longueur ≤ 3, valeurs dans {1,2}, départ g(0)=0) se
réduisent alors à « h(0) ≠ 0 et h ≡ 0 sur [1, n−2P] » — exactement les
propriétés définissant h (l'unique fonction de l'étape 7, recyclée en
*construction*). (iii) Le préfixe g(j) := 1 si h(j) ∈ {0,1}, 2 sinon,
propage dans {1,2}. ∎

## Théorème final (la loi complète)

> **`deg₃^sym(OR_n) = max( 3^⌊log₃n⌋, n − 3^⌊log₃n⌋ )` pour tout n ≥ 1.**
> Borne inférieure : Théorèmes D (périodicité) + E (rampe).
> Borne supérieure : Théorèmes F (0,1^P,2^{n−P}) + G (ci-dessus).

**Vérification** : 26/26 constructions explicites de degré exactement égal
à la loi avec couverture valide ; égalité loi = construction = DP
(faisable à la loi, infaisable au-dessous) partout.

## Le renversement élégant

La fonction `h = c(−1)^r C(w−1,r)` qui servait à l'étape 7 d'**obstruction**
(son unicité + sa non-nullité en r+1 donnaient la contradiction de la borne
inf) devient à l'étape 9 la **construction** de la borne sup — le même
objet, vu des deux côtés de la frontière. C'est le signe d'une loi
vraiment comprise.

## État du fil (9 étapes)

**10 théorèmes prouvés**, dont la **première loi exacte complète** :
deg₃^sym(OR_n) fermée des deux côtés pour tout n. Restent : la loi MAJ
mod 6 (C-F011, anomalies prouvées, certificats consécutifs mod 3
identifiés) et, à terme, la levée de la restriction symétrique.
