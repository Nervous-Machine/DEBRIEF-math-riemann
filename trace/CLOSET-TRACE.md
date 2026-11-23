# Closet trace: is there a small lemma in a small place that the proof hangs on?

Cycle `trace-2026-11-23-closet`, run 2026-11-23 21:38–21:42 UTC on the dependency tables written by the
[structure trace](STRUCTURE-TRACE.md) the same day. Pre-registered in `prereg_trace_closet.yaml`
(commit 8d1586d, 21:38 UTC, before the analysis ran). Outputs in `trace-closet/`: `report.md` (every table in full),
`hinges.tsv` (832 constants down to 0.1%), `joints.tsv`, `directories2.tsv`, `spine_full.txt`, `closets.txt` (empty),
`K6_statements.txt`, logs, `closet.sha256`.

**Question.** The structure trace found one hinge at the top (`everyCharacter`, the Dirichlet nonvanishing theorem)
and below it a tree whose heavy branches carry the names of large, long-studied theories. If so, an unexpected step,
had there been one, would have to be a closet: a constant with little text of its own, in a directory that is small by
lines, which the rest of the proof nevertheless depends on. This cycle looks for one in the dominator tree, down to
its last constant, and reports the size of the text at every hinge.

**Answer in one line.** No closet by location. Every one of the 81 constants that dominates at least 1% of the proof
lives in one of the ten large subject directories, and every one of them is short: median 4 lines of its own, the
longest 88. The hinges are glue; the mass is below them. The spine leaves the automorphic directory at 1.72% into
abelian-variety theory and ends in lattice point counts in `Formalism/LocalToGlobal`.

---

## K1. Hinges: constants dominating at least 1% of the root's lines

81 constants, all theorems. By second-level directory: Development/AutomorphicArithmetic 65, AutomorphicSpectrum 6,
AbelianVarietyTheory 4, WeilBound 3, Supplements/Kernels 2 (the renamings `rhOfAll`, `allChi`), Main 1 (the root).

Own lines of the 81: median 4, 72 at or under 20, one over 50 (`GlobalTheory.T.main_alt_alt`, 88 lines, 1.41%).
The nine over 20 lines: `nonempty_hyps_definite_side_of_closed_bound` 25 (33.3%), `hypotheses_nonempty_of_unramified_exponents_alt` 21 (11.3%),
`allRows_of_open0_alt` 37 (4.2%), `member_bundles_large_unramified_exponents_alt` 30 (2.6%), `open_orbit_of_unramified_exponents_alt` 31 (1.6%),
`main_alt_alt` 88 (1.4%), `shape_closed_link_n_of_green` 23 (1.4%), `volumeTheoremX_of_inputs` 50 (1.3%), `exists_baseLattice_of_pair_alt` 21 (1.0%).

The thirty largest (full 81 in `trace-closet/report.md`, down to 0.1% in `hinges.tsv`):

