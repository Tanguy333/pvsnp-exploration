# Tour 11 — Proposition « lifting + Tseitin/expandeur + KW pour 2COL » (rejetée)

- **Date** : 2026-05-23
- **Proposeur** : Qwen Max
- **Réfuteur** : Claude
- **Sous-but visé** : prescription Tour 11 du recadrage = `PARITY_n ∉ AC⁰ profondeur 2` sur n=4.
- **Verdict** : ⚠️ **LACUNE RÉPARABLE** — direction correcte sur P vs NP, mais
  erreur factuelle élémentaire (2COL ∈ P) + (j) régressée + chaîne conjecturale.
  **Rejet maintenu par l'utilisateur**. Prescription PARITY ∉ AC⁰ réaffirmée.

---

## Idée proposée (résumé fidèle)

Borne inférieure de profondeur de formule monotone pour une fonction NP via la
chaîne :

1. Tseitin `T_{G_n}` sur graphe expandeur 3-régulier `G_n` : `Width(T_{G_n}) = Ω(n)` (Ben-Sasson-Wigderson 2001).
2. Lifting avec gadget XOR de log-largeur : `D^cc(T ∘ XOR_b^N) ≥ Ω(Width · b)` (Raz-McKenzie 1999, Göös-Pitassi-Watson 2018).
3. Karchmer-Wigderson : transformer la borne de communication en borne de profondeur de formule monotone pour `2COL_G` (« il existe une 2-coloration valide du graphe »).
4. Conclusion : `D_m(2COL_{G_n}) ≥ Ω(n log n)`, au-delà de la borne triviale `Ω(n)`.

Test empirique préemptif annoncé sur Tseitin n=4, 6, 8 — **mais non livré**.

---

## Réfutation

### 1. Conditions formelles partiellement honorées

- (a) classe restreinte : formules monotones. ✓
- (b)(c) non-relativisant, non-algébrisant : revendiqués avec justification correcte (lifting theorems sont effectivement non-relativisants et non-algébrisants).
- (d)(e)(g) invariance logique, sauts polynomiaux, encodage non-trivialisant : OK.
- (f) contribution technique : programmée mais non livrée.
- (i) corrigée : lien à P vs NP explicite. ✓
- (j) **RÉGRESSÉE** : test préemptif annoncé mais aucun script livré, aucun résultat numérique. Les Tours 9 et 10 avaient honoré (j) effectivement.
- (k) phrase explicite reliant à P vs NP : ✓
- (l) lecture du cahier : ✓ (référence à Question Ouverte §9).

### 2. Erreur factuelle décisive — 2-COLORATION est dans P

Le Proposeur écrit :
> *« la fonction caractéristique du "il existe une 2-coloration valide du graphe" — fonction monotone dans une sous-classe NP. »*

**Faux.** 2-COLORATION = test de bipartiteness, **dans P** depuis les années 1970 (BFS/DFS linéaire). Pas NP-complet. 3-COLORATION l'est, CLIQUE_k l'est, mais pas 2COL.

Donc l'objet final ciblé n'est **pas dans NP \ P**. Toute borne `Ω(n log n)` sur une fonction *dans P* serait certes intéressante en soi (au-delà de Razborov 1985 sur CLIQUE), mais elle ne contribue pas à P vs NP de la manière revendiquée.

### 3. Erreur de cadre — 2COL n'est pas naturellement monotone

Deux encodages possibles, aucun ne marche :

- **Input = coloration des sommets** (n bits, x_i ∈ {0,1} = couleur du sommet i) : `f(x) = 1` ssi pour chaque arête (i,j), `x_i ≠ x_j`. Flipper `x_i` peut faire passer f de 0 à 1 ou inversement. **Pas monotone.**

- **Input = présence/absence d'arêtes** (m = C(n,2) bits) : `f(graphe) = 1` ssi bipartite. Ajouter une arête peut détruire la bipartiteness. **Anti-monotone**, donc équivalente à monotone par complémentation, mais alors c'est `f = NON-bipartite = existe-un-cycle-impair`, pas 2COL.

Karchmer-Wigderson s'applique aux fonctions monotones. Le Proposeur n'a pas identifié quelle fonction monotone précise il vise.

