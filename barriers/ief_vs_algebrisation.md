# D-006 — L'auto-test d'algébrisation de la voie iEF (ligne 15 × barrière n°3)

Tâche : D-006 (2026-08-08). Type D (cellule approche × barrière —
l'analogue de D-005, l'auto-test RR). **Statut : ANALYSE DU DÉPÔT sur
pièces auditées** — pas un fait des textes source, et aucune
revendication de nouveauté (analyse de barrière interne, comme D-005).

Pièces : AW08 = `bib/aaronson_wigderson_2008.md` (A-008, verbatims du
texte) ; AKPS = `bib/akps_2024.md` (A-019) ; PS23 =
`bib/pich_santhanam.md` (A-018). Objet testé : le transfert d'AKPS
ICALP 2024 — « iEF^tt(h) non polynomialement borné ⟹ #P ⊄ FP/poly » —
et, en amont, la voie PS23.

## 1. Pourquoi la question se pose

A-019 a établi le fait brut : le mécanisme central du transfert est
l'**arithmétisation** (sum-check LFKN sur F_p, « *arithmetize […] in
the usual way* »), et le texte **tait** les trois barrières classiques
(AW08 non cité, zéro occurrence d'« algebriz- »). Or la barrière
d'algébrisation dit précisément (A-008, verbatim) :

> « we show that all known non-relativizing results based on
> arithmetization—both inclusions such as IP = PSPACE and MIP = NEXP,
> and separations such as MAEXP ⊄ P/poly—do indeed algebrize. »

et

> « These results imply, in particular, that any resolution of the
> P versus NP problem will need to use non-algebrizing techniques. »

Le test opérationnel de l'audit A-008 (§6) : si l'argument reste valide
quand le simulateur reçoit une extension bas-degré Ã de l'oracle — ce
qui est le cas de toute preuve par arithmétisation pure, sum-check en
tête — il ne peut pas produire les grandes séparations.

## 2. FAIT 1 (inconditionnel, sourcé) : la CIBLE de la voie est derrière le mur

La conclusion du transfert est #P ⊄ FP/poly. Au sens AW08, une
séparation C ⊄ D algébrise si C^Ã ⊄ D^A pour tous (A, Ã) ; pour
montrer qu'une séparation EXIGE du non-algébrisant, il suffit d'un
témoin (A, Ã) qui la renverse. Le témoin est dans l'audit A-008 :
A PSPACE-complet, Ã son extension multilinéaire (elle-même
PSPACE-complète), avec `PSPACE^Ã ⊆ P^A` (liste des oracles, A-008 §3,
volet 2). Alors, par inclusions relativisantes standard :

#P^Ã ⊆ FP^(PP^Ã) ⊆ FP^(PSPACE^Ã) ⊆ FP^(P^A) = FP^A ⊆ FP^A/poly.

Donc **#P^Ã ⊆ FP^A/poly** : la séparation #P ⊄ FP/poly n'algébrise
pas — toute preuve exigera des techniques non-algébrisantes, par le
MÊME témoin que NP vs P/poly (et le motif est celui de l'oracle
`NEXP^Ã ⊂ P^A/poly` déjà listé par AW08). A fortiori pour le
renforcement visé par le problème ouvert (a) d'AKPS (NP ⊄ P/poly) et
pour la conclusion de PS23.

Ce fait ne dépend d'AUCUN choix de formalisation : il porte sur
l'énoncé-cible, pas sur le transfert.

## 3. FAIT 2 (sourcé) : le transfert est l'archétype algébrisant

Le cœur du transfert (Lemma 10 + Lemma 18 d'AKPS) est le protocole
LFKN : arithmétiser une 3CNF en polynôme de degré ≤ 3m sur F_p et
vérifier des sommes exponentielles ronde par ronde. C'est LE mécanisme
qu'AW08 classe dans le volet « tout ce qui arithmétise, algébrise »
(IP = PSPACE en est l'exemple canonique, et la liste auditée contient
`PSPACE^A ⊆ IP^Ã` — l'asymétrie exacte : le côté protocole reçoit Ã).

## 4. Le point délicat : formaliser « le transfert algébrise »

AW08 définit l'algébrisation pour des inclusions/séparations de
CLASSES. Le transfert d'AKPS relie un énoncé de complexité de preuves
(« iEF^tt p-borné ») à un énoncé de circuits (« #P ⊆ FP/poly ») —
l'appliquer exige un choix de formalisation, consigné ici :

- **(F1) Énoncé nu, sans oracle.** Le transfert tel qu'énoncé ne
  mentionne aucun oracle (les tautologies 3DNF arithmétisées sont
  concrètes, leur structure entièrement visible). La question « le
  transfert algébrise-t-il ? » n'a alors PAS de contenu direct — la
  barrière porte sur la survie des TECHNIQUES sous oracles, pas sur
  l'énoncé nu. C'est la lecture minimale, et elle ne qualifie rien.
- **(F2) Relativisation du langage et du système (choix du dépôt).**
  Langage propositionnel étendu par des atomes d'oracle α(x) ;
  systèmes relativisés (à la Krajíček) EF(α), iEF(α) ; axiomes tt
  relativisés ; côté protocole, SC^Ã : l'arithmétisation d'une clause
  contenant un littéral α(z) exige une extension bas-degré de α —
  exactement l'oracle algébrique Ã ; le Prover doit compter des
  solutions d'une formule à portes α (#P^A) ; le Vérifieur teste avec
  ses propres requêtes à Ã. Sous (F2), le pendant relativisé de
  Lemma 10 se lit : « #P^A ⊆ FP^Ã/poly ⟹ SC^Ã p-borné » — le motif
  d'oracles est exactement celui des inclusions algébrisantes d'AW08
  (le côté simulateur/protocole reçoit Ã).

**Le maillon non vérifiable sur pièces** : le pendant relativisé de la
chaîne interne d'AKPS — en particulier la soundness du sum-check
relativisé prouvée dans S¹₂(α, α̃) (Theorem 11 relativisé, avec une
axiomatisation de l'extension α̃), et le détour G_EXP relativisé. Les
textes audités ne l'énoncent pas. Signe favorable, sourcé : la
machinerie d'AKPS travaille DÉJÀ dans la théorie relativisée S¹₂(α)
pour le comptage de Jeřábek (A-019 §vi : « relativized theory
S¹₂(α) », l'oracle α y est la fonction dure du compteur) — la
formalisation est nativement oracle-compatible sur ce maillon. Le
maillon manquant est nommé : **« soundness S¹₂(α, α̃) du sum-check
relativisé »** — vérifiable par lecture de la thèse de Khaniki [39]
et du preprint [40] (non publiés, non audités — réserve d'A-019).

## 5. Verdict (à deux étages)

**Étage 1 — inconditionnel** : la voie iEF vise une cible
(#P ⊄ FP/poly, a fortiori NP ⊄ P/poly) qui est DERRIÈRE le mur
d'algébrisation (FAIT 1), et son transfert est bâti sur l'archétype
des techniques algébrisantes (FAIT 2). Le transfert ne peut donc PAS
être la source du contenu non-algébrisant que la cible exige.

**Étage 2 — sous (F2) et le maillon manquant** : si la chaîne d'AKPS
relativise algébriquement maillon par maillon (ce que sa structure
suggère et qu'aucune pièce ne contredit), alors relativement au témoin
(A PSPACE-complet, Ã multilinéaire) le transfert relativisé TIENT et
sa conclusion est FAUSSE — donc sa prémisse aussi : **le système
relativisé iEF(α)^tt est polynomialement borné relativement au
témoin**. Conséquence : toute preuve future de « iEF^tt non p-borné »
devra être NON-algébrisante. **La charge non-algébrisante de la voie
repose entièrement sur la borne de preuves manquante — la voie ne
s'échappe pas d'AW08 par son transfert.**

**Convergence de deux barrières** : c'est exactement l'endroit où la
barrière AUTO-RÉFÉRENTIELLE de Pich-Santhanam FOCS 2019 (A-012 ; « la
conjecture de Rudich n'a pas de preuves propositionnelles faisables »)
situe déjà la difficulté. Les deux analyses, indépendantes (oracles
algébriques d'un côté, auto-référence de l'autre), pointent le même
maillon : la borne inférieure pour un système fort. La ligne 15 porte
désormais cette convergence, sourcée.

**Ce que le verdict NE dit PAS** : que la voie est morte. Comme RR et
BGS, AW08 borne des techniques, pas des vérités (A-008 §5.1). Les
sorties documentées par AW08 lui-même s'appliquent : (i) la structure
des formules arithmétisées est RÉCUPÉRABLE depuis Ã (« if Ã was
produced by arithmetizing a 3SAT formula ϕ, then one can actually
recover ϕ in polynomial time by making oracle queries to Ã », A-008
§5.3) — une borne iEF exploitant la structure non-boîte-noire des
tt-formules ne serait pas bloquée par l'algébrisation telle que
définie ; (ii) la lecture-de-circuit à la Williams (le seul
franchissement connu) ; (iii) la localité. La cellule 15 doit lire :
« le transfert est un pont algébrisant vers une cible non-algébrisante ;
le travail non-algébrisant reste entièrement à faire, à l'endroit
que FOCS 2019 déclare auto-référentiellement difficile ».

## 6. L'amont PS23 (remarques, traçage non fait)

Le transfert de PS23 (« EF non p-borné + conditions S¹₂ ⟹
NP ⊄ P/poly ») a un mécanisme DIFFÉRENT (témoignage KPT, générateurs
de Nisan-Wigderson, comptage APC₁ — pas de sum-check). Même verdict
d'étage 1 : sa cible (NP ⊄ P/poly) est le témoin canonique d'AW08
(`NP^Ã = P^A = PSPACE` pour A PSPACE-complet — verbatim A-008 §3).
Le traçage maillon par maillon de son transfert sous oracles :
**[NON FAIT]** — les mécanismes NW/comptage sont réputés
boîte-noire-compatibles, mais les conditions de prouvabilité S¹₂
introduisent une subtilité (une hypothèse de prouvabilité peut être
FAUSSE relativement à un oracle sans que cela dise rien du monde nu) ;
une extension de D-006 à PS23 est possible mais n'est pas nécessaire
au verdict de la cellule (l'étage 1 suffit).

## 7. Réserves

1. (F2) est un CHOIX de formalisation du dépôt ; les systèmes
   relativisés à la Krajíček existent dans la littérature mais leur
   variante implicite iEF(α) et ses axiomes α̃ ne sont définis dans
   aucune pièce auditée. Un choix différent peut donner un énoncé
   différent — c'est consigné, pas caché.
2. Le maillon « soundness S¹₂(α, α̃) du sum-check relativisé » est
   PLAUSIBLE, non vérifié — il repose sur des textes non publiés
   (thèse Khaniki, preprint [40]) que ni A-019 ni D-006 n'ont ouverts.
   L'étage 2 du verdict est conditionnel à ce maillon.
3. L'étage 1 repose sur : la liste d'oracles auditée d'A-008
   (verbatims) + des inclusions relativisantes standard
   (#P ⊆ FP^PP ⊆ FP^PSPACE) — du folklore, employé comme tel, sans
   revendication.
4. Analyse de session, sans passe adverse tierce (comme D-005 à sa
   livraison) ; candidate au périmètre d'une future passe VER.
5. Antériorité : l'observation générale « les bornes de preuves pour
   systèmes forts butent sur les oracles » circule dans la littérature
   (Krajíček) ; aucune recherche systématique d'antériorité n'a été
   faite pour l'application spécifique au transfert AKPS — aucune
   nouveauté n'est revendiquée (règle : pas de revendication sans
   folklore-check ; il n'y a pas de revendication).

## 8. Clôture du fil D (décision utilisateur, 2026-08-08)

Le fil D (auto-tests de barrières sur voies vivantes : D-005, D-006)
est **clos en tant que fil**. Les continuations nommées ci-dessus —
vérification du maillon « soundness S¹₂(α, α̃) » sur la thèse de
Khaniki, passe adverse VER-D, sourçage de la formalisation (F2) chez
Krajíček, traçage du transfert PS23 — restent **ouvertes et
documentées, non poursuivies**. La cellule reste en état final
provisoire (étage 1 définitif, étage 2 conditionnel au maillon nommé).
Conditions de réouverture : décision utilisateur, ou mouvement du
domaine sur le maillon (p. ex. publication du preprint [40] de
Khaniki). Les cellules produites par le fil restent VIVANTES :
`depot_vs_rr.md` est la cellule du front MC ; ce fichier est l'état de
la colonne algébrisation de la ligne 15.
