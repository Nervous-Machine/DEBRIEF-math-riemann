#!/usr/bin/env python3 -I
"""Generate the R5 Lean file: #check for every name in the given files (spine first, then top dominators not on the spine)."""
import sys
spine = [l.strip() for l in open(sys.argv[1]) if l.strip()]
top = [l.strip() for l in open(sys.argv[2]) if l.strip()]
AUX = ("._proof_", ".proof_", "._eq_", ".match_", "._private")
extra = [n for n in top if n not in spine and not any(a in n for a in AUX)][:10]
out = ["import Main", "set_option pp.proofs false", "set_option pp.maxSteps 100000", "-- R5: statements of the spine constants, then the ten largest dominators off the spine (names chosen by analyze.py)"]
for n in spine: out.append(f"#check @{n}")
out.append("-- off the spine")
for n in extra: out.append(f"#check @{n}")
open(sys.argv[3], "w").write("\n".join(out) + "\n")
print(f"spine {len(spine)} extra {len(extra)} -> {sys.argv[3]}")
