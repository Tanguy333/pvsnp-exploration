# P vs NP — An Atlas of Dead Ends

*[Version française](README.fr.md)*

> **Mission (since 2026-08-07).** Explore the **P vs NP** problem through
> several routes in order to make significant progress, with the aim of a
> partial proof or a proof of P = NP or P ≠ NP. The central instrument is an
> **elimination atlas**: explore the routes, eliminate the ones that die
> (proofs, executable counterexamples, full-text audits, 27 archived rounds
> of adversarial refutation), so that the right route can emerge.
>
> **Honest framing, unchanged.** The problem has been open since 1971. This
> repository does not claim to have solved it, or to be close to solving it.
> No progress is claimed here without executable verification, a written
> prior-work check, and a test against the known barriers. The ambition is a
> heading, not a claim.

### What this repository has established (status as of 2026-07-25)

One thing closed: **Conjecture 5 of Krishan-Vishwanathan is false**. The
parity mechanism is proved, the enumeration is exhaustive cell by cell, and
one of the authors confirmed it in writing. This closes **one ingredient** of
a route towards MAJ ∉ ACC, not MAJ ∉ ACC itself. **Twenty-two full-text
audits**, with the marker `[NON TROUVÉ]` ("not found") wherever a piece is
missing; this is the format in which the repository delivers the most.
**Four certified exact instruments**, whose ceiling is published: n ≤ 7-8 for
the toric and CVP instruments, n = 10 for CP-SAT. And **one negative result
about the setup itself**, met twice along two independent paths and
quantified: the gap between what the workshop can measure and the scale at
which the phenomenon starts (n ≤ 8 versus n ≈ 4050; O(n²) versus
2^{polylog n}), see [`atlas/echelle_instrument.md`](atlas/echelle_instrument.md).
The rest (169 tasks, 188 scripts, 27 rounds) is cost, and it is presented as
such. **As of 2026-07-25, nothing here had advanced a proof of P ≠ NP.** That
assessment is dated and still accurate. Since 2026-08-07 the mission
explicitly aims at progress (see the header), and this assessment is the
baseline any future claim will have to beat, with evidence. The repository's
error log (36 self-corrections, including a false asymptotic claim caught
before it was sent to an author in the field) is part of the deliverable, on
the same footing as the results.

## The problem

Is every problem whose candidate solution can be checked in polynomial time
(the class NP) also *solvable* in polynomial time (the class P)? It is one of
the seven Millennium Prize Problems, open since 1971. No valid proof exists
today, and this repository documents, piece by piece, why the major known
families of attack cannot provide one.

## The central deliverable: the barriers × approaches matrix

**[`atlas/matrice_barrieres.en.md`](atlas/matrice_barrieres.en.md)** (English translation of the French reference [`atlas/matrice_barrieres.md`](atlas/matrice_barrieres.md)):
20 families of approaches, from diagonalization to Geometric Complexity
Theory (GCT), from the modular polynomial method to hardness magnification,
modern meta-complexity, toric polynomials, proof complexity, range avoidance,
lifting, the meta-complexity of depth-2 classes (row 18), Valiant-Cai
holographic algorithms (row 19, the first row in the P = NP direction), and
structured total search TFNP (row 20, the shortest chain in the matrix).
They are crossed with the 4 known barriers (relativization, natural proofs,
algebrization, monotone), plus a "**real lock**" column: what actually blocks
each approach today. Each cell points to its supporting evidence, either an
audit in `bib/` or a task record in `tasks/done/`. Wiring cells to scripts is
in progress in [`atlas/temoins.md`](atlas/temoins.md).

A **register of eliminations** at the end of the matrix holds directions that
were examined but have no open arrow towards P vs NP, so they do not become
rows.

**Scope of the measurements**: [`atlas/echelle_instrument.md`](atlas/echelle_instrument.md).
The instruments in this repository have a quantified ceiling (n ≤ 7-8 for the
toric and CVP instruments, n = 10 for CP-SAT), and several fronts of the
matrix live at a much larger characteristic scale. The repository paid for
this gap twice, along two independent paths, before writing it down.

The three lessons of the matrix:

1. **Only one row crosses all 4 barriers**: Williams' algorithmic method
   (NEXP ⊄ ACC⁰, 2011). Its extension lock is precise: there is no
   non-trivial SAT algorithm beyond ACC⁰.
2. **The classical barriers are no longer the front line.** Every live
   program has settled its relationship with the 3 classical barriers *by
   construction*, and is stuck on an **internal barrier of its own**
   (composite moduli since 1987, BIP 2019 for GCT, locality 2020 for
   magnification, and so on).
3. Any strategy precise enough to be executed generates the analysis of its
   own impossibility.

## The pieces

