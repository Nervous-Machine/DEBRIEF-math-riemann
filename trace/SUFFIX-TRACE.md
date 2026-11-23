# Suffix trace: retry fossils in the names

Cycle `trace-2026-11-23-suffix`, run 2026-11-23 23:50–23:56 UTC in the VM. Pre-registered in `prereg_trace_suffix.yaml`
(commit 1164c57, 22:13 UTC, before the dump ran; amendment A1 at c3a9606 replaced the dump script after the first
one proved too slow, before any analysis). Outputs in `trace-suffix/`: `report.md`, `families.tsv` (every family),
`reach_dir2.tsv` (every second-level directory), logs, `suffix.sha256`. The 352 MB name table stays in the VM
(`names_all.tsv`, hash in `suffix.sha256`).

**Question.** A finished proof discards its search, but some of it leaves fossils in the names: `_alt` stacked up to
five times, trailing primes, `_bis`, `_fix`. How common are they, how deep, are the earlier versions still used, how
does this compare with Mathlib's own naming, and where in the proof do they sit? Also, with every constant in the
environment now listed: what share of the archive's constants does the proof use?

**Answer in one line.** Retry marks are rare in the bulk, 1.5% of named constants and below Mathlib's rate of
primes, and concentrated at the hinges: 33 of the 81 constants carrying 1% or more of the proof have one, and 57% of
the proof's lines sit under a retry-named constant. The rewriting happened where the wings are joined. The proof
uses two thirds of the archive's constants; a third was written and never used.

---

## S0. Reach at the constant level

| set | constants | machine-named |
|---|---|---|
| environment (archive + Mathlib + Lean) | 2,701,132 | 1,060,608 |
| archive | 1,905,922 | 747,620 |
| library | 795,211 | 312,988 |
| cone of `riemannHypothesis` | 1,265,256 | 467,304 |
| cone as share of archive | 66.4% | named only 68.9% |

The structure trace measured reach by modules touched (86.5% of lines). By constants the figure is lower: of
1,158,302 named constants in the archive, 798,000 are used by the proof and 360,000 are not. Per top-level directory
the named-constant usage runs from 57% (PositivityTheory) to 86% (CompanionTheory); Development 72%, Formalism
62%, GroundTheory 60%. The lowest second-level directories with at least 1,000 named constants:
Formalism/WachLatticeTwists 23%, Formalism/SizeWindowBrackets 26%, GroundTheory/PAdicHodge 30%,
Formalism/FlagUnipotentLattices 31%, Formalism/PadicSubsetSums 35%. All 331 directories in `trace-suffix/reach_dir2.tsv`.
So the archive was not pruned to the proof before release: a third of what was written is not load-bearing.

## S1. Suffix classes, archive against library

Rates per 1,000 named constants. Machine-generated names (`_proof_n`, `match_n`, instances, …) are excluded throughout.

| class | archive | in the cone | library (Mathlib, Lean) |
|---|---|---|---|
| `_alt` (stacked any number of times) | 2.6 | 3.4 | 0.0 (4 constants) |
| trailing prime `'` | 10.6 | 12.3 | 23.1 |
| `_bis`, `_ter` | 0.1 | 0.1 | 0 |
| fix-words (`_fix` 712, `_fixed` 671, `_rev` 207, `_old` 25, `_new` 24, `_final` 14, `_again` 2, `_v0` 2) | 1.4 | 1.7 | 0.3 |
| any of the four | 14.7 | 17.5 | 23.5 |
| trailing digit after a lowercase letter (noisy) | 11.4 | 10.6 | 2.9 |

Primes are Mathlib house style (`foo` and `foo'`), and Mathlib uses them at twice the archive's rate. `_alt` and the
fix-words are the archive's own: 3,009 `_alt` constants against 4 in all of Mathlib, 1,657 fix-words against 145.

## S2. How deep `_alt` stacks

| depth | archive | in the cone |
|---|---|---|
| `_alt` | 2,789 | 2,498 |
| `_alt_alt` | 206 | 200 |
| `_alt_alt_alt` | 12 | 12 |
| four | 1 | 1 |
| five | 1 | 1 |

The two deepest are `GlobalTheory.T.main_theorem_from_published_results_alt_alt_alt_alt` and the same name with a
fifth `_alt`; both are in the cone, each carrying 1.30% of the proof. The twelve triple-stacks are all called
`main_alt_alt_alt` or similar under `GlobalTheory` namespaces (`AdmTame`, `AlgCharFromGal`, `ChiOneAbove`, …).

## S3. Families: a base name and its variants

A family is a set of named archive constants in one namespace whose last component strips to the same base under
the registered rules.

