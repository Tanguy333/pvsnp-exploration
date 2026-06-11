# Audit — Coppersmith, Mossinghoff, Scheinerman, Vanderkam 2023 (idéales PTE, taille 11)

- **Source** : *« Ideal solutions in the Prouhet–Tarry–Escott problem »*,
  [arXiv:2304.11254](https://arxiv.org/abs/2304.11254) (avril 2023),
  dédié à Peter Borwein. **Fourni par l'utilisateur** (2026-06-11),
  27 pages, texte intégral lu par extraction.
- **Pertinence** : la taille 11 = le témoin manquant du degré d = 10 de
  la Conjecture 5 de KV (cf. `notes/kv_note.md` §6bis — le « mur d = 10 »).

## REQUALIFICATION : recherche étendue, PAS preuve d'absence

L'énoncé « il n'y a pas de solution idéale en taille 11 » n'est **pas**
ce que le papier prouve. Verbatims :

> « *[Borwein, Lisoněk, Percival 2002] also proved that no **symmetric**
> ideal solutions with size n = 11 exist with height at most 2000* »

> « *We ﬁnd there are no **symmetric** ideal solutions for n = 11 with
> [height at most 3500]* » (recherche mod 29 → solution locale unique
> (16), puis (p₁, p₂) = (31, 29))

Les deux certificats portent sur les solutions **symétriques** (A = −A)
seulement. Le cas général (non symétrique) n'est couvert par aucune
recherche du papier. La non-existence totale en taille 11 est **ouverte**.

## Le détail qui change la perspective (équation 20)

Ils trouvent des solutions symétriques de taille 11 **à 2 irrationnels
quadratiques réels près** :
`A₁ = {−95, −68−α, −52, −48, −13, −9, 30, 34, 61, 65, 95+α}` (α racine
de x²+163x−8) — la taille 11 existe dans des extensions quadratiques
réelles de Q. L'obstruction entière est donc « fine », pas grossière.

## Complémentarité avec notre certificat réseau (V-016)

| Certificat | hypothèse | portée |
|---|---|---|
| BLP 2002 / CMSV 2023 | **symétrique seulement** | hauteur ≤ 2000 / **3500** |
| **Nous (V-016, SVP exact)** | **AUCUNE — toutes les solutions** | support ⊆ [0, N], N ≈ 70 |

Incomparables et complémentaires : leur borne est énorme mais
conditionnelle à la symétrie ; la nôtre est inconditionnelle mais à
petit support. À notre connaissance (à vérifier avant toute
revendication), le certificat inconditionnel à petit support n'est pas
dans la littérature — les méthodes de recherche classiques imposent
toutes des formes.

## Autres faits utiles extraits

- Kleiman 1975 : (n−1)! | Cₙ (constante des idéales) ; Rees-Smyth 1990 ;
  table des diviseurs requis de C′ₙ (Borwein et al. pour n = 11, 12, 13 ;
  CMSV pour 14 ≤ n ≤ 20).
- Premières recherches aux tailles 13..16 (symétriques) : rien.
- Smyth 1991 : famille infinie de symétriques idéales en taille 10
  (courbes elliptiques) ; Choudhry-Wróblewski 2008 : famille infinie en
  taille 12.
- Nouvelles idéales dans les corps quadratiques imaginaires (Gauss :
  tailles 10, 12 ; Z[i√2] : 9 ; Eisenstein : 9, 12).
