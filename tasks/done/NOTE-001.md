# NOTE-001 — La note T-F006 est finie : théorème CNF prouvé, réserve russe réduite, version arXiv anglaise prête

- **Type** : C (consolidation externe)
- **Exécutée le** : 2026-07-23
- **Outputs** : [`notes/dnf_min_ip.md`](../../notes/dnf_min_ip.md) (finalisée) +
  [`notes/dnf_min_ip_arxiv_en.md`](../../notes/dnf_min_ip_arxiv_en.md) (anglais,
  prêt pour conversion LaTeX) + [`checks/task_note001_cnf_ip.py`](../../checks/task_note001_cnf_ip.py)

## Ce qui a été fait

1. **Régression** : les vérifications existantes re-passées vertes —
   certificat dual exact k = 1..14 (`task_f006b`), LP 40/121 à
   n = 4, 5 (`task_f005b`).
2. **Réserve §6.3 LEVÉE — théorème CNF prouvé** :
   CNF_min(IP_{2n}) = (3ⁿ+1)/2. Clé (une ligne) : la bi-décomposition
   XOR est invariante par complémentation
   (¬IP_{2(n+1)} = ¬IP_{2n} ⊕ (x∧y)) — toute la machinerie de Tour 18
   se transfère verbatim. Vérifié en force brute n = 1..4 :
   |primes(¬IP)| = 2, 5, 14, 41, TOUS essentiels (et côté IP
   re-confirmé : 1, 4, 13, 40, tous essentiels).
3. **Réserve §6.1 RÉDUITE** : 3e campagne de recherche — requêtes
   indexées en russe (Яблонский, ДНФ, простые импликанты) et en
   anglais (Problemy Kibernetiki) : rien ; page de commentaires Jukna
   vérifiée (Malyshev 1967, sans rapport). Résiduel : fonds non
   numérisés — un russophone reste souhaitable, niveau accessible
   épuisé.
4. **Statut Göös consigné honnêtement** : mail du 2026-06-09 sans
   réponse consignée au 2026-07-23 (6 semaines) — le silence ne vaut
   ni confirmation ni infirmation.
5. **Version anglaise arXiv rédigée** : 3 théorèmes (DNF, CNF,
   correspondance poids-PTF), preuves complètes, table transversale
   3ⁿ, section novelty-status honnête (« would welcome any earlier
   reference »), section vérification machine, disclosure IA.

## Ce qui reste (hors dépôt — main de Tanguy)

- Relecture experte indépendante (la seule réserve restante — la
  relecture humaine de Tanguy du 2026-06-10 lève « aucun humain n'a
  lu », pas « aucun expert »).
- Conversion LaTeX + soumission arXiv (décision et geste de l'auteur).
