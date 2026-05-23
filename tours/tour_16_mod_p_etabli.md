# Tour 16 — `DNF_min(MOD_p_n) = Σ_{k ≡ 0 (mod p)} C(n, k)` (✅ Établi pour P vs NP)

- **Date** : 2026-05-23
- **Proposeur** : Qwen Max
- **Réfuteur** : Claude
- **Sous-but visé** : direction ouverte Tour 16, option 4 (diversification vers
  une autre famille de fonctions).
- **Verdict** : ✅ **ÉTABLI POUR P vs NP** — cinquième objet positif du dépôt,
  application non-triviale de L13 à la famille `MOD_p`.

---

## Idée proposée (résumé fidèle)

**Mini-théorème L16.** *Pour tout `p ≥ 2` et tout `n ≥ 1`, soit
`MOD_p_n(x) = [sum(x) ≡ 0 (mod p)]`. Alors :*
- *L16.1 : `MOD_p^{-1}(1)` est un independent set du graphe `Q_n`.*
- *L16.2 : Par L13 (Tour 13), `DNF_min(MOD_p_n) = |MOD_p^{-1}(1)| =
  Σ_{0 ≤ k ≤ n, k ≡ 0 (mod p)} C(n, k)`.*
- *L16.3 : Pour `p` fixé et `n → ∞`, `|MOD_p^{-1}(1)| ~ 2^n / p`,
  super-polynomial. Donc `MOD_p_n ∉ AC⁰ d=2 polynomial`.*

---

## Vérification du Réfuteur

### 1. Reproduction indépendante du calcul

Script `tour_16_mod_p_dnf.py` exécuté indépendamment, n=4 :

```
  p |  |MOD_p^{-1}(1)|  | attendu  | independent | DNF_min
 -- | ----------------- | -------- | ----------- | -------
  2 |                 8 |        8 |     ✓       |       8
  3 |                 5 |        5 |     ✓       |       5
  4 |                 2 |        2 |     ✓       |       2
  5 |                 1 |        1 |     ✓       |       1
```

**Comptes confirmés** :
- `MOD_2_4` : C(4,0) + C(4,2) + C(4,4) = 1 + 6 + 1 = 8 ✓
- `MOD_3_4` : C(4,0) + C(4,3) = 1 + 4 = 5 ✓
- `MOD_4_4` : C(4,0) + C(4,4) = 1 + 1 = 2 ✓
- `MOD_5_4` : C(4,0) = 1 ✓ (pas de k ∈ {1,2,3,4} avec k ≡ 0 mod 5)

**Independent set vérifié** : pour MOD_3_4, distance minimale entre paires de
`MOD_3_4^{-1}(1)` = 2. ✓ (aucune paire à distance Hamming 1).

### 2. Audit des preuves

**L16.1** (`MOD_p^{-1}(1)` independent dans Q_n) :

Preuve. Soient `x, y ∈ {0,1}^n` avec `dist_H(x, y) = 1`, différant sur le bit
`i`. Alors `sum(y) = sum(x) + (1 - 2x_i) = sum(x) ± 1`. Donc
`sum(y) ≢ sum(x) (mod p)` pour `p ≥ 2`. Si `x ∈ MOD_p^{-1}(1)` (`sum(x) ≡ 0
mod p`), alors `sum(y) ≡ ±1 ≢ 0 (mod p)`, donc `y ∉ MOD_p^{-1}(1)`. ∎

Audit : ✓ correct. Argument élémentaire, valide pour tout `p ≥ 2` et tout `n`.

**L16.2** (DNF minimal par L13) : application directe de L13 (Tour 13). La
condition « `f^{-1}(1)` independent dans `Q_n` » est satisfaite par L16.1.
L13 donne alors `DNF_min(f) = |f^{-1}(1)|`. ∎

**L16.3** (asymptotique) : par le **roots of unity filter** (théorème classique
de Gauss),
$$|\mathrm{MOD}_p^{-1}(1)| = \frac{1}{p} \sum_{j=0}^{p-1} (1 + \omega^j)^n$$
où `ω = e^{2πi/p}`. Le terme `j=0` donne `2^n / p`. Les autres termes vérifient
`|1 + ω^j| < 2` strictement pour `j ≠ 0` (et `p ≥ 2`), donc sont
asymptotiquement négligeables. Donc `|MOD_p^{-1}(1)| ~ 2^n / p` pour `p` fixé.

Super-polynomial → `MOD_p_n ∉ AC⁰ d=2 polynomial`. ✓

### 3. Test des barrières

- **Relativisation** : preuve combinatoire sans oracle. ✓
- **Razborov-Rudich** : la famille `{MOD_p_n : 2 ≤ p ≤ n+1}` a au plus
  `n` éléments parmi `2^{2^n}` fonctions. Densité ≪ `2^{-O(n)}`. Non-large. ✓
