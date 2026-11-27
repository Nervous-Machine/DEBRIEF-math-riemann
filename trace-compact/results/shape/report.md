# Shape of the compact edition

Graph: 849,098 constants in all, 51,804 in the archive (794 archive modules), 13,922 of them named; 35,883,755 edges, 491,492 inside the archive. Retry marks (no primes) per 1,000 named archive constants: 1.3 (before: 15.4 by the suffix trace's regexes over the whole archive).

Archive constants reached from any of the five entry theorems: 37,569 of 51,804 (72.5%); before: 66% of the archive's constants by the suffix trace.

## `riemannHypothesis`: the archive before, the compact edition, and Mathlib's hundred

| measure | archive before | compact edition | Mathlib Q1 | median | Q3 |
|---|---|---|---|---|---|
| cone constants | 1,265,256 | 37,561 | 30,253 | 36,032 | 46,352 |
| dominated lines | 10,660,526 | 82,826 | 75,408 | 92,248 | 125,716 |
| spine share, step 1 | 100.0% | 100.0% | 8.5% | 19.8% | 38.7% |
| step 2 | 100.0% | 99.2% | 7.0% | 13.5% | 26.4% |
| step 3 | 100.0% | 89.4% | 4.9% | 9.9% | 19.2% |
| step 5 | 66.8% | 19.5% | 3.2% | 6.7% | 13.1% |
| step 8 | 11.3% | 1.9% | 1.4% | 3.2% | 8.4% |
| spine length | 27 | 14 | 20 | 24 | 29 |
| step at which the spine leaves the root's directory | 13 | 1 | 2 | 5 | 10 |
| hinges at 1% | 81 | 40 | 30 | 37 | 46 |
| median own lines of hinges | 4 | 44 | 8 | 10 | 13 |
| longest hinge, lines | 88 | 146 | 90 | 93 | 106 |
| hinges with a retry mark | 32 | 0 | 0 | 0 | 0 |
| hinges with a prime | 1 | 0 | 1 | 2 | 2 |
| largest joint, share joined | 27.2% | 69.8% | 63.9% | 80.2% | 91.5% |
| three largest joints | 71.8% | 88.3% | 93.7% | 96.5% | 98.4% |
| largest directory's share of cone lines | 43.9% | 7.8% | 14.6% | 15.7% | 16.9% |
| largest share any constant in it dominates | 1.7% | 2.3% | 0.5% | 0.9% | 8.9% |
| retry marks per 1,000 named constants | 15.4 | 1.4 | 0.4 | 0.4 | 0.4 |

Largest directory before: Development/AbelianVarietyTheory; now: Lib/Shimura (40 directories in the cone).

## The five entry theorems

| root | cone | lines | spine at 3 | at 5 | hinges | median own | largest joint |
|---|---|---|---|---|---|---|---|
| `riemannHypothesis` | 37,561 | 82,826 | 89.4% | 19.5% | 40 | 44 | 69.8% |
| `riemannZeta_eq_zero_re` | 37,562 | 82,827 | 99.2% | 19.6% | 41 | 42 | 69.8% |
| `LFunction_ne_zero_of_half_lt_re` | 37,558 | 82,817 | 89.4% | 19.5% | 40 | 44 | 69.8% |
| `LFunction_eq_zero_re` | 37,561 | 82,825 | 89.4% | 19.5% | 40 | 44 | 69.7% |
| `LFunction_eq_zero_re_of_isPrimitive` | 37,563 | 82,830 | 99.2% | 19.6% | 41 | 42 | 69.7% |
