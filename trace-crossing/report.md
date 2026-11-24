# Crossing trace: what the wings reach, and how rare the joins are

Footprint of a constant = the set of Mathlib second-level directories its cone reaches (through the library boundary, for the archive). For a joint, the wings are its largest dominated children (up to six); a directory is exclusive to a wing when no other wing reaches it; the joint's crossings are the pairs of exclusive directories from different wings, each scored by how often Mathlib theorems depend on that pair together, as a ratio to what independence would give (crossings.tsv of the prior trace: 1 = as often as chance, below 1 = rarer, 0 = never seen together).

## X1. The archive

The cone of `riemannHypothesis` reaches 25 of 26 Mathlib directories: Mathlib/Algebra, Mathlib/AlgebraicGeometry, Mathlib/AlgebraicTopology, Mathlib/Analysis, Mathlib/CategoryTheory, Mathlib/Combinatorics, Mathlib/Control, Mathlib/Data, Mathlib/Dynamics, Mathlib/FieldTheory, Mathlib/Geometry, Mathlib/GroupTheory, Mathlib/Lean, Mathlib/LinearAlgebra, Mathlib/Logic, Mathlib/MeasureTheory, Mathlib/ModelTheory, Mathlib/NumberTheory, Mathlib/Order, Mathlib/Probability, Mathlib/RepresentationTheory, Mathlib/RingTheory, Mathlib/SetTheory, Mathlib/Tactic, Mathlib/Topology.

Not reached: Mathlib/Computability.

### The 20 largest joints: wings, footprints, rarest crossing

| joint | joins | wings (of) | footprint | Jaccard distance of the two largest wings | exclusive dirs | rarest pair the wings bring together | ratio to chance | Mathlib theorems with that pair |
|---|---|---|---|---|---|---|---|---|
| `every_character_of_literature_of_vWin` | 27.2% | 6 (50468) | 25 | 0.08 | 1 | (wings reach the same directories) |  |  |
| `everyCharacter` | 22.6% | 6 (58064) | 25 | 0.04 | 1 | (wings reach the same directories) |  |  |
| `nonempty_hyps_definite_side_of_closed_bound` | 22.0% | 6 (48115) | 25 | 0.04 | 0 | (wings reach the same directories) |  |  |
| `everyCharacter_of_row` | 10.6% | 6 (7843) | 25 | 0.08 | 2 | (wings reach the same directories) |  |  |
| `hypotheses_nonempty_of_unramified_exponents_alt` | 7.1% | 6 (5590) | 25 | 0.04 | 1 | (wings reach the same directories) |  |  |
| `vwin_of_hypotheses_H_E_alt` | 6.3% | 6 (5839) | 23 | 0.00 | 0 | (wings reach the same directories) |  |  |
| `every_character_of_theta_integrals_local_matching` | 6.3% | 6 (19001) | 25 | 0.12 | 3 | (wings reach the same directories) |  |  |
| `topCovolSlim2_use_alt_alt` | 3.1% | 6 (3428) | 23 | 0.04 | 1 | (wings reach the same directories) |  |  |
| `steps_holds` | 2.5% | 6 (4733) | 22 | 0.14 | 1 | (wings reach the same directories) |  |  |
| `allRows_of_open0_alt` | 2.4% | 6 (1118) | 25 | 0.12 | 1 | (wings reach the same directories) |  |  |
| `geometric_realization_of_weight_one` | 2.2% | 6 (927) | 22 | 0.00 | 0 | (wings reach the same directories) |  |  |
| `ontoX_of_hypotheses_alt_alt` | 1.7% | 6 (2004) | 24 | 0.00 | 1 | (wings reach the same directories) |  |  |
| `topCovolG_alt_alt` | 1.6% | 6 (2255) | 23 | 0.04 | 0 | (wings reach the same directories) |  |  |
| `goodTower_and_volume` | 1.5% | 6 (1717) | 22 | 0.23 | 0 | (wings reach the same directories) |  |  |
| `kodaira_spencer_of_weight_one` | 1.4% | 6 (1396) | 22 | 0.05 | 0 | (wings reach the same directories) |  |  |
| `deepStR_of_use` | 1.2% | 6 (2636) | 22 | 0.00 | 0 | (wings reach the same directories) |  |  |
| `volumeTheoremX_of_inputs` | 1.1% | 6 (596) | 22 | 0.27 | 0 | (wings reach the same directories) |  |  |
| `offDiag` | 1.0% | 6 (924) | 21 | 0.10 | 2 | (wings reach the same directories) |  |  |
| `member_bundles_large_unramified_exponents_alt` | 0.9% | 6 (805) | 24 | 0.21 | 2 | (wings reach the same directories) |  |  |
| `v_window_of_automorphy_csd_ss_mono_odd` | 0.8% | 6 (1186) | 23 | 0.00 | 0 | (wings reach the same directories) |  |  |