| # | constant | directory (under Development/ unless stated) | own lines | dominates | direct children | depth |
|---|---|---|---|---|---|---|
| 1 | `riemannHypothesis` | Main | 1 | 100.00% | 1 | 0 |
| 2 | `rhOfAll` | Supplements/Kernels | 1 | 100.00% | 3 | 1 |
| 3 | `allChi` | Supplements/Kernels | 1 | 100.00% | 1 | 2 |
| 4 | `UpperTheory.FinalTheorems.everyCharacter` | AutomorphicArithmetic/CharacterBoxes | 2 | 100.00% | 58,064 | 3 |
| 5 | `UpperTheory.FinalTheorems.everyCharacter_of_row` | AutomorphicArithmetic/CharacterBoxes | 2 | 77.43% | 7,843 | 4 |
| 6 | `UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin` | AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries | 4 | 66.82% | 50,468 | 5 |
| 7 | `UpperTheory.Lit.every_character_of_theta_integrals_local_matching` | same | 5 | 39.58% | 19,001 | 6 |
| 8 | `UpperTheory.Lit.nonempty_hyps_definite_side_of_closed_bound` | same | 25 | 33.30% | 48,115 | 7 |
| 9 | `GlobalTheory.Fc.S0.StageU.hypotheses_nonempty_of_unramified_exponents_alt` | same | 21 | 11.34% | 5,590 | 8 |
| 10 | `UpperTheory.One.vwin_of_row` | AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/ThresholdArguments/DenseThresholdCases | 2 | 8.57% | 4 | 5 |
| 11 | `UpperTheory.One.Join.automorphic_window_of_inputs` | same | 4 | 8.57% | 32 | 6 |
| 12 | `UpperTheory.One.Join.v_window_of_depth_zero_residual_bc_cm` | same | 4 | 8.47% | 10 | 7 |
| 13 | `UpperTheory.V.v_window_of_literal_automorphy_n` | same | 2 | 8.47% | 1 | 8 |
| 14 | `UpperTheory.V.HV.DescentVanishingReductions.v_window_of_automorphy_csd_ss_mono_odd` | same | 2 | 8.47% | 1,186 | 9 |
| 15 | `SelfIntersectionVolumeEstimates.topCovolSlim2_use_alt_alt` | AutomorphicArithmetic/…/ThirdPlaceSeries | 7 | 7.67% | 3,428 | 6 |
| 16 | `UpperTheory.V.HV.DescentVanishingReductions.vwin_of_hypotheses_H_E_alt` | AutomorphicArithmetic/…/DenseThresholdCases | 5 | 7.64% | 5,839 | 10 |
| 17 | `UpperTheory.Gal.Int.galoisLocalGlobalStrong_recParameter` | AutomorphicArithmetic/Foundations/GaloisRepresentations/IntegralStructures | 1 | 6.44% | 26 | 4 |
| 18 | `UpperTheory.Gal.Int.galoisRepresentations_of_thetaLift` | same | 1 | 6.05% | 97 | 5 |
| 19 | `UpperTheory.Gal.Int.Geo.geoOne_holds` | same, GeometricFlagBases | 1 | 5.31% | 145 | 6 |
| 20 | `UpperTheory.Gal.Int.Geo.geometric_realization_of_weight_one` | same | 1 | 5.03% | 927 | 7 |
| 21 | `PositivityTheory.HtPt.Ah.deep_slim_use` | WeilBound/CoreStatements/AutomorphicKernels/MoriwakiBigness/HilbertSamuelApplications | 6 | 4.55% | 32 | 7 |
| 22 | `GlobalTheory.CompanionTheory.Ar.Plug.deepStR_of_use` | same | 12 | 4.50% | 2,636 | 8 |
| 23 | `GlobalTheory.Fc.AllAtMemberStage0.allRows_of_open0_alt` | AutomorphicArithmetic/…/ThirdPlaceSeries | 37 | 4.23% | 1,118 | 9 |
| 24 | `GlobalTheory.CompanionTheory.Ar.Link.good_tower_volume_theorem_bis` | WeilBound/…/HilbertSamuelApplications | 11 | 3.29% | 3 | 9 |
| 25 | `GlobalTheory.T.final_theorem_of_inputs_right` | AutomorphicSpectrum/Proofs/GeometryProofs | 2 | 3.29% | 1 | 10 |
| 26 | `GlobalTheory.CompanionTheory.Ar.Top.goodTower_volume_of_reduced` | same | 12 | 3.29% | 638 | 11 |
| 27 | `UpperTheory.Gal.Int.Geo.steps_holds` | AutomorphicArithmetic/…/GeometricFlagBases | 1 | 2.86% | 4,733 | 8 |
| 28 | `GlobalTheory.Fc.S0.ontoX_and_lamLow_of_unitaryGroupHypotheses'` | AutomorphicArithmetic/…/ThirdPlaceSeries | 14 | 2.83% | 40 | 8 |
| 29 | `GlobalTheory.BigOn.ontoX_of_hypotheses_alt_alt` | same | 18 | 2.78% | 2,004 | 9 |
| 30 | `GlobalTheory.T.good_tower_volume_theorem` | AutomorphicSpectrum/Proofs/DivisibilityProofs | 2 | 2.77% | 1 | 12 |

