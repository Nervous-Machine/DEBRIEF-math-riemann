# Suffix trace: retry fossils in the names below `riemannHypothesis`

## S0. The environment, and how much of the archive's constants the proof uses

| set | constants | of which machine-named (aux) |
|---|---|---|
| environment | 2,701,132 | 1,060,608 |
| archive (all modules) | 1,905,922 | 747,620 |
| library (Mathlib, Lean, Init, …) | 795,211 | 312,988 |
| cone of the root | 1,265,256 | 467,304 |
| cone, as share of archive | 66.39% | named only: 68.89% |

### Archive constants per top-level directory: written vs used

| directory | constants | in the cone | share | named constants | named in cone | share |
|---|---|---|---|---|---|---|
| Development | 1,225,760 | 842,806 | 68.76% | 733,196 | 525,482 | 71.67% |
| Formalism | 451,321 | 277,887 | 61.57% | 285,359 | 178,342 | 62.50% |
| GroundTheory | 136,714 | 76,729 | 56.12% | 82,057 | 49,263 | 60.04% |
| ReciprocityTheory | 64,070 | 47,522 | 74.17% | 39,465 | 30,701 | 77.79% |
| CompanionTheory | 19,641 | 15,718 | 80.03% | 12,741 | 10,954 | 85.97% |
| PositivityTheory | 8,006 | 4,278 | 53.43% | 5,304 | 3,049 | 57.48% |
| Lemmata | 396 | 313 | 79.04% | 167 | 158 | 94.61% |
| Main | 5 | 1 | 20.00% | 5 | 1 | 20.00% |
| Statements | 5 | 0 | 0.00% | 4 | 0 | 0.00% |
| Supplements | 4 | 2 | 50.00% | 4 | 2 | 50.00% |

Second-level directories with the lowest named-constant usage (at least 1,000 named constants):

| directory | named constants | in cone | share |
|---|---|---|---|
| Formalism/WachLatticeTwists | 2,621 | 595 | 22.70% |
| Formalism/SizeWindowBrackets | 2,855 | 730 | 25.57% |
| GroundTheory/PAdicHodge | 5,818 | 1,725 | 29.65% |
| Formalism/FlagUnipotentLattices | 2,509 | 780 | 31.09% |
| Formalism/PadicSubsetSums | 1,219 | 424 | 34.78% |
| Formalism/LocalRingCardinality | 6,075 | 3,026 | 49.81% |
| Development/DiscreteGroups | 1,428 | 714 | 50.00% |
| GroundTheory/HeightsAndTheta | 42,789 | 23,263 | 54.37% |
| Formalism/SharpRestriction | 69,399 | 39,455 | 56.85% |
| PositivityTheory/AutomorphicForms | 5,299 | 3,044 | 57.44% |
| ReciprocityTheory/L2DbarEstimates | 1,847 | 1,087 | 58.85% |
| GroundTheory/ArithmeticGeometry | 3,905 | 2,312 | 59.21% |
| ReciprocityTheory/AnalyticForms | 2,433 | 1,477 | 60.71% |
| Formalism/LocalToGlobal | 93,838 | 57,572 | 61.35% |
| Formalism/GL3MeanSquares | 3,954 | 2,499 | 63.20% |

## S1. Suffix classes, archive against library (named constants only)

| class | archive, all | per 1,000 | archive, in cone | per 1,000 | library | per 1,000 |
|---|---|---|---|---|---|---|
| alt | 3,009 | 2.6 | 2,712 | 3.4 | 4 | 0.0 |
| prime | 12,324 | 10.6 | 9,809 | 12.3 | 11,160 | 23.1 |
| bis_ter | 91 | 0.1 | 60 | 0.1 | 0 | 0.0 |
| fixword | 1,657 | 1.4 | 1,385 | 1.7 | 145 | 0.3 |
| numbered | 13,151 | 11.4 | 8,467 | 10.6 | 1,387 | 2.9 |
| any retry class (alt, prime, bis_ter, fixword) | 17,081 | 14.7 | 13,966 | 17.5 | 11,309 | 23.5 |

Fix-words in the archive: fix 712, fixed 671, rev 207, old 25, new 24, final 14, again 2, v0 2

## S2. How many times `_alt` is stacked