### The wings of the three largest joints

`UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin`:

- `every_character_of_theta_integrals_local_matching` 39.6%: reaches 25 directories; only this wing reaches Mathlib/Control
- `topCovolSlim2_use_alt_alt` 7.7%: reaches 23 directories; nothing only this wing reaches
- `theta_integrals_agree_and_local_matching_of_literature` 1.1%: reaches 21 directories; nothing only this wing reaches
- `toroidalForFanKS` 0.8%: reaches 22 directories; nothing only this wing reaches
- `published_results_arithmetic` 0.7%: reaches 23 directories; nothing only this wing reaches
- `canonicalAlgorithmRules_isCorrect` 0.7%: reaches 15 directories; nothing only this wing reaches

`UpperTheory.FinalTheorems.everyCharacter`:

- `everyCharacter_of_row` 77.4%: reaches 25 directories; only this wing reaches Mathlib/Control
- `galoisLocalGlobalStrong_recParameter` 6.4%: reaches 24 directories; nothing only this wing reaches
- `zarhinGeometric_of_semistableReduction` 0.3%: reaches 19 directories; nothing only this wing reaches
- `coreG` 0.2%: reaches 15 directories; nothing only this wing reaches
- `deRham_potentiallySemistable` 0.2%: reaches 19 directories; nothing only this wing reaches
- `gm_of_bcfl` 0.2%: reaches 19 directories; nothing only this wing reaches

`UpperTheory.Lit.nonempty_hyps_definite_side_of_closed_bound`:

- `hypotheses_nonempty_of_unramified_exponents_alt` 11.3%: reaches 25 directories; nothing only this wing reaches
- `ontoX_and_lamLow_of_unitaryGroupHypotheses'` 2.8%: reaches 24 directories; nothing only this wing reaches
- `open0_of_unitary_group_hypotheses` 1.6%: reaches 25 directories; nothing only this wing reaches
- `thetaLift_row_properties_conj` 0.6%: reaches 20 directories; nothing only this wing reaches
- `functionalsSeparate_of_howeUnram_of_siegelWeil` 0.6%: reaches 21 directories; nothing only this wing reaches
- `fourier_coefficient_fit_of_join_alt` 0.6%: reaches 24 directories; nothing only this wing reaches

## X2. The same measures for the largest joint of each of the 100 large Mathlib proofs

Mathlib directories reached by the cone: Q1/median/Q3 13 / 14 / 16 of 26; the archive reaches 25 (measured at its largest joint, which carries the whole cone).

| measure | Mathlib Q1 | median | Q3 | archive, largest joint | archive, median of its top joints |
|---|---|---|---|---|---|
| Jaccard distance of the two largest wings | 0.14 | 0.27 | 0.39 | 0.08 | 0.04 |
| directories exclusive to one wing | 0 | 1 | 3 | 1 | 1 |
| rarest crossing, ratio to chance (joints with any exclusive pair: Mathlib 4 of 100, archive 0 of 20) | 0.00 | 2.52 | 5.04 | none | none |

Rarest crossings realised by Mathlib's largest joints (ten lowest ratios):

| root | joint | pair | ratio | theorems |
|---|---|---|---|---|
| `NumberField.mixedEmbedding.logMap_one` | `logMap_one` | Mathlib/Combinatorics + Mathlib/NumberTheory | 0.00 | 0 |
| `ContDiffBump.measure_closedBall_div_le_integral` | `measure_closedBall_div_le_integral` | Mathlib/Combinatorics + Mathlib/Dynamics | 0.00 | 0 |
| `Real.Wallis.W_le` | `W_le` | Mathlib/Combinatorics + Mathlib/Geometry | 5.04 | 1,523 |
| `integral_cos_mul_complex` | `integral_cos_mul_complex` | Mathlib/Combinatorics + Mathlib/Geometry | 5.04 | 1,523 |

