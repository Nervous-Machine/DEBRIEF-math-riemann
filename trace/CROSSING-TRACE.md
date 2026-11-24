# Crossing trace: do the wings of a joint come from different places?

Cycle `trace-2026-11-24-crossing`, run 2026-11-24 01:17–01:21 UTC in the VM. Pre-registered in `prereg_trace_crossing.yaml`
(commit 50ac0a6, 01:15 UTC; amendment A1 at 50e4547 after the first run failed on a cycle in the constant graph,
before any output). Outputs in `trace-crossing/`: `report.md`, `archive_joints.tsv`, `mathlib_joints.tsv`,
`mathlib_trees.json` (dominator trees of the eight largest Mathlib proofs, for drawing), logs, `crossing.sha256`.

**Question.** The general-relativity test: not whether the glue is short, but whether the domains it joins had been
joined before. For every joint, which Mathlib directories does each wing reach through the library boundary, how
different are the wings in those terms, and how rare in Mathlib are the pairs a joint brings together? The same for
the largest joint of each of the 100 large Mathlib proofs of the prior trace.

**Answer in one line.** At the resolution of Mathlib's directory tree the test saturates. The archive's cone reaches
25 of 26 directories and every wing of every large joint reaches 21 to 25 of them, so no joint brings together a
directory pair its wings did not already share. Mathlib's own largest joints behave the same way: 4 of 100 realise
any exclusive pair. The archive's wings are more alike than Mathlib's (Jaccard distance 0.08 against a median of
0.27), which is the one place it leaves the Mathlib range. A finer instrument is needed, and the data for it exists.

---

## X1. The archive

The cone of `riemannHypothesis` reaches every Mathlib directory except `Mathlib/Computability`. The twenty largest
joints (by lines meeting at them), with their six largest wings:

| joint | joins | footprint (of 26) | Jaccard distance, two largest wings | directories exclusive to one wing | crossing |
|---|---|---|---|---|---|
| `every_character_of_literature_of_vWin` | 27.2% | 25 | 0.08 | 1 | none |
| `everyCharacter` | 22.6% | 25 | 0.04 | 1 | none |
| `nonempty_hyps_definite_side_of_closed_bound` | 22.0% | 25 | 0.04 | 0 | none |
| `everyCharacter_of_row` | 10.6% | 25 | 0.08 | 2 | none |
| `hypotheses_nonempty_of_unramified_exponents_alt` | 7.1% | 25 | 0.04 | 1 | none |
| `vwin_of_hypotheses_H_E_alt` | 6.3% | 23 | 0.00 | 0 | none |
| `every_character_of_theta_integrals_local_matching` | 6.3% | 25 | 0.12 | 3 | none |
| … thirteen more at 0.8% to 3.1% | | 21–25 | 0.00–0.27 | 0–2 | none |

"None" means that no pair of directories exists with one directory reached only by one wing and the other only by
another; the exclusive directories, where there are any, are all on the same wing (the largest), so there is nothing
to score. The wing lists are in `trace-crossing/report.md`; the one directory only the largest wing reaches, at the
two top joints, is `Mathlib/Control`.

## X2. Mathlib's largest joints, same measures

| measure | Mathlib Q1 | median | Q3 | archive, largest joint | archive, median of its top 20 |
|---|---|---|---|---|---|
| directories the cone reaches | 13 | 14 | 16 | 25 | |
| Jaccard distance of the two largest wings | 0.14 | 0.27 | 0.39 | 0.08 | 0.04 |
| directories exclusive to one wing | 0 | 1 | 3 | 1 | 1 |
| joints realising any exclusive pair | 4 of 100 | | | 0 of 20 | |

The four Mathlib joints with a scorable crossing: two bring Combinatorics together with NumberTheory or Dynamics,
pairs Mathlib has never otherwise depended on together; two bring Combinatorics with Geometry, a pair five times
more common than chance. Four is too few to call a distribution.

## What the saturation means

The instrument is the directory tree, 26 bins. A cone of 30,000 constants already touches 14 of them; a cone of
1.3 million touches 25. Once every wing touches nearly everything, "which directories only this wing reaches" is
empty by construction, and the test reports nothing for the archive and almost nothing for Mathlib. Two things
survive the saturation. The archive's wings are more alike than Mathlib's, below the Mathlib first quartile, which
fits the chain shape of the prior trace: wings that are stages of one route draw on the same library, where wings
that are independent inputs to a fan do not. And the archive reaches 25 directories where no Mathlib proof in the
sample reaches more than 20: it uses nearly all of Mathlib.

The finer instrument is the same computation over Mathlib's third-level directories (a few hundred bins) or over
the boundary constants themselves, weighted by how rarely each is used, so that a wing's footprint is what it
distinctively reaches rather than everything it touches. The pair table for either can be built from the Mathlib
graph already on disk. That is a new registration, not a change to this one.

## Predictions registered before the run

| | prediction | outcome |
|---|---|---|
| P1 | the archive's cone reaches at least 24 of 27 directories | held: 25 of 26 (one directory, with no pairs in Mathlib, is absent from the pair table) |
| P2 | Jaccard distance of the two largest wings at the largest joint below 0.3 | held: 0.08 |
| P3 | no archive joint realises a crossing rarer than one fifth of chance | held, vacuously: no archive joint realises any crossing |
| P4 | the archive's largest joint inside the Mathlib interquartile range on Jaccard distance and on exclusive directories | **missed** on the first: 0.08 is below the Mathlib Q1 of 0.14; the second held (1, inside 0 to 3) |
| P5 | fewer than half of Mathlib's largest joints realise any exclusive pair | held: 4 of 100 |
| P6 | under 20 minutes and 60 GB | held: 4 m 00 s, 2.7 GB (after a failed first run of 1 m 27 s) |

Five of six held; P3 is a hollow pass and is marked as one.

## Procedure notes

The first run failed in the footprint pass, which assumed the constant graph has no cycles; an inductive type, its
constructors and its recursor name one another, and the walk records those edges in both directions. The pass now
iterates to a fixed point (three passes on the archive), as the dominator computation always did. Recorded as
amendment A1 before any output existed. Footprints are bit masks over the 26 directories that appear in the prior
trace's pair table; wings are a joint's six largest dominated children; the archive's twenty joints are those of the
closet trace. Nothing changed standing.