## K2. Directories: size against the largest share any constant in them dominates

A big theory is a second-level directory with at least 2% of the archive's 17,374,215 lines (347,484). Ten qualify.
A closet by location would be a hinge (1% or more) in a directory below that size. **There are none.** The largest
dominator in any small directory is `canonicalAlgorithmRules_isCorrect` in Development/ResolutionOfSingularities
(140,709 lines, 0.81% of the archive), dominating 0.66%.

| directory | lines | share of archive | own lines the proof uses | largest dominator in it | dominates |
|---|---|---|---|---|---|
| Development/AbelianVarietyTheory | 8,142,960 | 46.9% | 4,675,299 | `GlobalTheory.CarrierGap.offDiag` | 1.72% |
| Development/AutomorphicArithmetic | 1,776,375 | 10.2% | 1,306,270 | `UpperTheory.FinalTheorems.everyCharacter` | 100.00% |
| Development/AutomorphicSpectrum | 1,195,844 | 6.9% | 780,385 | `GlobalTheory.T.final_theorem_of_inputs_right` | 3.29% |
| Formalism/LocalToGlobal | 955,843 | 5.5% | 562,843 | `Formalism.L2.G.linkG_concrete5` | 0.72% |
| Development/WeilBound | 848,547 | 4.9% | 622,061 | `PositivityTheory.HtPt.Ah.deep_slim_use` | 4.55% |
| Formalism/SharpRestriction | 709,436 | 4.1% | 429,851 | `Formalism.MainNotions.G.GramWindowAlt.theorem_A_closed_form_holds` | 0.36% |
| GroundTheory/HeightsAndTheta | 641,322 | 3.7% | 327,338 | `GroundTheory.Heights₂.Heights.HilbertSamuel.TheoremHSMBlock.of_open` | 0.16% |
| Formalism/HermitianCurvature | 460,802 | 2.65% | | `…SmoothTransferRegularity.model_place_built_holds` | 0.20% |
| Formalism/PeriodIntegrals | 451,856 | 2.60% | | `Formalism.L2.SG.Pf.NcVal.OmVSt.OmVZ.omV_holdsX` | 0.13% |
| ReciprocityTheory/ReductiveGroups | 409,976 | 2.36% | | `ReciprocityTheory.ChartRestriction.DS.Lap.TopClosed.besselNVG` | 0.20% |

All 331 directories are in `trace-closet/directories2.tsv`.

**One thing the table shows that was not asked.** Development/AbelianVarietyTheory is 47% of the archive and the
proof uses 4.7 million of its lines, yet no constant in it dominates more than 1.72%. Dominated lines are credited
only to a constant that every path from the root passes through; a lemma reached from many places is credited to the
common ancestor above it. So the abelian-variety theory is reached from many directions and nothing in it is a step
that the rest of the proof passes through. It is substrate, in the sense of the dominator tree. That is a structural
fact about where the text sits, not a statement about what the hypotheses in it say (the Nielsen dispute, EG2).

## K3. Joints: where dominated mass meets

Joined lines = own lines + dominated lines of every dominated child except the largest: the mass that meets at this
constant and nowhere below it. A pure wrapper joins almost nothing. 120 constants dominate at least 0.5%; the top ten
by joined lines:

