# Brouillon — réponse 3 à Michael Mossinghoff

> ⚠️ **REMPLACÉ par `mossinghoff_reply_4_draft.md`** (version consolidée
> avec les nouveaux polynômes m=22/23 et le correctif τ(20) de l'audit
> 2026-06-29). Ne pas envoyer celui-ci. Sa phrase « A non-trivial n = 22
> product seems to need H >= 4 » s'est avérée fausse (le minimum 473 est
> de transit 2).

> À envoyer par Tanguy. Répond à : (1) OEIS — oui ; (2) langage compilé —
> déjà fait (Numba/LLVM), le mur est l'arbre, pas le langage ; + ce que
> l'extension a atteint (table validée à m=21, m=22 à la frontière).

---

**Subject:** Re: m = 20 entry — OEIS, and a note on the implementation

Dear Michael,

Thank you — I'll record the m = 20 value at A059753 (as a smallest-known
upper bound, with the polynomial and a note that it fills the gap in your
Table 1).

On the implementation, a happy coincidence: the search is already
compiled — I run the inner enumeration through Numba, which JIT-compiles
it to machine code via LLVM, so it's effectively at C speed without
leaving Python. That let me, after your note, validate the table up to
n = 21 (recovering your degree-294 product) in seconds, and confirm that
n = 22..25 have no flat pure product within transient height <= 3 and
degree <= 420. The genuine wall is not the language, and not memory
either (the search holds a flat ~0.1 GB): it is the height-bounded tree,
which at n = 22 grows about 25-50x per unit of allowed transient height
(748k, 39.6M, 1.05B nodes for H <= 1, 2, 3). A non-trivial n = 22 product
seems to need H >= 4, ~30 minutes on one core — so the next step is just
to let that run, or split the first levels across cores, rather than to
change language. I may do that if I return to widening the search.

I'll let you know once the OEIS entry is in. Thank you again for the
encouragement and the Cipu pointer.

Best,
Tanguy

---

## Statut épistémique (hors email)
- « déjà compilé via Numba/LLVM » : vrai (V-038).
- « table validée à m=21 (294) » : vrai, reproduit ce jour.
- « m=22..25 rien à transit<=3, degré<=420 » : vrai, mesuré ce jour.
- CORRECTION (26e auto-correction, 2026-06-28 ; renumerotee apres V-055) : l'« OOM exit 137 » était
  un FAUX diagnostic. Mémoire mesurée PLATE à ~0,11 Go quel que soit le
  transit ; le exit 137 était un kill par dépassement du timeout d'outil.
  Le mur est le TEMPS, pas la mémoire. Noeuds m=22 : 0,75M / 39,6M / 1,05G
  pour H<=1/2/3 (×53, ×26) à ~19M n/s. H<=4 ≈ 30 min/cœur (faisable).
- d(22) ≤ 473 TRIVIALEMENT (champion m=21 × (1−x^179)) — borne JUNK, ne
  pas l'annoncer. Le vrai d(22) (≈300-340) exige H>=4, non encore lancé.
- Ne RIEN promettre de plus tant que le transit-4 n'a pas tourné.
