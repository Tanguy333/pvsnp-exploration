# Instruction de candidature — « Spécifications Récursives Étroites » (SRE) — REJETÉE

Date : 2026-08-08. Tâche : PR-002. Candidature produite par le
Proposeur (Qwen) en réponse au prompt PR-001
(`prompts/proposeur_front_neuf.md`) — première candidature du
générateur externe réarmé. Instruction par le Réfuteur selon la
procédure CLAUDE.md §5. **Ceci n'est pas un Tour adverse** (suspension
inchangée) : c'est l'instruction d'une candidature de ligne 19.

## 0. La candidature, fidèlement résumée

Famille « SRE » : pour SAT (ou tout langage NP-complet), construire
par self-réduction un système fini d'équations booléennes E_N sur une
fonction inconnue f_N (f(x) = θ(f(y₁), …, f(y_k)) pour la fixation de
variables, plus équations de bord et de padding), et définir le
« seuil de fermeture » σ(E_N) = taille minimale d'un circuit
satisfaisant exactement E_N. Tout circuit décidant SAT satisfait E_N ;
donc σ(E_N) super-polynomial ⟹ SAT ∉ P/poly ⟹ P ≠ NP. Mécanisme
proposé : propager les équations dans la structure interne d'un petit
circuit hypothétique jusqu'à contradiction. Sous-lemme : la
spécification jouet S₄ (définition récursive de ⊕₄) n'est satisfaite
par aucun circuit {AND, OR, NOT}, fan-in ≤ 2, de ≤ 4 portes.

**Reformulation en une phrase** : définir SAT par ses équations de
self-réduction, appeler « seuil de fermeture » la taille du plus petit
circuit qui les satisfait, et espérer minorer ce seuil par propagation
syntaxique de contraintes.

## 1. Attaque logique n°1 — la mesure est une reformulation (zéro levier)

Si E_N détermine f_N de façon unique (c'est le but déclaré des
équations de bord et de padding : « elle peut n'admettre qu'une seule
table de vérité »), alors un circuit satisfait E_N **si et seulement
si** il calcule SAT_N — et donc, PAR DÉFINITION :

σ(E_N) = CC(SAT_N) (la complexité de circuits de SAT_N, exactement).

« Prouver σ(E_N) super-polynomial » est l'énoncé SAT ∉ P/poly
lui-même, renommé. La famille ne fournit aucun objet intermédiaire :
pas de mesure relaxée, pas de borne passerelle — un changement de
notation. **L'universalité le confirme** : toute fonction booléenne
admet une spécification récursive étroite qui la détermine (son
développement de Shannon f(x) = (x₁ ∧ f|_{x₁=1}) ∨ (¬x₁ ∧ f|_{x₁=0}),
plus les cas de base) ; pour cette spécification, σ = CC(f)
identiquement. La machinerie SRE s'applique à N'IMPORTE QUELLE
fonction et n'y dit rien de plus que « sa complexité de circuits est
sa complexité de circuits ». Le propre sous-lemme de la candidature
l'illustre : S₄ épingle ⊕₄ uniquement, donc « aucun circuit ≤ 4
portes ne satisfait S₄ » ≡ « CC(⊕₄) > 4 » — une borne inférieure de
circuits ordinaire pour la parité (voir §3 : elle est de 1974).

Et si E_N ne détermine PAS f uniquement : σ(E_N) devient « la taille
du modèle le plus facile » — c'est la minimisation de circuits d'une
FONCTION PARTIELLE (min sur les complétions), soit exactement le
territoire de la méta-complexité partielle : Levin 1973 (DNF-MCSP∗),
lignes 13 et 18 de la matrice — le dépôt lui-même vient de mesurer
cet objet (MC-017, Q0). Les deux lectures de σ retombent chacune dans
une case connue : reformulation de CC(SAT), ou méta-complexité
partielle existante. **Dans les deux cas : pas de famille nouvelle.**

## 2. Attaque logique n°2 — le « mécanisme » est un système de preuve (ligne 15)