| # | constant | directory | own lines | joins | dominates | direct children |
|---|---|---|---|---|---|---|
| 1 | `UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin` | AutomorphicArithmetic/…/ThirdPlaceSeries | 4 | 27.23% | 66.82% | 50,468 |
| 2 | `UpperTheory.FinalTheorems.everyCharacter` | AutomorphicArithmetic/CharacterBoxes | 2 | 22.57% | 100.00% | 58,064 |
| 3 | `UpperTheory.Lit.nonempty_hyps_definite_side_of_closed_bound` | AutomorphicArithmetic/…/ThirdPlaceSeries | 25 | 21.96% | 33.30% | 48,115 |
| 4 | `UpperTheory.FinalTheorems.everyCharacter_of_row` | AutomorphicArithmetic/CharacterBoxes | 2 | 10.61% | 77.43% | 7,843 |
| 5 | `GlobalTheory.Fc.S0.StageU.hypotheses_nonempty_of_unramified_exponents_alt` | AutomorphicArithmetic/…/ThirdPlaceSeries | 21 | 7.10% | 11.34% | 5,590 |
| 6 | `UpperTheory.V.HV.DescentVanishingReductions.vwin_of_hypotheses_H_E_alt` | AutomorphicArithmetic/…/DenseThresholdCases | 5 | 6.30% | 7.64% | 5,839 |
| 7 | `UpperTheory.Lit.every_character_of_theta_integrals_local_matching` | AutomorphicArithmetic/…/ThirdPlaceSeries | 5 | 6.28% | 39.58% | 19,001 |
| 8 | `SelfIntersectionVolumeEstimates.topCovolSlim2_use_alt_alt` | same | 7 | 3.12% | 7.67% | 3,428 |
| 9 | `UpperTheory.Gal.Int.Geo.steps_holds` | AutomorphicArithmetic/…/GeometricFlagBases | 1 | 2.55% | 2.86% | 4,733 |
| 10 | `GlobalTheory.Fc.AllAtMemberStage0.allRows_of_open0_alt` | AutomorphicArithmetic/…/ThirdPlaceSeries | 37 | 2.43% | 4.23% | 1,118 |

Every one of the top ten joints has at most 37 lines of its own; the ten largest short joints (at most 50 own lines)
are the same ten constants. Of the 120 constants above 0.5%, three have more than 50 own lines (the longest 186).
Three constants join more than a fifth of the proof each: a four-line theorem with 50,468 direct dependants, a
two-line theorem with 58,064, and a 25-line theorem with 48,115. The four-line one is the recipe printed in the
structure trace (literature statements + VWin → every character). These are the places where wings meet.

## K4. The spine to its end

| step | constant | directory | own lines | dominates | direct children |
|---|---|---|---|---|---|
| 0 | `riemannHypothesis` | Main | 1 | 100.00% | 1 |
| 1 | `rhOfAll` | Supplements/Kernels | 1 | 100.00% | 3 |
| 2 | `allChi` | Supplements/Kernels | 1 | 100.00% | 1 |
| 3 | `UpperTheory.FinalTheorems.everyCharacter` | Development/AutomorphicArithmetic/CharacterBoxes | 2 | 100.00% | 58,064 |
| 4 | `UpperTheory.FinalTheorems.everyCharacter_of_row` | same | 2 | 77.43% | 7,843 |
| 5 | `UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin` | …/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries | 4 | 66.82% | 50,468 |
| 6 | `UpperTheory.Lit.every_character_of_theta_integrals_local_matching` | same | 5 | 39.58% | 19,001 |
| 7 | `UpperTheory.Lit.nonempty_hyps_definite_side_of_closed_bound` | same | 25 | 33.30% | 48,115 |
| 8 | `GlobalTheory.Fc.S0.StageU.hypotheses_nonempty_of_unramified_exponents_alt` | same | 21 | 11.34% | 5,590 |
| 9 | `GlobalTheory.Fc.AllAtMemberStage0.allRows_of_open0_alt` | same | 37 | 4.23% | 1,118 |
| 10 | `GlobalTheory.LocalRows.lg1_sLp_sO_hTF` | same | 2 | 1.81% | 1 |
| 11 | `GlobalTheory.LocalRows.sLp_sO_hTF_of_siegelWeil` | same | 3 | 1.81% | 1 |
| 12 | `GlobalTheory.LocalRows.at_choice_alt` | same | 8 | 1.81% | 32 |
| 13 | `GlobalTheory.CarrierGap.offDiag` | Development/AbelianVarietyTheory/Proofs/FlagMeasures | 11 | 1.72% | 924 |
| 14 | `GlobalTheory.CarrierGap.theoremS_leaves_of_carrierG` | same | 24 | 0.72% | 749 |
| 15 | `Formalism.L2.SG.Pf.Coef.rowsDatumP_of_deep` | Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/RankPointCounts | 7 | 0.31% | 48 |
| 16 | `Formalism.L2.SG.Pf.Coef.cutAt_of_deep` | same | 25 | 0.31% | 194 |
| 17 | `Formalism.L2.SG.Pf.PCount.partnerCount_holds_all` | same | 2 | 0.16% | 14 |
| 18 | `Formalism.L2.SG.LsDatumA.integralClosureRank_and_residueTrdegLe` | same | 1 | 0.15% | 268 |
| 19 | `Formalism.L2.SG.LsDatumA.globalCount_of_split_mode` | same | 3 | 0.08% | 125 |
| 20 | `Formalism.L2.SG.LsDatumA.globalCount_of_module` | same | 5 | 0.04% | 1 |
| 21 | `Formalism.L2.SG.LsDatumA.localCount_of_module` | same | 4 | 0.04% | 62 |
| 22 | `Formalism.L2.SG.LsDatumA.claimR_at` | same | 2 | 0.01% | 14 |
| 23 | `Formalism.L2.SG.LsDatumA.claimRG_at` | same | 29 | 0.01% | 35 |
| 24 | `Formalism.L2.SG.LsDatumA.rg_fwd_sub` | same | 86 | 0.00% | 8 |
| 25 | `Formalism.L2.SG.LsDatumA.RGHyp.trF` | same | 38 | 0.00% | 2 |
| 26 | `Formalism.L2.SG.LsDatumA.RGHyp.trF._abel_1_1` | same | 0 | 0.00% | 0 |

