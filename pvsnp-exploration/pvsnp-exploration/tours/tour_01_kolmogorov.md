# Tour 01 — Incompressibilité de Kolmogorov des témoins

- **Date** : 2026-05-23
- **Proposeur** : Qwen Max
- **Réfuteur** : Claude
- **Sous-but visé** : choisir une direction + cartographier les barrières ; proposer une première idée mobilisant la méta-complexité.
- **Verdict** : ❌ **FAILLE FATALE**

---

## Idée proposée (résumé fidèle)

Attaquer P vs NP par la **compressibilité algorithmique des témoins** plutôt que
par la structure des circuits. Formaliser le fossé vérification/résolution comme
une impossibilité de « décompresser » en temps polynomial l'information d'un
témoin valide, pour une famille dense d'instances.

Squelette de l'argument :

- **Lemme 1 (incompressibilité)** : pour une distribution naturelle de 3-SAT au
  seuil de phase, tout témoin valide `w` satisfait `K^{n^c}(w) ≥ Ω(n)`
  (complexité de Kolmogorov à ressources bornées, **inconditionnelle**).
- **Lemme 2 (compression induite par P)** : si `SAT ∈ P`, alors par
  auto-réductibilité on construit `w` dont la description « code de A + x »
  donne `K_poly(w) = O(log n)`.
- **Confrontation** : sous `P = NP`, le même témoin aurait simultanément une
  complexité `O(log n)` et `Ω(n)` → contradiction → `P ≠ NP`.

Barrière revendiquée comme franchie : **preuves naturelles** (l'argument porte
sur le contenu informationnel des témoins, pas sur la table de vérité de `f`).

Aveux du Proposeur : (1) mur cas moyen / pire cas ; (2) saut non justifié au
Lemme 2 sur les préfixes intermédiaires ; (3) conjecturalité du Lemme 1.

---

## Réfutation

### 1. Reformulation
Montrer que si SAT ∈ P, l'auto-réductibilité rendrait les témoins compressibles,
contredisant leur incompressibilité algorithmique — d'où P ≠ NP.

### 2. Le point de rupture : équivoque conditionnel / inconditionnel
Le Lemme 2 est faux tel qu'énoncé. Pour reconstruire `w` à partir de
« (code de A, x) », il faut inclure **x**, de taille poly(n) — donc
`Kt(w) ≤ poly(n)`, **jamais** `O(log n)`. Ce que P fournit réellement, c'est
`Kt(w | x) = O(1)` : une complexité **conditionnelle**. Or le Lemme 1 borne le
Kt **inconditionnel**. La « confrontation » oppose deux quantités distinctes. Le
« et donc » non justifié est exactement à la jonction des deux lemmes.

### 3. La contradiction s'évapore dans les deux mises en cohérence
- **Tout inconditionnel** : Lemme 1 vrai (Ω(n)), Lemme 2 faux (poly(n), pas log n) → pas de contradiction.
- **Tout conditionnel (sachant x)** : Lemme 2 vrai (O(1)), Lemme 1 faux (le témoin lex-premier est *déterminé par x*, donc K(w|x) petit) → pas de contradiction.

L'argument ne « marche » qu'en panachant inconditionnel (L1) et conditionnel
(L2). Le fossé entre les deux **est** P vs NP → circularité. Non comblable : P ne
fournit structurellement qu'une compression conditionnelle.

### 4. Barrières — celle qui n'a pas été vue : la RELATIVISATION
Tout l'outillage (Kt à ressources bornées, auto-réductibilité, recherche↔décision)
**relativise**. Relativisé à un oracle A, l'argument « prouverait » identiquement
`P^A ≠ NP^A` pour tout A — alors qu'il existe des oracles avec `P^A = NP^A`
(Baker–Gill–Solovay). Donc, indépendamment du §2, l'argument ne peut
structurellement pas trancher P vs NP. Le Proposeur se félicitait d'éviter les
preuves naturelles (cadre de toute façon non pertinent ici) tout en fonçant dans
la relativisation sans la mentionner.

### 5. Verdict : FAILLE FATALE
Irrécupérable comme tentative de séparation inconditionnelle : sophisme
conditionnel/inconditionnel (circulaire) + argument relativisant (BGS).

**Nuance honnête** : le programme sous-jacent (méta-complexité, Kt des témoins,
MCSP) est réel et actif, mais il porte sur des bornes **conditionnelles** et la
complexité **en moyenne**, jamais sur une obstruction inconditionnelle pire-cas.

---

## Conséquences pour la suite
- Classé **❌ Réfuté** dans le cahier de bord (section 3).
- Question ouverte ouverte par ce tour : *existe-t-il une notion de complexité
  des témoins qui ne relativise pas* (arithmétisation à la Williams) ?
- Contrainte ajoutée au tour 2 : toute idée doit démontrer son caractère
  non-relativisant.
