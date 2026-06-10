# TÂCHE F-011, étape 10 : Théorèmes H, I, J — ✅ la loi MAJ mod 6 prouvée sur n ≤ 40

- **Type** : F (preuves — clôture de C-F011 sur le domaine calculé)
- **Exécutée le** : 2026-06-10
- **Script** : [`checks/task_f011e10_maj_law.py`](../../checks/task_f011e10_maj_law.py)
- **Incident consigné** : 1re version du glouton oubliait v_w = 0 (échec
  [A] + 6 faux échecs en [B]) — corrigé, tout passe.

Notation : t = ⌈n/2⌉, q₂/q₃ = plus petites puissances de 2/3 ≥ t,
L1 = min(q₂, q₃).

## Lemme 4 (glouton triangulaire — folklore)

> Pour tout premier p et toute fenêtre [t, D] : il existe
> V = Σ v_i e_i (i ≤ D) avec V ≢ 0 sur [t, D]. (Montée triangulaire :
> V(w) = v_w + (termes inférieurs) ; une valeur interdite, p−1 ≥ 1 choix.)

Vérifié sur ~950 fenêtres, p = 2 et 3.

## Théorème H (borne supérieure, général)

> `deg₆^sym(MAJ_n) ≤ L1(t)` hors anomalie (et = puissance suivante en cas
> d'anomalie, certificats explicites pour t = 2, 8, 16).

**Preuve.** Cas L1 = q₂ : u = e_{q₂} couvre [q₂, min(n, 2q₂−1)] mod 2
(Lucas) ; V = glouton mod 3 couvre [t, q₂−1] (Lemme 4) ; si n = 2q₂
(⟺ t = q₂), le poids w = 2q₂ est pair (Kummer) et se couvre mod 3 en
ajustant v_{q₂} ssi C(2q₂, q₂) ≢ 0 mod 3 — sinon anomalie. Cas L1 = q₃ :
v = e_{q₃} couvre [q₃, n] mod 3 (**jamais d'anomalie** : C(2q₃, q₃) ≡
C(2,1) = 2 mod 3) ; u = glouton mod 2 couvre [t, q₃−1]. ∎
**Vérifié** : 36/36 certificats explicites valides (n = 2..40 hors
anomalies), zéros + couverture en entiers exacts.

## Théorème I (borne inférieure, régime n ≥ max(q₂, q₃))

> Si d < L1 : U est q₂-périodique (BBR) et morte sur [q₂, n]
> (w − q₂ < t), V est q₃-périodique et morte sur [q₃, n]. Tout
> w ∈ [max(q₂,q₃), n] est doublement mort → `deg₆ ≥ L1`. ∎

Couvre 29 des 39 valeurs de n ≤ 40.

## Théorème J (borne inférieure, régime résiduel q₂ ≤ n < q₃ — l'argument MIXTE)

> Si d < t : trivial (noyau vide). Si t ≤ d < L1 = q₂ : U morte sur
> [q₂, n] par périodicité mod 2 ; et s'il existe w ∈ [q₂, n] avec
> w − q₂ < t et `C(w, i) ≡ 0 (mod 3)` pour tout i ∈ [t, q₂−1]
> (témoin Lucas-mort), alors w est doublement mort → `deg₆ ≥ q₂`.

**Établi sur tout le régime résiduel n ≤ 40** : n = 7, 8 triviaux
(L1 = t) ; n = 19..26 : témoin uniforme **w = 18 = (2,0,0)₃** (sous-
binômes {0, 9, 18} évitent [t, 15] ; mort mod 2 : 18−16 = 2 < t). C'est
le mécanisme découvert en préparation (mort mod 2 par périodicité + mort
mod 3 par Lucas — le mariage des deux moitiés du CRT).

## Bilan : C-F011 est PROUVÉE pour tout n ∈ [2, 40]

| Morceau | Portée |
|---|---|
| Théorème H (≤) | général (toute taille), vérifié n ≤ 40 |
| Théorème I (≥) | général pour n ≥ max(q₂,q₃) |
| Théorème J (≥) | régime résiduel — témoins vérifiés par cellule n ≤ 40 |
| Anomalies | certificats explicites t = 2, 8, 16 (étapes 3, 8) |

**Résiduel pour la loi générale (tout n)** : (a) le lemme d'existence du
témoin J (candidat : w = 2·3^β avec 3^β < t ≤ … — vrai sur toutes les
cellules testées) ; (b) les certificats d'anomalie pour t = 2^a général
(3 instances connues). Deux énoncés combinatoires précis et bornés.