27 steps. The spine stays in Development/AutomorphicArithmetic from step 3 to step 12, crosses into
AbelianVarietyTheory at step 13 (1.72%) and into Formalism/LocalToGlobal at step 15 (0.31%), where it runs down
through lattice point counts (Siegel lattices, cokernel counts, rank point counts) to a 38-line lemma about a
Hermitian-space hypothesis and the `abel` tactic's side goal under it.

## K5. Leverage

Among constants above 0.5% with at least two dominated children, the twenty with the fewest own lines per dominated
line have 1 to 25 own lines each and are the spine constants, the Galois-representation chain
(`galoisLocalGlobalStrong_recParameter`, `galoisRepresentations_of_thetaLift`, `geoOne_holds`,
`geometric_realization_of_weight_one`, `steps_holds`, `kodaira_spencer_of_weight_one`), the threshold chain
(`vwin_of_row` and its four successors), `topCovolSlim2_use_alt_alt`, `deep_slim_use`, and
`GlobalTheory.T.main_theorem_from_published_results_alt_alt_alt_alt_alt` (2 lines, 1.30%). Full table in `trace-closet/report.md`.

## K6. Statements, verbatim

The closets (none), the ten largest joints, the short joints and the five highest-leverage constants were all among
the twenty statements printed in the structure trace, except `steps_holds`. Printed here, with `pp.proofs false` in
the built environment (53 s, 54.9 GB): `steps_holds` and the last five spine constants.

