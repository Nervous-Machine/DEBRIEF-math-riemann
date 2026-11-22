# Asks — The claimed proof of the Riemann Hypothesis announced by Levent Alpöge on 20 November 2026, built with Claude and released as Lean 4 code

Each open gap below is a place a contribution can land. A contribution is one cycle in this repository's ledger, under your name. How to contribute, and the templates: https://github.com/Nervous-Machine/DEBRIEF/blob/main/CONTRIBUTING.md

## 1. The Lean development has not been built or kernel-checked by anyone outside the claimant (ledger id EG1)

The claimant reports a Lean development that compiles with standard axioms only. Nobody outside the claimant has reported building it.

Status: in cycle.

- **a pre-registered rerun: fetch at the pinned commit, build, confirm no sorry or admit, print the axioms** — contribution kind: rerun; who could act: anyone with a machine and a few hours.

Signal expected: a rerun cycle reporting build exit status, the sorry/admit scan and the axiom list for the main theorem. Resolution by: none registered.

## 2. Do the formal statements say what the problem asks? (ledger id EG2)

A Lean check establishes that the formal statement follows from its hypotheses. Whether that formal statement is the problem as posed is a separate question that a person has to answer. A third-party formalization of the problem statement exists, so part of this can be compared by machine.

Status: proposed.

- **a machine comparison of the claimant's main theorem with the third-party formal statement RiemannHypothesis in leanprover-community/mathlib4, then a human read of any difference** — contribution kind: trace (a reading guide); who could act: anyone who can read Lean; the two statements are public.
- **two independent mathematicians read the formal statement against the problem as posed and sign, or refuse** — contribution kind: read; who could act: a mathematician in the problem's area, about an hour with a reading guide.

Signal expected: a trace cycle and two signed read cycles, or a refusal naming the difference. Resolution by: none registered.

## 3. No independent mathematician has reported reading the proof, and there is no referee report (ledger id EG3)

The claim was announced by its author on the author's own site. No independent reading, referee report or journal submission is on the public record.

Status: proposed.

- **a read cycle by a mathematician in the area who is not an author, signing or refusing each main step** — contribution kind: read; who could act: a mathematician in the problem's area.
- **a referee report or journal acceptance, recorded by date** — contribution kind: data; who could act: a journal; the record notes the date when it happens.

Signal expected: a signed or refused read cycle; a dated referee report. Resolution by: none registered.

## 4. The Generalized Riemann Hypothesis statements are the claimant's own definitions, with no third-party formal statement to compare against (ledger id EG4)

Four of the five results in Main.lean are stated with definitions the claimant wrote in Statements.lean, about zeros and non-vanishing of Dirichlet L-functions. Mathlib has no definition of the Generalized Riemann Hypothesis to compare them with, so whether these four definitions say what the Generalized Riemann Hypothesis says is entirely a human read.

Status: proposed.

- **two independent mathematicians read the four definitions in Statements.lean against the Generalized Riemann Hypothesis as usually stated and sign, or refuse** — contribution kind: read; who could act: an analytic number theorist, about an hour with the file.

Signal expected: two signed read cycles, or a refusal naming the difference. Resolution by: none registered.

## 5. Compiled-output hashes agree byte for byte only between builds under the same absolute source path (ledger id EG5)

The record's certification rule asks two independent builders to publish matching hashes of the compiled output. Cycle 1 found that Lean writes each source file's absolute path into the output of any module that produced a warning, which is about half of this archive, so two builders in different directories can never match on those files. The rule needs a comparison that does not depend on where the build ran.

Status: proposed.

- **a decision by the record keeper on what two independent builders compare: the files that embed no path, the lean4export output (whose determinism is an open question on Sutherland's page and in Deicyde's notes), or a shared build path; then that comparison, run** — contribution kind: decision by the named party; who could act: Heidi Bennett, who set the rule, with the kernel.
- **a rebuild under /home/ubuntu/grh/src/lean, Sutherland's published path, or a comparison of the exported proof, whichever the decision names; either is a new pre-registered cycle** — contribution kind: rerun; who could act: Nervous Machine, once the rule is revised, about 15 hours of machine time.

Signal expected: a revised rule in this record, or a comparison on a path-independent artifact, or a rebuild under Sutherland's path that matches his manifest. Resolution by: none registered.
