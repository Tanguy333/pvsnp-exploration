# Tour 09 — Conjecture C9 (pure ⟺ equigenerated) pour fonctions monotones

- **Date** : 2026-05-23
- **Proposeur** : Qwen Max
- **Réfuteur** : Claude
- **Sous-but visé** : 10 conditions du Tour 9 (incluant (h) effectif et (j) test empirique préalable).
- **Verdict** : ⚠️ **LACUNE RÉPARABLE** — conjecture confirmée n=4 mais **réfutée n=5** (215 contre-exemples sur 7579 fonctions). Premier tour où le Proposeur honore vraiment (h) et (j) ; et premier vrai contenu intellectuel posé par lui (non par moi).

---

## Idée proposée (résumé fidèle)

**Conjecture C9.** Pour toute fonction monotone non-constante `f : {0,1}^n → {0,1}`,
l'idéal de Stanley-Reisner `I_f` admet une résolution libre minimale **pure**
(au sens Boij-Söderberg : un seul shift par index homologique) **si et seulement si**
tous les implicants premiers de `f` ont la même taille (i.e. `I_f` est
**equigenerated** comme idéal monomial squarefree).

- **L9.1** : pure ⇒ equigenerated. Triviale par contrapositive (deux degrés
  différents → deux shifts à l'index 0 → non-pure).
- **L9.2** : equigenerated ⇒ pure. Direction non-triviale.
- **L9.3** : C9 tient pour n=5. Conjecturel.
- **L9.4** : résolution Koszul de OR_n, formalisable Lean. Classique acquis.

Le Proposeur **livre le script `checks/tour_09_equigeneration_conjecture.py`**
(première fois où (h) est vraiment honorée par lui), avec verification
n=4 : tableau de contingence parfait 95/0/0/72.

---

## Réfutation / vérification

### 1. Constat préliminaire — vrai progrès, vraiment

Premier tour où :
- **(h) effectivement honorée** : le Proposeur a écrit et exécuté son
  script avant soumission, et l'a livré dans le repo (vérifié).
- **(j) appliquée** : conjecture testée sur n=4 (167 fonctions non-constantes,
  diagonale parfaite) avant d'être proposée.
- **(i) maintenue** : renoncement explicite à P vs NP préservé.
- La conjecture est **formulée clairement** et **falsifiable** : si elle est
  vraie, c'est un théorème d'algèbre commutative ; si elle est fausse, on
  trouve un contre-exemple explicite.

Le Proposeur a entendu les 9 itérations précédentes. C'est mesurable.

### 2. Vérification indépendante à n=4

J'ai exécuté `tour_09_equigeneration_conjecture.py` du Proposeur :

```
Tableau de contingence (n=4, 167 fonctions non-constantes) :
                |  equi=True | equi=False
  --------------|------------|------------
  pure=True     |         95 |          0
  pure=False    |          0 |         72
```

**Diagonale parfaite confirmée.** L'atlas du Tour 8 (95 fonctions pures
identifiées) correspond exactement à la classe equigenerated.

### 3. Extension à n=5 — la conjecture est réfutée

J'ai écrit [`checks/tour_09_extension_n5.py`](../checks/tour_09_extension_n5.py)
pour étendre le test. Défi technique : énumérer les **7581 fonctions monotones
n=5** (Dedekind M(5)) sans brute force `2^32`. Solution : récursion de Dedekind
— `f` monotone sur n vars ↔ paire `(f_0, f_1)` de fonctions monotones sur n-1
vars avec `f_0 ≤ f_1`. Permet de générer M(5) en quelques millisecondes.

**Résultat (calcul, ~6 secondes) :**

```
Tableau de contingence (n=5, 7579 fonctions non-constantes) :
                |  equi=True | equi=False
  --------------|------------|------------
  pure=True     |       1894 |          0
  pure=False    |        215 |       5470
```

- **L9.1** (pure ⇒ equigen) : **0 contre-exemple** sur 7579. ✓ (cohérent avec
  la preuve triviale par contrapositive).
- **L9.2** (equigen ⇒ pure) : **215 contre-exemples** sur 7579. ✗

**La conjecture C9 est donc réfutée à n=5.** L9.2 ne tient pas en général.

### 4. Contre-exemple canonique explicite

Le contre-exemple le plus petit (en nombre de mintermes) :

> **`f = (x_1 ∧ x_2 ∧ x_3) ∨ (x_1 ∧ x_2 ∧ x_4) ∨ (x_0 ∧ x_3 ∧ x_4)`**

- 3 mintermes, tous de taille 3 → **equigenerated**.
- `I_f = (x_1 x_2 x_3, x_1 x_2 x_4, x_0 x_3 x_4)`.

**Calcul des syzygies linéaires :**

| Paire de générateurs | Variable(s) partagée(s) | Syzygie | Degré |
|---|---|---|---|
| g_1, g_2 | x_1, x_2 | α = x_4 g_1 − x_3 g_2 | 4 |
| g_1, g_3 | x_3 | β = x_0 x_4 g_1 − x_1 x_2 g_3 | 5 |
| g_2, g_3 | x_4 | γ = x_0 x_3 g_2 − x_1 x_2 g_3 | 5 |

**Relation entre syzygies** : `β − γ = x_0 · α` (vérification directe).
Donc parmi `{α, β, γ}`, seules 2 syzygies sont minimales (par exemple α et β,
ou α et γ). α est de degré 4, β/γ de degré 5.

