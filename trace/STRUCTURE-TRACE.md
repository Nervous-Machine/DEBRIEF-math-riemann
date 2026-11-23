# Where the work sits: a structure map of Alpöge's Lean development below `riemannHypothesis`

**For:** anyone who wants to know, before opening a 17-million-line archive, which parts of it the kernel actually
uses for the main theorem, where the proof forks, and which lemmas everything else exists to prove.

**What this is.** Numbers computed from the built environment of cycle 2 (archive sha256 `9631b4f0…`, Lean v4.33.1,
Mathlib `0df444a3`), under the pre-registration `prereg_trace_structure.yaml` (hash in the file beside it,
committed before the walk ran). A dependency walk visited every constant named in the type or proof term of every
archive constant reachable from the five entry theorems of `Main.lean`; the tables below are set sizes, line counts
and dominator relations on that graph. Nothing here is a reading of the mathematics. Where this page offers a
one-line reading of a lemma's name or statement it says so, and the reading is the operating agent's (Claude Fable
5.1, for Nervous Machine, 23 November 2026). Nothing here changes standing.

**Occasion.** On 23 November Yochay Jerby wrote in public that the proof is correct but that "almost all of it goes
into proving an inequality about weighted sums over primes. Once the resulting bound is in hand, a short analytic
argument puts the zeros on the critical line." That is a claim about shape. Shape can be measured.

**Files.** `trace-structure/`: `DepCone.lean` (the walk), `analyze2.py` (the analysis), `report.md` (its full
output), `per_directory.tsv`, `per_directory2.tsv`, `dominators.tsv` (top 5,000), `spine.txt`,
`R5_statements.txt` (verbatim statements), the walk's logs, and `trace-structure.sha256` (hashes of everything
including the 198 MB node table and the 11.4 GB edge table, which stay in the VM and are available on request).

---

## 1. The whole archive, and how much of it the proof uses

| measure | value |
|---|---|
| constants reachable from `riemannHypothesis` inside the archive | 1,265,256 (of 1,265,279 reachable from all five entry theorems) |
| of which theorems / definitions / inductive types, constructors, recursors | 1,075,015 / 178,298 / 11,943 |
| of which auxiliary, machine-named (`_proof_n`, `match_n`, …) | 325,390 |
| source lines inside those constants' declarations | 10,611,120 of 17,374,215 (61.1%) |
| modules (files) touched | 146,437 of 175,187 (83.6%) |
| lines of the files touched | 15,027,754 of 17,374,215 (86.5%) |
| Mathlib and Lean constants named directly by archive constants | 67,981 (Mathlib 64,874; Init 3,040; Batteries 66; Aesop 1) |

The proof term reaches almost everything. Of 331 second-level directories, 23 contribute no constant at all, and
together they hold 8,101 lines, 0.05% of the archive (twelve small `Formalism/` directories, ten single-file
`Lemmata/` directories, `CompanionTheory/EightfoldTheory` with 9 lines). The rest is used, in proportions that vary
little by subject:

| directory | files | lines | share of lines in touched files | constants used |
|---|---|---|---|---|
| Development/AbelianVarietyTheory | 99,187 | 8,142,960 | 83.5% | 524,931 |
| Development/AutomorphicArithmetic | 18,431 | 1,776,375 | 92.1% | 128,661 |
| Development/AutomorphicSpectrum | 15,147 | 1,195,844 | 88.9% | 82,867 |
| Development/WeilBound | 7,051 | 848,547 | 96.6% | 80,531 |
| Development/ResolutionOfSingularities | 499 | 140,709 | 100.0% | 10,308 |
| Development/EtaleCohomology | 1,398 | 104,525 | 94.6% | 13,825 |
| Development/DiscreteGroups | 215 | 23,703 | 57.7% | 1,186 |
| Formalism (111 directories) | 18,254 | 3,200,748 | 87.8% | 278,273 |
| GroundTheory (12 directories) | 8,507 | 1,119,138 | 78.9% | 76,752 |
| ReciprocityTheory (26 directories) | 3,845 | 563,016 | 93.6% | 47,612 |
| CompanionTheory (6 directories) | 2,027 | 194,218 | 95.5% | 15,717 |
| PositivityTheory | 449 | 55,130 | 77.6% | 4,276 |
| Lemmata | 167 | 9,232 | 95.0% | 314 |

