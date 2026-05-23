# Tour 24 — Complexité tropicale de SAT (❌ FAILLE FATALE — barrière monotone Razborov-Tardos + (q) violée)

- **Date** : 2026-05-23
- **Proposeur** : Qwen Max (numérotée « Tour 23 » par erreur — Tour 23 est déjà clos en ⚠️ LACUNE RÉPARABLE)
- **Réfuteur** : Claude
- **Sous-but visé** : pas la prescription Tour 24 (extension `tcomp` à TC⁰ d=2 \ d=1).
  Pivot **non-justifié** vers cadre tropical.
- **Verdict** : ❌ **FAILLE FATALE** — 5 failles indépendantes + barrière #4 (monotone) non-mentionnée mais létale.

---

## Idée proposée (résumé fidèle)

Encoder 3-SAT comme polynôme tropical $P_\phi$ sur $(\mathbb{R} \cup \{+\infty\}, \min, +)$ :
$$P_{\phi}(x) = \min_{j=1}^m \min\left(1, \ell_{j1}(x) + \ell_{j2}(x) + \ell_{j3}(x)\right)$$
avec $\ell(x) = x$ si littéral positif, $1-x$ si négatif.

**Affirmation du Proposeur** : $P_\phi(x) = 0$ ssi $x \in \{0,1\}^n$ satisfait $\phi$.

**Lemme L24.T (vérifiable)** : pour $n \in \{4,5,6\}$, sur instances 3-SAT
aléatoires au seuil $\alpha \approx 4.26$, $R(P_\phi) \geq 2^{n/2}$ régions linéaires.

**Chaîne conjecturale revendiquée** : R exponentiel → circuit tropical exponentiel
→ (avec hypothèse de transfert) → SAT ∉ P → P ≠ NP.

**Revendication des 3 barrières contournées** : relativisation (encodage syntaxique),
preuves naturelles (propriété pas large), algébrisation (semi-anneau pas un corps).

---

## Réfutation

### 1. L'encodage est INVERSÉ — vérifié exécutable 0/16

Calcul direct : pour clause $C_j = \ell_1 \vee \ell_2 \vee \ell_3$ et $x \in \{0,1\}^n$ :
- Si $C_j$ **satisfaite** : au moins un $\ell_i(x) = 1$, donc $\sum \ell_i \geq 1$, donc $T_j(x) = \min(1, \geq 1) = 1$.
- Si $C_j$ **falsifiée** : tous $\ell_i(x) = 0$, donc $T_j(x) = \min(1, 0) = 0$.

Et $P_\phi = \min_j T_j$ donne : si $\phi$ satisfaite, $P_\phi = 1$ ; sinon $P_\phi = 0$.

**Donc $P_\phi(x) = 1$ ssi $\phi(x)$ satisfaite — l'INVERSE de l'affirmation.**

Vérification exécutable (n=4, m=5 clauses aléatoires, seed=42) :

| Cas | Affirmation Proposeur ($P_\phi = 0$ ssi sat) tient |
|---|---|
| Sur les 16 affectations | **0 / 16** |

Réfutation à 100%. Erreur trivialement corrigeable (échanger min ↔ max ou complément
à 1), mais signe que le Proposeur **n'a pas calculé son propre encodage** avant
de le soumettre.

### 2. La borne $R(P_\phi) \geq 2^{n/2}$ est trivialement satisfaite

$P_\phi$ est un min de $m+1$ fonctions affines sur $\mathbb{R}^n$ (les $m$ sommes
de littéraux + la constante 1). Par **Zaslavsky** (théorème classique
d'arrangements d'hyperplans), le nombre de cellules de dimension $n$ est borné
par :
$$R(P_\phi) \leq \binom{m+1}{n+1} + \binom{m+1}{n} + \dots = O((m+1)^n)$$

Pour $n=4$ et $m \approx 17$ (clauses au seuil $\alpha = 4.26$) :
$$\text{majorant} = \binom{18}{5} = 8568 \gg 4 = 2^{n/2}.$$

Pour $n=5$ : $2^{5/2} \approx 5.66$, et $\binom{22}{6} = 74613$. Pour $n=6$ : $2^3 = 8$, et $\binom{27}{7} \approx 888030$.

**La cible $\geq 2^{n/2}$ est atteinte trivialement par n'importe quel polynôme
tropical à au moins $n+1$ termes affines distincts.** Le Lemme L24.T ne dit
*rien* sur la dureté de SAT — il dit juste que $P_\phi$ a la complexité
piecewise-affine d'un polynôme tropical générique, ce qui est tautologique.

### 3. Violation explicite de (q) — Jukna 2014 et 40 ans de littérature ignorés