**Conclusion :**
- `β_{0,3}(I) = 3` (les 3 générateurs)
- `β_{1,4}(I) = 1` (la syzygie linéaire α)
- `β_{1,5}(I) = 1` (la syzygie quadratique restante)

**L'index homologique 1 a deux shifts (4 et 5).** Résolution non-pure. Mais
`I` est equigenerated. C9-L9.2 est réfutée.

### 5. Pourquoi cela arrive à n=5 et pas à n=4

Sur n=4, il y a au plus C(4, k) = au plus 6 implicants premiers pour k=2.
La structure combinatoire est trop contrainte pour que des syzygies à
deux degrés différents puissent coexister minimallement.

Sur n=5, on peut combiner des paires de générateurs partageant 2 variables
(syzygies linéaires de degré 4) ET des paires partageant 1 variable
(syzygies quadratiques de degré 5), à l'intérieur du même idéal. Cette
hétérogénéité produit les contre-exemples.

C'est un phénomène **combinatoire-algébrique** précis : la rigidité de
n=4 cache un comportement plus riche qui apparaît à n=5. Le Proposeur
avait anticipé ce risque (Aveu 1 : *« il est plausible que la converse
L9.2 échoue à n=5 ou plus grand »*).

### 6. Acquis positif

C'est le **deuxième objet positif** du dépôt (après l'atlas n=4 du Tour 8) :

> ✅ **Théorème (établi par calcul exhaustif).** La direction L9.1 (pure ⇒ equigen)
> est vraie pour toute fonction monotone (preuve trivial par contrapositive).
>
> ⚠️ **Fait empirique.** La direction L9.2 (equigen ⇒ pure) est vraie sur n=4
> (167 fonctions, 0 exception) mais **fausse sur n=5** (7579 fonctions,
> **215 exceptions**). Contre-exemple minimal explicite : `(x_1∧x_2∧x_3) ∨
> (x_1∧x_2∧x_4) ∨ (x_0∧x_3∧x_4)`.

C'est un fait mathématique précis, vérifié par calcul, et reproductible.
Aucune prétention asymptotique, aucune extrapolation. Pure observation.

### 7. Test des barrières

Inapplicables, comme l'a noté le Proposeur. Objet fini, pas d'oracle, pas
de borne inférieure asymptotique.

### 8. Verdict : ⚠️ LACUNE RÉPARABLE (4e consécutive)

**Pourquoi pas FAILLE FATALE :**
- La conjecture est posée proprement (testable, falsifiable, et testée).
- (h) et (j) honorées pour la première fois par le Proposeur.
- L9.1 reste vraie (théorème acquis).
- L'observation empirique « L9.2 vraie n=4, fausse n=5, 215 exceptions »
  est un **objet positif** ajouté au dépôt.

**Pourquoi pas SURVIT :**
- L9.2 est réfutée à n=5. La conjecture initiale C9 ne tient pas.

**La lacune précise.** Pour reformuler correctement la conjecture, on
pourrait essayer :
- *« I_f a résolution pure ssi I_f est equigenerated ET [condition
  combinatoire à identifier] »* — condition à découvrir.
- Examiner les **215 contre-exemples** sur n=5 et identifier ce qui les
  distingue des 1894 cas où equigen ⇒ pure tient.

Cette analyse fine est un programme de recherche d'algèbre commutative
intéressant en soi, indépendant de P vs NP.

---

## Nuance honnête

**C'est le meilleur tour à ce stade.** Pour la première fois, le Proposeur :
1. A écrit et exécuté un script avant soumission ;
2. A présenté une conjecture clairement falsifiable ;
3. A correctement anticipé le risque de réfutation (Aveu 1 mentionne
   explicitement « il est plausible que L9.2 échoue à n=5 ») ;
4. A reconnu la distance à P vs NP sans s'en cacher ;
5. A produit du contenu **original** (la conjecture est sienne, pas une
   reformulation de programme connu) — *probablement* original (Aveu 2
   mentionne le besoin de vérification bibliographique).

La conjecture est réfutée, mais **l'épistémologie est correcte** : poser,
tester, observer, ajuster. La boucle adverse fait son travail, mais cette
fois en partenariat constructif plutôt qu'en démolition pure.

## Conséquences pour la suite

- Piste 9 classée **⚠️ LACUNE RÉPARABLE** dans le cahier de bord, avec note
  positive sur l'épistémologie.
- **Deuxième objet positif acquis** : le fait empirique (L9.1 toujours, L9.2
  à n=4 seulement, contre-exemple n=5 explicite).
- Question ouverte mathématique précise ajoutée : *quelles conditions
  combinatoires distinguent les 1894 cas où equigen ⇒ pure tient des 215
  cas où elle échoue ?*
- Sous-but Tour 10 : continuer dans cette épistémologie. Soit raffiner C9
  en C9' (caractérisation plus fine), soit pivoter vers la formalisation
  Lean du L9.4 (résolution Koszul de OR_n).

## Scripts de vérification

- [`checks/tour_09_equigeneration_conjecture.py`](../checks/tour_09_equigeneration_conjecture.py)
  — script du Proposeur, vérification à n=4 (95/0/0/72).
- [`checks/tour_09_extension_n5.py`](../checks/tour_09_extension_n5.py)
  — extension du Réfuteur à n=5, génération via Dedekind, identification
  des 215 contre-exemples à L9.2.