Least used among directories of any size: `ReciprocityTheory/Chebotarev` (7.0% of 4,382 lines),
`GroundTheory/Brauer` (27.8% of 4,723), `GroundTheory/PAdicHodge` (39.7% of 64,317), `Formalism/WachLatticeTwists`
(40.3% of 38,367). The full table is `trace-structure/per_directory2.tsv`.

**What this does and does not say about the Nielsen dispute.** The dispute (cycle `external-2026-11-22-nielsen`)
holds that the archive's geometric layer carries no content. The proof term reaches 83.5% of the lines of
`AbelianVarietyTheory` and 524,931 of its constants. Reaching a constant is not the same as depending on its
content: a lemma can be in the cone and still have a hypothesis slot filled with `True`. This map answers "which
parts does the kernel touch", not "which hypotheses do work". The second question is still open (EG2, EG3).

## 2. The fork at the top

`Main.lean` proves `riemannHypothesis` as `Formalism.VW.rh_of_every allChi`, where `allChi` is the theorem
`UpperTheory.FinalTheorems.everyCharacter : UpperTheory.EveryCharacter`, and

```lean
def UpperTheory.EveryCharacter : Prop :=
  ∀ (N : ℕ) [NeZero N] (χ : DirichletCharacter ℂ N) (s : ℂ),
    1 / 2 < s.re → (χ ≠ 1 ∨ s ≠ 1) → DirichletCharacter.LFunction χ s ≠ 0
```

that is: no Dirichlet L-function vanishes to the right of the critical line. Measured:

| set | archive constants | declaration lines | share of the cone's lines |
|---|---|---|---|
| cone(`riemannHypothesis`) | 1,265,256 | 10,611,120 | 100% |
| cone(`everyCharacter`) | 1,265,249 | 10,611,055 | 100.00% |
| cone(`rh_of_every`), the derivation of RH from it | 6 | 64 | 0.00% |
| the two overlap in | 2 (the definition `EveryCharacter` and one part) | | |
| wrappers outside both (`allChi`, `rhOfAll`, `riemannHypothesis`) | 3 | 3 | |

The 64 lines under `rh_of_every` are `Formalism.VW.rh_of_right` (Mathlib only: the functional equation moves a zero
with real part below one half to one with real part above it) and `rh_of_every` itself (specialise `EveryCharacter`
to the trivial character modulo 1). Jerby's description of the top of the proof is exact: the whole archive proves
nonvanishing right of the line; a short analytic argument finishes.

## 3. Below the fork: where the mass goes

For every constant in the cone, its **dominated lines** are the declaration lines of the constants that can only be
reached from the root through it, that is, the part of the archive that exists to prove it and nothing else.
The dominator iteration converged in three passes; the root dominates 10,660,526 lines (distinct declaration ranges,
each counted once; the union-of-ranges figure above merges overlapping ranges and is slightly smaller).

**The spine**, following at each step the child that dominates the most lines:

| step | constant | directory | dominates | leaves the spine here |
|---|---|---|---|---|
| 3 | `UpperTheory.FinalTheorems.everyCharacter` | AutomorphicArithmetic/CharacterBoxes | 100% | 2,406,411 lines into 58,064 children |
| 4 | `UpperTheory.FinalTheorems.everyCharacter_of_row` | same | 77.4% | 1,130,994 |
| 5 | `UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin` | AutomorphicArithmetic/ThetaCorrespondence/…/ThirdPlaceSeries | 66.8% | 2,903,305 |
| 6 | `UpperTheory.Lit.every_character_of_theta_integrals_local_matching` | same | 39.6% | 670,011 |
| 7 | `UpperTheory.Lit.nonempty_hyps_definite_side_of_closed_bound` | same | 33.3% | 2,340,948 |
| 8 | `GlobalTheory.Fc.S0.StageU.hypotheses_nonempty_of_unramified_exponents_alt` | same | 11.3% | 757,399 |
| 9 | `GlobalTheory.Fc.AllAtMemberStage0.allRows_of_open0_alt` | same | 4.2% | (next child under 2%) |

