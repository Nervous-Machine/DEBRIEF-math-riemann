# Shape of the edited archive

Graph: 2,239,543 constants in all, 1,416,150 in the archive (59,541 archive modules), 792,261 of them named; 188,279,443 edges, 15,289,382 inside the archive. Retry marks (no primes) per 1,000 named archive constants: 4.4 (before: 15.4 by the suffix trace's regexes over the whole archive).

Archive constants reached from any of the five entry theorems: 1,186,375 of 1,416,150 (83.8%); before: 66% of the archive's constants by the suffix trace.

## `riemannHypothesis`: the archive before, the edited archive, and Mathlib's hundred

| measure | archive before | edited archive | Mathlib Q1 | median | Q3 |
|---|---|---|---|---|---|
| cone constants | 1,265,256 | 1,186,369 | 30,253 | 36,032 | 46,352 |
| dominated lines | 10,660,526 | 10,056,951 | 75,408 | 92,248 | 125,716 |
| spine share, step 1 | 100.0% | 100.0% | 8.5% | 19.8% | 38.7% |
| step 2 | 100.0% | 100.0% | 7.0% | 13.5% | 26.4% |
| step 3 | 100.0% | 76.9% | 4.9% | 9.9% | 19.2% |
| step 5 | 66.8% | 40.5% | 3.2% | 6.7% | 13.1% |
| step 8 | 11.3% | 4.3% | 1.4% | 3.2% | 8.4% |
| spine length | 27 | 26 | 20 | 24 | 29 |
| step at which the spine leaves the root's directory | 13 | 2 | 2 | 5 | 10 |
| hinges at 1% | 81 | 75 | 30 | 37 | 46 |
| median own lines of hinges | 4 | 7 | 8 | 10 | 13 |
| longest hinge, lines | 88 | 88 | 90 | 93 | 106 |
| hinges with a retry mark | 32 | 23 | 0 | 0 | 0 |
| hinges with a prime | 1 | 1 | 1 | 2 | 2 |
| largest joint, share joined | 27.2% | 26.3% | 63.9% | 80.2% | 91.5% |
| three largest joints | 71.8% | 72.1% | 93.7% | 96.5% | 98.4% |
| largest directory's share of cone lines | 43.9% | 41.6% | 14.6% | 15.7% | 16.9% |
| largest share any constant in it dominates | 1.7% | 2.4% | 0.5% | 0.9% | 8.9% |
| retry marks per 1,000 named constants | 15.4 | 4.7 | 0.4 | 0.4 | 0.4 |

Largest directory before: Development/AbelianVarietyTheory; now: Development/AbelianVarietyTheory (297 directories in the cone).

## The five entry theorems

| root | cone | lines | spine at 3 | at 5 | hinges | median own | largest joint |
|---|---|---|---|---|---|---|---|
| `riemannHypothesis` | 1,186,369 | 10,056,951 | 76.9% | 40.5% | 75 | 7 | 26.3% |
| `riemannZeta_eq_zero_re` | 1,186,371 | 10,056,954 | 100.0% | 66.8% | 76 | 7 | 26.3% |
| `LFunction_ne_zero_of_half_lt_re` | 1,186,359 | 10,056,888 | 66.8% | 34.3% | 74 | 7 | 26.3% |
| `LFunction_eq_zero_re` | 1,186,368 | 10,056,942 | 76.9% | 40.5% | 75 | 7 | 26.3% |
| `LFunction_eq_zero_re_of_isPrimitive` | 1,186,370 | 10,056,948 | 100.0% | 66.8% | 76 | 7 | 26.3% |
