#!/bin/sh
# Trace of the compact edition: the graph walk, the shape measures and the name and footprint measures. Runs in the VM
# after cycle 3 has built the compact edition. usage: sh run_compact.sh
set -u
W=~/untrusted/sernau-grh; S=~/nm-scripts; O=$W/trace; mkdir -p "$W/graph" "$O"
export PATH=$HOME/.elan/bin:$PATH
T() { date -u +%Y-%m-%dT%H:%M:%SZ; }
cd "$W/repo/grh-compact" || exit 1
echo "walk start $(T)" >> "$O/started.txt"
cp "$S/CompactGraph.lean" ./CompactGraph.lean && /usr/bin/time -v lake env lean CompactGraph.lean > "$O/walk_out.txt" 2> "$O/walk_err.txt"; echo "walk exit $?" >> "$O/walk_out.txt"
rm -f ./CompactGraph.lean
echo "shape start $(T)" >> "$O/started.txt"
/usr/bin/time -v python3 -I "$S/compact.py" "$W/graph" "$O/shape" "$S/mathlib_shapes.tsv" > "$O/shape_log.txt" 2> "$O/shape_err.txt"; echo "shape exit $?" >> "$O/shape_log.txt"
echo "names start $(T)" >> "$O/started.txt"
/usr/bin/time -v python3 -I "$S/names.py" "$W/graph" ~/untrusted/alpoge-rh/trace-structure/suffix/names_all.tsv ~/untrusted/alpoge-rh/trace-structure/nodes.tsv "$O/names" > "$O/names_log.txt" 2> "$O/names_err.txt"; echo "names exit $?" >> "$O/names_log.txt"
echo "end $(T)" >> "$O/started.txt"
cd "$O" && sha256sum shape/*.tsv shape/report.md names/names.json names/kept_names.txt "$W/graph/nodes.tsv" > "$O/outputs.sha256" 2>/dev/null
echo DONE > "$O/DONE"