Le mécanisme proposé — propager les équations dans le circuit
hypothétique, « procédure de clôture », contradiction locale — est une
DÉRIVATION : réfuter par étapes syntaxiques la formule propositionnelle
« il existe un circuit de taille s satisfaisant E_N ». C'est mot pour
mot l'objet de la complexité des preuves des bornes de circuits (les
lb-formulas — Razborov ; Krajíček), le cœur de la ligne 15. La force
de la « clôture » EST la force d'un système de preuve ; sa
« complétude » (leur manque n°2 : « rien ne garantit qu'une
propagation finie détectera la violation ») EST la question de la
puissance du système. Le positionnement (« pas des règles de preuve
mais des contraintes de fermeture ») ne survit pas à cette lecture :
borner σ par propagation, c'est prouver propositionnellement une
borne de circuits — et la ligne 15 documente ce qui garde cette porte
(la barrière auto-référentielle : Pich-Santhanam FOCS 2019, audit
A-012 ; et pour les versions « connexion », la barrière
Pich-Santhanam, audits A-018/A-019).

## 3. Contre-vérification exécutable — le sous-lemme est vrai, folklore, et non discriminant

Script : `checks/pr002_sre_parite.py` (synthèse de circuits par
CP-SAT sous la convention EXACTE de la candidature : {AND, OR, NOT},
fan-in ≤ 2, entrées et constantes gratuites, chaque porte coûte 1,
témoin re-vérifié par simulation indépendante).

**Résultats (2026-08-08, mesurés)** :

```
XOR_3 : k = 1..7 UNSAT ; k = 8 SAT (témoin re-vérifié) — MINIMUM = 8
XOR_4 : k = 1..9 UNSAT prouvé (127 s au palier 9) ; k = 10 NON CONCLU
        (timeout 300 s) ; majorant 12 CONSTRUIT et vérifié par
        simulation (mode borne12) — MINIMUM ∈ [10, 12]
```

Le sous-lemme (« aucun circuit ≤ 4 portes ») est donc VRAI — et
trivialement : le minimum réel de ⊕₄ est ≥ 10 sous leur convention,
plus de 2,5 fois leur borne. Antériorité : la complexité de ⊕_n sur la
base U₂ (portes binaires sans XOR/XNOR) est un théorème classique de
**Schnorr 1974** — 3(n−1) portes BINAIRES, les NOT étant gratuits dans
ce comptage (6 à n = 3, 9 à n = 4) ; sous la convention de la
candidature (NOT payant), la structure devient 4 portes par étage ⊕₂
— 4(n−1) : 8 mesuré exactement à n = 3, 12 réalisé à n = 4. Le
« premier pas » re-démontre un coin affaibli d'un phénomène établi il
y a 51 ans, que le folklore-check de la candidature n'a pas cité
(régime d'échec n°3 du prompt). Et il ne teste PAS le mécanisme de la
famille : la vérification (synthèse/énumération) n'utilise nulle part
la « propagation d'équations » — n'importe quelle définition de la
parité donnerait le même calcul ; la dureté vient de la parité, pas de
la « fermeture ». Résultat garanti d'avance + mécanisme non testé =
sous-lemme non discriminant (le prompt exigeait un test « réellement
discriminant »).

*Note de méthode : la première rédaction de cette section annonçait
6/9 (les valeurs de Schnorr) avant la fin du calcul — les valeurs
mesurées (8 ; [10, 12]) les ont corrigées avant consignation : les
minima sous convention NOT-payant ne sont PAS ceux du comptage
binaire. La leçon (ne jamais consigner un chiffre non mesuré) est
celle du dépôt ; l'écart lui-même illustre la sensibilité de ce genre
d'énoncés à la convention de comptage — un point que la candidature ne
spécifiait qu'à moitié.*

## 4. Test des barrières — l'auto-test de la candidature est invalide

La section [BARRIÈRES] de la candidature confond systématiquement
l'ÉNONCÉ et la TECHNIQUE. Que la spécification soit « syntaxique, sans
oracle » ne dit rien : tout énoncé candidat pour P ≠ NP est sans
oracle ; la barrière porte sur la survie des ARGUMENTS sous oracle.

- **Relativisation : la technique décrite RELATIVISE.** Les équations
  E_N relativisent verbatim — la self-réduction de SAT^A par fixation
  de variables vaut pour tout oracle A (elle est indépendante de
  l'oracle), donc E_N^A existe et, dans un monde P^A = NP^A (BGS),
  SAT^A a des circuits polynomiaux à portes-oracle qui satisfont
  E_N^A : σ(E_N^A) y est polynomial. Or le mécanisme proposé
  (propagation de valeurs de portes, cohérence locale, comptage de
  sous-fonctions) traite les portes de façon GÉNÉRIQUE — tel que
  décrit, il s'applique inchangé aux circuits à portes-oracle, donc
  chacune de ses étapes survit à l'oracle, donc il ne peut pas
  conclure. L'affirmation « le mécanisme ne relativise pas » n'est
  étayée par aucun ingrédient qui casse effectivement sous oracle —
  la candidature l'admet elle-même (manque n°3 : « une preuve complète
  devrait certifier que chaque étape exploite cette fragilité »).
- **Le dilemme fatal** : pour échapper à BGS, l'analyse doit être
  spécifique à la base {AND, OR, NOT} (regarder les portes, pas des
  boîtes) — mais c'est alors la méthode d'ÉLIMINATION DE PORTES,
  vieille de 50 ans, dont le plafond documenté est LINÉAIRE
  (Schnorr 1974 : 3(n−1) pour ⊕ ; état de l'art général ~(3+1/86)n,
  Find-Golovnev-Hirsch-Kulikov 2016) — aucun moteur super-linéaire, a
  fortiori super-polynomial, en un demi-siècle. Générique ⟹ mort par
  BGS ; spécifique ⟹ héritier du plafond gate-elimination sans engin
  neuf. La candidature ne propose rien qui sorte de ce dilemme.
- **Algébrisation** : même confusion — le témoin d'AW08 (A
  PSPACE-complet, Ã multilinéaire) rend σ(E_N^Ã-relatif) polynomial ;
  un argument dont les étapes survivent aux oracles algébriques ne
  conclut pas. Dire que « les opérations syntaxiques ne se relèvent
  pas en polynômes » ne protège pas la TECHNIQUE.
