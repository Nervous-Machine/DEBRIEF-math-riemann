# Proof-shape prior: the archive against 3,000 Mathlib proofs

Cycle `trace-2026-11-24-prior`, run 2026-11-24 00:54–00:59 UTC in the VM. Pre-registered in `prereg_trace_prior.yaml`
(commit d4ca9fb, 00:54 UTC, before the Mathlib graph was written). Outputs in `trace-prior/`: `report.md`,
`shapes.tsv` (one row per large proof), `crossings.tsv` (every directory pair), logs, `prior.sha256`. The Mathlib
graph itself (73 MB of nodes, 2.0 GB of edges) stays in the VM, hashes in `prior.sha256`.

**Question.** The three traces of 23 November measured one proof. One proof is one point. Mathlib, in the same
environment with the same kernel and naming habits, is a population of 253,598 named theorems. What does a Mathlib
proof look like under the same measures, and where does the archive fall?

**Answer in one line.** Mathlib proofs are fans and the archive is a chain. A large Mathlib proof has its mass meet
at the root, with the spine down to 10 percent by the third step; the archive holds 100 percent for three steps and
two thirds at the fifth. Its hinges are twice as many and half as long, carry rewrite marks where Mathlib's carry
none, and a single subject directory holds 44 percent of its lines against 16 percent in Mathlib. One thing the
archive shares with Mathlib: the largest directory is substrate in both, dominated by nothing in itself.

---

## Q1. How big is a Mathlib proof?

The cone of a theorem is every constant the kernel uses for it. For 3,000 Mathlib theorems drawn uniformly:

| decile | 10% | 20% | 30% | 40% | 50% | 60% | 70% | 80% | 90% | max |
|---|---|---|---|---|---|---|---|---|---|---|
| cone constants | 399 | 549 | 767 | 1,501 | 2,224 | 3,724 | 6,496 | 10,972 | 16,960 | 62,102 |

Median 2,224, mean 6,180. The archive's cone is 1,265,256 archive constants plus 67,981 of Mathlib's at its
boundary: twenty times the largest Mathlib proof in the sample, five hundred times the median. The ten largest
sampled Mathlib proofs are all in the archive's neighbourhood: number fields, Dirichlet L-functions, Hurwitz zeta,
modular forms, Mahler measure. Mathlib's deepest region is the one the archive builds on.

## Q2. Shape

The 100 largest sampled cones (30,000 to 62,000 constants), under the measures of the three archive traces.

| measure | Mathlib Q1 | median | Q3 | archive |
|---|---|---|---|---|
| cone constants | 30,253 | 36,032 | 46,352 | 1,265,256 |
| spine share, step 1 | 8.5% | 19.8% | 38.7% | 100.0% |
| step 2 | 7.0% | 13.5% | 26.4% | 100.0% |
| step 3 | 4.9% | 9.9% | 19.2% | 100.0% |
| step 5 | 3.2% | 6.7% | 13.1% | 66.8% |
| step 8 | 1.4% | 3.2% | 8.4% | 11.3% |
| spine length, steps to a leaf | 20 | 24 | 29 | 27 |
| step at which the spine leaves the root's directory | 2 | 5 | 10 | 13 |
| hinges at 1% | 30 | 37 | 46 | 81 |
| median own lines of hinges | 8 | 10 | 13 | 4 |
| longest hinge, lines | 90 | 93 | 106 | 88 |
| hinges with a rewrite mark (primes excluded) | 0 | 0 | 0 | 32 |
| hinges with a prime | 1 | 2 | 2 | 1 |
| largest joint, share of lines meeting there | 63.9% | 80.2% | 91.5% | 27.2% |
| three largest joints together | 93.7% | 96.5% | 98.4% | 71.8% |
| largest directory's share of cone lines | 14.6% | 15.7% | 16.9% | 43.9% |
| largest share any constant in that directory dominates | 0.5% | 0.9% | 8.9% | 1.7% |
| rewrite marks per 1,000 named constants (primes excluded) | 0.4 | 0.4 | 0.4 | 15.4 |

The archive's percentile in the Mathlib distribution: spine share at step 3, 100th; at step 5, 100th; hinges, 100th;
median own lines of hinges, 0th; largest joint, 0th; largest directory's share, 100th; largest directory's max
dominator, 58th; rewrite marks, 100th; spine length, 67th.

**Fans and chains.** In a Mathlib proof the mass meets at the root: the theorem itself joins 80 percent of its
lines from independent inputs, and the three largest joints account for 96 percent. The spine is thin from the
first step. In the archive the root joins nothing; the three wrappers pass everything to one theorem, that theorem
passes 77 percent to one child, and so on, so that the largest joint is only 27 percent and the three largest 72
percent. The archive's spine length is ordinary, 27 steps against a Mathlib median of 24. What is not ordinary is
how much stays on it.

