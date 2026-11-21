#!/bin/bash
# DEBRIEF-math-riemann cycle 2: resume the lake build of the pinned archive, pruning per-module setup.json files
# (Lake writes one per module, ~6 MB each, never needed once the module is built; Deicyde/riemann-hypothesis notes).
set -u
P=~/untrusted/alpoge-rh; OUT=$P/cycle2; mkdir -p $OUT
cd $P/src/lean || exit 1
{ echo "started $(date -u +%FT%TZ)"; uname -a; nproc; free -g | head -2; df -h / | tail -1; lake --version; cat lean-toolchain; } > $OUT/env.txt 2>&1
echo "R1 archive sha256: $(sha256sum $P/lean.tar.gz)" > $OUT/R1.txt
echo "built .olean before resume: $(find .lake/build/lib/lean -name "*.olean" | wc -l)" >> $OUT/R1.txt
# pruner: delete a module setup.json once its .trace is newer (module finished)
( while sleep 120; do
    find .lake/build/ir -name "*.setup.json" 2>/dev/null | while IFS= read -r f; do
      t=".lake/build/lib/lean/${f#.lake/build/ir/}"; [ "${t%.setup.json}.trace" -nt "$f" ] && rm -f "$f"; done
    echo "$(date -u +%T) $(df -h / | tail -1 | awk "{print \$3, \$4}") oleans $(find .lake/build/lib/lean -name "*.olean" | wc -l)" >> $OUT/progress.log
  done ) & PR=$!
/usr/bin/time -v lake build > $OUT/R3_build.log 2>&1; echo "R3 exit $?" >> $OUT/env.txt
kill $PR 2>/dev/null
find .lake/build/ir -name "*.setup.json" -delete 2>/dev/null
echo "finished $(date -u +%FT%TZ)" >> $OUT/env.txt; df -h / | tail -1 >> $OUT/env.txt
touch $OUT/DONE