- **Preuves naturelles** : l'argument d'étroitesse (anti-largeness)
  est correct dans la lettre — mais c'est l'échappatoire du singleton,
  disponible pour TOUTE approche « fonction spécifique », folklore et
  sans levier : elle n'a jamais produit de borne.

## 5. Recevabilité (grille PR-001)

| Champ | État |
|---|---|
| Énoncé visé, classe, chaîne | Conformes en forme ; la chaîne est correcte mais son maillon ouvert est LE problème entier (reformulé) |
| Test de plafond | Honnête sur l'échelle jouet ; mais le « phénomène » testé (dureté de ⊕₄) n'est pas le mécanisme de la famille |
| Folklore-check | **INSUFFISANT** : Schnorr 1974 (l'objet même du sous-lemme), les lb-formulas (ligne 15), l'élimination de portes et Levin 1973 (lecture partielle de σ) — tous absents ; les 3 cités (Cook, GRS, RR) ne sont pas les plus proches |
| Sous-lemme | Vrai, folklore, non discriminant (résultat garanti, mécanisme non testé) |
| Positionnement | La distinction revendiquée d'avec la ligne 15 ne tient pas (§2) ; les lectures alternatives tombent en lignes 13/18 (§1) |

## 6. VERDICT : FAILLE FATALE — candidature REJETÉE, pas de ligne 19

Motifs, citables : (1) la mesure centrale est une reformulation de
CC(SAT) (lecture unique) ou un objet existant des lignes 13/18
(lecture partielle) — zéro levier nouveau ; (2) le mécanisme est un
système de preuve de bornes de circuits — la famille se réduit à la
ligne 15 et à ses barrières auditées ; (3) l'auto-test des barrières
est invalide (confusion énoncé/technique) et la technique décrite est
prise dans le dilemme générique-BGS / spécifique-plafond-linéaire ;
(4) folklore-check manqué (Schnorr 1974 non vu alors qu'il contient le
sous-lemme) et premier pas non discriminant. Régimes d'échec du
prompt : n°3 (re-démonstration de folklore) constitué ; n°1
(spéculation sous barrières) constitué au niveau technique.

**Ce qui survit** : rien de spécifique à la candidature. La seule
observation exacte — « tout circuit pour SAT satisfait les équations
de sa self-réduction » — est la sémantique standard de SAT, déjà au
cœur des lb-formulas (ligne 15). Le générateur PR-001 a fonctionné
comme filtre : la candidature a été instruite et rejetée avec motifs
en une session, calcul à l'appui.
