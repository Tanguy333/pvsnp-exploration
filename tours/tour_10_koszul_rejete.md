# Tour 10 — Conjecture C10 (préemptivement réfutée) + proposition Lean Koszul (hors-sujet)

- **Date** : 2026-05-23
- **Proposeur** : Qwen Max
- **Réfuteur** : Claude
- **Sous-but visé** : 10 conditions du Tour 9 + (i) corrigée et (k) ajoutée par
  l'utilisateur (« on reste sur P vs NP »).
- **Verdict** : ⚠️ **LACUNE RÉPARABLE** — épistémologie excellente (test préemptif
  de C10), mais le pivot Lean cible un théorème hors-sujet vis-à-vis de P vs NP.
  Réponse de l'utilisateur : recentrer vers P vs NP au Tour 11.

---

## Partie A — Conjecture C10 (intersections uniformes), préemptivement réfutée

### Idée

Raffiner C9 du Tour 9 en exploitant la structure du contre-exemple minimal
n=5 : *« pour `f` monotone equigenerated, `I_f` a une résolution pure ssi
toutes les intersections non-vides entre paires de mintermes ont la même
taille »*.

### Test préemptif (condition (j) honorée)

Le Proposeur a écrit et exécuté
[`checks/tour_10_intersection_uniform_conjecture.py`](../checks/tour_10_intersection_uniform_conjecture.py)
AVANT de soumettre la conjecture. Sur les **2110 fonctions monotones non-
constantes equigenerated sur n=5** :

| | uniform=True | uniform=False |
|---|---:|---:|
| **pure=True** | 1002 | 893 |
| **pure=False** | 175 | 40 |

- Direction *pure ⇒ uniform* : **893 contre-exemples**.
- Direction *uniform ⇒ pure* : **175 contre-exemples**.
- Total : **1068 violations** sur 2110.

**Conjecture C10 massivement réfutée dans les deux directions.**

Le Proposeur, voyant la réfutation, a **retiré C10 sans la soumettre**. C'est
le deuxième tour consécutif où (j) est respectée — confirmation que
l'épistémologie a tenu (Tour 9 → Tour 10).

### Fait empirique négatif (acquis)

> *« La caractérisation `I_f` pure ⟺ `intersections-non-vides-uniformes`
> est fausse sur n=5 (1068 contre-exemples sur 2110 fonctions
> equigenerated). »*

Cet objet rejoint la section « 📚 Acquis hors-but principal » du cahier,
avec note explicite *« Lien à P vs NP : aucun démontré »*.

---

## Partie B — Pivot proposé vers Lean (Koszul de `m_n`) — REJETÉ

### Proposition du Proposeur

Après le retrait de C10, le Proposeur a pivoté stratégiquement : *« changer de
mode, passer de la proposition spéculative à la certification mécanique »*.
Théorème cible proposé : **formaliser en Lean 4 la résolution de Koszul de
l'idéal maximal `m_n = ⟨x_1, …, x_n⟩`**, en plusieurs phases (n=2, n=3, n
quelconque).

### Pourquoi c'est un bon mouvement stratégique

- Briser le pattern « LLM-Proposeur génère conjectures plausibles → script-
  Réfuteur démolit → connaissances négatives ».
- La certification Lean est **inattaquable par calcul** : le compilateur est le
  Réfuteur ultime.
- Cumulable et alignable sur Mathlib.

### Pourquoi le théorème cible est rejeté

Le Proposeur l'admet lui-même :
> *« Distance à P vs NP : maximale, assumée. Cette proposition est
> explicitement hors-sujet vis-à-vis de la question originale du dépôt. »*

Il invoque le sous-but Tour 10 antérieur qui autorisait *« renoncer à P vs NP
pour produire un objet certifié »*. Mais ce sous-but a été **explicitement
révisé** par l'utilisateur entre le Tour 9 et le Tour 10 (commit `2a3c292`,
recadrage du cahier) :

