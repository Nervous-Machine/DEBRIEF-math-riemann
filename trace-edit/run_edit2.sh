#!/bin/sh
# Amendment A1 of the edited-archive trace: the walk, the spot checks and the analysis again, on the clone and the cache
# that the first run put in place (steps 1 to 3 of run_edit.sh stand as recorded). The graph is written with integer
# ids. usage: sh run_edit2.sh
set -u
B=~/untrusted/alpoge-rh/edit; S=~/nm-scripts; mkdir -p "$B/graph" "$B/out" "$B/spot"
T() { date -u +%Y-%m-%dT%H:%M:%SZ; }
echo "A1 start $(T)" >> "$B/started.txt"; df -B1 --output=avail ~ | tail -1 > "$B/disk_A1_start.txt"
cd "$B/repo" || exit 1
rm -f "$B/spot_results.tsv"; mv "$B/spot" "$B/spot_run1" 2>/dev/null; mkdir -p "$B/spot"
# 4. the graph, from the module table
echo "walk start $(T)" >> "$B/started.txt"
cp "$S/ArchiveGraph.lean" ./ArchiveGraph.lean && /usr/bin/time -v lake env lean ArchiveGraph.lean > "$B/walk_out.txt" 2> "$B/walk_err.txt"; echo "walk exit $?" >> "$B/walk_out.txt"
echo "walk end $(T)" >> "$B/started.txt"
# 5. spot check: 20 random archive modules recompiled from source, compared with the cached olean
find src -name '*.lean' | sort | python3 -I -c "import sys,random;random.seed(20261125);L=[l.strip() for l in sys.stdin];print('\n'.join(random.sample(L,20)))" > "$B/spot_list.txt"
cp "$S/SpotCheck.lean" ./SpotCheck.lean
while read -r f; do
  m=$(echo "${f#src/}" | sed 's/\.lean$//' | tr '/' '.'); o=".lake/build/lib/lean/${f#src/}"; o="${o%.lean}.olean"; n="$B/spot/$(echo "$m").olean"
  timeout 1800 lake env lean -o "$n" "$f" > "$B/spot/$m.log" 2>&1; e=$?
  if [ -f "$n" ] && [ -f "$o" ]; then r=$(lake env lean --run SpotCheck.lean "$o" "$n" 2>&1 | tail -1); else r="no olean from the recompile (cached one present: $([ -f "$o" ] && echo yes || echo no))"; fi
  echo "$m	compile_exit $e	$r" >> "$B/spot_results.tsv"
done < "$B/spot_list.txt"
# 6. the measures
echo "analysis start $(T)" >> "$B/started.txt"
/usr/bin/time -v python3 -I "$S/edit.py" "$B/graph" "$B/out" "$S/mathlib_shapes.tsv" > "$B/analysis_log.txt" 2> "$B/analysis_err.txt"; echo "analysis exit $?" >> "$B/analysis_log.txt"
echo "end $(T)" >> "$B/started.txt"; df -B1 --output=avail ~ | tail -1 > "$B/disk_end.txt"
cd "$B" && sha256sum head.txt original_head.txt toolchain.txt manifest_revs.txt P0_diff.txt spot_results.tsv graph/nodes.tsv graph/edges.tsv out/*.tsv out/report.md > "$B/outputs.sha256" 2>/dev/null
echo DONE > "$B/DONE"
