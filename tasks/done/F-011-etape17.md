# TÂCHE F-011, étape 17 : l'asymétrie BAT l'anomalie — première sonde du modèle général

- **Type** : F (sonde exhaustive du modèle général — la marche vers les circuits)
- **Exécutée le** : 2026-06-10
- **Script** : [`checks/task_f011e17_asymmetry.py`](../../checks/task_f011e17_asymmetry.py)

## Résultat principal

> **`deg₆(MAJ_4) = 2 < 3 = deg₆^sym(MAJ_4)`** — un polynôme général de
> degré 2 représente faiblement MAJ_4 sur Z₆, battant la valeur
> symétrique *prouvée* (l'anomalie de l'étape 3). Exhaustif : d=1
> infaisable, d=2 faisable.

Et le ciblage est chirurgical : **aucun gain à n = 5, 6, 7** (général =
symétrique = 3, 3, 4, exhaustif sous ces valeurs). L'asymétrie ne casse
que le point d'anomalie.

## Le certificat explicite (vérifié en exact sur les 16 points)

> `V = x₁x₂ + x₁x₃ − x₁x₄ − x₂x₃ + x₂x₄ + x₃x₄ (mod 3)`, U = 0.

**Lecture combinatoire** : une **signature ±1 des arêtes de K₄** telle
que (i) chaque arête isolée est ≠ 0 (automatique), (ii) chaque triangle
somme à ≢ 0 mod 3, (iii) la somme totale des 6 signes ≡ 2 ≢ 0. La
contrainte symétrique (toutes arêtes égales = e₂) meurt à w = 4 car
C(4,2) = 6 ≡ 0 mod 6 ; la signature inhomogène esquive **l'annulation
binomiale** — l'anomalie est un artefact de la symétrie.

## Portée

1. **La restriction symétrique n'est PAS sans perte** sur Z₆, dès n = 4 —
   première donnée exhaustive sur la question générale-vs-symétrique
   (BBR la laissent ouverte pour OR : « tantalizing possibility » de
   O(log N) général vs Θ(√N) symétrique optimal).
2. Le mécanisme d'évasion (signatures non-homogènes contre annulations
   binomiales) est exactement le genre de phénomène qui rend le modèle
   général — celui du vrai mur de 1987 — plus difficile ET plus riche que
   le symétrique que nous avons cartographié.
3. **Question suivante naturelle (e18)** : les autres anomalies prouvées
   tombent-elles aussi ? `deg₆(MAJ_16) < 9 ?` — l'énumération est hors de
   portée (≈ 4·10⁴ monômes) ; la voie est la **construction** : généraliser
   la signature de K₄ (formes de degré q à coefficients signés sur les
   q-sous-ensembles, avec contraintes de sommes par strates de Lucas).

## Garde-fous

- Valeurs symétriques de référence prouvées (n=4) ou mesurées (n=5..7).
- « Non trouvé dans la littérature consultée » ≠ nouveau : la question
  générale-vs-symétrique est active (papier « Quadratic polynomials of
  small modulus cannot represent OR » repéré à l'audit) — un
  folklore-check dédié serait requis avant diffusion de ce point.