There is no second bottleneck. Below `everyCharacter` the mass divides at every step, and no constant other than
the four wrappers at the top dominates more than 77% of the lines. The largest dominators off the spine:

| constant | directory | dominates |
|---|---|---|
| `UpperTheory.One.vwin_of_row` | AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/ThresholdArguments | 8.6% |
| `SelfIntersectionVolumeEstimates.topCovolSlim2_use_alt_alt` | AutomorphicArithmetic/ThetaCorrespondence/…/ThirdPlaceSeries | 7.7% |
| `UpperTheory.Gal.Int.galoisLocalGlobalStrong_recParameter` | AutomorphicArithmetic/Foundations/GaloisRepresentations | 6.4% |
| `UpperTheory.Gal.Int.galoisRepresentations_of_thetaLift` | same | 6.1% |
| `UpperTheory.Gal.Int.Geo.geoOne_holds` | same, GeometricFlagBases | 5.3% |
| `PositivityTheory.HtPt.Ah.deep_slim_use` | WeilBound/CoreStatements/AutomorphicKernels/MoriwakiBigness/HilbertSamuelApplications | 4.6% |
| `GlobalTheory.CompanionTheory.Ar.Link.good_tower_volume_theorem_bis` | same | 3.3% |
| `GlobalTheory.T.final_theorem_of_inputs_right` | AutomorphicSpectrum/Proofs/GeometryProofs | 3.3% |

The top 40 are in `trace-structure/report.md`; the top 5,000 in `trace-structure/dominators.tsv`.

**A reading, labelled as such.** The names on the spine and among the large dominators speak of the theta
correspondence, Siegel–Eisenstein series, Galois representations and their local-global compatibility, Moriwaki
bigness and Hilbert–Samuel estimates, tower volumes. None of them is named for a sum over primes. That does not
decide what Jerby means: a weighted prime-sum inequality could be the content of a lemma with an automorphic name,
or could be his summary of the claimant's note rather than of the archive. What the map decides is narrower: at the
level of the formal dependency graph there is one hinge, `everyCharacter`, and below it the work is spread, not
concentrated in a second inequality. The statements of the spine and of the ten largest dominators off it follow,
verbatim, so a reader can judge what they say.

## 4. The statements, verbatim

Printed with `#check`, `pp.proofs false`, in the built environment (`trace-structure/R5_statements.lean`, output `R5_statements.txt`, 55 s, 54.9 GB). The spine first, then the ten largest dominators off it. Two things a reader will notice without any help: the hypotheses named `GlobalTheory.Published.*` (Artin reciprocity, Casselman–Wallach, discrete-series classification, Siegel toroidal integrals, …) are literature statements taken as inputs by the lemmas that carry them, and discharged somewhere above, since `everyCharacter` has no hypotheses and rests on Lean's three axioms only (cycle 2, R5); and the name `GlobalTheory.Mem.Top.Bl.anyGeometry`, which the Nielsen dispute cites, appears in the statement of the step-8 spine constant. Neither observation is a reading; both are places to start one.

