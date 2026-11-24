# Crossing trace at the third directory level

Cycle `trace-2026-11-24-crossing3`, run 2026-11-24 01:36–01:41 UTC in the VM. Pre-registered in
`prereg_trace_crossing3.yaml` (commit 08c685d, 01:36 UTC, before the run). Outputs in `trace-crossing3/`:
`report.md`, `crossings3.tsv` (the depth-3 pair table, 28,301 pairs), `archive_joints3.tsv`, `mathlib_joints3.tsv`,
`archive_top3_pairs3.tsv` (every crossing pair of the three largest joints), logs, `crossing3.sha256`.

**Question.** The depth-2 test saturated because 26 bins is too few. At depth 3 Mathlib has 590 directories. Does
the test discriminate now, and what does it say?

**Answer in one line.** The test unsaturates and then fails the other way. Sixteen of the archive's twenty joints
now realise crossings, and so do 23 of 100 Mathlib joints; but every crossing pair the archive realises, and 72
percent of Mathlib's, is a pair of directories that no Mathlib theorem has ever depended on together, so the
rarity score is zero for everyone and separates nothing. The pairs themselves are library corners (free algebras,
Dold–Kan, box integrals, derangements), reached incidentally by deep cones, not mathematical junctions. A crossing
test for this proof needs a semantic layer, which published theorems a wing rests on, not which Mathlib folders it
touches. One result survives both resolutions: the archive's wings are more alike than Mathlib's.

---

## Y1. The table

590 directories at depth 3; 448 are depended on by some Mathlib theorem outside their own directory; 28,301 pairs
seen together across 253,598 theorems, out of about 100,000 possible pairs among the 448. The table is sparse: most
pairs of directories have never co-occurred in one theorem's direct dependencies.

## Y2. The archive

The cone reaches 405 of 590 directories. The twenty largest joints:

| joint | joins | footprint | Jaccard, two largest wings | exclusive dirs | crossing pairs | never seen together in Mathlib |
|---|---|---|---|---|---|---|
| `every_character_of_literature_of_vWin` | 27.2% | 394 | 0.09 | 23 | 122 | 122 |
| `everyCharacter` | 22.6% | 405 | 0.09 | 37 | 232 | 228 |
| `nonempty_hyps_definite_side_of_closed_bound` | 22.0% | 380 | 0.05 | 4 | 0 | |
| `everyCharacter_of_row` | 10.6% | 397 | 0.05 | 20 | 51 | 51 |
| `hypotheses_nonempty_of_unramified_exponents_alt` | 7.1% | 380 | 0.05 | 6 | 9 | 9 |
| `vwin_of_hypotheses_H_E_alt` | 6.3% | 347 | 0.06 | 16 | 84 | 80 |
| `every_character_of_theta_integrals_local_matching` | 6.3% | 380 | 0.21 | 70 | 0 | |
| `topCovolSlim2_use_alt_alt` | 3.1% | 361 | 0.06 | 21 | 38 | 38 |
| `steps_holds` | 2.5% | 327 | 0.27 | 47 | 0 | |
| `allRows_of_open0_alt` | 2.4% | 361 | 0.12 | 53 | 453 | 451 |
| `geometric_realization_of_weight_one` | 2.2% | 356 | 0.16 | 50 | 651 | 644 |
| … nine more at 0.8% to 1.7% | | 265–373 | 0.01–0.41 | 3–35 | 0–90 | all or nearly all |

What only one wing reaches, at the top joint: the 39.6% wing alone reaches Analysis/BoxIntegral, Analysis/ODE,
Combinatorics/Additive, Control, Dynamics/FixedPoints, Geometry/Convex, LinearAlgebra/Transvection,
NumberTheory/Real, NumberTheory/Zsqrtd, Order/Atoms, Order/Extension, Probability/Independence, and more; the 7.7%
wing alone reaches Algebra/FreeAlgebra and Dynamics; the literature-inputs wing alone reaches
AlgebraicTopology/DoldKan, CategoryTheory/LiftingProperties, CategoryTheory/Subobject, NumberTheory/ClassNumber,
Topology/FiberBundle. The rarest pair the joint "brings together" is therefore Algebra/FreeAlgebra with
AlgebraicTopology/DoldKan. That is not a mathematical crossing. It is two pieces of infrastructure that two large
cones happened to pull in from different places.

## Y3. Mathlib

| measure | Mathlib Q1 | median | Q3 | archive, largest joint | archive, median of top 20 |
|---|---|---|---|---|---|
| directories the cone reaches, of 590 | 148 | 166 | 179 | 405 | |
| Jaccard distance of the two largest wings | 0.18 | 0.35 | 0.57 | 0.09 | 0.09 |
| directories exclusive to one wing | 8 | 19 | 42 | 23 | 18 |
| crossing pairs | 0 | 0 | 0 | 122 | 31 |
| joints with at least one crossing | 23 of 100 | | | | 16 of 20 |
| rarest crossing, ratio to chance | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| share of a joint's crossings never seen together in Mathlib | 58% | 72% | 83% | 100% | 100% |

Mathlib's own rarest crossings are the same kind of thing: Analysis/BoxIntegral with LinearAlgebra/Dual under a
Hurwitz zeta residue, Data/Matrix with Geometry/Convex under a bump function. Nobody would call those junctions
of ideas.

## What the two resolutions together say

At 26 bins every wing touches everything and the test is empty. At 590 bins the pair table is sparse, deep cones
pick up incidental corners of the library, and the test calls everything maximally rare. There is no directory
depth at which "which Mathlib folders a wing reaches" measures what Heidi Bennett's general-relativity question
asks, which is whether the ideas joined had been joined before. The instrument for that is semantic: which
published theorems (the `GlobalTheory.Published.*` hypotheses the structure trace found, the literature inputs named
in the joint statements) each wing rests on, and whether those results had met in print. That is a reading with a
bibliography, and this record can hold it when someone gives it.

The one thing both resolutions agree on is structural. The archive's two largest wings, at every top joint, draw
on nearly the same library (Jaccard distance 0.09 against a Mathlib median of 0.35, below the Mathlib first quartile
at both depths). Fans built from independent inputs have unlike wings; stages of one route have like wings. That is
the third measurement this day to point the same way as the chain shape, the short rewritten hinges and the single
concentrated directory: a search directed down one route, with its choices at the joins.

## Predictions registered before the run

| | prediction | outcome |
|---|---|---|
| P1 | 200 to 600 depth-3 directories; the archive reaches at least 60% | held: 590; 405 (69%) |
| P2 | at least 10 of 20 archive joints realise a crossing | held: 16 |
| P3 | some archive joint's rarest pair has ratio below 0.5 | held, by sparsity: every realised pair has ratio 0 |
| P4 | the archive's median rarest ratio inside the Mathlib interquartile range | held, hollow: both are 0.00 and the range is 0.00 to 0.00 |
| P5 | Jaccard distance at the archive's largest joint below the Mathlib median | held: 0.09 against 0.35 |
| P6 | under 25 minutes and 60 GB | held: 4 m 30 s, 2.9 GB |

Six of six held; two are hollow and marked so. The registration predicted the test would unsaturate and did not
predict that the rarity score would then collapse to zero for everyone; that is the finding, and it was not
foreseen.

## Procedure notes

Same script as the depth-2 trace with the depth as a parameter and the pair table built from the Mathlib graph at
that depth; footprints as bit masks over 590 bins; wings and joints as before. Nothing changed standing.