| | |
|---|---|
| families with two or more members | 5,046, covering 10,178 constants |
| sizes | 4,966 pairs, 74 triples, 6 of four |
| families with no member in the cone | 822 (16.3%) |
| exactly one member in the cone | 1,908, of which the latest variant 1,815 |
| two or more members in the cone (earlier versions still load-bearing) | 2,316 (45.9%) |
| base name used alongside one of its variants | 2,289 |

So when a lemma was rewritten and both versions kept, a little under half the time both are still used; a little
over a third of the time only the newest is. The families of four: `re_one_div_sub_zero_pos` and
`linearIndependent_coe_basis` (all four used), `true_geometry_finite_index`, `main_theorem_from_published_results`
and `local_component_measure_identity` (two of four used), `levi_normalizes_unipotent` (one). Every family is in
`trace-suffix/families.tsv`.

## S4. Where the retries sit

| | |
|---|---|
| hinges (1% or more of the proof) | 81 |
| hinges with a retry suffix | 33 (40.7%) |
| spine constants with one | 4 of 27 (3 on the closet trace's spine; the last step differs by a tie between two constants of equal dominated lines) |
| lines under the top-most retry-named constants | 6,120,389 of 10,660,526 (57.4%) |
| retry share of named constants in the cone, per top-level directory | Development 1.9%, ReciprocityTheory 1.8%, Formalism 1.7%, PositivityTheory 1.4%, CompanionTheory 1.3%, GroundTheory 0.7% |

The 33 (full list with shares in `trace-suffix/report.md`): the spine's `hypotheses_nonempty_of_unramified_exponents_alt`
(11.3%), `allRows_of_open0_alt` (4.2%) and `at_choice_alt` (1.8%); `topCovolSlim2_use_alt_alt` (7.7%),
`vwin_of_hypotheses_H_E_alt` (7.6%), `good_tower_volume_theorem_bis` (3.3%), `ontoX_and_lamLow_of_unitaryGroupHypotheses'`
(2.8%), `ontoX_of_hypotheses_alt_alt` (2.8%), `final_alt_alt` and `final_of_alt` (2.1%, 2.0%), `topCovolG_alt_alt`
(1.8%), `main_alt_alt` (1.4%), the five `main_theorem_*published*` variants at 1.3% to 1.4% each, and twenty more
between 1.0% and 1.8%.

Put against S1: in the bulk, 1.75% of named constants in the cone carry a retry mark; among the 81 hinges, 41% do.
The rewriting is twenty-three times denser at the hinges than in the body.

## Predictions registered before the run

| | prediction | outcome |
|---|---|---|
| P1 | at least 30 per 1,000 named cone constants carry `_alt`; deepest stack at least 5 | **missed** on the rate: 3.4 per 1,000, nine times fewer; the depth held (5) |
| P2 | library `_alt` under 1 per 1,000; archive prime rate within 3× of the library's | held: 0.005; 10.6 against 23.1 |
| P3 | in at least half the families, two or more members are in the cone | **missed**, narrowly: 45.9% |
| P4 | 12 to 35 of the 81 hinges carry a retry suffix | held: 33 |
| P5 | 1.4 to 2.5 million archive constants; 50% to 90% of the named ones used | held: 1,905,922; 68.9% |
| P6 | dump under 10 minutes, analysis under 10 minutes, each under 70 GB | **missed**: the registered dump was stopped after 95 minutes at 90 constants a second (amendment A1); its replacement took 1 m 10 s and 57 GB, the analysis 2 m 33 s and 4.1 GB |

Three of six held. P1 missed in the direction opposite to the earlier traces: I expected the archive to be far more
retry-marked than it is. The retries are not spread through the text; they are at the joins.

## What this does and does not say

A `_alt` is a lemma written again with the first version kept. It does not say why: a corrected hypothesis, a
changed route, a tactic that timed out. It does not say who wrote it. What the counts say is that the body of the
proof was mostly written once, that the joins were written several times, that the top theorem assembling the
published inputs was written at least six times with two versions still in use, and that a third of the archive's
constants were written and are not used. That is the shape of a search that happened at the hinges, which is where
the closet trace said the choices are. The attempt record would say what was tried at each; the archive says only
how many times.

## Procedure notes

The registered dump (`Names.lean`) wrote one line per constant after a per-constant module lookup and ran at about
90 constants a second; it was stopped at 499,418 names and its output set aside unused. `Names2.lean` walks the
environment's module table and writes each module's constants in a block: 186,200 modules, 2,741,727 constants
(2,701,132 distinct names: the environment lists a constant under every module that re-exports it), 1 m 10 s.
The analysis reuses the closet trace's loading and dominator code on the hash-checked walk tables.
Thresholds and regexes were fixed in the registration. Nothing changed standing.
