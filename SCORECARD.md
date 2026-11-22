# The claimed proof of the Riemann Hypothesis announced by Levent Alpöge on 20 November 2026, built with Claude and released as Lean 4 code

On 20 November 2026 Levent Alpöge, a mathematician at Anthropic, posted a four-page note on his personal site saying that he believes he has, working with Claude, found a proof of the Riemann Hypothesis, that the method also resolves the Generalized Riemann Hypothesis for Dirichlet L-functions, and that the argument has been formalized in Lean 4 without extra assumptions. He released no paper, only the Lean code. Nervous Machine fetched the archive the same day and pinned it by hash. It holds 175,187 Lean files, about 17.4 million lines, built against a pinned Mathlib. Its entry file states Mathlib's own definition RiemannHypothesis as its main result. Andrew Sutherland at MIT reports an independent compile, axiom audit and kernel replay; Nervous Machine's own pre-registered build compiled 32,018 of the 175,187 modules before its disk filled and is resumed as cycle 2. No independent mathematician has reported reading the argument. Nothing here has standing yet.

_Rendered from the briefing record. Items marked internal in the ledger (how the framework works, the state of the record) stay in `ledger.json` and are not shown here._

Record quality: full ledger. Opened at tier zero on 2026-11-20. Cycle 1's build halted on our own disk, not on the archive; cycle 2 finished it on 2026-11-21. One finding, accepted, on 2026-11-22. Nothing certified: the certification rule waits on a path-independent comparison (EG5).

**Standing.** Certified 0. Accepted 1. Refuted 0. Open gaps 4. An open gap is an input or question nobody has settled; it is not a finding and has no standing.

## Findings

| id | kind | standing | basis | cycles |
|---|---|---|---|---|
| F1 | learned | **accepted** | one pre-registered build by a party independent of the claimant, under amendment A1 of prereg_cycle1.yaml: one party's report gives accepted; certified needs a second independent party's matching hash of the compiled output, which the path dependence recorded in EG5 prevents until the rule is revised or a shared comparison is run | 1, 2 |

## Cycles, in order

| cycle | dated | by | kind | written first | verdict |
|---|---|---|---|---|---|
| 0 | 2026-11-16 to 2026-11-20 |  | replay | no | admitted |
| external-2026-11-20 | 2026-11-20 | None | replay | no | admitted |
| trace-2026-11-20 | 2026-11-20 | Nervous Machine (Heidi Bennett; Claude Fable 5.1 as the operating agent) | trace | no | confirmed |
| 1 | 2026-11-20 to 2026-11-21 | Nervous Machine (Heidi Bennett; Claude Fable 5.1 as the operating agent) | rerun | yes | mixed |
| external-2026-11-21 | 2026-11-21 | None | replay | no | admitted |
| 2 | 2026-11-21 to 2026-11-22 | Nervous Machine (Heidi Bennett; Claude Fable 5.1 as the operating agent) | rerun | yes | confirmed |

## Gaps, in the order that would settle things fastest

| priority | gap | status | closes with | who could act | signal expected | resolution by |
|---|---|---|---|---|---|---|
| 1 | The Lean development has not been built or kernel-checked by anyone outside the claimant | resolved learned | a pre-registered rerun: fetch at the pinned commit, build, confirm no sorry or admit, print the axioms | anyone with a machine and a few hours | a rerun cycle reporting build exit status, the sorry/admit scan and the axiom list for the main theorem | 2026-11-22, cycle 2 |
| 2 | Do the formal statements say what the problem asks? | proposed | a machine comparison of the claimant's main theorem with the third-party formal statement RiemannHypothesis in leanprover-community/mathlib4, then a human read of any difference; two independent mathematicians read the formal statement against the problem as posed and sign, or refuse | anyone who can read Lean; the two statements are public; a mathematician in the problem's area, about an hour with a reading guide | a trace cycle and two signed read cycles, or a refusal naming the difference | none registered |
| 3 | No independent mathematician has reported reading the proof, and there is no referee report | proposed | a read cycle by a mathematician in the area who is not an author, signing or refusing each main step; a referee report or journal acceptance, recorded by date | a mathematician in the problem's area; a journal; the record notes the date when it happens | a signed or refused read cycle; a dated referee report | none registered |
| 4 | The Generalized Riemann Hypothesis statements are the claimant's own definitions, with no third-party formal statement to compare against | proposed | two independent mathematicians read the four definitions in Statements.lean against the Generalized Riemann Hypothesis as usually stated and sign, or refuse | an analytic number theorist, about an hour with the file | two signed read cycles, or a refusal naming the difference | none registered |
| 5 | Compiled-output hashes agree byte for byte only between builds under the same absolute source path | proposed | a decision by the record keeper on what two independent builders compare: the files that embed no path, the lean4export output (whose determinism is an open question on Sutherland's page and in Deicyde's notes), or a shared build path; then that comparison, run; a rebuild under /home/ubuntu/grh/src/lean, Sutherland's published path, or a comparison of the exported proof, whichever the decision names; either is a new pre-registered cycle | Heidi Bennett, who set the rule, with the kernel; Nervous Machine, once the rule is revised, about 15 hours of machine time | a revised rule in this record, or a comparison on a path-independent artifact, or a rebuild under Sutherland's path that matches his manifest | none registered |

_Generated by DEBRIEF tools/render.py from ledger.json; protocol 0.1.0._
