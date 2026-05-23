# Tour 15-A — Profondeur logique de Bennett (❌ FAILLE FATALE — régression vers le pattern Tour 1)

- **Date** : 2026-05-23
- **Proposeur** : Qwen Max
- **Réfuteur** : Claude
- **Sous-but visé** : direction ouverte Tour 15.
- **Verdict** : ❌ **FAILLE FATALE** — auto-réfutation du Proposeur, pattern Tour 1
  (circularité conditionnel/inconditionnel) explicitement interdit par le cahier.

---

## Idée proposée (résumé fidèle)

Utiliser la **profondeur logique de Bennett** comme invariant non-relativisant.

- Si `P = NP`, toute fonction de NP a profondeur polynomiale (Lemmes 1+2).
- Exhiber une fonction NP à profondeur super-polynomiale (Lemme 3) → contradiction.
- Donc `P ≠ NP`.

---

## Réfutation

### 1. Le Proposeur s'auto-réfute

Citation textuelle du Lemme 3 du Proposeur :

> *« sous l'hypothèse `P = NP`, toute fonction NP est dans P, donc admet un
> algorithme polynomial, donc a une UDepth polynomiale. On ne peut donc pas
> exhiber de fonction NP à grande profondeur sans avoir déjà contredit
> l'hypothèse. **L'argument est circulaire.** »*

Et en conclusion :

> *« La piste de la profondeur logique offre un cadre conceptuel séduisant,
> mais bute pour l'instant sur la définition technique d'une mesure qui
> échappe à la fois à la circularité et aux barrières classiques. Elle est
> proposée ici comme **direction de recherche, en assumant ses lacunes
> actuelles**. »*

**Le Proposeur reconnaît explicitement que sa proposition est incomplète et
circulaire.** Au sens strict, ce n'est pas un théorème, c'est un brainstorm
ouvert. Réfutation par lui-même.

### 2. C'est exactement le pattern Tour 1 — explicitement interdit

Le cahier de bord §3 dit, à propos de la Piste 1 (incompressibilité Kt des
témoins) :

> *« Le sophisme central : la confrontation oppose un Kt **inconditionnel** à
> un Kt qui n'est petit que **conditionnellement à x** [...] Le fossé entre
> conditionnel et inconditionnel **est** P vs NP → circularité. **À NE JAMAIS
> réessayer sous cette forme.** »*

La structure logique du Tour 15-A est *identique* :
- Lemme 1 + 2 : *« sous P=NP, profondeur polynomiale »* (vrai conditionnellement).
- Lemme 3 : *« il existe une fonction NP à profondeur super-polynomiale »*
  (vrai inconditionnellement seulement si P ≠ NP).
- Le « gap » entre conditionnel et inconditionnel **est** P vs NP. Circularité.

C'est le pattern Tour 1 avec « profondeur de Bennett » à la place de « Kt à
ressources bornées ». Le cahier interdit explicitement cette forme.

### 3. Conditions du cahier violées

- **(h)** : aucun script livré, aucun code.
- **(j)** : aucun test empirique préalable. Aucun calcul.
- **(l)** : le cahier §3 dit explicitement *« à ne jamais réessayer sous
  cette forme »* pour le pattern Kt/Bennett-like. Le Proposeur n'a pas
  appliqué cette interdiction.

### 4. Test des barrières — sans objet

Les barrières (relativisation, RR, algébrisation) sont sans objet : il n'y
a pas de théorème à tester, juste une circularité interne reconnue par le
Proposeur.

### 5. Régression méthodologique

Après 3 ✅ Établis consécutifs (Tours 12, 13, 14) où le Proposeur honorait
(j)+(h)+(i)+(k)+(m), cette proposition est un **retour au mode spéculatif
des Tours 1-5**. Sans calcul, sans cible précise, sur un cadre conceptuel
non opérationnel, terminée par l'aveu *« proposée comme direction de
recherche en assumant ses lacunes »*.

C'est exactement le mode interdit par (i) corrigée et (j) renforcée.

### Verdict : ❌ FAILLE FATALE

Régression vers le pattern Tour 1 explicitement interdit par le cahier.
Auto-réfutation par le Proposeur. Aucun livrable vérifiable.

À NE PLUS jamais réessayer dans cette veine (Kolmogorov à ressources bornées,
profondeur logique, méta-complexité en argumentaire par contradiction
P=NP/profondeur). Le pattern est documenté et écarté définitivement.

## Note méthodologique

Cette proposition montre que **même après 3 ÉTABLIS consécutifs avec
épistémologie correcte, le Proposeur peut régresser** si on lui laisse trop
de liberté de direction. Le sous-but Tour 15 listait 4 options (extension
THRESHOLD_t, cross-validation, profondeur 3, Lean). Aucune ne mentionnait la
profondeur de Bennett ou méta-complexité Kolmogorov. Le Proposeur a inventé
sa propre option, qui se trouve être exactement un retour aux modes des
Tours 1-5.

Heureusement, le Proposeur a livré une **deuxième proposition** (Tour 15-B,
extension THRESHOLD_t) qui suit l'option 1 du sous-but et qui sera elle
✅ Établie. Le contraste entre les deux propositions du même tour est
pédagogiquement utile.
