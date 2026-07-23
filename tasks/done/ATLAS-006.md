# ATLAS-006 — La zone génératrice 6 est FERMÉE : la séparation prouvée de KV devient visible à n ≈ 4050, trois ordres de grandeur au-delà de tout instrument

- **Type** : A/D (extraction quantitative d'une preuve + clôture de zone)
- **Exécutée le** : 2026-07-23
- **Outputs** : [`bib/kv_asym_extraction.md`](../../bib/kv_asym_extraction.md) +
  zone 6 de [`atlas/matrice_barrieres.md`](../../atlas/matrice_barrieres.md)

## Ce qui a été fait

TR24-074 téléchargé (38 p.) et la preuve du Théorème 1.3.1 (borne
symétrique Ω(√(n/log n)) pour tous les Δ_w à ε = 1/2n) disséquée
jusqu'à son comptage : **pigeonhole effectif** n^{(d+1)²} < 2^{⌈n/2⌉+1}
(Lemme 3.7, à la Siegel, + lemme de décalage 3.8 pour γ_w ≠ 0 à tout
w). D'où d_max(n) explicite, calculé exactement par script.

## Les trois seuils

1. **La borne symétrique de KV est VIDE pour n ≤ 40** (d_max = 0) —
   ATLAS-005 (« gain invisible à n ≤ 7 ») est expliqué
   STRUCTURELLEMENT : le théorème ne dit rien dans la plage de
   l'instrument. Premier contenu : n = 41 (interdit le degré 1).
2. **Croisement prouvé sym/asym : n ≈ 4050** (d_max = 12 > log₂ n =
   12,0) — la séparation démontrée (borne inf sym > borne sup asym
   log₂ n de BHLR) n'est visible qu'à cette échelle.
3. **Instrument : n ≤ 8.** Écart : trois ordres de grandeur. La
   question de la zone (« pointer l'instrument sur la séparation
   prouvée ») a une réponse définitive : impossible.

## Conséquences

- La zone génératrice 6 sort de la liste des cibles ouvertes de la
  matrice (fermée avec chiffres, pas abandonnée).
- Le no-man's land 8 ≤ n ≤ ~4000 est documenté : la VRAIE séparation
  y commence peut-être (la borne de KV n'est pas serrée — la
  construction réelle est √(n log n)) mais ni preuve effective ni
  mesure ne peut le dire aujourd'hui.
- Cohérence avec le dossier AS : la route asymétrique (Conjecture 13)
  vit à des échelles hors instrument — c'est le même mur, vu deux fois.

## Précision honnête

d_max dérivé du comptage VERBATIM du papier ; les facteurs (2·+1) du
comptage des labels peuvent décaler d_max de ±1 et le croisement de
quelques pourcents — sans effet sur les ordres de grandeur ni sur la
clôture.
