#!/bin/bash
# Post-build checks for cycle 2 (R4, R5/R6, R7, R8), run after rh_cycle2.sh wrote DONE. All four run in parallel.
set -u
L=~/untrusted/alpoge-rh/src/lean
C=~/untrusted/alpoge-rh/cycle2
P=/home/heidibennett.guest/untrusted/alpoge-rh/src/lean/src/
cd "$L" || exit 1
echo "post started $(date -u +%FT%TZ)" >> "$C/env.txt"
{ du -sb .lake/build .lake/build/lib/lean .lake/build/ir
  echo "olean $(find .lake/build/lib/lean -name '*.olean' | wc -l)"
  echo "c $(find .lake/build/ir -name '*.c' | wc -l)"
  echo "setup.json $(find .lake/build/ir -name 'setup.json' | wc -l)"
} > "$C/disk.txt" 2>&1

# R7: sha256 of every .olean, in Sutherland's format (./path, C-sorted by path)
( cd .lake/build/lib/lean && find . -name '*.olean' -print0 | LC_ALL=C sort -z | xargs -0 -n 1000 -P 16 sha256sum | LC_ALL=C sort -k2 > "$C/oleans.sha256"; touch "$C/R7_DONE" ) &

# R8: which .olean files contain our absolute source directory as a byte string
( rm -rf /dev/shm/rh2; mkdir -p /dev/shm/rh2/wp && cd .lake/build/lib/lean && find . -name '*.olean' -print0 | xargs -0 -n 500 -P 8 sh -c 'grep -l -F "$0" "$@" > /dev/shm/rh2/wp/$$.txt 2>/dev/null; true' "$P"; cat /dev/shm/rh2/wp/*.txt | LC_ALL=C sort > "$C/with_path.txt"; touch "$C/R8_DONE" ) &

# R4: rescan of the source tree
( cd src && for p in '\bsorry\b' '\badmit\b' 'native_decide' '^\s*(noncomputable\s+|private\s+|protected\s+)*axiom\b' 'implemented_by' '\bextern\b' '\bunsafe\b' '\bopaque\b'; do echo "== pattern: $p"; grep -rnE --include='*.lean' "$p" . ; echo "-- files with hits: $(grep -rlE --include='*.lean' "$p" . | wc -l)"; done > "$C/R4.txt" 2>&1; touch "$C/R4_DONE" ) &

# R5, R6: axiom audit and statement identity in the built environment
( /usr/bin/time -v lake env lean ~/nm-scripts/Audit.lean > "$C/R5R6.txt" 2> "$C/R5R6.err"; echo "audit exit $?" >> "$C/R5R6.err"; touch "$C/R56_DONE" ) &

wait
echo "post finished $(date -u +%FT%TZ)" >> "$C/env.txt"
touch "$C/POST_DONE"