```lean
riemannHypothesis : RiemannHypothesis
rhOfAll : RiemannHypothesis
allChi : UpperTheory.EveryCharacter
UpperTheory.FinalTheorems.everyCharacter : UpperTheory.EveryCharacter
UpperTheory.FinalTheorems.everyCharacter_of_row : (UpperTheory.GalStar.Row0b
    fun {E Ω} [Field E] [NumberField E] [Field Ω] [Algebra E Ω] [IsAlgClosure E Ω] {A} {w} h rc =>
    UpperTheory.Zero.LLC.IsRecT h rc) →
  UpperTheory.EveryCharacter
UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin : UpperTheory.LiteratureTheorems.OpenLiteratureStatements →
  UpperTheory.Top.VWin → UpperTheory.EveryCharacter
UpperTheory.Lit.every_character_of_theta_integrals_local_matching : GlobalTheory.Fc.S0.UnitaryGroupThirdPlaceHypotheses →
  GlobalTheory.FunPr.ThetaLocalInputs →
    GlobalTheory.IndefiniteRowSideFullHecke.WeilTensorModels.ThetaIntegralsAgree →
      GlobalTheory.IndefiniteRowSideFullHecke.WeilTensorModels.LocalMatching →
        GlobalTheory.CovTop.CovolumeBoundOfX →
          UpperTheory.Zero.LLC.RecTExists → UpperTheory.Top.VWin → UpperTheory.EveryCharacter
UpperTheory.Lit.nonempty_hyps_definite_side_of_closed_bound : GlobalTheory.Fc.S0.UnitaryGroupThirdPlaceHypotheses →
  GlobalTheory.FunPr.ThetaLocalInputs →
    GlobalTheory.IndefiniteRowSideFullHecke.WeilTensorModels.ThetaIntegralsAgree →
      GlobalTheory.IndefiniteRowSideFullHecke.WeilTensorModels.LocalMatching →
        GlobalTheory.CovTop.CovolumeBoundOfX →
          ∀ (hL : UpperTheory.Zero.LLC.RecTExists),
            (∀ (cDep : ℝ),
                GlobalTheory.Fc.RL.LinkedAt (GlobalTheory.Mem.Top.Bl.parametersOfDependence hL cDep) fun Q L =>
                  GlobalTheory.Fc.R1.SlotNormCondition Q L fun 𝒞 =>
                    Formalism.MainNotions.Closed (fun {eps} => 𝒞) fun {eps} Fm x =>
                      GlobalTheory.NLink.BoundAtTwoThreeFamilyFonAlt Fm) →
              Nonempty (GlobalTheory.Fc.HypsAlt GlobalTheory.Fc.S0.NL GlobalTheory.Fc.DefiniteSideCondition)
GlobalTheory.Fc.S0.StageU.hypotheses_nonempty_of_unramified_exponents_alt : GlobalTheory.Fc.S0.UnitaryGroupThirdPlaceHypotheses →
  GlobalTheory.Fc.S0.RowRat →
    ∀ (hL : UpperTheory.Zero.LLC.RecTExists) (cDep : ℝ) (A : GlobalTheory.Mem.Top.GroupRetwisting.AtP),
      GlobalTheory.Mem.Top.EvLgG A →
        (GlobalTheory.Fc.RL.LinkedAt (GlobalTheory.Mem.Top.Bl.parametersOfDependence hL cDep) fun Q L =>
            GlobalTheory.Fc.R1.SlotNormCondition Q L fun 𝒞 =>
              Formalism.MainNotions.Closed (fun {eps} => 𝒞) fun {eps} Fm x =>
                GlobalTheory.NLink.BoundAtTwoThreeFamilyFonAlt Fm) →
          GlobalTheory.Fc.RL.LinkedAt
              (GlobalTheory.Mem.Top.Bl.parametersOfExtension
                (GlobalTheory.Mem.LiteralAutomorphy.extensionWithAtProperty hL
                  (GlobalTheory.HeightCounting.Up.extensionWithOrigin hL cDep) A)
                GlobalTheory.Mem.Top.Bl.SExt.none (GlobalTheory.Mem.Top.Bl.geoCl GlobalTheory.Mem.Top.Bl.anyGeometry))
              GlobalTheory.Fc.S0.FunctionalCondition →
            GlobalTheory.Fc.RL.LinkedAt
                (GlobalTheory.Mem.Top.Bl.parametersOfExtension
                  (GlobalTheory.Mem.LiteralAutomorphy.extensionWithAtProperty hL
                    (GlobalTheory.HeightCounting.Up.extensionWithOrigin hL cDep) A)
                  GlobalTheory.Mem.Top.Bl.SExt.none (GlobalTheory.Mem.Top.Bl.geoCl GlobalTheory.Mem.Top.Bl.anyGeometry))
                GlobalTheory.Fc.S0.CovolumeBoundThirdPlaceSeries →
              Nonempty (GlobalTheory.Fc.HypsAlt GlobalTheory.Fc.S0.NL GlobalTheory.Fc.DefiniteSideCondition)
GlobalTheory.Fc.AllAtMemberStage0.allRows_of_open0_alt : GlobalTheory.Published.GlobalArtinReciprocity →
  HeckeCharacterZeroLocus.SiegelWeilU.SiegelWeilUnitaryConvergent →
    GlobalTheory.Published.DiscreteSeriesCover →
      GlobalTheory.Published.HarishChandraModules →
        GlobalTheory.Published.CuspRapidDecay →
          GlobalTheory.Published.CasselmanWallach →
            GlobalTheory.Published.DiscreteSeriesClassification →
              GlobalTheory.BigOn.SurjectiveOntoX →
                GlobalTheory.BigTop.LambdaLowerBound₂ →
                  ∀ (hL : UpperTheory.Zero.LLC.RecTExists) (N : GlobalTheory.Mem.Top.Bl.NormChoiceExtension hL)
                    (S : GlobalTheory.Mem.Top.Bl.SExt) (Γ : GlobalTheory.Mem.Top.Bl.GeoP)
                    (NN : Formalism.MainNotions.FamClass → Prop),
                    GlobalTheory.Fc.S0.OpenParameterStatements (GlobalTheory.Mem.Top.Bl.parametersOfExtension N S Γ) →
                      GlobalTheory.Fc.RL.LinkedAt (GlobalTheory.Mem.Top.Bl.parametersOfExtension N S Γ)
                          GlobalTheory.Fc.S0.CovolumeBoundThirdPlaceSeries →
                        GlobalTheory.Fc.RL.LinkedAt (GlobalTheory.Mem.Top.Bl.parametersOfExtension N S Γ)
                            GlobalTheory.Fc.S0.FunctionalCondition →
                          (GlobalTheory.Fc.RL.LinkedAt (GlobalTheory.Mem.Top.Bl.parametersOfExtension N S Γ) fun Q L =>
                              GlobalTheory.Fc.R1.SlotNormCondition Q L NN) →
                            GlobalTheory.Fc.AllRowsAlt GlobalTheory.Mem.Top.Bl.KPx
                              (GlobalTheory.Mem.Top.Bl.IsBuiltE (GlobalTheory.Mem.Top.Bl.parametersOfExtension N S Γ).s)
                              (GlobalTheory.Mem.Top.Bl.IsGoodE (GlobalTheory.Mem.Top.Bl.parametersOfExtension N S Γ).s)
                              (GlobalTheory.Mem.Top.Bl.BundleLinkage
                                (GlobalTheory.Mem.Top.Bl.parametersOfExtension N S Γ))
                              NN GlobalTheory.Fc.DefiniteSideCondition
UpperTheory.One.vwin_of_row : (UpperTheory.GalStar.Row0b
    fun {E Ω} [Field E] [NumberField E] [Field Ω] [Algebra E Ω] [IsAlgClosure E Ω] {A} {w} h rc =>
    UpperTheory.Zero.LLC.IsRecT h rc) →
  UpperTheory.Top.VWin
UpperTheory.One.Join.automorphic_window_of_inputs : UpperTheory.LiteratureTheorems.OpenImageCondition →
  PositivityTheory.Rg.BcN.BaseChangeIsobaricN → UpperTheory.V.Z.Win.RowT → UpperTheory.Top.VWin
UpperTheory.One.Join.v_window_of_depth_zero_residual_bc_cm : UpperTheory.LiteratureTheorems.OpenImageCondition →
  PositivityTheory.Rg.BcN.BaseChangeIsobaricN →
    UpperTheory.V.Z.Win.RowT → GlobalTheory.Mem.LiteralAutomorphy.LiteratureCMHypothesis → UpperTheory.Top.VWin
UpperTheory.V.v_window_of_literal_automorphy_n : GlobalTheory.Mem.LiteralAutomorphy.LiteratureRankNHypothesis →
  UpperTheory.Top.VWin
UpperTheory.V.HV.DescentVanishingReductions.v_window_of_automorphy_csd_ss_mono_odd : GlobalTheory.Mem.LiteralAutomorphy.LiteratureRankNHypothesis →
  UpperTheory.Top.VWin
SelfIntersectionVolumeEstimates.topCovolSlim2_use_alt_alt : GlobalTheory.CompanionTheory.Hypotheses₂.ResolutionCharZero →
  GlobalTheory.CompanionTheory.Hypotheses₂.PrincipalisationCharZero →
    GlobalTheory.CompanionTheory.Hypotheses₂.PoincareLelongInv →
      PositivityTheory.MbHsUse.HSUse →
        ReciprocityTheory.ChartRestriction.G.ArakelovGeometry.MoriwakiBigStatement →
          GlobalTheory.CompanionTheory.Ar.HT.FarguesExact →
            GlobalTheory.CompanionTheory.Ar.GR.ZarhinStatement →
              GlobalTheory.CompanionTheory.Ar.Pub.NefRR →
                GlobalTheory.Published.SiegelToroidalIntegral →
                  GlobalTheory.Published.ToroidalForFanKS →
                    GlobalTheory.Published.SemiAbelianLieSeminegative →
                      GlobalTheory.Published.PointSeparationPair →
                        GlobalTheory.Published.ArDegree →
                          GlobalTheory.CovTop.PublishedHodgeBundleTheorems →
                            GlobalTheory.Published.GrothendieckDeformation → GlobalTheory.CovTop.CovolumeBoundOfX
UpperTheory.V.HV.DescentVanishingReductions.vwin_of_hypotheses_H_E_alt : UpperTheory.V.Af.HypothesesH' →
  UpperTheory.Top.VWin
UpperTheory.Gal.Int.galoisLocalGlobalStrong_recParameter : UpperTheory.GalStar.Row0b
  fun {E Ω} [Field E] [NumberField E] [Field Ω] [Algebra E Ω] [IsAlgClosure E Ω] {A} {w} => UpperTheory.Gal.Int.recT
UpperTheory.Gal.Int.galoisRepresentations_of_thetaLift : UpperTheory.TP.TLiftK →
  UpperTheory.GalStar.Row0b fun {E Ω} [Field E] [NumberField E] [Field Ω] [Algebra E Ω] [IsAlgClosure E Ω] {A} {w} =>
    UpperTheory.Gal.Int.recT
UpperTheory.Gal.Int.Geo.geoOne_holds : UpperTheory.Gal.Int.Geo.GeoOne
```

