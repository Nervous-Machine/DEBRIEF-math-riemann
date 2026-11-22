# DEBRIEF-math-riemann

A DEBRIEF mission record (protocol https://github.com/Nervous-Machine/DEBRIEF) for **The claimed proof of the Riemann Hypothesis announced by Levent Alpöge on 20 November 2026, built with Claude and released as Lean 4 code**.

**Standing, 22 November 2026 (UTC).** Certified 0. Accepted 1. Refuted 0. Open gaps 4. The claim and its artifacts are pinned. Nervous Machine's pre-registered build (cycles 1 and 2, `prereg_cycle1.yaml` and `prereg_cycle2.yaml`) compiled all 175,187 modules from the pinned archive against the pinned Mathlib with no error, found no sorry, admit or axiom in the source, confirmed that each of the five entry theorems rests on exactly Lean's three standard axioms, and confirmed that the main statement is Mathlib's own definition RiemannHypothesis, declared once and nowhere redefined. That is finding F1, standing **accepted**. Andrew Sutherland (MIT) has published an independent compile, axiom audit and kernel replays, and on 21 November the Lean and Mathlib communities issued a joint statement, which the page says is endorsed by the Lean FRO and the Mathlib Initiative, saying they certify both the statement and the proof of the Riemann Hypothesis; it names no individual and does not mention the four Dirichlet L-function statements. Both are recorded as what the public record shows, not as standings under this record's rule. Our compiled output is byte-identical to Sutherland's on 76,968 files, including the entry file, and differs on 98,219, every one of which carries the absolute source path that Lean writes into the output of any module that produced a warning (gap EG5); his own count of his build is the same split, and his build path is now public. Nothing is **certified**: the rule needs two independent matching hash reports, which that path dependence prevents until the rule is revised. A reading guide for the five statements exists. No mathematician has yet signed or refused it.

This claim is on the public claims board, https://math-board.nervousmachine.com, which shows its stage, who has contributed, and what it needs next.

## Conflict, stated once

The agent that pinned this record and runs its checks is Claude Fable 5.1, an Anthropic model. The claimant works at Anthropic and names Claude as his co-worker on the argument and its formalization. Heidi Bennett, who keeps this record, is independent of the claimant; the agent is not.

The trust anchor in a Lean check is the kernel, not whoever drives the build, and a driver can at most misreport. So the rule here is about reports, not operators: a build result is **certified** when two parties independent of the claimant and of each other publish matching hashes of the compiled output (`Main.olean` and the manifest of every compiled file), each saying what agent operated the build. One party alone, whatever operated it, gives **accepted**. Rule set 20 November 2026, amendment A1 of `prereg_cycle1.yaml`.

Cycle 1 found that the rule, as written, cannot be met by two parties who did not build under the same absolute path: about half of the compiled files embed the path of their source (EG5). The rule stands until the record keeper revises it; the candidates are in `prereg_cycle2.yaml` under `standing_consequences`. Since 21 November one more is concrete: Sutherland has published his build path, /home/ubuntu/grh/src/lean, so a rebuild under it could be compared file for file.

## The problem

Every zero of the Riemann zeta function that is not a negative even integer lies on the line where the real part equals one half. The Generalized Riemann Hypothesis says the same of the zeros of every Dirichlet L-function in the critical strip. Mathlib, the Lean mathematical library, states the Riemann Hypothesis as a definition named RiemannHypothesis: for every complex s with zeta of s equal to zero, s not of the form minus two times a positive integer, and s not equal to one, the real part of s is one half.

Source: https://www.claymath.org/millennium/riemann-hypothesis/ (posed: Bernhard Riemann (1859); one of the seven Clay Millennium Prize Problems (2000)).

A third-party formalization of the problem statement exists: `Mathlib/NumberTheory/LSeries/RiemannZeta.lean` in github.com/leanprover-community/mathlib4 at commit `0df444a360eaa60ab8c11dca51a86af692955474` (blob `3c92195fce20df7fda41cfd823b3266f83cf3070`). It is the natural reference for whether a claimant's Lean theorem states this problem.

## The claim

**Levent Alpöge**, using Claude (Anthropic), as stated by the claimant; the note names Claude as a co-worker on the argument and the formalization, submitted 2026-11-20 at https://alpo.ge/remark.pdf.

The note says the author believes he has found, with Claude, a proof of the Riemann Hypothesis, that the method extends to the Generalized Riemann Hypothesis, and that both have been formalized in Lean without assumptions. It describes the argument as a descendant of Stepanov's method over function fields, with chains of theta lifts between definite unitary groups standing in for multiplicity, and gives a twenty-step timeline from 6 October to 16 November 2026 that the author says Claude compiled. The note says the argument is very long, that the author has not mastered all of the mathematics it uses, that parts of his description paraphrase an AI-written summary and may be wrong, and that he chose to release only the Lean code rather than an informal write-up. The archive has no README, licence or build instructions. Its lakefile names eleven build targets and raises the default heartbeat and stack limits. The entry file Main.lean states five results: Mathlib's RiemannHypothesis, and four statements the claimant defines in Statements.lean about zeros and non-vanishing of Dirichlet L-functions.

Artifacts, pinned:

- a web page: https://alpo.ge/remark.pdf (sha256 3fc97784b71ddd44ff8aa0a177e99622a1c61b13cfa843a0989ee4a7a0cfeb8d, 245114 bytes, fetched 2026-11-20)
- a Lean development: https://alpo.ge/lean.tar.gz.part01 … part14 (14 parts, reassembled by concatenation; per-part hashes in source/parts.sha256) (sha256 9631b4f020199e580ba86178cb56c6e9b09f690c2369a80dc4334aa93f49c7fc, 239275554 bytes, fetched 2026-11-20)

Status on the problem page as of 2026-11-20: announced on the claimant's personal website; no paper, preprint, journal submission or independent report is on the public record.

## What is owed

Each open gap is in `ASKS.md` with what closes it and who could act. In order:

1. **Do the formal statements say what the problem asks?** (EG2): The machine half is settled (the main statement is Mathlib's definition). The human half is a reading of that definition against the problem as posed, by someone who did not write it.
2. **No independent mathematician has reported reading the proof, and there is no referee report** (EG3): Someone in the field reads it and says, under their name, what holds and what does not.
3. **The Generalized Riemann Hypothesis statements are the claimant's own definitions, with no third-party formal statement to compare against** (EG4): A reading of the four Dirichlet L-function definitions against the Generalized Riemann Hypothesis, by someone who did not write them.
4. **Compiled-output hashes agree byte for byte only between builds under the same absolute source path** (EG5): A decision on what two independent builders compare. Andrew Sutherland's build path, asked for here, is now on his page.

Closed: **EG1**, the build, kernel check and axiom audit on an independent machine (cycle 2, finding F1).

## Contributing

- **Rerun** (if there is a Lean development): copy `prereg_cycle1.yaml` as a model, fill in your own predictions, register it with `tools/prereg.py register` from the protocol repository and commit it *before* running anything. Run. Report with the **Rerun report** issue form; it becomes a `rerun` cycle under your name.
- **Read**: the reading guide is `trace/DEFINITIONAL-TRACE.md`, about half an hour. Sign or refuse its checklist with the **Semantic read** issue form; either becomes a `read` cycle under your name. Two independent signatures close the semantic gap; one refusal reopens it.
- **Anything else**: open a plain issue.

Rules and templates: https://github.com/Nervous-Machine/DEBRIEF/blob/main/CONTRIBUTING.md. Every contribution is one dated cycle under your own name and goes into `CITATION.cff` and the next release.

## Layout

```
ledger/riemann.json   the ledger (protocol 0.1.0)
claim.yaml            the pinned claim this record was opened from
SCORECARD.md / ASKS.md  generated from the ledger
trace/                the reading guide for the five statements (a `trace` cycle)
prereg_cycle1.yaml    Nervous Machine's pre-registration for the first build, hashed before it ran (.sha256 sidecar)
prereg_cycle2.yaml    the same for the resumed build, which finished
cycle1/, cycle2/      logs, hashes and summaries of those builds
source/               hashes of the 14 archive parts, the reassembled archive and its tar listing; fetch times
cycles/               contributed cycles, one file each
```

## Words

This record never calls the claim proved, verified or a theorem. It records what was claimed, what was checked by whom under what rule, and what is still open. Nothing here has standing until a cycle gives it one.