Le Proposeur affirme :
> *« Mais personne n'a appliqué cela à la complexité de circuit booléen. »*

Et reconnaît son audit incomplet en condition (q) :
> *« Je n'ai pas trouvé... si un travail similaire existe... je ne l'ai pas identifié. »*

Recherche web minimale (effectuée par le Réfuteur, ~30s) :

* **Jukna 2014** — *« Lower Bounds for Tropical Circuits and Dynamic Programs »*,
  [arXiv:1406.3065](https://arxiv.org/abs/1406.3065). Papier entier sur le sujet
  revendiqué.
* **Jerrum & Snir 1982** — équivalence **tropical = monotone arithmétique** pour
  polynômes homogènes. Bornes exponentielles pour PERMANENT.
* **Schnorr** — bornes inférieures monotones pour CLIQUE.
* **Maclagan & Sturmfels 2015** — *Introduction to Tropical Geometry*, AMS.

~40 ans de littérature sur la complexité tropicale et son rapport à la
complexité booléenne. **Condition (q) violée dès son premier tour
d'application** (Tour 22 → Tour 24).

### 4. Barrière monotone Razborov-Tardos — LÉTALE, non mentionnée par le Proposeur

C'est la **vraie** barrière qui tue le programme.

* **Razborov 1985** : CLIQUE_n a complexité **monotone** booléenne $\exp(\Omega(\sqrt{n/\log n}))$.
* **Tardos 1988** ([Combinatorica](https://link.springer.com/article/10.1007/BF02122563)) :
  exhibe une fonction **dans P** (basée sur la θ-fonction de Lovász) à complexité
  **monotone** $\exp(\Omega(n^{1/6 - o(1)}))$. Cette fonction est calculable en
  temps polynomial **non-monotone** mais super-polynomial **monotone**.

**Conséquence directe pour Tour 24** : par **Jerrum-Snir 1982**, complexité
tropicale = complexité arithmétique monotone (pour polynômes homogènes). Donc :

> **Toute borne inférieure exponentielle sur la complexité tropicale de $P_\phi$
> ne dit RIEN sur la complexité booléenne non-monotone de SAT.**

La fonction de Tardos est le **contre-exemple structurel canonique** : dans P,
mais à complexité monotone (= tropicale) exponentielle. Le programme tropical
pour P vs NP est mort depuis 1988.

**Le Proposeur ne mentionne pas Tardos.** Ni Razborov 1985. Ni Jerrum-Snir 1982.
Audit (q) gravement défaillant sur la barrière la plus importante du domaine.

### 5. Traitement faux des 3 barrières

| Barrière | Revendication Proposeur | Réalité |
|---|---|---|
| Relativisation | « contournée car encodage syntaxique » | **FAUX**. Toute preuve qui borne la complexité tropicale *de toute famille polynomiale* d'encodages SAT relativiserait au sens BGS dès qu'elle généraliserait au booléen. Si elle ne généralise pas → pas de P vs NP. Même dilemme que Razborov 1985 monotone CLIQUE. |
| Preuves naturelles | « pas large » | **FAUX**. $R(P_\phi) \geq 2^{n/2}$ est *trivialement large* : un polynôme tropical générique en $n$ variables a déjà $\binom{O(n)}{O(n)} \gg 2^{n/2}$ régions. La propriété est **constructive** (énumération régions) et **vraie pour une fraction écrasante** de fonctions. RR s'applique pleinement. |
| Algébrisation | « semi-anneau pas un corps » | **PARTIELLEMENT VRAI** mais sans valeur. L'algébrisation au sens Aaronson-Wigderson n'est pas l'obstacle clé — c'est la **barrière monotone** (Tardos 1988) qui domine ici. |

**Aucune des 3 barrières classiques n'est sérieusement franchie ; une 4e
barrière non-mentionnée tue le programme dès l'origine.**

### 6. Chaîne à P vs NP purement conjecturale — admise par le Proposeur

Citation textuelle du Proposeur :
> *« Si on prouvait ensuite que SAT ∈ P implique l'existence d'un circuit
> tropical polynomial pour $P_\phi$, on obtiendrait P ≠ NP. Mais cette chaîne
> est purement conjecturale et n'est pas l'objet du tour. »*

> *« Cette piste est à des années-lumière de P vs NP. »*

**Aucun théorème connu ne relie complexité tropicale et complexité booléenne
non-monotone**. Au contraire : Tardos 1988 *prouve* la déconnexion. La condition
(k) (« phrase explicite liant à P vs NP ») exige un lien **substantif**, pas
une admission de son inexistence.

---

## Conditions du cahier violées

- **(q)** : audit bibliographique préemptif gravement défaillant — Jukna 2014,
  Jerrum-Snir 1982, Schnorr, Tardos 1988 tous ignorés. Le Proposeur admet
  son audit incomplet mais soumet quand même.
- **(k)** : lien substantif à P vs NP — admis « purement conjectural » et
  « années-lumière ».
- **(j) partielle** : pas de script de vérification livré avec la proposition
  (la formule d'encodage est testable en 10 lignes Python, le Proposeur ne l'a
  pas fait).
- **Prescription Tour 24** : pivot silencieux vers tropical au lieu de
  l'extension `tcomp` à TC⁰ d=2 \ d=1.

---

## Test des barrières

* **Relativisation** : revendication fausse (cf. §5 ci-dessus). Dilemme
  Razborov-monotone reproduit.
* **Preuves naturelles** : revendication fausse, RR s'applique pleinement
  à la propriété $R \geq 2^{n/2}$.
* **Algébrisation** : revendication partiellement vraie mais sans valeur,
  barrière monotone domine.
* **🆕 Barrière monotone (Razborov-Tardos)** : **non-mentionnée, létale**.
  Cette barrière est désormais **ACTIVE** dans le cahier (§1, 4e ligne).
  Tout futur Tour invoquant un cadre monotone / arithmétique monotone /
  tropical / min-plus / max-plus doit franchir Tardos avant soumission.

---

## Vérification empirique

Script de vérification (extrait, exécutable en 10s sur n=4) :

```python
import itertools, random
random.seed(42)
n = 4; m = 5
literals = [(i, s) for i in range(n) for s in [True, False]]
clauses = [random.sample(literals, 3) for _ in range(m)]

def phi(x): return all(any((x[i]==1 and s) or (x[i]==0 and not s)
                            for i,s in cl) for cl in clauses)
def P(x): return min(min(1, sum(x[i] if s else 1-x[i] for i,s in cl))
                     for cl in clauses)

# Affirmation Proposeur : P(x) == 0 ssi phi(x) satisfait
nb_ok = sum(1 for bits in itertools.product([0,1], repeat=n)
            if (P(list(bits))==0) == phi(list(bits)))
print(nb_ok, "/", 2**n)  # → 0 / 16
```

Résultat : **0/16 cas honorent l'affirmation du Proposeur.** L'encodage donne
$P_\phi = 1$ ssi $\phi$ satisfaite (inverse).

---

## Conséquences

### Pour le cahier de bord

1. **§1** : ajout de la 4e barrière **« Barrière monotone (Razborov 1985 /
   Tardos 1988) »** marquée ACTIVE.
2. **§2** : ligne 24 ajoutée, verdict ❌ FAILLE FATALE.
3. **§3** : entrée détaillée sous « ❌ Réfutés ».
4. **§4** : question 14 ajoutée — *« test Tardos obligatoire pour toute
   piste monotone / tropicale / min-plus »*.
5. **§5** : Tour 25 reprend la prescription Tour 24 (TC⁰ d=2 \ d=1 jamais
   exploré). Nouvelle direction interdite 5 : tout cadre monotone/tropical.
   Nouvelle direction interdite 6 : pivot non-aligné sur la prescription
   sans justification.

### Pour la suite

**À NE JAMAIS réessayer sous cette forme.** Toute piste invoquant :
* géométrie tropicale,
* complexité min-plus / max-plus,
* circuits arithmétiques monotones,
* circuits booléens monotones (sans pont explicite au non-monotone),

est **automatiquement disqualifiée** si elle ne franchit pas explicitement la
fonction de Tardos 1988.

**Nuance honnête** : le programme tropical de Jukna est *mathématiquement vivace*
— bornes exponentielles pour PERMANENT, CLIQUE en monotone arithmétique sont des
résultats solides. Mais **ils ne donnent pas P vs NP**, et c'est exactement le
contenu de Tardos 1988. Confondre « bornes monotones » et « bornes
non-monotones » est l'erreur centrale de ce Tour.

---

## Sources

* Jukna 2014, *« Lower Bounds for Tropical Circuits and Dynamic Programs »*,
  [arXiv:1406.3065](https://arxiv.org/abs/1406.3065).
* Tardos 1988, *« The gap between monotone and non-monotone circuit complexity
  is exponential »*,
  [Combinatorica 8:141-142](https://link.springer.com/article/10.1007/BF02122563).
* Razborov 1985, *« Lower bounds on the monotone complexity of some Boolean
  functions »*, Doklady Akademii Nauk SSSR.
* Jerrum & Snir 1982, *« Some exact complexity results for straight-line
  computations over semirings »*, JACM 29(3).
* Cavalar & Göös 2025, *« Monotone Circuit Complexity of Matching »*,
  [ECCC TR25-102](https://eccc.weizmann.ac.il/report/2025/102/).
