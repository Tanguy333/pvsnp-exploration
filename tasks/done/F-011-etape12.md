# TÂCHE F-011, étape 12 : mesure n = 45..80 — ✅ régions prouvées confirmées, structure v2 partielle

- **Type** : F (mesure du territoire jamais sondé)
- **Exécutée le** : 2026-06-10
- **Script** : [`checks/task_f011e12_law_v2.py`](../../checks/task_f011e12_law_v2.py)

## La table (36 cellules nouvelles)

| n | t | deg₆^sym | structure |
|---|---|---|---|
| 45..54 | 23..27 | **27** partout | zone I — théorèmes confirmés ✓ |
| 55..63 | 28..32 | **32** partout | zone J (témoin w=54) — confirmée ✓ |
| **64** | 32 | **36 = 27+9** | l'« anomalie » prédite 64 par feu C-F011 tombe aussi |
| 65..70 | 33..35 | **40 = (3⁴−1)/2** | plateau répunit — (1,1,1,1)₃ |
| 71..72 | 36 | **44** | (1,1,2,2)₃ |
| 73..74 | 37 | **46** | (1,2,0,1)₃ |
| 75..80 | 38..40 | > 50 (cap dim 12) | valeur ≥ 51, non conclue |

## Enseignements

1. **Validation croisée des théorèmes** : les zones I et J prédisaient 27
   et 32 — mesuré exactement, 19/19 cellules. Les preuves de l'étape 10
   tiennent sur du territoire neuf.
2. **Le pattern d'anomalie « puissance suivante » est mort** : t = 32
   donne 36 = 27+9, pas 64 ni 81. Les trois anomalies prouvées (3, 9, 27)
   restent des théorèmes ; leur extrapolation était un artefact de plus.
3. **La zone v2 n'est PAS en puissances** : plateaux 36, 40, 44, 46 — des
   nombres à motifs base-3 riches (sommes de puissances de 3, dont le
   répunit (3⁴−1)/2 = 40 sur tout un plateau). Le mod 2 ne sert plus
   au-dessus de q₂ = 64 (périodicité), donc ces valeurs sont
   vraisemblablement gouvernées par la **loi mod 3 du cas t général** —
   jamais dérivée (notre loi OR exacte est le cas t = 1).
4. **Pas de loi v2 propre aujourd'hui** — dit honnêtement. La voie
   théorique est claire : généraliser la machinerie prouvée
   (descente → paires interdites → interpolation, Théorèmes E-G) du cas
   t = 1 au cas t général, puis comprendre la composition mod 6.

## Prochaine cible (e13, candidate)

**La loi mod 3 du cas t général comme théorème** — les outils existent
tous (Lemme 2 fenêtre/automate marche pour tout t ; la descente est
générale ; les paires interdites aussi). C'est la généralisation la plus
susceptible d'expliquer 36, 40, 44, 46 d'un coup — et un pas réel vers la
compréhension complète du modèle symétrique composite.
