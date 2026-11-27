# The same plan, rebuilt: the 76,000-line rewriting against the original

**Question.** On 25 November Luke Sernau, with colleagues at Anthropic and Claude, posted a second Lean development of the same five theorems. Its compact edition runs to 76,149 lines of code, against the original's 15.5 million. What did the rewriting keep, and what did it drop? Registration: [prereg_trace_compact.yaml](../prereg_trace_compact.yaml), eight predictions, one amendment. The build it walks is cycle 3 ([prereg_cycle3.yaml](../prereg_cycle3.yaml)). The rewriting was made at Anthropic with Claude, and this record's checks were run by Claude.

**The build.** At commit 72fead10, the compact edition built here in 18 minutes 48 seconds with no errors; the original took 14 hours 48 minutes. Its five theorems rest on Lean's three standard axioms. Its statement file is byte-identical to the original's. Lean's kernel replayed all 794 modules, and con-leche and con-ron accepted the exported proof. nanoda accepted it once its kernel extensions were switched on. lean4lean could not start on this machine. This is finding F2.

## Below `riemannHypothesis`

| measure | original | compact edition | Mathlib Q1 | median | Q3 |
|---|---|---|---|---|---|
| constants in the proof | 1,265,256 | 37,561 | 30,253 | 36,032 | 46,352 |
| lines in the proof | 10,660,526 | 82,826 | 75,408 | 92,248 | 125,716 |
| share carried by one chain, step 3 | 100% | 89.4% | 4.9% | 9.9% | 19.2% |
| step 5 | 66.8% | 19.5% | 3.2% | 6.7% | 13.1% |
| hinges at 1% | 81 | 40 | 30 | 37 | 46 |
| median lines per hinge | 4 | 44 | 8 | 10 | 13 |
| largest joint | 27.2% | 69.8% | 63.9% | 80.2% | 91.5% |
| retry marks per 1,000 names | 15.4 | 1.4 | 0.4 | 0.4 | 0.4 |

| | |
|---|---|
| named constants carrying an original name | 56 of 13,922 (0.4%) |
| original names that survive | 21 of 796,264 |
| direct Mathlib constants used | 29,310, against the original's 64,874 |
| of those, also used by the original | 80.5% |

The chain from the theorem down is short and can be read as mathematics. `riemannHypothesis` comes from `New.grh` (22 lines), which comes from a bound on the prime error term (21 lines), which comes from `star_inequality` (29 lines). That inequality joins 69.8% of the proof. Below it the proof fans out into Galois representations, Selmer groups and lattice forms.

**Predictions.** Six of eight held. Missed: S5, where a large joint appeared against the prediction that none would. Also missed: S8, where the registered names step did not finish because of a loop in the registrar's script, fixed under the amendment.

## What it means

**A different proof, the same plan.** Almost no names survive, and the part of the proof below the theorem is the size of an ordinary Mathlib theorem's. But the route is the same. Three steps down, one chain still carries nine tenths of the proof, which no Mathlib proof in the hundred does.

**How the pieces meet changed.** The original never gathered its argument. The rewriting gathers seven tenths of it into one inequality before the theorem, as human-written proofs do, and its steps are paragraphs rather than lines. The original's lack of joints was a property of its search, not of the argument. The single chain was not.

**What this does not say.** Shape is not reading. No mathematician has reported reading either edition (EG3), and a build settles nothing about what the statements mean (EG2, EG4).

## Files

[prereg_cycle3.yaml](../prereg_cycle3.yaml) · [cycle3/](../cycle3/) · [prereg_trace_compact.yaml](../prereg_trace_compact.yaml) · [trace-compact/](../trace-compact/) · [results/shape/report.md](../trace-compact/results/shape/report.md) · [results/names/names.json](../trace-compact/results/names/names.json)