- **Algébrisation** : pas d'arithmétisation. ✓

### 4. Note terminologique

Le Proposeur écrit dans ses chiffres *« MOD_2_4 (= PARITY) : 8 ✓ »*.

**Nuance** : strictement, selon la convention standard :
- `PARITY_n(x) = 1` ssi `sum(x)` est **impair** (= 1 mod 2).
- `MOD_2_n(x) = 1` ssi `sum(x) ≡ 0 (mod 2)` = **pair**.

Donc `MOD_2_n = ¬PARITY_n` au sens strict. Mais comme `Q_n` est biparti avec
classes de tailles égales, `|MOD_2^{-1}(1)| = |¬PARITY^{-1}(1)| =
|PARITY^{-1}(1)| = 2^(n-1) = 8` à `n=4`. Et `DNF_min` est le même. Le calcul
est correct ; seule la nomenclature « MOD_2 = PARITY » est imprécise.

C'est une nuance terminologique, pas mathématique. Notée mais sans impact.

### 5. Apport au dépôt

**Diversification réussie** : sortie partielle du paradigme THRESHOLD.

- **Lignée FSS** (Tours 12-15) : fonctions monotones symétriques (PARITY,
  MAJ_n, THRESHOLD_t).
- **Lignée Razborov-Smolensky** (Tour 16) : fonctions symétriques
  **non-monotones** (`MOD_p` n'est pas monotone car flipper un bit change
  `sum mod p`).

**Application non-triviale de L13** : jusqu'au Tour 16, L13 (caractérisation
par independent set de Q_n) n'avait été appliquée explicitement qu'à PARITY.
Tour 16 identifie une nouvelle famille (MOD_p) satisfaisant l'hypothèse, et
calcule la borne exacte. C'est une utilisation effective du théorème de
caractérisation comme **outil de production**.

**Ouverture vers Razborov-Smolensky 1987** : le théorème RS prouve `MOD_p ∉
AC⁰[q]` (profondeur arbitraire, modulo `q ≠ p` premiers) par la méthode
polynomiale modulaire. Tour 16 traite seulement le cas profondeur 2 par
application combinatoire de L13. C'est le **premier maillon** de la lignée RS
dans le dépôt.

### Verdict : ✅ ÉTABLI POUR P vs NP — 5e objet du dépôt

Toutes les 13 conditions (a)–(m) honorées. Théorème prouvé combinatoirement,
vérifié exhaustivement à n=4 pour `p ∈ {2,3,4,5}`, asymptotique établie par
argument classique (roots of unity filter), barrières testées et toutes
inapplicables.

---

## Nuance honnête (assumée par le Proposeur)

- **Théorème classique**, application directe de L13. Apport mathématique
  zéro vis-à-vis du front de la recherche.

- **5e itération dans la veine AC⁰ d=2** (Tours 12, 13, 14, 15-B, 16). Le
  Proposeur le note explicitement comme risque de saturation persistante.

- **Pas P vs NP.** `AC⁰ d=2 polynomial ⊊ P` est connu depuis FSS 1981 et déjà
  acquis depuis le Tour 12. Tour 16 ajoute juste de nouveaux témoins.

- **Apport pour le dépôt** : *diversification réussie de la famille de
  fonctions* (MOD au lieu de THRESHOLD), *ouverture de la lignée
  Razborov-Smolensky*, *application effective de L13* comme outil de
  production. Le théorème L13 (Tour 13) gagne donc en valeur a posteriori
  : il n'est plus seulement une caractérisation théorique mais permet
  d'établir directement de nouvelles bornes.

## Conséquences pour la suite

- **Cinq entrées** dans la section ✅ Établis pour P vs NP du cahier.
- **Saturation persistante** notée : 5 tours consécutifs dans `AC⁰ d=2`. Le
  Tour 17 devrait *vraiment* diversifier pour ne pas répéter indéfiniment
  les variations sur L13.
- **Sous-but Tour 17** : prescription forte vers **profondeur 3** (FSS-Håstad
  partiel), **formalisation Lean** d'un sous-lemme acquis, ou **Razborov 1985
  monotone CLIQUE** (lignée distincte de FSS et RS). Pas de nouvelle
  application de L13 (saturation).

## Script de vérification

[`checks/tour_16_mod_p_dnf.py`](../checks/tour_16_mod_p_dnf.py)
— livré par le Proposeur, exécuté indépendamment par le Réfuteur. Énumère
`MOD_p^{-1}(1)` pour `p ∈ {2,3,4,5}` à n=4, vérifie que c'est un independent
set de `Q_4` (distance Hamming minimale ≥ 2), applique L13 pour conclure.

**Note technique** : le script génère un `SyntaxWarning: invalid escape
sequence '\ '` (chaîne contenant `\ AC^0` non préfixée `r"..."`). Cosmétique,
n'affecte pas le résultat. Notable pour future correction.