```
.
├── README.md                  ← this file (English, default)
├── README.fr.md               ← French readme
├── CLAUDE.md                  ← agent rules (task mode + anti-evasion rules)
├── cahier_de_bord.md          ← log: leads, lemmas, questions, satellite register (§2 ter)
├── atlas/
│   ├── matrice_barrieres.md   ← THE deliverable: barriers × approaches matrix (20 rows, French reference)
│   ├── matrice_barrieres.en.md ← English translation of the matrix
│   ├── temoins.md             ← cell → script → command → output → runtime
│   └── echelle_instrument.md  ← setup note: the workshop's ceiling
├── bib/                       ← 22 bibliographic audits on full texts
│   ├── bgs_1975.md            ← relativization (both oracles, proofs)
│   ├── razborov_rudich_1997.md← natural proofs (definitions verbatim)
│   ├── aaronson_wigderson_2008.md ← algebrization (exact asymmetric definition)
│   ├── tardos_1988.md         ← monotone barrier (θ̄ mechanism + GLS)
│   ├── razborov_smolensky_1987.md ← modular polynomial method
│   ├── beigel_tarui_1994.md   ← SYM+ transformation (core of Williams)
│   ├── williams_2011.md       ← the only crossing of the 3 barriers
│   ├── cfi_abd.md             ← CFI, FPC ⊊ P, affine CSPs
│   └── l18_status.md          ← the only object in the repository not found in the literature
├── barriers/                  ← 4 detailed cells (approach × barrier)
├── tours/                     ← archives of the 27 adversarial rounds (idea + refutation)
├── checks/                    ← 188 executable verification scripts
├── data/                      ← 12 measurement datasets (L1 weight of PTFs on depth-2 TC⁰, …)
├── notes/                     ← summaries and drafts (including satellites, see log §2 ter)
├── roadmap/                   ← ARCHIVE 2026-05-23, not the repository's program
└── tasks/                     ← backlog (169 done), hors_cible/ (off-target), failed/
```

*(The counts above are real counts as of 2026-07-25, not estimates. The
previous readme announced 12, 9, ~30 and 25.)*

## How this repository was built

This is a spare-time project, carried out with LLMs (mainly Claude).

**Adversarial phase (Rounds 1-25).** Two LLMs in opposing roles: a
*Proposer* generates an idea, a *Refuter* demolishes it, with an obligation
to produce an executable counterexample whenever one is computable. Result:
25 refutation archives, and a clear diagnosis of **4 failure modes** of LLMs
on this problem (speculation killed by the barriers, off-topic drift,
re-proving folklore, evasive pivoting).

**Atlas phase (since 2026-06).** The adversarial loop is suspended, replaced
by **atomic anti-evasion tasks** (CLAUDE.md §8): full-text paper audits, ILP
measurements, matrix cells. Each task has its output specified in advance;
honest failure is allowed, invention is forbidden. Two adversarial rounds
were reopened (26 and 27) on a target that came from the Atlas; the thread
they produced was **closed on 2026-07-25**, and the loop suspended again.

**Refocusing (2026-07-25).** An internal audit measured that **160 of the 169
delivered tasks had never touched the deliverable**: the work was being
absorbed by the log, not by the Atlas. Diagnosis: the six anti-evasion rules
all regulated the *form* of a task, **none regulated its direction**. Four
rules were added (CLAUDE.md §8, rules 7 to 10): a mandatory link to a named
cell, **re-read at closing time**; a ceiling test ("at what scale does the
phenomenon start, and is it below my ceiling?"); a review per thread, where a
thread is defined by its *target*; and the requirement that any refocusing be
written into the rules themselves. Failure mode no. 5 is thus documented:
**a slow drift that local rigor does not detect**, where every task is
impeccable and the trajectory is off-topic.

## Verifiable results (and their honest status)

- **9 small theorems in Boolean combinatorics** (depth 2), proved and checked
  by computation. The bibliographic audit established that 8 of them are
  folklore (Quine 1952 → Hellerstein-Kletenik 2011). The 9th,
  `DNF_min(IP_{2n}) = (3^n−1)/2`, was **not found in the literature after two
  search campaigns** ([`bib/l18_status.md`](bib/l18_status.md)) and has a
  draft note ([`notes/dnf_min_ip.md`](notes/dnf_min_ip.md)).
- **A new measurement** ([`tasks/done/F-001.md`](tasks/done/F-001.md)): the L1
  weight of PTF representations on depth-2 TC⁰. EXACT_k has polynomial weight
  (O(n²), structural), IP has exponential weight (20 → 119 → 640); the
  polynomial-weight subclass does not cover depth-2 TC⁰, which quantifies the
  obstacle to extending Williams' method.
- **An open observation**: `min_D W(IP_{2k}) = (3^k−1)/2 = DNF_min(IP)` at the
  3 measured points. The constant 3^{n/2} governs the depth-2 complexity of IP
  in three distinct models (DNF, 2-CNF, PTF).

## Reopening the adversarial loop

A Round 26+ can only be opened on a **verifiable sub-lemma** from one of the
5 generating zones identified at the end of the Atlas (TC⁰ extension,
composite moduli, non-localizing technique, CPT bound, multiplicity
obstructions), not on a "big idea". The Atlas generates targets, not the
model's imagination.

## Disclaimer

This project is an exercise in method: getting LLMs to produce *verifiable*
understanding on a problem that is beyond them (and beyond everyone since
1971). Internal proofs were audited by the adversarial loop and by executable
verification, not by human referees. Do not cite any content of this
repository as an established result without independent verification,
including the Atlas, where each cell states exactly what it rests on.

Most of the repository (the log, the audits, the task files) is written
in French. The Atlas has an English translation:
[`atlas/matrice_barrieres.en.md`](atlas/matrice_barrieres.en.md).
