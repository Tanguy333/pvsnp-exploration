# Cahier de bord — Exploration P vs NP

> Document vivant. À joindre en contexte à **chaque** tour, pour le Proposeur comme pour le Réfuteur.
> Règle d'or : on ne réexplore jamais une impasse déjà documentée. On mesure le progrès par la compréhension accumulée, pas par « a-t-on la preuve ».

---

## 0. Méta

- **Question** : tout problème dont une solution candidate est vérifiable en temps polynomial est-il aussi résoluble en temps polynomial ? (P vs NP)
- **Direction choisie** : séparation **P ≠ NP**, via une classe restreinte à structure algébrique/géométrique ; cadre principal = complexité descriptive, ouverture GCT ; outils encouragés = méta-complexité / Kolmogorov.
- **Démarré le** : 2026-05-23
- **Dernière mise à jour** : 2026-05-23 (fin tour 1)
- **Nombre de tours effectués** : 1

---

## 1. Barrières connues (à garder sous les yeux en permanence)

| Barrière | En une ligne | Statut dans notre exploration |
|---|---|---|
| Relativisation (Baker–Gill–Solovay) | Une preuve qui « relativise » ne peut pas trancher P vs NP. | **ACTIVE** — a tué la piste 1. Tout outil relativisant (Kt, auto-réductibilité, recherche↔décision) est suspect. Exiger des techniques non-relativisantes (ex. arithmétisation à la Williams). |
| Preuves naturelles (Razborov–Rudich) | Les bornes inférieures « naturelles » échouent sous hypothèses cryptographiques standard. | Pertinente uniquement pour les arguments de type table de vérité / circuit. Ne s'applique pas aux arguments purement informationnels — donc « l'éviter » ne prouve rien en soi. |
| Algébrisation (Aaronson–Wigderson) | Généralise la relativisation aux techniques algébriques. | À surveiller dès qu'on mobilise l'arithmétisation. Non encore rencontrée frontalement. |

> Toute idée nouvelle DOIT dire laquelle de ces barrières elle prétend franchir, et comment. **Et explicitement traiter la relativisation.**

---

## 2. Pistes explorées

| # | Idée (résumé en 1 ligne) | Barrière visée | Verdict du Réfuteur | Statut |
|---|---|---|---|---|
| 1 | Incompressibilité (Kt) des témoins SAT : P comprimerait les témoins, contredisant leur incompressibilité | Preuves naturelles (revendiqué) | Équivoque K(w) vs K(w\|x) ; argument relativisant | ❌ **FAILLE FATALE** |
| 2 |  |  |  | *(à venir)* |

---

## 3. Lemmes et résultats

### ✅ Établis (vérifiés / démontrés rigoureusement)
- *(aucun pour l'instant)*

### ❓ Conjecturaux (plausibles mais non prouvés)
- *(aucun retenu pour l'instant)*

### ❌ Réfutés (faux — et pourquoi, pour ne pas y revenir)
- **Piste 1 — « contradiction de compressibilité des témoins ».** Le sophisme central : la confrontation oppose un Kt **inconditionnel** (Lemme 1, incompressibilité Ω(n)) à un Kt qui n'est petit que **conditionnellement à x** (Lemme 2, vrai sous la forme K(w|x)=O(1), pas K(w)=O(log n) — la description doit embarquer x, de taille poly(n)). En unifiant les deux quantités, la contradiction disparaît : soit Lemme 2 redevient faux (inconditionnel), soit Lemme 1 redevient faux (conditionnel, car le témoin lex-premier est déterminé par x). Le fossé entre conditionnel et inconditionnel **est** P vs NP → circularité.
- **De plus : la piste 1 relativise** (Kt, auto-réductibilité, recherche↔décision relativisent tous). Par BGS, elle ne peut donc structurellement pas séparer P de NP, même réparée. À NE JAMAIS réessayer sous cette forme.

---

## 4. Questions ouvertes prioritaires

1. **Existe-t-il une notion de complexité des témoins qui NE relativise PAS** (par ex. fondée sur l'arithmétisation, dans l'esprit des techniques de Williams) ? C'est la seule porte non condamnée dans la direction « méta-complexité ».
2. Côté complexité descriptive : la question « existe-t-il une logique capturant exactement P ? » (conjecture de Gurevich) offre-t-elle un angle non-relativisant exploitable ?
3. Sur quelle **classe restreinte** concrète (monotone, AC⁰, ACC⁰, ou modèle algébrique type permanent vs déterminant) concentrer l'effort, là où de vrais théorèmes de bornes inférieures existent ?

---

## 5. Sous-but du tour courant

> Un seul objectif concret et, si possible, vérifiable.

- **Tour 2** : le Proposeur doit livrer une idée qui (a) cible une **classe restreinte** précise et (b) emploie une technique dont il **démontre le caractère non-relativisant**. Toute idée relativisante est rejetée d'emblée. Interdiction de se contenter de questions de cadrage : une idée concrète est exigée.

---

## 6. Prochaine action

- [ ] Proposeur : générer une idée pour le sous-but ci-dessus (non-relativisante + classe restreinte)
- [ ] Réfuteur : attaquer l'idée, vérifier en priorité relativisation ET algébrisation
- [ ] Confronter à la littérature réelle (recherche web) : l'idée correspond-elle à une tentative déjà publiée/écartée ?
- [ ] Si « survit » : isoler un sous-lemme vérifiable / tenter une formalisation (Lean)
- [ ] Consigner le résultat (succès **ou** échec documenté) dans les sections 2 et 3