**Glue.** The archive has twice the Mathlib number of hinges and they are half as long: a median of 4 own lines
against 10, below every one of the 100 Mathlib proofs. Mathlib's hinges carry rewrite marks essentially never
(median 0 of about 37, and 0.4 per 1,000 constants overall); 32 of the archive's 81 do, and the overall rate is
38 times Mathlib's.

**Substrate is normal; concentration is not.** The earlier observation that abelian-variety theory is reached from
everywhere and dominated by nothing in itself turns out to be how Mathlib's largest directories behave too: the
median large Mathlib proof's biggest directory has a top dominator of 0.9 percent. The archive is unusual not in
having substrate but in how much of it: 44 percent of its lines in one directory against a Mathlib median of 16.

## Q3. Crossings

For every named Mathlib theorem, the set of second-level directories its direct dependencies come from, excluding
its own. 27 directories, 206 pairs seen together.

| most common pairs | theorems | | rarest pairs among common directories | theorems |
|---|---|---|---|---|
| Algebra + Data | 77,383 | | Geometry + SetTheory | 1 |
| Data + Order | 58,893 | | CategoryTheory + MeasureTheory | 11 |
| Algebra + Order | 39,208 | | Geometry + MeasureTheory | 12 |
| Data + Topology | 29,268 | | MeasureTheory + SetTheory | 13 |
| Data + Logic | 26,209 | | Combinatorics + MeasureTheory | 13 |
| Algebra + Topology | 26,005 | | CategoryTheory + SetTheory | 23 |

The full table with each pair's count against what independence would predict is `trace-prior/crossings.tsv`. It
describes Mathlib only. Scoring the archive's joins against it would need a mapping from the archive's subject
directories to Mathlib's, which is a reading, and is not done here.

## Predictions registered before the run

| | prediction | outcome |
|---|---|---|
| P1 | median cone 300 to 3,000 constants; at least 500 of 3,000 reach 2,000 | held: 2,224; 1,583 |
| P2 | median spine share at step 3 below 50%; the archive's 100% above Mathlib's Q3 | held: 9.9%; yes |
| P3 | median hinges 30 to 90; the archive's 81 inside the Mathlib interquartile range | **missed** on the second half: median 37, but the IQR is 30 to 46 and the archive is above every Mathlib proof |
| P4 | median own lines of hinges at least 8; the archive's 4 below Mathlib's Q1 | held: 10; yes |
| P5 | in at least 60 of 100, the largest directory's top dominator holds at least 10%; the archive's 1.72% below Mathlib's Q1 | **missed** on both halves: Mathlib's Q3 is 8.9%, so fewer than 25 reach 10%, and the archive sits at the 58th percentile. Substrate is normal |
| P6 | walk under 90 minutes and 70 GB; analysis under 30 minutes | held: 54 s and 7.5 GB; 2 m 25 s |
| P7 | the most common pair is Algebra with Order or Data | held: Algebra + Data |

Five of seven held. P5 is the instructive miss: I took the substrate pattern for a peculiarity of the archive, and
it is how large formal libraries look.

## What this does and does not say

Mathlib's theorems are mostly short, written by many people over a decade, and curated; the archive is one proof
written in months under direction. The comparison says the archive's shape is at the edge of the Mathlib
distribution on five measures and inside it on two. It does not say why. A chain shape with short, rewritten hinges
is what one would expect from a route assembled stage by stage toward a fixed target; it is also what one would
expect from a code base no one has refactored. Those are the two stories from the suffix trace again, and this
cycle does not separate them.

## The author's statement, read after this cycle

On 23 November, after this trace ran, Levent Alpöge wrote in public that the 250,000-page figure was a joke, that he
wrote no account he thought readable and "went off the Lean to lengthmaxx", that the Lean is "full of garbage
obviously, but compiles", and that he expects most of it to be unnecessary (cycle external-2026-11-23-alpoge). The
measures above were taken without that statement and are unchanged by it. Read with it, they describe an artifact its
author did not clean, and nothing in them should be taken as a measure of effort or method. What the kernel uses is
still what the kernel uses.

## Procedure notes

The Mathlib graph (772,126 module-constant rows, 771,129 distinct constants, 29.7 million edges, 20.4 million
distinct) was written in 54 seconds and 7.5 GB by walking the environment's module table and reading each module's
declaration-range table in one call. The archive walk of 23 November took 4 h 18 m for 1.3 million constants
because it looked up each constant's module and range one at a time inside the interpreter; the same overhead slowed
the first name dump of the suffix trace. The archive's dependency graph could be rewritten in minutes by the same
method; the one on record is correct as it stands and was not redone. The analysis reuses the archive traces'
dominator code per root. Sampling, thresholds and the seed were fixed in the registration. Nothing changed standing.