```lean
UpperTheory.Gal.Int.Geo.steps_holds : UpperTheory.Gal.Int.Geo.Steps
@Formalism.L2.SG.LsDatumA.claimR_at : ∀ {F : Type} [inst : Field F] [inst_1 : ValuativeRel F]
  [inst_2 : TopologicalSpace F] {E : Type} [inst_3 : CommRing E] [inst_4 : Algebra F E] [inst_5 : TopologicalSpace E]
  [inst_6 : MeasurableSpace E] (M : Formalism.MainNotions.S.Loc.Model F E) (r n : ℕ),
  M.OK → Formalism.L2.SG.LsDatumA.ClaimR M r n
@Formalism.L2.SG.LsDatumA.claimRG_at : ∀ {F : Type} [inst : Field F] [inst_1 : ValuativeRel F]
  [inst_2 : TopologicalSpace F] {E : Type} [inst_3 : CommRing E] [inst_4 : Algebra F E] [inst_5 : TopologicalSpace E]
  [inst_6 : MeasurableSpace E] (M : Formalism.MainNotions.S.Loc.Model F E) (r n : ℕ),
  M.OK → Formalism.L2.SG.LsDatumA.ClaimRG M r n
@Formalism.L2.SG.LsDatumA.rg_fwd_sub : ∀ {F : Type} [inst : Field F] [inst_1 : ValuativeRel F]
  [inst_2 : TopologicalSpace F] {E : Type} [inst_3 : CommRing E] [inst_4 : Algebra F E] [inst_5 : TopologicalSpace E]
  [inst_6 : MeasurableSpace E] {M : Formalism.MainNotions.S.Loc.Model F E} {V : Type} [inst_7 : AddCommGroup V]
  [inst_8 : Module E V] (H : Formalism.MainNotions.S.Loc.HermSp M V) {r : ℕ}
  (g : Formalism.MainNotions.S.Loc.SplitG M.L) {t₁ t₂ : Formalism.MainNotions.S.Loc.Term V M r}
  {Λ₂ : Submodule (↥M.L.O) V} {ψ : ↥(H.W0 t₁.f t₁.f') ≃ₗ[E] ↥(H.W0 t₂.f t₂.f')}
  {θ : Formalism.L2.SG.LsDatumA.DDt H t₁ ≃ₗ[↥M.L.O] Formalism.L2.SG.LsDatumA.DDt H t₂} {φ : H.Wb t₁.f ≃ₗ[E] H.Wb t₂.f}
  {φ' : H.Wb t₁.f' ≃ₗ[E] H.Wb t₂.f'},
  Formalism.L2.SG.LsDatumA.RGHyp H t₁ t₂ Λ₂ ψ θ φ φ' →
    Prod.map ⇑φ' ⇑φ '' H.iotaGraph g t₁ =
        H.iotaGraph g { abelian₂ := Λ₂, f := t₂.f, f' := t₂.f', T := t₂.T, T' := t₂.T' } →
      (fun p => (θ p.1, θ p.2.1, φ p.2.2.1, φ' p.2.2.2)) '' Formalism.L2.SG.LsDatumA.GamR H t₁ ((algebraMap F E) ↑g.q) ⊆
        Formalism.L2.SG.LsDatumA.GamR H t₂ ((algebraMap F E) ↑g.q)
@Formalism.L2.SG.LsDatumA.RGHyp.trF : ∀ {F : Type} [inst : Field F] [inst_1 : ValuativeRel F]
  [inst_2 : TopologicalSpace F] {E : Type} [inst_3 : CommRing E] [inst_4 : Algebra F E] [inst_5 : TopologicalSpace E]
  [inst_6 : MeasurableSpace E] {M : Formalism.MainNotions.S.Loc.Model F E} {V : Type} [inst_7 : AddCommGroup V]
  [inst_8 : Module E V] (H : Formalism.MainNotions.S.Loc.HermSp M V) {r : ℕ}
  {t₁ t₂ : Formalism.MainNotions.S.Loc.Term V M r} {Λ₂ : Submodule (↥M.L.O) V}
  {ψ : ↥(H.W0 t₁.f t₁.f') ≃ₗ[E] ↥(H.W0 t₂.f t₂.f')}
  {θ : Formalism.L2.SG.LsDatumA.DDt H t₁ ≃ₗ[↥M.L.O] Formalism.L2.SG.LsDatumA.DDt H t₂} {φ : H.Wb t₁.f ≃ₗ[E] H.Wb t₂.f}
  {φ' : H.Wb t₁.f' ≃ₗ[E] H.Wb t₂.f'},
  Formalism.L2.SG.LsDatumA.RGHyp H t₁ t₂ Λ₂ ψ θ φ φ' →
    ∀ {u₁ : V},
      u₁ ∈ Submodule.span E (Set.range (Sum.elim t₁.f t₁.f')) →
        ∀ (hu₁p : u₁ ∈ H.perp (H.X t₁.f)) (n : ↥(H.W0 t₁.f t₁.f')) (hx₁ : u₁ + ↑n ∈ H.perp (H.X t₁.f)) {a b : V},
          a ∈ Submodule.span E (Set.range (Sum.elim t₂.f t₂.f')) →
            b ∈ H.W0 t₂.f t₂.f' →
              ∀ (hap : a ∈ H.perp (H.X t₂.f)) (hx₂ : a + b ∈ H.perp (H.X t₂.f)),
                φ ((H.mkW t₁.f) ⟨u₁ + ↑n, hx₁⟩) = (H.mkW t₂.f) ⟨a + b, hx₂⟩ →
                  b = ↑(ψ n) ∧ φ ((H.mkW t₁.f) ⟨u₁, hu₁p⟩) = (H.mkW t₂.f) ⟨a, hap⟩
@Formalism.L2.SG.LsDatumA.RGHyp.trF._abel_1_1 : ∀ {F : Type} [inst : Field F] [inst_1 : ValuativeRel F]
  [inst_2 : TopologicalSpace F] {E : Type} [inst_3 : CommRing E] [inst_4 : Algebra F E] [inst_5 : TopologicalSpace E]
  [inst_6 : MeasurableSpace E] {M : Formalism.MainNotions.S.Loc.Model F E} {V : Type} [inst_7 : AddCommGroup V]
  [inst_8 : Module E V] (H : Formalism.MainNotions.S.Loc.HermSp M V) {r : ℕ}
  {t₁ t₂ : Formalism.MainNotions.S.Loc.Term V M r} {ψ : ↥(H.W0 t₁.f t₁.f') ≃ₗ[E] ↥(H.W0 t₂.f t₂.f')}
  (n : ↥(H.W0 t₁.f t₁.f')) {a b : V} (u' : V), ↑(ψ n) - b = u' + ↑(ψ n) - (a + b) - (u' - a)
```

