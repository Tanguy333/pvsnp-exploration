# ALG-001 — Mesures : le poids sous restrictions, et LA PRISE contre la candidature PR-005

Tâche : ALG-001. Script : `checks/alg001_poids_restrictions.py`.
Date : 2026-08-11. Graine 20260811, 20 restrictions par cas, W exact
(OPTIMAL exigé, témoins re-vérifiés).

## La table

| fonction | n | fixées (m restantes) | médiane W\|ρ | min | max | « W plein » annoncé |
|---|---|---|---|---|---|---|
| IP | 4 | 1 (3) | 1.5 | 1 | 2 | 20 |
| IP | 4 | 2 (2) | 1.0 | 0 | 2 | 20 |
| IP | 6 | 2 (4) | 2.0 | 1 | 3 | 119 |
| IP | 6 | 3 (3) | 2.0 | 0 | 3 | 119 |
| IP | 8 | 2 (6) | 3.0 | 2 | 4 | 640 |
| IP | 8 | 4 (4) | 2.0 | 1 | 3 | 640 |
| EXACT | 4-8 | (contrôle) | 2-6 | — | — | loi polynomiale : CONFORME |

## LA PRISE — la double calibration s'est retournée contre le proposant

Les médianes IP (~ nombre de paires survivantes) étaient TROP basses
pour être un effondrement : c'était un signal d'erreur de prémisse.
Vérification à la main : **W_MinSYM+(IP_{2k}) ≤ k, trivialement** —
le programme p = Σᵢ m_{paire_i} donne aux uns de IP des valeurs
IMPAIRES et aux zéros des valeurs PAIRES : ensembles disjoints, poids
k. IP est un SYM∘AND de k portes (c'est la structure Beigel-Tarui
même) — son poids MinSYM+ n'a jamais été exponentiel.

**La confusion de PR-005** : le « mur » 20/119/640 de F-001 est le
poids **PTF** (weight L1 d'une représentation en SIGNE — l'objet
pertinent pour les portes seuil) ; les lois du corpus MC sont le poids
**MinSYM+** (couvert exact à valeurs disjointes — l'objet pertinent
pour l'évaluation SYM∘AND). Deux mesures distinctes, conflées dans la
candidature. Le sous-lemme, exécuté, a falsifié la prémisse en
quelques secondes — exactement ce pour quoi il était conçu (« s'il
est réfuté par le calcul, la famille prend un coup »).

## Ce qui reste vrai, et le recalibrage

- Le contrôle EXACT est conforme aux lois (l'instrument est bon).
- Le verrou de la ligne 7 (l'algorithme THR∘THR) reste ce qu'il est —
  la prise ne porte que sur le PARAMÈTRE que le fil doit mesurer.
- **Recalibrage nommé (ALG-002 candidate)** : le poids PTF sous
  restrictions — l'objet RÉEL de F-001 (son instrument existe,
  `checks/task_f001*`) : le mur en signe 20/119/640 s'effondre-t-il
  sous ρ ? C'est la question qui avait un sens ; elle attend l'audit
  A-023 (en cours), chargé indépendamment de dire QUEL paramètre le
  transfert et le gabarit Williams 2014 consomment réellement pour
  les seuils (SYM+ pour ACC∘THR ; signe/rang probabiliste pour
  THR∘THR ?).
- La candidature PR-005 porte une note de correction MARQUÉE.