- **(i) CORRIGÉE** : *« Le Proposeur ne peut pas renoncer à P vs NP au profit
  de mathématiques décorrelées. »*
- **(k) AJOUTÉE** : *« Toute piste doit fournir une phrase explicite liant
  l'objet proposé à P vs NP. Sans cette phrase, hors sujet. »*

Le Proposeur ne fournit aucune phrase liant Koszul de `m_n` à P vs NP, parce
qu'il n'y en a pas. La motivation invoquée (*« incarne L9.1 »*) est circulaire :
L9.1 est lui-même un acquis « hors-but principal ».

### Verdict : ⚠️ LACUNE RÉPARABLE

- **Bon** : pivot stratégique (Lean), test préemptif (j), retrait honnête de C10.
- **Mauvais** : théorème cible hors-sujet vis-à-vis de P vs NP (admis).

### Direction prescrite pour le Tour 11

Le Réfuteur (avec validation utilisateur) prescrit la cible suivante pour le
Tour 11 :

**Mini-théorème PARITY ∉ AC⁰ profondeur 2 à n petit.**

Phases :
- *Phase A1* (Python, calculable) : énumérer tous les circuits DNF/CNF
  (= AC⁰ profondeur 2) sur n=4 variables de taille bornée, montrer par calcul
  exhaustif qu'aucun ne calcule la fonction `parity_4 = x_0 ⊕ x_1 ⊕ x_2 ⊕ x_3`.
  Exhiber la **taille minimale** d'un DNF/CNF calculant `parity_4` (qui vaut
  `2^(n-1)` selon FSS, ici 8 monômes de taille 4).
- *Phase A2* (Lean, ultérieur) : formaliser l'énoncé fini comme proposition
  décidable : `∀ C ∈ AC0_depth2_size_le N, ∃ w, C(w) ≠ parity_4(w)` pour `N`
  spécifique.
- *Phase A3* (long terme, perspective) : généraliser à n quelconque, conduisant
  à Furst-Saxe-Sipser 1981 puis Håstad 1986 (switching lemma).

**Lien à P vs NP** : `PARITY ∉ AC⁰` est le premier théorème non-trivial de
borne inférieure de circuit. C'est l'ancêtre direct de Razborov 1985 (monotone
CLIQUE), Razborov-Smolensky 1987 (AC⁰[p] ≠ AC⁰[q]), et Williams 2011 (NEXP ⊄
ACC⁰) — l'unique précédent ayant franchi les trois barrières. C'est dans cette
lignée que se trouve la voie crédible vers P vs NP.

---

## Synthèse

Le Tour 10 est un **micro-progrès épistémologique** (test préemptif de C10
honoré, retrait honnête) mais aussi une **dérive de sujet** (Koszul Lean) que
le recadrage utilisateur a stoppée immédiatement. C'est le premier tour où le
**Réfuteur**, plutôt que de réfuter, *prescrit* la direction suivante de
manière explicite, après validation utilisateur.

## Acquis

- 📚 (hors-but principal) **Fait empirique négatif C10** : caractérisation
  intersection-uniforme réfutée sur n=5 (1068 contre-exemples). Documenté dans
  `checks/tour_10_intersection_uniform_conjecture.py`.
- *(aucun acquis P vs NP ce tour)*.

## Conséquences pour la suite

- Piste 10 classée **⚠️ LACUNE RÉPARABLE** + direction prescrite.
- Sous-but Tour 11 : **PARITY ∉ AC⁰ profondeur 2 sur n=4 ou n=5**, calcul
  exhaustif Python + perspective formalisation Lean.
- Conditions (a)-(k) maintenues. (l) ajoutée implicitement par la pratique :
  *« Le Proposeur doit lire la version la plus récente du cahier avant de
  soumettre. Le Réfuteur peut prescrire une direction si le Proposeur dérive. »*
