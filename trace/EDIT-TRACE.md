# The same proof, edited: the archive's shape after four days of community cleanup

Trace cycle `trace-2026-11-25-edit`, run 2026-11-24/25 UTC. Pre-registered in `prereg_trace_edit.yaml` (sha256 in its
sidecar; commit 54c62e8 at 23:45 UTC, two minutes before the first fetch; amendment A1 at 796a1bc after the first run
filled the disk). Instrument in `trace-edit/`; results in `trace-edit/results/`.

## The question

The prior trace found the archive unlike any of a hundred large Mathlib proofs: a chain where Mathlib has fans. Three
differences ride together in that comparison: who reasoned, whether the text was edited, and whether it is one argument
or a library. The control that holds the first and third fixed is the same proof, edited. One exists in progress: since
20 November the Lean community has been cleaning the archive in `leanprover-community/riemann-hypothesis`, whose
`original` branch mirrors the submission and whose `main` was 2,641 commits ahead of it at the commit pinned here
(9282d3a1, 2026-11-24 18:24 UTC), under a comparator that checks on every merge that `Main` still proves the same five
statements with the three standard axioms. The editing is done largely by AI agents under human maintainers; the
repository carries an AGENTS.md addressed to agents. "Edited" here means edited by that process.

## What was done

The repository was cloned at the pinned commit in the VM. Its compiled files were fetched from the community's cache,
not compiled here (a compile took 14 h 48 m and 100 GB in cycle 2; the VM had 96 GB free), and checked three ways:
Lake's own `--no-build` check that every compiled file matches the pinned source by trace hash (exit 0), a byte
comparison of the `original` branch against the tarball this record pinned (identical, every Lean file), and a
recompile of twenty random source files compared with the cached ones constant by constant. The whole dependency graph
was then written from the module table (7 m 05 s; 71,018 modules, 59,828 of them the archive's; 2,268,083 constants,
188,283,699 edges) and the prior trace's measures were computed, unchanged, for the proof below `riemannHypothesis`
and the other four entry theorems.

## The result

| measure | archive, 23 Nov | edited archive | Mathlib Q1 | median | Q3 |
|---|---|---|---|---|---|
| cone constants | 1,265,256 | 1,186,369 | 30,253 | 36,032 | 46,352 |
| dominated lines | 10,660,526 | 10,056,951 | 75,408 | 92,248 | 125,716 |
| spine share, step 1 | 100.0% | 100.0% | 8.5% | 19.8% | 38.7% |
| step 2 | 100.0% | 100.0% | 7.0% | 13.5% | 26.4% |
| step 3 | 100.0% | 76.9% | 4.9% | 9.9% | 19.2% |
| step 5 | 66.8% | 40.5% | 3.2% | 6.7% | 13.1% |
| step 8 | 11.3% | 4.3% | 1.4% | 3.2% | 8.4% |
| spine length | 27 | 26 | 20 | 24 | 29 |
| hinges at 1% | 81 | 75 | 30 | 37 | 46 |
| median own lines of hinges | 4 | 7 | 8 | 10 | 13 |
| hinges with a retry mark | 32 | 23 | 0 | 0 | 0 |
| largest joint, share joined | 27.2% | 26.3% | 63.9% | 80.2% | 91.5% |
| three largest joints | 71.8% | 72.1% | 93.7% | 96.5% | 98.4% |
| largest directory's share of cone lines | 43.9% | 41.6% | 14.6% | 15.7% | 16.9% |
| retry marks per 1,000 named constants | 15.4 | 4.7 | 0.4 | 0.4 | 0.4 |

The archive as a whole is a quarter smaller (1,416,150 constants against about 1.9 million; 59,828 modules against
175,187 files, because files have been merged). The proof itself is six percent smaller. The five entry theorems now
reach 83.8% of the archive's constants, against 66% before: the unused third is being deleted.

**Read by step, the spine fell: 100% to 77% at step 3, 67% to 40% at step 5. Read by constant, it did not move.** The
edit removed two wrapper theorems from the top of the proof (`rhOfAll` and `allChi`, each dominating 100%, in the old
`Supplements/Kernels/MainTheorems`) and put the Main statement `LFunction_ne_zero_of_half_lt_re` directly above
`everyCharacter`. Every constant on the old spine is still on the new one, one step higher, with the same share:

| constant | share, 23 Nov | share, edited |
|---|---|---|
| everyCharacter | 100.0% | 100.0% |
| everyCharacter_of_row | 77.4% | 76.9% |
| every_character_of_literature_of_vWin | 66.8% | 66.8% |
| every_character_of_theta_integrals_local_matching | 39.6% | 40.5% |
| nonempty_hyps_definite_side_of_closed_bound | 33.3% | 34.3% |
| hypotheses_nonempty_of_unramified_exponents_alt | 11.3% | 11.6% |
| allRows_of_open0_alt | 4.2% | 4.3% |
| lg1_sLp_sO_hTF | 1.8% | 1.9% |

The largest joint is the same constant with the same share (26.3% against 27.2%). Of the 81 hinges, 61 keep their
names; on those, own lines are unchanged for 45, longer for 12, shorter for 4, median 7 before and after. The 20 that
are gone were short wrappers and retry variants (the `main_theorem_from_published_results_alt_alt_alt_alt` family
among them), which is why the median own length rose from 4 to 7: the short ones were deleted, the survivors were not
lengthened. All 23 retry-marked hinges are old hinges with their old names; none has been renamed yet, and 9 marked
hinges were removed. Retry marks across the archive fell from 15.4 to 4.7 per thousand named constants, mostly by
deletion of unused variants.

## Predictions

| | registered | outcome |
|---|---|---|
| P0 | original branch identical to the tarball | **held** (diff exit 0) |
| P1 | both caches fetch, `--no-build` exits 0, community cache under 60 GB | **missed on size**: fetch and check held; `.lake/build` is 71.1 GB |
| P2 | all twenty recompiled modules match the cached ones exactly | **missed as worded**: 17 of 20 exact; 2 differ only in the `_private.` prefix of match-splitter auxiliaries (`_private.src.…` from the recompile's path against `_private.Development.…` from Lake), same constants and counts; 1 recompile failed under `lake env lean` without the project's Lean options and matched exactly when run with them (diagnostic, not registered) |
| P3 | cone shrinks under 15%, archive over 10%, reach above 66% | **held**: 6.2%, about 25%, 83.8% |
| P4 | spine at least 90% at step 3 and 50% at step 5 | **missed**: 76.9% and 40.5%, because two wrapper steps were removed from the top; aligned by constant the spine is unchanged (diagnostic, not registered) |
| P5 | largest joint under 40% | **held**: 26.3% |
| P6 | 60 to 100 hinges; median own lines at most 6 | **missed on length**: 75 hinges; median 7 |
| P7 | 1 to 31 retry-marked hinges; rate under 15.4 | **held**: 23; 4.7 |
| P8 | walk under 30 min, analysis under 4 h, whole run under 10 h | **held**: 7 m 05 s (73.5 GB peak), 3 m 06 s, 22 minutes over the two runs |

Five of nine held. P4 and P6 were written against step indices and a median that the removal of short wrapper
theorems moves without touching the structure; the hypothesis they encoded, that the chain survives this much editing,
holds on the constant-aligned comparison. The next registration of this kind should align the spine by constant and
predict shares at named constants.

## What it means

Four days and 2,641 commits of editing, by agents under maintainers, deleted a quarter of the archive, merged two
thirds of its files, removed wrappers and dead variants, and left the dominator tree of the proof as it was: the same
constants carry the same shares, the same joint gathers the same quarter, the hinges are the same hinges. Nothing in
the comparison with Mathlib has moved toward Mathlib except the two measures that counted short wrappers. So far,
editing explains none of the chain. That is a statement about this edit at this commit, under a process whose stated
goal is readability and modularity "while preserving the logic of the proof"; it does not say what a rewrite that
changed the logic would do, and the author has said he expects the proof to simplify.

## What it does not settle

Whether editing can change the shape at all: this is one partial state of an ongoing edit, and the right next cycle is
this one again at a later commit under a new registration, aligned by constant. Nothing about the third difference,
one argument against library lemmas, which needs large single-purpose human Lean projects measured the same way.
Nothing about why any proof has the shape it has. The compiled files were the community's; Lake's trace check and
the twenty recompiles are the checks on them, and a compile from source would be a new registration with more disk.

## Files

`trace-edit/ArchiveGraph.lean`, `SpotCheck.lean`, `edit.py`, `run_edit.sh`, `run_edit2.sh` (A1), `edit_diag.py` and
`SpotNames_diag.lean` (diagnostics, not registered); `trace-edit/results/`: `report.md`, `shapes_edit.tsv`, the spine
and hinge tables for `riemannHypothesis`, `spot_results.tsv`, `P0_diff.txt`, `head.txt`, `manifest_revs.txt`,
`started.txt`, `walk_out.txt`, the cache logs, and `outputs_A1.sha256` with the hashes of every output including the
graph tables (nodes.tsv 98db623a…, edges.tsv d735cac1…), which stay in the VM.
