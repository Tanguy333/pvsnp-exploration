# TÂCHE F-011, étape 26 : THÉORÈME K′ — ✅ deuxième famille infinie de points 2t plats

- **Type** : F (théorème)
- **Exécutée le** : 2026-06-11
- **Script** : [`checks/task_f011e26_theorem_kprime.py`](../../checks/task_f011e26_theorem_kprime.py)

## Théorème K′

> Pour t = 2·3^k (k ≥ 0), s = 3^k, n = 2t, [n] = A ⊔ B en deux moitiés :
> **`V = e_t + e_s(A)·e_s(B) (mod 3)`** est une représentation faible de
> THR_{t, 2t} sur Z₆, **purement mod 3** — donc `deg₆(THR_{t,2t}) = t`
> (borne inférieure = Lemme 5/Möbius).

**Preuve (trois lemmes de Lucas, sur les profils (a, b), w = a+b).**
*(L1)* Fenêtre basse w ∈ [t, t+s) vive : en base 3, w = (2, digits(r))
domine t = (2, 0^k) → C(w,t) ≡ 1.
*(L2)* Fenêtre haute w ∈ [t+s, 2t] : a, b ∈ [s, t] forcés → leur digit
de position k vaut 1 ou 2 → C(a,s)·C(b,s) ≢ 0 ; et C(w,t) ≡ 0 (digit de
position k de w < 2). V = produit ≢ 0.
*(L3)* Non-collision en fenêtre basse : V = 1 + produit ≡ 0 exigerait
produit ≡ 2, donc un facteur 2 (⟺ a = t) — mais alors b = w−t < s et
l'autre facteur est 0. Donc V ∈ {1, 2}. ∎

**Vérifié** : k = 0..3 (t = 2, 6, 18, 54 ; n jusqu'à 108) — les trois
lemmes + couverture complète par profils, tout OK ; t = 2 et 6 déjà
vérifiés point-par-point (e17, e24, e25b).

## Portée

- **Deux familles infinies** de points n = 2t plats sont maintenant des
  théorèmes : **K** (t = 2^a, mod 2 + un monôme mod 3) et **K′**
  (t = 2·3^k, pur mod 3) — les anomalies symétriques s'effondrent le
  long des deux suites de puissances.
- La genèse est exemplaire du pipeline : SAT brut ÉCHOUE (4,5 h) →
  ansatz trouve le certificat n = 12 (0 s) → la forme close se lit →
  le mécanisme se comprend → **le théorème généralise à l'infini**.
- Reste pour « plate partout » : les t hors des deux familles (7, 10… —
  ceux qui exigeaient des tripartitions) et les n ≠ 2t : la conjecture
  générale `deg₆(MAJ_n) = ⌈n/2⌉` est confirmée n ≤ 20 + 32 et a
  maintenant deux squelettes infinis ; la construction tripartite
  générale est la prochaine marche (e27 candidate).