| depth | archive, all | archive, in cone | examples (in cone) |
|---|---|---|---|
| 1 | 2,789 | 2,498 | `CompanionTheory.D.gk.admitted.Gard.apply_alt`, `CompanionTheory.LimBd.Main.phase_zero_alt`, `CrystallineSemistableComparison.Pb.G3.norm_lt_one_of_residue_zero_alt` |
| 2 | 206 | 200 | `CompanionTheory.D.gk.admitted.Gard.eq_zero_of_alt_alt`, `CompanionTheory.PfEss.Zc2.split_alt_alt`, `CompanionTheory.WaveGrid.WGlue.weighted_uniform_rotated_of_expansion_alt_alt` |
| 3 | 12 | 12 | `GlobalTheory.AdmTame.main_alt_alt_alt`, `GlobalTheory.AlgCharFromGal.main_alt_alt_alt`, `GlobalTheory.ChiOneAbove.main_alt_alt_alt` |
| 4 | 1 | 1 | `GlobalTheory.T.main_theorem_from_published_results_alt_alt_alt_alt` |
| 5 | 1 | 1 | `GlobalTheory.T.main_theorem_from_published_results_alt_alt_alt_alt_alt` |

Deepest stack in the archive: 5; in the cone: 5.

## S3. Families: a base name and its retry variants

A family is the set of archive constants (named, same namespace) that strip to the same base name under the registered suffix rules. Only families with at least two members are counted.

Families with at least two members: 5,046, covering 10,178 constants. Size distribution: 2: 4,966, 3: 74, 4: 6

| members in the cone | families |
|---|---|
| 0 | 822 |
| 1 | 1,908 |
| 2 | 2,293 |
| 3 | 21 |
| 4 | 2 |

Families with no member in the cone: 822 (16.29%). Exactly one member used and it is the latest variant: 1,815. Two or more members used (earlier versions still load-bearing): 2,316 (45.90%). Base name used alongside a variant: 2,289.

Largest families:

| members | in cone | base |
|---|---|---|
| 4 | 4 | `Formalism.ZeroFreeDirichlet.re_one_div_sub_zero_pos` |
| 4 | 4 | `Formalism.F.linearIndependent_coe_basis` |
| 4 | 2 | `GlobalTheory.T.true_geometry_finite_index` |
| 4 | 2 | `GlobalTheory.T.main_theorem_from_published_results` |
| 4 | 2 | `GlobalTheory.T.local_component_measure_identity` |
| 4 | 1 | `GlobalTheory.T.levi_normalizes_unipotent` |
| 3 | 3 | `PositivityTheory.ResPlug.WeightsCompactStabilizer.principalisationCharZero` |
| 3 | 3 | `LateralTheory.E.TorEtPf.TorEt_of` |
| 3 | 3 | `LateralTheory.E.H2CurveOrder.LeafKumMuSurjPf.LeafKumMuSurj_of` |
| 3 | 3 | `GroundTheory.Heights₂.Heights.IndefiniteRowSideFullHecke.Regular.RegCharts.W` |
| 3 | 3 | `GlobalTheory.T.gram_det_change_of_basis` |
| 3 | 3 | `GlobalTheory.SplitLinear.off_norm` |
| 3 | 3 | `GlobalTheory.SnMass.VolN.GNGroup.cT_mul` |
| 3 | 3 | `GlobalTheory.GO.ChSrc.trueWt` |
| 3 | 3 | `GlobalTheory.CapFrame.herm_U` |
| 3 | 3 | `Formalism.MainNotions.flipOneThree.Pf.lpRingIndep_of` |
| 3 | 3 | `Formalism.MainNotions.ModuliIntegralCharts.H1.chartIndep2_of_open` |
| 3 | 3 | `Formalism.MainNotions.Lnk.frameRealF_of` |
| 3 | 3 | `Formalism.MainNotions.ColumnSystems.Pf.restCountLow_of` |
| 3 | 3 | `Formalism.MainNotions.BridgeLemma₂.planeMapAlt` |
| 3 | 3 | `Formalism.L2.SG.Pf.volPosC_of` |
| 3 | 3 | `Formalism.L2.SG.Pf.multPoly_holds_of` |
| 3 | 3 | `Formalism.L2.SG.Pf.inHHC_holds_of` |
| 3 | 3 | `Formalism.L2.SG.Pf.RegroupPf.regroupC_of` |
| 3 | 3 | `Formalism.L2.Col.twIdx_ok` |

## S4. Retry suffixes on the hinges and along the spine