### 4. La chaîne L10.5 est conjecturale — pattern récurrent

Aveu 2 du Proposeur : *« L10.5 n'est PAS prouvé... C'est exactement le type de saut conjectural qui a tué les Tours 4, 7, 9. Je le signale en avance pour ne pas refaire l'erreur. »*

Signaler le risque ne le réduit pas. C'est le **pattern conjecture-pont** qui a tué 9 itérations sur 10. Le Proposeur le reconnaît mais ne le contourne pas.

### 5. Risque de redondance avec Garg-Göös-Knop-Watson 2018

Le Proposeur identifie lui-même ce risque (Aveu 6). Sans vérification bibliographique préalable, la « contribution expositoire » annoncée peut être un travail déjà publié.

### 6. Verdict : ⚠️ LACUNE RÉPARABLE

- **Bon** : direction correcte (cadre lifting + KW + Tseitin/expandeur réellement en lien avec P vs NP), conditions formelles (i)+(k)+(l) honorées.
- **Mauvais** : erreur factuelle (2COL ∈ P), erreur de cadre (monotonicité), chaîne conjecturale, (j) régressée, redondance non vérifiée.

**Réparations possibles :**
- Remplacer 2COL par **CLIQUE_k** (NP-complète et monotone, c'est exactement la fonction de Razborov 1985).
- Livrer effectivement le test empirique.
- Vérifier la littérature GGKW 2018 et la chaîne L10.5.

Mais ces réparations sont substantielles. Et après 10 itérations dont 7 avec verdict ⚠️ ou ❌, la patience est limitée.

### 7. Décision utilisateur — Option 1

L'utilisateur **maintient la prescription Tour 11** du recadrage :

> Mini-théorème `PARITY_n ∉ AC⁰ profondeur 2` sur n=4 par calcul exhaustif Python.

Cette cible est :
- **Beaucoup plus simple** (énumération de DNF/CNF sur n=4 variables).
- **Pleinement aligné** sur P vs NP (lignée FSS → Razborov-Smolensky → Williams 2011).
- **Livrable en 1 script** de ~100 lignes Python.
- **Sans chaîne conjecturale** : la borne `2^(n-1)` est connue et exacte pour cette classe.

La proposition lifting+KW reste **un programme intéressant** mais dépasse le cadre de la boucle adverse à un Proposeur LLM. Si quelqu'un veut s'y attaquer sérieusement, il doit y travailler en mode recherche, pas en mode tour-par-tour avec corrections lourdes à chaque itération.

---

## Conséquences pour la suite

- Piste 11 classée **⚠️ LACUNE RÉPARABLE — rejetée par décision utilisateur**.
- Prescription Tour 12 : **identique à la prescription Tour 11 du recadrage** = `PARITY_n ∉ AC⁰ profondeur 2` sur n=4.
- Toute nouvelle proposition d'algèbre commutative décorrelée ou de variante CSP/lifting sera rejetée d'office.
- Le Proposeur a démontré qu'il peut produire des cadres conceptuels corrects (lifting+KW est légitime) mais qu'il fait encore des erreurs factuelles élémentaires (2COL ∈ P, niveau cours de licence en complexité).
- La boucle adverse maintient sa **prescription stricte** : revenir à PARITY ∉ AC⁰ jusqu'à ce qu'un livrable concret soit produit.

## Note méthodologique

C'est la **deuxième fois consécutive** (Tour 10 = Koszul Lean, Tour 11 = lifting/2COL) que le Réfuteur doit *prescrire* la direction plutôt que réfuter une proposition cohérente. C'est un changement de mode mesurable du dépôt :

> **Tours 1-9** : le Proposeur propose, le Réfuteur démolit par calcul.
> **Tours 10-11** : le Réfuteur doit aussi guider le Proposeur vers les bonnes cibles, parce que le Proposeur ne sait plus quoi proposer qui soit à la fois lié à P vs NP et accessible à la boucle.

C'est cohérent avec la trajectoire prévue : après 9 itérations de réfutation pure, la boucle a épuisé l'espace des « grandes idées spéculatives » et doit se rabattre sur des cibles techniques précises et bornées. PARITY ∉ AC⁰ sur n=4 en est une.
