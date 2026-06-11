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

## Complément — survey Chen Shuwen et al. 2025 (arXiv:2506.11429, 368 p.)

Lu par extraction (2026-06-11), vérification du statut « premier
certificat inconditionnel » de V-016. Verbatims clés :

> « *ideal non-symmetric solutions have only been discovered for PTE of
> degrees n ≤ 7* » (= tailles ≤ 8 ; convention du survey : degré =
> taille − 1) — même aux tailles 9, 10, 12, toutes les idéales connues
> sont symétriques.

> « *[formula (2.167)] is useful for searching for ideal non-symmetric
> solutions of PTE of degree 10. Based on (2.167), we have searched for
> **more than 6 years with several computers**, but still have not found
> such a solution **within the range of 1600**.* »

**Analyse** : la recherche non symétrique de Chen Shuwen (taille 11,
6 ans-machines, range 1600) passe par une **famille paramétrique à
4 paramètres** — pas une exhaustion sur toutes les solutions. Paysage
final des certificats taille 11 :

| Certificat | hypothèse | portée |
|---|---|---|
| CMSV 2023 | symétrique | hauteur ≤ 3500, exhaustif |
| Chen Shuwen 2025 | famille (2.167) non sym. | range 1600 |
| **V-016 (nous)** | **aucune** | support ⊆ [0, 70], exhaustif |

→ **V-016 confirmé comme seul certificat inconditionnel** (toutes les
solutions, aucune hypothèse de forme) — borne plus petite mais portée
non couverte ailleurs. Vérifié contre le survey de 368 pages, le plus
récent de la littérature (juin 2025).

## Relecture du survey POUR le dépôt (2026-06-11, demande utilisateur)

Trois apports examinés :

1. **Son P1 ouvert** (« degrees n = 10 and n ≥ 12 ») = notre mur d = 10
   (`notes/kv_note.md` §6bis) — cartographies alignées.
2. **Sa Conjecture 1 (entrelacement des solutions normalisées)** :
   traduite en notre langage, elle suggérait « les vecteurs minimaux du
   réseau ont des signes alternés », ce qui aurait attaqué les bouts ±1
   (= la Conjecture 5) par une voie de structure. **TESTÉ et RÉFUTÉ en
   30 s** : 4/72 minima alternent (échantillon de 15 cellules, d = 2..10,
   y compris sous-transition, max|coef| jusqu'à 44). L'entrelacement
   vaut pour les solutions idéales (différence constante de polynômes
   unitaires — argument classique) mais ne s'étend PAS aux minima
   généraux. Voie fermée, 8e hypothèse tuée le jour même.
3. **Ses types GPTE ouverts les plus simples** (P2 : (k=5), (k=6),
   (k=3,4)) sont attaquables par nos exhaustions (réseau ou
   meet-in-the-middle) — mais HORS CIBLE P vs NP : consigné comme
   quête latérale possible, non engagée (CLAUDE.md §8).

Ses conjectures de bornes (2-4, problème normalisé) optimisent les
recherches à grande hauteur (style D2) — peu transposables à notre SVP.