Hinges (at least 1% of the root's lines): 81; with a retry suffix: 33 (40.74%).
| hinge with retry suffix | dominates | classes |
|---|---|---|
| `GlobalTheory.Fc.S0.StageU.hypotheses_nonempty_of_unramified_exponents_alt` | 11.34% | alt |
| `SelfIntersectionVolumeEstimates.topCovolSlim2_use_alt_alt` | 7.67% | alt |
| `UpperTheory.V.HV.DescentVanishingReductions.vwin_of_hypotheses_H_E_alt` | 7.64% | alt |
| `GlobalTheory.Fc.AllAtMemberStage0.allRows_of_open0_alt` | 4.23% | alt |
| `GlobalTheory.CompanionTheory.Ar.Link.good_tower_volume_theorem_bis` | 3.29% | bis_ter |
| `GlobalTheory.Fc.S0.ontoX_and_lamLow_of_unitaryGroupHypotheses'` | 2.83% | prime |
| `GlobalTheory.BigOn.ontoX_of_hypotheses_alt_alt` | 2.78% | alt |
| `GlobalTheory.T.large_unramified_exponent_bundles_exist_alt` | 2.65% | alt |
| `GlobalTheory.Fc.StageOneU.member_bundles_large_unramified_exponents_alt` | 2.65% | alt |
| `UpperTheory.GalC.final_alt_alt` | 2.09% | alt |
| `UpperTheory.GalC.final_of_alt` | 2.00% | alt |
| `SelfIntersectionVolumeEstimates.topCovolG_alt_alt` | 1.84% | alt |
| `GlobalTheory.LocalRows.at_choice_alt` | 1.81% | alt |
| `GlobalTheory.T.member_exists_baseLattice_alt` | 1.78% | alt |
| `GlobalTheory.Mem.Top.Bl.exists_baseLattice_of_prime_alt` | 1.78% | alt |
| `GlobalTheory.Fc.S0.Open0ProofU.open_orbit_of_unramified_exponents_alt` | 1.60% | alt |
| `GlobalTheory.NLinkClose.main_alt_alt` | 1.41% | alt |
| `GlobalTheory.T.main_theorem_published_inputs_third_alt_alt` | 1.40% | alt |
| `GlobalTheory.miStarRow_alt_alt` | 1.40% | alt |
| `GlobalTheory.T.main_theorem_published_inputs_variant_alt_alt` | 1.37% | alt |
| `GlobalTheory.miStarRowClosing_alt_alt` | 1.37% | alt |
| `GlobalTheory.T.main_theorem_published_results_final_alt_alt` | 1.33% | alt |
| `GlobalTheory.Fam.miStar_row_alt_alt` | 1.33% | alt |
| `GlobalTheory.T.main_theorem_from_published_results_alt_alt_alt_alt_alt` | 1.30% | alt |
| `GlobalTheory.Fam.miAt_of_truePack_alt_alt` | 1.30% | alt |
| `GlobalTheory.T.main_theorem_from_published_results_alt_alt_alt_alt` | 1.30% | alt |
| `GlobalTheory.Fam.miStar2_of_allTrue_alt_alt` | 1.30% | alt |
| `GlobalTheory.T.true_geometry_family_row_data_alt` | 1.24% | alt |
| `GlobalTheory.MiTop.famAllQ_of_allTrue_alt` | 1.24% | alt |
| `GlobalTheory.row_hServ_of_link_alt` | 1.23% | alt |
| `GlobalTheory.Svd.servH_row_linkR_alt` | 1.23% | alt |
| `UpperTheory.V.HV.DescentVanishingReductions.sp4In0_alt` | 1.05% | alt |
| `GlobalTheory.Mem.Top.Bl.exists_baseLattice_of_pair_alt` | 1.03% | alt |

Spine constants: 27; with a retry suffix: 4: `GlobalTheory.Fc.S0.StageU.hypotheses_nonempty_of_unramified_exponents_alt`, `GlobalTheory.Fc.AllAtMemberStage0.allRows_of_open0_alt`, `GlobalTheory.LocalRows.at_choice_alt`, `Formalism.L2.SG.LsDatumA.RGHyp.trF'`

Lines dominated by the top-most retry-suffixed constants (no suffixed dominator above them): 6,120,389 of 10,660,526 (57.41%).

Per top-level directory, retry-suffixed share of the named constants in the cone:

| directory | named in cone | with retry suffix | share |
|---|---|---|---|
| Development | 525,482 | 9,842 | 1.87% |
| Formalism | 178,342 | 3,041 | 1.71% |
| GroundTheory | 49,263 | 354 | 0.72% |
| ReciprocityTheory | 30,701 | 549 | 1.79% |
| CompanionTheory | 10,954 | 138 | 1.26% |
| PositivityTheory | 3,049 | 42 | 1.38% |
| Lemmata | 158 | 0 | 0.00% |
| Supplements | 2 | 0 | 0.00% |
| Main | 1 | 0 | 0.00% |

