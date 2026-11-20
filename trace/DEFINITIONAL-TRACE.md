# Reading guide: the five statements in `Main.lean` of Alpöge's Lean development (archive sha256 9631b4f0…)

**For:** a number theorist willing to spend half an hour deciding whether the five formal statements say what the
note claims: the Riemann Hypothesis, and the Generalized Riemann Hypothesis.

**What this is.** Each statement verbatim from the archive, every definition it rests on named with its source, a
plain-language reading, and the specific point to confirm or refuse. The readings are the operating agent's (Claude
Fable 5.1, for Nervous Machine, 20 November 2026). They are an aid, not a check. Nothing here changes standing; a
human signature or refusal does, through the **Semantic read** issue form.

**What a build settles and what it does not.** A clean build and axiom audit mean Lean's kernel accepts that these
five statements follow from `propext`, `Classical.choice` and `Quot.sound`. They say nothing about whether the
statements are the Riemann Hypothesis. That is the question on this page.

**Sources, pinned.** `lean/src/Main.lean` and `lean/src/Statements.lean` in the archive (listing sha256 in
`source/listing.sha256`). Mathlib at commit `0df444a360eaa60ab8c11dca51a86af692955474` (tag v4.33.1, 21 August 2026),
file `Mathlib/NumberTheory/LSeries/RiemannZeta.lean` blob `3c92195f`. The claimant's note, `remark.pdf` sha256
`3fc97784…`.

**Time.** Part A, about 10 minutes. Part B, about 20 minutes.

---

## 0. Mathlib conventions a reader has to know

| convention | where | what it means here |
|---|---|---|
| `riemannZeta : ℂ → ℂ` is total | `Mathlib/NumberTheory/LSeries/RiemannZeta.lean` | the completed zeta function's analytic continuation, with a junk value at the pole `s = 1`. Every statement below excludes `s = 1` for that reason. |
| trivial zeros | same file, `riemannZeta_neg_two_mul_nat_add_one` | `riemannZeta (-2 * (n + 1)) = 0` for every natural `n`. The exclusion `¬∃ n : ℕ, s = -2 * (n + 1)` removes exactly these. |
| `(1 : ℂ) / 2` | Lean core | the complex number one half; `s.re = 1 / 2` is the critical line. |
| `DirichletCharacter ℂ N` | `Mathlib/NumberTheory/DirichletCharacter/Basic.lean` | a Dirichlet character modulo `N` with complex values; `1` is the trivial character; `χ.IsPrimitive` is primitivity. |
| `DirichletCharacter.LFunction χ s` | `Mathlib/NumberTheory/LSeries/DirichletContinuation.lean` | the analytic continuation of `L(s, χ)`, total on ℂ; for `χ = 1` it has the pole of zeta at `s = 1`, hence the clause `(χ ≠ 1 ∨ s ≠ 1)` in B2. |
| `[NeZero N]` | Lean core | `N ≠ 0`; the modulus is a positive natural number. |

---

## Part A. The Riemann Hypothesis

### A1. `riemannHypothesis : RiemannHypothesis`

Lean (`Main.lean`, line 4):
```lean
theorem riemannHypothesis : RiemannHypothesis := rhOfAll
```
`RiemannHypothesis` is **not defined in the archive**. It is Mathlib's, verbatim at the pinned commit
(`RiemannZeta.lean`, lines 182–186):
```lean
/-- A formal statement of the **Riemann hypothesis** – constructing a term of this type is worth a
million dollars. -/
@[wikidata Q205966]
def RiemannHypothesis : Prop :=
  ∀ (s : ℂ) (_ : riemannZeta s = 0) (_ : ¬∃ n : ℕ, s = -2 * (n + 1)) (_ : s ≠ 1), s.re = 1 / 2
```
**Reading.** For every complex `s`: if `ζ(s) = 0`, and `s` is not a negative even integer, and `s ≠ 1`, then
`Re s = 1/2`.

**Points to confirm.** (i) `riemannZeta` is the analytic continuation of the Riemann zeta function (Mathlib's docstring
and the lemmas `riemannZeta_eq_tsum_one_div_nat_add_one_cpow` for `Re s > 1`). (ii) The excluded set is exactly the
trivial zeros and the pole. (iii) The statement quantifies over all of ℂ, not only the critical strip; since the Euler
product gives no zeros for `Re s > 1` and the functional equation gives only the trivial zeros for `Re s < 0`, this
is the classical statement. The definition is Mathlib's, written by the Mathlib community, not by the claimant.

### A2. `riemannZeta_eq_zero_re : RiemannZetaZerosOnLine`