## 5. Predictions registered before the walk, and how they fared

| prediction | outcome |
|---|---|
| P1: cone(`everyCharacter`) ≥ 95% of the cone's lines; cone(`rh_of_every`) minus it < 1% | held: 100.00% and 0.00% |
| P2: touched modules hold 25% to 75% of the archive's lines; some top-level directory under 10% | missed: 86.5%; the only directory under 10% is `BuildAid`, 20 lines |
| P3: at least one Development/ and at least three Formalism/ second-level directories unused | missed: all seven Development/ directories are used; twelve Formalism/ ones are not |
| P4: the deepest spine constant still dominating ≥ 50% is in Development/ | held: step 5, 66.8%, `Development/AutomorphicArithmetic/ThetaCorrespondence` |
| P5: walk under 3 hours and 90 GB; cone between 200,000 and 3,000,000 constants | missed on time: 4 h 18 m 37 s; 83.7 GB; 1,265,256 constants |
| P6: 5,000 to 60,000 library constants at the boundary | missed: 67,981 |

Two of six held. The misses all run the same direction: the proof uses more of the archive, and more of Mathlib,
than I expected, and walking it takes longer.

## 6. Procedure notes

- The walk ran in the VM on cycle 2's build, 2026-11-23 14:26 to 18:44 UTC, one core, 83.7 GB peak; progress lines
  were buffered by the Lean process and appeared only at exit, so the run looked silent while it worked.
- The analysis was registered to run on the host. The edge table is 11.4 GB, so it ran in the VM instead, with
  `analyze2.py`, an integer-indexed rewrite of the registered `analyze.py` with the same measures and outputs; both
  were run on the Mathlib-only test graph and agree. 1 min 46 s, 2.9 GB.
- Declaration lines come from Lean's recorded declaration ranges; 409,544 constants in the cone have none (mostly
  machine-generated parts of other declarations) and contribute no lines. Dominated lines credit each distinct range
  once, to the shortest-named constant carrying it.
- The library boundary counts constants named directly by archive constants; Mathlib's own dependency cone below
  them was not walked.