`steps_holds` has a one-word statement, `Steps`, a named proposition defined elsewhere in the archive; what it says
is behind that definition, which this cycle did not unfold.

## Predictions registered before the run

| | prediction | outcome |
|---|---|---|
| P1 | 25 to 120 constants dominate at least 1% | held: 81 |
| P2 | zero closets by location | held: 0 |
| P3 | the five largest joints are under Development/AutomorphicArithmetic, each at most 200 own lines | held: 4, 2, 25, 2, 21 own lines |
| P4 | the spine leaves AutomorphicArithmetic only below 1%, and ends in Formalism/ or GroundTheory/ | **missed** on the first half: it leaves at step 13 into AbelianVarietyTheory at 1.72%; the second half held (ends in Formalism/LocalToGlobal) |
| P5 | analysis under 15 min and 60 GB; statements under 3 min | held: 1 m 43 s, 2.7 GB; 53 s, 54.9 GB |
| P6 | some constant with at most 50 own lines joins at least 5%, the largest on the structure trace's spine | held: `every_character_of_literature_of_vWin`, 4 own lines, joins 27.23%, spine step 5 |

## What this does and does not say

A short hinge can be a deep idea or a renaming; the dominator tree cannot tell them apart, and neither can a line
count. What the tree says is where the text sits: in ten large directories, joined by short theorems whose
hypothesis lists are the route. If there was an unexpected step in how this proof was found, it is not a small lemma
in a small place. It would have to be in the choice of which wings to join, which is visible in the statements of the
three largest joints and nowhere else in the archive, or in the attempts that were not published, which are not in
the archive at all. The abelian-variety theory, 47% of the text, is reached from many directions and dominated by
nothing in itself.

## Procedure notes

The analysis ran in the VM on the walk's tables (nodes.tsv 198 MB, edges.tsv 11.4 GB; hashes checked against
`trace-structure/trace-structure.sha256` before the run), with `trace-closet/closet.py`, which reuses the loading and
dominator code of the structure trace's `analyze2.py` unchanged. Thresholds (1%, 2%, 0.5%, 50 lines) were fixed in
the registration. Main.lean and Supplements/Kernels are excluded from the closet count by name, as registered, since
they are the 16-line wrapper file; they appear in every table. The statement run used `lake env lean` in the cycle 2
build directory, as the structure trace's R5 did. Nothing changed standing.