Lean (`Statements.lean`, lines 3–4):
```lean
def RiemannZetaZerosOnLine : Prop :=
  ∀ s : ℂ, riemannZeta s = 0 → (¬∃ n : ℕ, s = -2 * ((n : ℂ) + 1)) → s ≠ 1 → s.re = 1 / 2
```
**Reading.** The same statement as A1 with the cast `(n : ℂ)` written out. **Point to confirm.** A2 and A1 are the
same proposition up to the elaboration of the cast.

---

## Part B. "The Generalized Riemann Hypothesis"

The note says the method "easily extends much further, resolving the so-called Generalized Riemann Hypothesis". The
archive's three further statements are all about **Dirichlet L-functions**, that is, Hecke L-functions of ℚ only. They
are the claimant's own definitions in `Statements.lean`; Mathlib has no definition named for GRH. Whether
"Generalized Riemann Hypothesis" in the note means this, or GRH for all number fields, is a question for the claimant;
the record notes the narrower reading as what is formalized.

### B1. `LFunction_eq_zero_re : DirichletLZerosOnLine`

Lean (`Statements.lean`, lines 10–12):
```lean
def DirichletLZerosOnLine : Prop :=
  ∀ (N : ℕ) [NeZero N] (χ : DirichletCharacter ℂ N) (s : ℂ),
    0 < s.re → s.re < 1 → DirichletCharacter.LFunction χ s = 0 → s.re = 1 / 2
```
**Reading.** For every modulus `N ≥ 1`, every Dirichlet character `χ` mod `N` (primitive or not), and every `s` in the
open critical strip: if `L(s, χ) = 0` then `Re s = 1/2`. **Points to confirm.** (i) `DirichletCharacter.LFunction` is
the analytic continuation of `L(s, χ)`. (ii) Imprimitive characters are included; their L-functions differ from the
primitive one by finitely many Euler factors whose zeros lie on `Re s = 0`, outside the open strip, so including them
adds nothing false and nothing missing. (iii) This is GRH for Dirichlet L-functions, restricted to the open strip, which
is the classical form.

### B2. `LFunction_ne_zero_of_half_lt_re : DirichletLNonvanishingRightOfHalf`

Lean (`Statements.lean`, lines 6–8):
```lean
def DirichletLNonvanishingRightOfHalf : Prop :=
  ∀ (N : ℕ) [NeZero N] (χ : DirichletCharacter ℂ N) (s : ℂ),
    1 / 2 < s.re → (χ ≠ 1 ∨ s ≠ 1) → DirichletCharacter.LFunction χ s ≠ 0
```
**Reading.** For every `χ` and every `s` with `Re s > 1/2`, other than the pole of `L(s, 1)` at `s = 1`, `L(s, χ) ≠ 0`.
**Point to confirm.** This is the half-plane form of B1 (non-vanishing strictly right of the line); together with the
functional equation it is equivalent to B1 for primitive characters.

### B3. `LFunction_eq_zero_re_of_isPrimitive : PrimitiveDirichletLZerosOnLine`

Lean (`Statements.lean`, lines 14–16):
```lean
def PrimitiveDirichletLZerosOnLine : Prop :=
  ∀ (N : ℕ) [NeZero N] (χ : DirichletCharacter ℂ N), χ.IsPrimitive →
    ∀ s : ℂ, 0 < s.re → s.re < 1 → DirichletCharacter.LFunction χ s = 0 → s.re = 1 / 2
```
**Reading.** B1 restricted to primitive characters. **Point to confirm.** B3 is a special case of B1.

---

## Discrepancies recorded by the agent

| # | what | affects content? |
|---|---|---|
| D1 | The note says "Generalized Riemann Hypothesis" without qualification; the archive states it for Dirichlet characters only. Hecke L-functions of other number fields are not stated. | yes, for what "GRH" is taken to mean; no, for the Riemann Hypothesis itself |
| D2 | Four of five statements are the claimant's definitions, not a third party's. Their text is short enough to read in full above. | the reader decides |

---

## Sign-off checklist

Sign or refuse each item under your own name with the **Semantic read** issue form. A read counts as a signature when
every item not marked optional is signed. A refusal names the item and the reason, and carries the same weight.

- **A1** Mathlib's `RiemannHypothesis` at commit `0df444a3` is the Riemann Hypothesis as posed.
- **A2** `RiemannZetaZerosOnLine` is the same proposition as A1.
- **B1** `DirichletLZerosOnLine` is the Generalized Riemann Hypothesis for Dirichlet L-functions.
- **B2** `DirichletLNonvanishingRightOfHalf` is the half-plane form of B1. *(optional)*
- **B3** `PrimitiveDirichletLZerosOnLine` is a special case of B1. *(optional)*
- **D1** The archive's "GRH" is for Dirichlet L-functions only, and the record should say so. *(optional)*
